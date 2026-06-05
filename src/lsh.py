import random
import mmh3
import numpy as np

class MinHasher:
    """Encodes categorical text token sets down into static MinHash signature vectors."""
    def __init__(self, n=100, seed=42):
        random.seed(seed)
        self.seeds = [random.randint(1, (1 << 31) - 1) for _ in range(n)]
        
    def signature(self, tokens: set) -> np.ndarray:
        sig = []
        for seed in self.seeds:
            # Set prime boundaries as lookup defaults
            min_val = 2**32 - 1
            if tokens:
                for t in tokens:
                    h = mmh3.hash(t, seed, signed=False)
                    if h < min_val:
                        min_val = h
            sig.append(min_val)
        return np.array(sig, dtype=np.uint32)

class LSH:
    """Buckets document signatures to perform sub-linear candidate lookups across huge corpora."""
    def __init__(self, bands=20, rows=5):
        self.bands = bands
        self.rows = rows
        self.tables = [{} for _ in range(bands)]
        
    def add(self, doc_id: str, sig: np.ndarray):
        for b in range(self.bands):
            band_bytes = sig[b * self.rows:(b + 1) * self.rows].tobytes()
            self.tables[b].setdefault(band_bytes, []).append(doc_id)
            
    def query(self, sig: np.ndarray) -> list:
        candidates = set()
        for b in range(self.bands):
            band_bytes = sig[b * self.rows:(b + 1) * self.rows].tobytes()
            if band_bytes in self.tables[b]:
                candidates.update(self.tables[b][band_bytes])
        return list(candidates)