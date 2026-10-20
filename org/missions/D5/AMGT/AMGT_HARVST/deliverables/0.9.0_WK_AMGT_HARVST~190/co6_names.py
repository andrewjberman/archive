# HVST-co-6 names check (rule 30). Run from the repo root of the worktree:  python -u co6_names.py
#
# Method copied from cn5_names.py (HVST-cn-5), with the function, the file and the output changed.
#
# 1. Prints the builder names: lib/opal_naming.py name(amgt, None, gold-refresh, kind, qualifier) for each
#    resource the cell declares, the ECR repository (kind repo) included. A builder refusal is not caught: the
#    program writes the transcript it has so far, ends it with NAMES-ABORTED, and exits 1.
# 2. Reads the FIRST locals block of infra/aws/terraform/harvest/gold-refresh.tf and compares every literal
#    `key = "value"` against its builder name.
# 3. NEGATIVE CONTROL: plants one wrong literal in memory and proves the comparison reports it.
# 4. Writes its own transcript to co6_names.out beside this file (newline='\n'), and prints it.
# Exit 0 only when the control detects the plant AND the mismatch count is 0.

import os
import re
import sys

ROOT = os.getcwd()
DELIV = os.path.dirname(os.path.abspath(__file__))
TF_PATH = os.path.join(ROOT, "infra", "aws", "terraform", "harvest", "gold-refresh.tf")
OUT_PATH = os.path.join(DELIV, "co6_names.out")

if not os.path.isfile(os.path.join(ROOT, "lib", "opal_naming.py")):
    sys.exit("ERROR: run from the repo root of the worktree (lib/opal_naming.py not found in the cwd)")
sys.path.insert(0, ROOT)
from lib.opal_naming import name  # noqa: E402

SYSTEM = "amgt"
SCOPE = None
FUNCTION = "gold-refresh"

# (locals key in the .tf, what, kind, qualifier)
SPEC = [
    ("gold_build_project_name", "codebuild-project", "build", None),
    ("gold_build_role_name", "codebuild-role", "role", "build"),
    ("gold_build_policy_name", "codebuild-policy", "policy", "build"),
    ("gold_cluster_name", "ecs-cluster", "cluster", None),
    ("gold_task_family_name", "ecs-task", "task", None),
    ("gold_task_role_name", "task-role", "role", "task"),
    ("gold_task_policy_name", "task-policy", "policy", "task"),
    ("gold_exec_role_name", "exec-role", "role", "exec"),
    ("gold_scheduler_role_name", "scheduler-role", "role", "scheduler"),
    ("gold_scheduler_policy_name", "scheduler-policy", "policy", "scheduler"),
    ("gold_schedule_name", "schedule", "daily", None),
    ("gold_sg_name", "security-group", "sg", None),
    ("gold_ecr_repository_name", "ecr-repository", "repo", None),
]

out = []


def emit(line):
    out.append(line)
    print(line)


expected = {}
try:
    for key, what, kind, qual in SPEC:
        value = name(SYSTEM, SCOPE, FUNCTION, kind, qual)
        expected[key] = value
        emit("NAME %s %s %s %s" % (what, kind, qual if qual is not None else "-", value))
except Exception as exc:
    emit("NAMES-ABORTED builder name() refused: %s: %s" % (type(exc).__name__, exc))
    with open(OUT_PATH, "w", encoding="ascii", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    sys.exit(1)

LIT = re.compile(r'^\s*([a-z][a-z0-9_]*)\s*=\s*"([^"$]*)"\s*(#.*)?$')


def first_locals_block(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^locals\s*\{\s*$", line):
            start = i
            break
    if start is None:
        sys.exit("ERROR: no locals block in %s" % TF_PATH)
    body = []
    for line in lines[start + 1:]:
        if line.startswith("}"):
            break
        body.append(line)
    return body


def literals_of(body):
    found = {}
    for line in body:
        m = LIT.match(line)
        if m:
            found[m.group(1)] = m.group(2)
    return found


def compare(literals):
    matched = [k for k in expected if k in literals and literals[k] == expected[k]]
    mismatch = sorted(k for k in set(expected) | set(literals)
                      if literals.get(k) != expected.get(k))
    return len(literals), len(matched), mismatch


with open(TF_PATH, "r", encoding="utf-8") as fh:
    body = first_locals_block(fh.read())
literals = literals_of(body)
n_lit, n_match, mismatch = compare(literals)
for key in sorted(set(expected) | set(literals)):
    emit("LITERAL %s tf=%s builder=%s" % (key, literals.get(key, "<absent>"), expected.get(key, "<none>")))

planted_key = "gold_cluster_name"
planted = dict(literals)
planted[planted_key] = "amgt-gold-refresh-WRONG"
_, _, planted_mismatch = compare(planted)
detected = "yes" if planted_mismatch == [planted_key] else "no"
emit("NAMES-CONTROL planted_mismatch_detected=%s" % detected)
emit("NAMES-CHECK terraform_literals=%d builder_match=%d mismatches=%d" % (n_lit, n_match, len(mismatch)))

with open(OUT_PATH, "w", encoding="ascii", newline="\n") as fh:
    fh.write("\n".join(out) + "\n")

if detected != "yes" or mismatch:
    sys.exit(1)
