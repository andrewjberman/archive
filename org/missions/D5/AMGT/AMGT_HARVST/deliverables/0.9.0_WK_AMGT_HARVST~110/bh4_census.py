"""HVST-bh-4: what the GOLD securities list gains when a security the list knows only by its key takes its company
name from the identity registry. Read-only (S3 GET only); imports the served matcher and the real
universe_securities; re-implements no matcher.

BEFORE = `universe_securities.build(registry_join=False)` -- the registry join switched off by that PARAMETER
         (the pool name and the identity-map join are untouched).
AFTER  = `universe_securities.build()` as it stands.
Counts come from the REAL `pg._security_mentions` over every latest silver article (`pg._iter_latest_articles()`)."""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *[".."] * 7))
sys.path.insert(0, REPO)

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402


def asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def main():
    fails = []
    before_secs, before_sum = us.build(registry_join=False)
    after_secs, after_sum = us.build()
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    src = (after_sum.get("universe") or {}).get("source")
    fb = (after_sum.get("universe") or {}).get("fallback_reason")
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("BEFORE: build(registry_join=False); AFTER: build()")
    if set(before) != set(after) or len(before_secs) != S:
        fails.append("before/after security sets differ (%d vs %d)" % (len(before_secs), S))

    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    print("DENOMINATOR: securities %d, silver articles %d" % (S, N))
    if N == 0:
        fails.append("N is 0 (silver read returned no articles)")

    named = after_sum["names_from_registry"]
    k = len(named)
    print("REGISTRY NAME JOIN: %s" % asc(json.dumps(after_sum["registry_name_join"], sort_keys=True)))
    print("NAMES FROM REGISTRY: %d" % k)
    for row in named:
        key = row["security_key"]
        print(asc("  %s" % json.dumps({"security_key": key, "name": row["name"],
                                       "aliases": after[key]["aliases"],
                                       "ticker_aliases": after[key]["ticker_aliases"]})))
    if k != 3:
        fails.append("NAMES FROM REGISTRY is %d, not 3" % k)

    named_keys = [row["security_key"] for row in named]
    changed = sorted(key for key in after if before.get(key) != after[key])
    others = [key for key in changed if key not in named_keys]

    pairs = {"b": collections.Counter(), "a": collections.Counter()}
    ment = {"b": collections.Counter(), "a": collections.Counter()}
    for i, art in enumerate(articles, 1):
        if i % 500 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        for key in named_keys:
            for tag, secs in (("b", before), ("a", after)):
                count = pg._security_mentions(art, secs[key])["mention_count"]
                if count:
                    pairs[tag][key] += 1
                    ment[tag][key] += count
    for key in named_keys:
        p0, p1 = pairs["b"][key], pairs["a"][key]
        print(asc("%s %s -> %s: pairs before %d after %d gained %d; mention_count before %d after %d" % (
            key, before[key]["company"], after[key]["company"], p0, p1, p1 - p0, ment["b"][key], ment["a"][key])))
        if p1 < p0:
            fails.append("%s lost pairs (%d -> %d)" % (key, p0, p1))
    print("OTHER SECURITIES CHANGED: %d of %d" % (len(others), S))
    for key in others:
        print(asc("  changed: %s" % key))
    if others:
        fails.append("OTHER SECURITIES CHANGED is %d" % len(others))
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
