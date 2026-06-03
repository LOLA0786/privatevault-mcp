from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional

class ScanContextRequest(BaseModel):
    context_text: str = Field(..., description="Text/context to forward to PrivateVault backend")

class PolicyCheckRequest(BaseModel):
    action: str
    context: Dict[str, Any]

class AuditActionRequest(BaseModel):
    agent_id: str
    action: str
    context_hash: str

class RiskScoreRequest(BaseModel):
    context: Dict[str, Any]
    action: str

# Response models are now simple passthrough transformers (no enums/logic)
class ScanContextResponse(BaseModel):
    risk_score: int
    prompt_injection_detected: bool
    suspicious_patterns: List[str]
    recommendation: str
    rationale: Optional[str] = None
    backend_source: bool = True

class PolicyCheckResponse(BaseModel):
    allowed: bool
    reason: str
    violated_policies: List[str]
    trust_score: Optional[float] = None
    backend_decision: Optional[str] = None

class AuditActionResponse(BaseModel):
    audit_id: str
    timestamp: str
    backend_audit_id: Optional[str] = None

class RiskScoreResponse(BaseModel):
    score: float
    severity: str
    breakdown: Dict[str, Any]
    recommendation: str
    backend_source: bool = True
