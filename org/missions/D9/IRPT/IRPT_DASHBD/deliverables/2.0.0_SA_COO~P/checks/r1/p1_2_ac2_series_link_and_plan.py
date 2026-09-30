"""IRPT_DASHBD round 1 AC (DB-b-2, FWD-1 hop 2) -- the served series REPRODUCES the gold, and the publisher's Terraform plans clean.

Usage: python p1_2_ac2_series_link_and_plan.py <worktree root>
(a) SEAM: for the thread account 0027265115, three windows of 20 consecutive series days (the first 20, the middle 20, the last 20):
    the geometric link of `total_return_daily` from series equals the link over the gold account_return_daily rows read for the
    same dates (abs diff <= 1e-9), and series `value` equals the gold `market_value_eod` on those days.
(b) PLAN: the file org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-publish.plan.txt (the worker's
    saved `terraform plan -no-color` of infra/aws/terraform/investor-reporting/reporting-publish/) reads "0 to destroy", names
    aws_lambda_function, aws_iam_role and aws_scheduler_schedule additions, and the schedule name irpt-49f-reporting-publish-daily.
Pass line: DB-2-AC2 PASS. Base (at the cut): FAIL -- no series object and no plan file.
"""
import gzip
import io
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))
THREAD = "0027265115"
PLAN = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-publish.plan.txt"


def fail(msg):
    print("DB-2-AC2 FAIL: " + msg)
    sys.exit(1)


from lib import opal_naming as on  # noqa: E402
import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def get(uri):
    b, k = uri[5:].split("/", 1)
    return s3.get_object(Bucket=b, Key=k)["Body"].read()


try:
    series = json.loads(gzip.decompress(get(on.address("irpt", "49financial", "platinum", "reporting", "account=%s" % THREAD, "series.json.gz"))))
except Exception as exc:  # noqa: BLE001
    fail("series unreadable: %s" % str(exc)[:160])
dates = series["date"]
n = len(dates)
if n < 60:
    fail("series has %d days (need >= 60 for three 20-day windows)" % n)
windows = [(0, 20), (n // 2 - 10, n // 2 + 10), (n - 20, n)]
for lo, hi in windows:
    link_series = 1.0
    for i in range(lo, hi):
        link_series *= 1.0 + float(series["total_return_daily"][i] or 0.0)
    link_gold = 1.0
    for i in range(lo, hi):
        d = dates[i]
        rows = pq.read_table(io.BytesIO(get(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % d) + "/data.parquet"))).to_pylist()
        row = next((r for r in rows if str(r["account_id"]) == THREAD), None)
        if row is None:
            fail("gold date=%s has no row for %s though series does" % (d, THREAD))
        link_gold *= 1.0 + float(row["total_return_daily"] or 0.0)
        if abs(float(series["value"][i]) - float(row["market_value_eod"])) > 1e-6:
            fail("date=%s series value %r != gold market_value_eod %r" % (d, series["value"][i], row["market_value_eod"]))
    if abs(link_series - link_gold) > 1e-9:
        fail("window %s..%s link: series %.12f != gold %.12f" % (dates[lo], dates[hi - 1], link_series, link_gold))
    print("  window %s..%s: link %.6f reproduces the gold" % (dates[lo], dates[hi - 1], link_series - 1.0))

if not PLAN.exists():
    fail("plan file absent: %s" % PLAN)
txt = PLAN.read_text(encoding="utf-8", errors="replace")
m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", txt)
if not m:
    fail("plan file carries no 'Plan:' line")
if int(m.group(3)) != 0:
    fail("plan destroys %s resource(s)" % m.group(3))
for res in ("aws_lambda_function", "aws_iam_role", "aws_scheduler_schedule"):
    if not re.search(r"# .*%s\.\S+ will be created" % re.escape(res), txt):
        fail("plan does not create a %s" % res)
if "irpt-49f-reporting-publish-daily" not in txt:
    fail("plan does not name the schedule irpt-49f-reporting-publish-daily")
print("  plan: %s to add, %s to change, 0 to destroy" % (m.group(1), m.group(2)))
print("DB-2-AC2 PASS")
