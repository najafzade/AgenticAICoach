from coach_confidence_communication.analyzer import analyze_text


def test_analyze_text_flags_markers():
    text = "Sorry to bother you, but maybe we could just review this? It was decided yesterday."
    result = analyze_text(text)

    categories = {marker.category for marker in result.markers}
    assert "apology" in categories
    assert "hedging" in categories
    assert "minimizing" in categories
    assert "passive" in categories


def test_confidence_score_improves_with_strong_language():
    weak = "I just think maybe we could consider updating the deck."
    strong = "I recommend updating the deck today."

    weak_score = analyze_text(weak).confidence_score
    strong_score = analyze_text(strong).confidence_score

    assert strong_score >= weak_score
