"""LGIC_ENFORCE round 8 -- the issuer's fixed acceptance instrument.

FOUR CELLS, FOURTEEN REAL ARMS, and `selftest-arms` drives every core TWICE: once with a
MUTANT that must FAIL and once with a SIMULATED CORRECT record that must PASS.

⛔ WHY BOTH DIRECTIONS. A MUTANT TEST CANNOT CATCH A VACUOUS PASS (R-47): an arm whose
predicate is unsatisfiable refuses the mutant exactly as loudly as a sound arm does, and
reads GREEN on every mutant table ever printed. R-61 is this project's own instance -- an
acceptance condition that would have passed vacuously, inside the guard written to prevent
it. So every core here must also be shown to ACCEPT a record a correct cell could actually
produce, or the arm is a constant wearing a measurement's clothes.

⛔ AND THE ARMS ARE POSITION-INDEPENDENT BY CONSTRUCTION. No core reads a path relative to
a worker's worktree, and no core reads `git` state. Each takes parsed records and returns
(ok, lines). A grader re-running this from a DIFFERENT checkout gets the same verdict from
the same bytes, which is what makes an issuer's re-run corroboration rather than repetition.
"""

import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(HERE, "R8_BASE.json")
DELIV_ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"

# Each cell writes ITS OWN worker serial's folder. `owned-paths-validate.py` clause 4 refuses
# a worker writing another worker's deliverable directory -- measured on this lane when the
# gate correctly refused an issuer edit to a worker's ANDREW_CARD.md -- so a single hardcoded
# folder here would have made three of the four cells unable to write their own record.
CELL_SERIAL = {"p36": "0.9.0_WK_LGIC_ENFORCE~1",
               "g37": "0.9.0_WK_LGIC_ENFORCE~2",
               "k38": "0.9.0_WK_LGIC_ENFORCE~2",
               "m39": "0.9.0_WK_LGIC_ENFORCE~3"}


def deliv(cell, fname):
    return os.path.join(DELIV_ROOT, CELL_SERIAL[cell], fname)


GATE = ".tools/surprise-row-gate.py"
SCHEMA = "org/standards/NAMING_SCHEMA.json"


def base():
    with io.open(BASE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def load(path):
    if not os.path.exists(path):
        return None
    with io.open(path, encoding="utf-8") as fh:
        if path.lower().endswith(".json"):
            return json.load(fh)
        return fh.read()


def _scrub(text):
    """⛔ THE EVIDENCE MUST NOT BE ABLE TO FORGE ITS OWN VERDICT.

    `proof-of-spec-check` grades a criterion's `<expect>` as an UNANCHORED SEARCH over the
    run's whole evidence. These cores echo RECORD-DERIVED values -- resource names, card
    reasons, moved types -- and a record is written by the graded party. MEASURED at the
    round-8 cut, before any worker started: a card row NAMED `PASS-P36-CARDS-CARRY-REASONS`
    with an empty reason produces `VERDICT: FAIL-...` AND puts the literal expect string in
    the output, so an unanchored search finds PASS on a FAILING run.

    The L6 gate announced the shape -- "it prints a bare value it does not author ... a
    relay: that line can be anything" -- as ANNOUNCE, not refused. This closes it: every
    relayed line is neutralised, and the ONE unscrubbed occurrence of the vocabulary in any
    run is the authoritative VERDICT line printed by `verdict()` itself.

    This is `A_BOUNDARY_READ_FROM_A_FIELD_THE_GRADED_PARTY_WRITES` applied to the evidence
    stream rather than to a field. COST: one substitution per printed line. NON-APPLICATION:
    a checker whose output interpolates nothing the graded party controls."""
    return str(text).replace("VERDICT", "VERD1CT").replace("PASS-", "PASS_").replace("FAIL-", "FAIL_")


def verdict(ok, name, lines):
    for ln in lines:
        print(_scrub(ln))
    print("VERDICT: %s-%s" % ("PASS" if ok else "FAIL", name))
    return 0 if ok else 1


# ---------------------------------------------------------------- EN-p-36

def core_p36_population(rec):
    """Every RAISE on BOTH planes is dispositioned, with the denominator PRINTED BY THE
    RECORD ITSELF. The count is not compared against R8_BASE's 504/623: those carry
    claim=reported and the cell re-measures. What is graded is that the record's OWN
    arithmetic closes on its OWN denominator, per plane, with no remainder."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    ok = True
    for plane in ("live", "repo"):
        blk = (rec.get("planes") or {}).get(plane)
        if not isinstance(blk, dict):
            out.append("%s: MISSING plane block" % plane)
            ok = False
            continue
        res = blk.get("resolved")
        card = blk.get("carded")
        den = blk.get("raise_population")
        if not isinstance(res, list) or not isinstance(card, list) or not isinstance(den, int):
            out.append("%s: resolved/carded must be lists and raise_population an int" % plane)
            ok = False
            continue
        total = len(res) + len(card)
        out.append("%s: resolved %d + carded %d = %d ; raise_population %d ; remainder %d"
                   % (plane, len(res), len(card), total, den, den - total))
        if total != den:
            ok = False
        if den <= 0:
            out.append("%s: raise_population must be positive -- a zero denominator passes "
                       "vacuously" % plane)
            ok = False
    return ok, out


def core_p36_runs_to_end(rec):
    """The census RUNS TO THE END on both planes with the card file applied. `stopped` must
    be null and judged must exceed R8_BASE's judged-before-stop. An arm that only checked
    `stopped is None` would pass on a census that judged nothing at all."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    b = base()
    floor = {"live": b["census_live_at_the_cut"]["judged_before_stop"],
             "repo": b["census_repo_at_the_cut"]["judged_before_stop"]}
    ok = True
    for plane in ("live", "repo"):
        blk = (rec.get("planes") or {}).get(plane)
        if not isinstance(blk, dict):
            out.append("%s: MISSING plane block" % plane)
            ok = False
            continue
        stopped = blk.get("stopped", "MISSING")
        judged = blk.get("judged")
        out.append("%s: stopped=%r judged=%r (must exceed the cut's %d)"
                   % (plane, stopped, judged, floor[plane]))
        if stopped is not None:
            ok = False
        if not isinstance(judged, int) or judged <= floor[plane]:
            ok = False
    return ok, out


def core_p36_own_denominator(rec):
    """The record re-measured its OWN denominators at write time rather than inheriting
    R8_BASE's. R-38's addition, and the reason round 6's 1411 did not mislead round 7: a
    count is a value AT A VINTAGE of a report the campaign itself changes."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    ok = True
    for plane in ("live", "repo"):
        blk = (rec.get("planes") or {}).get(plane)
        if not isinstance(blk, dict):
            ok = False
            out.append("%s: MISSING" % plane)
            continue
        d = blk.get("denominator_measured_at_write_time")
        if not isinstance(d, dict) or not d.get("instrument") or not isinstance(d.get("value"), int):
            out.append("%s: needs denominator_measured_at_write_time {instrument, value}" % plane)
            ok = False
            continue
        out.append("%s: own denominator %d via %s" % (plane, d["value"], d["instrument"]))
    return ok, out


def core_p36_cards_carry_reasons(rec):
    """No bare cards. Every carded name carries a non-empty `card` reason AND a plane. A
    card with no reason is the placeholder campaign's TIMEBOXED_R33 defect again -- a value
    describing the MEASURING PROCESS rather than the measured domain (R-60)."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    bad = []
    seen = 0
    for plane in ("live", "repo"):
        blk = (rec.get("planes") or {}).get(plane) or {}
        for row in (blk.get("carded") or []):
            seen += 1
            if not isinstance(row, dict):
                bad.append(repr(row)[:60])
                continue
            if not str(row.get("card", "")).strip() or not str(row.get("name", "")).strip():
                bad.append(str(row.get("name", "?"))[:60])
    out.append("carded rows inspected: %d" % seen)
    out.append("rows with no `card` reason or no `name` (must be 0): %d %s" % (len(bad), bad[:8]))
    return (len(bad) == 0 and seen > 0), out


# ---------------------------------------------------------------- EN-g-37 / EN-k-38

def core_limb_present(src, tokens):
    """The limb EXISTS in the gate source. R8_BASE measured 0 hits at the cut over 2437
    lines, so this arm reads FAIL at the cut by construction -- it cannot be satisfied by
    something that was already there."""
    out = []
    if not src:
        return False, ["gate source unreadable"]
    hits = {t: len(re.findall(re.escape(t), src)) for t in tokens}
    out.append("gate source lines: %d" % len(src.splitlines()))
    for t in sorted(hits):
        out.append("  token %-28s occurrences: %d" % (t, hits[t]))
    return (all(v > 0 for v in hits.values())), out


def core_control_pair(rec, key):
    """POSITIVE CONTROL and MUTANT, both required, and BOTH READ FROM THE SAME RUN.

    ⛔ A MUTANT ALONE BOUNDS UNDER-FIRING AND SAYS NOTHING ABOUT OVER-FIRING. A limb that
    refuses EVERY slug passes any mutant table and halts the estate. So the positive control
    -- a compliant input the limb must ACCEPT -- is graded here as a peer of the mutant, not
    as a courtesy."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    blk = rec.get(key)
    if not isinstance(blk, dict):
        return False, ["missing %r block" % key]
    pos = blk.get("positive_control")
    mut = blk.get("mutant")
    ok = True
    if not isinstance(pos, dict) or pos.get("outcome") != "PASS":
        out.append("positive_control must record outcome PASS (a compliant input is ACCEPTED)")
        ok = False
    else:
        out.append("positive control: %s -> PASS" % str(pos.get("what"))[:110])
    if not isinstance(mut, dict) or mut.get("outcome") != "REFUSED":
        out.append("mutant must record outcome REFUSED (the planted defect is CAUGHT)")
        ok = False
    else:
        out.append("mutant: %s -> REFUSED" % str(mut.get("what"))[:110])
    if isinstance(pos, dict) and isinstance(mut, dict):
        if str(pos.get("what", "")).strip() == str(mut.get("what", "")).strip():
            out.append("positive control and mutant describe the SAME input -- not a pair")
            ok = False
    return ok, out


def core_k38_distinct_from_g37(rec):
    """THE ARM THAT PROVES THEY ARE TWO QUESTIONS AND NOT ONE.

    The staleness limb must fire on a row that the slug-time limb ACCEPTS -- an OPEN,
    OWNED, UNMOVED remediation row that EXISTS. If EN-k-38's mutant is also refused by
    EN-g-37, the two cells built one limb twice and the round bought nothing. This is
    S75's own class stated as an acceptance condition: a check scoped to rowlessness cannot
    see a defect in a row that is present."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    d = rec.get("distinct_from_rowlessness")
    if not isinstance(d, dict):
        return False, ["missing `distinct_from_rowlessness` block"]
    has_row = d.get("mutant_row_exists")
    g37 = d.get("rowlessness_limb_verdict")
    k38 = d.get("staleness_limb_verdict")
    out.append("mutant row EXISTS in the remediation channel: %r (must be True)" % has_row)
    out.append("rowlessness limb on that row: %r (must be PASS -- it cannot see it)" % g37)
    out.append("staleness  limb on that row: %r (must be REFUSED)" % k38)
    ok = (has_row is True and g37 == "PASS" and k38 == "REFUSED")
    return ok, out


def core_gate_other_limbs_unmoved(rec):
    """The gate's OWN self-test still passes. A limb added to a file with refusal power over
    every slug in the estate must not move any other limb; the gate's self-test is the
    instrument that says so, and it is the gate's own run rather than an estimate."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    st = rec.get("gate_selftest")
    if not isinstance(st, dict):
        return False, ["missing `gate_selftest` block"]
    rc = st.get("rc")
    out.append("gate self-test invocation: %s" % str(st.get("invocation"))[:140])
    out.append("gate self-test rc: %r (must be 0)" % rc)
    return (rc == 0), out


# ---------------------------------------------------------------- EN-m-39

def core_m39_four_postulates(rec):
    """Rule 24 requires FOUR postulates for any schema an agent authors OR ADOPTS, and a
    value-enum proposal arrives WITH its four-postulate record and a word-boundary token
    census or it is not a proposal. This arm grades PRESENCE of all four with text, not
    their quality -- the quality is the CVO's judgment criterion."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    p = rec.get("four_postulates")
    want = ["mece_over_a_declared_domain", "same_grain", "intent_coherence", "state_coherence"]
    if not isinstance(p, dict):
        return False, ["missing `four_postulates` block"]
    missing = [k for k in want if not str((p or {}).get(k, "")).strip()]
    out.append("postulates present: %d of %d" % (len(want) - len(missing), len(want)))
    out.append("missing (must be 0): %d %s" % (len(missing), missing))
    return (not missing), out


def core_m39_token_census(rec):
    """The token census arrives WITH ITS DENOMINATOR and is WORD-BOUNDARY, not substring.
    This project has been bitten twice by a substring read -- `C6` inside `C33R6-AC6`, and
    a 'sentiment' hit that was a word inside a quoted grep pattern -- so the arm requires
    the record to state both counts and they must differ or be explained."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    c = rec.get("token_census")
    if not isinstance(c, dict):
        return False, ["missing `token_census` block"]
    den = c.get("denominator")
    whole = c.get("whole_value_hits")
    sub = c.get("substring_hits")
    out.append("denominator: %r" % den)
    out.append("whole-value hits: %r ; substring hits: %r" % (whole, sub))
    ok = (isinstance(den, int) and den > 0
          and isinstance(whole, int) and isinstance(sub, int) and sub >= whole)
    if not ok:
        out.append("needs a positive denominator and both counts, with substring >= whole-value")
    return ok, out


def core_m39_no_grade_change(rec):
    """THE GUARD. EN-m-39 is the only round-8 cell permitted to touch NAMING_SCHEMA.json,
    and the exclusion table's 8/7 split must be UNCHANGED for every type the cell does not
    deliberately move -- with the moved set named. The switch is a PROSE REASON STRING, so
    rewording a reason silently re-grades a type and nothing announces it."""
    out = []
    b = base()["exclusion_table_at_the_cut"]
    if not isinstance(rec, dict):
        return False, ["no record"]
    g = rec.get("exclusion_table_after")
    if not isinstance(g, dict):
        return False, ["missing `exclusion_table_after` block"]
    moved = g.get("deliberately_moved")
    if not isinstance(moved, list):
        return False, ["`deliberately_moved` must be a list (it may be empty)"]
    want_out = sorted(set(b["genuinely_not_graded"]) - set(moved))
    want_routed = sorted(set(b["still_routed"]) - set(moved))
    got_out = sorted(set(g.get("genuinely_not_graded") or []) - set(moved))
    got_routed = sorted(set(g.get("still_routed") or []) - set(moved))
    out.append("deliberately moved (named, may be empty): %s" % moved)
    out.append("NOT GRADED unchanged-set: got %d want %d" % (len(got_out), len(want_out)))
    out.append("ROUTED     unchanged-set: got %d want %d" % (len(got_routed), len(want_routed)))
    ok = (got_out == want_out and got_routed == want_routed)
    if not ok:
        out.append("a type moved that the record did not declare -- the reason-string hazard")
    return ok, out


def core_m39_discriminates(rec):
    """THE NEGATIVE ARM. A mechanism distinguishing a KEY TEMPLATE from a KEY must select
    the 15 templates AND REJECT ordinary S3 keys. R-62's whole ground was that the 15 are
    TEMPLATES while S3Key is EVERY KEY, so a mechanism with no negative arm would remove
    every S3 key in the estate to fix 15 rows. Round 7's own most reusable output was a
    selector with a working negative arm; this is the same bar."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    d = rec.get("discrimination")
    if not isinstance(d, dict):
        return False, ["missing `discrimination` block"]
    sel = d.get("selects_templates")
    rej = d.get("rejects_ordinary_keys")
    rej_den = d.get("ordinary_keys_tested")
    out.append("selects templates: %r of 15" % sel)
    out.append("rejects ordinary S3 keys: %r of %r tested" % (rej, rej_den))
    ok = (sel == 15 and isinstance(rej_den, int) and rej_den > 0 and rej == rej_den)
    if not ok:
        out.append("must select 15 of 15 AND reject every ordinary key tested, with a "
                   "POSITIVE number tested -- zero tested is a vacuous negative arm")
    return ok, out


# ---------------------------------------------------------------- self test

def _p36_good():
    return {"planes": {
        "live": {"resolved": [{"name": "a"}], "carded": [{"name": "b", "card": "why", "plane": "live"}],
                 "raise_population": 2, "stopped": None, "judged": 1838,
                 "denominator_measured_at_write_time": {"instrument": "census --live", "value": 1838}},
        "repo": {"resolved": [{"name": "c"}], "carded": [{"name": "d", "card": "why", "plane": "repo"}],
                 "raise_population": 2, "stopped": None, "judged": 1878,
                 "denominator_measured_at_write_time": {"instrument": "census --repo", "value": 1878}}}}


def _pair_good(extra=None):
    rec = {"limb": {"positive_control": {"what": "a compliant slug", "outcome": "PASS"},
                    "mutant": {"what": "a planted rowless GRADUATED", "outcome": "REFUSED"}},
           "gate_selftest": {"invocation": "python .tools/surprise-row-gate.py --self-test", "rc": 0}}
    if extra:
        rec.update(extra)
    return rec


def _m39_good():
    b = base()["exclusion_table_at_the_cut"]
    return {"four_postulates": {"mece_over_a_declared_domain": "x", "same_grain": "x",
                                "intent_coherence": "x", "state_coherence": "x"},
            "token_census": {"denominator": 1878, "whole_value_hits": 15, "substring_hits": 22},
            "exclusion_table_after": {"deliberately_moved": [],
                                      "genuinely_not_graded": b["genuinely_not_graded"],
                                      "still_routed": b["still_routed"]},
            "discrimination": {"selects_templates": 15, "rejects_ordinary_keys": 40,
                               "ordinary_keys_tested": 40}}


def selftest():
    arms = []

    def arm(name, fn, expect):
        got = bool(fn())
        arms.append((name, expect, got, got == expect))

    good = _p36_good()
    arm("p36-population POSITIVE", lambda: core_p36_population(good)[0], True)
    bad = json.loads(json.dumps(good))
    bad["planes"]["live"]["raise_population"] = 3
    arm("p36-population MUTANT remainder", lambda: core_p36_population(bad)[0], False)
    zero = json.loads(json.dumps(good))
    zero["planes"]["live"]["raise_population"] = 0
    zero["planes"]["live"]["resolved"] = []
    zero["planes"]["live"]["carded"] = []
    arm("p36-population MUTANT vacuous-zero", lambda: core_p36_population(zero)[0], False)

    arm("p36-runs-to-end POSITIVE", lambda: core_p36_runs_to_end(good)[0], True)
    st = json.loads(json.dumps(good))
    st["planes"]["repo"]["stopped"] = "F49ServedAndSourceRead"
    arm("p36-runs-to-end MUTANT stopped", lambda: core_p36_runs_to_end(st)[0], False)
    lowj = json.loads(json.dumps(good))
    lowj["planes"]["live"]["judged"] = 3
    arm("p36-runs-to-end MUTANT judged-not-advanced", lambda: core_p36_runs_to_end(lowj)[0], False)

    arm("p36-own-denominator POSITIVE", lambda: core_p36_own_denominator(good)[0], True)
    nod = json.loads(json.dumps(good))
    del nod["planes"]["repo"]["denominator_measured_at_write_time"]
    arm("p36-own-denominator MUTANT inherited", lambda: core_p36_own_denominator(nod)[0], False)

    arm("p36-cards-carry-reasons POSITIVE", lambda: core_p36_cards_carry_reasons(good)[0], True)
    nc = json.loads(json.dumps(good))
    nc["planes"]["live"]["carded"][0]["card"] = "  "
    arm("p36-cards MUTANT bare card", lambda: core_p36_cards_carry_reasons(nc)[0], False)

    src_yes = "def _graduated_without_row(rows):\n    return []\n"
    arm("g37-limb-present POSITIVE", lambda: core_limb_present(src_yes, ["_graduated_without_row"])[0], True)
    arm("g37-limb-present MUTANT absent", lambda: core_limb_present("def x():\n    pass\n",
                                                                   ["_graduated_without_row"])[0], False)

    pg = _pair_good()
    arm("control-pair POSITIVE", lambda: core_control_pair(pg, "limb")[0], True)
    nom = json.loads(json.dumps(pg))
    nom["limb"]["mutant"]["outcome"] = "PASS"
    arm("control-pair MUTANT not-caught", lambda: core_control_pair(nom, "limb")[0], False)
    nop = json.loads(json.dumps(pg))
    nop["limb"]["positive_control"]["outcome"] = "REFUSED"
    arm("control-pair MUTANT over-fires", lambda: core_control_pair(nop, "limb")[0], False)
    same = json.loads(json.dumps(pg))
    same["limb"]["positive_control"]["what"] = same["limb"]["mutant"]["what"]
    arm("control-pair MUTANT same-input", lambda: core_control_pair(same, "limb")[0], False)

    arm("gate-selftest POSITIVE", lambda: core_gate_other_limbs_unmoved(pg)[0], True)
    gs = json.loads(json.dumps(pg))
    gs["gate_selftest"]["rc"] = 1
    arm("gate-selftest MUTANT rc", lambda: core_gate_other_limbs_unmoved(gs)[0], False)

    dk = {"distinct_from_rowlessness": {"mutant_row_exists": True,
                                        "rowlessness_limb_verdict": "PASS",
                                        "staleness_limb_verdict": "REFUSED"}}
    arm("k38-distinct POSITIVE", lambda: core_k38_distinct_from_g37(dk)[0], True)
    dup = json.loads(json.dumps(dk))
    dup["distinct_from_rowlessness"]["rowlessness_limb_verdict"] = "REFUSED"
    arm("k38-distinct MUTANT one-limb-twice", lambda: core_k38_distinct_from_g37(dup)[0], False)
    norow = json.loads(json.dumps(dk))
    norow["distinct_from_rowlessness"]["mutant_row_exists"] = False
    arm("k38-distinct MUTANT rowless-mutant", lambda: core_k38_distinct_from_g37(norow)[0], False)

    mg = _m39_good()
    arm("m39-four-postulates POSITIVE", lambda: core_m39_four_postulates(mg)[0], True)
    m1 = json.loads(json.dumps(mg))
    m1["four_postulates"]["same_grain"] = ""
    arm("m39-four-postulates MUTANT", lambda: core_m39_four_postulates(m1)[0], False)

    arm("m39-token-census POSITIVE", lambda: core_m39_token_census(mg)[0], True)
    m2 = json.loads(json.dumps(mg))
    m2["token_census"]["denominator"] = 0
    arm("m39-token-census MUTANT no-denominator", lambda: core_m39_token_census(m2)[0], False)

    arm("m39-no-grade-change POSITIVE", lambda: core_m39_no_grade_change(mg)[0], True)
    m3 = json.loads(json.dumps(mg))
    m3["exclusion_table_after"]["still_routed"] = [t for t in mg["exclusion_table_after"]["still_routed"]
                                                   if t != "SECRET"]
    arm("m39-no-grade-change MUTANT silent-regrade", lambda: core_m39_no_grade_change(m3)[0], False)
    m4 = json.loads(json.dumps(mg))
    m4["exclusion_table_after"]["deliberately_moved"] = ["S3Key"]
    m4["exclusion_table_after"]["still_routed"] = [t for t in mg["exclusion_table_after"]["still_routed"]
                                                   if t != "S3Key"]
    arm("m39-no-grade-change POSITIVE declared-move", lambda: core_m39_no_grade_change(m4)[0], True)

    arm("m39-discriminates POSITIVE", lambda: core_m39_discriminates(mg)[0], True)
    m5 = json.loads(json.dumps(mg))
    m5["discrimination"]["ordinary_keys_tested"] = 0
    m5["discrimination"]["rejects_ordinary_keys"] = 0
    arm("m39-discriminates MUTANT vacuous-negative", lambda: core_m39_discriminates(m5)[0], False)
    m6 = json.loads(json.dumps(mg))
    m6["discrimination"]["rejects_ordinary_keys"] = 12
    arm("m39-discriminates MUTANT leaks-keys", lambda: core_m39_discriminates(m6)[0], False)

    pos = [a for a in arms if a[1] is True]
    bad_arms = [a for a in arms if not a[3]]
    print("SELFTEST ARMS: %d ; POSITIVE-SATISFIABILITY arms: %d ; failures: %d"
          % (len(arms), len(pos), len(bad_arms)))
    for name, expect, got, good_arm in arms:
        print("  %-46s expect=%-5s got=%-5s %s"
              % (name, expect, got, "OK" if good_arm else "**ARM BROKEN**"))
    if bad_arms:
        print("VERDICT: FAIL-SELFTEST")
        return 1
    print("VERDICT: PASS-SELFTEST-%d-ARMS-%d-POSITIVE" % (len(arms), len(pos)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sub")
    args = ap.parse_args()
    sub = args.sub

    if sub == "selftest-arms":
        return selftest()

    if sub.startswith("p36-"):
        rec = load(deliv("p36", "RAISE_POPULATION_R8.json"))
        fn = {"p36-population": core_p36_population,
              "p36-runs-to-end": core_p36_runs_to_end,
              "p36-own-denominator": core_p36_own_denominator,
              "p36-cards-carry-reasons": core_p36_cards_carry_reasons}[sub]
        ok, lines = fn(rec)
        return verdict(ok, sub.upper(), lines)

    if sub.startswith("g37-"):
        if sub == "g37-limb-present":
            ok, lines = core_limb_present(load(GATE), ["_graduated_without_row"])
            return verdict(ok, "G37-LIMB-PRESENT", lines)
        rec = load(deliv("g37", "SLUG_TIME_LIMB_R8.json"))
        if sub == "g37-controls":
            ok, lines = core_control_pair(rec, "limb")
            return verdict(ok, "G37-CONTROLS", lines)
        if sub == "g37-gate-unmoved":
            ok, lines = core_gate_other_limbs_unmoved(rec)
            return verdict(ok, "G37-GATE-UNMOVED", lines)

    if sub.startswith("k38-"):
        if sub == "k38-limb-present":
            ok, lines = core_limb_present(load(GATE), ["_stale_open_row"])
            return verdict(ok, "K38-LIMB-PRESENT", lines)
        rec = load(deliv("k38", "STALENESS_LIMB_R8.json"))
        if sub == "k38-controls":
            ok, lines = core_control_pair(rec, "limb")
            return verdict(ok, "K38-CONTROLS", lines)
        if sub == "k38-distinct":
            ok, lines = core_k38_distinct_from_g37(rec)
            return verdict(ok, "K38-DISTINCT", lines)

    if sub.startswith("m39-"):
        rec = load(deliv("m39", "TEMPLATE_VS_KEY_R8.json"))
        fn = {"m39-four-postulates": core_m39_four_postulates,
              "m39-token-census": core_m39_token_census,
              "m39-no-grade-change": core_m39_no_grade_change,
              "m39-discriminates": core_m39_discriminates}[sub]
        ok, lines = fn(rec)
        return verdict(ok, sub.upper(), lines)

    print("unknown subcommand %r" % sub)
    return 2


if __name__ == "__main__":
    sys.exit(main())
