"""HVST-ab-3 BEFORE + PRE-RUN PRINT (issuer, read-only; no publisher request).

`--signing` writes the signing snapshot and the signed plan the halves cite. Without it, it writes the act-start snapshot
(`~83/ab3_before.json`) and the act-start plan (`~83/ab3_plan.json`), and prints `ACT-START GATE: OK` only when:
- every root equals signing;
- the outbox has no pending row;
- the plan equals the signed plan, pair for pair.
Otherwise it prints `ACT-START GATE: STOP`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ab3_common as c  # noqa: E402


def main():
    snap = c.snapshot()
    pend = c.outbox_pending()
    plan = c.full_plan()
    print("objects per root: %s" % {k: len(v) for k, v in snap.items()})
    print("outbox pending: %s" % pend)
    total = sum(v["pages"] for v in plan.values())
    print("PRE-RUN PRINT: %d (name, publisher) pairs, planned listing pages %d (basis DEFAULT on %d, MEASURED on 0)"
          % (len(plan), total, len(plan)))
    for k in sorted(plan):
        print("  %-28s pages %d bound %s" % (k, plan[k]["pages"], plan[k]["bound"]))
    if "--signing" in sys.argv:
        c.dump(c.SIGNING, {"snapshot": snap, "outbox_pending": pend})
        c.dump(c.PLAN_SIGNED, plan)
        print("wrote %s and %s" % (c.SIGNING, c.PLAN_SIGNED))
        return 0
    s = c.load(c.SIGNING)
    c.dump(os.path.join(c.WK, "ab3_before.json"), {"snapshot": snap, "outbox_pending": pend})
    c.dump(os.path.join(c.WK, "ab3_plan.json"), plan)
    drift = {k: tuple(len(x) for x in v) for k, v in c.diff(s["snapshot"], snap).items() if any(v)}
    plan_drift = plan != c.load(c.PLAN_SIGNED)
    if drift or any(pend.values()) or plan_drift:
        print("BEFORE DIFFERS (moved, removed, new) %s, outbox pending %s, plan drift %s" % (drift, pend, plan_drift))
        print("ACT-START GATE: STOP")
        return 1
    print("ACT-START GATE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
