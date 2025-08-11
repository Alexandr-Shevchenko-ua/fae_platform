# Requirements Writer Crew (Stage-1 of AI SDLC)

CrewAI-powered multi-agent pipeline: **Policy+Clarify → Draft → Validate** (warn-only).
LangSmith tracing via `@traceable`. English only, no Firecrawl.

## Run
```bash
pip install -e .
cp .env.example .env && export $(grep -v '^#' .env | xargs)
python -m requirements_crew.orchestrator --spec "Build a REST API for todos with CRUD and JWT"
```
Artifacts go to `artifacts/<timestamp>/`.
