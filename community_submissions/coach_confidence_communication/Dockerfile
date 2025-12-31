FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY src /app/src

EXPOSE 8000

CMD ["uvicorn", "coach_confidence_communication.api:app", "--host", "0.0.0.0", "--port", "8000"]
