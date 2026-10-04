"""Round 44 (IRPT_BCKEND ~P, row S264, CTO batch 234 item 1) -- the source map records the code that is live for
irpt-ycharts-generate, irpt-holdings and irpt-status (one record-terraform-deploy.sh --function run each).

Usage: python <this file> <repo_root> <criterion_id>
  IB44-2-AC1  in infra/aws/lambda/ci/lambda-source-map.json, each of the three rows' deployed_code_sha256 equals that
              function's live CodeSha256 (boto3 get_function_configuration, us-east-1, read now). Base: FAIL (all three
              differ: the map holds the 09-24 values).
  IB44-2-AC2  a GUARD: against base 80ba60328c, every OTHER function row of the source map is unchanged, and no row is
              added or removed. Base: PASS (no change).
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import subprocess
import sys
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FUNCS = ["irpt-ycharts-generate", "irpt-holdings", "irpt-status"]
BASE = "80ba60328c"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB44-2"))
        sys.exit(1)

    now = json.loads((root / MAP).read_bytes().decode("utf-8"))["functions"]
    if cid == "IB44-2-AC1":
        import boto3
        lam = boto3.client("lambda", region_name="us-east-1")
        for fn in FUNCS:
            live = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            got = (now.get(fn) or {}).get("deployed_code_sha256")
            if got != live:
                fail("%s: source map %s != live %s" % (fn, got, live))
            print("OK: %s deployed_code_sha256 = live %s" % (fn, live))
    elif cid == "IB44-2-AC2":
        r = subprocess.run(["git", "show", "%s:%s" % (BASE, MAP)], cwd=str(root), capture_output=True)
        if r.returncode or not r.stdout:
            fail("cannot read %s at %s (rc=%d)" % (MAP, BASE, r.returncode))
        base = json.loads(r.stdout.decode("utf-8"))["functions"]
        if set(base) != set(now):
            fail("rows added %s, removed %s" % (sorted(set(now) - set(base))[:5], sorted(set(base) - set(now))[:5]))
        moved = [fn for fn in base if fn not in FUNCS and base[fn] != now[fn]]
        if moved:
            fail("rows outside the three changed: %s" % moved[:10])
        print("OK: %d rows; only the three named rows may differ" % len(now))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
