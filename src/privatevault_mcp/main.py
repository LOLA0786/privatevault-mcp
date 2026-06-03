"""
Entry point for PrivateVault MCP server.
Supports both CLI and direct run.
"""
import typer
import uvicorn
from rich.console import Console
from rich.panel import Panel
from .api.main import app

console = Console()
app_cli = typer.Typer()

@app_cli.command()
def run(port: int = 8000, reload: bool = False):
    """Start the PrivateVault MCP server."""
    console.print(Panel.fit(
        "[bold cyan]PrivateVault MCP[/bold cyan]\n"
        "[white]Cognitive Runtime Security Control Plane[/white]\n\n"
        "MCP Tools ready for Claude Desktop, Cursor, LangGraph, CrewAI.\n"
        "OpenAPI at http://localhost:8000/docs",
        title="🚀 Starting PrivateVault MCP",
        border_style="bright_blue"
    ))

    uvicorn.run(
        "privatevault_mcp.api.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level="info"
    )

def main():
    app_cli()

if __name__ == "__main__":
    main()
EOF