"""IB29-2-AC2 -- the seam with the real neighbour: a REAL retained READY Analysis report passes the submit path's validation
locally with the report's own as-of as its cutoff, no narrative step, and the analysis template (nothing submitted or written).

Reads deliverables/0.9.0_WK_IRPT_BCKEND~101/SUBMIT_ANALYSIS_R29.json:
  {"report_ref": {"bucket", "key", "report_id"}, "validated": true, "cutoff": "YYYY-MM-DD", "template": "...",
   "narrative_step": false}
Grades: the retained report reads back from S3; the record's cutoff equals the latest `as_of_date` among the report's sections;
validated is true; the template is analysis-portrait-letter; narrative_step is false. Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~101/SUBMIT_ANALYSIS_R29.json"


def fail(msg):
    print("FAIL: " + msg)
    print("IB29-2-AC2 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rp = root / REC
    if not rp.is_file():
        fail("no record at %s" % REC)
    rec = json.loads(rp.read_text(encoding="utf-8"))
    ref = rec.get("report_ref") or {}
    try:
        import boto3
        body = boto3.client("s3").get_object(Bucket=ref["bucket"], Key=ref["key"])["Body"].read()
    except Exception as exc:  # noqa: BLE001
        fail("the retained report does not read back: %s" % exc.__class__.__name__)
    report = json.loads(body)
    report = report.get("report", report) if isinstance(report, dict) else report
    dates = sorted(str(s.get("as_of_date"))[:10] for s in (report.get("sections") or [])
                   if isinstance(s, dict) and s.get("as_of_date"))
    if not dates:
        fail("the report's sections carry no as_of_date")
    if str(rec.get("cutoff"))[:10] != dates[-1]:
        fail("cutoff %r is not the report's latest section as_of_date %s" % (rec.get("cutoff"), dates[-1]))
    if rec.get("validated") is not True:
        fail("validated is not true")
    if rec.get("template") != "analysis-portrait-letter":
        fail("template %r" % rec.get("template"))
    if rec.get("narrative_step") is not False:
        fail("narrative_step is not false")
    print("OK: report %s validates; cutoff %s = latest section as-of; template analysis-portrait-letter; no narrative step" % (
        ref.get("report_id"), dates[-1]))
    print("IB29-2-AC2 PASS")


if __name__ == "__main__":
    main()
