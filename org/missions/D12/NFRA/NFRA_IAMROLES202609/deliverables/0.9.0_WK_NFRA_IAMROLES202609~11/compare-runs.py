#!/usr/bin/env python3
"""compare-runs.py -- put two permission-cold population bundles side by side.

usage: python compare-runs.py <earlier-bundle.json> <later-bundle.json>

Stdlib only; reads the two files and nothing else (NO cloud call). Bundles are the shape written by
rerun-population.sh / round 3's permission-cold-raw-bundle.json. Exit 0 when it printed a
comparison (COMPARABLE: no is still a comparison, with the reasons named); 2 on a missing or
unreadable file.

COMPARABLE is `yes` only when lookback_days, population_rule and instrument_blobs are equal.
population_rule is compared with the excluded-role COUNT masked ("the 10 roles at Path ..."),
because that count is a result of the run, not part of the rule; the raw counts are printed on
their own line so nothing is hidden.
"""
import json
import re
import sys
from collections import Counter

STATUSES = ("used", "never-used", "unobservable")


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        print("ERROR: cannot read bundle %s: %s" % (path, e), file=sys.stderr)
        sys.exit(2)


def mask_rule(rule):
    return re.sub(r"the \d+ roles at Path", "the <N> roles at Path", rule or "")


def excluded_count(rule):
    m = re.search(r"the (\d+) roles at Path", rule or "")
    return m.group(1) if m else "?"


def totals(results, names):
    c = Counter()
    for n in names:
        for row in results[n].get("rows", []):
            c[row.get("status", "?")] += 1
    return c


def fmt_totals(c):
    total = sum(c.values())
    parts = ["granted=%d" % total]
    for s in STATUSES:
        parts.append("%s=%d" % (s, c.get(s, 0)))
    for s in sorted(k for k in c if k not in STATUSES):
        parts.append("%s=%d" % (s, c[s]))
    return " ".join(parts)


def perm_map(res):
    return {r["permission"]: r.get("status", "?") for r in res.get("rows", [])}


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    pa, pb = argv[1], argv[2]
    a, b = load(pa), load(pb)
    ra, rb = a.get("results", {}), b.get("results", {})

    diffs = []
    if a.get("lookback_days") != b.get("lookback_days"):
        diffs.append("lookback_days (%s vs %s)" % (a.get("lookback_days"), b.get("lookback_days")))
    if mask_rule(a.get("population_rule")) != mask_rule(b.get("population_rule")):
        diffs.append("population_rule")
    if a.get("instrument_blobs") != b.get("instrument_blobs"):
        diffs.append("instrument_blobs")
    if diffs:
        print("COMPARABLE: no -- differ: " + "; ".join(diffs))
    else:
        print("COMPARABLE: yes")
    print("RUN A: %s  run_date_utc=%s lookback=%s attempted=%s returned_rc0=%s results=%d account=%s"
          % (pa, a.get("run_date_utc"), a.get("lookback_days"), a.get("attempted"),
             a.get("returned_rc0"), len(ra), a.get("account")))
    print("RUN B: %s  run_date_utc=%s lookback=%s attempted=%s returned_rc0=%s results=%d account=%s"
          % (pb, b.get("run_date_utc"), b.get("lookback_days"), b.get("attempted"),
             b.get("returned_rc0"), len(rb), b.get("account")))
    print("EXCLUDED service-linked roles named in the rule: A=%s B=%s (raw rule counts; masked for COMPARABLE)"
          % (excluded_count(a.get("population_rule")), excluded_count(b.get("population_rule"))))
    for tag, bun in (("A", a), ("B", b)):
        bad = sorted(n for n, v in bun.get("per_role_rc", {}).items() if v.get("rc") != 0 or "json_error" in v)
        print("NOT CLEAN in %s (rc != 0 / unreadable), by name: %s" % (tag, ", ".join(bad) if bad else "none"))
        att = bun.get("attempted")
        if att is not None and att != len(bun.get("results", {})) + len(bad):
            print("NOTE %s: attempted=%s but results+failed=%d (members never attempted are not clean)"
                  % (tag, att, len(bun.get("results", {})) + len(bad)))

    sa, sb = set(ra), set(rb)
    inter = sorted(sa & sb)
    added = sorted(sb - sa)
    removed = sorted(sa - sb)
    print("INTERSECTION roles=%d" % len(inter))
    print()
    print("TOTALS, all roles:")
    print("  A: " + fmt_totals(totals(ra, sorted(sa))))
    print("  B: " + fmt_totals(totals(rb, sorted(sb))))
    print("TOTALS, intersection (%d roles):" % len(inter))
    print("  A: " + fmt_totals(totals(ra, inter)))
    print("  B: " + fmt_totals(totals(rb, inter)))
    print()
    print("ROLES ADDED (in B, not in A): %d" % len(added))
    for n in added:
        c = totals(rb, [n])
        print("  + %s  %s" % (n, fmt_totals(c)))
    print("ROLES REMOVED (in A, not in B): %d" % len(removed))
    for n in removed:
        c = totals(ra, [n])
        print("  - %s  %s" % (n, fmt_totals(c)))
    print()

    trans = Counter()
    same = 0
    per_role_change = {}
    perm_added = Counter()
    perm_removed = Counter()
    for n in inter:
        pma, pmb = perm_map(ra[n]), perm_map(rb[n])
        changed = 0
        for p in set(pma) | set(pmb):
            sa_, sb_ = pma.get(p), pmb.get(p)
            if sa_ is None:
                trans[("(absent)", sb_)] += 1
                perm_added[n] += 1
                changed += 1
            elif sb_ is None:
                trans[(sa_, "(absent)")] += 1
                perm_removed[n] += 1
                changed += 1
            elif sa_ != sb_:
                trans[(sa_, sb_)] += 1
                changed += 1
            else:
                same += 1
        if changed:
            per_role_change[n] = changed
    print("TRANSITIONS on the intersection (permission status in A -> B), count:")
    same = sum(len(perm_map(ra[n])) for n in inter) - sum(trans[k] for k in trans if k[1] == "(absent)" or k[0] == "(absent)") \
        - sum(trans[k] for k in trans if "(absent)" not in k)
    for (x, y), c in sorted(trans.items(), key=lambda kv: (-kv[1], kv[0])):
        print("  %s -> %s : %d" % (x, y, c))
    if not trans:
        print("  (none)")
    print("  unchanged (same status in both runs): %d" % same)
    print("  roles with at least one change: %d of %d" % (len(per_role_change), len(inter)))
    if per_role_change:
        print("ROLES WITH CHANGES, most first (role: changed permissions, +granted -revoked):")
        for n, c in sorted(per_role_change.items(), key=lambda kv: (-kv[1], kv[0])):
            print("  %s: %d  (+%d -%d)" % (n, c, perm_added.get(n, 0), perm_removed.get(n, 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
