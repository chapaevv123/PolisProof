# PolisProof — 115-second recording plan

Creator and voiceover: MagnatSV. Hard limit: 120 seconds.

## Before recording

1. Start the server from `artifacts/polisproof/track_2b`:
   `$env:PYTHONPATH='src'; python -m polisproof.server --host 127.0.0.1 --port 8877 --mode replay`
2. Open `http://127.0.0.1:8877/` in a 1920×1080 browser at 100% zoom.
3. Select **Multilingual budget conflict**, refresh once, and confirm the header
   says `RECORDED REPLAY`. Close bookmarks/download bars and notifications.
4. Do one rehearsal. Delete the rehearsal receipt from Downloads before the
   final take so the exported filename is easy to identify.

## Exact walkthrough and narration

| Time | Browser action | Narration |
|---:|---|---|
| 0–14 s | Hold on the title and three trust points. | “Public decisions are scattered across minutes, annexes and legal notes. PolisProof is sovereign, evidence-first AI that verifies what was actually decided.” |
| 14–29 s | Point to the demo question, then the visible `RECORDED REPLAY` label. | “This fictional case asks whether sixty thousand euros was approved unconditionally. For a reliable demo, this is clearly labelled deterministic recorded replay—not live inference.” |
| 29–47 s | Inspect the three source cards: German final minutes, French draft annex, Italian final note. | “The draft proposes sixty thousand euros. Final German minutes cap approval at forty thousand, and the Italian note requires legal review.” |
| 47–53 s | Click **Run analysis** once. | “I run the same evidence pipeline used by the application.” |
| 53–76 s | In **Evidence analysis**, point to each extracted claim and exact quoted span. | “Apertus extracts atomic claims, but every claim must cite an exact span from a hashed source document. The model is evidence to check, never authority.” |
| 76–94 s | Point to `BLOCKED`, then `AMOUNT CONFLICT` and `MISSING CONDITION`. | “Application-owned rules detect both the conflicting amount and the omitted authorization condition. The final verdict is blocked.” |
| 94–106 s | Point to execution mode, Apertus 8B → 70B route, and receipt hash. | “The audit trail records execution provenance, selective escalation and a tamper-evident output hash. Replay is never presented as live.” |
| 106–112 s | Click **Download JSON receipt**. Briefly show the downloaded file indicator. | “One click exports the complete JSON audit receipt for independent review.” |
| 112–115 s | Scroll slightly to “Models propose. Evidence decides.” | “PolisProof: models propose; evidence decides.” |

## Reliability checks

- Do not switch to live mode during recording.
- Do not click **Run analysis** more than once.
- Required visible outcome: `BLOCKED`, `AMOUNT CONFLICT`, `MISSING CONDITION`,
  `RECORDED REPLAY`, `Apertus 8B → Apertus 70B`, and a receipt hash.
- Confirm the exported JSON has `execution_mode: RECORDED_REPLAY`, three claims,
  two reason codes, and a 64-character `output_hash`.
- Target final duration: 115 seconds; reject any export longer than 120 seconds.
