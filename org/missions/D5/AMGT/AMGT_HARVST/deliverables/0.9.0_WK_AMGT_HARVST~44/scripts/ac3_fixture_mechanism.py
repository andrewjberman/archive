"""HVST-f-2 AC3 -- the planted fixture, OLD rule vs NEW rule. Pure (no I/O)."""
import sys

import _common as c
import fixtures as fx
from _common import pg

print("=" * 78)
print("FIXTURE -- MECHANISM TEST, NOT A HELD-OUT GRADE")
print("=" * 78)


def run(label, rows):
    print("\n%s: %d rows (tier-A %d, tier-B %d)" % (label, len(rows), sum(r["signal_tier"] == "A" for r in rows),
                                                   sum(r["signal_tier"] == "B" for r in rows)))
    with c.old_rule():
        o_names, o_ev = c.name_stems(rows, False), pg.event_rows(rows)
    n_names, n_ev = c.name_stems(rows, True), pg.event_rows(rows)
    print("  OLD rule: stripped name stems=%s ; %d event(s)" % (o_names, len(o_ev)))
    c.show_events(o_ev)
    print("  NEW rule: stripped name stems=%s ; %d event(s)" % (n_names, len(n_ev)))
    c.show_events(n_ev)
    return o_ev, n_ev


o2_events_ref = pg.event_rows(fx.variant2())
o1, n1 = run("variant 1 (the story is the security's ONLY coverage)", fx.variant1())
# Qualifying days are 09-10 and 09-11 (2 A/B rows and 2 tier-A publishers); 09-12 has one tier-A publisher (ft) plus a
# tier-B row, so it does not qualify and is outside the event: the same 4-article event variant 2 forms under the old rule.
ok1 = (len(o1) == 0 and len(n1) == 1 and n1[0]["articles_total"] == 4 and n1[0]["days_span"] == 2
       and str(n1[0]["first_day"]) == "2026-09-10" and str(n1[0]["last_day"]) == "2026-09-11"
       and n1[0]["article_keys"] == o2_events_ref[0]["article_keys"])
print("CHECK variant 1: old 0 events, new 1 event over its qualifying days 09-10..09-11 (4 articles), identical to the "
      "event variant 2 forms -> %s" % ("OK" if ok1 else "FAIL"))

o2, n2 = run("variant 2 (the same story among other coverage)", fx.variant2())
ok2 = len(o2) == 1 and o2 == n2
print("CHECK variant 2: the event is identical between old and new -> %s" % ("OK" if ok2 else "FAIL"))

o3, n3 = run("CONTROL (two unrelated multi-day stories of one security, no other coverage)", fx.control())
ok3 = len(n3) == 2 and {a for e in n3 for a in e["article_keys"]} == {r["article_key"] for r in fx.control()} \
    and all(not (set(a["article_keys"]) & set(b["article_keys"])) for a in n3 for b in n3 if a is not b)
print("CHECK control: the two stories do NOT merge; new rule forms %d events (%s)"
      % (len(n3), ", ".join("%s..%s %d articles" % (e["first_day"], e["last_day"], e["articles_total"]) for e in n3)))
print("CHECK control -> %s" % ("OK" if ok3 else "FAIL"))
sys.exit(0 if ok1 and ok2 and ok3 else 1)
