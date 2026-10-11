"""ar7_checks.py -- the mechanical checks of IRPT_ANLREQ round 7, workstream Y (cells AR-y-71 service, AR-y-72 portal).

Usage:  python ar7_checks.py <check> --root <workspace root> [--portal <portal root>]

  y71-bind   AR-y-71: the service test file holds the seven named tests and passes, and the reader
             census of the public-reason set exists with every row filled                         -> Y71-BIND-OK
  y71-keep   AR-y-71: the ops test folder passes whole (the difference control)                   -> Y71-KEEP-OK
  y72-open   AR-y-72: the portal test file holds the three named tests and passes (needs --portal) -> Y72-OPEN-OK
  y72-keep   AR-y-72: the whole TicketCenter test folder passes (needs --portal)                  -> Y72-KEEP-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
SVC_TEST = IR + "/ops/tests/test_report_ticket_binding.py"
SVC_NAMES = (
    "test_report_read_with_the_stored_ticket_id_answers",
    "test_report_read_with_another_ticket_id_is_refused",
    "test_report_read_with_no_ticket_id_answers_as_before",
    "test_request_with_no_stored_ticket_id_answers_whatever_ticket_asks",
    "test_malformed_ticket_id_is_refused_before_any_read",
    "test_a_viewer_not_admitted_reads_the_same_answer_with_a_wrong_ticket_as_with_a_right_one",
    "test_an_admitted_caller_is_told_the_ticket_does_not_match_by_its_own_public_reason",
)
PORTAL_TEST = "src/pages/TicketCenter/__tests__/package-open-ticket-binding.test.tsx"
PORTAL_NAMES = (
    "the Open control sends the ticket's own id with the report read",
    "a binding refusal is shown as a refusal and no report is rendered",
    "the request record is never shown in place of a refused report",
)
TOKENS = {"y71-bind": "Y71-BIND", "y71-keep": "Y71-KEEP", "y72-open": "Y72-OPEN", "y72-keep": "Y72-KEEP"}


def run(cmd, cwd, env=None):
    got = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    return got.returncode, (got.stdout or "") + (got.stderr or "")


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    env = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="y", AWS_DEFAULT_REGION="us-east-1")
    problems = []
    if check == "y71-bind":
        path = root / SVC_TEST
        if not path.is_file():
            return finish(check, ["no %s" % SVC_TEST])
        text = path.read_text(encoding="utf-8")
        for name in SVC_NAMES:
            if not re.search(r"^def %s\(" % name, text, flags=re.M):
                problems.append("no test named %s" % name)
        import json
        census = root / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r7/PUBLIC_REASON_READERS.json"
        if not census.is_file():
            problems.append("no reader census of the public-reason set (r7/PUBLIC_REASON_READERS.json)")
        else:
            doc = json.loads(census.read_text(encoding="utf-8"))
            readers = doc.get("readers") or []
            if not (isinstance(doc.get("new_public_reason"), str) and doc["new_public_reason"]):
                problems.append("the census does not name the new public reason")
            if not readers or not isinstance(doc.get("searched"), str) or not doc.get("searched"):
                problems.append("the census lists no reader, or does not say what was searched")
            for row in readers:
                if row.get("key_policy") not in ("EXACT", "TOLERANT") or row.get("side") not in ("SERVICE", "PORTAL") \
                        or not row.get("file_line") or row.get("meets_new_value") not in ("PASS", "REFUSES", "NOT_REACHED"):
                    problems.append("census row incomplete: %r" % (row.get("file_line"),))
            print("public-reason readers censused: %d" % len(readers))
        rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", SVC_TEST], root, env)
        print("\n".join([line for line in out.splitlines() if line.strip()][-1:]))
        if rc != 0:
            problems.append("pytest rc=%d on the binding test file" % rc)
        return finish(check, problems)
    if check == "y71-keep":
        rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", IR + "/ops/tests"], root, env)
        last = [line for line in out.splitlines() if line.strip()][-1:]
        print("\n".join(last))
        if rc != 0 or re.search(r"\d+ failed", last[0] if last else "failed"):
            problems.append("the ops test folder does not pass whole (rc=%d)" % rc)
        return finish(check, problems)
    if "--portal" not in argv:
        print(__doc__)
        return 2
    portal = Path(argv[argv.index("--portal") + 1])
    if check == "y72-open":
        path = portal / PORTAL_TEST
        if not path.is_file():
            return finish(check, ["no %s" % PORTAL_TEST])
        text = path.read_text(encoding="utf-8")
        for name in PORTAL_NAMES:
            if name not in text:
                problems.append("the test named %r is absent" % name)
        target = "./" + PORTAL_TEST
    else:
        target = "./src/pages/TicketCenter"
    rc, out = run(["bun", "test", target], portal)
    passed = re.search(r"(\d+) pass", out)
    failed = re.search(r"(\d+) fail", out)
    print("%s: %s pass, %s fail (rc=%d)" % (target, passed.group(1) if passed else "?", failed.group(1) if failed else "?", rc))
    if rc != 0 or not failed or int(failed.group(1)) != 0 or not passed or int(passed.group(1)) < (3 if check == "y72-open" else 42):
        problems.append("the portal tests do not pass")
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
