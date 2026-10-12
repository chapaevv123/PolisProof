# PolisProof hosting record

## Recommendation

The public replay demo is deployed as a **Render Web Service** at
`https://polisproof.onrender.com`. PolisProof is a
small state-free Python HTTP service, needs no database, and already has a
Dockerfile. Render supports Python/Docker web services and supplies a public
TLS URL. Configure health check `/api/health`, root directory `track_2b`, and
run in replay mode with no secrets.

Expected cost: **USD 0** on the Free instance while within Render's included
limits. Free services sleep after 15 minutes without inbound traffic and may
take about one minute to wake. Open the URL several minutes before judging and
run the demo once. The filesystem is ephemeral, which is acceptable because
receipts are downloaded in the browser and no server persistence is required.

## Hugging Face Spaces

A Docker Space is technically compatible: use `sdk: docker`, expose the
configured app port, and run the same standard-library server. CPU Basic is 2
vCPU, 16 GB RAM, and non-persistent disk—far more than replay mode needs.
However, current Hugging Face policy requires a paid account plan to create a
Gradio or Docker Space even though CPU Basic itself has no hourly hardware
charge. Therefore it is not the preferred zero-cost path for a new account.
Static Spaces are free but cannot run PolisProof's Python verification API.

If live inference is enabled later, store `HF_TOKEN` only in the platform's
encrypted Secrets settings, never as a repository variable or file. The public
demo should remain replay mode for reliability and zero inference spend.

## Other options

- GitHub Pages cannot run the Python backend. It is suitable only for a
  separately rewritten static showcase, not the real application.
- Local recording at `http://127.0.0.1:8877/` has no cold start, no external
  dependency, and is the preferred video-recording path.

## Render preparation

The repository includes `render.yaml`. The deployed service reports HTTP 200
at `/api/health` with `mode: REPLAY` and `live_configured: false`. Repository
publication and deployment are complete; no paid upgrade has been initiated.
