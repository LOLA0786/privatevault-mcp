from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Recommendation(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"

class ScanContextRequest(BaseModel):
    context_text: str = Field(..., description="Text to scan for risks and injections")

class ScanContextResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    prompt_injection_detected: bool
    suspicious_patterns: List[str]
    recommendation: Recommendation
    rationale: Optional[str] = None

class PolicyCheckRequest(BaseModel):
    action: str
    context: Dict[str, Any]

class PolicyCheckResponse(BaseModel):
    allowed: bool
    reason: str
    violated_policies: List[str]
    trust_score: Optional[float] = None

class AuditActionRequest(BaseModel):
    agent_id: str
    action: str
    context_hash: str

class AuditActionResponse(BaseModel):
    audit_id: str
    timestamp: str
    merkle_proof: Optional[str] = None

class RiskScoreRequest(BaseModel):
    context: Dict[str, Any]
    action: str

class RiskScoreResponse(BaseModel):
    score: float
    severity: Severity
    breakdown: Dict[str, float]  # 4-pillar trust
    recommendation: Recommendation

class AuditLog(BaseModel):
    id: str
    timestamp: datetime
    agent_id: str
    action: str
    context_hash: str
    risk_score: float
    verdict: str
    merkle_hash: str
