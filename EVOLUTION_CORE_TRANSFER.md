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

## Competition-publication improvements

8. **Evidence-backed technical communication.** Pair every prominent claim
   with a repository artifact, public endpoint, test command, or explicit
   limitation. Keep connectivity evidence separate from quality evidence.
9. **Competition README narrative.** Lead with the problem and real demo, then
   progressively disclose outcomes, architecture, evidence, reproduction, and
   limitations. Treat visual polish as navigation, not as proof.
10. **Reproducible public demos.** Use fictional versioned fixtures, expose the
    execution mode beside the verdict, and capture screenshots through the
    actual UI/API path at a declared viewport.
11. **Artifact provenance.** Label images, cassettes, receipts, reports, and
    live records by origin and execution mode; never let model names inside a
    replay cassette stand in for proof of execution.
12. **Publication hygiene.** Reconcile pending language after URLs go live,
    verify unauthenticated access, scan the exact Git diff for secrets/private
    data, and validate every relative README asset before pushing.
13. **Honest model disclosure.** State precisely what a successful smoke call
    proves, preserve provider failures, and render unavailable metrics as
    unavailable rather than zero.

## Candidates for later independent transfer tests

- Apply the README evidence ladder to a separate project and have a reviewer
  classify every quantitative claim as measured, inferred, or unavailable.
- Interrupt a paid benchmark mid-run and verify that offline recovery produces
  the same aggregate as a clean run over the saved records.
- Mix live, replay, fallback, and error receipts and test whether an unfamiliar
  reviewer can correctly identify provenance without inspecting source code.
- Run a publication gate on a seeded repository containing a fake secret,
  stale deployment claim, broken relative image, and misleading zero metric;
  require all four to be caught.
- Verify screenshot provenance by replaying the documented fixture through the
  public UI and comparing verdict, reason codes, claims, and receipt hash
  structure—not pixel identity.

These are transfer candidates only. No Evolution Score change is asserted.
