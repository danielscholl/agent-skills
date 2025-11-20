# Agent Skills Marketplace

A curated collection of production-ready Claude Code plugins providing web access, financial market data, and more. Install skills directly through Claude Code's plugin marketplace for seamless integration.

## Available Plugins

### 🛠️ Agent Tools
Essential tools for AI agents including web search and content fetching using Brave Search API.

**Features:**
- Semantic web search with AI-powered result summaries
- HTML-to-markdown conversion for clean content extraction
- Dual output modes (JSON + human-readable)

**Scripts:**
- `search.py` - Search the web with Brave Search API
- `fetch.py` - Fetch and convert web pages to markdown

### 📈 Kalshi Markets
Real-time prediction market data from Kalshi.

**Features:**
- Market prices, odds, and orderbook data
- Event series and settlement tracking
- Comprehensive trading analytics

**Scripts:**
- `status.py` - Check Kalshi API status
- `markets.py` - Browse all markets
- `search.py` - Find markets by keyword
- `market.py` - Get detailed market information
- `orderbook.py` - View bid/ask prices
- `trades.py` - Recent trade history
- `events.py` - List event groups
- `event.py` - Event details
- `series_list.py` - Browse series templates
- `series.py` - Series information

## Installation

### Via Claude Code Marketplace

Add this marketplace to Claude Code:

```bash
/plugin marketplace add file:///path/to/agent-skills
```

Install individual plugins:

```bash
/plugin install agent-tools@agent-skills
/plugin install kalshi-markets@agent-skills
```

Verify installation:

```bash
/skills
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/danielscholl/agent-base.git
   cd agent-base/ai-examples/agent-skills
   ```

2. Run scripts directly with UV:
   ```bash
   uv run plugins/agent-tools/skills/web/scripts/search.py --query "AI news" --json
   uv run plugins/kalshi-markets/skills/kalshi-markets/scripts/market.py TICKER
   ```

## Usage

### Agent Tools Examples

Search the web:
```bash
script_run web search --query "Claude Code plugins" --json
```

Fetch a web page:
```bash
script_run web fetch --url "https://example.com" --json
```

### Kalshi Markets Examples

Check API status:
```bash
script_run kalshi-markets status --json
```

Search markets:
```bash
script_run kalshi-markets search "election" --json
```

Get market details:
```bash
script_run kalshi-markets market TICKER --json
```

View orderbook:
```bash
script_run kalshi-markets orderbook TICKER --json
```

## Configuration

### Environment Variables

**Agent Tools** requires:
- `BRAVE_API_KEY` - Get from [Brave Search API](https://brave.com/search/api/)

**Kalshi Markets** requires:
- `KALSHI_API_KEY` - Get from [Kalshi](https://kalshi.com) (optional for public endpoints)

Set in your shell profile:
```bash
export BRAVE_API_KEY="your-brave-api-key"
export KALSHI_API_KEY="your-kalshi-api-key"
```

## Development

### Requirements

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) package manager
- jq (for validation scripts)

### Project Structure

```
agent-skills/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog
├── plugins/
│   ├── agent-tools/
│   │   ├── plugin.json           # Plugin metadata
│   │   └── skills/
│   │       └── web/
│   │           ├── SKILL.md      # Skill manifest
│   │           └── scripts/      # Python scripts
│   └── kalshi-markets/
│       ├── plugin.json
│       └── skills/
│           └── kalshi-markets/
│               ├── SKILL.md
│               └── scripts/
├── tests/
│   └── test_marketplace_schema.py
├── scripts/
│   └── validate-plugins.sh
└── docs/
    ├── decisions/                # Architecture Decision Records
    └── specs/                    # Feature specifications
```

### Validation

Run validation tests before committing:

```bash
# Validate directory structure and manifests
bash scripts/validate-plugins.sh

# Run schema validation tests
pytest tests/test_marketplace_schema.py -v

# Check script syntax
python -m py_compile plugins/*/skills/*/scripts/*.py
```

### Adding New Plugins

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Plugin directory structure
- Manifest requirements (plugin.json, SKILL.md)
- Script conventions (PEP 723 dependencies, CLI patterns)
- Testing and validation
- Submission process

## Architecture

### Design Decisions

- **PEP 723 Inline Dependencies**: All scripts declare dependencies inline for portability ([ADR-001](docs/decisions/ADR-001-pep723-dependencies.md))
- **Plugin Structure**: Plugins contain skills subdirectories for extensibility ([ADR-002](docs/decisions/ADR-002-plugin-structure.md))

### Key Patterns

- **Self-Contained Scripts**: Each script is fully independent with embedded dependencies
- **Dual Output Modes**: All scripts support `--json` for automation + human-readable default
- **Context Manager Pattern**: HTTP clients use `__enter__`/`__exit__` lifecycle
- **Structured Error Handling**: Consistent try/except with typed error responses

## Testing

### Unit Tests

```bash
pytest tests/ -v
```

### Integration Tests

```bash
# Test web search (requires BRAVE_API_KEY)
uv run plugins/agent-tools/skills/web/scripts/search.py --query "test" --json

# Test Kalshi status (no API key required)
uv run plugins/kalshi-markets/skills/kalshi-markets/scripts/status.py --json
```

### CI/CD

GitHub Actions automatically validates:
- Marketplace manifest schema
- Plugin manifest schemas
- SKILL.md frontmatter
- Directory structure
- Script syntax

See [.github/workflows/validate-plugins.yml](.github/workflows/validate-plugins.yml)

## Troubleshooting

### Plugin Installation Fails

1. Verify marketplace URL is correct
2. Check plugin directory structure matches spec
3. Validate manifests: `bash scripts/validate-plugins.sh`

### Script Execution Errors

1. Ensure UV is installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Check environment variables are set
3. Verify script has correct PEP 723 dependencies
4. Run with `--help` to see required arguments

### Validation Failures

1. Check JSON syntax in manifest files
2. Verify YAML frontmatter in SKILL.md
3. Ensure all required fields are present
4. Run validation script for detailed errors

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- **Issues**: [GitHub Issues](https://github.com/danielscholl/agent-base/issues)
- **Discussions**: [GitHub Discussions](https://github.com/danielscholl/agent-base/discussions)
- **Documentation**: See [docs/](docs/) directory

## Acknowledgments

Built with:
- [UV](https://docs.astral.sh/uv/) - Fast Python package manager
- [Click](https://click.palletsprojects.com/) - CLI framework
- [httpx](https://www.python-httpx.org/) - HTTP client
- [Brave Search API](https://brave.com/search/api/) - Web search
- [Kalshi API](https://kalshi.com) - Prediction market data
