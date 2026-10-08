"""HVST-bh-7: what the GOLD securities list gains when a brand belongs to the ISSUER -- limb (a) of `brand_refusal` no
longer refuses a brand because ANOTHER LISTING OF THE SAME ISSUER carries it (ASML NA company "ASML" vs ASML US
"ASML Holding NV"). Read-only (S3 GET only); imports the served matcher and the real universe_securities; re-implements
no matcher.

BEFORE = `universe_securities.build(issuer_grouping=False)` -- the grouping switched off by its own parameter.
AFTER  = `universe_securities.build()` as it stands.
Counts come from the REAL `pg._security_mentions` over every latest silver article (`pg._iter_latest_articles()`).
Only a security whose built dict differs between BEFORE and AFTER can have a different count (the matcher reads the
dict alone), so only those are run over the articles; every other security's pairs lost is 0 by that identity, which
is itself checked (SECURITIES CHANGED OUTSIDE A GROUP)."""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

BRAND, BRAND_KEY = "ASML", "ASML_US_Equity"


def asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def main():
    fails = []
    before_secs, before_sum = us.build(issuer_grouping=False)
    after_secs, after_sum = us.build()
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    src = (after_sum.get("universe") or {}).get("source")
    fb = (after_sum.get("universe") or {}).get("fallback_reason")
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("BEFORE: build(issuer_grouping=False); AFTER: build()")
    if set(before) != set(after):
        fails.append("before/after security sets differ (%d vs %d)" % (len(before), len(after)))

    roots = collections.defaultdict(list)
    for key in sorted(after):
        roots[key.split("_")[0]].append(key)
    multi = {r: ks for r, ks in sorted(roots.items()) if len(ks) > 1}
    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    print("DENOMINATOR: securities %d, ticker roots with two or more listings %d, silver articles %d"
          % (S, len(multi), N))
    if N == 0:
        fails.append("N is 0 (silver read returned no articles)")

    group_of = {}
    limb_of = {}
    for g in after_sum["issuer_groups"]:
        for key in g["keys"]:
            group_of[key] = tuple(g["keys"])
            limb_of[tuple(g["keys"])] = g["limb"]
    not_grouped = {tuple(item["keys"]): item["companies"] for item in after_sum["listings_sharing_a_root_not_grouped"]}
    for root, keys in multi.items():
        names = ["%s=%r" % (k, after[k]["company"]) for k in keys]
        grouped = [group_of[k] for k in keys if k in group_of]
        if len(grouped) == len(keys) and len(set(grouped)) == 1:
            verdict = "GROUPED by limb %s" % limb_of[grouped[0]]
        else:
            why = [item for item in not_grouped.items() if set(item[0]) <= set(keys)]
            verdict = "NOT GROUPED: no limb links them (%s)" % "; ".join(
                "%s company names %s" % (" / ".join(k), " vs ".join(repr(c) for c in cs)) for k, cs in why)
        print(asc("ROOT %s: listings %s -- %s" % (root, ", ".join(keys), verdict)))
        print(asc("    company names: %s" % "; ".join(names)))

    def refusal_set(summary):
        return {(r["security_key"], r["brand"], r["reason"]) for r in summary["whole_brand_refused"]}

    r0, r1 = refusal_set(before_sum), refusal_set(after_sum)
    print("BRAND REFUSALS: before %d after %d" % (len(r0), len(r1)))
    for item in sorted(r0 - r1):
        print(asc("  no longer refused: %s brand %r (was %s)" % (item[0], item[1], item[2])))
    for item in sorted(r1 - r0):
        print(asc("  NEWLY refused: %s brand %r (%s)" % item))
        fails.append("a refusal appeared: %s %r" % (item[0], item[1]))

    changed = sorted(k for k in after if before.get(k) != after[k])
    in_group = set(group_of)
    outside = [k for k in changed if k not in in_group]
    print("ALIAS SETS CHANGED: %d" % len(changed))
    counts = {}
    for key in changed:
        counts[key] = [0, 0, 0, 0]  # pairs before, pairs after, mentions before, mentions after
    lost = 0
    for i, art in enumerate(articles, 1):
        if i % 2000 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        for key in changed:
            b = pg._security_mentions(art, before[key])["mention_count"]
            a = pg._security_mentions(art, after[key])["mention_count"]
            c = counts[key]
            c[0] += 1 if b else 0
            c[1] += 1 if a else 0
            c[2] += b
            c[3] += a
            if b and not a:
                lost += 1
    for key in changed:
        c = counts[key]
        print(asc("  %s: aliases before %s after %s" % (key, json_list(before[key]), json_list(after[key]))))
        print(asc("      pairs before %d after %d; mention_count before %d after %d" % (c[0], c[1], c[2], c[3])))
    print("PAIRS LOST: %d (over the %d changed securities; the other %d are built byte-equal, so 0 by identity)"
          % (lost, len(changed), S - len(changed)))
    print("SECURITIES CHANGED OUTSIDE A GROUP: %d of %d" % (len(outside), S))
    for key in outside:
        print(asc("  changed outside a group: %s" % key))

    if BRAND_KEY not in after or BRAND not in after[BRAND_KEY]["aliases"]:
        fails.append("the brand %s is not in %s aliases after" % (BRAND, BRAND_KEY))
    if lost != 0:
        fails.append("PAIRS LOST is %d" % lost)
    if outside:
        fails.append("SECURITIES CHANGED OUTSIDE A GROUP is %d" % len(outside))
    print("CENSUS OK" if not fails and N > 0 else "CENSUS FAIL: " + "; ".join(fails))


def json_list(security):
    out = list(security["aliases"])
    if security.get("anchored_aliases"):
        out.append({"anchored": security["anchored_aliases"]})
    return out


if __name__ == "__main__":
    main()
