"""HVST-f-1 AC1: the per-form census of what ticker and short-name forms WOULD ADD over the served
alias sets, over the silver articles. Read-only."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def main():
    securities, articles, rows = C.compute()
    n_sec = len(securities)
    print("== HVST-f-1 AC1: ticker and brand form census ==")
    print("securities (denominator)=%d  silver articles (denominator)=%d  matcher=publication_gold._span_pattern "
          "(_match_counts' own pattern: longest-first, word-bounded, one span one count)" % (n_sec, len(articles)))
    print("ADDED = spans(aliases + [form]) minus spans(aliases), title and blocks; pair flips = title / lead(first %d blocks) "
          "flag False -> True; NEW pair = the security had 0 mentions in the article under the served aliases" % C.LEAD_BLOCKS)
    print("English-dictionary flag: NO dictionary is installed or in the estate (row Z-W43-S1). DICT-WORD marks a form that is "
          "(a) in sklearn's ENGLISH_STOP_WORDS (%d words), (b) in this cell's CURATED list (judgment, printed below), or "
          "(c) seen in the corpus in ordinary lower case. A form without the flag is NOT certified as a non-word." % len(C.STOP))
    print("CURATED list (%d): %s" % (len(C.CURATED_WORDS), ", ".join(sorted(C.CURATED_WORDS))))
    print()
    print("BRAND SOURCE: %s. Searched: json/jsonl/yaml keys brand|brands|short_name|also_known_as|aka|dba|former_name|"
          "alt_names|name_variants (4 files, none a company map: orioneclipse openapi, two portal themes, a tokenizer); "
          "'Alphabet' near 'Google' over json/jsonl/yaml/csv/py (3 files: two research transcripts, one narrative fixture, "
          "no alias map); lib/research SHORT_NAME|SECURITY_NAME|BRAND (ceo_search.company_short_name strips legal suffixes, "
          "which the served aliases already do). Securities covered by a sourced brand form: 0 of %d. "
          "So no sourced brand form is counted; class B1 is a DERIVATION from the universe's own `aliases` field and is not "
          "a brand list: it cannot produce 'Google' for Alphabet." % (C.NO_BRAND_SOURCE, n_sec))
    print()
    grand_forms = grand_hit_forms = 0
    for cls in C.CLASSES:
        crows = [r for r in rows if r["class"] == cls]
        gen = len(crows)
        covered = sum(1 for r in crows if r["covered"])
        with_hits = [r for r in crows if r["hits"]]
        print("== CLASS %s ==" % cls)
        print("forms generated=%d (denominator: %d securities; %d distinct strings); already an alias (not counted)=%d; "
              "forms with added hits=%d of %d generated" % (
                  gen, n_sec, len({r["form"] for r in crows}), covered, len(with_hits), gen))
        print("CLASS TOTAL: added pairs=%d (of which NEW pairs=%d) added mention_count=%d title flips=%d lead flips=%d  "
              "flagged forms=%d, of which with added hits=%d" % (
                  sum(r["pairs"] for r in crows), sum(r["new_pairs"] for r in crows),
                  sum(r["added_count"] for r in crows), sum(r["title_flips"] for r in crows),
                  sum(r["lead_flips"] for r in crows), sum(1 for r in crows if r["flags"]),
                  sum(1 for r in with_hits if r["flags"])))
        if not crows:
            print("(no ticker in the %d securities carries a share-class suffix such as BRK/B, so T2 differs from T1 for none; "
                  "'BP/' and 'NG/' are trailing-slash tickers, stripped in T1)" % n_sec)
        print("%-14s %-22s %-26s %5s %5s %6s %5s %5s  %s" % (
            "security_key", "form", "company", "pairs", "newP", "added", "tFlip", "lFlip", "flags"))
        for r in sorted(crows, key=lambda r: (-r["added_count"], r["form"])):
            if not r["hits"] and not r["covered"] and not r["flags"]:
                continue  # zero-hit unflagged forms are counted above, not listed
            print("%-14s %-22s %-26s %5d %5d %6d %5d %5d  %s%s%s" % (
                r["security_key"][:14], r["form"][:22], r["company"][:26], r["pairs"], r["new_pairs"],
                r["added_count"], r["title_flips"], r["lead_flips"],
                "COVERED-BY-ALIAS " if r["covered"] else "", ";".join(r["flags"]),
                "  ANOMALY(delta!=added)x%d" % r["anomalies"] if r["anomalies"] else ""))
        grand_forms += gen
        grand_hit_forms += len(with_hits)
        print()
    print("ALL CLASSES: added pairs=%d (NEW pairs=%d) added mention_count=%d title flips=%d lead flips=%d" % (
        sum(r["pairs"] for r in rows), sum(r["new_pairs"] for r in rows), sum(r["added_count"] for r in rows),
        sum(r["title_flips"] for r in rows), sum(r["lead_flips"] for r in rows)))
    sh = [r for r in rows if r["hits"] and any(f.startswith("SHORT") for f in r["flags"])]
    dw = [r for r in rows if r["hits"] and any(f.startswith("DICT") for f in r["flags"])]
    print("forms with added hits that are <=3 characters: %d; that carry a DICT-WORD flag: %d (both counted in the totals above)" % (len(sh), len(dw)))
    print("forms with added hits: %d of %d generated" % (grand_hit_forms, grand_forms))


if __name__ == "__main__":
    main()
