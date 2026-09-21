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


RECT_REL = os.path.join("workflows", "atom_decomposition", "runs", "portal-page-macro",
                         "20260811T1940Z", "rectangle.final.certified.json")
RECT = os.path.join(REPO, RECT_REL)
MARKER = " [MXC1-AC4-EXERCISE]"


def _read_bytes(path):
    with io.open(path, "rb") as f:
        return f.read()


def _write_bytes(path, data):
    # explicit byte-for-byte restore -- NEVER `git checkout --` / `git clean` (bound; row
    # NFRA_MCPINDEX-W1-S3 crossed this once already).
    with io.open(path, "wb") as f:
        f.write(data)


def _sha256(data):
    import hashlib
    return hashlib.sha256(data).hexdigest()


def _git_diff_stat(rel):
    r = subprocess.run(["git", "-C", REPO, "diff", "--stat", "--", rel], capture_output=True, text=True)
    return r.stdout.strip()


def _run_emitter():
    r = subprocess.run([sys.executable, EMIT], cwd=REPO, capture_output=True, text=True, timeout=90)
    return r.returncode, r.stdout, r.stderr


def _find_value_span(text, entity_id, field):
    """Byte-exact span of a JSON string VALUE for cells[field].value under the given entity_id,
    found by substring scan (never a full re-serialize, so every OTHER byte in the file is
    provably untouched by construction -- not just by re-diffing)."""
    i = text.find('"%s"' % entity_id)
    if i < 0:
        raise ValueError("entity_id %r not found" % entity_id)
    j = text.find('"%s"' % field, i)
    if j < 0:
        raise ValueError("field %r not found under entity %r" % (field, entity_id))
    prefix = '"value": "'
    k = text.find(prefix, j)
    if k < 0:
        raise ValueError("no \"value\": \" after field %r" % field)
    k += len(prefix)
    end = k
    bslash = chr(92)
    while True:
        end = text.find('"', end)
        if end < 0:
            raise ValueError("unterminated JSON string value")
        if text[end - 1] != bslash:
            break
        end += 1
    return k, end


def ac4():
    print("INSTRUMENT: exercise the named writer (AC3's resolved write-call, reached via "
          "emit_catalog_v02.py's main()) once at the cell's HEAD with one reversible change to an "
          "emitter input (RECT), diffing the served file (CAT) before/after by SHA-256 and by "
          "`git diff`, then reverting RECT to its saved original bytes and re-running to confirm the "
          "served file's SHA-256 returns to the pre-change value. Grant: AMENDMENT (issuer, "
          "2026-09-21, CTO ruling @f1c469829c/@de8bf648cd) adds CAT and RECT to this cell's <paths>.")
    print("VINTAGE (UTC): %s" % utcnow())
    print("RECT (emitter input): %s" % RECT_REL)
    print("CAT  (served file):   %s" % CAT_REL)

    pre_stat_cat = _git_diff_stat(CAT_REL)
    pre_stat_rect = _git_diff_stat(RECT_REL)
    print("PRE-EXERCISE git diff --stat (expect empty, both at HEAD): CAT=%r RECT=%r" % (pre_stat_cat, pre_stat_rect))
    if pre_stat_cat or pre_stat_rect:
        print("VERDICT: FAIL-MXC1-AC4 worktree not clean at HEAD before the exercise starts -- "
              "CAT stat=%r RECT stat=%r" % (pre_stat_cat, pre_stat_rect))
        return

    cat_orig = _read_bytes(CAT)
    rect_orig = _read_bytes(RECT)
    sha_cat_orig = _sha256(cat_orig)
    print("SAVED original bytes (in-process, never committed): CAT sha256=%s (%d bytes); "
          "RECT sha256=%s (%d bytes)" % (sha_cat_orig, len(cat_orig), _sha256(rect_orig), len(rect_orig)))

    # Run A -- baseline: writer run once, input UNCHANGED (this establishes the pre-change served
    # bytes at this exact HEAD; the committed CAT already carries this same content per AC5/AC6,
    # modulo the built_at_git_head vintage stamp, which does not move again below since no commit
    # happens between runs A/B/C).
    rc_a, out_a, err_a = _run_emitter()
    print("RUN A (baseline, input unchanged) rc=%d" % rc_a)
    print(out_a.strip().splitlines()[-1] if out_a.strip() else "(no stdout)")
    if rc_a != 0:
        print("VERDICT: FAIL-MXC1-AC4 baseline run A failed rc=%d stderr=%s" % (rc_a, err_a.strip()[:2000]))
        _write_bytes(CAT, cat_orig)
        return
    cat_a = _read_bytes(CAT)
    sha_a = _sha256(cat_a)
    print("RUN A served-file sha256=%s" % sha_a)

    # One reversible change to the emitter input: append MARKER inside the JSON string value of
    # mac.01.macro-data.cells.business_meaning.value -- a byte-exact substring insert, nothing else
    # in RECT touched.
    rect_text = rect_orig.decode("utf-8")
    k, end = _find_value_span(rect_text, "mac.01.macro-data", "business_meaning")
    rect_changed_text = rect_text[:end] + MARKER + rect_text[end:]
    rect_changed = rect_changed_text.encode("utf-8")
    _write_bytes(RECT, rect_changed)
    rect_diff_stat = _git_diff_stat(RECT_REL)
    print("APPLIED reversible input change: inserted %r at byte offset %d of RECT's "
          "mac.01.macro-data.business_meaning.value. git diff --stat RECT: %r" % (MARKER, end, rect_diff_stat))

    # Run B -- the named writer run once, WITH the change.
    rc_b, out_b, err_b = _run_emitter()
    print("RUN B (writer run, RECT changed) rc=%d" % rc_b)
    if rc_b != 0:
        print("VERDICT: FAIL-MXC1-AC4 run B failed rc=%d stderr=%s" % (rc_b, err_b.strip()[:2000]))
        _write_bytes(RECT, rect_orig)
        _write_bytes(CAT, cat_orig)
        return
    cat_b = _read_bytes(CAT)
    sha_b = _sha256(cat_b)
    print("RUN B served-file sha256=%s" % sha_b)
    # Diff run A's served bytes against run B's DIRECTLY (never against git HEAD -- run A's own
    # built_at_git_head vintage-stamp lines already differ from the committed HEAD bytes whenever
    # this worktree's HEAD has advanced since CAT was last committed, which is noise unrelated to
    # this exercise's ONE input change; see NFRA_MCPINDEX-W1-S4).
    import difflib
    lines_a = cat_a.decode("ascii").splitlines(keepends=True)
    lines_b = cat_b.decode("ascii").splitlines(keepends=True)
    udiff = list(difflib.unified_diff(lines_a, lines_b, fromfile="run_A_CAT", tofile="run_B_CAT", n=0))
    added_lines = [ln for ln in udiff if ln.startswith("+") and not ln.startswith("+++")]
    removed_lines = [ln for ln in udiff if ln.startswith("-") and not ln.startswith("---")]
    hunk_headers = [ln for ln in udiff if ln.startswith("@@")]
    print("DIRECT diff run_A_CAT vs run_B_CAT: %d hunk(s), %d added line(s), %d removed line(s)"
          % (len(hunk_headers), len(added_lines), len(removed_lines)))
    for ln in udiff:
        print("  " + ln.rstrip("\n"))
    # the changed line is the YAML literal-block CONTENT line under `business_meaning: |-` (the
    # field name itself is not repeated per-line); confirmed against the row instead by locating
    # the nearest preceding `entity: mac.01.macro-data` and `business_meaning:` key lines in run B.
    entity_idx = next((i for i, ln in enumerate(lines_b) if "entity: mac.01.macro-data" in ln), None)
    key_idx = None
    if entity_idx is not None:
        key_idx = next((entity_idx + off for off in range(0, 20)
                         if entity_idx + off < len(lines_b)
                         and lines_b[entity_idx + off].strip().startswith("business_meaning:")), None)
    changed_line_idx = next((i for i, ln in enumerate(lines_b) if MARKER.strip() in ln), None)
    row_touched = (len(hunk_headers) == 1 and len(added_lines) == 1 and len(removed_lines) == 1
                   and MARKER.strip() in added_lines[0]
                   and key_idx is not None and entity_idx is not None and changed_line_idx is not None
                   and entity_idx < key_idx < changed_line_idx <= key_idx + 5)
    print("ROW LOCATOR: entity line #%s ('entity: mac.01.macro-data'), business_meaning: key line #%s, "
          "changed content line #%s (0-indexed, run B)" % (entity_idx, key_idx, changed_line_idx))
    if sha_a == sha_b:
        print("VERDICT: FAIL-MXC1-AC4 served file SHA-256 did not change after the input change "
              "(run A %s == run B %s)" % (sha_a, sha_b))
        _write_bytes(RECT, rect_orig)
        _write_bytes(CAT, cat_orig)
        return
    if not row_touched:
        print("VERDICT: FAIL-MXC1-AC4 served file changed by more (or other) than exactly the "
              "mac.01.macro-data business_meaning row -- %d hunk(s), %d added line(s)"
              % (len(hunk_headers), len(added_lines)))
        _write_bytes(RECT, rect_orig)
        _write_bytes(CAT, cat_orig)
        return

    # Revert the emitter input to its EXACT saved original bytes (never `git checkout --`).
    _write_bytes(RECT, rect_orig)
    rect_diff_after_revert = _git_diff_stat(RECT_REL)
    print("REVERTED RECT to saved original bytes. git diff --stat RECT (expect empty): %r" % rect_diff_after_revert)

    # Run C -- the same writer, input unchanged (reverted). Its served-file SHA-256 must equal
    # run A's (same input -> same output; the run and its revert are both in this command log).
    rc_c, out_c, err_c = _run_emitter()
    print("RUN C (writer run, RECT reverted / unchanged) rc=%d" % rc_c)
    if rc_c != 0:
        print("VERDICT: FAIL-MXC1-AC4 run C failed rc=%d stderr=%s" % (rc_c, err_c.strip()[:2000]))
        _write_bytes(CAT, cat_orig)
        return
    cat_c = _read_bytes(CAT)
    sha_c = _sha256(cat_c)
    print("RUN C served-file sha256=%s" % sha_c)

    # Restore CAT to its exact saved original bytes (the amendment's bound: both granted paths
    # REVERTED and NEVER COMMITTED).
    _write_bytes(CAT, cat_orig)
    final_stat_cat = _git_diff_stat(CAT_REL)
    final_stat_rect = _git_diff_stat(RECT_REL)
    print("POST-REVERT git diff --stat (expect empty, both): CAT=%r RECT=%r" % (final_stat_cat, final_stat_rect))

    if sha_c != sha_a:
        print("VERDICT: FAIL-MXC1-AC4 served file SHA-256 with input reverted (%s) != baseline run A (%s)"
              % (sha_c, sha_a))
        return
    if final_stat_cat or final_stat_rect:
        print("VERDICT: FAIL-MXC1-AC4 post-revert diff is NOT empty -- CAT=%r RECT=%r"
              % (final_stat_cat, final_stat_rect))
        return
    print("VERDICT: PASS-MXC1-AC4")


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
