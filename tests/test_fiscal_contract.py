# tests/test_fiscal_contract.py
import io
import yaml
from pathlib import Path

REQUIRED_RECEIPT_FIELDS = {
    "id", "issue_datetime", "currency", "operation",
    "seller", "customer", "items", "totals", "payments",
}

def test_receipt_yaml_exists_and_loads():
    p = Path("integrations/fiscal/receipt_model.yaml")
    assert p.exists(), "receipt_model.yaml not found"
    data = yaml.safe_load(io.open(p, "r", encoding="utf-8"))
    assert isinstance(data, dict)
    assert "receipt" in data and isinstance(data["receipt"], dict)

def test_receipt_has_required_fields():
    p = Path("integrations/fiscal/receipt_model.yaml")
    data = yaml.safe_load(io.open(p, "r", encoding="utf-8"))
    r = data["receipt"]
    missing = REQUIRED_RECEIPT_FIELDS - set(r.keys())
    assert not missing, f"Missing fields in receipt: {sorted(missing)}"
    assert isinstance(r["items"], list) and len(r["items"]) > 0
    assert isinstance(r["payments"], list) and len(r["payments"]) > 0
