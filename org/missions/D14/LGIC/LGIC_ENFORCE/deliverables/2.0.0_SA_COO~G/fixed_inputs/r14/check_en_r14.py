"""LGIC_ENFORCE round 14 -- the arms for TWO cells the analysis ordered NOT to be paired.

1.0.0_SA_CTO @cf0cf68868: "DO NOT PAIR THEM: they share a file and nothing else, and A JOINT CELL WILL
REPORT THE EASIER ONE." So EN-r-7 (a REPAIR on the report's rendering) and EN-p-38 (a MEASUREMENT of a
grain ambiguity) have separate records, separate orders and separate arms, and no arm here reads the
other cell's record.

THE REPAIR'S SHAPE IS THE POINT, not the symptom: BOTH COLUMNS RENDER THROUGH ONE PATH. The arm does
NOT dictate which path -- any single renderer both columns call satisfies it -- because the CTO's
reason is forward-looking: "NOT to 'fix' the current column, or the asymmetry returns the next time a
third column is added."

Every criterion was built against a hand-made CORRECT record, driven as a POSITIVE-SATISFIABILITY arm
(the cut-time bar). The measurement cell's arm accepts an honest "no row carries more than one token"
as readily as a large overlap -- a criterion that only passed on a big number would be an instruction
to find one.
"""
import contextlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
CELL_AUTHOR = "0.9.0_WK_LGIC_ENFORCE~"
PRODUCER_PATHS = ["lib/opal_naming.py"]


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
    with open(os.path.join(HERE, "R14_BASE.json"), encoding="utf-8") as fh:
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
def core_one_path(rec):
    """ONE renderer, ONE rule, EVERY column routed -- proven by a token rendered alike in two columns.

    ⛔ IT DOES NOT GRADE THE COUNTS AGAINST EACH OTHER. Two columns hold DIFFERENT CONTENT, so
    `canonical_braces == current_braces` is a bar NO CORRECT ARTIFACT CAN MEET -- it would be the
    criterion that is the defect. The asymmetry lives in the RULE, and that is what is graded.

    The routed set is written as a SUBTRACTION from the table's own column denominator, never as a
    forward list of the columns the author had in mind (Rule 24).
    """
    r = ((rec or {}).get("render") or {})
    path = (r.get("one_path") or "").strip()
    routed, total = list(r.get("columns_routed") or []), list(r.get("columns_total") or [])
    rules = r.get("rule_per_column") or {}
    wit = r.get("witness") or {}
    disc = (r.get("population_discriminator") or "").strip()
    third = (r.get("third_column_argument") or "").strip()
    before, after = (r.get("before") or {}), (r.get("after") or {})
    bad, lines = [], ["one render path: %s" % _scrub(path or "(none named)"),
                      "columns in the table (denominator): %d %s" % (len(total), _scrub(total)),
                      "columns routed through the one path: %d" % len(routed),
                      "rows denominator: %s" % _scrub(r.get("denominator_rows"))]
    if ":" not in path:
        bad.append("the single render path is not named at a file:line site")
    if len(total) < 2:
        bad.append("fewer than TWO columns in the denominator: the defect IS the asymmetry between columns")
    unrouted = [c for c in total if c not in routed]
    lines.append("NOT routed (denominator MINUS routed): %d %s" % (len(unrouted), _scrub(unrouted)))
    if unrouted:
        bad.append("a column still renders outside the one path -- that is the asymmetry, moved")
    if [c for c in routed if c not in total]:
        bad.append("a routed column is not in the table's own denominator: the denominator is wrong")
    if set(rules) != set(total):
        bad.append("rule_per_column does not cover exactly the table's columns: %s"
                   % _scrub(sorted(set(total) ^ set(rules))))
    else:
        distinct = sorted({str(v).strip() for v in rules.values()})
        lines.append("DISTINCT rendering rules across the columns: %d %s" % (len(distinct), _scrub(distinct)))
        if len(distinct) != 1 or not distinct[0]:
            bad.append("more than ONE rendering rule survives: fixing ONE column moves the asymmetry, "
                       "it does not end it")
    rendered = (wit.get("rendered_in") or {})
    if not (wit.get("token") or "").strip() or len(rendered) < 2:
        bad.append("no WITNESS: a token that occurs in at least TWO columns, with its rendering in each")
    else:
        vals = sorted(set(rendered.values()))
        lines.append("witness token %s renders as %s across %d columns"
                     % (_scrub(wit.get("token")), _scrub(vals), len(rendered)))
        if len(vals) != 1:
            bad.append("THE ASYMMETRY SURVIVES AT THE WITNESS: the same token renders differently")
    for name, d in (("before", before), ("after", after)):
        miss = [k for k in ("canonical_braces", "canonical_parens", "current_braces", "current_parens")
                if d.get(k) is None]
        if miss:
            bad.append("%s block lacks %s (disclosure, not a bar on the counts)" % (name, _scrub(miss)))
    if not disc:
        bad.append("no population_discriminator: once no column is singled out by carrying braces, the "
                   "record must say what identifies the population instead")
    if not third:
        bad.append("no third-column argument: the repair must say why a NEW column renders the same way")
    return (not bad), lines + bad


def core_no_producer_change(own, foreign):
    lines = ["producer commits since the cut: %d by THIS CELL, %d elsewhere (EXCUSED)" % (len(own), len(foreign))]
    lines += ["    THIS CELL MOVED: %s" % _scrub(c) for c in own[:3]]
    return (not own), lines


def core_grain(rec):
    """The reconciliation, with the multiplicity measured -- and ZERO overlap is an admissible answer."""
    g = ((rec or {}).get("grain") or {})
    bad, lines = [], []
    for k in ("by_token_sum", "rows_with_a_placeholder", "rows_carrying_more_than_one"):
        if g.get(k) is None:
            bad.append("grain block lacks %s" % k)
    if not (g.get("input_report_pinned_at") or "").strip():
        bad.append("the input report is not PINNED by commit: a moving input cannot be reconciled")
    if not (g.get("reconciliation") or "").strip():
        bad.append("no reconciliation sentence: the two figures must be unable to read as disagreeing")
    dist = g.get("distribution") or {}
    if not isinstance(dist, dict) or not dist:
        bad.append("no distribution: how many rows carry 1, 2, 3 ... tokens")
    if not bad:
        s, rows, multi = g["by_token_sum"], g["rows_with_a_placeholder"], g["rows_carrying_more_than_one"]
        lines = ["by-token sum %s vs rows %s (difference %s)" % (_scrub(s), _scrub(rows), _scrub(s - rows)),
                 "rows carrying MORE THAN ONE token: %s" % _scrub(multi),
                 "distribution: %s" % _scrub(dist),
                 "input pinned at: %s" % _scrub(g.get("input_report_pinned_at"))]
        if s != rows and multi == 0:
            bad.append("the sum exceeds the row count while NO row carries more than one token -- "
                       "the reconciliation does not close")
        if s == rows and multi != 0:
            bad.append("the sum equals the row count while rows carry several tokens -- it cannot")
    return (not bad), lines + bad


def core_vintage(rec, resolvable, want):
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    have = {os.path.basename(k) for k in fx}
    missing = sorted(set(want) - have)
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


def _is_this_round(path, tag="r14"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


def _rec(cell):
    return load_json(base()["record_shape"]["paths"][cell])


# ------------------------------------------------------------------ arms
def r7_one_path():
    ok, lines = core_one_path(_rec("EN-r-7"))
    return verdict(ok, "PASS-R7-ONE-PATH", "FAIL-R7-ONE-PATH", lines)


def r7_no_producer_change():
    b = base()
    try:
        out = git(["log", "--format=%h %an %s", "%s..HEAD" % b["cut_pin"], "--"] + PRODUCER_PATHS)
    except InstrumentFailure as exc:
        return say("FAIL-R7-NO-PRODUCER-CHANGE", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    rows = [ln for ln in out.splitlines() if ln.strip()]
    own = [ln for ln in rows if CELL_AUTHOR in ln]
    ok, lines = core_no_producer_change(own, [ln for ln in rows if CELL_AUTHOR not in ln])
    return verdict(ok, "PASS-R7-NO-PRODUCER-CHANGE", "FAIL-R7-NO-PRODUCER-CHANGE",
                   ["S101 resolved at the source that the producer is CORRECT at the values"] + lines)


def p38_grain():
    ok, lines = core_grain(_rec("EN-p-38"))
    return verdict(ok, "PASS-P38-GRAIN", "FAIL-P38-GRAIN", lines)


def _cells_present():
    """The round-14 cells whose record EXISTS IN THIS CHECKOUT -- never the hard-coded pair.

    ⛔ THIS WRAPPER USED TO GRADE BOTH CELLS AND AND THEIR RESULTS, AND THAT WAS THE DEFECT
    (LGIC_ENFORCE-S106). The two cells run in SEPARATE WORKTREES by design -- the round's one
    instruction was DO NOT PAIR THEM -- so neither could ever see the other's record, and NEITHER
    COULD SATISFY THE ARM BY DOING ITS OWN WORK CORRECTLY AND COMPLETELY. I unpaired the cells, the
    orders, the records and the worktrees, and then paired them in an arm.

    ⭐ THE FIX TAKES NO ARGUMENT, DELIBERATELY: both orders' <invocation> lines are already at HEAD and
    a worker may be reading one RIGHT NOW. Changing the invocation would be a task-order modification,
    which no gate refuses and no worker sees. So the arm reads its population off the CHECKOUT: in a
    worker's worktree that is exactly its own cell; in the merged tree after the drain it is both, and
    grading both there is correct because both are present.

    An EMPTY population is REFUSED, not vacuously passed -- a cell that wrote no record at all must
    still fail this arm.
    """
    return [c for c in ("EN-r-7", "EN-p-38") if _rec(c) is not None]


def r14_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R14-VINTAGE-FIELD",
                   "no round-14 record exists in this checkout: an empty population is REFUSED here, "
                   "never passed vacuously")
    ok_all, out_lines = True, ["records present in THIS checkout: %d %s (the arm grades these and "
                               "only these -- S106)" % (len(cells), _scrub(cells))]
    for cell in cells:
        rec = _rec(cell)
        fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
        resolvable = True
        for path, commit in fx.items():
            try:
                git(["cat-file", "-e", "%s:%s" % (commit, path)])
            except InstrumentFailure:
                resolvable = False
        ok, lines = core_vintage(rec, resolvable, ("check_en_r14.py", "R14_BASE.json"))
        ok_all = ok_all and ok
        out_lines += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R14-VINTAGE-FIELD", "FAIL-R14-VINTAGE-FIELD", out_lines)


def r14_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R14-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    ok_all, lines = True, []
    for cell in ("EN-r-7", "EN-p-38"):
        ok, ls = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        lines += ["%s:" % cell] + ["  " + x for x in ls]
    return verdict(ok_all, "PASS-R14-STALE-PROOFS", "FAIL-R14-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


COLS = ["current", "canonical", "verdict", "type", "plane", "where"]


def _render_ok():
    return {"render": {"one_path": "org/.../render_row.py:41",
                       "columns_routed": list(COLS), "columns_total": list(COLS),
                       "rule_per_column": {c: "escape { } to ( )" for c in COLS},
                       "witness": {"token": "{snap}",
                                   "rendered_in": {"canonical": "(snap)", "current": "(snap)"}},
                       "population_discriminator": "the population is read from the census json, not from "
                                                   "which column still carries brace bytes",
                       "before": {"canonical_braces": 1303, "canonical_parens": 0,
                                  "current_braces": 0, "current_parens": 8},
                       "after": {"canonical_braces": 0, "canonical_parens": 1303,
                                 "current_braces": 0, "current_parens": 8},
                       "denominator_rows": 3264,
                       "third_column_argument": "any new column calls the same renderer, so it cannot diverge"},
            "fixed_inputs_at_pin": {"a/check_en_r14.py": "abc", "b/R14_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def _grain_ok(sum_=1449, rows=1303, multi=131):
    return {"grain": {"input_report_pinned_at": "c05f9f9fc9", "by_token_sum": sum_,
                      "rows_with_a_placeholder": rows, "rows_carrying_more_than_one": multi,
                      "distribution": {"1": rows - multi, "2": multi},
                      "reconciliation": "each row contributes once per DISTINCT token it carries"},
            "fixed_inputs_at_pin": {"a/check_en_r14.py": "abc", "b/R14_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def selftest_arms():
    r, g = _render_ok(), _grain_ok()
    arm("POSITIVE-BAR-render-correct-record", core_one_path(r)[0])
    arm("POSITIVE-BAR-grain-correct-record", core_grain(g)[0])
    arm("POSITIVE-BAR-grain-zero-overlap-is-admissible", core_grain(_grain_ok(1303, 1303, 0))[0],
        "an honest 'no row carries more than one token' PASSES -- a bar that only passed on a big overlap "
        "would be an instruction to find one")
    arm("POSITIVE-BAR-vintage", core_vintage(r, True, ("check_en_r14.py", "R14_BASE.json"))[0])
    arm("POSITIVE-BAR-no-producer-change", core_no_producer_change([], ["x 1.0.0_SA_CTO y"])[0])
    arm("POSITIVE-BAR-stale-mint", core_stale(["a mint"], r, set())[0])

    arm("POSITIVE-BAR-render-raw-rule-is-equally-admissible", core_one_path(
        dict(r, render=dict(r["render"],
                            rule_per_column={c: "no substitution, braces kept verbatim" for c in COLS},
                            witness={"token": "{snap}",
                                     "rendered_in": {"canonical": "{snap}", "current": "{snap}"}})))[0],
        "the arm does NOT dictate WHICH path -- escape-everywhere and escape-nowhere both PASS; "
        "only ONE RULE FOR EVERY COLUMN is required")
    arm("MUTANT-render-one-column-only", not core_one_path(
        dict(r, render=dict(r["render"], columns_routed=["current"])))[0],
        "fixing ONE column is the move the CTO refused: the asymmetry returns with a third column")
    arm("MUTANT-render-two-rules-survive", not core_one_path(
        dict(r, render=dict(r["render"],
                            rule_per_column=dict({c: "escape { } to ( )" for c in COLS},
                                                 canonical="braces kept verbatim"))))[0],
        "every column routed, but TWO rules: the asymmetry moved rather than ended")
    arm("MUTANT-render-witness-diverges", not core_one_path(
        dict(r, render=dict(r["render"], witness={"token": "{snap}",
                                                  "rendered_in": {"canonical": "{snap}",
                                                                  "current": "(snap)"}})))[0])
    arm("MUTANT-render-no-witness", not core_one_path(
        dict(r, render=dict(r["render"], witness={})))[0])
    arm("MUTANT-render-column-outside-denominator", not core_one_path(
        dict(r, render=dict(r["render"], columns_total=["current", "canonical"])))[0],
        "the subtraction must run over the TABLE's columns, not a forward list")
    arm("MUTANT-render-no-population-discriminator", not core_one_path(
        dict(r, render=dict(r["render"], population_discriminator="")))[0],
        "the escaping was load-bearing for the r13 arm; a repair that drops it silently must say "
        "what identifies the population instead")
    arm("MUTANT-render-no-site", not core_one_path(
        dict(r, render=dict(r["render"], one_path="the renderer")))[0])
    arm("MUTANT-render-no-third-column-argument", not core_one_path(
        dict(r, render=dict(r["render"], third_column_argument="")))[0])

    arm("MUTANT-grain-unpinned-input", not core_grain(
        dict(g, grain=dict(g["grain"], input_report_pinned_at="")))[0],
        "a moving input cannot be reconciled")
    arm("MUTANT-grain-no-reconciliation", not core_grain(
        dict(g, grain=dict(g["grain"], reconciliation="")))[0])
    arm("MUTANT-grain-arithmetic-does-not-close", not core_grain(_grain_ok(1449, 1303, 0))[0],
        "a sum above the row count with NO multi-token row cannot close")
    arm("MUTANT-grain-impossible-equality", not core_grain(_grain_ok(1303, 1303, 40))[0])
    arm("MUTANT-grain-no-distribution", not core_grain(
        dict(g, grain=dict(g["grain"], distribution={})))[0])

    arm("MUTANT-producer-own-commit", not core_no_producer_change(["a 0.9.0_WK_LGIC_ENFORCE~1 changed it"], [])[0])
    arm("MUTANT-vintage-absent", not core_vintage({}, True, ("check_en_r14.py", "R14_BASE.json"))[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(r, False, ("check_en_r14.py", "R14_BASE.json"))[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(r, stale_proofs={"proofs_re_run": ["n.proof_of_spec.json"]}), set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_ENFORCE.TO-EN-r-7-r14.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_ENFORCE.TO-EN-p-37-r13.x.proof_of_spec.json"))

    try:
        proofs_at_risk(["deadbeefdeadbeef nope"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True, "a failed retrieval RAISES (residual 1)")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-R7-ONE-PATH"))

    # ------------------------------------------------------------------ THE WIRING, NOT THE ARMS
    # ⛔ S106: every arm above drives a CORE with a hand-built record, ONE CELL AT A TIME -- and the
    # defect lived in the WRAPPER, which none of them touched. An injected self-test certifies the
    # ARMS, never the WIRING. These four drive the wrapper's own population decision.
    global _rec
    real_rec = _rec
    try:
        _rec = lambda c: _render_ok() if c == "EN-r-7" else None          # noqa: E731
        arm("WIRING-only-one-record-present-grades-only-it", _cells_present() == ["EN-r-7"],
            "a worker's worktree holds exactly ITS OWN record -- the population is the checkout, "
            "not a hard-coded pair")
        _rec = lambda c: None if c == "EN-r-7" else _grain_ok()           # noqa: E731
        arm("WIRING-the-sibling-alone-also-grades-alone", _cells_present() == ["EN-p-38"])
        _rec = lambda c: _render_ok() if c == "EN-r-7" else _grain_ok()   # noqa: E731
        arm("WIRING-merged-tree-grades-both", _cells_present() == ["EN-r-7", "EN-p-38"],
            "after the drain both records are present and grading both is correct")
        _rec = lambda c: None                                             # noqa: E731
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r14_vintage_field()
        arm("WIRING-empty-population-is-REFUSED-not-vacuous",
            "VERDICT: FAIL-R14-VINTAGE-FIELD" in buf.getvalue(),
            "the REAL arm is run, output captured: a cell that wrote no record must still fail, "
            "and an empty set is not a vacuous pass")
        # THE S106 REGRESSION ARM, and it is run against the REAL arm with a REAL resolvable pin --
        # a fixture naming a made-up commit cannot pass, because the arm resolves every pin against git.
        here = os.path.relpath(os.path.join(HERE, "check_en_r14.py"), REPO).replace(os.sep, "/")
        base_rel = os.path.relpath(os.path.join(HERE, "R14_BASE.json"), REPO).replace(os.sep, "/")
        live = dict(_render_ok(), fixed_inputs_at_pin={here: "HEAD", base_rel: "HEAD"})
        buf = io.StringIO()
        _rec = lambda c: live if c == "EN-r-7" else None                  # noqa: E731
        with contextlib.redirect_stdout(buf):
            r14_vintage_field()
        out = buf.getvalue()
        arm("WIRING-one-correct-record-ALONE-now-PASSES-the-real-arm",
            "VERDICT: PASS-R14-VINTAGE-FIELD" in out and "EN-p-38:" not in out,
            "BEFORE THE REPAIR THIS RETURNED FAIL ON THE SIBLING'S ABSENT HALF, which no correct "
            "artifact from one cell could ever fix -- and the absent cell is no longer even named")
    finally:
        _rec = real_rec

    bad = [n for n, ok, _ in _ARMS if not ok]
    pos = len([n for n, _, _ in _ARMS if n.startswith("POSITIVE")])
    for n, ok, note in _ARMS:
        print("  %-52s %-4s %s" % (n, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(_ARMS), pos, len(_ARMS) - pos))
    print("  NOT driven here, stated: the git reads -- live, exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"r7-one-path": r7_one_path, "r7-no-producer-change": r7_no_producer_change,
        "p38-grain": p38_grain, "r14-vintage-field": r14_vintage_field,
        "r14-stale-proofs": r14_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
