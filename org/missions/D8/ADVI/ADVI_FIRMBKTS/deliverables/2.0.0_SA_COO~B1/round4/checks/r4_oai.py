"""ADVI_FIRMBKTS round 4: the OAI's PRE-FLIP read for act 4 (the CTO's act-4 ADDENDUM 3, msg 3984), issuer 2.0.0_SA_COO~B1.

The OAI reads S3 only for a viewer request that passes the validator, and no seat here mints a session. So, before the flip:
  O1 the router oracle (`r4_oracle.mjs`, the router's own handler) prints nine (bucket, key) pairs, one per served class; each
     bucket is the canonical bucket and each key lies under ONE of the nine served prefixes the LIVE bucket policy's OAI Allow
     names (read from the document), and no pair is a 404 or 401 from the router;
  O2 a HEAD of one real key under each of the nine served prefixes at the new home succeeds (the actor's admitted identity),
     the denominator printed;
  O3 the OAI statement of the new bucket is byte-equal, in principal and action, to the OAI statement serving opal-data-bd
     today (the positive control; the resource differs by design: nine prefixes against the whole bucket).
A difference in any arm is a STOP.

  python r4_oai.py [--simulate-flip] [--firm 49financial] [--bucket opal-data-49financial] [--legacy opal-data-bd]
Last line: ROUND 4 OAI PREFLIGHT: <n> of 3 arms. READ-ONLY (get-bucket-policy, list-objects-v2 max-keys 1, head-object).
Plain ASCII; never prints an object body or a client identifier beyond the class prefix and a count.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OAI = "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E139998VWH0PD"
AWS = os.environ.get("AWS_CLI") or shutil.which("aws") or shutil.which("aws.cmd") or "aws"
BUN = shutil.which("bun") or "bun"


def aws(*a):
    r = subprocess.run([AWS] + list(a) + ["--output", "json"], capture_output=True, text=True, timeout=120)
    if r.returncode:
        return None, (r.stderr.strip().splitlines() or ["failed"])[-1][:160]
    return json.loads(r.stdout or "{}"), ""


def _lst(x):
    return x if isinstance(x, list) else [x]


def oai_stmts(bucket):
    d, err = aws("s3api", "get-bucket-policy", "--bucket", bucket)
    if d is None:
        return None, err
    st = json.loads(d["Policy"])["Statement"]
    out = []
    for s in st:
        p = s.get("Principal")
        a = p.get("AWS") if isinstance(p, dict) else p
        if s.get("Effect") == "Allow" and OAI in _lst(a or []):
            out.append(s)
    return out, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--simulate-flip", action="store_true")
    ap.add_argument("--firm", default="49financial")
    ap.add_argument("--bucket", default="opal-data-49financial")
    ap.add_argument("--legacy", default="opal-data-bd")
    a = ap.parse_args()
    res = []
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()

    new_st, e1 = oai_stmts(a.bucket)
    prefixes = []
    if new_st and len(new_st) == 1:
        for r in _lst(new_st[0].get("Resource", [])):
            pre = "arn:aws:s3:::%s/" % a.bucket
            if r.startswith(pre) and r.endswith("*"):
                prefixes.append(r[len(pre):-1])
    # O1
    cmd = [BUN, os.path.join(HERE, "r4_oracle.mjs"), "--firm", a.firm] + (["--simulate-flip"] if a.simulate_flip else [])
    o = subprocess.run(cmd, capture_output=True, text=True, timeout=110, cwd=root)
    rows = []
    try:
        rows = json.loads(o.stdout.strip().splitlines()[-1])["rows"]
    except (ValueError, IndexError, KeyError):
        pass
    ok1 = len(rows) == 9 and len(prefixes) == 9 and all(
        r.get("status") == "pass" and r.get("bucket") == a.bucket
        and any((r.get("key") or "").startswith(p) for p in prefixes) for r in rows)
    print("  O1 oracle rows=%d (simulate_flip=%s); OAI prefixes in the live policy=%d; pairs inside=%d" % (
        len(rows), a.simulate_flip, len(prefixes),
        sum(1 for r in rows if any((r.get("key") or "").startswith(p) for p in prefixes))))
    res.append(("O1 nine oracle pairs, each in the canonical bucket under one of the OAI's nine prefixes", ok1))

    # O2
    heads = 0
    for p in prefixes:
        d, err = aws("s3api", "list-objects-v2", "--bucket", a.bucket, "--prefix", p, "--max-keys", "1")
        k = ((d or {}).get("Contents") or [{}])[0].get("Key")
        if not k:
            continue
        h, err = aws("s3api", "head-object", "--bucket", a.bucket, "--key", k)
        if h is not None:
            heads += 1
    print("  O2 HEAD of one real key per OAI prefix: %d of %d" % (heads, len(prefixes)))
    res.append(("O2 a HEAD of one real key under each of the nine prefixes succeeds", len(prefixes) == 9 and heads == 9))

    # O3
    old_st, e3 = oai_stmts(a.legacy)
    ok3 = False
    if new_st and old_st and len(new_st) == 1:
        def key(s):
            return (sorted(_lst((s.get("Principal") or {}).get("AWS"))), sorted(_lst(s.get("Action"))))
        ok3 = any(key(new_st[0]) == key(s) for s in old_st)
    print("  O3 new OAI statements=%s legacy OAI statements=%s equal principal+action=%s" % (
        len(new_st or []), len(old_st or []), ok3))
    res.append(("O3 the OAI statement equals the one serving the legacy bucket in principal and action", ok3))

    for n, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", n))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 OAI PREFLIGHT: %d of 3 arms" % n)
    return 0 if n == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
