"""IRPT_DASHBD round 28 B (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's round-27 analysis: E1 measures and fixes the realized-lot
key (87 ids repeat within 2026-10-06's frame over 175 rows in 36 accounts, none identical in every column); E2 batches the lots stage so
its peak does not grow with the population. LOCAL: no S3 write.

Usage: python <this file> <repo_root> <criterion_id>
  DB28-1-AC1  LOT_KEY_E1.json: rows_read == 175 (the repeated-id rows of 2026-10-06); key_columns non-empty; unique_under_key == 175;
              `minimality` lists, for each column of key_columns, the unique count with that column dropped, and every one is < 175.
              Base: FAIL.
  DB28-1-AC2  the realized-lot contract's primary_key contains every key column; the producer's tests pass, including a test whose name
              contains "true_duplicate" (a planted row identical in every column still refuses) and one whose name contains
              "shared_id" (distinct lots sharing an id are kept). Base: FAIL.
  DB28-2-AC1  BATCHED_E2.json: population_count >= 7,000 and accounts_run equal to it; lots_stage_completed true; `runs` holds >= 2 runs
              with distinct batch_size, each with lots {wall_seconds, peak_mb} and total {wall_seconds, peak_mb}; the lots peak is FLAT
              across them -- max / min <= 1.25 (stated here before the run); handler_sha256 and producer_sha256 equal HEAD's bytes.
              The verdict against 2,048 MB is printed, not graded. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

W = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~27/"
KEY = W + "LOT_KEY_E1.json"
BATCH = W + "BATCHED_E2.json"
G = "data/assets/scripts/gold/irpt_reporting/"
PRODUCER = G + "account_activity_lots.py"
TESTS = G + "tests/test_account_activity_lots.py"
HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
REALIZED = "org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json"
FLAT = 1.25


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB28"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB28-1-AC1":
        r = load(KEY)
        cols, n, u = r.get("key_columns") or [], r.get("rows_read"), r.get("unique_under_key")
        if n != 175 or u != 175 or not cols:
            fail("rows_read %r, unique_under_key %r, key_columns %r" % (n, u, cols))
        mini = {m.get("dropped"): m.get("unique") for m in r.get("minimality") or []}
        missing = [c for c in cols if c not in mini]
        if missing or [c for c in cols if not isinstance(mini[c], int) or mini[c] >= 175]:
            fail("minimality %r does not show every key column necessary" % mini)
        print("OK: 175 of 175 unique under %s; dropping any one leaves %s" % (cols, {c: mini[c] for c in cols}))
    elif cid == "DB28-1-AC2":
        cols = load(KEY).get("key_columns") or []
        pk = load(REALIZED).get("primary_key") or []
        if [c for c in cols if c not in pk]:
            fail("realized primary_key %r lacks key columns %r" % (pk, [c for c in cols if c not in pk]))
        t = (root / TESTS).read_bytes().decode("utf-8") if (root / TESTS).is_file() else ""
        for w in ("true_duplicate", "shared_id"):
            if not re.search(r"^def test_\w*%s\w*\(" % w, t, re.M):
                fail("no test whose name contains %r" % w)
        rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(root / TESTS)], cwd=str(root),
                            capture_output=True, text=True, timeout=110)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
        m = re.search(r"(\d+) passed", out)
        if rr.returncode or not m:
            fail("pytest: %s" % out[-300:])
        print("OK: realized primary_key %s carries the key; %s producer tests pass (true_duplicate, shared_id included)" % (pk, m.group(1)))
    elif cid == "DB28-2-AC1":
        r = load(BATCH)
        pop, run = r.get("population_count"), r.get("accounts_run")
        if not isinstance(pop, int) or pop < 7000 or run != pop or r.get("lots_stage_completed") is not True:
            fail("population %r, accounts_run %r, lots_stage_completed %r" % (pop, run, r.get("lots_stage_completed")))
        runs = r.get("runs") or []
        sizes = {x.get("batch_size") for x in runs}
        if len(runs) < 2 or len(sizes) < 2:
            fail("%d runs over batch sizes %r" % (len(runs), sizes))
        peaks = []
        for x in runs:
            lots, tot = x.get("lots") or {}, x.get("total") or {}
            if None in (lots.get("wall_seconds"), lots.get("peak_mb"), tot.get("wall_seconds"), tot.get("peak_mb")):
                fail("run %r incomplete" % x.get("batch_size"))
            peaks.append(float(lots["peak_mb"]))
        if max(peaks) / min(peaks) > FLAT:
            fail("lots peaks %r are not flat (max/min %.2f > %s)" % (peaks, max(peaks) / min(peaks), FLAT))
        got = {"handler_sha256": hashlib.sha256((root / HANDLER).read_bytes()).hexdigest(),
               "producer_sha256": hashlib.sha256((root / PRODUCER).read_bytes()).hexdigest()}
        bad = [k for k, v in got.items() if r.get(k) != v]
        if bad:
            fail("%s differ from HEAD's bytes" % bad)
        verdict = "within 2,048 MB" if max(float(x["total"]["peak_mb"]) for x in runs) <= 2048 else "OVER 2,048 MB"
        print("OK: %d accounts, lots completed; lots peaks %s MB over batch sizes %s (flat, max/min %.2f); total peak %s" % (
            run, [round(p) for p in peaks], sorted(sizes), max(peaks) / min(peaks), verdict))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
