"""Validate bundled submission artifacts without third-party dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "docs" / "receipt.schema.json"
RECEIPT_PATH = ROOT / "demo" / "sample_audit_receipt.json"


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    missing = [key for key in schema["required"] if key not in receipt]
    if missing:
        raise SystemExit(f"RECEIPT_SCHEMA_INVALID missing={','.join(missing)}")
    properties = schema["properties"]
    if receipt["schema_version"] != properties["schema_version"]["const"]:
        raise SystemExit("RECEIPT_SCHEMA_INVALID schema_version")
    for key in ("execution_mode", "verification_status"):
        if receipt[key] not in properties[key]["enum"]:
            raise SystemExit(f"RECEIPT_SCHEMA_INVALID {key}")
    if not re.fullmatch(properties["output_hash"]["pattern"], receipt["output_hash"]):
        raise SystemExit("RECEIPT_SCHEMA_INVALID output_hash")
    for key in ("claims", "evidence", "reason_codes", "route"):
        if not isinstance(receipt[key], list):
            raise SystemExit(f"RECEIPT_SCHEMA_INVALID {key}")
    if not isinstance(receipt["human_report"], dict):
        raise SystemExit("RECEIPT_SCHEMA_INVALID human_report")
    print(f"RECEIPT_SCHEMA_VALID {RECEIPT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
