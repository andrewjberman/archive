"""Round 47 (IRPT_BCKEND ~P, CTO ROUND ANALYSIS rounds 42-46 item E3; row S178 by batch 234's class rule) -- the source map
records the live code of the six investor-reporting functions that lag it.

Usage: python <this file> <repo_root> <criterion_id>
  IB47-2-AC1  in infra/aws/lambda/ci/lambda-source-map.json, each of the six FUNCS rows carries deployed_code_sha256 = the
              live CodeSha256 (boto3 get_function_configuration, us-east-1, read now). Base: FAIL (all six lag).
  IB47-2-AC2  a GUARD: against base 2fd59da001, no row outside the six changes and none is added or removed.
              irpt-ycharts-generate is excluded: it is 2.0.0_SA_COO~Y's moving row (S320). Base: PASS.
  IB47-2-AC3  a GUARD: `.tools/comp-lambdamap check` (run through Git Bash) reports no finding beyond the 14 at the base.
              Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FUNCS = ["irpt-directory-refresh", "irpt-directory-search", "irpt-export-render", "irpt-holdings-refresh-lambda",
         "irpt-intake-poller", "irpt-narrative"]
MOVING = {"irpt-ycharts-generate"}
BASE = "2fd59da001"
BASE_FINDINGS = {
    "MISSING_ENTRY amgt-resapp-chatter-axis", "MISSING_ENTRY daily-sprint-generator",
    "MISSING_ENTRY find-insure-crawl-job-posting-{board}", "MISSING_ENTRY opal-49f-value-parity",
    "MISSING_ENTRY opal-data-refresh-api-qa-scratch", "MISSING_ENTRY opal-ms-ingest-liveness",
    "MISSING_ENTRY opal-otp-liveness", "MISSING_ENTRY opal-research-pull-enqueue", "MISSING_ENTRY opal-sentinel",
    "ORPHAN_ENTRY bd-fees-trigger", "WRONG_SOURCE_DIR bd-fees-trigger",
    "WRONG_SOURCE_DIR seeking-alpha-analysis-coordinator", "WRONG_SOURCE_DIR seeking-alpha-analysis-listing-parser",
    "WRONG_SOURCE_DIR seeking-alpha-analysis-scraper",
}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB47-2"))
        sys.exit(1)

    now = json.loads((root / MAP).read_bytes().decode("utf-8"))["functions"]
    if cid == "IB47-2-AC1":
        import boto3
        lam = boto3.client("lambda", region_name="us-east-1")
        for fn in FUNCS:
            live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            got = (now.get(fn) or {}).get("deployed_code_sha256")
            if got != live:
                fail("%s deployed_code_sha256 %s != live %s" % (fn, got, live))
            print("OK: %s = live %s" % (fn, live[:8]))
    elif cid == "IB47-2-AC2":
        r = subprocess.run(["git", "show", "%s:%s" % (BASE, MAP)], cwd=str(root), capture_output=True)
        if r.returncode or not r.stdout:
            fail("cannot read %s at %s (rc=%d)" % (MAP, BASE, r.returncode))
        base = json.loads(r.stdout.decode("utf-8"))["functions"]
        if set(base) != set(now):
            fail("rows added %s, removed %s" % (sorted(set(now) - set(base))[:5], sorted(set(base) - set(now))[:5]))
        moved = [fn for fn in base if fn not in FUNCS and fn not in MOVING and base[fn] != now[fn]]
        if moved:
            fail("rows outside the six changed: %s" % moved[:10])
        print("OK: %d rows; only the six (and ~Y's moving row) may differ" % len(now))
    elif cid == "IB47-2-AC3":
        sys.path.insert(0, str(root / ".tools"))
        from git_bash_resolver import bash_argv  # a bare "bash" resolves to WSL on this host
        r = subprocess.run(bash_argv(".tools/comp-lambdamap", "check"), cwd=str(root), capture_output=True, timeout=300)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
        if "DRIFT:" not in out and "OK" not in out:
            fail("comp-lambdamap check produced no verdict (rc=%d): %s" % (r.returncode, out[-300:]))
        found = set(" ".join(m) for m in re.findall(r"^\s*\[([A-Z_]+)\] ([^:]+):", out, re.M))
        extra = found - BASE_FINDINGS
        if extra:
            fail("new drift findings: %s" % sorted(extra))
        print("OK: %d finding(s), all present at the base (%d)" % (len(found), len(BASE_FINDINGS)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
