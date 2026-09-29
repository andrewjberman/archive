"""HVST-f-1 CONTROL: the census's added counts equal the SERVED function's own arithmetic.
For every generated form and every article, sum publication_gold._match_counts over the title and the blocks
with aliases and with aliases + [form]; the difference must equal the census's added_count for that pair
(and be 0 where the census reports no added hit). Read-only."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

pg = C.pg


def served_total(article, aliases):
    n = pg._match_counts(article.get("title") or "", aliases)[0]
    for block in article.get("text_blocks") or []:
        n += pg._match_counts(block or "", aliases)[0]
    return n


def main():
    securities = C.load_securities()
    articles = C.load_articles()
    checked = mismatches = with_added = 0
    for cls, form, sec in C.generate_forms(securities):
        aliases = list(pg._security_aliases(sec))
        if C.already_covered(form, aliases):
            continue
        for art in articles:
            r = C.added_for(art, sec, form)
            served_delta = served_total(art, aliases + [form]) - served_total(art, aliases)
            mine = r["added_count"] if r else 0
            checked += 1
            with_added += 1 if r else 0
            if served_delta != mine:
                mismatches += 1
                print("MISMATCH %s %r %s: served delta=%d census=%d" % (art["article_key"], form, sec["security_key"], served_delta, mine))
    print("(form, article) pairs checked=%d; with added hits=%d; mismatches vs publication_gold._match_counts=%d" % (
        checked, with_added, mismatches))
    print("CONTROL " + ("AGREES" if mismatches == 0 else "DISAGREES"))


if __name__ == "__main__":
    main()
