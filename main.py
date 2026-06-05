import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.preprocess import normalize
from src.exact import rabin_karp_windows
from src.winnow import winnow_fingerprints, fp_index
from src.lsh import MinHasher, LSH
from src.similarity import ngram_set, tfidf_cosine, jaccard
from src.scoring import coverage_from_matches, blended_score

app = FastAPI(title="Industrial Plagiarism Detection Processing Pipeline")

# Global Cache Core Reference Spaces
CORPUS_RAW = {}
CORPUS_NORM = {}
FINGERPRINT_INDEX = {}

MIN_HASHER = MinHasher(n=100)
LSH_INDEX = LSH(bands=20, rows=5)
SHINGLE_K = 5

class DocumentPayload(BaseModel):
    doc_id: str
    text: str

class AnalysisRequest(BaseModel):
    text: str
    top_k: int = 3

@app.post("/index")
def index_document(payload: DocumentPayload):
    global FINGERPRINT_INDEX
    CORPUS_RAW[payload.doc_id] = payload.text
    
    norm_text, _ = normalize(payload.text)
    CORPUS_NORM[payload.doc_id] = norm_text
    
    # Synchronize winnow inverted index layouts
    FINGERPRINT_INDEX = fp_index(CORPUS_NORM, k=SHINGLE_K, t=9)
    
    tokens = set(norm_text.split())
    sig = MIN_HASHER.signature(tokens)
    LSH_INDEX.add(payload.doc_id, sig)
    
    return {"status": "indexed", "doc_id": payload.doc_id}

@app.post("/analyze")
def analyze_submission(req: AnalysisRequest):
    if not CORPUS_NORM:
        raise HTTPException(status_code=400, detail="Reference corpus database is empty. Index files first.")
        
    sub_norm, _ = normalize(req.text)
    sub_tokens = set(sub_norm.split())
    
    # Query LSH buckets to quickly retrieve candidate matches
    sub_sig = MIN_HASHER.signature(sub_tokens)
    candidates = LSH_INDEX.query(sub_sig)
    
    # Fall back to evaluating all catalog entries if LSH returns zero bucket hits
    if not candidates:
        candidates = list(CORPUS_NORM.keys())
        
    results = []
    sub_ngrams = ngram_set(sub_norm, n=4)
    sub_fp_list = winnow_fingerprints(sub_norm, k=SHINGLE_K, t=9)
    sub_hashes = {h for _, h in sub_fp_list}
    
    for doc_id in candidates[:40]:
        ref_norm = CORPUS_NORM[doc_id]
        
        # Stage 1: Sliding Window Exact Matching Coverage
        rk_matches = rabin_karp_windows(sub_norm, ref_norm, w=30)
        exact_cov = coverage_from_matches(rk_matches, window_size=30, text_len=len(sub_norm))
        
        # Stage 2: Structural Fingerprint Intersection
        ref_fp_list = winnow_fingerprints(ref_norm, k=SHINGLE_K, t=9)
        ref_hashes = {h for _, h in ref_fp_list}
        shared_hashes = sub_hashes & ref_hashes
        winnow_overlap = len(shared_hashes) / max(1, len(sub_hashes | ref_hashes))
        
        # Stage 3: Paraphrase Vector Optimization Metrics
        jacc = jaccard(sub_ngrams, ngram_set(ref_norm, n=4))
        cosine_sim = tfidf_cosine(sub_norm, ref_norm)
        
        score = blended_score(exact_cov, winnow_overlap, cosine_sim, jacc)
        
        results.append({
            "doc_id": doc_id,
            "match_likelihood": score,
            "exact_coverage_ratio": round(exact_cov, 3),
            "winnow_overlap_ratio": round(winnow_overlap, 3),
            "tfidf_cosine_sim": round(cosine_sim, 3)
        })
        
    results.sort(key=lambda x: -x["match_likelihood"])
    top_matches = results[:req.top_k]
    
    overall_average = int(sum(r["match_likelihood"] for r in top_matches) / max(1, len(top_matches)))
    return {"overall_plagiarism_index": overall_average, "suspect_matches": top_matches}