"""IRPT_DASHBD round 26b (workstream B, issuer 2.0.0_SA_COO~D2) -- FWD-8's split Black Diamond pull, on Andrew's per-use word (MSTR msg
1103, record @5ef6d33141): ONE read-only pull, 2,299 accounts, 2,299 calls, 4,598 date ranges, each closure segment split at 2025-01-09
(1.0.0_SA_CTO~DELL2 round-19 analysis @b402b7b2e3 section 2). This cell builds the plan OFFLINE; the LIVE run is the issuer's act.

The denominator is `deliverables/0.9.0_WK_IRPT_DASHBD~14/CLOSURE_ALIGN_E1P.json` rows: one {account, segment {start, end}} per closure
segment, 2,299 rows, 2,299 accounts.

Usage: python <this file> <repo_root> <criterion_id>
  DB26-3-AC1  SPLIT_PULL_PLAN.json: dry_run true, vendor_calls 0; requests == accounts == 2,299 == the record's rows, ranges == 4,598;
              every request carries exactly two ranges, (segment start .. 2025-01-08) and (2025-01-10 .. segment end); each landing
              key equals the round-14 `_address(on, pull, bd_internal_id)` for the plan's `pull` token, and that token is not one of the
              `existing_pull_prefixes` the plan lists from S3. Base: FAIL.
  DB26-3-AC2  the offline tests tests/test_bd_split_pull.py pass (>= 6) and name `split`, `--go` and `denominators`. Base: FAIL.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RECORD = D + "0.9.0_WK_IRPT_DASHBD~14/CLOSURE_ALIGN_E1P.json"
W = D + "0.9.0_WK_IRPT_DASHBD~25/"
PLAN = W + "SPLIT_PULL_PLAN.json"
TESTS = W + "tests/test_bd_split_pull.py"
PULL6 = D + "0.9.0_WK_IRPT_DASHBD~6/bd_population_pull_e3.py"
LEFT_END, RIGHT_START = "2025-01-08", "2025-01-10"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB26-3"))
        sys.exit(1)

    def load(rel):
        p = root / rel
        if not p.is_file():
            fail("no %s" % rel)
        return json.loads(p.read_bytes().decode("utf-8"))

    if cid == "DB26-3-AC1":
        rows = load(RECORD)["rows"]
        seg = {r["account"]: r["segment"] for r in rows}
        plan = load(PLAN)
        if plan.get("dry_run") is not True or plan.get("vendor_calls") != 0:
            fail("dry_run %r, vendor_calls %r" % (plan.get("dry_run"), plan.get("vendor_calls")))
        reqs = plan.get("request_list") or []
        accts = [r.get("account") for r in reqs]
        if len(reqs) != len(rows) or set(accts) != set(seg) or len(set(accts)) != len(accts):
            fail("%d requests over %d distinct accounts; the record holds %d" % (len(reqs), len(set(accts)), len(rows)))
        bad = []
        for r in reqs:
            s = seg[r["account"]]
            want = [{"start": s["start"], "end": LEFT_END}, {"start": RIGHT_START, "end": s["end"]}]
            got = [{"start": x.get("start"), "end": x.get("end")} for x in (r.get("ranges") or [])]
            if got != want:
                bad.append(r["account"])
        if bad:
            fail("%d requests whose two ranges are not the split segment, e.g. %s" % (len(bad), bad[:3]))
        nranges = sum(len(r["ranges"]) for r in reqs)
        if nranges != 2 * len(rows):
            fail("%d ranges, want %d" % (nranges, 2 * len(rows)))
        pull = str(plan.get("pull") or "")
        if not pull or pull in (plan.get("existing_pull_prefixes") or []) or plan.get("existing_pull_prefixes") is None:
            fail("pull token %r empty, already landed, or no existing_pull_prefixes listed" % pull)
        sys.path.insert(0, str(root))
        from lib import opal_naming as on
        spec = importlib.util.spec_from_file_location("pull6", str(root / PULL6))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        wrong = [r["account"] for r in reqs if r.get("landing_key") != m._address(on, pull, r.get("bd_account"))]
        if wrong:
            fail("%d landing keys are not builder output, e.g. %s" % (len(wrong), wrong[:3]))
        print("OK: %d requests, %d accounts, %d ranges split at 2025-01-09; pull=%s (not among %d landed); builder keys; 0 vendor calls" % (
            len(reqs), len(set(accts)), nranges, pull, len(plan["existing_pull_prefixes"])))
    elif cid == "DB26-3-AC2":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        miss = [w for w in ("split", "--go", "denominators") if w not in src]
        if miss:
            fail("tests do not name %s" % miss)
        rr = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(t)], cwd=str(root),
                            capture_output=True, text=True, timeout=110)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (rr.stdout or "") + (rr.stderr or ""))
        m = re.search(r"(\d+) passed", out)
        if rr.returncode or not m or int(m.group(1)) < 6:
            fail("pytest: %s" % out[-300:])
        print("OK: %s offline tests pass" % m.group(1))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
