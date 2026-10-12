from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation

from .models import Artifact, AtomicClaim, ReasonCode, VerificationStatus
from .normalizer import injection_signals


HIGH_IMPACT = {"APPROVAL", "REJECTION", "EXPENDITURE", "AMENDMENT"}


def _amount(value: str | None) -> Decimal | None:
    if value is None:
        return None
    try:
        return Decimal(value.replace(" ", "").replace(",", "."))
    except InvalidOperation:
        return None


def _add(claim: AtomicClaim, code: ReasonCode) -> None:
    if code.value not in claim.reason_codes:
        claim.reason_codes.append(code.value)


def verify_claims(claims: list[AtomicClaim], artifacts: list[Artifact]) -> tuple[str, list[str]]:
    by_id = {a.artifact_id: a for a in artifacts}
    packet_codes: set[str] = set()

    for claim in claims:
        artifact = by_id.get(claim.source_artifact or "")
        if artifact is None:
            _add(claim, ReasonCode.SOURCE_NOT_FOUND)
        else:
            if claim.source_hash and claim.source_hash != artifact.sha256:
                _add(claim, ReasonCode.SOURCE_HASH_MISMATCH)
            if not claim.source_span or claim.source_span not in artifact.content:
                _add(claim, ReasonCode.SOURCE_SPAN_NOT_FOUND)
            if injection_signals(artifact.content):
                _add(claim, ReasonCode.PROMPT_INJECTION_QUARANTINED)
        if claim.claim_type in HIGH_IMPACT and (not claim.source_artifact or not claim.source_span):
            _add(claim, ReasonCode.UNSUPPORTED_CLAIM)

    groups: dict[tuple[str, str], list[AtomicClaim]] = defaultdict(list)
    for claim in claims:
        if claim.claim_type in {"APPROVAL", "REJECTION", "EXPENDITURE"}:
            groups[((claim.actor or "").casefold(), (claim.action or "").casefold())].append(claim)

    for group in groups.values():
        amounts = {_amount(c.amount) for c in group if _amount(c.amount) is not None}
        currencies = {c.currency for c in group if c.currency}
        dates = {c.date for c in group if c.date}
        actors = {c.actor.casefold() for c in group if c.actor}
        statuses = {c.decision_status for c in group if c.decision_status}
        conditions = {bool(c.condition) for c in group}
        codes: list[ReasonCode] = []
        if len(amounts) > 1:
            codes.append(ReasonCode.AMOUNT_CONFLICT)
        if len(currencies) > 1:
            codes.append(ReasonCode.CURRENCY_CONFLICT)
        if len(dates) > 1:
            codes.append(ReasonCode.DATE_CONFLICT)
        if len(actors) > 1:
            codes.append(ReasonCode.ACTOR_CONFLICT)
        if {"APPROVED", "REJECTED"} <= statuses:
            codes.append(ReasonCode.NEGATION_CONFLICT)
        if len(conditions) > 1:
            codes.append(ReasonCode.MISSING_CONDITION)
        for code in codes:
            for claim in group:
                _add(claim, code)

    supported = sum(
        1 for c in claims if c.source_artifact in by_id and c.source_span and c.source_span in by_id[c.source_artifact].content
    )
    coverage = supported / len(claims) if claims else 0.0
    if claims and coverage < 0.8:
        packet_codes.add(ReasonCode.LOW_EVIDENCE_COVERAGE.value)

    blocking = {
        ReasonCode.AMOUNT_CONFLICT.value, ReasonCode.CURRENCY_CONFLICT.value,
        ReasonCode.DATE_CONFLICT.value, ReasonCode.ACTOR_CONFLICT.value,
        ReasonCode.NEGATION_CONFLICT.value, ReasonCode.MISSING_CONDITION.value,
        ReasonCode.UNSUPPORTED_CLAIM.value, ReasonCode.SOURCE_NOT_FOUND.value,
        ReasonCode.SOURCE_SPAN_NOT_FOUND.value, ReasonCode.SOURCE_HASH_MISMATCH.value,
    }
    for claim in claims:
        packet_codes.update(claim.reason_codes)
        if blocking.intersection(claim.reason_codes):
            claim.verification_status = VerificationStatus.BLOCKED.value
        elif ReasonCode.PROMPT_INJECTION_QUARANTINED.value in claim.reason_codes:
            claim.verification_status = VerificationStatus.HUMAN_REVIEW.value
        else:
            claim.verification_status = VerificationStatus.VERIFIED.value

    if any(c.verification_status == VerificationStatus.BLOCKED.value for c in claims):
        status = VerificationStatus.BLOCKED.value
    elif not claims:
        status = VerificationStatus.INSUFFICIENT_EVIDENCE.value
    elif coverage < 0.8 or any(c.verification_status == VerificationStatus.HUMAN_REVIEW.value for c in claims):
        status = VerificationStatus.HUMAN_REVIEW.value
    else:
        status = VerificationStatus.VERIFIED.value
    return status, sorted(packet_codes)
