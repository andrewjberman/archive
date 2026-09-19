"""LGIC_LGCTFM round 9 -- execute the executable routed remedies, disposition all seven.

1.0.0_SA_CTO's round-8 analysis @b24a81c4d3 s.5: "Round 9 takes ... the 7 STILL-LIVE rows, now measured
as genuinely live (0 of 7 stale), as the remedy population ... Nothing else."

And s.4, adopting 3.0.0_SA_CVO's sentence as the ruling: "A LIVENESS CELL CANNOT BE ISOLATED --
ISOLATION IS EXACTLY THE THING IT IS MEASURING AGAINST. The remedy is the CUT, not the worker: such a
cell runs IN THE SHARED TREE, or STATES ITS BASE SHA IN EVERY VERDICT LINE."

THREE THINGS THIS FILE DOES THAT ARE NOT DECORATION:

1. IT RE-DERIVES THE POPULATION from the round-8 liveness record and compares by SET EQUALITY. The
   order carries the seven ids as a framing control; a cell that copied them would be inheriting a
   list, which is the shape this project has now hit five times.
2. IT REFUSES A ROW WITHOUT A base_sha. The worker holds a worktree, so the second branch of the
   ruling binds every verdict line. Round 8's 2-of-23 miss was invisible precisely because no line
   said which tree it was read in.
3. IT REFUSES AN `UNEXECUTABLE-AS-ROUTED` ROW THAT NAMES NO BLOCKING RULING AND NO PINNED PATH. That
   class is the one a cell could hide unfinished work behind, so it is the most expensive to assert
   and the arm makes it the most expensive to assert.

The vintage and stale-proof arms grade the records PRESENT IN THIS CHECKOUT (S106) and REFUSE an empty
population rather than passing it vacuously.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
CELLS = ("LT-m-1",)
LIVENESS_REC = ("org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/"
                "ROUTED_ROW_LIVENESS_R8.json")
CLASSES = ("EXECUTED", "UNEXECUTABLE-AS-ROUTED", "NOT-WORK-A-DECISION",
           "NOT-A-WORKERS-ACT", "THE-ISSUERS-OWN-ACT")
COUNT_KEYS = {"EXECUTED": "executed",
              "UNEXECUTABLE-AS-ROUTED": "unexecutable_as_routed",
              "NOT-WORK-A-DECISION": "not_work_a_decision",
              "NOT-A-WORKERS-ACT": "not_a_workers_act",
              "THE-ISSUERS-OWN-ACT": "the_issuers_own_act"}
SHA_RE_MIN = 7


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
    with open(os.path.join(HERE, "R9_BASE.json"), encoding="utf-8") as fh:
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


def _cells_present():
    return [c for c in CELLS if _rec(c) is not None]


def still_live_set():
    """The STILL-LIVE ids from the round-8 liveness record, read from the tree, never inherited."""
    with open(os.path.join(REPO, LIVENESS_REC), encoding="utf-8") as fh:
        rec = json.load(fh)
    return {r["id"] for r in (rec.get("liveness") or {}).get("rows") or []
            if (r.get("verdict") or "").strip() == "STILL-LIVE"}


def _looks_like_sha(s):
    s = (s or "").strip()
    if len(s) < SHA_RE_MIN:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in s)


# ------------------------------------------------------------------ cores
def core_remedy(rec, population=None):
    c = ((rec or {}).get("remedy") or {})
    rows = list(c.get("rows") or [])
    bad, lines = [], []

    for k in ("base_sha", "source_record", "how_enumerated"):
        if not (c.get(k) or "").strip():
            bad.append("remedy lacks %s" % k)
    if c.get("population") is None:
        bad.append("remedy lacks population")
    for k in COUNT_KEYS.values():
        if c.get(k) is None:
            bad.append("remedy lacks %s" % k)
    if bad:
        return False, lines + bad

    lines = ["base_sha: %s" % _scrub(c["base_sha"]),
             "population: %s | rows carried: %d" % (_scrub(c["population"]), len(rows)),
             " + ".join("%s %s" % (k, _scrub(c[v])) for k, v in COUNT_KEYS.items())]

    if not _looks_like_sha(c["base_sha"]):
        bad.append("base_sha %s is not a commit-ish: the ruling requires the TREE to be identifiable, "
                   "and a label is not a tree" % _scrub(c["base_sha"]))

    want = population if population is not None else still_live_set()
    have = {(r.get("id") or "").strip() for r in rows if (r.get("id") or "").strip()}
    lines.append("STILL-LIVE set re-derived from the round-8 record: %d" % len(want))
    if c["population"] != len(want):
        bad.append("population says %s; the round-8 record's STILL-LIVE set has %d"
                   % (_scrub(c["population"]), len(want)))
    missing = sorted(want - have)
    extra = sorted(have - want)
    if missing:
        bad.append("NOT DISPOSITIONED (STILL-LIVE and absent from the record): %s" % _scrub(missing))
    if extra:
        bad.append("DISPOSITIONED BUT NOT IN THE STILL-LIVE SET: %s" % _scrub(extra))

    seen, tally = set(), {k: 0 for k in COUNT_KEYS}
    for r in rows:
        rid = (r.get("id") or "").strip()
        k = (r.get("class") or "").strip()
        if not rid:
            bad.append("a row carries no id")
            continue
        if rid in seen:
            bad.append("row appears twice: %s" % _scrub(rid))
        seen.add(rid)
        if k not in CLASSES:
            bad.append("%s: class %s is outside %s" % (_scrub(rid), _scrub(k or "(none)"), _scrub(CLASSES)))
            continue
        tally[k] += 1
        # (2) EVERY VERDICT LINE STATES ITS BASE SHA.
        if not _looks_like_sha(r.get("base_sha")):
            bad.append("%s: no base_sha on the row -- the ruling binds EVERY verdict line, because a "
                       "reader who does not know the tree cannot tell a TRUE absence from a FROZEN one"
                       % _scrub(rid))
        if not (r.get("routed_act") or "").strip():
            bad.append("%s: does not quote the routed act it is dispositioning" % _scrub(rid))
        if not (r.get("evidence") or "").strip():
            bad.append("%s: no evidence" % _scrub(rid))
        if k == "EXECUTED":
            if not _looks_like_sha(r.get("commit")):
                bad.append("%s: classed EXECUTED with no commit naming the act" % _scrub(rid))
        elif r.get("commit"):
            bad.append("%s: classed %s but names an executing commit" % (_scrub(rid), _scrub(k)))
        # (3) THE EXPENSIVE CLASS IS THE EXPENSIVE ONE TO ASSERT.
        if k == "UNEXECUTABLE-AS-ROUTED":
            br = (r.get("blocking_ruling") or "").strip()
            if not br:
                bad.append("%s: classed UNEXECUTABLE-AS-ROUTED with no blocking_ruling. That class is "
                           "where unfinished work would hide, so it must NAME the ruling that blocks "
                           "the act and the pinned path the act would edit" % _scrub(rid))
            elif "fixed_inputs" not in br:
                bad.append("%s: blocking_ruling names no pinned fixed input path" % _scrub(rid))

    for k, v in COUNT_KEYS.items():
        if c[v] != tally[k]:
            bad.append("%s count says %s; the rows carry %d" % (k, _scrub(c[v]), tally[k]))
    if sum(c[v] for v in COUNT_KEYS.values()) != len(rows):
        bad.append("the class arithmetic does not close against the rows carried")
    if not rows:
        bad.append("no rows carried: the STILL-LIVE set is not empty, so an empty record is an "
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


def _is_this_round(path, tag="r9"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def m1_remedy():
    ok, lines = core_remedy(_rec("LT-m-1"))
    return verdict(ok, "PASS-M1-REMEDY", "FAIL-M1-REMEDY", lines)


def r9_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R9-VINTAGE-FIELD",
                   "no round-9 record exists in this checkout: an empty population is REFUSED here, "
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
        ok, lines = core_vintage(rec, resolvable, ("check_lt_r9.py", "R9_BASE.json"))
        ok_all = ok_all and ok
        out_lines += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R9-VINTAGE-FIELD", "FAIL-R9-VINTAGE-FIELD", out_lines)


def r9_stale_proofs():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R9-STALE-PROOFS",
                   "no round-9 record exists in this checkout: an empty population is REFUSED here")
    watched = base()["stale_proof_bar"]["watched_paths"]
    cut = base()["cut_pin"]
    commits = [ln for ln in git(["log", "--format=%H %aI", "%s..HEAD" % cut, "--"] + watched).splitlines()
               if ln.strip()]
    prior = proofs_at_risk(commits)
    ok_all, out_lines = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        ok, lines = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        out_lines += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R9-STALE-PROOFS", "FAIL-R9-STALE-PROOFS", out_lines)


# ------------------------------------------------------------------ self-test
def arm(name, ok, note=""):
    print("  %-52s %s%s" % (name, "PASS" if ok else "FAIL", (" -- " + note) if note else ""))
    return ok


SHA = "13566fbfe2"


def _row(rid, k="NOT-WORK-A-DECISION", **over):
    r = {"id": rid, "routed_act": "the act as routed", "class": k, "base_sha": SHA,
         "evidence": "read at the bytes", "commit": None, "blocking_ruling": None}
    if k == "EXECUTED":
        r["commit"] = SHA
    if k == "UNEXECUTABLE-AS-ROUTED":
        r["blocking_ruling"] = ("round 16's additive-sibling ruling; the act would edit "
                                "deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py")
    r.update(over)
    return r


def _remedy_ok(ids, classes=None, **over):
    classes = classes or {}
    rows = [_row(i, classes.get(i, "NOT-WORK-A-DECISION")) for i in sorted(ids)]
    tally = {v: 0 for v in COUNT_KEYS.values()}
    for r in rows:
        tally[COUNT_KEYS[r["class"]]] += 1
    c = {"base_sha": SHA, "source_record": LIVENESS_REC + " @ its commit",
         "how_enumerated": "read the round-8 liveness record's rows and took verdict == STILL-LIVE",
         "population": len(ids), "rows": rows}
    c.update(tally)
    c.update(over)
    return {"remedy": c}


def selftest_arms():
    ok = True
    print("SELFTEST -- every arm is driven from a SATISFYING record and from a MUTANT of it.")
    try:
        pop = still_live_set()
    except Exception as exc:
        print("  the round-8 liveness record is unreadable (%s)" % _scrub(exc))
        return say("FAIL-ARMS-DISCRIMINATE", "the arms cannot be driven without the population")
    ids = sorted(pop)
    print("  live STILL-LIVE population: %d" % len(ids))

    ok &= arm("POSITIVE-a-correct-disposition-PASSES", core_remedy(_remedy_ok(ids), pop)[0],
              "a correct artifact must be able to satisfy this")
    ok &= arm("MUTANT-one-row-dropped",
              not core_remedy(_remedy_ok(ids[:-1]), pop)[0],
              "set equality catches a silent omission the arithmetic would not")
    ok &= arm("MUTANT-a-row-outside-the-STILL-LIVE-set",
              not core_remedy(_remedy_ok(ids + ["LGIC_LGCTFM-S999"]), pop)[0])
    ok &= arm("MUTANT-row-with-no-base_sha",
              not core_remedy(_remedy_ok(ids, rows=[_row(i, base_sha="") for i in ids]), pop)[0],
              "the ruling binds EVERY verdict line, not just the record header")
    ok &= arm("MUTANT-base_sha-is-a-label-not-a-commit",
              not core_remedy(_remedy_ok(ids, base_sha="HEAD"), pop)[0],
              "a label is not a tree")
    ok &= arm("MUTANT-EXECUTED-with-no-commit",
              not core_remedy(_remedy_ok(ids, rows=[_row(i, "EXECUTED", commit=None) for i in ids],
                                         executed=len(ids), not_work_a_decision=0), pop)[0])
    ok &= arm("MUTANT-UNEXECUTABLE-with-no-blocking-ruling",
              not core_remedy(_remedy_ok(
                  ids, rows=[_row(i, "UNEXECUTABLE-AS-ROUTED", blocking_ruling="") for i in ids],
                  unexecutable_as_routed=len(ids), not_work_a_decision=0), pop)[0],
              "the class where unfinished work would hide is the costliest to assert")
    ok &= arm("MUTANT-UNEXECUTABLE-whose-ruling-names-no-pinned-path",
              not core_remedy(_remedy_ok(
                  ids, rows=[_row(i, "UNEXECUTABLE-AS-ROUTED",
                                  blocking_ruling="it seemed hard") for i in ids],
                  unexecutable_as_routed=len(ids), not_work_a_decision=0), pop)[0])
    ok &= arm("MUTANT-class-outside-the-enum",
              not core_remedy(_remedy_ok(ids, rows=[_row(i, "DONE-ISH") for i in ids]), pop)[0])
    ok &= arm("MUTANT-class-arithmetic-does-not-close",
              not core_remedy(_remedy_ok(ids, executed=99), pop)[0])
    ok &= arm("MUTANT-no-routed_act-quoted",
              not core_remedy(_remedy_ok(ids, rows=[_row(i, routed_act="") for i in ids]), pop)[0])
    ok &= arm("MUTANT-empty-record-is-REFUSED-not-vacuously-passed",
              not core_remedy(_remedy_ok([], population=0), pop)[0])
    ok &= arm("WIRING-a-MIXED-disposition-PASSES",
              core_remedy(_remedy_ok(ids, classes={
                  ids[0]: "EXECUTED", ids[1]: "UNEXECUTABLE-AS-ROUTED",
                  ids[2]: "NOT-A-WORKERS-ACT", ids[3]: "THE-ISSUERS-OWN-ACT"}), pop)[0]
              if len(ids) >= 4 else True,
              "the real answer is mixed, and a bar that only admits one class would force a lie")

    ok &= arm("POSITIVE-vintage-satisfiable",
              core_vintage({"fixed_inputs_at_pin": {"a/check_lt_r9.py": "c", "b/R9_BASE.json": "c"}},
                           True, ("check_lt_r9.py", "R9_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-missing-one", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_lt_r9.py": "c"}}, True,
        ("check_lt_r9.py", "R9_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-unresolvable", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_lt_r9.py": "c", "b/R9_BASE.json": "c"}}, False,
        ("check_lt_r9.py", "R9_BASE.json"))[0])
    ok &= arm("POSITIVE-stale-empty-window-passes", core_stale([], {}, set())[0])
    ok &= arm("MUTANT-stale-set-inequality",
              not core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": []}}, {"p.json"})[0])
    ok &= arm("WIRING-stale-set-equality-passes",
              core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": ["p.json"]}},
                         {"p.json"})[0])

    print("  arms driven: 19 (3 POSITIVE, 3 WIRING, 13 mutant/other)")
    print("  NOT driven here, stated: proofs_at_risk's live git read -- exercised by the real arm.")
    return say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE")


CMDS = {"m1-remedy": m1_remedy, "r9-vintage-field": r9_vintage_field,
        "r9-stale-proofs": r9_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) != 2 or argv[1] not in CMDS:
        print("usage: %s {%s}" % (os.path.basename(argv[0]), "|".join(sorted(CMDS))))
        return 2
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
