"""b-6 MEMBERSHIP LAW arms, scored against BOTH leaves 2.0.0_SA_COO 79840/79869 ruled.

TWO LEAVES, TWO BRANCHES, AND THAT IS THE POINT. The ruled QTD leaf exercises the
ABSENT branch (its window start precedes the jd2 membership floor, so new/lost cannot
be computed); the floor-aligned evidence leaf exercises the COMPUTABLE branch. An arm
suite that only ever saw one of them would score a branch that never runs.

NEVER SCORE AN ABSENT STATE WITHOUT A CONTROL THAT CAN FIRE. Every absence arm below is
paired with a mutation of the SAME predicate over a FABRICATED entry that violates it,
and the run FAILS if the mutation does not trip the arm. An absence arm with no firing
control is indistinguishable from an arm that cannot fail -- which is the shape of four
wrong arms this round, all of which passed while the product was right.

THE CONFOUND IS SCORED, NOT ASSUMED AWAY (arm 12). The evidence leaf's window-start
spine is schema_version 1.0 and its as-of spine is 2.0, so its membership deltas carry
relationship_id REASSIGNMENT as well as client movement. The arm asserts the leaf
DISCLOSES that on its face; it does not assert the numbers are clean, because they are
not. Measured 2026-08-28: 21.6% re-key across the version boundary in 34 days against
2.0% within 2.0 over 147 days.
"""
import copy
import json
import pathlib
import subprocess

ROOT = pathlib.Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                                   capture_output=True, text=True,
                                   check=True).stdout.strip())
EM = ROOT / "org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/emissions"
RULED = json.load(open(EM / "perfrp_book_advisor.json", encoding="utf-8"))
EVID = json.load(open(EM / "perfrp_book_advisor_floor_aligned.json", encoding="utf-8"))
FAILS = []
ABSENT = "NOT_COMPUTED_INPUTS_ABSENT"
# The client-table status vocabulary. The fourth member was ruled at 1.0.0_SA_CTO 80187
# and RENAMED at 80196 from UNMEASURABLE to this token, because COO 79841 had already
# put the same token on the same rows' new/lost FIGURES for the same cause: two words
# for one cause on one row reads as two different things having happened.
ABSENT_STATUS = "NOT_COMPUTED_INPUTS_ABSENT"
COMPUTABLE = ("new", "lost", "existing")


def check(name, cond, detail=""):
    print("  %-62s %s%s" % (name, "PASS" if cond else "*** FAIL ***",
                            ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(name)


def control(name, predicate, mutated):
    """The SAME predicate over a fabricated violation. It MUST return False."""
    ok = not predicate(mutated)
    print("     %-59s %s" % ("NEGATIVE CONTROL: " + name,
                             "FIRES" if ok else "*** DEAD ARM ***"))
    if not ok:
        FAILS.append("NEGATIVE CONTROL " + name)


def rows_of(leaf):
    return [r for e in leaf["entries"] for r in e["client_table"]]


print("=" * 78)
print("LEAF IDENTITY -- which branch each leaf actually exercises")
print("=" * 78)
for nm, L in (("ruled QTD", RULED), ("floor-aligned evidence", EVID)):
    w = L["window"]
    print("  %-24s %s..%s  computable=%-5s  spine %s->%s  entries=%d"
          % (nm, w["window_start"], w["window_end"],
             w["membership_basis"]["computable"],
             w["basis_version_change"]["window_start_schema_version"],
             w["basis_version_change"]["as_of_schema_version"], len(L["entries"])))
check("the two leaves exercise DIFFERENT branches (else one is unscored)",
      RULED["window"]["membership_basis"]["computable"]
      != EVID["window"]["membership_basis"]["computable"])
check("the ruled leaf is NOT labelled an evidence window",
      RULED["window"]["window_kind"] == "RULED CONTRACT PERIOD")
# THE FIELD, NOT THE PROSE. This arm first grepped "QTD" out of window_kind and FAILED
# on the leaf's own disclaimer ("...can never be read as QTD"), while the actual defect
# it should have caught -- period == "QTD" on the evidence leaf -- sat one key away and
# passed. A prose scan reads the sentence a consumer ignores and misses the field a
# consumer binds to. Fifth wrong arm this round; the product was wrong this time too.
check("the evidence leaf NEVER claims a contract period in the FIELD",
      EVID["window"]["period"] == "EVIDENCE-WINDOW"
      and EVID["window"]["requested_period"] == "QTD",
      "period=%r" % EVID["window"]["period"])
check("the ruled leaf DOES carry its contract period",
      RULED["window"]["period"] == "QTD")
check("the evidence leaf still SAYS so in prose (belt and braces)",
      "EVIDENCE WINDOW" in EVID["window"]["window_kind"])
check("they are SEPARATE FILES (DE~D 79860: one file, two vintages, silent mis-read)",
      (EM / "perfrp_book_advisor.json").exists()
      and (EM / "perfrp_book_advisor_floor_aligned.json").exists())

print()
print("=" * 78)
print("ARMS 1-4 -- THE ABSENT BRANCH (ruled QTD leaf)")
print("=" * 78)
E = RULED["entries"]


def all_absent(entries):
    return all(e["tiles"]["relationships"][k]["figure_state"] == ABSENT
               for e in entries for k in ("new", "lost"))


check("every new AND lost figure carries NOT_COMPUTED_INPUTS_ABSENT",
      all_absent(E), "%d of %d advisors, both figures" % (len(E), len(E)))
_mut = copy.deepcopy(E[:1])
_mut[0]["tiles"]["relationships"]["new"]["figure_state"] = "COMPUTED"
control("one advisor's `new` flipped to COMPUTED", all_absent, _mut)


def no_value_under_absent(entries):
    return not [1 for e in entries for k in ("new", "lost")
                if e["tiles"]["relationships"][k]["figure_state"] == ABSENT
                and e["tiles"]["relationships"][k]["value"] is not None]


check("NOT ONE absent figure carries a value (the real hazard, not the state)",
      no_value_under_absent(E), "0 of %d" % (2 * len(E)))
_mut = copy.deepcopy(E[:1])
_mut[0]["tiles"]["relationships"]["lost"]["value"] = 0
control("an absent figure given the value 0", no_value_under_absent, _mut)


def named_floor(entries):
    return all(str(e["tiles"]["relationships"][k]["reason"] or "").find("floor") >= 0
               or "partition at or before" in str(e["tiles"]["relationships"][k]["reason"])
               for e in entries for k in ("new", "lost"))


check("every absent reason NAMES the basis floor (not a bare 'unavailable')",
      named_floor(E))
_mut = copy.deepcopy(E[:1])
_mut[0]["tiles"]["relationships"]["new"]["reason"] = "unavailable"
control("a reason reduced to 'unavailable'", named_floor, _mut)

START_DEPENDENT = ("new", "lost", "existing", "union", "at_window_start")


def start_members_null(entries):
    return all(e["relationship_partition"][m] is None
               for e in entries for m in START_DEPENDENT)


check("every START-BOOK-DEPENDENT partition member is null, never 0",
      start_members_null(E),
      "%d members x %d advisors" % (len(START_DEPENDENT), len(E)))
_mut = copy.deepcopy(E[:1])
_mut[0]["relationship_partition"]["new"] = 0
control("partition.new set back to 0 (the pre-fix rendering)",
        start_members_null, _mut)
check("at_as_of SURVIVES (it needs no second vintage)",
      all(isinstance(e["relationship_partition"]["at_as_of"], int) for e in E))

print()
print("=" * 78)
print("ARMS 5-9 -- THE COMPUTABLE BRANCH (floor-aligned evidence leaf)")
print("=" * 78)
V = EVID["entries"]


def partition_identity(entries):
    return not [1 for e in entries
                if e["relationship_partition"]["new"]
                + e["relationship_partition"]["lost"]
                + e["relationship_partition"]["existing"]
                != e["relationship_partition"]["union"]]


check("AC3 identity: new + lost + existing == |union|", partition_identity(V),
      "%d of %d advisors" % (len(V), len(V)))
_mut = copy.deepcopy(V[:1])
_mut[0]["relationship_partition"]["new"] += 1
control("one advisor's `new` incremented by 1", partition_identity, _mut)


def new_lost_disjoint(entries):
    """COO 79840's named arm: no relationship is BOTH gained and lost."""
    for e in entries:
        s = [r["relationship_id"] for r in e["client_table"]]
        if len(s) != len(set(s)):
            return False
        n = {r["relationship_id"] for r in e["client_table"] if r["status"] == "new"}
        ll = {r["relationship_id"] for r in e["client_table"] if r["status"] == "lost"}
        if n & ll:
            return False
    return True


check("no relationship is in BOTH the new and lost sets", new_lost_disjoint(V),
      "0 overlapping of %d advisors" % len(V))
_dup = copy.deepcopy(V[:1])
_r = dict(_dup[0]["client_table"][0])
_r["status"] = "new"
_dup[0]["client_table"][0]["status"] = "lost"
_dup[0]["client_table"].append(_r)
control("a real key duplicated into BOTH statuses", new_lost_disjoint, _dup)


def computed_states(entries):
    return all(e["tiles"]["relationships"][k]["figure_state"] == "COMPUTED"
               for e in entries for k in ("new", "lost"))


check("the computable branch actually COMPUTES (states, not absences)",
      computed_states(V), "%d of %d advisors" % (len(V), len(V)))


def tile_matches_partition(entries):
    return not [1 for e in entries
                if e["tiles"]["relationships"]["new"]["value"]
                != e["relationship_partition"]["new"]
                or e["tiles"]["relationships"]["lost"]["value"]
                != e["relationship_partition"]["lost"]]


check("the TILE figure and the PARTITION count are the same number",
      tile_matches_partition(V), "%d advisors" % len(V))
_mut = copy.deepcopy(V[:1])
_mut[0]["tiles"]["relationships"]["new"]["value"] += 1
control("tile and partition made to disagree", tile_matches_partition, _mut)


def status_matches_sets(entries):
    for e in entries:
        c = {"new": 0, "lost": 0, "existing": 0}
        for r in e["client_table"]:
            if r["status"] in c:
                c[r["status"]] += 1
        p = e["relationship_partition"]
        if (c["new"], c["lost"], c["existing"]) != (p["new"], p["lost"], p["existing"]):
            return False
    return True


check("per-status ROW counts reproduce the partition counts",
      status_matches_sets(V), "%d advisors" % len(V))

print()
print("=" * 78)
print("ARMS 10-12 -- LAWS THAT BIND BOTH LEAVES")
print("=" * 78)
for nm, L in (("ruled", RULED), ("evidence", EVID)):
    ent = L["entries"]
    rk_entry = sum(e["re_keyed_clients"] for e in ent)
    rk_rows = sum(1 for r in rows_of(L) if r["key_continuity"] == "re_keyed")
    check("[%s] re_keyed_clients == re_keyed ROWS" % nm, rk_entry == rk_rows,
          "%d vs %d" % (rk_entry, rk_rows))
    missing = []
    for e in ent:
        have = {r["relationship_id"] for r in e["client_table"]}
        if e["re_keyed_clients"] > len([1 for r in e["client_table"]
                                        if r["key_continuity"] == "re_keyed"]):
            missing.append(e["key"])
        del have
    check("[%s] every key a FIGURE counts has a ROW to be counted in" % nm,
          not missing, "%d advisors short" % len(missing))
    bare = [1 for e in ent for t in e["tiles"].values() for v in t.values()
            if isinstance(v, dict) and "figure_state" not in v]
    check("[%s] no bare figure anywhere in the tiles" % nm, not bare,
          "0 of %d" % sum(len(t) for e in ent for t in e["tiles"].values()))
    st = {r["status"] for r in rows_of(L)}
    check("[%s] every row status is in the ruled vocabulary" % nm,
          st <= set(COMPUTABLE) | {ABSENT_STATUS}, str(sorted(st)))

# 1.0.0_SA_CTO 80187 item 3 -- THE ARM THAT MAKES THE FOURTH MEMBER REJECTABLE.
# The member is reachable IFF membership_computable is False. A row on the COMPUTABLE
# branch carrying it, or a row on the ABSENT branch carrying one of the three ruled
# values, is a FAIL -- not a curiosity. This is the predicate that keeps the enum MECE
# (postulate (i)); without it the fourth member is an unfalsifiable addition.
# 1.0.0_SA_CTO 80220 -- THE PATH, SPELLED IN FULL, AND AN EXISTENCE ASSERTION BEFORE
# THE COMPARISON. 80187 wrote the predicate as the FIELD NAME
# `membership_computable`; the field is NESTED at
# entries[].relationship_partition.membership_computable. 2.0.0_SA_COO read it at ENTRY
# level, got None on 146 of 146, and a None-vs-False comparison scores CLEAN on every
# row -- a wrong-level read wearing the shape of a pass, on BOTH branches. So the arm
# asserts the path RESOLVES on every entry (denominator printed) BEFORE it compares: a
# missing path is a FAIL of the arm, never a pass of the rule.
PATH = "entries[].relationship_partition.membership_computable"


def path_resolves(leaf):
    return all(isinstance(e.get("relationship_partition", {})
                          .get("membership_computable"), bool)
               for e in leaf["entries"])


def branch_vocabulary(leaf):
    """Per-ENTRY, off the nested path -- never off the window-level summary."""
    if not path_resolves(leaf):
        return False                    # a missing path FAILS; it never passes.
    for e in leaf["entries"]:
        computable = e["relationship_partition"]["membership_computable"]
        allowed = set(COMPUTABLE) if computable else {ABSENT_STATUS}
        if [1 for r in e["client_table"] if r["status"] not in allowed]:
            return False
    return True


for nm, L in (("ruled/absent", RULED), ("evidence/computable", EVID)):
    check("[%s] the nested PATH resolves on every entry (existence FIRST)" % nm,
          path_resolves(L), "%s -- %d of %d entries"
          % (PATH, sum(1 for e in L["entries"]
                       if isinstance(e.get("relationship_partition", {})
                                     .get("membership_computable"), bool)),
             len(L["entries"])))
    check("[%s] status vocabulary matches the BRANCH, never crosses" % nm,
          branch_vocabulary(L), "%d rows" % len(rows_of(L)))

# THE WRONG-LEVEL READ, SHIPPED AS ITS OWN NEGATIVE CONTROL (2.0.0_SA_COO 80210 item 1).
# This is the exact error that was made: read the field at ENTRY level, where it does
# not exist. It must FAIL the existence assertion -- if it passes, the arm cannot
# distinguish a resolved path from an absent one and is not an arm.
_wrong = copy.deepcopy(RULED)
for _e in _wrong["entries"]:
    _e["membership_computable"] = _e["relationship_partition"].pop(
        "membership_computable")            # move it UP a level: the wrong-level read
control("the field read one level too high (None x%d)" % len(_wrong["entries"]),
        path_resolves, _wrong)

# NEGATIVE CONTROL, planted BOTH ways -- a control that can only fire in one direction
# would leave the other half of the predicate unexercised.
import copy as _copy                                                    # noqa: E402
_x = _copy.deepcopy(RULED)
_x["entries"][0]["client_table"][0]["status"] = "existing"
control("a ruled value planted on the ABSENT branch", branch_vocabulary, _x)
_y = _copy.deepcopy(EVID)
_y["entries"][0]["client_table"][0]["status"] = ABSENT_STATUS
control("the absent member planted on the COMPUTABLE branch", branch_vocabulary, _y)

# 2.0.0_SA_COO 80252 item 2 -- THE OMISSION'S SAFETY CONDITION, AS AN ARM.
# account_grain_membership is OMITTED (not nulled) from the ruled leaf, because a key
# carrying null is still a key and 79869 froze that leaf's shape. But an omission is
# invisible to every presence instrument, so it is safe ONLY BECAUSE a sibling tells the
# reader why the block is missing: window.membership_basis.computable, present and
# reading false. I wrote that condition as a SENTENCE in 80248; a condition that lives
# only in prose is a protection that exists only as a description, and the next emitter
# to drop the sibling converts a safe omission into a silent one with nothing failing.
# PATHS SPELLED IN FULL, EXISTENCE BEFORE COMPARISON (1.0.0_SA_CTO 80220 discipline).
BLOCK_PATH = "window.account_grain_membership"
SIBLING_PATH = "window.membership_basis.computable"


def omission_is_explained(leaf):
    w = leaf.get("window", {})
    sibling = w.get("membership_basis", {}).get("computable")
    if not isinstance(sibling, bool):
        return False            # the sibling must RESOLVE before it can explain anything
    present = "account_grain_membership" in w
    # The block is present IFF the basis is computable; when it is absent the sibling
    # must be there AND read false, which is what makes the absence readable.
    return present == sibling


for nm, L in (("ruled/absent", RULED), ("evidence/computable", EVID)):
    w = L["window"]
    check("[%s] %s resolves, and gates %s" % (nm, SIBLING_PATH, BLOCK_PATH),
          omission_is_explained(L),
          "sibling=%r, block present=%s"
          % (w["membership_basis"]["computable"],
             "account_grain_membership" in w))

# NEGATIVE CONTROL, and it is the exact future failure COO named: drop the sibling and
# the omission becomes SILENT. The arm must fail; if it passes, the omission was never
# protected by anything.
_nosib = copy.deepcopy(RULED)
del _nosib["window"]["membership_basis"]["computable"]
control("the sibling REMOVED -- the omission goes silent", omission_is_explained, _nosib)
# And the other direction: the sibling left in place but flipped, so a present block
# would no longer be explained by it.
_flip = copy.deepcopy(RULED)
_flip["window"]["membership_basis"]["computable"] = True
control("the sibling flipped true while the block stays omitted",
        omission_is_explained, _flip)

bv = EVID["window"]["basis_version_change"]
# ---------------------------------------------------------------- REPOINTED 2026-08-29
# RULED 2.0.0_SA_COO 81723 as AMENDED by 81738, concurred 1.0.0_SA_CTO 81730, form from
# 3.0.0_SA_CVO 81733.
#
# WHAT WAS WRONG, and it is worse than "the arm went stale": the old form asserted
#     versions_differ is True AND warning AND "21.6" in warning
# which is a WORLD-STATE, and the fix INVERTED ITS POLARITY. On a correct post-rewrite
# artifact all three go False, so the arm FAILED on health; on the artifact 80410
# forbids -- one still emitting the stale literal -- it PASSED. IT ENCODED THE DEFECT AS
# THE ACCEPTANCE CRITERION. Measured: it failed against the corrected upstream while the
# producer was right.
#
# THE CONTRACT, NOT THE WORLD. An acceptance arm for a producer asserts what the PRODUCER
# GUARANTEES, not what the world happened to contain the day the arm was written. The
# guarantee is that the comparison is DISCLOSED AS FIELDS whatever the version state --
# `rekey_comparison` emits unconditionally precisely because `warning` is None exactly
# when the versions AGREE, which is the state (R) is finally read in.
rk = bv.get("rekey_comparison")


def _discloses(b):
    r = b.get("rekey_comparison")
    return (isinstance(r, dict) and isinstance(r.get("subject"), dict)
            and isinstance(r.get("control"), dict))


check("the leaf DISCLOSES the re-key comparison AS FIELDS, whatever the version state",
      _discloses(bv),
      "versions_differ=%s warning_present=%s"
      % (bv["versions_differ"], bv["warning"] is not None))
control("rekey_comparison removed -- the disclosure goes silent",
        _discloses, {k: v for k, v in bv.items() if k != "rekey_comparison"})

sub = (rk or {}).get("subject", {})
check("the derived SUBJECT carries its provenance and both sides WITH their pins",
      sub.get("basis") == "derived" and bool(sub.get("start_partition"))
      and bool(sub.get("end_partition")) and isinstance(sub.get("start_pin"), dict)
      and isinstance(sub.get("end_pin"), dict))


def _rate_recomputes(s):
    try:
        if s.get("rate_state") != "COMPUTED":
            return False
        return abs(s["rate"] - s["rekeyed_accounts"] / s["shared_accounts"]) < 1e-8
    except (KeyError, TypeError, ZeroDivisionError):
        return False


check("the derived rate RECOMPUTES from its own numerator and denominator",
      _rate_recomputes(sub),
      "%s of %s" % (sub.get("rekeyed_accounts"), sub.get("shared_accounts")))
control("the rate detached from its own numerator/denominator",
        _rate_recomputes, dict(sub, rate=(sub.get("rate") or 0.0) + 0.05))

# THE ARM FOR THE DEFECT THAT ACTUALLY OCCURRED. The pre-fix warning claimed
# "2026-07-15 -> 2026-08-18" while the leaf's own pins read 2026-07-14 -> 2026-08-27:
# it named a comparison THE EMISSION NEVER MADE. Nothing checked that, which is why the
# ratified S_R binding could parse the prose and bind to partitions the leaf never read.
_UP = EVID["window"]["upstream_pins"]


def _sides_are_the_pins(s):
    return (s.get("start_partition")
            == _UP["dimensions/dim_relationship@window_start"]["partition_date"]
            and s.get("end_partition")
            == _UP["dimensions/dim_relationship@as_of"]["partition_date"])


check("the subject's two sides ARE the partitions the emission actually read",
      _sides_are_the_pins(sub),
      "%s -> %s" % (sub.get("start_partition"), sub.get("end_partition")))
control("the subject's start side detached from the pin it was read from",
        _sides_are_the_pins, dict(sub, start_partition="1999-01-01"))

ctl = (rk or {}).get("control", {})


def _control_disowns(c):
    return (c.get("basis") == "measured" and bool(c.get("measured_at"))
            and c.get("partitions") is None and c.get("partitions_recorded") is False
            and bool(c.get("reason_partitions_absent")))


check("the DECLARED control disowns this emission and STATES ITS OWN LIMIT",
      _control_disowns(ctl),
      "measured_at=%s partitions_recorded=%s"
      % (ctl.get("measured_at"), ctl.get("partitions_recorded")))
control("the control claims recorded partitions it does not have",
        _control_disowns, dict(ctl, partitions_recorded=True))


# STATE COHERENCE (3.0.0_SA_CVO 81733, Rule 24 postulate (iv)): key the arm to the
# RELATION between the fields, never to a constant. Flipping the old `True` to `False`
# would have re-created the same defect facing the other way and broken again the first
# time a window legitimately spans two versions. These pass in BOTH worlds and still
# fail if the producer ever disagrees with itself.
def _versions_coherent(b):
    return b["versions_differ"] == (b["window_start_schema_version"]
                                    != b["as_of_schema_version"])


def _warning_coherent(b):
    return (b["warning"] is not None) == b["versions_differ"]


check("STATE COHERENCE: versions_differ agrees with the two version fields",
      _versions_coherent(bv),
      "%s vs %s -> %s" % (bv["window_start_schema_version"],
                          bv["as_of_schema_version"], bv["versions_differ"]))
control("versions_differ flipped against its own version fields",
        _versions_coherent, dict(bv, versions_differ=not bv["versions_differ"]))
check("STATE COHERENCE: the warning is present exactly when the versions differ",
      _warning_coherent(bv))
control("a warning present while the versions agree",
        _warning_coherent, dict(bv, warning="a stale sentence"))

# SECONDARY -- A REGRESSION GUARD ON ONE KNOWN STRING, AND NEVER COVERAGE OF 80410.
# 1.0.0_SA_CTO 81730 / 2.0.0_SA_COO 81738: an absence-of-one-token arm PASSES on a
# producer that hardcodes 21.7, or 1,542, or any other typed figure -- the same defect
# wearing a different literal. 80410 ruled DERIVE-OR-DECLARE, not "that string is gone".
# The DERIVATION arms above are what test the ruling; this one only guards the regression.
check("[regression guard, NOT coverage of 80410] the retired literal is absent",
      "21.6" not in (bv["warning"] or ""))

check("the ruled leaf reads ONE producer (no confound to disclose)",
      RULED["window"]["basis_version_change"]["versions_differ"] is False)

lb = EVID["window"]["label_basis"]
# REPOINTED, SAME FAULT, AND THIS ONE WAS NOT IN MY OWN FILING (81714 named two arms;
# running them found three). The old form asserted `window_start_supplies_labels is
# False` -- true ONLY in the pre-rewrite world. (S_L) is now TRUE, so the arm failed
# BECAUSE THE CAMPAIGN WORKED. It keys on label_basis rather than on versions_differ,
# which is exactly why a census scoped to the tokens I already knew about missed it.
# The contract: the leaf DECLARES the capability either way, and NAMES A REASON when it
# is absent -- never that the answer is a particular one.
def _label_declared(b):
    return (isinstance(b.get("window_start_supplies_labels"), bool)
            and (b["window_start_supplies_labels"] or bool(b.get("reason_if_absent"))))


check("the leaf DECLARES its start-vintage label capability, with a reason when absent",
      _label_declared(lb),
      "supplies_labels=%s" % lb.get("window_start_supplies_labels"))
control("label capability absent AND unexplained",
        _label_declared, dict(lb, window_start_supplies_labels=False,
                              reason_if_absent=None))

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S)/CONTROL(S) FAILED: %s" % (len(FAILS), FAILS))
else:
    print("RESULT: ALL ARMS PASS and EVERY NEGATIVE CONTROL FIRED.")
    print("Both branches scored: the ruled leaf's absence is stated with its floor and")
    print("carries no values; the evidence leaf computes, and discloses that its")
    print("numbers include producer reassignment rather than presenting them as churn.")
