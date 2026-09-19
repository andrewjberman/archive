"""LGIC_LGCTFM round 8 -- the routed-row LIVENESS re-read, cut BEFORE any remedy.

3.0.0_SA_CVO, S49 @938ea238ed: "A ROW IS DISARMED BY AN ACT BUT IS ONLY OBSERVED TO BE DISARMED BY A
READ, AND NOBODY RE-READS A ROW THEY DID NOT FILE ... THE COST IS NOT THE STALE ROW, IT IS THE WORK DONE
AROUND IT. Three seats routed, cut and re-measured against a hazard that no longer existed, and round 7's
LT-g-1 carried a criterion no correct artifact could satisfy AS A DIRECT CONSEQUENCE."

That criterion was MINE. So this round's ORDER is the finding: measure liveness, then remedy next round.

THE ARM GRADES THE SHAPE OF THE EVIDENCE AND NEVER THE DIRECTION OF THE ANSWER. All-live passes,
all-already-remedied passes, and the second is the more valuable result. A bar that leaned either way
would be an instruction, and the previous round already paid for one wrong lean.

⛔ AND EVERY VERDICT MUST CARRY WHAT WAS **READ AT HEAD** TO REACH IT. A row re-classified from the
route record's own prose is not a re-read -- it is the route quoted back, which is exactly the move that
produced the stale-row cost.
"""
import contextlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
CELLS = ("LT-l-1",)
VERDICTS = ("STILL-LIVE", "ALREADY-REMEDIED", "NOT-THIS-SEATS")


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
    with open(os.path.join(HERE, "R8_BASE.json"), encoding="utf-8") as fh:
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
def core_liveness(rec):
    """Every verdict carries what was READ AT HEAD. The direction of the answer is never graded."""
    lv = ((rec or {}).get("liveness") or {})
    rows = list(lv.get("rows") or [])
    bad, lines = [], []
    for k in ("denominator", "still_live", "already_remedied", "not_this_seats"):
        if lv.get(k) is None:
            bad.append("liveness lacks %s" % k)
    if not (lv.get("source_record") or "").strip():
        bad.append("no source_record: name the route record you read, WITH its commit")
    if not (lv.get("how_enumerated") or "").strip():
        bad.append("no how_enumerated: say how the routed set was derived from that record")
    if bad:
        return False, lines + bad

    den = lv["denominator"]
    lines = ["routed rows in the denominator: %s" % _scrub(den),
             "rows carried: %d" % len(rows),
             "STILL-LIVE %s + ALREADY-REMEDIED %s + NOT-THIS-SEATS %s"
             % (_scrub(lv["still_live"]), _scrub(lv["already_remedied"]), _scrub(lv["not_this_seats"]))]
    src = (lv.get("source_record") or "")
    # ⛔ A DIGIT IS NOT A COMMIT. The first cut of this check asked `any(ch.isdigit())` and was
    # satisfied by the "7" in REMEDIATION_ROUTE_R7.json -- a pin-detector that cannot tell a commit
    # from a filename, caught by this file's own MUTANT-source-record-unpinned arm before it shipped.
    # A pin is a HEX RUN of at least 7, and the filename's own digits do not qualify.
    if not re.search(r"(?:^|[@\s:])[0-9a-f]{7,40}(?:$|[\s)\].,])", src):
        bad.append("source_record names no commit: a route read without its vintage is the same "
                   "unpinned read this round exists to stop (a digit inside a FILENAME is not a pin)")
    if len(rows) != den:
        bad.append("rows carries %d entries for a denominator of %s -- every routed row gets a verdict"
                   % (len(rows), _scrub(den)))
    counts = {v: 0 for v in VERDICTS}
    seen = set()
    for e in rows:
        rid = (e.get("id") or "").strip()
        v = (e.get("verdict") or "").strip()
        ev = (e.get("evidence") or "").strip()
        if not rid:
            bad.append("an entry carries no row id")
            continue
        if rid in seen:
            bad.append("row id appears twice: %s" % _scrub(rid))
        seen.add(rid)
        if v not in VERDICTS:
            bad.append("%s: verdict %s is outside %s" % (_scrub(rid), _scrub(v or "(none)"),
                                                         _scrub(VERDICTS)))
            continue
        counts[v] += 1
        if not ev:
            bad.append("%s: NO EVIDENCE. Every verdict names what was READ AT HEAD to reach it -- a "
                       "path, a command or a commit" % _scrub(rid))
        elif len(ev) < 20:
            bad.append("%s: evidence is too thin to be a read (%d chars)" % (_scrub(rid), len(ev)))
        if v == "ALREADY-REMEDIED" and not (e.get("closed_by") or "").strip():
            bad.append("%s: ALREADY-REMEDIED with no closed_by -- name the commit or act that closed it, "
                       "because 'it looks fine now' is the read that let the last one go stale"
                       % _scrub(rid))
        if v != "ALREADY-REMEDIED" and (e.get("closed_by") or "").strip():
            bad.append("%s: closed_by is set on a %s row" % (_scrub(rid), _scrub(v)))
    for v in VERDICTS:
        key = {"STILL-LIVE": "still_live", "ALREADY-REMEDIED": "already_remedied",
               "NOT-THIS-SEATS": "not_this_seats"}[v]
        if lv[key] != counts[v]:
            bad.append("%s says %s but %d rows carry it" % (key, _scrub(lv[key]), counts[v]))
    if not rows:
        bad.append("no rows carried: the route record is not empty, so an empty liveness read is an "
                   "enumeration failure rather than a result")
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


def _is_this_round(path, tag="r8"):
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
def l1_liveness():
    ok, lines = core_liveness(_rec("LT-l-1"))
    return verdict(ok, "PASS-L1-LIVENESS", "FAIL-L1-LIVENESS", lines)


def r8_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R8-VINTAGE-FIELD",
                   "no round-8 record exists in this checkout: an empty population is REFUSED")
    ok_all, out = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        rec = _rec(cell)
        resolvable = True
        for path, commit in ((rec or {}).get("fixed_inputs_at_pin") or {}).items():
            try:
                git(["cat-file", "-e", "%s:%s" % (commit, path)])
            except InstrumentFailure:
                resolvable = False
        ok, lines = core_vintage(rec, resolvable, ("check_lt_r8.py", "R8_BASE.json"))
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R8-VINTAGE-FIELD", "FAIL-R8-VINTAGE-FIELD", out)


def r8_stale_proofs():
    b = base()
    try:
        out = git(["log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--"]
                  + list(b["stale_proof_bar"]["watched_paths"]))
        commits = [ln for ln in out.splitlines() if ln.strip()]
        prior = proofs_at_risk(commits)
    except InstrumentFailure as exc:
        return say("FAIL-R8-STALE-PROOFS", "INSTRUMENT FAILURE, NOT A CLEAN MINT: %s" % _scrub(exc))
    cells = _cells_present()
    ok_all, lines = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        ok, ls = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        lines += ["%s:" % cell] + ["  " + x for x in ls]
    return verdict(ok_all, "PASS-R8-STALE-PROOFS", "FAIL-R8-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
_ARMS = []


def arm(name, ok, note=""):
    _ARMS.append((name, bool(ok), note))


def _row(rid, v="STILL-LIVE", ev="read lib/opal_lgctfm.py:1762 at HEAD, the line is unchanged", closed=None):
    e = {"id": rid, "owner_in_route": "2.0.0_SA_COO~G", "verdict": v, "evidence": ev}
    if v == "ALREADY-REMEDIED":
        e["closed_by"] = closed or "5fd4251792"
    return e


def _live_ok(rows=None, den=None, sl=None, ar=None, nts=None, src=None):
    rows = rows if rows is not None else [_row("A"), _row("B", "ALREADY-REMEDIED"),
                                          _row("C", "NOT-THIS-SEATS")]
    counts = {v: sum(1 for r in rows if r.get("verdict") == v) for v in VERDICTS}
    return {"liveness": {"denominator": den if den is not None else len(rows),
                         "source_record": src or "REMEDIATION_ROUTE_R7.json@6c71cb4571",
                         "how_enumerated": "every row in the route record, by id",
                         "rows": rows,
                         "still_live": sl if sl is not None else counts["STILL-LIVE"],
                         "already_remedied": ar if ar is not None else counts["ALREADY-REMEDIED"],
                         "not_this_seats": nts if nts is not None else counts["NOT-THIS-SEATS"]},
            "fixed_inputs_at_pin": {"a/check_lt_r8.py": "abc", "b/R8_BASE.json": "abc"},
            "stale_proofs": {"proofs_re_run": []}}


def selftest_arms():
    ok = _live_ok()
    arm("POSITIVE-BAR-liveness-correct-record", core_liveness(ok)[0])
    arm("POSITIVE-BAR-ALL-still-live-passes",
        core_liveness(_live_ok([_row("A"), _row("B"), _row("C")]))[0],
        "the direction of the answer is never graded")
    arm("POSITIVE-BAR-ALL-already-remedied-passes",
        core_liveness(_live_ok([_row("A", "ALREADY-REMEDIED"), _row("B", "ALREADY-REMEDIED")]))[0],
        "and THIS is the more valuable result -- it is the one the last round paid for not having")
    arm("POSITIVE-BAR-vintage", core_vintage(ok, True, ("check_lt_r8.py", "R8_BASE.json"))[0])
    arm("POSITIVE-BAR-stale-mint", core_stale(["a mint"], ok, set())[0])

    arm("MUTANT-verdict-with-no-evidence", not core_liveness(
        _live_ok([_row("A", "STILL-LIVE", ""), _row("B")]))[0],
        "a verdict with no read behind it is the route quoted back at itself")
    arm("MUTANT-evidence-too-thin", not core_liveness(
        _live_ok([_row("A", "STILL-LIVE", "still true"), _row("B")]))[0])
    arm("MUTANT-already-remedied-without-closed-by", not core_liveness(
        _live_ok([{"id": "A", "verdict": "ALREADY-REMEDIED", "owner_in_route": "x",
                   "evidence": "the gate no longer refuses those five paths at HEAD"}]))[0],
        "'it looks fine now' is the read that let the last one go stale")
    arm("MUTANT-closed-by-on-a-live-row", not core_liveness(
        _live_ok([dict(_row("A"), closed_by="abc")]))[0])
    arm("MUTANT-source-record-unpinned", not core_liveness(
        _live_ok(src="REMEDIATION_ROUTE_R7.json"))[0],
        "a route read without its vintage is the unpinned read this round exists to stop")
    arm("MUTANT-rows-short-of-denominator", not core_liveness(_live_ok(den=9))[0])
    arm("MUTANT-count-disagrees-with-rows", not core_liveness(_live_ok(sl=99))[0])
    arm("MUTANT-verdict-off-enum", not core_liveness(
        _live_ok([dict(_row("A"), verdict="FIXED")]))[0])
    arm("MUTANT-duplicate-row-id", not core_liveness(_live_ok([_row("A"), _row("A")]))[0])
    arm("MUTANT-empty-rows", not core_liveness(_live_ok([], 0, 0, 0, 0))[0])

    arm("MUTANT-vintage-absent", not core_vintage({}, True, ("check_lt_r8.py", "R8_BASE.json"))[0])
    arm("MUTANT-vintage-unresolvable", not core_vintage(ok, False, ("check_lt_r8.py", "R8_BASE.json"))[0])
    arm("MUTANT-stale-invented", not core_stale(["a x"], dict(ok, stale_proofs={"proofs_re_run": ["n"]}),
                                                set())[0])
    arm("POSITIVE-round-scoped", _is_this_round("d/LGIC_LGCTFM.TO-LT-l-1-r8.x.proof_of_spec.json"))
    arm("MUTANT-frozen-round", not _is_this_round("d/LGIC_LGCTFM.TO-LT-g-1-r7.x.proof_of_spec.json"))
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-L1-LIVENESS"))

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
        _rec = lambda c: ok                                                # noqa: E731
        arm("WIRING-record-present-is-graded", _cells_present() == ["LT-l-1"])
        _rec = lambda c: None                                              # noqa: E731
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r8_vintage_field()
        arm("WIRING-empty-population-is-REFUSED", "VERDICT: FAIL-R8-VINTAGE-FIELD" in buf.getvalue())
    finally:
        _rec = real

    bad = [x for x, k, _ in _ARMS if not k]
    pos = len([x for x, _, _ in _ARMS if x.startswith("POSITIVE")])
    wir = len([x for x, _, _ in _ARMS if x.startswith("WIRING")])
    for x, k, note in _ARMS:
        print("  %-50s %-4s %s" % (x, "PASS" if k else "FAIL", note))
    print("  arms driven: %d (%d POSITIVE-SATISFIABILITY, %d WIRING, %d mutant/other)"
          % (len(_ARMS), pos, wir, len(_ARMS) - pos - wir))
    print("  NOT driven here, stated: the live git reads -- exercised by the real arms.")
    return say("PASS-ARMS-DISCRIMINATE" if not bad else "FAIL-ARMS-DO-NOT-DISCRIMINATE")


CMDS = {"l1-liveness": l1_liveness, "r8-vintage-field": r8_vintage_field,
        "r8-stale-proofs": r8_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
