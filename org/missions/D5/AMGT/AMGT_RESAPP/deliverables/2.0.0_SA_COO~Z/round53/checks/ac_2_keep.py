"""AMGT_RESAPP round 53, AMGT-ac-2 AC1 -- a D-1 regeneration keeps every served sentence (CTO round-52 ruling 3; disarms row Z-S314).
For ASML_NA_Equity (the name round 52 measured the drop on: company_description 6 -> 1, investment_thesis 1 -> 0, risks 2 -> 0), the
committed producer builds the D-1 document IN MEMORY from the stored newest analysis (`drafting_build.build_drafting_document`, the
`--rebuild-pool` transform) and it is compared with the STORED `drafting/v1/ASML_NA_Equity.json`:
  - every stored served sentence (sections[].sentences[].text) is present in the rebuilt document's sections, per section;
  - the served sentence count per section is >= the stored count.
Prints the per-section counts before and after. Writes nothing.
usage: python <this>   (from the repo root; S3 read-only)"""
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402

KEY = "ASML_NA_Equity"


def served(doc):
    return {s.get("section"): [str(x.get("text")) for x in (s.get("sentences") or [])] for s in doc.get("sections") or []}


def main():
    cl = boto3.client("s3", region_name="us-east-1")
    analysis = db._get_json_object(cl, db._newest_analysis_key(cl, KEY))
    stored = db._get_json_object(cl, db._drafting_pool_key(KEY))
    rebuilt = db.build_drafting_document(analysis)
    s0, s1 = served(stored), served(rebuilt)
    bad = []
    for sec, sents in s0.items():
        got = s1.get(sec) or []
        lost = [t for t in sents if t not in got]
        if lost or len(got) < len(sents):
            bad.append("%s: stored %d, rebuilt %d, lost %d" % (sec, len(sents), len(got), len(lost)))
    print("stored  %s" % {k: len(v) for k, v in s0.items()})
    print("rebuilt %s" % {k: len(v) for k, v in s1.items()})
    for b in bad:
        print("  BAD", b)
    ok = bool(s0) and not bad
    print("A D-1 REGENERATION KEEPS EVERY SERVED SENTENCE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
