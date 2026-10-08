"""HVST-bh-3: what the GOLD securities list loses when a bare ticker form shared with a company outside coverage counts
only beside a SECOND ANCHOR (CSL_AU_Equity's `CSL`, also Carlisle Companies' NYSE ticker). Read-only (S3 GET only);
imports the served matcher and the real universe_securities; re-implements no matcher.

BEFORE = `universe_securities.build(rule_path=<the shipped rule file with `ticker_anchors` removed>)` -- the list switched
         off by DATA (a temp copy of the rule file, written under the OS temp dir, deleted after the build).
AFTER  = `universe_securities.build()` as it stands.
Counts come from the REAL `pg._security_mentions` over every latest silver article (`pg._iter_latest_articles()`).
The 42 graded pairs are `all_pairs` of GOLD_REBUILD8_CSL_SAMPLE.json (39 good, 3 with `article_carries_carlisle`)."""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

KEY, FORM = "CSL_AU_Equity", "CSL"
SAMPLE = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables", "2.0.0_SA_COO_H",
                      "round58", "GOLD_REBUILD8_CSL_SAMPLE.json")


def asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def texts(article):
    out = [("title", article.get("title") or "")]
    for index, block in enumerate(article.get("text_blocks") or []):
        out.append(("block %d" % index, block if isinstance(block, str) else (block.get("text") or "")))
    return out


def spans(article, width=110):
    """Every exact-case span of the form in context, as 'where: ...context...'."""
    pattern = pg._span_pattern([], [FORM])
    found = []
    for where, text in texts(article):
        for match in pattern.finditer(text):
            lo, hi = max(0, match.start() - width), min(len(text), match.end() + width)
            found.append("%s: ...%s..." % (where, " ".join(text[lo:hi].split())))
    return found


def main():
    fails = []
    rule_path = us.WHOLE_BRAND_PATH
    with open(rule_path, "r", encoding="utf-8") as handle:
        rule = json.load(handle)
    entries = rule.get("ticker_anchors", [])
    off = dict(rule)
    off.pop("ticker_anchors", None)
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    try:
        json.dump(off, handle)
        handle.close()
        before_secs, before_sum = us.build(rule_path=handle.name)
    finally:
        os.unlink(handle.name)
    after_secs, after_sum = us.build()
    nosym = dict(rule)
    nosym["ticker_anchors"] = [{k: v for k, v in e.items() if k != "symbol_anchors"} for e in entries]
    handle2 = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    try:
        json.dump(nosym, handle2)
        handle2.close()
        nosym_secs, _nosym_sum = us.build(rule_path=handle2.name)
    finally:
        os.unlink(handle2.name)
    nosym_csl = next(s for s in nosym_secs if s["security_key"] == KEY)
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    src = (after_sum.get("universe") or {}).get("source")
    fb = (after_sum.get("universe") or {}).get("fallback_reason")
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("BEFORE: build() with ticker_anchors removed from the rule file; AFTER: build(); NO-SYMBOL: build() with each entry's symbol_anchors removed")
    print("SYMBOL ANCHORS: %s" % json.dumps(after[KEY].get("ticker_anchor_symbols")))
    print("ANCHORS: %s" % json.dumps(after[KEY].get("ticker_anchor_aliases")))
    if set(before) != set(after) or len(before_secs) != S:
        fails.append("before/after security sets differ (%d vs %d)" % (len(before_secs), S))
    if KEY not in after or after[KEY].get("anchor_required_ticker_aliases") != [FORM]:
        fails.append("%s does not carry the anchor-required form" % KEY)

    graded = json.load(open(SAMPLE, encoding="utf-8"))["all_pairs"]
    good_keys = [p["article_key"] for p in graded if not p["article_carries_carlisle"]]
    carlisle_keys = [p["article_key"] for p in graded if p["article_carries_carlisle"]]

    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    print("DENOMINATOR: securities %d, silver articles %d, graded pairs %d (good %d, Carlisle %d)"
          % (S, N, len(graded), len(good_keys), len(carlisle_keys)))
    if N == 0:
        fails.append("N is 0 (silver read returned no articles)")
    if (len(good_keys), len(carlisle_keys)) != (39, 3):
        fails.append("graded set is %d good / %d Carlisle, not 39 / 3" % (len(good_keys), len(carlisle_keys)))

    p0 = p1 = 0
    dropped, gained, recovered = [], [], []
    by_key = {}
    for i, art in enumerate(articles, 1):
        if i % 2000 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        b = pg._security_mentions(art, before[KEY])["mention_count"]
        a = pg._security_mentions(art, after[KEY])["mention_count"]
        by_key[art["article_key"]] = (b, a)
        p0 += 1 if b else 0
        p1 += 1 if a else 0
        if a and not pg._security_mentions(art, nosym_csl)["mention_count"]:
            recovered.append(art)
        if b and not a:
            dropped.append(art)
        if a and not b:
            gained.append(art)
    print("%s: pairs before %d after %d; dropped %d" % (KEY, p0, p1, len(dropped)))
    for art in dropped:
        print(asc("  dropped %s | %s" % (art["article_key"], art.get("title"))))
        for line in spans(art):
            print(asc("      " + line))
    if gained:
        fails.append("%d pairs GAINED on %s" % (len(gained), KEY))
        for art in gained:
            print(asc("  GAINED %s" % art["article_key"]))

    print("RECOVERED BY A SYMBOL ANCHOR: %d" % len(recovered))
    for art in recovered:
        print(asc("  %s | %s" % (art["article_key"], art.get("title"))))
        for line in spans(art):
            print(asc("      " + line))

    dropped_keys = {art["article_key"] for art in dropped}
    present = {art["article_key"] for art in articles}
    g = sum(1 for k in good_keys if by_key.get(k, (0, 0))[1])
    c = sum(1 for k in carlisle_keys if k in dropped_keys)
    print("GRADED GOOD PAIRS KEPT: %d of %d" % (g, len(good_keys)))
    print("GRADED CARLISLE PAIRS DROPPED: %d of %d" % (c, len(carlisle_keys)))
    missing = [k for k in good_keys + carlisle_keys if k not in present]
    if missing:
        print("GRADED PAIRS NOT IN THE SILVER READ: %s" % missing)
    lost_good = [art for art in dropped if art["article_key"] in set(good_keys)]
    if lost_good:
        print("GOOD PAIRS WITH NO ANCHOR (%d), each with its CSL text in context:" % len(lost_good))
        for art in lost_good:
            print(asc("  %s | %s" % (art["article_key"], art.get("title"))))
            for line in spans(art):
                print(asc("      " + line))

    graded_keys = set(good_keys) | set(carlisle_keys)
    ungraded = [art for art in dropped if art["article_key"] not in graded_keys]
    print("UNGRADED PAIRS DROPPED: %d" % len(ungraded))
    for art in ungraded:
        print(asc("  %s | %s" % (art["article_key"], art.get("title"))))
        for line in spans(art):
            print(asc("      " + line))

    other_entries = [e for e in entries if e.get("security_key") != KEY]
    others = sorted(key for key in after if before.get(key) != after[key] and key != KEY)
    print("OTHER COVERED FORMS UNDER THE RULE: %d" % len(other_entries))
    print("OTHER SECURITIES CHANGED: %d of %d" % (len(others), S))
    for key in others:
        print(asc("  changed: %s" % key))
    if others:
        fails.append("OTHER SECURITIES CHANGED is %d" % len(others))
    if g != 39:
        fails.append("GRADED GOOD PAIRS KEPT is %d of 39" % g)
    if c != 3:
        fails.append("GRADED CARLISLE PAIRS DROPPED is %d of 3" % c)
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
