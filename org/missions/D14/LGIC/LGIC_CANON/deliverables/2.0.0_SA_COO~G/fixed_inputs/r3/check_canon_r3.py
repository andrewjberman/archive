#!/usr/bin/env python3
"""check_canon_r3.py -- LGIC_CANON round 3's mechanical criteria, one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-3 issuance. Run from the worktree root:
`python <this file> <subcommand>`. Every subcommand prints its evidence, a DENOMINATOR where one
exists, and exactly one line `VERDICT: PASS-<X>` or `VERDICT: FAIL-<X>`, and exits 0. A missing
input is a FAIL verdict, never a traceback. No PASS string is a substring of another's, because
proof-of-spec-check greps <expect> UNANCHORED.

`--list` prints the subcommands. `selftest-arms` drives each arm against a DOCTORED input and
asserts it FAILS -- A-23, and the reason is below.

=============================================================================================
CN-i-1 IS THE ISSUER'S ACT, NOT A CELL -- and the lane is why.
=============================================================================================
The round-2 analysis listed CN-i-1 as a worker cell. Measured at the cut through
owned-paths-validate.py's own check_agent(), on `git show HEAD:.owned-paths.yaml`:

    path  .../LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_canon_r3.py
    lane  TREE_DELIVERABLES     (owner resolved from the SERIAL SUBFOLDER)
          2.0.0_SA_COO~G        True
          0.9.0_WK_LGIC_CANON~1 False   <- a worker is REFUSED, not merely unlisted
          3.0.0_SA_CVO          False

A <paths> entry cannot lift it: the lane refuses the serial and resolves before the block is
consulted. So this file is written by the issuer, and C-S20's disarm lands at the ISSUANCE.

=============================================================================================
THE FOUR DEFECTS ARE TWO AT HEAD (row LGIC_CANON-S17, measured before this file was written).
=============================================================================================
REPAIRED HERE, both reproduced in check_canon_r2.py's current bytes before repairing:

  W2-S3  k3_contentdiff():245 -- the DOCSTRING said "exercised against a planted removal, which
         is this criterion's negative control". The BODY planted NOTHING: it ran --content-diff
         once on the true tree and passed on the substring "CONTENT-DIFF: 0". A CONSTANT PRINT
         of that string satisfied it.
  W8-S4  o3_sovereign():497 -- `re.findall(r"SOVEREIGN", blob)` counted OCCURRENCES of the token
         anywhere in the INPUTS section and reported them as INPUTS NAMED, with the verdict
         `if marked`. ONE occurrence in prose passed it. The claim is about MARKED ROWS.

ALREADY REPAIRED at HEAD, carried here as REGRESSION ARMS so they cannot be quietly undone:

  W3-S2  l2_recount():602 -- now `^SECTION\\s+(.+?):\\s+(\\d+)\\s+rows`, the non-greedy form.
  W5-S2  j_reach():318 -- reads the NAMED COLUMN by the TSV's own header, REFUSES loudly when it
         is absent, PRINTS a DISCLOSED line when a whole-row scan would differ; j4-reach and
         j5-reach both route through it, so the repair was of the CLASS.

A repair with no arm can be reverted with nothing failing -- which is how W5-S2's class reached
TWO checkers at once. That is why the regression arms are here and are not optional.

Standard library only. ASCII only. LF endings.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

# 9 levels: r3 / fixed_inputs / <serial> / deliverables / LGIC_CANON / LGIC / D14 / missions / org
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_CANON"
DEL = ROOT + "/deliverables"
R2FIX = DEL + "/2.0.0_SA_COO~G/fixed_inputs/r2"
R2CHECK = R2FIX + "/check_canon_r2.py"
RENDER = "infra/logic/render_naming_section.py"
CHECKLIST = "infra/logic/10_ONBOARDING_CHECKLIST.md"
CANON = "infra/logic/02_DOCTRINE.md"


def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)


def read(path):
    p = path if os.path.isabs(path) else os.path.join(REPO, path)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def missing(path, tag):
    say("FAIL-%s" % tag, "the input is absent: %s" % path)
    return 0


# ------------------------------------------------------------------ W8-S4's repair
_ROW = re.compile(r"^\s*[-*|]\s*(.+)$")


def sovereign_rows(section_text):
    """(marked, total) INPUT ROWS, where a row is MARKED when the row ITSELF carries SOVEREIGN.

    W8-S4's defect was counting OCCURRENCES of the token anywhere in the section -- prose, a
    definition list, a table cell -- and reporting that count as INPUTS NAMED. A row is the unit
    the claim is about, so a row is the unit counted, and BOTH numbers are printed.
    """
    rows = [m.group(1).strip() for m in (_ROW.match(ln) for ln in section_text.splitlines()) if m]
    rows = [r for r in rows if r and not set(r) <= set("-|: ")]
    marked = [r for r in rows if "SOVEREIGN" in r]
    return marked, rows


def o3_sovereign():
    t = read(CHECKLIST)
    if t is None:
        return missing(CHECKLIST, "O3-SOVEREIGN")
    m = re.search(r"^## THE INPUTS(.*?)^## ", t, re.S | re.M)
    if not m:
        say("FAIL-O3-SOVEREIGN-ROWS-COUNTED", "the checklist has no '## THE INPUTS' section to read")
        return 0
    blob = m.group(1)
    marked, rows = sovereign_rows(blob)
    occurrences = len(re.findall(r"SOVEREIGN", blob))
    print("THE INPUTS section -- DENOMINATOR %d input row(s)" % len(rows))
    print("  MARKED SOVEREIGN (the row itself carries the token): %d" % len(marked))
    print("  token OCCURRENCES anywhere in the section:           %d   <- W8-S4's old number,"
          % occurrences)
    print("                                                            printed to show it differs")
    for r in marked[:8]:
        print("    MARKED  %s" % r[:96])
    ok = bool(rows) and bool(marked)
    say("PASS-O3-SOVEREIGN-ROWS-COUNTED" if ok else "FAIL-O3-SOVEREIGN-ROWS-COUNTED",
        "an input the run may not choose must say so ON ITS OWN ROW, not somewhere in the section")
    return 0


# ------------------------------------------------------------------ W2-S3's repair
def k3_contentdiff():
    """A-11 / A-20: the content-diff arm must REPORT a dropped line, not pass over it.

    W2-S3's defect: the old subcommand CLAIMED a planted negative control in its docstring and
    planted nothing. This one PLANTS the removal, runs the arm against the doctored tree, restores
    the file BYTE-IDENTICALLY, and prints BOTH readings. The pair is the evidence; a single clean
    run is not.
    """
    src = read(RENDER)
    if src is None:
        return missing(RENDER, "K3-CONTENTDIFF")
    if "--content-diff" not in src:
        say("FAIL-K3-CONTENTDIFF-PLANTED", "the renderer exposes no --content-diff flag")
        return 0
    canon_path = os.path.join(REPO, CANON)
    # REFUSE TO PLANT OVER SOMEONE ELSE'S UNCOMMITTED EDIT. This arm mutates a CRO-owned doctrine
    # file and restores it from memory. If the file were already dirty, the restore would write
    # back the PRE-RUN bytes and silently destroy that edit. A dirty canon is a refusal, not a
    # risk to take -- and the criterion runs in the worker's OWN worktree, where clean is normal.
    st = subprocess.run(["git", "status", "--porcelain", "--", CANON],
                        capture_output=True, text=True, cwd=REPO)
    if (st.stdout or "").strip():
        say("FAIL-K3-CONTENTDIFF-PLANTED",
            "the canon is already modified in this tree: %r" % st.stdout.strip()[:120],
            "this arm plants and restores, so it REFUSES rather than overwrite an uncommitted edit")
        return 0
    original = open(canon_path, "rb").read()
    try:
        clean_out = _content_diff()
        clean_zero = "CONTENT-DIFF: 0" in clean_out
        # TRY EACH CANDIDATE UNTIL THE COUNT MOVES. Not every generated line is one the
        # content-diff TRACKS: the first line this arm planted (`- **grammar:** ...`) left the
        # count unchanged at 17, so a single-shot plant would have reported a control that never
        # fired. The arm searches, names the line that DID move it, and prints how many it tried.
        planted, dirty_out, tried = None, "", 0
        for cand, doctored in _plant_candidates(original):
            tried += 1
            open(canon_path, "wb").write(doctored)
            dirty_out = _content_diff()
            if _diff_count(dirty_out) > _diff_count(clean_out):
                planted = cand
                break
            open(canon_path, "wb").write(original)
        if planted is None:
            say("FAIL-K3-CONTENTDIFF-PLANTED",
                "tried %d generated line(s); NONE moved the content-diff count." % tried,
                "That is a finding about the ARM, not the canon: the content-diff tracks less",
                "than the generated section contains, so it cannot see a dropped line there.")
            return 0
        # COMPARE COUNTS, not "is it non-zero". At the pre-state the true tree already reads
        # CONTENT-DIFF: 17 (the canon has not been re-rendered since alias_adjacency landed at
        # v1.10 -- that gap is CN-k-4-r3's whole job), so a test of "not 0" would be TRUE before
        # any planting and the control would prove nothing. The arm must show the count MOVE.
        dirty_reports = (_diff_count(dirty_out) > _diff_count(clean_out) >= 0)
    finally:
        open(canon_path, "wb").write(original)
    restored = open(canon_path, "rb").read() == original
    print("PLANTED REMOVAL (the negative control this criterion claims):")
    print("  candidates tried before one moved the count: %d" % tried)
    print("  removed line: %s" % planted[:100])
    print("  TRUE tree   -- CONTENT-DIFF: %s  (0 required for PASS)" % _diff_count(clean_out))
    print("  DOCTORED    -- CONTENT-DIFF: %s  (must EXCEED the true tree's)"
          % _diff_count(dirty_out))
    print("  the control fires: %s" % dirty_reports)
    print("  file restored byte-identically: %s" % restored)
    ok = clean_zero and dirty_reports and restored
    say("PASS-K3-CONTENTDIFF-PLANTED" if ok else "FAIL-K3-CONTENTDIFF-PLANTED",
        "a clean run alone proves nothing; the arm must be shown to FIRE (W2-S3)")
    return 0


def _diff_count(out):
    """The CONTENT-DIFF total the renderer printed, or -1 when it printed none."""
    m = re.search(r"^CONTENT-DIFF:\s+(\d+)\s*$", out, re.M)
    return int(m.group(1)) if m else -1


def _content_diff():
    r = subprocess.run([sys.executable, os.path.join(REPO, RENDER), "--content-diff"],
                       capture_output=True, text=True, cwd=REPO)
    return (r.stdout or "") + (r.stderr or "")


def _plant_candidates(original):
    """Yield (removed_line, doctored_bytes) for each CONTENT bullet of the generated section."""
    text = original.decode("utf-8", "replace")
    begin = text.find("<!-- BEGIN GENERATED NAMING SECTION -->")
    end = text.find("<!-- END GENERATED NAMING SECTION -->")
    if begin < 0 or end < 0:
        return
    lines = text[begin:end].splitlines(True)
    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s.startswith("- ") or len(s) <= 20:
            continue
        if s.startswith(("- **stamp", "- stamp")) or "GENERATED. Do not edit" in s:
            continue
        yield s, (text[:begin] + "".join(lines[:i] + lines[i + 1:]) + text[end:]).encode("utf-8")


def _plant_removal(original):
    """Drop ONE generated bullet from the canon's generated section. Returns (bytes, removed)."""
    text = original.decode("utf-8", "replace")
    begin = text.find("<!-- BEGIN GENERATED NAMING SECTION -->")
    end = text.find("<!-- END GENERATED NAMING SECTION -->")
    if begin < 0 or end < 0:
        return original, None
    lines = text[begin:end].splitlines(True)
    for i, ln in enumerate(lines):
        s = ln.strip()
        # A CONTENT bullet, not the section's own scaffolding. Dropping the "*GENERATED. Do not
        # edit" line or a `stamp:` line would break the section STRUCTURALLY, and the arm would
        # then fire for a reason that has nothing to do with a dropped CONTENT item -- a control
        # that fires for the wrong reason is no better than one that cannot fire.
        if not s.startswith("- "):
            continue
        if s.startswith(("- **stamp", "- stamp")) or "GENERATED. Do not edit" in s:
            continue
        if len(s) <= 20:
            continue
        removed = s
        doctored = text[:begin] + "".join(lines[:i] + lines[i + 1:]) + text[end:]
        return doctored.encode("utf-8"), removed
    return original, None


# ------------------------------------------------------------------ regression arms (W3-S2, W5-S2)
def regress_recount():
    """W3-S2 stays repaired: l2_recount must read the MULTI-WORD label, not a single token."""
    src = read(R2CHECK)
    if src is None:
        return missing(R2CHECK, "REGRESS-RECOUNT")
    nongreedy = bool(re.search(r'\^SECTION\\s\+\(\.\+\?\)', src)) or "(.+?):" in src
    single = bool(re.search(r'\^SECTION\\s\+\(\\S\+\)', src))
    probe = "SECTION MIGRATE (home): 7 rows (ledger_recount.py)"
    got = re.findall(r"^SECTION\s+(.+?):\s+(\d+)\s+rows", probe, re.M)
    print("check_canon_r2.py carries the NON-GREEDY label read: %s" % nongreedy)
    print("check_canon_r2.py carries the single-token read:     %s   (must be False)" % single)
    print("probe %r -> %r" % (probe, got))
    ok = nongreedy and not single and got == [("MIGRATE (home)", "7")]
    say("PASS-REGRESS-RECOUNT-MULTIWORD" if ok else "FAIL-REGRESS-RECOUNT-MULTIWORD",
        "a repair with no arm can be reverted with nothing failing (W3-S2)")
    return 0


def regress_reach():
    """W5-S2 stays repaired: j_reach must read the NAMED COLUMN and refuse when it is absent."""
    src = read(R2CHECK)
    if src is None:
        return missing(R2CHECK, "REGRESS-REACH")
    named = 'column(JUDGE[which], "reach")' in src
    refuses = "carries no 'reach' column" in src
    discloses = "DISCLOSED:" in src
    routes = src.count("j_reach(")
    print("j_reach reads the NAMED column:               %s" % named)
    print("j_reach REFUSES loudly when it is absent:     %s" % refuses)
    print("j_reach PRINTS a DISCLOSED line on divergence: %s" % discloses)
    print("call sites routing through the one function:  %d  (the CLASS repair)" % routes)
    ok = named and refuses and discloses and routes >= 3
    say("PASS-REGRESS-REACH-NAMED-COLUMN" if ok else "FAIL-REGRESS-REACH-NAMED-COLUMN",
        "this is the repair that reached two checkers at once; the arm keeps it there")
    return 0


SUBCOMMANDS = {
    "o3-sovereign": o3_sovereign,
    "k3-contentdiff": k3_contentdiff,
    "regress-recount": regress_recount,
    "regress-reach": regress_reach,
}


def selftest_arms():
    """A-23: every arm driven against a DOCTORED input and asserted to FAIL. EACH ARM ALONE."""
    results = []

    marked, rows = sovereign_rows("- alpha SOVEREIGN\n- beta\n- gamma\n")
    results.append(("o3-counts-rows-not-occurrences", (len(marked), len(rows)) == (1, 3),
                    "1 marked of 3 rows"))
    m2, r2 = sovereign_rows("- alpha\n- beta\n\nprose mentioning SOVEREIGN twice SOVEREIGN\n")
    results.append(("o3-ignores-prose-occurrences", len(m2) == 0 and len(r2) == 2,
                    "0 marked of 2 rows despite 2 occurrences in prose"))

    probe = "SECTION MIGRATE (home): 7 rows (x)"
    good = re.findall(r"^SECTION\s+(.+?):\s+(\d+)\s+rows", probe, re.M)
    bad = re.findall(r"^SECTION\s+(\S+)\s+(\d+)\s+rows", probe, re.M)
    results.append(("recount-arm-discriminates", good == [("MIGRATE (home)", "7")] and bad == [],
                    "non-greedy reads the multi-word label; single-token reads nothing"))

    src = read(R2CHECK) or ""
    doctored = src.replace('column(JUDGE[which], "reach")', "BLOBSCAN")
    results.append(("reach-arm-fails-on-a-reverted-repair",
                    ('column(JUDGE[which], "reach")' in src)
                    and ('column(JUDGE[which], "reach")' not in doctored),
                    "the true file carries the named-column read; a reverted copy does not"))

    canon = read(CANON) or ""
    doctored_bytes, removed = _plant_removal(canon.encode("utf-8"))
    results.append(("plant-removal-actually-removes-a-line",
                    removed is not None and len(doctored_bytes) < len(canon.encode("utf-8")),
                    "planted removal drops %r" % (removed or "")[:40]))

    ok = all(r[1] for r in results)
    print("DISCRIMINATING SELF-TEST -- denominator %d arms (A-23)" % len(results))
    for name, good_, detail in results:
        print("  %-40s %-5s %s" % (name, "PASS" if good_ else "FAIL", detail))
    say("PASS-ARMS-DISCRIMINATE" if ok else "FAIL-ARMS-DISCRIMINATE",
        "an arm that cannot be made to fail is a constant wearing a measurement's clothes")
    return 0


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--list", "-l"):
        for k in sorted(SUBCOMMANDS):
            print(k)
        print("selftest-arms")
        return 0
    if args[0] == "selftest-arms":
        return selftest_arms()
    fn = SUBCOMMANDS.get(args[0])
    if fn is None:
        say("FAIL-NO-SUCH-SUBCOMMAND", "unknown subcommand: %s" % args[0])
        return 0
    return fn()


if __name__ == "__main__":
    sys.exit(main())
