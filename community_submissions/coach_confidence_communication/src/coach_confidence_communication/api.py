from __future__ import annotations

import os
import uuid
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from coach_confidence_communication.analyzer import analyze_text, build_suggestions, format_markers
from coach_confidence_communication.crew import ConfidenceCoachCrew


app = FastAPI(title="AI Confidence Coach", version="0.1.0")

SESSION_STORE: dict[str, list[int]] = {}


class AnalyzeRequest(BaseModel):
    text: str = Field(..., description="User message or transcript to analyze")
    context: str | None = Field(
        default=None,
        description="Optional context like request, feedback, or update.",
    )
    session_id: str | None = Field(default=None, description="Provide to track revisions")


class AnalyzeResponse(BaseModel):
    session_id: str
    confidence_score: int
    confidence_label: str
    summary: dict[str, int]
    markers: list[dict[str, Any]]
    suggestions: list[str]
    progress: dict[str, Any]
    coach_feedback: str | None = None


def _get_session(session_id: str | None) -> str:
    if session_id and session_id in SESSION_STORE:
        return session_id
    new_id = session_id or str(uuid.uuid4())
    SESSION_STORE.setdefault(new_id, [])
    return new_id


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    session_id = _get_session(request.session_id)
    analysis = analyze_text(request.text)
    SESSION_STORE[session_id].append(analysis.confidence_score)
    progress = {
        "revision_count": len(SESSION_STORE[session_id]),
        "scores": SESSION_STORE[session_id],
    }

    use_crewai = os.getenv("USE_CREWAI", "true").lower() == "true"
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    suggestions = build_suggestions(analysis.markers)
    coach_feedback: str | None = None

    if use_crewai and has_key:
        crew = ConfidenceCoachCrew().crew()
        result = crew.kickoff(
            inputs={
                "text": request.text,
                "context": request.context or "general",
            }
        )
        coach_feedback = str(result)
    else:
        coach_feedback = (
            "Warm tip: lead with your main point, then add the request. "
            "You can be polite while staying direct."
        )

    return AnalyzeResponse(
        session_id=session_id,
        confidence_score=analysis.confidence_score,
        confidence_label=analysis.confidence_label,
        summary=analysis.summary,
        markers=format_markers(analysis.markers),
        suggestions=suggestions,
        progress=progress,
        coach_feedback=coach_feedback,
    )


@app.post("/analyze/rule-based", response_model=AnalyzeResponse)
async def analyze_rule_based(request: AnalyzeRequest) -> AnalyzeResponse:
    session_id = _get_session(request.session_id)
    analysis = analyze_text(request.text)
    SESSION_STORE[session_id].append(analysis.confidence_score)
    progress = {
        "revision_count": len(SESSION_STORE[session_id]),
        "scores": SESSION_STORE[session_id],
    }
    suggestions = build_suggestions(analysis.markers)
    coach_feedback = (
        "Consider removing softeners and using active voice. "
        "You can keep a respectful tone while sounding confident."
    )

    return AnalyzeResponse(
        session_id=session_id,
        confidence_score=analysis.confidence_score,
        confidence_label=analysis.confidence_label,
        summary=analysis.summary,
        markers=format_markers(analysis.markers),
        suggestions=suggestions,
        progress=progress,
        coach_feedback=coach_feedback,
    )
