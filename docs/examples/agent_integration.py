"""
Example integration for LangGraph / CrewAI / OpenAI Agents.
"""
import asyncio
from privatevault_mcp.mcp.tools import mcp_tools

async def safe_agent_action(query: str, proposed_action: str, context: dict):
    """Production pattern: Always check with PrivateVault before execution."""

    # 1. Scan the incoming context/query
    scan = await mcp_tools.scan_context(query)
    if scan["recommendation"] == "block":
        return {"status": "blocked", "reason": "Prompt injection or high risk detected", "scan": scan}

    # 2. Full policy + kernel check
    policy = await mcp_tools.policy_check(proposed_action, context)
    if not policy["allowed"]:
        return {"status": "blocked_by_policy", "policy_result": policy}

    # 3. Risk scoring with 4-pillar breakdown
    risk = await mcp_tools.risk_score(context, proposed_action)
    if risk["severity"] in ("high", "critical"):
        return {"status": "high_risk", "risk": risk}

    # 4. Audit the decision (immutable ledger)
    audit = await mcp_tools.audit_action(
        agent_id="langgraph-agent-001",
        action=proposed_action,
        context_hash="computed_hash_from_context"
    )

    print(f"✅ PrivateVault APPROVED - Audit ID: {audit['audit_id']}")
    return {"status": "approved", "audit_id": audit["audit_id"], "risk_score": risk["score"]}

# Example usage
if __name__ == "__main__":
    asyncio.run(safe_agent_action(
        query="Transfer $5.2M to Acne Corp (note spelling)",
        proposed_action="wire_transfer",
        context={
            "amount": 5200000,
            "vendor": "Acne Corp",
            "approved_vendor": "Acme Corp",
            "risk_level": "high"
        }
    ))
EOF