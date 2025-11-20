---
name: osdu
description: "GitLab CI/CD test job reliability analysis for OSDU projects. Tracks test job (unit/integration/acceptance) pass/fail status across pipeline runs. Use for test job status, flaky test job detection, test reliability metrics, cloud provider analytics. Wraps osdu-quality CLI."
version: 1.0.0
allowed-tools: Bash
---

# osdu

## 🎯 Triggers
**USE:** OSDU projects, GitLab CI/CD pipeline analysis, test job reliability metrics, flaky test job detection, pipeline health monitoring, cloud provider metrics (Azure/AWS/GCP/IBM/CIMPL), unit/integration/acceptance test analysis
**SKIP:** Individual test tracking, non-test jobs (build/deploy/lint), general test frameworks, non-OSDU projects, non-GitLab CI systems

## Important: What This Tool Tracks

**Pipeline Hierarchy:**
- **Pipeline Run** → **Test Stage** (unit/integration/acceptance) → **Test Job** → Test Suite

**What is tracked:** Test job pass/fail status across multiple pipeline runs
**What is NOT tracked:** Individual test results, non-test jobs (build, deploy, lint, etc.)

**Scope:** Only tracks jobs that run tests:
- **Unit test jobs** - Run unit test suites
- **Integration test jobs** - Run integration test suites
- **Acceptance test jobs** - Run acceptance/e2e test suites

**Key Distinction:**
- A **test job** runs a suite of tests (e.g., 100 tests)
- If 99 tests pass and 1 fails → the **test job fails**
- The tool tracks whether test jobs pass or fail across pipeline runs
- A "flaky test job" = a test job that sometimes passes, sometimes fails across multiple runs

**Example:**
- Pipeline #1: test job "unit-tests-azure" passes (100/100 tests)
- Pipeline #2: test job "unit-tests-azure" fails (99/100 tests)
- Pipeline #3: test job "unit-tests-azure" passes (100/100 tests)
- **Result:** This test job is "flaky" - unreliable across pipeline runs

## Prerequisites
- `osdu-quality` CLI tool installed (`uv tool install git+https://community.opengroup.org/danielscholl/osdu-quality.git`)
- GitLab authentication configured (either):
  - `GITLAB_TOKEN` environment variable set, OR
  - `glab` CLI authenticated (`glab auth login`)
- Access to OSDU GitLab projects

## Scripts (use via script_run)

**Test Job Status:**
- `status.py` - Get latest test job status by stage (unit/integration/acceptance)
  - Shows which test jobs passed/failed in recent pipeline runs
  - Only tracks jobs that run tests (unit/integration/acceptance)
  - `--pipelines N` - Analyze last N pipelines (default: 10)
  - `--project NAME` - Filter by specific project path
  - `--venus` - Filter Venus provider pipelines only
  - `--no-release` - Exclude release pipelines
  - `--format FORMAT` - Output format (json/markdown/terminal)

**Test Job Reliability Analysis:**
- `analyze.py` - Analyze test job reliability across multiple pipeline runs
  - Identifies flaky test jobs (test jobs that intermittently fail)
  - Calculates test job pass rates per stage
  - Only analyzes jobs that run tests
  - `--pipelines N` - Analyze last N pipelines (default: 10)
  - `--project NAME` - Filter by specific project path
  - `--stage STAGE` - Filter by test stage (unit/integration/acceptance)
  - `--provider PROVIDER` - Filter by cloud provider (azure/aws/gcp/ibm/cimpl)
  - `--format FORMAT` - Output format (json/markdown/terminal)

## Output Formats

Choose the right format for your use case:

**json** - Use when:
- Parsing and analyzing data programmatically
- Extracting specific metrics or values
- Need structured data for further processing
- Building automation or integrations

**markdown** - Use when:
- Creating reports for documentation
- Sharing results in issues, PRs, or chat
- Generating human-readable summaries
- Need formatted output for copy-paste
- Want tables and formatting preserved

**terminal** (default) - Use when:
- Interactive viewing in terminal
- Quick status checks
- Need colorized output
- Human reading directly from terminal

## Usage

**Pattern:** `script_run osdu <script> --format <format> [args]`
**Format selection:** Choose json, markdown, or terminal based on use case (see Output Formats above)
**Help:** `script_help osdu <script>` shows all options

## Quick Reference

```bash
# Get latest pipeline status (JSON for parsing)
script_run osdu status.py --format json --pipelines 10

# Check specific project status (Markdown for reports)
script_run osdu status.py --format markdown --project "partition"

# Analyze test quality for Azure pipelines (JSON for data extraction)
script_run osdu analyze.py --format json --pipelines 20 --provider azure

# Find flaky test jobs in unit stage (Markdown for sharing)
script_run osdu analyze.py --format markdown --stage unit --pipelines 30

# Venus provider status (Terminal for quick viewing)
script_run osdu status.py --venus --no-release

# Compare providers (JSON for analysis, then Markdown for summary)
script_run osdu analyze.py --format json --provider azure
script_run osdu analyze.py --format markdown --provider aws
```

## Error Handling

Scripts will fail gracefully with clear messages if:
- `osdu-quality` CLI is not installed
- `GITLAB_TOKEN` environment variable is not set
- GitLab API errors occur
- Invalid project or filter options provided
