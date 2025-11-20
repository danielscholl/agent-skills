# Kalshi Markets Plugin

Real-time prediction market data from Kalshi, providing comprehensive market information, trading data, event series, and settlement tracking.

## Overview

This plugin provides access to Kalshi's prediction markets API with 10 specialized scripts for market data analysis. All scripts work without authentication for public market data.

## Installation

```bash
/plugin install kalshi-markets@agent-skills
```

## Available Scripts

### Status & Discovery

- **status.py** - Check if Kalshi API is operational
- **markets.py** - Browse all active markets (paginated)
- **search.py** - Fast keyword search across ~6,900 markets (uses cache)
- **events.py** - List event groups
- **series_list.py** - Browse market series templates

### Market Details

- **market.py** - Get detailed market information by ticker
- **orderbook.py** - View bid/ask prices and depth
- **trades.py** - Recent trade history across markets
- **event.py** - Event details with associated markets
- **series.py** - Series template information

## Usage

All scripts support `--json` flag for structured output:

```bash
# Check API status
script_run kalshi-markets status --json

# Search for markets (uses cache)
script_run kalshi-markets search "election" --json

# Get market details
script_run kalshi-markets market TICKER --json

# View orderbook
script_run kalshi-markets orderbook TICKER --json

# Recent trades
script_run kalshi-markets trades --limit 10 --json
```

## Important: Search Cache Behavior

### What is the cache?

The `search.py` script uses a **local cache** for fast keyword searches across all Kalshi markets.

**Why?** Kalshi has ~6,900 active markets across hundreds of series. The API doesn't provide native keyword search, so searching requires fetching all markets via pagination and filtering locally. Without caching, each search would take several minutes.

### How it works

**First Run (2-5 minutes):**
1. Fetches all series and their markets from Kalshi API
2. Builds a searchable DataFrame with ~6,900 markets
3. Saves to CSV cache: `~/.cache/kalshi-markets/kalshi_markets_YYYYMMDD_HHMM.csv`

**Subsequent Searches (instant):**
1. Loads cached CSV into memory
2. Performs local text search
3. Returns results in milliseconds

**Cache Refresh:**
- Automatically rebuilds every **6 hours** to stay current
- Manual rebuild: `script_run kalshi-markets search --rebuild-cache --json`

### Cache Location

```
~/.cache/kalshi-markets/kalshi_markets_YYYYMMDD_HHMM.csv
```

**Size**: ~5-10 MB per cache file
**Permissions**: User read/write (no root access required)

### Cache Benefits

- **Speed**: Instant searches vs minutes per query
- **API Efficiency**: One cache build serves unlimited searches
- **Comprehensive**: Search across all market titles, descriptions, and metadata
- **Offline Capable**: Works without API calls once built
- **Auto-Refresh**: Stays up-to-date with 6-hour TTL

### Trade-offs

- **Initial Wait**: First search requires 2-5 minute cache build
- **Staleness**: Cache could be up to 6 hours old
- **Disk Usage**: ~5-10 MB per cache file (old files accumulate)

**Note**: Other scripts (`markets.py`, `market.py`, etc.) make real-time API calls without caching.

## Configuration

### Environment Variables

**Optional** for public endpoints:
- `KALSHI_API_KEY` - Required only for authenticated endpoints (account data, trading)

Public market data (prices, events, series) works without API keys.

### API Access

All scripts use Kalshi's public trade API:
- **Base URL**: `https://api.elections.kalshi.com/trade-api/v2`
- **Rate Limits**: Subject to Kalshi's API rate limits
- **Authentication**: Not required for market data endpoints

## Examples

### Quick Market Discovery

```bash
# Check if Kalshi is online
script_run kalshi-markets status --json

# Find election-related markets
script_run kalshi-markets search "trump" --limit 5 --json

# Browse all markets (paginated)
script_run kalshi-markets markets --limit 10 --json
```

### Market Analysis

```bash
# Get specific market details
script_run kalshi-markets market KXNBAGAME-25NOV19HOUCLE-HOU --json

# View orderbook depth
script_run kalshi-markets orderbook KXNBAGAME-25NOV19HOUCLE-HOU --depth 5 --json

# See recent trades
script_run kalshi-markets trades --ticker KXNBAGAME-25NOV19HOUCLE-HOU --limit 10 --json
```

### Event & Series Exploration

```bash
# List recent events
script_run kalshi-markets events --limit 20 --json

# Get event details
script_run kalshi-markets event KXNBAGAME-25NOV19HOUCLE --json

# Browse series templates
script_run kalshi-markets series_list --limit 50 --json

# Get series information
script_run kalshi-markets series KXNBAGAME --json
```

## Technical Details

### Dependencies

All scripts use PEP 723 inline dependencies (auto-installed by UV):
- `httpx` - HTTP client for API calls
- `click` - CLI framework
- `pandas` - Data processing (search.py only)

### Script Architecture

- **Self-Contained**: Each script is fully independent
- **Context Managers**: HTTP clients use proper lifecycle management
- **Error Handling**: Graceful error messages for API failures
- **Dual Output**: JSON mode + human-readable formatting

### Output Format

**JSON Mode** (`--json` flag):
```json
{
  "ticker": "KXNBAGAME-25NOV19HOUCLE-HOU",
  "title": "Houston vs Cleveland Winner?",
  "last_price_dollars": "0.8000",
  "liquidity_dollars": "2442301.01"
}
```

**Human-Readable Mode** (default):
```
Market: KXNBAGAME-25NOV19HOUCLE-HOU
Title: Houston vs Cleveland Winner?
Price: $0.80 (80%)
Liquidity: $2,442,301.01
```

## Troubleshooting

### Cache Build Takes Too Long

The first `search.py` run builds a cache of all markets (2-5 minutes). This is normal and only happens once every 6 hours.

**Workaround**: Use `markets.py` for real-time browsing without cache.

### Cache Permission Errors

The cache writes to `~/.cache/kalshi-markets/`. If you see permission errors, ensure your user has write access to your home directory's `.cache` folder.

### API Rate Limits

If you see rate limit errors, wait a few minutes before retrying. Consider:
- Using cached search instead of repeated `markets.py` calls
- Reducing pagination limits
- Adding delays between script calls

### Script Not Found

Ensure the plugin is installed:
```bash
/skills  # Should show kalshi-markets
```

If not installed, reinstall:
```bash
/plugin install kalshi-markets@agent-skills
```

## Data Freshness

- **search.py**: Up to 6 hours stale (cached)
- **All other scripts**: Real-time data from Kalshi API

## Additional Resources

- **Kalshi API Docs**: https://kalshi.com
- **Market Data**: All public endpoints available without authentication
- **Contract Terms**: Each series includes links to official contract documentation

## License

MIT License - See [LICENSE](../../LICENSE) for details.
