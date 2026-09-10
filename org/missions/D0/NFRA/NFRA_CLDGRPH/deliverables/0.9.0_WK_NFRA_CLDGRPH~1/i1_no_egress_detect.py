#!/usr/bin/env python3
"""i1_no_egress_detect.py -- the detector behind i1_no_egress.sh (CG-s-41, I1-AC4).

WHY THIS IS AN AST WALK AND NOT A GREP: every one of my deliverable scripts
CONTAINS the string "ecs run-task" -- in the docstring that says it never calls
one. A text detector would count those mentions and report a violation, and a
text detector tuned to not count them would be tuned until it reported zero,
which is the same number arrived at dishonestly. So this parses each Python file
and walks its CALL NODES: a docstring is not a call node, a comment is not a call
node, and a string inside print() is not a call node.

Two things are counted, and they are different:
  * ACTS  -- calls that would change the world (the five the egress hold names).
  * READS -- calls that only read Opal infrastructure (expressly permitted).

Files that are not Python (the shell script, the record, the source diff) are
scanned line-wise with comment lines removed, and that WEAKER GRAIN is declared
on its own line rather than blended into the strong one.

usage: i1_no_egress_detect.py <file> [<file> ...]
       prints one classified line per finding, then a summary block.
"""
from __future__ import annotations

import ast
import os
import re
import sys

# ---------------------------------------------------------------------------
# THE FIVE HELD ACTS, and the read verbs that are expressly permitted.
# Each act name is matched against a call's dotted name OR against a token
# sequence in a subprocess argv literal.
# ---------------------------------------------------------------------------
ACTS = {
    "ECS_RUN_TASK": {
        "attrs": {"run_task"},
        "argv": [("ecs", "run-task")],
    },
    "CODEBUILD_START": {
        "attrs": {"start_build", "start_build_batch"},
        "argv": [("codebuild", "start-build"), ("codebuild", "start-build-batch")],
    },
    "S3_WRITE": {
        "attrs": {"put_object", "upload_file", "upload_fileobj", "copy_object",
                  "delete_object", "delete_objects", "put_bucket_policy"},
        "argv": [("s3", "cp"), ("s3", "sync"), ("s3", "mv"), ("s3", "rm"),
                 ("s3api", "put-object"), ("s3api", "delete-object")],
    },
    "IMAGE_PUSH": {
        "attrs": {"put_image"},
        "argv": [("docker", "push"), ("docker", "build"), ("ecr", "put-image")],
    },
    "TERRAFORM_APPLY": {
        "attrs": set(),
        "argv": [("terraform", "apply"), ("safe-apply",), ("terraform", "destroy")],
    },
    # Not one of the five, but the hold's own words: "no act whose effect is an
    # SNS publish". Counted separately and reported beside them.
    "SNS_PUBLISH": {
        "attrs": {"publish"},
        "argv": [("sns", "publish")],
    },
}

READ_ATTRS = {
    "get_object", "head_object", "list_objects_v2", "list_objects", "get_bucket_policy",
    "head_bucket", "list_buckets", "get_caller_identity", "describe_tasks",
    "describe_task_definition", "list_tasks", "batch_get_builds", "lookup_events",
    "filter_log_events", "get_log_events", "describe_log_groups", "get_function",
    "get_role", "describe_table", "get_topic_attributes", "get_queue_attributes",
}
READ_ARGV_HEADS = {"s3api", "logs", "sts", "cloudtrail"}
READ_ARGV_PAIRS = {("s3", "ls"), ("ecs", "describe-services"), ("ecs", "list-tasks"),
                   ("codebuild", "batch-get-builds")}


def dotted(node) -> str:
    parts = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    return ".".join(reversed(parts))


# A string argument is an ARGV only when it is handed to something that EXECUTES.
# Without this, `f.write("... docker push ...")` reads as a docker push, and the
# harness that emits the control fixture convicts itself of running one. The
# narrowing is a CORRECTNESS fix, not a tuning-to-zero: the control below still
# fires on all six, which is the only reason this line is allowed to exist.
EXEC_LEAVES = {"run", "Popen", "call", "check_call", "check_output", "system",
               "popen", "spawn", "spawnv", "execv", "execvp"}


def argv_tokens(call) -> list:
    """Every string literal in an argument of an EXECUTING call -- a subprocess argv."""
    leaf = dotted(call.func).split(".")[-1]
    if leaf not in EXEC_LEAVES:
        return []
    out = []
    for a in list(call.args) + [k.value for k in call.keywords]:
        if isinstance(a, (ast.List, ast.Tuple)):
            toks = [e.value for e in a.elts
                    if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            if toks:
                out.append(toks)
        elif isinstance(a, ast.Constant) and isinstance(a.value, str):
            out.append(a.value.split())
    return out


def match_argv(toks: list, want: tuple) -> bool:
    joined = " ".join(t.replace("\\", "/").split("/")[-1] for t in toks)
    return all(w in joined.split() for w in want)


def scan_python(path):
    findings = []
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src, filename=path)
    lines = src.splitlines()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = dotted(node.func)
        leaf = name.split(".")[-1] if name else ""
        argvs = argv_tokens(node)
        hit = None
        for act, spec in ACTS.items():
            if leaf in spec["attrs"]:
                hit = (act, "call %s()" % name)
                break
            for want in spec["argv"]:
                if any(match_argv(t, want) for t in argvs):
                    hit = (act, "argv %s" % " ".join(want))
                    break
            if hit:
                break
        if hit:
            findings.append(("ACT", hit[0], path, node.lineno,
                             lines[node.lineno - 1].strip()[:110], hit[1]))
            continue
        if leaf in READ_ATTRS:
            findings.append(("READ", leaf, path, node.lineno,
                             lines[node.lineno - 1].strip()[:110], "call"))
            continue
        for t in argvs:
            heads = [x.replace("\\", "/").split("/")[-1] for x in t]
            if heads and (heads[0] in READ_ARGV_HEADS
                          or (len(heads) > 1 and (heads[0], heads[1]) in READ_ARGV_PAIRS)
                          or (len(heads) > 1 and heads[1] in READ_ARGV_HEADS)):
                findings.append(("READ", " ".join(heads[:3]), path, node.lineno,
                                 lines[node.lineno - 1].strip()[:110], "argv"))
                break
    return findings, len(lines)


def scan_text(path):
    """Line scan for non-Python files. TOKENS, never substrings.

    A substring test here is a false-positive machine: ("s3", "rm") matches any
    prose line that mentions an s3:// URL and the word "perform", and ("s3",
    "cp") matches half a page of this project's own records. The tokens are
    matched against the line SPLIT ON WHITESPACE-AND-PUNCTUATION, so `aws s3 cp
    a s3://b/k` still matches and "perform" no longer does.
    """
    findings = []
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    for i, raw in enumerate(lines, 1):
        line = raw.strip()
        if line.startswith("#") or line.startswith("//") or line.startswith("*"):
            continue
        toks = set(t for t in re.split(r"[^A-Za-z0-9_.:/-]+", line) if t)
        toks |= set(t.split("/")[-1] for t in toks)
        for act, spec in ACTS.items():
            for want in spec["argv"]:
                if all(w in toks for w in want):
                    findings.append(("ACT", act, path, i, line[:110], "text-token"))
    return findings, len(lines)


PROBE_SRC = "\n".join([
    "import boto3, subprocess",
    "def probe():",
    "    boto3.client('ecs').run_task(cluster='c', taskDefinition='t')",
    "    boto3.client('codebuild').start_build(projectName='p')",
    "    boto3.client('s3').put_object(Bucket='b', Key='k', Body=b'x')",
    "    subprocess.run(['docker', 'push', 'repo:tag'])",
    "    subprocess.run(['terraform', 'apply', '-auto-approve'])",
    "    boto3.client('sns').publish(TopicArn='a', Message='m')",
    "",
])
# THE PAYLOAD LIVES HERE, LITERALLY, AND THAT IS DELIBERATE. This file is inside
# the population the census covers, and the census does not flag it, because
# these tokens sit in a list of plain strings handed to write() -- not to an
# executing call. That is the EXEC_LEAVES rule doing its job on the hardest case
# available: the harness's own probe payload. It was NOT always so. The first
# run of this script convicted i1_no_egress.sh of a docker push and a terraform
# apply, because the payload was embedded in the shell script and the weak-grain
# line scan cannot tell a payload from a command. The remedy was to move the
# payload to a plane the strong grain can read and to teach the strong grain
# what an argv is -- NOT to soften the pattern until the number reached zero.


def emit_probe(path):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(PROBE_SRC)
    return path


def main(argv):
    if len(argv) > 2 and argv[1] == "--emit-probe":
        print("PROBE_WRITTEN %s" % emit_probe(argv[2]))
        return 0
    files = argv[1:]
    all_f = []
    py_lines = txt_lines = py_files = txt_files = 0
    for f in files:
        if not os.path.exists(f):
            print("SKIP: missing %s" % f)
            continue
        if f.endswith(".py"):
            fs, n = scan_python(f)
            py_lines += n
            py_files += 1
        else:
            fs, n = scan_text(f)
            txt_lines += n
            txt_files += 1
        all_f.extend(fs)

    print("DETECTOR COVERAGE:")
    print("  STRONG GRAIN (python AST call nodes): %d file(s), %d line(s)."
          % (py_files, py_lines))
    print("    A docstring, a comment and a string inside print() are NOT call")
    print("    nodes, so a MENTION of a held act cannot be counted as one.")
    print("  WEAK GRAIN (line scan, comment lines dropped): %d file(s), %d line(s)."
          % (txt_files, txt_lines))
    print("    This grain CANNOT tell a call from a mention. It is reported")
    print("    separately and never merged into the strong count.")
    print()
    acts = [f for f in all_f if f[0] == "ACT"]
    reads = [f for f in all_f if f[0] == "READ"]
    print("FINDINGS: %d act(s), %d read(s)" % (len(acts), len(reads)))
    for f in acts:
        print("  ACT   %-16s %s:%d  [%s]  %s" % (f[1], f[2], f[3], f[5], f[4]))
    for f in reads:
        print("  READ  %-22s %s:%d  %s" % (f[1], f[2], f[3], f[4]))
    print()
    per_act = {a: len([f for f in acts if f[1] == a]) for a in ACTS}
    for a in sorted(per_act):
        print("COUNT %s=%d" % (a, per_act[a]))
    print("COUNT READS=%d" % len(reads))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
