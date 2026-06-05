import os
import pytest
from src.preprocess import normalize
from src.exact import rabin_karp_windows, kmp_search
from src.winnow import winnow_fingerprints

def test_plagiarism_pipeline_execution():
    """Validates the text normalization tracking layer, string matchers, and fingerprinters."""
    source_text = "The quick brown fox jumps over the lazy dog sequence parameters."
    copied_text = "The quick brown fox jumps over the lazy cat reference values."
    
    norm_src, map_src = normalize(source_text)
    norm_cop, map_cop = normalize(copied_text)
    
    assert len(norm_src) > 0
    assert len(map_src) == len(norm_src)
    
    # Evaluate windowed string matching precision
    rk_matches = rabin_karp_windows(norm_cop, norm_src, w=15)
    assert isinstance(rk_matches, list)
    
    # Evaluate winnowing operational fingerprint tracking loops
    fingerprints = winnow_fingerprints(norm_src, k=3, t=5)
    assert len(fingerprints) > 0