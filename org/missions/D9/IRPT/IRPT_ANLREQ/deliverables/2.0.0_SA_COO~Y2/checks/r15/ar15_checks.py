"""ar15_checks.py -- the mechanical checks of IRPT_ANLREQ round 15, workstream Y.

Usage:  python ar15_checks.py <check> --portal <portal root>

  y151-wire   AR-y-151: the vendored wire type declares commentary_requested, nothing outside the generated wire
              folder and the tests names it, and the Investor Reporting suite passes with 0 failing     -> Y151-WIRE-OK
  y151-keep   AR-y-151: the TicketCenter test folder passes                                             -> Y151-KEEP-OK

Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import re
import subprocess
import sys
from pathlib import Path

WIRE = "src/pages/InvestorReporting/contracts/wire/AnalysisSubmissionRequest.ts"
MEMBER = "commentary_requested"
TOKENS = {"y151-wire": "Y151-WIRE", "y151-keep": "Y151-KEEP"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def bun(portal, target):
    got = subprocess.run(["bun", "test", target], cwd=str(portal), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
    def last(word):
        found = re.findall(r"^\s*(\d+) %s" % word, out, re.M)
        return int(found[-1]) if found else None
    passed, failed, errors = last("pass"), last("fail"), last("error")
    return (got.returncode, passed if passed is not None else -1, failed if failed is not None else -1, errors or 0)


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--portal" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    portal = Path(argv[argv.index("--portal") + 1])
    problems = []
    if check == "y151-keep":
        rc, passed, failed, errors = bun(portal, "./src/pages/TicketCenter")
        print("TicketCenter folder: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed != 0 or passed < 67:
            problems.append("the TicketCenter folder does not pass whole (67 passed at the base)")
        return finish(check, problems)
    wire = (portal / WIRE).read_text(encoding="utf-8") if (portal / WIRE).is_file() else ""
    if MEMBER not in wire:
        problems.append("the wire type does not declare %s" % MEMBER)
    senders = []
    for path in (portal / "src").rglob("*.ts*"):
        rel = path.relative_to(portal).as_posix()
        if "/contracts/wire/" in rel or "/__tests__/" in rel or rel.endswith(".test.ts") or rel.endswith(".test.tsx"):
            continue
        if MEMBER in path.read_text(encoding="utf-8", errors="replace"):
            senders.append(rel)
    print("files outside the wire folder and the tests that name the member: %d %s" % (len(senders), senders[:5]))
    if senders:
        problems.append("the member is named outside the generated wire folder and the tests: nothing may send it yet")
    rc, passed, failed, errors = bun(portal, "./src/pages/InvestorReporting")
    print("InvestorReporting suite: %d pass, %d fail, %d error (rc=%d)" % (passed, failed, errors, rc))
    if rc != 0 or failed != 0 or errors != 0 or passed < 1000:
        problems.append("the Investor Reporting suite does not pass with 0 failing")
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
