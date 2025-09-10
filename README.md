WORK IN PROGRESS

# pointless

Pointless is the AI buddy that reads your Jira tickets and codebase, then pretends it knows how long it'll take - just like your team, but faster. 

## Features

- 🤖 **AI-Powered Estimation**: Uses context-aware LLMs to estimate task effort
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
TODO

### API Usage
TODO

### Example Response
TODO

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

Guess.

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

We take no responsibility for how you use this project for effort estimations.
