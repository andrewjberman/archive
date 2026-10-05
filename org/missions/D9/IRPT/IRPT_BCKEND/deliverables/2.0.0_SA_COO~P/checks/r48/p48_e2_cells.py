"""Round 48 (IRPT_BCKEND ~P, E2 of the CTO's rounds 42-46 analysis, on E1's LIVE list @db0adf0053).

Usage: python <this file> <repo_root> <criterion_id>
  IB48-1-AC1  (S278) the test infra/aws/lambda/ci/tests/test_sha_handoff.sh exits 0 and prints at least 2 lines starting
              "PASS": a base64 sha holding '/' and '+' is written into a temp source map verbatim, and a malformed written
              value is refused by the post-write assertion. Base: FAIL (no test).
  IB48-1-AC2  (S278 guard) `bash -n infra/aws/lambda/ci/build-and-upload.sh` passes and build-and-upload.sh no longer reads the
              sha through process.env.SHA256. Base: FAIL (it does).
  IB48-2-AC1  (S322/S178) lambda-source-map.json carries rows irpt-49f-reporting-{gold,publish,read}-lambda, each with
              deployed_code_sha256 and iam_role equal to live, and no longer carries the keys irpt-reporting-{gold,publish,
              read}-lambda (which name no live function). Base: FAIL.
  IB48-2-AC2  (S322 guard) against base 123258bd51, no source-map row outside those six keys changes (irpt-ycharts-generate,
              ~Y's moving row, excepted), and comp-lambdamap check (Git Bash) reports no finding beyond the 14 at the base.
              Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "123258bd51"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
NEW = ["irpt-49f-reporting-gold-lambda", "irpt-49f-reporting-publish-lambda", "irpt-49f-reporting-read-lambda"]
OLD = ["irpt-reporting-gold-lambda", "irpt-reporting-publish-lambda", "irpt-reporting-read-lambda"]
MOVING = {"irpt-ycharts-generate"}
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
    sys.path.insert(0, str(root / ".tools"))
    from git_bash_resolver import bash_argv  # a bare "bash" resolves to WSL on this host

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB48"))
        sys.exit(1)

    if cid == "IB48-1-AC1":
        t = root / "infra/aws/lambda/ci/tests/test_sha_handoff.sh"
        if not t.is_file():
            fail("no infra/aws/lambda/ci/tests/test_sha_handoff.sh")
        r = subprocess.run(bash_argv(str(t)), cwd=str(root), capture_output=True, timeout=300)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
        n = sum(1 for ln in out.splitlines() if ln.startswith("PASS"))
        if r.returncode or n < 2:
            fail("rc=%d, %d PASS line(s): %s" % (r.returncode, n, out[-400:]))
        print("OK: %d PASS lines, rc 0" % n)
    elif cid == "IB48-1-AC2":
        f = root / "infra/aws/lambda/ci/build-and-upload.sh"
        r = subprocess.run(bash_argv("-n", str(f)), cwd=str(root), capture_output=True, timeout=60)
        if r.returncode:
            fail("bash -n: %s" % r.stderr.decode("utf-8", "replace")[-300:])
        if "process.env.SHA256" in f.read_bytes().decode("utf-8"):
            fail("build-and-upload.sh still reads process.env.SHA256")
        print("OK: bash -n passes; no process.env.SHA256 hand-off")
    elif cid == "IB48-2-AC1":
        import boto3
        lam = boto3.client("lambda", region_name="us-east-1")
        now = json.loads((root / MAP).read_bytes().decode("utf-8"))["functions"]
        for fn in NEW:
            row = now.get(fn)
            if not row:
                fail("%s has no row" % fn)
            cfg = lam.get_function_configuration(FunctionName=fn)
            if row.get("deployed_code_sha256") != cfg["CodeSha256"] or row.get("iam_role") != cfg["Role"].split("/")[-1]:
                fail("%s != live (%s/%s vs %s/%s)" % (fn, row.get("deployed_code_sha256"), row.get("iam_role"),
                                                     cfg["CodeSha256"], cfg["Role"].split("/")[-1]))
            print("OK: %s = live" % fn)
        stale = [k for k in OLD if k in now]
        if stale:
            fail("stale keys remain: %s" % stale)
    elif cid == "IB48-2-AC2":
        now = json.loads((root / MAP).read_bytes().decode("utf-8"))["functions"]
        r = subprocess.run(["git", "show", "%s:%s" % (BASE, MAP)], cwd=str(root), capture_output=True)
        base = json.loads(r.stdout.decode("utf-8"))["functions"]
        allowed = set(NEW) | set(OLD) | MOVING
        moved = [k for k in set(base) | set(now) if k not in allowed and base.get(k) != now.get(k)]
        if moved:
            fail("rows outside the six keys changed: %s" % moved[:8])
        r = subprocess.run(bash_argv(".tools/comp-lambdamap", "check"), cwd=str(root), capture_output=True, timeout=300)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
        if "DRIFT:" not in out and "OK" not in out:
            fail("comp-lambdamap produced no verdict")
        extra = set(" ".join(m) for m in re.findall(r"^\s*\[([A-Z_]+)\] ([^:]+):", out, re.M)) - BASE_FINDINGS
        if extra:
            fail("new drift findings: %s" % sorted(extra))
        print("OK: only the six keys moved; comp-lambdamap adds no finding")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
