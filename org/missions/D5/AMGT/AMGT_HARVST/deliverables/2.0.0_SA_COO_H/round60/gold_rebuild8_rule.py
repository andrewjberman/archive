"""HARVST served gold rebuild #8 -- THE RULE, one function read by the signing dry run and by the act's VERIFY.

Rebuild #8 changes the securities LIST (the served file `round33/securities.universe.r33.json`, 212 names, against the list
`universe_securities.build()` yields after HVST-bc-1, bd-1, be-1 and bg-1), so served rows legitimately move. The rule names
every way a row may move and refuses the rest.

MENTION (key = article_key, security_key):
- GONE: 0 LOST. A served pair that goes is class (h) REFUSED-FORM REMOVAL, and only then allowed, when ALL hold: every form
  in its served `match_forms` is a ticker form on the refusal list, the proposed list no longer gives that security the
  form, and the pair is one of the pairs NAMED in the pair's own list (`named_removals`). Such a pair is MOVED with its
  cause, never lost (1.0.0_SA_CTO~Z msg 31329). Any other gone pair is LOST and breaks the rule.
- A served row that CHANGES is in exactly one class, tested in this order:
  (c) HASH-ONLY   only `record_hash` differs and it equals the current stored silver row's (the rebuild-#7 class);
  (g) OWN-ALIAS   one of the security's own counting fields differs AND that security's name or alias set differs between the
                  served list and the proposed list;
  (f) CO-MENTION  only the co-mention fields differ (with or without record_hash) AND every security that entered or left
                  the row's co-mentioned set has a row in the same article that was added, changed as class (g), or
                  removed as class (h).
  Anything else is UNEXPLAINED and breaks the rule.
- Rows of class (g) whose `mention_count` went DOWN are counted and named by security; they are allowed only on a security
  that lost a served alias (the decorated and slash-tailed forms the list repair removed), and any other is UNEXPLAINED.
- ADDED rows are counted by security and split: on a NEW security, on a security whose alias set differs, on an unchanged one
  (silver grown since the served build).
DAILY (key = security_key, day):
- GONE: 0.
- A served row that CHANGES is (a) on a security with any added, changed or (h)-removed mention row; else (b) coverage-only on the as-of
  day or (d) coverage-only on a past day, by the four bounds of the rebuild-#5 CTO half; else OTHER, which breaks the rule.
"""
import collections
import json

CO_FIELDS = {"co_mention_count", "co_mentioned_securities", "is_roundup"}
OWN_FIELDS = {"mention_count", "match_forms", "blocks_hit", "blocks_total", "first_mention_block", "mention_in_title",
              "mention_in_lead", "signal_tier", "signal_weight"}
ALIAS_FIELDS = ("company", "aliases", "ticker_aliases", "anchored_aliases")
STATUS_RANK = {"DENIED": 0, "PARTIAL": 1, "COMPLETE": 2}


def _dump(value):
    return json.dumps(value, sort_keys=True, default=str)


def _fields(a, b):
    return {f for f in set(a) | set(b) if _dump(a.get(f)) != _dump(b.get(f))}


def _co_set(row):
    value = row.get("co_mentioned_securities") or []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            value = [v for v in value.split(",") if v]
    return set(value)


def coverage_class(before, after, as_of):
    diff = _fields(before, after)
    fields_only = bool(diff) and diff <= {"data_status", "publishers_covered", "publishers_covered_codes"}
    grows = ((after.get("publishers_covered") or 0) >= (before.get("publishers_covered") or 0)
             and set(after.get("publishers_covered_codes") or []) >= set(before.get("publishers_covered_codes") or [])
             and STATUS_RANK.get(after.get("data_status"), -1) >= STATUS_RANK.get(before.get("data_status"), -1))
    if not (fields_only and grows):
        return "OTHER", sorted(diff)
    return ("b" if str(after.get("day"))[:10] == str(as_of) else "d"), sorted(diff)


def rule(before_m, before_d, after_m, after_d, served_list, proposed_list, silver_hash, as_of,
         refused_forms=(), named_removals=()):
    """Returns a dict of counts, the named exceptions, and `holds`."""
    old = {s["security_key"]: s for s in served_list}
    new = {s["security_key"]: s for s in proposed_list}
    alias_differs = {k for k in set(old) & set(new)
                     if any(_dump(old[k].get(f)) != _dump(new[k].get(f)) for f in ALIAS_FIELDS)}
    lost_alias = set()
    for key in alias_differs:
        kept = {a.casefold() for a in (new[key].get("aliases") or []) + (new[key].get("anchored_aliases") or [])}
        if any(a.casefold() not in kept for a in (old[key].get("aliases") or [])):
            lost_alias.add(key)

    def mk(row):
        return (row.get("article_key"), row.get("security_key"))

    om = {mk(r): r for r in before_m}
    nm = {mk(r): r for r in after_m}
    gone = [k for k in om if k not in nm]
    refused = set(refused_forms)
    named = {tuple(k) for k in named_removals}
    removed_h = []
    for k in gone:
        forms = om[k].get("match_forms") or []
        if isinstance(forms, str):
            forms = json.loads(forms)
        kept_forms = set((new.get(k[1]) or {}).get("ticker_aliases") or [])
        if forms and all(f in refused and f not in kept_forms for f in forms) and k in named:
            removed_h.append(k)
    lost = [k for k in gone if k not in set(removed_h)]
    added = [k for k in nm if k not in om]
    changed = [k for k in nm if k in om and _dump(nm[k]) != _dump(om[k])]
    diffs = {k: _fields(om[k], nm[k]) for k in changed}

    cls = {}
    for k in changed:
        f = diffs[k]
        if f == {"record_hash"} and nm[k].get("record_hash") == silver_hash.get(k[0]):
            cls[k] = "c"
        elif f & OWN_FIELDS and k[1] in alias_differs and f <= OWN_FIELDS | CO_FIELDS | {"record_hash"}:
            cls[k] = "g"
    moved = collections.defaultdict(set)
    for k in added:
        moved[k[0]].add(k[1])
    for k in removed_h:
        moved[k[0]].add(k[1])
    for k, v in cls.items():
        if v == "g":
            moved[k[0]].add(k[1])
    for k in changed:
        if k in cls:
            continue
        f = diffs[k]
        if f and f <= CO_FIELDS | {"record_hash"}:
            delta = _co_set(om[k]) ^ _co_set(nm[k])
            if delta and delta <= moved[k[0]]:
                cls[k] = "f"
    unexplained = [k for k in changed if k not in cls]
    down = [k for k in changed if cls.get(k) == "g"
            and (nm[k].get("mention_count") or 0) < (om[k].get("mention_count") or 0)]
    down_by_sec = collections.Counter(k[1] for k in down)
    down_bad = sorted(k for k in down_by_sec if k not in lost_alias)

    added_by = collections.Counter()
    for k in added:
        added_by["new security" if k[1] not in old else ("alias set differs" if k[1] in alias_differs else "unchanged alias set")] += 1

    touched_secs = {k[1] for k in added} | {k[1] for k in changed} | {k[1] for k in removed_h}
    removed_articles = {k[0] for k in removed_h}
    removed_secs = {k[1] for k in removed_h}
    co_follow_h = [k for k in changed if cls.get(k) == "f" and k[0] in removed_articles
                   and (_co_set(om[k]) ^ _co_set(nm[k])) & removed_secs]

    def dk(row):
        return (row.get("security_key"), str(row.get("day"))[:10])

    od = {dk(r): r for r in before_d}
    nd = {dk(r): r for r in after_d}
    d_gone = [k for k in od if k not in nd]
    d_changed = [k for k in nd if k in od and _dump(nd[k]) != _dump(od[k])]
    d_cls = collections.Counter()
    d_other = {}
    for k in d_changed:
        if k[0] in touched_secs:
            d_cls["a"] += 1
            continue
        which, fields = coverage_class(od[k], nd[k], as_of)
        d_cls[which] += 1
        if which == "OTHER":
            d_other["|".join(k)] = fields
    unexplained_fields = collections.Counter(f for k in unexplained for f in diffs[k])
    daily_follow_h = [k for k in d_changed if k[0] in removed_secs]
    holds = (not lost and not unexplained and not down_bad and not d_gone and not d_other)
    return {
        "mention_served": len(om), "mention_built": len(nm), "mention_gone": len(gone), "mention_lost": len(lost),
        "mention_lost_keys": [list(k) for k in lost[:40]], "mention_removed_h": len(removed_h),
        "mention_removed_h_by_security": dict(collections.Counter(k[1] for k in removed_h)),
        "mention_removed_h_keys": [list(k) for k in sorted(removed_h)],
        "co_mention_rows_following_h": len(co_follow_h), "daily_rows_following_h": len(daily_follow_h),
        "mention_added": len(added),
        "mention_added_by": dict(added_by), "mention_changed": len(changed),
        "mention_changed_by_class": dict(collections.Counter(cls.values())),
        "mention_changed_unexplained": len(unexplained), "mention_unexplained_fields": dict(unexplained_fields),
        "mention_unexplained_sample": [list(k) + [sorted(diffs[k])] for k in unexplained[:20]],
        "mention_count_down_rows": len(down), "mention_count_down_by_security": dict(down_by_sec),
        "mention_count_down_not_on_a_lost_alias": down_bad,
        "securities_alias_differs": len(alias_differs), "securities_lost_a_served_alias": sorted(lost_alias),
        "daily_served": len(od), "daily_built": len(nd), "daily_gone": len(d_gone),
        "daily_added": len([k for k in nd if k not in od]), "daily_changed": len(d_changed),
        "daily_changed_by_class": dict(d_cls), "daily_other": d_other if len(d_other) <= 40 else dict(list(d_other.items())[:40]),
        "daily_other_count": len(d_other), "holds": holds}
