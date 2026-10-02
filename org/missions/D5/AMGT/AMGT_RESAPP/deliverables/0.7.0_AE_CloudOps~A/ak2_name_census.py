"""AMGT-ak-2 -- the PER-KEY name census of the DEPLOYED function, on the grade's own plane.

The round-61 check (b1_names.py) records only CodeSha256/LastModified as its `pre`, and its
C1/C3 clauses grade the POST state alone. The CTO half's condition 2 asks for the previously
unnamed keys' `display_name` and `name_source` printed BESIDE their pre-act values, and the
issuer's GO says it grades the 24 keys and RMS itself. Neither is possible from the sha-only
pre file, and the pre-act labels stop existing the moment the apply lands -- so this captures
them first, through the same capture_lib._invoke the criterion uses.

It is READ-ONLY: three GETs per run, no write to any store.

  --out <json>   write the census
  --label pre|post

Beside the capture it re-derives the base population figures the issuer's adversary run
declared (24 of 94 unnamed on each price ranking, 25 of 95 chatter rows by ticker). A
disagreement at --label pre is a finding BEFORE the build, not after.
"""
from __future__ import annotations

import argparse
import importlib.util
import json

import boto3

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
BUBBLES = ("BABA_US_Equity", "COST_US_Equity", "KPN_NA_Equity", "NOVN_SW_Equity")
CONTROL = "RMS_FP_Equity"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _root(ticker):
    return str(ticker or "").strip().split(" ")[0].upper()


def _unnamed(rows):
    """A row is UNNAMED-OR-TICKER-LABELLED exactly as C1 judges it."""
    out = []
    for r in rows:
        key = r.get("security_key")
        name = r.get("name")
        if not name:
            out.append((key, None, "absent"))
        elif str(name).strip().upper() == _root(r.get("ticker")):
            out.append((key, name, "ticker-as-name"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", choices=("pre", "post"), required=True)
    a = ap.parse_args()

    cl = _load("capture_lib", CAPTURE_LIB)
    lam = boto3.client("lambda", region_name=cl.REGION)
    cfg = boto3.client("lambda", region_name=cl.REGION).get_function_configuration(FunctionName=cl.FUNCTION)

    def call(path):
        body, meta = cl._invoke(lam, path)
        return (200, body) if body is not None else (meta.get("status"), None)

    snap = {
        "label": a.label,
        "CodeSha256": cfg["CodeSha256"],
        "LastModified": cfg["LastModified"],
        "rankings": {},
        "chatter": {},
        "overlay": {},
    }

    for kind in ("trending/price", "breakout/price"):
        st, body = call(PREFIX + "/lead-panel/rankings/" + kind)
        rows = (body or {}).get("rows") or []
        snap["rankings"][kind] = {
            "status": st,
            "denominator": len(rows),
            "rows": {r.get("security_key"): {"name": r.get("name"),
                                             "display_name": r.get("display_name"),
                                             "name_source": r.get("name_source"),
                                             "ticker": r.get("ticker")} for r in rows},
            "unnamed": [[k, n, why] for k, n, why in _unnamed(rows)],
        }
        u = snap["rankings"][kind]["unnamed"]
        print("%-16s status %s rows %d UNNAMED-OR-TICKER %d" % (kind, st, len(rows), len(u)))

    st, body = call(PREFIX + "/lead-panel/timeseries/collected/chatter")
    crows = (body or {}).get("rows") or []
    tick = [(r.get("security_key"), r.get("display_name")) for r in crows if r.get("name_source") == "ticker"]
    snap["chatter"] = {
        "status": st,
        "denominator": len(crows),
        "rows": {r.get("security_key"): {"display_name": r.get("display_name"),
                                         "name_source": r.get("name_source")} for r in crows},
        "ticker_named": [list(t) for t in tick],
        "bubbles": {k: [(next((r for r in crows if r.get("security_key") == k), {}) or {}).get("display_name"),
                        (next((r for r in crows if r.get("security_key") == k), {}) or {}).get("name_source")]
                    for k in BUBBLES},
    }
    print("chatter          status %s rows %d TICKER-NAMED %d" % (st, len(crows), len(tick)))

    st, ov = call(PREFIX + "/security/" + CONTROL + "/overlay")
    tr = snap["rankings"]["trending/price"]["rows"].get(CONTROL) or {}
    snap["overlay"][CONTROL] = {"status": st,
                                "overlay_display_name": (ov or {}).get("display_name"),
                                "row_display_name": tr.get("display_name"),
                                "row_name": tr.get("name"),
                                "row_name_source": tr.get("name_source")}
    print("overlay %-14s status %s overlay=%r row=%r name_source=%r"
          % (CONTROL, st, (ov or {}).get("display_name"), tr.get("display_name"), tr.get("name_source")))

    json.dump(snap, open(a.out, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("CENSUS %s written: %s" % (a.label, a.out))

    # The issuer's declared base figures, re-derived rather than trusted.
    if a.label == "pre":
        exp = {"trending/price": (24, 94), "breakout/price": (24, 94)}
        for kind, (eu, ed) in exp.items():
            got_u = len(snap["rankings"][kind]["unnamed"])
            got_d = snap["rankings"][kind]["denominator"]
            mark = "AGREES" if (got_u, got_d) == (eu, ed) else "DISAGREES -- STOP AND SURFACE"
            print("BASE CHECK %-16s declared %d of %d, measured %d of %d -- %s"
                  % (kind, eu, ed, got_u, got_d, mark))
        got_u, got_d = len(snap["chatter"]["ticker_named"]), snap["chatter"]["denominator"]
        mark = "AGREES" if (got_u, got_d) == (25, 95) else "DISAGREES -- STOP AND SURFACE"
        print("BASE CHECK chatter          declared 25 of 95, measured %d of %d -- %s" % (got_u, got_d, mark))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
