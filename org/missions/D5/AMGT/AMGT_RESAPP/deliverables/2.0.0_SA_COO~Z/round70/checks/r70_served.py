"""AMGT_RESAPP round 70 -- the CTO's round-69 analysis @0bdf5b47ae, section 4 items 1-4 (DSGN FWD-4, FWD-7, FWD-8, FWD-5).

  --cell c30|c31|c32|c33 --where local|deployed

Population for c30-c32: every covered name (`covered_universe.covered_security_keys()`, 95 at the cut); denominators print.
c30 (FWD-4, the header's seven figures), /security/<key>/thesis `header_figures` (the SAME set /overlay serves -- measured identical
    on ROG_SW and BA at the cut; /thesis is read because /overlay costs 6-15 s a name): for each of price (PX_LAST), market cap
    (CUR_MKT_CAP), enterprise value (CURR_ENTP_VAL), net debt (NET_DEBT), beta (EQY_BETA), average volume (VOLUME_AVG_30D) and
    short interest (SHORT_INT_RATIO or SI_PERCENT_EQUITY_FLOAT), the header carries an entry with a non-null value, OR an entry for
    that figure with a null value and a non-empty `reason`. C1: 0 names with a figure that is neither served nor reasoned.
c31 (FWD-7, the exec roster), /security/<key>/thesis `management`: SERVED with >= 1 officer and every officer naming a `source`;
    OR not SERVED with a non-empty `chain_tried` list (the F3 legs it tried) and a non-empty `reason`. C1: 0 names failing both.
c32 (FWD-8, peer price currency), /security/<key>/peers `members`: every member carries a non-empty `price_currency`, or a
    non-empty `price_currency_reason`. C1: 0 members failing both; members read printed.
c33 (FWD-5, own-publication origin), /security/<key>/timeline/day/<date> over DAY_PROBES: every article row carries `origin` in
    {"own", "external"}, and no "own" row follows an "external" row. C1: 0 rows without a valid origin; C2: order holds.
Verdict: R70 <CELL> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import importlib.util
import json

ROOT = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
CAPTURE_LIB = ROOT + "/0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
PREFIX = "/api/scoped/amgt"
SEVEN = {
    "price": ("PX_LAST",),
    "market cap": ("CUR_MKT_CAP",),
    "enterprise value": ("CURR_ENTP_VAL",),
    "net debt": ("NET_DEBT",),
    "beta": ("EQY_BETA",),
    "average volume": ("VOLUME_AVG_30D",),
    "short interest": ("SHORT_INT_RATIO", "SI_PERCENT_EQUITY_FLOAT"),
}
DAY_PROBES = (("BA_US_Equity", "2026-09-08"), ("AMD_US_Equity", "2026-09-08"), ("VLO_US_Equity", "2026-09-08"),
              ("NVDA_US_Equity", "2026-10-01"), ("BA_US_Equity", "2026-10-01"))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", choices=("c30", "c31", "c32", "c33"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), required=True)
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    from lib.research.api import scoped_amgt

    if a.where == "deployed":
        import boto3

        cl = _load("capture_lib", CAPTURE_LIB)
        lam = boto3.client("lambda", region_name=cl.REGION)

        def call(path, query=None):
            body, meta = cl._invoke(lam, path, query)
            return (200, body) if body is not None else (meta.get("status"), None)
    else:
        def call(path, query=None):
            r = scoped_amgt.handler({"rawPath": path, "requestContext": {"http": {"method": "GET"}},
                                     "headers": {"x-firm-id": "opal"}, "queryStringParameters": query})
            try:
                return r.get("statusCode"), json.loads(r.get("body") or "null")
            except ValueError:
                return r.get("statusCode"), None

    from lib.research.coverage import covered_universe

    keys = sorted(covered_universe.covered_security_keys())
    non200 = []
    if a.cell == "c30":
        bad = []
        for key in keys:
            st, ov = call(f"{PREFIX}/security/{key}/thesis")
            if st != 200:
                non200.append(f"{key}:{st}")
                continue
            figs = (ov or {}).get("header_figures") or []
            by = {}
            for f in figs:
                by.setdefault(str(f.get("mnemonic")), []).append(f)
            missing = []
            for label, mnems in SEVEN.items():
                entries = [f for m in mnems for f in by.get(m, [])]
                served = any(f.get("value") is not None for f in entries)
                reasoned = any(f.get("value") is None and str(f.get("reason") or "").strip() for f in entries)
                if not (served or reasoned):
                    missing.append(label)
            if missing:
                bad.append(f"{key}:{'/'.join(missing)}")
        print(f"   population: names {len(keys)} non-200 {len(non200)} e.g. {non200[:3]}")
        clause("C1 every header serves each of the seven figures or a reason per missing one", keys and not bad and not non200,
               f"names failing {len(bad)} e.g. {bad[:5]}")
    elif a.cell == "c31":
        bad, served = [], 0
        for key in keys:
            st, th = call(f"{PREFIX}/security/{key}/thesis")
            if st != 200:
                non200.append(f"{key}:{st}")
                continue
            mg = (th or {}).get("management") or {}
            offs = mg.get("officers") or []
            if mg.get("management_status") == "SERVED" and offs and all(str(o.get("source") or "").strip() for o in offs):
                served += 1
                continue
            if mg.get("management_status") != "SERVED" and (mg.get("chain_tried") or []) and str(mg.get("reason") or "").strip():
                continue
            bad.append(f"{key}:{mg.get('management_status')}/{mg.get('absent_because')}")
        print(f"   population: names {len(keys)} served {served} non-200 {len(non200)} e.g. {non200[:3]}")
        clause("C1 every name serves sourced officers, or the chain it tried with a reason", keys and not bad and not non200,
               f"names failing {len(bad)} e.g. {bad[:5]}")
    elif a.cell == "c32":
        bad, members = [], 0
        for key in keys:
            st, pr = call(f"{PREFIX}/security/{key}/peers")
            if st != 200:
                non200.append(f"{key}:{st}")
                continue
            for m in (pr or {}).get("members") or []:
                members += 1
                if not (str(m.get("price_currency") or "").strip() or str(m.get("price_currency_reason") or "").strip()):
                    bad.append(f"{key}/{m.get('security_key') or m.get('ticker')}")
        print(f"   population: names {len(keys)} members {members} non-200 {len(non200)} e.g. {non200[:3]}")
        clause("C1 every peer member serves its price currency or a reason", keys and members and not bad and not non200,
               f"members failing {len(bad)} e.g. {bad[:5]}")
    elif a.cell == "c33":
        rows, bad_origin, bad_order = 0, [], []
        for key, day in DAY_PROBES:
            st, b = call(f"{PREFIX}/security/{key}/timeline/day/{day}")
            if st != 200:
                non200.append(f"{key}/{day}:{st}")
                continue
            seen_external = False
            for art in (b or {}).get("articles") or []:
                rows += 1
                o = art.get("origin")
                if o not in ("own", "external"):
                    bad_origin.append(f"{key}/{day}:{art.get('publisher')}={o}")
                    continue
                if o == "external":
                    seen_external = True
                elif seen_external:
                    bad_order.append(f"{key}/{day}:{art.get('publisher')}")
        print(f"   population: probes {len(DAY_PROBES)} rows {rows} non-200 {len(non200)} e.g. {non200[:3]}")
        clause("C1 every day-route row serves origin in {own, external}", rows and not bad_origin and not non200,
               f"rows failing {len(bad_origin)} e.g. {bad_origin[:4]}")
        clause("C2 no own-publication row follows an external row", rows and not bad_order, f"rows out of order {len(bad_order)}")

    verdict = "YES" if ok and all(ok) else "NO"
    print(f"R70 {a.cell.upper()} SERVED: {verdict}")
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    raise SystemExit(main())
