"""ar13_checks.py -- the mechanical checks of IRPT_ANLREQ round 13, workstream Y.

Usage:  python ar13_checks.py y131-age  --portal <portal root>
        python ar13_checks.py y131-keep --portal <portal root>
        python ar13_checks.py y132-read --root <workspace root>

  y131-age    AR-y-131: hours up to 72, days from there; an age only for a named closed list of waiting statuses -> Y131-AGE-OK
  y131-keep   AR-y-131: the whole TicketCenter test folder passes                                              -> Y131-KEEP-OK
  y132-read   AR-y-132: the one-account read's record is complete                                              -> Y132-READ-OK

Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

TEST = "src/pages/TicketCenter/__tests__/queue-elapsed-age.test.tsx"
NAMES = (
    "47 hours reads as 47 hours",
    "71 hours reads as hours and 72 hours reads as 3 days",
    "a status outside the waiting list shows no age",
    "every waiting status shows an age",
)
RECORD = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r13/ONE_ACCOUNT_CHECK_READ.json"
KINDS = ("SEVERAL_ACCOUNTS", "TOTALS_ROW", "UNPRICEABLE_HOLDING", "KNOWN_GOOD")
TOKENS = {"y131-age": "Y131-AGE", "y131-keep": "Y131-KEEP", "y132-read": "Y132-READ"}


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
    if len(argv) < 2 or argv[1] not in TOKENS:
        print(__doc__)
        return 2
    check = argv[1]
    problems = []
    if check in ("y131-age", "y131-keep"):
        if "--portal" not in argv:
            print(__doc__)
            return 2
        portal = Path(argv[argv.index("--portal") + 1])
        if check == "y131-keep":
            rc, passed, failed = bun(portal, "./src/pages/TicketCenter")
            print("TicketCenter folder: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed != 0 or passed < 58:
                problems.append("the TicketCenter folder does not pass whole (58 passed at the base)")
            return finish(check, problems)
        text = (portal / TEST).read_text(encoding="utf-8") if (portal / TEST).is_file() else ""
        for name in NAMES:
            if name not in text:
                problems.append("the test named %r is absent" % name)
        if "Date.now()" in text or "new Date()" in text:
            problems.append("the test file reads the real clock")
        page = (portal / "src/pages/TicketCenter/TicketCenter.tsx").read_text(encoding="utf-8")
        helper = (portal / "src/pages/TicketCenter/elapsedAge.ts").read_text(encoding="utf-8")
        if "WAITING_STATUSES" not in page + helper:
            problems.append("no closed list named WAITING_STATUSES in TicketCenter.tsx or elapsedAge.ts")
        if "=== 'completed' ? ''" in page:
            problems.append("TicketCenter.tsx still decides the age by 'everything except completed'")
        rc, passed, failed = bun(portal, "./" + TEST)
        print("age test file: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed != 0 or passed < 5 + len(NAMES):
            problems.append("the age test file does not pass with at least %d tests" % (5 + len(NAMES)))
        return finish(check, problems)
    if "--root" not in argv:
        print(__doc__)
        return 2
    root = Path(argv[argv.index("--root") + 1])
    if not (root / RECORD).is_file():
        return finish(check, ["no %s" % RECORD])
    doc = json.loads((root / RECORD).read_text(encoding="utf-8"))
    signals = doc.get("account_recognition") or []
    if not signals or any(not (row.get("signal") and row.get("where_seen") and row.get("claim") in ("measured", "inferred")
                               and isinstance(row.get("false_positive_risk"), str)) for row in signals):
        problems.append("account_recognition needs at least one row with signal, where_seen, false_positive_risk and claim")
    today = {str(row.get("kind")): row for row in doc.get("door_today") or []}
    for kind in KINDS:
        row = today.get(kind)
        if not row:
            problems.append("door_today has no row for %s" % kind)
        elif not (row.get("input_built") and row.get("invocation") and row.get("result") and row.get("claim") in ("measured", "not_run")
                  and "turned_back" in row and "says_what_to_fix" in row):
            problems.append("door_today row %s is incomplete" % kind)
        elif row.get("claim") == "not_run" and not row.get("why_not_run"):
            problems.append("door_today row %s is not_run with no reason" % kind)
    door = doc.get("door") or {}
    if not (door.get("file_function") and door.get("refusal_carrier") and door.get("existing_refusal_codes") is not None):
        problems.append("door needs file_function, refusal_carrier and existing_refusal_codes")
    form = doc.get("form") or {}
    if not (form.get("file_function") and form.get("how_a_refusal_is_shown")):
        problems.append("form needs file_function and how_a_refusal_is_shown")
    cells = doc.get("proposed_cells") or []
    if not cells or any(not (row.get("what") and row.get("write_set") and row.get("risk") in ("LOCAL", "SERVED", "WORLD")) for row in cells):
        problems.append("proposed_cells needs at least one row with what, write_set and risk")
    if not isinstance(doc.get("not_read"), list):
        problems.append("not_read must be a list (empty if nothing was left unread)")
    print("recognition signals %d, door_today rows %d of %d, proposed cells %d" % (len(signals), len(today), len(KINDS), len(cells)))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
