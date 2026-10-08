"""HVST-bh-5: what the GOLD securities list gains when a legal name the identity record cut at 30 characters inside a
corporate suffix loses the fragment. Read-only (S3 GET only); imports the served matcher and the real
universe_securities; re-implements no matcher.

BEFORE = `universe_securities.build(fragment_rule=False)` -- the fragment rule switched off by that PARAMETER
         (the pool name, the identity-map join and the registry join are untouched).
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

EXPECTED = {"AIG_US_Equity": "American International Group", "KCDMY_US_Equity": "Kimberly-Clark de Mexico"}


def asc(t):
    return str(t).encode("ascii", "backslashreplace").decode("ascii")


def main():
    fails = []
    before_secs, before_sum = us.build(fragment_rule=False)
    after_secs, after_sum = us.build()
    before = {s["security_key"]: s for s in before_secs}
    after = {s["security_key"]: s for s in after_secs}
    S = len(after_secs)
    legal_names, info = us.load_legal_names()
    R = info["records_read"]
    exact = {key: value for key, value in legal_names.items() if len(value) == us.LEGAL_NAME_EXACT_LENGTH}
    n = len(exact)
    src = (after_sum.get("universe") or {}).get("source")
    fb = (after_sum.get("universe") or {}).get("fallback_reason")
    print("SECURITIES SOURCE: universe_securities.build() -> %s (fallback_reason=%s)" % (src, fb))
    print("BEFORE: build(fragment_rule=False); AFTER: build()")
    if set(before) != set(after) or len(before_secs) != S:
        fails.append("before/after security sets differ (%d vs %d)" % (len(before_secs), S))

    articles = list(pg._iter_latest_articles())
    articles.sort(key=lambda r: r["article_key"])
    N = len(articles)
    print("DENOMINATOR: identity records %d, names of exactly 30 characters %d, securities %d, silver articles %d"
          % (R, n, S, N))
    if N == 0:
        fails.append("N is 0 (silver read returned no articles)")
    if n == 0:
        fails.append("n is 0 (no name of exactly 30 characters)")

    cut = {row["security_key"]: row for row in after_sum["legal_names_cut_in_suffix"]}
    unchanged = {row["security_key"]: row for row in after_sum["legal_names_exact_length_unchanged"]}
    changed_keys = []
    for key in sorted(exact):
        if key in cut:
            row = cut[key]
            changed_keys.append(key)
            print(asc("%s original=%s -> name=%s | CHANGED (fragment=%r)" % (key, row["original"], row["name"],
                                                                           row["fragment"])))
        elif key in unchanged:
            print(asc("%s original=%s -> name=%s | UNCHANGED" % (key, exact[key], after[key]["company"])))
        else:
            print(asc("%s original=%s | NOT A POOL SECURITY (no line in the securities list)" % (key, exact[key])))
            continue
        print(asc("    aliases before: %s" % json.dumps(before[key]["aliases"])))
        print(asc("    aliases after:  %s" % json.dumps(after[key]["aliases"])))
    print("CHANGED: %d of %d" % (len(changed_keys), n))

    pairs = {"b": collections.Counter(), "a": collections.Counter()}
    ment = {"b": collections.Counter(), "a": collections.Counter()}
    for i, art in enumerate(articles, 1):
        if i % 500 == 0:
            print("progress %d/%d" % (i, N), flush=True)
        for key in changed_keys:
            for tag, secs in (("b", before), ("a", after)):
                count = pg._security_mentions(art, secs[key])["mention_count"]
                if count:
                    pairs[tag][key] += 1
                    ment[tag][key] += count
    for key in changed_keys:
        p0, p1 = pairs["b"][key], pairs["a"][key]
        print(asc("%s: pairs before %d after %d; mention_count before %d after %d" % (
            key, p0, p1, ment["b"][key], ment["a"][key])))
        if p1 < p0:
            fails.append("%s lost pairs (%d -> %d)" % (key, p0, p1))

    others = sorted(key for key in after if before.get(key) != after[key] and key not in changed_keys)
    print("OTHER SECURITIES CHANGED: %d of %d" % (len(others), S))
    for key in others:
        print(asc("  changed: %s" % key))
    if others:
        fails.append("OTHER SECURITIES CHANGED is %d" % len(others))

    for key, want in sorted(EXPECTED.items()):
        if key not in exact:
            print("%s: NOT ON THE LIST" % key)
            continue
        got = after[key]["company"] if key in after else None
        print(asc("%s reads %r (plant expects %r)" % (key, got, want)))
        if got != want:
            fails.append("%s reads %r, not %r" % (key, got, want))
    print("CENSUS OK" if not fails else "CENSUS FAIL: " + "; ".join(fails))


if __name__ == "__main__":
    main()
