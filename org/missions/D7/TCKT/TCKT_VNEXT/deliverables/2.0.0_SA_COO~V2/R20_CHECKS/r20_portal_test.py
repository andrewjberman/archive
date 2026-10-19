"""TCKT_VNEXT: run ONE portal test file with bun from the portal worktree and grade it.

  python r20_portal_test.py --portal <portal worktree> --file src/pages/TicketCenter/__tests__/<name>.test.tsx --min <N>

Prints `R20-PORTALTEST-OK <n> pass 0 fail` when the file exists, bun runs it from the portal as the working directory (the file given as a
./ path, so it is a path and not a filter), at least N tests pass and none fail; else `R20-PORTALTEST-BAD <reason>` and exit 1. The run is
bounded at 110 seconds. Nothing is written.
"""
import argparse
import os
import re
import subprocess
import sys


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal", required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--min", type=int, required=True)
    a = ap.parse_args(argv)
    path = os.path.join(a.portal, a.file)
    if not os.path.isfile(path):
        print("R20-PORTALTEST-BAD the test file does not exist: %s" % a.file)
        return 1
    try:
        out = subprocess.run(["bun", "test", "./" + a.file.replace("\\", "/")], cwd=a.portal, capture_output=True, text=True, timeout=110)
    except (OSError, subprocess.SubprocessError) as e:
        print("R20-PORTALTEST-BAD bun did not run: %s" % type(e).__name__)
        return 1
    text = re.sub(r"\x1b\[[0-9;]*m", "", out.stdout + out.stderr)
    p = re.search(r"^\s*(\d+) pass\s*$", text, re.M)
    f = re.search(r"^\s*(\d+) fail\s*$", text, re.M)
    if not p or not f:
        print("R20-PORTALTEST-BAD no pass and fail counts in the bun output (rc=%d)" % out.returncode)
        return 1
    n, bad = int(p.group(1)), int(f.group(1))
    if out.returncode != 0 or bad != 0 or n < a.min:
        print("R20-PORTALTEST-BAD %d pass, %d fail, need at least %d pass and 0 fail (rc=%d)" % (n, bad, a.min, out.returncode))
        return 1
    print("R20-PORTALTEST-OK %d pass 0 fail" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
