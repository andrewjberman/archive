#!/usr/bin/env python3
"""AR325-y-AC3 -- the candidate's scope, read from git (read-only).

SCOPE-OK only when `git diff --name-only origin/PROD <candidate>` lists only paths under src/pages/TicketCenter/ (the
three named source files, the two re-pinned test files and the new test file), and the diff of the candidate against
origin/PROD is empty under src/pages/InvestorReporting and src/api. Otherwise SCOPE-BAD <why>, exit 1.
"""
import sys

WK ="C:/dev/wk-irpt-anlreq-133"
PORTAL = WK + "/portal"
CAND = "cand/dell2/anlreq-internal-filer-chooses-firm"
BASE = "origin/PROD"
ALLOWED_PREFIX = "src/pages/TicketCenter/"
FORBIDDEN_DIRS = ["src/pages/InvestorReporting", "src/api"]

sys.path.insert(0, WK + "/.tools")
from msys_argv_guard import msys_safe_run  # noqa: E402  (git is MSYS-linked: spawn through the guard)


def git(*args):
    proc = msys_safe_run(["git", "-C", PORTAL, *args], capture_output=True, text=True, timeout=120)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    rc, names, err = git("diff", "--name-only", BASE, CAND)
    if rc != 0:
        print("SCOPE-BAD git diff --name-only rc=%s: %s" % (rc, err.strip()[:200]))
        return 1
    paths = [p for p in names.splitlines() if p.strip()]
    if not paths:
        print("SCOPE-BAD the candidate changes no path against %s" % BASE)
        return 1
    outside = [p for p in paths if not p.startswith(ALLOWED_PREFIX)]
    if outside:
        print("SCOPE-BAD path(s) outside %s: %s" % (ALLOWED_PREFIX, ", ".join(outside)))
        return 1
    for d in FORBIDDEN_DIRS:
        rc, diff, err = git("diff", BASE, CAND, "--", d)
        if rc != 0:
            print("SCOPE-BAD git diff rc=%s under %s: %s" % (rc, d, err.strip()[:200]))
            return 1
        if diff.strip():
            print("SCOPE-BAD the candidate changes %s against %s" % (d, BASE))
            return 1
    print("SCOPE-OK %d paths, all under %s; 0 changed lines under %s" % (len(paths), ALLOWED_PREFIX, ", ".join(FORBIDDEN_DIRS)))
    for p in paths:
        print("  " + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
