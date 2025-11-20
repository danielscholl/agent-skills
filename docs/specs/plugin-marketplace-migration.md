# Feature: Claude Code Plugin Marketplace Migration

## Feature Description

Transform the agent-skills repository into a Claude Code plugin marketplace, making the existing skills (web-access and kalshi-markets) compatible with Claude Code's plugin installation system. This enables users to install skills via `/plugin install skill-name@agent-skills` and allows distribution through Claude Code's marketplace ecosystem.

The migration includes:
- Creating marketplace infrastructure (`.claude-plugin/marketplace.json`)
- Restructuring directories from `skill-*` to `plugins/*` format
- Adding plugin manifests (`plugin.json`) for each skill
- Updating SKILL.md files with required 2025 schema fields (allowed-tools, version)
- Maintaining backward compatibility with existing script execution patterns
- Adding validation and testing infrastructure

## User Story

As a Claude Code user
I want to install agent skills via the plugin marketplace
So that I can easily discover, install, and use production-ready skills without manual configuration

## Problem Statement

The current agent-skills repository contains well-structured, production-ready skills (web-access, kalshi-markets) but lacks the infrastructure required for Claude Code's plugin marketplace:

1. **No marketplace discovery**: Missing `.claude-plugin/marketplace.json` prevents Claude Code from recognizing this as a plugin source
2. **Incompatible directory structure**: `skill-*` naming doesn't follow Claude Code's `plugins/*` convention
3. **Missing plugin metadata**: No `plugin.json` files for version tracking, authorship, and dependencies
4. **Incomplete SKILL.md schema**: Missing required 2025 fields (`allowed-tools`, `version`)
5. **No installation workflow**: Users must manually copy files instead of using `/plugin install`

## Solution Statement

Migrate the repository to Claude Code's plugin marketplace specification while preserving existing functionality:

1. Add marketplace manifest at `.claude-plugin/marketplace.json` with plugin catalog
2. Restructure directories: `skill-websearch/` → `plugins/web-access/skills/web-access/`
3. Create `plugin.json` manifests with metadata, versioning, and keywords
4. Update all SKILL.md files with `allowed-tools` and `version` frontmatter fields
5. Add testing infrastructure to validate plugin compatibility
6. Update documentation with installation instructions

This approach maintains 100% backward compatibility with existing `uv run` scripts while enabling marketplace distribution.

## Related Documentation

### Requirements
- Claude Code Plugins: https://code.claude.com/docs/en/plugins
- Claude Code Skills: https://code.claude.com/docs/en/skills
- PEP 723 Inline Dependencies: https://peps.python.org/pep-0723/

### Architecture Decisions
- ADR-001 (to be created): Use PEP 723 inline dependencies over requirements.txt
- ADR-002 (to be created): Maintain dual output modes (JSON + human-readable)
- ADR-003 (to be created): Plugin structure with skills/ subdirectory

## Codebase Analysis Findings

Based on deep codebase analysis by the codebase-analyst agent:

### Architecture Patterns to Follow
1. **PEP 723 Inline Dependencies**: Continue using `# /// script` headers in all Python files
2. **Self-Contained Scripts**: Keep each script fully independent with embedded client classes
3. **Dual Output Modes**: Maintain `--json` flag for automation + human-readable default
4. **Context Manager Pattern**: All HTTP clients use `__enter__`/`__exit__` lifecycle
5. **Structured Error Handling**: Consistent try/except with typed error responses

### Naming Conventions Discovered
- **Files**: Lowercase with hyphens (`search.py`, `market.py`)
- **Directories**: Kebab-case (`skill-websearch`, migrate to `web-access`)
- **Classes**: PascalCase (`BraveSearchClient`, `KalshiClient`)
- **Functions**: snake_case (`format_search_result`, `html_to_markdown`)
- **Constants**: UPPER_SNAKE_CASE (`API_BASE_URL`, `API_TIMEOUT`)

### Similar Implementations Found
- Both skills follow identical CLI patterns using Click
- Both use httpx context managers for HTTP operations
- Both implement dual output modes (JSON + formatted text)
- SKILL.md structure is consistent across both skills

### Integration Patterns
- Scripts execute via `uv run <path>` (UV auto-installs dependencies)
- Skills invoke via `script_run <skill-name> <script> --json`
- No shared library code - each script is fully standalone
- Environment variables for API keys (BRAVE_API_KEY, KALSHI_API_KEY)

## Relevant Files

### Existing Files
- `README.md`: Project overview (needs marketplace installation instructions)
- `skill-websearch/SKILL.md`: Web access skill manifest (needs allowed-tools, version)
- `skill-kalshi/SKILL.md`: Kalshi markets skill manifest (needs allowed-tools, version)
- `skill-websearch/scripts/*.py`: 2 Python scripts (search, fetch)
- `skill-kalshi/scripts/*.py`: 10 Python scripts (market data operations)

### New Files
- `.claude-plugin/marketplace.json`: Marketplace catalog manifest
- `plugins/web-access/plugin.json`: Web access plugin metadata
- `plugins/kalshi-markets/plugin.json`: Kalshi markets plugin metadata
- `tests/test_marketplace_schema.py`: Validation tests for marketplace compliance
- `scripts/validate-plugins.sh`: Plugin structure validation script
- `docs/decisions/ADR-001-pep723-dependencies.md`: Architecture decision record
- `docs/decisions/ADR-002-plugin-structure.md`: Architecture decision record
- `CONTRIBUTING.md`: Plugin contribution guidelines

## Implementation Plan

### Phase 1: Marketplace Infrastructure
Create the foundational marketplace files that enable Claude Code discovery without disrupting existing functionality.

**Tasks:**
- Create `.claude-plugin/marketplace.json` with plugin catalog
- Add validation schema for marketplace.json
- Update README.md with marketplace installation instructions

### Phase 2: Directory Migration
Restructure from skill-* to plugins/* format while maintaining script paths.

**Tasks:**
- Create `plugins/web-access/` directory structure
- Move `skill-websearch/` → `plugins/web-access/skills/web-access/`
- Create `plugins/kalshi-markets/` directory structure
- Move `skill-kalshi/` → `plugins/kalshi-markets/skills/kalshi-markets/`
- Update any hardcoded path references in scripts (none found)

### Phase 3: Plugin Manifests
Add plugin.json files with complete metadata for each skill.

**Tasks:**
- Create `plugins/web-access/plugin.json` with metadata, keywords, author
- Create `plugins/kalshi-markets/plugin.json` with metadata, keywords, author
- Add repository URLs and license information

### Phase 4: SKILL.md Schema Updates
Update existing SKILL.md files to 2025 schema compliance.

**Tasks:**
- Add `allowed-tools: Bash, WebFetch, WebSearch` to web-access/SKILL.md
- Add `version: 1.0.0` to web-access/SKILL.md
- Add `allowed-tools: Bash` to kalshi-markets/SKILL.md
- Add `version: 1.0.0` to kalshi-markets/SKILL.md
- Expand descriptions with trigger context

### Phase 5: Testing & Validation
Create automated validation to ensure ongoing marketplace compliance.

**Tasks:**
- Create `tests/test_marketplace_schema.py` for JSON schema validation
- Create `scripts/validate-plugins.sh` for structure validation
- Add GitHub Actions workflow for CI validation
- Test plugin installation via `/plugin marketplace add` command

### Phase 6: Documentation
Update all documentation to reflect marketplace structure.

**Tasks:**
- Create ADR-001: PEP 723 inline dependencies decision
- Create ADR-002: Plugin structure with skills/ subdirectory
- Create CONTRIBUTING.md with plugin development guidelines
- Add LICENSE file (MIT recommended)
- Update README.md with complete marketplace usage examples

## Step by Step Tasks

### Task 1: Create Marketplace Manifest
- **Description**: Create `.claude-plugin/marketplace.json` with plugin catalog listing both web-access and kalshi-markets plugins
- **Files to modify**:
  - `.claude-plugin/marketplace.json` (new)
- **Archon task**: Will be created during implementation

### Task 2: Create Web Access Plugin Manifest
- **Description**: Create `plugins/web-access/plugin.json` with complete metadata (name, version, description, author, keywords, repository)
- **Files to modify**:
  - `plugins/web-access/plugin.json` (new)
- **Archon task**: Will be created during implementation

### Task 3: Create Kalshi Markets Plugin Manifest
- **Description**: Create `plugins/kalshi-markets/plugin.json` with complete metadata
- **Files to modify**:
  - `plugins/kalshi-markets/plugin.json` (new)
- **Archon task**: Will be created during implementation

### Task 4: Migrate Web Access Directory Structure
- **Description**: Create `plugins/web-access/skills/web-access/` and move files from `skill-websearch/`
- **Files to modify**:
  - Move `skill-websearch/SKILL.md` → `plugins/web-access/skills/web-access/SKILL.md`
  - Move `skill-websearch/scripts/` → `plugins/web-access/skills/web-access/scripts/`
- **Archon task**: Will be created during implementation

### Task 5: Migrate Kalshi Markets Directory Structure
- **Description**: Create `plugins/kalshi-markets/skills/kalshi-markets/` and move files from `skill-kalshi/`
- **Files to modify**:
  - Move `skill-kalshi/SKILL.md` → `plugins/kalshi-markets/skills/kalshi-markets/SKILL.md`
  - Move `skill-kalshi/scripts/` → `plugins/kalshi-markets/skills/kalshi-markets/scripts/`
- **Archon task**: Will be created during implementation

### Task 6: Update Web Access SKILL.md Schema
- **Description**: Add `allowed-tools`, `version` fields to frontmatter; expand description with trigger context
- **Files to modify**:
  - `plugins/web-access/skills/web-access/SKILL.md`
- **Archon task**: Will be created during implementation

### Task 7: Update Kalshi Markets SKILL.md Schema
- **Description**: Add `allowed-tools`, `version` fields to frontmatter; expand description with trigger context
- **Files to modify**:
  - `plugins/kalshi-markets/skills/kalshi-markets/SKILL.md`
- **Archon task**: Will be created during implementation

### Task 8: Create Marketplace Schema Validation Tests
- **Description**: Create pytest tests to validate marketplace.json and plugin.json against Claude Code schemas
- **Files to modify**:
  - `tests/test_marketplace_schema.py` (new)
  - `tests/__init__.py` (new)
- **Archon task**: Will be created during implementation

### Task 9: Create Plugin Structure Validation Script
- **Description**: Create bash script to validate directory structure, required files, and SKILL.md schema
- **Files to modify**:
  - `scripts/validate-plugins.sh` (new)
- **Archon task**: Will be created during implementation

### Task 10: Add GitHub Actions CI Workflow
- **Description**: Create GitHub Actions workflow to run validation tests on every commit
- **Files to modify**:
  - `.github/workflows/validate-plugins.yml` (new)
- **Archon task**: Will be created during implementation

### Task 11: Create Architecture Decision Records
- **Description**: Document key architectural decisions (PEP 723 dependencies, plugin structure)
- **Files to modify**:
  - `docs/decisions/ADR-001-pep723-dependencies.md` (new)
  - `docs/decisions/ADR-002-plugin-structure.md` (new)
- **Archon task**: Will be created during implementation

### Task 12: Create CONTRIBUTING.md
- **Description**: Document guidelines for adding new plugins to the marketplace
- **Files to modify**:
  - `CONTRIBUTING.md` (new)
- **Archon task**: Will be created during implementation

### Task 13: Add LICENSE File
- **Description**: Add MIT license to repository
- **Files to modify**:
  - `LICENSE` (new)
- **Archon task**: Will be created during implementation

### Task 14: Update README.md
- **Description**: Add marketplace installation instructions, plugin listing, and usage examples
- **Files to modify**:
  - `README.md`
- **Archon task**: Will be created during implementation

### Task 15: Manual Installation Testing
- **Description**: Test plugin installation via `/plugin marketplace add` and verify skill activation
- **Files to modify**: None (manual testing task)
- **Archon task**: Will be created during implementation

## Testing Strategy

### Unit Tests
The validator agent will create comprehensive tests during implementation, including:

1. **Marketplace Schema Validation**
   - Test marketplace.json against Claude Code schema
   - Validate required fields (name, owner, plugins array)
   - Check plugin references point to valid directories

2. **Plugin Manifest Validation**
   - Test each plugin.json against schema
   - Validate semantic versioning format
   - Check required author fields

3. **SKILL.md Schema Validation**
   - Parse YAML frontmatter with PyYAML
   - Validate required fields (name, description, allowed-tools, version)
   - Check description length (max 1024 chars)
   - Validate name format (lowercase-with-hyphens, max 64 chars)

4. **Directory Structure Validation**
   - Verify plugins/ directory exists
   - Check each plugin has skills/ subdirectory
   - Validate SKILL.md presence in each skill

### Integration Tests
1. **Plugin Installation Test**
   - Add marketplace via `/plugin marketplace add file:///path/to/agent-skills`
   - Install plugin via `/plugin install web-access@agent-skills`
   - Verify skill appears in `/skills` output

2. **Script Execution Test**
   - Test `script_run web-access search --query "test" --json`
   - Verify JSON output structure
   - Test error handling with invalid inputs

3. **Environment Variable Handling**
   - Test scripts fail gracefully without API keys
   - Verify error messages guide user to set environment variables

### Edge Cases
- Empty marketplace.json plugins array
- Plugin with missing plugin.json
- SKILL.md with invalid YAML frontmatter
- SKILL.md missing required fields
- Circular plugin dependencies (not applicable here)
- Plugin name conflicts with built-in skills
- Invalid semantic version format (e.g., "v1.0", "1.0.0.0")
- Description exceeding 1024 character limit
- Skill name with uppercase letters or spaces
- Missing scripts/ directory in skill

## Acceptance Criteria

- [ ] `.claude-plugin/marketplace.json` exists and validates against Claude Code schema
- [ ] Two plugin manifests (`plugin.json`) exist and validate against schema
- [ ] Directory structure follows `plugins/<name>/skills/<name>/` pattern
- [ ] Both SKILL.md files include `allowed-tools` and `version` frontmatter fields
- [ ] All existing scripts execute without modification (`uv run` still works)
- [ ] Validation tests pass (`pytest tests/` returns 0 exit code)
- [ ] Validation script passes (`bash scripts/validate-plugins.sh` returns 0)
- [ ] GitHub Actions CI workflow runs validation on every commit
- [ ] README.md includes marketplace installation instructions
- [ ] CONTRIBUTING.md exists with plugin development guidelines
- [ ] LICENSE file exists (MIT recommended)
- [ ] Manual installation test succeeds (plugin installs via `/plugin install`)
- [ ] Skills activate correctly after installation
- [ ] Old `skill-*` directories are removed or deprecated
- [ ] No hardcoded paths broken by directory migration

## Validation Commands

```bash
# Validate marketplace schema
pytest tests/test_marketplace_schema.py -v

# Validate plugin structure
bash scripts/validate-plugins.sh

# Test script execution (no API calls required for help)
uv run plugins/web-access/skills/web-access/scripts/search.py --help
uv run plugins/kalshi-markets/skills/kalshi-markets/scripts/market.py --help

# Validate YAML frontmatter syntax
python -c "import yaml; yaml.safe_load(open('plugins/web-access/skills/web-access/SKILL.md').read().split('---')[1])"

# Run all tests
pytest tests/ -v

# Check for broken imports (none expected due to inline dependencies)
python -m py_compile plugins/*/skills/*/scripts/*.py
```

## Notes

### Migration Strategy
The migration follows a non-breaking approach:
1. Create new structure first (plugins/)
2. Test new structure thoroughly
3. Deprecate old structure (skill-*)
4. Remove old structure after confirmation

### Backward Compatibility
- All existing `uv run skill-*/scripts/*.py` commands continue working during migration
- Scripts use PEP 723 inline dependencies, so no requirements.txt updates needed
- No code changes required in Python scripts (paths are relative)

### Future Considerations
- **Plugin versioning**: Use semantic versioning for coordinated updates
- **Dependency pinning**: Consider pinning httpx, click versions in PEP 723 headers
- **Additional skills**: Framework supports easy addition of new skills
- **MCP server integration**: Could add MCP server support for advanced integrations
- **Testing infrastructure**: Could add integration tests that make real API calls (with test keys)

### Patterns Discovered by Codebase-Analyst
1. **Consistency wins**: Both skills follow identical patterns, making migration straightforward
2. **Self-contained benefits**: No shared library means no import path breakage
3. **Documentation-driven**: SKILL.md serves as both docs and skill manifest
4. **PEP 723 advantages**: Inline dependencies eliminate requirements.txt synchronization issues

## Execution

This spec can be implemented using: `/sdlc:implement docs/specs/plugin-marketplace-migration.md`

The implementation will:
1. Create Archon project for task tracking
2. Break down into granular tasks (30 min - 4 hours each)
3. Execute tasks sequentially with validation
4. Run sdlc:validator agent automatically after implementation
5. Generate comprehensive test suite
6. Validate all acceptance criteria
