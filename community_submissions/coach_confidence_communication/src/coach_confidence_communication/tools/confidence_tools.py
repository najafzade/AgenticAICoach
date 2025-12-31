import json

from crewai_tools import tool

from coach_confidence_communication.analyzer import analyze_text, build_suggestions, format_markers


@tool("confidence_marker_detector")
def confidence_marker_detector(text: str) -> str:
    """Detect low-confidence markers and return structured JSON output."""
    analysis = analyze_text(text)
    payload = {
        "markers": format_markers(analysis.markers),
        "summary": analysis.summary,
        "confidence_score": analysis.confidence_score,
        "confidence_label": analysis.confidence_label,
        "suggestions": build_suggestions(analysis.markers),
    }
    return json.dumps(payload)


@tool("confidence_rewrite_guidance")
def confidence_rewrite_guidance(text: str) -> str:
    """Provide rewritten guidance snippets for confidence improvements."""
    analysis = analyze_text(text)
    if not analysis.markers:
        return "Your message already reads confidently. Consider adding a clear call to action."

    guidance_lines = []
    for marker in analysis.markers:
        guidance_lines.append(
            f"- '{marker.phrase}' → use an active, direct alternative that states the intent upfront."
        )
    return "\n".join(guidance_lines)
