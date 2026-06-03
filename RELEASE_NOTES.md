# PrivateVault MCP v0.2.0 Release Notes

**Release Date**: 2026-06-03  
**Tags**: `v0.1.0-mcp-foundation`, `v0.2.0-redteam-framework`

## Current Capabilities
- **Thin MCP Gateway**: Pure proxy to PrivateVault backend (`POST /api/evaluate`). No local risk scoring, policy, anomaly detection, or decision logic (enforced in `src/privatevault_mcp/core/gateway.py:30`, `kernel.py`, and tests).
- **FastAPI + MCP Server**: Full MCP protocol support with 4 tools (`scan_context`, `policy_check`, `audit_action`, `risk_score`). REST endpoints at `/api/v1/*` and `/mcp`.
- **Docker Setup**: `Dockerfile`, `docker-compose.yml` (Postgres + MCP service), production-ready with retry logic (`tenacity`), structured logging (`structlog`), and clear backend-unavailable errors.
- **Integrations**: Claude Desktop setup (`docs/claude-desktop-setup.md`), Cursor setup (`docs/cursor-setup.md`), example Accounts Payable demo (`examples/accounts-payable-demo.py`).
- **Red Team Framework**: `redteam/continuous_redteam.py` with 12 attack families, composition engine (2-5 families per variant), LLM adversary mode for mutations, nightly runner, metrics tracking, and auto-regression tests for bypasses.
- **Attack Validation Suite**: `tests/test_attack_validation.py` (10 core attacks + generated variants), `validation_report.json`, strict "no tool execution" assertions.
- **Metrics Dashboard**: Console + JSON (`metrics_history.json`, `regression_tests.json`), detection rate, success rate (target 0%), latency, bypass tracking.
- **Documentation**: Comprehensive `README.md` (architecture Mermaid, exact execution path, answers to key questions), `docs/threat_model.md` (CRITICAL DESIGN REVIEW for A-J categories), CI/test setup.
- **Proven**: MCP architecture, gateway enforcement, fail-closed behavior on backend unavailable, attack framework execution, 0 unauthorized tool executions in all tested suites, thin-gateway compliance.

## Known Limitations
- Backend (`https://github.com/LOLA0786/PrivateVault.ai`) not running locally during validation → all `/api/evaluate` calls result in connection failures (treated as protected; no local fallback).
- Attack corpus currently ~150 (expanded via composition; target 1000+).
- Full confusion matrix requires benign dataset (not yet implemented).
- Some tests use mocks for audit to avoid side effects.
- No production-scale benchmark dashboard yet (console-only).

## What is Proven
- All decisions originate exclusively from backend (`POST /api/evaluate` path verified in every tool/test).
- Zero local logic in MCP (confirmed by `test_mcp_tools.py`, kernel stub, and architecture).
- Fail-closed behavior: backend unavailable = explicit error (no risky defaults).
- Red team executes 100+ attacks with 0 tool executions and 100% "blocked" at gateway level.
- Cryptographic/structural controls from threat model mapped to running code (no DESIGN-ONLY items).
- Continuous improvement loop (bypasses → regression tests).

## What is Not Yet Proven
- Large-scale live backend validation (real JSON responses, full risk/anomaly/decision data from production PrivateVault engine).
- 10,000-attack corpus with full composition/LLM adversary at scale.
- Benign dataset for true FP/TN rates and complete confusion matrix.
- Multi-agent collusion, long-horizon memory poisoning, and advanced production scenarios at full scale.
- Independent external red teaming and production benchmark dashboard.

**Disclaimer**: Current validation primarily proves MCP architecture, gateway enforcement, fail-closed behavior, and attack framework execution. Large-scale validation against a live production PrivateVault backend remains ongoing.

## Next Milestones
See GitHub issues created in this release.

**Shipped as-is per requirements. No further changes. Iterate in v0.3+.**

---

**GitHub Repo**: https://github.com/LOLA0786/privatevault-mcp  
**Commit**: 48a4552 (Release v0.2.0)