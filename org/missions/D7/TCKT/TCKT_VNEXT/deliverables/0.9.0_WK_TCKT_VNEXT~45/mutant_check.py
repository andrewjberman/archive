"""TO-R19-L1 AC2 -- the one mutant that must fire (cell R19-nr-1).

The mutant removes the contact-list restriction: when the stored requester address is not a configured
contact, the notice goes to the STORED address (the body address) instead of the firm's first contact.
The mutated lambda_function.py and a copy of the tests folder are written to a scratch folder INSIDE the
worktree's gitignored .scratch/ (outside the product tree infra/aws/lambda/ticket_center), and the new test
file is run against the copy with pytest (never by path).

    python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~45/mutant_check.py

Prints MUTANT-FIRES (exit 0) when the new test file FAILS on the mutant, else MUTANT-SURVIVES (exit 1).
No network, no AWS: the copied tests keep their SES and users-table guards (conftest.py).
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
SRC = os.path.join(REPO, "infra", "aws", "lambda", "ticket_center")
SCRATCH = os.path.join(REPO, ".scratch", "r19l1_mutant")
TEST_NAME = "test_notice_recipient_firm.py"

# The one line that falls back to the firm's first contact. It must occur exactly once in the source.
ANCHOR = "    return [contacts[0]]\n"
MUTANT_LINE = '    return [str(req.get("email") or "").strip()]\n'


def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def build_copy():
    """Write the mutated lambda and a copy of the tests folder into SCRATCH (overwrite only, no deletion)."""
    src_text = read_text(os.path.join(SRC, "lambda_function.py"))
    count = src_text.count(ANCHOR)
    if count != 1:
        print("MUTANT-NOT-BUILT: anchor occurs %d times, expected 1" % count)
        sys.exit(1)
    write_text(os.path.join(SCRATCH, "lambda_function.py"), src_text.replace(ANCHOR, MUTANT_LINE))
    tests_src = os.path.join(SRC, "tests")
    tests_dst = os.path.join(SCRATCH, "tests")
    os.makedirs(tests_dst, exist_ok=True)
    copied = 0
    for name in sorted(os.listdir(tests_src)):
        if name.endswith(".py"):
            shutil.copyfile(os.path.join(tests_src, name), os.path.join(tests_dst, name))
            copied += 1
    return os.path.join(tests_dst, TEST_NAME), copied


def main():
    test_path, copied = build_copy()
    cmd = [sys.executable, "-m", "pytest", test_path, "-q", "-p", "no:cacheprovider", "--color=no"]
    proc = subprocess.run(cmd, cwd=SCRATCH, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          timeout=100)
    out = proc.stdout.decode("utf-8", errors="replace")
    summary = [ln for ln in out.splitlines() if re.search(r"\b(passed|failed|error)", ln)]
    print("mutant: contact-list fallback replaced by the stored body address (anchor count 1)")
    print("scratch copy: %s (tests copied: %d .py files)" % (SCRATCH, copied))
    print("pytest rc=%d" % proc.returncode)
    print("pytest summary: %s" % (summary[-1] if summary else "none"))
    failed = proc.returncode != 0 and re.search(r"\b[1-9][0-9]* failed\b", out) is not None
    if failed:
        print("MUTANT-FIRES")
        sys.exit(0)
    print("MUTANT-SURVIVES")
    sys.exit(1)


if __name__ == "__main__":
    main()
