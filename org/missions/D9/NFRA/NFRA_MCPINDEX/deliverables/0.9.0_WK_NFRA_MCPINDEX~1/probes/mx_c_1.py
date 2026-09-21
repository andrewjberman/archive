#!/usr/bin/env python3
"""Probe for NFRA_MCPINDEX.TO-MX-c-1 (cell MX-c-1) -- criteria MXC1-AC1 .. MXC1-AC7.

Usage: py -3.12 mx_c_1.py AC<n>

Each handler prints its measurement (instrument, UTC vintage, denominator where a census is
involved) and then exactly one line:
  VERDICT: PASS-MXC1-AC<n>
  VERDICT: FAIL-MXC1-AC<n> <reason>

AC7 is a judgment criterion (graded by 3.0.0_SA_CVO at L9, cell_refs has no <invocation>); if
invoked directly here it prints its own text and evidence pointers and emits NO verdict line
(a judgment row carries no verdict -- PROOF_OF_SPEC.schema.json `judgment`).
"""
from __future__ import annotations

import datetime
import io
import os
import re
import subprocess
import sys

REPO = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
).stdout.strip()
REPO = REPO.replace("/", os.sep)

EMIT_REL = os.path.join("workflows", "atom_decomposition", "emit_catalog_v02.py")
CAT_REL = os.path.join("infra", "aws", "ec2", "opal-gateway", "app", "refs", "DATA_CATALOG.yaml")
EMIT = os.path.join(REPO, EMIT_REL)
CAT = os.path.join(REPO, CAT_REL)

# The cell's cut base (this worker's identity line: "cut from CLOUD @4a475fe055"). Fixed so the
# AC5 diff check is reproducible at any point after this cell's own commit, not just pre-commit.
BASE_COMMIT = "4a475fe055"

ASSIGN_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=.*DATA_CATALOG\.yaml")
DISCLAIM_RE = re.compile(r"(?i)never\s+(touch|writ)")
# scoped variant for AC2/AC5: a disclaimer ABOUT the live catalog, not any "never touch" in the
# file (e.g. an unrelated served-portal-key comment at :709) -- must also name DATA_CATALOG.
CATALOG_DISCLAIM_RE = re.compile(r"(?i)(?=.*never\s+(?:touch|writ))(?=.*data_catalog)")


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_ls_files():
    out = subprocess.run(["git", "-C", REPO, "ls-files"], capture_output=True, text=True, check=True)
    return [ln for ln in out.stdout.splitlines() if ln]


def read_lines(path):
    with io.open(path, encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def candidates_and_writers():
    """AC1's census: every tracked .py file containing the literal 'DATA_CATALOG.yaml' string
    (the candidate set), then, within each, every write-call (open(...,'w'...), .write_text(,
    shutil.copy/move) whose target variable was itself assigned from a right-hand side
    containing that same literal (so the write call need not repeat the literal itself, as in
    emit_catalog_v02.py's `OUT = os.path.join(OUT_DIR, "DATA_CATALOG.yaml")` then
    `io.open(OUT, "w", ...)`)."""
    files = git_ls_files()
    candidates = []
    for rel in files:
        if not rel.endswith(".py"):
            continue
        p = os.path.join(REPO, rel.replace("/", os.sep))
        if not os.path.isfile(p):
            continue
        try:
            lines = read_lines(p)
        except Exception:
            continue
        if not any("DATA_CATALOG.yaml" in ln for ln in lines):
            continue
        candidates.append((rel, lines))

    writers = []
    for rel, lines in candidates:
        varnames = set()
        for ln in lines:
            m = ASSIGN_RE.match(ln)
            if m:
                varnames.add(m.group(1))
        if not varnames:
            continue
        for i, ln in enumerate(lines, start=1):
            for var in varnames:
                ve = re.escape(var)
                if re.search(r"(?:^|[.\s(])open\(\s*%s\s*,\s*[\"']w" % ve, ln):
                    writers.append((rel, var, i, ln))
                elif re.search(r"\b%s\.write_text\(" % ve, ln):
                    writers.append((rel, var, i, ln))
                elif re.search(r"shutil\.(?:copy2?|copyfile|move)\([^)]*\b%s\b" % ve, ln):
                    writers.append((rel, var, i, ln))
    return files, candidates, writers


def ac1():
    files, candidates, writers = candidates_and_writers()
    print("INSTRUMENT: python code census over `git ls-files` (tracked files only), repo=%s" % REPO)
    print("VINTAGE (UTC, read time): %s" % utcnow())
    print("DENOMINATOR (tracked files scanned): %d" % len(files))
    print("CANDIDATE .py FILES containing the literal 'DATA_CATALOG.yaml' (denominator %d of %d tracked):"
          % (len(candidates), len(files)))
    for rel, _lines in candidates:
        print("  CANDIDATE: %s" % rel)
    print("WRITE-CALLS found (open(VAR,'w'...) / VAR.write_text( / shutil.copy|move(...,VAR) where VAR was "
          "assigned from a literal containing 'DATA_CATALOG.yaml') -- denominator %d:" % len(writers))
    for rel, var, lineno, ln in writers:
        print("  WRITE-CALL: %s:%d  var=%s  %s" % (rel, lineno, var, ln.strip()))
    print("VERDICT: PASS-MXC1-AC1")


def ac2():
    files, candidates, writers = candidates_and_writers()
    print("INSTRUMENT: same census as AC1, re-run; printing each writer's own bytes at its write call, "
          "and any line in that file matching a disclaim pattern (case-insensitive 'never touch|writ').")
    print("VINTAGE (UTC): %s" % utcnow())
    if not writers:
        print("VERDICT: FAIL-MXC1-AC2 no writer found by the AC1 census -- nothing to print bytes for")
        return
    by_file = {}
    for rel, var, lineno, ln in writers:
        by_file.setdefault(rel, []).append((var, lineno, ln))
    for rel, hits in by_file.items():
        p = os.path.join(REPO, rel.replace("/", os.sep))
        lines = read_lines(p)
        for var, lineno, _ln in hits:
            print("WRITE-CALL BYTES -- %s:%d: %s" % (rel, lineno, lines[lineno - 1]))
        found_disclaim = False
        for i, ln in enumerate(lines, start=1):
            if CATALOG_DISCLAIM_RE.search(ln):
                print("DISCLAIM-LINE BYTES -- %s:%d: %s" % (rel, i, ln))
                found_disclaim = True
        if not found_disclaim:
            l5 = lines[4] if len(lines) >= 5 else "(file has fewer than 5 lines)"
            print("DISCLAIM-LINE BYTES -- %s: no line currently matches the disclaim pattern; module "
                  "docstring line 5 currently reads -- %s:5: %s" % (rel, rel, l5))
    print("VERDICT: PASS-MXC1-AC2")


def ac3():
    files, candidates, writers = candidates_and_writers()
    live_norm = os.path.normcase(os.path.normpath(CAT))
    print("INSTRUMENT: same census as AC1; a writer TARGETS THE LIVE PATH if importing its module and "
          "reading the write-call's variable attribute resolves (os.path.normpath) to %s" % CAT_REL)
    print("VINTAGE (UTC): %s" % utcnow())
    print("WRITERS FOUND: %d" % len(writers))
    if len(writers) == 0:
        print("VERDICT: FAIL-MXC1-AC3 REFUSED -- zero writers found by the census, not one")
        return
    if len(writers) > 1:
        for rel, var, lineno, ln in writers:
            print("  WRITER: %s:%d var=%s" % (rel, lineno, var))
        print("VERDICT: FAIL-MXC1-AC3 REFUSED -- %d writers found, not exactly one" % len(writers))
        return
    rel, var, lineno, ln = writers[0]
    if rel != EMIT_REL.replace(os.sep, "/"):
        print("VERDICT: FAIL-MXC1-AC3 REFUSED -- the one writer found is %s, not the emitter" % rel)
        return
    # resolve the writer's own target by importing the module (side-effect-free: main() is
    # guarded by `if __name__ == "__main__"`) and reading its OUT attribute directly.
    sys.path.insert(0, os.path.dirname(EMIT))
    import importlib
    if "emit_catalog_v02" in sys.modules:
        del sys.modules["emit_catalog_v02"]
    mod = importlib.import_module("emit_catalog_v02")
    resolved = os.path.normcase(os.path.normpath(getattr(mod, var)))
    print("RESOLVED TARGET (module attribute %s.%s): %s" % (rel, var, getattr(mod, var)))
    print("LIVE PATH (this cell's grain): %s" % CAT)
    if resolved != live_norm:
        print("VERDICT: FAIL-MXC1-AC3 REFUSED -- resolved target %s != live path %s" % (resolved, live_norm))
        return
    print("MATCH: resolved target == live path")
    print("VERDICT: PASS-MXC1-AC3")


def ac4():
    print("INSTRUMENT: grant-boundary read of this cell's <paths> block against what AC4 requires to exercise.")
    print("VINTAGE (UTC): %s" % utcnow())
    print("<paths> GRANTED to 0.9.0_WK_NFRA_MCPINDEX~1 for MX-c-1 (task order NFRA_MCPINDEX.TO-MX-c-1):")
    print("  workflows/atom_decomposition/emit_catalog_v02.py")
    print("  org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md")
    print("  (plus this worker's own deliverables folder, per the worker face)")
    print("AC4 REQUIRES writing, at minimum:")
    print("  %s (the served/live catalog AC4 calls 'the served file' -- CAT)" % CAT_REL)
    print("  an emitter INPUT under workflows/atom_decomposition/runs/<unit>/<stamp>/rectangle.final.certified.json"
          " (a resolved-substrate source; see lift_catalog_v02.py resolve_substrates()/scan_unit()) to make the "
          "'one reversible change to an emitter input' the criterion names")
    print("Neither path is in the <paths> grant. Bound (worker face BOUNDS): 'A path you need that is not named "
          "is a BLOCKING surprise row on that criterion -- never an override.' Bound 9: a criterion that cannot "
          "be satisfied as written is REFUSED and reported with its measurement, never repaired, widened or met "
          "by another route (redirecting OUT to a scratch path would not exercise the NAMED writer against the "
          "NAMED live path, which is what AC3/AC4 both require).")
    print("Filed: NFRA_MCPINDEX-W1-S1 (class BLOCKING) in "
          "org/missions/D9/NFRA/NFRA_MCPINDEX/surprise-channel/investigations/INVESTIGATION_v1.md")
    print("VERDICT: FAIL-MXC1-AC4 REFUSED -- exercising the named writer against the live path requires writing "
          "%s and a workflows/atom_decomposition/runs/ input file, neither granted by this cell's <paths>; "
          "filed as BLOCKING row NFRA_MCPINDEX-W1-S1, not overridden" % CAT_REL)


def ac5():
    print("INSTRUMENT: `git diff` of %s against this cell's fixed cut base %s (robust whether run "
          "pre-commit or post-commit), plus a direct read of the current docstring bytes." % (EMIT_REL, BASE_COMMIT))
    print("VINTAGE (UTC): %s" % utcnow())
    stat = subprocess.run(
        ["git", "-C", REPO, "diff", "--stat", BASE_COMMIT, "--", EMIT_REL],
        capture_output=True, text=True,
    )
    print("git diff --stat %s -- %s:" % (BASE_COMMIT, EMIT_REL))
    print(stat.stdout.strip() or "(empty -- no diff against base)")
    if stat.returncode != 0:
        print("VERDICT: FAIL-MXC1-AC5 git diff --stat failed rc=%d stderr=%s" % (stat.returncode, stat.stderr.strip()))
        return
    stat_lines = [ln for ln in stat.stdout.strip().splitlines() if ln.strip()]
    files_touched = [ln for ln in stat_lines if "|" in ln]
    if len(files_touched) != 1 or EMIT_REL.replace(os.sep, "/") not in files_touched[0]:
        print("VERDICT: FAIL-MXC1-AC5 --stat names %d file(s), expected exactly 1 (%s)"
              % (len(files_touched), EMIT_REL))
        return
    diff0 = subprocess.run(
        ["git", "-C", REPO, "diff", "-U0", BASE_COMMIT, "--", EMIT_REL],
        capture_output=True, text=True,
    )
    print("git diff -U0 %s -- %s:" % (BASE_COMMIT, EMIT_REL))
    print(diff0.stdout)
    hunk_headers = re.findall(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", diff0.stdout, re.M)
    if len(hunk_headers) != 1:
        print("VERDICT: FAIL-MXC1-AC5 %d hunks in the diff, expected exactly 1 (the docstring hunk)"
              % len(hunk_headers))
        return
    old_start, old_n, new_start, new_n = hunk_headers[0]
    new_start_i = int(new_start)
    new_n_i = int(new_n) if new_n else 1
    if new_start_i < 1 or (new_start_i + max(new_n_i, 1) - 1) > 10:
        print("VERDICT: FAIL-MXC1-AC5 the sole hunk touches lines outside 1-10 (+%s,%s)" % (new_start, new_n))
        return
    lines = read_lines(EMIT)
    print("CURRENT docstring lines 1-10 of %s:" % EMIT_REL)
    for i in range(1, 11):
        print("  :%d: %s" % (i, lines[i - 1] if i - 1 < len(lines) else ""))
    print("CURRENT :38-43 (the ONE CATALOG HOME comment + OUT_DIR/OUT) for comparison:")
    for i in range(38, 44):
        print("  :%d: %s" % (i, lines[i - 1] if i - 1 < len(lines) else ""))
    line5 = lines[4] if len(lines) >= 5 else ""
    if CATALOG_DISCLAIM_RE.search(line5) or DISCLAIM_RE.search(line5):
        print("VERDICT: FAIL-MXC1-AC5 line 5 still reads as a disclaimer: %r" % line5)
        return
    if "WRITES" not in line5.upper() and "WRITE" not in line5.upper():
        print("VERDICT: FAIL-MXC1-AC5 line 5 does not state the emitter writes the live file: %r" % line5)
        return
    print("VERDICT: PASS-MXC1-AC5")


def ac6():
    print("INSTRUMENT: direct read of %s header line 3." % CAT_REL)
    print("VINTAGE (UTC): %s" % utcnow())
    if not os.path.isfile(CAT):
        print("VERDICT: FAIL-MXC1-AC6 %s does not exist" % CAT_REL)
        return
    lines = read_lines(CAT)
    if len(lines) < 3:
        print("VERDICT: FAIL-MXC1-AC6 %s has fewer than 3 lines" % CAT_REL)
        return
    line3 = lines[2]
    print("%s:3: %s" % (CAT_REL, line3))
    if "emit_catalog_v02.py" not in line3:
        print("VERDICT: FAIL-MXC1-AC6 header line 3 does not name the writer: %r" % line3)
        return
    print("VERDICT: PASS-MXC1-AC6")


def ac7():
    print("MXC1-AC7 is a JUDGMENT criterion (cell_refs='MX-c-1', no <invocation> in the task order); it is "
          "graded by 3.0.0_SA_CVO at L9, never self-graded here. No PASS/FAIL verdict line follows.")
    print("Record for the CVO: the cell's writer finding is s.1 falsifier 2 + s.11 finding 1 of "
          "org/missions/D9/NFRA/NFRA_MCPINDEX/decompositions/NFRA_MCPINDEX_DECOMP.md, mechanically "
          "reproduced by MXC1-AC1/AC2/AC3 above, and the corrected docstring (MXC1-AC5) + unchanged catalog "
          "header (MXC1-AC6) are the two carriers a reader with only those three objects would have.")


HANDLERS = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6, "AC7": ac7}


def main(argv):
    if len(argv) != 2 or argv[1] not in HANDLERS:
        sys.stderr.write("usage: mx_c_1.py AC1|AC2|AC3|AC4|AC5|AC6|AC7\n")
        return 2
    HANDLERS[argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
