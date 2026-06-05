def coverage_from_matches(matches: list, window_size=30, text_len=0) -> float:
    """Aggregates contiguous exact match spans to determine the absolute text overlap coverage."""
    if text_len == 0:
        return 0.0
    covered = [0] * text_len
    for start, _ in matches:
        for i in range(start, min(start + window_size, text_len)):
            covered[i] = 1
    return sum(covered) / max(1, text_len)

def blended_score(exact_cov: float, winnow_overlap: float, tfidf: float, jaccard_score: float) -> int:
    """Combines metrics from multi-stage search steps to calculate an integrated likelihood score."""
    w1, w2, w3, w4 = 0.4, 0.3, 0.2, 0.1
    aggregated = w1 * exact_cov + w2 * winnow_overlap + w3 * tfidf + w4 * jaccard_score
    return int(100 * min(1.0, aggregated))