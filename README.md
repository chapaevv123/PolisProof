<p align="center">
  <img src="track_2b/docs/assets/polisproof-hero.svg" width="100%" alt="PolisProof — Sovereign AI. Verifiable Public Decisions. Multilingual records flow through Apertus and a deterministic evidence gate into an audit receipt.">
</p>

<p align="center">
  <a href="https://polisproof.onrender.com"><strong>LIVE DEMO</strong></a>
  &nbsp;·&nbsp;
  <a href="https://youtu.be/Wo-tzCz955A"><strong>WATCH VIDEO</strong></a>
  &nbsp;·&nbsp;
  <a href="track_2b/MagnatSV_Report.pdf"><strong>TECHNICAL PDF</strong></a>
  &nbsp;·&nbsp;
  <a href="track_2b/demo/sample_audit_receipt.json"><strong>SAMPLE RECEIPT</strong></a>
</p>

<p align="center">
  <img alt="Hack Apertus 2026" src="https://img.shields.io/badge/Hack_Apertus-2026-34d7ed?style=flat-square&labelColor=061421">
  <img alt="Track 2B" src="https://img.shields.io/badge/Track-2B-55e3aa?style=flat-square&labelColor=061421">
  <img alt="Unit tests: 45 passing" src="https://img.shields.io/badge/tests-45%2F45_passing-55e3aa?style=flat-square&labelColor=061421">
  <img alt="Code license: Apache 2.0" src="https://img.shields.io/badge/code-Apache--2.0-9cecf5?style=flat-square&labelColor=061421">
</p>

## Public decisions deserve more than a fluent summary

Minutes, draft annexes, and legal notes can disagree across languages and
versions. A plausible AI summary may silently promote a proposal into an
approval, change an amount, or omit a binding condition. Those errors become
dangerous when the output looks authoritative.

**PolisProof is an evidence-first compiler for public decisions.** Apertus
extracts atomic claims from multilingual records; PolisProof binds each claim
to an exact source span and document hash, checks contradictions and missing
conditions with deterministic rules, selectively escalates disputed context,
and exports a reproducible JSON audit receipt. Models propose claims. The
application owns the verdict.

> **Public demo disclosure:** the hosted site runs the bundled synthetic cases
> in `RECORDED_REPLAY` mode. It does not make fresh live Apertus calls.

## Watch the 86-second demo

<p align="center">
  <a href="https://youtu.be/Wo-tzCz955A">
    <img src="https://img.youtube.com/vi/Wo-tzCz955A/maxresdefault.jpg" width="760" alt="Watch the 86-second PolisProof demo on YouTube">
  </a>
  <br>
  <a href="https://youtu.be/Wo-tzCz955A"><strong>▶ WATCH THE 86-SECOND DEMO</strong></a>
</p>

## Interface at a glance

The judge-facing workspace keeps source documents, evidence-bound claims, and
the deterministic decision gate visible together. Execution provenance is
shown before analysis begins.

<p align="center"><img src="track_2b/docs/assets/polisproof-home.png" width="100%" alt="PolisProof homepage with product introduction, replay disclosure, multilingual source documents, Run analysis control, evidence panel, and decision gate"></p>

## Real application, three reproducible outcomes

All materials shown below are fictional contributor-authored fixtures. The
screenshots were captured from the real local UI and API at 1920×1080.

### 1. BLOCKED — multilingual amount conflict

The French draft proposes **EUR 60,000**. Final German minutes approve at most
**EUR 40,000**, and the Italian note requires legal review. PolisProof returns
`BLOCKED` with `AMOUNT_CONFLICT` and `MISSING_CONDITION`.

<p align="center"><img src="track_2b/docs/assets/polisproof-blocked.png" width="100%" alt="PolisProof showing three multilingual source documents, exact evidence spans, a BLOCKED verdict, amount conflict, missing condition, and JSON receipt export"></p>

### 2. VERIFIED — clean approval

A final English resolution consistently approves EUR 25,000 for a library roof
subject to structural inspection. Its evidence-bound claim passes the gate.

<p align="center"><img src="track_2b/docs/assets/polisproof-verified.png" width="100%" alt="PolisProof clean approval case showing exact source evidence and a VERIFIED verdict"></p>

### 3. HUMAN_REVIEW — malicious appendix

An untrusted appendix contains prompt-injection language and no actual
decision. PolisProof quarantines the packet with
`PROMPT_INJECTION_QUARANTINED` instead of certifying it.

<p align="center"><img src="track_2b/docs/assets/polisproof-human-review.png" width="100%" alt="PolisProof malicious appendix case showing prompt injection quarantined and a HUMAN_REVIEW verdict"></p>

## What PolisProof actually does

1. Normalizes multilingual UTF-8 records and computes stable SHA-256 hashes.
2. Extracts typed, atomic claims with Apertus 8B or an explicitly labelled
   replay/fallback path.
3. Requires every supported claim to cite an exact span in a named artifact.
4. Applies deterministic amount, currency, date, actor, negation, condition,
   source, hash, and prompt-injection checks.
5. Routes disputed context to Apertus 70B when that lane is configured.
6. Emits a human-readable result and a machine-readable JSON receipt with
   provenance, routing, evidence, reason codes, usage metadata, and output hash.

The receipt hash detects changes to the receipt's canonical content. **A hash
alone is not a digital signature and does not independently authenticate who
created the receipt.**

## Multilingual evidence workflow

```mermaid
flowchart LR
    A[German minutes<br/>FINAL] --> D[Normalize + SHA-256]
    B[French annex<br/>DRAFT] --> D
    C[Italian legal note<br/>FINAL] --> D
    D --> E[Apertus 8B<br/>atomic claims]
    E --> F{Deterministic<br/>evidence gate}
    F -->|consistent| G[VERIFIED]
    F -->|material dispute| H[Apertus 70B<br/>targeted review]
    F -->|injection / ambiguity| I[HUMAN_REVIEW]
    H --> J[BLOCKED or review]
    G --> K[JSON audit receipt]
    I --> K
    J --> K
```

### Model roles

| Component | Responsibility | Authority |
|---|---|---|
| Apertus 8B | Multilingual atomic-claim extraction | Proposes claims only |
| PolisProof gate | Exact-span and cross-document verification | Owns verdict and reason codes |
| Apertus 70B | Reviews only disputed context | Cannot override deterministic checks |
| Receipt builder | Canonicalizes provenance and result metadata | Produces change-detecting hash, not a signature |

The target deployment is on-premise or air-gapped behind an OpenAI-compatible
Apertus endpoint. That sovereign deployment is an architectural target; local
Apertus-weight execution was **not** verified on the development machine.

## Real Apertus execution evidence

Two authenticated Hugging Face routed smoke calls returned HTTP 200:

| Lane | Confirmed model route | Result | Scope |
|---|---|---|---|
| 8B | `swiss-ai/Apertus-8B-Instruct-2509:publicai` | HTTP 200, `POLISPROOF_OK` | Connectivity only |
| 70B | `swiss-ai/Apertus-70B-Instruct-2509:featherless-ai` | HTTP 200, `POLISPROOF_OK` | Connectivity only |

This proves that both model API routes executed. It does **not** establish
end-to-end extraction accuracy. A later bounded 30-packet live attempt was
blocked downstream by HTTP 403 / Cloudflare error 1010. Consequently, live
claim precision, recall, schema reliability, adversarial success, and routing
savings remain **unavailable**. See the sanitized
[evidence register](EVIDENCE.md) and [live results](evidence/live/results.md).

### Execution modes are never conflated

| Mode | Meaning |
|---|---|
| `LIVE_APERTUS` | A configured live endpoint returned the model output |
| `RECORDED_REPLAY` | A bundled synthetic cassette produced the reproducible demo |
| `OFFLINE_FALLBACK` | Conservative local extraction was used without a model |
| `ERROR` | Analysis did not complete |

The [public Render demo](https://polisproof.onrender.com) intentionally uses
`RECORDED_REPLAY` for zero-cost, deterministic judging.

## Security and untrusted documents

- Credentials are read from process environment variables and excluded from
  receipts, fixtures, and evidence artifacts.
- Uploaded bodies are capped at 1 MB and static file access is path-contained.
- Recognized prompt-injection markers force `HUMAN_REVIEW`.
- Missing evidence, invalid model output, and missing escalation data fail
  closed rather than silently becoming approvals.
- Synthetic fixtures contain no personal data or real-world allegations.

This is a defensive prototype, not a proof that arbitrary prompt injection is
solved. The four frozen adversarial corpus cases were structurally validated,
but live model-level adversarial rates are unavailable.

## Measured evaluation

| Check | Measured result | Interpretation |
|---|---:|---|
| Unit tests | **45 / 45 passed** | Parser, verifier, pipeline, fallback, routing, receipt, corpus checks |
| Deterministic cases | **12 / 12 passed** | Small synthetic rule-evaluation set |
| Frozen live corpus structure | **30 packets valid** | EN/DE/FR/IT schema and provenance validated |
| Sample receipt schema | **valid** | Bundled receipt matches the public schema |
| Technical report | **6 pages** | Competition limit verified |
| Real 8B / 70B smoke | **2 HTTP 200 calls** | Connectivity, not quality |
| Full live model quality | **unavailable** | Provider denied the bounded attempt |

The deterministic set is deliberately small and synthetic. It must not be
interpreted as a population accuracy estimate or an Apertus benchmark.

## Quick start

Requirements: Python 3.11+. The default demo needs no network, credentials, or
third-party Python package.

```powershell
git clone https://github.com/chapaevv123/PolisProof.git
cd PolisProof\track_2b
$env:PYTHONPATH='src'
python -m polisproof.server --host 127.0.0.1 --port 8877 --mode replay
```

Open **http://127.0.0.1:8877/** and select **Run analysis**.

macOS/Linux:

```bash
cd PolisProof/track_2b
PYTHONPATH=src python -m polisproof.server --host 127.0.0.1 --port 8877 --mode replay
```

## Docker and Render

```bash
cd track_2b
docker compose up --build
# Open http://127.0.0.1:8080/
```

The repository's [`render.yaml`](render.yaml) deploys the same Docker runtime
in replay mode. The current public instance is
**https://polisproof.onrender.com**. Free services may cold-start after idle
time; no server-side persistence is required.

## Tests and reproducibility

From `track_2b/`:

```bash
python -m unittest discover -s tests -v
python evaluation/run_eval.py
python evaluation/validate_artifacts.py
python evaluation/live_benchmark.py --validate-corpus
```

Live evaluation is deliberately separate and fails closed when credentials are
missing. Never commit `HF_TOKEN`; inject it securely into the process only when
an authorized live run is intended.

Useful reproducibility artifacts:

- [Synthetic conflict packet](track_2b/fixtures/packets/demo_conflict.json)
- [Recorded 8B extraction](track_2b/fixtures/cassettes/demo_conflict_8b.json)
- [Recorded 70B review](track_2b/fixtures/cassettes/demo_conflict_70b.json)
- [Sample audit receipt](track_2b/demo/sample_audit_receipt.json)
- [Receipt JSON Schema](track_2b/docs/receipt.schema.json)
- [Frozen 30-packet corpus](track_2b/evaluation/polisproof_eval_v1.json)

## Repository structure

```text
PolisProof/
├── track_2b/
│   ├── src/polisproof/       # pipeline, providers, verifier, receipt, server
│   ├── src/web/              # responsive judge-facing interface
│   ├── fixtures/             # fictional packets and recorded cassettes
│   ├── evaluation/           # deterministic and live-only harnesses
│   ├── tests/                # standard-library unit suite
│   ├── demo/                 # sample receipt and report
│   └── MagnatSV_Report.pdf   # six-page technical report
├── evidence/                 # sanitized smoke and interrupted-run evidence
├── LICENSES/                 # documentation and synthetic-data notices
├── EVIDENCE.md               # evidence register and limitations
└── render.yaml               # public replay deployment blueprint
```

## Licence and attribution

- Source code: [Apache License 2.0](LICENSE)
- Documentation and design: [CC-BY-4.0](LICENSES/CC-BY-4.0-NOTICE.md)
- Contributor-authored synthetic data: [CDLA-Permissive-2.0](LICENSES/CDLA-PERMISSIVE-2.0-NOTICE.md)
- Apertus model weights are not redistributed by this repository.

## Hackathon

- **Event:** Hack Apertus 2026
- **Track:** 2B — Apertus Adoption: Own Project
- **Canonical project ID:** `49937`
- **Author:** **MagnatSV**
- **Repository:** https://github.com/chapaevv123/PolisProof
- **Demo:** https://polisproof.onrender.com
- **Video:** https://youtu.be/Wo-tzCz955A
- **Submission status:** `NOT_SUBMITTED`

---

<p align="center"><strong>AI can summarize a decision. PolisProof proves what was actually decided.</strong></p>
