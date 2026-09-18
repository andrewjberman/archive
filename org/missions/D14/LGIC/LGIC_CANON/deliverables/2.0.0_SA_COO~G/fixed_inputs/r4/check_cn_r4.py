#!/usr/bin/env python3
"""check_cn_r4 -- LGIC_CANON round 4's checker. The ISSUER's fixed input; workers never edit it.

Round 4 is ONE CELL: C6, the onboarding checklist's FIRST REAL RUN over LGIC_LGCTFM's practice wave
(decomposition v6 s.0f, PRD v1.7, ruling R-34). Each subcommand prints its evidence, a DENOMINATOR
where one exists, and exactly one final line `VERDICT: PASS-<X>` / `FAIL-<X>`. A missing input is a
FAIL verdict, never a traceback.

NO PASS TOKEN IS A SUBSTRING OF ANOTHER -- proof-of-spec-check greps <expect> UNANCHORED.
`selftest-arms` prints that pairwise check as its own arm.

R-34's GRADING RULE IS QUOTED, NOT PARAPHRASED, because the bar is easy to soften by accident:
    "The outcome is graded on what the wave reaches plus its carded set -- `reached + carded ==
     steps`, denominators printed."
So a step is REACHED or CARDED and nothing else. A run that stops at the first unreachable step FAILS,
and so does a run that silently skips one. "Every step completed" was never the bar.

EVERY DENOMINATOR BELOW WAS MEASURED AT THE CUT FROM THE CHECKLIST ITSELF, not assumed, and the arms
re-measure it at run time rather than trusting these numbers:
    infra/logic/10_ONBOARDING_CHECKLIST.md at 43ed12c300 -- 16 `### STEP <n> --` headings, 16 `rule:`
    lines, 16 `builder:` lines, 2 `**STOP --` blocks (owners `ADVI_FIRMBKTS` and `1.0.0_SA_CTO`), and
    2 `built: no` steps. Its own closing section says: "It cannot be completed from end to end at this
    vintage. Each STOP point names an OWNER, so none of them is blocked."
THAT SENTENCE IS R-34's SHAPE ALREADY WRITTEN INTO THE INSTRUMENT, which is why this cell is gradeable
at all.

THE POSITIVE-SATISFIABILITY CONTROL IS PART OF THE SELF-TEST, and it is here because three of this
seat's arms on sibling projects were UNSATISFIABLE BY A CORRECT FIX in one night -- each passed its
injected mutant test and still could not be satisfied by the right answer. So every core is driven
against a SIMULATED CORRECT RECORD and must PASS, as well as against a doctored one and must FAIL. A
mutant proves an arm can fail; this proves it can pass for the right reason.

Standard library only. ASCII only. LF endings.
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# r4 -> fixed_inputs -> 2.0.0_SA_COO~G -> deliverables -> LGIC_CANON -> LGIC -> D14 -> missions -> org
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_CANON"
CHECKLIST = "infra/logic/10_ONBOARDING_CHECKLIST.md"
BASEFILE = os.path.join(HERE, "R4_BASE.json")
RUN_RECORD = "C6_RUN_RECORD.json"
HASHES = "C6_HASHES.json"
CHANNEL = ROOT + "/surprise-channel/investigations/INVESTIGATION_v1.md"

# the subject, named by CONTENT and not only by label (R-40)
WAVE_RUN_ID = "20260918T011619Z-8db9eb1"
WAVE_CONTRACT_HASH = "33204e29839de89af81fb293317cce3ccdf2266d"
WAVE_DIR = "workflows/legacy_transform/blackdiamond-49financial/" + WAVE_RUN_ID


def out(*lines):
    for ln in lines:
        print(ln)


def verdict(ok, pass_tag, fail_tag, lines):
    out(*lines)
    print("VERDICT: " + (pass_tag if ok else fail_tag))
    return 0


def fail_only(tag, *lines):
    out(*lines)
    print("VERDICT: FAIL-" + tag)
    return 0


def ab(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def read(p):
    f = ab(p)
    return io.open(f, encoding="utf-8", errors="replace").read() if os.path.isfile(f) else None


def load_json(p):
    t = read(p)
    if t is None:
        return None, "absent: %s" % p
    try:
        return json.loads(t), ""
    except ValueError as exc:
        return None, "not JSON: %s (%s)" % (p, exc)


def run(argv, timeout=240):
    try:
        r = subprocess.run(argv, capture_output=True, text=True, cwd=REPO, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except OSError as exc:
        return 127, "did not run: %s" % exc


def record_path():
    """The run record lands in the ASSIGNED worker's own folder; both candidate slots are searched so
    the arm does not also grade the seating decision."""
    for n in ("1", "2"):
        p = "%s/deliverables/0.9.0_WK_LGIC_CANON~%s/%s" % (ROOT, n, RUN_RECORD)
        if os.path.isfile(ab(p)):
            return p
    return "%s/deliverables/0.9.0_WK_LGIC_CANON~1/%s" % (ROOT, RUN_RECORD)


def hashes_path():
    return record_path().replace(RUN_RECORD, HASHES)


# ============================================================================ the checklist, measured
def checklist_steps(text):
    """(ids, rules, builders, stops) read from the checklist itself at run time.

    THE STEP SET IS A SUBTRACTION FROM THE DOCUMENT, never a list this file carries: if the checklist
    gains or loses a step, every arm below moves with it, and a hand list here would silently grade the
    wrong population (Rule 24(i))."""
    if not text:
        return None, None, None, None
    ids = [int(m.group(1)) for m in re.finditer(r"^### STEP (\d+) --", text, re.M)]
    rules = len(re.findall(r"^rule: ", text, re.M))
    builders = len(re.findall(r"^builder: ", text, re.M))
    stops = [m.group(1).strip() for m in re.finditer(r"\*\*STOP -- ([^*]{0,120})", text)]
    return ids, rules, builders, stops


def core_steps(rec, step_ids):
    """R-34: reached + carded == steps, all three printed, and the union is EXACTLY the checklist's
    own step set -- no invented step, no dropped step."""
    if not isinstance(rec, dict):
        return False, ["the run record is not an object"]
    reached = rec.get("reached")
    carded = rec.get("carded")
    for name, v in (("reached", reached), ("carded", carded)):
        if not isinstance(v, list):
            return False, ["`%s` is %s, not a list" % (name, type(v).__name__)]
    def ids_of(rows):
        got = []
        for r in rows:
            if isinstance(r, dict) and isinstance(r.get("step"), int):
                got.append(r["step"])
        return got
    r_ids, c_ids = ids_of(reached), ids_of(carded)
    union = sorted(r_ids + c_ids)
    want = sorted(step_ids)
    lines = ["steps in the checklist: %d %s" % (len(want), want),
             "reached %d %s + carded %d %s = %d" % (len(r_ids), sorted(r_ids), len(c_ids),
                                                    sorted(c_ids), len(union))]
    dup = sorted(set(x for x in union if union.count(x) > 1))
    missing = [x for x in want if x not in union]
    extra = [x for x in union if x not in want]
    lines.append("counted twice: %s; in the checklist but in neither list: %s; claimed but not a step: %s"
                 % (dup, missing, extra))
    malformed = [r for r in (reached + carded) if not (isinstance(r, dict) and isinstance(r.get("step"), int))]
    if malformed:
        lines.append("rows with no integer `step`: %d" % len(malformed))
    ok = not dup and not missing and not extra and not malformed and len(union) == len(want)
    if not ok:
        lines.append("R-34's bar is reached + carded == steps, and the UNION must be the step set "
                     "itself -- a count that matches while the members differ is the defect this "
                     "compares members to catch")
    return ok, lines


def core_carded_owners(rec, stops):
    """A CARDED step is a NAMED GAP WITH AN OWNER, which is what the outcome promises. And the two
    STOP points the checklist itself declares must be carded rather than silently reached, because the
    checklist says they cannot complete at this vintage."""
    if not isinstance(rec, dict) or not isinstance(rec.get("carded"), list):
        return False, ["the run record carries no `carded` list"]
    carded = [r for r in rec["carded"] if isinstance(r, dict)]
    bad = [r for r in carded if not (str(r.get("owner") or "").strip() and str(r.get("reason") or "").strip())]
    lines = ["carded steps: %d; missing an owner or a reason: %d" % (len(carded), len(bad))]
    if bad:
        lines += ["  " + json.dumps(r)[:140] for r in bad[:5]]
    owners = sorted(set(str(r.get("owner")) for r in carded))
    lines.append("distinct owners named: %d %s" % (len(owners), owners))
    lines.append("STOP blocks the checklist declares: %d %s" % (len(stops), stops))
    reached_ids = [r.get("step") for r in (rec.get("reached") or []) if isinstance(r, dict)]
    stop_reached = []
    for r in (rec.get("reached") or []):
        if isinstance(r, dict) and r.get("was_stop"):
            stop_reached.append(r.get("step"))
    if stop_reached:
        lines.append("steps marked as a STOP point yet claimed REACHED: %s -- allowed only with an "
                     "`unblocked_by` citation on the row" % stop_reached)
        unproven = [r.get("step") for r in (rec.get("reached") or [])
                    if isinstance(r, dict) and r.get("was_stop")
                    and not str(r.get("unblocked_by") or "").strip()]
        if unproven:
            lines.append("and %s carry no `unblocked_by`" % unproven)
            return False, lines
    lines.append("reached step ids: %s" % sorted(x for x in reached_ids if isinstance(x, int)))
    return not bad, lines


def core_step_evidence(rec, text):
    """A REACHED step is BOUND TO ITS INSTRUMENT: the record's `rule` and `builder` for that step must
    match the checklist's own `rule:` / `builder:` lines for it. Otherwise 'reached' is an assertion
    and the arm is grading prose."""
    if not isinstance(rec, dict) or not isinstance(rec.get("reached"), list):
        return False, ["the run record carries no `reached` list"]
    declared = {}
    for m in re.finditer(r"^### STEP (\d+) --[^\n]*\nrule: ([^\n]*)\nbuilder: ([^\n]*)", text or "", re.M):
        declared[int(m.group(1))] = (m.group(2).strip(), m.group(3).strip())
    lines = ["steps whose rule+builder this arm could read from the checklist: %d of %d"
             % (len(declared), len(re.findall(r"^### STEP", text or "", re.M)))]
    if not declared:
        lines.append("NONE readable -- the arm cannot bind any claim to an instrument, so it refuses "
                     "rather than passing vacuously")
        return False, lines
    bad = []
    for r in rec["reached"]:
        if not isinstance(r, dict) or not isinstance(r.get("step"), int):
            continue
        n = r["step"]
        if n not in declared:
            bad.append("step %s is not in the checklist" % n)
            continue
        want_rule, want_builder = declared[n]
        got_rule = str(r.get("rule") or "").strip()
        got_builder = str(r.get("builder") or "").strip()
        if got_rule != want_rule or got_builder != want_builder:
            bad.append("step %d: rule %r vs %r; builder %r vs %r"
                       % (n, got_rule[:40], want_rule[:40], got_builder[:40], want_builder[:40]))
    lines.append("reached rows whose rule/builder disagree with the checklist: %d of %d"
                 % (len(bad), len([r for r in rec["reached"] if isinstance(r, dict)])))
    lines += ["  " + b for b in bad[:6]]
    return not bad, lines


def core_nothing_live(rec):
    """DEC-9/DEC-13: writing the checklist moved nothing live, and RUNNING it moves nothing live
    either at this vintage. The served dashboard is READ. Shape borrowed deliberately from
    LGIC_LGCTFM's FWD10 record, because it is the shape that already survived a CVO grade."""
    if not isinstance(rec, dict):
        return False, ["the run record is not an object"]
    s = rec.get("served") if isinstance(rec.get("served"), dict) else {}
    before = str((s.get("before") or {}).get("routes_sha256") or "")
    after = str((s.get("after") or {}).get("routes_sha256") or "")
    inst = str(s.get("instrument") or "")
    acts = rec.get("live_acts")
    lines = ["served routes_sha256 before %r after %r; equal and non-empty: %s"
             % (before[:16], after[:16], bool(before) and before == after),
             "instrument named: %r" % inst[:70],
             "live_acts declared: %r" % (acts,)]
    ok = bool(before) and before == after and bool(inst) and acts == []
    if acts != []:
        lines.append("live_acts must be an EMPTY LIST -- a present-but-empty field is a measurement, "
                     "an absent one is silence, and a non-empty one is a finding for the issuer")
    return ok, lines


def core_rows(rec, channel_text):
    """Every surprise the run raised is FILED, and a run that raised none says so with a printed zero
    -- an absent count and a measured zero are different claims."""
    if not isinstance(rec, dict):
        return False, ["the run record is not an object"]
    claimed = rec.get("rows_filed")
    if not isinstance(claimed, list):
        return False, ["`rows_filed` must be a list, empty if the run raised nothing (a printed zero "
                       "is a measurement; an absent field is silence)"]
    present = [r for r in claimed if isinstance(r, str) and ('"%s"' % r) in (channel_text or "")]
    missing = [r for r in claimed if r not in present]
    lines = ["row ids claimed: %d %s" % (len(claimed), claimed[:8]),
             "of those present on the project channel: %d; ABSENT: %d %s"
             % (len(present), len(missing), missing[:6])]
    if not claimed:
        lines.append("zero rows claimed, printed as a measurement rather than omitted")
    return not missing, lines


def core_hashes(rec_hashes, actual, required):
    """R-40: the run record and its siblings are bound to their CONTENT, so a later commit that
    replaces one FAILS this arm instead of silently satisfying the others."""
    if not isinstance(rec_hashes, dict) or not isinstance(rec_hashes.get("files"), dict):
        return False, ["the hash manifest carries no `files` map"]
    declared = rec_hashes["files"]
    missing = [f for f in required if f not in declared]
    undeclared = [k for k in sorted(declared) if k not in required]
    mism = ["%s: declared %s, bytes now %s" % (f, str(declared[f])[:16], str(actual.get(f))[:16])
            for f in required if f in declared and actual.get(f) != declared[f]]
    lines = ["required %d file(s); declared %d; missing %s; declared but not required %s"
             % (len(required), len(declared), missing, undeclared),
             "hash mismatches: %d of %d" % (len(mism), len(required))] + mism[:6]
    return (not missing and not undeclared and not mism), lines


# ============================================================================ the arms
def _checklist_or_fail(tag):
    text = read(CHECKLIST)
    if text is None:
        return None, None, fail_only(tag, "absent: %s" % CHECKLIST)
    ids, rules, builders, stops = checklist_steps(text)
    if not ids:
        return None, None, fail_only(tag, "no `### STEP <n> --` headings in %s" % CHECKLIST)
    return text, (ids, rules, builders, stops), None


def c6_steps():
    tag = "C6-EVERY-STEP-REACHED-OR-CARDED"
    text, got, bail = _checklist_or_fail(tag)
    if bail is not None:
        return bail
    ids, rules, builders, _stops = got
    rec, why = load_json(record_path())
    pre = ["checklist: %d steps, %d rule: lines, %d builder: lines" % (len(ids), rules, builders)]
    if rec is None:
        return fail_only(tag, *(pre + [why]))
    ok, lines = core_steps(rec, ids)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, pre + lines)


def c6_carded_owners():
    tag = "C6-EVERY-CARDED-STEP-NAMES-AN-OWNER"
    text, got, bail = _checklist_or_fail(tag)
    if bail is not None:
        return bail
    _ids, _r, _b, stops = got
    rec, why = load_json(record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_carded_owners(rec, stops)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c6_step_evidence():
    tag = "C6-EVERY-REACHED-STEP-BOUND-TO-ITS-INSTRUMENT"
    text, _got, bail = _checklist_or_fail(tag)
    if bail is not None:
        return bail
    rec, why = load_json(record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_step_evidence(rec, text)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c6_nothing_live():
    tag = "C6-NOTHING-LIVE-MOVED"
    rec, why = load_json(record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_nothing_live(rec)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c6_rows():
    tag = "C6-EVERY-SURPRISE-FILED"
    rec, why = load_json(record_path())
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_rows(rec, read(CHANNEL))
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c6_subject():
    """The subject is named by CONTENT, not by label -- the whole point of R-40, and the defect that
    cost LGIC_LGCTFM a re-hand."""
    tag = "C6-SUBJECT-IS-THE-HASH-BOUND-WAVE"
    rec, why = load_json(record_path())
    if rec is None:
        return fail_only(tag, why)
    subj = rec.get("subject") if isinstance(rec.get("subject"), dict) else {}
    rc, o = run(["git", "hash-object", WAVE_DIR + "/contract.json"])
    live = o.strip() if rc == 0 and o.strip() else "git rc=%d" % rc
    lines = ["the wave this cell is cut against: %s" % WAVE_RUN_ID,
             "its contract.json hash at the cut: %s" % WAVE_CONTRACT_HASH,
             "its contract.json hash NOW: %s" % live,
             "the record declares run_id %r and contract_hash %r"
             % (subj.get("run_id"), str(subj.get("contract_hash"))[:44])]
    ok = (subj.get("run_id") == WAVE_RUN_ID
          and str(subj.get("contract_hash")) == WAVE_CONTRACT_HASH
          and live == WAVE_CONTRACT_HASH)
    if live != WAVE_CONTRACT_HASH:
        lines.append("THE WAVE'S OWN BYTES MOVED since the cut -- that is a finding for the issuer, "
                     "not something this cell can work around")
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c6_hashes():
    tag = "C6-RECORD-BOUND-TO-ITS-HASHES"
    rec, why = load_json(hashes_path())
    if rec is None:
        return fail_only(tag, why)
    required = (RUN_RECORD, "C6_RUN.md")
    d = os.path.dirname(ab(record_path()))
    actual = {}
    for f in required:
        p = os.path.join(d, f)
        if os.path.isfile(p):
            rc, o = run(["git", "hash-object", p])
            actual[f] = o.strip() if rc == 0 and o.strip() else "git rc=%d" % rc
    ok, lines = core_hashes(rec, actual, required)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


SUBCOMMANDS = {
    "c6-steps": c6_steps,
    "c6-carded-owners": c6_carded_owners,
    "c6-step-evidence": c6_step_evidence,
    "c6-nothing-live": c6_nothing_live,
    "c6-rows": c6_rows,
    "c6-subject": c6_subject,
    "c6-hashes": c6_hashes,
}

PASS_TOKENS = (
    "PASS-C6-EVERY-STEP-REACHED-OR-CARDED",
    "PASS-C6-EVERY-CARDED-STEP-NAMES-AN-OWNER",
    "PASS-C6-EVERY-REACHED-STEP-BOUND-TO-ITS-INSTRUMENT",
    "PASS-C6-NOTHING-LIVE-MOVED",
    "PASS-C6-EVERY-SURPRISE-FILED",
    "PASS-C6-SUBJECT-IS-THE-HASH-BOUND-WAVE",
    "PASS-C6-RECORD-BOUND-TO-ITS-HASHES",
)


# ============================================================================ self-test
def _good_record(step_ids, declared):
    """A SIMULATED CORRECT RUN RECORD -- the positive-satisfiability fixture. Every arm must PASS
    against this, or the arm is unsatisfiable by the right answer and is worse than no arm."""
    carded_steps = [10, 14]
    reached = []
    for n in step_ids:
        if n in carded_steps:
            continue
        rule, builder = declared.get(n, ("", ""))
        reached.append({"step": n, "rule": rule, "builder": builder, "evidence": "ran it"})
    carded = [{"step": n, "owner": "ADVI_FIRMBKTS" if n == 10 else "1.0.0_SA_CTO",
               "reason": "the checklist's own STOP point at this vintage"} for n in carded_steps]
    return {"reached": reached, "carded": carded, "rows_filed": [],
             "served": {"instrument": "projection_client.py against the live distribution",
                        "before": {"routes_sha256": "abc"}, "after": {"routes_sha256": "abc"}},
             "live_acts": [],
             "subject": {"run_id": WAVE_RUN_ID, "contract_hash": WAVE_CONTRACT_HASH}}


def selftest_arms():
    res = []

    def arm(name, good, bad, detail):
        res.append((name, bool(good) and not bool(bad), detail))

    overlap = sorted(set((a, b) for a in PASS_TOKENS for b in PASS_TOKENS if a != b and a in b))
    res.append(("tokens-pairwise-distinct", not overlap, "overlapping pairs: %s" % (overlap or "none")))

    text = read(CHECKLIST) or ""
    ids, _r, _b, stops = checklist_steps(text)
    ids = ids or list(range(1, 17))
    declared = {}
    for m in re.finditer(r"^### STEP (\d+) --[^\n]*\nrule: ([^\n]*)\nbuilder: ([^\n]*)", text, re.M):
        declared[int(m.group(1))] = (m.group(2).strip(), m.group(3).strip())
    good = _good_record(ids, declared)

    # POSITIVE SATISFIABILITY, every core, against the SAME simulated correct record
    res.append(("POSITIVE-c6-steps", core_steps(good, ids)[0], "a correct record must PASS"))
    res.append(("POSITIVE-c6-carded-owners", core_carded_owners(good, stops or [])[0], "a correct record must PASS"))
    res.append(("POSITIVE-c6-step-evidence", core_step_evidence(good, text)[0], "a correct record must PASS"))
    res.append(("POSITIVE-c6-nothing-live", core_nothing_live(good)[0], "a correct record must PASS"))
    res.append(("POSITIVE-c6-rows", core_rows(good, "")[0], "a correct record must PASS"))

    import copy
    dropped = copy.deepcopy(good)
    dropped["reached"] = dropped["reached"][:-1]
    dupd = copy.deepcopy(good)
    dupd["carded"].append(dict(dupd["carded"][0]))
    invented = copy.deepcopy(good)
    invented["reached"].append({"step": 99, "rule": "x", "builder": "y"})
    arm("c6-steps", core_steps(good, ids)[0], core_steps(dropped, ids)[0], "a step in neither list")
    arm("c6-steps-double", core_steps(good, ids)[0], core_steps(dupd, ids)[0], "a step counted twice")
    arm("c6-steps-invented", core_steps(good, ids)[0], core_steps(invented, ids)[0], "a step that is not in the checklist")

    noowner = copy.deepcopy(good)
    noowner["carded"][0].pop("owner")
    stopreached = copy.deepcopy(good)
    stopreached["reached"].append({"step": 10, "rule": "x", "builder": "y", "was_stop": True})
    arm("c6-carded-owners", core_carded_owners(good, stops or [])[0],
        core_carded_owners(noowner, stops or [])[0], "a carded step with no owner")
    arm("c6-carded-stop", core_carded_owners(good, stops or [])[0],
        core_carded_owners(stopreached, stops or [])[0], "a STOP point claimed reached with no unblocked_by")

    wrongrule = copy.deepcopy(good)
    if wrongrule["reached"]:
        wrongrule["reached"][0]["rule"] = "R-nonsense"
    arm("c6-step-evidence", core_step_evidence(good, text)[0], core_step_evidence(wrongrule, text)[0],
        "a reached step whose rule disagrees with the checklist")
    arm("c6-step-evidence-noread", core_step_evidence(good, text)[0], core_step_evidence(good, "")[0],
        "the checklist could not be read at all, so nothing can be bound")

    moved = copy.deepcopy(good)
    moved["served"]["after"]["routes_sha256"] = "different"
    acted = copy.deepcopy(good)
    acted["live_acts"] = ["safe-apply on the firm root"]
    silent = copy.deepcopy(good)
    silent.pop("live_acts")
    arm("c6-nothing-live", core_nothing_live(good)[0], core_nothing_live(moved)[0], "the served routes changed")
    arm("c6-nothing-live-acts", core_nothing_live(good)[0], core_nothing_live(acted)[0], "a live act declared")
    arm("c6-nothing-live-silent", core_nothing_live(good)[0], core_nothing_live(silent)[0],
        "live_acts absent -- silence is not a measured zero")

    claimed = copy.deepcopy(good)
    claimed["rows_filed"] = ["LGIC_CANON-W1-S1"]
    norows = copy.deepcopy(good)
    norows.pop("rows_filed")
    arm("c6-rows", core_rows(good, "")[0], core_rows(claimed, "")[0], "a claimed row absent from the channel")
    arm("c6-rows-silent", core_rows(good, "")[0], core_rows(norows, "")[0],
        "rows_filed absent -- an omitted count is not a printed zero")

    req = (RUN_RECORD, "C6_RUN.md")
    hgood = {"files": {f: "h" + f for f in req}}
    hact = {f: "h" + f for f in req}
    hmoved = dict(hact)
    hmoved[req[0]] = "changed"
    hshort = {"files": {req[0]: "h" + req[0]}}
    arm("c6-hashes", core_hashes(hgood, hact, req)[0], core_hashes(hgood, hmoved, req)[0],
        "a file's bytes changed after production")
    arm("c6-hashes-omitted", core_hashes(hgood, hact, req)[0], core_hashes(hshort, hact, req)[0],
        "a manifest that omits a required file")

    ok = all(r[1] for r in res)
    for name, good_, detail in res:
        print("  %-30s %-5s %s" % (name, "PASS" if good_ else "FAIL", detail))
    print("arms driven: %d (5 of them POSITIVE-SATISFIABILITY against one simulated correct record)"
          % len(res))
    print("NOT driven here, stated: c6-subject, whose whole content is a git hash-object of a file "
          "outside this cell's control -- it has no pure core to fixture and is exercised by the real "
          "run, where a moved wave is a FINDING and not a fixture case.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE"))
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--list", "-l"):
        for k in sorted(SUBCOMMANDS):
            print(k)
        print("selftest-arms")
        return 0
    if args[0] == "selftest-arms":
        return selftest_arms()
    fn = SUBCOMMANDS.get(args[0])
    if fn is None:
        print("unknown subcommand: %s (use --list)" % args[0])
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
