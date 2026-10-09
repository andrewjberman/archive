"""AMGT_RESAPP round-83 PREP (DRAFT, not issued) -- PBR's 20-F sections cut by IDENTITY (row AMGT_RESAPP-D1-W323-S1).

  python r83_pbr.py --crit AC1 [--cache <dir>]

AC1 (build): read the five cached real 20-F texts (default .scratch/r82_20f/<KEY>.txt; the cache is the input, nothing is
    fetched), run document.cut(text, "20-F") in-process, and grade:
    P1 PBR business is the "Our Business" section the cross-reference table cites for Item 4.B with its four sub-sections
       (contents page 63): the cut starts on running-header page 63 (offsets 318985-319100) and opens "Exploration & Production".
    P2 PBR risk is the "Risks" section the table cites for Item 3.D (contents page 30): it starts inside running-header page 30
       (offsets 208986-209800) and ends at the "Cybersecurity Framework and Risk Management" heading (Item 16K, header page 57).
    P3 PBR mdna is the "Operating and Financial Review and Prospects" section the table cites for Item 5 (contents page 170): it
       starts on running-header page 169 or 170 (offsets 549850-549960), opens "Consolidated Financial Performance" and does not run
       past the "Management and Employees" divider (header page 191, offset 593198).
    P4 the other four names' 12 cells (business, risk, mdna) are unchanged from the merged cutter @9f252e010a: start offset,
       chars and sha256 prefix, as measured 2026-10-09 on the same cache.
    Lengths are printed, never graded: round 82 showed a plausible length on a wrong section.
Verdict: R83 PBR AC1: YES|NO (exit 0|1). At the base (box/dell1 @9f252e010a): NO -- P1 (business is "About us" at 198623) and
    P3 (mdna is "Liquidity and Capital Resources" at 568965) FAIL; P2 and P4 PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import types

KEY = "PBR_US_Equity"
ITEMS = ("business", "risk", "mdna")

# (start offset in the cached text, chars, sha256[:16]) of each cell at the merged cutter @9f252e010a
BASELINE = {
    "ASML_NA_Equity": {
        "business": (104372, 60000, "b4c0ff6071e21ef1"),
        "risk": (227926, 53968, "eec4b38988f67c60"),
        "mdna": (196348, 31578, "94a987b885876def"),
    },
    "BABA_US_Equity": {
        "business": (490926, 60000, "cbedc9423f19aca2"),
        "risk": (135987, 70000, "5190afa5643b2ec7"),
        "mdna": (716753, 80000, "a1cbfdea529ff374"),
    },
    "NU_US_Equity": {
        "business": (98628, 60000, "6f14a79396e4c211"),
        "risk": (329501, 70000, "2a396609775656ca"),
        "mdna": (622154, 80000, "14af18e5d012af6f"),
    },
    "SAP_GY_Equity": {
        "business": (239867, 60000, "81da5b2b5ae01a5a"),
        "risk": (206122, 33745, "61fe957b4d1dd4aa"),
        "mdna": (318035, 80000, "670e2470b57b0dc3"),
    },
}

BUSINESS_START = (318985, 319100)
BUSINESS_OPENS = "Exploration & Production"
RISK_START = (208986, 209800)
RISK_END_HEADING = "Cybersecurity Framework and Risk Management"
MDNA_START = (549850, 549960)
MDNA_OPENS = "Consolidated Financial Performance"
MDNA_LIMIT = 593198


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _document(root):
    if root and root not in sys.path:
        sys.path.insert(0, root)
    try:
        import fitz  # noqa: F401
    except Exception:  # noqa: BLE001 -- a box without PyMuPDF; cut() never reads it
        sys.modules["fitz"] = types.ModuleType("fitz")
    from lib.research.filings import document

    return document


def _cells(document, text):
    sections = document.cut(text, "20-F")["sections"]
    out = {}
    for item in ITEMS:
        sec = sections.get(item) or {}
        body = sec.get("text") or ""
        start = text.find(body[:300]) if body else -1
        out[item] = {
            "status": sec.get("status"),
            "start": start,
            "chars": sec.get("chars") or 0,
            "full_chars": sec.get("full_chars") or 0,
            "sha": hashlib.sha256(body.encode("utf-8")).hexdigest()[:16],
            "heading": (sec.get("heading_matched") or "").replace("\n", " ")[:60],
            "head": body[:160],
        }
    return out


def ac1(cache):
    document = _document(_root())
    path = os.path.join(cache, KEY + ".txt")
    if not os.path.isfile(path):
        print("   no cached text at %s" % path)
        return say(False, "P0 the cached PBR filing text exists")
    text = open(path, encoding="utf-8").read()
    cells = _cells(document, text)
    for item in ITEMS:
        c = cells[item]
        print("   %s %-8s %-6s start=%d chars=%d full=%d heading=%r" % (
            KEY, item, c["status"], c["start"], c["chars"], c["full_chars"], c["heading"]))
    b, r, m = cells["business"], cells["risk"], cells["mdna"]
    p1 = say(b["status"] == "OK" and BUSINESS_START[0] <= b["start"] <= BUSINESS_START[1] and BUSINESS_OPENS in b["head"],
             "P1 business is the Our Business section (Item 4.B; header page 63; opens %r)" % BUSINESS_OPENS)
    risk_end = r["start"] + r["full_chars"]
    cyber = text.find("\n" + RISK_END_HEADING + "\n", max(r["start"], 0))  # the body heading, not the contents line
    p2 = say(r["status"] == "OK" and RISK_START[0] <= r["start"] <= RISK_START[1] and cyber > 0 and abs(risk_end - (cyber + 1)) <= 2,
             "P2 risk is the Risks section (Item 3.D; header page 30) closed at %r (end %d, heading %d)" % (
                 RISK_END_HEADING, risk_end, cyber + 1))
    mdna_end = m["start"] + m["full_chars"]
    p3 = say(m["status"] == "OK" and MDNA_START[0] <= m["start"] <= MDNA_START[1] and MDNA_OPENS in m["head"]
             and mdna_end <= MDNA_LIMIT + 100,
             "P3 mdna is the Operating and Financial Review and Prospects section (Item 5; header page 170; end %d <= %d)" % (
                 mdna_end, MDNA_LIMIT))
    same = 0
    for key, want in BASELINE.items():
        p = os.path.join(cache, key + ".txt")
        if not os.path.isfile(p):
            print("   %s: no cached text" % key)
            continue
        got = _cells(document, open(p, encoding="utf-8").read())
        for item in ITEMS:
            g = got[item]
            ok = (g["start"], g["chars"], g["sha"]) == want[item]
            same += ok
            if not ok:
                print("   MOVED %s %s: start %d chars %d sha %s (was %s)" % (key, item, g["start"], g["chars"], g["sha"], want[item]))
    p4 = say(same == 12, "P4 the other four names' cells unchanged: %d of 12" % same)
    return p1 and p2 and p3 and p4


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--cache", default=os.path.join(".scratch", "r82_20f"))
    a = ap.parse_args()
    ok = ac1(a.cache)
    print("R83 PBR AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
