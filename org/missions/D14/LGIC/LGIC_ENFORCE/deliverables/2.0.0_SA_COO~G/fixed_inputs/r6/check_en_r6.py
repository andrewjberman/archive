#!/usr/bin/env python3
"""check_en_r6 -- LGIC_ENFORCE round 6's checker. The ISSUER's fixed input; workers never edit it.

Round 6 is TWO cells: the DISARM SWEEP over the armed population (R-46 as corrected, N = 43) and the
CAMPAIGN CONTINUATION over the 1370 rows EN-c-28's timebox handed forward. Each subcommand prints its
evidence, a DENOMINATOR, and exactly one final `VERDICT: PASS-<X>` / `FAIL-<X>`. A missing input is a
FAIL verdict, never a traceback.

NO PASS TOKEN IS A SUBSTRING OF ANOTHER; `selftest-arms` prints that pairwise check as its own arm.

=============================================================================================
THE SWEEP'S PREDICATE IS IMPLEMENTED HERE AND THE CELL MUST PRINT THE SAME ONE
=============================================================================================
`1.0.0_SA_CTO`'s round-5 analysis adopted the sweep with three conditions, and condition 1 is that the
ARMED predicate and the owner-attribution rule are PRINTED BEFORE THE COUNT. That condition exists
because two seats counted the same channel on the same night and got 57 and 54, and a sweep graded on
a number nobody shares certifies nothing.

So `s32-predicate` does something unusual and deliberate: it requires the cell to DECLARE its predicate
in its own record, and it refuses a declaration that does not MATCH the one this file implements. A cell
that prints one rule and counts by another would otherwise pass.

R-46 AS CORRECTED, which is what this file implements:
  * a row id is ARMED if ANY of its occurrences carries hazard_standing == 'ARMED'
  * DISTINCT IDS, never occurrences -- the same channel gives 92 at the occurrence level and 57 at the
    distinct-id level, so the choice is part of the measurement
  * an ARMED id is CLOSED only where a REMEDIATION document carries a REAL DISPOSITION:
    remediation.state == 'REMEDIATED', or a disarm block with state == 'DISARMED' AND an `at`.
    INERT is a LABEL; only a CLOCK closes. An adjudication clock does NOT close an investigation row.
  * owner resolution order: disarm_owner -> disarm.owner -> owner (top level, per R-42)
MEASURED AT THE CUT with exactly this predicate: 275 occurrences, 183 distinct ids, 57 armed, 14 closed
by a clock (10 in REMEDIATION_v1, 4 in v2, 0 borrowed from an adjudication), 43 STILL ARMED, owners
35 / 7 / 1. Both seats derived 43 independently from the rule rather than from each other's answer.

=============================================================================================
THE SWEEP'S SCOPE IS 35, NOT 43, AND THE PARTITION IS PRINTED
=============================================================================================
Of the 43, only 35 name `2.0.0_SA_COO~G`. `1.0.0_SA_CTO` holds 7 and `3.0.0_SA_CVO` holds 1, and a
worker of this lane CANNOT disarm another seat's row. So the cell's population is 35 and it must print
43 == 35 IN SCOPE + 8 OWNED ELSEWHERE with the other owners named. A sweep that silently graded itself
on 35 while the round called it 43 would be this evening's own subset-not-population defect, one more
time.

THE POSITIVE-SATISFIABILITY CONTROL IS IN THE SELF-TEST, as it now is by default on this lane: every
core is driven against a SIMULATED CORRECT RECORD and must PASS, as well as against a doctored one and
must FAIL. Four of this seat's arms in one night were unsatisfiable by a correct fix, each having
passed its own mutant test.

Standard library only. ASCII only. LF endings.
"""
import glob
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
CHANNEL_GLOB = ROOT + "/surprise-channel/**/*.md"
R5_CAMPAIGN = ROOT + "/deliverables/0.9.0_WK_LGIC_ENFORCE~1/PLACEHOLDER_CAMPAIGN_R5.json"
EXEMPTIONS = "infra/logic/registry/exemptions.json"
BASEFILE = os.path.join(HERE, "R6_BASE.json")

SWEEP_RECORD = "DISARM_SWEEP_R6.json"
CAMPAIGN_RECORD = "PLACEHOLDER_CAMPAIGN_R6.json"

LANE = "2.0.0_SA_COO~G"
TIMEBOX_OVERAGE = 25

# The predicate the cell must DECLARE, matched on these three keys. The values are compared after
# whitespace collapse so formatting is not the test; the RULE is.
REQUIRED_PREDICATE = {
    "armed_predicate": "a row id is ARMED if ANY of its occurrences carries hazard_standing == ARMED",
    "occurrence_or_distinct": "DISTINCT IDS, never occurrences",
    "owner_resolution_order": "disarm_owner -> disarm.owner -> owner",
}


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


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip().lower()


def record_path(name):
    for n in ("1", "2", "3", "4"):
        p = "%s/deliverables/0.9.0_WK_LGIC_ENFORCE~%s/%s" % (ROOT, n, name)
        if os.path.isfile(ab(p)):
            return p
    return "%s/deliverables/0.9.0_WK_LGIC_ENFORCE~1/%s" % (ROOT, name)


# ==================================================================== the predicate, implemented once
def channel_rows():
    """[(document, row)] -- EVERY occurrence, never deduped. The dedup choice is the measurement."""
    pairs = []
    for p in sorted(glob.glob(os.path.join(ab(ROOT), "surprise-channel", "**", "*.md"), recursive=True)):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"```json(.*?)```", t, re.S):
            try:
                d = json.loads(m.group(1))
            except ValueError:
                continue
            for r in (d if isinstance(d, list) else [d]):
                if isinstance(r, dict) and r.get("id"):
                    pairs.append((os.path.basename(p), r))
    return pairs


def owner_of(r):
    for v in (r.get("disarm_owner"),
              (r.get("disarm") or {}).get("owner") if isinstance(r.get("disarm"), dict) else None,
              r.get("owner")):
        if str(v or "").strip():
            return str(v).strip()
    return "<NO OWNER FIELD>"


def closing_clock(doc, r):
    """R-46's operative half. Only a REMEDIATION document's clock closes."""
    if "REMEDIATION" not in doc.upper():
        return None
    rem = r.get("remediation")
    if isinstance(rem, dict) and str(rem.get("state") or "").upper() == "REMEDIATED":
        return "remediation.state=REMEDIATED"
    dz = r.get("disarm")
    if isinstance(dz, dict) and str(dz.get("state") or "").upper() == "DISARMED" and str(dz.get("at") or "").strip():
        return "disarm DISARMED at %s" % dz.get("at")
    return None


def armed_population():
    """(still_armed {id: owner}, closed {id: why}, note) -- the whole predicate in one place."""
    pairs = channel_rows()
    byid = defaultdict(list)
    for doc, r in pairs:
        byid[r["id"]].append((doc, r))
    still, closed = {}, {}
    for rid, rows in byid.items():
        if not any(str(r.get("hazard_standing")) == "ARMED" for _d, r in rows):
            continue
        why = None
        for doc, r in rows:
            why = closing_clock(doc, r)
            if why:
                break
        if why:
            closed[rid] = why
        else:
            first = next(r for _d, r in rows if str(r.get("hazard_standing")) == "ARMED")
            still[rid] = owner_of(first)
    note = ("occurrences %d; distinct ids %d; armed ids %d; closed by a clock %d; STILL ARMED %d"
            % (len(pairs), len(byid), len(still) + len(closed), len(closed), len(still)))
    return still, closed, note


# ==================================================================== EN-s-32: the disarm sweep
def core_predicate(rec):
    """Condition 1: the cell DECLARES its predicate, and the declaration MATCHES the one this file
    implements. A cell that prints one rule and counts by another would otherwise pass."""
    if not isinstance(rec, dict):
        return False, ["the sweep record is not an object"]
    dec = rec.get("predicate")
    if not isinstance(dec, dict):
        return False, ["no `predicate` object -- condition 1 is that the rule is PRINTED BEFORE the count"]
    lines, bad = [], []
    for k, want in sorted(REQUIRED_PREDICATE.items()):
        got = dec.get(k)
        hit = norm(want) in norm(got)
        lines.append("  %-24s declared=%r matches=%s" % (k, str(got)[:70], hit))
        if not hit:
            bad.append(k)
    lines.insert(0, "predicate keys required %d; declared %d; mismatched %s"
                % (len(REQUIRED_PREDICATE), len(dec), bad))
    ordering = rec.get("printed_before_count")
    lines.append("the record asserts the predicate precedes its counts: %r" % (ordering,))
    if ordering is not True:
        bad.append("printed_before_count")
        lines.append("`printed_before_count` must be literally true -- the ORDER is the condition, not "
                     "merely the presence of the fields")
    return not bad, lines


def core_denominator(rec, measured_n):
    """Condition 2: re-measured at the cell's OWN write time, start and close both printed, and neither
    carried in from the analysis. The arm re-derives the population itself and compares."""
    if not isinstance(rec, dict):
        return False, ["the sweep record is not an object"]
    d = rec.get("denominators")
    if not isinstance(d, dict):
        return False, ["no `denominators` object"]
    a, b = d.get("armed_at_start"), d.get("armed_at_close")
    inst = str(d.get("instrument") or "").strip()
    lines = ["armed_at_start %r; armed_at_close %r; instrument %r" % (a, b, inst[:70]),
             "this arm's OWN re-derivation of the armed population right now: %d" % measured_n]
    ok = isinstance(a, int) and isinstance(b, int) and bool(inst)
    if not ok:
        lines.append("both populations must be ints and the instrument must be named")
        return False, lines
    if a != measured_n and b != measured_n:
        lines.append("NEITHER declared population matches this arm's own re-derivation -- a denominator "
                     "that agrees with no independent read is carried in, not measured")
        return False, lines
    if a != b and not str(rec.get("denominator_delta_note") or "").strip():
        lines.append("start and close DIFFER with no `denominator_delta_note` -- a moved denominator is "
                     "a finding, not a rounding")
        return False, lines
    return True, lines


def core_partition(rec, owners):
    """43 == 35 IN SCOPE + 8 OWNED ELSEWHERE, with the other owners NAMED. A sweep that silently graded
    itself on its own subset while the round called it 43 is this evening's subset-not-population
    defect one more time."""
    if not isinstance(rec, dict):
        return False, ["the sweep record is not an object"]
    ins = rec.get("in_scope")
    out_ = rec.get("owned_elsewhere")
    if not isinstance(ins, list) or not isinstance(out_, list):
        return False, ["`in_scope` and `owned_elsewhere` must both be lists -- the partition is the claim"]
    total = len(ins) + len(out_)
    measured_total = len(owners)
    mine_measured = sum(1 for o in owners.values() if o == LANE)
    others = Counter(o for o in owners.values() if o != LANE)
    lines = ["in_scope %d + owned_elsewhere %d = %d; this arm measures the armed population at %d"
             % (len(ins), len(out_), total, measured_total),
             "measured owners: %s in scope, others %s" % (mine_measured, dict(others)),
             "every owned_elsewhere entry names an owner: %s"
             % all(isinstance(x, dict) and str(x.get("owner") or "").strip() for x in out_)]
    if total != measured_total:
        lines.append("PARTITION DOES NOT COVER THE POPULATION -- %d declared against %d measured"
                     % (total, measured_total))
        return False, lines
    if len(ins) != mine_measured:
        lines.append("in_scope %d disagrees with the %d rows measured to name %s"
                     % (len(ins), mine_measured, LANE))
        return False, lines
    if not all(isinstance(x, dict) and str(x.get("owner") or "").strip() for x in out_):
        lines.append("an owned_elsewhere entry with no owner is exactly the row that goes unworked")
        return False, lines
    return True, lines


def core_graded(rec):
    """disarmed + restated == in_scope, and a RESTATED row must carry a reason that DIFFERS from the one
    it had. Otherwise 'restated' is a no-op that reads as work."""
    if not isinstance(rec, dict):
        return False, ["the sweep record is not an object"]
    ins = rec.get("in_scope")
    if not isinstance(ins, list):
        return False, ["no `in_scope` list"]
    dis = [x for x in ins if isinstance(x, dict) and str(x.get("outcome") or "").upper() == "DISARMED"]
    res = [x for x in ins if isinstance(x, dict) and str(x.get("outcome") or "").upper() == "RESTATED"]
    neither = [x for x in ins if isinstance(x, dict)
               and str(x.get("outcome") or "").upper() not in ("DISARMED", "RESTATED")]
    lines = ["in_scope %d = disarmed %d + restated %d; neither %d"
             % (len(ins), len(dis), len(res), len(neither))]
    if neither:
        lines.append("rows with no DISARMED/RESTATED outcome: %s"
                     % [x.get("id") for x in neither[:6]])
        return False, lines
    noop = [x for x in res if norm(x.get("reason_before")) == norm(x.get("reason_after"))
            or not str(x.get("reason_after") or "").strip()]
    lines.append("restated rows whose reason did NOT change: %d %s"
                 % (len(noop), [x.get("id") for x in noop[:6]]))
    if noop:
        lines.append("a restatement that repeats the old reason is a no-op wearing the outcome's name")
        return False, lines
    nodis = [x for x in dis if not str(x.get("evidence") or "").strip()]
    lines.append("disarmed rows with no evidence string: %d" % len(nodis))
    return not nodis, lines


def _sweep():
    return load_json(record_path(SWEEP_RECORD))


def s32_predicate():
    tag = "S32-PREDICATE-PRINTED-AND-MATCHING"
    rec, why = _sweep()
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_predicate(rec)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def s32_denominator():
    tag = "S32-ARMED-DENOMINATOR-RE-MEASURED"
    rec, why = _sweep()
    if rec is None:
        return fail_only(tag, why)
    still, closed, note = armed_population()
    ok, lines = core_denominator(rec, len(still))
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, [note] + lines)


def s32_partition():
    tag = "S32-PARTITION-COVERS-THE-POPULATION"
    rec, why = _sweep()
    if rec is None:
        return fail_only(tag, why)
    still, closed, note = armed_population()
    ok, lines = core_partition(rec, still)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, [note] + lines)


def s32_graded():
    tag = "S32-EVERY-IN-SCOPE-ROW-DISARMED-OR-RESTATED"
    rec, why = _sweep()
    if rec is None:
        return fail_only(tag, why)
    ok, lines = core_graded(rec)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


# ==================================================================== EN-c-33: the campaign continued
def core_c33_population(rec, measured_start):
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    d = rec.get("denominators") if isinstance(rec.get("denominators"), dict) else {}
    dec = d.get("population_at_start")
    lines = ["round 5's delta_riding_next_round count, read fresh from its own record: %d" % measured_start,
             "this round declares population_at_start=%r" % (dec,)]
    if dec != measured_start:
        lines.append("MISMATCH -- a start that disagrees with a fresh read of the handing record is "
                     "inherited, not measured")
        return False, lines
    return True, lines


def core_c33_covered(rec, start):
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    buckets = {k: rec.get(k) for k in ("resolved", "carded", "deferred")}
    for k, v in buckets.items():
        if not isinstance(v, list):
            return False, ["`%s` is %s, not a list" % (k, type(v).__name__)]
    n = sum(len(v) for v in buckets.values())
    lines = ["resolved %d + carded %d + deferred %d = %d; START %d"
             % (len(buckets["resolved"]), len(buckets["carded"]), len(buckets["deferred"]), n, start)]
    if n != start:
        lines.append("UNACCOUNTED: %d row(s) in none of the three lists" % (start - n))
        return False, lines
    bad = [r for r in (buckets["carded"] + buckets["deferred"])
           if not (isinstance(r, dict) and str(r.get("owner") or "").strip()
                   and str(r.get("reason") or "").strip())]
    lines.append("carded or deferred rows missing an owner or a reason: %d" % len(bad))
    return not bad, lines


def core_c33_classes(rec, r5_classes):
    """Round 5's three carded classes are carried FORWARD BY NAME with their counts, and the
    NON_SYSTEM class is dispositioned distinctly rather than folded into the timebox -- they are
    different questions and one remedy does not move both (Rule 24(iv))."""
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    dec = rec.get("inherited_classes")
    if not isinstance(dec, dict):
        return False, ["no `inherited_classes` map -- round 5's split must be carried by name, not "
                       "collapsed into a single total"]
    lines = ["round 5's classes, read fresh from its record: %s" % json.dumps(r5_classes),
             "this round declares: %s" % json.dumps(dec)]
    missing = [k for k in r5_classes if k not in dec]
    wrong = [k for k in r5_classes if k in dec and dec[k] != r5_classes[k]]
    lines.append("classes missing %s; counts disagreeing %s" % (missing, wrong))
    if missing or wrong:
        return False, lines
    nsd = rec.get("non_system_disposition")
    okd = isinstance(nsd, dict) and str(nsd.get("rule") or "").strip() and isinstance(nsd.get("count"), int)
    lines.append("NON_SYSTEM_PLACEHOLDER_TOKEN carries its own disposition rule and count: %s (%s)"
                 % (okd, json.dumps(nsd)[:140]))
    return okd, lines


def core_c33_fence(now_text, base_text):
    if base_text is None:
        return False, ["the pinned base copy of the fence file could not be read"]
    if now_text is None:
        return False, ["the fence file is absent at HEAD"]
    same = now_text == base_text
    return same, ["fence bytes at HEAD %d; at the pinned base %d; identical %s"
                  % (len(now_text), len(base_text), same)]


def core_c33_timebox(rec, start, overage):
    if not isinstance(rec, dict):
        return False, ["the campaign record is not an object"]
    res = rec.get("resolved")
    if not isinstance(res, list):
        return False, ["`resolved` is not a list"]
    bar = start + overage
    stopped = bool(rec.get("stopped_on_timebox"))
    delta = rec.get("delta_riding_next_round")
    lines = ["resolved %d; R-33 bar is start %d + %d = %d; stopped_on_timebox %s"
             % (len(res), start, overage, bar, stopped)]
    if len(res) > bar:
        lines.append("OVER THE BAR without stopping")
        return False, lines
    if stopped:
        okd = isinstance(delta, dict) and isinstance(delta.get("count"), int) and str(delta.get("owner") or "").strip()
        lines.append("stopped, so a delta record is required: %s (%s)" % (okd, json.dumps(delta)[:120]))
        return okd, lines
    return True, lines


def _r5():
    d, why = load_json(R5_CAMPAIGN)
    if d is None:
        return None, None, why
    start = (d.get("delta_riding_next_round") or {}).get("count")
    classes = dict(Counter(str(r.get("reason")) for r in (d.get("carded") or []) if isinstance(r, dict)))
    return start, classes, ""


def _camp():
    return load_json(record_path(CAMPAIGN_RECORD))


def c33_population():
    tag = "C33-START-IS-ROUND-5S-MEASURED-DELTA"
    start, _c, why = _r5()
    if start is None:
        return fail_only(tag, why or "round 5's delta count is unreadable")
    rec, why2 = _camp()
    if rec is None:
        return fail_only(tag, why2)
    ok, lines = core_c33_population(rec, start)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c33_covered():
    tag = "C33-EVERY-CARRIED-ROW-ACCOUNTED"
    start, _c, why = _r5()
    rec, why2 = _camp()
    if start is None or rec is None:
        return fail_only(tag, why or why2)
    ok, lines = core_c33_covered(rec, start)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c33_classes():
    tag = "C33-INHERITED-CLASSES-CARRIED-BY-NAME"
    _s, classes, why = _r5()
    rec, why2 = _camp()
    if classes is None or rec is None:
        return fail_only(tag, why or why2)
    ok, lines = core_c33_classes(rec, classes)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c33_fence():
    tag = "C33-APPLIED-FENCE-UNCHANGED"
    d, why = load_json(BASEFILE)
    base = (d or {}).get("base_commit")
    if not base:
        return fail_only(tag, why or "R6_BASE.json carries no base_commit")
    import subprocess
    r = subprocess.run(["git", "show", "%s:%s" % (base, EXEMPTIONS)],
                       capture_output=True, text=True, cwd=REPO)
    ok, lines = core_c33_fence(read(EXEMPTIONS), r.stdout if r.returncode == 0 else None)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


def c33_timebox():
    tag = "C33-R33-TIMEBOX-RESPECTED"
    start, _c, why = _r5()
    rec, why2 = _camp()
    if start is None or rec is None:
        return fail_only(tag, why or why2)
    ok, lines = core_c33_timebox(rec, start, TIMEBOX_OVERAGE)
    return verdict(ok, "PASS-" + tag, "FAIL-" + tag, lines)


SUBCOMMANDS = {
    "s32-predicate": s32_predicate,
    "s32-denominator": s32_denominator,
    "s32-partition": s32_partition,
    "s32-graded": s32_graded,
    "c33-population": c33_population,
    "c33-covered": c33_covered,
    "c33-classes": c33_classes,
    "c33-fence": c33_fence,
    "c33-timebox": c33_timebox,
}

PASS_TOKENS = (
    "PASS-S32-PREDICATE-PRINTED-AND-MATCHING",
    "PASS-S32-ARMED-DENOMINATOR-RE-MEASURED",
    "PASS-S32-PARTITION-COVERS-THE-POPULATION",
    "PASS-S32-EVERY-IN-SCOPE-ROW-DISARMED-OR-RESTATED",
    "PASS-C33-START-IS-ROUND-5S-MEASURED-DELTA",
    "PASS-C33-EVERY-CARRIED-ROW-ACCOUNTED",
    "PASS-C33-INHERITED-CLASSES-CARRIED-BY-NAME",
    "PASS-C33-APPLIED-FENCE-UNCHANGED",
    "PASS-C33-R33-TIMEBOX-RESPECTED",
)


# ==================================================================== self-test
def selftest_arms():
    import copy
    res = []

    def arm(name, good, bad, detail):
        res.append((name, bool(good) and not bool(bad), detail))

    overlap = sorted(set((a, b) for a in PASS_TOKENS for b in PASS_TOKENS if a != b and a in b))
    res.append(("tokens-pairwise-distinct", not overlap, "overlapping pairs: %s" % (overlap or "none")))

    owners = dict([("R%d" % i, LANE) for i in range(35)]
                  + [("X%d" % i, "1.0.0_SA_CTO") for i in range(7)] + [("Y", "3.0.0_SA_CVO")])
    sweep = {
        "predicate": dict(REQUIRED_PREDICATE),
        "printed_before_count": True,
        "denominators": {"armed_at_start": 43, "armed_at_close": 43,
                         "instrument": "the printed predicate re-run over the channel"},
        "in_scope": [{"id": "R%d" % i, "outcome": "DISARMED", "evidence": "the act, cited"}
                     for i in range(35)],
        "owned_elsewhere": ([{"id": "X%d" % i, "owner": "1.0.0_SA_CTO"} for i in range(7)]
                            + [{"id": "Y", "owner": "3.0.0_SA_CVO"}]),
    }
    # POSITIVE SATISFIABILITY first, every core, one simulated correct record
    res.append(("POSITIVE-s32-predicate", core_predicate(sweep)[0], "a correct record must PASS"))
    res.append(("POSITIVE-s32-denominator", core_denominator(sweep, 43)[0], "a correct record must PASS"))
    res.append(("POSITIVE-s32-partition", core_partition(sweep, owners)[0], "a correct record must PASS"))
    res.append(("POSITIVE-s32-graded", core_graded(sweep)[0], "a correct record must PASS"))

    noord = copy.deepcopy(sweep)
    noord["printed_before_count"] = False
    wrongp = copy.deepcopy(sweep)
    wrongp["predicate"]["occurrence_or_distinct"] = "occurrences"
    arm("s32-predicate", core_predicate(sweep)[0], core_predicate(wrongp)[0],
        "a declared predicate that does not match the implemented one")
    arm("s32-predicate-order", core_predicate(sweep)[0], core_predicate(noord)[0],
        "the predicate present but not asserted to precede the count")
    arm("s32-denominator", core_denominator(sweep, 43)[0], core_denominator(sweep, 41)[0],
        "a declared population matching no independent re-derivation")
    moved = copy.deepcopy(sweep)
    moved["denominators"]["armed_at_close"] = 40
    arm("s32-denominator-note", core_denominator(sweep, 43)[0], core_denominator(moved, 43)[0],
        "the denominator moved with no note")
    short = copy.deepcopy(sweep)
    short["owned_elsewhere"] = short["owned_elsewhere"][:-1]
    noowner = copy.deepcopy(sweep)
    noowner["owned_elsewhere"][0].pop("owner")
    subset = copy.deepcopy(sweep)
    subset["in_scope"] = subset["in_scope"][:30]
    arm("s32-partition", core_partition(sweep, owners)[0], core_partition(short, owners)[0],
        "the partition leaves a row in neither half")
    arm("s32-partition-owner", core_partition(sweep, owners)[0], core_partition(noowner, owners)[0],
        "an owned_elsewhere row with no owner named")
    arm("s32-partition-subset", core_partition(sweep, owners)[0], core_partition(subset, owners)[0],
        "in_scope smaller than the rows measured to name this lane")
    noop = copy.deepcopy(sweep)
    noop["in_scope"][0] = {"id": "R0", "outcome": "RESTATED",
                           "reason_before": "same words", "reason_after": "same words"}
    nooutcome = copy.deepcopy(sweep)
    nooutcome["in_scope"][0] = {"id": "R0"}
    noev = copy.deepcopy(sweep)
    noev["in_scope"][0] = {"id": "R0", "outcome": "DISARMED"}
    arm("s32-graded", core_graded(sweep)[0], core_graded(nooutcome)[0], "a row with no outcome")
    arm("s32-graded-noop", core_graded(sweep)[0], core_graded(noop)[0],
        "a RESTATED row whose reason did not change")
    arm("s32-graded-evidence", core_graded(sweep)[0], core_graded(noev)[0],
        "a DISARMED row with no evidence")

    r5c = {"TIMEBOXED_R33": 1134, "NON_SYSTEM_PLACEHOLDER_TOKEN": 235, "TYPE_MISMATCH_NEEDS_CONFIRMATION": 1}
    camp = {"denominators": {"population_at_start": 1370, "population_at_close": 1370,
                             "instrument": "a fresh read of round 5's delta record"},
            "resolved": [{"current": "a"}], "carded": [], "deferred": [],
            "inherited_classes": dict(r5c),
            "non_system_disposition": {"rule": "the token is not a system; it is carded under its own reason", "count": 235},
            "stopped_on_timebox": True,
            "delta_riding_next_round": {"count": 1369, "owner": LANE}}
    camp["deferred"] = [{"current": "d%d" % i, "owner": LANE, "reason": "TIMEBOXED_R33"} for i in range(1369)]
    res.append(("POSITIVE-c33-population", core_c33_population(camp, 1370)[0], "a correct record must PASS"))
    res.append(("POSITIVE-c33-covered", core_c33_covered(camp, 1370)[0], "a correct record must PASS"))
    res.append(("POSITIVE-c33-classes", core_c33_classes(camp, r5c)[0], "a correct record must PASS"))
    res.append(("POSITIVE-c33-timebox", core_c33_timebox(camp, 1370, 25)[0], "a correct record must PASS"))
    arm("c33-population", core_c33_population(camp, 1370)[0], core_c33_population(camp, 1411)[0],
        "a start inherited rather than read from the handing record")
    shortc = copy.deepcopy(camp)
    shortc["deferred"] = shortc["deferred"][:-5]
    arm("c33-covered", core_c33_covered(camp, 1370)[0], core_c33_covered(shortc, 1370)[0],
        "rows in none of the three lists")
    noown = copy.deepcopy(camp)
    noown["deferred"][0].pop("owner")
    arm("c33-covered-owner", core_c33_covered(camp, 1370)[0], core_c33_covered(noown, 1370)[0],
        "a deferred row with no owner")
    folded = copy.deepcopy(camp)
    folded.pop("non_system_disposition")
    dropped = copy.deepcopy(camp)
    dropped["inherited_classes"].pop("NON_SYSTEM_PLACEHOLDER_TOKEN")
    arm("c33-classes", core_c33_classes(camp, r5c)[0], core_c33_classes(dropped, r5c)[0],
        "an inherited class dropped from the carry-forward")
    arm("c33-classes-folded", core_c33_classes(camp, r5c)[0], core_c33_classes(folded, r5c)[0],
        "the NON_SYSTEM class folded in with no disposition of its own")
    over = copy.deepcopy(camp)
    over["resolved"] = [{}] * 2000
    over["stopped_on_timebox"] = False
    nodelta = copy.deepcopy(camp)
    nodelta.pop("delta_riding_next_round")
    arm("c33-timebox", core_c33_timebox(camp, 1370, 25)[0], core_c33_timebox(over, 1370, 25)[0],
        "over the bar without stopping")
    arm("c33-timebox-delta", core_c33_timebox(camp, 1370, 25)[0], core_c33_timebox(nodelta, 1370, 25)[0],
        "stopped with no delta record")
    arm("c33-fence", core_c33_fence("abc", "abc")[0], core_c33_fence("abd", "abc")[0], "the fence changed")
    arm("c33-fence-blind", core_c33_fence("abc", "abc")[0], core_c33_fence("abc", None)[0],
        "the baseline could not be read at all")

    ok = all(r[1] for r in res)
    for name, good, detail in res:
        print("  %-30s %-5s %s" % (name, "PASS" if good else "FAIL", detail))
    print("arms driven: %d (8 of them POSITIVE-SATISFIABILITY against two simulated correct records)"
          % len(res))
    print("NOT driven here, stated: armed_population() itself, whose content is a read of the live "
          "channel -- it has no fixture and is exercised by the real run, where the sweep's own "
          "denominator arm compares the cell's declaration against it.")
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
