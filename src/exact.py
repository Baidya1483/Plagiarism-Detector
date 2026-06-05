def kmp_search(text: str, pat: str) -> list:
    """Searches for exact structural patterns using Knuth-Morris-Pratt failure maps."""
    if not pat or not text:
        return []
    lps = [0] * len(pat)
    j = 0
    
    # Pre-compute the Longest Prefix Suffix (LPS) failure table array
    for i in range(1, len(pat)):
        while j > 0 and pat[i] != pat[j]:
            j = lps[j - 1]
        if pat[i] == pat[j]:
            j += 1
            lps[i] = j
            
    matches = []
    j = 0
    for i, ch in enumerate(text):
        while j > 0 and ch != pat[j]:
            j = lps[j - 1]
        if ch == pat[j]:
            j += 1
        if j == len(pat):
            matches.append(i - j + 1)
            j = lps[j - 1]
            
    return matches

def rabin_karp_windows(text: str, ref: str, w=30, base=256, mod=10**9 + 7) -> list:
    """Slides a rolling hash window across input text segments to identify long matches."""
    if len(text) < w or len(ref) < w:
        return []
        
    powp = pow(base, w - 1, mod)
    ref_hashes = {}
    hr = 0
    
    # Compute baseline reference hash values
    for ch in ref[:w]:
        hr = (hr * base + ord(ch)) % mod
    ref_hashes.setdefault(hr, []).append(0)
    
    for i in range(w, len(ref)):
        hr = ((hr - ord(ref[i - w]) * powp) % mod + mod) % mod
        hr = (hr * base + ord(ref[i])) % mod
        ref_hashes.setdefault(hr, []).append(i - w + 1)
        
    matches = []
    h = 0
    for ch in text[:w]:
        h = (h * base + ord(ch)) % mod
        
    if h in ref_hashes:
        for j in ref_hashes[h]:
            if text[:w] == ref[j:j + w]:
                matches.append((0, j))
                
    for i in range(w, len(text)):
        h = ((h - ord(text[i - w]) * powp) % mod + mod) % mod
        h = (h * base + ord(text[i])) % mod
        if h in ref_hashes:
            for j in ref_hashes[h]:
                if text[i - w + 1:i + 1] == ref[j:j + w]:
                    matches.append((i - w + 1, j))
                    
    return matches