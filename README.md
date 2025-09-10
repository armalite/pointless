# pointless

Pointless is the AI buddy that reads your Jira tickets and codebase, then pretends it knows how long it'll take - just like your team, but faster. 

## Status
 - WORK IN PROGRESS. 
 - This repo currently contains the project scaffold (CLI + FastAPI) and a deterministic placeholder estimator for smoke tests. 
 - The real product is the LLM-based estimator with progressive retrieval from Jira + GitHub.

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