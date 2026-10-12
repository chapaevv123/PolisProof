# PolisProof — Track 2B

**AI can summarize a decision. PolisProof proves what was actually decided.**

PolisProof compiles multilingual public-decision packets into atomic claims,
binds every claim to an exact source span and SHA-256 digest, applies
deterministic verification, escalates disputed claims from Apertus 8B to 70B,
and exports a tamper-evident decision receipt. A model output is evidence to
check, never authority.

## Judge demo

Open `http://localhost:8080`, then select **Compile decision**. The synthetic
German/French/Italian packet contrasts a draft claim of unconditional EUR
60,000 approval with the actual record: EUR 40,000, conditional on legal
review. The gate returns `BLOCKED`, `AMOUNT_CONFLICT`, and
`MISSING_CONDITION`, with exact evidence and an exportable receipt.

The interface also accepts a UTF-8 `.txt` document or a packet `.json` file.
When no model is reachable, uploads use a conservative deterministic extractor
and are visibly labelled `OFFLINE_FALLBACK`; they are never presented as live
Apertus output. The bundled fixture remains `RECORDED_REPLAY` until replaced by
genuine evidence.

## Run

Requirements: Docker with Compose support. No network or credentials are
needed for the default replay demo.

```sh
make run       # Docker, UI on http://localhost:8080
make test      # isolated Python standard-library tests
make eval      # frozen synthetic evaluation; writes evaluation/latest_results.json
make eval-live # genuine Apertus benchmark; never falls back to replay
```

Without Docker, Python 3.11+ can run the same code:

```sh
PYTHONPATH=src python -m polisproof.server --host 127.0.0.1 --port 8080
python -m unittest discover -s tests -v
python evaluation/run_eval.py
```

## Live Apertus

Set `POLISPROOF_MODE=live`, `LLM_BASE_URL`, `LLM_API_KEY`, and optionally
`LLM_NAME_8B` / `LLM_NAME_70B`. The endpoint must implement OpenAI-compatible
`/chat/completions`. Secrets are read only from the environment and never
placed in receipts. `LLM_NAME` is also accepted for the 8B lane for template
compatibility. Minimal live 8B and 70B smoke execution is evidenced in
`../evidence/live/smoke_2026-10-12.json`; full-corpus execution is not yet
evidenced.
When credentials are absent, `make eval-live` exits with
`LIVE_APERTUS_CREDENTIALS_REQUIRED`. It writes sanitized records only under
`../evidence/live/{8b,70b,routed}/`; it never stores authorization headers.

The frozen live corpus is `evaluation/polisproof_eval_v1.json`: 30 synthetic,
realistic packets across English, German, French, and Italian. Validate it
without credentials with `python evaluation/live_benchmark.py --validate-corpus`.

### Hugging Face routed inference

The HF OpenAI-compatible endpoint is `https://router.huggingface.co/v1`.
Configure a scoped read token as `HF_TOKEN` in the process environment; do not
put it in `.env`, source control, screenshots, commands saved to shell history,
or chat. The harness defaults name the v1.5 checkpoints, but provider routing
and availability can change. On 2026-10-12 HF exposed the older 2509 instruct
checkpoints as live while v1.5 8B had no provider mapping and v1.5 70B reported
a provider error. Inspect the live catalog immediately before a run and
override model names explicitly when necessary.

No automatic paid run should begin until the HF billing page shows a spending
limit at or below USD 1.00 for this pass and the current provider price is
visible. PolisProof does not estimate or invent prices that HF does not return
in the completion response.

## Why Apertus

The 8B/70B split is the product architecture: multilingual Apertus 8B extracts
routine claims locally; deterministic checks identify only disputed claims for
70B adjudication. Fully open weights allow the whole path to run on-premise or
air-gapped, preserving sensitive civic records and avoiding an opaque API
dependency. Its multilingual scope directly fits Swiss and cross-border public
records. Swapping in a closed remote API would weaken auditability, data
sovereignty, and offline deployment.

## Data and licence

All packet and replay fixtures are small, synthetic, created by PolisProof
contributors, and released under CDLA-Permissive-2.0. They contain no personal
data. Source code is Apache-2.0; documentation is CC-BY-4.0. The repository
root contains the Apache-2.0 `LICENSE`. See `data/README.md` and
`technical_report.md` for provenance and limitations.
