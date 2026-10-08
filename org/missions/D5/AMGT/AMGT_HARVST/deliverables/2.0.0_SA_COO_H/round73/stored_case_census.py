"""AMGT_HARVST round 73 -- THE CENSUS `1.0.0_SA_CTO~Z` R27 (msg 31867) asks for before R26(b) is ruled (issuer; NO WRITE).

Over the served gold rebuild #9 built (the rows the diagnostic dump kept, `.runtime/harvest-backfill/r72_dump/
served_mention.json`, 48,358 pairs) and the list it was served from (`round64/securities.universe.r64.json`): which pairs a
STORED-CASE alias rule would remove, by security. The rule tested: a security's aliases match only in their stored case
(as its ticker forms already do), instead of case-insensitively. A pair is REMOVED when, under that rule, the security's
mention count in the article falls to 0. Silver is read (S3 GET only); nothing is written anywhere but this folder.
"""
import collections
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *[".."] * 8))
sys.path.insert(0, ROOT)

from lib.research.harvest import publication_gold as pg  # noqa: E402

LIST = os.path.join(HERE, "..", "round64", "securities.universe.r64.json")
DUMP = os.path.join(ROOT, ".runtime", "harvest-backfill", "r72_dump", "served_mention.json")
OUT = os.path.join(HERE, "stored_case_census.json")


def stored_case(security):
    """The same security, its aliases moved into the exact-case forms."""
    return dict(security, aliases=[], ticker_aliases=list(security.get("aliases") or []) + list(security.get("ticker_aliases") or []),
                company=None)


def main():
    securities = {s["security_key"]: s for s in json.load(open(LIST, encoding="utf-8"))}
    served = json.load(open(DUMP, encoding="utf-8"))
    pairs = collections.defaultdict(list)
    for row in served:
        pairs[row["article_key"]].append(row["security_key"])
    print("SERVED PAIRS %d over %d articles; securities in the list %d" % (len(served), len(pairs), len(securities)))
    sys.stdout.flush()
    seen, removed, kept, no_aliases, no_article = 0, [], 0, 0, 0
    found = set()
    for article in pg._iter_latest_articles():
        key = article.get("article_key")
        if key not in pairs:
            continue
        found.add(key)
        for sk in pairs[key]:
            sec = securities.get(sk)
            if sec is None:
                continue
            if not sec.get("aliases"):
                no_aliases += 1
                continue
            seen += 1
            before = pg._security_mentions(article, sec).get("mention_count") or 0
            after = pg._security_mentions(article, stored_case(sec)).get("mention_count") or 0
            if before and not after:
                removed.append({"article_key": key, "security_key": sk, "title": article.get("title") or "",
                                "aliases": sec.get("aliases")})
            else:
                kept += 1
    no_article = len(set(pairs) - found)
    by_sec = collections.Counter(r["security_key"] for r in removed)
    result = {"served_pairs": len(served), "pairs_tested": seen, "pairs_on_a_security_with_no_aliases": no_aliases,
              "articles_not_found_in_silver": no_article, "removed": len(removed), "kept": kept,
              "removed_by_security": dict(by_sec.most_common()), "removed_rows": removed}
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, indent=1, ensure_ascii=True)
    print("TESTED %d pairs on securities with aliases (%d on securities with none, not affected); articles not found in "
          "silver %d" % (seen, no_aliases, no_article))
    print("A STORED-CASE ALIAS RULE REMOVES %d of %d tested pairs, over %d securities" % (len(removed), seen, len(by_sec)))
    for sk, n in by_sec.most_common(40):
        aliases = securities[sk].get("aliases")
        sample = [r["title"][:90].encode("ascii", "replace").decode("ascii") for r in removed if r["security_key"] == sk][:2]
        print("  %-20s %5d  aliases %s  e.g. %s" % (sk, n, aliases, sample))
    return 0


if __name__ == "__main__":
    sys.exit(main())
