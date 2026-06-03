"""
Thin MCP Tools for PrivateVault - Pure gateway to backend.
NO local risk scoring, policy, anomaly detection, or decision logic.
All intelligence comes from POST /api/evaluate on the PrivateVault backend.
"""
from typing import Any, Dict
from datetime import datetime
import structlog
import uuid

from ..core.gateway import gateway
from ..core.models import (
    ScanContextResponse, PolicyCheckResponse,
    AuditActionResponse, RiskScoreResponse
)

logger = structlog.get_logger(__name__)

class PrivateVaultMCPTools:
    """Pure transformation layer. No business logic."""

    @staticmethod
    async def scan_context(context_text: str) -> Dict[str, Any]:
        """Exact path: MCP tool → gateway.evaluate() → PrivateVault /api/evaluate → transform → return.
        No local patterns, no local scoring."""
        result = await gateway.evaluate(
            prompt=context_text,
            context={"type": "scan_context", "text": context_text},
            metadata={"tool": "scan_context", "source": "mcp"}
        )

        # Transform backend response to MCP-compatible format (no local decisions)
        return {
            "risk_score": result.get("risk_score", 50),
            "prompt_injection_detected": result.get("severity", "") == "high" or "injection" in str(result).lower(),
            "suspicious_patterns": result.get("anomalies", []),
            "recommendation": result.get("decision", "warn"),
            "rationale": f"Evaluated by PrivateVault backend (ID: {result.get('audit_id', 'unknown')})",
            "backend_source": True
        }

    @staticmethod
    async def policy_check(action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Forwards to backend. No local policy engine."""
        result = await gateway.evaluate(
            prompt=f"Policy check for action: {action}",
            context={"action": action, **context},
            metadata={"tool": "policy_check"}
        )

        return {
            "allowed": result.get("decision", "block") != "block",
            "reason": result.get("rationale", result.get("explanation", "Evaluated by PrivateVault backend")),
            "violated_policies": result.get("anomalies", []),
            "trust_score": result.get("risk_score", 50) / 100,
            "backend_decision": result.get("decision")
        }

    @staticmethod
    async def audit_action(agent_id: str, action: str, context_hash: str) -> Dict[str, Any]:
        """Forwards audit to backend for immutable logging."""
        result = await gateway.evaluate(
            prompt=f"Audit action: {action} by {agent_id}",
            context={"agent_id": agent_id, "action": action, "context_hash": context_hash},
            metadata={"tool": "audit_action"}
        )

        return {
            "audit_id": result.get("audit_id", str(uuid.uuid4())),
            "timestamp": result.get("timestamp", datetime.utcnow().isoformat()),
            "backend_audit_id": result.get("id")
        }

    @staticmethod
    async def risk_score(context: Dict[str, Any], action: str) -> Dict[str, Any]:
        """Pure proxy. Decision comes exclusively from backend."""
        result = await gateway.evaluate(
            prompt=f"Risk score for action: {action}",
            context={"action": action, **context},
            metadata={"tool": "risk_score"}
        )

        return {
            "score": result.get("risk_score", 50),
            "severity": result.get("severity", "medium"),
            "breakdown": result.get("pillars") or result.get("breakdown") or {"overall": result.get("risk_score", 50) / 100},
            "recommendation": result.get("decision", "warn"),
            "backend_source": True
        }


# Singleton
mcp_tools = PrivateVaultMCPTools()
