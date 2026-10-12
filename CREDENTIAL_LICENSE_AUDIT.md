# Credential and licence audit — 2026-10-13

## Credentials

- `HF_TOKEN`: absent from the current process environment.
- `LLM_API_KEY` and `LLM_BASE_URL`: absent from the current process environment.
- Repository scan found no Hugging Face token-shaped value, bearer token, or
  populated API-key assignment.
- `.env` is ignored; `.env.example` contains placeholders only.
- Saved live records contain errors, model metadata, latency, and sanitized
  response details, but no authorization header or API key.

Result: **PASS for public-content secret hygiene**, subject to repeating a
platform-native secret scan immediately before publication.

## Licences

- Root `LICENSE`: Apache License 2.0; appropriate for source code.
- Documentation declares CC-BY-4.0.
- Synthetic data declares CDLA-Permissive-2.0 and contains no personal data.
- Third-party model weights are not redistributed.
- No vendored dependency tree is present; runtime application code uses the
  Python standard library.

Result: **PASS**. Explicit CC-BY-4.0 and CDLA-Permissive-2.0 notices are now
included under `LICENSES/`, alongside the root Apache-2.0 code licence.
