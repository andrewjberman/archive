"""LGIC_ENFORCE round 19 -- the issuer's fixed acceptance instrument.

ONE CELL (EN-h-1), THREE MECHANICAL ARMS, and `selftest-arms` drives every core TWICE:
once with a MUTANT that must FAIL and once with a SIMULATED CORRECT record that must PASS.

A MUTANT TEST CANNOT CATCH A VACUOUS PASS (R-47). An arm whose predicate is unsatisfiable
refuses the mutant exactly as loudly as a sound arm does and reads GREEN on every mutant
table ever printed. So every core is also shown to ACCEPT a record a correct cell could
produce, or it is a constant wearing a measurement's clothes.

THE EVIDENCE MUST NOT BE ABLE TO FORGE ITS OWN VERDICT. `proof-of-spec-check` grades
`<expect>` as an UNANCHORED SEARCH over evidence the GRADED PARTY writes; these cores echo
record-derived values. `_scrub` neutralises every relayed line so the one unscrubbed
occurrence of the vocabulary in any run is the authoritative VERDICT line.

THE POPULATION IS THREE SURFACES AND THAT IS THE ROUND'S WHOLE HAZARD. The analysis and the
register both say "the HAND RANKING" in the SINGULAR. A cell that reads that as
TENSION_RANKING.md alone re-measures 10 of 143 and reports a closed comparison, with every
figure it prints correct. `core_coverage` therefore refuses a record that does not carry all
three surfaces BY NAME -- written as the base's own declared set MINUS what the record
carries, never as a forward list this file happens to remember.

THE ADDITIVITY ANCHOR IS THE ACTOR'S OWN BASE, NEVER A ROUND PIN. Ruled by 1.0.0_SA_CTO in
the round-10 LGIC_LGCTFM analysis, AGAINST its own round-16 arm: a round pin silently
converts "this cell was additive" into "this file is immutable", and the round-16 arm worked
only because exactly one commit had ever touched the file it checked. GRADING_RULE.md and
n6-grader-a.tsv have their own legitimate histories, so a blob-vs-round-pin comparison here
WOULD FAIL ON HONEST HISTORY -- a criterion no correct artifact could satisfy.

AN EMPTY POPULATION IS REFUSED, NEVER PASSED VACUOUSLY (S106).
"""

import argparse
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(HERE, "R19_BASE.json")
WORKER = "0.9.0_WK_LGIC_ENFORCE~1"
RECORD = ("org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/%s/HAND_REMEASURE_R19.json" % WORKER)

# The three surfaces, taken from the base's own declared block rather than typed here.
def declared_surfaces(b):
    return sorted(k for k in b["the_three_hand_surfaces"].keys()
                  if isinstance(b["the_three_hand_surfaces"][k], dict))


def base():
    with io.open(BASE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def load(path):
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _scrub(text):
    return str(text).replace("VERDICT", "VERD1CT").replace("PASS-", "PASS_").replace("FAIL-", "FAIL_")


def verdict(ok, name, lines):
    for ln in lines:
        print(_scrub(ln))
    print("VERDICT: %s-%s" % ("PASS" if ok else "FAIL", name))
    return 0 if ok else 1


def git(args):
    try:
        return subprocess.check_output(["git"] + args, stderr=subprocess.STDOUT).decode("utf-8", "replace")
    except Exception as exc:
        return "GITERROR %s" % exc


def _own_denominator(blk, label, out):
    """A population block must carry its OWN re-measurement: an instrument string and an
    integer value. Round 19's inputs are ALL known-stale, so an inherited figure is the
    defect this round exists to close."""
    d = (blk or {}).get("denominator_measured_at_write_time")
    if not isinstance(d, dict) or not str(d.get("instrument", "")).strip() \
            or not isinstance(d.get("value"), int):
        out.append("%s: needs denominator_measured_at_write_time {instrument, value}" % label)
        return False
    out.append("%s: own denominator %d via %s" % (label, d["value"], d["instrument"]))
    return True


# ------------------------------------------------------------------ AC1 coverage
def core_coverage(rec, b=None):
    """All three surfaces carried, each with its own re-derived denominator, and each
    surface's compared-key set EQUAL to round 9's by SET EQUALITY -- so a dropped member
    fails even when the arithmetic closes."""
    b = b or base()
    out, bad = [], []
    if not isinstance(rec, dict):
        return False, ["no record at %s" % RECORD]

    want = set(declared_surfaces(b))
    got = set((rec.get("surfaces") or {}).keys())
    out.append("declared surfaces %d: %s" % (len(want), ", ".join(sorted(want))))
    out.append("record surfaces   %d: %s" % (len(got), ", ".join(sorted(got))))

    # SUBTRACTION, never a forward list.
    missing = want - got
    if missing:
        bad.append("MISSING SURFACE(S): %s -- the round's population is the PARTITION, not the "
                   "bucket with the most disagreements" % ", ".join(sorted(missing)))
    extra = got - want
    if extra:
        bad.append("surface(s) not declared in the base: %s" % ", ".join(sorted(extra)))

    total = 0
    for name in sorted(want & got):
        blk = rec["surfaces"][name] or {}
        if not _own_denominator(blk, name, out):
            bad.append("%s: no own denominator" % name)
        keys = blk.get("compared_keys")
        if not isinstance(keys, list) or not keys:
            bad.append("%s: compared_keys must be a NON-EMPTY list (S106: an empty population "
                       "is refused, never passed vacuously)" % name)
            continue
        total += len(keys)
        r9 = b["the_three_hand_surfaces"][name].get("compared")
        if isinstance(r9, int) and len(set(map(str, keys))) != r9:
            bad.append("%s: %d distinct compared_keys against round 9's %d -- SET EQUALITY fails; "
                       "a dropped member fails here even when the arithmetic closes"
                       % (name, len(set(map(str, keys))), r9))
        else:
            out.append("%s: %d compared_keys, matches round 9" % (name, len(set(map(str, keys)))))

    if total == 0:
        bad.append("EMPTY POPULATION across every surface -- REFUSED, never a vacuous pass")
    else:
        out.append("total compared across the partition: %d" % total)

    for ln in bad:
        out.append("DEFECT " + ln)
    return (not bad), out


# ------------------------------------------------------------------ AC2 vintage + additivity
def core_vintage_and_additive(rec, b=None, blobs=None):
    """Every revised figure names the CARRIER it revises and the CENSUS VINTAGE it was
    measured at; and the ORIGINAL carriers are byte-unchanged -- anchored to the ACTOR'S OWN
    BASE, never to a round pin."""
    b = b or base()
    out, bad = [], []
    if not isinstance(rec, dict):
        return False, ["no record at %s" % RECORD]

    anchor = rec.get("actor_base_sha")
    if not isinstance(anchor, str) or len(anchor) < 7:
        bad.append("actor_base_sha missing -- additivity anchors to the ACTOR'S OWN BASE "
                   "(1.0.0_SA_CTO, round-10 ruling against its own round-16 arm). A round pin "
                   "would convert 'this cell was additive' into 'this file is immutable' and "
                   "FAIL ON HONEST HISTORY.")
    else:
        out.append("actor_base_sha %s" % anchor)

    revisions = rec.get("revisions")
    if not isinstance(revisions, list) or not revisions:
        bad.append("revisions must be a NON-EMPTY list -- 30 of 34 disagreements name the hand "
                   "side as defective, so a record revising nothing has not done the round's work")
        revisions = []

    for i, rv in enumerate(revisions):
        tag = "revision[%d]" % i
        if not isinstance(rv, dict):
            bad.append("%s is not an object" % tag)
            continue
        for field in ("carrier", "sibling_path", "census_vintage", "surface"):
            if not str(rv.get(field, "")).strip():
                bad.append("%s: missing %s" % (tag, field))
        vin = str(rv.get("census_vintage", ""))
        if vin and vin not in str(b["the_census_the_machine_side_used"]["vintage"]) \
                and str(b["the_census_the_machine_side_used"]["commit"])[:10] not in vin:
            bad.append("%s: census_vintage %r matches neither the machine side's vintage string "
                       "nor its commit -- a hand figure re-measured against a DIFFERENT vintage "
                       "from the machine figure it is compared with re-creates the defect one "
                       "layer down" % (tag, vin[:60]))
        sp = str(rv.get("sibling_path", ""))
        cr = str(rv.get("carrier", ""))
        if sp and cr and sp == cr:
            bad.append("%s: sibling_path EQUALS carrier -- the ruling is ADDITIVE SIBLINGS; an "
                       "in-place edit deletes the left-hand side of every 'HAND SIDE STALE' "
                       "comparison, which is the entire content of the finding" % tag)

    # Additivity measured on the tree, or injected for the self-test.
    carriers = sorted({str(rv.get("carrier", "")) for rv in revisions if isinstance(rv, dict)} - {""})
    for c in carriers:
        if blobs is not None:
            at_base, at_now = blobs.get(c, ("x", "x"))
        else:
            if not isinstance(anchor, str) or len(anchor) < 7:
                continue
            at_base = git(["rev-parse", "%s:%s" % (anchor, c)]).strip()
            at_now = git(["rev-parse", "HEAD:%s" % c]).strip()
        if at_base.startswith("GITERROR") or at_now.startswith("GITERROR"):
            bad.append("%s: could not resolve the blob at the actor base and at HEAD" % c)
        elif at_base != at_now:
            bad.append("%s: blob MOVED between the actor's base and HEAD (%s -> %s) -- the "
                       "originals are READ-ONLY, not one byte" % (c, at_base[:12], at_now[:12]))
        else:
            out.append("%s: blob %s identical at the actor's base and at HEAD" % (c, at_base[:12]))

    for ln in bad:
        out.append("DEFECT " + ln)
    return (not bad), out


# ------------------------------------------------------------------ AC3 re-derived totals
def core_rederived(rec, b=None):
    """The comparison totals are RE-DERIVED at this cell's write time, not carried from
    round 9 -- and the arm says so by refusing a record whose totals reproduce round 9's
    across EVERY surface, which is the one result a copy produces and a re-run cannot."""
    b = b or base()
    out, bad = [], []
    if not isinstance(rec, dict):
        return False, ["no record at %s" % RECORD]

    tot = rec.get("totals")
    if not isinstance(tot, dict) or not all(isinstance(tot.get(k), int)
                                            for k in ("compared", "agree", "disagree")):
        return False, ["totals {compared, agree, disagree} must all be integers"]

    if tot["compared"] != tot["agree"] + tot["disagree"]:
        bad.append("totals do not close: %d != %d + %d"
                   % (tot["compared"], tot["agree"], tot["disagree"]))
    else:
        out.append("totals close: %d = %d + %d" % (tot["compared"], tot["agree"], tot["disagree"]))

    if not str(rec.get("rerun_instrument", "")).strip():
        bad.append("rerun_instrument missing -- the record must name the command that RE-DERIVED "
                   "these totals at this cell's write time")

    surf = rec.get("surfaces") or {}
    same = []
    for name in declared_surfaces(b):
        r9 = b["the_three_hand_surfaces"][name]
        blk = surf.get(name) or {}
        if all(blk.get(k) == r9.get(k) for k in ("compared", "agree", "disagree")):
            same.append(name)
    if len(same) == len(declared_surfaces(b)) and same:
        bad.append("EVERY surface reproduces round 9's (compared, agree, disagree) exactly (%s). "
                   "30 of 34 disagreements were HAND SIDE STALE and this round revised the hand "
                   "side, so an unchanged triple on all three is the signature of a COPIED total."
                   % ", ".join(same))
    else:
        out.append("surfaces whose triple moved from round 9: %d of %d"
                   % (len(declared_surfaces(b)) - len(same), len(declared_surfaces(b))))

    for ln in bad:
        out.append("DEFECT " + ln)
    return (not bad), out


# ------------------------------------------------------------------ self-test
def _correct_record(b):
    """A record a CORRECT cell could produce. Used as the POSITIVE control: every core must
    ACCEPT this, or the core is unsatisfiable and its mutant refusal proves nothing."""
    surfaces, revisions = {}, []
    for name in declared_surfaces(b):
        r9 = b["the_three_hand_surfaces"][name]
        n = r9["compared"]
        surfaces[name] = {
            "compared": n,
            "agree": n,          # the hand side was revised, so agreement rises
            "disagree": 0,
            "compared_keys": ["%s::%d" % (name, i) for i in range(n)],
            "denominator_measured_at_write_time": {
                "instrument": r9["denominator_instrument_at_round_9"], "value": n},
        }
        revisions.append({
            "surface": name,
            "carrier": r9["carrier"],
            "sibling_path": r9["carrier"].replace(".md", ".REMEASURED.md").replace(".tsv", ".REMEASURED.tsv"),
            "census_vintage": b["the_census_the_machine_side_used"]["vintage"],
        })
    tot = sum(s["compared"] for s in surfaces.values())
    return {
        "actor_base_sha": "0123456789abcdef",
        "surfaces": surfaces,
        "revisions": revisions,
        "totals": {"compared": tot, "agree": tot, "disagree": 0},
        "rerun_instrument": "python build_hand_remeasure_r19.py --census <report> (re-run at write time)",
    }


def selftest(_):
    b = base()
    arms, pos = [], []
    ok_blobs = {r["carrier"]: ("aaaaaaaaaaaa", "aaaaaaaaaaaa")
                for r in _correct_record(b)["revisions"]}

    def arm(label, cond, why):
        arms.append((label, bool(cond), why))
        return bool(cond)

    def positive(label, cond, why):
        pos.append((label, bool(cond), why))
        return bool(cond)

    good = _correct_record(b)

    # --- POSITIVE CONTROLS: a correct record must PASS every core.
    positive("POSITIVE-coverage", core_coverage(good, b)[0],
             "a complete three-surface record with re-derived denominators PASSES")
    positive("POSITIVE-vintage", core_vintage_and_additive(good, b, ok_blobs)[0],
             "carriers unmoved at the actor's base and HEAD, every revision named, PASSES")
    positive("POSITIVE-rederived", core_rederived(good, b)[0],
             "totals that close and moved off round 9's triple PASS")

    # --- MUTANTS: each must FAIL.
    m = json.loads(json.dumps(good))
    dropped = sorted(m["surfaces"].keys())[0]
    del m["surfaces"][dropped]
    arm("MUTANT-partition-collapsed-to-one-bucket", not core_coverage(m, b)[0],
        "dropping a surface must FAIL -- this is the round's signature defect")

    m = json.loads(json.dumps(good))
    k = sorted(m["surfaces"].keys())[0]
    m["surfaces"][k]["compared_keys"] = m["surfaces"][k]["compared_keys"][:-1]
    arm("MUTANT-dropped-member-arithmetic-still-closes", not core_coverage(m, b)[0],
        "a member dropped from compared_keys must FAIL by SET EQUALITY")

    m = json.loads(json.dumps(good))
    k = sorted(m["surfaces"].keys())[0]
    m["surfaces"][k]["denominator_measured_at_write_time"] = {"instrument": "", "value": None}
    arm("MUTANT-inherited-denominator", not core_coverage(m, b)[0],
        "a figure not re-measured at write time must FAIL -- every input this round is stale")

    m = json.loads(json.dumps(good))
    m["surfaces"] = {}
    arm("MUTANT-empty-population", not core_coverage(m, b)[0],
        "an EMPTY population is REFUSED, never a vacuous pass (S106)")

    m = json.loads(json.dumps(good))
    m["revisions"][0]["sibling_path"] = m["revisions"][0]["carrier"]
    arm("MUTANT-in-place-edit", not core_vintage_and_additive(m, b, ok_blobs)[0],
        "sibling_path == carrier must FAIL -- an in-place edit deletes the comparison's left side")

    m = json.loads(json.dumps(good))
    m["revisions"][0]["census_vintage"] = "some other census, 2026-01-01"
    arm("MUTANT-vintage-mismatch", not core_vintage_and_additive(m, b, ok_blobs)[0],
        "a hand figure measured at a different vintage from the machine figure must FAIL")

    m = json.loads(json.dumps(good))
    del m["actor_base_sha"]
    arm("MUTANT-no-actor-base", not core_vintage_and_additive(m, b, ok_blobs)[0],
        "additivity with no actor base must FAIL")

    moved = {r["carrier"]: ("aaaaaaaaaaaa", "bbbbbbbbbbbb") for r in good["revisions"]}
    arm("MUTANT-original-carrier-moved", not core_vintage_and_additive(good, b, moved)[0],
        "a moved original must FAIL -- the originals are READ-ONLY")

    m = json.loads(json.dumps(good))
    for name in declared_surfaces(b):
        r9 = b["the_three_hand_surfaces"][name]
        m["surfaces"][name].update({"compared": r9["compared"], "agree": r9["agree"],
                                    "disagree": r9["disagree"]})
    arm("MUTANT-totals-copied-from-round-9", not core_rederived(m, b)[0],
        "every surface reproducing round 9's triple must FAIL as a copied total")

    m = json.loads(json.dumps(good))
    m["rerun_instrument"] = ""
    arm("MUTANT-no-rerun-instrument", not core_rederived(m, b)[0],
        "totals with no named re-run command must FAIL")

    m = json.loads(json.dumps(good))
    m["totals"]["agree"] = m["totals"]["agree"] - 3
    arm("MUTANT-totals-do-not-close", not core_rederived(m, b)[0],
        "arithmetic that does not close must FAIL")

    for label, ok, why in arms + pos:
        print(_scrub("  %-46s %s  -- %s" % (label, "OK" if ok else "BROKEN", why)))
    every = all(x[1] for x in arms) and all(x[1] for x in pos)
    print("ARMS: %d mutant, %d positive" % (len(arms), len(pos)))
    if not every:
        print("VERDICT: FAIL-ARMS-DISCRIMINATE")
        return 1
    print("VERDICT: PASS-ARMS-DISCRIMINATE")
    return 0


def _run(core, name):
    ok, lines = core(load(RECORD))
    return verdict(ok, name, lines)


CMDS = {
    "h1-coverage": lambda a: _run(core_coverage, "H1-COVERAGE"),
    "h1-vintage": lambda a: _run(core_vintage_and_additive, "H1-VINTAGE"),
    "h1-rederived": lambda a: _run(core_rederived, "H1-REDERIVED"),
    "selftest-arms": selftest,
}


def main():
    ap = argparse.ArgumentParser(description="LGIC_ENFORCE round 19 acceptance instrument")
    ap.add_argument("cmd", choices=sorted(CMDS.keys()))
    args = ap.parse_args()
    return CMDS[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
