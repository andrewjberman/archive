"""IB28-1-AC2 -- the seam with the real neighbour: a REAL retained READY Analysis report, read back through the new export path,
yields a contract-valid bundle and an analysis print query (built locally; nothing submitted, rendered or written to AWS).

Reads deliverables/0.9.0_WK_IRPT_BCKEND~101/ANALYSIS_EXPORT_R28.json:
  {"report_ref": {"bucket", "key", "report_id", "revision"}, "request_status": "READY",
   "bundle_file": "<repo-relative path of the saved bundle JSON>", "print_query": {...}}
Grades: the retained report object exists in S3 at bucket/key and carries the AnalysisReport required keys; the saved bundle
carries every ExportBundle required key, exactly one authorized_report_revisions row naming the report's id and revision,
live_vendor_request_during_render false, and a non-empty selected_sections no longer than the report's sections; the print
query's kind is "analysis" and it names the report. Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~101/ANALYSIS_EXPORT_R28.json"


def fail(msg):
    print("FAIL: " + msg)
    print("IB28-1-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rp = root / REC
    if not rp.is_file():
        fail("no record at %s" % REC)
    rec = json.loads(rp.read_text(encoding="utf-8"))
    ref = rec.get("report_ref") or {}
    if rec.get("request_status") != "READY":
        fail("request_status %r is not READY" % rec.get("request_status"))
    schemas = root / "docs/contracts/investor-reporting/v1"
    rep_req = json.loads((schemas / "AnalysisReport.schema.json").read_text(encoding="utf-8"))["required"]
    bun_req = json.loads((schemas / "ExportBundle.schema.json").read_text(encoding="utf-8"))["required"]
    try:
        import boto3
        body = boto3.client("s3").get_object(Bucket=ref["bucket"], Key=ref["key"])["Body"].read()
    except Exception as exc:  # noqa: BLE001
        fail("the retained report does not read back: %s" % exc.__class__.__name__)
    report = json.loads(body)
    report = report.get("report", report) if isinstance(report, dict) else report
    missing = [k for k in rep_req if k not in report]
    if missing:
        fail("the retained object lacks AnalysisReport keys %s" % missing)
    bp = root / str(rec.get("bundle_file") or "")
    if not bp.is_file():
        fail("no saved bundle at %s" % rec.get("bundle_file"))
    bundle = json.loads(bp.read_text(encoding="utf-8"))
    missing = [k for k in bun_req if k not in bundle]
    if missing:
        fail("the bundle lacks ExportBundle keys %s" % missing)
    rows = bundle["authorized_report_revisions"]
    if len(rows) != 1 or rows[0].get("report_id") != ref.get("report_id") or rows[0].get("revision") != ref.get("revision"):
        fail("authorized_report_revisions does not name exactly the report")
    if bundle["live_vendor_request_during_render"] is not False:
        fail("live_vendor_request_during_render is not false")
    sel = bundle["selected_sections"]
    if not sel or len(sel) > len(report["sections"]):
        fail("selected_sections %d against %d report sections" % (len(sel or []), len(report["sections"])))
    q = rec.get("print_query") or {}
    if q.get("kind") != "analysis":
        fail("print_query kind %r" % q.get("kind"))
    if ref.get("report_id") not in json.dumps(q):
        fail("print_query does not name the report")
    print("OK: report %s rev %s READY; bundle %d of %d sections; print kind analysis" % (
        ref.get("report_id"), str(ref.get("revision"))[:12], len(sel), len(report["sections"])))
    print("IB28-1-AC2 PASS")


if __name__ == "__main__":
    main()
