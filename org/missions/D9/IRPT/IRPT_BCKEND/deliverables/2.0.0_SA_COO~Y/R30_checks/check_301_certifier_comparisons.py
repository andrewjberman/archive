#!/usr/bin/env python3
"""IB-yr-301 AC1 -- certification is HANDED the chosen comparisons and refuses a report that does not print them.

Five cases against `publication.build_publication` and `certify.missing_comparison_names`, all offline
(a two-page PDF built with fitz, the same census the extract tests use; no AWS, no vendor):
  0. CONTROL: build_publication with NO `comparisons` argument builds the specimen (so a failure below is the
     comparison rule and never the specimen).
  1. comparisons=["Opal Long-Term"] on a PDF that prints it            -> builds, fragment equal to case 0's
  2. comparisons=["Opal Long-Term", "Opal Growth"], second NOT printed -> PublicationRefused COMPARISON_NOT_PRINTED
  3. WHOLE NAME: the PDF prints only "Opal Long-Term-Plus"             -> PublicationRefused COMPARISON_NOT_PRINTED
  4. comparisons=() is today's behaviour                               -> fragment and evidence_sha256 equal to case 0's
  5. certify.missing_comparison_names(pdf, [..two names..])            -> ["Opal Growth"]
PASS iff the control and all five hold. Base run (before the cut): FAIL at case 1 -- build_publication takes no
`comparisons` argument, so certification is never handed the chosen names (S194 half 2).
Issuer 2.0.0_SA_COO~Y, round 30. ASCII only.
"""
import os
import sys

ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[8])  # parents[0] is R30_checks; the repo root is parents[8]
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "lambda", "investor-reporting", "ycharts", "extract"))

import fitz  # noqa: E402
import certify  # noqa: E402
import publication  # noqa: E402

CENSUS = {"sections": [
    {"id": "S1", "title": "Summary", "pages": [99], "fields": [{"field": "Return", "unit": "pct"}]},
    {"id": "S2", "title": "Growth of Wealth", "pages": [99], "fields": []},
    {"id": "S3", "title": "Disclosure", "pages": [99],
     "fields": [{"term": "Risk", "definition": "All investments carry risk."}]}]}


def pdf(names):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((40, 80), "Return")
    page.insert_text((300, 80), "10.30%")
    page = doc.new_page()
    page.insert_text((40, 50), "Growth of Wealth")
    page.insert_text((40, 100), "All investments")
    page.insert_text((40, 115), "carry risk.")
    page = doc.new_page()
    for i, name in enumerate(names):
        page.insert_text((40, 60 + 30 * i), name)
    data = doc.tobytes()
    doc.close()
    return data


def build(data, **kw):
    return publication.build_publication(data, CENSUS, specimen_label="synthetic", specimen_id="r30-301", **kw)


def refusal(data, comparisons):
    try:
        build(data, comparisons=comparisons)
        return "BUILT"
    except publication.PublicationRefused as exc:
        return str(exc)


def main():
    printed = pdf(["Opal Long-Term"])
    try:
        base = build(printed)
    except Exception as exc:  # the specimen itself must build, or nothing below means anything
        print("FAIL: control -- the specimen does not build without comparisons: %s %s" % (type(exc).__name__, exc))
        return 1
    held, first = 0, None

    def case(n, ok, detail):
        nonlocal held, first
        if ok:
            held += 1
        elif first is None:
            first = "case %d: %s" % (n, detail)

    try:
        one = build(printed, comparisons=["Opal Long-Term"])
        case(1, one["fragment"] == base["fragment"], "a printed comparison changed the fragment")
    except Exception as exc:
        case(1, False, "%s %s" % (type(exc).__name__, exc))
    for n, data, names in ((2, printed, ["Opal Long-Term", "Opal Growth"]),
                           (3, pdf(["Opal Long-Term-Plus"]), ["Opal Long-Term"])):
        try:
            got = refusal(data, names)
            case(n, got == "COMPARISON_NOT_PRINTED", "expected COMPARISON_NOT_PRINTED, got %s" % got)
        except Exception as exc:
            case(n, False, "%s %s" % (type(exc).__name__, exc))
    try:
        empty = build(printed, comparisons=())
        case(4, empty["fragment"] == base["fragment"] and empty["evidence_sha256"] == base["evidence_sha256"],
             "an empty comparisons sequence changed the publication")
    except Exception as exc:
        case(4, False, "%s %s" % (type(exc).__name__, exc))
    try:
        missing = certify.missing_comparison_names(printed, ["Opal Long-Term", "Opal Growth"])
        case(5, list(missing) == ["Opal Growth"], "missing_comparison_names returned %r" % (missing,))
    except Exception as exc:
        case(5, False, "%s %s" % (type(exc).__name__, exc))
    if held == 5:
        print("PASS: 5 of 5 comparison-certification cases hold")
        return 0
    print("FAIL: %d of 5 comparison-certification cases hold -- %s" % (held, first))
    return 1


if __name__ == "__main__":
    sys.exit(main())
