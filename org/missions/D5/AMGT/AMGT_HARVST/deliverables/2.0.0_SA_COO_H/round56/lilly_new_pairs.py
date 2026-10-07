"""Read-only: list the articles where a bare `Lilly` would be LLY_US_Equity's ONLY mention on the gold plane.

S3 GET through the served iterator; no put, no build. Run from the repo root: `PYTHONPATH=. python <this file>`."""
import json

from lib.research.harvest import publication_gold as pg
from lib.research.harvest import universe_securities as us


def main():
    securities, _summary = us.build()
    sec = next(s for s in securities if s["security_key"] == "LLY_US_Equity")
    aliases, exact = pg._security_aliases(sec), pg._security_exact_aliases(sec)
    base = pg._span_pattern(aliases, exact)
    plus = pg._span_pattern(list(aliases) + ["Lilly"], exact)
    count = 0
    new_pairs = []
    for article in pg._iter_latest_articles():
        count += 1
        texts = [article.get("title") or ""]
        for block in article.get("text_blocks") or []:
            texts.append(block if isinstance(block, str) else (block.get("text") or ""))
        if any(base.search(text) for text in texts):
            continue
        hits = []
        for index, text in enumerate(texts):
            for match in plus.finditer(text):
                hits.append({"where": "title" if index == 0 else "block %d" % (index - 1),
                             "context": text[max(0, match.start() - 160): match.end() + 160]})
        if hits:
            new_pairs.append({"article_key": article.get("article_key"), "publisher": article.get("publisher"),
                              "title": article.get("title"), "url": article.get("url"), "hits": hits})
    print(json.dumps({"articles": count, "aliases": aliases, "exact": exact, "new_pairs": new_pairs},
                     indent=1, ensure_ascii=True))


if __name__ == "__main__":
    main()
