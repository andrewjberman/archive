"""LGIC_ENFORCE round 12 -- the arms for EN-t-45.

THE ROUND'S QUESTION IS REACHABILITY, NOT SUBTLETY. Round 11 asked whether a test catches the
CHEAPEST WRONG FIX and answered it by mutating the real suite. That answer exposed a second-order
fact (1.0.0_SA_CTO @84b02d1573): the other tests hold a PRIVATE BY-PATH COPY of the library, so a
substitution of the module the estate actually imports never reaches them. They are not resistant
to a mutant -- THEY NEVER SEE IT -- and a green that no substitution can move is not weak evidence
about the predicate, it is NO evidence.

So the mutant here is BLUNT BY DESIGN: spell `blackdiamond` back to `bd` everywhere. Against a
suite that binds like a consumer it is lethal and obvious; against the suite as it stands at the
cut it changes nothing, and THAT is the measurement. A subtle mutant would confound the two
questions.

Every arm prints its DENOMINATOR. `selftest-arms` drives every core, including
POSITIVE-SATISFIABILITY arms a correct record must pass, and one LIVE positive control of the
failure path -- because a checker whose failure path returns the passing value is the defect this
round's own fixed input was repaired for (residual (1), @eda1e967d0).
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
TESTS = os.path.join(REPO, "lib", "tests", "test_opal_naming.py")
ROUND10_TEST = "test_r3_bd_left_in_the_function_is_spelled_blackdiamond"


def _scrub(t):
    """No verdict token from graded material can reach this output as a bare word."""
    return str(t).replace("VERDICT:", "verdict-").replace("PASS-", "pass-").replace("FAIL-", "fail-")


def say(tag, *lines):
    for ln in lines:
        print("  %s" % ln)
    print("VERDICT: %s" % tag)
    return 0


def verdict(ok, p, f, lines):
    return say(p if ok else f, *lines)


def base():
    with open(os.path.join(HERE, "R12_BASE.json"), encoding="utf-8") as fh:
        return json.load(fh)


def load_json(rel):
    p = rel if os.path.isabs(rel) else os.path.join(REPO, rel)
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def tests_text():
    with open(TESTS, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------ cores
def core_binding(text):
    """Per test: does it reach the BY-PATH copy, or resolve the shipped module at call time?

    The denominator is every `def test_*` in the module, and the two buckets are measured from the
    function's own body -- never from a count someone wrote down.
    """
    names = re.findall(r"^def (test_\w+)\(", text, re.M)
    by_path, consumer = [], []
    for n in names:
        m = re.search(r"^def %s\(.*?(?=^def |\Z)" % re.escape(n), text, re.S | re.M)
        body = m.group(0) if m else ""
        if re.search(r"\bon\.\w+\s*\(", body):
            by_path.append(n)
        if re.search(r"sys\.modules\.get\(\s*[\"']opal_naming[\"']|_shipped_\w+\s*\(", body):
            consumer.append(n)
    return names, by_path, consumer


def core_binding_ok(names, by_path, rec):
    """Every test reaches the shipped module, EXCEPT residuals the record NAMES with a reason."""
    b = ((rec or {}).get("binding") or {})
    named = {r.get("test"): (r.get("why_it_must_keep_the_by_path_copy") or "").strip()
             for r in (b.get("residuals") or []) if isinstance(r, dict)}
    unexplained = [n for n in by_path if not named.get(n)]
    lines = ["tests in module: %d (denominator)" % len(names),
             "still reaching the by-path copy: %d" % len(by_path),
             "residuals NAMED with a reason in the record: %d" % len([k for k, v in named.items() if v])]
    if unexplained:
        lines.append("UNEXPLAINED (a residual is named with its reason or it is not a residual): %s"
                     % _scrub(sorted(unexplained)[:6]))
    claimed_after = b.get("reached_the_by_path_copy_after")
    if claimed_after is not None and claimed_after != len(by_path):
        lines.append("RECORD DISAGREES WITH THE MEASUREMENT: record says %s, measured %d"
                     % (_scrub(claimed_after), len(by_path)))
        return False, lines
    return (not unexplained), lines


def core_suite(before_ids, after_ids):
    """The two hand-stale worked cases are out of scope; the bar is an IDENTICAL failing set."""
    b, a = sorted(before_ids), sorted(after_ids)
    lines = ["baseline failing ids: %d" % len(b), "current failing ids: %d" % len(a)]
    if b != a:
        lines.append("NEW failures: %s" % _scrub(sorted(set(a) - set(b))[:5]))
        lines.append("DISAPPEARED: %s" % _scrub(sorted(set(b) - set(a))[:5]))
    return b == a, lines


def core_mutation(shipped_failing, mutant_failing, baseline_ids, rec):
    """A mutant that reaches the suite KILLS tests. Zero kills is the defect, not a pass."""
    killed = sorted(set(mutant_failing) - set(shipped_failing))
    r10 = [k for k in killed if ROUND10_TEST in k]
    m = ((rec or {}).get("mutation") or {})
    claimed = sorted(m.get("killed_by_the_keyed_mutant") or [])
    lines = ["as shipped, failing: %d (baseline %d)" % (len(shipped_failing), len(baseline_ids)),
             "under the mutant, failing: %d" % len(mutant_failing),
             "KILLED BY THE MUTANT (the measurement): %d" % len(killed),
             "the round-10 test among them: %s" % bool(r10),
             "record claims %d killed" % len(claimed)]
    if not killed:
        lines.append("ZERO KILLS: the substitution did not reach a single test -- unmutatable by construction")
        return False, lines
    if not r10:
        lines.append("the round-10 test SURVIVED: it still holds a copy no substitution reaches")
        return False, lines
    if claimed and set(claimed) != set(killed):
        lines.append("RECORD DISAGREES: claimed-not-measured %s | measured-not-claimed %s"
                     % (_scrub(sorted(set(claimed) - set(killed))[:4]),
                        _scrub(sorted(set(killed) - set(claimed))[:4])))
        return False, lines
    return True, lines


def core_note(text):
    """The hazard is named AT THE SITE a reader opens, not only in a channel row."""
    want = ["by-path", "consumer", "S90"]
    missing = [w for w in want if w.lower() not in text.lower()]
    return (not missing), ["note tokens required: %s" % _scrub(want),
                           "missing: %s" % (_scrub(missing) if missing else "none")]


class InstrumentFailure(RuntimeError):
    """AN EXCEPTION IS NOT AN EMPTY SET (CTO residual (1) @84b02d1573).

    EMPTY is the value that PASSES at a mint, so a failed retrieval that answers `set()` is
    indistinguishable from a clean mint -- in the one direction that produces a green.
    """


def _is_this_round(path, tag):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    oldest = commits[-1].split()[0]
    tag = os.path.basename(HERE)
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", "%s^" % oldest, "--", ROOT],
                       cwd=REPO, capture_output=True, timeout=120)
    if r.returncode != 0:
        raise InstrumentFailure("git ls-tree %s^ rc=%d: %s" % (
            oldest, r.returncode, (r.stderr or b"").decode("utf-8", "replace").strip()[:200]))
    return set(ln for ln in (r.stdout or b"").decode("utf-8", "replace").splitlines()
               if _is_this_round(ln, tag))


def core_stale(commits, rec, prior):
    """SET EQUALITY against the proofs that could actually be stale. The COUNT is informational.

    Never `len(listed) > 0`: S90 measured that this forces a real path that was NEVER AT RISK when
    the honest answer is zero, so every green it produced was vacuous.
    """
    n = len(commits)
    if n == 0:
        return True, ["fixed-input commits since the cut: 0 -- no proof can be stale against them"]
    sp = ((rec or {}).get("stale_proofs") or {})
    named = set(sp.get("proofs_re_run") or [])
    prior = set(prior or ())
    lines = ["fixed-input commits since the cut: %d (informational, checkout-dependent)" % n,
             "proofs pinned BEFORE the earliest of them: %d" % len(prior),
             "record enumerates: %d" % len(named)]
    if named - prior:
        lines.append("NAMED BUT NEVER AT RISK: %s" % _scrub(sorted(named - prior)[:4]))
    if prior - named:
        lines.append("AT RISK AND NOT RE-RUN: %s" % _scrub(sorted(prior - named)[:4]))
    return named == prior, lines


# ------------------------------------------------------------------ pytest
def _run_pytest(extra_env=None, plugin_dir=None):
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    if plugin_dir:
        env["PYTHONPATH"] = plugin_dir + os.pathsep + env.get("PYTHONPATH", "")
    # `--color=no` AND an escape-stripper: pytest colours FAILED, so `^FAILED` never matches a
    # coloured line and the parse returns ZERO FAILURES from a run that failed. Measured at the
    # cut -- the suite has 2 known failures and this function reported 0 until both were added.
    # A terminal renders the codes invisible, so the wrong answer LOOKS like the right one.
    args = [sys.executable, "-m", "pytest", "lib/tests/test_opal_naming.py", "-q", "--no-header",
            "--color=no", "-p", "no:cacheprovider"]
    if plugin_dir:
        args += ["-p", "r12_mutant"]
    r = subprocess.run(args, cwd=REPO, capture_output=True, timeout=900, env=env)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    out = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", out)
    failing = sorted(set(re.findall(r"^FAILED\s+\S+::(\S+)", out, re.M)))
    if not failing:
        failing = sorted(set(re.findall(r"(?m)^\S+::(\S+)\s+FAILED", out)))
    # THE PARSE CHECKS ITSELF AGAINST PYTEST'S OWN SUMMARY. A regex that silently matches nothing
    # returns an EMPTY list, and empty reads as "nothing failed" -- the same shape as residual (1),
    # one instrument down. If the two disagree the arm raises rather than reporting a clean run.
    m = re.search(r"(\d+) failed", out)
    claimed = int(m.group(1)) if m else 0
    if claimed != len(failing):
        raise InstrumentFailure(
            "pytest's summary says %d failed, the id parse found %d -- the parse is wrong, not the suite"
            % (claimed, len(failing)))
    return failing, out


_PLUGIN = '''import importlib.machinery, importlib.util, os, sys
_ws = os.environ["R12_WS"]
_loader = importlib.machinery.SourceFileLoader("opal_naming", os.path.join(_ws, "lib", "opal_naming.py"))
_spec = importlib.util.spec_from_loader("opal_naming", _loader)
_mod = importlib.util.module_from_spec(_spec)
_loader.exec_module(_mod)
_real = _mod.grade


def _blunt(name, node_type):
    """THE BLUNT MUTANT: spell the vendor back to bd everywhere. Lethal to any test that can SEE it."""
    v, c = _real(name, node_type)
    return v, (c.replace("blackdiamond", "bd") if isinstance(c, str) else c)


_mod.grade = _blunt
sys.modules["opal_naming"] = _mod
'''


def _write_plugin():
    # A TEMP DIR, never the repo: the plugin is a RUN ARTIFACT the checker regenerates every call,
    # and a generated file inside a fixed-input directory is churn a later round would have to
    # explain -- worse, it would land in a worker's `git status` looking like something to commit.
    d = tempfile.mkdtemp(prefix="r12_mutant_")
    with open(os.path.join(d, "r12_mutant.py"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(_PLUGIN)
    return d


# ------------------------------------------------------------------ arms
def t45_binding():
    b = base()
    names, by_path, consumer = core_binding(tests_text())
    rec = load_json(b["record_shape"]["paths"]["EN-t-45"])
    ok, lines = core_binding_ok(names, by_path, rec)
    lines.insert(1, "resolving the shipped module at call time: %d" % len(consumer))
    lines.insert(0, "at the cut this read 38 total / 33 by-path / 2 consumer -- re-measured here, never inherited")
    return verdict(ok, "PASS-T45-BINDING", "FAIL-T45-BINDING", lines)


def t45_suite():
    b = base()
    try:
        failing, _ = _run_pytest()
    except InstrumentFailure as exc:
        return say("FAIL-T45-SUITE", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    ok, lines = core_suite(b["suite_baseline"]["failing_ids"], failing)
    return verdict(ok, "PASS-T45-SUITE", "FAIL-T45-SUITE", lines)


def t45_mutant():
    b = base()
    try:
        shipped, _ = _run_pytest()
        d = _write_plugin()
        mutant, out = _run_pytest(extra_env={"R12_WS": REPO}, plugin_dir=d)
    except InstrumentFailure as exc:
        return say("FAIL-T45-MUTANT", "INSTRUMENT FAILURE: %s" % _scrub(exc))
    if "ImportError" in out or "INTERNALERROR" in out:
        return say("FAIL-T45-MUTANT", "INSTRUMENT FAILURE: the plugin did not load -- %s" % _scrub(out[-200:]))
    rec = load_json(b["record_shape"]["paths"]["EN-t-45"])
    ok, lines = core_mutation(shipped, mutant, b["suite_baseline"]["failing_ids"], rec)
    return verdict(ok, "PASS-T45-MUTANT", "FAIL-T45-MUTANT", lines)


def t45_note():
    ok, lines = core_note(tests_text())
    return verdict(ok, "PASS-T45-NOTE", "FAIL-T45-NOTE", lines)


def t45_stale_proofs():
    b = base()
    args = ["git", "log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
    args += list(b["stale_proof_bar"]["watched_paths"])
    r = subprocess.run(args, cwd=REPO, capture_output=True, timeout=120)
    if r.returncode != 0:
        return say("FAIL-T45-STALE-PROOFS", "INSTRUMENT FAILURE: git log rc=%d" % r.returncode)
    out = [ln for ln in (r.stdout or b"").decode("utf-8", "replace").splitlines() if ln.strip()]
    rec = load_json(b["record_shape"]["paths"]["EN-t-45"])
    try:
        prior = proofs_at_risk(out)
    except InstrumentFailure as exc:
        return say("FAIL-T45-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    ok, lines = core_stale(out, rec, prior)
    return verdict(ok, "PASS-T45-STALE-PROOFS", "FAIL-T45-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def selftest_arms():
    text_bad = "def test_a():\n    on.grade('x', 'LAMBDA')\n\ndef test_b():\n    _shipped_grade()('x', 'L')\n"
    names, by_path, consumer = core_binding(text_bad)
    arm("POSITIVE-binding-splits-the-two-shapes", names == ["test_a", "test_b"] and by_path == ["test_a"]
        and consumer == ["test_b"], "one of each, measured from the bodies")
    arm("POSITIVE-binding-clean", core_binding_ok(["t"], [], {})[0], "nothing by-path is the passing state")
    arm("POSITIVE-binding-residual-named", core_binding_ok(
        ["t"], ["t"], {"binding": {"reached_the_by_path_copy_after": 1,
                                   "residuals": [{"test": "t", "why_it_must_keep_the_by_path_copy": "it tests the loader itself"}]}})[0],
        "a residual NAMED with a reason is admissible")
    arm("MUTANT-binding-residual-unexplained", not core_binding_ok(
        ["t"], ["t"], {"binding": {"residuals": [{"test": "t", "why_it_must_keep_the_by_path_copy": ""}]}})[0],
        "an empty reason is not a reason")
    arm("MUTANT-binding-record-disagrees", not core_binding_ok(
        ["t"], ["t"], {"binding": {"reached_the_by_path_copy_after": 0,
                                   "residuals": [{"test": "t", "why_it_must_keep_the_by_path_copy": "x"}]}})[0],
        "a record claiming 0 against a measured 1 fails")

    arm("POSITIVE-suite-identical", core_suite(["a", "b"], ["b", "a"])[0], "order does not matter")
    arm("MUTANT-suite-new-failure", not core_suite(["a"], ["a", "c"])[0])
    arm("MUTANT-suite-fixed-in-passing", not core_suite(["a", "b"], ["a"])[0],
        "a baseline failure that DISAPPEARS is also a change this round did not authorise")

    rec_ok = {"mutation": {"killed_by_the_keyed_mutant": ["x", ROUND10_TEST]}}
    arm("POSITIVE-mutation-kills-including-r10", core_mutation(
        ["base"], ["base", "x", ROUND10_TEST], ["base"], rec_ok)[0])
    arm("MUTANT-mutation-zero-kills", not core_mutation(["base"], ["base"], ["base"], {})[0],
        "a substitution that reaches nothing is the defect, never a pass")
    arm("MUTANT-mutation-r10-survives", not core_mutation(
        ["base"], ["base", "x"], ["base"], {"mutation": {"killed_by_the_keyed_mutant": ["x"]}})[0])
    arm("MUTANT-mutation-record-disagrees", not core_mutation(
        ["base"], ["base", "x", ROUND10_TEST], ["base"], {"mutation": {"killed_by_the_keyed_mutant": ["x"]}})[0])

    arm("POSITIVE-note-present", core_note("holds a by-path copy; a consumer sees the shipped one. S90.")[0])
    arm("MUTANT-note-missing-token", not core_note("some unrelated docstring")[0])

    arm("POSITIVE-stale-none", core_stale([], None, set())[0])
    arm("POSITIVE-stale-mint", core_stale(
        ["abc mint"], {"stale_proofs": {"proofs_re_run": []}}, set())[0],
        "a mint puts NO proof at risk -- [] is the honest answer (S88/S90)")
    arm("MUTANT-stale-invented", not core_stale(
        ["abc x"], {"stale_proofs": {"proofs_re_run": ["never/existed.proof_of_spec.json"]}}, set())[0],
        "the shape S90 falsified: a real path that was never at risk cannot buy a PASS")
    arm("MUTANT-stale-unenumerated", not core_stale(
        ["abc x"], {"stale_proofs": {"proofs_re_run": []}}, {"a/p.proof_of_spec.json"})[0])
    arm("POSITIVE-stale-count-moves", core_stale(
        ["a x", "b y", "c z"], {"stale_proofs": {"fixed_input_commits_since_cut": 1, "proofs_re_run": []}},
        set())[0], "a record whose checkout counted 1 against a tree counting 3 still passes: the SET is the bar")
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_ENFORCE.TO-EN-t-45-r12.x.proof_of_spec.json", "r12"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_ENFORCE.TO-EN-t-44-r11.x.proof_of_spec.json", "r12"),
        "an r11 proof is frozen history (R-43): an r12 edit cannot make it stale")

    try:
        proofs_at_risk(["deadbeefdeadbeef no-such-commit"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "it returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True,
            "a failed retrieval RAISES; it does not return the value that passes (CTO residual (1))")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-T45-BINDING"))

    bad = [n for n, ok, _ in _ARMS if not ok]
    pos = len([n for n, _, _ in _ARMS if n.startswith("POSITIVE")])
    for n, ok, note in _ARMS:
        print("  %-42s %-4s %s" % (n, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(_ARMS), pos, len(_ARMS) - pos))
    print("  NOT driven here, stated: the two pytest runs and the git reads -- live calls with no fixture,")
    print("  exercised by the real arms, which print their own denominators.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"t45-binding": t45_binding, "t45-suite": t45_suite, "t45-mutant": t45_mutant,
        "t45-note": t45_note, "t45-stale-proofs": t45_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
