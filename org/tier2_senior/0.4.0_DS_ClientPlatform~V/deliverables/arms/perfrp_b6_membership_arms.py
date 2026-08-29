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
def branch_vocabulary(leaf):
    computable = leaf["window"]["membership_basis"]["computable"]
    allowed = set(COMPUTABLE) if computable else {ABSENT_STATUS}
    return not [1 for r in rows_of(leaf) if r["status"] not in allowed]


for nm, L in (("ruled/absent", RULED), ("evidence/computable", EVID)):
    check("[%s] status vocabulary matches the BRANCH, never crosses" % nm,
          branch_vocabulary(L),
          "computable=%s, %d rows" % (L["window"]["membership_basis"]["computable"],
                                      len(rows_of(L))))

# NEGATIVE CONTROL, planted BOTH ways -- a control that can only fire in one direction
# would leave the other half of the predicate unexercised.
import copy as _copy                                                    # noqa: E402
_x = _copy.deepcopy(RULED)
_x["entries"][0]["client_table"][0]["status"] = "existing"
control("a ruled value planted on the ABSENT branch", branch_vocabulary, _x)
_y = _copy.deepcopy(EVID)
_y["entries"][0]["client_table"][0]["status"] = ABSENT_STATUS
control("the absent member planted on the COMPUTABLE branch", branch_vocabulary, _y)

bv = EVID["window"]["basis_version_change"]
check("the evidence leaf DISCLOSES the producer confound on its face",
      bv["versions_differ"] is True and bv["warning"] and "21.6" in bv["warning"],
      "spine %s -> %s" % (bv["window_start_schema_version"],
                          bv["as_of_schema_version"]))
check("the ruled leaf reads ONE producer (no confound to disclose)",
      RULED["window"]["basis_version_change"]["versions_differ"] is False)
lb = EVID["window"]["label_basis"]
check("the evidence leaf declares its start vintage supplies NO labels",
      lb["window_start_supplies_labels"] is False and lb["reason_if_absent"])

print()
print("=" * 78)
if FAILS:
    print("RESULT: %d ARM(S)/CONTROL(S) FAILED: %s" % (len(FAILS), FAILS))
else:
    print("RESULT: ALL ARMS PASS and EVERY NEGATIVE CONTROL FIRED.")
    print("Both branches scored: the ruled leaf's absence is stated with its floor and")
    print("carries no values; the evidence leaf computes, and discloses that its")
    print("numbers include producer reassignment rather than presenting them as churn.")
