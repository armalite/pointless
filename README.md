# pointless

**"Finally, an AI that's as bad at estimating as your team - but way faster!"**

Pointless is the AI buddy that reads your Jira tickets and codebase, then pretends it knows how long it'll take - just like your team, but faster. Perfect for when you need confident-sounding estimates with zero accountability!

## Features

- 🤖 **AI-Powered Estimation**: Uses sophisticated algorithms (random numbers) to estimate task effort
- 📊 **Confidence Metrics**: Provides confidence levels so you know how wrong we might be
- 🏷️ **Complexity Assessment**: Categorizes tasks from "trivial" to "expert" (mostly expert)
- 📝 **Detailed Reasoning**: Explains our wild guesses with pseudo-scientific justification
- 🔄 **Multiple Interfaces**: CLI for developers, REST API for integrations
- 🎯 **Jira Integration Ready**: Supports Jira ticket IDs (because everything is in Jira)

## Installation

```bash
# Install from source
git clone https://github.com/armalite/pointless.git
cd pointless
poetry install

# Or install from PyPI (when published)
pip install pointless
```

## Quick Start

### CLI Usage

```bash
# Basic estimation
pointless estimate "Fix login bug"

# Detailed estimation with context
pointless estimate "Implement OAuth2 authentication" \
  --desc "Add OAuth2 with JWT tokens and refresh mechanism" \
  --jira "AUTH-123" \
  --context "Express.js API with MongoDB" \
  --tag "security" --tag "urgent"

# JSON output for scripts
pointless estimate "Refactor user service" --format json
```

### API Usage

```bash
# Start the API server
uvicorn pointless.interfaces.api:app --reload

# Or use Poetry script
poetry run uvicorn pointless.interfaces.api:app --reload
```

```bash
# Health check
curl http://localhost:8000/healthz

# Create estimation
curl -X POST "http://localhost:8000/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix critical payment bug",
    "description": "Payment processing fails on checkout",
    "jira_ticket_id": "PAY-456",
    "tags": ["urgent", "bug", "payment"]
  }'
```

### Example Response

```json
{
  "estimated_hours": 8.4,
  "complexity": "complex",
  "confidence": 0.65,
  "reasoning": "Based on task analysis, estimated complex complexity. Key factors: Complex keyword detected: critical, Urgent tag - estimate may be optimistic. Applied 1.2x adjustment for estimation uncertainty.",
  "factors": [
    "Complex keyword detected: critical",
    "Urgent tag - estimate may be optimistic",
    "No description provided - assuming simple task"
  ]
}
```

## Development

### Setup

```bash
# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run linting
poetry run black .
poetry run isort .
poetry run flake8 .
```

### Docker

```bash
# Build image
docker build -t pointless .

# Run API
docker run -p 8000:8000 pointless

# Run CLI
docker run pointless pointless estimate "Test task"
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Why "Pointless"?

Because let's be honest - most software estimation is pretty pointless anyway. At least our AI admits it's just making educated guesses based on keyword detection and random adjustments. It's like having a junior developer's estimation confidence with a senior developer's cynicism.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-estimation`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -am 'Add amazing estimation feature'`)
6. Push to the branch (`git push origin feature/amazing-estimation`)
7. Open a Pull Request

## License

MIT License - because even our license choices are pointless.

## Disclaimer

This tool is for entertainment and educational purposes. Please don't actually use it for real project planning. Or do - we're not your manager.