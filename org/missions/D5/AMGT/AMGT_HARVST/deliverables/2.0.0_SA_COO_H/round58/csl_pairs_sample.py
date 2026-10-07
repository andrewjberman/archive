"""Read-only: every pair that rests on the exact-case ticker form `CSL` for CSL_AU_Equity (CSL LTD), for row
AMGT_HARVST-Z-S101 and 1.0.0_SA_CTO~Z msg 31209 term 2.

A pair rests on the form when the served matcher's `_security_mentions` counts a mention with the proposed alias set and none
with `CSL` removed. Each pair prints every span of the form in context, and one MECHANICAL flag: whether the article's text
carries the word `Carlisle`. It draws 10 pairs, `random.Random(60)`, sorted by article key before sampling, and grades nothing.
S3 GET through the served iterator; no put. Run from the repo root: `PYTHONPATH=. python <this file>`."""
import io
import json
import os
import random
import re

from lib.research.harvest import publication_gold as pg

HERE = os.path.dirname(os.path.abspath(__file__))
KEY, FORM = "CSL_AU_Equity", "CSL"


def main():
    proposed = json.load(open(os.path.join(HERE, "securities.universe.signing2.json"), encoding="utf-8"))
    sec = next(s for s in proposed if s["security_key"] == KEY)
    without = dict(sec)
    without["ticker_aliases"] = [f for f in (sec.get("ticker_aliases") or []) if f != FORM]
    pattern = pg._span_pattern([], [FORM])
    carlisle = re.compile(r"\bCarlisle\b")
    rows = []
    count = 0
    for article in pg._iter_latest_articles():
        count += 1
        if pg._security_mentions(article, sec)["mention_count"] < 1:
            continue
        if pg._security_mentions(article, without)["mention_count"] >= 1:
            continue
        texts = [("title", article.get("title") or "")]
        for index, block in enumerate(article.get("text_blocks") or []):
            texts.append(("block %d" % index, block if isinstance(block, str) else (block.get("text") or "")))
        spans = []
        for where, text in texts:
            for match in pattern.finditer(text):
                spans.append({"where": where, "context": text[max(0, match.start() - 160): match.end() + 160]})
        rows.append({"article_key": article.get("article_key"), "publisher": article.get("publisher"),
                     "title": article.get("title"), "url": article.get("url"), "spans": spans,
                     "article_carries_carlisle": any(carlisle.search(t) for _w, t in texts)})
    rows.sort(key=lambda r: r["article_key"] or "")
    with_carlisle = sum(1 for r in rows if r["article_carries_carlisle"])
    print("SECURITY %s aliases=%s exact=%s" % (KEY, json.dumps(sec.get("aliases")), json.dumps(sec.get("ticker_aliases"))))
    print("DENOMINATOR: silver articles %d; pairs resting on the form %s: %d" % (count, FORM, len(rows)))
    print("MECHANICAL FLAG: article text carries the word Carlisle in %d of %d pairs" % (with_carlisle, len(rows)))
    print("BY PUBLISHER: %s" % json.dumps({p: sum(1 for r in rows if r["publisher"] == p)
                                            for p in sorted({r["publisher"] for r in rows})}))
    sample = random.Random(60).sample(rows, min(10, len(rows)))
    for n, r in enumerate(sample, start=1):
        r["n"] = n
        r["verdict"] = None
    about = ("10 pairs that rest on the exact-case form CSL for CSL_AU_Equity (CSL LTD, the Australian company). Per row: does "
             "CSL here name CSL Limited. JUDGMENT, graded by 3.0.0_SA_CVO~Z; 9 of 10 keeps the form, less refuses it "
             "(1.0.0_SA_CTO~Z msg 31209 term 2; row AMGT_HARVST-Z-S101).")
    json.dump({"about": about, "seed": 60, "articles": count, "pairs": len(rows), "pairs_with_carlisle": with_carlisle,
               "all_pairs": rows, "sample": sample},
              open(os.path.join(HERE, "GOLD_REBUILD8_CSL_SAMPLE.json"), "w", encoding="utf-8"), indent=1, default=str)
    lines = ["# Gold rebuild #8 -- the CSL sample for `3.0.0_SA_CVO~Z`", "", about, "",
             "Population: %d pairs over %d silver articles; the article text carries the word Carlisle in %d of them "
             "(a mechanical flag, not a grade)." % (len(rows), count, with_carlisle), "",
             "| n | publisher | title | the form in context | article carries Carlisle | names CSL Limited? |",
             "|---|---|---|---|---|---|"]
    for r in sample:
        ctx = " // ".join("%s: ...%s..." % (s["where"], s["context"].replace("|", "/").replace("\n", " ")) for s in r["spans"][:2])
        lines.append("| %d | %s | %s | %s | %s | |" % (r["n"], r["publisher"], str(r["title"]).replace("|", "/"), ctx,
                                                     "yes" if r["article_carries_carlisle"] else "no"))
    io.open(os.path.join(HERE, "GOLD_REBUILD8_CSL_SAMPLE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("SAMPLE: %d rows; of them carrying Carlisle: %d" % (len(sample), sum(1 for r in sample if r["article_carries_carlisle"])))


if __name__ == "__main__":
    main()
