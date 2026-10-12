from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone


def canonical_json(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_receipt(packet_id: str, artifacts: list, claims: list, status: str, reason_codes: list[str], routes: list, parser_repairs: int, execution_mode: str = "UNKNOWN") -> dict:
    body = {
        "schema_version": "polisproof.receipt.v1",
        "execution_mode": execution_mode,
        "packet_id": packet_id,
        "artifact_hashes": {a.artifact_id: a.sha256 for a in artifacts},
        "claims": [c.to_dict() for c in claims],
        "evidence": [
            {"claim_id": c.claim_id, "artifact_id": c.source_artifact, "exact_span": c.source_span, "source_hash": c.source_hash}
            for c in claims
        ],
        "verification_status": status,
        "reason_codes": reason_codes,
        "route": [r.to_dict() for r in routes],
        "model_identifiers": sorted({r.model for r in routes}),
        "prompt_template_sha256": hashlib.sha256(b"polisproof-extract-v1").hexdigest(),
        "parser_repair_count": parser_repairs,
        "latency_ms": sum(r.latency_ms for r in routes),
        "token_counts": {
            "input": sum(r.input_tokens for r in routes),
            "output": sum(r.output_tokens for r in routes),
        },
        "human_report": {
            "headline": f"Decision status: {status}",
            "summary": f"{len(claims)} atomic claim(s); {len(reason_codes)} verification reason(s).",
            "reasons": reason_codes,
            "disclaimer": "Model and fallback outputs are non-authoritative; evidence checks determine the verdict."
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    stable = dict(body)
    stable.pop("timestamp")
    body["output_hash"] = hashlib.sha256(canonical_json(stable).encode("utf-8")).hexdigest()
    return body
