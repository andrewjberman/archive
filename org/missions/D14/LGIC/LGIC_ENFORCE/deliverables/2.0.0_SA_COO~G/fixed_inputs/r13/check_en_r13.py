"""LGIC_ENFORCE round 13 -- the arms for EN-p-37, a MEASUREMENT cell on R-38's placeholder population.

WHAT THE ARMS CAN AND CANNOT DO, STATED FIRST because it bounds every verdict below: this checker CANNOT
re-run a live census. It grades the cell's OWN REPORT ARTIFACT -- it re-counts the placeholder rows in the
report the cell produced and compares that to what the record claims. So a PASS here means THE RECORD AGREES
WITH THE ARTIFACT THE CELL PRODUCED, never that the live plane was read correctly. The live half is
`EN-p-37`'s judgment criterion and 3.0.0_SA_CVO's at L9.

Every criterion was built against a hand-made CORRECT record (`_correct()`), driven as a
POSITIVE-SATISFIABILITY arm -- the CTO's cut-time bar: "can a CORRECT artifact satisfy this? Where the honest
answer is no, THE CRITERION IS THE DEFECT, NOT THE CELL."

Carried forward rather than re-learned: an UNATTRIBUTED item is ADMISSIBLE when named with a reason (what is
refused is SILENCE); UNDETERMINED is a legitimate verdict on the cause question when its evidence says what
was tried; the no-repair arm grades the CELL'S OWN COMMITS BY AUTHOR (W1-S39); a failed retrieval RAISES
rather than returning the value that passes (CTO residual 1).
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
CELL_AUTHOR = "0.9.0_WK_LGIC_ENFORCE~"
NO_REPAIR_PATHS = ["infra/logic/registry/", "lib/opal_naming.py"]
PLACEHOLDER = re.compile(r"\{[a-z_]+\}")


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
    with open(os.path.join(HERE, "R13_BASE.json"), encoding="utf-8") as fh:
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


def count_report(path):
    """Re-count the placeholder rows in the cell's OWN report. Returns (rows, with_placeholder, tokens)."""
    p = path if os.path.isabs(path) else os.path.join(REPO, path)
    if not os.path.exists(p):
        raise InstrumentFailure("the report named by the record does not exist: %s" % path)
    with open(p, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    rows = [ln for ln in text.split("\n") if ln.startswith("|") and not set(ln) <= set("|- ")]
    hit, tokens = [], {}
    for ln in rows:
        found = PLACEHOLDER.findall(ln)
        if found:
            hit.append(ln)
            for tok in set(found):
                tokens[tok] = tokens.get(tok, 0) + 1
    return len(rows), len(hit), tokens


# ------------------------------------------------------------------ cores
def core_population(rows, with_ph, rec):
    pop = ((rec or {}).get("population") or {})
    d = ((rec or {}).get("delta_against_the_inherited_figure") or {})
    lines = ["report rows re-counted by THIS arm: %d (denominator)" % rows,
             "rows carrying a placeholder, re-counted: %d" % with_ph,
             "record claims: %s of %s" % (_scrub(pop.get("rows_with_a_placeholder")), _scrub(pop.get("judged_rows")))]
    bad = []
    if pop.get("rows_with_a_placeholder") != with_ph:
        bad.append("RECORD DISAGREES WITH THE ARTIFACT IT PRODUCED")
    if not (pop.get("registry_vintage") or "").strip():
        bad.append("no registry_vintage: a census figure without its vintage is not a measurement")
    if not (pop.get("measured_at") or "").strip():
        bad.append("no measured_at")
    if d.get("now") is not None and d.get("now") != with_ph:
        bad.append("the delta block's `now` disagrees with the re-count")
    if not (d.get("inherited_vintage") or "").strip():
        bad.append("the delta names no vintage for the INHERITED figure -- both vintages or it is not a delta")
    if d.get("direction") not in (None, "GREW", "SHRANK", "UNCHANGED"):
        bad.append("direction is not one of GREW/SHRANK/UNCHANGED")
    return (not bad), lines + bad


def core_tokens(tokens_measured, rec):
    tk = ((rec or {}).get("tokens") or {})
    by = tk.get("by_token") or []
    named = {e.get("token"): e.get("rows") for e in by if isinstance(e, dict)}
    lines = ["distinct placeholder tokens re-counted: %d %s" % (len(tokens_measured), _scrub(sorted(tokens_measured))),
             "record names: %d (claims distinct=%s)" % (len(by), _scrub(tk.get("distinct")))]
    bad = []
    if tk.get("distinct") is not None and tk.get("distinct") != len(by):
        bad.append("`distinct` disagrees with the by_token list")
    missing = sorted(set(tokens_measured) - set(named))
    invented = sorted(set(named) - set(tokens_measured))
    if missing:
        bad.append("TOKENS IN THE REPORT AND NOT IN THE RECORD: %s" % _scrub(missing[:5]))
    if invented:
        bad.append("TOKENS NAMED BUT NOT IN THE REPORT: %s" % _scrub(invented[:5]))
    return (not bad), lines + bad


def core_producers(tokens_measured, rec):
    pr = ((rec or {}).get("producers") or {})
    by = pr.get("by_producer") or []
    attributed, bad = set(), []
    for e in by:
        if not (e.get("producer") or "").strip() or not (e.get("how_it_was_attributed") or "").strip():
            bad.append("a by_producer entry lacks producer or how_it_was_attributed")
        attributed |= set(e.get("tokens") or [])
    un = ((rec or {}).get("unattributed") or {})
    un_tokens = set(un.get("tokens") or [])
    if un_tokens and not (un.get("why") or "").strip():
        bad.append("unattributed tokens listed with no `why`")
    silent = sorted(set(tokens_measured) - attributed - un_tokens)
    lines = ["producers named: %d (record states %s)" % (len(by), _scrub(pr.get("count"))),
             "tokens attributed: %d | unattributed WITH a reason: %d" % (len(attributed), len(un_tokens)),
             "tokens in NEITHER list: %d" % len(silent)]
    if silent:
        bad.append("SILENT TOKENS: %s" % _scrub(silent[:5]))
    if pr.get("count") is not None and pr.get("count") != len(by):
        bad.append("producer COUNT disagrees with the by_producer list")
    return (not bad), lines + bad


def core_cause(rec):
    """UNDETERMINED is a legitimate verdict -- with evidence saying what was tried and what it could not settle."""
    c = ((rec or {}).get("one_cause_or_several") or {})
    v, ev = c.get("verdict"), (c.get("evidence") or "").strip()
    lines = ["verdict: %s" % _scrub(v), "evidence length: %d" % len(ev)]
    if v not in ("ONE", "SEVERAL", "UNDETERMINED"):
        return False, lines + ["verdict must be ONE, SEVERAL or UNDETERMINED"]
    if not ev:
        return False, lines + ["a verdict with no evidence is an assumption -- including UNDETERMINED"]
    return True, lines


def core_no_repair(own, foreign):
    lines = ["registry/builder commits since the cut: %d by THIS CELL, %d elsewhere (EXCUSED)"
             % (len(own), len(foreign))]
    lines += ["    THIS CELL MOVED: %s" % _scrub(c) for c in own[:4]]
    lines += ["    excused: %s" % _scrub(c) for c in foreign[:3]]
    return (not own), lines


def core_vintage(rec, resolvable):
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    want = {"check_en_r13.py", "R13_BASE.json"}
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
    if prior - named:
        lines.append("AT RISK AND NOT RE-RUN: %s" % _scrub(sorted(prior - named)[:3]))
    return named == prior, lines


def _is_this_round(path, tag="r13"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    oldest = commits[-1].split()[0]
    out = git(["ls-tree", "-r", "--name-only", "%s^" % oldest, "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def _rec():
    return load_json(base()["record_shape"]["paths"]["EN-p-37"])


def _report_counts(rec):
    path = ((rec or {}).get("population") or {}).get("report_path")
    if not path:
        raise InstrumentFailure("the record names no report_path -- the arm cannot re-count what it cannot find")
    return count_report(path)


def p37_population():
    rec = _rec()
    try:
        rows, with_ph, _t = _report_counts(rec)
    except InstrumentFailure as exc:
        return say("FAIL-P37-POPULATION", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    ok, lines = core_population(rows, with_ph, rec)
    return verdict(ok, "PASS-P37-POPULATION", "FAIL-P37-POPULATION",
                   ["this arm grades the record against the CELL'S OWN REPORT, never against the live plane"] + lines)


def p37_tokens():
    rec = _rec()
    try:
        _r, _w, tokens = _report_counts(rec)
    except InstrumentFailure as exc:
        return say("FAIL-P37-TOKENS", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    ok, lines = core_tokens(tokens, rec)
    return verdict(ok, "PASS-P37-TOKENS", "FAIL-P37-TOKENS", lines)


def p37_producers():
    rec = _rec()
    try:
        _r, _w, tokens = _report_counts(rec)
    except InstrumentFailure as exc:
        return say("FAIL-P37-PRODUCERS", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    ok, lines = core_producers(tokens, rec)
    return verdict(ok, "PASS-P37-PRODUCERS", "FAIL-P37-PRODUCERS", lines)


def p37_cause():
    ok, lines = core_cause(_rec())
    return verdict(ok, "PASS-P37-CAUSE", "FAIL-P37-CAUSE", lines)


def p37_no_repair():
    b = base()
    try:
        out = git(["log", "--format=%h %an %s", "%s..HEAD" % b["cut_pin"], "--"] + NO_REPAIR_PATHS)
    except InstrumentFailure as exc:
        return say("FAIL-P37-NO-REPAIR", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    rows = [ln for ln in out.splitlines() if ln.strip()]
    own = [ln for ln in rows if CELL_AUTHOR in ln]
    ok, lines = core_no_repair(own, [ln for ln in rows if CELL_AUTHOR not in ln])
    return verdict(ok, "PASS-P37-NO-REPAIR", "FAIL-P37-NO-REPAIR", lines)


def r13_vintage_field():
    rec = _rec()
    fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
    resolvable = True
    for path, commit in fx.items():
        try:
            git(["cat-file", "-e", "%s:%s" % (commit, path)])
        except InstrumentFailure:
            resolvable = False
    ok, lines = core_vintage(rec, resolvable)
    return verdict(ok, "PASS-R13-VINTAGE-FIELD", "FAIL-R13-VINTAGE-FIELD", lines)


def r13_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R13-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    ok, lines = core_stale(commits, _rec(), prior)
    return verdict(ok, "PASS-R13-STALE-PROOFS", "FAIL-R13-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _correct():
    return {"population": {"judged_rows": 3000, "rows_with_a_placeholder": 2, "registry_vintage": "9f4a569d",
                           "measured_at": "2026-09-19T08:00Z", "report_path": "x/report.md"},
            "delta_against_the_inherited_figure": {"inherited": 1411, "inherited_vintage": "round-4 census",
                                                   "now": 2, "direction": "SHRANK"},
            "tokens": {"distinct": 1, "by_token": [{"token": "{system}", "rows": 2}]},
            "producers": {"count": 1, "by_producer": [{"producer": "lib/opal_naming.py:900",
                                                       "tokens": ["{system}"],
                                                       "how_it_was_attributed": "instrumented name() and re-ran"}]},
            "unattributed": {"tokens": [], "why": ""},
            "one_cause_or_several": {"verdict": "ONE", "evidence": "every row's token is {system} from one site"},
            "fixed_inputs_at_pin": {"a/check_en_r13.py": "abc", "b/R13_BASE.json": "abc"},
            "stale_proofs": {"fixed_input_commits_since_cut": 1, "proofs_re_run": []}}


def selftest_arms():
    good, toks = _correct(), {"{system}": 2}

    arm("POSITIVE-BAR-correct-record-satisfies-population", core_population(3000, 2, good)[0],
        "the CTO's cut-time bar, exercised rather than promised")
    arm("POSITIVE-BAR-correct-record-satisfies-tokens", core_tokens(toks, good)[0])
    arm("POSITIVE-BAR-correct-record-satisfies-producers", core_producers(toks, good)[0])
    arm("POSITIVE-BAR-correct-record-satisfies-cause", core_cause(good)[0])
    arm("POSITIVE-BAR-correct-record-satisfies-vintage", core_vintage(good, True)[0])
    arm("POSITIVE-BAR-correct-record-satisfies-stale", core_stale(["a x"], good, set())[0])
    arm("POSITIVE-BAR-correct-record-satisfies-no-repair", core_no_repair([], ["x 1.0.0_SA_CTO y"])[0])

    arm("MUTANT-population-record-disagrees-with-its-own-report", not core_population(3000, 5, good)[0])
    arm("MUTANT-population-no-registry-vintage", not core_population(3000, 2, dict(
        good, population=dict(good["population"], registry_vintage="")))[0],
        "a census figure without its vintage is not a measurement")
    arm("MUTANT-population-delta-without-inherited-vintage", not core_population(3000, 2, dict(
        good, delta_against_the_inherited_figure={"inherited": 1411, "now": 2}))[0],
        "both vintages or it is not a delta")

    arm("MUTANT-tokens-missing-a-measured-token", not core_tokens({"{system}": 2, "{scope}": 1}, good)[0])
    arm("MUTANT-tokens-invented", not core_tokens({}, good)[0])
    arm("MUTANT-tokens-distinct-disagrees", not core_tokens(toks, dict(
        good, tokens={"distinct": 3, "by_token": good["tokens"]["by_token"]}))[0])

    arm("POSITIVE-producers-unattributed-with-a-reason", core_producers({"{x}": 1}, dict(
        good, producers={"count": 0, "by_producer": []},
        unattributed={"tokens": ["{x}"], "why": "no call site reachable from the served graph"}))[0],
        "a cell that cannot attribute says so WITHOUT fabricating a producer")
    arm("MUTANT-producers-silent-token", not core_producers({"{x}": 1}, dict(
        good, producers={"count": 0, "by_producer": []}, unattributed={"tokens": [], "why": ""}))[0])
    arm("MUTANT-producers-no-instrument", not core_producers(toks, dict(
        good, producers={"count": 1, "by_producer": [{"producer": "p", "tokens": ["{system}"],
                                                      "how_it_was_attributed": ""}]}))[0])

    arm("POSITIVE-cause-undetermined-with-evidence", core_cause(
        {"one_cause_or_several": {"verdict": "UNDETERMINED", "evidence": "two sites reach it; neither excluded"}})[0],
        "UNDETERMINED is a legitimate verdict -- forcing ONE or SEVERAL is how a cell invents a cause")
    arm("MUTANT-cause-no-evidence", not core_cause({"one_cause_or_several": {"verdict": "ONE", "evidence": ""}})[0])
    arm("MUTANT-cause-bad-verdict", not core_cause({"one_cause_or_several": {"verdict": "PROBABLY", "evidence": "x"}})[0])

    arm("MUTANT-no-repair-own-commit", not core_no_repair(["a 0.9.0_WK_LGIC_ENFORCE~1 moved the registry"], [])[0])
    arm("MUTANT-vintage-absent", not core_vintage({}, True)[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(good, False)[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(
        good, stale_proofs={"proofs_re_run": ["never.proof_of_spec.json"]}), set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_ENFORCE.TO-EN-p-37-r13.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_ENFORCE.TO-EN-t-45-r12.x.proof_of_spec.json"))

    try:
        proofs_at_risk(["deadbeefdeadbeef no-such-commit"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True, "a failed retrieval RAISES (residual 1)")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-P37-TOKENS"))

    bad = [n for n, ok, _ in _ARMS if not ok]
    pos = len([n for n, _, _ in _ARMS if n.startswith("POSITIVE")])
    for n, ok, note in _ARMS:
        print("  %-54s %-4s %s" % (n, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(_ARMS), pos, len(_ARMS) - pos))
    print("  NOT driven here, stated: the report read and the git calls -- live, exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"p37-population": p37_population, "p37-tokens": p37_tokens, "p37-producers": p37_producers,
        "p37-cause": p37_cause, "p37-no-repair": p37_no_repair, "r13-vintage-field": r13_vintage_field,
        "r13-stale-proofs": r13_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
