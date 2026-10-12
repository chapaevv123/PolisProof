# Technical report — PolisProof

- **Track:** Track 2B — Own Project
- **Event:** Hack Apertus Online 2026
- **Author / developer:** MagnatSV
- **Demo:** video URL pending owner publication

## 1. Summary

Public decisions are frequently summarized from inconsistent minutes, draft
annexes, and multilingual notes. PolisProof does not treat an LLM summary as a
decision. It compiles atomic claims, attaches byte-stable evidence, rejects
unsupported or contradictory claims deterministically, selectively escalates
disputes, and emits a reproducible decision receipt. The central demo blocks
an unconditional EUR 60,000 claim because the final record approves at most
EUR 40,000 and requires legal review.

## 2. Architecture

`packet -> normalize/hash -> Apertus 8B extraction -> strict parser ->
deterministic gate -> disputed-only Apertus 70B -> signed-by-hash receipt`

The model never determines the final status. Exact-span existence, source hash,
amount, currency, date, negation, condition, and evidence-coverage checks are
application-owned. Untrusted-document prompt injection forces human review.
The receipt includes source hashes, claims, evidence spans, route events, model
identifiers, token counts, latency fields, parser repairs, and an output hash.

### Target architecture (mandatory)

Primary target: **air-gapped**, also deployable on-premise. The web server and
verification code use only the Python standard library. At runtime, the model
endpoint can be an OpenAI-compatible local Apertus server on the same protected
network. Replay mode has no network dependency. Docker is the only clean-run
dependency. A sovereign Swiss cloud endpoint is also compatible, but is not
required for the architecture claim.

## 3. Use of Apertus

- 8B: multilingual atomic-claim extraction for every packet.
- 70B: adjudication context only when deterministic checks find a material
  conflict; it cannot overrule the gate.
- Models: `swiss-ai/Apertus-v1.5-8B` and
  `swiss-ai/Apertus-v1.5-70B`.
- Prompt: fixed system prompt in `src/polisproof/provider.py`, temperature 0.
- Serving: OpenAI-compatible endpoint configured solely by environment.

The included cassettes are synthetic offline demonstrations. Separate live
smoke evidence proves one minimal 8B and one minimal 70B request, but token
reduction and corpus-level quality/latency remain an explicit owner gate.

## 4. Data

The frozen evaluation and demo packets are contributor-authored synthetic data
under CDLA-Permissive-2.0. They include English, German, French, and Italian,
no people, and no personal data. Each packet embeds provenance. Total data is
far below the 100 MB limit. The synthetic 70B replay is labelled as such and
contains zero token/latency claims.

## 5. Evaluation

`make eval` executes 12 frozen rule cases and three end-to-end replay packets.
It derives results from emitted receipts. Current verified local results are in
`evaluation/latest_results.json`; do not interpret replay timing as inference
latency.

| Metric | Current result |
|---|---:|
| Frozen deterministic cases | 12/12 |
| Contradiction recall | 100% (8/8 synthetic fault cases) |
| Unsupported-claim block rate | 100% (1/1) |
| False-block rate | 0% (0/1 clean end-to-end packet) |
| Evidence coverage | 100% (5/5 replay claims) |
| Schema-valid receipt rate | 100% (3/3) |
| 8B-only packet rate | 66.7% (2/3) |
| 70B escalation rate | 33.3% (1/3) |
| Live 70B input-token reduction | not measured |

These are small synthetic-set measurements, not population estimates.

## 6. Limitations

There is live provider smoke evidence, but no live corpus evaluation yet.
Extraction precision/recall, structured-output reliability, representative
latency, and token savings cannot be claimed until a frozen live run is
captured. Exact string spans are conservative and may send
benign formatting variations to review. The 12-case evaluation is intentionally
small. Receipts are tamper-evident hashes, not cryptographic signatures.

## 7. Reproducibility

The Docker image is `python:3.11-slim`, uses no third-party Python packages,
and runs as an unprivileged user. `make run`, `make test`, and `make eval` need
no parent paths, virtual environment, cache, or secret in replay mode. The
generated result includes local wall-clock samples and explicitly scopes them
as pipeline-only timing.

## 8. Next steps

Run the frozen corpus once against genuine Apertus 8B and 70B endpoints, retain
raw responses and usage metadata, add at least 50 adjudicated multilingual
packets, then publish precision/recall confidence intervals and the measured
token/cost comparison. Record a two-minute demo after those results are fixed.

## 9. Live Apertus evaluation

`POLISPROOF_EVAL_V1` freezes 30 contributor-authored packets across English,
German, French, and Italian: 8 clean, 7 contradiction, 5 condition, 4
unsupported, 4 adversarial, and 2 ambiguous cases. Every packet includes
ground truth, expected claims/status/reason codes, provenance, and licence.

The live harness runs the identical corpus in three modes: 8B-only, 70B-only,
and routed 8B → deterministic gate → selective 70B. It captures sanitized raw
content, provider-reported tokens, latency, parse/repair behavior, claims,
citations, route decisions, and verdicts. It emits a non-cherry-picked
comparison table. `make eval-live` cannot use replay and fails closed with
`LIVE_APERTUS_CREDENTIALS_REQUIRED` when authentication is missing.

### 8B vs 70B and routing results

On 2026-10-12 authenticated HF routed smoke calls succeeded for Apertus 8B
Instruct 2509 through Public AI and Apertus 70B Instruct 2509 through
Featherless. Both returned `POLISPROOF_OK`; provider usage was 69 input and 6
output tokens. Observed latencies were 1746.573 ms and 7568.207 ms. These two
trivial prompts prove execution only. Claim precision/recall, representative
latency, token reduction, structured-output reliability, adversarial success,
and comparative 8B/70B value remain **UNAVAILABLE**.

### Structured output reliability

The harness distinguishes first-pass JSON, bounded parser repair, invalid
schema, refusal, excessive prose captured by repairs, and provider errors. Real
rates remain unavailable until the live run.

### Adversarial results

Four frozen prompt-injection packets test ignored instructions, fake system
messages, malicious appendices, and false authority. The application continues
to quarantine recognized injection text deterministically. Model-level
injection success and leakage remain unavailable until live execution.

## License

Documentation: Creative Commons Attribution 4.0 (CC-BY-4.0). Code: Apache-2.0.
Synthetic data: CDLA-Permissive-2.0.
