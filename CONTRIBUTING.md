# Contributing to Agent Skills Marketplace

Thank you for your interest in contributing to the Agent Skills Marketplace! This document provides guidelines for adding new plugins and skills to the marketplace.

## Table of Contents

- [Quick Start](#quick-start)
- [Plugin Development Guidelines](#plugin-development-guidelines)
- [Directory Structure](#directory-structure)
- [Plugin Manifest (plugin.json)](#plugin-manifest-pluginjson)
- [Skill Manifest (SKILL.md)](#skill-manifest-skillmd)
- [Script Requirements](#script-requirements)
- [Testing](#testing)
- [Submission Process](#submission-process)

## Quick Start

1. Fork the repository
2. Create a new plugin directory: `plugins/your-plugin-name/`
3. Add plugin manifest, skills, and scripts
4. Run validation: `bash scripts/validate-plugins.sh`
5. Submit a pull request

## Plugin Development Guidelines

### Naming Conventions

- **Plugin names**: lowercase-with-hyphens (e.g., `web-access`, `kalshi-markets`)
- **Skill names**: lowercase-with-hyphens, max 64 characters
- **Script files**: lowercase with `.py` extension (e.g., `search.py`, `market.py`)
- **Classes**: PascalCase (e.g., `BraveSearchClient`, `KalshiClient`)
- **Functions**: snake_case (e.g., `format_result`, `fetch_data`)

### Code Style

- Use PEP 8 for Python code
- Include type hints where helpful
- Add docstrings for classes and non-trivial functions
- Keep scripts self-contained and focused on single responsibilities

## Directory Structure

Follow this structure for all plugins:

```
plugins/
└── your-plugin-name/
    ├── plugin.json              # Plugin metadata
    └── skills/
        └── your-skill-name/
            ├── SKILL.md         # Skill manifest
            └── scripts/         # Executable scripts
                ├── script1.py
                └── script2.py
```

### Multi-Skill Plugins

If your plugin contains multiple related skills:

```
plugins/
└── your-plugin-name/
    ├── plugin.json
    └── skills/
        ├── skill-one/
        │   ├── SKILL.md
        │   └── scripts/
        └── skill-two/
            ├── SKILL.md
            └── scripts/
```

## Plugin Manifest (plugin.json)

Create a `plugin.json` file at the plugin root:

```json
{
  "name": "your-plugin-name",
  "displayName": "Your Plugin Display Name",
  "version": "1.0.0",
  "description": "Concise description of what your plugin does",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "url": "https://github.com/yourusername"
  },
  "keywords": [
    "keyword1",
    "keyword2",
    "keyword3"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/danielscholl/agent-base"
  },
  "license": "MIT",
  "skills": [
    "your-skill-name"
  ]
}
```

### Required Fields

- `name`: Plugin identifier (lowercase-with-hyphens)
- `displayName`: Human-readable name for UI display
- `version`: Semantic version (X.Y.Z format)
- `description`: 1-2 sentence overview
- `author`: Object with at least `name` field
- `license`: License identifier (MIT recommended)
- `skills`: Array of skill names contained in this plugin

### Semantic Versioning

Follow semver (X.Y.Z):
- **X** (major): Breaking changes
- **Y** (minor): New features, backward compatible
- **Z** (patch): Bug fixes, backward compatible

## Skill Manifest (SKILL.md)

Each skill must have a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: your-skill-name
description: Detailed description of when and how to use this skill. Include trigger conditions and use cases.
version: 1.0.0
allowed-tools: Bash, WebFetch, WebSearch
---

# your-skill-name

## 🎯 Triggers
**When user wants to:**
- Specific use case 1
- Specific use case 2

**Skip when:**
- Condition where skill shouldn't be used

## Scripts

### script1
**What:** Brief description
**Pattern:** Usage pattern
**Example:** Concrete example

## Quick Reference
```
User request → script_run your-skill-name script1 --arg value --json
```

## Requires
- Environment variables or dependencies
```

### SKILL.md Requirements

1. **YAML Frontmatter** (between `---` delimiters):
   - `name`: Skill identifier (must match directory name)
   - `description`: Max 1024 characters
   - `version`: Semantic version
   - `allowed-tools`: String or array of Claude Code tools the skill uses

2. **Triggers Section**: Clear guidance on when to use the skill

3. **Scripts Section**: Document each script with usage patterns

4. **Examples**: Concrete examples help Claude understand usage

## Script Requirements

### PEP 723 Inline Dependencies

All scripts MUST use PEP 723 inline dependencies:

```python
#!/usr/bin/env python3
"""
Script description.
"""
# /// script
# dependencies = [
#   "httpx>=0.24.0",
#   "click>=8.1.0",
# ]
# ///

import click
import httpx

# Your code here
```

### Script Structure

1. **Shebang**: `#!/usr/bin/env python3`
2. **Docstring**: Brief description of what the script does
3. **PEP 723 block**: Declare all dependencies
4. **Imports**: Standard library, then third-party
5. **Main logic**: Keep focused and modular

### CLI Interface

Use Click for command-line interfaces:

```python
@click.command()
@click.option('--query', required=True, help='Search query')
@click.option('--json', is_flag=True, help='Output JSON format')
def main(query: str, json: bool):
    """Execute the script."""
    # Implementation
```

### Dual Output Modes

Support both JSON and human-readable output:

```python
if json:
    click.echo(json.dumps(result))
else:
    click.echo(f"Formatted result: {result}")
```

### Error Handling

Handle errors gracefully:

```python
try:
    result = fetch_data(query)
except Exception as e:
    if json:
        click.echo(json.dumps({"error": str(e)}))
    else:
        click.echo(f"Error: {e}", err=True)
    sys.exit(1)
```

### Context Managers

Use context managers for resources:

```python
class MyClient:
    def __enter__(self):
        # Setup
        return self

    def __exit__(self, *args):
        # Cleanup
        pass

with MyClient() as client:
    result = client.fetch()
```

## Testing

### Validation Scripts

Run validation before submitting:

```bash
# Structure validation
bash scripts/validate-plugins.sh

# Schema validation
pytest tests/test_marketplace_schema.py -v

# Script syntax check
python -m py_compile plugins/*/skills/*/scripts/*.py
```

### Manual Testing

Test your scripts work correctly:

```bash
# Test help output
uv run plugins/your-plugin/skills/your-skill/scripts/script.py --help

# Test JSON output
uv run plugins/your-plugin/skills/your-skill/scripts/script.py --json
```

## Submission Process

1. **Fork and Branch**
   ```bash
   git checkout -b add-plugin-your-plugin-name
   ```

2. **Implement Plugin**
   - Create directory structure
   - Add plugin.json and SKILL.md
   - Write scripts with PEP 723 dependencies
   - Add comprehensive documentation

3. **Validate**
   ```bash
   bash scripts/validate-plugins.sh
   pytest tests/test_marketplace_schema.py -v
   ```

4. **Update Marketplace Manifest**

   Add your plugin to `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "your-plugin-name",
     "path": "plugins/your-plugin-name",
     "description": "Brief description"
   }
   ```

5. **Commit Changes**
   ```bash
   git add plugins/your-plugin-name
   git add .claude-plugin/marketplace.json
   git commit -m "feat: add your-plugin-name plugin"
   ```

6. **Submit Pull Request**
   - Title: `feat: add [plugin-name] plugin`
   - Description: Explain what the plugin does and why it's useful
   - Include testing evidence (screenshots, logs)

## Code Review Checklist

Before submitting, ensure:

- [ ] Plugin follows directory structure conventions
- [ ] plugin.json includes all required fields
- [ ] SKILL.md has valid YAML frontmatter with required fields
- [ ] All scripts use PEP 723 inline dependencies
- [ ] Scripts support `--json` output mode
- [ ] Scripts include `--help` documentation
- [ ] Error handling is comprehensive and user-friendly
- [ ] Validation scripts pass without errors
- [ ] README.md updated if needed
- [ ] No sensitive data (API keys, credentials) committed

## Questions?

- Open an issue for discussion
- Check existing plugins for examples
- Review ADR documents in `docs/decisions/`

Thank you for contributing to the Agent Skills Marketplace!
