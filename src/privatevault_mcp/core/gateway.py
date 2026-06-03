"""
Thin gateway to PrivateVault backend (https://github.com/LOLA0786/PrivateVault.ai).
No local risk scoring, policy decisions, anomaly detection, or governance logic.
All intelligence lives in the PrivateVault /api/evaluate endpoint.
"""
import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Dict, Any
import json
from datetime import datetime
import os

logger = structlog.get_logger(__name__)

class PrivateVaultGateway:
    """Pure proxy/gateway. Single source of truth is the PrivateVault backend."""

    def __init__(self):
        self.base_url = os.getenv("PRIVATEVAULT_URL", "http://localhost:8001")  # Default for local backend
        self.api_key = os.getenv("PRIVATEVAULT_API_KEY")
        self.client = httpx.AsyncClient(timeout=30.0)
        self.logger = logger.bind(component="PrivateVaultGateway")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException))
    )
    async def evaluate(self, prompt: str, context: Dict[str, Any], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Sole entrypoint. Forwards EVERY request to PrivateVault /api/evaluate.
        No local computation of risk, decision, anomalies, or policy.
        """
        if metadata is None:
            metadata = {}

        payload = {
            "prompt": prompt,
            "context": context,
            "metadata": {
                **metadata,
                "source": "mcp_gateway",
                "timestamp": datetime.now().isoformat()
            }
        }

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key or "mcp-gateway-default"
        }

        try:
            self.logger.info("gateway_request", url=f"{self.base_url}/api/evaluate", prompt_length=len(prompt))
            response = await self.client.post(
                f"{self.base_url}/api/evaluate",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()

            self.logger.info("gateway_response",
                           risk_score=result.get("risk_score"),
                           severity=result.get("severity"),
                           decision=result.get("decision", "unknown"))

            return result

        except Exception as e:
            self.logger.error("gateway_failure", error=str(e), backend_url=self.base_url)
            raise RuntimeError(f"PrivateVault backend unavailable at {self.base_url}/api/evaluate. No local fallback allowed.") from e


gateway = PrivateVaultGateway()
