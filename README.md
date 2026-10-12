# PolisProof

**AI can summarize a decision. PolisProof proves what was actually decided.**

PolisProof is an evidence-first verifier for multilingual public decisions.
It uses Apertus to extract atomic claims, binds them to exact source spans,
detects contradictions and missing conditions deterministically, and emits a
tamper-evident JSON receipt.

- Creator: **MagnatSV**
- Hackathon: Hack Apertus 2026, Track 2B — Own Project
- Canonical project ID: `49937`
- Status: locally complete; external publication and submission pending

The runnable template-compatible project is in `track_2b/`.

```powershell
cd track_2b
$env:PYTHONPATH='src'
python -m polisproof.server --host 127.0.0.1 --port 8877 --mode replay
```

Open `http://127.0.0.1:8877/` and select **Run analysis**. The interface is
optimized for a 1920×1080, 115-second demonstration and explicitly labels the
bundled synthetic result as `RECORDED_REPLAY`.

![PolisProof demo interface](track_2b/demo/website-preview.png)

For verification, run `python -m unittest discover -s tests -v`,
`python evaluation/run_eval.py`, and
`python evaluation/validate_artifacts.py` from `track_2b/`.

The default demo is network-free recorded replay and is visibly labelled as
such. Live Hugging Face inference requires `HF_TOKEN`, is separately labelled
`LIVE_APERTUS`, and uses the verified 2509 instruct checkpoints. See
`track_2b/README.md` for setup, architecture, evidence, and limitations.

No X/Twitter profile is required or represented as active. Repository and
video URLs remain intentionally blank until the owner publishes them.

Code is Apache-2.0. Documentation and synthetic-data licence notices are in
`LICENSES/`. See `HOSTING_PLAN.md` for the prepared zero-cost deployment path;
no external service has been created or deployed.
