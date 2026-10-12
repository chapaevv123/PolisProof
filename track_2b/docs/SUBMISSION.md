# Hack Apertus submission package

## Short description

PolisProof is a sovereign decision compiler for public records. Apertus 8B
extracts multilingual atomic claims from minutes, resolutions, and annexes;
application-owned checks bind each claim to exact evidence and block conflicts;
Apertus 70B reviews only disputed claims. The result is an auditable JSON
receipt—not another authoritative-sounding summary.

## Why it matters

Public decisions often span inconsistent versions and languages. A fluent
summary can silently promote a proposal into an approval or omit a legal
condition. PolisProof makes those failures visible and reviewable.

## Two-minute demo script

1. **0:00–0:15 — Problem.** Show the draft claim: “Council approved €60,000
   unconditionally.” Explain that all materials are fictional.
2. **0:15–0:35 — Packet.** Point to German final minutes, French draft annex,
   and Italian legal note. Run the bundled demo.
3. **0:35–1:05 — Proof.** Show atomic claims and verbatim source spans. Highlight
   the final €40,000 ceiling and required legal review.
4. **1:05–1:25 — Gate.** Show `BLOCKED`, `AMOUNT_CONFLICT`, and
   `MISSING_CONDITION`. Explain that deterministic checks—not the model—own the
   verdict.
5. **1:25–1:43 — Apertus.** Show the 8B extraction route and targeted 70B
   escalation with honest LIVE/REPLAY/FALLBACK status.
6. **1:43–1:55 — Receipt.** Export the JSON receipt and show hashes, evidence,
   model attribution, tokens, latency, and route.
7. **1:55–2:00 — Close.** “AI can summarize a decision. PolisProof proves what
   was actually decided.”

## Owner submission checklist

- [ ] Review all open-source contents and confirm they were created during the event.
- [ ] Run `make test`, `make eval`, and `make run` with Docker.
- [x] Add genuine minimal Apertus 8B/70B smoke evidence and retain the explicit
  limitation that the frozen corpus is still unrun.
- [x] Replace pending team/name fields in the technical report (`MagnatSV`).
- [x] Render `technical_report.md` to `MagnatSV_Report.pdf` (six pages).
- [ ] Record and upload a public demo video no longer than two minutes.
- [ ] Create a public repository from the official template and keep `track_2b/` unchanged (current package has no Git metadata).
- [ ] Confirm repository URL and video URL work in a private browser window.
- [ ] Optionally publish the evaluation dataset using the official HF dataset template.
- [ ] Complete the official form at `https://hackapertus.ch/online-hack/submissions` before 16 October 2026, 12:00 CEST / 13:00 Europe/Kyiv.
- [ ] Save submission confirmation evidence; only then mark `SUBMITTED`.

## Known limitations

Replay data is synthetic and never presented as live inference. Offline fallback
uses conservative pattern extraction and cannot replace multilingual Apertus.
Exact-span matching may send harmless formatting variations to review. A receipt
hash is tamper-evident, not a digital signature.
