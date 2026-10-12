# Current Apertus access — verified 2026-10-12

## CSCS managed API

- Base URL: `https://api.inference.cscs.ch/v1`
- Chat endpoint: `/v1/chat/completions`
- Authentication: Bearer API key (`CSCS_INFERENCE_API_KEY`)
- Models: `swiss-ai/Apertus-v1.5-8B` and `swiss-ai/Apertus-v1.5-70B`
- Compatibility: OpenAI-compatible; responses can include prompt, completion,
  and total-token usage.
- Access: an active CSCS project from an open call, partnership, or cscs2go;
  the project PI/deputy provisions an inference resource, then a member creates
  a key in the Inference API UI.
- Limits: token budgets and reset periods can be key-specific; global resource
  limits also apply. No universal hackathon quota or concurrency limit was
  found in current public documentation.
- Hackathon/Discord: public pages direct participants to Discord for discussion
  but do not state that Discord onboarding itself grants API access.

First-party sources:

- https://docs.cscs.ch/services/inference/api/
- https://huggingface.co/swiss-ai/Apertus-v1.5-8B
- https://huggingface.co/swiss-ai/Apertus-v1.5-70B
- https://hackapertus.ch/online-hack

## Local weights

Both checkpoints can be self-hosted with vLLM or SGLang through an
OpenAI-compatible endpoint. Hugging Face login and acceptance of the
Apache-2.0 licence, AUP, and contact-information gate are required to download
the files. Local inference avoids a hosted API key but requires appropriate
accelerator capacity; official examples use tensor parallelism for 70B.

## Hugging Face routed smoke verification

Verified on 2026-10-12 without recording the credential:

- Authentication: valid user access token.
- Live 8B route: `swiss-ai/Apertus-8B-Instruct-2509:publicai`, priced at
  USD 0.10/M input tokens and USD 0.20/M output tokens in HF's authenticated
  router catalog.
- Live 70B route: `swiss-ai/Apertus-70B-Instruct-2509:featherless-ai`.
  Featherless lists the Apertus 70B class at USD 0.875/M input tokens and
  USD 2.075/M output tokens.
- The v1.5 8B checkpoint had no provider mapping; the v1.5 70B checkpoint's
  Featherless mapping reported `error`. These are availability observations,
  not statements about downloadable weights.
- Both bounded smoke calls returned HTTP 200 and `POLISPROOF_OK`. Full sanitized
  evidence is in `evidence/live/smoke_2026-10-12.json`.

Pricing sources:

- https://router.huggingface.co/v1/models
- https://featherless.ai/docs/request-pricing-and-credits

## Owner action

Use an authorized CSCS project inference resource and create a scoped API key
at `https://ui.inference.cscs.ch`, or obtain the hackathon-provided access
instructions from the participant portal/Discord. Configure the key locally as
`CSCS_INFERENCE_API_KEY` and optionally set
`LLM_BASE_URL=https://api.inference.cscs.ch/v1`. Never paste the key into chat,
source control, issue trackers, or evidence files.
