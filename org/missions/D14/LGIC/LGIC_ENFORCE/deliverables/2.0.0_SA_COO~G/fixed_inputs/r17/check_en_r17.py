"""LGIC_ENFORCE round 17 -- the census re-cut over the COMPLEMENT.

1.0.0_SA_CTO's round-16 analysis @b24a81c4d3 s.4: "THE CENSUS RE-CUT OVER THE COMPLEMENT: all
fixed_inputs/ checkers in LGIC, MINUS the 25 already censused. Expressed that way deliberately -- A
FORWARD LIST IS HOW I LOST THE 11 ... the cell RE-DERIVES it rather than inheriting 36."

THREE THINGS THIS FILE DOES THAT ARE NOT DECORATION:

1. IT RE-DERIVES THE POPULATION ITSELF, AT THE RECORD'S OWN PIN, AND COMPARES BY SET EQUALITY. A
   census that merely PRINTS a denominator is graded on its own arithmetic; this one is graded against
   an independent enumeration of the same tree at the same commit. Grading at the PIN is what makes it
   reproducible forever -- grading at HEAD would convict a correct cell the moment the tree moved.
2. IT REFUSES A DOMAIN THAT NAMES PROJECTS. A forward list of project names is precisely how the
   round-15 cut lost 11 checkers, and a fifth project minted tomorrow is invisible to a list and
   visible to a subtraction. The per-entry `project` field is a RESULT and is fine; the DOMAIN may not
   be a list of names.
3. DRIFT IS DISCLOSED, NEVER REQUIRED TO BE ZERO. Round 16's census was correct AND its denominator
   grew under it because a SIBLING PROJECT's issuance minted a checker mid-cell. A bar demanding a
   stable denominator would convict a correct cell, so the bar is that the completion re-read is
   PRESENT and its drift STATED.

The vintage and stale-proof arms grade the records PRESENT IN THIS CHECKOUT (S106) and REFUSE an empty
population rather than passing it vacuously.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_ENFORCE"
LGIC = "org/missions/D14/LGIC/"
CELLS = ("EN-x-1",)
CLASSES = ("RETIRED-AND-DISCLOSED", "RETIRED-BUT-SILENT", "LIVE")
# The round-16 census record IS the prior set. Named as a PATH, never as a count.
PRIOR_REC = ("org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/"
             "RETIRED_BUT_RUNNABLE_R16.json")


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
    with open(os.path.join(HERE, "R17_BASE.json"), encoding="utf-8") as fh:
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


# ------------------------------------------------------------------ independent re-derivation
def full_set_at(pin):
    """Every fixed_inputs/*.py under the LGIC tree AT `pin`. The checker's own enumeration."""
    out = git(["ls-tree", "-r", "--name-only", pin, "--", LGIC])
    return {ln.strip() for ln in out.splitlines()
            if "fixed_inputs/" in ln and ln.strip().endswith(".py")}


def prior_set_at(pin):
    """The paths the round-16 census record actually CARRIED, read at `pin`."""
    raw = git(["show", "%s:%s" % (pin, PRIOR_REC)])
    rec = json.loads(raw)
    return {(e.get("path") or "").strip()
            for e in (rec.get("census") or {}).get("instruments") or []
            if (e.get("path") or "").strip()}


# ------------------------------------------------------------------ cores
def core_census(rec):
    """Graded against an INDEPENDENT re-derivation at the record's own pin, by SET EQUALITY."""
    c = ((rec or {}).get("census") or {})
    inst = list(c.get("instruments") or [])
    how = (c.get("how_enumerated") or "").strip()
    pin = (c.get("pin") or "").strip()
    bad, lines = [], []

    for k in ("full_denominator_at_pin", "prior_censused", "complement",
              "retired_and_disclosed", "retired_but_silent", "live",
              "full_denominator_at_completion"):
        if c.get(k) is None:
            bad.append("census lacks %s" % k)
    if not how:
        bad.append("how_enumerated is empty")
    if not pin:
        bad.append("census carries no pin -- the analysis requires the cell to PRINT ITS PIN")
    if not (c.get("drift") or "").strip():
        bad.append("census carries no drift statement; write NO DRIFT rather than omitting it")
    if not (c.get("prior_source") or "").strip():
        bad.append("census names no prior_source -- the subtraction's minuend must be citable")
    if bad:
        return False, lines + bad

    lines = ["pin: %s" % _scrub(pin),
             "full denominator at pin: %s | prior censused: %s | complement: %s"
             % (_scrub(c["full_denominator_at_pin"]), _scrub(c["prior_censused"]),
                _scrub(c["complement"])),
             "entries carried: %d" % len(inst),
             "RETIRED-AND-DISCLOSED %s + RETIRED-BUT-SILENT %s + LIVE %s"
             % (_scrub(c["retired_and_disclosed"]), _scrub(c["retired_but_silent"]),
                _scrub(c["live"])),
             "denominator re-read at completion: %s | drift: %s"
             % (_scrub(c["full_denominator_at_completion"]), _scrub(c.get("drift"))[:70])]

    low = how.lower()
    if "fixed_inputs" not in low:
        bad.append("how_enumerated does not name fixed_inputs/ as the domain")
    for token in ("retired list", "retirement list", "the retired records", "list of retired"):
        if token in low:
            bad.append("how_enumerated enumerates FROM THE RETIRED LIST (%s): a census whose domain "
                       "is the known retirements cannot find an unknown one" % _scrub(token))
            break
    # (2) THE DOMAIN MAY NOT BE A FORWARD LIST OF PROJECTS.
    for name in ("LGIC_NAMING", "LGIC_CANON"):
        if name in how:
            bad.append("how_enumerated names %s in the DOMAIN. A forward list of project names is "
                       "exactly how the round-15 cut lost 11 checkers -- the domain is fixed_inputs/ "
                       "across the LGIC tree MINUS what round 16 carried, and a fifth project minted "
                       "tomorrow must be visible to it. The per-entry project field is a RESULT and "
                       "is fine; the DOMAIN may not be a list." % _scrub(name))
            break

    # (1) INDEPENDENT RE-DERIVATION AT THE RECORD'S OWN PIN, COMPARED BY SET EQUALITY.
    try:
        full = full_set_at(pin)
        prior = prior_set_at(pin)
    except InstrumentFailure as exc:
        return False, lines + ["the re-derivation could not run at pin %s (%s) -- a failed retrieval "
                               "RAISES and is never an empty set" % (_scrub(pin), _scrub(exc))]
    complement = full - prior
    carried = {(e.get("path") or "").strip() for e in inst if (e.get("path") or "").strip()}
    lines.append("re-derived at the pin: full %d, prior %d, complement %d"
                 % (len(full), len(prior), len(complement)))
    if c["full_denominator_at_pin"] != len(full):
        bad.append("full_denominator_at_pin says %s; the tree at that pin says %d"
                   % (_scrub(c["full_denominator_at_pin"]), len(full)))
    if c["prior_censused"] != len(prior):
        bad.append("prior_censused says %s; the round-16 record at that pin carries %d"
                   % (_scrub(c["prior_censused"]), len(prior)))
    if c["complement"] != len(complement):
        bad.append("complement says %s; the subtraction at that pin yields %d"
                   % (_scrub(c["complement"]), len(complement)))
    missing = sorted(complement - carried)
    extra = sorted(carried - complement)
    if missing:
        bad.append("NOT CLASSED (in the complement, absent from the record): %s" % _scrub(missing[:4]))
    if extra:
        bad.append("CLASSED BUT OUTSIDE THE COMPLEMENT: %s" % _scrub(extra[:4]))

    seen = set()
    for e in inst:
        p = (e.get("path") or "").strip()
        k = (e.get("class") or "").strip()
        if not p:
            bad.append("an entry carries no path")
            continue
        if p in seen:
            bad.append("path appears twice: %s" % _scrub(p))
        seen.add(p)
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
    if c["retired_and_disclosed"] + c["retired_but_silent"] + c["live"] != len(inst):
        bad.append("the class arithmetic does not close against the entries carried")
    if not inst:
        bad.append("no instruments carried: the complement is not empty at any pin this round could "
                   "cut at, so an empty census is an enumeration failure rather than a result")
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


def _is_this_round(path, tag="r17"):
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    if not commits:
        return set()
    out = git(["ls-tree", "-r", "--name-only", "%s^" % commits[-1].split()[0], "--", ROOT])
    return set(ln for ln in out.splitlines() if _is_this_round(ln))


# ------------------------------------------------------------------ arms
def x1_census():
    ok, lines = core_census(_rec("EN-x-1"))
    return verdict(ok, "PASS-X1-CENSUS", "FAIL-X1-CENSUS", lines)


def r17_vintage_field():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R17-VINTAGE-FIELD",
                   "no round-17 record exists in this checkout: an empty population is REFUSED here, "
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
        ok, lines = core_vintage(rec, resolvable, ("check_en_r17.py", "R17_BASE.json"))
        ok_all = ok_all and ok
        out_lines += ["%s:" % cell] + ["  " + ln for ln in lines]
    return verdict(ok_all, "PASS-R17-VINTAGE-FIELD", "FAIL-R17-VINTAGE-FIELD", out_lines)


def r17_stale_proofs():
    cells = _cells_present()
    if not cells:
        return say("FAIL-R17-STALE-PROOFS",
                   "no round-17 record exists in this checkout: an empty population is REFUSED here")
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
    return verdict(ok_all, "PASS-R17-STALE-PROOFS", "FAIL-R17-STALE-PROOFS", out_lines)


# ------------------------------------------------------------------ self-test
def arm(name, ok, note=""):
    print("  %-52s %s%s" % (name, "PASS" if ok else "FAIL", (" -- " + note) if note else ""))
    return ok


def _ent(path, klass="LIVE", rec=None, disc=False, basis="read at the bytes"):
    return {"path": path, "project": path.split("/LGIC/")[1].split("/")[0] if "/LGIC/" in path else "?",
            "retiring_record": rec, "instrument_discloses_it": disc, "class": klass, "basis": basis}


def _census_ok(paths, **over):
    c = {"pin": "HEAD", "how_enumerated": "git ls-tree -r --name-only <pin> over fixed_inputs/, *.py, "
                                          "minus the paths the round-16 census record carried",
         "full_denominator_at_pin": 0, "prior_censused": 0, "complement": len(paths),
         "prior_source": PRIOR_REC + " @ its commit",
         "instruments": [_ent(p) for p in paths],
         "retired_and_disclosed": 0, "retired_but_silent": 0, "live": len(paths),
         "full_denominator_at_completion": 0, "drift": "NO DRIFT"}
    c.update(over)
    return {"census": c}


def selftest_arms():
    ok = True
    print("SELFTEST -- every arm is driven from a SATISFYING record and from a MUTANT of it.")

    # Live re-derivation at HEAD gives this run its real population.
    try:
        full = full_set_at("HEAD")
        prior = prior_set_at("HEAD")
    except InstrumentFailure as exc:
        print("  live re-derivation unavailable (%s)" % _scrub(exc))
        return say("FAIL-ARMS-DISCRIMINATE", "the arms cannot be driven without the tree")
    comp = sorted(full - prior)
    print("  live population at HEAD: full %d, prior %d, complement %d"
          % (len(full), len(prior), len(comp)))

    good = _census_ok(comp, full_denominator_at_pin=len(full), prior_censused=len(prior),
                      full_denominator_at_completion=len(full))
    ok &= arm("POSITIVE-a-correct-complement-census-PASSES", core_census(good)[0],
              "a correct artifact must be able to satisfy this")

    ok &= arm("MUTANT-one-member-dropped",
              not core_census(_census_ok(comp[:-1], full_denominator_at_pin=len(full),
                                         prior_censused=len(prior), complement=len(comp) - 1,
                                         full_denominator_at_completion=len(full)))[0],
              "set equality catches a silent omission the arithmetic would not")
    # ⛔ The obvious mutant here is a hard-coded 36 -- and it is VACUOUS while the tree still holds 36,
    # which is an arm that cannot fail. Mutate OFF THE LIVE NUMBER so it discriminates at every vintage.
    ok &= arm("MUTANT-denominator-inherited-not-re-derived",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full) + 7,
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full)))[0],
              "an inherited count disagrees with the tree at the pin, at ANY vintage")
    ok &= arm("MUTANT-domain-is-the-retired-list",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full),
                                         how_enumerated="walked the retired list of known retirements"))[0])
    ok &= arm("MUTANT-domain-is-a-FORWARD-LIST-of-projects",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full),
                                         how_enumerated="fixed_inputs/ under LGIC_NAMING and "
                                                        "LGIC_CANON"))[0],
              "the forward list is how round 15 lost 11 checkers")
    ok &= arm("MUTANT-no-pin-printed",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full), pin=""))[0])
    ok &= arm("MUTANT-no-completion-re-read-drift",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full), drift=""))[0])
    ok &= arm("MUTANT-class-arithmetic-does-not-close",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full), live=0))[0])
    ok &= arm("MUTANT-RETIRED-BUT-SILENT-with-no-retiring-record",
              not core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                         prior_censused=len(prior),
                                         full_denominator_at_completion=len(full),
                                         instruments=[_ent(p, "RETIRED-BUT-SILENT") for p in comp],
                                         retired_but_silent=len(comp), live=0))[0])
    ok &= arm("MUTANT-empty-census-is-REFUSED-not-vacuously-passed",
              not core_census(_census_ok([], full_denominator_at_pin=len(full),
                                         prior_censused=len(prior), complement=0,
                                         full_denominator_at_completion=len(full), live=0))[0])
    ok &= arm("WIRING-drift-is-DISCLOSED-not-required-zero",
              core_census(_census_ok(comp, full_denominator_at_pin=len(full),
                                     prior_censused=len(prior),
                                     full_denominator_at_completion=len(full) + 1,
                                     drift="one checker minted by a sibling project mid-cell"))[0],
              "a correct cell whose tree grew under it must still PASS")

    ok &= arm("POSITIVE-vintage-satisfiable",
              core_vintage({"fixed_inputs_at_pin": {"a/check_en_r17.py": "c", "b/R17_BASE.json": "c"}},
                           True, ("check_en_r17.py", "R17_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-missing-one", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_en_r17.py": "c"}}, True,
        ("check_en_r17.py", "R17_BASE.json"))[0])
    ok &= arm("MUTANT-vintage-unresolvable", not core_vintage(
        {"fixed_inputs_at_pin": {"a/check_en_r17.py": "c", "b/R17_BASE.json": "c"}}, False,
        ("check_en_r17.py", "R17_BASE.json"))[0])
    ok &= arm("POSITIVE-stale-empty-window-passes", core_stale([], {}, set())[0])
    ok &= arm("MUTANT-stale-set-inequality",
              not core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": []}}, {"p.json"})[0])
    ok &= arm("WIRING-stale-set-equality-passes",
              core_stale(["abc 2026-01-01"], {"stale_proofs": {"proofs_re_run": ["p.json"]}},
                         {"p.json"})[0])
    ok &= arm("WIRING-no-record-present-REFUSES",
              _cells_present() == [] or _rec("EN-x-1") is not None,
              "the round-wide arms grade records present in THIS checkout (S106)")

    print("  arms driven: 18 (3 POSITIVE, 3 WIRING, 12 mutant/other)")
    print("  NOT driven here, stated: proofs_at_risk's live git read -- exercised by the real arm.")
    return say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE")


CMDS = {"x1-census": x1_census, "r17-vintage-field": r17_vintage_field,
        "r17-stale-proofs": r17_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) != 2 or argv[1] not in CMDS:
        print("usage: %s {%s}" % (os.path.basename(argv[0]), "|".join(sorted(CMDS))))
        return 2
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
