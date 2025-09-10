"""Command-line interface for pointless using Typer."""

import logging
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.estimate import estimate_effort
from ..core.models import EstimationRequest

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    name="pointless",
    help="Pointless AI effort estimation - because someone has to guess!",
    no_args_is_help=True,
)

console = Console()


@app.command()
def estimate(
    title: str = typer.Argument(..., help="Task title or summary"),
    description: Optional[str] = typer.Option(
        None, "--desc", "-d", help="Detailed task description"
    ),
    jira_ticket: Optional[str] = typer.Option(
        None, "--jira", "-j", help="Jira ticket ID"
    ),
    codebase_context: Optional[str] = typer.Option(
        None, "--context", "-c", help="Relevant codebase context"
    ),
    tags: Optional[List[str]] = typer.Option(
        None, "--tag", "-t", help="Task tags (can be used multiple times)"
    ),
    output_format: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json"
    ),
) -> None:
    """
    Estimate effort for a task using our sophisticated AI (totally not random).

    Example:
        pointless estimate "Fix login bug" --desc "Users can't login on mobile" \\
            --jira "PROJ-123"
    """
    try:
        # Create estimation request
        request = EstimationRequest(
            title=title,
            description=description,
            jira_ticket_id=jira_ticket,
            codebase_context=codebase_context,
            tags=tags or [],
        )

        # Get estimation
        result = estimate_effort(request)

        # Display results
        if output_format.lower() == "json":
            console.print_json(result.model_dump_json(indent=2))
        else:
            _display_estimate_table(request, result)

    except Exception as e:
        logger.error(f"Estimation failed: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Show version information."""
    from .. import __version__

    console.print(f"pointless version {__version__}")


def _display_estimate_table(request: EstimationRequest, result) -> None:
    """Display estimation results in a formatted table."""

    # Main results panel
    results_text = f"""
[bold]Estimated Hours:[/bold] {result.estimated_hours}
[bold]Complexity:[/bold] {result.complexity.value.title()}
[bold]Confidence:[/bold] {result.confidence * 100:.0f}%
    """

    console.print(
        Panel(
            results_text.strip(),
            title="[bold blue]Effort Estimation Results[/bold blue]",
            border_style="blue",
        )
    )

    # Reasoning panel
    console.print(
        Panel(
            result.reasoning,
            title="[bold green]Reasoning[/bold green]",
            border_style="green",
        )
    )

    # Factors table
    if result.factors:
        table = Table(title="Key Factors Considered")
        table.add_column("Factor", style="cyan")

        for factor in result.factors:
            table.add_row(factor)

        console.print(table)

    # Task details
    details_text = f"[bold]Title:[/bold] {request.title}"
    if request.jira_ticket_id:
        details_text += f"\n[bold]Jira:[/bold] {request.jira_ticket_id}"
    if request.tags:
        details_text += f"\n[bold]Tags:[/bold] {', '.join(request.tags)}"

    console.print(
        Panel(
            details_text,
            title="[bold yellow]Task Details[/bold yellow]",
            border_style="yellow",
        )
    )


if __name__ == "__main__":
    app()
