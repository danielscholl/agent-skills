# OSDU Quality Tools Plugin

GitLab CI/CD test quality analysis for OSDU projects. This plugin wraps the [osdu-quality](https://community.opengroup.org/danielscholl/osdu-quality) CLI tool, enabling AI agents to analyze pipeline status, detect flaky tests, and monitor test reliability across OSDU projects.

## Features

- **Pipeline Status Reporting**: Get latest test status by stage (unit/integration/acceptance)
- **Flaky Test Detection**: Identify tests that fail intermittently across multiple pipeline runs
- **Reliability Metrics**: Calculate pass rates and test quality scores
- **Cloud Provider Analytics**: Filter and analyze by provider (Azure, AWS, GCP, IBM, CIMPL)
- **Multi-Project Analysis**: Aggregate quality metrics across OSDU projects
- **Dual Output Modes**: JSON for automation or human-readable tables for terminal

## Installation

### Via Claude Code Marketplace

```bash
# Install the plugin
claude-code plugin install osdu

# Verify installation
claude-code plugin list
```

### Manual Installation

```bash
# Clone repository
git clone https://github.com/danielscholl/agent-base
cd ai-examples/agent-skills

# Plugin is ready to use via script_run
```

## Prerequisites

### 1. Install osdu-quality CLI

```bash
uv tool install git+https://community.opengroup.org/danielscholl/osdu-quality.git
```

Verify installation:
```bash
osdu-quality --version
```

### 2. Configure GitLab Authentication

The plugin requires GitLab authentication. Choose one of the following methods:

**Option 1: GitLab Token (recommended for automation)**

Set a GitLab personal access token with `read_api` scope:

```bash
export GITLAB_TOKEN='your-gitlab-token-here'
```

To make it permanent, add to your shell profile (`~/.bashrc`, `~/.zshrc`):
```bash
echo 'export GITLAB_TOKEN="your-gitlab-token-here"' >> ~/.zshrc
source ~/.zshrc
```

**Option 2: glab CLI Authentication (recommended for interactive use)**

Authenticate using the GitLab CLI:

```bash
# Install glab if needed
brew install glab  # macOS
# or download from https://gitlab.com/gitlab-org/cli

# Authenticate
glab auth login
```

## Available Scripts

### status.py - Pipeline Status

Get latest test status by stage for OSDU projects.

**Usage:**
```bash
# Basic status with JSON output (for AI parsing)
script_run osdu status.py --format json --pipelines 10

# Specific project with Markdown (for reports)
script_run osdu status.py --format markdown --project "partition"

# More pipelines with terminal output (quick viewing)
script_run osdu status.py --pipelines 20

# Venus provider only
script_run osdu status.py --format json --venus

# Exclude release pipelines
script_run osdu status.py --format markdown --no-release
```

**Options:**
- `--pipelines N` - Number of pipelines to analyze (default: 10)
- `--project NAME` - Filter by project name
- `--venus` - Filter Venus provider pipelines only
- `--no-release` - Exclude release pipelines
- `--format FORMAT` - Output format: json, markdown, or terminal (default: terminal)

### analyze.py - Quality Analysis

Analyze test reliability across multiple pipelines, detect flaky tests, calculate pass rates.

**Usage:**
```bash
# Basic analysis with JSON (for AI parsing)
script_run osdu analyze.py --format json --pipelines 10

# Analyze more pipelines with Markdown (for documentation)
script_run osdu analyze.py --format markdown --pipelines 30

# Filter by test stage with JSON
script_run osdu analyze.py --format json --stage unit

# Filter by cloud provider with Markdown (for reports)
script_run osdu analyze.py --format markdown --provider azure

# Combine filters
script_run osdu analyze.py --format json --stage integration --provider aws --pipelines 20

# Specific project analysis
script_run osdu analyze.py --format markdown --project "partition"
```

**Options:**
- `--pipelines N` - Number of pipelines to analyze (default: 10)
- `--project NAME` - Filter by project name
- `--stage STAGE` - Filter by stage: unit, integration, acceptance
- `--provider PROVIDER` - Filter by provider: azure, aws, gcp, ibm, cimpl
- `--format FORMAT` - Output format: json, markdown, or terminal (default: terminal)

## Use Cases

### 1. Monitor Pipeline Health

Ask Claude Code:
> "Show me the latest pipeline status for partition"

Claude will use `status.py` to fetch current test results.

### 2. Find Flaky Jobs

Ask Claude Code:
> "Find flaky jobs in the unit stage across the last 30 pipelines"

Claude will use `analyze.py --stage unit --pipelines 30` to detect jobs with intermittent failures.

### 3. Analyze Cloud Provider Metrics

Ask Claude Code:
> "Compare test reliability between Azure and AWS providers"

Claude will run `analyze.py --provider azure` and `analyze.py --provider aws` to compare metrics.

### 4. Quality Trends

Ask Claude Code:
> "What's the test pass rate for integration tests over the last 50 pipelines?"

Claude will use `analyze.py --stage integration --pipelines 50` for trend analysis.

## Output Formats

Choose the right format for your use case using `--format` option:

### JSON (`--format json`)

**Use for:**
- AI parsing and analysis
- Extracting specific metrics
- Automation and integrations
- Structured data processing

**Example output:**
```json
{
  "summary": {
    "total_pipelines": 20,
    "analyzed_stages": ["unit", "integration", "acceptance"],
    "overall_pass_rate": 92.5
  },
  "flaky_tests": [
    {
      "name": "test_authentication_timeout",
      "stage": "integration",
      "pass_rate": 65.0,
      "total_runs": 20,
      "failures": 7
    }
  ],
  "by_provider": {
    "azure": {"pass_rate": 95.0, "pipelines": 12},
    "aws": {"pass_rate": 88.5, "pipelines": 8}
  }
}
```

### Markdown (`--format markdown`)

**Use for:**
- Documentation and reports
- Sharing in issues, PRs, or chat
- Human-readable summaries
- Formatted output for copy-paste
- Preserving tables and structure

**Example output:**
```markdown
# Pipeline Status Report

## Summary
- Total Pipelines: 20
- Overall Pass Rate: 92.5%

## Flaky Tests

| Test Name | Stage | Pass Rate | Failures |
|-----------|-------|-----------|----------|
| test_authentication_timeout | integration | 65.0% | 7/20 |

## Provider Breakdown

| Provider | Pass Rate | Pipelines |
|----------|-----------|-----------|
| Azure | 95.0% | 12 |
| AWS | 88.5% | 8 |
```

### Terminal (default)

**Use for:**
- Interactive terminal viewing
- Quick status checks
- Colorized output
- Human reading directly

Human-readable tables with colors and formatting. This is the default when `--format` is omitted.

## Configuration

### Authentication

GitLab authentication is required. Choose one method:

| Method | Description |
|--------|-------------|
| `GITLAB_TOKEN` | GitLab personal access token with `read_api` scope (recommended for automation) |
| `glab auth login` | GitLab CLI authentication (recommended for interactive use) |

### osdu-quality CLI

The plugin requires the `osdu-quality` CLI tool. Install it with:

```bash
uv tool install git+https://community.opengroup.org/danielscholl/osdu-quality.git
```

For more information, see the [osdu-quality documentation](https://community.opengroup.org/danielscholl/osdu-quality/-/blob/main/docs/userguide.md).

## Troubleshooting

### Error: "osdu-quality CLI not found"

**Solution:** Install the CLI tool:
```bash
uv tool install git+https://community.opengroup.org/danielscholl/osdu-quality.git
osdu-quality --version
```

### Error: "GitLab authentication not configured"

**Solution:** Configure GitLab authentication using one of these methods:

**Option 1: Set GITLAB_TOKEN**
```bash
export GITLAB_TOKEN='your-token-here'
```

To make it permanent:
```bash
echo 'export GITLAB_TOKEN="your-token"' >> ~/.zshrc
source ~/.zshrc
```

**Option 2: Use glab CLI**
```bash
glab auth login
```

### Error: "osdu-quality command failed"

**Possible causes:**
1. Invalid project name - verify project path in GitLab
2. Insufficient GitLab permissions - token needs `read_api` scope
3. Network issues - check GitLab connectivity
4. No pipelines found - try different filters or time range

**Solution:** Check the error message for specific details. The plugin passes through osdu-quality error messages for debugging.

### Empty Results

If you get no results:
- Increase `--pipelines` count
- Remove filters (`--project`, `--stage`, `--provider`) to broaden search
- Verify project has CI/CD pipelines in GitLab
- Check that pipelines contain test results

## Examples

### Quick Health Check
```bash
script_run osdu status.py --json --pipelines 5
```

### Deep Flaky Test Analysis
```bash
script_run osdu analyze.py --json --pipelines 50 --stage unit
```

### Provider Comparison
```bash
script_run osdu analyze.py --json --provider azure --pipelines 20
script_run osdu analyze.py --json --provider aws --pipelines 20
```

### Project-Specific Analysis
```bash
script_run osdu analyze.py --json --project "partition" --pipelines 30
```

## Related Resources

- [osdu-quality CLI Tool](https://community.opengroup.org/danielscholl/osdu-quality)
- [osdu-quality User Guide](https://community.opengroup.org/danielscholl/osdu-quality/-/blob/main/docs/userguide.md)
- [OSDU Forum](https://community.opengroup.org/osdu)

## License

MIT License - See [LICENSE](../../LICENSE) for details.

## Author

**Daniel Scholl**
- GitHub: [@danielscholl](https://github.com/danielscholl)
- Email: daniel.scholl@gmail.com
