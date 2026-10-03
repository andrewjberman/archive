"""AMGT_RESAPP round 65 -- the served display-name list on the deployed function (the CTO half's post-act read, the L8 artifact).

Prints every served display_name on /lead-panel/rankings/breakout/price and /lead-panel/timeseries/collected/chatter with its
display_name_source, the all-caps count per route (no acronym exception, the Z-S340 census predicate), and where each of the five
declared cut names is served. Writes the list to --out as JSON for the CVO's L9 read.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
ROUTES = ("/lead-panel/rankings/breakout/price", "/lead-panel/timeseries/collected/chatter")
CUT = ("Mitsubishi UFJ Financial Group", "Sumitomo Mitsui Financial Group", "America Movil SAB de CV",
       "Grupo Aeroportuario del Centro Norte SAB de CV", "Universal Music Group NV")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import boto3

    spec = importlib.util.spec_from_file_location("capture_lib", CAPTURE_LIB)
    cl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cl)
    lam = boto3.client("lambda", region_name=cl.REGION)
    out = {}
    for route in ROUTES:
        body, meta = cl._invoke(lam, PREFIX + route)
        rows = (body or {}).get("rows") or []
        names = [{"security_key": r.get("security_key"), "display_name": r.get("display_name"),
                  "display_name_source": r.get("display_name_source")} for r in rows]
        caps = [n["display_name"] for n in names if n["display_name"] and n["display_name"] == n["display_name"].upper()
                and any(ch.isalpha() for ch in n["display_name"])]
        out[route] = {"rows": len(rows), "all_caps_no_exception": caps, "names": names}
        print(f"{route}: rows {len(rows)}; all-caps with no acronym exception {len(caps)}: {caps}")
    for cut in CUT:
        where = [r.rsplit("/", 1)[-1] for r in ROUTES if any(n["display_name"] == cut for n in out[r]["names"])]
        print(f"cut name {cut!r}: served on {where or 'neither route (not in either list today)'}")
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
