"""AMGT-kk-3 transform (deliverable, not product code), offline, no fetch, no model call.
  py -3.12 build_kk3.py --prior <current stored draft json> --out <repaired json> [--nu-whole <build_repaired.py output, no --first-only>]
company_description keeps only sentences whose EVERY evidence record locates in the business item (the merged
drafting_build.location_is_business rule: 20-F Item 4 / 4.B, 10-K Item 1), read from the draft's evidence_records[].source.location.
--nu-whole: take text/text_original of sentences numbered 6, 11, 19 (1-based over ALL sections of the stored draft) from that file.
Every other byte of the document is kept (the document is re-serialised with indent=2, the repo draft convention)."""
import argparse
import json
import sys
sys.path.insert(0, ".")
from lib.research.filings.drafting_build import location_is_business

ap = argparse.ArgumentParser()
ap.add_argument("--prior", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--nu-whole")
a = ap.parse_args()
doc = json.load(open(a.prior, encoding="utf-8"))
if a.nu_whole:
    whole = json.load(open(a.nu_whole, encoding="utf-8"))
    n = 0
    for sa, sb in zip(doc["sections"], whole["sections"]):
        for x, y in zip(sa["sentences"], sb["sentences"]):
            n += 1
            if n in (6, 11, 19):
                print("restored %d (%s): %d -> %d chars" % (n, sa["section"], len(x["text"]), len(y["text"])))
                x["text"] = y["text"]
                x["text_original"] = y["text_original"]
loc = {r["id"]: ((r.get("source") or {}).get("location")) for r in doc["evidence_records"]}
for sec in doc["sections"]:
    if sec["section"] != "company_description":
        continue
    keep, drop = [], []
    for i, s in enumerate(sec["sentences"], 1):
        ids = s.get("evidence") or []
        ok = bool(ids) and all(e in loc and location_is_business(loc[e]) for e in ids)
        (keep if ok else drop).append(s)
        print("  description %2d %s | %s | %s" % (i, "KEEP" if ok else "DROP", [loc.get(e) for e in ids], s["text"][:60].encode("ascii", "replace").decode()))
    sec["sentences"] = keep
    print("company_description: kept %d, removed %d" % (len(keep), len(drop)))
json.dump(doc, open(a.out, "w", encoding="utf-8", newline="\n"), indent=2)
