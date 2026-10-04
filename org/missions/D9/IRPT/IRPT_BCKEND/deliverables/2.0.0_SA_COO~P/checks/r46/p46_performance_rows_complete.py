"""Round 46 (IRPT_BCKEND ~P, row S293 remainder / W114-S1; naming gate admits the edit @7de9db9085) -- the source map records what runs for the performance functions: the adapter and
the 49F producer carry their live deploy record, the Inflection producer gains its entry, and the 49F entry names its
live role.

Usage: python <this file> <repo_root> <criterion_id>
  IB46-1-AC1  in infra/aws/lambda/ci/lambda-source-map.json, read against live (boto3 get_function_configuration, us-east-1):
              irpt-performance-adapter, irpt-holdings-performance-lambda and irpt-inf-holdings-performance-lambda each carry
              deployed_code_sha256 = the live CodeSha256 and iam_role = the live role name; the Inflection row's
              tf_resource is module.irpt_holdings_performance_inf.aws_lambda_function.this. Base: FAIL.
  IB46-1-AC2  a GUARD: against base 7de9db9085, no function row outside the 49F and Inflection rows changes, and the only row added is
              irpt-inf-holdings-performance-lambda. Base: PASS.
  IB46-1-AC3  a GUARD: `.tools/comp-lambdamap check` reports no finding beyond the 14 it reports at the base (listed
              below), so the new entry adds no drift. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
ROWS = ["irpt-performance-adapter", "irpt-holdings-performance-lambda", "irpt-inf-holdings-performance-lambda"]
NEW = "irpt-inf-holdings-performance-lambda"
INF_TF = "module.irpt_holdings_performance_inf.aws_lambda_function.this"
BASE = "7de9db9085"
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
        print("%s FAIL" % (cid or "IB45-1"))
        sys.exit(1)

    now = json.loads((root / MAP).read_bytes().decode("utf-8"))["functions"]
    if cid == "IB46-1-AC1":
        import boto3
        lam = boto3.client("lambda", region_name="us-east-1")
        for fn in ROWS:
            row = now.get(fn)
            if not row:
                fail("%s has no row" % fn)
            cfg = lam.get_function_configuration(FunctionName=fn)
            live_sha, live_role = cfg["CodeSha256"], cfg["Role"].split("/")[-1]
            if row.get("deployed_code_sha256") != live_sha:
                fail("%s deployed_code_sha256 %s != live %s" % (fn, row.get("deployed_code_sha256"), live_sha))
            if row.get("iam_role") != live_role:
                fail("%s iam_role %s != live %s" % (fn, row.get("iam_role"), live_role))
            print("OK: %s = live (%s, %s)" % (fn, live_sha[:8], live_role))
        if now[NEW].get("tf_resource") != INF_TF:
            fail("%s tf_resource is %r" % (NEW, now[NEW].get("tf_resource")))
        if now[NEW].get("tf_file") != now["irpt-holdings-performance-lambda"].get("tf_file"):
            fail("%s tf_file %r differs from the 49F row's" % (NEW, now[NEW].get("tf_file")))
    elif cid == "IB46-1-AC2":
        r = subprocess.run(["git", "show", "%s:%s" % (BASE, MAP)], cwd=str(root), capture_output=True)
        if r.returncode or not r.stdout:
            fail("cannot read %s at %s (rc=%d)" % (MAP, BASE, r.returncode))
        base = json.loads(r.stdout.decode("utf-8"))["functions"]
        added, removed = set(now) - set(base), set(base) - set(now)
        if removed or not added <= {NEW}:
            fail("rows added %s, removed %s" % (sorted(added)[:5], sorted(removed)[:5]))
        moved = [fn for fn in base if fn not in ROWS[1:] and base[fn] != now[fn]]
        if moved:
            fail("rows outside the three changed: %s" % moved[:10])
        print("OK: %d rows; added %s; only the named rows may differ" % (len(now), sorted(added)))
    elif cid == "IB46-1-AC3":
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
