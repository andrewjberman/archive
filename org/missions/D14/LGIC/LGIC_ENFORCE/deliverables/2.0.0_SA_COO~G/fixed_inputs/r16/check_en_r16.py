"""LGIC_ENFORCE round 16 -- the retired-marker cell and the retired-but-runnable census.

1.0.0_SA_CTO @f818ebd12b: "The class is: AN INSTRUMENT THAT HAS BEEN RETIRED IN A RECORD BUT IS STILL
RUNNABLE FROM THE TREE ... a census of the class is a round-16 cell ... ⛔ THE SUBTRACTION'S DOMAIN IS
`fixed_inputs/` ACROSS THE PROJECT, NOT THE RETIRED LIST -- reading the retired list can only find
retirements someone already wrote down."

TWO THINGS THIS FILE DOES THAT ARE NOT DECORATION:

1. The marker arm PROVES ADDITIVITY rather than asking for it. It refuses unless the pinned checker's
   blob is IDENTICAL at its round-13 pin and at HEAD -- the stale-proof protection made mechanical,
   because a marker that "additively" edited the pinned input would otherwise read exactly like one
   that did not.
2. The census arm REFUSES A DENOMINATOR THAT CAME FROM THE RETIRED LIST. A census whose domain is the
   set of known retirements cannot find an unknown one, and it reports a confident number while doing
   it -- this project has hit that shape twice.

No arm reads a second cell's record (S106); the round-wide arms grade the records PRESENT IN THIS
CHECKOUT and REFUSE an empty population rather than passing it vacuously.
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
CELLS = ("EN-m-2", "EN-s-1")
CLASSES = ("RETIRED-AND-DISCLOSED", "RETIRED-BUT-SILENT", "LIVE")
PROJECTS = ("LGIC_ENFORCE", "LGIC_LGCTFM")


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
    with open(os.path.join(HERE, "R16_BASE.json"), encoding="utf-8") as fh:
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
def core_marker(rec):
    """ADDITIVE is PROVEN, not promised: the pinned checker's blob must be IDENTICAL at pin and HEAD."""
    m = ((rec or {}).get("marker") or {})
    path = (m.get("marker_path") or "").strip()
    cmds = list(m.get("cmds_named") or [])
    rrec = (m.get("retiring_record") or "").strip()
    chk = (m.get("checker_path") or "").strip()
    b_pin = (m.get("checker_blob_at_r13_pin") or "").strip()
    b_head = (m.get("checker_blob_at_head") or "").strip()
    notclose = (m.get("what_this_does_not_close") or "").strip()
    bad, lines = [], ["marker: %s" % _scrub(path or "(none)"),
                      "CMDs named: %d %s" % (len(cmds), _scrub(cmds)),
                      "beside the pinned input: %s" % _scrub(chk or "(none)")]
    if not path.endswith("RETIRED.md"):
        bad.append("the marker is not a RETIRED.md sibling")
    if len(cmds) < 1:
        bad.append("no retired CMD named: the marker must say WHICH commands were retired")
    if not rrec:
        bad.append("no retiring_record: the marker must cite the record that retired them")
    if not chk:
        bad.append("no checker_path: the marker must name the pinned input it sits beside")
    if path and chk and os.path.dirname(path) != os.path.dirname(chk):
        bad.append("the marker is not IN THE SAME DIRECTORY as the checker -- a sibling or nothing")
    if not b_pin or not b_head:
        bad.append("the checker's blob is not recorded at BOTH its round-13 pin and HEAD -- that pair "
                   "is the only thing that proves this cell was additive")
    elif b_pin != b_head:
        bad.append("THE PINNED INPUT MOVED: blob at pin %s != blob at HEAD %s. This cell was required to "
                   "be ADDITIVE, and editing a closed round's fixed input is the stale-proof hazard the "
                   "round-15 L9 named" % (_scrub(b_pin[:12]), _scrub(b_head[:12])))
    else:
        lines.append("checker blob IDENTICAL at pin and HEAD (%s) -- additivity PROVEN, not promised"
                     % _scrub(b_pin[:12]))
    if not notclose:
        bad.append("what_this_does_not_close is empty: this cell does NOT stop the CMD returning PASS to "
                   "a runner, and the record says so or it oversells itself")
    return (not bad), lines + bad


def core_census(rec):
    """The domain is fixed_inputs/, NEVER the retired list, and the classes are MECE over it."""
    c = ((rec or {}).get("census") or {})
    inst = list(c.get("instruments") or [])
    how = (c.get("how_enumerated") or "").strip()
    bad, lines = [], []
    for k in ("denominator", "retired_and_disclosed", "retired_but_silent", "live"):
        if c.get(k) is None:
            bad.append("census lacks %s" % k)
    if not how:
        bad.append("how_enumerated is empty")
    if bad:
        return False, lines + bad

    den = c["denominator"]
    lines = ["instruments in the denominator: %s" % _scrub(den),
             "entries carried: %d" % len(inst),
             "RETIRED-AND-DISCLOSED %s + RETIRED-BUT-SILENT %s + LIVE %s"
             % (_scrub(c["retired_and_disclosed"]), _scrub(c["retired_but_silent"]), _scrub(c["live"]))]
    low = how.lower()
    if "fixed_inputs" not in low:
        bad.append("how_enumerated does not name fixed_inputs/ as the domain -- the CTO's instruction is "
                   "that the domain is fixed_inputs/ ACROSS THE PROJECT, never the retired list")
    for token in ("retired list", "retirement list", "the retired records", "list of retired"):
        if token in low:
            bad.append("how_enumerated enumerates FROM THE RETIRED LIST (%s): a census whose domain is "
                       "the known retirements cannot find an unknown one, and it reports a confident "
                       "number while doing it" % _scrub(token))
            break
    seen = set()
    projects = set()
    for e in inst:
        p = (e.get("path") or "").strip()
        k = (e.get("class") or "").strip()
        if not p:
            bad.append("an entry carries no path")
            continue
        if p in seen:
            bad.append("path appears twice: %s" % _scrub(p))
        seen.add(p)
        projects.add((e.get("project") or "").strip())
        if k not in CLASSES:
            bad.append("%s: class %s is outside %s" % (_scrub(p), _scrub(k or "(none)"), _scrub(CLASSES)))
            continue
        if not (e.get("basis") or "").strip():
            bad.append("%s: no basis for how disclosure was determined" % _scrub(p))
        if k == "LIVE" and (e.get("retiring_record") or None):
            bad.append("%s: classed LIVE but carries a retiring record" % _scrub(p))
        if k.startswith("RETIRED") and not (e.get("retiring_record") or "").strip():
            bad.append("%s: classed %s with no retiring record named" % (_scrub(p), _scrub(k)))
        if k == "RETIRED-BUT-SILENT" and e.get("instrument_discloses_it"):
            bad.append("%s: classed RETIRED-BUT-SILENT while instrument_discloses_it is true" % _scrub(p))
        if k == "RETIRED-AND-DISCLOSED" and not e.get("instrument_discloses_it"):
            bad.append("%s: classed RETIRED-AND-DISCLOSED while instrument_discloses_it is false"
                       % _scrub(p))
    missing_projects = [p for p in PROJECTS if p not in projects]
    if inst and missing_projects:
        bad.append("the census carries no instrument from %s -- it was cut ONCE ACROSS BOTH PROJECTS"
                   % _scrub(missing_projects))
    if len(inst) > den:
        bad.append("more entries than the denominator admits")
    if c["retired_and_disclosed"] + c["retired_but_silent"] + c["live"] != len(inst):
        bad.append("the class arithmetic does not close against the entries carried")
    if not inst:
        bad.append("no instruments carried: fixed_inputs/ is not empty in either project, so an empty "
                   "census is an enumeration failure rather than a result")
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


def _is_this_round(path, tag="r16"):
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
def m2_marker():
    ok, lines = core_marker(_rec("EN-m-2"))
    return verdict(ok, "PASS-M2-MARKER", "FAIL-M2-MARKER", lines)


def s1_census():
    ok, lines = core_census(_rec("EN-s-1"))
    return verdict(ok, "PASS-S1-CENSUS", "FAIL-S1-CENSUS", lines)


def r16_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R16-VINTAGE-FIELD",
                   "no round-16 record exists in this checkout: an empty population is REFUSED")
    ok_all, out = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        rec = _rec(cell)
        resolvable = True
        for path, commit in ((rec or {}).get("fixed_inputs_at_pin") or {}).items():
            try:
                git(["cat-file", "-e", "%s:%s" % (commit, path)])
            except InstrumentFailure:
                resolvable = False
        ok, lines = core_vintage(rec, resolvable, ("check_en_r16.py", "R16_BASE.json"))
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R16-VINTAGE-FIELD", "FAIL-R16-VINTAGE-FIELD", out)


def r16_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R16-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    cells = _cells_present()
    ok_all, lines = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        ok, ls = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        lines += ["%s:" % cell] + ["  " + x for x in ls]
    return verdict(ok_all, "PASS-R16-STALE-PROOFS", "FAIL-R16-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _marker_ok(**over):
    m = {"marker_path": "a/fixed_inputs/r13/RETIRED.md",
         "cmds_named": ["p37-population", "p37-tokens", "p37-producers"],
         "retiring_record": "deliverables/.../DISCRIMINATOR_SWEEP_R15.json",
         "checker_path": "a/fixed_inputs/r13/check_en_r13.py",
         "checker_blob_at_r13_pin": "deadbeefcafe0001", "checker_blob_at_head": "deadbeefcafe0001",
         "what_this_does_not_close": "a runner who never opens the directory still gets a green"}
    m.update(over)
    return {"marker": m, "fixed_inputs_at_pin": {"a/check_en_r16.py": "abc", "b/R16_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def _ent(path, proj, klass, rec="a/rec.json", disc=None):
    if disc is None:
        disc = (klass == "RETIRED-AND-DISCLOSED")
    return {"path": path, "project": proj, "class": klass, "basis": "read the file",
            "retiring_record": (rec if klass.startswith("RETIRED") else None),
            "instrument_discloses_it": disc}


def _census_ok(entries=None, den=12, rad=1, rbs=1, live=1, how=None):
    entries = entries if entries is not None else [
        _ent("e/fixed_inputs/r13/check_en_r13.py", "LGIC_ENFORCE", "RETIRED-BUT-SILENT"),
        _ent("e/fixed_inputs/r15/check_en_r15.py", "LGIC_ENFORCE", "RETIRED-AND-DISCLOSED"),
        _ent("l/fixed_inputs/r7/check_lt_r7.py", "LGIC_LGCTFM", "LIVE")]
    return {"census": {"denominator": den,
                       "how_enumerated": how or "enumerated every checker under fixed_inputs/ in BOTH "
                                                "projects with comp-find --name, denominator printed",
                       "instruments": entries, "retired_and_disclosed": rad,
                       "retired_but_silent": rbs, "live": live},
            "fixed_inputs_at_pin": {"a/check_en_r16.py": "abc", "b/R16_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def selftest_arms():
    m, c = _marker_ok(), _census_ok()
    arm("POSITIVE-BAR-marker-correct-record", core_marker(m)[0])
    arm("POSITIVE-BAR-census-correct-record", core_census(c)[0])
    arm("POSITIVE-BAR-census-ZERO-silent-is-a-RESULT",
        core_census(_census_ok([_ent("e/fixed_inputs/r15/check_en_r15.py", "LGIC_ENFORCE",
                                     "RETIRED-AND-DISCLOSED"),
                                _ent("l/fixed_inputs/r7/check_lt_r7.py", "LGIC_LGCTFM", "LIVE")],
                               12, 1, 0, 1))[0],
        "finding no further silent instrument PASSES -- a bar that only passed on finding more would be "
        "an instruction to find more")
    arm("POSITIVE-BAR-vintage", core_vintage(m, True, ("check_en_r16.py", "R16_BASE.json"))[0])
    arm("POSITIVE-BAR-stale-mint", core_stale(["a mint"], m, set())[0])

    arm("MUTANT-marker-pinned-input-MOVED", not core_marker(
        _marker_ok(checker_blob_at_head="0000000000000002"))[0],
        "THE ARM THIS CELL EXISTS FOR: an 'additive' cell that edited the pinned input reads exactly "
        "like one that did not, unless the blobs are compared")
    arm("MUTANT-marker-no-blob-pair", not core_marker(_marker_ok(checker_blob_at_head=""))[0])
    arm("MUTANT-marker-not-a-sibling", not core_marker(
        _marker_ok(marker_path="a/elsewhere/RETIRED.md"))[0])
    arm("MUTANT-marker-no-cmds", not core_marker(_marker_ok(cmds_named=[]))[0])
    arm("MUTANT-marker-no-retiring-record", not core_marker(_marker_ok(retiring_record=""))[0])
    arm("MUTANT-marker-oversells", not core_marker(_marker_ok(what_this_does_not_close=""))[0],
        "the marker does not stop the CMD returning PASS, and the record says so or it oversells")

    arm("MUTANT-census-domain-is-the-retired-list", not core_census(
        _census_ok(how="walked the retired list from the round-15 record and checked each"))[0],
        "a census whose domain is the KNOWN retirements cannot find an unknown one")
    arm("MUTANT-census-domain-unnamed", not core_census(_census_ok(how="looked at the checkers"))[0])
    arm("MUTANT-census-one-project-only", not core_census(
        _census_ok([_ent("e/fixed_inputs/r13/check_en_r13.py", "LGIC_ENFORCE", "RETIRED-BUT-SILENT")],
                   12, 0, 1, 0))[0],
        "cut ONCE ACROSS BOTH PROJECTS, so a single-project denominator is not the claim's population")
    arm("MUTANT-census-class-contradicts-disclosure", not core_census(
        _census_ok([_ent("e/a.py", "LGIC_ENFORCE", "RETIRED-BUT-SILENT", disc=True),
                    _ent("l/b.py", "LGIC_LGCTFM", "LIVE")], 12, 0, 1, 1))[0])
    arm("MUTANT-census-LIVE-with-a-retiring-record", not core_census(
        _census_ok([dict(_ent("e/a.py", "LGIC_ENFORCE", "LIVE"), retiring_record="r.json"),
                    _ent("l/b.py", "LGIC_LGCTFM", "LIVE")], 12, 0, 0, 2))[0])
    arm("MUTANT-census-arithmetic-open", not core_census(_census_ok(None, 12, 2, 1, 1))[0])
    arm("MUTANT-census-empty", not core_census(_census_ok([], 12, 0, 0, 0))[0],
        "fixed_inputs/ is not empty in either project, so an empty census is an enumeration failure")
    arm("MUTANT-census-duplicate-path", not core_census(
        _census_ok([_ent("e/a.py", "LGIC_ENFORCE", "LIVE"), _ent("e/a.py", "LGIC_LGCTFM", "LIVE")],
                   12, 0, 0, 2))[0])

    arm("MUTANT-vintage-absent", not core_vintage({}, True, ("check_en_r16.py", "R16_BASE.json"))[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(m, False, ("check_en_r16.py", "R16_BASE.json"))[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(m, stale_proofs={"proofs_re_run": ["n.json"]}),
                                                set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_ENFORCE.TO-EN-m-2-r16.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_ENFORCE.TO-EN-d-1-r15.x.proof_of_spec.json"))
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-M2-MARKER"))

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
        _rec = lambda x: m if x == "EN-m-2" else None                      # noqa: E731
        arm("WIRING-one-record-present-grades-only-it", _cells_present() == ["EN-m-2"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r16_vintage_field()
        arm("WIRING-the-absent-sibling-is-not-named", "EN-s-1:" not in buf.getvalue(),
            "the S106 regression arm: no absent sibling is named, so none can fail this cell")
        _rec = lambda x: {"EN-m-2": m, "EN-s-1": c}.get(x)                 # noqa: E731
        arm("WIRING-merged-tree-grades-both", _cells_present() == list(CELLS))
        _rec = lambda x: None                                              # noqa: E731
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r16_vintage_field()
        arm("WIRING-empty-population-is-REFUSED", "VERDICT: FAIL-R16-VINTAGE-FIELD" in buf.getvalue())
    finally:
        _rec = real

    bad = [x for x, ok, _ in _ARMS if not ok]
    pos = len([x for x, _, _ in _ARMS if x.startswith("POSITIVE")])
    wir = len([x for x, _, _ in _ARMS if x.startswith("WIRING")])
    for x, ok, note in _ARMS:
        print("  %-54s %-4s %s" % (x, "PASS" if ok else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d WIRING, %d mutant/other)"
          % (len(_ARMS), pos, wir, len(_ARMS) - pos - wir))
    print("  NOT driven here, stated: the live git reads -- exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"m2-marker": m2_marker, "s1-census": s1_census,
        "r16-vintage-field": r16_vintage_field, "r16-stale-proofs": r16_stale_proofs,
        "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
