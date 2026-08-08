"""Sync commands for CLI."""

import click
from blackboard.application.services.sync_service import SyncService
from blackboard.application.dto import SyncOptions, SyncStatus
from blackboard.infrastructure.providers.blackboard import BlackboardProvider
from blackboard.infrastructure.http import HTTPClient, OAuth2Auth, TokenBucketRateLimiter
from blackboard.interfaces.config.settings import Settings
from blackboard.infrastructure.logging import get_logger

logger = get_logger(__name__)


def _get_provider():
    """Create a BlackboardProvider from environment settings."""
    try:
        settings = Settings.from_env()
        auth = OAuth2Auth(settings.auth)
        rate_limiter = TokenBucketRateLimiter(settings.rate_limit)
        http_client = HTTPClient(auth, settings.http, rate_limiter)
        return BlackboardProvider(http_client)
    except Exception as e:
        click.echo(f"Error initializing Blackboard provider: {e}", err=True)
        click.echo("Make sure all required environment variables are set (BB_BASE_URL, BB_CLIENT_ID, etc.)", err=True)
        raise click.Abort()


@click.command(name="sync-students")
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
@click.option("--file", type=click.Path(exists=True), help="JSON file with student data")
@click.pass_context
def sync_students(ctx, dry_run, file):
    """Sync students from a JSON file to Blackboard."""
    if not file:
        click.echo("Please provide a JSON file with --file", err=True)
        raise click.Abort()
    
    import json
    with open(file, "r") as f:
        external_students = json.load(f)
    
    provider = _get_provider()
    service = SyncService(provider)
    options = SyncOptions(dry_run=dry_run)
    result = service.sync_students(external_students, options)
    
    _print_result(result, "Student sync")


@click.command(name="sync-courses")
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
@click.option("--file", type=click.Path(exists=True), help="JSON file with course data")
@click.pass_context
def sync_courses(ctx, dry_run, file):
    """Sync courses from a JSON file to Blackboard."""
    if not file:
        click.echo("Please provide a JSON file with --file", err=True)
        raise click.Abort()
    
    import json
    with open(file, "r") as f:
        external_courses = json.load(f)
    
    provider = _get_provider()
    service = SyncService(provider)
    options = SyncOptions(dry_run=dry_run)
    result = service.sync_courses(external_courses, options)
    
    _print_result(result, "Course sync")


@click.command(name="sync-enrollments")
@click.option("--dry-run", is_flag=True, help="Preview changes without applying")
@click.option("--file", type=click.Path(exists=True), help="JSON file with enrollment data")
@click.pass_context
def sync_enrollments(ctx, dry_run, file):
    """Sync enrollments from a JSON file to Blackboard."""
    if not file:
        click.echo("Please provide a JSON file with --file", err=True)
        raise click.Abort()
    
    import json
    with open(file, "r") as f:
        external_enrollments = json.load(f)
    
    provider = _get_provider()
    service = SyncService(provider)
    options = SyncOptions(dry_run=dry_run)
    result = service.sync_enrollments(external_enrollments, options)
    
    _print_result(result, "Enrollment sync")


def _print_result(result, title):
    """Print sync result in a human-friendly format."""
    click.echo(f"\n{title} completed with status: {result.status.value}")
    click.echo(f"  Created: {result.created}")
    click.echo(f"  Updated: {result.updated}")
    click.echo(f"  Deleted: {result.deleted}")
    click.echo(f"  Skipped: {result.skipped}")
    if result.errors:
        click.echo("  Errors:")
        for error in result.errors:
            click.echo(f"    - {error}")