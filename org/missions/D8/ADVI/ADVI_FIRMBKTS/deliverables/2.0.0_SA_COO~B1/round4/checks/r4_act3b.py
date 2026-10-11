"""ADVI_FIRMBKTS round 4: the LIVE read of act 3b (the readers' admission to opal-data-49financial), issuer 2.0.0_SA_COO~B1.

Reads the LIVE bucket policy (s3api get-bucket-policy, read-only) and compares it with the policy the REGISTRY renders at the
tree's HEAD (the module `opal_name` evaluated with `terraform console` on a mirror tree: the blanket Deny from
`fence_patterns` and `fence_exemption_arns`, then `fence_scoped_statements`, then `fence_scoped_allow_statements`).

--arms live [--root <tree>]  (3 arms)
  L1 the live policy's statements equal the rendered policy's, statement by statement after normalization (a one-element
     string is a one-element list; lists are sorted; the Sid names the pair), and neither side has a statement the other lacks
     (both counts printed).
  L2 no statement of the live policy allows a write or delete action, `s3:*`, or a bucket-wide object resource to any principal
     other than the named reader rows, and every Allow names exactly one principal ARN (never `*`).
  L3 an UNSIGNED anonymous GET of the ownership key returns 403 (the one real read from a principal that is not admitted;
     the QA runner of this fabric shares an admitted role, so it cannot be the negative arm).
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r4_modallow as ma  # noqa: E402

BUCKET = ma.BUCKET
KEY = "advi/49financial/platinum/49financial/ownership_map.json"
SHAPED = ("Action", "NotAction", "Resource", "NotResource")


def _norm_stmt(s):
    o = {}
    for k, v in s.items():
        if k in SHAPED:
            o[k] = sorted(v if isinstance(v, list) else [v])
        elif k == "Principal":
            if isinstance(v, dict):
                o[k] = {pk: sorted(pv if isinstance(pv, list) else [pv]) for pk, pv in v.items()}
            else:
                o[k] = v
        elif k == "Condition":
            o[k] = {op: {ck: sorted(cv if isinstance(cv, list) else [cv]) for ck, cv in body.items()}
                    for op, body in v.items()}
        else:
            o[k] = v
    return o


def _live():
    r = subprocess.run(["aws", "s3api", "get-bucket-policy", "--bucket", BUCKET, "--output", "json"],
                       capture_output=True, text=True, timeout=90)
    if r.returncode:
        return None
    return json.loads(json.loads(r.stdout)["Policy"])["Statement"]


def live(root):
    res = []
    stm = _live()
    with tempfile.TemporaryDirectory() as td:
        head = ma._mirror(os.path.join(td, "head"), root, None)
        pats = (ma._eval(head, "local.fence_patterns") or {}).get("49financial", [])
        arns = (ma._eval(head, "local.fence_exemption_arns") or {}).get(BUCKET, [])
        deny = (ma._eval(head, "local.fence_scoped_statements") or {}).get(BUCKET, [])
        allow = (ma._eval(head, "local.fence_scoped_allow_statements") or {}).get(BUCKET, [])
    rend = [{"Sid": "DenyForeignFirmPrincipals", "Effect": "Deny", "Principal": "*", "Action": "s3:*",
             "Resource": ["arn:aws:s3:::%s" % BUCKET, "arn:aws:s3:::%s/*" % BUCKET],
             "Condition": {"ArnNotLike": {"aws:PrincipalArn": list(pats) + list(arns)}}}]
    rend += deny + allow
    if stm is None or not pats:
        print("  live policy unreadable or fence_patterns empty (patterns=%d)" % len(pats))
        res.append(("L1 the live policy equals the rendered policy", False))
    else:
        a = {s.get("Sid"): json.dumps(_norm_stmt(s), sort_keys=True) for s in stm}
        b = {s.get("Sid"): json.dumps(_norm_stmt(s), sort_keys=True) for s in rend}
        only_live = sorted(set(a) - set(b))
        only_rend = sorted(set(b) - set(a))
        diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        print("  statements live=%d rendered=%d; only live=%s only rendered=%s differing=%s" % (
            len(stm), len(rend), only_live, only_rend, diff))
        res.append(("L1 the live policy equals the rendered policy, statement by statement",
                    not only_live and not only_rend and not diff and len(stm) == len(rend)))

    bad = []
    for s in stm or []:
        if s.get("Effect") != "Allow":
            continue
        acts = s.get("Action", [])
        acts = acts if isinstance(acts, list) else [acts]
        ress = s.get("Resource", [])
        ress = ress if isinstance(ress, list) else [ress]
        p = (s.get("Principal") or {})
        pa = p.get("AWS") if isinstance(p, dict) else p
        pa = pa if isinstance(pa, list) else [pa]
        if any(a in ("s3:*", "*") or a.startswith(("s3:Put", "s3:Delete")) for a in acts):
            bad.append((s.get("Sid"), "write action"))
        if any(r in ("*", "arn:aws:s3:::%s/*" % BUCKET) for r in ress):
            bad.append((s.get("Sid"), "bucket-wide resource"))
        if len(pa) != 1 or pa[0] in ("*", None):
            bad.append((s.get("Sid"), "principal"))
    print("  allow statements=%d; violations=%s" % (sum(1 for s in stm or [] if s.get("Effect") == "Allow"), bad))
    res.append(("L2 no Allow writes, deletes, names a wildcard principal or the whole bucket", stm is not None and not bad))

    url = "https://%s.s3.amazonaws.com/%s" % (BUCKET, KEY)
    code = None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="GET"), timeout=30) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:  # noqa: BLE001
        code = "ERR:%s" % type(e).__name__
    print("  anonymous GET of the ownership key -> %s" % code)
    res.append(("L3 an unsigned GET of the ownership key returns 403", code == 403))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("live",), required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = ma._root(a.root)
    if not shutil.which("terraform"):
        print("ABSENT: terraform is not on PATH")
        print("ROUND 4 ACT 3B LIVE: 0 of 3 arms")
        sys.exit(1)
    try:
        res = live(root)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:200]))
        res = [("the live policy and the render readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 ACT 3B LIVE: %d of 3 arms" % n)
    sys.exit(0 if n == 3 else 1)


if __name__ == "__main__":
    main()
