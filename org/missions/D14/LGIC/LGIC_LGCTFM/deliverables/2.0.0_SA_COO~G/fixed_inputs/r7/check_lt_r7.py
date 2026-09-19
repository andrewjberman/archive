"""LGIC_LGCTFM round 7 -- the arms for THREE cells, and NO ARM READS A SECOND CELL'S RECORD.

1.0.0_SA_CTO @ed073a4d48: "AND 'DO NOT PAIR' BINDS THE CRITERION, NOT ONLY THE CELL. S106 is that
instruction defeated one level down: two correctly separated cells re-coupled by a shared grading arm
that ANDs both."

So every cell arm here takes its record from ONE path and grades ONLY that. The two round-wide arms
grade THE RECORDS PRESENT IN THIS CHECKOUT -- a worker's worktree carries exactly its own, the merged
tree carries all three -- and an EMPTY population is REFUSED rather than vacuously passed.

Every criterion was built against a hand-made CORRECT record driven as a POSITIVE-SATISFIABILITY arm,
and the self-test ALSO DRIVES THE WRAPPERS, not only the cores: the S106 defect lived in a wrapper no
arm touched.
"""
import contextlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
CELLS = ("LT-n-3", "LT-g-1", "LT-r-3")
BASIS = ("FILENAME", "PATH", "CONTENT")


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
    with open(os.path.join(HERE, "R7_BASE.json"), encoding="utf-8") as fh:
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
def core_node_types(rec):
    """BOTH denominators printed, BOTH differences RECOMPUTED from the record's own lists.

    A small answer passes: emitted-minus-declared of exactly ONE is as admissible as a large set, and
    so is ZERO. What is refused is a difference the record ASSERTS but its own lists do not support --
    the one thing a reader cannot check without re-deriving it.
    """
    n = ((rec or {}).get("node_types") or {})
    emitted, declared = list(n.get("emitted") or []), list(n.get("declared") or [])
    bad, lines = [], []
    for k in ("emitted_denominator", "declared_denominator"):
        if n.get(k) is None:
            bad.append("node_types lacks %s -- a set without its denominator is not a measurement" % k)
    if not emitted:
        bad.append("no EMITTED set: the population is what the engine actually produces")
    if not declared:
        bad.append("no DECLARED set: the enum at a named pin")
    if not (n.get("how_emitted_was_obtained") or "").strip():
        bad.append("how_emitted_was_obtained is empty: name the instrument you RAN, not the inference")
    if not (n.get("schema_pin") or "").strip():
        bad.append("no schema_pin: the enum moves, so the read needs its vintage")
    if not bad:
        e_minus_d = sorted(set(emitted) - set(declared))
        d_minus_e = sorted(set(declared) - set(emitted))
        lines = ["emitted: %d (denominator %s) | declared: %d (denominator %s)"
                 % (len(set(emitted)), _scrub(n.get("emitted_denominator")),
                    len(set(declared)), _scrub(n.get("declared_denominator"))),
                 "emitted MINUS declared (the violation class): %d %s" % (len(e_minus_d), _scrub(e_minus_d)),
                 "declared MINUS emitted (a finding, NOT a defect claim): %d %s"
                 % (len(d_minus_e), _scrub(d_minus_e)),
                 "schema pin: %s" % _scrub(n.get("schema_pin"))]
        for key, got in (("emitted_minus_declared", e_minus_d), ("declared_minus_emitted", d_minus_e)):
            stated = n.get(key)
            if stated is None:
                bad.append("%s is absent: state it, and the arm re-derives it from your own lists" % key)
            elif sorted(set(stated)) != got:
                bad.append("%s DISAGREES with the record's own lists: stated %s, derived %s"
                           % (key, _scrub(sorted(set(stated))), _scrub(got)))
        if len(set(emitted)) != n.get("emitted_denominator"):
            bad.append("emitted_denominator does not equal the emitted set's size")
        if len(set(declared)) != n.get("declared_denominator"):
            bad.append("declared_denominator does not equal the declared set's size")
    return (not bad), lines + bad


def core_gate_scope(rec):
    """A refusal with no ADMITTING control cannot tell a scoped guard from a broken one."""
    g = ((rec or {}).get("gate_scope") or {})
    refused = list(g.get("refused") or [])
    adm = g.get("admitting_control") or {}
    pred, basis = (g.get("refusing_predicate") or "").strip(), (g.get("refusal_basis") or "").strip()
    bad, lines = [], ["refused paths: %d (denominator %s)" % (len(refused), _scrub(g.get("refused_denominator"))),
                      "refusing predicate: %s" % _scrub(pred or "(none named)"),
                      "refusal basis: %s" % _scrub(basis or "(none)")]
    if not refused:
        bad.append("no refused paths recorded: the row claims a refusal, so show it")
    for r in refused:
        if not (r.get("path") or "").strip() or not (r.get("verdict") or "").strip():
            bad.append("a refused entry lacks its path or the gate's OWN output line")
            break
    if ":" not in pred:
        bad.append("the refusing predicate is not named at a file:line site")
    if basis not in BASIS:
        bad.append("refusal_basis must be one of %s -- it decides whether a RENAME lapses the guard"
                   % _scrub(BASIS))
    if not (adm.get("path") or "").strip() or not (adm.get("verdict") or "").strip():
        bad.append("NO ADMITTING CONTROL: a path the gate ADMITS, with its output line. Without it a "
                   "scoped guard and a guard that refuses everything read identically")
    elif adm.get("path") in [r.get("path") for r in refused]:
        bad.append("the admitting control's path is ALSO in the refused list: it controls nothing")
    else:
        lines.append("admitting control: %s -> %s" % (_scrub(adm.get("path")), _scrub(adm.get("verdict"))))
    if not (g.get("gate_pin") or "").strip():
        bad.append("no gate_pin: the gate is another seat's live artifact and moves")
    return (not bad), lines + bad


def core_route(rec):
    """The arithmetic closes over a STATED predicate, and UNROUTABLE is an honest answer."""
    r = ((rec or {}).get("remediation_route") or {})
    rows = list(r.get("rows") or [])
    unroutable = list(r.get("unroutable") or [])
    bad, lines = [], []
    for k in ("denominator", "population", "retired", "routed"):
        if r.get(k) is None:
            bad.append("remediation_route lacks %s" % k)
    if not (r.get("predicate") or "").strip():
        bad.append("NO PREDICATE STATED: 19 and 23 are both true of this channel under different "
                   "predicates, so a population without its predicate is an inherited count")
    if not bad:
        den, pop = r["denominator"], r["population"]
        lines = ["denominator (all remediation rows at your write time): %s" % _scrub(den),
                 "predicate: %s" % _scrub(str(r.get("predicate"))[:110]),
                 "population (denominator MINUS what the predicate excludes): %s" % _scrub(pop),
                 "routed %s + retired %s + unroutable %d" % (_scrub(r["routed"]), _scrub(r["retired"]),
                                                             len(unroutable))]
        if pop > den:
            bad.append("the population exceeds its own denominator")
        if r["routed"] + r["retired"] + len(unroutable) != pop:
            bad.append("the disposition arithmetic does not close against the population")
        if len(rows) != pop:
            bad.append("rows carries %d entries for a population of %s -- every member gets a row"
                       % (len(rows), _scrub(pop)))
        for e in rows:
            if not (e.get("id") or "").strip() or not (e.get("next_act") or "").strip() \
                    or not (e.get("basis") or "").strip():
                bad.append("a row lacks its id, next_act or basis -- the NEXT ACT is the gap, not the owner")
                break
        ids = [e.get("id") for e in rows]
        if len(set(ids)) != len(ids):
            bad.append("a row id appears twice")
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


def _is_this_round(path, tag="r7"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


def _cells_present():
    """The population is THE CHECKOUT, never a hard-coded tuple -- the S106 repair, carried forward."""
    return [c for c in CELLS if _rec(c) is not None]


# ------------------------------------------------------------------ arms
def n3_population():
    ok, lines = core_node_types(_rec("LT-n-3"))
    return verdict(ok, "PASS-N3-POPULATION", "FAIL-N3-POPULATION", lines)


def g1_scope():
    ok, lines = core_gate_scope(_rec("LT-g-1"))
    return verdict(ok, "PASS-G1-SCOPE", "FAIL-G1-SCOPE", lines)


def r3_route():
    ok, lines = core_route(_rec("LT-r-3"))
    return verdict(ok, "PASS-R3-ROUTE", "FAIL-R3-ROUTE", lines)


def r7_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R7-VINTAGE-FIELD",
                   "no round-7 record exists in this checkout: an empty population is REFUSED, never "
                   "passed vacuously")
    ok_all, out = True, ["records present in THIS checkout: %d %s (graded, and only these -- S106)"
                         % (len(cells), _scrub(cells))]
    for cell in cells:
        rec = _rec(cell)
        resolvable = True
        for path, commit in ((rec or {}).get("fixed_inputs_at_pin") or {}).items():
            try:
                git(["cat-file", "-e", "%s:%s" % (commit, path)])
            except InstrumentFailure:
                resolvable = False
        ok, lines = core_vintage(rec, resolvable, ("check_lt_r7.py", "R7_BASE.json"))
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R7-VINTAGE-FIELD", "FAIL-R7-VINTAGE-FIELD", out)


def r7_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R7-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    cells = _cells_present()
    ok_all, lines = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        ok, ls = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        lines += ["%s:" % cell] + ["  " + x for x in ls]
    if not cells:
        lines.append("no record present yet -- the window is graded when a record exists")
    return verdict(ok_all, "PASS-R7-STALE-PROOFS", "FAIL-R7-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _nodes_ok(emitted=("LAMBDA", "S3_BUCKET", "COGNITO_USER_POOL"), declared=("LAMBDA", "S3_BUCKET")):
    e, d = list(emitted), list(declared)
    return {"node_types": {"emitted": e, "emitted_denominator": len(set(e)),
                           "declared": d, "declared_denominator": len(set(d)),
                           "emitted_minus_declared": sorted(set(e) - set(d)),
                           "declared_minus_emitted": sorted(set(d) - set(e)),
                           "how_emitted_was_obtained": "python lib/opal_lgctfm.py walk --all, rc=0",
                           "schema_pin": "ed073a4d48"},
            "fixed_inputs_at_pin": {"a/check_lt_r7.py": "abc", "b/R7_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def _gate_ok():
    return {"gate_scope": {"refused": [{"path": "run/contract.json", "verdict": "REFUSED: name off-pattern"}],
                           "refused_denominator": 5,
                           "refusing_predicate": ".tools/naming-gate.py:214",
                           "refusal_basis": "FILENAME",
                           "admitting_control": {"path": "run/opal-lgctfm-contract.json",
                                                 "verdict": "OK: admitted"},
                           "gate_pin": "ed073a4d48"},
            "fixed_inputs_at_pin": {"a/check_lt_r7.py": "abc", "b/R7_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def _route_ok(pop=3, routed=2, retired=1, unroutable=()):
    rows = [{"id": "LGIC_LGCTFM-S%d" % i, "owner": "2.0.0_SA_COO~G",
             "next_act": "RETIRE" if i == 1 else "cut in round 8", "basis": "measured at HEAD"}
            for i in range(pop)]
    return {"remediation_route": {"denominator": 35, "predicate": "not closed AND disarm empty",
                                  "population": pop, "rows": rows, "retired": retired, "routed": routed,
                                  "unroutable": list(unroutable)},
            "fixed_inputs_at_pin": {"a/check_lt_r7.py": "abc", "b/R7_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def selftest_arms():
    n, g, r = _nodes_ok(), _gate_ok(), _route_ok()
    arm("POSITIVE-BAR-nodes-correct-record", core_node_types(n)[0])
    arm("POSITIVE-BAR-nodes-ONE-violation-is-admissible", core_node_types(_nodes_ok())[0],
        "exactly one emitted-minus-declared value passes -- the round-2 row's own claim")
    arm("POSITIVE-BAR-nodes-ZERO-violations-is-admissible",
        core_node_types(_nodes_ok(("LAMBDA",), ("LAMBDA", "S3_BUCKET")))[0],
        "if the enum has moved since round 2 the honest answer is ZERO, and it PASSES -- a bar that "
        "only passed on a violation would be an instruction to find one")
    arm("POSITIVE-BAR-gate-correct-record", core_gate_scope(g)[0])
    arm("POSITIVE-BAR-route-correct-record", core_route(r)[0])
    arm("POSITIVE-BAR-route-unroutable-is-honest",
        core_route(_route_ok(3, 1, 1, ({"id": "x", "why": "owner is a retired lane"},)))[0],
        "a row the cell cannot route is a finding, not a failure -- it passes when the arithmetic closes")
    arm("POSITIVE-BAR-vintage", core_vintage(n, True, ("check_lt_r7.py", "R7_BASE.json"))[0])
    arm("POSITIVE-BAR-stale-mint", core_stale(["a mint"], n, set())[0])

    arm("MUTANT-nodes-asserted-difference-disagrees", not core_node_types(
        dict(n, node_types=dict(n["node_types"], emitted_minus_declared=["LAMBDA"])))[0],
        "the arm RE-DERIVES both differences from the record's own lists")
    arm("MUTANT-nodes-denominator-lies", not core_node_types(
        dict(n, node_types=dict(n["node_types"], emitted_denominator=99)))[0])
    arm("MUTANT-nodes-no-instrument", not core_node_types(
        dict(n, node_types=dict(n["node_types"], how_emitted_was_obtained="")))[0])
    arm("MUTANT-nodes-no-schema-pin", not core_node_types(
        dict(n, node_types=dict(n["node_types"], schema_pin="")))[0])
    arm("MUTANT-nodes-emitted-empty", not core_node_types(
        dict(n, node_types=dict(n["node_types"], emitted=[])))[0])

    arm("MUTANT-gate-no-admitting-control", not core_gate_scope(
        dict(g, gate_scope=dict(g["gate_scope"], admitting_control={})))[0],
        "without it a scoped guard and a broken one read identically")
    arm("MUTANT-gate-control-is-also-refused", not core_gate_scope(
        dict(g, gate_scope=dict(g["gate_scope"],
                                admitting_control={"path": "run/contract.json", "verdict": "x"})))[0])
    arm("MUTANT-gate-predicate-not-a-site", not core_gate_scope(
        dict(g, gate_scope=dict(g["gate_scope"], refusing_predicate="the name check")))[0])
    arm("MUTANT-gate-basis-off-enum", not core_gate_scope(
        dict(g, gate_scope=dict(g["gate_scope"], refusal_basis="SOMEHOW")))[0],
        "the basis decides whether a RENAME lapses the guard silently")
    arm("MUTANT-gate-no-pin", not core_gate_scope(
        dict(g, gate_scope=dict(g["gate_scope"], gate_pin="")))[0])

    arm("MUTANT-route-no-predicate", not core_route(
        dict(r, remediation_route=dict(r["remediation_route"], predicate="")))[0],
        "19 and 23 are both true here under different predicates")
    arm("MUTANT-route-arithmetic-open", not core_route(_route_ok(3, 1, 1))[0])
    arm("MUTANT-route-rows-short", not core_route(
        dict(r, remediation_route=dict(r["remediation_route"], rows=[])))[0])
    arm("MUTANT-route-population-exceeds-denominator", not core_route(
        dict(r, remediation_route=dict(r["remediation_route"], denominator=2)))[0])
    arm("MUTANT-route-duplicate-id", not core_route(
        dict(r, remediation_route=dict(r["remediation_route"],
                                       rows=[r["remediation_route"]["rows"][0]] * 3)))[0])

    arm("MUTANT-vintage-absent", not core_vintage({}, True, ("check_lt_r7.py", "R7_BASE.json"))[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(n, False, ("check_lt_r7.py", "R7_BASE.json"))[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(n, stale_proofs={"proofs_re_run": ["n.json"]}),
                                                set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_LGCTFM.TO-LT-n-3-r7.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_LGCTFM.TO-LT-e-7-r6.x.proof_of_spec.json"))
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-N3-POPULATION"))

    try:
        proofs_at_risk(["deadbeefdeadbeef nope"])
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "returned a value instead of raising")
    except InstrumentFailure:
        arm("POSITIVE-CONTROL-instrument-failure-raises", True, "a failed retrieval RAISES")
    except Exception as exc:
        arm("POSITIVE-CONTROL-instrument-failure-raises", False, "wrong exception: %s" % _scrub(exc))

    # -------------------------------------------------------------- THE WIRING
    # S106: the defect lived in a WRAPPER that no core arm touched. These drive the wrappers.
    global _rec
    real = _rec
    try:
        _rec = lambda c: n if c == "LT-n-3" else None                      # noqa: E731
        arm("WIRING-one-record-present-grades-only-it", _cells_present() == ["LT-n-3"],
            "a worker's worktree holds exactly ITS OWN record")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r7_vintage_field()
        arm("WIRING-one-cell-ALONE-is-graded-alone", "LT-g-1:" not in buf.getvalue()
            and "LT-r-3:" not in buf.getvalue(),
            "THE S106 REGRESSION ARM: no absent sibling is named, so no absent sibling can fail it")
        _rec = lambda c: {"LT-n-3": n, "LT-g-1": g, "LT-r-3": r}.get(c)     # noqa: E731
        arm("WIRING-merged-tree-grades-all-three", _cells_present() == list(CELLS))
        _rec = lambda c: None                                              # noqa: E731
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r7_vintage_field()
        arm("WIRING-empty-population-is-REFUSED", "VERDICT: FAIL-R7-VINTAGE-FIELD" in buf.getvalue(),
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


CMDS = {"n3-population": n3_population, "g1-scope": g1_scope, "r3-route": r3_route,
        "r7-vintage-field": r7_vintage_field, "r7-stale-proofs": r7_stale_proofs,
        "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
