#!/usr/bin/env python3
"""AR384-y-AC2: bun test on the two test files and on the folder src/pages/TicketCenter.

Runs in the portal worktree, which must be AT cand/dell2/anlreq-test-lint-fixes (HEAD equal, and no
local change to the two files), since bun test reads the files from disk.
Prints `TESTS-OK <n> passed, 0 failed` (n = the folder's pass count) only when the folder has 0 failed;
otherwise `TESTS-BAD <why>` and exit 1.
Control: eslint on the same two files at origin/DEV (the base, read from git, not from disk) prints
`BASE-HAS-ERRORS <n>`; n must be at least 2 for the control to hold.
"""
import json
import re
import subprocess
import sys

sys.path.insert(0, "C:/dev/wk-irpt-anlreq-284/.tools")
from git_bash_resolver import git_bash  # noqa: E402

PORTAL = "C:/dev/wk-irpt-anlreq-284/portal"
CAND = "cand/dell2/anlreq-test-lint-fixes"
BASE_REF = "origin/DEV"
FOLDER = "src/pages/TicketCenter"
FILES = [
    "src/pages/TicketCenter/__tests__/filing-hint.test.tsx",
    "src/pages/TicketCenter/__tests__/filing-decision-tree.test.tsx",
]
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def bad(why):
    print(f"TESTS-BAD {why}")
    sys.exit(1)


def git(*args):
    return subprocess.run(["git", "-C", PORTAL, *args], capture_output=True)


def bun_test(targets):
    bash = git_bash()
    if not bash:
        bad("no Git Bash resolved (git_bash_resolver returned None)")
    cmd = "bun test " + " ".join(targets)
    p = subprocess.run([bash, "-c", cmd], cwd=PORTAL, capture_output=True)
    text = ANSI.sub("", (p.stdout + p.stderr).decode("utf-8", "replace"))
    passes = re.findall(r"(\d+) pass\b", text)
    fails = re.findall(r"(\d+) fail\b", text)
    return p.returncode, (int(passes[-1]) if passes else None), (int(fails[-1]) if fails else None), text


def base_error_count(bash):
    total = 0
    for path in FILES:
        blob = git("show", f"{BASE_REF}:{path}")
        if blob.returncode != 0:
            return None
        cmd = f"bun x eslint --stdin --stdin-filename {path} -f json"
        p = subprocess.run([bash, "-c", cmd], cwd=PORTAL, input=blob.stdout, capture_output=True)
        try:
            data = json.loads(p.stdout.decode("utf-8", "replace"))
        except ValueError:
            return None
        total += sum(r.get("errorCount", 0) for r in data)
    return total


def main():
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    cand = git("rev-parse", "--verify", "--quiet", CAND).stdout.decode().strip()
    if not cand:
        bad(f"branch {CAND} not found")
    if head != cand:
        bad(f"worktree HEAD {head[:12]} is not {CAND} {cand[:12]}")
    dirty = git("status", "--porcelain", "--", *FILES).stdout.decode().strip()
    if dirty:
        bad(f"local change to the two files: {dirty!r}")

    rc_files, p_files, f_files, _ = bun_test(FILES)
    if rc_files != 0 or f_files not in (0, None):
        bad(f"two-file run rc={rc_files} fail={f_files}")
    rc_dir, p_dir, f_dir, text_dir = bun_test([FOLDER])
    if p_dir is None or f_dir is None:
        bad(f"folder run rc={rc_dir}: no pass/fail summary in output")
    if rc_dir != 0 or f_dir != 0:
        bad(f"folder {FOLDER} rc={rc_dir} fail={f_dir} pass={p_dir}")

    bash = git_bash()
    base_n = base_error_count(bash) if bash else None
    print(f"TESTS-OK {p_dir} passed, 0 failed")
    print(f"BASE-HAS-ERRORS {base_n if base_n is not None else 'UNREAD'}")
    sys.exit(0)


if __name__ == "__main__":
    main()
