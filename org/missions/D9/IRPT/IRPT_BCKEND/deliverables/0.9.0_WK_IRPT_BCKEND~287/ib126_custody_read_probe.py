"""IB126 custody-report-read probe (worker 0.9.0_WK_IRPT_BCKEND~287, IRPT_BCKEND.TO-IB-pr-428). READ ONLY, LOCAL ONLY.

No existing test calls `custody-report-read` through the guarded Entry and holds the whole envelope:
export/tests/test_custody_read.py calls the compute function (`custody_read.custody_report_read`) and sees
only the `data` payload. This module is NOT product code and NOT a replacement for that test. It reuses,
unaltered, the fixtures of export/tests/test_custody_writer_composed.py (the in-memory retention world and
the REAL deployed handler `entry.lambda_handler` pointed at recorded storage), persists one custody report
exactly as that file's own `test_guarded_or_scheduled_a_verified_opal_caller_persists_through_the_entry`
does, then asks the same handler for it back on the read route. The envelope is captured by
ib126_capture_plugin.py (IB126_WRAP=entry.lambda_handler IB126_OP=custody-report-read).

Run from infra/aws/lambda/investor-reporting/export/tests with PYTHONPATH naming this folder.
"""
from test_custody_writer_composed import (  # noqa: F401  (fixtures + names, reused unaltered)
    TENANT, _opal_headers, entry, retention_world, served_entry, world)

READ_ROUTE = "GET /api/scoped/investor-reporting/custody-report/{reportId}"


def test_ib126_custody_report_read_through_the_real_entry(served_entry):  # noqa: F811
    w = served_entry
    persisted = w.call(_opal_headers())
    assert persisted.get("ok") is not False, persisted
    ref = persisted["data"]
    event = {"routeKey": READ_ROUTE, "headers": _opal_headers(),
             "pathParameters": {"reportId": ref["report_id"]},
             "queryStringParameters": {"revision": ref["revision"], "selected_tenant": TENANT}}
    answer = entry.lambda_handler(event, None)
    assert answer.get("ok") is not False, {k: answer.get(k) for k in ("ok", "operation", "status")}
    assert answer["operation"] == "custody-report-read"
