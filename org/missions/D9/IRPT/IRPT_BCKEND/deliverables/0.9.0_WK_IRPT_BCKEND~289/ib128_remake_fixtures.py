"""IB128-1 (0.9.0_WK_IRPT_BCKEND~289): write the two thin fixtures' `instance` from the handler answers captured by
ib128_capture.sh. The `data` member is taken as returned; the wrapper's _fixture/_expect are kept, _source is updated.
Usage (repo root): python <this> ; run ib128_capture.sh first."""
import json
FX = "infra/aws/lambda/investor-reporting/_contracts/fixtures/"
A = ".scratch/answers/"
JOBS = [
    ("DirectoryPage.valid.json", "directory-browse.json",
     "RE-MADE BY THE HANDLER (IB-pr-430, 0.9.0_WK_IRPT_BCKEND~289): `data` of the SECOND (last, next_cursor null) page answered by "
     "directory/entry.py ENTRY.handle for GET /api/scoped/investor-reporting/directory/browse, run by the unaltered test "
     "directory/tests/test_bootstrap_browse.py::test_initial_page_and_continuation_are_whole_and_stable (in-memory fakes, synthetic values), "
     "captured by ib128_capture.sh; schema docs/contracts/investor-reporting/v1/DirectoryPage.schema.json"),
    ("AnalysisUploadResult.valid.json", "analysis-input-upload.json",
     "RE-MADE BY THE HANDLER (IB-pr-430, 0.9.0_WK_IRPT_BCKEND~289): `data` of the NORMALIZED answer built by intake/uploads.py "
     "(_normalized_response) through served.Entry.handle for POST analysis-input-upload, written exactly as captured by "
     "ib128_capture_upload.py (run via ib128_capture.sh) on the same handler path and in-memory fakes as the test "
     "intake/tests/test_deferred_resolution.py::test_resident_resolves_through_the_broker_to_the_12_03_frozen_input, with TWO "
     "differences from that test: the acting principal's firm id is the synthetic fir_000000000000000000000001, and the firm registry is the synthetic "
     "ib128_synthetic_firm_registry.json (one enabled client firm, fir_000000000000000000000001) through the environment variable IRPT_FIRM_REGISTRY; "
     "schema docs/contracts/investor-reporting/v1/AnalysisUploadResult.schema.json"),
]
for fx, ans, source in JOBS:
    p = FX + fx
    wrapper = json.load(open(p, encoding="utf-8"))
    answer = json.load(open(A + ans, encoding="utf-8"))
    wrapper["_source"] = source
    wrapper["instance"] = answer["data"]
    open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(wrapper, indent=2, ensure_ascii=True) + "\n")
    print("OK: wrote", fx, list(wrapper))
