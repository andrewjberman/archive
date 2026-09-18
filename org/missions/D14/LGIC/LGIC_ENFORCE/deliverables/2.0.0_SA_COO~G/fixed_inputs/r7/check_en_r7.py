"""LGIC_ENFORCE ROUND 7 -- the fixed input. Two cells, nine mechanical arms.

ROUND 7 DOES NOT ATTEMPT THE 1093 DEFERRED ROWS, AND THAT IS THE ROUND'S CENTRAL CHOICE.
R-60 read FWD-5's ACCEPT at the bytes: "a ranked list of every name and address that breaks the
pattern, each paired with its correct form, totals shown ... THIS IS THE LIST CLEAN-UP PROJECTS
START FROM." THE OUTCOME IS THE LIST. Resolution is the clean-up projects' work, and rounds 5 and 6
ground against a bar FWD-5 never set -- 41 rows a round, about thirty rounds to go, a net 82 of 1411
moved in two rounds. So round 7 works on what makes the LIST true instead.

BOTH CELLS ARE ABOUT LABELS THAT LIE, WHICH IS ONE AXIS AND ONE INTENT (Rule 24 iii):
  EN-t-34  a label that hides a two-remedy row, and a reason that names the wrong thing entirely
  EN-o-35  a claim field that says `inferred` where a directive could say better

A NOTE ON THE TABLE BOTH CELLS READ, because a reader who trusts its NAME will be wrong:
`types_not_graded_by_kind` is a ROUTING table, not an exclusion list. lib/opal_naming.py:493 unions
the WHOLE table into graded_types; :1012 removes a type only if str(why).startswith("NOT GRADED").
15 entries: 8 genuinely out, 7 STILL GRADED including S3Key. A CTO ruling reached for it as an
exclusion mechanism and was wrong (R-61, corrected by R-62). REWORDING A REASON SILENTLY CHANGES
GRADING BEHAVIOUR -- eight types sit on that edge. Neither cell here touches it, and `t34-no-grade-
change` REFUSES a cell that does.
"""

import copy
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
BASEFILE = os.path.join(HERE, "R7_BASE.json")
SCHEMA = "org/standards/NAMING_SCHEMA.json"

LABEL_RECORD = "LABEL_TRUTH_R7.json"
OWNER_RECORD = "OWNER_CONFIRMATION_R7.json"

# The reason text the 15 carry TODAY and must NOT still carry. It says the TOKEN is not a system;
# the truth R-62 adopted is that the ROW IS NOT A NAME.
STALE_REASON = "NON_SYSTEM_PLACEHOLDER_TOKEN"


def out(*lines):
    for ln in lines:
        print(ln)


def verdict(ok, pass_tag, fail_tag, lines):
    out(*lines)
    print("VERDICT: " + (pass_tag if ok else fail_tag))
    return 0


def say(tag, *lines):
    out(*lines)
    print("VERDICT: " + tag)
    return 0


def ab(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def read(p):
    try:
        with io.open(ab(p), encoding="utf-8", newline="") as fh:
            return fh.read()
    except Exception:
        return None


def load_json(p):
    t = read(p)
    if t is None:
        return None
    try:
        return json.loads(t)
    except Exception:
        return None


def base():
    return load_json(BASEFILE) or {}


def record_path(name):
    for n in ("1", "2", "3", "4"):
        p = "%s/deliverables/0.9.0_WK_LGIC_ENFORCE~%s/%s" % (ROOT, n, name)
        if os.path.isfile(ab(p)):
            return p
    return "%s/deliverables/0.9.0_WK_LGIC_ENFORCE~1/%s" % (ROOT, name)


# ============================================================ EN-t-34, the labels that lie
def core_t34_51_both(rec, want):
    """Every one of the 51 carries a label naming BOTH remedies, and the count is re-derived."""
    lines = []
    if not isinstance(rec, dict):
        return False, ["the record does not parse as an object"]
    rows = rec.get("two_remedy_rows")
    if not isinstance(rows, list):
        return False, ["two_remedy_rows is not a list"]
    lines.append("two_remedy_rows: %d (the pin measured %d, re-identified independently of the "
                 "record's own label)" % (len(rows), want))
    bad = [r.get("current") for r in rows
           if not isinstance(r, dict) or len(r.get("remedies") or []) != 2]
    lines.append("rows NOT naming exactly two remedies (must be 0): %d %s" % (len(bad), bad[:5]))
    return (len(rows) == want and not bad and want > 0), lines


def core_t34_51_actionable(rec):
    """A label a later census can ACT on names each remedy's CARRIER, not merely that there are two.

    'Two remedies' is a description. 'The {system} half is a resources.json row and the {cadence}
    half is the schedule' is an instruction. The arm grades the difference, because the defect this
    cell exists to fix was a label that described instead of instructing."""
    lines = []
    rows = (rec or {}).get("two_remedy_rows")
    if not isinstance(rows, list):
        return False, ["two_remedy_rows is not a list"]
    nocarrier = []
    for r in rows:
        rem = (r or {}).get("remedies") or []
        if any(not str((x or {}).get("carrier") or "").strip() for x in rem):
            nocarrier.append(r.get("current"))
    lines.append("rows: %d" % len(rows))
    lines.append("rows with a remedy naming no CARRIER (must be 0): %d %s" % (len(nocarrier), nocarrier[:5]))
    defn = str((rec or {}).get("label_definition") or "").strip()
    lines.append("label_definition present: %s" % bool(defn))
    return (not nocarrier and bool(defn) and len(rows) > 0), lines


def core_t34_15_true(rec, want):
    """The 15 carry a reason saying the ROW IS NOT A NAME, and NOT the stale token reason."""
    lines = []
    rows = (rec or {}).get("key_template_rows")
    if not isinstance(rows, list):
        return False, ["key_template_rows is not a list"]
    lines.append("key_template_rows: %d (the pin measured %d)" % (len(rows), want))
    stale = [r.get("current") for r in rows if STALE_REASON in json.dumps(r or {})]
    lines.append("rows still carrying the STALE reason %s (must be 0): %d %s"
                 % (STALE_REASON, len(stale), stale[:5]))
    noreason = [r.get("current") for r in rows if not str((r or {}).get("reason") or "").strip()]
    lines.append("rows with no reason at all (must be 0): %d %s" % (len(noreason), noreason[:5]))
    return (len(rows) == want and not stale and not noreason and want > 0), lines


def core_t34_no_grade_change(schema_now, pinned):
    """THE GUARD. R-62 REFUSED removing S3Key from the name grade -- it would remove EVERY S3 key in
    the estate to fix 15 templates. So this arm reads PASS at the cut and can only be broken by the
    cell touching the table. It also re-counts the 'NOT GRADED' prefix switch, because that is the
    real control and a reworded reason silently moves a type across it."""
    lines = []
    if not isinstance(schema_now, dict):
        return False, ["the schema could not be read"]
    tng = schema_now.get("types_not_graded_by_kind")
    if not isinstance(tng, dict):
        return False, ["types_not_graded_by_kind is not an object"]
    really_out = sorted(k for k, v in tng.items() if str(v).startswith("NOT GRADED"))
    routed = sorted(k for k, v in tng.items() if not str(v).startswith("NOT GRADED"))
    want_out = pinned.get("genuinely_not_graded") or []
    want_routed = pinned.get("STILL_GRADED_merely_routed") or []
    lines.append("entries %d (pinned %s)" % (len(tng), pinned.get("entries")))
    lines.append("genuinely NOT GRADED: %d %s" % (len(really_out), really_out))
    lines.append("  pinned:             %d %s" % (len(want_out), want_out))
    lines.append("STILL GRADED (routed): %d ; pinned %d" % (len(routed), len(want_routed)))
    ok = (really_out == sorted(want_out) and routed == sorted(want_routed)
          and len(tng) == pinned.get("entries"))
    if not ok:
        lines.append("THE EXCLUSION TABLE MOVED. R-62 refused that act; a reworded reason moves a "
                     "type across the 'NOT GRADED' switch silently.")
    return ok, lines


# ============================================================ EN-o-35, the owner confirmations
def core_o35_population(rec, want):
    lines = []
    if not isinstance(rec, dict):
        return False, ["the record does not parse as an object"]
    conf = rec.get("confirmed")
    card = rec.get("carded")
    if not isinstance(conf, list) or not isinstance(card, list):
        return False, ["confirmed and carded must both be lists"]
    lines.append("population pinned at %d ; confirmed %d + carded %d = %d"
                 % (want, len(conf), len(card), len(conf) + len(card)))
    ids = [r.get("current") for r in conf + card if isinstance(r, dict)]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    lines.append("a row in BOTH lists (must be empty): %s" % dupes)
    return (len(conf) + len(card) == want and not dupes and want > 0), lines


def core_o35_directive(rec):
    """A CONFIRMED row cites an OWNING DIRECTIVE. A sibling resource is what it already had."""
    lines = []
    conf = (rec or {}).get("confirmed")
    if not isinstance(conf, list):
        return False, ["confirmed is not a list"]
    bad = [r.get("current") for r in conf
           if not str((r or {}).get("owning_directive") or "").strip()]
    nocite = [r.get("current") for r in conf
              if not str((r or {}).get("directive_citation") or "").strip()]
    lines.append("confirmed rows: %d" % len(conf))
    lines.append("without an owning_directive (must be 0): %d %s" % (len(bad), bad[:5]))
    lines.append("without a directive_citation (must be 0): %d %s" % (len(nocite), nocite[:5]))
    return (not bad and not nocite), lines


def core_o35_claim_moves(rec):
    """A CONFIRMED row's claim leaves `inferred`; a CARDED row's stays, WITH a reason."""
    lines = []
    conf = (rec or {}).get("confirmed") or []
    card = (rec or {}).get("carded") or []
    still = [r.get("current") for r in conf if str((r or {}).get("owner_claim")) == "inferred"]
    moved = [r.get("current") for r in card if str((r or {}).get("owner_claim")) != "inferred"]
    noreason = [r.get("current") for r in card if not str((r or {}).get("reason") or "").strip()]
    lines.append("confirmed still reading `inferred` (must be 0): %d %s" % (len(still), still[:5]))
    lines.append("carded NO LONGER reading `inferred` (must be 0): %d %s" % (len(moved), moved[:5]))
    lines.append("carded with no reason (must be 0): %d %s" % (len(noreason), noreason[:5]))
    return (not still and not moved and not noreason), lines


def core_o35_no_silent_upgrade(rec):
    """A claim cannot move without its BASIS moving. Upgrading `inferred` to a stronger claim while
    the evidence string stays byte-identical is a relabelling, not a confirmation -- and it is the
    exact shape that makes a value stop carrying its claim."""
    lines = []
    conf = (rec or {}).get("confirmed") or []
    same = [r.get("current") for r in conf
            if str((r or {}).get("owner_basis") or "") == str((r or {}).get("owner_basis_round_6") or "")
            and str((r or {}).get("owner_basis") or "").strip()]
    missing = [r.get("current") for r in conf
               if not str((r or {}).get("owner_basis_round_6") or "").strip()]
    lines.append("confirmed rows: %d" % len(conf))
    lines.append("whose basis is BYTE-IDENTICAL to round 6's (must be 0): %d %s" % (len(same), same[:5]))
    lines.append("not carrying round 6's basis for comparison (must be 0): %d %s"
                 % (len(missing), missing[:5]))
    return (not same and not missing), lines


# ================================================================== the real subcommands
def t34_51_both():
    b = base()
    want = (b.get("the_51_two_remedy_rows") or {}).get("re_identified_here") or 0
    rec = load_json(record_path(LABEL_RECORD))
    if rec is None:
        return say("FAIL-T34-51-NAME-BOTH-REMEDIES", "record not found at %s" % record_path(LABEL_RECORD))
    ok, lines = core_t34_51_both(rec, want)
    return verdict(ok, "PASS-T34-51-NAME-BOTH-REMEDIES", "FAIL-T34-51-NAME-BOTH-REMEDIES", lines)


def t34_51_actionable():
    rec = load_json(record_path(LABEL_RECORD))
    if rec is None:
        return say("FAIL-T34-LABEL-IS-ACTIONABLE", "record not found")
    ok, lines = core_t34_51_actionable(rec)
    return verdict(ok, "PASS-T34-LABEL-IS-ACTIONABLE", "FAIL-T34-LABEL-IS-ACTIONABLE", lines)


def t34_15_true():
    b = base()
    want = (b.get("the_15_key_templates") or {}).get("count") or 0
    rec = load_json(record_path(LABEL_RECORD))
    if rec is None:
        return say("FAIL-T34-15-CARRY-A-TRUE-REASON", "record not found")
    ok, lines = core_t34_15_true(rec, want)
    return verdict(ok, "PASS-T34-15-CARRY-A-TRUE-REASON", "FAIL-T34-15-CARRY-A-TRUE-REASON", lines)


def t34_no_grade_change():
    b = base()
    ok, lines = core_t34_no_grade_change(load_json(SCHEMA), b.get("the_exclusion_switch_HAZARD") or {})
    return verdict(ok, "PASS-T34-NO-GRADE-CHANGE", "FAIL-T34-NO-GRADE-CHANGE", lines)


def o35_population():
    b = base()
    want = (b.get("the_41_inferred_owner_claims") or {}).get("count") or 0
    rec = load_json(record_path(OWNER_RECORD))
    if rec is None:
        return say("FAIL-O35-EVERY-ROW-ADDRESSED", "record not found at %s" % record_path(OWNER_RECORD))
    ok, lines = core_o35_population(rec, want)
    return verdict(ok, "PASS-O35-EVERY-ROW-ADDRESSED", "FAIL-O35-EVERY-ROW-ADDRESSED", lines)


def o35_directive():
    rec = load_json(record_path(OWNER_RECORD))
    if rec is None:
        return say("FAIL-O35-CONFIRMED-CITES-A-DIRECTIVE", "record not found")
    ok, lines = core_o35_directive(rec)
    return verdict(ok, "PASS-O35-CONFIRMED-CITES-A-DIRECTIVE",
                   "FAIL-O35-CONFIRMED-CITES-A-DIRECTIVE", lines)


def o35_claim_moves():
    rec = load_json(record_path(OWNER_RECORD))
    if rec is None:
        return say("FAIL-O35-CLAIM-MATCHES-ITS-LIST", "record not found")
    ok, lines = core_o35_claim_moves(rec)
    return verdict(ok, "PASS-O35-CLAIM-MATCHES-ITS-LIST", "FAIL-O35-CLAIM-MATCHES-ITS-LIST", lines)


def o35_no_silent_upgrade():
    rec = load_json(record_path(OWNER_RECORD))
    if rec is None:
        return say("FAIL-O35-NO-SILENT-UPGRADE", "record not found")
    ok, lines = core_o35_no_silent_upgrade(rec)
    return verdict(ok, "PASS-O35-NO-SILENT-UPGRADE", "FAIL-O35-NO-SILENT-UPGRADE", lines)


# ================================================================== the arm self-test
def selftest_arms():
    b = base()
    w51 = (b.get("the_51_two_remedy_rows") or {}).get("re_identified_here") or 0
    w15 = (b.get("the_15_key_templates") or {}).get("count") or 0
    w41 = (b.get("the_41_inferred_owner_claims") or {}).get("count") or 0
    haz = b.get("the_exclusion_switch_HAZARD") or {}
    res = []

    def arm(name, good_ok, bad_ok, why):
        res.append((name, good_ok and not bad_ok, why))

    good_label = {
        "label_definition": "TWO_CARRIER_ROW: a row whose canonical form needs a value from two "
                            "different carriers, neither of which alone clears it.",
        "two_remedy_rows": [
            {"current": "r%d" % i,
             "remedies": [{"token": "system", "carrier": "infra/logic/registry/resources.json"},
                          {"token": "cadence", "carrier": "the schedule that drives it"}]}
            for i in range(w51)],
        "key_template_rows": [
            {"current": "k%d" % i,
             "reason": "THE ROW IS NOT A NAME: an S3 key FORMAT TEMPLATE is a producer's runtime "
                       "substitution field, so the name grade's placeholder question never applied."}
            for i in range(w15)],
    }
    good_owner = {
        "confirmed": [{"current": "c%d" % i, "owner_claim": "confirmed",
                       "owning_directive": "D8 / ADVI_INFSHIP",
                       "directive_citation": "org/missions/DIRECTIVES.yaml:485",
                       "owner_basis": "LEG C (directive): ...",
                       "owner_basis_round_6": "LEG A (declared): ..."} for i in range(w41 - 3)],
        "carded": [{"current": "d%d" % i, "owner_claim": "inferred",
                    "reason": "no directive claims this resource"} for i in range(3)],
    }
    schema_now = load_json(SCHEMA)

    res.append(("POSITIVE-t34-51-both", core_t34_51_both(good_label, w51)[0], "a correct record must PASS"))
    res.append(("POSITIVE-t34-actionable", core_t34_51_actionable(good_label)[0], "a correct record must PASS"))
    res.append(("POSITIVE-t34-15-true", core_t34_15_true(good_label, w15)[0], "a correct record must PASS"))
    res.append(("POSITIVE-t34-no-grade-change", core_t34_no_grade_change(schema_now, haz)[0],
                "the UNTOUCHED schema must PASS -- this arm is a GUARD"))
    res.append(("POSITIVE-o35-population", core_o35_population(good_owner, w41)[0], "a correct record must PASS"))
    res.append(("POSITIVE-o35-directive", core_o35_directive(good_owner)[0], "a correct record must PASS"))
    res.append(("POSITIVE-o35-claim-moves", core_o35_claim_moves(good_owner)[0], "a correct record must PASS"))
    res.append(("POSITIVE-o35-no-silent-upgrade", core_o35_no_silent_upgrade(good_owner)[0],
                "a correct record must PASS"))

    one_remedy = copy.deepcopy(good_label)
    one_remedy["two_remedy_rows"][0]["remedies"] = one_remedy["two_remedy_rows"][0]["remedies"][:1]
    short51 = copy.deepcopy(good_label)
    short51["two_remedy_rows"] = short51["two_remedy_rows"][:-1]
    arm("t34-51-both", core_t34_51_both(good_label, w51)[0], core_t34_51_both(one_remedy, w51)[0],
        "a two-carrier row labelled with one remedy -- the defect itself")
    arm("t34-51-count", core_t34_51_both(good_label, w51)[0], core_t34_51_both(short51, w51)[0],
        "a row of the 51 missing from the record")
    nocarrier = copy.deepcopy(good_label)
    nocarrier["two_remedy_rows"][0]["remedies"][0].pop("carrier")
    nodefn = copy.deepcopy(good_label)
    nodefn["label_definition"] = ""
    arm("t34-actionable", core_t34_51_actionable(good_label)[0], core_t34_51_actionable(nocarrier)[0],
        "a remedy naming no carrier -- a description wearing an instruction's name")
    arm("t34-definition", core_t34_51_actionable(good_label)[0], core_t34_51_actionable(nodefn)[0],
        "a label with no definition a later census could read")
    stale = copy.deepcopy(good_label)
    stale["key_template_rows"][0]["reason"] = "canonical carries a %s" % STALE_REASON
    arm("t34-15-true", core_t34_15_true(good_label, w15)[0], core_t34_15_true(stale, w15)[0],
        "a template still carrying the reason that says the TOKEN is not a system")
    if isinstance(schema_now, dict):
        moved = copy.deepcopy(schema_now)
        tng = moved["types_not_graded_by_kind"]
        tng["S3Key"] = "NOT GRADED: " + str(tng["S3Key"])
        arm("t34-no-grade-change", core_t34_no_grade_change(schema_now, haz)[0],
            core_t34_no_grade_change(moved, haz)[0],
            "S3Key pushed across the 'NOT GRADED' switch -- the act R-62 REFUSED, and the exact "
            "one-prefix edit that silently changes grading")

    shortp = copy.deepcopy(good_owner)
    shortp["carded"] = shortp["carded"][:-1]
    both = copy.deepcopy(good_owner)
    both["carded"] = both["carded"] + [dict(good_owner["confirmed"][0])]
    arm("o35-population", core_o35_population(good_owner, w41)[0], core_o35_population(shortp, w41)[0],
        "a row of the 41 in neither list")
    arm("o35-population-double", core_o35_population(good_owner, w41)[0], core_o35_population(both, w41)[0],
        "a row in BOTH lists")
    nodir = copy.deepcopy(good_owner)
    nodir["confirmed"][0].pop("owning_directive")
    nocite = copy.deepcopy(good_owner)
    nocite["confirmed"][0]["directive_citation"] = ""
    arm("o35-directive", core_o35_directive(good_owner)[0], core_o35_directive(nodir)[0],
        "a confirmation naming no directive -- a sibling's inheritance again")
    arm("o35-citation", core_o35_directive(good_owner)[0], core_o35_directive(nocite)[0],
        "a directive named but not cited")
    stuck = copy.deepcopy(good_owner)
    stuck["confirmed"][0]["owner_claim"] = "inferred"
    noreason = copy.deepcopy(good_owner)
    noreason["carded"][0]["reason"] = ""
    arm("o35-claim-moves", core_o35_claim_moves(good_owner)[0], core_o35_claim_moves(stuck)[0],
        "a confirmed row whose claim never left `inferred`")
    arm("o35-carded-reason", core_o35_claim_moves(good_owner)[0], core_o35_claim_moves(noreason)[0],
        "a carded row with no reason")
    silent = copy.deepcopy(good_owner)
    silent["confirmed"][0]["owner_basis"] = silent["confirmed"][0]["owner_basis_round_6"]
    arm("o35-no-silent-upgrade", core_o35_no_silent_upgrade(good_owner)[0],
        core_o35_no_silent_upgrade(silent)[0],
        "a claim upgraded while its evidence string stayed byte-identical -- a relabelling")

    pos = [r for r in res if r[0].startswith("POSITIVE-")]
    for name, ok, why in res:
        print("  %-30s %s  %s" % (name, "PASS" if ok else "FAIL", why))
    allok = all(ok for _, ok, _ in res)
    print("arms driven: %d (%d POSITIVE-SATISFIABILITY against simulated correct records, %d mutant)"
          % (len(res), len(pos), len(res) - len(pos)))
    print("NOT driven here, stated: record_path() itself, whose content is a live filesystem read -- it "
          "has no fixture and is exercised by the real run.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if allok else "FAIL-ARMS-DO-NOT-DISCRIMINATE"))
    return 0


CMDS = {
    "t34-51-both": t34_51_both, "t34-actionable": t34_51_actionable, "t34-15-true": t34_15_true,
    "t34-no-grade-change": t34_no_grade_change,
    "o35-population": o35_population, "o35-directive": o35_directive,
    "o35-claim-moves": o35_claim_moves, "o35-no-silent-upgrade": o35_no_silent_upgrade,
    "selftest-arms": selftest_arms,
}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("unknown subcommand: %s" % (argv[1] if len(argv) > 1 else "<none>"))
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
