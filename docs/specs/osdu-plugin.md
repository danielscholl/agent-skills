# Feature: OSDU Quality Plugin

## Feature Description

Create a new Claude Code plugin called `osdu` that wraps the `osdu-quality` CLI tool, enabling AI agents to analyze GitLab CI/CD test quality for OSDU projects. The plugin will provide two main capabilities:

1. **Status Reporting**: Get latest test status by stage (unit/integration/acceptance) for OSDU projects
2. **Quality Analysis**: Analyze test reliability across multiple pipelines, detect flaky tests, calculate pass rates, and provide cloud provider metrics

This plugin follows the established agent-skills marketplace patterns, using CLI subprocess wrappers instead of direct API calls, with dual output modes (JSON for automation, TTY for humans) and comprehensive error handling.

## User Story

**As a** DevOps engineer or QA analyst working on OSDU projects
**I want to** query GitLab CI/CD test quality metrics and pipeline status through natural language
**So that I** can quickly identify flaky tests, monitor pipeline health, and analyze test reliability without manually navigating GitLab or running CLI commands

## Problem Statement

OSDU is a large-scale platform with multiple projects running CI/CD pipelines on GitLab. Engineers need to:
- Monitor test status across projects (unit, integration, acceptance stages)
- Identify flaky tests that intermittently fail
- Analyze test reliability trends across multiple pipeline runs
- Filter results by cloud provider (Azure, AWS, GCP, IBM, CIMPL)
- Generate reports in various formats (terminal, markdown, JSON)

Currently, this requires:
1. Installing and learning the `osdu-quality` CLI tool
2. Remembering complex command-line flags and options
3. Manually executing commands and parsing output
4. Understanding GitLab API authentication

An AI agent with access to these capabilities can answer natural language queries like:
- "Show me the latest pipeline status for infra-azure-provisioning"
- "Find flaky tests in the unit test stage"
- "Analyze test quality for Azure provider over the last 20 pipelines"

## Solution Statement

Create a Claude Code plugin that wraps the `osdu-quality` CLI tool with two Python scripts:

1. **status.py**: Wraps `osdu-quality status` command for latest test status by stage
2. **analyze.py**: Wraps `osdu-quality analyze` command for multi-project quality analysis

The plugin will:
- Use subprocess to execute `osdu-quality` CLI commands
- Validate that `osdu-quality` is installed and `GITLAB_TOKEN` is set
- Map Click options to `osdu-quality` CLI flags
- Support dual output modes (JSON and human-readable)
- Handle errors gracefully with clear messages
- Follow PEP 723 inline dependency declarations
- Include comprehensive SKILL.md with trigger conditions for Claude

## Related Documentation

### Requirements
- [osdu-quality Design Requirements](https://community.opengroup.org/danielscholl/osdu-quality/-/blob/main/docs/design/requirements.md) - Original design goal to create an AI-ready tool

### Architecture Decisions
- [ADR-001: PEP 723 Dependencies](docs/decisions/ADR-001-pep723-dependencies.md) - All scripts use inline dependencies
- [ADR-002: Plugin Structure](docs/decisions/ADR-002-plugin-structure.md) - Plugins use skills/ subdirectory pattern

### External Resources
- [osdu-quality GitLab Project](https://community.opengroup.org/danielscholl/osdu-quality)
- [osdu-quality User Guide](https://community.opengroup.org/danielscholl/osdu-quality/-/blob/main/docs/userguide.md)

## Codebase Analysis Findings

### Architecture Patterns
- **CLI Wrapper Pattern**: Use `subprocess.run()` to execute external CLI tools (new pattern for this marketplace)
- **Context Managers**: Use `__enter__`/`__exit__` for resource cleanup (from Kalshi/Agent-Tools)
- **Dual Output**: `--json` flag + human-readable default (from all existing plugins)
- **Error Handling**: Try/except with different formats for JSON vs TTY (from plugins/kalshi-markets/skills/kalshi-markets/scripts/status.py)

### Naming Conventions
- Plugin name: `osdu` (lowercase-with-hyphens)
- Skill name: `osdu` (matches plugin for single-skill plugins)
- Script files: `status.py`, `analyze.py` (lowercase.py)
- Functions: `snake_case` (check_osdu_cli, run_osdu_status)
- Classes: `PascalCase` (not needed for CLI wrappers)

### Similar Implementations
No existing CLI wrapper plugins in the marketplace - this will be the first. Existing plugins use HTTP APIs:
- `plugins/agent-tools/skills/web/scripts/search.py` - Brave API wrapper
- `plugins/kalshi-markets/skills/kalshi-markets/scripts/status.py` - Kalshi API wrapper

### Integration Patterns
- **PEP 723 Dependencies**: Minimal (only `click` needed for CLI wrappers)
- **Environment Variables**: Validate `GITLAB_TOKEN` before execution
- **CLI Availability**: Check `osdu-quality --version` succeeds before running commands
- **Subprocess Execution**: Use `capture_output=True, check=True, text=True` for clean error handling

### Testing Patterns (from tests/test_marketplace_schema.py)
- Marketplace manifest validation
- Plugin.json schema validation
- SKILL.md YAML frontmatter validation
- Semantic versioning checks
- Directory structure compliance
- Script syntax validation

## Archon Project

**Project ID**: `1e5db513-d39e-4133-8111-3d32e4ee1f42`

This project will track all implementation tasks using Archon MCP for task management.

## Relevant Files

### Existing Files to Reference
- `plugins/kalshi-markets/plugin.json` - Template for plugin metadata
- `plugins/kalshi-markets/skills/kalshi-markets/SKILL.md` - Template for skill manifest
- `plugins/kalshi-markets/skills/kalshi-markets/scripts/status.py` - Error handling pattern
- `scripts/validate-plugins.sh` - Validation requirements
- `tests/test_marketplace_schema.py` - Testing requirements
- `.claude-plugin/marketplace.json` - Marketplace catalog (needs update)

### New Files to Create
- `plugins/osdu/plugin.json` - Plugin metadata with author, version, keywords
- `plugins/osdu/README.md` - Plugin documentation
- `plugins/osdu/skills/osdu/SKILL.md` - Skill manifest with triggers and usage patterns
- `plugins/osdu/skills/osdu/scripts/status.py` - Status command wrapper
- `plugins/osdu/skills/osdu/scripts/analyze.py` - Analyze command wrapper

### Files to Modify
- `.claude-plugin/marketplace.json` - Add osdu plugin entry

## Implementation Plan

### Phase 1: Foundation (Plugin Structure)
Create the basic plugin directory structure and metadata files following marketplace conventions.

**Tasks**:
1. Create plugin directory structure
2. Write plugin.json with metadata
3. Create skill directory and SKILL.md manifest
4. Write plugin README.md

**Validation**: Structure passes `bash scripts/validate-plugins.sh`

### Phase 2: Core Implementation (CLI Wrappers)
Implement the two main scripts that wrap osdu-quality commands.

**Tasks**:
1. Implement status.py CLI wrapper
2. Implement analyze.py CLI wrapper
3. Add error handling and validation
4. Test dual output modes (JSON + TTY)

**Validation**: Scripts execute successfully with `uv run`

### Phase 3: Integration (Marketplace & Testing)
Integrate with marketplace and validate all components.

**Tasks**:
1. Update marketplace.json catalog
2. Run validation suite
3. Test script execution
4. Create plugin README documentation

**Validation**: All tests pass, plugin installable via marketplace

## Step by Step Tasks

### Task 1: Create Plugin Directory Structure
- **Description**: Create `plugins/osdu/` directory with `skills/osdu/scripts/` subdirectory
- **Files to create**:
  - `plugins/osdu/` (directory)
  - `plugins/osdu/skills/` (directory)
  - `plugins/osdu/skills/osdu/` (directory)
  - `plugins/osdu/skills/osdu/scripts/` (directory)
- **Archon task**: Will be created during implementation

### Task 2: Write plugin.json Manifest
- **Description**: Create plugin metadata with name, version, author, keywords, and skills array
- **Files to create**: `plugins/osdu/plugin.json`
- **Content Requirements**:
  - name: "osdu"
  - displayName: "OSDU Quality Tools"
  - version: "1.0.0"
  - description: GitLab CI/CD test quality analysis
  - author: Daniel Scholl
  - keywords: osdu, gitlab, ci-cd, test-quality, flaky-tests, pipeline-analysis
  - license: MIT
  - skills: ["osdu"]
- **Archon task**: Will be created during implementation

### Task 3: Create SKILL.md Manifest
- **Description**: Write skill manifest with YAML frontmatter, triggers, script documentation, and usage examples
- **Files to create**: `plugins/osdu/skills/osdu/SKILL.md`
- **Content Requirements**:
  - YAML frontmatter: name, description, version, allowed-tools
  - Triggers section: When to use (OSDU projects, test analysis) and when to skip
  - Scripts section: Document status.py and analyze.py with patterns
  - Quick Reference: Concrete usage examples
  - Requires: osdu-quality CLI and GITLAB_TOKEN
- **Archon task**: Will be created during implementation

### Task 4: Implement status.py CLI Wrapper
- **Description**: Create Python script that wraps `osdu-quality status` command
- **Files to create**: `plugins/osdu/skills/osdu/scripts/status.py`
- **Implementation Details**:
  - Shebang: `#!/usr/bin/env python3`
  - PEP 723 dependencies: `click`
  - Function: `check_osdu_cli()` - Verify CLI is installed
  - Function: `run_osdu_status()` - Execute osdu-quality status with subprocess
  - CLI options: --pipelines, --project, --venus, --no-release, --json
  - Error handling: Subprocess errors, missing GITLAB_TOKEN, CLI not found
  - Output: JSON when --json flag, otherwise pass through TTY output
- **Archon task**: Will be created during implementation

### Task 5: Implement analyze.py CLI Wrapper
- **Description**: Create Python script that wraps `osdu-quality analyze` command
- **Files to create**: `plugins/osdu/skills/osdu/scripts/analyze.py`
- **Implementation Details**:
  - Shebang: `#!/usr/bin/env python3`
  - PEP 723 dependencies: `click`
  - Function: `check_osdu_cli()` - Verify CLI is installed (reuse pattern)
  - Function: `run_osdu_analyze()` - Execute osdu-quality analyze with subprocess
  - CLI options: --pipelines, --project, --stage, --provider, --json
  - Error handling: Subprocess errors, missing GITLAB_TOKEN, CLI not found
  - Output: JSON when --json flag, otherwise pass through TTY output
- **Archon task**: Will be created during implementation

### Task 6: Create Plugin README
- **Description**: Write comprehensive plugin documentation
- **Files to create**: `plugins/osdu/README.md`
- **Content Sections**:
  - Overview and features
  - Installation via marketplace
  - Available scripts with examples
  - Configuration (GITLAB_TOKEN, osdu-quality CLI)
  - Use cases and examples
  - Output formats
  - Troubleshooting
- **Archon task**: Will be created during implementation

### Task 7: Update Marketplace Catalog
- **Description**: Add osdu plugin entry to marketplace.json
- **Files to modify**: `.claude-plugin/marketplace.json`
- **Changes**:
  - Add plugin object to plugins array:
    ```json
    {
      "name": "osdu",
      "path": "plugins/osdu",
      "description": "GitLab CI/CD test quality analysis for OSDU projects"
    }
    ```
- **Archon task**: Will be created during implementation

### Task 8: Validate Plugin Structure
- **Description**: Run validation scripts to ensure compliance
- **Commands to run**:
  ```bash
  bash scripts/validate-plugins.sh
  pytest tests/test_marketplace_schema.py -v
  python -m py_compile plugins/osdu/skills/osdu/scripts/*.py
  ```
- **Expected**: All validations pass with zero errors
- **Archon task**: Will be created during implementation

### Task 9: Test Script Execution
- **Description**: Manually test both scripts with various options
- **Test Cases**:
  1. Help output: `uv run plugins/osdu/skills/osdu/scripts/status.py --help`
  2. JSON output: `uv run plugins/osdu/skills/osdu/scripts/status.py --json --pipelines 5`
  3. Project filter: `uv run plugins/osdu/skills/osdu/scripts/status.py --json --project "platform/deployment-and-operations/infra-azure-provisioning"`
  4. Analyze command: `uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --pipelines 10`
  5. Stage filter: `uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --stage unit`
  6. Error handling: Test without GITLAB_TOKEN, test with osdu-quality uninstalled
- **Expected**: All tests execute successfully or fail gracefully with clear errors
- **Archon task**: Will be created during implementation

## Testing Strategy

### Unit Tests
No custom unit tests needed - marketplace schema tests will validate:
- Plugin manifest structure
- SKILL.md YAML frontmatter syntax
- Directory structure compliance
- Semantic versioning
- Script syntax (py_compile)

### Integration Tests
Manual testing of actual osdu-quality command execution:

1. **Status Command Tests**:
   ```bash
   # Basic status
   uv run plugins/osdu/skills/osdu/scripts/status.py --json --pipelines 10

   # Specific project
   uv run plugins/osdu/skills/osdu/scripts/status.py --json --project "infra-azure-provisioning"

   # Venus provider only
   uv run plugins/osdu/skills/osdu/scripts/status.py --json --venus

   # TTY output
   uv run plugins/osdu/skills/osdu/scripts/status.py --pipelines 5
   ```

2. **Analyze Command Tests**:
   ```bash
   # Basic analysis
   uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --pipelines 20

   # Stage filter
   uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --stage unit

   # Provider filter
   uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --provider azure

   # Multiple filters
   uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --stage integration --provider aws
   ```

3. **Error Handling Tests**:
   ```bash
   # Missing GITLAB_TOKEN
   unset GITLAB_TOKEN && uv run plugins/osdu/skills/osdu/scripts/status.py --json

   # Invalid project
   uv run plugins/osdu/skills/osdu/scripts/status.py --json --project "nonexistent"
   ```

### Edge Cases
- **CLI not installed**: Script should detect and provide installation instructions
- **GITLAB_TOKEN missing**: Clear error message with remediation steps
- **Invalid project name**: Pass through osdu-quality error message
- **Network issues**: Subprocess should capture and report GitLab API errors
- **Empty results**: Handle gracefully when no pipelines found
- **JSON parsing errors**: Validate JSON output from osdu-quality before echoing
- **Subprocess failures**: Capture stderr and display with context

## Acceptance Criteria

- [ ] Plugin directory structure follows ADR-002 pattern (plugins/osdu/skills/osdu/)
- [ ] plugin.json includes all required fields with valid semantic version
- [ ] SKILL.md has valid YAML frontmatter with required fields (name, description, version, allowed-tools)
- [ ] status.py successfully wraps `osdu-quality status` command
- [ ] analyze.py successfully wraps `osdu-quality analyze` command
- [ ] Both scripts support --json flag for structured output
- [ ] Both scripts pass through human-readable TTY output when --json not specified
- [ ] Both scripts validate GITLAB_TOKEN environment variable
- [ ] Both scripts check for osdu-quality CLI availability
- [ ] Both scripts use PEP 723 inline dependencies (click only)
- [ ] Error handling provides clear messages for JSON and TTY modes
- [ ] All Click options map correctly to osdu-quality CLI flags
- [ ] Plugin passes `bash scripts/validate-plugins.sh` validation
- [ ] Plugin passes pytest schema validation tests
- [ ] Scripts pass Python syntax validation (py_compile)
- [ ] Marketplace.json updated with osdu plugin entry
- [ ] README.md provides comprehensive documentation
- [ ] Manual testing confirms all commands execute successfully
- [ ] Plugin installable via Claude Code marketplace

## Validation Commands

```bash
# Validate plugin structure and manifests
bash scripts/validate-plugins.sh

# Run schema validation tests
pytest tests/test_marketplace_schema.py -v

# Validate Python syntax
python -m py_compile plugins/osdu/skills/osdu/scripts/*.py

# Test status script help
uv run plugins/osdu/skills/osdu/scripts/status.py --help

# Test status script execution (JSON)
uv run plugins/osdu/skills/osdu/scripts/status.py --json --pipelines 5

# Test status script execution (TTY)
uv run plugins/osdu/skills/osdu/scripts/status.py --pipelines 5

# Test analyze script help
uv run plugins/osdu/skills/osdu/scripts/analyze.py --help

# Test analyze script execution (JSON)
uv run plugins/osdu/skills/osdu/scripts/analyze.py --json --pipelines 10

# Test analyze script execution (TTY)
uv run plugins/osdu/skills/osdu/scripts/analyze.py --pipelines 10

# Verify marketplace integration
jq '.plugins[] | select(.name == "osdu")' .claude-plugin/marketplace.json
```

## Notes

### Design Decisions

1. **CLI Wrapper vs Direct API**:
   - Using subprocess to wrap osdu-quality CLI instead of calling GitLab API directly
   - Rationale: osdu-quality already handles authentication, pagination, data aggregation, and complex analysis logic
   - Benefit: No need to reimplement 1000+ lines of GitLab API integration

2. **Minimal Dependencies**:
   - Only `click` needed for CLI parsing
   - No httpx, markdownify, or other libraries
   - Rationale: osdu-quality CLI handles all HTTP communication

3. **Pass-Through Output**:
   - When --json flag used, parse and validate JSON from osdu-quality
   - When --json not used, pass through TTY output directly
   - Rationale: osdu-quality has well-formatted terminal output with colors and tables

4. **Environment Variable Validation**:
   - Check GITLAB_TOKEN before execution
   - Provide helpful error messages
   - Rationale: osdu-quality requires authentication, better to fail fast with clear message

### Future Enhancements

1. **Additional Commands**: osdu-quality may add more commands in future (e.g., trends, export)
2. **Caching**: Could cache results to reduce GitLab API calls
3. **Filtering**: Could add post-processing filters on JSON output
4. **Multi-Project**: Could orchestrate parallel analysis across multiple projects
5. **Visualization**: Could generate markdown reports with charts

### Patterns Discovered

**New Pattern: CLI Wrapper**
This is the first plugin in the marketplace to wrap an external CLI tool rather than calling an API directly. Key pattern elements:

```python
def check_cli_available(tool_name: str) -> None:
    """Verify external CLI tool is installed"""
    try:
        subprocess.run([tool_name, "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        raise Exception(f"{tool_name} not found. Install with: pip install {tool_name}")

def run_cli_command(cmd: list[str], expect_json: bool = False) -> Any:
    """Execute CLI command and parse output"""
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, text=True)
        if expect_json:
            return json.loads(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command failed: {e.stderr}")
```

This pattern can be reused for other CLI wrappers (e.g., kubectl, terraform, gcloud, azure-cli).

## Execution

This spec can be implemented using: `/sdlc:implement docs/specs/osdu-plugin.md`

The implementation will:
1. Create Archon tasks for each step
2. Follow the step-by-step task order
3. Use the validator agent to ensure code quality
4. Run validation commands after each phase
5. Mark tasks complete in Archon as they finish
