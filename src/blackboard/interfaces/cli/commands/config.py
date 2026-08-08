"""Configuration commands for CLI."""

import click
from blackboard.interfaces.config.settings import Settings
from blackboard.infrastructure.logging import get_logger

logger = get_logger(__name__)


@click.group(name="config")
def config_group():
    """Manage configuration."""
    pass


@config_group.command(name="show")
@click.pass_context
def show_config(ctx):
    """Show current configuration."""
    settings = Settings.from_env()
    click.echo("Current configuration:")
    click.echo(f"  Base URL: {settings.http.base_url or '(not set)'}")
    click.echo(f"  Timeout: {settings.http.timeout}s")
    click.echo(f"  Max retries: {settings.http.max_retries}")
    click.echo(f"  Rate limit enabled: {settings.rate_limit.enabled}")
    click.echo(f"  Calls per second: {settings.rate_limit.calls_per_second}")
    click.echo(f"  Log level: {settings.logging.level}")
    click.echo(f"  Log JSON: {settings.logging.json_format}")
    
    if not settings.http.base_url:
        click.echo("\n⚠️  Base URL is not set. Please set the BB_BASE_URL environment variable.")
        click.echo("   Create a .env file in the project root with:\n")
        click.echo("   BB_BASE_URL=https://your-blackboard-instance.com")
        click.echo("   BB_CLIENT_ID=your_client_id")
        click.echo("   BB_CLIENT_SECRET=your_client_secret")
        click.echo("   BB_TOKEN_URL=https://your-blackboard-instance.com/learn/api/public/v1/oauth2/token")


@config_group.command(name="validate")
@click.pass_context
def validate_config(ctx):
    """Validate configuration by testing connection to Blackboard."""
    settings = Settings.from_env()
    
    # Check required fields
    missing = []
    if not settings.http.base_url:
        missing.append("BB_BASE_URL")
    if not settings.auth.client_id:
        missing.append("BB_CLIENT_ID")
    if not settings.auth.client_secret.get_secret_value():
        missing.append("BB_CLIENT_SECRET")
    if not settings.auth.token_url:
        missing.append("BB_TOKEN_URL")
    
    if missing:
        click.echo(f"✗ Missing required environment variables: {', '.join(missing)}", err=True)
        click.echo("Please set them in a .env file or export them in your shell.")
        click.echo("See .env.example for reference.")
        raise click.Abort()
    
    try:
        from blackboard.infrastructure.providers.blackboard import BlackboardProvider
        from blackboard.infrastructure.http import HTTPClient, OAuth2Auth, TokenBucketRateLimiter
        auth = OAuth2Auth(settings.auth)
        rate_limiter = TokenBucketRateLimiter(settings.rate_limit)
        http_client = HTTPClient(auth, settings.http, rate_limiter)
        provider = BlackboardProvider(http_client)
        # Try to list one student to test connection
        provider.list_students(limit=1)
        click.echo("✓ Configuration is valid. Successfully connected to Blackboard.")
    except Exception as e:
        click.echo(f"✗ Configuration validation failed: {e}", err=True)
        click.echo("\nTroubleshooting tips:")
        click.echo("  1. Verify that BB_BASE_URL points to a valid Blackboard instance.")
        click.echo("  2. Check that BB_CLIENT_ID and BB_CLIENT_SECRET are correct.")
        click.echo("  3. Ensure the token URL is reachable: BB_TOKEN_URL")
        click.echo("  4. If using a self-signed certificate, you may need to disable SSL verification (not recommended for production).")
        raise click.Abort()