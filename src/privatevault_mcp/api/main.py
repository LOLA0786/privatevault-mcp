"""
FastAPI server for PrivateVault MCP with OpenAPI docs.
Exposes both REST endpoints and MCP protocol compatibility.
"""
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import structlog
from contextlib import asynccontextmanager
from ..core.models import (
    ScanContextRequest, ScanContextResponse,
    PolicyCheckRequest, PolicyCheckResponse,
    AuditActionRequest, AuditActionResponse,
    RiskScoreRequest, RiskScoreResponse
)
from ..mcp.tools import mcp_tools

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("privatevault_mcp_startup", status="ready", version="0.1.0")
    yield
    logger.info("privatevault_mcp_shutdown")

app = FastAPI(
    title="PrivateVault MCP",
    description="Cognitive Runtime Security Control Plane for AI Agents. MCP + REST.",
    version="0.1.0",
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
    """MCP Tool 1: Scan context for injection and risk."""
    return await mcp_tools.scan_context(request.context_text)

@router.post("/policy-check", response_model=PolicyCheckResponse)
async def policy_check(request: PolicyCheckRequest):
    """MCP Tool 2: Policy + trust kernel check."""
    return await mcp_tools.policy_check(request.action, request.context)

@router.post("/audit-action", response_model=AuditActionResponse)
async def audit_action(request: AuditActionRequest):
    """MCP Tool 3: Record immutable audit."""
    return await mcp_tools.audit_action(request.agent_id, request.action, request.context_hash)

@router.post("/risk-score", response_model=RiskScoreResponse)
async def risk_score(request: RiskScoreRequest):
    """MCP Tool 4: Full 4-pillar risk scoring."""
    return await mcp_tools.risk_score(request.context, request.action)

app.include_router(router)

# MCP compatibility endpoint (simple JSON-RPC style for Claude/Cursor)
@app.post("/mcp")
async def mcp_handler(payload: Dict[str, Any]):
    """Basic MCP protocol handler for desktop tools."""
    method = payload.get("method")
    params = payload.get("params", {})

    if method == "scan_context":
        return await mcp_tools.scan_context(params.get("context_text", ""))
    elif method == "policy_check":
        return await mcp_tools.policy_check(params.get("action", ""), params.get("context", {}))
    elif method == "audit_action":
        return await mcp_tools.audit_action(
            params.get("agent_id", "unknown"),
            params.get("action", ""),
            params.get("context_hash", "")
        )
    elif method == "risk_score":
        return await mcp_tools.risk_score(params.get("context", {}), params.get("action", ""))

    return {"error": "Unknown method", "supported": ["scan_context", "policy_check", "audit_action", "risk_score"]}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "privatevault-mcp", "mcp_tools": 4}

@app.get("/")
async def root():
    return {
        "message": "PrivateVault MCP Server",
        "docs": "/docs",
        "mcp_tools": ["scan_context", "policy_check", "audit_action", "risk_score"],
        "status": "production-ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("privatevault_mcp.api.main:app", host="0.0.0.0", port=8000, reload=True)
EOF