"""HVST-bb-1: what the GOLD text matcher would ADD if the slug-plane brands Meta and Lilly were
aliases there. Dry run; read-only (S3 GET only); imports the served matcher, re-implements none."""
import collections
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

BRANDS = [("META_US_Equity", "Meta"), ("LLY_US_Equity", "Lilly")]
LEAD = 3


def asc(t):
    return t.encode("ascii", "backslashreplace").decode("ascii")


def spans(text, aliases, exact):
    pat = pg._span_pattern(aliases, exact)
    if pat is None or not text:
        return []
    return [(m.start(), m.end(), m.group(0)) for m in pat.finditer(text)]


def texts_of(article):
    out = [("title", article.get("title") or "")]
    for i, b in enumerate(article.get("text_blocks") or []):
        out.append(("block %d" % i, b or ""))
    return out


def added_for(article, aliases, exact, form):
    combined = aliases + [form]
    hits = []
    base_total = 0
    bt = bl = ct = cl = False
    for idx, (where, text) in enumerate(texts_of(article)):
        b = spans(text, aliases, exact)
        c = spans(text, combined, exact)
        base_total += len(b)
        if b:
            if where == "title":
                bt = True
            elif idx - 1 < LEAD:
                bl = True
        if c:
            if where == "title":
                ct = True
            elif idx - 1 < LEAD:
                cl = True
        bset = {(s, e) for s, e, _ in b}
        for s, e, m in c:
            if (s, e) not in bset:
                hits.append({"where": where, "position": s, "end": e, "matched": m,
                             "context": asc(text[max(0, s - 200):e + 200])})
    return {"hits": hits, "base_count": base_total, "title_flip": ct and not bt, "lead_flip": cl and not bl}


def main():
    fails = []
    securities, summary = us.build()
    src = (summary.get("universe") or {}).get("source")
    fb = (summary.get("universe") or {}).get("fallback_reason")
    by_key = {}
    for s in securities:
        by_key.setdefault(s["security_key"], s)
    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N, S = len(articles), len(securities)
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("DENOMINATOR: securities %d (source %s), silver articles %d" % (S, src, N))
    if N == 0 or S == 0:
        fails.append("N or S is 0")
    results = {}
    for key, brand in BRANDS:
        sec = by_key.get(key)
        if sec is None:
            fails.append("%s not in securities" % key)
            continue
        aliases = pg._security_aliases(sec)
        exact = pg._security_exact_aliases(sec)
        print("BASELINE %s aliases=%s exact=%s" % (key, asc(json.dumps(aliases)), asc(json.dumps(exact))))
        if any(brand.casefold() == a.casefold() for a in aliases):
            fails.append("%s already in baseline of %s" % (brand, key))
        a_with = new_pairs = added = tf = lf = 0
        pubs = collections.Counter()
        rows = []
        for i, art in enumerate(articles, 1):
            if i % 500 == 0:
                print("progress %d/%d" % (i, N), flush=True)
            r = added_for(art, aliases, exact, brand)
            if not r["hits"]:
                continue
            a_with += 1
            new = r["base_count"] == 0
            new_pairs += int(new)
            added += len(r["hits"])
            tf += int(r["title_flip"])
            lf += int(r["lead_flip"])
            pub = pg._row_publisher(art)
            pubs[pub] += 1
            try:
                url = pg.article_url(art)
            except Exception:  # noqa: BLE001
                url = None
            for h in r["hits"]:
                rows.append({"brand": brand, "security_key": key, "article_key": art["article_key"],
                             "publisher": pub, "title": asc(art.get("title") or ""),
                             "url": url, "where": h["where"], "position": h["position"],
                             "context": h["context"], "new_pair": new, "verdict": None})
        print("%s %s: articles_with_added %d of %d articles; NEW pairs %d (the security had 0 mentions in the "
              "article under the served aliases); added mention_count %d; title flips %d; lead flips %d"
              % (key, brand, a_with, N, new_pairs, added, tf, lf))
        print("PUBLISHER SPLIT %s %s: %s" % (key, brand, json.dumps(dict(sorted(pubs.items(), key=lambda p: str(p[0]))))))
        form = aliases[0]
        cn = sum(len(added_for(art, aliases, exact, form)["hits"]) for art in articles)
        print("CONTROL %s: %s adds %d" % (key, form, cn))
        if cn != 0:
            fails.append("CONTROL %s adds %d" % (key, cn))
        rows.sort(key=lambda r: (r["article_key"], r["position"]))
        samp = rows if len(rows) <= 30 else random.Random(55).sample(rows, 30)
        results[brand] = (rows, samp)
    rng = random.Random(55)
    pick = rng.sample(articles, min(20, N)) if N else []
    agree = n = 0
    for art in pick:
        for key, _b in BRANDS:
            sec = by_key.get(key)
            if sec is None:
                continue
            mine = sum(len(spans(t, pg._security_aliases(sec), pg._security_exact_aliases(sec)))
                       for _w, t in texts_of(art))
            served = pg._security_mentions(art, sec)["mention_count"]
            n += 1
            agree += int(mine == served)
    print("AGREEMENT: %d of %d" % (agree, n))
    if agree != n or n == 0:
        fails.append("AGREEMENT %d of %d" % (agree, n))
    out = []
    for brand, (rows, samp) in results.items():
        if len(samp) != min(30, len(rows)):
            fails.append("sample size %s" % brand)
        print("SAMPLE %s: %d of %d added rows; new_pair rows in sample %d" % (
            brand, len(samp), len(rows), sum(1 for r in samp if r["new_pair"])))
        for k, r in enumerate(samp, 1):
            row = {"n": k}
            row.update(r)
            out.append(row)
    with open(os.path.join(HERE, "GOLD_PLANE_CENSUS_SAMPLE.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    with open(os.path.join(HERE, "GOLD_PLANE_CENSUS_SAMPLE.md"), "w", encoding="utf-8") as fh:
        for brand in results:
            fh.write("## %s\n\nDoes this word name the company? (verdict column empty)\n\n" % brand)
            fh.write("| n | publisher | title | span in context | new_pair | verdict |\n|---|---|---|---|---|---|\n")
            for r in out:
                if r["brand"] == brand:
                    ctx = r["context"].replace("|", "\\|").replace("\n", " ")
                    fh.write("| %d | %s | %s | %s (%s) | %s | |\n" % (
                        r["n"], r["publisher"], r["title"].replace("|", "\\|"), ctx, r["where"], r["new_pair"]))
            fh.write("\n")
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
