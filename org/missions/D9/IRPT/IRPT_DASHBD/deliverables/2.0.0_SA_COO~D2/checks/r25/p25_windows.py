"""IRPT_DASHBD round 25 (workstream B, issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-24 analysis @99580aac8c: E2 measures the
lot-lag bound (W21-S5), E1 names and fixes the 4 non-rounding windows (W21-S4), E3 sets the pandas option once per process and hardens
the served producer's classify_and_sum against None (W21-S6). LOCAL: no S3 write, no deploy.

The round-24 record `deliverables/0.9.0_WK_IRPT_DASHBD~21/IDENTITY_REGRADE_E2.json` carries `regrade` (91 graded; 36 failures, 4 of
them not ROUNDING). This checker re-reads it as the denominator.

Usage: python <this file> <repo_root> <criterion_id>
  DB25-1-AC1  the lag distribution: LOT_LAG_E2.json `lags` {n > 0, percentiles {p50, p90, p95, p99, max}, counts_by_days summing to n},
              `leg_lag_days` (int) and `covered_percentile`; the share of lags <= leg_lag_days, re-derived from counts_by_days, is at
              least covered_percentile; the producer's `LEG_LAG_DAYS = <int>` equals leg_lag_days. Base: FAIL.
  DB25-2-AC1  the 4 windows read: WINDOWS_E1.json `windows` names exactly round 24's 4 non-ROUNDING accounts, each with non-empty
              `lot_events` and a non-empty `cause`. Base: FAIL.
  DB25-2-AC2  the 91-window re-run: `regrade` graded == 91, passed + failed == graded, one classed row per failure; the producer source
              names none of the 4 account ids (no per-account patch). Base: FAIL.
  DB25-3-AC1  the option once per process: a test in test_account_activity_lots.py whose name contains "thread" passes, and the whole
              file passes. Base: FAIL.
  DB25-3-AC2  the served producer hardened: tests/test_account_return_daily_none.py names classify_and_sum and passes (>= 1 test).
              Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

P = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
R24 = P + "0.9.0_WK_IRPT_DASHBD~21/IDENTITY_REGRADE_E2.json"
W = P + "0.9.0_WK_IRPT_DASHBD~22/"
LAG = W + "LOT_LAG_E2.json"
WIN = W + "WINDOWS_E1.json"
G = "data/assets/scripts/gold/irpt_reporting/"
PRODUCER = G + "account_activity_lots.py"
TESTS = G + "tests/test_account_activity_lots.py"
NONE_TESTS = G + "tests/test_account_return_daily_none.py"


def _load(root, rel, fail):
    p = root / rel
    if not p.is_file():
        fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def _pytest(root, args, fail):
    rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + args, cwd=str(root),
                        capture_output=True, text=True, timeout=110)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
    m = re.search(r"(\d+) passed", out)
    if rr.returncode or not m:
        fail("pytest %s: %s" % (args, out[-300:]))
    return int(m.group(1))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB25"))
        sys.exit(1)

    if cid == "DB25-1-AC1":
        rec = _load(root, LAG, fail)
        lags = rec.get("lags") or {}
        n = lags.get("n")
        pct = lags.get("percentiles") or {}
        counts = {int(k): int(v) for k, v in (lags.get("counts_by_days") or {}).items()}
        if not isinstance(n, int) or n <= 0 or sum(counts.values()) != n:
            fail("n %r against counts summing to %d" % (n, sum(counts.values())))
        miss = [k for k in ("p50", "p90", "p95", "p99", "max") if pct.get(k) is None]
        if miss:
            fail("percentiles lack %s" % miss)
        k = rec.get("leg_lag_days")
        cov = rec.get("covered_percentile")
        if not isinstance(k, int) or cov is None:
            fail("leg_lag_days %r or covered_percentile %r missing" % (k, cov))
        share = 100.0 * sum(v for d, v in counts.items() if d <= k) / n
        if share + 1e-9 < float(cov):
            fail("lags <= %d cover %.2f%%, below the stated %s" % (k, share, cov))
        src = (root / PRODUCER).read_bytes().decode("utf-8")
        m = re.search(r"^LEG_LAG_DAYS\s*=\s*(\d+)", src, re.M)
        if not m or int(m.group(1)) != k:
            fail("producer LEG_LAG_DAYS %r, record %r" % (m and m.group(1), k))
        print("OK: %d lags; p50 %s p90 %s p95 %s p99 %s max %s; LEG_LAG_DAYS %d covers %.2f%% (stated %s)" % (
            n, pct["p50"], pct["p90"], pct["p95"], pct["p99"], pct["max"], k, share, cov))
    elif cid in ("DB25-2-AC1", "DB25-2-AC2"):
        r24 = _load(root, R24, fail).get("regrade") or {}
        four = {f["account_id"] for f in r24.get("failures") or [] if f.get("class") != "ROUNDING"}
        rec = _load(root, WIN, fail)
        if cid == "DB25-2-AC1":
            wins = rec.get("windows") or []
            got = {w.get("account_id") for w in wins}
            if got != four or len(wins) != len(four):
                fail("windows %s, round 24's non-ROUNDING %s" % (sorted(got), sorted(four)))
            bad = [w["account_id"] for w in wins if not w.get("lot_events") or not str(w.get("cause") or "").strip()]
            if bad:
                fail("windows without lot events or a cause: %s" % bad)
            print("OK: %d windows read against lot events, each with its cause" % len(wins))
        else:
            r = rec.get("regrade") or {}
            fails = r.get("failures") or []
            if r.get("graded") != r24.get("graded") or r.get("passed", -1) + r.get("failed", -1) != r.get("graded"):
                fail("graded %r (round 24: %r), passed %r, failed %r" % (r.get("graded"), r24.get("graded"), r.get("passed"), r.get("failed")))
            if len(fails) != r.get("failed") or [f for f in fails if not f.get("class")]:
                fail("%d failure rows for failed=%r, or a failure without a class" % (len(fails), r.get("failed")))
            src = (root / PRODUCER).read_bytes().decode("utf-8")
            named = sorted(a for a in four if a in src)
            if named:
                fail("the producer names account ids %s (a per-account patch)" % named)
            by = {}
            for f in fails:
                by[f["class"]] = by.get(f["class"], 0) + 1
            print("OK: re-run over %d windows: %d tie, %d miss (%s); no account id in the producer" % (
                r["graded"], r["passed"], r["failed"], by))
    elif cid == "DB25-3-AC1":
        t = (root / TESTS).read_bytes().decode("utf-8") if (root / TESTS).is_file() else ""
        if not re.search(r"^def test_\w*thread\w*\(", t, re.M):
            fail("no test whose name contains 'thread' in %s" % TESTS)
        k = _pytest(root, [TESTS, "-k", "thread"], fail)
        total = _pytest(root, [TESTS], fail)
        print("OK: %d threaded test(s) pass; the file's %d tests pass" % (k, total))
    elif cid == "DB25-3-AC2":
        p = root / NONE_TESTS
        if not p.is_file() or "classify_and_sum" not in p.read_bytes().decode("utf-8"):
            fail("no %s naming classify_and_sum" % NONE_TESTS)
        k = _pytest(root, [NONE_TESTS], fail)
        print("OK: %d None-hardening test(s) pass" % k)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
