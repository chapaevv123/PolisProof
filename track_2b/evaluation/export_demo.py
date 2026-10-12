from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from polisproof.pipeline import PolisProofPipeline

receipt = PolisProofPipeline(ROOT, "replay").compile_fixture("demo_conflict")
demo = ROOT / "demo"
demo.mkdir(exist_ok=True)
(demo / "sample_audit_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
report = receipt["human_report"]
(demo / "sample_decision_report.md").write_text(
    "# PolisProof decision report\n\n"
    f"**Execution:** {receipt['execution_mode']}  \n"
    f"**Verdict:** {receipt['verification_status']}  \n"
    f"**Reasons:** {', '.join(receipt['reason_codes'])}  \n"
    f"**Receipt:** `{receipt['output_hash']}`\n\n"
    "## Verified record\n\n- Approved ceiling: EUR 40,000\n- Legal review: required\n\n"
    "The fictional EUR 60,000 annex is a proposal, not unconditional approval.\n\n"
    f"> {report['disclaimer']}\n", encoding="utf-8")
print(receipt["output_hash"])
