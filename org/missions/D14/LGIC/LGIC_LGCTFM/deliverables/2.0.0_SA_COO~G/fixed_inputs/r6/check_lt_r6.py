"""LGIC_LGCTFM round 6 -- the arms for LT-e-7: does ONE repair resolve BOTH sites?

1.0.0_SA_CTO's round-5 analysis @cf0cf68868 cut this round to ESTABLISH what round 5 only made
plausible, and named the trap in the same sentence: "the record says 'plausibly', which is a
hypothesis the round EARNED, not a finding; A CELL THAT ASSUMES IT WILL REPORT AGREEMENT RATHER THAN
MEASURE IT."

SO THE ARMS ARE BUILT SO THAT EVERY VERDICT IS REACHABLE. `ONE_REPAIR`, `TWO_REPAIRS` and
`UNDETERMINED` all PASS when the evidence supports them. An arm that only passed on ONE_REPAIR would
be an instruction to confirm the hypothesis -- the exact criterion-is-the-defect shape the CTO's
cut-time bar names, and this round would be the worst place to ship one.

Carried forward rather than re-learned: an UNDETERMINED verdict is admissible WITH evidence; the
no-repair arm grades the CELL'S OWN commits BY AUTHOR (W1-S39); a failed retrieval RAISES rather than
returning the value that passes (CTO residual 1); the commit list is ONE ordered `git log` (residual 2).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
CELL_AUTHOR = "0.9.0_WK_LGIC_LGCTFM~"
ENGINE_PATHS = ["lib/opal_lgctfm.py"]
VERDICTS = ("ONE_REPAIR", "TWO_REPAIRS", "UNDETERMINED")


def _scrub(t):
    return str(t).replace("VERDICT:", "verdict-").replace("PASS-", "pass-").replace("FAIL-", "fail-")


def say(tag, *lines):
    for ln in lines:
        print("  %s" % ln)
    print("VERDICT: %s" % tag)
    return 0


def verdict(ok, p, f, lines):
    return say(p if ok else f, *lines)


def base():
    with open(os.path.join(HERE, "R6_BASE.json"), encoding="utf-8") as fh:
        return json.load(fh)


def load_json(rel):
    p = rel if os.path.isabs(rel) else os.path.join(REPO, rel)
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


class InstrumentFailure(RuntimeError):
    """An exception is not an empty set: EMPTY is the value that PASSES (CTO residual 1)."""


def git(args, timeout=120):
    r = subprocess.run(["git"] + args, cwd=REPO, capture_output=True, timeout=timeout)
    if r.returncode != 0:
        raise InstrumentFailure("git %s rc=%d: %s" % (args[0], r.returncode,
                                                      (r.stderr or b"").decode("utf-8", "replace")[:160]))
    return (r.stdout or b"").decode("utf-8", "replace")


# ------------------------------------------------------------------ cores
def core_hypothesis(rec):
    """The hypothesis AND its falsifier are stated -- before any result can be read back into them."""
    h = ((rec or {}).get("hypothesis") or {})
    stated, fals = (h.get("stated") or "").strip(), (h.get("falsifier") or "").strip()
    lines = ["hypothesis stated: %d chars" % len(stated), "falsifier stated: %d chars" % len(fals)]
    bad = []
    if len(stated) < 40:
        bad.append("no hypothesis, or too thin to falsify")
    if len(fals) < 40:
        bad.append("NO FALSIFIER: a hypothesis with no stated falsifier is a conclusion waiting for evidence")
    return (not bad), lines + bad


def core_experiment(rec):
    """A DISCRIMINATING experiment: one change, both classes counted BEFORE and AFTER, with a denominator."""
    e = ((rec or {}).get("experiment") or {})
    before, after = (e.get("before") or {}), (e.get("after") or {})
    bad, lines = [], []
    for name, d in (("before", before), ("after", after)):
        missing = [k for k in ("tier_prefixed", "firm_prefixed", "denominator_s3key") if d.get(k) is None]
        if missing:
            bad.append("%s block lacks %s" % (name, _scrub(missing)))
    if not (e.get("what_was_changed") or "").strip():
        bad.append("the change under test is not described")
    if not (e.get("instrument") or "").strip():
        bad.append("no instrument named: a before/after with no command is a claim, not a measurement")
    if not (e.get("where_it_ran") or "").strip():
        bad.append("no location: the experiment runs in a scratch copy and the record says where")
    if not bad:
        lines = ["change: %s" % _scrub(str(e.get("what_was_changed"))[:70]),
                 "tier-prefixed  %s -> %s" % (_scrub(before.get("tier_prefixed")), _scrub(after.get("tier_prefixed"))),
                 "firm-prefixed  %s -> %s" % (_scrub(before.get("firm_prefixed")), _scrub(after.get("firm_prefixed"))),
                 "denominator (S3Key rows) %s -> %s" % (_scrub(before.get("denominator_s3key")),
                                                        _scrub(after.get("denominator_s3key")))]
        if before.get("tier_prefixed") == after.get("tier_prefixed") and \
           before.get("firm_prefixed") == after.get("firm_prefixed"):
            lines.append("NOTE: neither class moved -- that is a RESULT, not a failure of this arm")
    return (not bad), lines + bad


def core_verdict(rec):
    """EVERY verdict is reachable. The arm grades whether the evidence SEPARATES the two classes."""
    v = ((rec or {}).get("verdict") or {})
    val, ev = v.get("value"), (v.get("evidence") or "").strip()
    e = ((rec or {}).get("experiment") or {})
    before, after = (e.get("before") or {}), (e.get("after") or {})
    lines = ["verdict: %s (all of %s pass when the evidence supports them)" % (_scrub(val), _scrub(list(VERDICTS))),
             "evidence: %d chars" % len(ev)]
    if val not in VERDICTS:
        return False, lines + ["verdict must be one of %s" % _scrub(list(VERDICTS))]
    if len(ev) < 60:
        return False, lines + ["a verdict with no evidence is an assumption -- including UNDETERMINED"]
    # the evidence must speak to BOTH classes, whichever verdict it reaches
    ev_low = ev.lower()
    if not ("tier" in ev_low and "firm" in ev_low):
        return False, lines + ["the evidence names only one class: the question is about BOTH sites"]
    if val == "ONE_REPAIR":
        moved_both = (after.get("tier_prefixed") == 0 and after.get("firm_prefixed") == 0)
        if not moved_both:
            return False, lines + ["ONE_REPAIR claimed while a class still carries rows after the change"]
    if val == "TWO_REPAIRS":
        one_moved = (after.get("tier_prefixed") != before.get("tier_prefixed")) or \
                    (after.get("firm_prefixed") != before.get("firm_prefixed"))
        still_left = (after.get("tier_prefixed") or 0) > 0 or (after.get("firm_prefixed") or 0) > 0
        if not (one_moved and still_left):
            lines.append("NOTE: TWO_REPAIRS is accepted on the evidence text; the counts do not show a partial move")
    return True, lines


def core_no_landed_repair(own, foreign):
    lines = ["engine commits since the cut: %d by THIS CELL, %d elsewhere (EXCUSED)" % (len(own), len(foreign))]
    lines += ["    THIS CELL MOVED: %s" % _scrub(c) for c in own[:3]]
    return (not own), lines


def core_vintage(rec, resolvable):
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    want = {"check_lt_r6.py", "R6_BASE.json"}
    have = {os.path.basename(k) for k in fx}
    missing = sorted(want - have)
    lines = ["fixed inputs named at pin: %d %s" % (len(fx), _scrub(sorted(have))),
             "each commit resolvable: %s" % resolvable]
    if missing:
        lines.append("NOT NAMED: %s" % _scrub(missing))
    return (not missing and bool(fx) and resolvable), lines


def core_stale(commits, rec, prior):
    n = len(commits)
    if n == 0:
        return True, ["fixed-input commits since the cut: 0 -- no proof can be stale against them"]
    sp = ((rec or {}).get("stale_proofs") or {})
    named, prior = set(sp.get("proofs_re_run") or []), set(prior or ())
    lines = ["fixed-input commits since the cut: %d (informational)" % n,
             "proofs at risk: %d | record enumerates: %d" % (len(prior), len(named))]
    if named - prior:
        lines.append("NAMED BUT NEVER AT RISK: %s" % _scrub(sorted(named - prior)[:3]))
    return named == prior, lines


def _is_this_round(path, tag="r6"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def _rec():
    return load_json(base()["record_shape"]["paths"]["LT-e-7"])


def e7_hypothesis():
    ok, lines = core_hypothesis(_rec())
    return verdict(ok, "PASS-E7-HYPOTHESIS", "FAIL-E7-HYPOTHESIS", lines)


def e7_experiment():
    ok, lines = core_experiment(_rec())
    return verdict(ok, "PASS-E7-EXPERIMENT", "FAIL-E7-EXPERIMENT", lines)


def e7_verdict():
    ok, lines = core_verdict(_rec())
    return verdict(ok, "PASS-E7-VERDICT", "FAIL-E7-VERDICT", lines)


def e7_no_landed_repair():
    b = base()
    try:
        out = git(["log", "--format=%h %an %s", "%s..HEAD" % b["cut_pin"], "--"] + ENGINE_PATHS)
    except InstrumentFailure as exc:
        return say("FAIL-E7-NO-LANDED-REPAIR", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    rows = [ln for ln in out.splitlines() if ln.strip()]
    own = [ln for ln in rows if CELL_AUTHOR in ln]
    ok, lines = core_no_landed_repair(own, [ln for ln in rows if CELL_AUTHOR not in ln])
    return verdict(ok, "PASS-E7-NO-LANDED-REPAIR", "FAIL-E7-NO-LANDED-REPAIR", lines)


def r6_vintage_field():
    rec = _rec()
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    resolvable = True
    for path, commit in fx.items():
        try:
            git(["cat-file", "-e", "%s:%s" % (commit, path)])
        except InstrumentFailure:
            resolvable = False
    ok, lines = core_vintage(rec, resolvable)
    return verdict(ok, "PASS-R6-VINTAGE-FIELD", "FAIL-R6-VINTAGE-FIELD", lines)


def r6_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R6-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    ok, lines = core_stale(commits, _rec(), prior)
    return verdict(ok, "PASS-R6-STALE-PROOFS", "FAIL-R6-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _rec_for(value, after_tier, after_firm):
    return {"hypothesis": {"stated": "a single repair at the portal-stitch ingestion removes both classes of row",
                           "falsifier": "either class still carries rows after the single change is applied"},
            "experiment": {"what_was_changed": "resolve() records the firm-writer bucket instead of leaving arn empty",
                           "where_it_ran": "a scratch copy outside the repo",
                           "instrument": "python lib/opal_lgctfm.py walk --subject 49financial (scratch)",
                           "before": {"tier_prefixed": 23, "firm_prefixed": 1, "denominator_s3key": 154},
                           "after": {"tier_prefixed": after_tier, "firm_prefixed": after_firm,
                                     "denominator_s3key": 154}},
            "verdict": {"value": value,
                        "evidence": "the tier-prefixed class went to %s and the firm-prefixed class went to %s, "
                                    "measured on the same run" % (after_tier, after_firm)},
            "fixed_inputs_at_pin": {"a/check_lt_r6.py": "abc", "b/R6_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def selftest_arms():
    one = _rec_for("ONE_REPAIR", 0, 0)
    two = _rec_for("TWO_REPAIRS", 0, 1)
    und = _rec_for("UNDETERMINED", 23, 1)

    arm("POSITIVE-BAR-ONE_REPAIR-is-reachable", core_verdict(one)[0],
        "the hypothesis CONFIRMED passes")
    arm("POSITIVE-BAR-TWO_REPAIRS-is-reachable", core_verdict(two)[0],
        "the hypothesis FALSIFIED passes -- the arm does not reward agreement (CTO, round-5 analysis)")
    arm("POSITIVE-BAR-UNDETERMINED-is-reachable", core_verdict(und)[0],
        "and so does an honest inconclusive result")
    arm("POSITIVE-BAR-hypothesis-and-falsifier", core_hypothesis(one)[0])
    arm("POSITIVE-BAR-experiment-complete", core_experiment(one)[0])
    arm("POSITIVE-BAR-vintage", core_vintage(one, True)[0])
    arm("POSITIVE-BAR-no-landed-repair", core_no_landed_repair([], ["x 4.0.0_SA_CRO y"])[0])
    arm("POSITIVE-BAR-stale-mint", core_stale(["a mint"], one, set())[0])

    arm("MUTANT-hypothesis-without-a-falsifier", not core_hypothesis(
        {"hypothesis": {"stated": one["hypothesis"]["stated"], "falsifier": ""}})[0],
        "a hypothesis with no falsifier is a conclusion waiting for evidence")
    arm("MUTANT-experiment-no-instrument", not core_experiment(
        dict(one, experiment=dict(one["experiment"], instrument="")))[0])
    arm("MUTANT-experiment-no-after-counts", not core_experiment(
        dict(one, experiment=dict(one["experiment"], after={"tier_prefixed": 0})))[0])
    arm("MUTANT-verdict-ONE_REPAIR-while-a-class-remains", not core_verdict(
        _rec_for("ONE_REPAIR", 0, 1))[0], "the cheapest wrong answer, refused on the counts")
    arm("MUTANT-verdict-evidence-names-one-class", not core_verdict(
        dict(one, verdict={"value": "ONE_REPAIR", "evidence": "the tier-prefixed rows all went to zero on this run, "
                                                              "measured over the same denominator as before"}))[0],
        "the question is about BOTH sites")
    arm("MUTANT-verdict-no-evidence", not core_verdict(dict(one, verdict={"value": "UNDETERMINED", "evidence": ""}))[0])
    arm("MUTANT-verdict-bad-value", not core_verdict(dict(one, verdict={"value": "PROBABLY_ONE", "evidence": "x" * 80}))[0])
    arm("MUTANT-no-landed-repair-own-commit", not core_no_landed_repair(
        ["abc 0.9.0_WK_LGIC_LGCTFM~1 landed the fix"], [])[0])
    arm("MUTANT-vintage-absent", not core_vintage({}, True)[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(one, False)[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(one, stale_proofs={"proofs_re_run": ["no.proof_of_spec.json"]}), set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_LGCTFM.TO-LT-e-7-r6.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_LGCTFM.TO-LT-m-2-r5.x.proof_of_spec.json"))

    try:
        proofs_at_risk(["deadbeefdeadbeef nope"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True, "a failed retrieval RAISES (residual 1)")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-E7-VERDICT"))

    bad = [n for n, ok, _ in _ARMS if not ok]
    pos = len([n for n, _, _ in _ARMS if n.startswith("POSITIVE")])
    for n, ok, note in _ARMS:
        print("  %-48s %-4s %s" % (n, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(_ARMS), pos, len(_ARMS) - pos))
    print("  NOT driven here, stated: the git reads -- live, exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"e7-hypothesis": e7_hypothesis, "e7-experiment": e7_experiment, "e7-verdict": e7_verdict,
        "e7-no-landed-repair": e7_no_landed_repair, "r6-vintage-field": r6_vintage_field,
        "r6-stale-proofs": r6_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
