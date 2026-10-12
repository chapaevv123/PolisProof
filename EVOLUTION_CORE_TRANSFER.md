# Evolution Core transfer evidence

Reusable improvements produced by the PolisProof sprint:

1. **Execution-state provenance.** Every output distinguishes
   `LIVE_APERTUS`, `RECORDED_REPLAY`, `OFFLINE_FALLBACK`, and `ERROR`. Transfer
   this enum and its UI visibility to any agent that mixes live and cached
   inference.
2. **Provider errors are not benchmark scores.** Aggregate only successful
   model responses into quality, safety, and routing denominators; retain
   provider-error attempts and latency separately.
3. **Interrupted-run recovery.** Persist one sanitized record per fixture and
   support offline re-summarization, allowing a partial run to be audited
   without repeating paid calls.
4. **Model output is evidence, not authority.** Bind claims to exact source
   spans and hashes; keep verdict logic deterministic and fail closed.
5. **Selective escalation.** Route disputed claims to the larger model and
   capture the reason, rather than treating model size as authority.
6. **Spend-aware evaluation.** Freeze the corpus, bound fixtures and output
   tokens, record provider-reported usage when available, and never infer a
   billing amount from missing metadata.
7. **Artifact isolation gate.** Validate tests, evaluation, and schemas without
   parent paths, secrets, caches, or network access before publication.

Concrete implementation evidence is in
`track_2b/evaluation/live_benchmark.py`, especially `--summarize-existing`,
successful-run filtering, per-fixture evidence files, and fail-closed
credential handling.
