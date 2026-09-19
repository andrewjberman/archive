"""LGIC_ENFORCE round 18 -- R-38's resolve/card half over the re-derived placeholder population.

1.0.0_SA_CTO's ruling @4a5b0cafa8: "Round 18 carries the second half over the 1303-row population, the
cell re-measuring its own denominator at write time and printing resolved + carded == its own
re-derived population. NOT re-opening round 13; NOT treating 1303 as an inherited constant, since it
moved from 1411 once and will move again."

THREE THINGS THIS FILE DOES THAT ARE NOT DECORATION:

1. IT RE-DERIVES THE POPULATION ITSELF from the source the record DECLARES, and compares by SET
   EQUALITY ON THE ROW INDEX. A count can agree while the membership differs; only the set catches a
   swap. ⛔ THE INDEX, NOT THE NAME: the population is a MULTISET -- 1303 placeholder rows, 630
   distinct `current` names, 1200 distinct whole rows -- so a name-keyed arm would pass a record
   dispositioning 630 of 1303 with its arithmetic closing. This file shipped that defect for one
   revision and its OWN SELF-TEST caught it, by printing a population that disagreed with the
   issuer's independent read.
2. IT REFUSES A PARTITION DEFINED BY A TOKEN LIST. R-38 names {system}/{scope}/{cadence}, and the
   population carries NINE distinct tokens. CARDED is POPULATION MINUS RESOLVED -- a subtraction --
   and a `how_enumerated` that defines the population by naming tokens is the forward-list defect this
   project has been corrected for four times.
3. IT MAKES RESOLVED THE COSTLY CLASS TO ASSERT. A RESOLVED row must name the declared source its
   substitution was MEASURED from; a CARDED row must name an owner AND a reason. Neither is assertable
   by shrugging, and RESOLVED is the one that claims a measurement was taken.

The vintage and stale-proof arms grade the records PRESENT IN THIS CHECKOUT (S106) and REFUSE an empty
population rather than passing it vacuously.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
CELLS = ("EN-t-1",)
DISPOSITIONS = ("RESOLVED", "CARDED")
TOKEN_RE = re.compile(r"\{([a-z_]+)\}")
INHERITED = 1303


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
    with open(os.path.join(HERE, "R18_BASE.json"), encoding="utf-8") as fh:
        return json.load(fh)


class InstrumentFailure(RuntimeError):
    """An exception is not an empty set: EMPTY is the value that PASSES at a mint."""


def git(args, timeout=180):
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


# ------------------------------------------------------------------ independent re-derivation
def population_from(source_path):
    """Re-derive {judged_rows, set-of-ROW-INDICES-with-a-literal-token} from the declared source.

    Reads the RAW `canonical` field of the census rows -- never the rendered table, whose braces
    round 14 escaped and which is why count_report() was retired.

    ⛔ THE POPULATION IS A MULTISET AND THE KEY MUST BE THE ROW INDEX. Measured at the cut against
    NAMING_CENSUS_REPORT.r13.md: 1303 placeholder ROWS collapse to 630 distinct `current` names, 1059
    distinct (current, plane, type) tuples, and only 1200 distinct WHOLE ROWS -- there are genuine
    duplicate rows. NO FIELD COMBINATION MAKES IT A SET. An arm keyed on the name would have passed a
    record dispositioning 630 of 1303 with its arithmetic closing, which is this project's own
    collapse defect (a grader keyed on basename and got 13 keys for 14 entries) one turn later and in
    my own instrument. The index is the only stable identifier against a fixed source artifact.
    """
    p = os.path.join(REPO, source_path)
    if not os.path.isfile(p):
        raise InstrumentFailure("declared source does not exist: %s" % source_path)
    with open(p, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    fences = re.findall(r"```json\s*(.*?)```", text, re.S)
    if not fences:
        raise InstrumentFailure("declared source carries no fenced JSON: %s" % source_path)
    doc = json.loads(fences[0])
    rows = doc.get("rows") or []
    if not rows:
        raise InstrumentFailure("declared source's rows[] is empty")
    pop = {i for i, r in enumerate(rows)
           if isinstance(r.get("canonical"), str) and TOKEN_RE.search(r["canonical"])}
    return len(rows), pop


# ------------------------------------------------------------------ cores
def core_resolution(rec):
    c = ((rec or {}).get("resolution") or {})
    rows = list(c.get("rows") or [])
    bad, lines = [], []

    for k in ("source", "source_vintage", "how_enumerated", "drift_against_inherited"):
        if not (c.get(k) or "").strip():
            bad.append("resolution lacks %s" % k)
    for k in ("judged_rows", "population", "resolved", "carded"):
        if c.get(k) is None:
            bad.append("resolution lacks %s" % k)
    if bad:
        return False, lines + bad

    lines = ["source: %s" % _scrub(c["source"]),
             "source vintage: %s" % _scrub(c["source_vintage"])[:70],
             "judged rows: %s | population: %s" % (_scrub(c["judged_rows"]), _scrub(c["population"])),
             "RESOLVED %s + CARDED %s | rows carried: %d"
             % (_scrub(c["resolved"]), _scrub(c["carded"]), len(rows)),
             "drift against the inherited %d: %s" % (INHERITED, _scrub(c["drift_against_inherited"])[:60])]

    # (2) THE PARTITION MAY NOT BE DEFINED BY A TOKEN LIST.
    low = (c["how_enumerated"] or "").lower()
    named = [t for t in ("{system}", "{scope}", "{cadence}") if t in low]
    if len(named) >= 2 and "minus" not in low and "subtract" not in low:
        bad.append("how_enumerated defines the population by naming tokens (%s) with no subtraction: "
                   "R-38 names THREE tokens and the population carries NINE, so a token list is a "
                   "FORWARD LIST. CARDED is POPULATION MINUS RESOLVED." % _scrub(named))

    # (1) INDEPENDENT RE-DERIVATION FROM THE DECLARED SOURCE, COMPARED BY SET EQUALITY.
    try:
        judged, pop = population_from(c["source"])
    except InstrumentFailure as exc:
        return False, lines + ["the re-derivation could not run (%s) -- a failed retrieval RAISES and "
                               "is never an empty set" % _scrub(exc)]
    carried = {r.get("row_index") for r in rows if isinstance(r.get("row_index"), int)}
    lines.append("re-derived from the declared source: judged %d, population %d" % (judged, len(pop)))
    if c["judged_rows"] != judged:
        bad.append("judged_rows says %s; the source carries %d" % (_scrub(c["judged_rows"]), judged))
    if c["population"] != len(pop):
        bad.append("population says %s; the source yields %d" % (_scrub(c["population"]), len(pop)))
    missing = sorted(pop - carried)
    extra = sorted(carried - pop)
    if missing:
        bad.append("NOT DISPOSITIONED (%d in the population, absent from the record): %s"
                   % (len(missing), _scrub(missing[:4])))
    if extra:
        bad.append("DISPOSITIONED BUT OUTSIDE THE POPULATION (%d): %s"
                   % (len(extra), _scrub(extra[:4])))

    seen, tally = set(), {"RESOLVED": 0, "CARDED": 0}
    for r in rows:
        idx = r.get("row_index")
        cur = (r.get("current") or "").strip()
        d = (r.get("disposition") or "").strip()
        if not isinstance(idx, int):
            bad.append("a row carries no integer row_index -- the population is a MULTISET (1303 "
                       "rows, 630 distinct names) and the INDEX is its only stable key")
            continue
        if idx in seen:
            bad.append("row_index appears twice: %s" % _scrub(idx))
        seen.add(idx)
        if d not in DISPOSITIONS:
            bad.append("%s: disposition %s is outside %s"
                       % (_scrub(cur), _scrub(d or "(none)"), _scrub(DISPOSITIONS)))
            continue
        tally[d] += 1
        # (3) RESOLVED IS THE COSTLY CLASS: it asserts a measurement was taken.
        if d == "RESOLVED":
            if not (r.get("measured_from") or "").strip():
                bad.append("%s: RESOLVED with no measured_from -- RESOLVED asserts the substitution "
                           "was MEASURED FROM A DECLARED SOURCE, and a row that names none is an "
                           "inference wearing a measurement's label" % _scrub(cur))
        else:
            if not (r.get("owner") or "").strip():
                bad.append("%s: CARDED with no owner" % _scrub(cur))
            if not (r.get("reason") or "").strip():
                bad.append("%s: CARDED with no reason" % _scrub(cur))
    for k in DISPOSITIONS:
        if c[k.lower()] != tally[k]:
            bad.append("%s count says %s; the rows carry %d" % (k, _scrub(c[k.lower()]), tally[k]))
    if c["resolved"] + c["carded"] != len(rows):
        bad.append("the disposition arithmetic does not close against the rows carried")
    if not rows:
        bad.append("no rows carried: the population is not empty at any pin this round could cut at, "
                   "so an empty record is an enumeration failure rather than a result")
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


def _is_this_round(path, tag="r18"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def t1_resolution():
    ok, lines = core_resolution(_rec("EN-t-1"))
    return verdict(ok, "PASS-T1-RESOLUTION", "FAIL-T1-RESOLUTION", lines)


def r18_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R18-VINTAGE-FIELD",
                   "no round-18 record exists in this checkout: an empty population is REFUSED here, "
                   "never passed vacuously")
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
        ok, lines = core_vintage(rec, resolvable, ("check_en_r18.py", "R18_BASE.json"))
        ok_all = ok_all and ok
        out += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R18-VINTAGE-FIELD", "FAIL-R18-VINTAGE-FIELD", out)


def r18_stale_proofs():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R18-STALE-PROOFS",
                   "no round-18 record exists in this checkout: an empty population is REFUSED here")
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
    return verdict(ok_all, "PASS-R18-STALE-PROOFS", "FAIL-R18-STALE-PROOFS", out)


# ------------------------------------------------------------------ self-test
def arm(name, ok, note=""):
    print("  %-54s %s%s" % (name, "PASS" if ok else "FAIL", (" -- " + note) if note else ""))
    return ok


SRC = ("org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/"
       "NAMING_CENSUS_REPORT.r13.md")
HOW = ("read the ONE fenced JSON object's rows[] and took every row whose RAW canonical carries a "
       "literal token; CARDED is that population MINUS the RESOLVED set")


def _res_ok(judged, pop, **over):
    names = sorted(pop)
    rows = [{"row_index": i, "current": "name-%d" % i, "tokens": ["system"],
             "disposition": "CARDED", "measured_from": None,
             "owner": "1.0.0_SA_CTO", "reason": "pending a registry rule"} for i in names]
    c = {"source": SRC, "source_vintage": "built from the estate as of ...", "how_enumerated": HOW,
         "judged_rows": judged, "population": len(names),
         "drift_against_inherited": "NO DRIFT against 1303", "rows": rows,
         "resolved": 0, "carded": len(names)}
    c.update(over)
    return {"resolution": c}


def selftest_arms():
    ok = True
    print("SELFTEST -- every arm is driven from a SATISFYING record and from a MUTANT of it.")
    try:
        judged, pop = population_from(SRC)
    except InstrumentFailure as exc:
        print("  the declared source is unreadable (%s)" % _scrub(exc))
        return say("FAIL-ARMS-DISCRIMINATE", "the arms cannot be driven without the population")
    print("  live re-derivation: judged %d, population %d" % (judged, len(pop)))

    good = _res_ok(judged, pop)
    ok &= arm("POSITIVE-a-correct-all-CARDED-record-PASSES", core_resolution(good)[0],
              "carding is a disposition R-38 asks for by name, not a failure")

    mixed = _res_ok(judged, pop)
    mixed["resolution"]["rows"][0].update({"disposition": "RESOLVED",
                                           "measured_from": "NAMING_SCHEMA.json grade.placeholder",
                                           "owner": None, "reason": None})
    mixed["resolution"]["resolved"] = 1
    mixed["resolution"]["carded"] = len(pop) - 1
    ok &= arm("POSITIVE-a-MIXED-record-PASSES", core_resolution(mixed)[0],
              "the real answer is mixed and a bar admitting one class would force a lie")

    drop = _res_ok(judged, pop)
    drop["resolution"]["rows"] = drop["resolution"]["rows"][:-1]
    drop["resolution"]["carded"] = len(pop) - 1
    drop["resolution"]["population"] = len(pop) - 1
    ok &= arm("MUTANT-one-member-dropped", not core_resolution(drop)[0],
              "set equality catches an omission whose arithmetic closes")

    ok &= arm("MUTANT-population-inherited-not-re-derived",
              not core_resolution(_res_ok(judged, pop, population=INHERITED + 7))[0],
              "a number that disagrees with the declared source at ANY vintage")
    ok &= arm("MUTANT-partition-defined-by-a-TOKEN-LIST",
              not core_resolution(_res_ok(
                  judged, pop,
                  how_enumerated="took the rows carrying {system}, {scope} or {cadence}"))[0],
              "R-38 names 3 tokens; the population carries 9")
    ok &= arm("WIRING-a-token-list-WITH-a-subtraction-PASSES",
              core_resolution(_res_ok(
                  judged, pop,
                  how_enumerated="{system}/{scope}/{cadence} are resolved; CARDED is the population "
                                 "MINUS that set"))[0],
              "naming the tokens is fine; defining the population by them is not")

    noc = _res_ok(judged, pop)
    for r in noc["resolution"]["rows"]:
        r["reason"] = ""
    ok &= arm("MUTANT-CARDED-with-no-reason", not core_resolution(noc)[0])
    noo = _res_ok(judged, pop)
    for r in noo["resolution"]["rows"]:
        r["owner"] = ""
    ok &= arm("MUTANT-CARDED-with-no-owner", not core_resolution(noo)[0])

    nores = _res_ok(judged, pop)
    for r in nores["resolution"]["rows"]:
        r.update({"disposition": "RESOLVED", "measured_from": ""})
    nores["resolution"]["resolved"] = len(pop)
    nores["resolution"]["carded"] = 0
    ok &= arm("MUTANT-RESOLVED-with-no-measured_from", not core_resolution(nores)[0],
              "RESOLVED asserts a measurement; a row naming no source is an inference")

    ok &= arm("MUTANT-arithmetic-does-not-close",
              not core_resolution(_res_ok(judged, pop, resolved=99))[0])
    ok &= arm("MUTANT-no-drift-statement",
              not core_resolution(_res_ok(judged, pop, drift_against_inherited=""))[0])
    ok &= arm("MUTANT-source-does-not-exist",
              not core_resolution(_res_ok(judged, pop, source="does/not/exist.md"))[0],
              "a failed retrieval RAISES rather than reading as an empty population")
    ok &= arm("MUTANT-empty-record-is-REFUSED-not-vacuously-passed",
              not core_resolution(_res_ok(judged, set(), population=0, carded=0))[0])

    ok &= arm("POSITIVE-vintage-satisfiable", core_vintage(
        {"fixed_inputs_at_pin": {"a/check_en_r18.py": "c", "b/R18_BASE.json": "c"}}, True,
        ("check_en_r18.py", "R18_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-missing-one", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_en_r18.py": "c"}}, True,
        ("check_en_r18.py", "R18_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-unresolvable", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_en_r18.py": "c", "b/R18_BASE.json": "c"}}, False,
        ("check_en_r18.py", "R18_BASE.json"))[0])
    ok &= arm("POSITIVE-stale-empty-window-passes", core_stale([], {}, set())[0])
    ok &= arm("MUTANT-stale-set-inequality",
              not core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": []}}, {"p.json"})[0])
    ok &= arm("WIRING-stale-set-equality-passes",
              core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": ["p.json"]}},
                         {"p.json"})[0])

    print("  arms driven: 19 (4 POSITIVE, 3 WIRING, 12 mutant/other)")
    print("  NOT driven here, stated: proofs_at_risk's live git read -- exercised by the real arm.")
    return say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE")


CMDS = {"t1-resolution": t1_resolution, "r18-vintage-field": r18_vintage_field,
        "r18-stale-proofs": r18_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) != 2 or argv[1] not in CMDS:
        print("usage: %s {%s}" % (os.path.basename(argv[0]), "|".join(sorted(CMDS))))
        return 2
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
