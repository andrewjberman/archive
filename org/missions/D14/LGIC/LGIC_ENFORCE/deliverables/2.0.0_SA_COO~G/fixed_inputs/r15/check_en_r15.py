"""LGIC_ENFORCE round 15 -- the retired-discriminator sweep.

1.0.0_SA_CTO @7761d31eaf: "ITS ACCEPTANCE ARM IS A POSITIVE CONTROL: each re-pointed instrument must
still return round 13's 1303 on the raw rows -- because A ZERO IS EXACTLY WHAT A BROKEN ONE WILL REPORT."

That sentence is the whole design. Every instrument in this sweep fails by returning a CLEAN,
DENOMINATOR-BEARING ZERO: it does not error, it does not warn, IT AGREES WITH ITSELF. So no arm here
accepts "the instrument ran and reported a number" -- the re-pointed ones must report THE NUMBER.

Carried forward from S106: no arm reads a second cell's record, and the round-wide arms grade the
records PRESENT IN THIS CHECKOUT, refusing an EMPTY population rather than passing it vacuously.
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
CELLS = ("EN-d-1",)
DISPOSITIONS = ("RE-POINTED", "RETIRED", "UNAFFECTED")
CONTROL_VALUE = 1303


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
    with open(os.path.join(HERE, "R15_BASE.json"), encoding="utf-8") as fh:
        return json.load(fh)


class InstrumentFailure(RuntimeError):
    """An exception is not an empty set: EMPTY is the value that PASSES at a mint."""


def git(args, timeout=120):
    r = subprocess.run(["git"] + args, cwd=REPO, capture_output=True, timeout=timeout)
    if r.returncode != 0:
        raise InstrumentFailure("git %s rc=%d: %s" % (args[0], r.returncode,
                                                      (r.stderr or b"").decode("utf-8", "replace")[:160]))
    return (r.stdout or b"").decode("utf-8", "replace")


def _rec(cell):
    p = os.path.join(REPO, base()["record_shape"]["paths"][cell])
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


# ------------------------------------------------------------------ cores
def core_sweep(rec):
    """The enumeration is a SUBTRACTION; the arithmetic closes; and every RE-POINTED instrument
    returns 1303 -- never merely 'a number', because a broken one returns a clean 0."""
    s = ((rec or {}).get("sweep") or {})
    inst = list(s.get("instruments") or [])
    bad, lines = [], []
    for k in ("denominator", "re_pointed", "retired", "unaffected"):
        if s.get(k) is None:
            bad.append("sweep lacks %s" % k)
    if not (s.get("how_enumerated") or "").strip():
        bad.append("how_enumerated is empty: name the UNSCOPED read that produced the denominator -- a "
                   "forward list of remembered instruments omits in silence")
    if bad:
        return False, lines + bad

    den = s["denominator"]
    lines = ["instruments in the denominator (the unscoped read): %s" % _scrub(den),
             "entries carried: %d" % len(inst),
             "RE-POINTED %s + RETIRED %s + UNAFFECTED %s"
             % (_scrub(s["re_pointed"]), _scrub(s["retired"]), _scrub(s["unaffected"]))]
    if len(inst) > den:
        bad.append("more entries than the denominator admits")
    if s["re_pointed"] + s["retired"] + s["unaffected"] != len(inst):
        bad.append("the disposition arithmetic does not close against the entries carried")

    seen, controlled = set(), 0
    for e in inst:
        p = (e.get("path") or "").strip()
        d = (e.get("disposition") or "").strip()
        if not p:
            bad.append("an entry carries no path")
            continue
        if p in seen:
            bad.append("path appears twice: %s" % _scrub(p))
        seen.add(p)
        if d not in DISPOSITIONS:
            bad.append("%s: disposition %s is outside %s" % (_scrub(p), _scrub(d or "(none)"),
                                                             _scrub(DISPOSITIONS)))
            continue
        if not (e.get("basis") or "").strip():
            bad.append("%s: no basis for its disposition" % _scrub(p))
        if d == "RE-POINTED":
            c = e.get("control") or {}
            got = c.get("returns")
            if not (c.get("on") or "").strip() or not (c.get("invocation") or "").strip():
                bad.append("%s: RE-POINTED with no control naming what it now reads and what was RUN"
                           % _scrub(p))
            elif got != CONTROL_VALUE:
                bad.append("%s: POSITIVE CONTROL RETURNED %s, NOT %d -- and a clean %s is exactly what a "
                           "BROKEN instrument reports here, which is why this arm demands the number"
                           % (_scrub(p), _scrub(got), CONTROL_VALUE, _scrub(got)))
            else:
                controlled += 1
                lines.append("  control OK %s -> %d on %s" % (_scrub(p), CONTROL_VALUE, _scrub(c.get("on"))))
        elif e.get("control"):
            bad.append("%s: a control is recorded on a %s entry -- only RE-POINTED carries one"
                       % (_scrub(p), _scrub(d)))
    if s["re_pointed"] and controlled != s["re_pointed"]:
        bad.append("re_pointed says %s but %d carried a passing control" % (_scrub(s["re_pointed"]),
                                                                           controlled))
    if not inst:
        lines.append("NO instrument read the population off the rendered table -- an admissible RESULT, "
                     "graded on its denominator, not on finding breakage")
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
    if not commits:
        return True, ["fixed-input commits since the cut: 0 -- no proof can be stale against them"]
    sp = ((rec or {}).get("stale_proofs") or {})
    named, prior = set(sp.get("proofs_re_run") or []), set(prior or ())
    lines = ["fixed-input commits since the cut: %d (informational)" % len(commits),
             "proofs at risk: %d | record enumerates: %d" % (len(prior), len(named))]
    if named - prior:
        lines.append("NAMED BUT NEVER AT RISK: %s" % _scrub(sorted(named - prior)[:3]))
    return named == prior, lines


def _is_this_round(path, tag="r15"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


def _cells_present():
    return [c for c in CELLS if _rec(c) is not None]


# ------------------------------------------------------------------ arms
def d1_sweep():
    ok, lines = core_sweep(_rec("EN-d-1"))
    return verdict(ok, "PASS-D1-SWEEP", "FAIL-D1-SWEEP", lines)


def r15_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R15-VINTAGE-FIELD",
                   "no round-15 record exists in this checkout: an empty population is REFUSED, never "
                   "passed vacuously")
    ok_all, out = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        rec = _rec(cell)
        resolvable = True
        for path, commit in ((rec or {}).get("fixed_inputs_at_pin") or {}).items():
            try:
                git(["cat-file", "-e", "%s:%s" % (commit, path)])
            except InstrumentFailure:
                resolvable = False
        ok, lines = core_vintage(rec, resolvable, ("check_en_r15.py", "R15_BASE.json"))
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R15-VINTAGE-FIELD", "FAIL-R15-VINTAGE-FIELD", out)


def r15_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R15-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    cells = _cells_present()
    ok_all, lines = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        ok, ls = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        lines += ["%s:" % cell] + ["  " + x for x in ls]
    return verdict(ok_all, "PASS-R15-STALE-PROOFS", "FAIL-R15-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _entry(path, disp="RE-POINTED", returns=CONTROL_VALUE):
    e = {"path": path, "reads_the_rendered_table": True, "used_the_brace_discriminator": True,
         "disposition": disp, "basis": "measured at HEAD"}
    if disp == "RE-POINTED":
        e["control"] = {"returns": returns, "on": "NAMING_CENSUS_REPORT.r13.md rows json",
                        "invocation": "python recount.py --raw"}
    return e


def _sweep_ok(entries=None, den=9, rp=2, ret=1, un=0):
    entries = entries if entries is not None else [
        _entry("a/one.py"), _entry("b/two.py"), _entry("c/three.py", "RETIRED")]
    return {"sweep": {"denominator": den,
                      "how_enumerated": "comp-find over the corpus for readers of the table, denominator printed",
                      "instruments": entries, "re_pointed": rp, "retired": ret, "unaffected": un},
            "fixed_inputs_at_pin": {"a/check_en_r15.py": "abc", "b/R15_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def selftest_arms():
    s = _sweep_ok()
    arm("POSITIVE-BAR-sweep-correct-record", core_sweep(s)[0])
    arm("POSITIVE-BAR-sweep-ZERO-instruments-is-a-RESULT",
        core_sweep(_sweep_ok([], 9, 0, 0, 0))[0],
        "if nothing read the population off the braces, that PASSES on its denominator -- a bar that "
        "only passed on finding breakage would be an instruction to find some")
    arm("POSITIVE-BAR-sweep-all-retired-is-honest",
        core_sweep(_sweep_ok([_entry("a/x.py", "RETIRED")], 9, 0, 1, 0))[0],
        "an instrument that CANNOT return 1303 is not re-pointable and belongs in RETIRED")
    arm("POSITIVE-BAR-sweep-unaffected-carries-no-control",
        core_sweep(_sweep_ok([_entry("a/x.py", "UNAFFECTED")], 9, 0, 0, 1))[0])
    arm("POSITIVE-BAR-vintage", core_vintage(s, True, ("check_en_r15.py", "R15_BASE.json"))[0])
    arm("POSITIVE-BAR-stale-mint", core_stale(["a mint"], s, set())[0])

    arm("MUTANT-control-returns-ZERO", not core_sweep(
        _sweep_ok([_entry("a/x.py", "RE-POINTED", 0)], 9, 1, 0, 0))[0],
        "THE ARM THIS ROUND EXISTS FOR: a clean 0 is exactly what a broken instrument reports")
    arm("MUTANT-control-returns-a-plausible-other-number", not core_sweep(
        _sweep_ok([_entry("a/x.py", "RE-POINTED", 1302)], 9, 1, 0, 0))[0],
        "off by one is still not round 13's population")
    arm("MUTANT-re-pointed-with-no-control", not core_sweep(
        _sweep_ok([{"path": "a/x.py", "disposition": "RE-POINTED", "basis": "b"}], 9, 1, 0, 0))[0])
    arm("MUTANT-control-on-a-RETIRED-entry", not core_sweep(
        _sweep_ok([dict(_entry("a/x.py", "RETIRED"), control={"returns": 1303, "on": "x",
                                                              "invocation": "y"})], 9, 0, 1, 0))[0])
    arm("MUTANT-no-how-enumerated", not core_sweep(
        dict(s, sweep=dict(s["sweep"], how_enumerated="")))[0],
        "a forward list of remembered instruments omits in silence")
    arm("MUTANT-arithmetic-open", not core_sweep(_sweep_ok(None, 9, 3, 1, 0))[0])
    arm("MUTANT-entries-exceed-denominator", not core_sweep(_sweep_ok(None, 2, 2, 1, 0))[0])
    arm("MUTANT-duplicate-path", not core_sweep(
        _sweep_ok([_entry("a/x.py"), _entry("a/x.py")], 9, 2, 0, 0))[0])
    arm("MUTANT-disposition-off-enum", not core_sweep(
        _sweep_ok([dict(_entry("a/x.py"), disposition="FIXED")], 9, 1, 0, 0))[0])
    arm("MUTANT-no-basis", not core_sweep(
        _sweep_ok([dict(_entry("a/x.py"), basis="")], 9, 1, 0, 0))[0])
    arm("MUTANT-re-pointed-count-disagrees-with-controls", not core_sweep(
        _sweep_ok([_entry("a/x.py")], 9, 2, 0, 0))[0])

    arm("MUTANT-vintage-absent", not core_vintage({}, True, ("check_en_r15.py", "R15_BASE.json"))[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(s, False, ("check_en_r15.py", "R15_BASE.json"))[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(s, stale_proofs={"proofs_re_run": ["n.json"]}),
                                                set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_ENFORCE.TO-EN-d-1-r15.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_ENFORCE.TO-EN-r-7-r14.x.proof_of_spec.json"))
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-D1-SWEEP"))

    try:
        proofs_at_risk(["deadbeefdeadbeef nope"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True, "a failed retrieval RAISES")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    # -------------------------------------------------------------- THE WIRING (S106)
    global _rec
    real = _rec
    try:
        _rec = lambda c: s                                                 # noqa: E731
        arm("WIRING-record-present-is-graded", _cells_present() == ["EN-d-1"])
        _rec = lambda c: None                                              # noqa: E731
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r15_vintage_field()
        arm("WIRING-empty-population-is-REFUSED", "VERDICT: FAIL-R15-VINTAGE-FIELD" in buf.getvalue(),
            "a cell that wrote no record must still fail; an empty set is not a pass")
    finally:
        _rec = real

    bad = [x for x, ok, _ in _ARMS if not ok]
    pos = len([x for x, _, _ in _ARMS if x.startswith("POSITIVE")])
    wir = len([x for x, _, _ in _ARMS if x.startswith("WIRING")])
    for x, ok, note in _ARMS:
        print("  %-52s %-4s %s" % (x, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d WIRING, %d mutant/other)"
          % (len(_ARMS), pos, wir, len(_ARMS) - pos - wir))
    print("  NOT driven here, stated: the live git reads -- exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"d1-sweep": d1_sweep, "r15-vintage-field": r15_vintage_field,
        "r15-stale-proofs": r15_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
