from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .models import AtomicClaim


@dataclass
class ParseResult:
    claims: list[AtomicClaim]
    repair_count: int
    valid: bool
    error: str | None = None


def _claim(data: dict, model_source: str, model_version: str) -> AtomicClaim:
    clean = {k: v for k, v in data.items() if k in AtomicClaim.__dataclass_fields__}
    clean.setdefault("model_source", model_source)
    clean.setdefault("model_version", model_version)
    clean.setdefault("confidence", 0.5)
    return AtomicClaim(**clean)


def parse_model_output(raw: str, model_source: str, model_version: str) -> ParseResult:
    attempts: list[str] = [raw.strip()]
    fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", raw, re.S | re.I)
    if fenced:
        attempts.append(fenced.group(1).strip())
    object_match = re.search(r"(\{.*\}|\[.*\])", raw, re.S)
    if object_match:
        attempts.append(object_match.group(1).strip())

    errors: list[str] = []
    for repair_count, candidate in enumerate(dict.fromkeys(attempts)):
        try:
            parsed = json.loads(candidate)
            items = parsed.get("claims", []) if isinstance(parsed, dict) else parsed
            if not isinstance(items, list):
                raise ValueError("claims must be a list")
            claims = [_claim(item, model_source, model_version) for item in items]
            return ParseResult(claims, repair_count, True)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            errors.append(str(exc))

    # One bounded tagged-section fallback; never loop or ask the model to self-repair.
    tagged: list[AtomicClaim] = []
    for block in re.findall(r"<CLAIM>(.*?)</CLAIM>", raw, re.S | re.I):
        fields = {}
        for line in block.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip().lower()] = value.strip() or None
        if {"claim_id", "claim_type", "statement"} <= fields.keys():
            try:
                tagged.append(_claim(fields, model_source, model_version))
            except ValueError as exc:
                errors.append(str(exc))
    if tagged:
        return ParseResult(tagged, 1, True)
    return ParseResult([], min(len(attempts) - 1, 1), False, "; ".join(errors[-2:]))
