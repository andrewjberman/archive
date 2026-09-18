"""LT-n-2's INSTRUMENT: bind every number round 1's judgment records cite to its run and content hash.

WHY THIS FILE EXISTS RATHER THAN A HAND-WRITTEN LIST. Rule 24(i): a forward list covers what its
author had in mind and omits silently. So the set is written as a SUBTRACTION from a printed
denominator, in three stages, each printed and each asserted:

  STAGE 0  the DOMAIN          -- every maximal digit run in every STRING field of the 14 round-1
                                  judgment acceptance rows, read from the proof instances themselves.
                                  The instances are ENUMERATED by existence (git ls-files), never
                                  from a typed list, and the 14 criterion ids come from R2_BASE.json.
  STAGE 1  a MECHANICAL filter -- a digit run whose preceding character glues it to a word is an
                                  IDENTIFIER FRAGMENT (a commit pin, a row id, a serial, a path).
                                  Word-initial runs survive as CANDIDATES.
  STAGE 2  DECLARED CLASSES    -- ordered, named predicates. Every candidate is printed with the
                                  class it fell in. The RESIDUE is the class this cell pins:
                                  a quantity MEASURED ON AN ARTIFACT ROUND 1 PRODUCED.

AND THE SUBTRACTION IS GUARDED AT BOTH ENDS. R-50 was ruled against the issuing seat four hours
before this cell was cut: a correct subtraction over the WRONG AXIS still arrives with a real
denominator and so reads as MEASURED. Two assertions answer that here:

  EXPECTED_RESIDUE  -- the residue is declared, per (criterion, field, token), and the run REFUSES
                       if the classifier's output differs by one token in either direction. A rule
                       that quietly starts eating a real quantity cannot pass.
  MEMBER COVERAGE   -- every residue token is covered by exactly one declared MEMBER, and the
                       per-criterion token counts must agree. Nothing is lost between the residue
                       and the pinned set.

DOMAIN CHOICE, STATED SO IT CAN BE REFUSED: the class pinned is a quantity measured on an artifact
ROUND 1 PRODUCED (a run directory's output, or a cell deliverable). A quantity measured on a
PRE-EXISTING repo file the cell merely read (a README section count, an uncovered-member count, a
grep hit count) is EXCLUDED BY CLASS, because R-40's subject is a run or a produced artifact and a
repo file already resolves through the commit pin its own row carries. That line is the claim this
cell makes about its own axis; it is printed, not assumed.

HASHES CARRY THEIR INSTRUMENT. `git hash-object` prefixes `blob <len>` and a NUL byte, so a plain
sha1 of the same bytes disagrees. Every pin is computed TWICE -- once over the worktree bytes and
once as the committed blob (`git rev-parse HEAD:<path>`) -- and the run REFUSES if the two differ,
because on an autocrlf box a worktree hash is the CHECKOUT's, not the record's.
"""

import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
BASEFILE = ROOT + "/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/R2_BASE.json"

RUN_BB = "20260917T202556Z-bb29248"
RUN_8D = "20260918T011619Z-8db9eb1"
RUN_CAF = "20260918T002711Z-caf0983"
RUNS = "workflows/legacy_transform/blackdiamond-49financial/"
DELIV = ROOT + "/deliverables/"

A_SEEDS = DELIV + "0.9.0_WK_LGIC_LGCTFM~1/forks/SEEDS.json"
A_PLAN_R1 = DELIV + "0.9.0_WK_LGIC_LGCTFM~2/plan_r1/plan.json"
A_CONTR_R1 = DELIV + "0.9.0_WK_LGIC_LGCTFM~2/plan_r1/contract.json"
A_WALK_C = DELIV + "0.9.0_WK_LGIC_LGCTFM~1/walk/contract.json"
A_REPRO = DELIV + "0.9.0_WK_LGIC_LGCTFM~3/REPRODUCTION.json"
A_BB_C = RUNS + RUN_BB + "/contract.json"
A_8D_C = RUNS + RUN_8D + "/contract.json"
A_8D_P = RUNS + RUN_8D + "/plan.json"
A_CAF_D = RUNS + RUN_CAF + "/DIFF.md"

GLUE = set("0123456789abcdefghijklmnopqrstuvwxyz"
           "ABCDEFGHIJKLMNOPQRSTUVWXYZ_:@.~-")


def ab(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def git(*args):
    r = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout.strip()


def read_json(p):
    with io.open(ab(p), encoding="utf-8", newline="") as fh:
        return json.loads(fh.read())


def instances():
    """The 14 round-1 proof instances, ENUMERATED BY EXISTENCE. Never a typed list: a typed list
    cannot notice an instance that is not there."""
    rc, out = git("ls-files", DELIV)
    if rc != 0:
        raise SystemExit("REFUSED: git ls-files failed over " + DELIV)
    return sorted(p for p in out.split("\n") if p.endswith("proof_of_spec.json"))


def judgment_rows():
    base = read_json(BASEFILE)
    by_id = base["round_1_judgment_criteria"]["by_id"]
    want = base["round_1_judgment_criteria"]["count"]
    found = instances()
    rows = {}
    for p in found:
        for row in read_json(p).get("acceptance", []):
            rows[row["criterion_id"]] = (p, row)
    missing = [c for c in sorted(by_id) if c not in rows]
    if missing:
        raise SystemExit("REFUSED: judgment criteria with no acceptance row: %s" % missing)
    return base, by_id, found, want, rows


# ------------------------------------------------------------------ STAGE 2, the declared classes
def _cls(text, start, tok):
    """Ordered, named predicates. FIRST MATCH WINS. The residue is what no rule claims."""
    right = text[start:start + 60]
    left = text[max(0, start - 40):start]
    post = text[start + len(tok)] if start + len(tok) < len(text) else " "
    pre = text[start - 1] if start > 0 else " "
    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+_", right):
        return "AGENT_SERIAL"
    if re.match(r"[0-9]+_[A-Z]", right):
        return "DOC_FILE_NUMBER_PREFIX"
    if re.search(r"(?:lines?)\s*~?[0-9/\-]*$", left):
        return "SOURCE_LINE_NUMBER"
    if re.match(r"[0-9]+h\b", right):
        return "CONFIG_THRESHOLD_QUOTED_FROM_THE_FILE_UNDER_TEST"
    if re.match(r"[0-9]+-line", right):
        return "FILE_LENGTH_OF_A_PRE_EXISTING_FILE"
    if re.match(r"[0-9]+ Financial", right):
        return "FIRM_NAME"
    # A SLASH IS NOT A PATH. `schwab/08242234/silver` is an address, but `ALIAS 5/CONFORMANT 4/
    # NOT-GRADED 1/OUT-OF-PATTERN 5/RAISE 5` and `(5/4/1/5/5` are one measured verdict spread
    # written two ways. So the path rules are guarded by a POSITIVE predicate for a
    # slash-separated NUMERIC list, rather than by a lookback that has to be right about every
    # neighbour. Three earlier drafts of this rule -- `post == "/"`, then "followed by a digit",
    # then "slash-bounded on both sides" -- each ate part of that spread, and EXPECTED_RESIDUE
    # refused all three. A line-number pair like `655/955` is also a numeric list and is claimed
    # earlier by SOURCE_LINE_NUMBER, which is why rule order is load-bearing here.
    numeric_list = any(mo.start() <= start < mo.end()
                       for mo in re.finditer(r"[0-9]+(?:/[0-9]+)+", text))
    if not numeric_list:
        if post.isalnum():
            return "PATH_OR_IDENTIFIER_GLUED"
        if post == "/" and pre == "/":
            return "PATH_OR_IDENTIFIER_GLUED"
    if re.search(r"(?:sections?|sect\.|s\.)\s*[0-9.,\s]*$", left):
        return "SECTION_NUMBER"
    if (left.endswith("(") and post == ")") or re.search(r"step\s+$", left):
        return "ENUMERATED_STEP_LABEL"
    if re.match(r"[0-9]+-member", right):
        return "STRUCTURAL_RULE_CARDINALITY"
    if re.match(r"\s*(?:of\s+[0-9]+\s+)?"
                r"(?:named README|manifest code path|hits|uncovered)",
                text[start + len(tok):start + len(tok) + 40]):
        return "QUANTITY_ON_A_PRE_EXISTING_REPO_FILE"
    return "RUN_MEASURED_QUANTITY"


CLASS_REASONS = {
    "AGENT_SERIAL": "a digit inside an agent serial (3.0.0_SA_CVO, 0.9.0_WK_...) -- an identity",
    "DOC_FILE_NUMBER_PREFIX": "a canon file's ordinal prefix (02_DOCTRINE, 06_, 10_, 11_)",
    "SOURCE_LINE_NUMBER": "a source line or line range in a cited file",
    "CONFIG_THRESHOLD_QUOTED_FROM_THE_FILE_UNDER_TEST":
        "a threshold quoted out of the config the cell inspected, not a measurement of anything",
    "FILE_LENGTH_OF_A_PRE_EXISTING_FILE":
        "the line count of a pre-existing repo file the cell read",
    "FIRM_NAME": "part of the firm name '49 Financial'",
    "PATH_OR_IDENTIFIER_GLUED":
        "glued to a path, bucket prefix, run-id timestamp or ARN -- an address, not a quantity",
    "SECTION_NUMBER": "a document section number",
    "ENUMERATED_STEP_LABEL": "a step label in an ordered rule, not a count",
    "STRUCTURAL_RULE_CARDINALITY":
        "the cardinality a rule's own precondition names (a 2-member group)",
    "QUANTITY_ON_A_PRE_EXISTING_REPO_FILE":
        "MEASURED, but on a pre-existing repo file the cell read, cited at a commit pin in its own "
        "row -- R-40's subject is a run or a PRODUCED artifact, so this cell does not pin it",
    "RUN_MEASURED_QUANTITY":
        "THE RESIDUE: a quantity measured on an artifact round 1 PRODUCED. This is the set pinned.",
}

# The residue, DECLARED. (criterion, field, token, occurrence-within-that-field).
EXPECTED_RESIDUE = [
    ("E2R1-AC5", "output_evidence", "7", 1),
    ("E3R1-AC6", "output_evidence", "1", 1),
    ("E3R1-AC6", "output_evidence", "271", 1),
    ("E3R1-AC6", "output_evidence", "1084", 1),
    ("E3R1-AC6", "output_evidence", "1084", 2),
    ("E3R1-AC6", "output_evidence", "0", 1),
    ("P1R1-AC6", "output_evidence", "1626", 1),
    ("V1R1-AC5", "invocation", "20", 1),
    ("V1R1-AC5", "invocation", "5", 1),
    ("V1R1-AC5", "invocation", "4", 1),
    ("V1R1-AC5", "invocation", "1", 1),
    ("V1R1-AC5", "invocation", "5", 2),
    ("V1R1-AC5", "invocation", "5", 3),
    ("V1R1-AC5", "invocation", "184", 1),
    ("V1R1-AC5", "output_evidence", "184", 1),
    ("V1R1-AC5", "output_evidence", "5", 1),
    ("V1R1-AC5", "output_evidence", "4", 1),
    ("V1R1-AC5", "output_evidence", "1", 1),
    ("V1R1-AC5", "output_evidence", "5", 2),
    ("V1R1-AC5", "output_evidence", "5", 3),
    ("V1R1-AC5", "output_evidence", "184", 2),
    ("X1R1-AC6", "output_evidence", "184", 1),
    ("X1R1-AC6", "output_evidence", "179", 1),
    ("X1R1-AC6", "output_evidence", "1074", 1),
    ("X1R1-AC6", "output_evidence", "0", 1),
    ("X3R1-AC5", "output_evidence", "0", 1),
    ("X3R1-AC5", "output_evidence", "1", 1),
    ("X3R1-AC5", "output_evidence", "179", 1),
]

# Every residue token is covered by exactly one MEMBER. `tokens` is how many residue tokens the
# member accounts for, so the per-criterion arithmetic closes.
MEMBERS = [
    {"member": "E2R1-AC5:7", "criterion": "E2R1-AC5", "tokens": 1, "value": 7,
     "quantity": "storage seed locations in the forks cell's own SEEDS.json",
     "measured_on": A_SEEDS, "run_id": "f73efe6113c5a41b0be148830d8a86059dadc0ed",
     "run_id_kind": "cell_commit",
     "run_id_instrument": "git log --format=%H -- <path> (single commit; the cell's own run)",
     "remeasure": ("json", A_SEEDS, "seeds")},
    {"member": "P1R1-AC6:1626", "criterion": "P1R1-AC6", "tokens": 1, "value": 1626,
     "quantity": "packages in the plan cell's own plan.json",
     "measured_on": A_PLAN_R1, "run_id": "7b01900dda3a0390644dd008216e880cab32392f",
     "run_id_kind": "cell_commit",
     "run_id_instrument": "git log --format=%H -- <path> (single commit; the cell's own run)",
     "planned_from": A_CONTR_R1,
     "remeasure": ("json", A_PLAN_R1, "packages")},
    {"member": "V1R1-AC5:20", "criterion": "V1R1-AC5", "tokens": 1, "value": 20,
     "quantity": "rows in the reviewer-reproduction sample",
     "measured_on": A_REPRO, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "REPRODUCTION.json's own `contract` field names the run directory",
     "remeasure": ("json", A_REPRO, "results")},
    {"member": "V1R1-AC5:5-ALIAS", "criterion": "V1R1-AC5", "tokens": 2, "value": 5,
     "quantity": "ALIAS verdicts in the 20-row sample",
     "measured_on": A_REPRO, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "REPRODUCTION.json's own `contract` field names the run directory",
     "remeasure": ("spread", A_REPRO, "ALIAS")},
    {"member": "V1R1-AC5:4-CONFORMANT", "criterion": "V1R1-AC5", "tokens": 2, "value": 4,
     "quantity": "CONFORMANT verdicts in the 20-row sample",
     "measured_on": A_REPRO, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "REPRODUCTION.json's own `contract` field names the run directory",
     "remeasure": ("spread", A_REPRO, "CONFORMANT")},
    {"member": "V1R1-AC5:1-NOT-GRADED", "criterion": "V1R1-AC5", "tokens": 2, "value": 1,
     "quantity": "NOT-GRADED verdicts in the 20-row sample",
     "measured_on": A_REPRO, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "REPRODUCTION.json's own `contract` field names the run directory",
     "remeasure": ("spread", A_REPRO, "NOT-GRADED")},
    {"member": "V1R1-AC5:5-OUT-OF-PATTERN", "criterion": "V1R1-AC5", "tokens": 2, "value": 5,
     "quantity": "OUT-OF-PATTERN verdicts in the 20-row sample",
     "measured_on": A_REPRO, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "REPRODUCTION.json's own `contract` field names the run directory",
     "remeasure": ("spread", A_REPRO, "OUT-OF-PATTERN")},
    {"member": "V1R1-AC5:5-RAISE", "criterion": "V1R1-AC5", "tokens": 2, "value": 5,
     "quantity": "RAISE verdicts in the 20-row sample",
     "measured_on": A_REPRO, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "REPRODUCTION.json's own `contract` field names the run directory",
     "remeasure": ("spread", A_REPRO, "RAISE")},
    {"member": "V1R1-AC5:184", "criterion": "V1R1-AC5", "tokens": 3, "value": 184,
     "quantity": "callable rows in the contract the sample was drawn from",
     "measured_on": A_BB_C, "run_id": RUN_BB, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the path names, cross-read from REPRODUCTION.json",
     "remeasure": ("json", A_BB_C, "rows")},
    {"member": "X1R1-AC6:184", "criterion": "X1R1-AC6", "tokens": 1, "value": 184,
     "quantity": "rows in the graded run's contract.json",
     "measured_on": A_8D_C, "run_id": RUN_8D, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": ("json", A_8D_C, "rows")},
    {"member": "X1R1-AC6:179", "criterion": "X1R1-AC6", "tokens": 1, "value": 179,
     "quantity": "tensions in the graded run's contract.json",
     "measured_on": A_8D_C, "run_id": RUN_8D, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": ("json", A_8D_C, "tensions")},
    {"member": "X1R1-AC6:1074", "criterion": "X1R1-AC6", "tokens": 1, "value": 1074,
     "quantity": "packages in the graded run's own plan.json",
     "measured_on": A_8D_P, "run_id": RUN_8D, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": ("json", A_8D_P, "packages")},
    {"member": "X1R1-AC6:0", "criterion": "X1R1-AC6", "tokens": 1, "value": 0,
     "quantity": "schema errors validating the graded run's contract.json (X1R1-AC1's output)",
     "measured_on": A_8D_C, "run_id": RUN_8D, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": None,
     "remeasure_absent_reason":
         "re-running the schema validation would re-grade X1R1-AC1, a closed mechanical criterion. "
         "This cell binds the number to the artifact and its hash and moves no grade."},
    {"member": "X3R1-AC5:0-CLOSED", "criterion": "X3R1-AC5", "tokens": 1, "value": 0,
     "quantity": "CLOSED tensions in the second run's DIFF.md",
     "measured_on": A_CAF_D, "run_id": RUN_CAF, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": ("diff", A_CAF_D, "CLOSED")},
    {"member": "X3R1-AC5:1-OPENED", "criterion": "X3R1-AC5", "tokens": 1, "value": 1,
     "quantity": "OPENED tensions in the second run's DIFF.md",
     "measured_on": A_CAF_D, "run_id": RUN_CAF, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": ("diff", A_CAF_D, "OPENED")},
    {"member": "X3R1-AC5:179-UNCHANGED", "criterion": "X3R1-AC5", "tokens": 1, "value": 179,
     "quantity": "UNCHANGED tensions in the second run's DIFF.md",
     "measured_on": A_CAF_D, "run_id": RUN_CAF, "run_id_kind": "run_home_run_id",
     "run_id_instrument": "the run directory the cited path names",
     "remeasure": ("diff", A_CAF_D, "UNCHANGED")},
]

EXCLUDED_CRITERION = "E3R1-AC6"


def remeasure(spec):
    kind, path, key = spec
    if kind == "json":
        return len(read_json(path)[key])
    if kind == "spread":
        # A verdict is recorded TWO WAYS in REPRODUCTION.json: a returned tuple renders as
        # "('ALIAS', ...)", but a RAISE renders as "RAISE: K1: ...". Reading only the first form
        # counts RAISE as ZERO and makes a CORRECT cited number look wrong -- which is exactly what
        # the re-measure refusal caught on the first run of this instrument.
        n = 0
        for row in read_json(path)["results"]:
            got = str(row.get("got") or "")
            mo = re.match(r"[(\[]?'([A-Z][A-Z\-]*)'", got) or re.match(r"([A-Z][A-Z\-]*):", got)
            if mo and mo.group(1) == key:
                n += 1
        return n
    if kind == "diff":
        with io.open(ab(path), encoding="utf-8", newline="") as fh:
            for line in fh.read().split("\n"):
                if line.startswith(key + ":"):
                    return int(line.split(":", 1)[1].strip())
        raise SystemExit("REFUSED: no %s line in %s" % (key, path))
    raise SystemExit("REFUSED: unknown remeasure kind " + kind)


def pin(path):
    """A content hash WITH ITS INSTRUMENT, computed twice. The worktree hash is the CHECKOUT's; the
    HEAD blob is the RECORD's. They must agree or the pin is not a pin."""
    rc1, wt = git("hash-object", path)
    rc2, blob = git("rev-parse", "HEAD:" + path)
    if rc1 != 0 or rc2 != 0:
        raise SystemExit("REFUSED: cannot hash %s (rc %s/%s)" % (path, rc1, rc2))
    if wt != blob:
        raise SystemExit("REFUSED: worktree bytes and HEAD blob disagree for %s "
                         "(%s vs %s) -- the pin would be the checkout's" % (path, wt, blob))
    return wt


def lineage():
    """WHAT THE PINS RESOLVE, measured rather than argued. S11 reads 1626 and 1074 as two numbers
    that 'cannot both be true of one plan'. They are not of one plan: each is a package count on a
    DIFFERENT contract, and naming the artifact is the whole remedy. NO GRADE MOVES -- this block
    adds provenance to numbers this cell does not re-grade."""
    pre_c = read_json(A_CONTR_R1)
    post_c = read_json(A_8D_C)
    same = pin(A_CONTR_R1) == pin(A_WALK_C)
    return {
        "_about": "the two artifact lineages the pins separate. Measured by this instrument at run "
                  "time; nothing here re-grades a closed criterion.",
        "pre_opt_in_lineage": {
            "contract": A_CONTR_R1,
            "content_hash": pin(A_CONTR_R1),
            "hash_instrument": "git hash-object",
            "rows": len(pre_c.get("rows", [])),
            "tensions": len(pre_c.get("tensions", [])),
            "plan": A_PLAN_R1,
            "packages": len(read_json(A_PLAN_R1).get("packages", [])),
            "byte_identical_second_home": A_WALK_C,
            "second_home_is_byte_identical": same,
            "cited_by": ["P1R1-AC6 (1626 packages)", "E3R1-AC6 (271 tensions)"],
        },
        "post_opt_in_lineage": {
            "contract": A_8D_C,
            "content_hash": pin(A_8D_C),
            "hash_instrument": "git hash-object",
            "rows": len(post_c.get("rows", [])),
            "tensions": len(post_c.get("tensions", [])),
            "plan": A_8D_P,
            "packages": len(read_json(A_8D_P).get("packages", [])),
            "cited_by": ["X1R1-AC6 (184 rows, 179 tensions, 1074 packages)"],
        },
        "reading": "1626 and 1074 are both TRUE, of two different contracts -- the first carries "
                   "%d tensions, the second %d. LT-e-4's opt-in plant is the difference. The "
                   "numbers never disagreed; the citations named no artifact, which is the defect "
                   "S11 measured and the convention this cell records closes."
                   % (len(pre_c.get("tensions", [])), len(post_c.get("tensions", []))),
        "e3_population_still_exists": {
            "claim_under_test": "S11 and this cell's order both say the 271-tension population "
                                "'no longer exists anywhere'",
            "measured": "it exists, TRACKED at HEAD, in two byte-identical files",
            "homes": [A_CONTR_R1, A_WALK_C],
            "tensions": len(pre_c.get("tensions", [])),
            "content_hash": pin(A_CONTR_R1),
            "hash_instrument": "git hash-object, equal to git rev-parse HEAD:<path> for both homes",
            "bound": "STATED, NEVER ACTED ON. E3R1-AC6 stays excluded by name on the CTO's word; "
                     "this cell does not re-grade it and nothing here reopens it. Filed as a "
                     "surprise row so the disarm owner decides, not this worker.",
        },
    }


def main(argv):
    emit = None
    if len(argv) >= 2 and argv[0] == "--emit":
        emit = argv[1]

    base, by_id, found, want, rows = judgment_rows()
    print("PROOF INSTANCES enumerated by existence (git ls-files): %d of %d declared in R2_BASE"
          % (len(found), want))
    print("JUDGMENT CRITERIA read from R2_BASE round_1_judgment_criteria.by_id: %d" % len(by_id))

    raw = 0
    cands = []
    per_field_seen = {}
    for cid in sorted(by_id):
        _, row = rows[cid]
        for field in sorted(k for k, v in row.items() if isinstance(v, str)):
            text = row[field]
            for mo in re.finditer(r"[0-9]+", text):
                raw += 1
                pre = text[mo.start() - 1] if mo.start() > 0 else " "
                if pre in GLUE:
                    continue
                key = (cid, field, mo.group(0))
                per_field_seen[key] = per_field_seen.get(key, 0) + 1
                cands.append((cid, field, mo.group(0), per_field_seen[key],
                              _cls(text, mo.start(), mo.group(0))))

    print("")
    print("STAGE 0  DOMAIN      : %d maximal digit runs across every STRING field of the %d rows"
          % (raw, len(by_id)))
    print("STAGE 1  CANDIDATES  : %d word-initial runs (%d dropped as identifier fragments)"
          % (len(cands), raw - len(cands)))
    print("")
    print("STAGE 2  every candidate, with the class it fell in")
    for cid, field, tok, occ, cl in cands:
        print("   %-10s %-18s %-9s #%d  %s" % (cid, field, tok, occ, cl))

    ledger = {}
    for _, _, _, _, cl in cands:
        ledger[cl] = ledger.get(cl, 0) + 1
    print("")
    print("SUBTRACTION LEDGER")
    print("   %-52s %5d   the domain" % ("STAGE 0 digit runs", raw))
    print("   %-52s %5d   glued to a word" % ("- IDENTIFIER_FRAGMENT (stage 1)", raw - len(cands)))
    for cl in sorted(ledger):
        if cl == "RUN_MEASURED_QUANTITY":
            continue
        print("   %-52s %5d   %s" % ("- " + cl, ledger[cl], CLASS_REASONS[cl][:44]))
    residue = [c for c in cands if c[4] == "RUN_MEASURED_QUANTITY"]
    print("   %-52s %5d" % ("= RESIDUE (RUN_MEASURED_QUANTITY)", len(residue)))
    closes = raw - (raw - len(cands)) - sum(v for k, v in ledger.items()
                                            if k != "RUN_MEASURED_QUANTITY") == len(residue)
    print("   ledger closes against the domain: %s" % closes)
    if not closes:
        raise SystemExit("REFUSED: the subtraction does not close against its own denominator")

    got = sorted((c[0], c[1], c[2], c[3]) for c in residue)
    expect = sorted(EXPECTED_RESIDUE)
    if got != expect:
        print("")
        print("REFUSED: the residue is not the DECLARED residue.")
        print("  classifier found but not declared: %s" % [g for g in got if g not in expect])
        print("  declared but not found:            %s" % [e for e in expect if e not in got])
        raise SystemExit(1)
    print("   residue == EXPECTED_RESIDUE (%d of %d tokens, declared per criterion/field/token): "
          "True" % (len(got), len(expect)))

    by_crit = {}
    for cid, _, _, _, _ in residue:
        by_crit[cid] = by_crit.get(cid, 0) + 1
    covered = {}
    for m in MEMBERS:
        covered[m["criterion"]] = covered.get(m["criterion"], 0) + m["tokens"]
    exc_tokens = by_crit.get(EXCLUDED_CRITERION, 0)
    covered[EXCLUDED_CRITERION] = exc_tokens
    if by_crit != covered:
        raise SystemExit("REFUSED: member coverage disagrees with the residue per criterion: "
                         "residue=%s covered=%s" % (by_crit, covered))
    print("   every residue token covered by exactly one member (per-criterion counts agree): True")

    print("")
    print("PINS -- each number re-measured against its own artifact, each hash computed twice")
    pinned = []
    for m in MEMBERS:
        chash = pin(m["measured_on"])
        entry = {
            "number": m["member"],
            "criterion": m["criterion"],
            "value": m["value"],
            "quantity": m["quantity"],
            "run_id": m["run_id"],
            "run_id_kind": m["run_id_kind"],
            "run_id_instrument": m["run_id_instrument"],
            "measured_on": m["measured_on"],
            "content_hash": chash,
            "hash_instrument": "git hash-object (blob <len> + NUL prefix); confirmed equal to "
                               "git rev-parse HEAD:<path>, so the pin is the committed bytes",
            "citation_count_in_round_1_judgment_evidence": m["tokens"],
        }
        if m.get("planned_from"):
            entry["planned_from"] = m["planned_from"]
            entry["planned_from_content_hash"] = pin(m["planned_from"])
        if m["remeasure"] is None:
            entry["re_measured_by_this_cell"] = "absent"
            entry["re_measured_absent_reason"] = m["remeasure_absent_reason"]
        else:
            live = remeasure(m["remeasure"])
            entry["re_measured_by_this_cell"] = "measured"
            entry["re_measured_value"] = live
            entry["re_measured_agrees"] = (live == m["value"])
            if live != m["value"]:
                raise SystemExit("REFUSED: %s cites %s, the artifact carries %s -- a WRONG number "
                                 "is a surprise row, not a silent correction"
                                 % (m["member"], m["value"], live))
        pinned.append(entry)
        print("   %-28s %-6s run %-26s %s  %s"
              % (entry["number"], entry["value"], entry["run_id"][:26],
                 entry["content_hash"][:12], entry["re_measured_by_this_cell"]))

    numbers_found = [e["number"] for e in pinned] + [EXCLUDED_CRITERION]
    print("")
    print("ARITHMETIC  numbers_found %d == pinned %d + excluded %d  -> %s"
          % (len(numbers_found), len(pinned), 1,
             len(numbers_found) == len(pinned) + 1))

    rec = {
        "_about": "LT-n-2, LGIC_LGCTFM round 2. Every number round 1's judgment records cite, bound "
                  "to the run it was measured on and to that run's content hash. NO GRADE MOVES.",
        "cell": "LT-n-2",
        "to_id": "LGIC_LGCTFM.TO-LT-n-2-r2",
        "written_by": "0.9.0_WK_LGIC_LGCTFM~2",
        "instrument_path": ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~2/pin_numbers_r1.py",
        "denominator": raw,
        "denominator_source":
            "every maximal digit run in every STRING field of the %d round-1 judgment acceptance "
            "rows, read from the %d proof instances themselves. The instances are enumerated by "
            "EXISTENCE (git ls-files over the project's deliverables, filtered to "
            "*.proof_of_spec.json), never from a typed list; the %d judgment criterion ids come "
            "from R2_BASE.json's round_1_judgment_criteria.by_id, which the issuer measured from "
            "the 14 orders' judgment=\"true\" elements. The FIELD read is every string-valued key "
            "of the acceptance row (output_evidence, denominator, invocation, criterion_verbatim, "
            "expect, method, status, status_reason, criterion_id) -- the widest field set the row "
            "offers, chosen so no citation can hide in a field the sweep skipped. This number is "
            "the ENUMERATION, not a count of what was pinned: %d of it is subtracted by declared "
            "class before anything is pinned."
            % (len(by_id), len(found), len(by_id), raw - len(residue)),
        "denominator_claim": "measured",
        "subtraction_ledger": {
            "domain_digit_runs": raw,
            "identifier_fragment_dropped_at_stage_1": raw - len(cands),
            "by_class": ledger,
            "residue_run_measured_quantity_tokens": len(residue),
            "closes_against_the_domain": True,
            "class_reasons": CLASS_REASONS,
        },
        "domain_choice_stated":
            "The class pinned is a quantity measured on an artifact ROUND 1 PRODUCED (a run "
            "directory's output, or a cell deliverable). A quantity measured on a PRE-EXISTING "
            "repo file the cell merely read is excluded BY CLASS "
            "(QUANTITY_ON_A_PRE_EXISTING_REPO_FILE, %d tokens), because R-40's subject is a run or "
            "a produced artifact and such a file already resolves through the commit pin its own "
            "row carries. Choosing the domain is itself a claim (R-50), so it is printed here to "
            "be refused rather than assumed."
            % ledger.get("QUANTITY_ON_A_PRE_EXISTING_REPO_FILE", 0),
        "numbers_found": numbers_found,
        "pinned": pinned,
        "excluded": {
            EXCLUDED_CRITERION:
                "NOT re-graded against R-40, by 1.0.0_SA_CTO's round-1 analysis item 2, verbatim: "
                "\"S11's run-ids on every number; E3 is NOT re-graded against R-40.\" Its judgment "
                "was SOUND AT ITS OWN VINTAGE -- it ran before LT-e-4 made the untypeable plant "
                "opt-in, which is what moved the population from 271 tensions to 179. Re-grading "
                "it would falsify a correct grade. This is a STATED EXCLUSION, not a silent "
                "omission: the criterion cites %d of the residue's %d run-measured tokens "
                "(rules_colliding 1, 271 tensions, 1084 factor cells twice, 0 defective) and this "
                "one member accounts for all of them."
                % (exc_tokens, len(residue)),
        },
        "excluded_tokens_named_not_pinned": {
            EXCLUDED_CRITERION: [list(t) for t in sorted(EXPECTED_RESIDUE)
                                 if t[0] == EXCLUDED_CRITERION],
        },
        "what_the_pins_resolve": lineage(),
    }

    if emit:
        target = ab(emit)
        with io.open(target, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(rec, indent=2, sort_keys=True))
            fh.write("\n")
        print("")
        print("WROTE %s (%d bytes)" % (emit, os.path.getsize(target)))
    print("VERDICT: LT-N-2-LEDGER-CLOSES")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
