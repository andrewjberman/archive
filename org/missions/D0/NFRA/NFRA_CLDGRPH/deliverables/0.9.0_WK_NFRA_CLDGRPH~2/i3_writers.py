#!/usr/bin/env python3
"""I3-AC1 -- NAME `OWNED_BY`'s other writer.

THE QUESTION. Round 8's CG-s-36 established BY SUBTRACTION that `OWNED_BY` has a writer
that is not the stitch fold: 0 occurrences across derive_stitch.py + derive_runner.py
against 232 live `S3Key -OWNED_BY-> S3_BUCKET` edges. Knowing THAT is not knowing WHAT,
and a remedy resting on an unnamed writer being benign is the shape this cell exists to
prevent. This names it, or says UNIDENTIFIED with the sweep's denominator.

THREE INSTRUMENTS, DELIBERATELY ON DIFFERENT PLANES (rule 22: a second seat's confirmation
via the first seat's method is repetition, not corroboration):

  A  REPOSITORY, rail plane -- `comp-find 'OWNED_BY' --files --all`. Supplies the
     REPOSITORY DENOMINATOR (files scanned, with its own printed exclusion floor) and the
     candidate set. Corpus resolution is a property of the CHECKOUT this runs in, so the
     run states its TREE and carries a positive control that only fires in this worktree.

  B  REPOSITORY, git-index plane -- an independent sweep over `git ls-files`, emission-
     classified. Different corpus definition (tracked-only) and different matcher, so it
     can DISAGREE with A; where it does, the disagreement is printed, not smoothed.

  C  LIVE PRODUCER PLANE -- the edge_type histogram of every payload under
     s3://opal-313476888478-globgrph/producers/, captured out-of-band (read-only) into
     i3_producer_payload_census.json with the listing that is its denominator. This is
     the DISCRIMINATING arm: it does not ask which file mentions the token, it asks which
     producer DECLARES the edges, and it either reconciles to 232 or it does not.

WHAT COUNTS AS A WRITER. A file that CONSTRUCTS or DECLARES an `OWNED_BY` edge that
reaches a folded graph artifact. A file that READS, MAPS, ASSERTS or DESCRIBES the type
is not a writer, and the classification of every candidate is printed -- a count whose
members are withheld cannot be checked.

BOUNDS, STATED RATHER THAN NARROWED.
  (1) Instrument B reads .py/.json/.jsonl/.yaml/.yml/.patch under 4 MB. Files above the
      cap and other extensions are EXCLUDED AND COUNTED. A writer in an excluded file is
      invisible to B -- which is exactly why A (whole corpus) supplies the denominator.
  (2) A writer that exists ONLY as deployed bytes and never in the repository cannot be
      seen by A or B. C is what covers that hole, at the payload grain.
  (3) The MS-family attribution is INFERRED, not measured: this run does not query the
      served graph. It is stated as inferred and the arithmetic remainder is printed.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE
while WS.name and not (WS / ".git").exists():
    WS = WS.parent

TERM = "OWNED_BY"
CONTROL_TOKEN = "I3TREECONTROLTOKENWK2CLDGRPH"
CONTROL_FILE = HERE / "i3_tree_control.txt"
CENSUS_CAPTURE = HERE / "i3_producer_payload_census.json"
LISTING_CAPTURE = HERE / "i3_s3_producers_listing.json"

EXTS = (".py", ".json", ".jsonl", ".yaml", ".yml", ".patch")
SIZE_CAP = 4_000_000

PAYLOAD_EMIT = re.compile(r'"edge_type"\s*:\s*"%s"' % TERM)
CODE_EMIT = re.compile(r'(?:append|_edge|edge|emit|add_edge)[^\n]{0,120}["\']%s["\']' % TERM)

# The classification, decided by READING each candidate that matched an emission shape.
# Cited file:line so a reader re-derives rather than believes.
CLASSIFIED = {
    "infra/aws/globgrph/ms_cloud_extract.py": (
        "WRITER-CODE",
        "emits `_edge(node['id'], f'ms:user:{owner}', 'OWNED_BY')` inside _crawl_drive -- "
        "the MS doc-cloud custody edge (MsDriveItem -> MS_USER). Folded by "
        "derive_runner.extract_ms_cloud, which returns the graph unchanged when MS is "
        "disabled (its default)."),
    "org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-A.storage_producer.json": (
        "WRITER-PAYLOAD",
        "producer='graphuni-storage', lane 0.8.0_AE_CloudComp~A, generated 2026-06-30. "
        "169 declared S3Key -OWNED_BY-> arn:aws:s3:::<bucket> edges."),
    "org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-A.storage_producer_phaseB.json": (
        "WRITER-PAYLOAD",
        "producer='graphuni-storage', Phase-B remainder, generated 2026-07-01. "
        "63 declared S3Key -OWNED_BY-> arn:aws:s3:::<bucket> edges."),
    "org/modules/graph/comp_coverage_check.py": (
        "READER",
        "`elif et == 'OWNED_BY':` in the roll-up resolver -- consumes the edge as the "
        "fine->coarse direction; its one payload-shaped hit is a self-test fixture."),
    "org/modules/graph/cse_schema.py": (
        "READER/MAPPER",
        "the CSE vocabulary map and map_cloudedge's target-typed resolver "
        "(OWNED_BY -> OWNS for an actor target, CONTAINS for a container target)."),
    ".tools/tool_index.py": (
        "INDEX/DESCRIPTION",
        "the tool index's edge-type catalogue. NOTE: it already NAMES the producer -- "
        "\"Producer=graphuni-storage (~A)\" -- which is why an emission-shaped census "
        "over CODE alone could not find what a description had recorded all along."),
    "org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/NFRA_MOTIF_P1_canonical_ab_catalog.py": (
        "READER",
        "motif catalogue: OWNED_BY appears inside Cypher WHERE clauses that MATCH it."),
    "infra/aws/globgrph/tests/test_ms_cloud_cert.py": (
        "TEST",
        "asserts the MS cert's behaviour around the OWNED_BY edge; emits nothing served."),
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~3/h4_fourth_point.py": (
        "MISSION-HARNESS",
        "a sibling worker's analysis script; not an estate producer."),
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_disagreement.py": (
        "MISSION-HARNESS",
        "a sibling worker's analysis script; not an estate producer."),
}
WRITER_KINDS = ("WRITER-CODE", "WRITER-PAYLOAD")


def sh(args, timeout=90):
    p = subprocess.run(args, capture_output=True, cwd=str(WS), timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def tree_kind() -> str:
    """A LINKED worktree carries `.git` as a FILE; the main tree carries it as a DIR."""
    return "WORKTREE" if (WS / ".git").is_file() else "MAIN"


def comp_find(pattern):
    rc, out, err = sh([sys.executable, ".tools/comp-find", pattern, "--files", "--all"])
    return rc, out, err


def parse_denominator(out: str):
    m = re.search(r"across\s+(\d+)\s+file\(s\)\s+scanned", out)
    return int(m.group(1)) if m else 0


def listed_paths(out: str):
    paths = []
    for line in out.splitlines():
        s = line.strip()
        if not s or s.startswith(("comp-find", "DENOMINATOR", "BANDS", "PAGE", "[", "MORE")):
            continue
        if line.startswith("    ") and not line.startswith("     "):
            paths.append(s.split(":")[0] if s.count(":") and " " not in s else s)
    return paths


def main() -> int:
    rel = str(HERE.relative_to(WS)).replace("\\", "/")
    print("I3-AC1 -- WHO ELSE WRITES OWNED_BY")
    print("  TREE        : %s" % str(WS).replace("\\", "/"))
    branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"])[1].strip()
    head = sh(["git", "rev-parse", "HEAD"])[1].strip()
    print("  BRANCH/HEAD : %s @ %s" % (branch, head))
    print("  ENVIRONMENT : local worktree; instrument C's bytes were captured OUT OF BAND by")
    print("                read-only AWS calls (list-objects-v2 + get-object) and are stored")
    print("                beside this script. THIS RUN MAKES NO NETWORK CALL.")
    print("  GRAIN       : A/B = repository files; C = producer PAYLOADS. Neither is the")
    print("                served graph: no arm here re-measures what round 8 measured.")
    print("")

    # ---- the tree positive control -------------------------------------------------------
    kind = tree_kind()
    if not CONTROL_FILE.exists():
        CONTROL_FILE.write_text(
            "I3 TREE POSITIVE CONTROL -- 0.9.0_WK_NFRA_CLDGRPH~2, CG-s-42.\n"
            "This file exists ONLY on branch wk-cldgrph-9-2. If the census below scans the\n"
            "MAIN tree instead of this worktree, this token cannot appear in its hits and the\n"
            "control reads DID-NOT-FIRE. It costs one file and it survives its own premise:\n"
            "the corpus resolver is a property of the checkout, and only this run can see that.\n"
            "TOKEN: " + CONTROL_TOKEN + "\n"
            "It also carries the census term once so the OWNED_BY sweep sees it: " + TERM + "\n",
            encoding="utf-8", newline="")
    crc, cout, cerr = comp_find(CONTROL_TOKEN)
    ctrl_paths = listed_paths(cout)
    ctrl_hit = any(p.endswith("i3_tree_control.txt") for p in ctrl_paths)
    if kind == "MAIN":
        control = "N/A-MAIN-TREE"
    else:
        control = "FIRED" if ctrl_hit else "DID-NOT-FIRE"
    print("  TREE POSITIVE CONTROL")
    print("    control file : %s/i3_tree_control.txt (branch-only)" % rel)
    print("    comp-find rc : %d, hits naming the control: %s" % (crc, ctrl_hit))
    print("    reading      : the corpus the rail scanned IS this checkout" if ctrl_hit
          else "    reading      : the rail did NOT scan this checkout -- every count below is void")
    print("")

    # ---- instrument A --------------------------------------------------------------------
    arc, aout, aerr = comp_find(TERM)
    denom = parse_denominator(aout)
    a_paths = [p for p in listed_paths(aout)]
    print("  INSTRUMENT A -- rail plane (comp-find '%s' --files --all), rc=%d" % (TERM, arc))
    dline = [ln for ln in aout.splitlines() if "DENOMINATOR" in ln]
    for ln in dline:
        print("   %s" % ln.strip())
    print("    COVERAGE   : corpus=all == tracked + untracked + gitignored MINUS the printed")
    print("                 ephemeral floor; the floor and the binary count are on that line.")
    print("    files naming the term: %d" % len(a_paths))

    # ---- instrument B --------------------------------------------------------------------
    tracked = [f for f in sh(["git", "ls-files", "-z"])[1].split("\0") if f]
    cand = [f for f in tracked if f.endswith(EXTS)]
    read_n = skipped_big = 0
    b_mention, b_emit = [], {}
    for f in cand:
        ap = WS / f
        try:
            if ap.stat().st_size > SIZE_CAP:
                skipped_big += 1
                continue
            txt = ap.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        read_n += 1
        if TERM not in txt:
            continue
        b_mention.append(f)
        pn, cn = len(PAYLOAD_EMIT.findall(txt)), len(CODE_EMIT.findall(txt))
        if pn or cn:
            b_emit[f] = (pn, cn)
    print("")
    print("  INSTRUMENT B -- git-index plane, emission-classified")
    print("    DENOMINATOR: %d tracked file(s); %d carry a scannable extension %s;"
          % (len(tracked), len(cand), ",".join(EXTS)))
    print("                 %d READ, %d EXCLUDED above the %d-byte cap (declared, not silent)."
          % (read_n, skipped_big, SIZE_CAP))
    print("    files naming the term: %d ; files matching an EMISSION shape: %d"
          % (len(b_mention), len(b_emit)))
    print("    A-vs-B: B is tracked-only, so B <= A by construction. B not in A: %s"
          % sorted(set(b_mention) - set(a_paths))[:5])

    # ---- classification ------------------------------------------------------------------
    print("")
    print("  CLASSIFICATION OF EVERY EMISSION-SHAPED CANDIDATE (%d), members printed:"
          % len(b_emit))
    writers = []
    unclassified = []
    for f in sorted(b_emit):
        pn, cn = b_emit[f]
        if f in CLASSIFIED:
            kindf, why = CLASSIFIED[f]
        else:
            kindf, why = "UNCLASSIFIED", "not read by this run"
            unclassified.append(f)
        if kindf in WRITER_KINDS:
            writers.append(f)
        print("    %-14s payload=%-4d code=%-4d %s" % (kindf, pn, cn, f))
        print("                   -> %s" % why)
    if unclassified:
        print("    WARN: %d candidate(s) UNCLASSIFIED -- the count below is a floor, not a total"
              % len(unclassified))

    # ---- instrument C: the discriminating arm --------------------------------------------
    print("")
    print("  INSTRUMENT C -- LIVE PRODUCER PLANE (captured; this run only reads the capture)")
    cap = json.loads(CENSUS_CAPTURE.read_text(encoding="utf-8"))
    listing = json.loads(LISTING_CAPTURE.read_text(encoding="utf-8"))
    keys = [o["Key"] for o in listing.get("Contents", [])]
    print("    capture      : %s (captured_at %s)" % (CENSUS_CAPTURE.name, cap["captured_at_utc"]))
    print("    DENOMINATOR  : %d of %d payload(s) under producers/ -- the listing beside it IS"
          % (cap["totals"]["payloads"], len(keys)))
    print("                   the denominator (%s)" % LISTING_CAPTURE.name)
    for row in cap["payloads"]:
        print("      %-42s producer=%-34s edges=%-6d STORED_IN=%-4d OWNED_BY=%d"
              % (row["local_basename"], row["producer"], row["edges_total"],
                 row["STORED_IN"], row["OWNED_BY"]))
    print("    TOTALS       : STORED_IN=%d  OWNED_BY=%d"
          % (cap["totals"]["STORED_IN"], cap["totals"]["OWNED_BY"]))
    by_prod = {}
    for row in cap["payloads"]:
        if row["OWNED_BY"]:
            by_prod[row["producer"]] = by_prod.get(row["producer"], 0) + row["OWNED_BY"]
    print("    OWNED_BY by producer: %s" % json.dumps(by_prod))

    # ---- the reconciliation --------------------------------------------------------------
    served_s3key_family = 232          # round 8 W1-S47, served plane, vintage 2026-09-10T12:24:50
    served_total = 6385                # same measurement, all OWNED_BY families
    payload_total = cap["totals"]["OWNED_BY"]
    reconciles = payload_total == served_s3key_family
    print("")
    print("  RECONCILIATION -- two planes, two instruments, one number")
    print("    round 8 (SERVED plane, projection query): S3Key -OWNED_BY-> S3_BUCKET = %d"
          % served_s3key_family)
    print("    this run (PRODUCER plane, payload bytes) : graphuni-storage declares       = %d"
          % payload_total)
    print("    AGREE=%s -- and the agreement DISCRIMINATES: had the 232 come from anywhere" % reconciles)
    print("    else, a payload census of every producer would not land on the same integer.")
    print("    UNRECONCILED REMAINDER: %d of %d served OWNED_BY edges are NOT S3Key-family."
          % (served_total - served_s3key_family, served_total))
    print("    Their writer is INFERRED (not measured here): ms_cloud_extract.py is the only")
    print("    estate emitter of an OWNED_BY edge onto an `ms:user:` target. This run does not")
    print("    query the served graph, so that attribution is stated as INFERRED and is not")
    print("    counted as a measurement.")

    # ---- the summary block ---------------------------------------------------------------
    named_producers = sorted(set(by_prod)) + ["ms-cloud-extract (code-plane, MS_USER family)"]
    print("")
    print("=" * 78)
    print("TREE_READ=%s" % kind)
    print("TREE_POSITIVE_CONTROL=%s" % control)
    print("REPOSITORY_DENOMINATOR=%d file(s)" % denom)
    print("  definition: files scanned by instrument A over corpus=all, its own exclusion")
    print("  floor printed on its DENOMINATOR line above. Instrument B's independent")
    print("  denominator is %d tracked file(s), %d read." % (len(tracked), read_n))
    print("OWNED_BY_WRITERS=%d" % len(writers))
    print("  definition: distinct ESTATE FILES that CONSTRUCT or DECLARE an OWNED_BY edge")
    print("  reaching a folded artifact. Readers, mappers, tests, indexes and mission")
    print("  harnesses are excluded and each exclusion is named above.")
    for w in writers:
        print("    writer file: %s" % w)
    print("OWNED_BY_NAMED_PRODUCERS=%d" % len(named_producers))
    for p in named_producers:
        print("    producer: %s" % p)
    print("")
    if writers:
        print("WRITER_NAMED printed")
        print("  THE OTHER WRITER IS `graphuni-storage` -- the NFRA_GRAPHUNI P1-A storage")
        print("  producer of lane 0.8.0_AE_CloudComp~A. It declares 169 + 63 = 232 S3Key")
        print("  -OWNED_BY-> arn:aws:s3:::<bucket> edges in")
        print("    org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-A.storage_producer.json")
        print("    org/projects/NFRA_GRAPHUNI/NFRA_GRAPHUNI.P1-A.storage_producer_phaseB.json")
        print("  served as producers/graphuni/storage_s3keys{,_phaseB}.json and re-read by")
        print("  derive_runner.ingest_graphuni_producers on EVERY derive (the call is")
        print("  UNCONDITIONAL; the flag-gated EXTRACT_PIPELINE_CLOUD replacement is default OFF).")
        print("  ITS MATERIALIZER IS NOT IN THE REPOSITORY: org/projects/NFRA_GRAPHUNI/")
        print("  storage_producer.py is UNTRACKED (10,137 B, CTO MATERIALIZER_CENSUS_20260827")
        print("  _REPO_PLANE.md:208). The PAYLOADS are tracked, which is why a repository")
        print("  census can name the writer at all -- and why bound (2) above is not academic.")
        print("  SECOND WRITER, DIFFERENT FAMILY: infra/aws/globgrph/ms_cloud_extract.py")
        print("  (MsDriveItem -OWNED_BY-> MS_USER), folded by extract_ms_cloud, MS-disabled")
        print("  by default. Its edges are NOT the 232.")
        print("  NOT ASSUMED BENIGN: graphuni-storage's payloads are FROZEN (last modified")
        print("  2026-06-30 / 2026-07-01) yet re-read every cycle, so its edges are re-created")
        print("  each derive from bytes nobody has regenerated in ten weeks. That is a fact")
        print("  about the writer, stated, not a judgement about whether it is safe.")
    else:
        print("WRITER=UNIDENTIFIED")
        print("  denominator: %d file(s) scanned (A), %d tracked read (B), %d payload(s) (C)"
              % (denom, read_n, cap["totals"]["payloads"]))

    ok = (denom > 0 and (control in ("FIRED", "N/A-MAIN-TREE")) and bool(writers)
          and reconciles and not unclassified)
    print("")
    print("SELF_CHECK=%s" % ("OK" if ok else "REVIEW"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
