# AI Confidence Coach (CrewAI + FastAPI)

This application analyzes communication for low-confidence markers (hedging, apologizing, minimizing language, passive voice) and returns warm, actionable suggestions to strengthen confidence. It also tracks progress across revisions.

## Features
- **Confidence marker detection** with heuristic rules.
- **CrewAI orchestration** with YAML-configured agents and tasks.
- **FastAPI endpoint** for production-ready interaction.
- **Revision tracking** with confidence score history.

## Project Structure
```
community_submissions/coach_confidence_communication/
├── README.md
├── Dockerfile
├── pyproject.toml
├── src/coach_confidence_communication/
│   ├── api.py
│   ├── analyzer.py
│   ├── crew.py
│   ├── main.py
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   └── tools/
│       └── confidence_tools.py
└── tests/
    └── test_analyzer.py
```

## Step-by-Step Setup

### 1) Install dependencies
```bash
cd community_submissions/coach_confidence_communication
poetry install
```

### 2) (Optional) Configure LLM access
CrewAI will use the OpenAI API if you export an API key. Without a key, the API still returns rule-based feedback.
```bash
export OPENAI_API_KEY="your-key"
```

### 3) Run the FastAPI server
```bash
poetry run uvicorn coach_confidence_communication.api:app --host 0.0.0.0 --port 8000
```

### 4) Call the API
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Sorry to bother you, but maybe we could just review this?","context":"request"}'
```

### 5) Submit a revision
Re-submit with the `session_id` from the first response to track progress.
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"session_id":"<session-id>","text":"Please review this update today.","context":"request"}'
```

### 6) Run the CrewAI workflow directly
```bash
poetry run confidence_coach --text "Maybe we could consider an update." --context "status update"
```

## Docker (Optional)
```bash
docker build -t confidence-coach .
docker run -p 8000:8000 -e OPENAI_API_KEY=$OPENAI_API_KEY confidence-coach
```

## Testing
```bash
poetry run pytest
```

## Deployment Notes
- You can deploy the FastAPI app to Render, Railway, or GCP Cloud Run.
- Use `uvicorn coach_confidence_communication.api:app --host 0.0.0.0 --port $PORT` as the start command.
- Ensure `OPENAI_API_KEY` is configured for CrewAI responses in production.

## Demo UI Video
Record a short (under 2 minutes) screen demo of the API in action and attach it to your PR if you want to showcase the coach in the community.
