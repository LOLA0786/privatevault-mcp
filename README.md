# PrivateVault MCP — Pre-Execution Policy Enforcement for AI Agents

Stop AI agents *before* they execute a bad action — not after.

PrivateVault MCP is a Model Context Protocol server that places a runtime
decision firewall between any MCP-capable agent (Claude Desktop, Cursor,
OpenAI Agents, LangGraph, CrewAI) and the tools it calls. Every sensitive
action is evaluated against policy, trust, and context-integrity checks
before execution, and every decision is recorded in a tamper-evident
audit ledger.
Agent → MCP tool call → PrivateVault evaluate → ALLOW / WARN / BLOCK → tool executes (or never does)

## Why this exists

Provenance tells you what you installed. It cannot tell you whether an
agent is about to chain individually legitimate tools and poisoned
context into a $5.2M wire transfer. Scanning happens after context
assembly; enforcement has to happen before execution. This server is
the enforcement point.

## 60-second demo

An accounts-payable agent receives a poisoned invoice instructing a
$5.2M transfer to "Acne Corp":
PRIVATEVAULT_URL=http://localhost:8001 python examples/accounts-payable-demo.py

What you'll see, with real request/response logs (no mocks, no screenshots):
1. scan_context() and policy_check() intercept the action
2. Backend returns {"decision": "block", "risk_score": 87, "severity": "high"}
3. transfer_funds() never executes
4. An immutable audit record is written

## Security model (read this if you're a security reviewer)

This server intentionally contains **zero** local decision logic — no
risk scoring, no policy evaluation, no injection detection. It is a
thin, authenticated gateway to the PrivateVault decision engine
(`POST /api/evaluate`), which is the single source of truth for every
ALLOW / WARN / BLOCK.

- If the backend is unreachable, the server fails **closed** with a 502.
  No silent fallback, no local guessing.
- Sole evaluation path: `src/privatevault_mcp/core/gateway.py`
- Full execution path for every tool call is documented in
  [docs/execution-path.md](docs/execution-path.md)

This is deliberate: an enforcement point that can be made to decide
locally is an enforcement point that can be subverted locally.

## Quick start
git clone https://github.com/privatevault-ai/privatevault-mcp.git
cd privatevault-mcp
cp .env.example .env   # set PRIVATEVAULT_URL and PRIVATEVAULT_API_KEY
docker compose up -d
curl http://localhost:8000/health

Setup guides: [Claude Desktop](docs/claude-desktop-setup.md) ·
[Cursor](docs/cursor-setup.md) ·
[Agent integration example](docs/examples/agent_integration.py)

## MCP tools exposed

| Tool | Purpose |
|---|---|
| `scan_context` | Context-integrity and injection evaluation before the agent acts |
| `policy_check` | Pre-execution authorization for a proposed tool call |

## Status

Results to date were demonstrated under controlled conditions; the
engine targets sub-2ms enforcement decisions with Merkle-chained audit
trails and deterministic replay. Red-team scenarios live in `redteam/`.

Built by [PrivateVault](https://privatevault.ai) — Decision Security
Engineering for autonomous AI.
