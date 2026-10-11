"""ar12_checks.py -- the mechanical checks of IRPT_ANLREQ round 12, workstream Y.

Usage:  python ar12_checks.py <check> --portal <portal root>

  y121-age    AR-y-121: the elapsed-age test file holds the five named tests and passes   -> Y121-AGE-OK
  y121-keep   AR-y-121: the whole TicketCenter test folder passes                         -> Y121-KEEP-OK

Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import re
import subprocess
import sys
from pathlib import Path

TEST = "src/pages/TicketCenter/__tests__/queue-elapsed-age.test.tsx"
NAMES = (
    "an age states its unit in words",
    "a ticket with no created time prints nothing",
    "a created time after now prints nothing",
    "the age is computed against the given now and not the clock",
    "the queue row shows the age beside the created time for an open ticket",
)
TOKENS = {"y121-age": "Y121-AGE", "y121-keep": "Y121-KEEP"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def bun(portal, target):
    got = subprocess.run(["bun", "test", target], cwd=str(portal), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
    passed, failed = re.search(r"(\d+) pass", out), re.search(r"(\d+) fail", out)
    return got.returncode, int(passed.group(1)) if passed else -1, int(failed.group(1)) if failed else -1


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--portal" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    portal = Path(argv[argv.index("--portal") + 1])
    problems = []
    if check == "y121-age":
        path = portal / TEST
        if not path.is_file():
            return finish(check, ["no %s" % TEST])
        text = path.read_text(encoding="utf-8")
        for name in NAMES:
            if name not in text:
                problems.append("the test named %r is absent" % name)
        if "Date.now()" in text or "new Date()" in text:
            problems.append("the test file reads the real clock (Date.now() or new Date()); now must be a fixed value")
        rc, passed, failed = bun(portal, "./" + TEST)
        print("new file: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed != 0 or passed < len(NAMES):
            problems.append("the new test file does not pass with at least %d tests" % len(NAMES))
        return finish(check, problems)
    rc, passed, failed = bun(portal, "./src/pages/TicketCenter")
    print("TicketCenter folder: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
    if rc != 0 or failed != 0 or passed < 53:
        problems.append("the TicketCenter folder does not pass whole (53 passed at the base)")
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
