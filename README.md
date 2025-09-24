# pointless
Pointless is the AI buddy that reads your Jira tickets and codebase, then pretends it knows how long it'll take - just like your team, but faster. 

## Status
 - WORK IN PROGRESS. 
 - This repo currently contains the project scaffold (CLI + FastAPI) and a deterministic placeholder estimator for smoke tests. 
 - The real product is the LLM-based estimator with progressive retrieval from Jira + GitHub.

## Why (Story) Pointless?
Estimating every task manually is calorie-counting peanuts. Pointless just does it for you: **plan → effort → confidence**. If someone needs story points, we’ll garnish the plate.

## Features

- 🤖 **AI-Powered Estimation** — Uses context-aware LLMs to size work (days/points).
- 🔎 **Progressive Retrieval** — Pulls just-enough context from Jira + GitHub; expands only if confidence is low.
- 🧭 **Plan-First Output** — Produces a concrete work plan (steps with effort hours) before sizing.
- 📁 **Impacted Files** — Lists likely files/paths to touch so reviewers can sanity-check fast.
- 📊 **Confidence Metrics** — Tells you how wrong we might be (with ranges).
- ❓ **Assumptions & Questions** — Surfaces unknowns that drive estimate variance.
- 🏷️ **Complexity Assessment** — Tags tasks from “trivial” to “expert” (mostly expert).
- 📝 **Detailed Reasoning** — Explains our wild guesses with pseudo-scientific justification.
- 🔄 **Multiple Interfaces** — CLI for developers, REST API for integrations.
- 🎯 **Jira Integration Ready** — Accepts Jira ticket IDs (because everything is in Jira).
- 📝 **Write-Back to Jira (optional)** — Posts estimate, confidence, and assumptions to the ticket.
- 🎯 Story Points (optional) — Output points alongside days/hours for teams that still need them.
- 🎯 **Calibration (later)** — Learns from past tickets to tighten ranges per team.
- 🧩 **Pluggable Models** — Bring your own LLM (OpenAI/Anthropic/Gemini), configurable context limits.
- 🔐 **Local-First / Private** — Runs locally; easy to containerize for on-prem/VPC.
- 🧪 **Deterministic Baseline Mode** — Heuristic stub for CI smoke tests while the LLM flow evolves.


## Install
```
git clone https://github.com/armalite/pointless.git
cd pointless
poetry install
```

## Configuration


### Heuristic
```bash
POINTLESS_ESTIMATOR=heuristic   # default for now; LLM path coming soon
```

### LLM
```bash
POINTLESS_JIRA_BASE_URL=...
POINTLESS_JIRA_TOKEN=...          # or OAuth later
POINTLESS_GH_TOKEN=...            # or GitHub App later
POINTLESS_MODEL_PROVIDER=openai   # provider selection
POINTLESS_OPENAI_API_KEY=...
POINTLESS_CONFIDENCE_THRESHOLD=0.7
POINTLESS_MAX_FILES=20
```

### MCP (Model Context Protocol) Integration
```bash
POINTLESS_MCP_ENABLED=true                    # Enable MCP integration
POINTLESS_MCP_ATLASSIAN_SERVER_URL=...        # Atlassian MCP server URL
POINTLESS_MCP_ATLASSIAN_API_TOKEN=...         # Atlassian API token
POINTLESS_MCP_ATLASSIAN_EMAIL=...             # Atlassian account email
POINTLESS_MCP_TIMEOUT=30                      # MCP request timeout in seconds
```

### GitHub MCP Integration
```bash
POINTLESS_MCP_GITHUB_ENABLED=true             # Enable GitHub MCP integration
POINTLESS_MCP_GITHUB_SERVER_URL=...           # GitHub MCP server URL
POINTLESS_MCP_GITHUB_TOKEN=...                # GitHub access token
POINTLESS_MCP_GITHUB_TIMEOUT=30               # GitHub MCP request timeout in seconds
```

You can store these in a local .env (gitignored).


## Quick Start

### CLI
Basic estimate:
```bash
poetry run pointless estimate \
  "Add client method to get all domain monitors" \
  -d "Expose GET /domains/{id}/monitors via sdk/client.py"
```

With tags (repeatable) and optional local repo path:
```bash
poetry run pointless estimate \
  "Add client method to get all domain monitors" \
  -d "Expose GET /domains/{id}/monitors via sdk/client.py" \
  -t urgent -t backend \
  -r ~/src/your-repo
```

With MCP integration for Jira ticket data:
```bash
poetry run pointless estimate \
  "Add client method to get all domain monitors" \
  -j PROJ-123 \
  --mcp
```

With GitHub MCP integration for codebase analysis:
```bash
poetry run pointless estimate \
  "Add API endpoint for user management" \
  --description "Create REST endpoints for CRUD operations" \
  --github-owner octocat \
  --github-repo Hello-World \
  --github-mcp
```

Combined MCP integration (Jira + GitHub):
```bash
poetry run pointless estimate \
  "Implement user authentication" \
  -j AUTH-456 \
  --mcp \
  --github-owner myorg \
  --github-repo myapp \
  --github-mcp
```

Show help / version: 
```bash
poetry run pointless --help
poetry run pointless version
```

Example output:
```bash
{
  "estimated_hours": 3.4,
  "complexity": "moderate",
  "confidence": 0.7,
  "reasoning": "Heuristic baseline only; final implementation will use progressive retrieval over Jira/GitHub and an LLM (plan→size) with confidence & assumptions.",
  "factors": [
    "Moderate description length",
    "Enhanced with Jira ticket data via MCP",
    "Enhanced with GitHub codebase analysis via MCP",
    "TypeScript complexity detected",
    "Multiple architecture patterns detected (3)"
  ],
  "mcp_data_used": true,
  "jira_ticket_summary": "Implement user authentication system",
  "github_data_used": true,
  "github_repository": "myorg/myapp",
  "github_analysis_summary": "Analyzed 5 relevant files, detected 3 complexity indicators"
}
```

### API
Run the server locally:
```bash
poetry run uvicorn pointless.interfaces.api:app --host 0.0.0.0 --port 8080
```

Health check:
```bash
curl http://localhost:8080/healthz
```

Estimate (POST JSON):
```bash
curl -X POST http://localhost:8080/estimate \
  -H 'Content-Type: application/json' \
  -d '{
        "title": "Add client method to get all domain monitors",
        "description": "Expose GET /domains/{id}/monitors via sdk/client.py",
        "tags": ["urgent"]
      }'
```

With MCP integration:
```bash
curl -X POST http://localhost:8080/estimate \
  -H 'Content-Type: application/json' \
  -d '{
        "title": "Add client method to get all domain monitors",
        "description": "Expose GET /domains/{id}/monitors via sdk/client.py",
        "jira_ticket_id": "PROJ-123",
        "use_mcp": true,
        "tags": ["urgent"]
      }'
```

With GitHub MCP integration:
```bash
curl -X POST http://localhost:8080/estimate \
  -H 'Content-Type: application/json' \
  -d '{
        "title": "Add API endpoint for user management",
        "description": "Create REST endpoints for CRUD operations",
        "github_owner": "octocat",
        "github_repo": "Hello-World",
        "use_github_mcp": true,
        "tags": ["backend"]
      }'
```

Tip: pretty-print with jq:
```bash
curl -s http://localhost:8080/healthz | jq

```

(The current responses come from the deterministic placeholder; the LLM + progressive retrieval flow will replace this output.)

## Roadmap (near-term)

 - LLM output schema & prompts (plan → size → confidence/assumptions/questions)
 - Progressive retrieval v1 (rank → fetch snippets → expand)
 - ✅ GitHub connectors (MCP integration for codebase analysis)
 - Jira & GitHub connectors (MCP or direct APIs) - Jira partially complete
 - Write-back to Jira (comment/fields)
 - Optional Docker/Compose; Helm later if useful


 ## License
 MIT