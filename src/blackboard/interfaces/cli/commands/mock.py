"""Mock server command."""

import click
from tests.integration.mock_blackboard.server import create_app


@click.command(name="mock-server")
@click.option("--port", default=5000, help="Port to run the mock server on")
@click.option("--host", default="127.0.0.1", help="Host to bind to")
def mock_server(port, host):
    """Start the mock Blackboard server for testing."""
    app = create_app()
    click.echo(f"Starting mock Blackboard server on http://{host}:{port}")
    app.run(host=host, port=port)