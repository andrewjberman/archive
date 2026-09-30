"""RIV-d-2 AC1 -- the SERVED page: the day's page exists at the builder's platinum prefix in the real bucket, leads
with BASG's trades, names the newest BASG report date, and its manifest says the publish Lambda wrote it and every
guardrail passed (or is NOT-APPLICABLE)."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

RECORD = "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/0.9.0_WK_ETFS_RIVALS~5/d2_live.json"


def run(v):
    import boto3

    root = c.setup_path()
    rec = json.loads((root / RECORD).read_text(encoding="utf-8"))
    day = rec["act_day"]
    uri = c.address("rivalfunds", "etfs", "platinum", "page", f"date={day}")
    bucket, key = uri[5:].split("/", 1)
    s3 = boto3.client("s3", region_name="us-east-1")
    html = s3.get_object(Bucket=bucket, Key=f"{key}/index.html")["Body"].read().decode("utf-8")
    man = json.loads(s3.get_object(Bucket=bucket, Key=f"{key}/manifest.json")["Body"].read())
    t, h = html.find('id="trades"'), html.find('id="holdings"')
    v.check(t != -1 and h != -1 and t < h, f"served page {uri}/index.html leads with trades")
    newest = rec.get("newest_basg_report_date")
    v.check(bool(newest) and newest in html, f"the page names the newest BASG report date ({newest})")
    v.check(man.get("runtime") == "rivalfunds-publish-page-lambda", f"written by the publish Lambda ({man.get('runtime')})")
    res = {x["check"]: x["status"] for x in man.get("checks", [])}
    v.check(len(res) == 6 and all(s in ("PASS", "NOT-APPLICABLE") for s in res.values()), f"six guardrails PASS/NOT-APPLICABLE ({res})")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
