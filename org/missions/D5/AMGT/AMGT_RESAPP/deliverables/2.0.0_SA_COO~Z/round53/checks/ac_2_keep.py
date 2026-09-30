"""AMGT_RESAPP round 53, AMGT-ac-2 AC1 -- a D-1 regeneration keeps every SPAN-CARRYING served sentence (AMENDMENT 1, CTO msg 27185:
Z-S314 re-classified as C-VERBATIM-GATE HOLD working as designed; a stored sentence with no verbatim span is correctly held on rebuild).
For ASML_NA_Equity (the name round 52 measured the drop on: company_description 6 -> 1, investment_thesis 1 -> 0, risks 2 -> 0), the
committed producer builds the D-1 document IN MEMORY from the stored newest analysis (`drafting_build.build_drafting_document`, the
`--rebuild-pool` transform) and it is compared with the STORED `drafting/v1/ASML_NA_Equity.json`:
  - every stored served sentence that carries a verbatim span (non-empty `quoted_spans`) is present in the rebuilt document's sections,
    per section; the count of stored sentences WITHOUT a span (held on rebuild by design) is printed beside it.
Prints the per-section counts before and after. Writes nothing.
usage: python <this>   (from the repo root; S3 read-only)"""
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402

KEY = "ASML_NA_Equity"


def served(doc, spanned_only=False):
    return {s.get("section"): [str(x.get("text")) for x in (s.get("sentences") or [])
                               if not spanned_only or x.get("quoted_spans")] for s in doc.get("sections") or []}


def main():
    cl = boto3.client("s3", region_name="us-east-1")
    analysis = db._get_json_object(cl, db._newest_analysis_key(cl, KEY))
    stored = db._get_json_object(cl, db._drafting_pool_key(KEY))
    rebuilt = db.build_drafting_document(analysis)
    s0, s1, sp = served(stored), served(rebuilt), served(stored, spanned_only=True)
    bad = []
    for sec, sents in sp.items():
        got = s1.get(sec) or []
        lost = [t for t in sents if t not in got]
        if lost:
            bad.append("%s: span-carrying stored %d, lost %d" % (sec, len(sents), len(lost)))
    print("stored (all)            %s" % {k: len(v) for k, v in s0.items()})
    print("stored (span-carrying)  %s" % {k: len(v) for k, v in sp.items()})
    print("rebuilt                 %s" % {k: len(v) for k, v in s1.items()})
    print("stored without a span (held on rebuild by design): %d" % (sum(map(len, s0.values())) - sum(map(len, sp.values()))))
    for b in bad:
        print("  BAD", b)
    ok = sum(map(len, sp.values())) > 0 and not bad
    print("A D-1 REGENERATION KEEPS EVERY SPAN-CARRYING SERVED SENTENCE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
