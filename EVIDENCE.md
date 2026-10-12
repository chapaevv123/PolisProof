# PolisProof evidence register — 2026-10-12

| Claim | Evidence | Status |
|---|---|---|
| Continuity baseline | `python -m unittest discover -s tests -v`: 35/35 | verified |
| Current regression suite | same command after changes: 44/44 | verified |
| Frozen rule evaluation | `evaluation/latest_results.json`: 12/12 | verified, synthetic |
| Contradiction recall | 8/8 labelled synthetic fault cases | 100% |
| Unsupported-claim block | 1/1 labelled case | 100% |
| False-block rate | 0/1 clean end-to-end packet | 0% |
| Evidence coverage | 5/5 end-to-end replay claims | 100% |
| Routing | 2/3 packets 8B-only; 1/3 escalated to 70B | verified replay behavior |
| Demo result | HTTP API: `BLOCKED`, `AMOUNT_CONFLICT`, `MISSING_CONDITION` | verified |
| Receipt | 64-character output hash; deterministic test passes | verified |
| Clean isolation | copied project under `%TEMP%`; 44/44 and 12/12 | verified |
| Receipt schema | `evaluation/validate_artifacts.py`: `RECEIPT_SCHEMA_VALID` | verified |
| Docker shape | `docker compose config` succeeds | verified |
| Docker execution | daemon unavailable | not verified |
| Apertus 8B/70B execution | `evidence/live/smoke_2026-10-12.json`: two HTTP 200 responses | verified smoke only |
| Token reduction | needs live all-70B comparator | not measured |
| Model inference latency | needs live frozen run | not measured |

Replay cassettes are synthetic demo artifacts. Model names in them are not treated as evidence of model execution.

## LIVE_APERTUS log

HF authentication was verified without recording the token. Two minimal real
inference calls were recorded; the frozen corpus has not been run.

The live-only harness, evidence schema, 30-packet `POLISPROOF_EVAL_V1` corpus,
and result-table generator are ready. Invocation without credentials returns
`LIVE_APERTUS_CREDENTIALS_REQUIRED`; no replay fallback occurs.

| MODEL | ENDPOINT CLASS | FIXTURE | TIMESTAMP | LATENCY | TOKENS | RAW RESPONSE PATH | PARSE RESULT | CLAIMS | ROUTE | VERDICT |
|---|---|---|---|---:|---:|---|---|---:|---|---|
| Apertus 8B Instruct 2509 | HF routed / Public AI | smoke | 2026-10-12 | 1746.573 ms | 75 | `evidence/live/smoke_2026-10-12.json` | exact text | 0 | 8B | HTTP 200 |
| Apertus 70B Instruct 2509 | HF routed / Featherless | smoke | 2026-10-12 | 7568.207 ms | 75 | `evidence/live/smoke_2026-10-12.json` | exact text | 0 | 70B | HTTP 200 |

## Finalization evidence — 2026-10-12

- Owner-reported screenshot evidence: USD 10.00 Hugging Face compute credits
  claimed. This proves credit availability only, not authentication or inference.
- Local credential presence: `HF_TOKEN` PRESENT and authenticated; its value was
  neither printed nor stored. Other credential families were not needed.
- Calculated inference cost this pass: USD 0.000080925 from provider-reported
  tokens and inspected rates; the completion responses did not contain billing
  ledger amounts.
- Current test suite: 44/44 passing.
- Final isolated-copy gate: 44/44 tests, 12/12 evaluation, and receipt schema
  validation all passed without parent paths, credentials, or caches.
- Upload integration smoke: HTTP 200, `OFFLINE_FALLBACK`, one evidence-bound
  claim, EUR 10,000, legal-review condition, 64-character receipt hash.
- Sample receipt: `track_2b/demo/sample_audit_receipt.json`.
- Sample report: `track_2b/demo/sample_decision_report.md`.
- Canonical reconciliation: `CANONICAL_STATE.json`; external submission remains
  `NOT_SUBMITTED`.

## Recovered bounded benchmark attempt — 2026-10-13

The interrupted run left six saved fixtures in each of 8B-only, 70B-only, and
routed mode (18 records total). Every saved record contains an HTTP 403 from
the downstream provider, identified in the response as Cloudflare error 1010.
There were zero successful model responses, so claim quality, schema quality,
adversarial success, and live routing rates are `UNAVAILABLE`, not zero.
Provider-attempt latency remains descriptive network evidence only.

The summarizer now excludes provider-error rows from model-quality
denominators and can rebuild the table using `--summarize-existing` without a
network request. The regression suite is now 45/45, including a test that
prevents provider failures from being scored as model failures.
