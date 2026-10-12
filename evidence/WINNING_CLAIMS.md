# Winning-claim validation — 2026-10-12

| Claim | Status | Evidence boundary |
|---|---|---|
| A. Most cases can stay on 8B. | UNSUPPORTED | Only 3-packet synthetic replay routing exists; no live 30-packet result. |
| B. 70B is reserved for genuinely ambiguous cases. | PARTIALLY_SUPPORTED | Code selectively routes non-verified/material conflicts, but live route precision is unmeasured. |
| C. Routing materially reduces expensive large-model work. | UNSUPPORTED | Harness calculates calls and provider-reported tokens, but no live comparator exists. |
| D. Deterministic verification catches errors model-only processing misses. | SUPPORTED | Frozen deterministic tests catch amount/date/currency/negation/condition/source/hash faults and prompt injection; 12/12 pass. This is a system claim, not a live-model comparison. |
| E. Sovereign deployment can keep source records local. | SUPPORTED | Replay is network-free; official Apertus weights support local OpenAI-compatible serving; CSCS states processing remains in its Swiss infrastructure and prompts/responses are not recorded. |

Only D and E are currently suitable as headline claims. A–C require genuine
live results from `POLISPROOF_EVAL_V1`.
