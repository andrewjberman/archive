#!/usr/bin/env python3
"""AR325-y-AC2 -- the one mutant that must fire.

The candidate's src (read from the candidate branch with git archive, never from the working tree) is copied to a
scratch folder OUTSIDE the portal product tree, in the worker's .scratch. In that copy only, filingFirm is made to
return '' for an internal caller again (the PROD shape). The new test file is run against the copy.

Control first: the UNMUTATED copy must pass the new file (6 of 6), so that a failure of the mutated copy is caused by
the mutant and by nothing else. Prints MUTANT-FIRES only when the mutated run has at least one failing case; otherwise
MUTANT-SURVIVES (exit 1). A broken control prints MUTANT-CONTROL-BAD (exit 1). The scratch copy is removed afterwards;
its node_modules is a junction that is removed as a link only (cmd rmdir without /S), never followed.
"""
import io
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET

WK = "C:/dev/wk-irpt-anlreq-133"
PORTAL = WK + "/portal"
SCRATCH = WK + "/.scratch"
CAND = "cand/dell2/anlreq-internal-filer-chooses-firm"
TSX = "src/pages/TicketCenter/AnalysisRequestParts.tsx"
NEW_FILE = "src/pages/TicketCenter/__tests__/internal-filer-chooses-firm.test.ts"
# The candidate's line for the internal branch of filingFirm, and its PROD-shape replacement (no chosen firm for staff).
ANCHOR = "  if (internal) return chosen !== null && firms.some(f => f.id === chosen) ? chosen : ''"
MUTANT = "  if (internal) return ''"

sys.path.insert(0, WK + "/.tools")
from msys_argv_guard import msys_safe_run  # noqa: E402  (git is MSYS-linked: spawn through the guard)


def junit_cases(bun, cwd, target, out):
    if os.path.exists(out):
        os.remove(out)
    proc = subprocess.run([bun, "test", target, "--reporter=junit", "--reporter-outfile=" + out],
                          cwd=cwd, capture_output=True, text=True, timeout=240)
    if not os.path.exists(out):
        return proc.returncode, None
    return proc.returncode, [(tc.get("name", ""), any(ch.tag in ("failure", "error") for ch in tc))
                             for tc in ET.parse(out).iter("testcase")]


def extract_candidate(dest):
    raw = msys_safe_run(["git", "-C", PORTAL, "archive", "--format=tar", CAND, "src", "tsconfig.json", "tsconfig.app.json"],
                        capture_output=True)
    if raw.returncode != 0:
        raise RuntimeError("git archive rc=%s: %s" % (raw.returncode, raw.stderr[:200]))
    tarfile.open(fileobj=io.BytesIO(raw.stdout)).extractall(dest)


def link_node_modules(dest):
    target = os.path.realpath(PORTAL + "/node_modules")
    link = os.path.join(dest, "node_modules")
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", link.replace("/", "\\"), target.replace("/", "\\")],
                          capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.isdir(link):
        raise RuntimeError("junction for node_modules not made: %s" % proc.stdout.strip())
    return link


def unlink_node_modules(link):
    # RD without /S removes the junction itself and does not descend into its target.
    subprocess.run(["cmd", "/c", "rmdir", link.replace("/", "\\")], capture_output=True, text=True)


def main():
    bun = shutil.which("bun")
    if not bun:
        print("MUTANT-CONTROL-BAD bun is not on PATH")
        return 1
    os.makedirs(SCRATCH, exist_ok=True)
    dest = tempfile.mkdtemp(prefix="mutant_", dir=SCRATCH)
    link = None
    try:
        extract_candidate(dest)
        link = link_node_modules(dest)
        out = os.path.join(SCRATCH, "mutant_check.xml")

        # Control: the unmutated candidate copy must pass every case of the new file.
        rc0, cases0 = junit_cases(bun, dest, NEW_FILE, out)
        if cases0 is None or any(failed for _, failed in cases0) or len(cases0) != 6:
            bad = [n for n, f in (cases0 or []) if f]
            print("MUTANT-CONTROL-BAD unmutated copy does not pass the new file: rc=%s cases=%s failing=%s"
                  % (rc0, None if cases0 is None else len(cases0), bad))
            return 1

        tsx_path = os.path.join(dest, TSX.replace("/", os.sep))
        with open(tsx_path, "r", encoding="utf-8", newline="") as fh:
            text = fh.read()
        hits = text.count(ANCHOR)
        if hits != 1:
            print("MUTANT-CONTROL-BAD anchor line found %d time(s) in %s, expected 1" % (hits, TSX))
            return 1
        with open(tsx_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text.replace(ANCHOR, MUTANT))

        rc1, cases1 = junit_cases(bun, dest, NEW_FILE, out)
        if cases1 is None:
            print("MUTANT-CONTROL-BAD the mutated run wrote no report (rc=%s)" % rc1)
            return 1
        failing = [n for n, f in cases1 if f]
        if failing:
            print("MUTANT-FIRES mutated copy (filingFirm internal -> '') fails %d of %d cases of the new file; control passed %d of 6"
                  % (len(failing), len(cases1), 6))
            for n in failing:
                print("  fired: " + n[:120])
            return 0
        print("MUTANT-SURVIVES mutated copy passes all %d cases of the new file" % len(cases1))
        return 1
    finally:
        if link:
            unlink_node_modules(link)
        # Remove the scratch copy only when the junction is gone: a tree walk must never follow it into node_modules.
        if not (link and os.path.lexists(link)):
            shutil.rmtree(dest, ignore_errors=True)
        else:
            print("MUTANT-CLEANUP the node_modules junction in %s was not removed; scratch left in place" % dest)


if __name__ == "__main__":
    sys.exit(main())
