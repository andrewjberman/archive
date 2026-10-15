"""AR-y-359 AC2: check the r41b address amendment of the two FWD-1 driver files against the committed base.

Read-only and offline: it runs git only to read the base blob and the working-tree diff.
Prints ADDRESS-OK <n> lines changed, r41a gone, r41b present (exit 0) or ADDRESS-BAD <why> (exit 1).
Run: python <worktree>/org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~156/address_check.py
"""
import re
import subprocess
import sys
from pathlib import Path

BASE = "3514aeecc6ad6be52977aaf06b0946f47f4b9814"
FOLDER = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver"
DRIVER = FOLDER + "/fwd1_driver.mjs"
MINT = FOLDER + "/fwd1_mint.py"
FILES = [DRIVER, MINT]
OLD = b"r41a"
NEW_ADDR = b"fwd1-staff-r41b@opal.invalid"
HERE = Path(__file__).resolve().parent


def git(args, cwd=None):
    p = subprocess.run(["git"] + args, cwd=str(cwd or HERE), capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("git rc=%d %s" % (p.returncode, p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def bad(why):
    print("ADDRESS-BAD " + why)
    sys.exit(1)


def root():
    return git(["rev-parse", "--show-toplevel"]).decode("utf-8").strip()


def selftest_span(lines):
    """1-based inclusive (start, end) of function selftest() in a list of text lines."""
    start = next(i for i, ln in enumerate(lines) if ln.startswith("function selftest()"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")
    return start + 1, end + 1


def post_allowed(blob):
    head = blob.index(b"const POST_ALLOWED = [")
    tail = blob.index(b"\n]\n", head) + 3
    return blob[head:tail]


def main():
    try:
        top = root()
        new = {}
        old = {}
        for f in FILES:
            with open(top + "/" + f, "rb") as fh:
                new[f] = fh.read()
            old[f] = git(["show", BASE + ":" + f])
    except (RuntimeError, OSError) as e:
        bad("read error " + str(e))

    # 1. r41a in neither amended file; the full r41b address exactly once in each
    for f in FILES:
        if OLD in new[f]:
            bad("r41a still present in " + f)
        n = new[f].count(NEW_ADDR)
        if n != 1:
            bad("r41b address occurs %d times in %s (want exactly 1)" % (n, f))

    # 2. the route guard list is byte-identical to the base
    if post_allowed(new[DRIVER]) != post_allowed(old[DRIVER]):
        bad("POST_ALLOWED differs from the base")

    # 3. every changed line is an address line, the title line, or inside self-test
    # pathspecs are repo-relative: the diff runs from the repo root, not from this folder
    diff = git(["diff", "-U0", BASE, "--", DRIVER, MINT], cwd=top).decode("utf-8").split("\n")
    new_span = selftest_span(new[DRIVER].decode("utf-8").split("\n"))
    old_span = selftest_span(old[DRIVER].decode("utf-8").split("\n"))
    cur = None
    o_no = n_no = 0
    changed = 0
    hunks = 0
    allowed_counts = {"address": 0, "title": 0, "selftest": 0}
    for ln in diff:
        if ln.startswith("+++ "):
            cur = ln[6:] if ln.startswith("+++ b/") else None
            continue
        if ln.startswith("--- "):
            continue
        m = re.match(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", ln)
        if m:
            o_no, n_no = int(m.group(1)), int(m.group(2))
            hunks += 1
            continue
        if not ln or ln[0] not in "+-":
            continue
        text = ln[1:]
        changed += 1
        if cur is None:
            bad("changed line outside the two files")
        if cur == MINT:
            if text.startswith('EMAIL = "'):
                allowed_counts["address"] += 1
            else:
                bad("mint helper changed outside the address line: " + text[:60])
        else:
            if text.startswith("const EMAIL = '"):
                allowed_counts["address"] += 1
            elif text.startswith("const TITLE = '"):
                allowed_counts["title"] += 1
            elif ln[0] == "+" and new_span[0] <= n_no <= new_span[1]:
                allowed_counts["selftest"] += 1
            elif ln[0] == "-" and old_span[0] <= o_no <= old_span[1]:
                allowed_counts["selftest"] += 1
            else:
                bad("driver line outside the address, title and self-test: " + text[:60])
        if ln[0] == "+":
            n_no += 1
        else:
            o_no += 1

    if changed == 0:
        bad("no change against the base in the two files")
    print("ADDRESS-OK %d lines changed, r41a gone, r41b present" % changed)
    print("DENOMINATOR changed_lines=%d hunks=%d files=%d allowed=%s selftest_span_new=%d-%d selftest_span_base=%d-%d"
          % (changed, hunks, len(FILES), allowed_counts, new_span[0], new_span[1], old_span[0], old_span[1]))
    sys.exit(0)


if __name__ == "__main__":
    main()
