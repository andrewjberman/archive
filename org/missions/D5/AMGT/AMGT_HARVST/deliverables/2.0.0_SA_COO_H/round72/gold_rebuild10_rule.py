"""HARVST served gold rebuild #10 -- THE RULE, one function read by the signing dry run and by the act's VERIFY.

It is rebuild #9's rule (`round64/gold_rebuild9_rule.py`) with ONE more way a pair may go, for the capitalised-headline
rule (HVST-bk-2, `1.0.0_SA_CTO~Z` R15 and msg 31745): LOST 0 except pairs NAMED BY KEY, UNEXPLAINED 0. Rebuild #10 changes
the MATCHER only (in a headline capitalised throughout, an exact-case form alone does not pair) and not the list, so:

MENTION (key = article_key, security_key):
- GONE: a served pair that goes is class (n) NAMED REMOVAL, and only then allowed, when the pair is one of the pairs named by
  key AND either (as in rebuild #9) its security is LIST-MOVED or FALLBACK, or (new) EVERY form in its served `match_forms`
  is an EXACT-CASE form of that security in the served list (one of its `ticker_aliases`, or its company string when its
  alias list is empty). The second arm is the only thing the headline rule can remove: a pair that rested on exact-case
  forms alone. Any other gone pair is LOST and breaks the rule.
- A served row that CHANGES is (c) hash-only, (g) own counting fields on a LIST-MOVED or FALLBACK security, or (f)
  co-mention fields only where every security entering or leaving the set has an added, (g)-changed or removed row in that
  article. Anything else is UNEXPLAINED and breaks the rule. (The headline rule's census read 0 pairs with a lower count
  but kept, so no new changed class is opened; if one appears the rule breaks and it is read.)
- A class-(g) `mention_count` that goes DOWN is allowed only on a security that lost a served alias or is FALLBACK.
DAILY: gone 0; changed is (a) on a touched security, else (b)/(d) coverage-only, else OTHER, which breaks the rule.
"""
import collections
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "gold_rebuild8_rule", os.path.join(os.path.dirname(HERE), "round60", "gold_rebuild8_rule.py"))
r8 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r8)

ALIAS_FIELDS = ("company", "aliases", "ticker_aliases", "anchored_aliases", "anchor_required_ticker_aliases",
                "ticker_anchor_aliases", "ticker_anchor_symbols")


def rule(before_m, before_d, after_m, after_d, served_list, proposed_list, silver_hash, as_of, named_removals=()):
    """Returns a dict of counts, the named exceptions, and `holds`. `named_removals` is an iterable of
    (article_key, security_key)."""
    old = {s["security_key"]: s for s in served_list}
    new = {s["security_key"]: s for s in proposed_list}
    list_moved = {k for k in set(old) & set(new)
                  if any(r8._dump(old[k].get(f)) != r8._dump(new[k].get(f)) for f in ALIAS_FIELDS)}
    fallback = {k for k in set(old) & set(new) if not (old[k].get("aliases") or [])}
    may_move = list_moved | fallback
    lost_alias = set()
    for key in list_moved:
        kept = {a.casefold() for a in (new[key].get("aliases") or []) + (new[key].get("anchored_aliases") or [])}
        if any(a.casefold() not in kept for a in (old[key].get("aliases") or [])):
            lost_alias.add(key)

    def mk(row):
        return (row.get("article_key"), row.get("security_key"))

    om = {mk(r): r for r in before_m}
    nm = {mk(r): r for r in after_m}
    named = {tuple(k) for k in named_removals}
    gone = [k for k in om if k not in nm]
    def _exact_forms(key):
        sec = old.get(key) or {}
        forms = set(sec.get("ticker_aliases") or [])
        if not (sec.get("aliases") or []) and sec.get("company"):
            forms.add(sec["company"])
        return forms

    def _served_forms(row):
        forms = row.get("match_forms") or []
        if isinstance(forms, str):
            forms = json.loads(forms)
        return list(forms)

    def _rested_on_exact_forms(k):
        forms = _served_forms(om[k])
        return bool(forms) and set(forms) <= _exact_forms(k[1])

    removed_n = [k for k in gone if k in named and (k[1] in may_move or _rested_on_exact_forms(k))]
    removed_set = set(removed_n)
    lost = [k for k in gone if k not in removed_set]
    named_not_gone = sorted(k for k in named if k not in removed_set)
    added = [k for k in nm if k not in om]
    changed = [k for k in nm if k in om and r8._dump(nm[k]) != r8._dump(om[k])]
    diffs = {k: r8._fields(om[k], nm[k]) for k in changed}

    cls = {}
    for k in changed:
        f = diffs[k]
        if f == {"record_hash"} and nm[k].get("record_hash") == silver_hash.get(k[0]):
            cls[k] = "c"
        elif f & r8.OWN_FIELDS and k[1] in may_move and f <= r8.OWN_FIELDS | r8.CO_FIELDS | {"record_hash"}:
            cls[k] = "g"
    moved = collections.defaultdict(set)
    for k in added:
        moved[k[0]].add(k[1])
    for k in removed_n:
        moved[k[0]].add(k[1])
    for k, v in cls.items():
        if v == "g":
            moved[k[0]].add(k[1])
    for k in changed:
        if k in cls:
            continue
        f = diffs[k]
        if f and f <= r8.CO_FIELDS | {"record_hash"}:
            delta = r8._co_set(om[k]) ^ r8._co_set(nm[k])
            if delta and delta <= moved[k[0]]:
                cls[k] = "f"
    unexplained = [k for k in changed if k not in cls]
    down = [k for k in changed if cls.get(k) == "g"
            and (nm[k].get("mention_count") or 0) < (om[k].get("mention_count") or 0)]
    down_by_sec = collections.Counter(k[1] for k in down)
    down_bad = sorted(k for k in down_by_sec if k not in lost_alias | fallback)

    added_by = collections.Counter()
    for k in added:
        added_by["new security" if k[1] not in old else
                 ("list-moved or fallback security" if k[1] in may_move else "unchanged security")] += 1
    g_by_sec = collections.Counter(k[1] for k, v in cls.items() if v == "g")

    touched_secs = {k[1] for k in added} | {k[1] for k in changed} | {k[1] for k in removed_n}

    def dk(row):
        return (row.get("security_key"), str(row.get("day"))[:10])

    od = {dk(r): r for r in before_d}
    nd = {dk(r): r for r in after_d}
    d_gone = [k for k in od if k not in nd]
    d_changed = [k for k in nd if k in od and r8._dump(nd[k]) != r8._dump(od[k])]
    d_cls = collections.Counter()
    d_other = {}
    for k in d_changed:
        if k[0] in touched_secs:
            d_cls["a"] += 1
            continue
        which, fields = r8.coverage_class(od[k], nd[k], as_of)
        d_cls[which] += 1
        if which == "OTHER":
            d_other["|".join(k)] = fields
    holds = (not lost and not unexplained and not down_bad and not d_gone and not d_other)
    return {
        "mention_served": len(om), "mention_built": len(nm), "mention_gone": len(gone), "mention_lost": len(lost),
        "mention_lost_keys": [list(k) for k in lost[:40]],
        "mention_removed_named": len(removed_n), "mention_removed_named_keys": [list(k) for k in sorted(removed_n)],
        "mention_removed_named_by_security": dict(collections.Counter(k[1] for k in removed_n)),
        "named_total": len(named), "named_not_gone": [list(k) for k in named_not_gone],
        "mention_removed_named_on_exact_forms": [list(k) for k in sorted(removed_n) if k[1] not in may_move],
        "mention_added": len(added), "mention_added_by": dict(added_by),
        "mention_added_by_moved_security": dict(collections.Counter(k[1] for k in added if k[1] in may_move)),
        "mention_changed": len(changed), "mention_changed_by_class": dict(collections.Counter(cls.values())),
        "mention_changed_g_by_security": dict(g_by_sec),
        "mention_changed_unexplained": len(unexplained),
        "mention_unexplained_fields": dict(collections.Counter(f for k in unexplained for f in diffs[k])),
        "mention_unexplained_sample": [list(k) + [sorted(diffs[k])] for k in unexplained[:20]],
        "mention_count_down_rows": len(down), "mention_count_down_by_security": dict(down_by_sec),
        "mention_count_down_not_allowed": down_bad,
        "securities_list_moved": sorted(list_moved), "securities_fallback": sorted(fallback),
        "securities_lost_a_served_alias": sorted(lost_alias),
        "daily_served": len(od), "daily_built": len(nd), "daily_gone": len(d_gone),
        "daily_added": len([k for k in nd if k not in od]), "daily_changed": len(d_changed),
        "daily_changed_by_class": dict(d_cls),
        "daily_other": d_other if len(d_other) <= 40 else dict(list(d_other.items())[:40]),
        "daily_other_count": len(d_other), "holds": holds}


def _selftest():
    """Fixture: a named pair that rested on an exact-case form alone goes as (n); three negative controls break the rule:
    the same pair unnamed; a named pair whose served forms include a name alias; an own-field change on an unmoved security."""
    served = [{"security_key": "PM", "company": "Philip Morris", "aliases": ["Philip Morris"], "ticker_aliases": ["PM"]},
              {"security_key": "C", "company": "C Co", "aliases": ["C Co"], "ticker_aliases": []}]

    def row(a, s, n=1, forms=("x",)):
        return {"article_key": a, "security_key": s, "mention_count": n, "match_forms": list(forms), "record_hash": "h",
                "co_mentioned_securities": [], "co_mention_count": 0}

    before = [row("x1", "PM", forms=["PM"]), row("x2", "PM", forms=["Philip Morris", "PM"]), row("x3", "C")]
    ok = rule(before, [], [before[1], before[2]], [], served, served, {}, "2026-10-08", named_removals=[("x1", "PM")])
    assert ok["holds"] and ok["mention_removed_named"] == 1, ok
    assert ok["mention_removed_named_on_exact_forms"] == [["x1", "PM"]], ok
    unnamed = rule(before, [], [before[1], before[2]], [], served, served, {}, "2026-10-08", named_removals=[])
    assert not unnamed["holds"] and unnamed["mention_lost"] == 1
    alias = rule(before, [], [before[0], before[2]], [], served, served, {}, "2026-10-08", named_removals=[("x2", "PM")])
    assert not alias["holds"] and alias["mention_lost"] == 1
    own = rule(before, [], [before[0], before[1], row("x3", "C", 5)], [], served, served, {}, "2026-10-08")
    assert not own["holds"] and own["mention_changed_unexplained"] == 1
    print("SELFTEST OK: holds on the named exact-form case; 3 of 3 negative controls break the rule")


if __name__ == "__main__":
    _selftest()
