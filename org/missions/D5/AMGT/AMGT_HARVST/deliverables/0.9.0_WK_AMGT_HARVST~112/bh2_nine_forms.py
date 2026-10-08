"""Read-only census: every pair resting on one of nine exact-case ticker forms. Grades nothing. S3 GET only.
Run from repo root: PYTHONPATH=. python <this file>"""
import io
import json
import os

from lib.research.harvest import publication_gold as pg

HERE = os.path.dirname(os.path.abspath(__file__))
LIST = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round60/securities.universe.r60.json"
DRY = [("BNP", 5), ("HEI", 3), ("SNPS", 3), ("DG", 2), ("ED", 2), ("GPN", 2), ("ADBE", 1), ("NKE", 1), ("SHOP", 1)]


def main():
    secs = json.load(open(LIST, encoding="utf-8"))
    targets = []  # (form, sec, without, pattern, dry)
    carriers = {}
    for form, dry in DRY:
        found = [s for s in secs if form in (s.get("ticker_aliases") or [])]
        carriers[form] = found
        print("FORM %s carried by: %s" % (form, ", ".join(s["security_key"] for s in found) or "NO SECURITY CARRIES THIS FORM"))
        for s in found:
            w = dict(s)
            w["ticker_aliases"] = [f for f in s["ticker_aliases"] if f != form]
            targets.append((form, s, w, pg._span_pattern([], [form]), dry))
    k = len({s["security_key"] for t in targets for s in [t[1]]})
    rows = {}
    n = 0
    for article in pg._iter_latest_articles():
        n += 1
        if n % 500 == 0:
            print("progress: %d articles" % n, flush=True)
        cache = {}
        texts = None
        for form, sec, w, pat, _d in targets:
            key = sec["security_key"]
            if key not in cache:
                cache[key] = pg._security_mentions(article, sec)["mention_count"]
            if cache[key] < 1 or pg._security_mentions(article, w)["mention_count"] >= 1:
                continue
            if texts is None:
                texts = [("title", article.get("title") or "")]
                for i, b in enumerate(article.get("text_blocks") or []):
                    texts.append(("block %d" % i, b if isinstance(b, str) else (b.get("text") or "")))
            spans = []
            for where, text in texts:
                for m in pat.finditer(text):
                    spans.append({"where": where, "context": text[max(0, m.start() - 120): m.end() + 120]})
            rows.setdefault((form, key), []).append({
                "form": form, "security_key": key, "company": sec.get("company"),
                "article_key": article.get("article_key"), "publisher": article.get("publisher"),
                "title": article.get("title"), "url": article.get("url"), "spans": spans})
    print("DENOMINATOR: forms %d, securities carrying one %d, silver articles %d" % (len(DRY), k, n))
    allrows = []
    for form, dry in DRY:
        for s in carriers[form]:
            r = sorted(rows.get((form, s["security_key"]), []), key=lambda x: x["article_key"] or "")
            print("%s %s: pairs resting on the form %d (dry run 3: %d)" % (form, s["security_key"], len(r), dry))
            allrows.extend(r)
    for i, r in enumerate(allrows, start=1):
        r["row"] = i
    T = len(allrows)
    print("TOTAL: %d pairs" % T)
    json.dump({"articles": n, "pairs": T, "rows": allrows}, open(os.path.join(HERE, "BH2_NINE_FORMS.json"), "w", encoding="utf-8"), indent=1, default=str)
    counts = {}
    for r in allrows:
        counts[(r["form"], r["security_key"])] = counts.get((r["form"], r["security_key"]), 0) + 1
    L = ["# BH2 nine unreached ticker forms", "",
         "Population: every pair (article, security) over %d silver articles that rests on one of nine exact-case ticker forms "
         "no reviewer read, %d pairs in all, none sampled. A pair rests on a form when pg._security_mentions counts at least one "
         "mention with the security as listed in the r60 universe file and none with that form removed from its ticker_aliases. "
         "Counts: %s. Question per row: does <FORM> here name <company>. No verdict, no grade." % (
             n, T, "; ".join("%s %s %d" % (f, k_, c) for (f, k_), c in counts.items())), "",
         "| row | form | security | company | publisher | title | url | spans |", "|---|---|---|---|---|---|---|---|"]
    for r in allrows:
        sp = " // ".join("%s: ...%s..." % (s["where"], s["context"].replace("|", "/").replace("\n", " ")) for s in r["spans"])
        L.append("| %d | %s | %s | %s | %s | %s | %s | %s |" % (r["row"], r["form"], r["security_key"], r["company"], r["publisher"],
                 str(r["title"]).replace("|", "/"), r["url"], sp))
    io.open(os.path.join(HERE, "BH2_NINE_FORMS.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    fails = []
    if n <= 0:
        fails.append("N is 0")
    for f, _d in DRY:
        if not carriers[f]:
            fails.append("form %s carried by no security" % f)
    if T < 20:
        fails.append("T %d below 20; forms fallen: %s" % (T, [f for f, d in DRY if sum(c for (ff, _), c in counts.items() if ff == f) < d]))
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
