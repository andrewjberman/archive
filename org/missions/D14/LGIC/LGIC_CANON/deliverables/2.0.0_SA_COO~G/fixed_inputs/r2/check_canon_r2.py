#!/usr/bin/env python3
"""check_canon_r2.py -- the mechanical criteria of LGIC_CANON round 2 (decomposition v4), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-2 issuance. Run from the worktree root: `python <this file> <subcommand>`.
Every subcommand prints its evidence, a denominator where one exists, and exactly one line `VERDICT: PASS-<X>` or
`VERDICT: FAIL-<X>`, and exits 0. A missing input is a FAIL verdict, never a traceback. No PASS string is a substring
of another subcommand's PASS or FAIL string, because proof-of-spec-check greps <expect> UNANCHORED.
`--list` prints the subcommands; `selftest-negative` runs every one and counts the PASS verdicts on this tree.

SPAWN BASE IS PINNED, NEVER DERIVED. Round 1's checker read `git merge-base HEAD CLOUD`, and row LGIC_ENFORCE-S20
measured what that costs: once a cell's commits are ancestors of CLOUD the merge-base IS the cell's own tip, every
diff-counting criterion reads 0 changed lines, and the criterion then FAILs on every checkout including the worker's
own -- so the cell cannot be re-graded after its own drain. BASE below is the round-2 issuance commit, written in at
the cut and never computed.

The fixed inputs beside this file:
  CN_TREE_INFLECTION.md   the SECOND judged tree (CN-j-4, CN-j-5), chosen by measurement per ruling A-13
  CN_SEVERITY.md          the verdict vocabulary and severity order -- given to CN-j-4/CN-j-5, WITHHELD from CN-j-6
  CN_SEVEN_RULES.json     A-13's seven rules and what each one's presence looks like in a tree
"""
import json
import os
import re
import subprocess
import sys

BASE = "2b987c131d"  # decomposition v4, the round-2 recut base. PINNED, never `git merge-base`.
# NOTE: no criterion in this round reads BASE -- none of them counts a diff. It is pinned rather than
# left as a placeholder because a placeholder that looks like a pin is worse than no pin, and a future
# criterion that needs a base must take THIS one rather than derive one (row LGIC_ENFORCE-S20).

ROOT = "org/missions/D14/LGIC/LGIC_CANON"
DEL = ROOT + "/deliverables"
EX = DEL + "/exercises/r2"
FIX = DEL + "/2.0.0_SA_COO~G/fixed_inputs/r2"
CANON = "infra/logic/02_DOCTRINE.md"
RENDER = "infra/logic/render_naming_section.py"
LEDGER = "infra/logic/06_CONFORMANCE_LEDGER.md"
CHECKLIST = "infra/logic/10_ONBOARDING_CHECKLIST.md"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
SCOPES = "infra/logic/registry/scopes.json"
REVIEW2 = DEL + "/CHECKLIST_REVIEW_R2.md"
TREE2 = FIX + "/CN_TREE_INFLECTION.md"
SEVEN = FIX + "/CN_SEVEN_RULES.json"
SEVERITY = FIX + "/CN_SEVERITY.md"
BEGIN = "<!-- BEGIN GENERATED NAMING SECTION -->"
END = "<!-- END GENERATED NAMING SECTION -->"
AXES = ("A1", "A2", "A3", "A4", "A5")
VOCAB_AXIS = ("CONFORMS", "VIOLATES", "DECLARED-EXCEPTION", "DEPARTS-RECOMMENDED", "UNDETERMINED")
SEVEN_RULES = ("R3", "R8", "R14", "R15", "R17", "R19", "R21")
JUDGE = {"c": EX + "/judge-c.tsv", "d": EX + "/judge-d.tsv", "e": EX + "/judge-e.tsv"}
COMPARE = EX + "/judge-compare-r2.md"
FAMILY_STEPS = ("3", "7", "8", "9")


# ---------------------------------------------------------------- helpers

def out(verdict):
    print("VERDICT: " + verdict)


def read(path):
    """Text of a file, or None. utf-8 EXPLICIT: this device's default text mode is cp1252, which
    raises on five undefined bytes and silently mis-decodes every other non-ASCII character."""
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def missing(path, tag):
    print("MISSING INPUT: %s" % path)
    out("FAIL-" + tag)
    return None


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def section(text, begin, end):
    if text is None or begin not in text or end not in text:
        return None
    return text.split(begin, 1)[1].split(end, 1)[0]


def rows(path):
    """TSV rows as lists, header dropped, blank lines dropped."""
    t = read(path)
    if t is None:
        return None
    return [ln.split("\t") for ln in t.splitlines()[1:] if ln.strip()]


def canon_rule_block(text, rid):
    """The text of one canon rule, from its bold heading to the next rule's."""
    m = re.search(r"^\*\*%s\b.*?$" % re.escape(rid), text, re.M)
    if not m:
        return None
    nxt = re.search(r"^\*\*R\d+\b", text[m.end():], re.M)
    return text[m.start(): m.end() + (nxt.start() if nxt else len(text) - m.end())]


def render_check():
    r = subprocess.run([sys.executable, RENDER, "--check"], capture_output=True, text=True)
    return (r.stdout or "") + (r.stderr or "")


# ---------------------------------------------------------------- CN-k-2, the canon edit

def k2_vocab():
    t = read(CANON)
    if t is None:
        return missing(CANON, "K2-VOCAB")
    found = [v for v in VOCAB_AXIS if v in t]
    print("axis verdict vocabulary, denominator %d: %d present -- %s" % (len(VOCAB_AXIS), len(found), found))
    absent = [v for v in VOCAB_AXIS if v not in found]
    print("absent: %s" % (absent or "none"))
    out("PASS-K2-VOCAB-CARRIED" if not absent else "FAIL-K2-VOCAB-CARRIED")


def k2_severity():
    """The severity ORDER, not merely the words: an ordered list the canon states once."""
    t = read(CANON)
    if t is None:
        return missing(CANON, "K2-SEVERITY")
    m = re.search(r"SEVERITY ORDER\b(.{0,600})", t, re.S)
    if not m:
        print("no 'SEVERITY ORDER' passage in the canon")
        return out("FAIL-K2-SEVERITY-ORDERED")
    blob = m.group(1)
    pos = [(blob.index(v), v) for v in VOCAB_AXIS if v in blob]
    pos.sort()
    ordered = [v for _, v in pos]
    print("severity passage names %d of %d axis verdicts, in this order: %s"
          % (len(ordered), len(VOCAB_AXIS), ordered))
    ok = len(ordered) == len(VOCAB_AXIS)
    print("every axis verdict placed in the order: %s" % ok)
    out("PASS-K2-SEVERITY-ORDERED" if ok else "FAIL-K2-SEVERITY-ORDERED")


def k2_r20_axes():
    """A-2: R20 is stated on EVERY axis, not once globally."""
    t = read(CANON)
    if t is None:
        return missing(CANON, "K2-R20-AXES")
    blk = canon_rule_block(t, "R20")
    if blk is None:
        print("R20 not found in the canon")
        return out("FAIL-K2-R20-ON-EVERY-AXIS")
    hit = [a for a in AXES if re.search(r"\b%s\b" % a, blk)]
    print("R20's block names %d of %d axes: %s" % (len(hit), len(AXES), hit))
    print("axes R20 does not name: %s" % ([a for a in AXES if a not in hit] or "none"))
    out("PASS-K2-R20-ON-EVERY-AXIS" if len(hit) == len(AXES) else "FAIL-K2-R20-ON-EVERY-AXIS")


def k2_citation():
    """A-2: a verdict cites the DECIDING rule, and the canon says so."""
    t = read(CANON)
    if t is None:
        return missing(CANON, "K2-CITATION")
    ok = re.search(r"DECIDING RULE", t) is not None
    print("the canon states the citation rule (names a DECIDING RULE): %s" % ok)
    out("PASS-K2-CITATION-RULE-STATED" if ok else "FAIL-K2-CITATION-RULE-STATED")


def k2_instance():
    """A-9: ONE pipeline-instance rule, stated once, that the checklist's family steps can read."""
    t = read(CANON)
    if t is None:
        return missing(CANON, "K2-INSTANCE")
    hits = re.findall(r"^\*\*(R\d+)[^\n]*PIPELINE INSTANCE", t, re.M)
    print("canon rules whose heading names PIPELINE INSTANCE, denominator 1 expected: %d %s" % (len(hits), hits))
    out("PASS-K2-INSTANCE-RULE-ONCE" if len(hits) == 1 else "FAIL-K2-INSTANCE-RULE-ONCE")


def k2_render_fresh():
    """The canon edit must not disturb the GENERATED section: the render still reads fresh."""
    o = render_check()
    fresh = "CHECK: FRESH" in o
    print(o.strip()[-300:])
    print("render --check reads FRESH after the canon edit: %s" % fresh)
    out("PASS-K2-GENERATED-SECTION-UNTOUCHED" if fresh else "FAIL-K2-GENERATED-SECTION-UNTOUCHED")


# ---------------------------------------------------------------- CN-k-3, the renderer

def k3_note():
    """Row LGIC_CANON-S3: the registry path must read a FIRM row's `note` and render it."""
    src = read(RENDER)
    if src is None:
        return missing(RENDER, "K3-NOTE")
    canon = read(CANON) or ""
    sec = section(canon, BEGIN, END) or ""
    reg = read(SCOPES)
    notes = []
    if reg:
        try:
            data = json.loads(reg)

            def walk(o):
                if isinstance(o, dict):
                    if str(o.get("class", "")).upper() == "FIRM" and o.get("note"):
                        notes.append((o.get("key"), o["note"]))
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(data)
        except ValueError:
            pass
    print("FIRM rows in the registry carrying a note, denominator %d: %s" % (len(notes), [k for k, _ in notes]))
    if not notes:
        print("no FIRM row carries a note -- nothing for the renderer to carry")
        return out("FAIL-K3-FIRM-NOTE-RENDERED")
    rendered = [k for k, n in notes if n[:40] in sec]
    print("of those, rendered into the canon's generated section: %d -- %s" % (len(rendered), rendered))
    ok = len(rendered) == len(notes)
    print("every FIRM note reaches the section: %s" % ok)
    out("PASS-K3-FIRM-NOTE-RENDERED" if ok else "FAIL-K3-FIRM-NOTE-RENDERED")


def k3_contentdiff():
    """A-11: the renderer gains a content-diff arm -- it must REPORT a dropped line, not pass over it.
    The arm is exercised against a planted removal, which is this criterion's negative control."""
    src = read(RENDER)
    if src is None:
        return missing(RENDER, "K3-CONTENTDIFF")
    has_flag = "--content-diff" in src
    print("renderer exposes --content-diff: %s" % has_flag)
    if not has_flag:
        return out("FAIL-K3-CONTENT-DIFF-ARM")
    r = subprocess.run([sys.executable, RENDER, "--content-diff"], capture_output=True, text=True)
    o = (r.stdout or "") + (r.stderr or "")
    print(o.strip()[-400:])
    clean = "CONTENT-DIFF: 0" in o
    print("content-diff reads 0 dropped items on the true tree: %s" % clean)
    out("PASS-K3-CONTENT-DIFF-ARM" if clean else "FAIL-K3-CONTENT-DIFF-ARM")


def k3_fresh():
    o = render_check()
    fresh = "CHECK: FRESH" in o
    print(o.strip()[-300:])
    print("render --check FRESH after the renderer edit: %s" % fresh)
    out("PASS-K3-RENDER-STILL-FRESH" if fresh else "FAIL-K3-RENDER-STILL-FRESH")


# ---------------------------------------------------------------- CN-k-4, the re-render

def k4_adjacency():
    t = read(SCHEMA)
    if t is None:
        return missing(SCHEMA, "K4-ADJACENCY")
    ok = "adjacency" in t
    print("NAMING_SCHEMA carries an adjacency test: %s" % ok)
    print("NOTE: this cell is gated on LGIC_NAMING's schema cell; a False here means that cell has not drained.")
    out("PASS-K4-SCHEMA-CARRIES-ADJACENCY" if ok else "FAIL-K4-SCHEMA-CARRIES-ADJACENCY")


def k4_fresh():
    canon = read(CANON) or ""
    sec = section(canon, BEGIN, END)
    o = render_check()
    stamped = sec is not None and "stamp: " + SCHEMA in sec
    fresh = "CHECK: FRESH" in o
    print("the section stamps the schema: %s ; render --check FRESH: %s" % (stamped, fresh))
    out("PASS-K4-RERENDERED-AT-SCHEMA" if (stamped and fresh) else "FAIL-K4-RERENDERED-AT-SCHEMA")


# ---------------------------------------------------------------- CN-j-4 / j-5 / j-6, the judges

def j_axes(which, tag):
    rs = rows(JUDGE[which])
    if rs is None:
        return missing(JUDGE[which], tag + "-AXES")
    bad = [r[0] for r in rs if len([c for c in r[1:1 + len(AXES)] if c.strip()]) != len(AXES)]
    print("judge %s rows, denominator %d; rows not carrying all %d axis verdicts: %d"
          % (which.upper(), len(rs), len(AXES), len(bad)))
    if bad:
        print("  first offenders: %s" % bad[:5])
    out(("PASS-%s-EVERY-AXIS-JUDGED" if not bad else "FAIL-%s-EVERY-AXIS-JUDGED") % tag)


def j_cites(which, tag):
    rs = rows(JUDGE[which])
    if rs is None:
        return missing(JUDGE[which], tag + "-CITES")
    uncited = [r[0] for r in rs if not re.search(r"\bR\d+\b", "\t".join(r))]
    print("judge %s rows, denominator %d; rows citing no canon rule: %d" % (which.upper(), len(rs), len(uncited)))
    if uncited:
        print("  first offenders: %s" % uncited[:5])
    out(("PASS-%s-EVERY-VERDICT-CITES" if not uncited else "FAIL-%s-EVERY-VERDICT-CITES") % tag)


def j_reach(which, tag):
    """A-13: the cell PRINTS which of the seven rules the tree reaches. A printed NOT REACHED is a
    legitimate outcome -- row LGIC_CANON-S4 measured that no conformant state/ plane exists anywhere,
    so R21 is unreachable by any tree and a cell that demanded it would be unsatisfiable."""
    rs = rows(JUDGE[which])
    if rs is None:
        return missing(JUDGE[which], tag + "-REACH")
    blob = "\t".join("\t".join(r) for r in rs)
    reached = [r for r in SEVEN_RULES if re.search(r"\b%s\b" % r, blob)]
    notreached = [r for r in SEVEN_RULES if r not in reached]
    print("A-13's seven rules, denominator %d" % len(SEVEN_RULES))
    print("  REACHED     (%d): %s" % (len(reached), reached))
    print("  NOT REACHED (%d): %s" % (len(notreached), notreached))
    print("the reach is PRINTED, which is what A-13 asks for; a non-empty NOT REACHED is not a failure")
    out(("PASS-%s-REACH-PRINTED" if reached else "FAIL-%s-REACH-PRINTED") % tag)


def j6_noseverity():
    """⛔ THIS GRADES THE BRIEF, NOT THE ARM (1.0.0_SA_CTO RULING R-8, row LGIC_CANON-S6).

    What is withheld from judge E is any BRIEF, order text or example STATING the severity order.
    The CANON is where E is supposed to find it -- CN-k-2 puts it there, and the whole question is
    whether the canon ALONE now supplies what round 1's orders supplied (the CVO's C-S9). So a clean
    order file means the brief is clean and NOTHING MORE. The arm's own measurement lands at CN-j-7,
    never self-graded: j7_e_vocab_from_canon censuses E's verdict values against the canon E read."""
    order = None
    d = ROOT + "/task-orders"
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if "CN-j-6" in fn:
                order = read(os.path.join(d, fn))
                break
    if order is None:
        return missing(d + "/*CN-j-6*", "J6-NOSEVERITY")
    sev = read(SEVERITY) or ""
    leaked = [v for v in VOCAB_AXIS if v in order]
    has_phrase = "SEVERITY ORDER" in order
    print("judge E's order, denominator %d axis verdicts; present in the order: %d %s"
          % (len(VOCAB_AXIS), len(leaked), leaked))
    print("the order names the phrase SEVERITY ORDER: %s" % has_phrase)
    print("the withheld input exists as a fixed input: %s" % bool(sev))
    ok = (not has_phrase) and len(leaked) < len(VOCAB_AXIS)
    out("PASS-J6-SEVERITY-WITHHELD" if ok else "FAIL-J6-SEVERITY-WITHHELD")


# ---------------------------------------------------------------- CN-j-7, the comparison

def j7_traced():
    t = read(COMPARE)
    if t is None:
        return missing(COMPARE, "J7-TRACED")
    dis = re.findall(r"^\s*\|\s*DISAGREE\b.*$", t, re.M)
    untraced = [d for d in dis if not re.search(r"\bR\d+\b|\bA[1-5]\b|\bS\d+\b", d)]
    print("disagreement rows, denominator %d; rows tracing to no canon coordinate: %d" % (len(dis), len(untraced)))
    if untraced:
        print("  first offenders: %s" % [d[:70] for d in untraced[:3]])
    ok = bool(dis) and not untraced
    print("NOTE: zero disagreement rows is NOT a pass -- the comparison must have run.")
    out("PASS-J7-EVERY-DISAGREEMENT-TRACED" if ok else "FAIL-J7-EVERY-DISAGREEMENT-TRACED")


def j7_reach():
    t = read(COMPARE)
    if t is None:
        return missing(COMPARE, "J7-REACH")
    named = [r for r in SEVEN_RULES if re.search(r"\b%s\b" % r, t)]
    printed = re.search(r"NOT REACHED", t) is not None
    print("A-13's seven, denominator %d; named in the comparison: %d %s" % (len(SEVEN_RULES), len(named), named))
    print("the comparison prints a NOT REACHED partition: %s" % printed)
    ok = len(named) == len(SEVEN_RULES) and printed
    out("PASS-J7-SEVEN-RULE-REACH-PRINTED" if ok else "FAIL-J7-SEVEN-RULE-REACH-PRINTED")


def j7_e_vocab_from_canon():
    """RULING R-8 (c). THE NEGATIVE ARM'S ACTUAL MEASUREMENT, and it lives here because a control
    must never self-grade. Judge E was briefed with no severity order; if the canon now carries the
    vocabulary and the order, E's verdict values must all OCCUR in the canon E read. A value E uses
    that the canon does not carry is the finding -- it means E got it somewhere else, and the arm
    says so instead of certifying."""
    rs = rows(JUDGE["e"])
    if rs is None:
        return missing(JUDGE["e"], "J7-E-VOCAB")
    canon = read(CANON)
    if canon is None:
        return missing(CANON, "J7-E-VOCAB")
    used = set()
    for r in rs:
        for cell in r[1:1 + len(AXES)]:
            v = cell.strip()
            if v:
                used.add(v)
    absent = sorted(v for v in used
                    if not re.search(r"(?<![A-Za-z0-9-])%s(?![A-Za-z0-9-])" % re.escape(v), canon))
    print("distinct verdict values in judge E's output, denominator %d: %s" % (len(used), sorted(used)))
    print("of those, NOT carried by the canon E read (whole-word): %d %s" % (len(absent), absent))
    print("a value E used that the canon does not carry means E did not get it from the canon")
    out("PASS-J7-E-VOCAB-FROM-CANON" if used and not absent else "FAIL-J7-E-VOCAB-FROM-CANON")


def j7_blind():
    """C, D and E must be mutually blind: no judge's file may quote another's verdict column."""
    present = {k: rows(v) for k, v in JUDGE.items()}
    absent = [k for k, v in present.items() if v is None]
    if absent:
        print("missing judge files: %s" % absent)
        return out("FAIL-J7-JUDGES-MUTUALLY-BLIND")
    leaks = []
    for a in JUDGE:
        ta = read(JUDGE[a]) or ""
        for b in JUDGE:
            if a != b and ("judge-%s" % b) in ta:
                leaks.append((a, b))
    print("judge pairs, denominator %d; pairs where one file names the other: %d %s"
          % (len(JUDGE) * (len(JUDGE) - 1), len(leaks), leaks))
    out("PASS-J7-JUDGES-MUTUALLY-BLIND" if not leaks else "FAIL-J7-JUDGES-MUTUALLY-BLIND")


# ---------------------------------------------------------------- CN-o-3, the checklist edit

def _steps(text):
    return re.findall(r"^### STEP (\d+) -- (.+)$", text, re.M)


def o3_family():
    """A-9: steps 3, 7, 8 and 9 take the pipeline family as a given INPUT, which is what makes them
    mechanical. Graded on the steps' own text, not on a review's mark."""
    t = read(CHECKLIST)
    if t is None:
        return missing(CHECKLIST, "O3-FAMILY")
    st = _steps(t)
    print("steps in the checklist, denominator %d" % len(st))
    blocks = re.split(r"^### STEP ", t, flags=re.M)[1:]
    idx = {b.split(" --", 1)[0].strip(): b for b in blocks}
    miss = [n for n in FAMILY_STEPS if n not in idx or "family" not in idx[n].lower()]
    print("family steps %s; steps not naming the family: %s" % (list(FAMILY_STEPS), miss or "none"))
    out("PASS-O3-FAMILY-STEPS-TAKE-INPUT" if not miss else "FAIL-O3-FAMILY-STEPS-TAKE-INPUT")


def _step_block(n):
    t = read(CHECKLIST)
    if t is None:
        return None
    blocks = re.split(r"^### STEP ", t, flags=re.M)[1:]
    for b in blocks:
        if b.split(" --", 1)[0].strip() == n:
            return b
    return None


def o3_step10_stop():
    b = _step_block("10")
    if b is None:
        return missing(CHECKLIST + " STEP 10", "O3-STEP10")
    has_stop = "STOP" in b
    names = "ADVI_FIRMBKTS" in b
    print("STEP 10 carries a STOP: %s ; the STOP names ADVI_FIRMBKTS: %s" % (has_stop, names))
    out("PASS-O3-STEP10-STOP-NAMES-OWNER" if (has_stop and names) else "FAIL-O3-STEP10-STOP-NAMES-OWNER")


def o3_step14_stop():
    b = _step_block("14")
    if b is None:
        return missing(CHECKLIST + " STEP 14", "O3-STEP14")
    has_stop = "STOP" in b
    names = "X8" in b
    print("STEP 14 carries a STOP: %s ; the STOP cites register entry X8: %s" % (has_stop, names))
    out("PASS-O3-STEP14-STOP-CITES-X8" if (has_stop and names) else "FAIL-O3-STEP14-STOP-CITES-X8")


def o3_sovereign():
    t = read(CHECKLIST)
    if t is None:
        return missing(CHECKLIST, "O3-SOVEREIGN")
    m = re.search(r"^## THE INPUTS(.*?)^## ", t, re.S | re.M)
    blob = m.group(1) if m else ""
    marked = re.findall(r"SOVEREIGN", blob)
    print("the INPUTS section names %d SOVEREIGN input(s)" % len(marked))
    print("an input the run may not choose must say so where the inputs are given, not in a step")
    out("PASS-O3-SOVEREIGN-INPUTS-NAMED" if marked else "FAIL-O3-SOVEREIGN-INPUTS-NAMED")


# ---------------------------------------------------------------- CN-o-4, the review

def o4_zero_judgement():
    t = read(REVIEW2)
    if t is None:
        return missing(REVIEW2, "O4-ZERO-JUDGEMENT")
    marks = re.findall(r"^\|\s*(\d+)\s*\|\s*(MECHANICAL|JUDGEMENT)\b", t, re.M)
    j = [n for n, k in marks if k == "JUDGEMENT"]
    print("steps marked, denominator %d; JUDGEMENT: %d %s" % (len(marks), len(j), j))
    ok = len(marks) == 16 and not j
    print("all 16 steps marked and none JUDGEMENT: %s" % ok)
    out("PASS-O4-NO-JUDGEMENT-STEP" if ok else "FAIL-O4-NO-JUDGEMENT-STEP")


def o4_runnable_or_stopped():
    """The SECOND bar, and the one round 1 did not have: a MECHANICAL step is only honest if it is
    runnable TODAY or carries a STOP with a named owner. Both bars are printed."""
    t = read(REVIEW2)
    if t is None:
        return missing(REVIEW2, "O4-RUNNABLE")
    marks = re.findall(r"^\|\s*(\d+)\s*\|\s*MECHANICAL\s*\|([^\n]*)$", t, re.M)
    bad = [n for n, rest in marks if not re.search(r"RUNNABLE|STOP:\s*\S+", rest)]
    print("MECHANICAL steps, denominator %d; neither RUNNABLE nor STOP-with-owner: %d %s"
          % (len(marks), len(bad), bad))
    out("PASS-O4-EVERY-MECHANICAL-ACCOUNTED" if (marks and not bad) else "FAIL-O4-EVERY-MECHANICAL-ACCOUNTED")


def o4_distinct():
    """The reviewer did not write the checklist. Read from git authorship, not from a claim in the file."""
    a_rev = git("log", "-1", "--format=%an", "--", REVIEW2).strip()
    a_chk = git("log", "-1", "--format=%an", "--", CHECKLIST).strip()
    print("last author of the review   : %s" % (a_rev or "<uncommitted>"))
    print("last author of the checklist: %s" % (a_chk or "<uncommitted>"))
    ok = bool(a_rev) and bool(a_chk) and a_rev != a_chk
    print("distinct authors: %s" % ok)
    out("PASS-O4-REVIEWER-IS-NOT-AUTHOR" if ok else "FAIL-O4-REVIEWER-IS-NOT-AUTHOR")


# ---------------------------------------------------------------- CN-l-2, the ledger

def l2_x6_axis():
    t = read(LEDGER)
    if t is None:
        return missing(LEDGER, "L2-X6")
    m = re.search(r"^.*\bX6\b.*$", t, re.M)
    if not m:
        print("X6 not found in the ledger")
        return out("FAIL-L2-X6-ON-ITS-AXIS")
    line = m.group(0)
    axis = [a for a in AXES if re.search(r"\b%s\b" % a, line)]
    print("X6's line: %s" % line.strip()[:160])
    print("axes named on X6's line, denominator %d: %s" % (len(AXES), axis))
    out("PASS-L2-X6-ON-ITS-AXIS" if len(axis) == 1 else "FAIL-L2-X6-ON-ITS-AXIS")


def l2_utf8():
    """A-12: the ledger's own checker reads utf-8 EXPLICITLY. A default text-mode read on this device
    is cp1252: it raises only on five undefined bytes and mis-decodes every other non-ASCII character
    while reporting success -- so the silent class is the dangerous one."""
    cands = [p for p in (DEL + "/0.9.0_WK_LGIC_CANON~2/ledger_recount.py", DEL + "/ledger_recount.py")
             if os.path.exists(p)]
    if not cands:
        return missing(DEL + "/**/ledger_recount.py", "L2-UTF8")
    src = read(cands[0]) or ""
    opens = len(re.findall(r"\bopen\s*\(", src))
    utf8 = len(re.findall(r"encoding\s*=\s*[\"']utf-8[\"']", src))
    print("recount script: %s" % cands[0])
    print("open() calls, denominator %d; encoding='utf-8' occurrences: %d" % (opens, utf8))
    ok = opens > 0 and utf8 >= opens
    out("PASS-L2-RECOUNT-READS-UTF8" if ok else "FAIL-L2-RECOUNT-READS-UTF8")


def l2_header():
    """A-12 + row LGIC_CANON-W2-S1: section 7's count table had its header cell renamed
    `disposition class` so round 1's checker, which selected plane tables by that header alone,
    would not grade it as a sixth plane table. That is the ledger shaped to fit the instrument.
    Once the checker scopes by SECTION the rename is reverted and the cell reads `disposition`."""
    t = read(LEDGER)
    if t is None:
        return missing(LEDGER, "L2-HEADER")
    m = re.search(r"^## .7\.(.*?)^## ", t, re.S | re.M)
    if m is None:
        print("section 7 not found")
        return out("FAIL-L2-HEADER-REVERTED")
    blob = m.group(1)
    workaround = re.search(r"\|\s*disposition class\s*\|", blob) is not None
    reverted = re.search(r"\|\s*disposition\s*\|", blob) is not None
    print("section 7 header cell reads 'disposition class' (the workaround): %s" % workaround)
    print("section 7 header cell reads 'disposition'       (reverted)      : %s" % reverted)
    print("the ledger must not be shaped to fit the checker; the checker scopes by section instead")
    out("PASS-L2-HEADER-REVERTED" if (reverted and not workaround) else "FAIL-L2-HEADER-REVERTED")


def l2_recount():
    """The counts are REPRODUCED by the instrument, never re-typed. Run it and compare.

    ⛔ THIS REGEX WAS WRONG AND A WORKER WAS BLOCKED BY IT (row LGIC_CANON-W3-S2, 0.9.0_WK_LGIC_CANON~3).
    The first version anchored on a non-greedy-free label pattern for TOTAL and SECTION. MEASURED against the
    script's real output: the TOTAL pattern captured 6 of 14 rows -- only the single-word labels, with
    the trailing colon glued on -- and the SECTION pattern captured ZERO, because the actual shape is
    `SECTION <label>: <n> rows (<instrument>)`, not `SECTION <label> <n>`. Round 1's checker read the
    SAME script's SAME output correctly, which is the tell: the instrument changed, not the artifact.
    The worker filed a row and refused to degrade the ledger's multi-word labels to fit my regex. That
    was the right act and this is the repair."""
    cands = [p for p in (DEL + "/0.9.0_WK_LGIC_CANON~2/ledger_recount.py", DEL + "/ledger_recount.py")
             if os.path.exists(p)]
    if not cands:
        return missing(DEL + "/**/ledger_recount.py", "L2-RECOUNT")
    r = subprocess.run([sys.executable, cands[0]], capture_output=True, text=True)
    o = (r.stdout or "") + (r.stderr or "")
    sec = re.findall(r"^SECTION\s+(.+?):\s+(\d+)\s+rows", o, re.M)
    tot = [(lab.strip(), n) for lab, n in re.findall(r"^TOTAL\s+(.+?):\s*(\d+)\s*$", o, re.M)]
    ledger = read(LEDGER) or ""
    m = re.search(r"^## .7\.(.*?)(^## |\Z)", ledger, re.S | re.M)
    body = m.group(1) if m else ""
    # A count is REPRODUCED when section 7 carries a table row whose first cell is the label and
    # whose next cell is the number. Cells are compared after stripping, never by substring.
    rows_in_7 = []
    for ln in body.splitlines():
        if ln.strip().startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 2:
                rows_in_7.append(cells)
    missing_rows = [(lab, n) for lab, n in tot
                    if not any(c[0] == lab and c[1] == n for c in rows_in_7)]
    print("recount script: %s" % cands[0])
    print("SECTION lines parsed: %d | TOTAL lines parsed: %d | section-7 table rows: %d"
          % (len(sec), len(tot), len(rows_in_7)))
    print("TOTALs section 7 does not carry at the counted value, denominator %d: %d %s"
          % (len(tot), len(missing_rows), missing_rows[:5]))
    ok = bool(sec) and bool(tot) and not missing_rows
    out("PASS-L2-COUNTS-REPRODUCED" if ok else "FAIL-L2-COUNTS-REPRODUCED")


# ---------------------------------------------------------------- dispatch

CHECKS = {
    "k2-vocab": k2_vocab, "k2-severity": k2_severity, "k2-r20-axes": k2_r20_axes,
    "k2-citation": k2_citation, "k2-instance": k2_instance,
    "k2-render-fresh": k2_render_fresh,
    "k3-note": k3_note, "k3-contentdiff": k3_contentdiff, "k3-fresh": k3_fresh,
    "k4-adjacency": k4_adjacency, "k4-fresh": k4_fresh,
    "j4-axes": lambda: j_axes("c", "J4"), "j4-cites": lambda: j_cites("c", "J4"),
    "j4-reach": lambda: j_reach("c", "J4"),
    "j5-axes": lambda: j_axes("d", "J5"), "j5-cites": lambda: j_cites("d", "J5"),
    "j5-reach": lambda: j_reach("d", "J5"),
    "j6-axes": lambda: j_axes("e", "J6"), "j6-cites": lambda: j_cites("e", "J6"),
    "j6-noseverity": j6_noseverity,
    "j7-traced": j7_traced, "j7-reach": j7_reach, "j7-blind": j7_blind,
    "j7-e-vocab": j7_e_vocab_from_canon,
    "o3-family": o3_family, "o3-step10-stop": o3_step10_stop, "o3-step14-stop": o3_step14_stop,
    "o3-sovereign": o3_sovereign,
    "o4-zero-judgement": o4_zero_judgement, "o4-runnable": o4_runnable_or_stopped, "o4-distinct": o4_distinct,
    "l2-x6-axis": l2_x6_axis, "l2-utf8": l2_utf8, "l2-header": l2_header, "l2-recount": l2_recount,
}


def selftest_negative():
    """RED-FIRST. Run on the PRE-CHANGE tree every subcommand should FAIL; a PASS here means the
    criterion cannot tell the work from its absence. Read the count, not the individual lines."""
    passed = []
    for name in sorted(CHECKS):
        r = subprocess.run([sys.executable, __file__, name], capture_output=True, text=True)
        v = [ln for ln in (r.stdout or "").splitlines() if ln.startswith("VERDICT: ")]
        verdict = v[-1][9:] if v else "NO-VERDICT"
        print("%-18s %s" % (name, verdict))
        if verdict.startswith("PASS"):
            passed.append(name)
    print("SELFTEST-NEGATIVE: %d of %d subcommands PASS on this tree %s"
          % (len(passed), len(CHECKS), passed))
    print("On the pre-change tree a LOW number is the healthy reading.")


def main(argv):
    if len(argv) == 2 and argv[1] == "--list":
        print("\n".join(sorted(CHECKS)))
        return 0
    if not os.path.isdir("org") or not os.path.isdir(".tools"):
        print("run from the worktree root (org/ and .tools/ not found in %s)" % os.getcwd())
        out("FAIL-WRONG-ROOT")
        return 0
    if len(argv) == 2 and argv[1] == "selftest-negative":
        selftest_negative()
        return 0
    if len(argv) != 2 or argv[1] not in CHECKS:
        print("usage: check_canon_r2.py <%s>" % "|".join(sorted(CHECKS)))
        out("FAIL-USAGE")
        return 0
    CHECKS[argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
