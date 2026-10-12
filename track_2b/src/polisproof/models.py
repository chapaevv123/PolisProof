from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    MODEL_UNAVAILABLE = "MODEL_UNAVAILABLE"
    MODEL_OUTPUT_INVALID = "MODEL_OUTPUT_INVALID"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class ReasonCode(str, Enum):
    AMOUNT_CONFLICT = "AMOUNT_CONFLICT"
    MISSING_CONDITION = "MISSING_CONDITION"
    DATE_CONFLICT = "DATE_CONFLICT"
    ACTOR_CONFLICT = "ACTOR_CONFLICT"
    CURRENCY_CONFLICT = "CURRENCY_CONFLICT"
    SOURCE_NOT_FOUND = "SOURCE_NOT_FOUND"
    SOURCE_SPAN_NOT_FOUND = "SOURCE_SPAN_NOT_FOUND"
    SOURCE_HASH_MISMATCH = "SOURCE_HASH_MISMATCH"
    UNSUPPORTED_CLAIM = "UNSUPPORTED_CLAIM"
    VERSION_CONFLICT = "VERSION_CONFLICT"
    NEGATION_CONFLICT = "NEGATION_CONFLICT"
    DUPLICATE_CONFLICT = "DUPLICATE_CONFLICT"
    LOW_EVIDENCE_COVERAGE = "LOW_EVIDENCE_COVERAGE"
    MODEL_OUTPUT_INVALID = "MODEL_OUTPUT_INVALID"
    PROMPT_INJECTION_QUARANTINED = "PROMPT_INJECTION_QUARANTINED"
    AMBIGUOUS_EVIDENCE = "AMBIGUOUS_EVIDENCE"


CLAIM_TYPES = {
    "APPROVAL", "REJECTION", "EXPENDITURE", "CONDITION", "DEADLINE",
    "ACTOR", "VOTE", "OBJECTION", "AMENDMENT", "PROCEDURAL_REQUIREMENT",
}


@dataclass(frozen=True)
class Artifact:
    artifact_id: str
    title: str
    language: str
    content: str
    sha256: str
    version: str = "1"
    media_type: str = "text/plain"
    timecode: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AtomicClaim:
    claim_id: str
    claim_type: str
    statement: str
    actor: str | None = None
    action: str | None = None
    amount: str | None = None
    currency: str | None = None
    date: str | None = None
    condition: str | None = None
    decision_status: str | None = None
    source_artifact: str | None = None
    source_span: str | None = None
    source_hash: str | None = None
    language: str | None = None
    model_source: str = "replay"
    model_version: str = "recorded-v1"
    confidence: float = 0.0
    verification_status: str = VerificationStatus.HUMAN_REVIEW.value
    reason_codes: list[str] = field(default_factory=list)
    escalation_reason: str | None = None

    def __post_init__(self) -> None:
        if self.claim_type not in CLAIM_TYPES:
            raise ValueError(f"Unsupported claim type: {self.claim_type}")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RouteEvent:
    claim_id: str
    lane: str
    reason: str
    model: str
    latency_ms: int = 0
    input_tokens: int = 0
    output_tokens: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
