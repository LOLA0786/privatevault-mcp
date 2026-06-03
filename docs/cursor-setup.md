# Cursor Setup for PrivateVault MCP

## 1. Install Cursor (with MCP support)

## 2. Configure MCP in Cursor Settings

Cursor supports MCP servers via `cursor.json` or the MCP panel.

Add the following to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "privatevault-mcp": {
      "url": "http://localhost:8000/mcp",
      "name": "PrivateVault",
      "description": "Cognitive Runtime Security for agents"
    }
  }
}
```

Or run the server locally:

```bash
cd privatevault-mcp
docker compose up -d
```

## 3. In Cursor Composer / Agent

Use natural language:

"Before writing this code or making API calls, check with PrivateVault MCP using policy_check and risk_score."

Cursor will automatically call the MCP tools and show structured results with trust scores, risk breakdown, and audit records.

**Pro tip**: Pin the PrivateVault panel for live governance during coding sessions.
EOF