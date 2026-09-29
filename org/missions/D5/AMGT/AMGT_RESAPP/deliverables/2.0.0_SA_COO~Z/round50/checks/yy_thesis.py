"""AMGT_RESAPP round 50 -- /thesis passes the dossier's served fields (AMGT-yy-2) and the base case names its owner (AMGT-yy-4).

Reads /thesis for four names (AZN_LN, IMB_LN, AMD_US, ADBE_US: CORPUS round 14's p-4 names) either IN PROCESS on this tree's
`scoped_amgt.handler` (--plane local) or from the DEPLOYED function (--plane served), and compares with `read_dossier(key)`:
  --what fields: `dossier_fields.thesis_pillars` carries every dossier pillar (count equal, each with its `terms` when the dossier's
                 does) and `dossier_fields.{management, fund_of_record, last_stated_position}` each carry the dossier's value, or
                 an ABSENT status with the dossier's own absent reason. Prints pillars P of D over the names.
  --what label:  `model.cases.base.label` reads exactly "Opal's historical-multiple reference" wherever the base case is present.
usage: python <this> --plane local|served --what fields|label   (from the repo root)"""
import argparse
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.getcwd())
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
NAMES = ["AZN_LN_Equity", "IMB_LN_Equity", "AMD_US_Equity", "ADBE_US_Equity"]
LABEL = "Opal's historical-multiple reference"
SCALARS = ("management", "fund_of_record", "last_stated_position")


def _pillars(fields):
    """AMENDMENT 1 (row Z-W177-S1): only a LIST is pillars; an absent object {absent, value} counts 0, never len(dict)."""
    value = fields.get("thesis_pillars")
    return value if isinstance(value, list) else []


def thesis(plane, cl, key):
    path = "%s/security/%s/thesis" % (cl.ROUTE_PREFIX, key)
    if plane == "served":
        import boto3
        obj, meta = cl._invoke(boto3.client("lambda", region_name=cl.REGION), path)
        return obj, meta
    from lib.research.api import scoped_amgt as sa
    resp = sa.handler(cl._event(path, None))
    body = resp.get("body")
    return (json.loads(body) if resp.get("statusCode") == 200 and isinstance(body, str) else None), {"status": resp.get("statusCode")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plane", choices=("local", "served"), required=True)
    ap.add_argument("--what", choices=("fields", "label"), required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    from lib.research.corpus import dossier
    bad, served_p, held_p = [], 0, 0
    for key in NAMES:
        obj, meta = thesis(a.plane, cl, key)
        if obj is None:
            bad.append("%s: /thesis read failed %s" % (key, str(meta)[:120]))
            continue
        if a.what == "label":
            base = ((obj.get("model") or {}).get("cases") or {}).get("base")
            if base is not None and base.get("label") != LABEL:
                bad.append("%s: base label %r" % (key, base.get("label")))
            continue
        fields = (dossier.read_dossier(key)["document"].get("fields")) or {}
        got = obj.get("dossier_fields")
        if not isinstance(got, dict):
            bad.append("%s: /thesis carries no dossier_fields" % key)
            held_p += len(_pillars(fields))
            continue
        want_p = _pillars(fields)
        got_p = got.get("thesis_pillars") or []
        if not want_p and isinstance(fields.get("thesis_pillars"), dict):
            # AMENDMENT 1: the dossier's pillars field is itself ABSENT -> served as [] plus thesis_pillars_absent (ruled at the drain)
            absent = got.get("thesis_pillars_absent") or {}
            if got_p or absent.get("status") != "ABSENT" or not absent.get("reason"):
                bad.append("%s: absent pillars field should serve [] + thesis_pillars_absent ABSENT (%r)" % (key, absent))
        held_p += len(want_p)
        served_p += len(got_p)
        if len(got_p) != len(want_p):
            bad.append("%s: pillars %d of %d" % (key, len(got_p), len(want_p)))
        for w, g in zip(want_p, got_p):
            if w.get("terms") and g.get("terms") != w.get("terms"):
                bad.append("%s: pillar terms differ" % key)
                break
        for name in SCALARS:
            w, g = fields.get(name) or {}, got.get(name)
            if not isinstance(g, dict):
                bad.append("%s: %s missing" % (key, name))
            elif w.get("value") is not None and g.get("value") != w.get("value"):
                bad.append("%s: %s value differs" % (key, name))
            elif w.get("value") is None and g.get("status") != "ABSENT":
                bad.append("%s: %s should read ABSENT (%r)" % (key, name, w.get("absent")))
    for b in bad:
        print("  BAD", b)
    if a.what == "fields":
        print("plane %s: pillars %d of %d over %d names" % (a.plane, served_p, held_p, len(NAMES)))
        ok = not bad and held_p > 0 and served_p == held_p
        print("/THESIS PASSES THE DOSSIER'S FIELDS: %s" % ("YES" if ok else "NO"))
    else:
        ok = not bad
        print("THE BASE CASE NAMES ITS OWNER: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
