"""HVST-ad-2 BEFORE + PRE-RUN PRINT (issuer, read-only; no publisher request).

`--signing` writes the signing snapshot and the signed plan. Without it, it writes the act-start snapshot and plan into
`~88/` and prints `ACT-START GATE: OK` only when:
- every root equals signing;
- the outbox has no pending row;
- the plan equals the signed plan.
Otherwise it prints `ACT-START GATE: STOP`.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ad2_common as c  # noqa: E402


def main():
    snap, pend, plan = c.snapshot(), c.outbox_pending(), c.plan()
    print("objects per root: %s" % {k: len(v) for k, v in snap.items()})
    print("outbox pending: %s" % pend)
    print("PRE-RUN PRINT: %d names x sa, planned listing pages %d (basis DEFAULT on %d)"
          % (len(plan), sum(v["pages"] for v in plan.values()), len(plan)))
    for k, v in plan.items():
        print("  %-28s %-8s pages %d bound %s" % (k, v["sa_symbol"], v["pages"], v["bound"]))
    if "--signing" in sys.argv:
        c.dump(c.SIGNING, {"snapshot": snap, "outbox_pending": pend})
        c.dump(c.PLAN_SIGNED, plan)
        print("wrote the signing snapshot and plan")
        return 0
    s = c.load(c.SIGNING)
    c.dump(os.path.join(c.WK, "ad2_before.json"), {"snapshot": snap, "outbox_pending": pend})
    c.dump(os.path.join(c.WK, "ad2_plan.json"), plan)
    drift = {k: tuple(len(x) for x in v) for k, v in c.diff(s["snapshot"], snap).items() if any(v)}
    if drift or any(pend.values()) or plan != c.load(c.PLAN_SIGNED):
        print("BEFORE DIFFERS: %s; outbox %s; plan drift %s" % (drift, pend, plan != c.load(c.PLAN_SIGNED)))
        print("ACT-START GATE: STOP")
        return 1
    print("ACT-START GATE: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
