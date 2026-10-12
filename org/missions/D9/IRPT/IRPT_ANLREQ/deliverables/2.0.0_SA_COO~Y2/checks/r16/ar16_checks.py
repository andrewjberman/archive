"""ar16_checks.py -- the mechanical checks of IRPT_ANLREQ round 16, workstream Y.

Usage:  python ar16_checks.py <check> --root <workspace root> [--portal <portal root>]

  y161-count    AR-y-161: the stored-input count script self-tests offline and its record is complete   -> Y161-COUNT-OK
  y162-reland   AR-y-162: the stored-input contract's named tests and the reader's named tests pass     -> Y162-RELAND-OK
  y162-keep     AR-y-162: the whole intake test folder passes                                           -> Y162-KEEP-OK
  y163-read     AR-y-163: the read of the internal firm reader and a caller with no users row           -> Y163-READ-OK
  y164-sent     AR-y-164: the ticket page shows commentary_sent and offers the one-time control (needs --portal) -> Y164-SENT-OK
  y165-read     AR-y-165: the read of the original-file route's rule and trusted headers                -> Y165-READ-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

INTAKE = "infra/aws/lambda/investor-reporting/intake"
DEL = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%s/r16/"
CONTRACT_TESTS = (
    "test_an_input_stored_by_the_base_reader_is_read_unchanged_by_the_new_reader",
    "test_an_input_stored_by_the_new_reader_with_an_altered_template_is_refused",
    "test_an_original_with_altered_bytes_is_refused_under_both_versions",
    "test_a_stored_input_with_no_version_member_reads_as_the_version_before",
    "test_the_readers_output_on_the_fixtures_is_pinned_to_its_version",
)
READER_TESTS = (
    "test_account_column_with_two_values_is_turned_back_with_words",
    "test_account_number_sign_header_is_an_account_column",
    "test_account_column_with_one_value_is_accepted",
    "test_repeated_header_row_says_what_is_seen_and_asks",
    "test_total_row_is_turned_back_with_its_row_number",
    "test_same_ticker_on_two_rows_is_not_several_accounts",
    "test_known_good_sheet_is_accepted",
)
SENT_TEST = "src/pages/TicketCenter/__tests__/commentary-sent.test.tsx"
SENT_NAMES = (
    "a ticket with commentary_sent shows who sent it and when",
    "the control is offered only when a draft exists and nothing is recorded",
    "the press asks for confirmation before it posts",
    "a confirmed press posts once with no body and shows the recorded sender",
    "each refusal code is shown in words",
)
TOKENS = {"y161-count": "Y161-COUNT", "y162-reland": "Y162-RELAND", "y162-keep": "Y162-KEEP", "y163-read": "Y163-READ",
          "y164-sent": "Y164-SENT", "y165-read": "Y165-READ"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def pytest(root, target):
    got = subprocess.run([sys.executable, "-m", "pytest", target, "-q", "-p", "no:cacheprovider"], cwd=str(root / INTAKE),
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
    passed, failed = re.search(r"(\d+) passed", out), re.search(r"(\d+) failed", out)
    return got.returncode, int(passed.group(1)) if passed else 0, int(failed.group(1)) if failed else 0


def load(root, rel, problems):
    if not (root / rel).is_file():
        problems.append("no %s" % rel)
        return None
    return json.loads((root / rel).read_text(encoding="utf-8"))


def named(path, names, problems):
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    for name in names:
        if ("def %s(" % name) not in text:
            problems.append("the test %s is absent from %s" % (name, path.name))
    return bool(text)


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y161-count":
        base = DEL % "52"
        script = root / (base + "count_stored_inputs.py")
        if not script.is_file():
            problems.append("no %scount_stored_inputs.py" % base)
        else:
            got = subprocess.run([sys.executable, str(script), "--self-test"], cwd=str(root), capture_output=True, text=True,
                                 encoding="utf-8", errors="replace")
            line = (got.stdout or "").strip().splitlines()[-1] if (got.stdout or "").strip() else ""
            try:
                out = json.loads(line)
            except ValueError:
                out = None
            if got.returncode != 0 or not isinstance(out, dict):
                problems.append("--self-test does not exit 0 with one JSON object as its last line (rc=%d)" % got.returncode)
            else:
                for key in ("inputs_by_lane", "template_inputs", "read_differently", "by_cause", "unreadable", "turned_back_with_a_report"):
                    if key not in out:
                        problems.append("the self-test output lacks %r" % key)
                text = script.read_text(encoding="utf-8")
                for banned in ("put_item", "update_item", "delete_item", "put_object", "delete_object", "invoke(", "send_message"):
                    if banned in text:
                        problems.append("the script contains the write call %r" % banned)
        doc = load(root, base + "COUNT_SCRIPT_RECORD.json", problems)
        if doc is not None:
            if not (doc.get("reads") and doc.get("new_reader_source") and doc.get("output_fields") and isinstance(doc.get("writes"), list)
                    and doc.get("how_a_report_is_tied_to_an_input") and isinstance(doc.get("not_read"), list)):
                problems.append("the record needs reads, new_reader_source, output_fields, writes, how_a_report_is_tied_to_an_input, not_read")
            if doc.get("writes"):
                problems.append("the record lists a write; the count is read-only")
        return finish(check, problems)
    if check == "y162-reland":
        have = named(root / INTAKE / "tests/test_stored_input_contract.py", CONTRACT_TESTS, problems)
        have = named(root / INTAKE / "tests/test_template_account_totals.py", READER_TESTS, problems) and have
        if have:
            rc, passed, failed = pytest(root, "tests/test_stored_input_contract.py")
            print("contract tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < len(CONTRACT_TESTS):
                problems.append("the stored-input contract tests do not pass")
            rc, passed, failed = pytest(root, "tests/test_template_account_totals.py")
            print("reader tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < len(READER_TESTS):
                problems.append("the reader tests do not pass")
        reader = (root / INTAKE / "template_reader.py").read_text(encoding="utf-8")
        if "READER_VERSION" not in reader:
            problems.append("template_reader.py declares no READER_VERSION")
        return finish(check, problems)
    if check == "y162-keep":
        rc, passed, failed = pytest(root, "tests")
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 292:
            problems.append("the intake test folder does not pass whole (292 passed at the base)")
        return finish(check, problems)
    if check == "y163-read":
        doc = load(root, DEL % "53" + "INTERNAL_READER_NO_ROW_READ.json", problems)
        if doc is not None:
            reader = doc.get("reader") or {}
            if not (reader.get("file_function") and reader.get("stated_rule")):
                problems.append("reader needs file_function and stated_rule")
            cases = {str(row.get("case")): row for row in doc.get("cases") or []}
            for case in ("NO_ROW", "DISABLED_ROW", "ACTIVE_ROW_OWN_FIRM", "ACTIVE_ROW_OTHER_FIRM"):
                row = cases.get(case)
                if not row or not (row.get("returns") and row.get("claim") in ("measured", "inferred") and row.get("evidence")):
                    problems.append("cases lacks a complete row for %s" % case)
            routes = doc.get("routes_it_guards") or []
            if not routes or any(not (row.get("route") and row.get("file_line")) for row in routes):
                problems.append("routes_it_guards needs at least one row with route and file_line")
            if not doc.get("the_ticket_service_shape") or not doc.get("proposed_cell") or not isinstance(doc.get("not_read"), list):
                problems.append("the_ticket_service_shape, proposed_cell and not_read are required")
        return finish(check, problems)
    if check == "y164-sent":
        if "--portal" not in argv:
            print(__doc__)
            return 2
        portal = Path(argv[argv.index("--portal") + 1])
        text = (portal / SENT_TEST).read_text(encoding="utf-8") if (portal / SENT_TEST).is_file() else ""
        for name in SENT_NAMES:
            if name not in text:
                problems.append("the test named %r is absent" % name)
        got = subprocess.run(["bun", "test", "./src/pages/TicketCenter"], cwd=str(portal), capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
        passed, failed = re.findall(r"^\s*(\d+) pass", out, re.M), re.findall(r"^\s*(\d+) fail", out, re.M)
        p, f = (int(passed[-1]) if passed else -1), (int(failed[-1]) if failed else -1)
        print("TicketCenter folder: %d pass, %d fail (rc=%d)" % (p, f, got.returncode))
        if got.returncode != 0 or f != 0 or p < 67 + len(SENT_NAMES):
            problems.append("the TicketCenter folder does not pass whole with the five new tests (67 at the base)")
        return finish(check, problems)
    doc = load(root, DEL % "54" + "ORIGINAL_ROUTE_RULE_READ.json", problems)
    if doc is not None:
        route = doc.get("route") or {}
        if not (route.get("operation") and route.get("handler_file_function") and route.get("owner_check_file_line")):
            problems.append("route needs operation, handler_file_function and owner_check_file_line")
        if not doc.get("trusted_headers") or not doc.get("how_a_caller_is_shaped"):
            problems.append("trusted_headers and how_a_caller_is_shaped are required")
        tools = doc.get("instruments") or []
        if not tools or any(not (row.get("instrument") and isinstance(row.get("can_shape_another_firms_client"), bool)
                                 and isinstance(row.get("writes_anything"), bool) and row.get("evidence")) for row in tools):
            problems.append("instruments needs rows with instrument, can_shape_another_firms_client, writes_anything and evidence")
        arms = doc.get("arms") or {}
        if not (arms.get("other_firm_client") and arms.get("owner_twin") and arms.get("what_is_never_written")):
            problems.append("arms needs other_firm_client, owner_twin and what_is_never_written")
        if not isinstance(doc.get("not_read"), list):
            problems.append("not_read must be a list")
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
