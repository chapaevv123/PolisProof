# PolisProof build status — 2026-10-12

- Recovered existing pipeline, verifier, parser, replay fixtures, UI, and 35-test baseline intact.
- Baseline: 35/35 passed once before edits.
- Current: 44/44 passed; frozen deterministic evaluation 12/12 passed.
- Fixed false 70B routing proof: escalation now calls a distinct 70B provider/cassette and missing replay data fails closed.
- Replaced hard-coded routing metrics with values derived from three end-to-end receipts.
- Added Docker/Compose, Makefile, Track 2B README, technical report, data provenance, and receipt export UI.
- Isolated copy: current tests and evaluation pass without parent paths, venv, credentials, or caches.
- HTTP smoke: health 200; demo `BLOCKED`; `AMOUNT_CONFLICT,MISSING_CONDITION`; route `8B->70B`.
- Docker Compose config validates. Docker build/run is unverified because the local Docker daemon is stopped.
- HF authentication and minimal real Apertus 8B/70B execution are evidenced in
  `evidence/live/smoke_2026-10-12.json`; this is not a corpus benchmark.
- Added frozen `POLISPROOF_EVAL_V1`: 30 packets across EN/DE/FR/IT (8 clean,
  7 contradiction, 5 condition, 4 unsupported, 4 adversarial, 2 ambiguous).
- Added live-only 8B/70B/routed harness, sanitized evidence schema, comparison
  generator, adversarial measures, and fail-closed `make eval-live`.
- Verified official CSCS OpenAI-compatible access path and both v1.5 model IDs;
  HF routed authentication is now verified while CSCS credentials remain absent.

Largest remaining gap: the genuine frozen 30-packet Apertus 8B/70B/routed run
and statistically meaningful multilingual extraction evaluation.

## Recovery update — 2026-10-13

- Recovered 18 records from the interrupted bounded live attempt: six per
  mode. All were downstream HTTP 403 / Cloudflare 1010 provider failures.
- Corrected aggregation so failed provider calls do not appear as zero model
  quality, safety, or routing scores; those results are now `UNAVAILABLE`.
- Added offline `--summarize-existing` recovery with no network or spend.
- Re-ran 44/44 tests, 12/12 deterministic evaluation, receipt validation,
  30-packet corpus validation, and the HTTP replay smoke on port 8877.
- Confirmed the final PDF has six pages. No MP4, public repository, or external
  submission was created. Status remains `NOT_SUBMITTED`.

## Finalization update

- Owner-confirmed Hugging Face credits: USD 10.00. Authentication verified.
- Two bounded smoke calls calculated at USD 0.000080925 total; no provider
  billing-ledger amount was returned.
- Added HF routed-inference support without changing CSCS/local support.
- Added upload ingestion, conservative deterministic fallback, explicit execution
  mode, human-readable report, receipt schema, sample outputs, submission copy,
  video script, and owner checklist.
- HTTP upload smoke passed in `OFFLINE_FALLBACK`; no live success was simulated.
- Final isolated copy passed 44/44 tests, 12/12 evaluation cases, and bundled
  receipt schema validation. Project contents total 318,294 bytes.
- Canonical project 49937, participation, and build records reconciled. Statuses:
  `BUILDING`, `LOCALLY_FUNCTIONAL_LIVE_SMOKE_VERIFIED`, `NOT_SUBMITTED`.
