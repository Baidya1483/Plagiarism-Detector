import re
import unicodedata

def normalize(text: str):
    """Strips punctuation, lowercases characters, and maintains a map of character offsets."""
    idx_map = []
    out = []
    
    # Process text character-by-character to retain accurate spatial track matrices
    for i, ch in enumerate(text):
        if ch.isspace():
            ch = " "
        ch = unicodedata.normalize("NFKC", ch)
        if re.match(r"[A-Za-z0-9 ]", ch):
            out.append(ch.lower())
            idx_map.append(i)
            
    # Collapse multiple spaces down to individual single tokens
    raw_str = "".join(out)
    collapsed_str = re.sub(r"\s+", " ", raw_str)
    
    # Synchronize tracking offsets across character collapse boundaries
    final_map = []
    space_count = 0
    i = 0
    while i < len(raw_str):
        if raw_str[i] == " ":
            final_map.append(idx_map[i])
            while i < len(raw_str) and raw_str[i] == " ":
                i += 1
        else:
            final_map.append(idx_map[i])
            i += 1
            
    return collapsed_str.strip(), final_map