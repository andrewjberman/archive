"""HVST-g-1 control: can the census see the case rule? MUTANT = the new securities file with every ticker form moved
into the ordinary (case-insensitive) alias list, i.e. the pre-round-18 way of admitting a ticker. Over the 120 silver
articles the REAL rule must find no lower-case ticker hit and the MUTANT must find some (COST's lower-case 'cost',
'now' for NOW, 'fix' for FIX), so a zero for the real rule is a measurement and not a blind reader.
S3 GET/LIST only (silver articles): no put, no delete, no vendor call."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402


def lower_hits(articles, sec, aliases, exact):
    """Spans of `sec` whose matched text is not the ticker's exact form and equals its own lower case."""
    n = 0
    for art in articles:
        for _where, text in C.texts_of(art):
            for _s, _e, m, label, kind in C.spans_with_forms(text, aliases, exact):
                if m.lower() == m and m.upper() in {t.upper() for t in sec.get("ticker_aliases") or []}:
                    n += 1
    return n


def main():
    articles = sorted(pg._iter_latest_articles(), key=lambda r: r["article_key"])
    securities = C.load_json(C.NEW_PATH)
    real = mutant = 0
    per = {}
    for sec in securities:
        if not sec.get("ticker_aliases"):
            continue
        r = lower_hits(articles, sec, pg._security_aliases(sec), pg._security_exact_aliases(sec))
        m = lower_hits(articles, sec, pg._security_aliases(sec) + list(sec["ticker_aliases"]), [])
        real += r
        mutant += m
        if r or m:
            per[sec["security_key"]] = (r, m)
    print("securities with a ticker form: %d of %d; silver articles=%d" % (
        sum(1 for s in securities if s.get("ticker_aliases")), len(securities), len(articles)))
    for k, (r, m) in sorted(per.items(), key=lambda kv: -kv[1][1]):
        print("  %-16s lower-case ticker hits: real rule=%d  mutant (case-insensitive)=%d" % (k, r, m))
    print("TOTAL lower-case ticker hits: real rule=%d; mutant=%d" % (real, mutant))
    ok = real == 0 and mutant > 0
    print("MUTANT %s" % ("KILLED (the reader can see lower-case hits; the real rule has none)" if ok else "SURVIVED -- CONTROL FAILS"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
