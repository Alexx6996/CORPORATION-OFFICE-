# integrations/payments/router.py
from fastapi import APIRouter, HTTPException, Request, status, Depends
from pydantic import BaseModel

# Общая зависимость авторизации (OIDC либо аварийный Basic)
from apps.backend_core.auth.oidc_verifier import get_current_user, AuthUser

router = APIRouter(prefix="/payments", tags=["payments"])

class ChargeRequest(BaseModel):
    amount: int
    currency: str = "RUB"
    customer_id: str | None = None
    description: str | None = None

class ChargeResponse(BaseModel):
    id: str
    status: str

@router.get("/health", summary="Payments integration healthcheck")
async def health() -> dict:
    return {"status": "ok"}

@router.post("/charge", response_model=ChargeResponse, summary="Create test charge (sandbox)")
async def create_charge(
    req: ChargeRequest,
    user: AuthUser = Depends(get_current_user),
) -> ChargeResponse:
    # TODO: integrate provider SDK (sandbox). This is a stub.
    if req.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="amount must be > 0")
    return ChargeResponse(id="test_charge_0001", status="created")

@router.post("/webhook", summary="Payments provider webhook endpoint")
async def webhook(
    request: Request,
    user: AuthUser = Depends(get_current_user),
) -> dict:
    # TODO: verify signature and process event types (payment.succeeded, refund.created, etc.)
    payload = await request.body()
    # For now, just acknowledge
    return {"received": True, "bytes": len(payload)}
