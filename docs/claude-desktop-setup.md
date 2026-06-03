# Claude Desktop Setup for PrivateVault MCP

## 1. Install Claude Desktop (if not already)

## 2. Add PrivateVault MCP as a Tool Server

Create or edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "privatevault": {
      "command": "uvx",
      "args": [
        "privatevault-mcp@latest"
      ],
      "env": {
        "XAI_API_KEY": "your-key-here"
      }
    }
  }
}
```

## 3. Restart Claude Desktop

## 4. Usage in Prompts

```
Before taking any action, call the PrivateVault MCP tools:
- Use scan_context on my query
- Use policy_check on the proposed action
- Only proceed if policy_check.allowed == true
```

**Example output from PrivateVault** will appear in Claude with full trust breakdown, recommendation, and audit_id.

See `docs/examples/` for prompt templates.
EOF