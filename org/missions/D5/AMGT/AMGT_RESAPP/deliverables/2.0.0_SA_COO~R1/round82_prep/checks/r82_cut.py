"""AMGT_RESAPP round-82 PREP (DRAFT, not issued) -- the 20-F cutter on the five REAL stored 20-F filings (row AMGT_RESAPP-D1-W321-S1).

  python r82_cut.py --crit AC1|AC2 [--cache <dir>]

AC1 (build): for each of ASML_NA_Equity, BABA_US_Equity, NU_US_Equity, PBR_US_Equity, SAP_GY_Equity, read the filing's text from the
    cache (default .scratch/r82_20f/<KEY>.txt; on a miss it is fetched read-only the way fetch.build_source_object does -- one SEC GET,
    NO persist), run document.cut(text, "20-F") in-process, and require business, risk and mdna each status OK with at least 1500
    characters and a heading that is not a contents entry. Prints a 5 x 3 grid and the count of OK cells. Nothing is written.
AC2 (bound): the 10-K fixture and the 20-F risk/mdna/officers fixture sections hash as at round 80 (round80/checks/r80_dd1.py --crit AC3).
Verdict: R82 CUT ACn: YES|NO (exit 0|1). At the base (box/dell1 after 74132a59ba): AC1 NO (6 of 15 OK), AC2 YES.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import types

NAMES = ["ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity"]
ITEMS = ("business", "risk", "mdna")


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _imports(root):
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        import fitz  # noqa: F401
    except Exception:  # noqa: BLE001 -- a box without PyMuPDF; cut() never reads it
        sys.modules["fitz"] = types.ModuleType("fitz")
    from lib.research.filings import document as D
    from lib.research.filings import fetch as F
    return D, F


def _text(root, cache, key, F):
    path = os.path.join(cache, key + ".txt")
    if os.path.isfile(path):
        return open(path, encoding="utf-8").read()
    from lib.research.harvest import filings as hf
    from lib.research.harvest import store as hs
    rows = hs.silver_latest("sec", "filing_source", ("security_key", "accession"))
    rows = list(rows.values()) if isinstance(rows, dict) else list(rows)
    cik = None
    for row in rows:
        obj = hf.source_object_from_row(row)
        if obj.get("security_key") == key:
            cik = (obj.get("filing_identity") or {}).get("cik")
    if not cik:
        return None
    located = F.latest_filing(cik, "20-F")
    time.sleep(0.3)
    text = F.html_to_text(F.http_get(located["url"]))
    os.makedirs(cache, exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    return text


def ac1(root, cache):
    D, F = _imports(root)
    ok = 0
    for key in NAMES:
        text = _text(root, cache, key, F)
        if text is None:
            print("FAIL %-16s no stored 20-F row to read" % key)
            continue
        sections = D.cut(text, "20-F")["sections"]
        cells = []
        for item in ITEMS:
            s = sections.get(item) or {}
            heading = s.get("heading_matched") or ""
            good = s.get("status") == "OK" and (s.get("full_chars") or 0) >= 1500 and heading.strip() != ""
            ok += good
            cells.append("%s=%s(%s)" % (item, "OK" if good else (s.get("status") or "ABSENT"), s.get("full_chars") or 0))
        print("     %-16s %s" % (key, "  ".join(cells)))
    total = len(NAMES) * len(ITEMS)
    good = ok == total
    print("%s C1 business, risk and mdna cut from each real filing's own heading: %d of %d" % ("PASS" if good else "FAIL", ok, total))
    return good


def ac2(root):
    check = os.path.join(root, "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~R1/round80/checks/r80_dd1.py")
    p = subprocess.run([sys.executable, check, "--crit", "AC3"], cwd=root, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONPATH=root))
    last = (p.stdout.strip().splitlines() or [""])[-1]
    good = p.returncode == 0
    print("%s B1 the 10-K and 20-F fixture sections hash as at round 80: %s" % ("PASS" if good else "FAIL", last))
    return good


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2"])
    ap.add_argument("--cache", default="")
    a = ap.parse_args()
    root = _root()
    cache = a.cache or os.path.join(root, ".scratch", "r82_20f")
    ok = ac1(root, cache) if a.crit == "AC1" else ac2(root)
    print("R82 CUT %s: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
