#!/usr/bin/env python3
"""MDPF_CANON round 11, CN-s-6 -- Global's axis drops the ENUMERATED date 2026-10-16 (issuer's check, read-only).

  python r11_cn_s_6.py real          run from the repo (worktree) root; reads the three staged per-firm legs of the
                                     2026-10-17 13:30Z fire from LEGS_DIR (outside the repo, client-scale) and runs the
                                     tree's build_global_artifact over them.
  python r11_cn_s_6.py selftest      prints the arm names and exits 0 (the arms are exercised by running `real` against
                                     a scratch reference and against planted mutants; see the order's preflight).

Arms (counts, dates and flags only; no client figure is printed):
  S0  GLOBAL_AXIS_DROP_DATES is exactly frozenset({"2026-10-16"}); GLOBAL_CROSS_AXIS_EXEMPT_DATES still holds its 20
      dates and does NOT hold 2026-10-16 (the CTO: never both).
  S1  build_global_artifact over the real legs EMITS (no coherence refusal), its dates carry no 2026-10-16 and its
      as_of_last is 2026-10-15 (the frontier).
  S2  the last row has a non-None model_aua, opal_aggregate_aua and non_model_aua, and the five CORE_MODEL_KEYS carry a
      non-None model_value on every date from 2026-07-21 to as_of_last.
  S3  the call leaves its inputs as it found them: the Cottonwood leg keeps 499 dates ending 2026-10-16, the other two
      legs keep 489 dates ending 2026-10-15.
  S4  NOT a general rule: the same Cottonwood leg with its 2026-10-16 relabelled 2026-10-19 (a date nothing enumerates)
      is still REFUSED by gate (v) with the presence-disagreement message.
Exit 0 only when every arm passes. ASCII only.
"""
import copy
import json
import os
import subprocess
import sys

LEGS_DIR = "C:/dev/_deploy_artifacts/canon_s6"
DROP = "2026-10-16"
res = []


def arm(name, ok, note=""):
    res.append(bool(ok))
    print("  %-3s %s %s" % (name, "PASS" if ok else "FAIL", note))


def load(root):
    sys.path.insert(0, os.path.join(root, "data", "mdpf", "scripts", "gold"))
    sys.path.insert(0, os.path.join(root, "data", "assets", "scripts", "gold"))
    import dim_mdpf_aggregate_aua_timeseries as spine
    return spine


def legs():
    return [json.load(open("%s/leg_%s.json" % (LEGS_DIR, k))) for k in ("49financial", "inflection", "cottonwood")]


def build(spine, a49, ainf, acot):
    try:
        return spine.build_global_artifact(a49, ainf, acot), None
    except (Exception, SystemExit) as e:
        return None, "%s: %s" % (type(e).__name__, e)


def real():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    spine = load(root)
    a49, ainf, acot = legs()
    snap = copy.deepcopy((a49["dates"], ainf["dates"], acot["dates"]))
    print("ROUND 11 CN-S-6 (tree %s, legs %d/%d/%d dates):" % (root, len(a49["dates"]), len(ainf["dates"]), len(acot["dates"])))

    drop = getattr(spine, "GLOBAL_AXIS_DROP_DATES", None)
    ex = spine.GLOBAL_CROSS_AXIS_EXEMPT_DATES
    arm("S0", drop == frozenset({DROP}) and len(ex) == 20 and DROP not in ex,
        "drop=%r exempt=%d holds_drop_date=%s" % (None if drop is None else sorted(drop), len(ex), DROP in ex))

    g, err = build(spine, a49, ainf, acot)
    if g is None:
        arm("S1", False, "REFUSED: " + err.splitlines()[0] + " | " + (err.splitlines()[1] if len(err.splitlines()) > 1 else ""))
        arm("S2", False, "no artifact")
    else:
        D = g["dates"]
        arm("S1", DROP not in D and g.get("as_of_last") == "2026-10-15",
            "dates=%d last=%s as_of_last=%s has_drop_date=%s" % (len(D), D[-1], g.get("as_of_last"), DROP in D))
        i = len(D) - 1
        head = all(g[k][i] is not None for k in ("model_aua", "opal_aggregate_aua", "non_model_aua"))
        bad = [(k, D[j]) for k in spine.CORE_MODEL_KEYS if k in g["by_model"]
               for j in range(len(D)) if D[j] >= "2026-07-21" and g["by_model"][k]["model_value"][j] is None]
        arm("S2", head and not bad, "last-row headline present=%s core None cells since 2026-07-21=%d" % (head, len(bad)))

    arm("S3", (len(acot["dates"]), acot["dates"][-1], len(a49["dates"]), a49["dates"][-1], len(ainf["dates"]), ainf["dates"][-1])
        == (499, "2026-10-16", 489, "2026-10-15", 489, "2026-10-15") and snap == (a49["dates"], ainf["dates"], acot["dates"]),
        "cot=%d..%s 49f=%d..%s inf=%d..%s" % (len(acot["dates"]), acot["dates"][-1], len(a49["dates"]), a49["dates"][-1],
                                             len(ainf["dates"]), ainf["dates"][-1]))

    b49, binf, bcot = legs()
    bcot["dates"] = [("2026-10-19" if d == DROP else d) for d in bcot["dates"]]
    g2, err2 = build(spine, b49, binf, bcot)
    arm("S4", g2 is None and "presence disagreement" in err2,
        "relabelled date -> %s" % ("REFUSED (v)" if g2 is None and "presence disagreement" in err2 else ("emitted" if g2 else err2.splitlines()[0])))

    k = sum(res)
    print("ROUND 11 CN-S-6 REAL: %d of %d arms" % (k, len(res)))
    return 0 if k == len(res) else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "real":
        sys.exit(real())
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        print("arms: S0 constants, S1 emits+axis, S2 headline+core, S3 inputs untouched, S4 not-a-general-rule")
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
