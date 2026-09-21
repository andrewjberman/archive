"""LGIC_ENFORCE ROUND 11 -- the fixed input. One cell (EN-t-44), five arms.

Round 10 fixed grade() and wrote a test that would pass the very substitution its judgment criterion
existed to rule out (S86). Round 11 promotes 3.0.0_SA_CVO's own L9 probe into the suite and carries S87's
unobservable branch AT ITS SITE. The analysis is explicit that this is not new test design: the inputs
exist, the expectation is measured, the run has happened.

THE ARM THAT MATTERS IS THE MUTANT. A probe test that only ever runs against the REAL grade() proves the
two names render correctly and nothing else. `t44-mutant` swaps in a KEYED SUBSTITUTION -- the cheapest
wrong fix, which rewrites the census instance and leaves every other name raw -- and REQUIRES each probe
test to fail against it. Without that, the promotion is a green carrying no information, which is the
defect S86 names one level up.

AND THIS ROUND CARRIES THE ROUND-10 ANALYSIS'S STALE-PROOF BAR as `t44-stale-proofs`: a fixed input that
moves mid-round leaves every proof pinned before it STALE-UNGRADED. The discriminator is one git log that
usually returns zero, so the bar costs nothing when nothing moved -- and it is the only instrument that
sees the OVERSTATE mirror, where a regressed input leaves a proof reading PASS while the arm now FAILS.
"""

import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
BASEFILE = os.path.join(HERE, "R11_BASE.json")
SUITE = "lib/tests/test_opal_naming.py"
FENCE = re.compile("```json" + "\n" + "(.*?)" + "\n" + "```", re.S)
ORDER_SHAPE = re.compile(r"RECORD SHAPE[^\n]*\n+```json\n(.*?)\n```", re.S)


def _scrub(t):
    return str(t).replace("VERDICT", "VERD1CT").replace("PASS-", "PASS_").replace("FAIL-", "FAIL_")


def say(tag, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + tag)
    return 0


def verdict(ok, p, f, lines):
    return say(p if ok else f, *lines)


def base():
    with open(BASEFILE, encoding="utf-8") as fh:
        return json.load(fh)


def load_json(p):
    try:
        with open(os.path.join(REPO, p), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def naming():
    sys.path.insert(0, os.path.join(REPO, "lib"))
    try:
        import opal_naming as on  # noqa: E402
        return on
    finally:
        sys.path.pop(0)


def suite_text():
    try:
        with open(os.path.join(REPO, SUITE), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def test_module():
    """Import the suite as a module so its test functions can be CALLED against a mutant."""
    sys.path.insert(0, os.path.join(REPO, "lib"))
    sys.path.insert(0, os.path.join(REPO, os.path.dirname(SUITE)))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("t_on_r11", os.path.join(REPO, SUITE))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    except Exception as exc:  # a suite that cannot import is a FAIL, never a pass
        return exc
    finally:
        sys.path.pop(0)
        sys.path.pop(0)


def probe_tests(mod, names):
    """-> {probe name: [test function names whose SOURCE carries it]}"""
    import inspect
    out = {n: [] for n in names}
    for attr in dir(mod):
        if not attr.startswith("test_"):
            continue
        fn = getattr(mod, attr)
        if not callable(fn):
            continue
        try:
            src = inspect.getsource(fn)
        except (OSError, TypeError):
            continue
        for n in names:
            if n in src:
                out[n].append(attr)
    return out


def run_pytest():
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-rf", "--color=no", "-p", "no:cacheprovider", SUITE],
                       cwd=REPO, capture_output=True, timeout=900)
    txt = (p.stdout or b"").decode("utf-8", "replace")
    ids = [re.sub(r" - .*$", "", ln[len("FAILED "):]).strip() for ln in txt.splitlines() if ln.startswith("FAILED ")]
    tail = [ln for ln in txt.splitlines() if re.search(r"\d+ (passed|failed)", ln)]
    return ids, (tail[-1] if tail else "no summary line")


# ------------------------------------------------------------------ cores
def core_probes(found, names, renders, expected):
    bad = [n for n in names if not found.get(n)]
    wrong = ["%s -> %s" % (_scrub(n), _scrub(renders.get(n))) for n in names if renders.get(n) != expected]
    lines = ["probe %s: test(s) %s ; renders %s" % (_scrub(n), _scrub(found.get(n) or "NONE"), _scrub(renders.get(n)))
             for n in names]
    if bad:
        lines.append("probes with no test asserting them: %s" % _scrub(bad))
    if wrong:
        lines.append("probes whose render is not the expected one: %s" % _scrub(wrong))
    return (not bad and not wrong and len(names) > 0), lines


def core_mutant(failures, found, names):
    """Every probe test must FAIL under the keyed substitution."""
    expected = sorted({t for n in names for t in found.get(n, [])})
    failed = sorted(failures)
    missing = [t for t in expected if t not in failed]
    lines = ["probe test(s) driven against the keyed-substitution mutant: %d" % len(expected),
             "failed under the mutant: %d %s" % (len(failed), _scrub(failed))]
    if missing:
        lines.append("DID NOT FAIL under the mutant (a test that cannot catch the wrong fix): %s" % _scrub(missing))
    return (bool(expected) and not missing), lines


def core_comment(src, needles):
    miss = [n for n in needles if n.lower() not in src.lower()]
    return (not miss), "comment at the site carries %d of %d required references%s" % (
        len(needles) - len(miss), len(needles), ("; missing " + _scrub(miss)) if miss else "")


def core_tests(now, baseline):
    new = sorted(set(now) - set(baseline))
    gone = sorted(set(baseline) - set(now))
    return (not new and not gone), "failing now %d, baseline %d, NEW %d, silenced %d%s" % (
        len(now), len(baseline), len(new), len(gone), ("; NEW=" + _scrub(new)) if new else "")


def core_stale(commits, record):
    """The round-10 analysis's bar: a fixed input that moved mid-round leaves pinned proofs stale."""
    n = len(commits)
    if n == 0:
        return True, ["fixed input commits since the cut: 0 -- no proof can be stale against it"]
    rec = ((record or {}).get("stale_proofs") or {})
    listed = rec.get("proofs_re_run") or []
    ok = rec.get("fixed_input_commits_since_cut") == n and len(listed) > 0
    return ok, ["fixed input commits since the cut: %d (%s)" % (n, _scrub(commits[:3])),
                "record enumerates %d re-run proof(s) and claims %s commit(s)"
                % (len(listed), _scrub(rec.get("fixed_input_commits_since_cut")))]


# ------------------------------------------------------------------ arms
def t44_probes():
    b = base()
    mod = test_module()
    if isinstance(mod, Exception):
        return say("FAIL-T44-PROBES", "the suite does not import: %s" % _scrub(mod))
    on = naming()
    names = b["probes"]["names"]
    renders = {n: on.grade(n, b["probes"]["node_type"])[1] for n in names}
    ok, lines = core_probes(probe_tests(mod, names), names, renders, b["probes"]["expected_render"])
    return verdict(ok, "PASS-T44-PROBES", "FAIL-T44-PROBES", lines)


def t44_mutant():
    b = base()
    mod = test_module()
    if isinstance(mod, Exception):
        return say("FAIL-T44-MUTANT", "the suite does not import: %s" % _scrub(mod))
    on = naming()
    names = b["probes"]["names"]
    found = probe_tests(mod, names)
    inst = b["probes"]["census_instance_for_contrast"]
    real = on.grade

    def keyed(name, node_type):
        """THE CHEAPEST WRONG FIX: rewrite the census instance, leave every other name as it was."""
        if name == inst["name"]:
            return real(name, node_type)
        v, c = real(name, node_type)
        return v, c.replace("blackdiamond", "bd")

    failures = []
    on.grade = keyed
    try:
        for t in sorted({t for n in names for t in found.get(n, [])}):
            try:
                getattr(mod, t)()
            except Exception:
                failures.append(t)
    finally:
        on.grade = real
    ok, lines = core_mutant(failures, found, names)
    return verdict(ok, "PASS-T44-MUTANT", "FAIL-T44-MUTANT", lines)


def t44_comment():
    on = naming()
    import inspect
    try:
        src = inspect.getsource(on._r3_spell)
    except (AttributeError, OSError, TypeError) as exc:
        return say("FAIL-T44-COMMENT", "cannot read _r3_spell: %s" % _scrub(exc))
    ok, line = core_comment(src, ["S87", "FN1b", "observ"])
    return verdict(ok, "PASS-T44-COMMENT", "FAIL-T44-COMMENT",
                   [line, "(the branch itself is NOT removed -- %d line(s) of source read)" % len(src.split("\n"))])


def t44_tests():
    b = base()
    ids, summary = run_pytest()
    if "passed" not in summary and "failed" not in summary:
        return say("FAIL-T44-TESTS", "the suite did not run: %s" % _scrub(summary))
    ok, line = core_tests(ids, b["suite_baseline"]["failing_ids"])
    return verdict(ok, "PASS-T44-TESTS", "FAIL-T44-TESTS", ["suite: " + _scrub(summary), line])


def t44_stale_proofs():
    b = base()
    out = []
    for p in b["stale_proof_bar"]["watched_paths"]:
        r = subprocess.run(["git", "log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--", p],
                           cwd=REPO, capture_output=True, timeout=120)
        out += [ln for ln in (r.stdout or b"").decode("utf-8", "replace").splitlines() if ln.strip()]
    ok, lines = core_stale(out, load_json(b["record_shape"]["path"]))
    return verdict(ok, "PASS-T44-STALE-PROOFS", "FAIL-T44-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
def selftest_arms():
    b = base()
    res = []

    def arm(n, ok, why=""):
        res.append((n, bool(ok), why))

    names = b["probes"]["names"]
    exp = b["probes"]["expected_render"]
    good = {n: ["test_r3_probe"] for n in names}
    renders = {n: exp for n in names}
    arm("POSITIVE-probes", core_probes(good, names, renders, exp)[0], "both probes asserted and rendering")
    arm("MUTANT-probes-missing-test", not core_probes({names[0]: ["t"], names[1]: []}, names, renders, exp)[0])
    arm("MUTANT-probes-wrong-render", not core_probes(good, names, {names[0]: exp, names[1]: "x"}, exp)[0])
    arm("POSITIVE-mutant", core_mutant(["test_r3_probe"], good, names)[0], "the probe test fails under the mutant")
    arm("MUTANT-mutant-survives", not core_mutant([], good, names)[0], "a test the wrong fix passes -> FAIL")
    arm("POSITIVE-comment", core_comment("# unobservable today; FN1b subtracts it; see S87", ["S87", "FN1b", "observ"])[0])
    arm("MUTANT-comment-partial", not core_comment("# see S87", ["S87", "FN1b", "observ"])[0])
    bl = b["suite_baseline"]["failing_ids"]
    arm("POSITIVE-tests", core_tests(list(bl), bl)[0])
    arm("MUTANT-tests-new", not core_tests(list(bl) + ["x::new"], bl)[0])
    arm("MUTANT-tests-silenced", not core_tests(bl[:1], bl)[0])
    arm("POSITIVE-stale-none", core_stale([], None)[0], "no fixed-input commit -> nothing can be stale")
    rec = {"stale_proofs": {"fixed_input_commits_since_cut": 1, "proofs_re_run": ["x.proof_of_spec.json"]}}
    arm("POSITIVE-stale-enumerated", core_stale(["abc fix"], rec)[0], "moved AND enumerated")
    arm("MUTANT-stale-unenumerated", not core_stale(["abc fix"], None)[0], "moved and NOT enumerated -> FAIL")
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-T44-PROBES"))

    want = b["record_shape"]["shape"]
    orders = sorted(glob.glob(os.path.join(REPO, ROOT, "task-orders", "LGIC_ENFORCE.TO-EN-*-r11.*.md")))
    quoting = 0
    for op in orders:
        with open(op, encoding="utf-8") as fh:
            m = ORDER_SHAPE.search(fh.read())
        if m:
            quoting += 1
            try:
                got = json.loads(m.group(1))
            except ValueError:
                got = None
            arm("S85-order-quotes-carrier:" + os.path.basename(op)[len("LGIC_ENFORCE.TO-"):][:18], got == want)
    arm("S85-every-order-quotes", quoting == len(orders), "%d of %d round-11 order(s)" % (quoting, len(orders)))

    for n, ok, why in res:
        print("  %-38s %s  %s" % (n, "PASS" if ok else "FAIL", _scrub(why)))
    pos = sum(1 for n, _o, _w in res if n.startswith("POSITIVE-"))
    print("arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(res), pos, len(res) - pos))
    print("NOT driven here, stated: the pytest run, grade() and the git log -- live calls with no fixture, "
          "exercised by the real arms, which print their own denominators.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if all(o for _n, o, _w in res) else "FAIL-ARMS-DO-NOT-DISCRIMINATE"))
    return 0


CMDS = {"t44-probes": t44_probes, "t44-mutant": t44_mutant, "t44-comment": t44_comment,
        "t44-tests": t44_tests, "t44-stale-proofs": t44_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
