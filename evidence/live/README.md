# LIVE_APERTUS evidence area

This directory is reserved exclusively for genuine live Apertus evidence.
Replay cassettes never belong here. A bounded two-call provider smoke test is
recorded in `smoke_2026-10-12.json`; full corpus records are produced only by
`make eval-live`.

Expected layout:

```text
live/
  smoke_2026-10-12.json
  8b/<fixture_id>.json
  70b/<fixture_id>.json
  routed/<fixture_id>.json
  summary.json
  results.md
```

Each packet record uses `polisproof.live-run.v1`, contains sanitized response
content and provider-reported usage when available, and never stores request
headers or credentials. Empty directories are intentionally not represented in
source control. A smoke record proves authentication and model execution but is
not a substitute for the three-mode frozen evaluation.
