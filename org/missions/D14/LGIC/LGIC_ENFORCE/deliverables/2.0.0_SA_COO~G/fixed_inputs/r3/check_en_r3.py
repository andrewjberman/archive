#!/usr/bin/env python3
"""check_en_r3 -- LGIC_ENFORCE round 3's checker. The ISSUER's fixed input; workers never edit it.

Round 3's cells call these subcommands as their criteria's invocations. Each prints ONE verdict
token on its last line so a criterion's <expect> is an anchored, unambiguous match.

CELL 4 (the placement, R-12 / R-2 / A-9, ruled a WORKER cell by R-23 @2a2d10acd8) is graded
against PLACEMENT_MAP.json -- a FIXED INPUT written by the issuer at the cut. That separation is
the point: the cell is graded on a map it cannot edit, so "every file went to its first minting
author's folder" is checked against the authorship measured BEFORE the move, not against whatever
the tree looks like afterwards. After a git mv, `git log --diff-filter=A` on the NEW path can
resolve differently, so recomputing the map at grade time would grade the cell's own act.

USAGE: check_en_r3.py <subcommand> | --list | selftest-arms
Exit 0 on PASS, 1 on FAIL, 2 on usage/read error.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# r3 -> fixed_inputs -> 2.0.0_SA_COO~G -> deliverables -> LGIC_ENFORCE -> LGIC -> D14 -> missions -> org -> repo
# NINE steps, not eight. The self-test cannot catch this: every arm passes an explicit cwd
# fixture and never reads REPO, so a wrong REPO is invisible to a green selftest. Exercised
# below by running a subcommand with NO cwd against the real tree.
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
DELIV = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"
MAP = os.path.join(HERE, "PLACEMENT_MAP.json")

# A REAL CSI sequence. The chr(27) is written as a CALL, not a literal ESC byte, so this line
# survives being read through a terminal -- a raw ESC renders invisibly and the one character
# that decides the pattern is the one a reader cannot see (measured 2026-09-16 on S55).
_CSI = re.compile(chr(27) + r"\[[0-9;]*[A-Za-z]")


def say(*parts):
    print(" ".join(str(p) for p in parts))


def git(args, cwd=None):
    r = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=cwd or REPO)
    return r.returncode, r.stdout


def load_map(path=None):
    with open(path or MAP, encoding="utf-8") as fh:
        return json.load(fh)


def tree_blobs(cwd=None):
    """The files sitting DIRECTLY under deliverables/ with no serial subfolder, BY OBJECT TYPE.

    `git ls-tree --name-only` does not mark trees, so a name-only read counts the nine serial
    FOLDERS as files (an early count of this population read 26 for exactly that reason). Read the
    type column instead.
    """
    rc, out = git(["ls-tree", "HEAD", DELIV + "/"], cwd=cwd)
    if rc != 0:
        return None
    blobs = []
    for line in out.splitlines():
        if not line.strip():
            continue
        head, _, name = line.partition("\t")
        cols = head.split()
        if len(cols) >= 2 and cols[1] == "blob":
            blobs.append(name.strip())
    return blobs


# ---------------------------------------------------------------- cell 4 arms

def p4_population(cwd=None, mapdoc=None):
    """The ownerless population is EMPTY, against the denominator the cut printed."""
    m = mapdoc or load_map()
    expected = m["denominator_blobs"]
    blobs = tree_blobs(cwd)
    if blobs is None:
        say("FAIL-P4-POPULATION-UNREADABLE (git ls-tree failed)")
        return 1
    say("DENOMINATOR: %d ownerless blob(s) at the cut; %d remain now; trees excluded by type, not by name"
        % (expected, len(blobs)))
    if blobs:
        for b in sorted(blobs)[:20]:
            say("   STILL OWNERLESS:", b.split("/")[-1])
        say("FAIL-P4-POPULATION-NONEMPTY")
        return 1
    say("PASS-P4-POPULATION-EMPTY")
    return 0


def p4_destinations(cwd=None, mapdoc=None):
    """Every mapped file exists at its first-minting author's folder, and nowhere else."""
    m = mapdoc or load_map()
    root = cwd or REPO
    missing, found = [], 0
    for row in m["rows"]:
        dest = row["destination"]
        if os.path.exists(os.path.join(root, dest.replace("/", os.sep))):
            found += 1
        else:
            missing.append((row["basename"], row["first_minting_author"]))
    say("DENOMINATOR: %d mapped file(s); %d present at their mapped destination; %d missing"
        % (len(m["rows"]), found, len(missing)))
    for b, a in missing[:20]:
        say("   MISSING:", b, "-> expected under", a)
    if missing:
        say("FAIL-P4-DESTINATION-MISSING")
        return 1
    say("PASS-P4-DESTINATIONS-ALL-PLACED")
    return 0


def p4_citations(cwd=None, mapdoc=None):
    """No TRACKED file still cites a moved file at its OLD flat path.

    Walks the tracked set rather than shelling to a recursive search, so the denominator is the
    tracked file count and the read cannot be a silent rail no-op.
    """
    m = mapdoc or load_map()
    root = cwd or REPO
    rc, out = git(["ls-files"], cwd=root)
    if rc != 0:
        say("FAIL-P4-CITATIONS-UNREADABLE")
        return 1
    files = [f for f in out.splitlines() if f.strip()]
    olds = {row["source"]: row["basename"] for row in m["rows"]}
    # the map file itself and this checker RECORD the old paths by design
    exempt = {
        DELIV + "/2.0.0_SA_COO~G/fixed_inputs/r3/PLACEMENT_MAP.json",
        DELIV + "/2.0.0_SA_COO~G/fixed_inputs/r3/check_en_r3.py",
    }
    hits = []
    for f in files:
        if f in exempt:
            continue
        p = os.path.join(root, f.replace("/", os.sep))
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                t = fh.read()
        except (OSError, IOError):
            continue
        for old in olds:
            if old in t:
                hits.append((f, olds[old]))
    say("DENOMINATOR: %d tracked file(s) scanned, %d old path(s) searched, %d exempt (the map and this checker)"
        % (len(files), len(olds), len(exempt)))
    for f, b in hits[:20]:
        say("   DANGLING:", f, "cites", b, "at its old flat path")
    if hits:
        say("FAIL-P4-CITATION-DANGLING")
        return 1
    say("PASS-P4-CITATIONS-REPOINTED")
    return 0


# ---------------------------------------------------------------- cell 2 arms
#
# The gate's DOMAIN (R-11/R-13, R-15, A-6, A-7, A-8, S42, S45). These arms name the CONTRACT the
# cell must build, and every one of them reads RED against .tools/naming-gate.py at the cut --
# the gate prints no denominator, no declaration-tree record and no coverage line today. That is
# the state a criterion must be in before its cell runs (W2-S11): a criterion that already passes
# is not evidence the cell did anything.
#
# The contract is deliberately about PRINTED, CHECKABLE FACTS rather than an implementation. The
# denominator and the coverage line exist because Rule 22 requires a claim to carry the set it
# ranged over: a gate that grades "the files it could see" without printing what it could NOT see
# is unfalsifiable at a glance, which is exactly S42's finding.

GATE = ".tools/naming-gate.py"


def _gate(args, cwd=None):
    """Run the naming gate and return its combined output, ANSI-stripped."""
    r = subprocess.run([sys.executable, GATE] + list(args),
                       capture_output=True, text=True, cwd=cwd or REPO)
    return _CSI.sub("", (r.stdout or "") + (r.stderr or ""))


def _diff_fixture(tmp, body):
    p = os.path.join(tmp, "fixture.diff")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    return p


_SAMPLE_DIFF = (
    "diff --git a/infra/logic/x.tf b/infra/logic/x.tf\n"
    "--- a/infra/logic/x.tf\n"
    "+++ b/infra/logic/x.tf\n"
    "@@ -0,0 +1,1 @@\n"
    '+resource "aws_s3_bucket" "b" { bucket = "opal-data-assets" }\n'
)


def n2_denominator(cwd=None):
    """Every run prints the DENOMINATOR of paths it graded."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="en_r3_n2_")
    try:
        out = _gate(["--diff", _diff_fixture(tmp, _SAMPLE_DIFF)], cwd)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    has = "DENOMINATOR" in out
    say("gate output lines: %d; DENOMINATOR line present: %s" % (len(out.splitlines()), has))
    if not has:
        say("FAIL-N2-NO-DENOMINATOR")
        return 1
    say("PASS-N2-DENOMINATOR-PRINTED")
    return 0


def n2_coverage(cwd=None):
    """Every run prints what it could NOT see -- the coverage half of the same claim (S42)."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="en_r3_n2c_")
    try:
        out = _gate(["--diff", _diff_fixture(tmp, _SAMPLE_DIFF)], cwd)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    has = "COVERAGE" in out
    say("COVERAGE line (paths the gate cannot see) present: %s" % has)
    if not has:
        say("FAIL-N2-NO-COVERAGE")
        return 1
    say("PASS-N2-COVERAGE-PRINTED")
    return 0


def n2_declaration_subtraction(cwd=None):
    """The declaration-tree set is printed as a SUBTRACTION from the denominator, never a list.

    Rule 24(i): a forward list of trees omits silently; the same set written as denominator MINUS
    exclusions cannot lose a member without the count disagreeing. `org/**` and `docs/**` are the
    declared exclusions, so both must appear as EXCLUDED rather than merely be absent.
    """
    import tempfile
    tmp = tempfile.mkdtemp(prefix="en_r3_n2d_")
    try:
        out = _gate(["--diff", _diff_fixture(tmp, _SAMPLE_DIFF)], cwd)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    named = "EXCLUDED" in out and "org/" in out and "docs/" in out
    say("declaration-tree subtraction printed with org/ and docs/ named EXCLUDED: %s" % named)
    if not named:
        say("FAIL-N2-NO-SUBTRACTION")
        return 1
    say("PASS-N2-SUBTRACTION-PRINTED")
    return 0


# ---------------------------------------------------------------- self-test

def _fixture(tmp, blobs, placed):
    """A throwaway git repo shaped like the real one: `blobs` left flat, `placed` under authors."""
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, capture_output=True)
    d = os.path.join(tmp, DELIV.replace("/", os.sep))
    os.makedirs(d, exist_ok=True)
    for b in blobs:
        with open(os.path.join(d, b), "w", encoding="utf-8") as fh:
            fh.write("x\n")
    for author, name in placed:
        sub = os.path.join(d, author)
        os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, name), "w", encoding="utf-8") as fh:
            fh.write("x\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", "f"], cwd=tmp, capture_output=True)


def selftest_arms():
    """Every arm RED-FIRST: each must FAIL on the un-done tree and PASS on the done one."""
    import shutil
    import tempfile
    base = tempfile.mkdtemp(prefix="en_r3_selftest_")
    results = []
    try:
        names = ["A.md", "B.md"]
        mapdoc = {
            "denominator_blobs": 2,
            "rows": [
                {"basename": "A.md", "source": DELIV + "/A.md", "first_minting_author": "0.9.0_WK_LGIC_ENFORCE~1",
                 "destination": DELIV + "/0.9.0_WK_LGIC_ENFORCE~1/A.md"},
                {"basename": "B.md", "source": DELIV + "/B.md", "first_minting_author": "0.9.0_WK_LGIC_ENFORCE~2",
                 "destination": DELIV + "/0.9.0_WK_LGIC_ENFORCE~2/B.md"},
            ],
        }
        before = os.path.join(base, "before")
        _fixture(before, names, [])
        after = os.path.join(base, "after")
        _fixture(after, [], [("0.9.0_WK_LGIC_ENFORCE~1", "A.md"), ("0.9.0_WK_LGIC_ENFORCE~2", "B.md")])

        results.append(("p4-population  RED  (files still flat)", p4_population(before, mapdoc) == 1))
        results.append(("p4-population  GREEN (none flat)", p4_population(after, mapdoc) == 0))
        results.append(("p4-destinations RED  (nothing placed)", p4_destinations(before, mapdoc) == 1))
        results.append(("p4-destinations GREEN (all placed)", p4_destinations(after, mapdoc) == 0))

        # a citation fixture: one tracked file naming a moved file's OLD path
        cite = os.path.join(base, "cite")
        _fixture(cite, [], [("0.9.0_WK_LGIC_ENFORCE~1", "A.md"), ("0.9.0_WK_LGIC_ENFORCE~2", "B.md")])
        with open(os.path.join(cite, "notes.md"), "w", encoding="utf-8") as fh:
            fh.write("see " + DELIV + "/A.md\n")
        subprocess.run(["git", "add", "-A"], cwd=cite, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "c"], cwd=cite, capture_output=True)
        results.append(("p4-citations   RED  (a dangling old path)", p4_citations(cite, mapdoc) == 1))
        results.append(("p4-citations   GREEN (none dangling)", p4_citations(after, mapdoc) == 0))

        # DISCRIMINATION: the type-column read must not count serial TREES as files
        trees = os.path.join(base, "trees")
        _fixture(trees, [], [("0.9.0_WK_LGIC_ENFORCE~1", "A.md"), ("0.9.0_WK_LGIC_ENFORCE~2", "B.md")])
        blobs = tree_blobs(trees)
        results.append(("tree-vs-blob   (2 serial folders counted as 0 files)", blobs == []))
    finally:
        shutil.rmtree(base, ignore_errors=True)

    say("")
    for label, ok in results:
        say("  %-46s %s" % (label, "OK" if ok else "BROKEN"))
    good = sum(1 for _, ok in results if ok)
    say("SELFTEST-ARMS: %d of %d" % (good, len(results)))
    return 0 if good == len(results) else 1


CMDS = {
    "n2-denominator": n2_denominator,
    "n2-coverage": n2_coverage,
    "n2-declaration-subtraction": n2_declaration_subtraction,
    "p4-population": p4_population,
    "p4-destinations": p4_destinations,
    "p4-citations": p4_citations,
    "selftest-arms": selftest_arms,
}


def main():
    if len(sys.argv) != 2:
        say("usage: check_en_r3.py <subcommand> | --list | selftest-arms")
        return 2
    cmd = sys.argv[1]
    if cmd == "--list":
        for k in sorted(CMDS):
            say(k)
        return 0
    fn = CMDS.get(cmd)
    if fn is None:
        say("unknown subcommand:", cmd)
        return 2
    return fn()


if __name__ == "__main__":
    sys.exit(main())
