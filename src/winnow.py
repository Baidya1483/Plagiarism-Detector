import hashlib
from collections import defaultdict

def shingle_tokens(text: str, k=5):
    """Splits normalized text inputs down into k-word overlapping shingle blocks."""
    tokens = text.split()
    for i in range(len(tokens) - k + 1):
        yield i, " ".join(tokens[i:i + k])

def hash_shingle(shingle: str) -> int:
    return int(hashlib.blake2b(shingle.encode(), digest_size=8).hexdigest(), 16)

def winnow_fingerprints(text: str, k=5, t=9) -> list:
    """Filters shingle hashes down into location-aware structural document fingerprints."""
    w = max(1, t - k + 1)
    hashes = []
    for pos, sh in shingle_tokens(text, k):
        hashes.append((pos, hash_shingle(sh)))
        
    fingerprints = []
    last_min = None
    
    for i in range(len(hashes) - w + 1):
        window = hashes[i:i + w]
        # Robust localized minimum selection rule logic
        mpos, mval = min(window, key=lambda x: x[1])
        if (mpos, mval) != last_min:
            fingerprints.append((mpos, mval))
            last_min = (mpos, mval)
            
    return fingerprints

def fp_index(texts: dict, k=5, t=9) -> defaultdict:
    inv = defaultdict(list)
    for doc_id, txt in texts.items():
        for pos, h in winnow_fingerprints(txt, k=k, t=t):
            inv[h].append((doc_id, pos))
    return inv