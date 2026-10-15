#!/usr/bin/env python3
"""AR352-y-AC2 checker (worker 0.9.0_WK_IRPT_ANLREQ~153, order IRPT_ANLREQ.TO-AR-y-352).

Reads POST_ALLOWED from the committed base fwd1_driver.mjs (git show <base>:<path>) and from the
amended working file, then prints ALLOWLIST-OK only when:
  - the base has seven POST shapes and every one is still present, unchanged and in the same order;
  - the added entries equal the record's q3.added;
  - every added entry is an anchored exact path (starts ^, ends $, no .*, no +, no |);
  - each added entry is a POST request in the record's q1.requests with class read_shaped.
Otherwise prints ALLOWLIST-BAD <why> and exits 1. Prints the denominator.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]  # <root>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>
sys.path.insert(0, str(ROOT / ".tools"))
from msys_argv_guard import msys_safe_run  # noqa: E402

DRIVER_REL = ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/"
              "0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/fwd1_driver.mjs")
RECORD = HERE / "r41" / "ALLOWLIST_AMEND.json"
BASE_SEVEN = 7


def post_allowed(text):
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("const POST_ALLOWED = ["):
            start = i
            break
    if start is None:
        raise ValueError("no 'const POST_ALLOWED = [' in the file")
    out = []
    for line in lines[start + 1:]:
        s = line.strip()
        if s == "]":
            return out
        if not s or s.startswith("//"):
            continue
        m = re.fullmatch(r"/(.*)/,", s)
        if not m:
            raise ValueError("unparsed POST_ALLOWED line: " + s)
        out.append(m.group(1))
    raise ValueError("POST_ALLOWED is not closed")


def git_show(base, path):
    cmd = ["git", "-C", str(ROOT), "show", base + ":" + path]
    res = msys_safe_run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        raise ValueError("git show failed rc=%d: %s" % (res.returncode, res.stderr.decode("utf-8", "replace").strip()))
    return res.stdout.decode("utf-8")


def path_of(source):
    """'^\\/api\\/x$' -> '/api/x' (anchored exact source only; None otherwise)."""
    if not (source.startswith("^") and source.endswith("$")):
        return None
    return re.sub(r"\\(.)", r"\1", source[1:-1])


def main():
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    base = record["base"]
    problems = []
    base_list = post_allowed(git_show(base, DRIVER_REL))
    amended_list = post_allowed((ROOT / DRIVER_REL).read_text(encoding="utf-8"))
    if len(base_list) != BASE_SEVEN:
        problems.append("base holds %d POST shapes, not %d" % (len(base_list), BASE_SEVEN))
    if amended_list[:len(base_list)] != base_list:
        gone = [b for b in base_list if b not in amended_list]
        problems.append("base entries not kept unchanged and in order: %s" % (gone or "order changed"))
    added = [a for a in amended_list if a not in base_list]
    if added != list(record["q3"]["added"]):
        problems.append("added %r != record q3.added %r" % (added, record["q3"]["added"]))
    requests = record["q1"]["requests"]
    for a in added:
        if not (a.startswith("^") and a.endswith("$")):
            problems.append("added entry not anchored: " + a)
        for bad in (".*", "+", "|"):
            if bad in a:
                problems.append("added entry carries %r: %s" % (bad, a))
        p = path_of(a)
        match = [r for r in requests if r["method"] == "POST" and r["path"] == p and r["class"] == "read_shaped"]
        if p is None or not match:
            problems.append("added entry has no POST read_shaped request in q1: " + a)
    if problems:
        print("ALLOWLIST-BAD " + "; ".join(problems))
        return 1
    read_shaped = sum(1 for r in requests if r["class"] == "read_shaped")
    print("ALLOWLIST-OK %d added, seven kept" % len(added))
    print("denominator: %d amended POST_ALLOWED entries = %d base kept + %d added; "
          "q1.requests %d, of which read_shaped %d; added entries matched %d"
          % (len(amended_list), len(base_list), len(added), len(requests), read_shaped, len(added)))
    print("base %s; base file %s" % (base, DRIVER_REL))
    return 0


if __name__ == "__main__":
    sys.exit(main())
