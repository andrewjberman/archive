"""AMGT_RESAPP round 52, AMGT-ab-2 / ab-6 -- /thesis's `dossier_fields` block is served for EVERY name, and carries `pack_shape`
(CTO round-51 analysis item 2; AMGT_CORPUS round-20 rulings 2-3, row Z-W2-S15).
Through the ROUTE (`scoped_amgt.handler` in process for --plane local, the DEPLOYED function for --plane served; never a component
called with a handed input -- CTO round-51 ruling 5), GET /security/<key>/thesis and read `dossier_fields`:
  --what absent: 6501_JP_Equity (no research_dossier object at all) serves the block with `thesis_pillars: []`,
      `thesis_pillars_absent`, and each of management / fund_of_record / last_stated_position / pack_shape as
      {status: ABSENT, value: null, reason: <non-empty>} -- never a bare {status: READ_FAILED}.
  --what shape: AZN_LN_Equity and ADBE_US_Equity serve `pack_shape` {status: SERVED, value: 'pdf', basis: [..]} and AMD_US_Equity
      serves `pack_shape` {status: ABSENT, value: null, reason: <the dossier's absent text>} (the dossier /5 objects, measured at
      the cut: AZN pdf, ADBE pdf, AMD absent).
usage: python <this> --plane local|served --what absent|shape   (from the repo root)"""
import argparse
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.getcwd())
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
SCALARS = ("management", "fund_of_record", "last_stated_position", "pack_shape")
SHAPE = {"AZN_LN_Equity": "pdf", "ADBE_US_Equity": "pdf", "AMD_US_Equity": None}


def thesis(plane, cl, key):
    path = "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, key)
    if plane == "served":
        import boto3
        obj, _meta = cl._invoke(boto3.client("lambda", region_name=cl.REGION), path)
        return obj
    from lib.research.api import scoped_amgt as sa
    resp = sa.handler(cl._event(path, None))
    body = resp.get("body")
    return json.loads(body) if resp.get("statusCode") == 200 and isinstance(body, str) else None


def absent_ok(f):
    return isinstance(f, dict) and f.get("status") == "ABSENT" and f.get("value") is None and bool(f.get("reason"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plane", choices=("local", "served"), required=True)
    ap.add_argument("--what", choices=("absent", "shape"), required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    bad = []
    if a.what == "absent":
        df = (thesis(a.plane, cl, "6501_JP_Equity") or {}).get("dossier_fields")
        print("6501_JP_Equity dossier_fields: %s" % json.dumps(df)[:400])
        if not isinstance(df, dict) or df.get("status") == "READ_FAILED":
            bad.append("no per-field block (%s)" % (df or {}).get("status"))
        else:
            if df.get("thesis_pillars") != [] or not absent_ok(dict((df.get("thesis_pillars_absent") or {}), value=None)):
                bad.append("thesis_pillars / thesis_pillars_absent")
            bad += ["%s not ABSENT-with-reason" % n for n in SCALARS if not absent_ok(df.get(n))]
        label = "A NAME WITH NO DOSSIER SERVES EVERY FIELD ABSENT WITH ITS REASON"
    else:
        for key, want in SHAPE.items():
            ps = ((thesis(a.plane, cl, key) or {}).get("dossier_fields") or {}).get("pack_shape")
            print("%s pack_shape: %s" % (key, json.dumps(ps)[:200]))
            if want is None:
                ok = absent_ok(ps)
            else:
                ok = isinstance(ps, dict) and ps.get("status") == "SERVED" and ps.get("value") == want and bool(ps.get("basis"))
            if not ok:
                bad.append("%s pack_shape (want %s)" % (key, want or "ABSENT"))
        label = "PACK_SHAPE PASSES THROUGH FROM THE DOSSIER"
    for b in bad:
        print("  BAD", b)
    print("plane %s: %s: %s" % (a.plane, label, "YES" if not bad else "NO"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
