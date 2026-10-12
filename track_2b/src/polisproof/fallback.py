from __future__ import annotations

import re

from .models import Artifact, AtomicClaim


APPROVAL = re.compile(r"\b(approved?|approves?|genehmigt|bewilligt|approuv(?:e|é|ée)|approv(?:a|ato|ata))\b", re.I)
REJECTION = re.compile(r"\b(rejected?|refused?|abgelehnt|lehnt\s+ab|rejet(?:é|ée)|refus(?:e|é|ée)|respint[oa])\b", re.I)
AMOUNT = re.compile(r"(?:(EUR|CHF|€)\s*(\d{1,3}(?:[ .,'’]\d{3})+|\d+)|(\d{1,3}(?:[ .,'’]\d{3})+|\d+)\s*(EUR|CHF|€))", re.I)
CONDITION = re.compile(r"\b(subject to|conditional on|provided that|vorbehaltlich|unter der bedingung|sous réserve|à condition|previa|solo dopo)\b(.+)", re.I)
DATE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def _actor(span: str) -> str | None:
    patterns = (
        (r"\b(council|board|committee)\b", None),
        (r"\b(der rat|gemeinderat|schulkommission|ausschuss)\b", None),
        (r"\b(le conseil|la commission|le comité)\b", None),
        (r"\b(il consiglio|la giunta|la commissione|il comitato)\b", None),
    )
    for pattern, _ in patterns:
        match = re.search(pattern, span, re.I)
        if match:
            return match.group(1)
    return None


def extract_fallback(artifacts: list[Artifact]) -> list[AtomicClaim]:
    """Conservative no-model extraction: copy explicit decisions; never infer."""
    claims: list[AtomicClaim] = []
    for artifact in artifacts:
        for span in _sentences(artifact.content):
            approved = APPROVAL.search(span)
            rejected = REJECTION.search(span)
            if not approved and not rejected:
                continue
            amount_match = AMOUNT.search(span)
            currency = None
            amount = None
            if amount_match:
                currency = amount_match.group(1) or amount_match.group(4)
                currency = "EUR" if currency == "€" else currency.upper() if currency else None
                amount = re.sub(r"\D", "", amount_match.group(2) or amount_match.group(3))
            condition_match = CONDITION.search(span)
            date_match = DATE.search(span)
            status = "REJECTED" if rejected and not approved else "APPROVED"
            claim_type = "REJECTION" if status == "REJECTED" else "APPROVAL"
            claims.append(AtomicClaim(
                claim_id=f"fallback-{len(claims)+1}", claim_type=claim_type,
                statement=span, actor=_actor(span), action="decision",
                amount=amount, currency=currency, date=date_match.group(1) if date_match else None,
                condition=condition_match.group(0) if condition_match else None,
                decision_status=status, source_artifact=artifact.artifact_id,
                source_span=span, source_hash=artifact.sha256, language=artifact.language,
                model_source="OFFLINE_FALLBACK", model_version="deterministic-v1", confidence=1.0,
            ))
    return claims
