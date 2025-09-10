FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Poetry and deps
COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry && poetry install --no-interaction --no-ansi

# App code
COPY pointless /app/pointless

EXPOSE 8080
CMD ["poetry", "run", "uvicorn", "pointless.interfaces.api:app", "--host", "0.0.0.0", "--port", "8080"]
