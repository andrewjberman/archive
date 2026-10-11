"""IB128-1 (0.9.0_WK_IRPT_BCKEND~289), AMENDMENTS 1 and 2: capture the NORMALIZED analysis-input-upload answer by the SAME
handler path as intake/tests/test_deferred_resolution.py::test_resident_resolves_through_the_broker_to_the_12_03_frozen_input
(served.Entry.handle -> intake/uploads.py:_normalized_response), with the in-memory fakes that test builds, and exactly TWO differences:
  1. the acting principal's firm id is the synthetic fir_000000000000000000000001 (the test module's claims() default x-firm-id is replaced in memory);
  2. IRPT_FIRM_REGISTRY points at ib128_synthetic_firm_registry.json (set BEFORE any packaged module is imported).
No file under any tests/ folder, no handler and no real registry is edited. LOCAL ONLY; synthetic values only.
Usage (repo root): python <this> ; writes .scratch/answers/analysis-input-upload.json (git-ignored)."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.popen("git -C \"%s\" rev-parse --show-toplevel" % HERE).read().strip())
SYNTH = str(HERE / "ib128_synthetic_firm_registry.json")
os.environ["IRPT_FIRM_REGISTRY"] = SYNTH  # BEFORE any packaged module is imported
SYNTH_FIRM = "fir_000000000000000000000001"

IR = ROOT / "infra/aws/lambda/investor-reporting"
sys.path.insert(0, str(IR / "intake/tests"))
import test_uploads as legacy  # noqa: E402  (also puts intake/, _authz/, _scope/, _ids/ on sys.path)
import ids  # noqa: E402

assert ids._find_registry() == SYNTH, ids._find_registry()
assert ids.firm_ids() == (SYNTH_FIRM,), ids.firm_ids()

_orig_claims = legacy.claims
legacy.claims = lambda **changes: _orig_claims(**{"x-firm-id": SYNTH_FIRM, **changes})  # difference 1, in memory only

import test_deferred_resolution as t  # noqa: E402
import test_resolution_broker as broker_world  # noqa: E402

fixture = t.case
make_case = getattr(fixture, "_get_wrapped_function", None)
make_case = make_case() if make_case else fixture.__wrapped__
case = make_case()

first = t.post(case, t.payload())
_, _, operation, raw, calls, wrapped, _, resolver = broker_world.world(
    {"body": [broker_world.row("AAPL"), broker_world.row("VNQ")]})
retained = t.resolve(case, resolver)
assert retained["state"] == t.NORMALIZED and len(calls) == 1, retained

# the SAME final POST the test makes, but keeping the whole envelope served.Entry.handle returns
envelope = legacy.build_upload_entry(case.service).handle({"routeKey": legacy.ROUTE,
    "headers": case.headers, "body": json.dumps(t.payload())})
assert "data" in envelope, envelope
data = envelope["data"]
assert data["state"] == t.NORMALIZED and data["upload_id"] == first["upload_id"], data
assert data["portfolio"]["holdings"]["total_dollars"] == "12.03"
assert case.owner["firm_id"] == SYNTH_FIRM, case.owner["firm_id"]

out = ROOT / ".scratch/answers"
out.mkdir(parents=True, exist_ok=True)
(out / "analysis-input-upload.json").write_text(json.dumps(envelope), encoding="utf-8")
print("OK: captured operation=%s state=%s firm=%s registry=%s" % (envelope.get("operation"), data["state"], case.owner["firm_id"], SYNTH))
