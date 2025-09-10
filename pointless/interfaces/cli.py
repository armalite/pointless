from __future__ import annotations

import json
from typing import List

import typer

from ..core.estimate import estimate_effort
from ..core.models import EstimationRequest

app = typer.Typer(help="Pointless: AI effort estimates (CLI)")


@app.command()
def estimate(
    title: str = typer.Argument(..., help="Short task title"),
    description: str = typer.Option("", "--description", "-d", help="Task description"),
    jira: str = typer.Option("", "--jira", "-j", help="Jira ticket ID (optional)"),
    tags: List[str] = typer.Option(None, "--tag", "-t", help="Repeatable tag, e.g. -t urgent"),
) -> None:
    """Estimate from CLI; prints JSON to stdout."""
    req = EstimationRequest(
        title=title,
        description=description,
        jira_ticket_id=jira or None,
        tags=tags or [],
    )
    res = estimate_effort(req)
    typer.echo(json.dumps(res.model_dump(), indent=2))


if __name__ == "__main__":
    app()
