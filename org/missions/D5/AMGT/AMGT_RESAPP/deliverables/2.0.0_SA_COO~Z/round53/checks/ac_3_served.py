"""AMGT_RESAPP round 53, AMGT-ac-3 -- the slash-key window's served outcomes, read from the DEPLOYED `opal-amgt-scoped-api` (read-only).
  --what code:   CodeSha256 differs from the base the halves sign (`nKWCfQRQ3/lL6cJxgYG3dZr0tcVdOBheeMMNaoWQE+w=`, ab-6) and Successful.
  --what codes:  /timeline for AMZN_US_Equity: every series entry carries the key `publishers_found_codes` (HVST q-5, 91b74a9047).
  --what save --dir D / --what bpng --dir D:  for BP/_LN_Equity and NG/_LN_Equity (addressed as the page does, the slash URL-quoted),
                 the overlay / peers / thesis bodies. `save` writes their canonical sha256 to D/bpng.json (the executor, BEFORE the act);
                 `bpng` re-reads them and PASSES when every body is byte-equal to the saved one (they must read the same data at the
                 encoded keys after the act as at the raw keys before it).
                 AMENDMENT 2 (row Z-S318): the body reports its own read path inside the `*_read` provenance subtrees (posture_read,
                 peer_read, scores_read, management_read), and the act moves that path BY DESIGN. `bpng` therefore rewrites the
                 encoded name back to the raw one INSIDE `*_read` subtrees ONLY, and every other byte must still equal the pre-act
                 capture (dossier citations stored encoded before the act are NOT rewritten). It prints the count of rewritten strings:
                 0 would mean the path never moved.
usage: python <this> --what code|codes|save|bpng [--dir D]   (from the repo root)"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import urllib.parse

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PRIOR = "nKWCfQRQ3/lL6cJxgYG3dZr0tcVdOBheeMMNaoWQE+w="
NAMES = ("BP/_LN_Equity", "NG/_LN_Equity")
ROUTES = ("overlay", "peers", "thesis")
VOLATILE = ("generated_at", "read_at", "served_at", "request_id")
ENCODED = {"BP-SLASH-_LN_Equity": "BP/_LN_Equity", "NG-SLASH-_LN_Equity": "NG/_LN_Equity"}


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def read_path_raw(o, in_read=False, n=None):
    """AMENDMENT 2: the encoded name back to raw inside `*_read` subtrees only; n[0] counts the rewrites."""
    if isinstance(o, dict):
        return {k: read_path_raw(v, in_read or k.endswith("_read"), n) for k, v in o.items()}
    if isinstance(o, list):
        return [read_path_raw(v, in_read, n) for v in o]
    if in_read and isinstance(o, str) and any(e in o for e in ENCODED):
        n[0] += 1
        for e, r in ENCODED.items():
            o = o.replace(e, r)
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("code", "codes", "save", "bpng"), required=True)
    ap.add_argument("--dir", default="")
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    lam = boto3.client("lambda", region_name=cl.REGION)
    if a.what == "code":
        c = lam.get_function_configuration(FunctionName=cl.FUNCTION)
        print("deployed CodeSha256 %s LastModified %s (base %s)" % (c["CodeSha256"], c["LastModified"], PRIOR))
        ok = c["CodeSha256"] != PRIOR and c.get("LastUpdateStatus") == "Successful"
        label = "THE ONE BUILD LANDED"
    elif a.what == "codes":
        obj, _m = cl._invoke(lam, "%s/security/AMZN_US_Equity/timeline" % cl.ROUTE_PREFIX)
        ser = (obj or {}).get("series") or []
        carrying = sum(1 for e in ser if isinstance(e, dict) and "publishers_found_codes" in e)
        print("AMZN /timeline series %d; entries carrying publishers_found_codes %d" % (len(ser), carrying))
        ok = bool(ser) and carrying == len(ser)
        label = "/TIMELINE SERVES PUBLISHERS_FOUND_CODES"
    else:
        sums, rewrites = {}, [0]
        for n in NAMES:
            for r in ROUTES:
                obj, meta = cl._invoke(lam, "%s/security/%s/%s" % (cl.ROUTE_PREFIX, urllib.parse.quote(n, safe=""), r))
                body = strip(obj) if a.what == "save" else read_path_raw(strip(obj), n=rewrites)
                sums["%s %s" % (n, r)] = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() if obj else None
        path = os.path.join(a.dir, "bpng.json")
        if a.what == "save":
            os.makedirs(a.dir, exist_ok=True)
            json.dump(sums, open(path, "w", encoding="utf-8"), indent=1)
            print("saved %d body hashes to %s (%d empty)" % (len(sums), path, sum(1 for v in sums.values() if not v)))
            ok = all(sums.values())
            label = "BP AND NG PRE-ACT BODIES SAVED"
        else:
            try:
                before = json.load(open(path, encoding="utf-8"))
            except FileNotFoundError:
                print("no pre-act capture at %s" % path)
                before = {}
            moved = [k for k in sums if not before or before.get(k) != sums[k] or not sums[k]]
            print("read-path strings rewritten encoded->raw inside *_read subtrees: %d" % rewrites[0])
            print("bodies %d; moved or empty vs the pre-act capture: %d %s" % (len(sums), len(moved), moved[:6]))
            ok = bool(before) and not moved
            label = "BP AND NG READ THE SAME DATA AT THE ENCODED KEYS"
    print("%s: %s" % (label, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
