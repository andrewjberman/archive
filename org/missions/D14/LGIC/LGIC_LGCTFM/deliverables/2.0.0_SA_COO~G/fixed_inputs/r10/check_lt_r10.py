"""LGIC_LGCTFM round 10 -- the class split, and W1-S21's conformant additive re-route.

1.0.0_SA_CTO's round-9 analysis @25bd9cb1fd s.2, adopting 3.0.0_SA_CVO's finding: "THE RECORD FLATTENS
A DISTINCTION THAT MATTERS: a future round reading 'UNEXECUTABLE-AS-ROUTED x2' will treat both as
equally blocked when ONE HAS A CHEAP ADDITIVE RE-ROUTE AND THE OTHER HAS NONE."

THREE THINGS THIS FILE DOES THAT ARE NOT DECORATION:

1. IT RE-DERIVES THE POPULATION from the round-9 record -- the rows actually carrying the flat
   UNEXECUTABLE-AS-ROUTED value -- and compares by SET EQUALITY. The order names two; the record is
   the authority.
2. BOTH NEW CLASSES MUST NAME SOMETHING. RE-ROUTABLE names the conformant alternative;
   IN-PRINCIPLE names what would have to change for one to exist. A row that says only "blocked"
   satisfies neither, so the split cannot be asserted by shrugging.
3. THE ADDITIVITY PROOF IS ANCHORED TO THE CELL'S OWN BASE, NOT TO A ROUND PIN. check_lt_r1.py has SIX
   commits touching it -- legitimate repairs during round 1 -- so a blob-vs-round-1-pin comparison
   would FAIL ON HONEST HISTORY and be a criterion no correct artifact could satisfy. The bar that
   answers the real question is blob-at-base == blob-at-HEAD: it proves THIS CELL did not touch the
   pinned input, which is the only thing this round can be responsible for.

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
CELLS = ("LT-r-1",)
CLASSES = ("UNEXECUTABLE-AS-ROUTED-RE-ROUTABLE", "UNEXECUTABLE-IN-PRINCIPLE")
COUNT_KEYS = {"UNEXECUTABLE-AS-ROUTED-RE-ROUTABLE": "re_routable",
              "UNEXECUTABLE-IN-PRINCIPLE": "in_principle"}
SOURCE_REC = ("org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/"
              "ROUTED_ROW_REMEDY_R9.json")
FLAT = "UNEXECUTABLE-AS-ROUTED"
SHA_MIN = 7


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
    with open(os.path.join(HERE, "R10_BASE.json"), encoding="utf-8") as fh:
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


def _looks_like_sha(s):
    s = (s or "").strip()
    return len(s) >= SHA_MIN and all(ch in "0123456789abcdefABCDEF" for ch in s)


def flat_rows():
    """The ids the round-9 record ACTUALLY carries with the flat class. The record is the authority."""
    p = os.path.join(REPO, SOURCE_REC)
    if not os.path.isfile(p):
        raise InstrumentFailure("the round-9 record is absent: %s" % SOURCE_REC)
    with open(p, encoding="utf-8") as fh:
        rec = json.load(fh)
    return {r["id"] for r in (rec.get("remedy") or {}).get("rows") or []
            if (r.get("class") or "").strip() == FLAT}


# ------------------------------------------------------------------ cores
def core_reclass(rec, population=None):
    c = ((rec or {}).get("reclass") or {})
    rows = list(c.get("rows") or [])
    bad, lines = [], []

    for k in ("base_sha", "source_record", "how_enumerated"):
        if not (c.get(k) or "").strip():
            bad.append("reclass lacks %s" % k)
    if c.get("population") is None:
        bad.append("reclass lacks population")
    for v in COUNT_KEYS.values():
        if c.get(v) is None:
            bad.append("reclass lacks %s" % v)
    if bad:
        return False, lines + bad

    lines = ["base_sha: %s" % _scrub(c["base_sha"]),
             "population: %s | rows carried: %d" % (_scrub(c["population"]), len(rows)),
             " + ".join("%s %s" % (k, _scrub(c[v])) for k, v in COUNT_KEYS.items())]

    if not _looks_like_sha(c["base_sha"]):
        bad.append("base_sha %s is not a commit-ish" % _scrub(c["base_sha"]))

    want = population if population is not None else flat_rows()
    have = {(r.get("id") or "").strip() for r in rows if (r.get("id") or "").strip()}
    lines.append("flat-valued rows re-derived from the round-9 record: %d" % len(want))
    if c["population"] != len(want):
        bad.append("population says %s; the round-9 record carries %d rows with the flat class"
                   % (_scrub(c["population"]), len(want)))
    missing, extra = sorted(want - have), sorted(have - want)
    if missing:
        bad.append("NOT RE-CLASSED: %s" % _scrub(missing))
    if extra:
        bad.append("RE-CLASSED BUT NOT FLAT-VALUED IN THE SOURCE: %s" % _scrub(extra))

    seen, tally = set(), {k: 0 for k in COUNT_KEYS}
    for r in rows:
        rid = (r.get("id") or "").strip()
        k = (r.get("new_class") or "").strip()
        if not rid:
            bad.append("a row carries no id")
            continue
        if rid in seen:
            bad.append("row appears twice: %s" % _scrub(rid))
        seen.add(rid)
        if (r.get("prior_class") or "").strip() != FLAT:
            bad.append("%s: prior_class is not %s" % (_scrub(rid), FLAT))
        if not _looks_like_sha(r.get("base_sha")):
            bad.append("%s: no base_sha on the row" % _scrub(rid))
        if k not in CLASSES:
            bad.append("%s: new_class %s is outside %s"
                       % (_scrub(rid), _scrub(k or "(none)"), _scrub(CLASSES)))
            continue
        tally[k] += 1
        # (2) BOTH CLASSES MUST NAME SOMETHING.
        if not (r.get("names") or "").strip():
            bad.append("%s: classed %s and NAMES nothing -- RE-ROUTABLE must name the conformant "
                       "alternative and IN-PRINCIPLE must name what would have to change. A row that "
                       "says only 'blocked' satisfies neither." % (_scrub(rid), _scrub(k)))
        if not (r.get("evidence") or "").strip():
            bad.append("%s: no evidence" % _scrub(rid))
    for k, v in COUNT_KEYS.items():
        if c[v] != tally[k]:
            bad.append("%s count says %s; the rows carry %d" % (k, _scrub(c[v]), tally[k]))
    if sum(c[v] for v in COUNT_KEYS.values()) != len(rows):
        bad.append("the class arithmetic does not close against the rows carried")
    if not rows:
        bad.append("no rows carried: the round-9 record's flat-valued set is not empty, so an empty "
                   "record is an enumeration failure rather than a result")
    return (not bad), lines + bad


def core_reroute(rec, exists=None, blobs=None):
    c = ((rec or {}).get("re_route") or {})
    bad, lines = [], []
    for k in ("row", "artifact", "precedent", "pinned_input_blob_at_base",
              "pinned_input_blob_at_head", "what_it_does_not_close"):
        if not (c.get(k) or "").strip():
            bad.append("re_route lacks %s" % k)
    if bad:
        return False, lines + bad

    lines = ["row: %s" % _scrub(c["row"]), "artifact: %s" % _scrub(c["artifact"]),
             "pinned input blob at base: %s" % _scrub(c["pinned_input_blob_at_base"])[:14],
             "pinned input blob at HEAD: %s" % _scrub(c["pinned_input_blob_at_head"])[:14]]

    present = exists if exists is not None else os.path.isfile(
        os.path.join(REPO, c["artifact"]))
    lines.append("the sibling document exists: %s" % present)
    if not present:
        bad.append("the re-route names an artifact that does not exist: %s" % _scrub(c["artifact"]))
    if "fixed_inputs/r1/" not in c["artifact"]:
        bad.append("the sibling is not beside the checker in fixed_inputs/r1/ -- W1-S21's basis "
                   "requires the causes to sit WHERE A LATER RE-DERIVATION WILL MEET THEM")

    # (3) ADDITIVITY, ANCHORED TO THIS CELL'S OWN BASE.
    at_base, at_head = c["pinned_input_blob_at_base"], c["pinned_input_blob_at_head"]
    if blobs is not None:
        at_base, at_head = blobs
    else:
        # The record's claimed HEAD blob is checked against the TREE, so the record cannot
        # assert additivity by simply writing the same string twice.
        pinned = base()["record_shape"]["pinned_input"]
        try:
            live = git(["rev-parse", "HEAD:%s" % pinned]).strip()
        except InstrumentFailure as exc:
            return False, lines + ["the pinned input could not be read (%s) -- a failed retrieval "
                                   "RAISES and is never an agreement" % _scrub(exc)]
        if at_head != live:
            bad.append("pinned_input_blob_at_head %s disagrees with the tree's %s"
                       % (_scrub(at_head)[:14], _scrub(live)[:14]))
    if at_base != at_head:
        bad.append("THE PINNED INPUT MOVED: blob at this cell's base %s != blob at HEAD %s. The "
                   "re-route is ADDITIVE and this cell may not touch check_lt_r1.py."
                   % (_scrub(at_base)[:14], _scrub(at_head)[:14]))
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


def _is_this_round(path, tag="r10"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def r1_reclass():
    ok, lines = core_reclass(_rec("LT-r-1"))
    return verdict(ok, "PASS-R1-RECLASS", "FAIL-R1-RECLASS", lines)


def r1_reroute():
    ok, lines = core_reroute(_rec("LT-r-1"))
    return verdict(ok, "PASS-R1-REROUTE", "FAIL-R1-REROUTE", lines)


def r10_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R10-VINTAGE-FIELD",
                   "no round-10 record exists in this checkout: an empty population is REFUSED here")
    ok_all, out = True, ["records present in THIS checkout: %d %s (S106)" % (len(cells), _scrub(cells))]
    for cell in cells:
        rec = _rec(cell)
        fx = ((rec or {}).get("fixed_inputs_at_pin") or {})
        resolvable = True
        for path, commit in fx.items():
            try:
                git(["cat-file", "-e", "%s:%s" % (commit, path)])
            except InstrumentFailure:
                resolvable = False
        ok, lines = core_vintage(rec, resolvable, ("check_lt_r10.py", "R10_BASE.json"))
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R10-VINTAGE-FIELD", "FAIL-R10-VINTAGE-FIELD", out)


def r10_stale_proofs():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R10-STALE-PROOFS",
                   "no round-10 record exists in this checkout: an empty population is REFUSED here")
    watched = base()["stale_proof_bar"]["watched_paths"]
    cut = base()["cut_pin"]
    commits = [ln for ln in git(["log", "--format=%H %aI", "%s..HEAD" % cut, "--"] + watched).splitlines()
               if ln.strip()]
    prior = proofs_at_risk(commits)
    ok_all, out = True, ["records present in THIS checkout: %d %s" % (len(cells), _scrub(cells))]
    for cell in cells:
        ok, lines = core_stale(commits, _rec(cell), prior)
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R10-STALE-PROOFS", "FAIL-R10-STALE-PROOFS", out)


# ------------------------------------------------------------------ self-test
def arm(name, ok, note=""):
    print("  %-52s %s%s" % (name, "PASS" if ok else "FAIL", (" -- " + note) if note else ""))
    return ok


SHA = "021d1947bb"
BLOB = "8835d6519b67d96bb6bc07b4230c0be81a4590f0"
SIB = "org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/DRIFT_CAUSES.md"


def _rc_ok(ids, classes=None, **over):
    classes = classes or {}
    rows = [{"id": i, "prior_class": FLAT,
             "new_class": classes.get(i, "UNEXECUTABLE-IN-PRINCIPLE"), "base_sha": SHA,
             "names": "what would have to change", "evidence": "read at the bytes"}
            for i in sorted(ids)]
    tally = {v: 0 for v in COUNT_KEYS.values()}
    for r in rows:
        # tolerate an out-of-enum class: the MUTANT that plants one must still build a record.
        key = COUNT_KEYS.get(r["new_class"])
        if key:
            tally[key] += 1
    c = {"base_sha": SHA, "source_record": SOURCE_REC + " @ its commit",
         "how_enumerated": "read the round-9 record's rows and took class == " + FLAT,
         "population": len(ids), "rows": rows}
    c.update(tally)
    c.update(over)
    return {"reclass": c}


def _rr_ok(**over):
    c = {"row": "LGIC_LGCTFM-W1-S21", "artifact": SIB,
         "precedent": "LGIC_ENFORCE round 16's additive-sibling ruling",
         "pinned_input_blob_at_base": BLOB, "pinned_input_blob_at_head": BLOB,
         "what_it_does_not_close": "it adds no arm and does not change the checker's output"}
    c.update(over)
    return {"re_route": c}


def selftest_arms():
    ok = True
    print("SELFTEST -- every arm is driven from a SATISFYING record and from a MUTANT of it.")
    try:
        pop = flat_rows()
    except InstrumentFailure as exc:
        print("  the round-9 record is unreadable (%s)" % _scrub(exc))
        return say("FAIL-ARMS-DISCRIMINATE", "the arms cannot be driven without the population")
    ids = sorted(pop)
    print("  live flat-valued population from the round-9 record: %d %s" % (len(ids), ids))

    mixed = {ids[0]: "UNEXECUTABLE-IN-PRINCIPLE"}
    if len(ids) > 1:
        mixed[ids[1]] = "UNEXECUTABLE-AS-ROUTED-RE-ROUTABLE"
    ok &= arm("POSITIVE-a-correct-MIXED-split-PASSES", core_reclass(_rc_ok(ids, mixed), pop)[0],
              "the real answer is one of each, and a bar admitting one class would force a lie")
    ok &= arm("MUTANT-one-row-dropped", not core_reclass(_rc_ok(ids[:-1]), pop)[0])
    ok &= arm("MUTANT-a-row-not-flat-valued-in-the-source",
              not core_reclass(_rc_ok(ids + ["LGIC_LGCTFM-S999"]), pop)[0])
    ok &= arm("MUTANT-class-NAMES-nothing",
              not core_reclass(_rc_ok(ids, mixed, rows=[
                  {"id": i, "prior_class": FLAT, "new_class": mixed.get(i, CLASSES[1]),
                   "base_sha": SHA, "names": "", "evidence": "x"} for i in ids]), pop)[0],
              "neither class is assertable by shrugging")
    ok &= arm("MUTANT-row-with-no-base_sha",
              not core_reclass(_rc_ok(ids, mixed, rows=[
                  {"id": i, "prior_class": FLAT, "new_class": mixed.get(i, CLASSES[1]),
                   "base_sha": "", "names": "n", "evidence": "x"} for i in ids]), pop)[0])
    ok &= arm("MUTANT-prior_class-not-the-flat-value",
              not core_reclass(_rc_ok(ids, mixed, rows=[
                  {"id": i, "prior_class": "EXECUTED", "new_class": mixed.get(i, CLASSES[1]),
                   "base_sha": SHA, "names": "n", "evidence": "x"} for i in ids]), pop)[0])
    ok &= arm("MUTANT-class-outside-the-enum",
              not core_reclass(_rc_ok(ids, {i: "HARD" for i in ids}), pop)[0])
    ok &= arm("MUTANT-arithmetic-does-not-close",
              not core_reclass(_rc_ok(ids, mixed, re_routable=9), pop)[0])
    ok &= arm("MUTANT-empty-record-is-REFUSED",
              not core_reclass(_rc_ok([], population=0), pop)[0])

    ok &= arm("POSITIVE-a-correct-re-route-PASSES",
              core_reroute(_rr_ok(), exists=True, blobs=(BLOB, BLOB))[0])
    ok &= arm("MUTANT-the-sibling-does-not-exist",
              not core_reroute(_rr_ok(), exists=False, blobs=(BLOB, BLOB))[0])
    ok &= arm("MUTANT-the-sibling-is-not-beside-the-checker",
              not core_reroute(_rr_ok(artifact="docs/DRIFT_CAUSES.md"), exists=True,
                               blobs=(BLOB, BLOB))[0])
    ok &= arm("MUTANT-THE-PINNED-INPUT-MOVED",
              not core_reroute(_rr_ok(), exists=True, blobs=(BLOB, "0" * 40))[0],
              "additivity anchored to THIS CELL'S base, not a round pin")
    ok &= arm("MUTANT-re-route-says-nothing-about-its-limit",
              not core_reroute(_rr_ok(what_it_does_not_close=""), exists=True,
                               blobs=(BLOB, BLOB))[0])

    ok &= arm("POSITIVE-vintage-satisfiable", core_vintage(
        {"fixed_inputs_at_pin": {"a/check_lt_r10.py": "c", "b/R10_BASE.json": "c"}}, True,
        ("check_lt_r10.py", "R10_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-missing-one", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_lt_r10.py": "c"}}, True,
        ("check_lt_r10.py", "R10_BASE.json"))[0])
    ok &= arm("POSITIVE-stale-empty-window-passes", core_stale([], {}, set())[0])
    ok &= arm("MUTANT-stale-set-inequality",
              not core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": []}}, {"p.json"})[0])
    ok &= arm("WIRING-stale-set-equality-passes",
              core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": ["p.json"]}},
                         {"p.json"})[0])

    print("  arms driven: 19 (4 POSITIVE, 1 WIRING, 14 mutant/other)")
    print("  NOT driven here, stated: the live git blob read -- exercised by the real re-route arm.")
    return say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE")


CMDS = {"r1-reclass": r1_reclass, "r1-reroute": r1_reroute,
        "r10-vintage-field": r10_vintage_field, "r10-stale-proofs": r10_stale_proofs,
        "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) != 2 or argv[1] not in CMDS:
        print("usage: %s {%s}" % (os.path.basename(argv[0]), "|".join(sorted(CMDS))))
        return 2
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
