"""HVST-bh-10: what the GOLD securities list loses when HEICO's bare ticker form `HEI` (also how Hawaiian Electric
Industries, outside coverage, is written) counts only beside a SECOND ANCHOR. Read-only (S3 GET only); imports the served
matcher and the real universe_securities; re-implements no matcher.

BEFORE = `universe_securities.build(rule_path=<the shipped rule file with the HEI_US_Equity `ticker_anchors` entry removed
         and every other entry kept>)` -- the HEI entry switched off by DATA (a temp copy of the rule file, written under
         the OS temp dir, deleted after the build).
AFTER  = `universe_securities.build()` as it stands.
Counts come from the REAL `pg._security_mentions` over every latest silver article (`pg._iter_latest_articles()`).
The 3 graded pairs are rows 3 to 5 of BH2_NINE_FORMS (HEICO 2, Hawaiian Electric 1), grade
org/tier1_exec/3.0.0_SA_CVO/deliverables/AMGT_HARVST_ROUND61_FALLBACK_AND_NINE_FORMS_GRADE_20261008.md @31fbcebb42."""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

KEY, FORM = "HEI_US_Equity", "HEI"
HEICO_PAIRS = ["sa:3584086", "sa:3685322"]      # 2 HEICO in aerospace ticker lists
HAWAIIAN_PAIRS = ["sa:4412260"]                  # 1 Hawaiian Electric ("The utility's dividend to HEI remains suspended")
# what could identify HEICO in an article that carries only the bare form (case-insensitive substring read)
IDENTIFIERS = ["heico", "hei.a", "hei-a", "hei/a", "wencor", "flight support", "electronic technologies",
               "mendelson", "hawaiian electric"]


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


def identifiers(article):
    """Which identifying strings the whole article carries (case-insensitive), with the count of occurrences."""
    blob = "\n".join(text for _w, text in texts(article)).lower()
    return {token: blob.count(token) for token in IDENTIFIERS if token in blob}


def main():
    fails = []
    with open(us.WHOLE_BRAND_PATH, "r", encoding="utf-8") as handle:
        rule = json.load(handle)
    entries = rule.get("ticker_anchors", [])
    off = dict(rule)
    off["ticker_anchors"] = [e for e in entries if e.get("security_key") != KEY]
    handle = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    try:
        json.dump(off, handle)
        handle.close()
        before_secs, _before_sum = us.build(rule_path=handle.name)
    finally:
        os.unlink(handle.name)
    after_secs, after_sum = us.build()
    nosym = dict(rule)
    nosym["ticker_anchors"] = [({k: v for k, v in e.items() if k != "symbol_anchors"} if e.get("security_key") == KEY else e)
                               for e in entries]
    handle2 = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    try:
        json.dump(nosym, handle2)
        handle2.close()
        nosym_secs, _nosym_sum = us.build(rule_path=handle2.name)
    finally:
        os.unlink(handle2.name)
    nosym_hei = next(s for s in nosym_secs if s["security_key"] == KEY)
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    src = (after_sum.get("universe") or {}).get("source")
    fb = (after_sum.get("universe") or {}).get("fallback_reason")
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("BEFORE: build() with the %s ticker_anchors entry removed from the rule file; AFTER: build(); NO-SYMBOL: build() with the %s symbol_anchors removed" % (KEY, KEY))
    print("HEI ENTRIES IN THE RULE FILE: %d" % sum(1 for e in entries if e.get("security_key") == KEY))
    print("SYMBOL ANCHORS: %s" % json.dumps(after[KEY].get("ticker_anchor_symbols")))
    print("ANCHORS: %s" % json.dumps(after[KEY].get("ticker_anchor_aliases")))
    if set(before) != set(after) or len(before_secs) != S:
        fails.append("before/after security sets differ (%d vs %d)" % (len(before_secs), S))
    if KEY not in after or after[KEY].get("anchor_required_ticker_aliases") != [FORM]:
        fails.append("%s does not carry the anchor-required form" % KEY)
    if "anchor_required_ticker_aliases" in before.get(KEY, {}):
        fails.append("BEFORE still carries the anchor-required form")

    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    print("DENOMINATOR: securities %d, silver articles %d, graded pairs 3 (HEICO 2, Hawaiian Electric 1)" % (S, N))
    if N == 0:
        fails.append("N is 0 (silver read returned no articles)")

    p0 = p1 = 0
    dropped, gained, depend = [], [], []
    by_key = {}
    for i, art in enumerate(articles, 1):
        if i % 2000 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        b = pg._security_mentions(art, before[KEY])["mention_count"]
        a = pg._security_mentions(art, after[KEY])["mention_count"]
        by_key[art["article_key"]] = (b, a)
        p0 += 1 if b else 0
        p1 += 1 if a else 0
        if a and not pg._security_mentions(art, nosym_hei)["mention_count"]:
            depend.append(art)
        if b and not a:
            dropped.append(art)
        if a and not b:
            gained.append(art)
    print("%s: pairs before %d after %d; dropped %d" % (KEY, p0, p1, len(dropped)))
    for art in dropped:
        print(asc("  dropped %s | %s" % (art["article_key"], art.get("title"))))
        for line in spans(art):
            print(asc("      HEI span " + line))
    if gained:
        fails.append("%d pairs GAINED on %s" % (len(gained), KEY))
        for art in gained:
            print(asc("  GAINED %s" % art["article_key"]))

    print("PAIRS THAT DEPEND ON A SYMBOL ANCHOR (kept only because of it): %d" % len(depend))
    for art in depend:
        print(asc("  %s | %s" % (art["article_key"], art.get("title"))))
    dropped_keys = {art["article_key"] for art in dropped}
    present = {art["article_key"] for art in articles}
    g = sum(1 for k in HEICO_PAIRS if by_key.get(k, (0, 0))[1])
    h = sum(1 for k in HAWAIIAN_PAIRS if k in dropped_keys)
    print("GRADED HEICO PAIRS KEPT: %d of %d" % (g, len(HEICO_PAIRS)))
    print("GRADED HAWAIIAN ELECTRIC PAIRS DROPPED: %d of %d" % (h, len(HAWAIIAN_PAIRS)))
    missing = [k for k in HEICO_PAIRS + HAWAIIAN_PAIRS if k not in present]
    if missing:
        print("GRADED PAIRS NOT IN THE SILVER READ: %s" % missing)
    lost = [art for art in dropped if art["article_key"] in set(HEICO_PAIRS)]
    if lost:
        print("LOST HEICO PAIRS (%d), each with its HEI text in context and what in the article identifies HEICO:" % len(lost))
        for art in lost:
            print(asc("  %s | %s" % (art["article_key"], art.get("title"))))
            for line in spans(art):
                print(asc("      HEI span " + line))
            print(asc("      identifying strings in the whole article (case-insensitive, count): %s"
                      % (json.dumps(identifiers(art)) if identifiers(art) else "NONE of %s" % IDENTIFIERS)))
            print(asc("      title: %s" % art.get("title")))

    graded_keys = set(HEICO_PAIRS) | set(HAWAIIAN_PAIRS)
    ungraded = [art for art in dropped if art["article_key"] not in graded_keys]
    print("UNGRADED PAIRS DROPPED: %d" % len(ungraded))
    for art in ungraded:
        print(asc("  %s | %s" % (art["article_key"], art.get("title"))))
        for line in spans(art):
            print(asc("      HEI span " + line))

    others = sorted(key for key in after if before.get(key) != after[key] and key != KEY)
    print("OTHER SECURITIES CHANGED: %d of %d" % (len(others), S))
    for key in others:
        print(asc("  changed: %s" % key))
    if others:
        fails.append("OTHER SECURITIES CHANGED is %d" % len(others))
    if g != 2:
        fails.append("GRADED HEICO PAIRS KEPT is %d of 2" % g)
    if h != 1:
        fails.append("GRADED HAWAIIAN ELECTRIC PAIRS DROPPED is %d of 1" % h)
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
