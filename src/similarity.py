from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def ngram_set(text: str, n=4) -> set:
    tokens = text.split()
    if len(tokens) < n:
        return set([" ".join(tokens)])
    return {" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}

def jaccard(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / max(1, len(set_a | set_b))

def tfidf_cosine(text_a: str, text_b: str) -> float:
    """Calculates vector space similarity matrices across slightly reworded or paraphrased text."""
    if not text_a.strip() or not text_b.strip():
        return 0.0
    vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 2))
    tfidf_matrices = vectorizer.fit_transform([text_a, text_b])
    return float(cosine_similarity(tfidf_matrices[0], tfidf_matrices[1])[0, 0])