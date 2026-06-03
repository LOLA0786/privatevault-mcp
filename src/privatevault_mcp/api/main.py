"""
FastAPI server for PrivateVault MCP with OpenAPI docs.
Exposes both REST endpoints and MCP protocol compatibility.
"""
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import structlog
from contextlib import asynccontextmanager
from typing import Dict, Any

from ..core.models import (
    ScanContextRequest, ScanContextResponse,
    PolicyCheckRequest, PolicyCheckResponse,
    AuditActionRequest, AuditActionResponse,
    RiskScoreRequest, RiskScoreResponse
)
from ..mcp.tools import mcp_tools
from ..core.gateway import gateway

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("privatevault_mcp_startup", status="ready", version="0.2.0", mode="thin_gateway")
    yield
    await gateway.client.aclose()
    logger.info("privatevault_mcp_shutdown")

app = FastAPI(
    title="PrivateVault MCP (Thin Gateway)",
    description="Pure gateway to PrivateVault backend (https://github.com/LOLA0786/PrivateVault.ai). "
                "NO local risk scoring, policy, or decision logic. All evaluation via POST /api/evaluate.",
    version="0.2.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1", tags=["privatevault"])

@router.post("/scan-context", response_model=ScanContextResponse)
async def scan_context(request: ScanContextRequest):
    """MCP Tool: Forwards to PrivateVault backend ONLY. No local logic."""
    try:
        return await mcp_tools.scan_context(request.context_text)
    except Exception as e:
        logger.error("scan_context_failed", error=str(e))
        raise HTTPException(status_code=502, detail=f"PrivateVault backend unavailable: {str(e)}")

@router.post("/policy-check", response_model=PolicyCheckResponse)
async def policy_check(request: PolicyCheckRequest):
    try:
        return await mcp_tools.policy_check(request.action, request.context)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/audit-action", response_model=AuditActionResponse)
async def audit_action(request: AuditActionRequest):
    try:
        return await mcp_tools.audit_action(request.agent_id, request.action, request.context_hash)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/risk-score", response_model=RiskScoreResponse)
async def risk_score(request: RiskScoreRequest):
    try:
        return await mcp_tools.risk_score(request.context, request.action)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

app.include_router(router)

# MCP compatibility endpoint (JSON-RPC style for Claude Desktop / Cursor)
@app.post("/mcp")
async def mcp_handler(payload: Dict[str, Any]):
    """MCP protocol handler - routes everything to backend via gateway."""
    method = payload.get("method", "")
    params = payload.get("params", {})

    try:
        if method == "scan_context" or method == "scanContext":
            return await mcp_tools.scan_context(params.get("context_text", params.get("text", "")))
        elif method in ("policy_check", "policyCheck"):
            return await mcp_tools.policy_check(
                params.get("action", ""), params.get("context", {})
            )
        elif method in ("audit_action", "auditAction"):
            return await mcp_tools.audit_action(
                params.get("agent_id", "unknown"),
                params.get("action", ""),
                params.get("context_hash", params.get("hash", ""))
            )
        elif method in ("risk_score", "riskScore"):
            return await mcp_tools.risk_score(
                params.get("context", {}), params.get("action", "")
            )
        else:
            return {"error": f"Unknown method: {method}", "supported_tools": ["scan_context", "policy_check", "audit_action", "risk_score"]}
    except Exception as e:
        logger.error("mcp_handler_error", method=method, error=str(e))
        return {"error": f"Backend unavailable: {str(e)}", "status": "error"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "privatevault-mcp",
        "mode": "thin_gateway",
        "backend": gateway.base_url,
        "mcp_tools": 4,
        "note": "All decisions come from PrivateVault /api/evaluate. No local logic."
    }

@app.get("/")
async def root():
    return {
        "message": "PrivateVault MCP - Thin Gateway to PrivateVault.ai Backend",
        "docs": "/docs",
        "architecture": "Claude/Cursor/Agent → MCP (auth+transform+retry) → POST /api/evaluate → PrivateVault Engine",
        "single_source_of_truth": "PrivateVault backend (https://github.com/LOLA0786/PrivateVault.ai)",
        "no_local_logic": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("privatevault_mcp.api.main:app", host="0.0.0.0", port=8000, reload=True)
EOF