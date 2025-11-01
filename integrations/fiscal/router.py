# integrations/fiscal/router.py
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
import yaml
from pathlib import Path

# Общая зависимость авторизации (OIDC или аварийный Basic)
from apps.backend_core.auth.oidc_verifier import get_current_user, AuthUser  # type: ignore

router = APIRouter(prefix="/fiscal", tags=["fiscal"])

class FiscalEmitRequest(BaseModel):
    order_id: str
    amount: float
    currency: str = "RUB"

class FiscalEmitResponse(BaseModel):
    receipt_id: str
    status: str

@router.get("/health", summary="Fiscal integration healthcheck")
async def health() -> dict:
    return {"status": "ok"}

@router.post("/emit", response_model=FiscalEmitResponse, summary="Сформировать фискальный чек (стаб)")
async def emit_receipt(
    req: FiscalEmitRequest,
    user: AuthUser = Depends(get_current_user),
) -> FiscalEmitResponse:
    """
    Стаб: валидируем черновой YAML-модель и возвращаем фиктивный чек.
    В будущем вместо этого — генерация и отправка в ОФД.
    """
    path = Path("integrations/fiscal/receipt_model.yaml")
    if not path.exists():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="receipt_model.yaml missing")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "receipt" not in data:
            raise ValueError("invalid receipt model")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"receipt model error: {e}")

    if req.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="amount must be > 0")

    return FiscalEmitResponse(receipt_id=f"rcpt_{req.order_id}", status="created")
