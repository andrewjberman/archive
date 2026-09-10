#!/usr/bin/env python3
"""H2-AC2 -- THE SHRINKING-EMISSION ARM, RED FIRST, THEN GREEN.

NFRA_CLDGRPH TO-CG-H-2 / cell CG-s-37, worker 0.9.0_WK_NFRA_CLDGRPH~1.

A producer that reads back its own output is silently idempotent under a FIXED emission and
silently WRONG under a SHRINKING one. Under a fixed emission every archived member collides
with a fresh one and the collision rule collapses it, so nothing shows. The failure is only
representable by a fixture that SHRINKS -- cycle 1 emits a STRICT SUPERSET of cycle 2 -- and
that is what this harness builds.

TWO ARMS IN ONE RUN, and both execute REAL PRODUCER SOURCE, never a transcription:

  BASELINE (RED)  -- _collapse_stitch_copies as it stands at the pre-fix commit
                     BASELINE_COMMIT (this worktree's cut), read with `git show`.
  CURRENT (GREEN) -- _collapse_stitch_copies as it stands in the worktree file.

Only three module-level objects are executed out of each source (STITCH_SOURCE,
RETIRED_STITCH_PROPS, _collapse_stitch_copies), lifted by an ast parse, so the harness does
not need boto3, the portal extractor or the trace graph -- and so it cannot accidentally
reach AWS. HARNESS GRAIN: node objects in a classes_data union, counted by id.

WHY THE BASELINE IS RE-DERIVED RATHER THAN STORED: after the fix is committed, a stored
"it used to fail" is an assertion. Reading the pre-fix blob out of git makes the red arm
reproducible by anyone at any later commit. ENVIRONMENT: both arms run in the same process,
same python, same fixture -- the only variable is the producer source.

NEGATIVE CONTROL, both arms: a node BOTH cycles emit must survive EXACTLY ONCE, and the
surviving object must be THIS cycle's. The control is itself exercised against a MUTANT
collapse that drops every stitch node -- if the control cannot catch that, it is not a
control.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[7]
PRODUCER_REL = "infra/aws/globgrph/derive_stitch.py"
PRODUCER = WS / "infra" / "aws" / "globgrph" / "derive_stitch.py"
BASELINE_COMMIT = "2fd5cae09f"          # the commit this worktree was cut from -- PRE-FIX
WANT_DEFS = ("_collapse_stitch_copies",)
WANT_NAMES = ("STITCH_SOURCE", "RETIRED_STITCH_PROPS")

CYCLE1_IDS = ["n1", "n2", "n3", "n4", "n5"]     # prior cycle: the SUPERSET
CYCLE2_IDS = ["n1", "n2"]                       # this cycle: a STRICT SUBSET
PRIOR_ONLY = [i for i in CYCLE1_IDS if i not in CYCLE2_IDS]
BOTH_CYCLES = [i for i in CYCLE1_IDS if i in CYCLE2_IDS]


def lift(src: str, label: str):
    """Execute ONLY the collapse function and its two module constants out of `src`."""
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in WANT_DEFS:
            keep.append(node)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in WANT_NAMES:
                    keep.append(node)
    ns: dict = {}
    exec(compile(ast.Module(body=keep, type_ignores=[]), "<%s>" % label, "exec"), ns)
    missing = [n for n in WANT_DEFS + WANT_NAMES if n not in ns]
    if missing:
        raise SystemExit("ERROR: lift(%s) missing %s" % (label, missing))
    return ns["_collapse_stitch_copies"]


def fixture():
    """The union derive_stitch builds: archived snapshot nodes + this cycle's emission.

    Archived nodes sit in the class bucket the snapshot wrote them under ('stitch_cloud');
    the fresh emission lands in the bucket named for its canonical type. That split is the
    reason one id becomes two node objects and the reason a per-class check cannot see it.
    """
    archived = [{"id": i, "type": "Component", "source": "portal-stitch",
                 "origin_marker": "CYCLE1_ARCHIVED"} for i in CYCLE1_IDS]
    fresh = [{"id": i, "type": "Component", "source": "portal-stitch",
              "origin_marker": "CYCLE2_FRESH"} for i in CYCLE2_IDS]
    # a NON-stitch node with the same id in two class buckets: the producer promises never to
    # touch these (an S3 bucket is legitimately both S3_BUCKET and S3_BUCKET_POLICY)
    canon_a = {"id": "canon1", "type": "S3_BUCKET", "source": None}
    canon_b = {"id": "canon1", "type": "S3_BUCKET_POLICY", "source": None}
    classes_data = {
        "stitch_cloud": {"nodes": list(archived) + [canon_a]},
        "component": {"nodes": list(fresh) + [canon_b]},
    }
    fresh_objs = {id(n) for n in fresh}
    return classes_data, fresh_objs


def mutant_collapse(classes_data, fresh_objs=None):
    """An OVER-BROAD fix: drop EVERY stitch node, archived or fresh. Exists so the negative
    control can be shown catching something -- an unrun control is a promise, not a check."""
    dropped = {"prior_cycle_copy": 0, "cross_class_copy": 0, "retired_props_dropped": 0}
    for v in classes_data.values():
        v["nodes"] = [n for n in v.get("nodes", []) if n.get("source") != "portal-stitch"]
    return dropped


def survey(classes_data, fresh_objs):
    surv = {}
    for cls, v in classes_data.items():
        for n in v.get("nodes", []):
            surv.setdefault(str(n.get("id")), []).append(
                {"class": cls, "marker": n.get("origin_marker"),
                 "is_fresh_object": id(n) in fresh_objs, "source": n.get("source")})
    return surv


def run_arm(collapse, label):
    classes_data, fresh_objs = fixture()
    dropped = collapse(classes_data, fresh_objs)
    surv = survey(classes_data, fresh_objs)
    prior_only_surviving = [i for i in PRIOR_ONLY if i in surv]
    both = BOTH_CYCLES[0]
    both_rows = surv.get(both, [])
    both_once = len(both_rows) == 1
    both_is_fresh = bool(both_rows) and both_rows[0]["is_fresh_object"]
    canon_rows = surv.get("canon1", [])
    return {"label": label, "dropped_counters": dropped,
            "prior_only_surviving": prior_only_surviving,
            "prior_only_denominator": len(PRIOR_ONLY),
            "both_cycles_node": both, "both_cycles_rows": both_rows,
            "both_survives_once": both_once, "both_surviving_object_is_fresh": both_is_fresh,
            "non_stitch_id_rows": len(canon_rows),
            "surviving_ids": sorted(surv)}


def show(arm):
    print("  ARM=%s" % arm["label"])
    print("    counters returned by the producer: %s" % json.dumps(arm["dropped_counters"]))
    print("    PRIOR_CYCLE_ONLY node ids: %s (denominator %d, the strict-superset remainder)"
          % (PRIOR_ONLY, arm["prior_only_denominator"]))
    print("    surviving prior-cycle-only ids: %s -> %d of %d"
          % (arm["prior_only_surviving"] or "NONE", len(arm["prior_only_surviving"]),
             arm["prior_only_denominator"]))
    print("    node emitted by BOTH cycles (%s): %d surviving copy/copies, fresh_object=%s"
          % (arm["both_cycles_node"], len(arm["both_cycles_rows"]),
             str(arm["both_surviving_object_is_fresh"]).lower()))
    print("    NON-STITCH id present in two class buckets: %d rows surviving (must stay 2 -- the "
          "producer promises never to touch these)" % arm["non_stitch_id_rows"])
    print("    surviving ids: %s" % arm["surviving_ids"])


def main() -> int:
    baseline_src = subprocess.run(
        ["git", "-C", str(WS), "show", "%s:%s" % (BASELINE_COMMIT, PRODUCER_REL)],
        capture_output=True, text=True, timeout=60)
    if baseline_src.returncode != 0:
        print("ERROR: could not read the pre-fix blob %s:%s -- %s"
              % (BASELINE_COMMIT, PRODUCER_REL, baseline_src.stderr.strip()[:300]))
        return 2
    current_src = PRODUCER.read_text(encoding="utf-8")
    head = subprocess.run(["git", "-C", str(WS), "rev-parse", "HEAD"],
                          capture_output=True, text=True, timeout=60).stdout.strip()

    print("H2-AC2 SHRINK ARM -- NFRA_CLDGRPH CG-s-37")
    print("TREE_READ=%s" % WS)
    print("INSTRUMENT: the producer's OWN _collapse_stitch_copies, lifted by ast from two "
          "sources and executed -- baseline from git blob %s:%s, current from the worktree file"
          % (BASELINE_COMMIT, PRODUCER_REL))
    print("COVERAGE: 1 function of 1 (the only node-side prior-cycle rule in the file, located "
          "by name); fixture denominator = %d cycle-1 ids, %d cycle-2 ids, %d prior-cycle-only"
          % (len(CYCLE1_IDS), len(CYCLE2_IDS), len(PRIOR_ONLY)))
    print("GRAIN: node OBJECTS in a classes_data union, counted by id and by object identity")
    print("BASELINE_ENVIRONMENT: same process, same python %s, same fixture; the only variable "
          "is the producer source. HEAD=%s" % (sys.version.split()[0], head))
    print("")

    baseline = run_arm(lift(baseline_src.stdout, "baseline@%s" % BASELINE_COMMIT),
                       "BASELINE (pre-fix source @%s)" % BASELINE_COMMIT)
    current = run_arm(lift(current_src, "current"), "CURRENT (worktree source)")
    mutant = run_arm(mutant_collapse, "MUTANT (over-broad: drops every stitch node)")

    print("---- BASELINE ARM: this must be RED, or the fixture cannot represent the failure ----")
    show(baseline)
    baseline_red = len(baseline["prior_only_surviving"]) > 0
    print("  BASELINE_VERDICT=%s" % ("RED (prior-cycle-only nodes survived)" if baseline_red
                                     else "GREEN -- STOP: an arm that was always green is not a "
                                          "test; file a row"))
    print("")
    print("---- CURRENT ARM ----")
    show(current)
    print("")
    print("---- MUTANT ARM (exercises the negative control; not a verdict on the producer) ----")
    show(mutant)
    mutant_caught = not (mutant["both_survives_once"] and mutant["both_surviving_object_is_fresh"])
    print("  the control catches the over-broad mutant: %s" % str(mutant_caught).lower())
    print("")

    cap = Path(__file__).with_name("h2_shrink_arm.capture.json")
    cap.write_text(json.dumps({"head": head, "baseline_commit": BASELINE_COMMIT,
                               "baseline": baseline, "current": current, "mutant": mutant},
                              indent=1), encoding="utf-8")
    print("CAPTURE=%s" % cap.name)

    ok = (baseline_red and not current["prior_only_surviving"]
          and current["both_survives_once"] and current["both_surviving_object_is_fresh"]
          and current["non_stitch_id_rows"] == 2 and mutant_caught)
    print("BASELINE_RED_CAPTURED=%s" % str(baseline_red).lower())
    print("BASELINE_SURVIVORS=%d of %d prior-cycle-only nodes survived the PRE-FIX source"
          % (len(baseline["prior_only_surviving"]), len(PRIOR_ONLY)))
    print("SHRINK_ARM=%s" % ("PASS" if ok else "FAIL"))
    print("PRIOR_CYCLE_ONLY_NODES_SURVIVING=%d of %d"
          % (len(current["prior_only_surviving"]), len(PRIOR_ONLY)))
    print("BOTH_CYCLES_NODE_SURVIVES_ONCE=%s"
          % str(current["both_survives_once"] and current["both_surviving_object_is_fresh"]).lower())
    print("NON_STITCH_UNTOUCHED=%s" % str(current["non_stitch_id_rows"] == 2).lower())
    print("NEGATIVE_CONTROL=%s" % ("FIRED" if mutant_caught else "DID-NOT-FIRE"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
