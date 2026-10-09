"""AMGT_RESAPP round-84 PREP -- the cutter strips a filing's running page header (CTO~DELL1 round-83 analysis R1 item 3).

  python r84_header.py --crit AC1 [--cache DIR]

Cuts the five cached real 20-F filings in-process with lib/research/filings/document.cut(text, "20-F") (no network, no
store read, no write) and grades the 15 cut sections (business, risk, mdna):

  H1 no running-page-header line is left in any of the 15 cut sections (denominator printed per name and per section).
  H2 negative control: lines planted inside ASML's business section that merely RESEMBLE furniture -- a prose sentence
     that opens with the report title, a sentence ending in a number, and a standalone number NOT next to furniture --
     are all KEPT by the cutter.

The check defines furniture on its own (it never imports the producer's rule), from the WHOLE filing text:
  - a candidate is a line (digits normalised to '#', zero-width characters removed) with at least two letters and 8 or
    more characters that repeats 100 or more times in the filing;
  - a candidate is furniture when 80% or more of its occurrences sit next to a page-number line (`n`, `F-n`, `F- n`,
    roman `i`..), or the line itself ends in `I <page>` (an integrated report's `<title> I <n>`), or -- iterated to a
    fixpoint -- 80% or more of its occurrences sit next to furniture (a navigation-tab block: ASML's four tabs);
  - a page-number line next to furniture is furniture too.
Measured at the base (2026-10-09): ASML 7 furniture lines (4 tabs, 'ASML Annual Report #', 'General disclosures',
'Environmental'), BABA and SAP 'Table of Contents', NU 'Form #-F | #', PBR 'Annual Report and Form #-F # I #' (+ three
F-page headers outside the cuts). Repeated table cells ('Total', 'RMB', 'NA', XBRL members) are not furniture.

Verdict: R84 HEADER AC1: YES|NO (exit 0|1). At the base it reads NO (H1: 115/48/72 ASML lines, 28/26/46 BABA, ...).
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import subprocess
import sys
import types

NAMES = ("ASML_NA_Equity", "BABA_US_Equity", "NU_US_Equity", "PBR_US_Equity", "SAP_GY_Equity")
ITEMS = ("business", "risk", "mdna")
PAGENO = re.compile(r"^(?:[A-Z]-\s?)?\d{1,4}$|^[ivxlc]{1,6}$")
INLINE_PAGE = re.compile(r" I \d{1,4}$")
ZW = "​‌‍﻿"
MIN_REPEAT = 100
SHARE = 0.8
PLANTS = (
    "ASML Annual Report 2025 records net sales of EUR 32.7 billion, a new high for the company.",
    "The number of EUV systems we shipped in the year was 48",
    "4713",
)


def clean(line):
    return line.strip().strip(ZW).strip()


def norm(line):
    return re.sub(r"\d+", "#", clean(line))


def furniture(text):
    seq = [clean(raw) for raw in text.split("\n")]
    seq = [s for s in seq if s]
    keys = [norm(s) for s in seq]
    counts = collections.Counter(keys)
    cand = {k for k, n in counts.items() if n >= MIN_REPEAT and len(k) >= 8 and re.search(r"[A-Za-z]{2}", k)}
    pos = collections.defaultdict(list)
    for i, k in enumerate(keys):
        if k in cand:
            pos[k].append(i)
    isnum = [bool(PAGENO.match(s)) for s in seq]

    def share(k, pred):
        ps = pos[k]
        hit = sum(1 for i in ps if (i > 0 and pred(i - 1)) or (i + 1 < len(seq) and pred(i + 1)))
        return hit / len(ps)

    fur = {k for k in cand if share(k, lambda j: isnum[j]) >= SHARE or INLINE_PAGE.search(seq[pos[k][0]])}
    grown = True
    while grown:
        grown = False
        for k in sorted(cand - fur):
            if share(k, lambda j: keys[j] in fur) >= SHARE:
                fur.add(k)
                grown = True
    return fur


def left_in(section_text, fur):
    """(furniture lines left, non-blank lines) in one cut section."""
    lines = [clean(raw) for raw in section_text.split("\n")]
    lines = [s for s in lines if s]
    keys = [norm(s) for s in lines]
    bad = {i for i, k in enumerate(keys) if k in fur}
    for i in list(bad):
        for j in (i - 1, i + 1):
            if 0 <= j < len(lines) and PAGENO.match(lines[j]):
                bad.add(j)
    return len(bad), len(lines)


def imports(root):
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        import fitz  # noqa: F401
    except Exception:  # noqa: BLE001 -- a box without PyMuPDF; cut() never reads it
        sys.modules["fitz"] = types.ModuleType("fitz")
    from lib.research.filings import document as D
    return D


def plant(text, D):
    """ASML's text with the PLANTS inserted at a body line ~2,000 chars into its cut business section."""
    sec = D.cut(text, "20-F")["sections"]["business"]
    body = sec.get("text") or ""
    anchor = None
    for raw in body[2000:].split("\n"):
        s = raw.strip()
        if len(s) >= 40 and text.count(s) == 1:
            anchor = s
            break
    if anchor is None:
        return None
    at = text.index(anchor) + len(anchor)
    return text[:at] + "\n" + "\n".join(PLANTS) + "\n" + text[at:]


def ac1(root, cache):
    D = imports(root)
    total_left = 0
    for key in NAMES:
        path = os.path.join(cache, key + ".txt")
        if not os.path.isfile(path):
            print("FAIL %-16s no cached filing at %s" % (key, path))
            return False
        text = open(path, encoding="utf-8").read()
        fur = furniture(text)
        sections = D.cut(text, "20-F")["sections"]
        cells = []
        for item in ITEMS:
            s = sections.get(item) or {}
            n, of = left_in(s.get("text") or "", fur)
            total_left += n
            cells.append("%s %d of %d" % (item, n, of))
        print("   %-16s furniture %d %s | left: %s" % (key, len(fur), sorted(fur)[:4], "; ".join(cells)))
    h1 = total_left == 0
    print("%s H1 running-header lines left in the 15 cut sections: %d" % ("PASS" if h1 else "FAIL", total_left))

    asml = open(os.path.join(cache, "ASML_NA_Equity.txt"), encoding="utf-8").read()
    planted = plant(asml, D)
    if planted is None:
        print("FAIL H2 no unique anchor line found in ASML's business section to plant beside")
        return False
    body = D.cut(planted, "20-F")["sections"]["business"].get("text") or ""
    kept = [p for p in PLANTS if any(clean(raw) == p for raw in body.split("\n"))]
    h2 = len(kept) == len(PLANTS)
    print("%s H2 planted look-alike lines kept in ASML's business cut: %d of %d" % ("PASS" if h2 else "FAIL", len(kept), len(PLANTS)))
    return h1 and h2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1"])
    ap.add_argument("--cache", default=None)
    a = ap.parse_args()
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    cache = a.cache or os.path.join(root, ".scratch", "r82_20f")
    ok = ac1(root, cache)
    print("R84 HEADER AC1: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
