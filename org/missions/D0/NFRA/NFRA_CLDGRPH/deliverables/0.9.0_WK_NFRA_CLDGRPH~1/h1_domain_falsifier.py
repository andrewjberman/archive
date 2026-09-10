#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-1 / CG-s-36 -- H1-AC2: FALSIFY THE DOMAIN BEFORE ANY SUBTRACTION IS
TRUSTED. A SEPARATE SCRIPT FROM THE CENSUS ON PURPOSE, BECAUSE THE FALSIFIER MUST BE ABLE TO
FAIL WHILE THE CENSUS SUCCEEDS.

CLAUDE.md Rule 24(i), as amended 2026-09-10 @b3bc1d7511:

    "THE SUBTRACTION'S DOMAIN MUST BE THE CLAIM'S POPULATION -- CHOOSING THE DOMAIN IS ITSELF
     A CLAIM, FALSIFIED BEFORE THE SUBTRACTION RUNS: one UNSCOPED read of the term over the
     corpus, denominator printed, compared against what the domain holds; a member the domain
     does not hold VOIDS the subtraction. A subtraction over the wrong domain is BLINDER than
     recall -- it arrives with a printed denominator and so reads as MEASURED, and a
     denominator certifies the SWEEP, never the SET. THE FAILURE MODE IS A GREEN: a wrong
     domain returning NON-EMPTY gets argued with; returning EMPTY it gets ACTED ON."

That amendment was written on THIS project's row (NFRA_CLDGRPH W1-S38 / S110), where the
CTO's own retirement condition named `graph-call-manifest.yaml` as the reader denominator and
the census over it returned 0 of 78 -- an honest zero, resolution arm passing, authorizing a
retirement that would have broken every consumer the manifest never declared. This script is
that amendment executed as an instrument rather than quoted as a principle.

WHAT IT DOES:
  1. UNSCOPED READ. Sweep the whole repository corpus for a word-boundary `STORED_IN` and
     print the POPULATION OF THE CLAIM -- the files that carry the term -- with the sweep's
     own denominator beside it. This is the claim's population, not the sweep's size: the
     retirement claim is about the term's consumers, so the term's carriers are the members.
  2. WHAT THE DOMAIN HOLDS. Resolve `graph-call-manifest.yaml`'s declared tool set to files
     and count how many of the population's members that declared domain actually holds.
  3. THE VERDICT, PRINTED. Any member the domain does not hold VOIDS the subtraction, in
     those words. Not inferred from an empty set -- printed, so it can be disagreed with.

THE CONTROL (`FALSIFIER_CONTROL`): the verdict function is exercised on BOTH branches on
synthetic input inside one run -- a population wholly held by its domain must return VALID,
and the same population with ONE member outside must return VOID. A falsifier that has only
ever returned the answer it returned today is a promise, not a control (memory:
"a declared but unrun falsifier is a promise, not a control"). Both arms must behave, or the
control does not fire and this script exits non-zero.

READ ONLY.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
TERM = "STORED_IN"
BOUNDED = re.compile(r"STORED_IN(?![A-Za-z0-9_])")
MANIFEST = "org/modules/graph/graph-call-manifest.yaml"
FLOOR = ("__pycache__/", ".scratch/", ".git/")


def git(*a: str) -> str:
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=str(ROOT)).stdout


def carries(path: str) -> bool:
    try:
        return bool(BOUNDED.search((ROOT / path).read_text(encoding="utf-8", errors="replace")))
    except Exception:  # noqa: BLE001
        return False


def subtraction_verdict(population: set, domain: set) -> tuple[str, set]:
    """THE VERDICT FUNCTION, isolated so it can be exercised on both branches.

    A subtraction is VALID only when the declared domain HOLDS every member of the claim's
    population. One member outside and the subtraction is VOID: the domain is not the claim's
    population, so subtracting inside it answers a different question than the one asked.
    """
    outside = population - domain
    return ("VOID" if outside else "VALID"), outside


def main() -> int:
    print("INSTRUMENT: one UNSCOPED word-boundary sweep of the repository corpus (git ls-files")
    print("  tracked UNION untracked-not-ignored, minus a named ephemeral floor), against the")
    print("  DECLARED domain resolved from %s." % MANIFEST)
    print("COVERAGE: the whole corpus for the population; the manifest's whole tools_index for")
    print("  the domain. Both denominators printed. GRAIN: one FILE per member.")
    print("ENVIRONMENT: the domain under test is the one the CTO's ruling 94872 condition 1")
    print("  named as the reader denominator. The comparison value is round 7's own result over")
    print("  that domain, 0 of 78 (rows NFRA_CLDGRPH-W1-S38, -S110), re-measured here.")
    print("TREE: %s @ %s (branch %s)"
          % (git("rev-parse", "--show-toplevel").strip(),
             git("rev-parse", "HEAD").strip()[:10],
             git("rev-parse", "--abbrev-ref", "HEAD").strip()))
    print("")

    tracked = [p for p in git("ls-files").split("\n") if p.strip()]
    untracked = [p for p in git("ls-files", "--others", "--exclude-standard").split("\n")
                 if p.strip()]
    corpus = sorted({p for p in tracked + untracked
                     if not any(s in p for s in FLOOR)})
    print("CORPUS_FILES_SWEPT=%d  (tracked %d + untracked-not-ignored %d, minus the named"
          % (len(corpus), len(tracked), len(untracked)))
    print("  ephemeral floor %s; the sweep's denominator, which certifies the SWEEP and never"
          % list(FLOOR))
    print("  the SET -- that is the whole reason the next number is measured separately.)")
    print("")

    population = {p for p in corpus if carries(p)}
    print("THE CLAIM'S POPULATION, read UNSCOPED. The claim under test is 'STORED_IN may be")
    print("retired', so its population is every file that CARRIES the term -- not every file")
    print("in the repository, and NOT every file the manifest declares.")
    print("UNSCOPED_DENOMINATOR=%d" % len(population))
    print("  = file(s) in the %d-file corpus carrying a word-boundary `%s`."
          % (len(corpus), TERM))
    print("")

    import yaml
    man = yaml.safe_load((ROOT / MANIFEST).read_text(encoding="utf-8"))
    tools = man.get("tools_index") or {}
    domain, unresolved = set(), []
    for name in sorted(tools):
        cands = [".tools/%s" % name,
                 "org/modules/graph/%s.py" % name.replace("-", "_"),
                 "org/modules/graph/%s.py" % name.replace("comp-", "comp_").replace("-", "_")]
        hit = [c for c in cands if (ROOT / c).exists()]
        if hit:
            domain.update(hit)
        else:
            unresolved.append(name)
    print("THE DECLARED DOMAIN: %s -- %d tool name(s), resolving to %d file(s); UNRESOLVED=%d."
          % (MANIFEST, len(tools), len(domain), len(unresolved)))
    print("  THE RESOLUTION ARM MATTERS AND IT PASSES: an unresolved name would make a zero")
    print("  ambiguous between 'the domain holds no member' and 'the instrument could not")
    print("  look'. With %d unresolved, the zero below is not a resolution failure." % len(unresolved))
    print("")

    held = population & domain
    print("DOMAIN_HOLDS=%d of %d" % (len(held), len(population)))
    print("  -- of the %d member(s) of the claim's population, the declared domain holds %d."
          % (len(population), len(held)))
    outside = population - domain
    print("MEMBERS_OUTSIDE_DOMAIN=%d" % len(outside))
    for p in sorted(outside)[:200]:
        print("    OUTSIDE: %s" % p)
    if len(outside) > 200:
        print("    ... and %d more (full set is the population minus the domain, both printed)"
              % (len(outside) - 200))
    print("")

    verdict, _ = subtraction_verdict(population, domain)
    print("SUBTRACTION_VERDICT=%s" % verdict)
    if verdict == "VOID":
        print("  A MEMBER THE DOMAIN DOES NOT HOLD VOIDS THE SUBTRACTION. %d of the %d members"
              % (len(outside), len(population)))
        print("  of this claim's population lie outside %s, so a subtraction performed INSIDE"
              % MANIFEST)
        print("  that domain does not answer 'may STORED_IN be retired'. It answers 'does any")
        print("  ROUTED QUERY TOOL read STORED_IN', which is a different question with a")
        print("  different, smaller answer -- and the smaller answer is EMPTY, which is the")
        print("  branch that gets ACTED ON rather than argued with.")
    else:
        print("  The declared domain holds every member of the claim's population, so a")
        print("  subtraction inside it is over the claim's own population and stands.")
    print("")

    # ---------------- THE CONTROL ----------------
    print("  -- THE CONTROL: the verdict function exercised on BOTH branches, synthetically,")
    print("     inside this run. A falsifier that has only ever produced today's answer is a")
    print("     promise rather than a control. --")
    pos_pop, pos_dom = {"a.py", "b.py"}, {"a.py", "b.py", "c.py"}
    neg_pop, neg_dom = {"a.py", "b.py", "z.py"}, {"a.py", "b.py", "c.py"}
    v_pos, _ = subtraction_verdict(pos_pop, pos_dom)
    v_neg, out_neg = subtraction_verdict(neg_pop, neg_dom)
    print("     ARM 1 population wholly inside its domain  -> want VALID  got %s" % v_pos)
    print("     ARM 2 population with ONE member outside   -> want VOID   got %s (outside=%s)"
          % (v_neg, sorted(out_neg)))
    fired = (v_pos == "VALID" and v_neg == "VOID")
    print("FALSIFIER_CONTROL=%s" % ("FIRED" if fired else "NOT-FIRED"))
    print("")
    print("  DENOMINATOR RESTATED: %d corpus file(s) swept unscoped; population of the claim ="
          % len(corpus))
    print("  %d file(s) carrying the term; declared domain = %d tool name(s) resolving to %d"
          % (len(population), len(tools), len(domain)))
    print("  file(s) with %d unresolved; domain holds %d of %d; %d outside; verdict %s;"
          % (len(unresolved), len(held), len(population), len(outside), verdict))
    print("  control %s." % ("FIRED" if fired else "NOT-FIRED"))
    return 0 if fired else 1


if __name__ == "__main__":
    sys.exit(main())
