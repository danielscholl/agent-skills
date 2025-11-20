# Agent Tools Plugin

Essential web tools for AI agents including semantic search and content fetching using Brave Search API.

## Overview

This plugin provides two core capabilities for web access:
- **Web Search**: Semantic search using Brave Search API with AI-powered result summaries
- **Web Fetch**: HTML-to-markdown conversion for clean content extraction

## Installation

```bash
/plugin install agent-tools@agent-skills
```

## Available Scripts

### search.py - Web Search

Search the web using Brave Search API with AI-powered result summarization.

**Features:**
- Semantic search with relevance ranking
- AI-generated result summaries
- Query rewriting for better results
- Configurable result count (max 20)

**Usage:**
```bash
script_run web search --query "Claude Code plugins" --json
script_run web search --query "python tutorials" --count 10 --json
```

**Options:**
- `--query TEXT` - Search query (required)
- `--count INTEGER` - Number of results, max 20 (default: 10)
- `--json` - Output as JSON instead of human-readable format

### fetch.py - Web Content Fetching

Fetch web pages and convert HTML to clean markdown format.

**Features:**
- HTML-to-markdown conversion
- Automatic content cleaning
- Link preservation
- Image alt text extraction

**Usage:**
```bash
script_run web fetch --url "https://example.com" --json
script_run web fetch --url "https://docs.anthropic.com/claude/docs" --json
```

**Options:**
- `--url TEXT` - URL to fetch (required)
- `--json` - Output as JSON instead of human-readable format

## Configuration

### Required Environment Variables

**BRAVE_API_KEY** - Get your API key from [Brave Search API](https://brave.com/search/api/)

Set in your shell profile:
```bash
export BRAVE_API_KEY="your-brave-api-key-here"
```

### API Access

- **Service**: Brave Search API
- **Pricing**: Free tier available, paid tiers for higher volume
- **Rate Limits**: Subject to Brave API plan limits

## Use Cases

### Web Search

- Find current information beyond knowledge cutoff
- Research recent news or events
- Discover online resources and documentation
- Get AI-powered summaries of search results

### Web Fetch

- Extract clean text from documentation pages
- Convert blog posts to markdown
- Fetch article content for analysis
- Retrieve structured content from web pages

## Examples

### Research Assistant

```bash
# Find recent AI news
script_run web search --query "AI breakthroughs 2025" --json

# Fetch specific documentation
script_run web fetch --url "https://docs.example.com/api" --json
```

### Content Analysis

```bash
# Search for technical articles
script_run web search --query "rust async programming" --count 5 --json

# Extract article content
script_run web fetch --url "https://blog.example.com/async-rust" --json
```

### Current Events

```bash
# Find latest news
script_run web search --query "tech news today" --json

# Get specific news article
script_run web fetch --url "https://news.example.com/article" --json
```

## Technical Details

### Dependencies

All scripts use PEP 723 inline dependencies (auto-installed by UV):
- `httpx` - HTTP client for API calls
- `click` - CLI framework
- `markdownify` - HTML-to-markdown conversion (fetch.py)

### Script Architecture

- **Self-Contained**: Each script declares its own dependencies
- **Context Managers**: HTTP clients use proper lifecycle management
- **Error Handling**: Graceful failures with helpful error messages
- **Dual Output**: JSON mode for automation + human-readable default

### Output Format

**JSON Mode** (`--json` flag):
```json
{
  "query": "python tutorials",
  "results": [
    {
      "title": "Learn Python - Free Interactive Python Tutorial",
      "url": "https://www.learnpython.org/",
      "description": "LearnPython.org is a free interactive Python tutorial...",
      "age": "2024-01-15"
    }
  ]
}
```

**Human-Readable Mode** (default):
```
Search Results for: python tutorials

1. Learn Python - Free Interactive Python Tutorial
   URL: https://www.learnpython.org/
   LearnPython.org is a free interactive Python tutorial...
   Age: 2024-01-15
```

## Limitations

### Search Limitations

- **Max Results**: 20 results per query (Brave API limit)
- **Rate Limits**: Subject to your Brave API plan
- **No Image Search**: Text search only
- **No Filtering**: Can't filter by date range or domain (use query syntax)

### Fetch Limitations

- **HTML Only**: Won't work with JavaScript-heavy single-page apps
- **Public Pages**: No authentication support for protected content
- **Size Limits**: Very large pages may timeout
- **Rendering**: No JavaScript execution (gets raw HTML)

## Troubleshooting

### "Missing BRAVE_API_KEY"

Set the environment variable:
```bash
export BRAVE_API_KEY="your-api-key"
```

Verify it's set:
```bash
echo $BRAVE_API_KEY
```

### API Rate Limit Errors

You've exceeded your Brave API plan limits. Solutions:
- Wait for rate limit reset (usually 1 minute)
- Upgrade your Brave API plan
- Reduce search frequency

### Fetch Returns Empty Content

The target page likely uses JavaScript for content rendering. Try:
- Checking the URL loads in a browser
- Looking for alternative documentation URLs
- Using search instead to find better sources

### Connection Timeouts

- Check your internet connection
- Verify the target URL is accessible
- Try again in a few moments

## Best Practices

### Search Queries

- **Be Specific**: "Claude Code plugin tutorial" vs "plugins"
- **Use Quotes**: "exact phrase match" for precise results
- **Recent Content**: Add "2025" or "latest" for current information
- **Limit Results**: Use `--count` to get just what you need

### Fetching Content

- **Verify URLs**: Check URLs are valid before fetching
- **Documentation Sites**: Work best (static HTML content)
- **Check robots.txt**: Be respectful of site policies
- **Rate Limiting**: Don't fetch too many pages in quick succession

## Privacy & Security

- **API Key Security**: Never commit BRAVE_API_KEY to version control
- **Request Privacy**: All requests go through Brave Search (see their privacy policy)
- **No Data Storage**: Scripts don't store search results or fetched content
- **HTTPS Only**: All API calls use secure connections

## Additional Resources

- **Brave Search API**: https://brave.com/search/api/
- **API Documentation**: https://api.search.brave.com/app/documentation
- **Pricing**: https://brave.com/search/api/#pricing

## License

MIT License - See [LICENSE](../../LICENSE) for details.
