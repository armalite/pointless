WORK IN PROGRESS

# pointless

Pointless is the AI buddy that reads your Jira tickets and codebase, then pretends it knows how long it'll take - just like your team, but faster. 

Status: Work in progress. This repo currently contains the project scaffold (CLI + FastAPI) and a deterministic placeholder estimator for smoke tests. The real product is the LLM-based estimator with progressive retrieval from Jira + GitHub.

## Features

- 🤖 **AI-Powered Estimation**: Uses context-aware LLMs to estimate task effort
- 📊 **Confidence Metrics**: Provides confidence levels so you know how wrong we might be
- 🏷️ **Complexity Assessment**: Categorizes tasks from "trivial" to "expert" (mostly expert)
- 📝 **Detailed Reasoning**: Explains our wild guesses with pseudo-scientific justification
- 🔄 **Multiple Interfaces**: CLI for developers, REST API for integrations
- 🎯 **Jira Integration Ready**: Supports Jira ticket IDs (because everything is in Jira)

## What Pointless will do

🤖 LLM plan → size: The model drafts a concrete change plan, then sizes it into days/points with confidence, assumptions, and questions.

🔎 Progressive retrieval: Pull just-enough context from Jira (issue text/AC) and GitHub (relevant files/snippets, history). Expand only if confidence is low.

🧾 Grounded output (JSON):
```json
{
  "points": 5,
  "days": 2.5,
  "confidence": 0.78,
  "rationale": "...",
  "drivers": ["..."],
  "impacted_files": ["sdk/client.py", "tests/test_client.py"],
  "assumptions": ["..."],
  "questions": ["..."],
  "plan": [{"description":"...", "effort_hours":4}]
}

```
Until the LLM flow lands, the CLI/API returns a temporary heuristic response to keep development unblocked.

## Install
```
git clone https://github.com/armalite/pointless.git
cd pointless
poetry install
```

## Configuration


### Heuristic
```bash
EEAI_ESTIMATOR=heuristic   # default for now; LLM path coming soon
```

### LLM
```bash
EEAI_JIRA_BASE_URL=...
EEAI_JIRA_TOKEN=...          # or OAuth later
EEAI_GH_TOKEN=...            # or GitHub App later
EEAI_MODEL_PROVIDER=openai   # provider selection
EEAI_OPENAI_API_KEY=...
EEAI_CONFIDENCE_THRESHOLD=0.7
EEAI_MAX_FILES=20
```
You can store these in a local .env (gitignored).


Roadmap (near-term)

 - LLM output schema & prompts (plan → size → confidence/assumptions/questions)
 - Progressive retrieval v1 (rank → fetch snippets → expand)
 - Jira & GitHub connectors (MCP or direct APIs)
 - Write-back to Jira (comment/fields)
 - Optional Docker/Compose; Helm later if useful


 ## License
 MIT