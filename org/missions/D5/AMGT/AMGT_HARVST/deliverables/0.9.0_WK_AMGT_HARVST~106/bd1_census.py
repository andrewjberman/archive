"""HVST-bd-1: what the GOLD matcher gains when `Meta` is a gold brand and a bare `Lilly` is an ANCHORED gold brand.
Dry run; read-only (S3 GET only through the served iterator); counts come from the REAL
`publication_gold._security_mentions`, never a re-implemented matcher.
BEFORE = the list as merged with the two `gold` objects ignored (a rule copy with them removed);
AFTER  = `universe_securities.build()` as it stands."""
import collections
import copy
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
MUST_DROP = ["wsj:510e7738-752c-4376-889b-7f0d60761963", "barrons:WP-BAR-0001937680"]
SEED = 57
BARE_LILLY = pg._alias_pattern("Lilly")


def asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def texts_of(article):
    return [(article.get("title") or "", "title")] + [(b or "", "block %d" % i)
                                                      for i, b in enumerate(article.get("text_blocks") or [])]


def context(text, match, width=70):
    lo, hi = max(0, match.start() - width), min(len(text), match.end() + width)
    return text[lo:hi].replace("\n", " ")


def main():
    fails = []
    document, provenance = us._read_universe()
    rule_after = us.load_alias_rule()
    rule_before = copy.deepcopy(rule_after)
    for entry in rule_before["whole_brands"]:
        entry.pop("gold", None)
    legal_names, legal_info = us.load_legal_names()
    before_secs, before_sum = us.securities_from_universe(document, rule=rule_before, legal_names=legal_names)
    after_secs, after_sum = us.build()
    control_secs, _cs = us.securities_from_universe(document, rule=rule_after, legal_names=legal_names)
    if control_secs != after_secs:
        fails.append("build() differs from securities_from_universe(document, rule, legal_names=map)")
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    src = (after_sum.get("universe") or {}).get("source")
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)"
          % (src, (after_sum.get("universe") or {}).get("fallback_reason")))
    print("DENOMINATOR: securities %d, silver articles %d" % (S, N))
    if N == 0 or S == 0 or len(before_secs) != S or set(before) != set(after):
        fails.append("N or S is 0, or the before/after security sets differ (%d vs %d)" % (len(before_secs), S))
    for label in ("gold_brand_admitted", "gold_brand_anchored", "gold_brand_refused"):
        print("SUMMARY %s: %s" % (label, asc(json.dumps(after_sum[label]))))
    print("SUMMARY whole_brand_admitted before %d after %d; refused before %d after %d" % (
        len(before_sum["whole_brand_admitted"]), len(after_sum["whole_brand_admitted"]),
        len(before_sum["whole_brand_refused"]), len(after_sum["whole_brand_refused"])))
    for key, _b in BRANDS:
        print("ALIASES %s before %s after %s anchored_aliases %s ticker_aliases %s" % (
            key, asc(json.dumps(before[key]["aliases"])), asc(json.dumps(after[key]["aliases"])),
            asc(json.dumps(after[key].get("anchored_aliases"))), asc(json.dumps(after[key]["ticker_aliases"]))))

    dict_differs = sorted(k for k in after if before[k] != after[k])
    others_differ = [k for k in dict_differs if k not in dict(BRANDS)]
    others_same = sorted(k for k in after if k not in dict_differs)
    print("SECURITY DICTS THAT DIFFER (before vs after): %d of %d: %s" % (len(dict_differs), S, dict_differs))
    rng = random.Random(SEED)
    sample_same = rng.sample(others_same, min(5, len(others_same)))
    measured = sorted(set(k for k, _b in BRANDS) | set(others_differ) | set(sample_same))

    pairs = {"b": collections.Counter(), "a": collections.Counter()}
    ments = {"b": collections.Counter(), "a": collections.Counter()}
    title_gain = collections.Counter()
    lead_gain = collections.Counter()
    differ_art = collections.Counter()
    lilly_no_anchor = []
    lilly_alias_pat = pg._span_pattern(pg._security_aliases(after["LLY_US_Equity"]),
                                       pg._security_exact_aliases(after["LLY_US_Equity"]))
    for i, art in enumerate(articles, 1):
        if i % 500 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        for k in measured:
            rb = pg._security_mentions(art, before[k])
            ra = pg._security_mentions(art, after[k])
            if rb["mention_count"]:
                pairs["b"][k] += 1
                ments["b"][k] += rb["mention_count"]
            if ra["mention_count"]:
                pairs["a"][k] += 1
                ments["a"][k] += ra["mention_count"]
            title_gain[k] += int(ra["mention_in_title"] and not rb["mention_in_title"])
            lead_gain[k] += int(ra["mention_in_lead"] and not rb["mention_in_lead"])
            if (rb["mention_count"], rb["mention_in_title"], rb["mention_in_lead"]) != (
                    ra["mention_count"], ra["mention_in_title"], ra["mention_in_lead"]):
                differ_art[k] += 1
        # the bare-Lilly articles with no anchor: a bare Lilly span and no unanchored alias or LLY anywhere
        spans = []
        anchored = False
        for text, where in texts_of(art):
            if lilly_alias_pat is not None and lilly_alias_pat.search(text):
                anchored = True
                break
            for m in BARE_LILLY.finditer(text):
                spans.append("%s: ...%s..." % (where, context(text, m)))
        if spans and not anchored:
            lilly_no_anchor.append((art["article_key"], spans))
    print("progress %d/%d" % (N, N), flush=True)

    for key, brand in BRANDS:
        p0, p1 = pairs["b"][key], pairs["a"][key]
        m0, m1 = ments["b"][key], ments["a"][key]
        print(asc("%s %s: pairs before %d after %d gained %d; mention_count before %d after %d; "
                  "title flags gained %d; lead flags gained %d" % (
                      key, brand, p0, p1, p1 - p0, m0, m1, title_gain[key], lead_gain[key])))
    print("LILLY ANCHOR: bare-Lilly articles with no anchor %d" % len(lilly_no_anchor))
    for article_key, spans in lilly_no_anchor:
        print(asc("  %s (%d bare span(s))" % (article_key, len(spans))))
        for span in spans:
            print(asc("    " + span))

    print("OTHER SECURITIES MEASURED: %d whose dict differs, plus %d sampled with an equal dict %s"
          % (len(others_differ), len(sample_same), sample_same))
    other_changed = [k for k in others_differ + sample_same
                     if pairs["b"][k] != pairs["a"][k] or ments["b"][k] != ments["a"][k] or differ_art[k] > 0]
    # every other security whose dict is equal is unchanged by purity of _security_mentions(article, security);
    # the sampled ones are the empirical check of that, measured through the real function over every article.
    print("OTHER SECURITIES CHANGED: %d of %d" % (len(other_changed), S))
    for k in other_changed:
        print("  changed: %s pairs %d -> %d, mentions %d -> %d" % (k, pairs["b"][k], pairs["a"][k],
                                                                    ments["b"][k], ments["a"][k]))

    lilly_gain = pairs["a"]["LLY_US_Equity"] - pairs["b"]["LLY_US_Equity"]
    lilly_ment_gain = ments["a"]["LLY_US_Equity"] - ments["b"]["LLY_US_Equity"]
    meta_gain = pairs["a"]["META_US_Equity"] - pairs["b"]["META_US_Equity"]
    dropped = {k for k, _s in lilly_no_anchor}
    if not N > 0:
        fails.append("N is 0")
    if lilly_gain != 0:
        fails.append("Lilly pairs gained %d, expected 0" % lilly_gain)
    if not lilly_ment_gain > 0:
        fails.append("Lilly mention_count gained %d, expected > 0" % lilly_ment_gain)
    for key in MUST_DROP:
        if key not in dropped:
            fails.append("%s is not in the Lilly no-anchor list" % key)
    if not meta_gain > 0:
        fails.append("Meta pairs gained %d, expected > 0" % meta_gain)
    if other_changed:
        fails.append("OTHER SECURITIES CHANGED %d, expected 0" % len(other_changed))
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
