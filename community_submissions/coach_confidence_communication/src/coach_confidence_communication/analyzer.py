from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Iterable


HEDGING_PHRASES = [
    "i just think",
    "i just feel",
    "maybe we could",
    "maybe we should",
    "i guess",
    "kind of",
    "sort of",
    "perhaps",
    "possibly",
]

APOLOGY_PHRASES = [
    "sorry to bother",
    "sorry for",
    "i apologize",
    "apologies",
    "sorry",
]

MINIMIZING_PHRASES = [
    "dumb question",
    "just",
    "just a",
    "just an",
    "only",
    "a bit",
    "tiny",
    "minor",
]

PASSIVE_VOICE_PATTERN = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\b\s+\w+ed\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Marker:
    category: str
    phrase: str
    start: int
    end: int
    suggestion: str


@dataclass(frozen=True)
class AnalysisResult:
    markers: list[Marker]
    confidence_score: int
    summary: dict[str, int]
    confidence_label: str


SUGGESTION_MAP = {
    "hedging": "State the point directly without softeners.",
    "apology": "Skip unnecessary apologies and lead with your request.",
    "minimizing": "Remove minimizing language and own the request.",
    "passive": "Use active voice to show ownership and clarity.",
}


def _find_phrases(text: str, phrases: Iterable[str], category: str) -> list[Marker]:
    markers: list[Marker] = []
    lowered = text.lower()
    for phrase in phrases:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            end = index + len(phrase)
            markers.append(
                Marker(
                    category=category,
                    phrase=text[index:end],
                    start=index,
                    end=end,
                    suggestion=SUGGESTION_MAP[category],
                )
            )
            start = end
    return markers


def _find_passive_voice(text: str) -> list[Marker]:
    markers: list[Marker] = []
    for match in PASSIVE_VOICE_PATTERN.finditer(text):
        markers.append(
            Marker(
                category="passive",
                phrase=match.group(0),
                start=match.start(),
                end=match.end(),
                suggestion=SUGGESTION_MAP["passive"],
            )
        )
    return markers


def _confidence_score(marker_count: int, word_count: int) -> int:
    if word_count == 0:
        return 1
    ratio = marker_count / max(word_count, 1)
    if ratio < 0.02 and marker_count <= 1:
        return 5
    if ratio < 0.04:
        return 4
    if ratio < 0.06:
        return 3
    if ratio < 0.08:
        return 2
    return 1


def analyze_text(text: str) -> AnalysisResult:
    markers: list[Marker] = []
    markers.extend(_find_phrases(text, HEDGING_PHRASES, "hedging"))
    markers.extend(_find_phrases(text, APOLOGY_PHRASES, "apology"))
    markers.extend(_find_phrases(text, MINIMIZING_PHRASES, "minimizing"))
    markers.extend(_find_passive_voice(text))

    word_count = len(re.findall(r"\b\w+\b", text))
    score = _confidence_score(len(markers), word_count)
    summary = {
        "hedging": sum(1 for marker in markers if marker.category == "hedging"),
        "apology": sum(1 for marker in markers if marker.category == "apology"),
        "minimizing": sum(1 for marker in markers if marker.category == "minimizing"),
        "passive": sum(1 for marker in markers if marker.category == "passive"),
    }
    label = {
        1: "Low",
        2: "Cautious",
        3: "Balanced",
        4: "Confident",
        5: "Highly Confident",
    }[score]

    return AnalysisResult(markers=markers, confidence_score=score, summary=summary, confidence_label=label)


def format_markers(markers: Iterable[Marker]) -> list[dict[str, str | int]]:
    return [asdict(marker) for marker in markers]


def build_suggestions(markers: Iterable[Marker]) -> list[str]:
    suggestions = []
    for marker in markers:
        suggestions.append(
            f"Replace '{marker.phrase}' with a direct statement. {marker.suggestion}"
        )
    return suggestions
