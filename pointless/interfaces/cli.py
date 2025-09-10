from __future__ import annotations

import json
from typing import List

import typer

from pointless import __version__
from pointless.core.estimate import estimate_effort
from pointless.core.models import EstimationRequest

app = typer.Typer(help="Pointless: AI effort estimates")


@app.command("estimate")
def estimate_cmd(
    title: str = typer.Argument(..., help="Short task title"),
    description: str = typer.Option("", "--description", "-d", help="Task description"),
    jira: str = typer.Option("", "--jira", "-j", help="Jira ticket ID (optional)"),
    tags: List[str] = typer.Option(None, "--tag", "-t", help="Repeatable tag, e.g. -t urgent"),
    repo: str = typer.Option("", "--repo", "-r", help="Local repo path to scan (optional)"),
) -> None:
    """Estimate from CLI; prints JSON to stdout."""
    req = EstimationRequest(
        title=title,
        description=description,
        jira_ticket_id=jira or None,
        tags=tags or [],
        codebase_context=repo or None,
    )
    res = estimate_effort(req)
    typer.echo(json.dumps(res.model_dump(), indent=2))


@app.command("version")
def version_cmd() -> None:
    """Print version and exit."""
    typer.echo(__version__)


if __name__ == "__main__":
    app()
