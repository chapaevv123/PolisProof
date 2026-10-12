# Hack Apertus submission draft

- Project name: **PolisProof**
- Creator / developer: **MagnatSV**
- Track: **2B — Apertus Adoption: Own Project**
- Repository URL: **https://github.com/chapaevv123/PolisProof**
- Public demo URL: **https://polisproof.onrender.com**
- Demo video URL: **https://youtu.be/Wo-tzCz955A**
- Technical report: `MagnatSV_Report.pdf`
- Dataset URL: omitted; dataset publication is optional

## Concise pitch

PolisProof is a sovereign, evidence-first AI system that identifies
contradictions and missing approval conditions in public decisions using
Apertus and deterministic verification.

## Description

Public decisions are often scattered across multilingual minutes, draft
annexes and legal notes. A fluent summary can silently turn a proposal into an
approval or omit a binding condition. PolisProof uses Apertus 8B to extract
atomic claims with exact source spans, verifies those claims against normalized
and hashed documents, and routes only disputed context to Apertus 70B. The
model never decides the verdict: deterministic rules block unsupported claims,
amount/date/actor conflicts, negation conflicts and missing conditions.

The fictional demonstration contrasts a EUR 60,000 draft with final minutes
limiting approval to EUR 40,000 and requiring legal review. PolisProof returns
`BLOCKED`, `AMOUNT_CONFLICT`, and `MISSING_CONDITION`, then exports an auditable
JSON receipt.

Real Hugging Face smoke calls succeeded with
`swiss-ai/Apertus-8B-Instruct-2509:publicai` and
`swiss-ai/Apertus-70B-Instruct-2509:featherless-ai`. A later stratified corpus
attempt was blocked by downstream Cloudflare error 1010, so no live quality
percentages are claimed. The target architecture runs the open Apertus weights
on-premise or air-gapped behind the same OpenAI-compatible interface. Hosted HF
inference is an integration demonstration, not the sovereign deployment.

## Novel components

- Exact-span, source-hash evidence binding.
- Deterministic cross-document verification with fail-closed behavior.
- Selective 8B-to-70B escalation with route provenance.
- Explicit `LIVE_APERTUS`, `RECORDED_REPLAY`, `OFFLINE_FALLBACK`, and `ERROR`
  execution states.
- Tamper-evident receipts and adversarial document quarantine.

## Limitations

The 30-packet live benchmark is incomplete, local Apertus weights were not run,
and receipt hashes are tamper-evident rather than digitally signed. The current
quality evidence is deterministic/replay evaluation plus two real smoke calls.

Official submission entry point:
`https://hackapertus.ch/online-hack/submissions`

Legal name and any private registration fields must be completed by the owner
inside the official form. No active X profile is claimed or required.
