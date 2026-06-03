"""
PrivateVault CognitiveExecutionKernel stub.

**REMOVED** - All local trust, risk, Merkle, and decision logic has been eliminated per architecture requirements.
The MCP server is a **thin gateway only**. All evaluation happens exclusively in the PrivateVault backend via POST /api/evaluate.

This file exists only to prevent import errors in tests/docs. Do not use or extend it.
"""
# No-op stub to maintain compatibility without local logic
class CognitiveExecutionKernel:
    """Stub - no functionality. See gateway.py for the only evaluation path."""
    def __init__(self):
        pass

    def calculate_trust_breakdown(self, *args, **kwargs):
        raise RuntimeError("Local kernel removed. Use PrivateVaultGateway.evaluate() → /api/evaluate only.")

    def decide(self, *args, **kwargs):
        raise RuntimeError("Local kernel removed. Use PrivateVaultGateway.evaluate() → /api/evaluate only.")


kernel = CognitiveExecutionKernel()
