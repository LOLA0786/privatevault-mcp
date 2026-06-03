# PrivateVault MCP

**Cognitive Runtime Security & Decision Security Control Plane for AI Agents**

The industry-standard MCP server that brings PrivateVault governance, trust scoring, policy enforcement, and audit to Claude Desktop, Cursor, LangGraph, CrewAI, and OpenAI Agents.

> **Grok may allow subtle mutations. PrivateVault MCP blocks them at the execution gate.**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org)
[![FastMCP](https://img.shields.io/badge/MCP-FastMCP-brightgreen)](https://modelcontextprotocol.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-OpenAPI-success)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-Apache%202.0-green)](LICENSE)

## Features

- **4 Production MCP Tools**: `scan_context`, `policy_check`, `audit_action`, `risk_score`
- **CognitiveExecutionKernel**: Risk-tiered thresholds, 4-pillar trust breakdown (intent stability, memory integrity, authority lineage, retrieval confidence), dynamic Merkle + latent drift detection
- **Non-bypassable AIFirewall** with pattern blocking and capability scoping
- **PostgreSQL-backed Audit Ledger** with immutable records
- **Real xAI/Grok Integration** (messages payload, robust fallback)
- **MCP Compliant** — works natively in Claude Desktop, Cursor, Windsurf, etc.
- **Async FastAPI** server with OpenAPI docs, structured logging (`structlog`), Pydantic v2
- **Dockerized** (with Postgres) + GitHub Actions CI
- **Zero regression** when disabled (additive only)

## Quick Start

```bash
git clone https://github.com/LOLA0786/privatevault-mcp.git
cd privatevault-mcp
cp .env.example .env  # Add XAI_API_KEY
docker compose up -d
# or
pip install -e .
privatevault-mcp
```

**Claude Desktop / Cursor**: See `docs/claude-desktop-setup.md` and `docs/cursor-setup.md`.

## MCP Tools

### 1. `scan_context(context_text: str)`
Scans for prompt injection, suspicious patterns, and risk.

**Output**:
```json
{
  "risk_score": 85,
  "prompt_injection_detected": true,
  "suspicious_patterns": ["base64 encoded payload", "system override"],
  "recommendation": "block"
}
```

### 2. `policy_check(action: str, context: dict)`
Enforces enterprise policies with full PrivateVault kernel.

### 3. `audit_action(agent_id: str, action: str, context_hash: str)`
Records immutable audit with Merkle proof.

### 4. `risk_score(context: dict, action: str)`
Returns 4-pillar trust breakdown + severity.

See full examples in `docs/examples/`.

## Architecture

```mermaid
graph TD
    A[AI Agent (Claude/Cursor/LangGraph)] --> B[MCP Client]
    B --> C[PrivateVault MCP Server]
    C --> D[CognitiveExecutionKernel]
    D --> E[AIFirewall + Policy Engine]
    E --> F[Merkle Ledger + Postgres Audit]
    F --> G[xAI/Grok Decision Layer]
    G --> H[Structured Audit + Replay]
```

## Setup Guides

- [Claude Desktop](docs/claude-desktop-setup.md)
- [Cursor](docs/cursor-setup.md)
- [Docker](docker-compose.yml)
- [Example Agent Integration](docs/examples/agent_integration.py)

## Development

```bash
# Install
pip install -e ".[test]"

# Run tests
pytest

# Run server
uvicorn privatevault_mcp.api.main:app --reload

# Docker
docker compose up --build
```

**Production Ready** — Clean, secure, observable, and impressive for enterprise pilots.

---

**Next Milestones (v0.2)**: Redis cache, multi-tenant, advanced red-team scenarios, SDK clients for LangGraph/CrewAI.

Built with ❤️ for autonomous agent safety.
EOF