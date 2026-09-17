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

=============================================================================================
v2 AT THE ROUND-3 CUT -- the CELL arms (2.0.0_SA_COO~G, 2026-09-17)
=============================================================================================
The four arms above are the INSTRUMENT repairs. The arms below grade the round-3 CELLS, one
subcommand per mechanical criterion, each built as a PURE core (text in, verdict out) so that
`selftest-arms` can drive every core ALONE against a GREEN fixture that must pass and a DOCTORED
fixture that must fail (A-23, and LGIC_ENFORCE-S55: a belt tested only with its braces proves the
union). A core that cannot be made to fail is reported as a failed self-test.

  CN-k-4 (r3)  k4-producer        A-20: the producer exclusion prints its no-consumer predicate
  CN-k-5       k5-census          title v1.1 and the section-0 count, both RECOUNTED from rule blocks
               k5-coordinates     R-9(iii): four `resolves R-9(iii) C<k>:` lines in their named blocks
               k5-r1-vintage      A-4: R1's census line carries its vintage
               k5-short-sovereign A-6 restated: SHORT is SOVEREIGN, read thereafter; the row count agrees
  CN-j-8/9/10  j8|j9|j10-rows     per-plane rows over the tree, five axis verdicts, worst verdict + rule
               j8|j9|j10-reach    the reach column read BY NAME over the six rules R-9(iv) names
               j8|j9|j10-blind    A-22: siblings' answer files ABSENT at the judge's stated base commit
               j10-unbriefed      the unbriefed arm's ORDER FILE carries no severity order (read at the cut)
  CN-j-11      j11-intersection   intersection + positive control printed BEFORE the first ROLL-UP line
               j11-rollup         the roll-up agreement counts, recounted from the three judges' rows
               j11-traced         every diverging plane traced to a canon line
               j11-reach          the union reach over the six, recounted
  CN-l-3       l3-state-plane     A-21: section 2 carries a state/ row, or names no state/ plane at all

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


# ================================================================== v2: the round-3 CELL arms
LEDGER = "infra/logic/06_CONFORMANCE_LEDGER.md"
FIX3 = DEL + "/2.0.0_SA_COO~G/fixed_inputs/r3"
TREE = FIX3 + "/CN_TREE_R3.md"
EX3 = DEL + "/exercises/r3"
JUDGE3 = {"f": EX3 + "/judge-f.tsv", "g": EX3 + "/judge-g.tsv", "h": EX3 + "/judge-h.tsv"}
COMPARE3 = EX3 + "/judge-compare-r3.md"
TO_J10 = ROOT + "/task-orders/LGIC_CANON.TO-CN-j-10-r3.judge-h-unbriefed.md"
SIX = ("R3", "R8", "R14", "R15", "R19", "R21")
VOCAB = ("CONFORMS", "DECLARED-EXCEPTION", "DEPARTS-RECOMMENDED", "UNDETERMINED", "VIOLATES")
COLS = ["plane", "A1", "A2", "A3", "A4", "A5", "rules", "worst_verdict", "worst_rule", "reach", "why"]
PRODUCER = "/key/legacy_served_paths/producer"
# (coordinate, the rule block the line must sit in, the counterpart token the line must name)
COORDS = (("C1", "R10", r"\bR9\b"), ("C2", "R1", r"\bcensus\b"),
          ("C3", "R6", r"\bR5\b"), ("C4", "R19", r"\bR18\b"))
NUMWORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}


def verdict(ok, pass_s, fail_s, lines):
    say(pass_s if ok else fail_s, *lines)
    return 0


def git_rc(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True, cwd=REPO)
    return r.returncode, (r.stdout or "").strip()


# ------------------------------------------------------------------ CN-k-5 cores
def rule_blocks(text):
    """{Rn: block text}. A block opens on a line starting `**R<n>` and closes at the next rule,
    a heading (`#`) or a `---` rule line -- the recount section 0 of the canon itself describes."""
    blocks, cur, buf = {}, None, []
    for ln in text.splitlines():
        m = re.match(r"^\*\*R(\d+)\b", ln)
        if m or ln.startswith("#") or ln.startswith("---"):
            if cur is not None:
                blocks[cur] = "\n".join(buf)
            cur, buf = (("R" + m.group(1)), [ln]) if m else (None, [])
            continue
        if cur is not None:
            buf.append(ln)
    if cur is not None:
        blocks[cur] = "\n".join(buf)
    return blocks


def core_k5_census(canon):
    title = canon.splitlines()[0] if canon else ""
    blocks = rule_blocks(canon)
    parts = ("authority:", "census:", "non-application:")
    carrying = [k for k, b in blocks.items() if all(p in b for p in parts)]
    m = re.search(r"^RULES CARRYING ALL THREE PARTS:\s*(\d+) of (\d+)\s*$", canon, re.M)
    typed = (int(m.group(1)), int(m.group(2))) if m else None
    v11 = re.search(r"\bv1\.1\b", title) is not None
    ok = v11 and typed == (len(carrying), len(blocks))
    return ok, ["title line: %r -> carries v1.1: %s" % (title[:90], v11),
                "RULE BLOCKS RECOUNTED -- DENOMINATOR %d block(s); carrying all three parts: %d"
                % (len(blocks), len(carrying)),
                "blocks missing a part: %s" % sorted(set(blocks) - set(carrying)),
                "section 0 types: %s" % (("%d of %d" % typed) if typed else "NO COUNT LINE")]


def core_k5_coords(canon):
    blocks = rule_blocks(canon)
    found, lines = 0, ["COORDINATES -- DENOMINATOR %d (R-9 iii)" % len(COORDS)]
    for cid, rule, counterpart in COORDS:
        b = blocks.get(rule, "")
        hits = [ln for ln in b.splitlines()
                if re.match(r"^\W*resolves R-9\(iii\) %s:" % cid, ln)]
        good = [h for h in hits if re.search(counterpart, h)]
        found += 1 if good else 0
        lines.append("  %s in %s: %d line(s), naming %s: %d" % (cid, rule, len(hits), counterpart, len(good)))
    lines.append("coordinates carried: %d of %d" % (found, len(COORDS)))
    return found == len(COORDS), lines


def core_k5_r1(canon):
    b = rule_blocks(canon).get("R1", "")
    cl = [ln for ln in b.splitlines() if re.match(r"^\W*census:", ln)]
    good = [ln for ln in cl if re.search(r"as of [^\n]*(@[0-9a-f]{7,}|2026-\d\d-\d\d)", ln)]
    return (len(cl) == 1 and len(good) == 1), [
        "R1 block census line(s), denominator %d: %r" % (len(cl), [c[:100] for c in cl]),
        "carrying a vintage ('as of' + @hash or a date): %d" % len(good)]


def _table_rows(blob):
    out = []
    for ln in blob.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        out.append(cells)
    return out


def core_k5_short(checklist):
    m = re.search(r"^## THE INPUTS(.*?)^## ", checklist or "", re.S | re.M)
    if not m:
        return False, ["no '## THE INPUTS' section"]
    rows = [r for r in _table_rows(m.group(1)) if r and r[0].lower() != "input"]
    marks = [re.sub(r"[*`]", "", r[1]).strip() if len(r) > 1 else "" for r in rows]
    short = [i for i, r in enumerate(rows) if "SHORT" in r[0]]
    short_ok = len(short) == 1 and marks[short[0]] == "SOVEREIGN"
    sov, giv = marks.count("SOVEREIGN"), marks.count("GIVEN")
    odd = [k for k in marks if k not in ("SOVEREIGN", "GIVEN", "DERIVED")]
    s = re.search(r"^(\w+) rows: (\w+) SOVEREIGN\b.*?\b(\w+) GIVEN", m.group(1), re.M)

    def num(w):
        return int(w) if w.isdigit() else NUMWORDS.get(w.lower(), -1)
    said = (num(s.group(1)), num(s.group(2)), num(s.group(3))) if s else None
    ok = short_ok and not odd and said == (len(rows), sov, giv)
    return ok, ["INPUT ROWS -- DENOMINATOR %d; marks SOVEREIGN %d, GIVEN %d, other %s"
                % (len(rows), sov, giv, odd),
                "SHORT row(s): %d; its mark: %r" % (len(short), marks[short[0]] if short else None),
                "the prose count reads (rows, SOVEREIGN, GIVEN): %s" % (said,)]


# ------------------------------------------------------------------ CN-k-4 (r3) core
def core_k4_producer(out):
    m = re.search(r"^EXCLUSION-PREDICATE producer: (\d+) consumer\(s\) of (\d+) file\(s\) scanned",
                  out, re.M)
    if not m:
        return False, ["no 'EXCLUSION-PREDICATE producer: <n> consumer(s) of <m> file(s) scanned' line"]
    n, den = int(m.group(1)), int(m.group(2))
    excluded = re.search(r"^EXCLUDED: %s\b" % re.escape(PRODUCER), out, re.M) is not None
    ok = den > 0 and (excluded == (n == 0))
    return ok, ["producer consumers %d of %d file(s) scanned; EXCLUDED line printed: %s" % (n, den, excluded),
                "the exclusion must hold exactly while the consumer count is zero (A-20)"]


# ------------------------------------------------------------------ CN-l-3 core
def core_l3(ledger):
    m = re.search(r"^## .2\.(.*?)^## ", ledger or "", re.S | re.M)
    if not m:
        return False, ["section 2 not found"]
    blob = m.group(1)
    rows = _table_rows(blob)
    plane_rows = [r for r in rows if "state/" in r[0]]
    decided = [r for r in plane_rows if len(r) >= 6 and "R21" in r[3] and r[4].strip() and r[5].strip()]
    elsewhere = sum(1 for r in rows for c in r[1:] if "state/" in c)
    elsewhere += sum(1 for ln in blob.splitlines() if not ln.strip().startswith("|") and "state/" in ln)
    if plane_rows:
        branch, ok = "ROW", len(decided) == len(plane_rows)
    elif elsewhere == 0:
        branch, ok = "NARROWED", True
    else:
        branch, ok = "NEITHER", False
    return ok, ["SECTION 2 -- DENOMINATOR %d table row(s)" % len(rows),
                "rows whose PLANE cell names state/: %d (decided under R21: %d)" % (len(plane_rows), len(decided)),
                "state/ named anywhere else in section 2: %d" % elsewhere,
                "BRANCH: %s" % branch]


# ------------------------------------------------------------------ the judges' cores
def tree_planes(tree):
    m = re.search(r"^## The planes(.*?)^## ", tree or "", re.S | re.M)
    if not m:
        return []
    return [re.sub(r"`", "", r[0]).strip() for r in _table_rows(m.group(1))
            if r and r[0].strip().lower() != "plane"]


def parse_tsv(text):
    lines = [ln for ln in (text or "").splitlines() if ln.strip()]
    if not lines:
        return [], []
    head = lines[0].split("\t")
    return head, [dict(zip(head, ln.split("\t"))) for ln in lines[1:]]


def core_j_rows(tsv, planes):
    head, rows = parse_tsv(tsv)
    if head != COLS:
        return False, ["header %r is not %r" % (head, COLS)]
    got = [r.get("plane", "").strip() for r in rows]
    bad = []
    for r in rows:
        axes = [r.get(a, "").strip() for a in COLS[1:6]]
        if any(a not in VOCAB for a in axes):
            bad.append((r["plane"], "axis value off vocabulary"))
        if any(not re.search(r"\bA%d:\s*R\d+" % k, r.get("rules", "")) for k in range(1, 6)):
            bad.append((r["plane"], "an axis cites no rule"))
        if r.get("worst_verdict", "").strip() not in axes:
            bad.append((r["plane"], "worst_verdict is not one of the row's own axis verdicts"))
        if not re.fullmatch(r"R\d+", r.get("worst_rule", "").strip()):
            bad.append((r["plane"], "worst_rule is not one rule id"))
    cover = sorted(got) == sorted(planes) and len(set(got)) == len(got)
    ok = bool(planes) and cover and not bad
    return ok, ["ROWS %d over a tree of %d plane(s); same set, no duplicates: %s" % (len(rows), len(planes), cover),
                "row defects, denominator %d: %d %s" % (len(rows), len(bad), bad[:4])]


def reach_set(tsv):
    head, rows = parse_tsv(tsv)
    if "reach" not in head:
        return None, "no 'reach' column"
    toks, bad = set(), 0
    for r in rows:
        for t in re.split(r"[\s,;]+", r.get("reach", "").strip()):
            if not t:
                continue
            if re.fullmatch(r"R\d+", t):
                toks.add(t)
            elif t.lower() != "none":
                bad += 1
    return (None, "%d reach token(s) neither a rule id nor 'none'" % bad) if bad else (toks, "")


def core_j_reach(tsv):
    toks, why = reach_set(tsv)
    if toks is None:
        return False, [why]
    got = [r for r in SIX if r in toks]
    return True, ["REACHED %d of %d: %s" % (len(got), len(SIX), got),
                  "NOT REACHED %d of %d: %s" % (len(SIX) - len(got), len(SIX), [r for r in SIX if r not in toks])]


def core_j10(order_text):
    leaks = len(re.findall(r"CN_SEVERITY", order_text or ""))
    chain = len(re.findall(r"(?:%s)\s*[<>]" % "|".join(re.escape(v) for v in VOCAB), order_text or ""))
    ok = bool(order_text) and leaks == 0 and chain == 0
    return ok, ["unbriefed order file read: %s" % bool(order_text),
                "names CN_SEVERITY: %d ; carries an ordered verdict chain: %d (both must be 0)" % (leaks, chain)]


def worst_map(tsv):
    _, rows = parse_tsv(tsv)
    return {r.get("plane", "").strip(): r.get("worst_verdict", "").strip() for r in rows}


def _line_num(text, pat):
    for i, ln in enumerate(text.splitlines()):
        m = re.match(pat, ln)
        if m:
            return i, m
    return None, None


def core_j11_intersection(cmp_text, tsvs, planes):
    maps = {k: worst_map(v) for k, v in tsvs.items()}
    inter = set(maps["f"]) & set(maps["g"]) & set(maps["h"])
    i_int, m_int = _line_num(cmp_text, r"^PLANE INTERSECTION F\.G\.H:\s*(\d+) of (\d+)")
    i_pos, m_pos = _line_num(cmp_text, r"^POSITIVE CONTROL F\.F:\s*(\d+) of (\d+)")
    i_roll, _ = _line_num(cmp_text, r"^ROLL-UP")
    order_ok = None not in (i_int, i_pos, i_roll) and i_int < i_roll and i_pos < i_roll
    vals_ok = (m_int is not None and m_pos is not None
               and (int(m_int.group(1)), int(m_int.group(2))) == (len(inter), len(planes))
               and (int(m_pos.group(1)), int(m_pos.group(2))) == (len(maps["f"]), len(maps["f"])))
    ok = order_ok and vals_ok and len(inter) > 0
    return ok, ["recounted: intersection %d of %d tree plane(s); F.F %d" % (len(inter), len(planes), len(maps["f"])),
                "printed: %s ; %s" % (m_int.group(0) if m_int else "NO INTERSECTION LINE",
                                      m_pos.group(0) if m_pos else "NO POSITIVE CONTROL LINE"),
                "both printed BEFORE the first ROLL-UP line: %s" % order_ok]


def _agree(maps, keys, inter):
    return sum(1 for p in inter if len({maps[k].get(p) for k in keys}) == 1)


def core_j11_rollup(cmp_text, tsvs):
    maps = {k: worst_map(v) for k, v in tsvs.items()}
    inter = set(maps["f"]) & set(maps["g"]) & set(maps["h"])
    want = {"F.G.H": _agree(maps, "fgh", inter), "F.G": _agree(maps, "fg", inter),
            "F.H": _agree(maps, "fh", inter), "G.H": _agree(maps, "gh", inter)}
    lines, ok = ["ROLL-UP recounted over the intersection, DENOMINATOR %d" % len(inter)], len(inter) > 0
    for k, a in want.items():
        m = re.search(r"^ROLL-UP AGREE %s:\s*(\d+) of (\d+)" % re.escape(k), cmp_text, re.M)
        got = (int(m.group(1)), int(m.group(2))) if m else None
        ok = ok and got == (a, len(inter))
        lines.append("  %-6s recounted %d of %d ; printed %s" % (k, a, len(inter), got))
    return ok, lines


def core_j11_traced(cmp_text, tsvs, canon_lines):
    maps = {k: worst_map(v) for k, v in tsvs.items()}
    inter = set(maps["f"]) & set(maps["g"]) & set(maps["h"])
    div = sorted(p for p in inter if len({maps[k].get(p) for k in "fgh"}) > 1)
    dl = [ln for ln in cmp_text.splitlines() if ln.startswith("DIVERGE ")]
    m = re.search(r"^ROLL-UP DIVERGE:\s*(\d+) of (\d+)", cmp_text, re.M)
    untraced = []
    for p in div:
        hit = [ln for ln in dl if p in ln.replace("`", "")]
        cites = [int(n) for ln in hit for n in re.findall(r"02_DOCTRINE\.md:(\d+)", ln)]
        if not hit or not cites or any(n < 1 or n > canon_lines for n in cites):
            untraced.append(p)
    ok = (m is not None and (int(m.group(1)), int(m.group(2))) == (len(div), len(inter))
          and len(dl) == len(div) and not untraced)
    return ok, ["DIVERGING planes recounted: %d of %d ; printed %s" % (len(div), len(inter), m.group(0) if m else None),
                "DIVERGE lines: %d ; untraced to a canon line in range (1..%d): %d %s"
                % (len(dl), canon_lines, len(untraced), untraced[:4])]


def core_j11_reach(cmp_text, tsvs):
    union = set()
    for v in tsvs.values():
        toks, _ = reach_set(v)
        union |= (toks or set())
    got = [r for r in SIX if r in union]
    m = re.search(r"^UNION REACHED:\s*(\d+) of (\d+)", cmp_text, re.M)
    ok = m is not None and (int(m.group(1)), int(m.group(2))) == (len(got), len(SIX))
    return ok, ["union reach recounted: %d of %d %s ; printed %s" % (len(got), len(SIX), got, m.group(0) if m else None)]


def blind_core(base, siblings, canon_path, require_v11=True):
    """(ok, lines) -- A-22: the base resolves and is an ancestor of HEAD; a POSITIVE CONTROL file is
    visible at base (so an absence below is a measurement, not a blind probe); every sibling
    answer file is ABSENT at base; the canon at base already carries CN-k-5's v1.1 title."""
    rc, full = git_rc("rev-parse", "--verify", "--quiet", (base or "0") + "^{commit}")
    if rc != 0:
        return False, ["base %r does not resolve to a commit" % base]
    anc = git_rc("merge-base", "--is-ancestor", full, "HEAD")[0] == 0
    pos = git_rc("cat-file", "-e", "%s:%s" % (full, canon_path))[0] == 0
    present = [s for s in siblings if git_rc("cat-file", "-e", "%s:%s" % (full, s))[0] == 0]
    _, title = git_rc("show", "%s:%s" % (full, canon_path))
    v11 = re.search(r"\bv1\.1\b", (title.splitlines() or [""])[0]) is not None
    ok = anc and pos and not present and (v11 or not require_v11)
    return ok, ["base %s ancestor of HEAD: %s" % (full[:10], anc),
                "POSITIVE CONTROL %s visible at base: %s" % (canon_path, pos),
                "sibling answer files PRESENT at base, denominator %d: %d %s" % (len(siblings), len(present), present),
                "canon at base carries v1.1 (CN-k-5 drained first): %s" % v11]


# ------------------------------------------------------------------ CLI wrappers
def _canon():
    return read(CANON)


def k5_census():
    t = _canon()
    if t is None:
        return missing(CANON, "K5-CENSUS-RECOUNTED")
    ok, lines = core_k5_census(t)
    return verdict(ok, "PASS-K5-CENSUS-RECOUNTED", "FAIL-K5-CENSUS-RECOUNTED", lines)


def k5_coordinates():
    t = _canon()
    if t is None:
        return missing(CANON, "K5-FOUR-COORDINATES")
    ok, lines = core_k5_coords(t)
    return verdict(ok, "PASS-K5-FOUR-COORDINATES", "FAIL-K5-FOUR-COORDINATES", lines)


def k5_r1_vintage():
    t = _canon()
    if t is None:
        return missing(CANON, "K5-R1-CENSUS-VINTAGED")
    ok, lines = core_k5_r1(t)
    return verdict(ok, "PASS-K5-R1-CENSUS-VINTAGED", "FAIL-K5-R1-CENSUS-VINTAGED", lines)


def k5_short_sovereign():
    t = read(CHECKLIST)
    if t is None:
        return missing(CHECKLIST, "K5-SHORT-SOVEREIGN-READ")
    ok, lines = core_k5_short(t)
    return verdict(ok, "PASS-K5-SHORT-SOVEREIGN-READ", "FAIL-K5-SHORT-SOVEREIGN-READ", lines)


def k4_producer():
    if read(RENDER) is None:
        return missing(RENDER, "K4-PRODUCER-PREDICATE")
    ok, lines = core_k4_producer(_content_diff())
    return verdict(ok, "PASS-K4-PRODUCER-PREDICATE", "FAIL-K4-PRODUCER-PREDICATE", lines)


def l3_state_plane():
    t = read(LEDGER)
    if t is None:
        return missing(LEDGER, "L3-STATE-PLANE-DECIDED")
    ok, lines = core_l3(t)
    return verdict(ok, "PASS-L3-STATE-PLANE-DECIDED", "FAIL-L3-STATE-PLANE-DECIDED", lines)


def j_rows3(which, tag):
    tsv, tree = read(JUDGE3[which]), read(TREE)
    if tsv is None:
        return missing(JUDGE3[which], tag + "-ROWS-WELLFORMED")
    if tree is None:
        return missing(TREE, tag + "-ROWS-WELLFORMED")
    ok, lines = core_j_rows(tsv, tree_planes(tree))
    return verdict(ok, "PASS-%s-ROWS-WELLFORMED" % tag, "FAIL-%s-ROWS-WELLFORMED" % tag, lines)


def j_reach3(which, tag):
    tsv = read(JUDGE3[which])
    if tsv is None:
        return missing(JUDGE3[which], tag + "-REACH-OVER-SIX")
    ok, lines = core_j_reach(tsv)
    return verdict(ok, "PASS-%s-REACH-OVER-SIX" % tag, "FAIL-%s-REACH-OVER-SIX" % tag, lines)


def j_blind3(which, tag):
    meta_path = JUDGE3[which][:-4] + ".base"
    meta = read(meta_path)
    if meta is None:
        return missing(meta_path, tag + "-BLIND-AT-BASE")
    m = re.search(r"^base_commit:\s*([0-9a-f]{7,40})\s*$", meta, re.M)
    sib = [p for k, p in JUDGE3.items() if k != which] + [COMPARE3]
    ok, lines = blind_core(m.group(1) if m else None, sib, CANON)
    return verdict(ok, "PASS-%s-BLIND-AT-BASE" % tag, "FAIL-%s-BLIND-AT-BASE" % tag, lines)


def j10_unbriefed():
    t = read(TO_J10)
    if t is None:
        return missing(TO_J10, "J10-UNBRIEFED-ORDER")
    ok, lines = core_j10(t)
    return verdict(ok, "PASS-J10-UNBRIEFED-ORDER", "FAIL-J10-UNBRIEFED-ORDER", lines)


def _j11_inputs(tag):
    c = read(COMPARE3)
    if c is None:
        missing(COMPARE3, tag)
        return None
    tsvs = {}
    for k, p in JUDGE3.items():
        t = read(p)
        if t is None:
            missing(p, tag)
            return None
        tsvs[k] = t
    return c, tsvs


def j11_intersection():
    got = _j11_inputs("J11-INTERSECTION-FIRST")
    if got is None:
        return 0
    tree = read(TREE)
    if tree is None:
        return missing(TREE, "J11-INTERSECTION-FIRST")
    ok, lines = core_j11_intersection(got[0], got[1], tree_planes(tree))
    return verdict(ok, "PASS-J11-INTERSECTION-FIRST", "FAIL-J11-INTERSECTION-FIRST", lines)


def j11_rollup():
    got = _j11_inputs("J11-ROLLUP-RECOUNTED")
    if got is None:
        return 0
    ok, lines = core_j11_rollup(*got)
    return verdict(ok, "PASS-J11-ROLLUP-RECOUNTED", "FAIL-J11-ROLLUP-RECOUNTED", lines)


def j11_traced():
    got = _j11_inputs("J11-DIVERGENCE-TRACED")
    if got is None:
        return 0
    ok, lines = core_j11_traced(got[0], got[1], len((_canon() or "").splitlines()))
    return verdict(ok, "PASS-J11-DIVERGENCE-TRACED", "FAIL-J11-DIVERGENCE-TRACED", lines)


def j11_reach():
    got = _j11_inputs("J11-UNION-REACH")
    if got is None:
        return 0
    ok, lines = core_j11_reach(*got)
    return verdict(ok, "PASS-J11-UNION-REACH", "FAIL-J11-UNION-REACH", lines)


SUBCOMMANDS = {
    "o3-sovereign": o3_sovereign,
    "k3-contentdiff": k3_contentdiff,
    "regress-recount": regress_recount,
    "regress-reach": regress_reach,
    "k4-producer": k4_producer,
    "k5-census": k5_census,
    "k5-coordinates": k5_coordinates,
    "k5-r1-vintage": k5_r1_vintage,
    "k5-short-sovereign": k5_short_sovereign,
    "l3-state-plane": l3_state_plane,
    "j8-rows": lambda: j_rows3("f", "J8"), "j9-rows": lambda: j_rows3("g", "J9"),
    "j10-rows": lambda: j_rows3("h", "J10"),
    "j8-reach": lambda: j_reach3("f", "J8"), "j9-reach": lambda: j_reach3("g", "J9"),
    "j10-reach": lambda: j_reach3("h", "J10"),
    "j8-blind": lambda: j_blind3("f", "J8"), "j9-blind": lambda: j_blind3("g", "J9"),
    "j10-blind": lambda: j_blind3("h", "J10"),
    "j10-unbriefed": j10_unbriefed,
    "j11-intersection": j11_intersection,
    "j11-rollup": j11_rollup,
    "j11-traced": j11_traced,
    "j11-reach": j11_reach,
}


# ------------------------------------------------------------------ v2 self-test fixtures
_CANON_OK = "\n".join([
    "# 02 -- THE CANON -- v1.1", "RULES CARRYING ALL THREE PARTS: 2 of 2", "## rules",
    "**R1 -- A.** x", "- authority: a", "- census: 5 of 5 (as of 01_CENSUS.md @d35653da5e)",
    "- non-application: none", "- resolves R-9(iii) C2: key grammar against the census clearance",
    "**R10 -- B.** y", "- authority: b", "- census: c", "- non-application: none",
    "- resolves R-9(iii) C1: monolith clearance read with R9", "## end"])
_CANON_4 = _CANON_OK.replace("## end", "\n".join([
    "**R6 -- C.** z", "- resolves R-9(iii) C3: which bucket, with R5",
    "**R19 -- D.** w", "- resolves R-9(iii) C4: duration and in-flight, with R18", "## end"]))
_CHECK_OK = "\n".join([
    "## THE INPUTS", "| input | mark | who | where |", "|---|---|---|---|",
    "| the LONG form | **SOVEREIGN** | Andrew | Step 1 |", "| the SHORT form | **SOVEREIGN** | Andrew | Step 1 |",
    "| display name | GIVEN | firm | tenant |", "Three rows: two SOVEREIGN, one GIVEN, none chosen.", "## NEXT"])
_LEDGER_OK = "\n".join([
    "## \u00a72. FIRMS", "| bucket . plane | objects | newest | rules | disposition | decided |", "|---|---|---|---|---|---|",
    "| `opal-data-bd/gold/_state/` | 3 | 09-12 | R21 | MIGRATE -> state/ | DECIDED |",
    "| `opal-data-bd/gold/` | 9 | 09-12 | R5 | MIGRATE, absorbs gold/state/code | DECIDED |", "## \u00a73. NEXT"])
_TREE_OK = "## The planes\n| plane | tier |\n|---|---|\n| `p/one/` | bronze |\n| `p/two/` | silver |\n## What next\n"


def _tsv(rows):
    head = "\t".join(COLS)
    return "\n".join([head] + ["\t".join(r) for r in rows]) + "\n"


_R = "A1:R9; A2:R4; A3:R1; A4:R13; A5:R10"
_TSV_F = _tsv([["p/one/", "CONFORMS", "CONFORMS", "VIOLATES", "UNDETERMINED", "CONFORMS", _R, "VIOLATES", "R1", "R3", "w"],
               ["p/two/", "CONFORMS", "CONFORMS", "CONFORMS", "CONFORMS", "CONFORMS", _R, "CONFORMS", "R10", "none", "w"]])
_TSV_H = _TSV_F.replace("VIOLATES\tR1\tR3", "UNDETERMINED\tR13\tR21")
_CMP_OK = "\n".join([
    "PLANE INTERSECTION F.G.H: 2 of 2", "POSITIVE CONTROL F.F: 2 of 2",
    "ROLL-UP AGREE F.G.H: 1 of 2", "ROLL-UP AGREE F.G: 2 of 2", "ROLL-UP AGREE F.H: 1 of 2",
    "ROLL-UP AGREE G.H: 1 of 2", "ROLL-UP DIVERGE: 1 of 2",
    "DIVERGE `p/one/` F,G VIOLATES vs H UNDETERMINED -- infra/logic/02_DOCTRINE.md:5",
    "UNION REACHED: 2 of 6"])


def selftest_v2():
    """[(name, behaved, detail)] -- every v2 core driven ALONE on a GREEN fixture that must PASS and a
    DOCTORED fixture that must FAIL. Both halves are required: a suite of refusals alone passes a
    core that refuses everything."""
    tsvs = {"f": _TSV_F, "g": _TSV_F, "h": _TSV_H}
    pairs = [
        ("k5-census", core_k5_census(_CANON_OK)[0], core_k5_census(_CANON_OK.replace("v1.1", "v1.0"))[0],
         "a typed count that disagrees with the recount / a v1.0 title"),
        ("k5-coordinates", core_k5_coords(_CANON_4)[0], core_k5_coords(_CANON_OK)[0], "two of four coordinates"),
        ("k5-r1-vintage", core_k5_r1(_CANON_OK)[0],
         core_k5_r1(_CANON_OK.replace(" (as of 01_CENSUS.md @d35653da5e)", ""))[0], "census line without vintage"),
        ("k5-short-sovereign", core_k5_short(_CHECK_OK)[0],
         core_k5_short(_CHECK_OK.replace("SHORT form | **SOVEREIGN**", "SHORT form | **SOVEREIGN** else DERIVED"))[0],
         "SHORT row marked SOVEREIGN-or-DERIVED"),
        ("k4-producer", core_k4_producer(
            "EXCLUSION-PREDICATE producer: 0 consumer(s) of 40 file(s) scanned\nEXCLUDED: %s -- none\n" % PRODUCER)[0],
         core_k4_producer("EXCLUSION-PREDICATE producer: 2 consumer(s) of 40 file(s) scanned\nEXCLUDED: %s\n"
                          % PRODUCER)[0], "an exclusion held while two consumers exist"),
        ("l3-state-plane", core_l3(_LEDGER_OK)[0],
         core_l3(_LEDGER_OK.replace("| `opal-data-bd/gold/_state/` | 3 | 09-12 | R21 | MIGRATE -> state/ | DECIDED |\n",
                                    ""))[0], "state/ named in prose with no row"),
        ("j-rows", core_j_rows(_TSV_F, tree_planes(_TREE_OK))[0],
         core_j_rows(_TSV_F.replace("\tVIOLATES\tR1\t", "\tDEPARTS-RECOMMENDED\tR1\t"), tree_planes(_TREE_OK))[0],
         "a worst verdict none of the row's axes carries"),
        ("j-reach", core_j_reach(_TSV_F)[0], core_j_reach(_TSV_F.replace("\tR3\t", "\tsome\t"))[0],
         "a reach token that is not a rule id"),
        ("j10-unbriefed", core_j10("judge the tree; name the most-severe finding")[0],
         core_j10("read CN_SEVERITY.md: CONFORMS < VIOLATES")[0], "a leaked severity order"),
        ("j11-intersection", core_j11_intersection(_CMP_OK, tsvs, ["p/one/", "p/two/"])[0],
         core_j11_intersection("ROLL-UP AGREE F.G.H: 1 of 2\n" + _CMP_OK, tsvs, ["p/one/", "p/two/"])[0],
         "a ROLL-UP printed before the intersection"),
        ("j11-rollup", core_j11_rollup(_CMP_OK, tsvs)[0],
         core_j11_rollup(_CMP_OK.replace("F.H: 1 of 2", "F.H: 2 of 2"), tsvs)[0], "a mis-typed pair count"),
        ("j11-traced", core_j11_traced(_CMP_OK, tsvs, 50)[0],
         core_j11_traced(_CMP_OK.replace(" -- infra/logic/02_DOCTRINE.md:5", ""), tsvs, 50)[0],
         "a divergence with no canon line"),
        ("j11-reach", core_j11_reach(_CMP_OK, tsvs)[0],
         core_j11_reach(_CMP_OK.replace("2 of 6", "3 of 6"), tsvs)[0], "a mis-typed union"),
        ("j-blind", blind_core("HEAD", [EX3 + "/no-such-sibling.tsv"], CANON, require_v11=False)[0],
         blind_core("HEAD", [CANON], CANON, require_v11=False)[0],
         "a sibling PRESENT at base (the canon itself planted as the sibling)"),
        ("j-blind-base", blind_core("HEAD", [], CANON, require_v11=False)[0],
         blind_core("0000000", [], CANON, require_v11=False)[0], "a base that resolves to no commit"),
    ]
    out = []
    for name, green, doctored, detail in pairs:
        out.append((name + "-green-passes", bool(green), "the GREEN fixture passes"))
        out.append((name + "-doctored-fails", not doctored, detail))
    return out


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

    results.extend(selftest_v2())
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
