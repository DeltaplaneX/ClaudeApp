# Claude MCP Configuration

## Apify MCP Integration

This project uses the Apify MCP server integration to provide access to:
- Actors
- Documentation
- RAG Web Browser (`apify/rag-web-browser`)
- Website Content Crawler (`apify/website-content-crawler`)

### Setup

To use the Apify MCP integration, you need to set the `APIFY_API_TOKEN` environment variable with your Apify API token.

#### Setting the Environment Variable

**Linux/macOS:**
```bash
export APIFY_API_TOKEN="your-apify-api-token-here"
```

**Windows (PowerShell):**
```powershell
$env:APIFY_API_TOKEN="your-apify-api-token-here"
```

**Windows (Command Prompt):**
```cmd
set APIFY_API_TOKEN=your-apify-api-token-here
```

#### Making it Permanent

To make the environment variable persistent:

**Linux/macOS:**
Add the export command to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
echo 'export APIFY_API_TOKEN="your-apify-api-token-here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
1. Open System Properties > Environment Variables
2. Add a new user or system variable named `APIFY_API_TOKEN`
3. Set the value to your API token

### Configuration Details

The MCP server configuration is located in `.claude/mcp.json`:
- **URL:** `https://mcp.apify.com/?tools=actors,docs,apify/rag-web-browser,apify/website-content-crawler`
- **Transport:** HTTP
- **Authentication:** Bearer token via Authorization header
