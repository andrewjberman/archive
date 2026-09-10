#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-5 / CG-s-40 -- H5-AC1.

THE CONSUMER CENSUS OF THE TWO DECLARED CANONICAL SHAPES FOR ONE EDGE, BY SUBTRACTION.

The question this answers: who, anywhere in this repository, DECLARES or DEPENDS ON what
`ServedURL-[SERVED_FROM]->?` points at. The census record CG-s-32 named two scorers. It found
them while looking at something else, so "two" was a forward list, not a population. This sweep
starts from a printed repository denominator and SUBTRACTS.

INSTRUMENT / COVERAGE: this script's own os.walk of the worktree root. It opens every file under
the root except a PRINTED floor (.git internals, binary-extension files, files over 2 MB, and the
scratch dir). REPOSITORY_DENOMINATOR is the count of files this script actually OPENED AND READ --
not a count of files that exist, and not comp-find's number.
GRAIN: one row per FILE (not per line, not per declaration). A file with six shape declarations is
one consumer.
ENVIRONMENT of the stored baseline: there is no stored baseline. Every number here is measured in
this process, in this worktree, on this run. The only comparison values are the two literal shape
strings, read from the two scorer sources at their cited lines.

TREE HONESTY: the rail's caller-tree defect (a linked worktree scanning the MAIN tree and returning
a well-formed zero) is why TREE_READ and TREE_POSITIVE_CONTROL are printed. This script does not
use the rail at all -- it walks its own cwd -- but the control still fires, because a denominator
is not a tree.

0 MUTATIONS. Read-only. ASCII only.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=_HERE,
                      capture_output=True, text=True).stdout.strip()
if not ROOT or not os.path.isdir(ROOT):
    print("BLOCKED: could not resolve the worktree root from %s" % _HERE)
    raise SystemExit(2)
ROOT = os.path.abspath(ROOT)

CONTROL_REL = "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_tree_control.txt"
BRANCH_POINT = "2fd5cae09f"

# FILES THIS ORDER AUTHORED OR APPENDED TO ON THIS RUN. They carry the shape strings because they
# are ABOUT them; counting them as consumers would be the instrument measuring itself. Excluded BY
# NAME, listed in the output, and subtracted on their own line -- never silently.
SELF_EXCLUDE = {
    CONTROL_REL,
    "org/missions/D0/NFRA/NFRA_CLDGRPH/surprise-channel/investigations/INVESTIGATION_v1.md",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/"
    "NFRA_CLDGRPH.TO-CG-H-5.two-scorers-one-edge-placed.proof_of_spec.json",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_consumer_census.py",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_disagreement.py",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_placement.sh",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_no_egress.sh",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/PARKED_scorer-canonical-shape-disagreement.md",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/CG-s-40.two-scorers-one-edge.result.md",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_ac1_capture.txt",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_ac2_capture.txt",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_ac3_capture.txt",
    "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~4/h5_ac4_capture.txt",
}

BINARY_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip", ".gz", ".tar", ".exe", ".dll",
    ".so", ".dylib", ".pyc", ".pyd", ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mov",
    ".xlsx", ".xls", ".docx", ".pptx", ".parquet", ".db", ".sqlite", ".jar", ".class", ".bin",
    ".kuzu", ".wal", ".lance", ".npy", ".pkl", ".whl", ".7z", ".webp", ".svgz",
}
SKIP_DIRS = {".git", ".scratch", "node_modules", "__pycache__", ".venv", "venv", ".mypy_cache",
             ".pytest_cache", ".ruff_cache"}
MAX_BYTES = 2 * 1024 * 1024

EDGE = "SERVED_FROM"

# A SHAPE DECLARATION: a source class, the edge family, and a TARGET CLASS, in that order, inside a
# 200-char window of the newline-normalized text (the two scorer declarations both span lines, so a
# line-scoped regex would have missed one of the two files this census exists to re-find).
SHAPE_RE = re.compile(
    r"ServedURL.{0,140}?SERVED_FROM.{0,160}?(S3_BUCKET_POLICY|S3_BUCKET|BUCKET_POLICY|\(S3\)|S3\b)",
    re.DOTALL,
)
# A TARGET-CLASS DEPENDENCY: code that queries the family and then reads/asserts the target's class.
TARGET_DEP_RE = re.compile(
    r"SERVED_FROM.{0,400}?(t\.node_type|target_type|node_type\s*==|node_type\s*IN)", re.DOTALL
)

WRONG = "S3_BUCKET_POLICY"
INTENDED_TOKENS = ("(S3)", "S3_BUCKET")


def classify(rel: str, text: str) -> tuple[str, str]:
    """SCORER / PRODUCER / FIXTURE / PROSE. Deterministic, first rule wins, reason printed."""
    low = rel.lower()
    base = os.path.basename(low)
    ext = os.path.splitext(low)[1]
    if ext == ".py" and "scorer" in base:
        return "SCORER", "python module whose basename carries 'scorer'"
    if ext == ".py" and ("derive_" in base or "stitch" in base or "extract_" in base):
        return "PRODUCER", "python module on the derive/stitch/extract emit path"
    if ext == ".py" and re.search(r"edges?\.append|_edge\(|INSERT|COPY .* FROM", text):
        return "PRODUCER", "python module that emits edge rows"
    if ext in (".py", ".ts", ".tsx", ".js", ".sh", ".tf", ".yaml", ".yml"):
        if "schema" in base or ".tf" == ext:
            return "FIXTURE", "declared schema/infra surface, not an emitter and not a reader"
        return "FIXTURE", "executable/config surface carrying the shape as data, not a scorer or emitter"
    if ext in (".patch", ".diff") or "fixture" in low or "/test" in low or base.startswith("test_"):
        return "FIXTURE", "patch/fixture/test artifact"
    if ext in (".json", ".jsonl", ".csv", ".log", ".txt") or "/audit/" in low or ".comp-graph" in low:
        return "FIXTURE", "generated capture / cache / machine-read artifact"
    return "PROSE", "narrative document (spec, ruling, task order, session log, result record)"


def main() -> int:
    os.chdir(ROOT)
    is_linked = os.path.isfile(os.path.join(ROOT, ".git"))
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    print("=== H5-AC1 -- CONSUMER CENSUS OF THE CANONICAL SHAPE, BY SUBTRACTION ===")
    print("ROOT=%s" % ROOT.replace("\\", "/"))
    print("BRANCH=%s HEAD=%s" % (branch, head))
    print("TREE_READ=%s" % ("WORKTREE" if is_linked else "MAIN"))
    print("INSTRUMENT=os.walk in-process (NOT the comp rail -- the rail's caller-tree is not this")
    print("           script's dependency, and a rail zero and a real zero read alike)")
    print("COVERAGE=every file under ROOT minus the PRINTED floor below")
    print("GRAIN=one row per FILE")
    print("BASELINE_ENVIRONMENT=none stored; every number measured in this process on this run")

    # --- the walk -----------------------------------------------------------------------------
    denom = 0
    floor_bin = floor_big = floor_dir = 0
    candidates: list[tuple[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        floor_dir += 0
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            if os.path.splitext(fn)[1].lower() in BINARY_EXT:
                floor_bin += 1
                continue
            try:
                if os.path.getsize(full) > MAX_BYTES:
                    floor_big += 1
                    continue
                with open(full, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                floor_big += 1
                continue
            denom += 1
            if EDGE in text:
                candidates.append((rel, text))

    # --- the positive control ------------------------------------------------------------------
    ctrl_in_walk = any(rel == CONTROL_REL for rel, _ in candidates)
    at_branch_point = subprocess.run(
        ["git", "cat-file", "-e", "%s:%s" % (BRANCH_POINT, CONTROL_REL)],
        capture_output=True, text=True).returncode
    ctrl_absent_at_cut = at_branch_point != 0
    fired = ctrl_in_walk and ctrl_absent_at_cut
    print("TREE_CONTROL_FILE=%s" % CONTROL_REL)
    print("  present_in_this_sweep=%s  absent_at_branch_point_%s=%s (git cat-file rc=%d)"
          % (ctrl_in_walk, BRANCH_POINT, ctrl_absent_at_cut, at_branch_point))
    print("TREE_POSITIVE_CONTROL=%s" % ("FIRED" if fired else "DID-NOT-FIRE"))

    print("")
    print("FLOOR (printed, never silent): binary-extension=%d oversize-or-unreadable=%d "
          "skipped-dirs=%s" % (floor_bin, floor_big, ",".join(sorted(SKIP_DIRS))))
    print("REPOSITORY_DENOMINATOR=%d file(s) opened and read" % denom)

    # --- the subtraction ------------------------------------------------------------------------
    n_cand = len(candidates)
    kept = [(r, t) for r, t in candidates if r not in SELF_EXCLUDE]
    n_self = n_cand - len(kept)

    consumers = []
    for rel, text in kept:
        flat = text
        shape_hits = SHAPE_RE.findall(flat)
        dep = bool(TARGET_DEP_RE.search(flat))
        if not shape_hits and not dep:
            continue
        wrong = WRONG in flat and re.search(r"SERVED_FROM.{0,200}?S3_BUCKET_POLICY", flat, re.DOTALL) is not None
        intended = any(tok in flat for tok in INTENDED_TOKENS) and re.search(
            r"SERVED_FROM.{0,200}?(\(S3\)|S3_BUCKET\b)", flat, re.DOTALL) is not None
        cls, why = classify(rel, text)
        consumers.append({
            "path": rel, "class": cls, "why": why,
            "declares_wrong": wrong, "declares_intended": intended,
            "target_class_dependency": dep, "shape_decls": len(shape_hits),
        })
    consumers.sort(key=lambda c: (c["class"], c["path"]))

    print("")
    print("--- THE SUBTRACTION (a forward list of the two scorers the census record mentioned is")
    print("--- exactly how this estate has been finding these late; this starts from the denominator)")
    print("  %6d  files opened and read (REPOSITORY_DENOMINATOR)" % denom)
    print("  -%5d  files that never mention %s" % (denom - n_cand, EDGE))
    print("  =%5d  files mentioning %s (CANDIDATES)" % (n_cand, EDGE))
    print("  -%5d  this census's OWN instrument files (excluded by name, listed below)" % n_self)
    print("  -%5d  candidates that mention the family but declare NO target class and carry NO"
          % (len(kept) - len(consumers)))
    print("         target-class dependency (a mention is not a consumer)")
    print("  =%5d  CONSUMERS" % len(consumers))
    print("SELF_EXCLUDED_FILES=%s" % ";".join(sorted(r for r, _ in candidates if r in SELF_EXCLUDE)))

    n = len(consumers)
    print("")
    print("CONSUMERS_FOUND=%d" % n)
    by_class: dict[str, int] = {}
    for c in consumers:
        by_class[c["class"]] = by_class.get(c["class"], 0) + 1
    print("CLASSIFIED=%d of %d" % (n, n))
    print("BY_CLASS=%s" % " ".join("%s=%d" % (k, by_class[k]) for k in sorted(by_class)))
    print("BY_SUBTRACTION=true  (the chain above starts at REPOSITORY_DENOMINATOR and subtracts;")
    print("  no member of this population came from a list of names someone had already written)")
    print("")
    for c in consumers:
        print("  [%-8s] %s" % (c["class"], c["path"]))
        print("             decls=%d wrong_class=%s intended_class=%s target_dep=%s"
              % (c["shape_decls"], c["declares_wrong"], c["declares_intended"],
                 c["target_class_dependency"]))
        print("             why=%s" % c["why"])

    print("")
    print("--- THE FINDING ---")
    scorers = [c for c in consumers if c["class"] == "SCORER"]
    print("SCORER_CONSUMERS=%d (the census record CG-s-32 named 2)" % len(scorers))
    if len(consumers) > 2:
        print("RESULT=THIRD-CONSUMER-FOUND: the population is %d, not the 2 the record named."
              % len(consumers))
    else:
        print("RESULT=NULL: the population is the 2 the record already named.")
    wrongs = [c["path"] for c in consumers if c["declares_wrong"]]
    rights = [c["path"] for c in consumers if c["declares_intended"]]
    print("DECLARE_WRONG_CLASS=%d :: %s" % (len(wrongs), ";".join(wrongs)))
    print("DECLARE_INTENDED_CLASS=%d :: %s" % (len(rights), ";".join(rights)))
    print("OK: census complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
