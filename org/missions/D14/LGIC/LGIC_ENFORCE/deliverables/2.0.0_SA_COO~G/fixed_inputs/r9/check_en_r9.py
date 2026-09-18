"""LGIC_ENFORCE round 9 -- the issuer's fixed acceptance instrument.

THREE CELLS, TWELVE REAL ARMS, and `selftest-arms` drives every core TWICE: once with a
MUTANT that must FAIL and once with a SIMULATED CORRECT record that must PASS.

⛔ A MUTANT TEST CANNOT CATCH A VACUOUS PASS (R-47). An arm whose predicate is unsatisfiable
refuses the mutant exactly as loudly as a sound arm does and reads GREEN on every mutant
table ever printed. So every core must also be shown to ACCEPT a record a correct cell could
produce, or it is a constant wearing a measurement's clothes.

⛔ AND ROUND 8 ADDED A SECOND BAR THIS FILE CARRIES FROM THE START (S82): a control that
proves a gate DISCRIMINATES says nothing about the SIZE of the set it fires on. Where a cell
here produces a population, its arm requires the DENOMINATOR RE-MEASURED AT THE CELL'S OWN
WRITE TIME -- because two of round 9's own input figures (43 worked cases, 91 stale rows)
were ALREADY STALE at the cut, measured at 45 and 94.

⛔ AND THE EVIDENCE MUST NOT BE ABLE TO FORGE ITS OWN VERDICT. `proof-of-spec-check` grades
`<expect>` as an UNANCHORED SEARCH over evidence the GRADED PARTY writes; these cores echo
record-derived values. `_scrub` neutralises every relayed line so the one unscrubbed
occurrence of the vocabulary in any run is the authoritative VERDICT line. Measured at the
round-8 cut before any worker started: a row NAMED `PASS-...` produced a FAIL verdict and
put the literal expect string in the evidence anyway.
"""

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.join(HERE, "R9_BASE.json")
DELIV_ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"

CELL_SERIAL = {"c40": "0.9.0_WK_LGIC_ENFORCE~1",
               "s41": "0.9.0_WK_LGIC_ENFORCE~2",
               "b42": "0.9.0_WK_LGIC_ENFORCE~3"}


def deliv(cell, fname):
    return os.path.join(DELIV_ROOT, CELL_SERIAL[cell], fname)


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


def _own_denominator(blk, label, out):
    """A population block must carry its OWN re-measurement: an instrument string and an
    integer value. R-38's addition, and round 9's two stale inputs are why it is an arm
    rather than a convention."""
    d = (blk or {}).get("denominator_measured_at_write_time")
    if not isinstance(d, dict) or not str(d.get("instrument", "")).strip() \
            or not isinstance(d.get("value"), int):
        out.append("%s: needs denominator_measured_at_write_time {instrument, value}" % label)
        return False
    out.append("%s: own denominator %d via %s" % (label, d["value"], d["instrument"]))
    return True


# ---------------------------------------------------------------- EN-c-40

def core_c40_recount(rec):
    """THE ARM THAT EXISTS BECAUSE THE REGISTER'S FIGURE IS WRONG. The register and the
    round-8 analysis both say section 9 carries 43 worked cases; the issuer parsed the fence
    and got 45. The cell RE-COUNTS at its own write time and PRINTS the denominator, and
    whichever number it gets, it states which carrier is stale. An arm that accepted 43
    unexamined would have propagated the error into the comparison's own population."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    w = rec.get("worked_cases")
    if not isinstance(w, dict):
        return False, ["missing `worked_cases` block"]
    ok = _own_denominator(w, "worked_cases", out)
    n = w.get("counted")
    reg = base()["the_three_instruments_for_EN_c_40"]["GRADING_RULE.md"]["worked_cases_cited"]
    iss = base()["the_three_instruments_for_EN_c_40"]["GRADING_RULE.md"]["worked_cases_MEASURED"]
    out.append("cell counted: %r | register cites %d | issuer measured %d" % (n, reg, iss))
    if not isinstance(n, int) or n <= 0:
        out.append("counted must be a POSITIVE int -- a zero count passes vacuously")
        ok = False
    stale = str(w.get("which_carrier_is_stale", "")).strip()
    if not stale:
        out.append("must NAME which carrier is stale given its own count")
        ok = False
    else:
        out.append("names the stale carrier: %s" % stale[:110])
    return ok, out


def core_c40_population(rec):
    """The comparison covers all THREE surfaces with a denominator each. Clause 3 is
    'totals agree with the hand ranking' -- a comparison over one surface is not that."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    surf = rec.get("surfaces")
    want = ("grading_rule_worked_cases", "n6_grader_rows", "tension_ranking_surfaces")
    if not isinstance(surf, dict):
        return False, ["missing `surfaces` block"]
    ok = True
    missing = [k for k in want if k not in surf]
    out.append("surfaces present: %d of %d ; missing %s" % (len(want) - len(missing), len(want), missing))
    if missing:
        ok = False
    for k in want:
        blk = surf.get(k)
        if not isinstance(blk, dict):
            continue
        if not _own_denominator(blk, "  " + k, out):
            ok = False
        c = blk.get("compared")
        if not isinstance(c, int) or c <= 0:
            out.append("  %s: `compared` must be a POSITIVE int" % k)
            ok = False
    return ok, out


def core_c40_agreement(rec):
    """AGREEMENT IS A MEASURED VERDICT PER SURFACE, NEVER A SENTENCE. Each surface records
    `agree` and `disagree` as integers summing to its own `compared`, so a surface cannot be
    reported as agreeing by omission."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    surf = rec.get("surfaces") or {}
    ok = bool(surf)
    if not surf:
        out.append("no surfaces")
    for k in sorted(surf):
        blk = surf[k] or {}
        a, d, c = blk.get("agree"), blk.get("disagree"), blk.get("compared")
        if not all(isinstance(x, int) for x in (a, d, c)):
            out.append("%s: agree/disagree/compared must all be ints" % k)
            ok = False
            continue
        out.append("%s: agree %d + disagree %d = %d ; compared %d ; remainder %d"
                   % (k, a, d, a + d, c, c - (a + d)))
        if a + d != c:
            ok = False
    return ok, out


def core_c40_disagreements_named(rec):
    """EVERY DISAGREEMENT IS NAMED. A count of disagreements with no ids is a number nobody
    can act on, and clause 3's whole point is that the totals be reconcilable."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    surf = rec.get("surfaces") or {}
    ok = bool(surf)
    for k in sorted(surf):
        blk = surf[k] or {}
        d = blk.get("disagree")
        names = blk.get("disagreements")
        if not isinstance(d, int):
            ok = False
            continue
        if not isinstance(names, list) or len(names) != d:
            out.append("%s: `disagreements` must list exactly %r entries, got %r"
                       % (k, d, (len(names) if isinstance(names, list) else None)))
            ok = False
            continue
        bad = [x for x in names if not str((x or {}).get("name", "")).strip()
               or not str((x or {}).get("why", "")).strip()]
        out.append("%s: %d disagreement(s) listed, %d missing name/why" % (k, d, len(bad)))
        if bad:
            ok = False
    return ok, out


# ---------------------------------------------------------------- EN-s-41

def core_s41_decision(rec):
    """The scope decision is RECORDED as one of two named branches with a reason. 'Patched
    silently' is the outcome this cell exists to prevent, so an unstated branch fails."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    d = rec.get("decision")
    if not isinstance(d, dict):
        return False, ["missing `decision` block"]
    br = str(d.get("branch", "")).strip()
    why = str(d.get("why", "")).strip()
    out.append("branch: %r" % br)
    out.append("reason present: %s (%d chars)" % (bool(why), len(why)))
    ok = br in ("HOLD-BRACE-ONLY", "WIDEN") and len(why) >= 40
    if not ok:
        out.append("branch must be HOLD-BRACE-ONLY or WIDEN, with a reason of substance")
    return ok, out


def core_s41_population(rec):
    """The %-style population is MEASURED with its own denominator. A scope decision taken
    without knowing how many rows it moves is the S82 defect one level over."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    p = rec.get("percent_style_population")
    if not isinstance(p, dict):
        return False, ["missing `percent_style_population` block"]
    ok = _own_denominator(p, "percent_style", out)
    n = p.get("rows")
    out.append("rows carrying a %%-style field: %r" % n)
    if not isinstance(n, int) or n < 1:
        out.append("must be a POSITIVE int -- W3-S17 names at least one, so zero falsifies the read")
        ok = False
    return ok, out


def core_s41_negative_arm(rec):
    """WHICHEVER BRANCH, A NEGATIVE ARM WITH A POSITIVE TESTED DENOMINATOR. HOLD must show
    the brace-only scope still REJECTS the %-style row (so the hold is deliberate, not an
    oversight). WIDEN must show the widened scope still REJECTS ordinary keys (so it does not
    swallow the estate -- R-62's ground)."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    n = rec.get("negative_arm")
    if not isinstance(n, dict):
        return False, ["missing `negative_arm` block"]
    tested = n.get("tested")
    rejected = n.get("rejected")
    out.append("negative arm: rejected %r of %r tested" % (rejected, tested))
    ok = (isinstance(tested, int) and tested > 0
          and isinstance(rejected, int) and rejected == tested)
    if not ok:
        out.append("must reject EVERY case tested, with a POSITIVE tested denominator -- "
                   "zero tested is a vacuous negative arm")
    return ok, out


def core_s41_no_silent_move(rec):
    """The exclusion table's 8/7 split is unchanged for every type the cell does not DECLARE
    it is moving. The switch is a PROSE REASON STRING, so rewording a reason silently
    re-grades a type."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    g = rec.get("exclusion_table_after")
    if not isinstance(g, dict):
        return False, ["missing `exclusion_table_after` block"]
    moved = g.get("deliberately_moved")
    if not isinstance(moved, list):
        return False, ["`deliberately_moved` must be a list (it may be empty)"]
    want_out = ["API_ROUTE", "CLOUDFRONT_DISTRIBUTION", "EVENT_SOURCE", "IAM_USER",
                "KMS_KEY", "ROUTE53_RECORD", "SERVICE_PRINCIPAL", "VPC_ENDPOINT"]
    want_routed = ["EVENT_RULE", "LOG_GROUP", "S3Key", "S3_BUCKET", "S3_BUCKET_POLICY",
                   "SCHEDULE", "SECRET"]
    got_out = sorted(set(g.get("genuinely_not_graded") or []) - set(moved))
    got_routed = sorted(set(g.get("still_routed") or []) - set(moved))
    exp_out = sorted(set(want_out) - set(moved))
    exp_routed = sorted(set(want_routed) - set(moved))
    out.append("deliberately moved (named, may be empty): %s" % moved)
    out.append("NOT GRADED unchanged-set: got %d want %d" % (len(got_out), len(exp_out)))
    out.append("ROUTED     unchanged-set: got %d want %d" % (len(got_routed), len(exp_routed)))
    ok = (got_out == exp_out and got_routed == exp_routed)
    if not ok:
        out.append("a type moved that the record did not declare -- the reason-string hazard")
    return ok, out


# ---------------------------------------------------------------- EN-b-42

def core_b42_remeasured(rec):
    """THE SET GROWS WITH THE ROUND NUMBER BY CONSTRUCTION. The register says 91 at round 8;
    the issuer measured 94 at this cut. A plan written against an inherited figure is already
    wrong when it lands, so the cell's own denominator is the arm."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    p = rec.get("stale_population")
    if not isinstance(p, dict):
        return False, ["missing `stale_population` block"]
    ok = _own_denominator(p, "stale_population", out)
    n = p.get("rows")
    b = base()["the_stale_backlog_for_EN_b_42"]
    out.append("cell measured %r | register cites %d at round 8 | issuer measured %d at the cut"
               % (n, b["stale_at_round_8"], b["stale_at_round_9_THIS_CUT"]))
    if not isinstance(n, int) or n <= 0:
        out.append("must be a POSITIVE int")
        ok = False
    return ok, out


def core_b42_every_row_owned(rec):
    """Every stale row carries a NAMED owner. `assignments` must cover the measured
    population exactly -- owned + deferred == rows, remainder zero."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    p = rec.get("stale_population") or {}
    n = p.get("rows")
    a = rec.get("assignments")
    d = rec.get("deferred")
    if not isinstance(a, list) or not isinstance(d, list) or not isinstance(n, int):
        return False, ["needs `assignments` and `deferred` lists and a measured row count"]
    out.append("owned %d + deferred %d = %d ; population %d ; remainder %d"
               % (len(a), len(d), len(a) + len(d), n, n - (len(a) + len(d))))
    bad = [x for x in a if not str((x or {}).get("id", "")).strip()
           or not str((x or {}).get("owner", "")).strip()]
    out.append("assignments missing id or owner (must be 0): %d" % len(bad))
    return (len(a) + len(d) == n and not bad and n > 0), out


def core_b42_no_category_owners(rec):
    """AN OWNER THAT IS A CATEGORY DECAYS EXACTLY LIKE NO OWNER (R-70). This arm refuses the
    category words this estate has actually used, and requires each owner to look like a
    serial or a project code rather than a class of seats."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    a = rec.get("assignments")
    if not isinstance(a, list):
        return False, ["missing `assignments`"]
    banned = ("clean-up projects", "cleanup projects", "the clean-up", "whoever", "a later",
              "the next round", "someone", "TBD", "unassigned", "a future project")
    bad = []
    for x in a:
        o = str((x or {}).get("owner", ""))
        low = o.lower()
        if any(b.lower() in low for b in banned) or not o.strip():
            bad.append(str((x or {}).get("id", "?")) + " -> " + o[:40])
    out.append("assignments inspected: %d" % len(a))
    out.append("owners that are CATEGORIES rather than named parties (must be 0): %d %s"
               % (len(bad), bad[:6]))
    return (len(a) > 0 and not bad), out


def core_b42_deferred_carry_reasons(rec):
    """A deferred row is a decision, not an omission: it names why and what would un-defer
    it. Otherwise 'deferred' is this round's TIMEBOXED_R33 -- a value describing the
    measuring process rather than the measured domain."""
    out = []
    if not isinstance(rec, dict):
        return False, ["no record"]
    d = rec.get("deferred")
    if not isinstance(d, list):
        return False, ["missing `deferred`"]
    bad = [str((x or {}).get("id", "?")) for x in d
           if not str((x or {}).get("why", "")).strip()
           or not str((x or {}).get("un_defers_when", "")).strip()]
    out.append("deferred rows: %d ; missing why/un_defers_when (must be 0): %d %s"
               % (len(d), len(bad), bad[:6]))
    return (not bad), out


# ---------------------------------------------------------------- self test

def _c40_good():
    return {"worked_cases": {"counted": 45, "which_carrier_is_stale": "the register's 43 is stale",
                             "denominator_measured_at_write_time": {"instrument": "parse the fence", "value": 45}},
            "surfaces": {
                "grading_rule_worked_cases": {"compared": 45, "agree": 44, "disagree": 1,
                                              "disagreements": [{"name": "x", "why": "y"}],
                                              "denominator_measured_at_write_time": {"instrument": "i", "value": 45}},
                "n6_grader_rows": {"compared": 88, "agree": 88, "disagree": 0, "disagreements": [],
                                   "denominator_measured_at_write_time": {"instrument": "i", "value": 88}},
                "tension_ranking_surfaces": {"compared": 10, "agree": 10, "disagree": 0, "disagreements": [],
                                             "denominator_measured_at_write_time": {"instrument": "i", "value": 10}}}}


def _s41_good():
    return {"decision": {"branch": "HOLD-BRACE-ONLY",
                         "why": "the %-style class is a different object and widening the brace rule would swallow it"},
            "percent_style_population": {"rows": 2,
                                         "denominator_measured_at_write_time": {"instrument": "i", "value": 3254}},
            "negative_arm": {"tested": 40, "rejected": 40},
            "exclusion_table_after": {"deliberately_moved": [],
                                      "genuinely_not_graded": ["API_ROUTE", "CLOUDFRONT_DISTRIBUTION", "EVENT_SOURCE",
                                                               "IAM_USER", "KMS_KEY", "ROUTE53_RECORD",
                                                               "SERVICE_PRINCIPAL", "VPC_ENDPOINT"],
                                      "still_routed": ["EVENT_RULE", "LOG_GROUP", "S3Key", "S3_BUCKET",
                                                       "S3_BUCKET_POLICY", "SCHEDULE", "SECRET"]}}


def _b42_good():
    return {"stale_population": {"rows": 94,
                                 "denominator_measured_at_write_time": {"instrument": "srg._stale_open_row", "value": 94}},
            "assignments": [{"id": "LGIC_ENFORCE-S%d" % i, "owner": "1.0.0_SA_CTO"} for i in range(90)],
            "deferred": [{"id": "LGIC_ENFORCE-X%d" % i, "why": "w", "un_defers_when": "u"} for i in range(4)]}


def selftest():
    arms = []

    def arm(name, fn, expect):
        got = bool(fn())
        arms.append((name, expect, got, got == expect))

    g = _c40_good()
    arm("c40-recount POSITIVE", lambda: core_c40_recount(g)[0], True)
    m = json.loads(json.dumps(g))
    m["worked_cases"]["which_carrier_is_stale"] = ""
    arm("c40-recount MUTANT no-stale-call", lambda: core_c40_recount(m)[0], False)
    m2 = json.loads(json.dumps(g))
    m2["worked_cases"]["counted"] = 0
    arm("c40-recount MUTANT vacuous-zero", lambda: core_c40_recount(m2)[0], False)

    arm("c40-population POSITIVE", lambda: core_c40_population(g)[0], True)
    m3 = json.loads(json.dumps(g))
    del m3["surfaces"]["n6_grader_rows"]
    arm("c40-population MUTANT one-surface-short", lambda: core_c40_population(m3)[0], False)

    arm("c40-agreement POSITIVE", lambda: core_c40_agreement(g)[0], True)
    m4 = json.loads(json.dumps(g))
    m4["surfaces"]["grading_rule_worked_cases"]["agree"] = 40
    arm("c40-agreement MUTANT remainder", lambda: core_c40_agreement(m4)[0], False)

    arm("c40-disagreements POSITIVE", lambda: core_c40_disagreements_named(g)[0], True)
    m5 = json.loads(json.dumps(g))
    m5["surfaces"]["grading_rule_worked_cases"]["disagreements"] = []
    arm("c40-disagreements MUTANT unnamed", lambda: core_c40_disagreements_named(m5)[0], False)

    s = _s41_good()
    arm("s41-decision POSITIVE", lambda: core_s41_decision(s)[0], True)
    n1 = json.loads(json.dumps(s))
    n1["decision"]["branch"] = "patched"
    arm("s41-decision MUTANT unstated-branch", lambda: core_s41_decision(n1)[0], False)
    n1b = json.loads(json.dumps(s))
    n1b["decision"]["branch"] = "WIDEN"
    arm("s41-decision POSITIVE other-branch", lambda: core_s41_decision(n1b)[0], True)

    arm("s41-population POSITIVE", lambda: core_s41_population(s)[0], True)
    n2 = json.loads(json.dumps(s))
    n2["percent_style_population"]["rows"] = 0
    arm("s41-population MUTANT zero", lambda: core_s41_population(n2)[0], False)

    arm("s41-negative-arm POSITIVE", lambda: core_s41_negative_arm(s)[0], True)
    n3 = json.loads(json.dumps(s))
    n3["negative_arm"] = {"tested": 0, "rejected": 0}
    arm("s41-negative-arm MUTANT vacuous", lambda: core_s41_negative_arm(n3)[0], False)
    n4 = json.loads(json.dumps(s))
    n4["negative_arm"] = {"tested": 40, "rejected": 12}
    arm("s41-negative-arm MUTANT leaks", lambda: core_s41_negative_arm(n4)[0], False)

    arm("s41-no-silent-move POSITIVE", lambda: core_s41_no_silent_move(s)[0], True)
    n5 = json.loads(json.dumps(s))
    n5["exclusion_table_after"]["still_routed"] = ["EVENT_RULE"]
    arm("s41-no-silent-move MUTANT regrade", lambda: core_s41_no_silent_move(n5)[0], False)

    b = _b42_good()
    arm("b42-remeasured POSITIVE", lambda: core_b42_remeasured(b)[0], True)
    p1 = json.loads(json.dumps(b))
    del p1["stale_population"]["denominator_measured_at_write_time"]
    arm("b42-remeasured MUTANT inherited", lambda: core_b42_remeasured(p1)[0], False)

    arm("b42-every-row-owned POSITIVE", lambda: core_b42_every_row_owned(b)[0], True)
    p2 = json.loads(json.dumps(b))
    p2["deferred"] = []
    arm("b42-every-row-owned MUTANT remainder", lambda: core_b42_every_row_owned(p2)[0], False)

    arm("b42-no-category-owners POSITIVE", lambda: core_b42_no_category_owners(b)[0], True)
    p3 = json.loads(json.dumps(b))
    p3["assignments"][0]["owner"] = "the clean-up projects"
    arm("b42-no-category MUTANT category", lambda: core_b42_no_category_owners(p3)[0], False)

    arm("b42-deferred-reasons POSITIVE", lambda: core_b42_deferred_carry_reasons(b)[0], True)
    p4 = json.loads(json.dumps(b))
    p4["deferred"][0]["un_defers_when"] = ""
    arm("b42-deferred-reasons MUTANT bare", lambda: core_b42_deferred_carry_reasons(p4)[0], False)

    pos = [a for a in arms if a[1] is True]
    broken = [a for a in arms if not a[3]]
    print("SELFTEST ARMS: %d ; POSITIVE-SATISFIABILITY arms: %d ; failures: %d"
          % (len(arms), len(pos), len(broken)))
    for name, expect, got, good in arms:
        print("  %-46s expect=%-5s got=%-5s %s" % (name, expect, got, "OK" if good else "**ARM BROKEN**"))
    if broken:
        print("VERDICT: FAIL-SELFTEST")
        return 1
    print("VERDICT: PASS-SELFTEST-%d-ARMS-%d-POSITIVE" % (len(arms), len(pos)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sub")
    sub = ap.parse_args().sub

    if sub == "selftest-arms":
        return selftest()

    if sub.startswith("c40-"):
        rec = load(deliv("c40", "HAND_COMPARISON_R9.json"))
        fn = {"c40-recount": core_c40_recount,
              "c40-population": core_c40_population,
              "c40-agreement": core_c40_agreement,
              "c40-disagreements": core_c40_disagreements_named}[sub]
        ok, lines = fn(rec)
        return verdict(ok, sub.upper(), lines)

    if sub.startswith("s41-"):
        rec = load(deliv("s41", "PERCENT_STYLE_SCOPE_R9.json"))
        fn = {"s41-decision": core_s41_decision,
              "s41-population": core_s41_population,
              "s41-negative-arm": core_s41_negative_arm,
              "s41-no-silent-move": core_s41_no_silent_move}[sub]
        ok, lines = fn(rec)
        return verdict(ok, sub.upper(), lines)

    if sub.startswith("b42-"):
        rec = load(deliv("b42", "STALE_BACKLOG_R9.json"))
        fn = {"b42-remeasured": core_b42_remeasured,
              "b42-every-row-owned": core_b42_every_row_owned,
              "b42-no-category-owners": core_b42_no_category_owners,
              "b42-deferred-reasons": core_b42_deferred_carry_reasons}[sub]
        ok, lines = fn(rec)
        return verdict(ok, sub.upper(), lines)

    print("unknown subcommand %r" % sub)
    return 2


if __name__ == "__main__":
    sys.exit(main())
