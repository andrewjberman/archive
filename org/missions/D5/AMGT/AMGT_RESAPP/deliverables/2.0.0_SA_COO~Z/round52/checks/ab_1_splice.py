"""AMGT_RESAPP round 52, AMGT-ab-1 -- ASML's D-1 drafting document takes the rewritten analysis's thesis_driver and NOTHING ELSE moves
(CTO round-51 analysis item 1, issuer ruling at the cut: a full `--rebuild-pool` of ASML would ALSO drop served sentences --
company_description 6 -> 1, investment_thesis 1 -> 0, risks 2 -> 0 -- under today's stricter verbatim gate, so the act splices).
`lib.research.filings.drafting_build.splice_driver(stored_document, analysis, provenance) -> document` returns the stored D-1 document
with ONLY `thesis_driver` replaced by the analysis's own (the value `build_drafting_document` would carry, `drafting_build.py:365`) AND
the splice's PROVENANCE recorded in the document (CTO msg 27014 condition 1: the source analysis key and its S3 VersionId, so the D-1 is
never silently mixed-vintage) -- inside `thesis_driver` or in ONE added top-level key, wherever the served schema admits it.
This check, READ-ONLY on the stored objects for ASML_NA_Equity (newest analysis; drafting/v1/ASML_NA_Equity.json):
  - the top-level keys that differ are 'thesis_driver' plus at most ONE other key (the provenance's home), and the moved keys carry
    both provenance values (the analysis key and its VersionId, read here with head_object);
  - the spliced thesis_driver carries >= 2 points with a span;
  - the SERVED reader's own validator (`scoped_amgt._validate_drafting_document`) accepts the spliced document.
The served proof (the chart on the route) is AMGT-ab-6's.
usage: python <this>   (from the repo root; S3 read-only)"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import boto3  # noqa: E402
from lib.research.api import scoped_amgt as sa  # noqa: E402
from lib.research.filings import drafting_build as db  # noqa: E402

KEY = "ASML_NA_Equity"


def main():
    if not hasattr(db, "splice_driver"):
        print("drafting_build has no splice_driver")
        print("THE D-1 DOCUMENT TAKES THE SPANNED DRIVER AND NOTHING ELSE MOVES: NO")
        return 1
    cl = boto3.client("s3", region_name="us-east-1")
    akey = db._newest_analysis_key(cl, KEY)
    analysis = db._get_json_object(cl, akey)
    vid = cl.head_object(Bucket=db.POOL_BUCKET if hasattr(db, "POOL_BUCKET") else "opal-data-harvest", Key=akey).get("VersionId")
    provenance = {"analysis_key": akey, "analysis_version_id": vid}
    stored = db._get_json_object(cl, db._drafting_pool_key(KEY))
    before = json.dumps(stored, sort_keys=True)
    spliced = db.splice_driver(stored, analysis, provenance)
    mutated_input = json.dumps(stored, sort_keys=True) != before
    keys = sorted(set(spliced) | set(stored))
    moved = [k for k in keys if json.dumps(spliced.get(k), sort_keys=True) != json.dumps(stored.get(k), sort_keys=True)]
    pts = (spliced.get("thesis_driver") or {}).get("points") or []
    spanned = sum(1 for p in pts if isinstance(p, dict) and p.get("span"))
    valid, reason = sa._validate_drafting_document(spliced)
    moved_text = json.dumps({k: spliced.get(k) for k in moved}, sort_keys=True)
    prov_ok = akey in moved_text and bool(vid) and vid in moved_text
    print("differing top-level keys: %s; driver points %d, spanned %d; served validator: %s %s; input mutated: %s; provenance %s @ %s "
          "recorded: %s" % (moved, len(pts), spanned, valid, reason or "", mutated_input, akey, vid, prov_ok))
    ok = ("thesis_driver" in moved and len(moved) <= 2 and prov_ok and spanned >= 2 and valid and not mutated_input)
    print("THE D-1 DOCUMENT TAKES THE SPANNED DRIVER AND NOTHING ELSE MOVES: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
