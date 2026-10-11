"""ADVI_FIRMBKTS round 4: the LIVE reader of act 4's deployed units (the eleven units of the act-4 pair), issuer 2.0.0_SA_COO~B1.

READ-ONLY (lambda get-function-configuration / list-versions-by-function, cloudfront get-distribution-config). It compares
what is DEPLOYED with an expectation file the actor writes at the build (the artifacts' hashes, the published versions):

  {"irpt": {"<function>": "<base64 sha256 of the artifact>", ...8 entries},
   "edge": {"<function>": {"version": "<N>", "sha": "<base64 sha256>"}, ...3 entries: shared-advisor-router,
            shared-advisor-router-response, auth-validator-edge}}

--arms irpt --expect <file>     8 arms: each IRPT function's live CodeSha256 equals its expected artifact hash.
--arms edge --expect <file>     6 arms: for each edge function, the published version's CodeSha256 equals the expected hash
                                and EVERY association of that function on the distribution names that version (count printed).
Last line: ROUND 4 ACT 4 <IRPT|EDGE>: <n> of <N> arms. Plain ASCII; no object body and no client identifier is printed.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

DIST = "EVTSA9VEHNZVH"
AWS = os.environ.get("AWS_CLI") or shutil.which("aws") or shutil.which("aws.cmd") or "aws"


def aws(*a):
    r = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True, timeout=110)
    if r.returncode:
        return None, (r.stderr.strip().splitlines() or ["failed"])[-1][:140]
    return json.loads(r.stdout or "{}"), ""


def irpt(exp):
    res = []
    for fn, want in sorted(exp.get("irpt", {}).items()):
        d, err = aws("lambda", "get-function-configuration", "--function-name", fn, "--region", "us-east-1")
        got = (d or {}).get("CodeSha256")
        print("  %-34s live=%s expect=%s%s" % (fn, (got or "?")[:14], want[:14], (" (%s)" % err) if err else ""))
        res.append(("%s deployed code equals its artifact" % fn, got == want))
    return res


def edge(exp):
    res = []
    cfg, err = aws("cloudfront", "get-distribution-config", "--id", DIST)
    behaviors = []
    if cfg:
        dc = cfg["DistributionConfig"]
        behaviors = list((dc.get("CacheBehaviors") or {}).get("Items") or []) + [dc.get("DefaultCacheBehavior") or {}]
    arns = []
    for b in behaviors:
        for x in ((b.get("LambdaFunctionAssociations") or {}).get("Items") or []):
            arns.append(x.get("LambdaFunctionARN", ""))
    for fn, w in sorted(exp.get("edge", {}).items()):
        d, e2 = aws("lambda", "get-function-configuration", "--function-name", fn, "--qualifier", str(w["version"]),
                    "--region", "us-east-1")
        sha_ok = (d or {}).get("CodeSha256") == w["sha"]
        mine = [a for a in arns if (":function:%s:" % fn) in a]
        on_ver = [a for a in mine if a.endswith(":" + str(w["version"]))]
        print("  %-34s version %s sha_ok=%s associations=%d on_version=%d%s" % (
            fn, w["version"], sha_ok, len(mine), len(on_ver), (" (%s)" % e2) if e2 else ""))
        res.append(("%s version %s equals its artifact" % (fn, w["version"]), sha_ok))
        res.append(("%s: every association names version %s" % (fn, w["version"]), len(mine) > 0 and len(mine) == len(on_ver)))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("irpt", "edge"), required=True)
    ap.add_argument("--expect", required=True)
    a = ap.parse_args()
    try:
        exp = json.load(open(a.expect, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("ERROR: expectation file unreadable: %s" % type(e).__name__)
        print("ROUND 4 ACT 4 %s: 0 of 0 arms" % a.arms.upper())
        return 1
    res = irpt(exp) if a.arms == "irpt" else edge(exp)
    for n, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", n))
    k = sum(1 for _, ok in res if ok)
    total = len(res)
    want = 8 if a.arms == "irpt" else 6
    print("ROUND 4 ACT 4 %s: %d of %d arms" % (a.arms.upper(), k, want))
    return 0 if (k == total and total == want) else 1


if __name__ == "__main__":
    sys.exit(main())
