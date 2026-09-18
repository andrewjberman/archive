"""LGIC_LGCTFM ROUND 2 -- the fixed input. Three cells, twelve mechanical arms.

ROUND 2 IS A HARDENING ROUND AND SAYS SO. FWD-4 closes on Andrew's own read of ANDREW_CARD.md and
FWD-6 when a real migration's decomposition is cut from the plan (LGIC_CANON's C6 practice wave).
NEITHER can be moved by a cell here. What round 2 buys is an instrument the R19 migrations can trust:
which of round 1's fourteen judgment claims a LATER seat can actually re-derive, every number bound to
its run and its content hash, and a decision card that names its own subject.

TWO CONSTRUCTION RULES, BOTH FROM DEFECTS THIS LANE COMMITTED RATHER THAN FROM PRINCIPLE.

1. EVERY ARM IS POSITION-INDEPENDENT. No arm resolves its subject by position in a directory and none
   reads `git merge-base HEAD CLOUD`. Round 1's checker did both: x1-r16 and x1-footprint measured a
   branch against its own base and read FALSE FAIL for any later seat (row S10), while x2-flag and
   x3-filed read VACUOUS PASS off-branch on an empty window and on 0 >= 0 (row S18, ruled R-47). A
   false fail announces itself; a vacuous pass does not, which is why the silent pair was found only by
   an UNSCOPED read of the shared mechanism and not from the list of observed failures.

2. EVERY CORE IS DRIVEN BOTH WAYS. `selftest-arms` runs each core against a SIMULATED CORRECT record
   and requires PASS, and against a doctored one and requires FAIL. Three of this lane's round-1 arms
   were UNSATISFIABLE BY A CORRECT FIX and all three passed their injected self-tests, because a
   fixture written by the arm's author shares the arm's assumption. A MUTANT TEST CANNOT CATCH A
   VACUOUS PASS: the mutant proves an arm CAN fail, and a vacuous arm fails it happily while passing
   everything real. Both controls, or the arm is not cut.
"""

import copy
import hashlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
BASEFILE = os.path.join(HERE, "R2_BASE.json")

DERIV_RECORD = "RE_DERIVATION_R2.json"
PINS_RECORD = "NUMBER_PINS_R2.json"

LANE = "2.0.0_SA_COO~G"


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


def git(*args):
    try:
        r = subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout
    except Exception as exc:
        return 1, str(exc)


def record_path(name):
    """The worker slot is NOT hard-coded: whichever slot wrote the record owns it. A cell's record is
    found by EXISTENCE across the slots, never by assuming slot 1 -- round 6 of LGIC_ENFORCE had two
    orders on one slot and a sibling project had four slots on one round."""
    for n in ("1", "2", "3", "4"):
        p = "%s/deliverables/0.9.0_WK_LGIC_LGCTFM~%s/%s" % (ROOT, n, name)
        if os.path.isfile(ab(p)):
            return p
    return "%s/deliverables/0.9.0_WK_LGIC_LGCTFM~1/%s" % (ROOT, name)


def tracked(p):
    """(bool, note) -- is this path TRACKED by git? Row LGIC_ENFORCE-S69: a record that cites an
    UNTRACKED instrument has an unverifiable claim at its centre, and the drain deletes the evidence as
    routine hygiene. Nothing in the estate grades an `instrument` string, so this arm does."""
    rc, _ = git("ls-files", "--error-unmatch", p)
    return rc == 0, ("TRACKED" if rc == 0 else "NOT TRACKED -- git ls-files --error-unmatch refuses it")


# ==================================================================== LT-a-2, the re-derivation record
def core_a2_partition(rec, expected_ids):
    """Every round-1 judgment claim in EXACTLY ONE class, over the denominator the ORDERS give."""
    lines = []
    if not isinstance(rec, dict):
        return False, ["the record does not parse as an object"]
    red = rec.get("re_derived")
    nrd = rec.get("not_re_derivable")
    if not isinstance(red, list) or not isinstance(nrd, list):
        return False, ["re_derived and not_re_derivable must both be lists"]
    rid = [r.get("criterion") for r in red if isinstance(r, dict)]
    nid = [r.get("criterion") for r in nrd if isinstance(r, dict)]
    both = sorted(set(rid) & set(nid))
    seen = set(rid) | set(nid)
    missing = sorted(set(expected_ids) - seen)
    extra = sorted(seen - set(expected_ids))
    lines.append("round-1 judgment criteria the ORDERS carry: %d" % len(expected_ids))
    lines.append("classified RE_DERIVED %d + NOT_RE_DERIVABLE %d = %d" % (len(rid), len(nid), len(rid) + len(nid)))
    lines.append("in BOTH classes (must be empty): %s" % both)
    lines.append("MISSING from the partition (must be empty): %s" % missing)
    lines.append("classified but not a round-1 judgment criterion (must be empty): %s" % extra)
    ok = not both and not missing and not extra and len(seen) == len(expected_ids)
    return ok, lines


def core_a2_mechanism(rec):
    """A NOT_RE_DERIVABLE entry states its MECHANISM and what it OBSERVED. A class with no mechanism is
    an opinion; the observed verdict is what makes it a measurement."""
    lines = []
    nrd = (rec or {}).get("not_re_derivable")
    if not isinstance(nrd, list):
        return False, ["not_re_derivable is not a list"]
    bad_mech = [r.get("criterion") for r in nrd
                if not isinstance(r, dict) or not str(r.get("mechanism") or "").strip()]
    bad_obs = [r.get("criterion") for r in nrd
               if not isinstance(r, dict) or not str(r.get("verdict_observed") or "").strip()]
    lines.append("NOT_RE_DERIVABLE entries: %d" % len(nrd))
    lines.append("without a mechanism (must be 0): %d %s" % (len(bad_mech), bad_mech[:6]))
    lines.append("without an observed verdict (must be 0): %d %s" % (len(bad_obs), bad_obs[:6]))
    return (not bad_mech and not bad_obs), lines


def core_a2_floor(rec, floor_arms):
    """FOUR IS A FLOOR, NOT AN ANSWER. The known arms must appear, AND the count must be >= 4 -- a
    partition that lands on exactly the handed list has probably worked from the list."""
    lines = []
    nrd = (rec or {}).get("not_re_derivable")
    if not isinstance(nrd, list):
        return False, ["not_re_derivable is not a list"]
    blob = json.dumps(nrd)
    present = [a for a in floor_arms if a in blob]
    lines.append("known checkout-dependent arms named in the record: %d of %d %s"
                 % (len(present), len(floor_arms), present))
    lines.append("NOT_RE_DERIVABLE count: %d (the FLOOR is %d)" % (len(nrd), len(floor_arms)))
    if len(nrd) == len(floor_arms):
        lines.append("NOTE: the count EQUALS the floor -- admissible, but the record must carry an "
                     "`unscoped_read` note saying how the population was searched rather than taken")
    unscoped = str((rec or {}).get("unscoped_read") or "").strip()
    lines.append("`unscoped_read` note present: %s" % bool(unscoped))
    ok = len(present) == len(floor_arms) and len(nrd) >= len(floor_arms) and bool(unscoped)
    return ok, lines


def core_a2_instrument(rec, tracked_fn):
    """The cited instrument must be a path a LATER READER CAN REACH. Row LGIC_ENFORCE-S69."""
    lines = []
    inst = str((rec or {}).get("instrument_path") or "").strip()
    lines.append("record's declared instrument_path: %r" % inst)
    if not inst:
        return False, lines + ["no instrument_path declared"]
    ok, note = tracked_fn(inst)
    lines.append("git ls-files --error-unmatch: %s" % note)
    pos = str((rec or {}).get("ran_from") or "").strip()
    lines.append("declared THIRD POSITION it ran from: %r" % pos)
    return (ok and bool(pos)), lines


# ============================================================================ LT-n-2, the number pins
def core_n2_subtraction(rec):
    """The set is a SUBTRACTION from a printed denominator, never a forward list (Rule 24(i))."""
    lines = []
    if not isinstance(rec, dict):
        return False, ["the record does not parse as an object"]
    den = rec.get("denominator")
    src = str(rec.get("denominator_source") or "").strip()
    found = rec.get("numbers_found")
    pinned = rec.get("pinned")
    excluded = rec.get("excluded")
    for name, v, want in (("numbers_found", found, list), ("pinned", pinned, list),
                          ("excluded", excluded, dict)):
        if not isinstance(v, want):
            return False, lines + ["%s must be a %s" % (name, want.__name__)]
    lines.append("denominator %r from %r" % (den, src[:90]))
    lines.append("numbers_found %d = pinned %d + excluded %d ?  %s"
                 % (len(found), len(pinned), len(excluded),
                    len(found) == len(pinned) + len(excluded)))
    ok = (bool(src) and isinstance(den, int) and den > 0
          and len(found) == len(pinned) + len(excluded) and len(found) > 0)
    return ok, lines


def core_n2_e3(rec, excluded_by_name):
    """E3 is excluded BY NAME with a reason. The analysis says so in terms, and a silent omission and a
    stated exclusion are different states."""
    lines = []
    exc = (rec or {}).get("excluded")
    if not isinstance(exc, dict):
        return False, ["excluded is not an object"]
    lines.append("excluded ids: %s" % sorted(exc.keys()))
    miss = [k for k in excluded_by_name if k not in exc]
    noreason = [k for k in excluded_by_name if k in exc and not str(exc.get(k) or "").strip()]
    lines.append("required exclusions missing (must be empty): %s" % miss)
    lines.append("required exclusions with no reason (must be empty): %s" % noreason)
    return (not miss and not noreason), lines


def core_n2_pins(rec):
    """Every pinned number carries its run id, its content hash AND THE INSTRUMENT."""
    lines = []
    pinned = (rec or {}).get("pinned")
    if not isinstance(pinned, list):
        return False, ["pinned is not a list"]
    no_run = [p.get("number") for p in pinned if not str((p or {}).get("run_id") or "").strip()]
    no_hash = [p.get("number") for p in pinned if not str((p or {}).get("content_hash") or "").strip()]
    lines.append("pinned numbers: %d" % len(pinned))
    lines.append("without a run_id (must be 0): %d %s" % (len(no_run), no_run[:6]))
    lines.append("without a content_hash (must be 0): %d %s" % (len(no_hash), no_hash[:6]))
    return (not no_run and not no_hash and len(pinned) > 0), lines


def core_n2_hash_instrument(rec):
    """A HASH WITHOUT ITS INSTRUMENT IS TWO NUMBERS. `git hash-object` prefixes `blob <len>` and a NUL
    byte, so a plain sha1 of the same bytes disagrees -- measured on this project's own contract.json:
    33204e29... by git hash-object, 9c5cdb87... by sha1. This seat computed the plain one first and
    briefly read it as a MISMATCH against a hash it had already published."""
    lines = []
    pinned = (rec or {}).get("pinned")
    if not isinstance(pinned, list):
        return False, ["pinned is not a list"]
    bad = [p.get("number") for p in pinned if not str((p or {}).get("hash_instrument") or "").strip()]
    lines.append("pinned numbers: %d" % len(pinned))
    lines.append("without a hash_instrument (must be 0): %d %s" % (len(bad), bad[:8]))
    return (not bad and len(pinned) > 0), lines


# ================================================================================ LT-c-2, the card
def card_parts(text):
    lines = text.split("\n")
    tbl = [ln for ln in lines if ln.startswith("| ")]
    idx = [i for i, ln in enumerate(lines) if ln.startswith("**RECOMMENDATION")]
    rec = "\n".join(lines[idx[0]:idx[0] + 4]) if idx else ""
    return "\n".join(tbl), rec, len(tbl)


def core_c2_names_run(text, run_id, chash):
    """The card must name its own subject ON ITS FACE -- the run id, the content hash, and the word
    that says which instrument produced the hash."""
    lines = []
    if text is None:
        return False, ["the card could not be read"]
    has_run = run_id in text
    has_hash = chash in text
    has_inst = "hash-object" in text
    lines.append("run id %r on its face: %s" % (run_id, has_run))
    lines.append("contract content hash on its face: %s" % has_hash)
    lines.append("the hash's INSTRUMENT named on its face (hash-object): %s" % has_inst)
    return (has_run and has_hash and has_inst), lines


def core_c2_frozen(text, want_tbl_sha, want_rec_sha, want_rows):
    """THE RANKING AND THE RECOMMENDATION MUST NOT MOVE. S6's condition was that the card's correction
    reach the decision-maker BESIDE it rather than as a silent rewrite, and it did, by
    1.0.0_SA_CTO's adjudication. So this cell ADDS a pin and a pointer and changes neither."""
    lines = []
    if text is None:
        return False, ["the card could not be read"]
    tbl, rec, rows = card_parts(text)
    got_t = hashlib.sha1(tbl.encode("utf-8")).hexdigest()
    got_r = hashlib.sha1(rec.encode("utf-8")).hexdigest()
    lines.append("ranking table rows %d (pinned %d)" % (rows, want_rows))
    lines.append("table sha1     %s (pinned %s) identical %s" % (got_t, want_tbl_sha, got_t == want_tbl_sha))
    lines.append("recommendation sha1 %s (pinned %s) identical %s" % (got_r, want_rec_sha, got_r == want_rec_sha))
    return (got_t == want_tbl_sha and got_r == want_rec_sha and rows == want_rows), lines


# ============================================================================ the real subcommands
def a2_partition():
    b = base()
    rec = load_json(record_path(DERIV_RECORD))
    ids = sorted((b.get("round_1_judgment_criteria") or {}).get("by_id", {}).keys())
    if rec is None:
        return say("FAIL-A2-PARTITION-COVERS-ROUND-1", "record not found at %s" % record_path(DERIV_RECORD))
    ok, lines = core_a2_partition(rec, ids)
    return verdict(ok, "PASS-A2-PARTITION-COVERS-ROUND-1", "FAIL-A2-PARTITION-COVERS-ROUND-1", lines)


def a2_mechanism():
    rec = load_json(record_path(DERIV_RECORD))
    if rec is None:
        return say("FAIL-A2-EVERY-CLASS-NAMES-ITS-MECHANISM", "record not found")
    ok, lines = core_a2_mechanism(rec)
    return verdict(ok, "PASS-A2-EVERY-CLASS-NAMES-ITS-MECHANISM",
                   "FAIL-A2-EVERY-CLASS-NAMES-ITS-MECHANISM", lines)


def a2_floor():
    b = base()
    rec = load_json(record_path(DERIV_RECORD))
    arms = (b.get("checkout_dependent_arms_KNOWN") or {}).get("arms", [])
    if rec is None:
        return say("FAIL-A2-KNOWN-FOUR-ARE-A-FLOOR", "record not found")
    ok, lines = core_a2_floor(rec, arms)
    return verdict(ok, "PASS-A2-KNOWN-FOUR-ARE-A-FLOOR", "FAIL-A2-KNOWN-FOUR-ARE-A-FLOOR", lines)


def a2_instrument():
    rec = load_json(record_path(DERIV_RECORD))
    if rec is None:
        return say("FAIL-A2-INSTRUMENT-IS-TRACKED", "record not found")
    ok, lines = core_a2_instrument(rec, tracked)
    return verdict(ok, "PASS-A2-INSTRUMENT-IS-TRACKED", "FAIL-A2-INSTRUMENT-IS-TRACKED", lines)


def n2_subtraction():
    rec = load_json(record_path(PINS_RECORD))
    if rec is None:
        return say("FAIL-N2-SET-IS-A-SUBTRACTION", "record not found at %s" % record_path(PINS_RECORD))
    ok, lines = core_n2_subtraction(rec)
    return verdict(ok, "PASS-N2-SET-IS-A-SUBTRACTION", "FAIL-N2-SET-IS-A-SUBTRACTION", lines)


def n2_e3():
    b = base()
    rec = load_json(record_path(PINS_RECORD))
    req = sorted((b.get("excluded_by_name") or {}).keys())
    if rec is None:
        return say("FAIL-N2-E3-EXCLUDED-BY-NAME", "record not found")
    ok, lines = core_n2_e3(rec, req)
    return verdict(ok, "PASS-N2-E3-EXCLUDED-BY-NAME", "FAIL-N2-E3-EXCLUDED-BY-NAME", lines)


def n2_pins():
    rec = load_json(record_path(PINS_RECORD))
    if rec is None:
        return say("FAIL-N2-EVERY-NUMBER-CARRIES-ITS-RUN", "record not found")
    ok, lines = core_n2_pins(rec)
    return verdict(ok, "PASS-N2-EVERY-NUMBER-CARRIES-ITS-RUN",
                   "FAIL-N2-EVERY-NUMBER-CARRIES-ITS-RUN", lines)


def n2_hash_instrument():
    rec = load_json(record_path(PINS_RECORD))
    if rec is None:
        return say("FAIL-N2-EVERY-HASH-NAMES-ITS-INSTRUMENT", "record not found")
    ok, lines = core_n2_hash_instrument(rec)
    return verdict(ok, "PASS-N2-EVERY-HASH-NAMES-ITS-INSTRUMENT",
                   "FAIL-N2-EVERY-HASH-NAMES-ITS-INSTRUMENT", lines)


def c2_names_run():
    b = base()
    g = b.get("graded_run_round_1") or {}
    text = read((b.get("card") or {}).get("path", ""))
    ok, lines = core_c2_names_run(text, g.get("run_id", ""), g.get("contract_git_hash_object", ""))
    return verdict(ok, "PASS-C2-CARD-NAMES-ITS-RUN-AND-HASH",
                   "FAIL-C2-CARD-NAMES-ITS-RUN-AND-HASH", lines)


def c2_frozen():
    b = base()
    c = b.get("card") or {}
    text = read(c.get("path", ""))
    ok, lines = core_c2_frozen(text, c.get("ranking_table_sha1", ""),
                               c.get("recommendation_paragraph_sha1", ""),
                               c.get("ranking_table_rows", 0))
    return verdict(ok, "PASS-C2-RANKING-AND-RECOMMENDATION-UNCHANGED",
                   "FAIL-C2-RANKING-AND-RECOMMENDATION-UNCHANGED", lines)


def c2_pointer():
    b = base()
    text = read((b.get("card") or {}).get("path", ""))
    lines = []
    if text is None:
        return say("FAIL-C2-CARD-POINTS-AT-THE-ADJUDICATION", "the card could not be read")
    has = "662d53b793" in text
    lines.append("the adjudication commit 662d53b793 cited on the card's face: %s" % has)
    lines.append("NOT REQUIRED and NOT GRADED: any change to the recommendation's wording. S6's "
                 "condition was that the correction reach the decision-maker BESIDE the card, and the "
                 "adjudication is that carrier.")
    return verdict(has, "PASS-C2-CARD-POINTS-AT-THE-ADJUDICATION",
                   "FAIL-C2-CARD-POINTS-AT-THE-ADJUDICATION", lines)


# ================================================================================ the arm self-test
GOOD_DERIV = {
    "instrument_path": "org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_lt_r2.py",
    "ran_from": "a fresh detached checkout at the drained tip, neither round-1 branch nor its grader",
    "unscoped_read": "grep of base_ref() and of _last_two() over the whole round-1 checker, then every caller inspected",
    "re_derived": [],
    "not_re_derivable": [],
}

GOOD_PINS = {
    "denominator": 3,
    "denominator_source": "every number cited in round 1's judgment evidence, enumerated from the instances",
    "numbers_found": ["P1R1-AC6:1626", "X1R1-AC6:1074", "E3R1-AC6:271"],
    "pinned": [
        {"number": "P1R1-AC6:1626", "run_id": "20260918T011619Z-8db9eb1",
         "content_hash": "33204e29839de89af81fb293317cce3ccdf2266d", "hash_instrument": "git hash-object"},
        {"number": "X1R1-AC6:1074", "run_id": "20260918T011619Z-8db9eb1",
         "content_hash": "f26d46db87f3d8bcbf7b7ff13dafe708030c6d48", "hash_instrument": "git hash-object"},
    ],
    "excluded": {"E3R1-AC6": "sound at its own vintage; not re-graded against R-40"},
}


def selftest_arms():
    b = base()
    ids = sorted((b.get("round_1_judgment_criteria") or {}).get("by_id", {}).keys())
    arms = (b.get("checkout_dependent_arms_KNOWN") or {}).get("arms", [])
    req_exc = sorted((b.get("excluded_by_name") or {}).keys())
    res = []

    def arm(name, good_ok, bad_ok, why):
        res.append((name, good_ok and not bad_ok, why))

    # ---- a SIMULATED CORRECT re-derivation record, built from the pinned denominator ----------
    good = copy.deepcopy(GOOD_DERIV)
    good["not_re_derivable"] = [
        {"criterion": ids[i], "arm": arms[i] if i < len(arms) else "x?",
         "mechanism": "resolves its subject by position or by branch base",
         "verdict_observed": "PASS on an empty window"} for i in range(len(arms))
    ]
    good["re_derived"] = [{"criterion": c, "how": "re-ran the cited invocation from the third position"}
                          for c in ids[len(arms):]]

    res.append(("POSITIVE-a2-partition", core_a2_partition(good, ids)[0], "a correct record must PASS"))
    res.append(("POSITIVE-a2-mechanism", core_a2_mechanism(good)[0], "a correct record must PASS"))
    res.append(("POSITIVE-a2-floor", core_a2_floor(good, arms)[0], "a correct record must PASS"))
    res.append(("POSITIVE-a2-instrument",
                core_a2_instrument(good, lambda p: (True, "TRACKED (stub)"))[0], "a correct record must PASS"))

    short = copy.deepcopy(good)
    short["re_derived"] = short["re_derived"][:-1]
    dup = copy.deepcopy(good)
    dup["re_derived"] = dup["re_derived"] + [{"criterion": ids[0], "how": "x"}]
    arm("a2-partition", core_a2_partition(good, ids)[0], core_a2_partition(short, ids)[0],
        "a claim in neither class")
    arm("a2-partition-double", core_a2_partition(good, ids)[0], core_a2_partition(dup, ids)[0],
        "a claim in BOTH classes")
    nomech = copy.deepcopy(good)
    nomech["not_re_derivable"][0].pop("mechanism")
    noobs = copy.deepcopy(good)
    noobs["not_re_derivable"][0]["verdict_observed"] = ""
    arm("a2-mechanism", core_a2_mechanism(good)[0], core_a2_mechanism(nomech)[0],
        "a NOT_RE_DERIVABLE class with no mechanism")
    arm("a2-mechanism-observed", core_a2_mechanism(good)[0], core_a2_mechanism(noobs)[0],
        "a class asserting a failure it never observed")
    dropped = copy.deepcopy(good)
    dropped["not_re_derivable"] = dropped["not_re_derivable"][:-1]
    nounsc = copy.deepcopy(good)
    nounsc["unscoped_read"] = ""
    arm("a2-floor", core_a2_floor(good, arms)[0], core_a2_floor(dropped, arms)[0],
        "a known checkout-dependent arm missing from the record")
    arm("a2-floor-unscoped", core_a2_floor(good, arms)[0], core_a2_floor(nounsc, arms)[0],
        "the floor met with no account of how the population was searched")
    noinst = copy.deepcopy(good)
    noinst["instrument_path"] = ""
    arm("a2-instrument", core_a2_instrument(good, lambda p: (True, "stub"))[0],
        core_a2_instrument(noinst, lambda p: (True, "stub"))[0], "no instrument declared")
    arm("a2-instrument-untracked", core_a2_instrument(good, lambda p: (True, "stub"))[0],
        core_a2_instrument(good, lambda p: (False, "NOT TRACKED"))[0],
        "an instrument no later reader can reach")

    # ---- a SIMULATED CORRECT pins record ------------------------------------------------------
    gp = copy.deepcopy(GOOD_PINS)
    gp["excluded"] = {k: "stated reason" for k in req_exc} or gp["excluded"]
    gp["numbers_found"] = [p["number"] for p in gp["pinned"]] + sorted(gp["excluded"].keys())
    gp["denominator"] = len(gp["numbers_found"])
    res.append(("POSITIVE-n2-subtraction", core_n2_subtraction(gp)[0], "a correct record must PASS"))
    res.append(("POSITIVE-n2-e3", core_n2_e3(gp, req_exc)[0], "a correct record must PASS"))
    res.append(("POSITIVE-n2-pins", core_n2_pins(gp)[0], "a correct record must PASS"))
    res.append(("POSITIVE-n2-hash-instrument", core_n2_hash_instrument(gp)[0], "a correct record must PASS"))

    nosrc = copy.deepcopy(gp)
    nosrc["denominator_source"] = ""
    mismatch = copy.deepcopy(gp)
    mismatch["numbers_found"] = mismatch["numbers_found"] + ["ghost"]
    arm("n2-subtraction", core_n2_subtraction(gp)[0], core_n2_subtraction(nosrc)[0],
        "a set with no denominator source -- a forward list wearing a count")
    arm("n2-subtraction-sums", core_n2_subtraction(gp)[0], core_n2_subtraction(mismatch)[0],
        "found != pinned + excluded")
    dropexc = copy.deepcopy(gp)
    dropexc["excluded"] = {}
    noreason = copy.deepcopy(gp)
    noreason["excluded"] = {k: "" for k in req_exc}
    arm("n2-e3", core_n2_e3(gp, req_exc)[0], core_n2_e3(dropexc, req_exc)[0],
        "E3 silently omitted instead of excluded by name")
    arm("n2-e3-reason", core_n2_e3(gp, req_exc)[0], core_n2_e3(noreason, req_exc)[0],
        "excluded with no reason")
    norun = copy.deepcopy(gp)
    norun["pinned"][0]["run_id"] = ""
    nohash = copy.deepcopy(gp)
    nohash["pinned"][0]["content_hash"] = ""
    arm("n2-pins-run", core_n2_pins(gp)[0], core_n2_pins(norun)[0], "a number naming no run")
    arm("n2-pins-hash", core_n2_pins(gp)[0], core_n2_pins(nohash)[0], "a number carrying no content hash")
    noi = copy.deepcopy(gp)
    noi["pinned"][1]["hash_instrument"] = ""
    arm("n2-hash-instrument", core_n2_hash_instrument(gp)[0], core_n2_hash_instrument(noi)[0],
        "a hash with no instrument -- two numbers wearing one name")

    # ---- the card -----------------------------------------------------------------------------
    b2 = base()
    c = b2.get("card") or {}
    g = b2.get("graded_run_round_1") or {}
    orig = read(c.get("path", "")) or ""
    good_card = orig.replace(
        "## The subject",
        "## The subject\n\nRun `%s`, contract content hash `%s` by `git hash-object`; ranking confirmed "
        "by adjudication 662d53b793.\n" % (g.get("run_id", ""), g.get("contract_git_hash_object", "")), 1)
    res.append(("POSITIVE-c2-names-run",
                core_c2_names_run(good_card, g.get("run_id", ""), g.get("contract_git_hash_object", ""))[0],
                "a correctly pinned card must PASS"))
    res.append(("POSITIVE-c2-frozen",
                core_c2_frozen(good_card, c.get("ranking_table_sha1", ""),
                               c.get("recommendation_paragraph_sha1", ""), c.get("ranking_table_rows", 0))[0],
                "a pin that touches neither table nor recommendation must PASS"))
    arm("c2-names-run",
        core_c2_names_run(good_card, g.get("run_id", ""), g.get("contract_git_hash_object", ""))[0],
        core_c2_names_run(orig, g.get("run_id", ""), g.get("contract_git_hash_object", ""))[0],
        "the card as it stands, naming no run")
    moved = good_card.replace("| 1 | T-0001 |", "| 1 | T-9999 |", 1)
    arm("c2-frozen-table",
        core_c2_frozen(good_card, c.get("ranking_table_sha1", ""),
                       c.get("recommendation_paragraph_sha1", ""), c.get("ranking_table_rows", 0))[0],
        core_c2_frozen(moved, c.get("ranking_table_sha1", ""),
                       c.get("recommendation_paragraph_sha1", ""), c.get("ranking_table_rows", 0))[0],
        "a change to the ranking table")
    reworded = good_card.replace("**RECOMMENDATION:** Accept", "**RECOMMENDATION:** Reject", 1)
    arm("c2-frozen-recommendation",
        core_c2_frozen(good_card, c.get("ranking_table_sha1", ""),
                       c.get("recommendation_paragraph_sha1", ""), c.get("ranking_table_rows", 0))[0],
        core_c2_frozen(reworded, c.get("ranking_table_sha1", ""),
                       c.get("recommendation_paragraph_sha1", ""), c.get("ranking_table_rows", 0))[0],
        "a silent rewrite of the recommendation -- the act S6 exists to prevent")

    pos = [r for r in res if r[0].startswith("POSITIVE-")]
    mut = [r for r in res if not r[0].startswith("POSITIVE-")]
    for name, ok, why in res:
        print("  %-30s %s  %s" % (name, "PASS" if ok else "FAIL", why))
    allok = all(ok for _, ok, _ in res)
    print("arms driven: %d (%d POSITIVE-SATISFIABILITY against simulated correct records, %d mutant)"
          % (len(res), len(pos), len(mut)))
    print("NOT driven here, stated: tracked() itself, whose content is a live git call -- it has no "
          "fixture and is exercised by the real run, where a2-instrument reads it against the record's "
          "own declared path.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if allok else "FAIL-ARMS-DO-NOT-DISCRIMINATE"))
    return 0


CMDS = {
    "a2-partition": a2_partition, "a2-mechanism": a2_mechanism, "a2-floor": a2_floor,
    "a2-instrument": a2_instrument,
    "n2-subtraction": n2_subtraction, "n2-e3": n2_e3, "n2-pins": n2_pins,
    "n2-hash-instrument": n2_hash_instrument,
    "c2-names-run": c2_names_run, "c2-frozen": c2_frozen, "c2-pointer": c2_pointer,
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
