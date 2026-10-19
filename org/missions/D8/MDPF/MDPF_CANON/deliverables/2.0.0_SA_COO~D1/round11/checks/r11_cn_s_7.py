#!/usr/bin/env python3
"""MDPF_CANON round 11, CN-s-7 (DRAFT, issuer's check, read-only) -- Global's axis keeps 2026-10-16 once all three legs carry it.

  python r11_cn_s_7.py real      run from the repo (worktree) root; reads the three staged legs of the 2026-10-19 13:30Z fire
                                 (LEGS_NEW, outside the repo, client-scale) and the 2026-10-17 legs (LEGS_OLD, where only
                                 Cottonwood carried 2026-10-16) and runs the tree's build_global_artifact over each.

Arms (counts, dates and flags only; no client figure is printed):
  S0  GLOBAL_AXIS_DROP_DATES is an EMPTY frozenset; GLOBAL_CROSS_AXIS_EXEMPT_DATES still holds its 20 dates and not 2026-10-16.
  S1  over the NEW legs the build EMITS, its dates carry 2026-10-16 and its as_of_last is 2026-10-16.
  S2  the last row has non-None model_aua, opal_aggregate_aua and non_model_aua, and the five CORE_MODEL_KEYS carry a
      non-None model_value on every date from 2026-07-21 to as_of_last.
  S3  the call leaves its inputs as it found them: the NEW legs keep 490, 490 and 499 dates, each ending 2026-10-16.
  S4  control: over the OLD legs (2026-10-16 only at Cottonwood) gate (v) REFUSES again with the presence-disagreement
      message: with the drop set empty the gate is the only protection, and it still fires.
Exit 0 only when every arm passes. ASCII only.
"""
import copy
import json
import subprocess
import sys

LEGS_NEW = "C:/dev/_deploy_artifacts/canon_s6/fire_20261019"
LEGS_OLD = "C:/dev/_deploy_artifacts/canon_s6"
LAST = "2026-10-16"
res = []


def arm(name, ok, note=""):
    res.append(bool(ok))
    print("  %-3s %s %s" % (name, "PASS" if ok else "FAIL", note))


def load(root):
    import os
    sys.path.insert(0, os.path.join(root, "data", "mdpf", "scripts", "gold"))
    sys.path.insert(0, os.path.join(root, "data", "assets", "scripts", "gold"))
    import dim_mdpf_aggregate_aua_timeseries as spine
    return spine


def legs(d):
    return [json.load(open("%s/leg_%s.json" % (d, k))) for k in ("49financial", "inflection", "cottonwood")]


def build(spine, a49, ainf, acot):
    try:
        return spine.build_global_artifact(a49, ainf, acot), None
    except (Exception, SystemExit) as e:
        return None, "%s: %s" % (type(e).__name__, e)


def real():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    spine = load(root)
    a49, ainf, acot = legs(LEGS_NEW)
    snap = copy.deepcopy((a49["dates"], ainf["dates"], acot["dates"]))
    print("ROUND 11 CN-S-7 (tree %s, new legs %d/%d/%d dates):" % (root, len(a49["dates"]), len(ainf["dates"]), len(acot["dates"])))

    drop = getattr(spine, "GLOBAL_AXIS_DROP_DATES", None)
    ex = spine.GLOBAL_CROSS_AXIS_EXEMPT_DATES
    arm("S0", drop == frozenset() and len(ex) == 20 and LAST not in ex,
        "drop=%r exempt=%d holds_date=%s" % (None if drop is None else sorted(drop), len(ex), LAST in ex))

    g, err = build(spine, a49, ainf, acot)
    if g is None:
        arm("S1", False, "REFUSED: " + err.splitlines()[0][:160])
        arm("S2", False, "no artifact")
    else:
        D = g["dates"]
        arm("S1", LAST in D and g.get("as_of_last") == LAST, "dates=%d last=%s as_of_last=%s" % (len(D), D[-1], g.get("as_of_last")))
        i = len(D) - 1
        head = all(g[k][i] is not None for k in ("model_aua", "opal_aggregate_aua", "non_model_aua"))
        bad = [(k, D[j]) for k in spine.CORE_MODEL_KEYS if k in g["by_model"]
               for j in range(len(D)) if D[j] >= "2026-07-21" and g["by_model"][k]["model_value"][j] is None]
        arm("S2", head and not bad, "last-row headline present=%s core None cells since 2026-07-21=%d" % (head, len(bad)))

    arm("S3", (len(a49["dates"]), a49["dates"][-1], len(ainf["dates"]), ainf["dates"][-1], len(acot["dates"]), acot["dates"][-1])
        == (490, LAST, 490, LAST, 499, LAST) and snap == (a49["dates"], ainf["dates"], acot["dates"]),
        "49f=%d..%s inf=%d..%s cot=%d..%s" % (len(a49["dates"]), a49["dates"][-1], len(ainf["dates"]), ainf["dates"][-1],
                                             len(acot["dates"]), acot["dates"][-1]))

    o49, oinf, ocot = legs(LEGS_OLD)
    g2, err2 = build(spine, o49, oinf, ocot)
    arm("S4", g2 is None and "presence disagreement" in err2,
        "old legs -> %s" % ("REFUSED (v)" if g2 is None and "presence disagreement" in err2 else ("emitted" if g2 else err2.splitlines()[0][:120])))

    k = sum(res)
    print("ROUND 11 CN-S-7 REAL: %d of %d arms" % (k, len(res)))
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "real":
        sys.exit(real())
    print(__doc__)
    sys.exit(2)
