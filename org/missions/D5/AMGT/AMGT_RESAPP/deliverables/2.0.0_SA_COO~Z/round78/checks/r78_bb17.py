"""AMGT_RESAPP round 78 -- AMGT-bb-17, the adapter cell: every hookup of the round, read through the handler.

  python r78_bb17.py --crit AC1 --where local|deployed
  python r78_bb17.py --crit AC2 --where local

AC1 (build) the six hookups are served. `--where local` runs the handler in-process on the tree; `--where deployed` invokes
the function (GET-shaped direct invokes), and is the line the redeploy's list carries.
  H1 coverage marker (bb-10): /overlay carries `research_coverage`; a covered name reads status covered, a pool name
     outside coverage reads outside_coverage with one plain sentence;
  H2 country (bb-9): the country header figure reads in plain case with the stored text beside it;
  H3 one statement of inputs (bb-2): /thesis carries `input_provenance` with exactly one filings row, placed before the pack row;
  H4 officer rank (bb-3): on every sampled roster that holds a chief-executive title, that row is first;
  H5 source names (bb-11): every entry of the overlay's `provenance` carries a `source_name` key;
  H6 peer price listing (bb-8): no sampled peer row is served a currency from a United States record behind a foreign price.
AC2 (bound) the round-77 served shape still holds on the tree: r77_served_shape.py --where local reads YES.
Verdict: R78 BB17 <crit> SERVED: YES|NO (exit 0|1). Read-only.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
COVERED = "AMD_US_Equity"
OUTSIDE = "MSFT_US_Equity"
ROSTER_SAMPLE = ("BA_US_Equity", "HD_US_Equity", "BABA_US_Equity", "1299_HK_Equity", "8306_JP_Equity", "AMD_US_Equity")
PEER_SAMPLE = ("2317_TT_Equity", "AMD_US_Equity", "BA_US_Equity", "ASML_NA_Equity", "PBR_US_Equity")
CHIEF = re.compile(r"chief executive|\bCEO\b", re.I)


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _reader(where):
    if where == "deployed":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")

        def raw(event):
            return json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    else:
        from lib.research.api import scoped_amgt

        def raw(event):
            return scoped_amgt.handler(event)

    def body(path):
        event = {"rawPath": PREFIX + path, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
                 "queryStringParameters": None}
        r = raw(event)
        try:
            return r.get("statusCode"), json.loads(r.get("body") or "{}")
        except (ValueError, TypeError):
            return r.get("statusCode"), {}

    return body


def _peer_rows(node, out):
    if isinstance(node, dict):
        if "ticker" in node and isinstance(node.get("identity"), dict):
            out.append(node)
        for value in node.values():
            _peer_rows(value, out)
    elif isinstance(node, list):
        for value in node:
            _peer_rows(value, out)


def ac1(where):
    body = _reader(where)
    results = []

    def clause(name, cond, detail=""):
        results.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    _, ov_in = body("/security/%s/overlay" % COVERED)
    _, ov_out = body("/security/%s/overlay" % OUTSIDE)
    m_in, m_out = ov_in.get("research_coverage") or {}, ov_out.get("research_coverage") or {}
    clause("H1 a covered name reads covered and a pool name outside coverage says so once",
           m_in.get("status") == "covered" and m_out.get("status") == "outside_coverage" and bool(m_out.get("sentence")),
           "%s: %r; %s: %r" % (COVERED, m_in.get("status"), OUTSIDE, m_out.get("status")))

    _, ov_ba = body("/security/BA_US_Equity/overlay")
    country = [h for h in ov_ba.get("header_figures") or [] if h.get("mnemonic") == "COUNTRY_FULL_NAME"]
    c = country[0] if country else {}
    clause("H2 the country reads in plain case with the stored text beside it",
           c.get("value") == "United States" and c.get("value_as_stored") == "UNITED STATES",
           "value %r stored %r" % (c.get("value"), c.get("value_as_stored")))

    _, th_ba = body("/security/BA_US_Equity/thesis")
    rows = th_ba.get("input_provenance") or []
    names = [r.get("input") for r in rows if isinstance(r, dict)]
    filings = [i for i, n in enumerate(names) if n == "filings"]
    placed = len(filings) == 1 and ("pack" not in names or filings[0] == names.index("pack") - 1)
    clause("H3 the thesis carries one statement of inputs with one filings row before the pack row", placed, "rows %s" % names)

    checked, first = 0, 0
    for key in ROSTER_SAMPLE:
        _, th = (key, th_ba) if key == "BA_US_Equity" else body("/security/%s/thesis" % key)
        officers = ((th.get("management") or {}).get("officers")) or []
        roles = [str(o.get("role") or "") for o in officers]
        if any(CHIEF.search(r) for r in roles):
            checked += 1
            first += 1 if CHIEF.search(roles[0]) else 0
    clause("H4 a chief-executive row leads every sampled roster that holds one", checked >= 3 and first == checked,
           "%d of %d rosters with such a row" % (first, checked))

    prov = ov_ba.get("provenance")
    # AMENDMENT 1 (issuer, row Z-W302-S1): the overlay's provenance is {"inputs": [entry, ...]}; the first cut of this
    # clause took the dict's values as the entries and so read 0 of 0. The entries are read from every list it holds.
    entries = []
    for part in (prov if isinstance(prov, list) else list(prov.values()) if isinstance(prov, dict) else []):
        entries.extend(part if isinstance(part, list) else [part])
    entries = [e for e in entries if isinstance(e, dict) and "source" in e]
    clause("H5 every provenance entry carries a plain source name key", bool(entries) and all("source_name" in e for e in entries),
           "%d of %d" % (sum(1 for e in entries if "source_name" in e), len(entries)))

    wrong, seen = [], 0
    for key in PEER_SAMPLE:
        _, ov = body("/security/%s/overlay" % key)
        peer_rows = []
        _peer_rows(ov.get("peers"), peer_rows)
        for row in peer_rows:
            rk = (row.get("identity") or {}).get("security_key") or ""
            ticker = str(row.get("ticker") or "")
            if row.get("price_currency") and rk.endswith("_US_Equity") and ticker != rk.split("_")[0] \
                    and row.get("country") not in (None, "United States"):
                wrong.append((key, ticker, rk, row.get("price_currency")))
            seen += 1
    clause("H6 no sampled peer row is served a United States record's currency behind a foreign price",
           seen > 0 and not wrong, "rows read %d, wrong %d %s" % (seen, len(wrong), wrong[:3]))

    ok = all(results)
    print("R78 BB17 AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac2():
    root = _root()
    check = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round77/checks/r77_served_shape.py"
    p = subprocess.run([sys.executable, check, "--where", "local"], cwd=root, capture_output=True, text=True,
                       env=dict(__import__("os").environ, PYTHONPATH=root))
    last = [ln for ln in p.stdout.splitlines() if ln.strip()][-1:] or [""]
    ok = p.returncode == 0
    print("%s B1 the round-77 served shape still reads YES on the tree rc=%d %s" % ("PASS" if ok else "FAIL", p.returncode, last[0][:120]))
    print("R78 BB17 AC2 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    a = ap.parse_args()
    sys.path.insert(0, _root())
    return ac1(a.where) if a.crit == "AC1" else ac2()


if __name__ == "__main__":
    sys.exit(main())
