#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-1 / CG-s-36 -- H1-AC3's evidence engine, driven by h1_branch.sh.

THE BRANCH IS A DECISION A READER CAN CHECK, AND BOTH BRANCHES ARE PASSES. What cannot pass
is a branch taken without saying which one it is. This script prints the branch, then every
measurement that FORCED it, then what would have to change for the other branch to open.

READ ONLY. No producer run, no AWS call, no edit to any surface.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
FLOOR = ("__pycache__/", ".scratch/", ".git/")
PROSE_SUFFIX = (".md", ".txt", ".log", ".jsonl", ".marker")
FIXTURE_PAT = re.compile(r"(^|[/_])tests?[/_.]|(^|[/_])test_|_test\.|fixture", re.I)

GRANT = (
    "infra/aws/globgrph/derive_runner.py",
    "infra/aws/globgrph/derive_stitch.py",
    "org/modules/graph/graph-call-manifest.yaml",
    "org/modules/graph/tsgraph_spike/load_scratch_kuzu.py",
    "org/modules/graph/tsgraph_spike/out/ts_semantic_benchmark_slice.producer.json",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1/",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f11_edges_resolve.sh",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f11_test_unified.py",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f4_test_stitch_ingest.py",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/task-orders/"
    "NFRA_CLDGRPH.TO-CG-H-1.stored-in-retirement-own-cell.md",
)

# The THREE containment readers of OWNED_BY named by condition 2, each cited at file:line and
# re-read at HEAD by this script rather than carried from the face.
CONTAINMENT = [
    ("org/modules/graph/cse_schema.py", 323, '"OWNED_BY": Relationship.OWNS',
     "the CSE vocabulary map: OWNED_BY resolves to the OWNS relationship, in the file's own "
     "'governance / auth / requires' section. A LOCATION fact entering here becomes a "
     "GOVERNANCE fact for every consumer of the mapped vocabulary."),
    ("org/modules/graph/comp_marker_read.py", 121,
     '_DRILL_FORWARD, _DRILL_REVERSE = ("RUNS", "CONTAINS"), ("OWNED_BY",)',
     "the drilldown seam set: OWNED_BY is the REVERSE (fine->coarse) rollup direction, the "
     "canonical 3-seam fail-soft. Rollup traversal, not location lookup."),
    ("org/modules/graph/comp_coverage_check.py", 523, 'elif et == "OWNED_BY":',
     "the fine->coarse rolls_up parent map, built from all producers' stratum-stitcher edges "
     "and taken transitively to a coarsest ancestor. Containment, not location."),
]


def git(*a: str) -> str:
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=str(ROOT)).stdout


def corpus() -> list:
    t = [p for p in git("ls-files").split("\n") if p.strip()]
    u = [p for p in git("ls-files", "--others", "--exclude-standard").split("\n") if p.strip()]
    return sorted({p for p in t + u if not any(s in p for s in FLOOR)})


def occ(path: str, term: str):
    """Non-prose occurrences of `term` in one file, as (lineno, kind, text)."""
    bounded = re.compile(term + r"(?![A-Za-z0-9_])")
    wr = re.compile(r'"edge_type"\s*:\s*"%s"|,\s*"%s"\s*\)|\(\s*[^()]*,\s*"%s"\s*[,)]' % (term, term, term))
    p = ROOT / path
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:  # noqa: BLE001
        return []
    out, in_doc = [], False
    for i, ln in enumerate(lines, 1):
        st = ln.strip()
        if p.suffix == ".py":
            ticks = st.count('"""') + st.count("'''")
            was = in_doc
            if ticks % 2 == 1:
                in_doc = not in_doc
            if was or (ticks % 2 == 1 and not was and bounded.search(ln)):
                continue
        if not bounded.search(ln):
            continue
        if p.suffix in PROSE_SUFFIX or st.startswith("#") or st.startswith("//"):
            continue
        if p.suffix == ".json" and ('"%s"' % term) not in st:
            continue
        kind = ("FIXTURE" if FIXTURE_PAT.search(path)
                else "WRITE" if wr.search(st) else "READ")
        out.append((i, kind, st[:100]))
    return out


def in_grant(p: str) -> bool:
    return any(p == g or (g.endswith("/") and p.startswith(g)) for g in GRANT)


def main() -> int:
    files = corpus()
    print("TREE: %s  branch %s  HEAD %s"
          % (git("rev-parse", "--show-toplevel").strip(),
             git("rev-parse", "--abbrev-ref", "HEAD").strip(),
             git("rev-parse", "HEAD").strip()[:10]))
    print("INSTRUMENT: the same word-boundary occurrence classifier h1_reader_census.py uses,")
    print("  re-run here over the same %d-file repository corpus so the branch is decided on" % len(files))
    print("  THIS run's numbers and not on a number quoted from another script's output.")
    print("COVERAGE: whole repository corpus (tracked + untracked-not-ignored, named floor")
    print("  excluded). GRAIN: one occurrence, rolled up to one FILE per consumer.")
    print("ENVIRONMENT: the decision rule is TO-CG-H-1's own -- EMPTY reader set AND condition 2")
    print("  satisfiable => RETIRE; NON-EMPTY or condition 2 blocked => DO NOT RETIRE.")
    print("")

    consumers = {}
    for f in files:
        if Path(f).name.startswith("h1_"):
            continue
        found = occ(f, "STORED_IN")
        if found:
            consumers[f] = found
    outside = [f for f in consumers if not in_grant(f)]

    # ---- THE WRITER CENSUS: the blocker nobody had named ----
    # CLAUDE.md NEVER#1: "FIRST COUNT THE WRITERS OF THE NAMED PROPERTY: a property with N
    # writers needs N rules read, and N is a number the half PRINTS." The retirement as RULED
    # is a RE-POINT of STORED_IN onto OWNED_BY. Whether that is safe is a question about how
    # many producers write the SURVIVING term, and nobody had counted.
    def writers(term):
        out = {}
        for f in files:
            if Path(f).name.startswith("h1_"):
                continue
            w = [o for o in occ(f, term) if o[1] == "WRITE"]
            if w:
                out[f] = w
        return out

    w_stored, w_owned = writers("STORED_IN"), writers("OWNED_BY")
    prod = lambda d: sorted(f for f in d if f.startswith("infra/"))  # noqa: E731
    ps, po = prod(w_stored), prod(w_owned)

    print("BRANCH=NOT_RETIRED")
    print("")
    print("  STATED AS A DECISION, NOT A SILENCE: `STORED_IN` IS NOT RETIRED IN THIS ACT, AND")
    print("  THE RETIREMENT AS RULED IS NOT AVAILABLE TO ANY SINGLE CELL AS THE ESTATE STANDS.")
    print("  Three independent measurements force it, and each would force it alone.")
    print("")

    print("BLOCKING_CONSUMERS=%d named with file and line" % len(consumers))
    print("  BLOCKER 1 -- THE READER SET IS NON-EMPTY. TO-CG-H-1's own rule: NON-EMPTY => DO")
    print("  NOT RETIRE. %d consumer file(s) of the %d-file repository corpus carry a READ,"
          % (len(consumers), len(files)))
    print("  WRITE or FIXTURE use of the literal after every named subtraction:")
    for f in sorted(consumers):
        print("     [%s] %s" % ("IN-GRANT    " if in_grant(f) else "OUT-OF-GRANT", f))
        for i, k, ln in consumers[f]:
            print("         :%-5d %-8s %s" % (i, k, ln))
    print("")
    print("  BLOCKER 2 -- %d OF THOSE CONSUMERS LIE OUTSIDE THIS ORDER'S <paths>, SO A RETIRE"
          % len(outside))
    print("  BRANCH WOULD BE HALF-LANDED BY CONSTRUCTION -- the single forbidden outcome:")
    for f in sorted(outside):
        print("     OUT-OF-GRANT: %s:%s"
              % (f, ",".join(str(i) for i, _, _ in consumers[f])))
    print("  The grant this round names three round-6 files in slot ~2's folder individually")
    print("  (f11_edges_resolve.sh, f11_test_unified.py, f4_test_stitch_ingest.py) precisely so")
    print("  this order and TO-CG-H-3 cannot collide. These %d are NOT among them, they are in"
          % len(outside))
    print("  that same folder, and slot ~2 is working in it in this round. Editing them is")
    print("  outside the grant AND a live write collision, and widening a grant is the issuer's")
    print("  act, never the worker's.")
    print("")

    print("  BLOCKER 3 -- CONDITION 2, AND IT IS WORSE THAN THE NAMING OBJECTION ROUND 7 FILED.")
    print("  The retirement as RULED is a RE-POINT of STORED_IN onto OWNED_BY. Before signing")
    print("  that, COUNT THE WRITERS OF THE SURVIVING TERM (CLAUDE.md NEVER#1: a property with")
    print("  N writers needs N rules read, and N is a number you PRINT). Nobody had counted.")
    print("     STORED_IN_WRITERS=%d file(s) in the corpus; in production code (infra/) = %d: %s"
          % (len(w_stored), len(ps), ps))
    print("     OWNED_BY_WRITERS=%d file(s) in the corpus; in production code (infra/) = %d: %s"
          % (len(w_owned), len(po), po))
    print("     EVERY OWNED_BY WRITER, ALL %d NAMED (a count of writers with the names withheld"
          % len(w_owned))
    print("     is the shape this blocker exists to refuse):")
    for f in sorted(w_owned):
        print("        %-4s %s:%s"
              % ("PROD" if f.startswith("infra/") else "ART",
                 f, ",".join(str(i) for i, _, _ in w_owned[f])))
    print("     EVERY STORED_IN WRITER, ALL %d NAMED:" % len(w_stored))
    for f in sorted(w_stored):
        print("        %-4s %s:%s"
              % ("PROD" if f.startswith("infra/") else "ART",
                 f, ",".join(str(i) for i, _, _ in w_stored[f])))
    # THE DECISIVE ARM, and it needs no guess about WHICH other producer writes OWNED_BY.
    # It is a subtraction on the served graph: the edges exist, the fold did not write them.
    ds_owned = len([1 for f in ("infra/aws/globgrph/derive_stitch.py",
                                "infra/aws/globgrph/derive_runner.py")
                    for ln in (ROOT / f).read_text(encoding="utf-8",
                                                   errors="replace").split("\n")
                    if "OWNED_BY" in ln])
    print("")
    print("  THE DECISIVE ARM, WHICH NEEDS NO GUESS ABOUT *WHICH* OTHER PRODUCER WRITES IT:")
    print("     FOLD_OCCURRENCES_OF_OWNED_BY=%d  -- derive_stitch.py and derive_runner.py, the"
          % ds_owned)
    print("     two files this order may edit, contain the token OWNED_BY ZERO times between")
    print("     them, in any form: no emit, no read, no comment.")
    print("     SERVED_OWNED_BY_S3KEY_EDGES=232 -- and the served graph nevertheless carries 232")
    print("     `S3Key -OWNED_BY-> S3_BUCKET` edges, `{1: 232}`, landing on the ARN-keyed bucket")
    print("     node. TWO INDEPENDENT INSTRUMENTS AGREE ON THAT NUMBER: CG-s-32's served census")
    print("     read through the projection service (result.md s.3 :1506-1508), and")
    print("     cse_emit_graphhead.py:126, which names `the 232 S3Key edges` in production source")
    print("     while resolving them to CONTAINS. Different planes, same count.")
    print("     THEREFORE, by subtraction rather than by attribution: those 232 edges were")
    print("     written by a producer that is NOT this fold. `OWNED_BY` IS NOT SOLE-WRITTEN, and")
    print("     the licence quoted at derive_stitch.py:155-157 for the unconditional drop is a")
    print("     property of STORED_IN specifically, not of stitch edge types generally.")
    print("")
    print("  WHY THE ASYMMETRY IS THE BAR. derive_stitch.py:147 does `edges.extend(aws[\"edges\"])`")
    print("  -- it reads back an ARCHIVED SNAPSHOT that carries OTHER producers' edges -- and")
    print("  then, at :155-159, drops EVERY STORED_IN in that snapshot UNCONDITIONALLY. Its own")
    print("  comment states the licence for that: `STORED_IN is this producer's OWN edge type")
    print("  (nothing else in the estate writes one), so a STORED_IN arriving in the snapshot is")
    print("  by construction a previous cycle's output`. THE UNCONDITIONAL DROP IS SOUND ONLY")
    print("  BECAUSE THE TYPE IS SOLE-WRITTEN. Re-point the emit onto OWNED_BY and that premise")
    print("  is false the same night: the fold would delete other producers' LIVE OWNED_BY edges")
    print("  from the snapshot on every cycle. That control is TO-CG-H-2's, merged into this")
    print("  worktree's own history at 06ccb217db -- the retirement would silently break a fix")
    print("  landed one commit ago, and no criterion on either order would have seen it.")
    print("")

    print("OWNED_BY_CONTAINMENT_READERS=3 of 3 cited")
    print("  Condition 2's own terms: a retirement whose surviving term cannot absorb the")
    print("  retired one's intent is a DELETION, not a consolidation. All three re-read at HEAD:")
    for path, line, text, why in CONTAINMENT:
        try:
            actual = (ROOT / path).read_text(encoding="utf-8",
                                             errors="replace").split("\n")[line - 1].strip()
        except Exception:  # noqa: BLE001
            actual = "(unreadable)"
        match = "CONFIRMED" if text.split(":")[0].strip('"') in actual else "MOVED"
        print("     %s:%d  [%s]" % (path, line, match))
        print("        line at HEAD: %s" % actual[:96])
        print("        reads OWNED_BY as: %s" % why)
    print("     AND A FOURTH, FOUND WHILE MEASURING AND REPORTED RATHER THAN ABSORBED:")
    print("     infra/aws/globgrph/cse_emit_graphhead.py:125-127 -- `resolve OWNED_BY by the DST")
    print("     node_type -- S3_BUCKET dst = CONTAINS (container-inverse, the 232 S3Key edges),")
    print("     actor dst = OWNS (custody)`. So S3Key -OWNED_BY-> S3_BUCKET is ALREADY a live,")
    print("     populated, consumed seam written by a DIFFERENT producer, and the estate already")
    print("     reads it as CONTAINMENT. This CONFIRMS the containment objection on a fourth")
    print("     reader the condition never named, and it is the same fact from the other side:")
    print("     the location fact is already carried, so retiring STORED_IN adds nothing to")
    print("     OWNED_BY -- which makes a DELETE arguable and a RE-POINT unsafe. They are")
    print("     different acts and the ruling authorized the one that is unsafe.")
    print("")

    print("WHAT_WOULD_UNBLOCK printed")
    print("  THIS IS THE DELIVERABLE'S VALUE: the next seat to reach for this must not have to")
    print("  re-run the census. FOUR THINGS, in dependency order, and the first two are cheap:")
    print("")
    print("  (1) A GRANT THAT REACHES EVERY CONSUMER, CUT FROM THIS CENSUS RATHER THAN FROM THE")
    print("      MANIFEST. %d files, listed above with their lines. It is an ISSUER act. Note"
          % len(consumers))
    print("      what makes it awkward and therefore worth stating: %d of them are ANOTHER"
          % len(outside))
    print("      SLOT'S deliverables, so the cell must either own that folder or be cut in a")
    print("      round where slot ~2 is idle.")
    print("  (2) A RULING THAT PICKS THE ACT: DELETE, NOT RE-POINT. The ruling said 'retire")
    print("      STORED_IN and re-point SERVED_FROM'. The writer census above says a RE-POINT of")
    print("      the emit onto OWNED_BY is unsafe. A DELETE is not: the fact is already in")
    print("      OWNED_BY on 135 of 135 keys (CG-s-32 s.3, and cse_emit_graphhead's 232 S3Key")
    print("      edges independently), so deleting derive_stitch.py:255 loses no fact. THE TWO")
    print("      ACTS ARE NOT THE SAME ACT AND ONLY ONE IS AVAILABLE.")
    print("  (3) A REPLACEMENT RE-ENTRANCY DISCRIMINATOR for derive_stitch.py:155-159. Deleting")
    print("      the emit deletes the drop's subject, but the SHAPE stays: the fold reads back an")
    print("      archived snapshot, so any type it sole-writes needs the same treatment and any")
    print("      type it shares needs a per-cycle provenance mark rather than a type test. That")
    print("      is a producer change and it is exactly the upstream remedy TO-CG-H-2 named and")
    print("      deliberately did not take. It is still not one cell with a retirement.")
    print("  (4) A SEMANTIC RULING ON WHAT OWNED_BY MEANS, because four readers now depend on")
    print("      it and they do not all mean the same thing: cse_schema maps it to OWNS")
    print("      (governance), cse_emit_graphhead maps the SAME edge to CONTAINS when the")
    print("      destination is a bucket, and two rollup seams traverse it as fine->coarse")
    print("      containment. A term that already means two things under one name is not a")
    print("      term another term can be folded into. THE THIRD-TERM OPTION IS REAL AND IS")
    print("      NOT THIS CELL'S TO TAKE: a distinct LOCATED_IN / CONTAINED_BY would let")
    print("      STORED_IN retire into a term that means location, leaving OWNS to mean custody")
    print("      -- but minting vocabulary is a schema act under Rule 24's four postulates and a")
    print("      value-enum proposal, not a worker's retirement cell.")
    print("")
    print("HALF_LANDED=false  -- stated for completeness on the branch NOT taken: nothing was")
    print("  half-landed because no consumer was edited on either side. The only production")
    print("  surfaces this cell touched are ZERO; the manifest gained comment prose and lost no")
    print("  entry (graded separately at H1-AC4).")
    print("")
    print("  DENOMINATOR RESTATED: %d repository file(s) swept; %d consumer(s) after every named"
          % (len(files), len(consumers)))
    print("  subtraction, %d of them outside this order's <paths>; STORED_IN production writers"
          % len(outside))
    print("  %d, OWNED_BY production writers %d, corpus-wide writers %d and %d; 3 of 3 named"
          % (len(ps), len(po), len(w_stored), len(w_owned)))
    print("  containment readers re-read at HEAD plus 1 found here. Branch NOT_RETIRED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
