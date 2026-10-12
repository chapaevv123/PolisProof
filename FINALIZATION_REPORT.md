# PolisProof finalization report — 2026-10-13

## Canonical status

- Project ID: `49937`
- Hackathon / track: Hack Apertus 2026 / 2B
- Public author: MagnatSV
- Participation status: `BUILDING`
- Submission status: `NOT_SUBMITTED`

## Recovered state

The previous sprint had completed the application, replay evaluation, live
smoke proof, six-page report rendering, and most submission copy. Port 8877
was not listening when this sprint resumed. Several unrelated or
permission-obscured Python processes existed, but none held a network socket;
no process was terminated. The interrupted live benchmark had saved 18
records: six each for 8B, 70B, and routed mode.

## Verification completed in this sprint

- Local unit suite: 44/44 passed.
- Frozen deterministic evaluation: 12/12 passed.
- Receipt schema: valid.
- Frozen live corpus: valid, 30 packets.
- HTTP replay smoke on `127.0.0.1:8877`: health 200; demo compile 200;
  `RECORDED_REPLAY`; `BLOCKED`; `AMOUNT_CONFLICT,MISSING_CONDITION`; 64-character
  output hash. The temporary server was stopped after the check.
- PDF: `track_2b/MagnatSV_Report.pdf`, six pages (six PDF page objects and six
  rendered page previews).
- Secret scan: no token-shaped or API-key assignment found in project files;
  only `.env.example` matched credential-related filenames.

## Live Apertus evidence

Earlier authenticated smoke calls genuinely reached Apertus 8B and 70B and
returned HTTP 200. Their calculated total cost was USD 0.000080925. The later
bounded benchmark sample reached downstream providers but all 18 saved runs
failed with HTTP 403 / Cloudflare error 1010. They are provider failures, not
model-quality failures. The summary now excludes them from quality,
adversarial, and routing-rate denominators and reports those metrics as
`UNAVAILABLE`.

No live request was made in this sprint: `HF_TOKEN`, `LLM_API_KEY`, and
`LLM_BASE_URL` were absent from the current environment. Additional spend was
USD 0.00; cumulative calculated spend remains USD 0.000080925, below the
USD 0.50 sprint cap.

## Deliverables

- Runnable project and browser demo: complete locally.
- Honest live evidence and benchmark harness: complete; corpus-level quality
  results unavailable because the provider denied the bounded sample.
- Technical PDF: complete, six pages.
- Video package: published at `https://youtu.be/Wo-tzCz955A` (86 seconds).
- Public repository: `https://github.com/chapaevv123/PolisProof`.
- Public replay demo: `https://polisproof.onrender.com`.
- Hackathon submission: checklist and copy ready; intentionally not submitted.

## Remaining owner actions

1. Review the published repository, replay demo, video, and licence notices.
2. Securely inject a scoped `HF_TOKEN` only if another provider preflight or
   benchmark attempt is desired; do not paste it into chat or files.
3. Complete private form
   fields, submit, retain confirmation evidence, and only then change
   `NOT_SUBMITTED`.
