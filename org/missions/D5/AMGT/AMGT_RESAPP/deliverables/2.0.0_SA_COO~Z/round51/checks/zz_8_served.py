"""AMGT_RESAPP round 51, AMGT-zz-8 -- the ONE build's served outcomes, read from the DEPLOYED `opal-amgt-scoped-api` (read-only invokes).
  --what code:  CodeSha256 differs from the base the halves sign (`pVa+sgzj8XNZ9uvJqCOwRNCJn0IZhUklnWZh6JbO7B0=`, yy-5's act) and
                LastUpdateStatus Successful.
  --what rows:  over the four lead-panel axes, every row carries `name_source` when named and `places_moved` (int, or null with
                `places_moved_reason`); named rows exceed 16 (the cut's count) and at least one places_moved is an int.
  --what chart: ASML_NA_Equity's /thesis `thesis_driver_chart` is SERVED from source 'filing' with >= 2 numeric points.
(The six UNRESOLVED-unit names are graded by the served sweep, zz-8's AC2 invocation.)
usage: python <this> --what code|rows|chart   (from the repo root)"""
import argparse
import importlib.util
import sys

import boto3

CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PRIOR = "pVa+sgzj8XNZ9uvJqCOwRNCJn0IZhUklnWZh6JbO7B0="
AXES = [("trending", "chatter"), ("trending", "price"), ("breakout", "chatter"), ("breakout", "price")]


def num(v):
    try:
        float(str(v).replace(",", ""))
        return True
    except (TypeError, ValueError):
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("code", "rows", "chart"), required=True)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    client = boto3.client("lambda", region_name=cl.REGION)
    conf = client.get_function_configuration(FunctionName=cl.FUNCTION)
    print("deployed CodeSha256 %s LastUpdateStatus %s (base %s)" % (conf["CodeSha256"], conf.get("LastUpdateStatus"), PRIOR))
    if a.what == "code":
        ok = conf["CodeSha256"] != PRIOR and conf.get("LastUpdateStatus") == "Successful"
        label = "THE ONE BUILD LANDED"
    elif a.what == "rows":
        rows, bad = [], []
        for mv, sj in AXES:
            obj, meta = cl._invoke(client, "%s/lead-panel/rankings/%s/%s" % (cl.ROUTE_PREFIX, mv, sj))
            rows.extend((obj or {}).get("rows") or [])
        named = [r for r in rows if r.get("name")]
        ints = sum(1 for r in rows if isinstance(r.get("places_moved"), int))
        for r in rows:
            if r.get("name") and not r.get("name_source"):
                bad.append("%s named without name_source" % r.get("ticker"))
            if "places_moved" not in r or (r["places_moved"] is None and not r.get("places_moved_reason")):
                bad.append("%s places_moved missing or null without a reason" % r.get("ticker"))
        for b in bad[:5]:
            print("  BAD", b)
        print("served rows %d; named %d (cut: 16); places_moved int %d" % (len(rows), len(named), ints))
        ok = rows and not bad and len(named) > 16 and ints > 0
        label = "THE SERVED LEAD-LIST ROWS CARRY NAMES AND PLACES MOVED"
    else:
        obj, meta = cl._invoke(client, "%s/security/ASML_NA_Equity/thesis" % cl.ROUTE_PREFIX)
        ch = (obj or {}).get("thesis_driver_chart") or {}
        pts = ch.get("points") or []
        print("ASML chart %s source %r points %d" % (ch.get("status"), ch.get("source"), len(pts)))
        ok = ch.get("status") == "SERVED" and ch.get("source") == "filing" and len(pts) >= 2 and all(num(p.get("value")) for p in pts)
        label = "THE SERVED DRIVER CHART READS THE FILING'S VERIFIED POINTS"
    print("%s: %s" % (label, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
