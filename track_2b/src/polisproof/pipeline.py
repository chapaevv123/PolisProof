from __future__ import annotations

import json
from pathlib import Path

from .models import ReasonCode, RouteEvent, VerificationStatus
from .normalizer import build_artifact
from .parser import parse_model_output
from .provider import ApertusProvider, ModelUnavailable
from .fallback import extract_fallback
from .receipt import build_receipt
from .verifier import verify_claims


class PolisProofPipeline:
    def __init__(self, project_root: Path, mode: str = "replay") -> None:
        self.project_root = project_root
        self.provider = ApertusProvider(project_root / "fixtures" / "cassettes", mode=mode)

    def compile(self, packet: dict) -> dict:
        artifacts = [build_artifact(item) for item in packet["artifacts"]]
        documents = "\n\n".join(
            f"<document id='{a.artifact_id}' language='{a.language}'>\n{a.content}\n</document>" for a in artifacts
        )
        routes: list[RouteEvent] = []
        try:
            response = self.provider.complete(packet["packet_id"], documents, "8B")
        except ModelUnavailable as exc:
            claims = extract_fallback(artifacts)
            status, codes = verify_claims(claims, artifacts)
            routes.append(RouteEvent("packet", "FALLBACK", "model-unavailable", "deterministic-v1"))
            receipt = build_receipt(packet["packet_id"], artifacts, claims, status, codes, routes, 0, "OFFLINE_FALLBACK")
            receipt["model_error"] = str(exc)
            return receipt
        parsed = parse_model_output(response.raw, response.mode, response.model)
        routes.append(RouteEvent("packet", "8B", "initial extraction", response.model, response.latency_ms, response.input_tokens, response.output_tokens))
        if not parsed.valid:
            return {
                "verification_status": VerificationStatus.MODEL_OUTPUT_INVALID.value,
                "reason_codes": [ReasonCode.MODEL_OUTPUT_INVALID.value], "claims": [], "error": parsed.error,
            }
        artifact_map = {a.artifact_id: a for a in artifacts}
        for claim in parsed.claims:
            if claim.source_artifact in artifact_map and not claim.source_hash:
                claim.source_hash = artifact_map[claim.source_artifact].sha256
        status, codes = verify_claims(parsed.claims, artifacts)

        material = {"AMOUNT_CONFLICT", "DATE_CONFLICT", "NEGATION_CONFLICT", "MISSING_CONDITION", "ACTOR_CONFLICT"}
        if material.intersection(codes):
            disputed = [claim for claim in parsed.claims if material.intersection(claim.reason_codes)]
            disputed_ids = {claim.source_artifact for claim in disputed}
            escalation_documents = "\n\n".join(
                f"<document id='{a.artifact_id}' language='{a.language}'>\n{a.content}\n</document>"
                for a in artifacts if a.artifact_id in disputed_ids
            )
            try:
                adjudication = self.provider.complete(packet["packet_id"], escalation_documents, "70B")
                adjudication_parse = parse_model_output(adjudication.raw, adjudication.mode, adjudication.model)
                route_reason = ",".join(sorted(material.intersection(codes)))
                routes.append(RouteEvent(
                    "disputed-claims", "70B", route_reason, adjudication.model,
                    adjudication.latency_ms, adjudication.input_tokens, adjudication.output_tokens,
                ))
                if not adjudication_parse.valid:
                    codes = sorted(set(codes) | {ReasonCode.MODEL_OUTPUT_INVALID.value})
            except ModelUnavailable:
                # Verification remains fail-closed. The receipt makes the unavailable
                # escalation explicit instead of inventing a successful model call.
                routes.append(RouteEvent("disputed-claims", "70B_UNAVAILABLE", "cassette-or-model-unavailable", self.provider.model_70b))
            for claim in parsed.claims:
                if material.intersection(claim.reason_codes):
                    claim.escalation_reason = ",".join(sorted(material.intersection(claim.reason_codes)))

        return build_receipt(packet["packet_id"], artifacts, parsed.claims, status, codes, routes, parsed.repair_count, response.mode)

    def compile_fixture(self, fixture_id: str) -> dict:
        path = self.project_root / "fixtures" / "packets" / f"{fixture_id}.json"
        return self.compile(json.loads(path.read_text(encoding="utf-8")))
