"""LGIC_LGCTFM round 5 -- the arms for LT-m-2, a MEASUREMENT cell.

1.0.0_SA_CTO's round-4 analysis @abea09f936 cut this as a measurement and NOT a repair: the bucketless
S3Key rows are plausibly SEVERAL causes, and a cell that assumes one remedy makes the NUMBERS agree
rather than the DATA. The questions are WHICH PRODUCER writes an S3Key with no bucket, and HOW MANY
producers there are.

EVERY CRITERION HERE WAS BUILT AGAINST A HAND-MADE CORRECT RECORD BEFORE IT SHIPPED -- the bar round 4
earned, stated by the CTO and binding at CUT time: "can a CORRECT artifact satisfy this?  Where the
honest answer is no, THE CRITERION IS THE DEFECT, NOT THE CELL." That record is `_correct()` below and
it is driven as a POSITIVE-SATISFIABILITY arm, so the bar is exercised rather than promised.

Two shapes are carried forward from round 4's four repairs rather than re-learned:
  * the no-repair arm grades the CELL'S OWN COMMITS BY AUTHOR, never the tree (W1-S39: another
    project's commit failed my cell, and the cheapest green was to revert a seat that was not in the
    round);
  * a failed retrieval RAISES instead of returning the value that PASSES (CTO residual 1), and the
    commit list is ONE ordered `git log` over all watched paths (residual 2).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
CELL_AUTHOR = "0.9.0_WK_LGIC_LGCTFM~"
NO_REPAIR_PATHS = ["lib/opal_lgctfm.py", "infra/logic/registry/",
                   "org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json"]


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
    with open(os.path.join(HERE, "R5_BASE.json"), encoding="utf-8") as fh:
        return json.load(fh)


def load_json(rel):
    p = rel if os.path.isabs(rel) else os.path.join(REPO, rel)
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


class InstrumentFailure(RuntimeError):
    """An exception is not an empty set: EMPTY is the value that PASSES at a mint (CTO residual 1)."""


def git(args, timeout=120):
    r = subprocess.run(["git"] + args, cwd=REPO, capture_output=True, timeout=timeout)
    if r.returncode != 0:
        raise InstrumentFailure("git %s rc=%d: %s" % (args[0], r.returncode,
                                                      (r.stderr or b"").decode("utf-8", "replace")[:160]))
    return (r.stdout or b"").decode("utf-8", "replace")


# ------------------------------------------------------------------ measurement
def newest_run():
    home = os.path.join(REPO, "workflows", "legacy_transform", "blackdiamond-49financial")
    runs = [d for d in os.listdir(home) if os.path.isdir(os.path.join(home, d))]
    if not runs:
        raise InstrumentFailure("no run directory under %s" % home)
    runs.sort(key=lambda d: os.path.getmtime(os.path.join(home, d)))
    return os.path.join(home, runs[-1]), runs[-1]


def measure_population():
    """The bucketless S3Key rows, measured from the run's own contract. Returns (row_ids, by_shape, n_s3)."""
    run_dir, run_id = newest_run()
    p = os.path.join(run_dir, "contract.json")
    if not os.path.exists(p):
        raise InstrumentFailure("no contract.json in %s" % run_id)
    with open(p, encoding="utf-8") as fh:
        c = json.load(fh)
    s3 = [r for r in (c.get("rows") or []) if r.get("node_type") == "S3Key"]
    tiers = {"gold", "silver", "bronze", "platinum"}
    ids, shapes = [], {}
    for r in s3:
        v = ((r.get("current") or {}).get("arn_or_path") or {}).get("value")
        if not isinstance(v, str):
            ids.append(r.get("row_id"))
            shapes["no_path_value"] = shapes.get("no_path_value", 0) + 1
            continue
        body = v[3:] if v.startswith("s3:") else v
        head = body.split("/")[0] if body else ""
        if not head:
            ids.append(r.get("row_id"))
            shapes["bare_s3_colon"] = shapes.get("bare_s3_colon", 0) + 1
        elif head in tiers:
            ids.append(r.get("row_id"))
            shapes["tier_prefixed"] = shapes.get("tier_prefixed", 0) + 1
        elif "-" not in head and "." not in head:
            # a bucket name carries a separator in this estate; a bare word is a firm/scope token
            ids.append(r.get("row_id"))
            shapes["firm_prefixed"] = shapes.get("firm_prefixed", 0) + 1
    return sorted(i for i in ids if i), shapes, len(s3), run_id


# ------------------------------------------------------------------ cores
def core_population(measured_ids, shapes, n_s3, rec):
    pop = ((rec or {}).get("population") or {})
    named = sorted(pop.get("row_ids") or [])
    lines = ["S3Key rows in the run: %d (denominator)" % n_s3,
             "measured WITHOUT a resolvable bucket: %d %s" % (len(measured_ids), _scrub(shapes)),
             "record enumerates: %d" % len(named)]
    if named != sorted(measured_ids):
        lines.append("NAMED BUT NOT MEASURED: %s" % _scrub(sorted(set(named) - set(measured_ids))[:5]))
        lines.append("MEASURED AND NOT NAMED: %s" % _scrub(sorted(set(measured_ids) - set(named))[:5]))
        return False, lines
    if pop.get("without_a_resolvable_bucket") not in (None, len(measured_ids)):
        lines.append("record's COUNT disagrees with its own list")
        return False, lines
    return True, lines


def core_producers(measured_ids, rec):
    """Every row is attributed to a NAMED producer, or listed as unattributed WITH a reason.

    An unattributed row is ADMISSIBLE -- a cell that genuinely cannot reach a producer must be able to
    say so without fabricating one. What is refused is SILENCE: a row in neither list.
    """
    pr = ((rec or {}).get("producers") or {})
    by = pr.get("by_producer") or []
    attributed, bad = {}, []
    for entry in by:
        who = (entry.get("producer") or "").strip()
        how = (entry.get("how_it_was_attributed") or "").strip()
        if not who or not how:
            bad.append("a by_producer entry lacks producer or how_it_was_attributed")
        for rid in entry.get("rows") or []:
            attributed[rid] = who
    un = ((rec or {}).get("unattributed") or {})
    un_rows = set(un.get("rows") or [])
    if un_rows and not (un.get("why") or "").strip():
        bad.append("unattributed rows are listed with no `why`")
    covered = set(attributed) | un_rows
    missing = sorted(set(measured_ids) - covered)
    lines = ["producers named: %d (record states %s)" % (len(by), _scrub(pr.get("count"))),
             "rows attributed: %d | unattributed WITH a reason: %d" % (len(attributed), len(un_rows)),
             "rows in NEITHER list: %d" % len(missing)]
    if missing:
        lines.append("SILENT ROWS: %s" % _scrub(missing[:5]))
    if pr.get("count") is not None and pr.get("count") != len(by):
        bad.append("producer COUNT disagrees with the by_producer list")
    return (not missing and not bad), lines + bad


def core_no_repair(own_commits, foreign):
    lines = ["commits touching the engine/registries since the cut: %d by THIS CELL, %d elsewhere (EXCUSED)"
             % (len(own_commits), len(foreign))]
    lines += ["    THIS CELL MOVED: %s" % _scrub(c) for c in own_commits[:4]]
    lines += ["    excused: %s" % _scrub(c) for c in foreign[:3]]
    return (not own_commits), lines


def core_vintage(rec, resolvable):
    """The vintage FIELD (CTO ADDENDUM 3): each fixed input the cell invoked, with its commit."""
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    want = {"check_lt_r5.py", "R5_BASE.json"}
    have = {os.path.basename(k) for k in fx}
    lines = ["fixed inputs named at pin: %d %s" % (len(fx), _scrub(sorted(have))),
             "each commit resolvable: %s" % resolvable]
    missing = sorted(want - have)
    if missing:
        lines.append("NOT NAMED: %s" % _scrub(missing))
    return (not missing and bool(fx) and resolvable), lines


def core_stale(commits, rec, prior):
    n = len(commits)
    if n == 0:
        return True, ["fixed-input commits since the cut: 0 -- no proof can be stale against them"]
    sp = ((rec or {}).get("stale_proofs") or {})
    named, prior = set(sp.get("proofs_re_run") or []), set(prior or ())
    lines = ["fixed-input commits since the cut: %d (informational, checkout-dependent)" % n,
             "proofs at risk: %d | record enumerates: %d" % (len(prior), len(named))]
    if named - prior:
        lines.append("NAMED BUT NEVER AT RISK: %s" % _scrub(sorted(named - prior)[:3]))
    if prior - named:
        lines.append("AT RISK AND NOT RE-RUN: %s" % _scrub(sorted(prior - named)[:3]))
    return named == prior, lines


def _is_this_round(path, tag="r5"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    oldest = commits[-1].split()[0]
    out = git(["ls-tree", "-r", "--name-only", "%s^" % oldest, "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def s41_population():
    b = base()
    try:
        ids, shapes, n_s3, run_id = measure_population()
    except InstrumentFailure as exc:
        return say("FAIL-S41-POPULATION", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    rec = load_json(b["record_shape"]["paths"]["LT-m-2"])
    ok, lines = core_population(ids, shapes, n_s3, rec)
    return verdict(ok, "PASS-S41-POPULATION", "FAIL-S41-POPULATION", ["run read: %s" % _scrub(run_id)] + lines)


def s41_producers():
    b = base()
    try:
        ids, _s, _n, _r = measure_population()
    except InstrumentFailure as exc:
        return say("FAIL-S41-PRODUCERS", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    rec = load_json(b["record_shape"]["paths"]["LT-m-2"])
    ok, lines = core_producers(ids, rec)
    return verdict(ok, "PASS-S41-PRODUCERS", "FAIL-S41-PRODUCERS", lines)


def s41_no_repair():
    b = base()
    try:
        out = git(["log", "--format=%h %an %s", "%s..HEAD" % b["cut_pin"], "--"] + NO_REPAIR_PATHS)
    except InstrumentFailure as exc:
        return say("FAIL-S41-NO-REPAIR", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    rows = [ln for ln in out.splitlines() if ln.strip()]
    own = [ln for ln in rows if CELL_AUTHOR in ln]
    foreign = [ln for ln in rows if CELL_AUTHOR not in ln]
    ok, lines = core_no_repair(own, foreign)
    return verdict(ok, "PASS-S41-NO-REPAIR", "FAIL-S41-NO-REPAIR", lines)


def r5_vintage_field():
    b = base()
    rec = load_json(b["record_shape"]["paths"]["LT-m-2"])
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    resolvable = True
    for path, commit in fx.items():
        try:
            git(["cat-file", "-e", "%s:%s" % (commit, path)])
        except InstrumentFailure:
            resolvable = False
    ok, lines = core_vintage(rec, resolvable)
    return verdict(ok, "PASS-R5-VINTAGE-FIELD", "FAIL-R5-VINTAGE-FIELD", lines)


def r5_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R5-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    rec = load_json(b["record_shape"]["paths"]["LT-m-2"])
    ok, lines = core_stale(commits, rec, prior)
    return verdict(ok, "PASS-R5-STALE-PROOFS", "FAIL-R5-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _correct(ids):
    """THE HAND-BUILT CORRECT RECORD. Every criterion must be satisfiable by THIS."""
    return {"population": {"s3key_rows": 154, "without_a_resolvable_bucket": len(ids), "row_ids": list(ids)},
            "producers": {"count": 1, "by_producer": [
                {"producer": "lib/opal_lgctfm.py:cmd_walk s3 leg", "rows": list(ids),
                 "how_it_was_attributed": "instrumented the leg and re-ran it"}]},
            "unattributed": {"rows": [], "why": ""},
            "fixed_inputs_at_pin": {"a/check_lt_r5.py": "abc1234", "b/R5_BASE.json": "abc1234"},
            "stale_proofs": {"fixed_input_commits_since_cut": 1, "proofs_re_run": []}}


def selftest_arms():
    ids = ["R-0001", "R-0002", "R-0003"]
    good = _correct(ids)
    shapes = {"tier_prefixed": 2, "firm_prefixed": 1}

    arm("POSITIVE-BAR-a-correct-record-satisfies-population", core_population(ids, shapes, 154, good)[0],
        "the bar the CTO set at cut time, exercised rather than promised")
    arm("POSITIVE-BAR-a-correct-record-satisfies-producers", core_producers(ids, good)[0])
    arm("POSITIVE-BAR-a-correct-record-satisfies-vintage", core_vintage(good, True)[0])
    arm("POSITIVE-BAR-a-correct-record-satisfies-no-repair", core_no_repair([], ["x 4.0.0_SA_CRO y"])[0])
    arm("POSITIVE-BAR-a-correct-record-satisfies-stale", core_stale(["a x"], good, set())[0])

    arm("MUTANT-population-underenumerates", not core_population(ids, shapes, 154,
        {"population": {"row_ids": ids[:2]}})[0])
    arm("MUTANT-population-invents-a-row", not core_population(ids, shapes, 154,
        {"population": {"row_ids": ids + ["R-9999"]}})[0])
    arm("MUTANT-population-count-disagrees", not core_population(ids, shapes, 154,
        {"population": {"row_ids": ids, "without_a_resolvable_bucket": 2}})[0])

    arm("POSITIVE-producers-unattributed-with-a-reason", core_producers(ids, {
        "producers": {"count": 1, "by_producer": [{"producer": "p", "rows": ids[:2], "how_it_was_attributed": "i"}]},
        "unattributed": {"rows": ids[2:], "why": "the leg is not reachable from the served graph"}})[0],
        "a cell that genuinely cannot attribute a row says so WITHOUT fabricating a producer")
    arm("MUTANT-producers-silent-row", not core_producers(ids, {
        "producers": {"count": 1, "by_producer": [{"producer": "p", "rows": ids[:2], "how_it_was_attributed": "i"}]},
        "unattributed": {"rows": [], "why": ""}})[0], "a row in NEITHER list is the refusal")
    arm("MUTANT-producers-unattributed-without-a-reason", not core_producers(ids, {
        "producers": {"count": 1, "by_producer": [{"producer": "p", "rows": ids[:2], "how_it_was_attributed": "i"}]},
        "unattributed": {"rows": ids[2:], "why": ""}})[0])
    arm("MUTANT-producers-count-disagrees", not core_producers(ids, {
        "producers": {"count": 3, "by_producer": [{"producer": "p", "rows": ids, "how_it_was_attributed": "i"}]}})[0])
    arm("MUTANT-producers-no-instrument", not core_producers(ids, {
        "producers": {"count": 1, "by_producer": [{"producer": "p", "rows": ids, "how_it_was_attributed": ""}]}})[0],
        "HOW a row was attributed is required: an inference from the path's shape is not an attribution")

    arm("MUTANT-no-repair-own-commit", not core_no_repair(["abc 0.9.0_WK_LGIC_LGCTFM~1 moved the engine"], [])[0])
    arm("POSITIVE-no-repair-foreign-commit-excused", core_no_repair([], ["abc 4.0.0_SA_CRO registry(...)"])[0],
        "another seat's commit is not this cell's act (W1-S39, carried forward)")

    arm("MUTANT-vintage-absent", not core_vintage({}, True)[0])
    arm("MUTANT-vintage-unresolvable-commit", not core_vintage(good, False)[0])
    arm("MUTANT-vintage-missing-one-input", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_lt_r5.py": "abc"}}, True)[0])

    arm("POSITIVE-stale-mint", core_stale(["a mint"], {"stale_proofs": {"proofs_re_run": []}}, set())[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], {"stale_proofs": {"proofs_re_run": ["never.proof_of_spec.json"]}}, set())[0])
    arm("MUTANT-stale-unenumerated", not core_stale(["a x"], {"stale_proofs": {"proofs_re_run": []}}, {"p.proof_of_spec.json"})[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_LGCTFM.TO-LT-m-2-r5.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_LGCTFM.TO-LT-x-5-r4.x.proof_of_spec.json"),
        "an r4 proof is frozen history (R-43)")

    try:
        proofs_at_risk(["deadbeefdeadbeef no-such-commit"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "it returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True, "a failed retrieval RAISES (CTO residual 1)")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-S41-POPULATION"))

    bad = [n for n, ok, _ in _ARMS if not ok]
    pos = len([n for n, _, _ in _ARMS if n.startswith("POSITIVE")])
    for n, ok, note in _ARMS:
        print("  %-52s %-4s %s" % (n, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(_ARMS), pos, len(_ARMS) - pos))
    print("  NOT driven here, stated: the contract read and the git calls -- live, exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"s41-population": s41_population, "s41-producers": s41_producers, "s41-no-repair": s41_no_repair,
        "r5-vintage-field": r5_vintage_field, "r5-stale-proofs": r5_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
