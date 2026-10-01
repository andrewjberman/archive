"""IRPT_DASHBD round 1 AC (DB-b-2, FWD-1 hop 2) -- the served series REPRODUCES the gold, a null breaks the link, and the
publisher's Terraform plans clean. Rewritten counterexample-first (rows IRPT_DASHBD-S6 limb d, S7).

Usage: python p1_2_ac2_series_link_and_plan.py <worktree root>
       python p1_2_ac2_series_link_and_plan.py --self-test     (no AWS: the counterexamples must each FAIL, the good windows PASS)

(a) SEAM: for the thread account, three windows of 20 consecutive series days (the first 20, the middle 20, the last 20). In each
    window `compare_window` is the whole rule, and it is what --self-test exercises:
      - a null `total_return_daily` is a GAP: it is null in the series exactly where it is null in the gold, and nowhere else. It
        is never read as 0.0 (the table contract and the SERIES contract both say a null breaks the link);
      - the window is linked in SEGMENTS between gaps, and every segment's product in the series equals the gold's (1e-9);
      - series `value` equals the gold `market_value_eod` on every day (1e-6).
    The number of gaps per window is printed.
(b) PLAN: org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-publish.plan.txt reads "0 to destroy",
    names aws_lambda_function, aws_iam_role and aws_scheduler_schedule additions, and the schedule irpt-49f-reporting-publish-daily.
Pass line: DB-2-AC2 PASS. Base (at the cut): FAIL -- no series object and no plan file.
"""
import gzip
import io
import json
import math
import re
import sys
from pathlib import Path


def segments(returns):
    """[(first index, last index, product)] for each run of non-null returns; a null ends a run and starts no product."""
    out, start, prod = [], None, 1.0
    for i, r in enumerate(returns):
        if r is None:
            if start is not None:
                out.append((start, i - 1, prod))
            start, prod = None, 1.0
            continue
        value = float(r)
        if math.isnan(value) or math.isinf(value):
            raise ValueError("return at index %d is not finite: %r" % (i, r))
        if start is None:
            start = i
        prod *= 1.0 + value
    if start is not None:
        out.append((start, len(returns) - 1, prod))
    return out


def compare_window(series_returns, gold_returns, series_values, gold_values):
    """Failures of one window; empty = the series reproduces the gold. Also returns the gap count."""
    out = []
    if not (len(series_returns) == len(gold_returns) == len(series_values) == len(gold_values)):
        return ["window lengths differ"], 0
    gaps = 0
    for i, (s, g) in enumerate(zip(series_returns, gold_returns)):
        if (s is None) != (g is None):
            out.append("day %d: series return %r but gold return %r (a null is a gap in both or in neither)" % (i, s, g))
        gaps += s is None
    for i, (sv, gv) in enumerate(zip(series_values, gold_values)):
        if sv is None or gv is None or abs(float(sv) - float(gv)) > 1e-6:
            out.append("day %d: series value %r != gold market_value_eod %r" % (i, sv, gv))
    if out:
        return out, gaps
    try:
        seg_s, seg_g = segments(series_returns), segments(gold_returns)
    except ValueError as exc:
        return [str(exc)], gaps
    for (a, b, ps), (_a, _b, pg) in zip(seg_s, seg_g):
        if abs(ps - pg) > 1e-9:
            out.append("segment days %d..%d: series link %.12f != gold link %.12f" % (a, b, ps, pg))
    return out, gaps


def self_test():
    good = [0.001] * 20
    vals = [100.0 + i for i in range(20)]
    with_gap = good[:7] + [None] + good[8:]
    cases = [
        ("good: 20 measured days, identical", good, good, vals, vals, False),
        ("good: one gap, null in both, linked in two segments", with_gap, with_gap, vals, vals, False),
        ("COUNTER: the series carries 0.0 where the gold is null (the old check linked across it as zero)",
         good[:7] + [0.0] + good[8:], with_gap, vals, vals, True),
        ("COUNTER: the series is null where the gold has a number", with_gap, good, vals, vals, True),
        ("COUNTER: one day's return differs by 1 basis point", good[:3] + [0.0011] + good[4:], good, vals, vals, True),
        ("COUNTER: a value differs from the gold", good, good, vals[:5] + [999.0] + vals[6:], vals, True),
    ]
    bad = 0
    for name, sr, gr, sv, gv, must_fail in cases:
        failures, gaps = compare_window(sr, gr, sv, gv)
        verdict = bool(failures) == must_fail
        bad += not verdict
        print("  %s %-100s -> %s" % ("ok " if verdict else "BAD", name, failures[0] if failures else "holds (%d gap(s))" % gaps))
    print("SELF-TEST %s: %d of %d cases behave as declared (%d counterexamples must fail, %d good windows must hold)"
          % ("PASS" if not bad else "FAIL", len(cases) - bad, len(cases), sum(c[5] for c in cases), sum(not c[5] for c in cases)))
    return 1 if bad else 0


def fail(msg):
    print("DB-2-AC2 FAIL: " + msg)
    sys.exit(1)


def _thread_account(root):
    """The thread account: the seat's record deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json; the check FAILS without
    it rather than falling back to a typed account (every round-1 check reads the thread account from that file)."""
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json"
    try:
        return str(json.loads(p.read_text(encoding="utf-8"))["thread_account"])
    except (OSError, ValueError, KeyError) as exc:
        fail("THREAD_ACCOUNT.json unreadable (%s): %s" % (type(exc).__name__, p))


def main(root):
    sys.path.insert(0, str(root))
    thread = _thread_account(root)
    plan = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-publish.plan.txt"
    from lib import opal_naming as on
    import boto3
    import pyarrow.parquet as pq

    s3 = boto3.client("s3", region_name="us-east-1")

    def get(uri):
        bucket, key = uri[5:].split("/", 1)
        return s3.get_object(Bucket=bucket, Key=key)["Body"].read()

    try:
        series = json.loads(gzip.decompress(get(on.address("irpt", "49financial", "platinum", "reporting", "account=%s" % thread, "series.json.gz"))))
    except Exception as exc:  # noqa: BLE001
        fail("series unreadable: %s" % str(exc)[:160])
    dates = series["date"]
    n = len(dates)
    if n < 60:
        fail("series has %d days (need >= 60 for three 20-day windows)" % n)
    for lo, hi in [(0, 20), (n // 2 - 10, n // 2 + 10), (n - 20, n)]:
        gold_r, gold_v = [], []
        for i in range(lo, hi):
            d = dates[i]
            rows = pq.read_table(io.BytesIO(get(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % d) + "/data.parquet"))).to_pylist()
            row = next((r for r in rows if str(r["account_id"]) == thread), None)
            if row is None:
                fail("gold date=%s has no row for %s though series does" % (d, thread))
            gold_r.append(row["total_return_daily"])
            gold_v.append(row["market_value_eod"])
        failures, gaps = compare_window(series["total_return_daily"][lo:hi], gold_r, series["value"][lo:hi], gold_v)
        if failures:
            fail("window %s..%s: %s" % (dates[lo], dates[hi - 1], "; ".join(failures[:3])))
        print("  window %s..%s: reproduces the gold in %d segment(s), %d gap day(s)" % (dates[lo], dates[hi - 1], gaps + 1, gaps))

    if not plan.exists():
        fail("plan file absent: %s" % plan)
    txt = plan.read_text(encoding="utf-8", errors="replace")
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


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve())
