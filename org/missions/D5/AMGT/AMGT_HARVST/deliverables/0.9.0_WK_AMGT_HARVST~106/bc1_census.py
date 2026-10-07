"""HVST-bc-1: what the GOLD securities list gains when each security's legal name is read from the collector's
identity record. Dry run; read-only (S3 GET only); imports the served matcher and the real universe_securities,
re-implements no matcher. BEFORE = the pool list with the join off; AFTER = `universe_securities.build()`."""
import collections
import importlib.util
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

BB1 = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                   "0.9.0_WK_AMGT_HARVST~105", "bb1_census.py")
BRANDS = [("META_US_Equity", "Meta"), ("LLY_US_Equity", "Lilly")]
SEED = 56


def asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def load_bb1():
    spec = importlib.util.spec_from_file_location("bb1_census_round55", BB1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def texts_of(article):
    out = [article.get("title") or ""]
    out.extend(b or "" for b in (article.get("text_blocks") or []))
    return out


def pattern_of(sec):
    return pg._span_pattern(pg._security_aliases(sec), pg._security_exact_aliases(sec))


def count_in(pattern, texts):
    if pattern is None:
        return 0
    return sum(sum(1 for _ in pattern.finditer(t)) for t in texts if t)


def key_only(sec):
    return list(sec.get("aliases") or []) == [sec["security_key"]]


def main():
    fails = []
    document, provenance = us._read_universe()
    rule = us.load_alias_rule()
    before_secs, before_sum = us.securities_from_universe(document, rule=rule)
    after_secs, after_sum = us.build()
    legal_names, legal_info = us.load_legal_names()
    control_secs, _cs = us.securities_from_universe(document, rule=rule, legal_names=legal_names)
    if control_secs != after_secs:
        fails.append("build() differs from securities_from_universe(document, legal_names=map)")
    src = (after_sum.get("universe") or {}).get("source")
    fb = (after_sum.get("universe") or {}).get("fallback_reason")
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    R = legal_info["records_read"]
    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("DENOMINATOR: securities %d, silver articles %d, identity records %d" % (S, N, R))
    print("LEGAL NAME JOIN: %s" % asc(json.dumps(after_sum["legal_name_join"], sort_keys=True)))
    if N == 0 or S == 0 or len(before_secs) != S:
        fails.append("N or S is 0, or before/after security counts differ (%d vs %d)" % (len(before_secs), S))

    pool_named = {e.get("security_key") for e in document.get("names", []) if e.get("name")}
    ko_before = sorted(k for k, s in before.items() if key_only(s))
    ko_after = sorted(k for k, s in after.items() if key_only(s))
    print("KEY-ONLY ALIAS SETS: before %d of %d, after %d of %d" % (len(ko_before), S, len(ko_after), S))
    for k in ko_after:
        has_pool = k in pool_named
        has_identity = k in legal_names
        print("  still key-only: %s (pool name %s; identity record %s) -- why: no pool name and no identity record"
              % (k, "YES" if has_pool else "no", "YES" if has_identity else "no"))
        if has_pool or has_identity:
            fails.append("%s is key-only after but has a pool name or an identity record" % k)

    def brand_list(rows):
        return sorted("%s:%s" % (r["security_key"], r["brand"]) for r in rows)

    print("WHOLE BRANDS: admitted before %s after %s; refused before %s after %s" % (
        brand_list(before_sum["whole_brand_admitted"]), brand_list(after_sum["whole_brand_admitted"]),
        brand_list(before_sum["whole_brand_refused"]), brand_list(after_sum["whole_brand_refused"])))
    print("WHOLE BRANDS ALREADY AN ALIAS: before %s after %s" % (
        brand_list(before_sum["whole_brand_already_an_alias"]), brand_list(after_sum["whole_brand_already_an_alias"])))
    for label in ("company_name_from_pool", "company_name_from_identity"):
        print("SUMMARY %s: %d" % (label, after_sum[label]))
    for label in ("company_name_absent", "legal_name_slash_tail_stripped", "legal_name_exactly_30_chars"):
        print("SUMMARY %s: %d %s" % (label, after_sum[label]["count"], asc(json.dumps(after_sum[label]["keys"]))))

    changed = [k for k in after
               if (before[k]["aliases"], before[k]["ticker_aliases"], before[k]["company"])
               != (after[k]["aliases"], after[k]["ticker_aliases"], after[k]["company"])]
    print("CHANGED SECURITIES: %d of %d" % (len(changed), S))
    pat_b = {k: pattern_of(before[k]) for k in changed}
    pat_a = {k: pattern_of(after[k]) for k in changed}
    pairs_b = collections.Counter()
    pairs_a = collections.Counter()
    ment_b = collections.Counter()
    ment_a = collections.Counter()
    for i, art in enumerate(articles, 1):
        if i % 500 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        texts = texts_of(art)
        for k in changed:
            cb = count_in(pat_b[k], texts)
            ca = count_in(pat_a[k], texts)
            if cb:
                pairs_b[k] += 1
                ment_b[k] += cb
            if ca:
                pairs_a[k] += 1
                ment_a[k] += ca
    rows = []
    for k in changed:
        rows.append((pairs_a[k] - pairs_b[k], k))
    rows.sort(key=lambda r: (-r[0], r[1]))
    print("PER-NAME TABLE (%d lines; sorted by pairs gained)" % len(rows))
    down = []
    for gained, k in rows:
        print(asc("%s %s -> %s: pairs before %d after %d gained %d; mention_count before %d after %d" % (
            k, before[k]["company"], after[k]["company"], pairs_b[k], pairs_a[k], gained, ment_b[k], ment_a[k])))
        if gained < 0:
            down.append(k)
    P0, P1 = sum(pairs_b.values()), sum(pairs_a.values())
    print("TOTAL: names changed %d of %d; pairs before %d after %d gained %d" % (len(changed), S, P0, P1, P1 - P0))
    if down:
        fails.append("pairs went DOWN for %s" % ", ".join(down))
    if not len(ko_after) < len(ko_before):
        fails.append("after is not less than before for key-only alias sets (%d vs %d)" % (len(ko_after), len(ko_before)))

    print("NAME-QUALITY CLASS")
    slash = set(after_sum["legal_name_slash_tail_stripped"]["keys"])
    cut30 = set(after_sum["legal_name_exactly_30_chars"]["keys"])
    for gained, k in rows:
        if k in slash or k in cut30:
            classes = ",".join(c for c, s in (("slash_tail_stripped", slash), ("exactly_30_chars", cut30)) if k in s)
            print(asc("  %s [%s] %s -> %s: pairs gained %d" % (k, classes, before[k]["company"], after[k]["company"], gained)))
    unchanged_class = sorted((slash | cut30) - set(changed))
    print("  in class but alias set unchanged: %s" % asc(json.dumps(unchanged_class)))

    bb1 = load_bb1()
    print("AGAINST THE LIST WITH LEGAL NAMES")
    for key, brand in BRANDS:
        sec = after.get(key)
        if sec is None:
            fails.append("%s not in securities" % key)
            continue
        aliases = pg._security_aliases(sec)
        exact = pg._security_exact_aliases(sec)
        print("BASELINE %s aliases=%s exact=%s" % (key, asc(json.dumps(aliases)), asc(json.dumps(exact))))
        if any(brand.casefold() == a.casefold() for a in aliases):
            print("NOTE %s: %s is already an alias of the list with legal names; the brand adds nothing" % (key, brand))
        a_with = new_pairs = added = tf = lf = 0
        for art in articles:
            r = bb1.added_for(art, aliases, exact, brand)
            if not r["hits"]:
                continue
            a_with += 1
            new_pairs += int(r["base_count"] == 0)
            added += len(r["hits"])
            tf += int(r["title_flip"])
            lf += int(r["lead_flip"])
        print("%s %s: articles_with_added %d of %d articles; NEW pairs %d (the security had 0 mentions in the "
              "article under the served aliases); added mention count %d; title flips %d; lead flips %d"
              % (key, brand, a_with, N, new_pairs, added, tf, lf))

    rng = random.Random(SEED)
    gained_keys = [k for g, k in rows if g > 0] or changed
    five = rng.sample(sorted(gained_keys), min(5, len(gained_keys)))
    base_pick = rng.sample(articles, min(10, N)) if N else []
    hit_articles = [a for a in articles if any(count_in(pat_a[k], texts_of(a)) for k in five)]
    hit_pick = rng.sample(hit_articles, min(10, len(hit_articles)))
    seen = set()
    pick = []
    for a in base_pick + hit_pick:
        if a["article_key"] not in seen:
            seen.add(a["article_key"])
            pick.append(a)
    for a in rng.sample(articles, len(articles)):
        if len(pick) >= min(20, N):
            break
        if a["article_key"] not in seen:
            seen.add(a["article_key"])
            pick.append(a)
    agree = n = nonzero = 0
    for art in pick:
        texts = texts_of(art)
        for k in five:
            mine = count_in(pat_a[k], texts)
            served = pg._security_mentions(art, after[k])["mention_count"]
            n += 1
            nonzero += int(served > 0)
            agree += int(mine == served)
    print("AGREEMENT SAMPLE: %d articles, securities %s, pairs with a nonzero served count %d" % (
        len(pick), asc(json.dumps(five)), nonzero))
    print("AGREEMENT: %d of %d" % (agree, n))
    if agree != n or n == 0:
        fails.append("AGREEMENT %d of %d" % (agree, n))
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
