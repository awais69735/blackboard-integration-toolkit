"""CLI entry point."""

import click
from blackboard.infrastructure.logging import configure_logging, get_logger
from blackboard.interfaces.config.settings import Settings
from .commands import sync
from .commands.config import config_group

logger = get_logger(__name__)


@click.group()
@click.option("--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)")
@click.pass_context
def cli(ctx, log_level):
    """Blackboard Integration Toolkit CLI."""
    ctx.ensure_object(dict)
    ctx.obj["log_level"] = log_level
    # Configure logging early
    settings = Settings.from_env()
    settings.logging.level = log_level
    configure_logging(settings.logging)


# Remove the old `config` command – use the group instead.
# We'll add the group.
cli.add_command(config_group)


@cli.command(name="mock-server")
@click.option("--port", default=5000, help="Port to run the mock server on")
@click.pass_context
def mock_server(ctx, port):
    """Start the mock Blackboard server (development only)."""
    try:
        from blackboard.testing.mock_server import create_app
        app = create_app()
        click.echo(f"Starting mock Blackboard server on http://localhost:{port}")
        app.run(host="0.0.0.0", port=port, debug=True)
    except ImportError as e:
        click.echo(f"Error: Mock server not available: {e}", err=True)
        click.echo("Make sure the blackboard.testing module is installed.", err=True)
        raise click.Abort()

# Include sync commands
cli.add_command(sync.sync_students)
cli.add_command(sync.sync_courses)
cli.add_command(sync.sync_enrollments)