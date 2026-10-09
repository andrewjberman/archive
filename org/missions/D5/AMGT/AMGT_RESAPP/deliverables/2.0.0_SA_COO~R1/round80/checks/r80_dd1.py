"""r80_r1.py -- round 80 cell R1 checks (2.0.0_SA_COO~R1, DRAFT at the cut).

--crit AC1  BUILD: a 20-F has a `business` section (Item 4.B Business overview), cut from its own
            heading and closed before Item 4.C / Item 5; a 20-F with no such heading reads
            business FAILED with a reason; fetch.EXCERPT_ITEMS["20-F"] carries "business".
--crit AC2  BUILD: lib/research/filings/section_census.py prints, for every stored 20-F name, which
            heading each stored item came from, and one count line whose denominator equals the
            number of stored 20-F rows this checker reads itself (read only).
--crit AC3  BOUND: the cutter's existing outputs do not move: the 10-K fixture's three sections and
            the 20-F fixture's risk / mdna / officers sections hash exactly as at the base.

PyMuPDF (`fitz`) does not import on dell1; cut() never touches it, so this checker stubs the
module when the import fails and prints that it did.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import types

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
if ROOT and ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    import fitz  # noqa: F401
except Exception as exc:  # dell1: not installed / DLL load failure
    sys.modules["fitz"] = types.ModuleType("fitz")
    print("NOTE: fitz stubbed for this check (%s); cut() does not use it" % type(exc).__name__)


def _para(marker, n=40):
    return " ".join(["%s sentence %d about this part of the filing and nothing else." % (marker, i) for i in range(n)])


FIXTURE_20F = "\n".join([
    "Item 3. Key Information",
    "D. Risk Factors",
    _para("RISKMARK"),
    "Item 4. Information on the Company",
    "A. History and development of the company",
    _para("HISTMARK", 5),
    "B. Business overview",
    _para("BUSINESSMARK"),
    "C. Organizational structure",
    _para("ORGMARK", 5),
    "Item 4A. Unresolved Staff Comments",
    "None.",
    "Item 5. Operating and Financial Review and Prospects",
    _para("MDNAMARK"),
    "Item 6. Directors, Senior Management and Employees",
    _para("OFFICERMARK"),
    "Item 7. Major Shareholders and Related Party Transactions",
    _para("HOLDERMARK", 5),
    "Item 16K. Cybersecurity",
    "Risk factors - Cybersecurity and other security",
    _para("CYBERMARK"),
    "Share capital",
    _para("SHARECAPMARK"),
])

FIXTURE_20F_NO_BUSINESS = FIXTURE_20F.replace("B. Business overview\n", "")

FIXTURE_10K = "\n".join([
    "Item 1. Business",
    _para("TENKBUS"),
    "Item 1A. Risk Factors",
    _para("TENKRISK"),
    "Item 1B. Unresolved Staff Comments",
    "None.",
    "Item 7. Management's Discussion and Analysis of Financial Condition",
    _para("TENKMDNA"),
    "Item 7A. Quantitative and Qualitative Disclosures About Market Risk",
    _para("TENKQ", 5),
    "Item 10. Directors, Executive Officers and Corporate Governance",
    _para("TENKOFF"),
    "Item 11. Executive Compensation",
    _para("TENKCOMP", 5),
])

# Measured at the base (box/dell1 0e77b427cd) by `--crit BASEHASH`; AC3 compares against these.
BASE_HASHES = {
    "10-K:risk": "38ec4f2ff4c8f22996232524f8a8037d7e7bbd7c1e116c0460c0355d3602e123",
    "10-K:mdna": "2f907204b6dbce63235cc4128908ad63a6e0fb325a6b6294e1e7c2e6b57b99ec",
    "10-K:officers": "cfb2041b41e4c755a776d747fc9556a11ccdafc5499d92ef704c07f96b196705",
    "20-F:risk": "ab299b2f36b12ca1117a7772a719fc85cbc296aa811f0720f2103d8c1f784390",
    "20-F:mdna": "705604c25dd4ec20157f2292d5373371cbc87345104a4f29ebccbe1a29ec9bb7",
    "20-F:officers": "9ce8f007a65bc2a94b693b4237883efe1fc6fb8042027628c3cb6580f0a86629",
}


def _hash_section(sec):
    blob = json.dumps({k: sec.get(k) for k in ("status", "text", "full_chars", "heading_matched")}, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _section_hashes():
    from lib.research.filings import document
    out = {}
    for family, text in (("10-K", FIXTURE_10K), ("20-F", FIXTURE_20F)):
        sections = document.cut(text, family)["sections"]
        for key in ("risk", "mdna", "officers"):
            out["%s:%s" % (family, key)] = _hash_section(sections[key])
    return out


def ac1():
    from lib.research.filings import document, fetch
    ok = True
    sections = document.cut(FIXTURE_20F, "20-F")["sections"]
    bus = sections.get("business")
    if not bus:
        print("A1 FAIL: the 20-F cut has no business key (keys: %s)" % sorted(sections))
        ok = False
    else:
        text = bus.get("text") or ""
        cond = (bus.get("status") == "OK" and text.lstrip().lower().startswith("b. business overview")
                and "BUSINESSMARK" in text and "ORGMARK" not in text and "MDNAMARK" not in text
                and "SHARECAPMARK" not in text and "RISKMARK" not in text)
        print("A1 %s: business status=%s, starts=%r, own text only=%s" % (
            "PASS" if cond else "FAIL", bus.get("status"), text[:22], cond))
        ok = ok and cond
    bus2 = document.cut(FIXTURE_20F_NO_BUSINESS, "20-F")["sections"].get("business")
    cond2 = bool(bus2) and bus2.get("status") == "FAILED" and not bus2.get("text") and bool(bus2.get("reason"))
    print("A2 %s: a 20-F with no Business overview heading reads business FAILED with a reason" % ("PASS" if cond2 else "FAIL"))
    ok = ok and cond2
    items = list(getattr(fetch, "EXCERPT_ITEMS", {}).get("20-F", []))
    cond3 = "business" in items
    print("A3 %s: fetch.EXCERPT_ITEMS['20-F'] = %s" % ("PASS" if cond3 else "FAIL", items))
    ok = ok and cond3
    print("R80 R1 AC1 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def _stored_20f_keys():
    from lib.research.harvest import filings as hf
    from lib.research.harvest import store as hs
    keys = set()
    for vendor in ("sec", "issuer-site"):
        rows = hs.silver_latest(vendor, "filing_source", ("security_key", "accession"))
        rows = list(rows.values()) if isinstance(rows, dict) else list(rows)
        for row in rows:
            obj = hf.source_object_from_row(row)
            if (obj.get("form") or obj.get("family")) == "20-F":
                keys.add(obj["security_key"])
    return keys


def ac2():
    path = os.path.join(ROOT, "lib", "research", "filings", "section_census.py")
    if not os.path.exists(path):
        print("C0 FAIL: lib/research/filings/section_census.py does not exist")
        print("R80 R1 AC2 SERVED: NO")
        return 1
    expected = _stored_20f_keys()
    proc = subprocess.run([sys.executable, "-m", "lib.research.filings.section_census", "--stored"],
                          capture_output=True, text=True, cwd=ROOT, timeout=600,
                          env=dict(os.environ, PYTHONPATH=ROOT))
    out = proc.stdout
    print(out.rstrip()[-3000:])
    ok = proc.returncode == 0
    print("C1 %s: census exit=%d" % ("PASS" if ok else "FAIL", proc.returncode))
    named = {k for k in expected if re.search(r"^%s\b" % re.escape(k), out, re.M)}
    c2 = named == expected
    print("C2 %s: %d of %d stored 20-F names have a census line" % ("PASS" if c2 else "FAIL", len(named), len(expected)))
    m = re.search(r"^SECTION CENSUS: (\d+) of (\d+) stored 20-F names", out, re.M)
    c3 = bool(m) and int(m.group(2)) == len(expected)
    print("C3 %s: count line denominator %s, checker's own count %d" % (
        "PASS" if c3 else "FAIL", m.group(2) if m else "ABSENT", len(expected)))
    asml = re.search(r"^ASML_NA_Equity\b.*$", out, re.M)
    c4 = bool(asml) and "risk: FALLBACK" in asml.group(0)
    print("C4 %s: ASML NA's line names its stored risk text as the fallback heading" % ("PASS" if c4 else "FAIL"))
    ok = ok and c2 and c3 and c4
    print("R80 R1 AC2 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def ac3():
    now = _section_hashes()
    ok = True
    for key, want in BASE_HASHES.items():
        same = want is not None and now.get(key) == want
        ok = ok and same
        print("B %s: %s %s" % ("PASS" if same else "FAIL", key, (now.get(key) or "")[:12]))
    print("R80 R1 AC3 SERVED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", required=True, choices=["AC1", "AC2", "AC3", "BASEHASH"])
    ap.add_argument("--where", default="local")
    args = ap.parse_args()
    if args.crit == "BASEHASH":
        print(json.dumps(_section_hashes(), indent=1, sort_keys=True))
        return 0
    return {"AC1": ac1, "AC2": ac2, "AC3": ac3}[args.crit]()


if __name__ == "__main__":
    sys.exit(main())
