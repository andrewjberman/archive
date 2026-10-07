"""Read-only: the second graded sample ruled by 1.0.0_SA_CTO~Z msg 31173 -- pairs that rest on a NEW exact-case ticker form.

A pair (article, security) rests on the form when the served matcher's own `_security_mentions` counts at least one mention
with the security's proposed alias set, and none with the new ticker form removed. Lists: the served file
`round33/securities.universe.r33.json` and the proposed list this run's dry run saved, `securities.universe.signing2.json`.
S3 GET through the served iterator; no put, no build. Run from the repo root: `PYTHONPATH=. python <this file>`.

Sample: 10 pairs from each of the seven named forms (all where fewer) and 30 across the other forms, `random.Random(59)`,
rows sorted by (security_key, article_key) before sampling. It grades nothing."""
import collections
import io
import json
import os
import random

from lib.research.harvest import publication_gold as pg

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
SEVEN = ("BATS", "JD", "ICT", "ML", "BE", "SAN", "CAT")


def context(article, form):
    texts = [("title", article.get("title") or "")]
    for index, block in enumerate(article.get("text_blocks") or []):
        texts.append(("block %d" % index, block if isinstance(block, str) else (block.get("text") or "")))
    pattern = pg._span_pattern([], [form])
    for where, text in texts:
        match = pattern.search(text)
        if match:
            return where, text[max(0, match.start() - 160): match.end() + 160]
    return None, None


def main():
    served = {s["security_key"]: s for s in json.load(open(os.path.join(PARENT, "round33", "securities.universe.r33.json"),
                                                           encoding="utf-8"))}
    proposed = json.load(open(os.path.join(HERE, "securities.universe.signing2.json"), encoding="utf-8"))
    targets = []
    for sec in proposed:
        fresh = [f for f in (sec.get("ticker_aliases") or [])
                 if f not in ((served.get(sec["security_key"]) or {}).get("ticker_aliases") or [])]
        if fresh:
            without = dict(sec)
            without["ticker_aliases"] = [f for f in (sec.get("ticker_aliases") or []) if f not in fresh]
            targets.append((sec, without, fresh[0]))
    print("SECURITIES WITH A NEW TICKER FORM: %d" % len(targets))
    rows = []
    count = 0
    for article in pg._iter_latest_articles():
        count += 1
        for sec, without, form in targets:
            if pg._security_mentions(article, sec)["mention_count"] < 1:
                continue
            if pg._security_mentions(article, without)["mention_count"] >= 1:
                continue
            where, text = context(article, form)
            rows.append({"security_key": sec["security_key"], "company": sec.get("company"), "form": form,
                         "article_key": article.get("article_key"), "publisher": article.get("publisher"),
                         "title": article.get("title"), "url": article.get("url"), "where": where, "context": text})
    by_form = collections.Counter(r["form"] for r in rows)
    print("DENOMINATOR: silver articles %d; pairs resting on a new ticker form %d over %d securities" % (
        count, len(rows), len({r["security_key"] for r in rows})))
    print("BY FORM: %s" % dict(by_form.most_common()))
    rows.sort(key=lambda r: (r["security_key"], r["article_key"] or ""))
    rng = random.Random(59)
    sample = []
    for form in SEVEN:
        pool = [r for r in rows if r["form"] == form]
        for r in rng.sample(pool, min(10, len(pool))):
            sample.append(dict(r, group="seven:" + form))
    rest = [r for r in rows if r["form"] not in SEVEN]
    for r in rng.sample(rest, min(30, len(rest))):
        sample.append(dict(r, group="other"))
    for n, r in enumerate(sample, start=1):
        r["n"] = n
        r["verdict"] = None
    groups = collections.Counter(r["group"] for r in sample)
    print("SAMPLE: %d rows; %s" % (len(sample), dict(groups)))
    about = ("Pairs that rest on a NEW exact-case ticker form. Per row: does the form in this article name that company. "
             "JUDGMENT, graded by 3.0.0_SA_CVO~Z (1.0.0_SA_CTO~Z msg 31173). Each of the seven named forms: 9 of 10 or better "
             "keeps it, anything less puts it in ticker_refusals. The other forms together: bar 29 of 30, and a miss names "
             "its form for the same test.")
    json.dump({"about": about, "seed": 59, "articles": count, "pairs": len(rows), "by_form": dict(by_form),
               "sample_groups": dict(groups), "sample": sample},
              open(os.path.join(HERE, "GOLD_REBUILD8_FORM_SAMPLE.json"), "w", encoding="utf-8"), indent=1, default=str)
    lines = ["# Gold rebuild #8 -- the ticker-form sample for `3.0.0_SA_CVO~Z`", "", about, "",
             "Population: %d pairs over %d silver articles. By form: %s" % (len(rows), count, dict(by_form.most_common())), "",
             "| n | group | form | security | publisher | title | the form in context | names the company? |",
             "|---|---|---|---|---|---|---|---|"]
    for r in sample:
        ctx = (r["context"] or "").replace("|", "/").replace("\n", " ")
        lines.append("| %d | %s | %s | %s (%s) | %s | %s | %s: ...%s... | |" % (
            r["n"], r["group"], r["form"], r["security_key"], r["company"], r["publisher"],
            str(r["title"]).replace("|", "/"), r["where"], ctx))
    io.open(os.path.join(HERE, "GOLD_REBUILD8_FORM_SAMPLE.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    print("PUTS SENT 0 (no client write is called by this script)")


if __name__ == "__main__":
    main()
