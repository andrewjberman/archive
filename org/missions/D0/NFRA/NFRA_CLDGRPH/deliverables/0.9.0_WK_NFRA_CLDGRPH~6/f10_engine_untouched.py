"""F10-AC5 -- THE ENGINE UNTOUCHED.

cmd_derive, cmd_snapshot and cmd_iceberg_commit must be BYTE-IDENTICAL to their bytes at the
hand-off commit. The grain matters: this is not "the file is unchanged" (it is changed -- main()
gained a call and the module gained a preamble function). It is "these three FUNCTION BODIES are
unchanged", which is what the nightly Fargate derive-runner depends on, because it calls the engine
IN-PROCESS and never goes through the CLI.

METHOD: `git show <hand-off>:<file>` for the OLD bytes, the worktree for the NEW, each parsed with
`ast` and sliced by the function's own line range -- so the comparison follows the function even if
it moved, rather than comparing line numbers. Both sides are LF-normalised (autocrlf checkout).

CONTROLS PRINTED:
  * a POSITIVE CONTROL on the comparator: main() -- which this order DID change -- must compare
    UNEQUAL. A comparator that returns "unchanged" for everything proves nothing.
  * the git show is never `2>/dev/null`: a mangled ref returns clean-empty and would read as an
    absent function. rc + byte count are printed.
"""

import ast
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f10_lib as L  # noqa: E402

FILE = "org/modules/graph/comp_aws_cli.py"
HANDOFF = os.environ.get("F10_HANDOFF_REF", "973a20aff99fc737772203545fa546deef093547")
ENGINE = ["cmd_derive", "cmd_snapshot", "cmd_iceberg_commit"]
CONTROL = "main"
RUNNER = "infra/aws/globgrph/derive_runner.py"


def show(ref, path):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, path)],
                       capture_output=True, cwd=L.WS, timeout=60)
    return p.returncode, p.stdout.replace(b"\r\n", b"\n"), p.stderr.decode("utf-8", "replace")


def slices(src_bytes):
    text = src_bytes.decode("utf-8", "replace")
    lines = text.splitlines(keepends=True)
    tree = ast.parse(text)
    out = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = "".join(lines[node.lineno - 1:node.end_lineno])
            out[node.name] = body
    return out


print("F10-AC5 -- the engine untouched")
print("  hand-off ref: %s" % HANDOFF)
print("")

rc_old, old_bytes, err_old = show(HANDOFF, FILE)
print("  git show %s:%s  rc=%d  bytes=%d  stderr=%r"
      % (HANDOFF[:12], FILE, rc_old, len(old_bytes), err_old.strip()[:60]))
if rc_old != 0 or not old_bytes:
    print("  BLOCKED: the hand-off bytes could not be read; refusing to claim UNCHANGED against an "
          "empty read (a mangled ref returns clean-empty).")
    print("CMD_DERIVE_BYTES_UNCHANGED=UNREADABLE")
    print("RC=1")
    sys.exit(1)

with open(os.path.join(L.WS, FILE), "rb") as fh:
    new_bytes = fh.read().replace(b"\r\n", b"\n")
print("  worktree %s  bytes=%d" % (FILE, len(new_bytes)))
print("")

old = slices(old_bytes)
new = slices(new_bytes)

unchanged = 0
for fn in ENGINE:
    a, b = old.get(fn), new.get(fn)
    same = (a is not None and a == b)
    unchanged += 1 if same else 0
    print("  %-20s handoff_bytes=%-6s worktree_bytes=%-6s IDENTICAL=%s"
          % (fn, len(a) if a is not None else "ABSENT",
             len(b) if b is not None else "ABSENT", "YES" if same else "NO"))

ctl_same = (old.get(CONTROL) == new.get(CONTROL))
print("")
print("  POSITIVE CONTROL on the comparator: %s (this order DID change it) compares IDENTICAL=%s "
      "-- so the YESes above are a measurement, not a constant"
      % (CONTROL, "YES" if ctl_same else "NO"))

# the derive-runner's in-process call site
# NOT the first line that MENTIONS the name -- derive_runner.py:5 is a DOCSTRING mention, and
# taking it would have named the wrong line as the call site. The site is resolved with `ast` as an
# actual ast.Call to comp_aws_cli.cmd_derive, which a comment or docstring cannot be.
callsite = None
rpath = os.path.join(L.WS, RUNNER)
if os.path.exists(rpath):
    with open(rpath, "r", encoding="utf-8", errors="replace") as fh:
        rsrc = fh.read()
    rlines = rsrc.splitlines()
    for node in ast.walk(ast.parse(rsrc)):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and f.attr == "cmd_derive":
                callsite = (node.lineno, rlines[node.lineno - 1].strip())
                break
print("")
if callsite:
    print("  derive-runner in-process call site: %s:%d   %s" % (RUNNER, callsite[0], callsite[1]))
print("")

# THE SUMMARY LINES ARE PRINTED IN THE ORDER THE CRITERION'S `expect` READS THEM. The expect is an
# ORDERED regex (A[\s\S]*B[\s\S]*C): a probe that prints the same three facts in a different order
# fails a criterion it has actually met, which is what a first run of this probe did.
print("CMD_DERIVE_BYTES_UNCHANGED=%s" % ("true" if old.get("cmd_derive") == new.get("cmd_derive")
                                         else "false"))
print("HANDLERS_UNCHANGED=%d of %d" % (unchanged, len(ENGINE)))
if callsite:
    print("DERIVE_RUNNER_CALLSITE=%s:%d" % (RUNNER, callsite[0]))
else:
    print("DERIVE_RUNNER_CALLSITE=NOT-FOUND (%s)" % RUNNER)

ok = (unchanged == len(ENGINE) and not ctl_same and callsite is not None)
print("RC=%d" % (0 if ok else 1))
sys.exit(0 if ok else 1)
