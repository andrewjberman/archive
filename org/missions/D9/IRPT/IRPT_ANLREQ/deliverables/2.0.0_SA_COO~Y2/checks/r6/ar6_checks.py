"""ar6_checks.py -- the mechanical checks of IRPT_ANLREQ round 6, workstream Y (cell AR-y-61).

Usage:  python ar6_checks.py <check> --portal <portal root>

  y61-record   the new test file holds the four named tests and passes                      -> Y61-RECORD-OK
  y61-keep     the whole TicketCenter test folder passes (the difference control)           -> Y61-KEEP-OK

--portal is REQUIRED. Each check prints its token on the last line, or the token with -FAIL after one FAIL line per problem.
The checks write nothing.
"""
import re
import subprocess
import sys
from pathlib import Path

NEW = "src/pages/TicketCenter/__tests__/analysis-form-i1-record.test.tsx"
NAMES = (
    "after the analysis post answers, the form records the request id on the ticket",
    "a refused record is shown with the service's words and the ticket stays filed",
    "a failed analysis post records nothing",
    "retry sends the analysis again and then records",
)
TOKENS = {"y61-record": "Y61-RECORD", "y61-keep": "Y61-KEEP"}


def bun(portal, target):
    got = subprocess.run(["bun", "test", target], cwd=str(portal), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (got.stdout or "") + (got.stderr or "")
    passed = re.search(r"(\d+) pass", out)
    failed = re.search(r"(\d+) fail", out)
    return got.returncode, int(passed.group(1)) if passed else -1, int(failed.group(1)) if failed else -1


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--portal" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    portal = Path(argv[argv.index("--portal") + 1])
    problems = []
    if check == "y61-record":
        path = portal / NEW
        if not path.is_file():
            problems.append("no %s" % NEW)
        else:
            text = path.read_text(encoding="utf-8")
            for name in NAMES:
                if name not in text:
                    problems.append("the test named %r is absent" % name)
            rc, passed, failed = bun(portal, "./" + NEW)
            print("new file: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed != 0 or passed < len(NAMES):
                problems.append("the new test file does not pass with at least %d tests" % len(NAMES))
    else:
        rc, passed, failed = bun(portal, "./src/pages/TicketCenter")
        print("TicketCenter folder: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed != 0 or passed < 42:
            problems.append("the TicketCenter folder does not pass whole (42 passed at the base)")
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
