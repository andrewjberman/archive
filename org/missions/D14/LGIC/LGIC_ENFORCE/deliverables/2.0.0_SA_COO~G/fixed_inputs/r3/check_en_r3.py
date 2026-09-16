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
import shutil as _shutil
import subprocess
import sys
import tempfile as _tempfile

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


# ---------------------------------------------------------------- cell 3a arm
#
# LGIC_NAMING-S21: proof-of-spec-check.py's surprises limb resolves a cited row by globbing
# WORKSPACE = Path(__file__).resolve().parent.parent -- the checkout holding the SCRIPT -- not the
# checkout holding the INSTANCE being graded. So the main checkout's script, pointed at an instance
# on a side branch or in a linked worktree whose channel carries the row, reads "resolves to NO row"
# although the row is committed in the graded tree. The CVO's L9 and the L10 gate run that script.
#
# The arm builds a throwaway git repo shaped like the tree: a channel carrying a planted row id that
# the script's own checkout does NOT carry, and an instance citing it. It runs the script under test
# against that instance and PASSes only when the limb resolves the planted row. Reproduced RED at
# HEAD before this arm was written: "0 resolve to a channel row ... names row id LGIC_ENFORCE-S9990
# which resolves to NO row".


POS_CHECK = ".tools/proof-of-spec-check.py"
_PLANTED_RID = "LGIC_ENFORCE-S9990"


def _s21_fixture(root):
    """A git repo at `root` whose channel carries _PLANTED_RID and whose instance cites it."""
    subprocess.run(["git", "init", "-q"], cwd=root, capture_output=True)
    ch = os.path.join(root, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "surprise-channel", "investigations")
    os.makedirs(ch, exist_ok=True)
    with open(os.path.join(ch, "INVESTIGATION_v1.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# fixture\n\n```json\n" + json.dumps([{"id": _PLANTED_RID, "project": "LGIC_ENFORCE"}], indent=1)
                 + "\n```\n")
    dl = os.path.join(root, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "deliverables", "0.9.0_WK_LGIC_ENFORCE~9")
    os.makedirs(dl, exist_ok=True)
    inst = os.path.join(dl, "LGIC_ENFORCE.TO-EN-q-9.fixture.proof_of_spec.json")
    with open(inst, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"schema_version": "1.0", "to_id": "LGIC_ENFORCE.TO-EN-q-9",
                   "surprises": [_PLANTED_RID + ": planted row present ONLY in the graded checkout"]}, fh)
    subprocess.run(["git", "add", "-A"], cwd=root, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "f"],
                   cwd=root, capture_output=True)
    return inst


def _limb_resolves(script, inst):
    """(resolved, evidence line). Reads the limb's OWN frame and announce lines."""
    r = subprocess.run([sys.executable, script, inst], capture_output=True, text=True)
    out = _CSI.sub("", (r.stdout or "") + (r.stderr or ""))
    miss = "names row id %s which resolves to NO row" % _PLANTED_RID
    frame = [ln for ln in out.splitlines() if ln.strip().startswith("surprises-frame:")]
    ev = frame[0].strip() if frame else "(no surprises-frame line -- the limb did not run)"
    if not frame:
        return None, ev
    return (miss not in out and " 1 resolve to a channel row" in ev), ev


def i3_channel_root(script=None):
    """The script under test resolves a cited row from the INSTANCE's checkout."""
    token = _i3_verdict(script)
    say(token)
    return 0 if token.startswith("PASS-") else 1


def _i3_verdict(script=None):
    """The verdict TOKEN, printed evidence above it. A self-test compares tokens so a control can never
    pass for the wrong reason (a RED that is really LIMB-DID-NOT-RUN is not a RED)."""
    script = script or os.path.join(REPO, POS_CHECK)
    base = _tempfile.mkdtemp(prefix="en_r3_i3_")
    try:
        inst = _s21_fixture(base)
        # CONTROL on the premise: the planted id must be ABSENT from the script's own checkout, or a
        # PASS would prove nothing about rooting.
        own = os.path.abspath(os.path.join(os.path.dirname(script), os.pardir))
        own_ch = os.path.join(own, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "surprise-channel",
                              "investigations", "INVESTIGATION_v1.md")
        try:
            with open(own_ch, encoding="utf-8", errors="replace") as fh:
                premise_broken = _PLANTED_RID in fh.read()
        except (OSError, IOError):
            premise_broken = False
        if premise_broken:
            say("PREMISE: %s already exists in the script's own checkout -- the arm cannot discriminate" % _PLANTED_RID)
            return "FAIL-I3-PREMISE-BROKEN"
        resolved, ev = _limb_resolves(script, inst)
        say("script under test: %s" % script)
        say("planted row %s: present in the GRADED checkout, absent from the script's own" % _PLANTED_RID)
        say("limb frame: %s" % ev[:220])
        if resolved is None:
            return "FAIL-I3-LIMB-DID-NOT-RUN"
        if not resolved:
            return "FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT"
        return "PASS-I3-ROOTED-AT-INSTANCE-CHECKOUT"
    finally:
        _shutil.rmtree(base, ignore_errors=True)


def _install_script(root):
    """A copy of the live script under `root`, WITH the schema it reads relative to its own root
    (org/standards/PROOF_OF_SPEC.schema.json) -- without it the copy exits rc=2 before any limb runs,
    which is how a first version of this self-test reported a RED for the wrong reason."""
    os.makedirs(os.path.join(root, ".tools"), exist_ok=True)
    os.makedirs(os.path.join(root, "org", "standards"), exist_ok=True)
    dst = os.path.join(root, ".tools", "proof-of-spec-check.py")
    _shutil.copy(os.path.join(REPO, POS_CHECK), dst)
    _shutil.copy(os.path.join(REPO, "org", "standards", "PROOF_OF_SPEC.schema.json"),
                 os.path.join(root, "org", "standards", "PROOF_OF_SPEC.schema.json"))
    return dst


def _selftest_i3():
    """Both controls use COPIES of the script, so the self-test does not depend on whether the live
    script has been fixed yet. RED: a copy rooted in a checkout WITHOUT the row must return EXACTLY
    FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT. GREEN: a copy rooted INSIDE the graded checkout -- what a correct
    fix is equivalent to -- must resolve the row."""
    out = []
    elsewhere = _tempfile.mkdtemp(prefix="en_r3_i3_other_")
    try:
        mis = _install_script(elsewhere)
        tok = _i3_verdict(mis)
        out.append(("i3 RED   mis-rooted copy -> ROOTED-AT-SCRIPT (%s)" % tok[:28],
                    tok == "FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT"))
    finally:
        _shutil.rmtree(elsewhere, ignore_errors=True)

    base = _tempfile.mkdtemp(prefix="en_r3_i3_in_")
    try:
        inst = _s21_fixture(base)
        rooted = _install_script(base)
        resolved, _ev = _limb_resolves(rooted, inst)
        out.append(("i3 GREEN copy rooted INSIDE the graded checkout", resolved is True))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


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

    results.extend(_selftest_i3())

    say("")
    for label, ok in results:
        say("  %-46s %s" % (label, "OK" if ok else "BROKEN"))
    good = sum(1 for _, ok in results if ok)
    say("SELFTEST-ARMS: %d of %d" % (good, len(results)))
    return 0 if good == len(results) else 1


CMDS = {
    "i3-channel-root": i3_channel_root,
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
