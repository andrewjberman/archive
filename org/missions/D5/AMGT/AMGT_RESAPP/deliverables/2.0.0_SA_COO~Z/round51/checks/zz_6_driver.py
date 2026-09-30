"""AMGT_RESAPP round 51, AMGT-zz-6 AC1 -- the thesis driver's chart series reaches the chart from SERVED numbers (DSGN FWD-1; CTO
round-50 ruling 5).

Over every identified research-library name, `/thesis` is run IN PROCESS on this tree's `scoped_amgt.handler` (8 threads) and its
`thesis_driver` / `thesis_driver_chart` read. Census printed:
  names I; with a thesis_driver D; chart SERVED C (status SERVED, >= 2 points, every point a number); ABSENT with a reason A
PASS when C >= 1, C + A == D (every driver name is SERVED or ABSENT-with-reason, none silent), and every SERVED chart names its
`source` (model block mnemonic or filing points) -- never a guessed match.
usage: python <this>   (from the repo root)"""
import concurrent.futures as cf
import importlib.util
import json
import os
import sys

sys.path.insert(0, os.getcwd())
CAPTURE_LIB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"


def num(v):
    try:
        float(str(v).replace(",", ""))
        return True
    except (TypeError, ValueError):
        return False


def main():
    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    from lib.research.api import scoped_amgt as sa
    from lib.research.corpus import library
    from lib.research.identity import crosswalk
    pilots = crosswalk.load_pilots()
    keys = []
    for folder in library.list_folders(library.library_root()):
        k = sa.resolve_identity(crosswalk.harvester_key(folder, pilots)[0]).get("security_key")
        if k:
            keys.append(k)

    def one(key):
        resp = sa.handler(cl._event("%s/security/%s/thesis" % (cl.ROUTE_PREFIX, key), None))
        body = json.loads(resp["body"]) if resp.get("statusCode") == 200 and isinstance(resp.get("body"), str) else {}
        return key, body.get("thesis_driver"), body.get("thesis_driver_chart")

    served, absent, silent, drivers, unsourced = [], [], [], 0, []
    with cf.ThreadPoolExecutor(8) as pool:
        for key, drv, chart in pool.map(one, keys):
            if not drv:
                continue
            drivers += 1
            chart = chart or {}
            pts = chart.get("points") or []
            if chart.get("status") == "SERVED" and len(pts) >= 2 and all(num(p.get("value")) for p in pts):
                served.append(key)
                if not chart.get("source"):
                    unsourced.append(key)
            elif chart.get("status") == "ABSENT" and chart.get("reason"):
                absent.append(key)
            else:
                silent.append(key)
    print("names %d; with a thesis_driver %d; chart SERVED %d %s; ABSENT with a reason %d; neither %d %s; SERVED without a source %d" % (
        len(keys), drivers, len(served), served[:5], len(absent), len(silent), silent[:3], len(unsourced)))
    ok = len(served) >= 1 and len(served) + len(absent) == drivers and not unsourced
    print("THE DRIVER CHART IS SERVED FROM SERVED NUMBERS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
