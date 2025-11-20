#!/usr/bin/env python3
# /// script
# dependencies = [
#     "click",
# ]
# ///

"""
OSDU Quality Analysis Script

Analyze test reliability across multiple pipelines for OSDU projects.
Detects flaky tests, calculates pass rates, and provides cloud provider metrics.

Usage:
    uv run analyze.py --json --pipelines 20
    uv run analyze.py --json --stage unit --pipelines 30
    uv run analyze.py --json --provider azure
    uv run analyze.py --json --project "partition"
"""

import json
import os
import subprocess
import sys
from typing import Any

import click


def check_prerequisites() -> None:
    """
    Check that osdu-quality CLI is installed and GitLab authentication is configured.

    Authentication can be either:
    - GITLAB_TOKEN environment variable
    - glab CLI authentication (glab auth login)

    Raises:
        Exception: If prerequisites are not met
    """
    # Check GitLab authentication (GITLAB_TOKEN or glab auth)
    has_token = bool(os.getenv("GITLAB_TOKEN"))
    has_glab_auth = False

    if not has_token:
        # Check if glab is authenticated
        try:
            result = subprocess.run(
                ["glab", "auth", "status"],
                capture_output=True,
                check=True,
                text=True,
            )
            has_glab_auth = True
        except (FileNotFoundError, subprocess.CalledProcessError):
            has_glab_auth = False

    if not has_token and not has_glab_auth:
        raise Exception(
            "GitLab authentication not configured.\n"
            "Use one of:\n"
            "  - export GITLAB_TOKEN='your-token-here'\n"
            "  - glab auth login"
        )

    # Check osdu-quality CLI
    try:
        subprocess.run(
            ["osdu-quality", "--version"],
            capture_output=True,
            check=True,
            text=True,
        )
    except FileNotFoundError:
        raise Exception(
            "osdu-quality CLI not found.\n"
            "Install with: uv tool install git+https://community.opengroup.org/danielscholl/osdu-quality.git"
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"osdu-quality CLI check failed: {e.stderr}")


def run_osdu_analyze(
    pipelines: int,
    project: str | None,
    stage: str | None,
    provider: str | None,
    output_format: str,
) -> tuple[str, int]:
    """
    Execute osdu-quality analyze command.

    Args:
        pipelines: Number of pipelines to analyze
        project: Optional project name filter
        stage: Optional test stage filter (unit/integration/acceptance)
        provider: Optional cloud provider filter (azure/aws/gcp/ibm/cimpl)
        output_format: Output format (json, markdown, or terminal)

    Returns:
        Tuple of (output_string, exit_code)

    Raises:
        Exception: If command execution fails
    """
    # Build command
    cmd = ["osdu-quality", "analyze", "--pipelines", str(pipelines)]

    if project:
        cmd.extend(["--project", project])
    if stage:
        cmd.extend(["--stage", stage])
    if provider:
        cmd.extend(["--provider", provider])

    # Add output format if not default terminal (tty)
    if output_format != "terminal":
        cmd.extend(["--output", output_format])

    try:
        # Execute command
        result = subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            text=True,
        )
        return result.stdout, 0

    except subprocess.CalledProcessError as e:
        # Command failed - return stderr
        error_msg = e.stderr if e.stderr else e.stdout
        raise Exception(f"osdu-quality command failed:\n{error_msg}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")


@click.command()
@click.option(
    "--pipelines",
    default=10,
    type=int,
    help="Number of pipelines to analyze (default: 10)",
)
@click.option(
    "--project",
    type=str,
    help="Filter by project name (e.g., 'partition')",
)
@click.option(
    "--stage",
    type=click.Choice(["unit", "integration", "acceptance"], case_sensitive=False),
    help="Filter by test stage",
)
@click.option(
    "--provider",
    type=click.Choice(["azure", "aws", "gcp", "ibm", "cimpl"], case_sensitive=False),
    help="Filter by cloud provider",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "markdown", "terminal"], case_sensitive=False),
    default="terminal",
    help="Output format: json (structured data), markdown (reports/docs), or terminal (default, colored tables)",
)
def main(
    pipelines: int,
    project: str | None,
    stage: str | None,
    provider: str | None,
    output_format: str,
):
    """
    Analyze test reliability across multiple OSDU pipelines.

    Provides:
    - Flaky test detection (tests that fail intermittently)
    - Pass rate calculations per test stage
    - Cloud provider metrics breakdown
    - Multi-project quality analysis

    Output Formats:
    - json: Structured data for AI parsing and automation
    - markdown: Human-readable reports, great for documentation and sharing
    - terminal: Interactive display with colors and tables (default)

    Requires:
    - osdu-quality CLI installed (uv tool install git+https://...)
    - GitLab authentication (GITLAB_TOKEN env var OR glab auth login)
    """
    try:
        # Check prerequisites
        check_prerequisites()

        # Run osdu-quality analyze command
        output, exit_code = run_osdu_analyze(
            pipelines=pipelines,
            project=project,
            stage=stage,
            provider=provider,
            output_format=output_format,
        )

        # Output results
        click.echo(output)
        sys.exit(exit_code)

    except Exception as e:
        if output_format == "json":
            # JSON error format
            error_data = {"error": str(e)}
            click.echo(json.dumps(error_data, indent=2))
        else:
            # Human-readable error (markdown and terminal)
            click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
