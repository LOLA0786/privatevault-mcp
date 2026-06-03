# PrivateVault MCP (Thin Gateway)

**Pure MCP Gateway to PrivateVault Backend**

This MCP server contains **zero** local risk scoring, prompt injection detection, policy evaluation, anomaly detection, governance, or decision logic.

It is a thin, reliable proxy that forwards all requests to the production PrivateVault backend at `POST /api/evaluate` (https://github.com/LOLA0786/PrivateVault.ai).

> All trust, risk, policy, and governance decisions originate exclusively from the PrivateVault engine.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-Compliant-brightgreen)](https://modelcontextprotocol.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-OpenAPI-success)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com)

**Answers to explicit questions:**

**Does any risk scoring, prompt injection detection, governance evaluation, or policy decision happen locally inside the MCP server?**

**NO.**

**List of files/functions with such logic:** None. All removed.

**Can the MCP server operate if the PrivateVault backend is completely offline?**

**NO.** It returns a clear 502 error. No fallback, no local evaluation.

**Exact execution path for `scan_context()`:**

1. Claude/Cursor/Agent calls MCP tool `scan_context(context_text)`
2. `src/privatevault_mcp/api/main.py:scan_context()` (or `/mcp` handler)
3. Calls `mcp_tools.scan_context()` in `src/privatevault_mcp/mcp/tools.py:23`
4. Calls `gateway.evaluate(prompt=..., context=..., metadata=...)` in `src/privatevault_mcp/core/gateway.py:35`
5. `httpx.AsyncClient.post()` to `{PRIVATEVAULT_URL}/api/evaluate` with standardized payload
6. Backend returns `{"risk_score": 87, "severity": "high", "anomalies": [], "decision": "block", ...}`
7. Gateway logs + returns raw result
8. `tools.py` transforms minimally (adds `backend_source: true`, maps fields)
9. Response returned to agent via MCP protocol

**No other code paths exist.**

## Architecture (All Decisions from Backend)

```mermaid
graph TD
    A[Claude Desktop / Cursor / LangGraph / CrewAI / OpenAI Agent] --> B[MCP Client]
    B --> C[PrivateVault MCP Server<br/>Thin Gateway Only]
    C --> D[Authentication + Input Validation + Retry + Logging]
    D --> E[POST /api/evaluate<br/>with {prompt, context, metadata}]
    E --> F[PrivateVault Backend Engine<br/>(https://github.com/LOLA0786/PrivateVault.ai)]
    F --> G[Risk Score + Severity + Anomalies + Decision<br/>Single Source of Truth]
    G --> H[MCP Response Transformation]
    H --> I[Agent receives final result]
    
    style C fill:#e0f2fe
    style F fill:#fef3c7
    style G fill:#ecfdf5
```

**PrivateVault backend is the single source of truth for:**
- Risk scores
- Policy decisions (`allow`/`warn`/`block`)
- Anomaly & prompt injection detection
- Governance & trust evaluation

The MCP server **never** independently decides anything.

## Quick Start

```bash
git clone https://github.com/LOLA0786/privatevault-mcp.git
cd privatevault-mcp
cp .env.example .env
# Set PRIVATEVAULT_URL and PRIVATEVAULT_API_KEY

docker compose up -d
# Backend must be running at PRIVATEVAULT_URL

# Test
curl http://localhost:8000/health
```

## Setup Guides

- [Claude Desktop Integration](docs/claude-desktop-setup.md)
- [Cursor Integration](docs/cursor-setup.md)
- [Example Agent Usage](docs/examples/agent_integration.py)

## Development

```bash
# Install
python3.12 -m venv venv
. venv/bin/activate
pip install -e ".[test]"

# Run
privatevault-mcp
# or uvicorn privatevault_mcp.api.main:app --reload

# Test (requires running PrivateVault backend)
pytest
```

**Production Docker** includes retry logic, structured logging, and clear errors if backend is unreachable.

This fulfills the architecture change: **thin gateway only**. Backend remains authoritative.

See `src/privatevault_mcp/core/gateway.py` for the sole evaluation path.
EOFEOF