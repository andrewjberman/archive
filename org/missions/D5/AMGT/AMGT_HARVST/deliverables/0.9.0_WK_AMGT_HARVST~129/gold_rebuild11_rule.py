"""HARVST served gold rebuild #11 -- THE RULE, one function read by the signing dry run and by the act's VERIFY.

Rebuild #11 serves the AIG_US_Equity / OMAB_MM_Equity / OMAB_US_Equity list move and nothing else. It is rebuild #10's rule
(`round72/gold_rebuild10_rule.py`) with the served list = `round72/securities.universe.r72.json` and the proposed list =
`securities.universe.r75.json`, and ONE change to the gone arm:

MENTION (key = article_key, security_key):
- GONE: a served pair may go only when its security is LIST-MOVED or FALLBACK, or it is named by key in
  REBUILD11_NAMED_REMOVALS.json (empty). Any other gone pair is LOST and breaks the rule. Gone pairs are counted per security.
- A served row that CHANGES is (c) hash-only, (g) own counting fields on a LIST-MOVED or FALLBACK security, or (f)
  co-mention fields only where every security entering or leaving the set has an added, (g)-changed or removed row in that
  article. Anything else is UNEXPLAINED and breaks the rule.
- A class-(g) `mention_count` that goes DOWN is allowed only on a security that lost a served alias or is FALLBACK.
DAILY: gone 0; changed is (a) on a touched security, else (b)/(d) coverage-only, else OTHER, which breaks the rule.
"""
import collections
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
_spec = importlib.util.spec_from_file_location(
    "gold_rebuild8_rule", os.path.join(PARENT, "2.0.0_SA_COO_H", "round60", "gold_rebuild8_rule.py"))
r8 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r8)

ALIAS_FIELDS = ("company", "aliases", "ticker_aliases", "anchored_aliases", "anchor_required_ticker_aliases",
                "ticker_anchor_aliases", "ticker_anchor_symbols")


def rule(before_m, before_d, after_m, after_d, served_list, proposed_list, silver_hash, as_of, named_removals=()):
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
    removed_n = [k for k in gone if k[1] in may_move or k in named]
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
    reasons = []
    if lost:
        reasons.append("%d served pair(s) LOST on a security that is neither list-moved nor fallback nor named: %s"
                       % (len(lost), sorted(collections.Counter(k[1] for k in lost).items())))
    if unexplained:
        reasons.append("%d changed mention row(s) UNEXPLAINED, fields %s"
                       % (len(unexplained), dict(collections.Counter(f for k in unexplained for f in diffs[k]))))
    if down_bad:
        reasons.append("mention_count went DOWN on a security that lost no alias and is not fallback: %s" % down_bad)
    if d_gone:
        reasons.append("%d daily row(s) gone" % len(d_gone))
    if d_other:
        reasons.append("%d daily row(s) changed OTHER" % len(d_other))
    return {
        "mention_served": len(om), "mention_built": len(nm), "mention_gone": len(gone), "mention_lost": len(lost),
        "mention_lost_keys": [list(k) for k in lost[:40]],
        "mention_gone_by_security": dict(collections.Counter(k[1] for k in gone)),
        "mention_removed_keys": [list(k) for k in sorted(removed_n)],
        "named_total": len(named), "named_not_gone": [list(k) for k in named_not_gone],
        "mention_added": len(added), "mention_added_by": dict(added_by),
        "mention_added_by_security_moved": dict(collections.Counter(k[1] for k in added if k[1] in may_move)),
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
        "daily_other_count": len(d_other), "reasons": reasons, "holds": not reasons}


def _selftest():
    """Fixture: a pair gone on a list-moved security holds; negative control: a pair lost on an UNCHANGED security breaks;
    a named pair on an unchanged security holds; an own-field change on an unmoved security breaks."""
    served = [{"security_key": "A", "company": "A Co", "aliases": ["A Co", "A Corp"], "ticker_aliases": []},
              {"security_key": "C", "company": "C Co", "aliases": ["C Co"], "ticker_aliases": []}]
    moved = [dict(served[0], aliases=["A Co"]), served[1]]

    def row(a, s, n=1, forms=("x",)):
        return {"article_key": a, "security_key": s, "mention_count": n, "match_forms": list(forms), "record_hash": "h",
                "co_mentioned_securities": [], "co_mention_count": 0}

    before = [row("x1", "A"), row("x3", "C")]
    ok = rule(before, [], [before[1]], [], served, moved, {}, "2026-10-08")
    assert ok["holds"] and ok["mention_gone"] == 1 and ok["mention_lost"] == 0, ok
    neg = rule(before, [], [before[0]], [], served, moved, {}, "2026-10-08")
    assert not neg["holds"] and neg["mention_lost"] == 1 and neg["reasons"], neg
    nam = rule(before, [], [before[0]], [], served, moved, {}, "2026-10-08", named_removals=[("x3", "C")])
    assert nam["holds"] and nam["mention_removed_keys"] == [["x3", "C"]], nam
    own = rule(before, [], [before[0], row("x3", "C", 5)], [], served, moved, {}, "2026-10-08")
    assert not own["holds"] and own["mention_changed_unexplained"] == 1, own
    print("SELFTEST OK: holds on a pair gone on a list-moved security; negative controls break the rule: "
          "a pair lost on an UNCHANGED security, an own-field change on an unmoved security; a named pair holds")


if __name__ == "__main__":
    _selftest()
