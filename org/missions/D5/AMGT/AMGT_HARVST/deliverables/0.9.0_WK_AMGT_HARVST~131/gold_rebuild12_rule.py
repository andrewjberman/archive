"""HARVST served gold rebuild #12 -- THE RULE, one function read by the signing dry run and by the act's VERIFY.

Rebuild #12 serves R30 (a capital-initial ALIAS rule, HVST-br-1) and nothing else. The list does NOT move: the served list and
the proposed list are both `securities.universe.r75.json`. Built against the served rebuild #11 parts.

MENTION (key = article_key, security_key):
- GONE: a served pair may go ONLY when it is in br-1's R30 removal class (`r30_class`, a set of pair keys the caller computed
  with br-1's own classifier `br1_census.mentions`: mentioned under the pre-R30 rule, not under R30). Any other gone pair is
  OUTSIDE the class (LOST) and breaks the rule. A list entry that moves breaks the rule.
- A served row that CHANGES is (c) hash-only, or (f) co-mention fields only where every security entering or leaving the
  co-mentioned set has an added or removed row in that article. Anything else is UNEXPLAINED, breaks the rule, and is printed
  as an OUTSIDE row (a kept pair whose own counting fields fell under R30 is marked `r30_partial`).
- ADDED rows are counted (silver grown since the served build); they are reported, they do not break the rule.
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


def rule(before_m, before_d, after_m, after_d, served_list, proposed_list, silver_hash, as_of, r30_class=(),
         r30_partial=()):
    r30_class = {tuple(k) for k in r30_class}
    r30_partial = {tuple(k) for k in r30_partial}
    old = {s["security_key"]: s for s in served_list}
    new = {s["security_key"]: s for s in proposed_list}
    list_moved = sorted(k for k in set(old) | set(new) if r8._dump(old.get(k)) != r8._dump(new.get(k)))

    def mk(row):
        return (row.get("article_key"), row.get("security_key"))

    om = {mk(r): r for r in before_m}
    nm = {mk(r): r for r in after_m}
    gone = [k for k in om if k not in nm]
    removed_n = [k for k in gone if k in r30_class]
    removed_set = set(removed_n)
    lost = [k for k in gone if k not in removed_set]
    added = [k for k in nm if k not in om]
    changed = [k for k in nm if k in om and r8._dump(nm[k]) != r8._dump(om[k])]
    diffs = {k: r8._fields(om[k], nm[k]) for k in changed}

    cls = {}
    for k in changed:
        if diffs[k] == {"record_hash"} and nm[k].get("record_hash") == silver_hash.get(k[0]):
            cls[k] = "c"
    moved = collections.defaultdict(set)
    for k in added:
        moved[k[0]].add(k[1])
    for k in removed_n:
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

    outside = []
    for k in sorted(lost):
        outside.append({"article_key": k[0], "security_key": k[1], "kind": "gone",
                        "match_forms": om[k].get("match_forms"),
                        "why": "served pair gone and NOT in br-1's R30 removal class"})
    for k in sorted(unexplained):
        partial = k in r30_partial
        outside.append({"article_key": k[0], "security_key": k[1], "kind": "changed",
                        "match_forms": [om[k].get("match_forms"), nm[k].get("match_forms")],
                        "why": ("kept pair, R30 partial: own fields %s changed (mention_count %s -> %s)"
                                % (sorted(diffs[k]), om[k].get("mention_count"), nm[k].get("mention_count"))
                                if partial else
                                "changed row not explained by the R30 class: fields %s" % sorted(diffs[k]))})

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
    if list_moved:
        reasons.append("%d list entr(ies) moved: %s" % (len(list_moved), list_moved[:20]))
    if lost:
        reasons.append("%d served pair(s) gone OUTSIDE br-1's R30 class: %s"
                       % (len(lost), sorted(collections.Counter(k[1] for k in lost).items())))
    if unexplained:
        reasons.append("%d changed mention row(s) UNEXPLAINED (%d of them R30-partial kept pairs), fields %s"
                       % (len(unexplained), len([k for k in unexplained if k in r30_partial]),
                          dict(collections.Counter(f for k in unexplained for f in diffs[k]))))
    if d_gone:
        reasons.append("%d daily row(s) gone" % len(d_gone))
    if d_other:
        reasons.append("%d daily row(s) changed OTHER" % len(d_other))
    return {
        "mention_served": len(om), "mention_built": len(nm), "mention_gone": len(gone), "mention_lost": len(lost),
        "r30_removals": len(removed_n),
        "removed_by_security": dict(collections.Counter(k[1] for k in removed_n)),
        "mention_removed_keys": [list(k) for k in sorted(removed_n)],
        "mention_added": len(added), "mention_added_by_security": dict(collections.Counter(k[1] for k in added)),
        "mention_changed": len(changed), "mention_changed_by_class": dict(collections.Counter(cls.values())),
        "mention_changed_unexplained": len(unexplained),
        "mention_unexplained_fields": dict(collections.Counter(f for k in unexplained for f in diffs[k])),
        "outside_rows": outside, "outside_count": len(outside), "list_moved": list_moved,
        "daily_served": len(od), "daily_built": len(nd), "daily_gone": len(d_gone),
        "daily_added": len([k for k in nd if k not in od]), "daily_changed": len(d_changed),
        "daily_changed_by_class": dict(d_cls),
        "daily_other": d_other if len(d_other) <= 40 else dict(list(d_other.items())[:40]),
        "daily_other_count": len(d_other), "reasons": reasons, "holds": not reasons}


def _selftest():
    """Positive control: an R30-class pair gone holds. Negative controls: a non-class pair gone breaks; a list entry that
    moves breaks; an own-field change on a kept pair breaks (marked partial when br-1 says so)."""
    lst = [{"security_key": "A", "company": "A Co", "aliases": ["A Co", "A"]},
           {"security_key": "C", "company": "C Co", "aliases": ["C Co"]}]

    def row(a, s, n=1, forms=("x",)):
        return {"article_key": a, "security_key": s, "mention_count": n, "match_forms": list(forms), "record_hash": "h",
                "co_mentioned_securities": [], "co_mention_count": 0}

    before = [row("x1", "A"), row("x3", "C")]
    ok = rule(before, [], [before[1]], [], lst, lst, {}, "2026-10-08", r30_class=[("x1", "A")])
    assert ok["holds"] and ok["mention_gone"] == 1 and ok["r30_removals"] == 1 and ok["outside_count"] == 0, ok
    neg = rule(before, [], [before[0]], [], lst, lst, {}, "2026-10-08", r30_class=[("x1", "A")])
    assert not neg["holds"] and neg["mention_lost"] == 1 and neg["outside_count"] == 1 and neg["reasons"], neg
    moved = rule(before, [], before, [], lst, [lst[0], dict(lst[1], aliases=["C"])], {}, "2026-10-08")
    assert not moved["holds"] and moved["list_moved"] == ["C"], moved
    part = rule(before, [], [before[0], row("x3", "C", 0)], [], lst, lst, {}, "2026-10-08", r30_partial=[("x3", "C")])
    assert not part["holds"] and part["mention_changed_unexplained"] == 1 and "R30 partial" in part["outside_rows"][0]["why"], part
    print("SELFTEST OK: holds on an R30-class pair gone; negative controls break the rule: a non-class pair gone, a list "
          "entry that moves, an own-field change on a kept pair")


if __name__ == "__main__":
    _selftest()
