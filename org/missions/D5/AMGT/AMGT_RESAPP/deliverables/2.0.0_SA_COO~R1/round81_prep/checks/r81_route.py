"""AMGT_RESAPP round 81 (DRAFT, prepared ahead of the round-80 analysis) -- the security route resolves a typed name or ticker.

  python r81_route.py --crit AC1 [--where local|deployed]
  python r81_route.py --crit AC2                      # local only: the bound

Source of the ask: 1.0.0_SA_CTO~DELL1 msg 1619, DSGN_AMGTV1 ledger/CTO_RULING_ROUND57_R1A_R6_20261009.md R1(a): "the RESAPP security
route accepts a typed name or ticker and resolves it server-side, or returns a not-found."

AC1 (build):
  C1 /security/AMD/thesis (a typed ticker root) answers 200 and serves AMD_US_Equity's body;
  C2 /security/Advanced Micro Devices/thesis (a typed company name) answers 200 and serves AMD_US_Equity's body;
  C3 /security/zzqx/thesis answers 404 with a plain sentence naming what was typed;
  C4 /security/Micro/thesis (three companies match) answers 404 and its sentence says more than one company matches.
  "Serves the body" = equal to /security/AMD_US_Equity/thesis once every `identity.requested` (the echoed typed text) and
  `identity.identity_basis` are set aside -- the only fields a typed form may change.
AC2 (bound): for keys that resolve TODAY (AMD_US_Equity, BA_US_Equity, ABNB_US_Equity, the Bloomberg form "AMD US"), the LOCAL
  tree's /thesis body hashes (canonical JSON, sorted keys) equal to the DEPLOYED function's body for the same key, read in the same
  run. 10-K and uncovered names only: the round-80 merge of dd-1 moves a 20-F name's passage_coverage on the tree before any
  redeploy. A stored baseline is NOT used: the live store moves between runs (measured at the cut: AMD's hash changed in minutes).
Verdict: R81 ROUTE ACn SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from urllib.parse import quote

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
CANON = "AMD_US_Equity"
BOUND_KEYS = ("AMD_US_Equity", "BA_US_Equity", "ABNB_US_Equity", "AMD US")


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _getter(where):
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        root = _root()
        if root not in sys.path:
            sys.path.insert(0, root)
        from lib.research.api import scoped_amgt

        def raw(event):
            return scoped_amgt.handler(event)

    def get(text):
        event = {"rawPath": "%s/security/%s/thesis" % (PREFIX, quote(text, safe="")),
                 "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
                 "queryStringParameters": None}
        try:
            r = raw(event)
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except Exception as err:  # noqa: BLE001 -- a failed read is a FAIL line, never a crash
            return "%s: %s" % (type(err).__name__, str(err)[:100]), {}
    return get


def _strip(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "identity" and isinstance(v, dict):
                v = {ik: iv for ik, iv in v.items() if ik not in ("requested", "identity_basis")}
            out[k] = _strip(v)
        return out
    if isinstance(node, list):
        return [_strip(v) for v in node]
    return node


def _hash(body):
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def ac1(where):
    get = _getter(where)
    code0, canon = get(CANON)
    want = _hash(_strip(canon))
    print("   canonical %s: %s, %d keys" % (CANON, code0, len(canon)))
    r = []
    for cid, text in (("C1", "AMD"), ("C2", "Advanced Micro Devices")):
        code, body = get(text)
        same = code == 200 and _hash(_strip(body)) == want
        r.append(say(code0 == 200 and same, "%s %r answers %s and serves %s's body" % (cid, text, code, CANON)))
    code, body = get("zzqx")
    reason = str(body.get("reason") or body.get("message") or "")
    r.append(say(code == 404 and "zzqx" in reason, "C3 'zzqx' answers %s with a plain sentence: %r" % (code, reason[:120])))
    code, body = get("Micro")
    reason = str(body.get("reason") or body.get("message") or "")
    several = any(w in reason.lower() for w in ("companies match", "more than one", "several"))
    r.append(say(code == 404 and several, "C4 'Micro' (three matches) answers %s and says more than one matches: %r"
                 % (code, reason[:120])))
    return all(r)


def ac2():
    local, deployed = _getter("local"), _getter("deployed")
    r = []
    for key in BOUND_KEYS:
        lc, lb = local(key)
        dc, db = deployed(key)
        lh, dh = _hash(lb), _hash(db)
        r.append(say(lc == dc == 200 and lh == dh, "B1 %r /thesis: local %s %s, deployed %s %s" % (key, lc, lh[:12], dc, dh[:12])))
    return all(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"))
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    if not a.crit:
        ap.error("--crit is required")
    ok = ac1(a.where) if a.crit == "AC1" else ac2()
    print("R81 ROUTE %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
