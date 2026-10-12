# PolisProof architecture

Author: MagnatSV

```text
fictional or user-supplied documents
                  |
          normalize + SHA-256
                  |
       Apertus 8B claim extraction
                  |
       strict schema/parser boundary
                  |
 deterministic evidence + conflict gate
          |                    |
      verified          disputed claims only
                               |
                   Apertus 70B review context
                               |
                 gate-owned final verdict
                               |
            evidence report + JSON receipt
```

The LLM proposes claims; it never owns the verdict. Exact-span checks, source
hashes, conflict rules, and fail-closed behavior remain application-controlled.

## Deployment boundary

The code is designed for an OpenAI-compatible endpoint. The judged sovereign
target is an on-premise or air-gapped deployment of the open Apertus weights.
The Hugging Face route is only a hosted integration demonstration and is not
described as sovereign, local, or air-gapped. Replay and deterministic fallback
are network-free, but they do not prove local Apertus inference.
