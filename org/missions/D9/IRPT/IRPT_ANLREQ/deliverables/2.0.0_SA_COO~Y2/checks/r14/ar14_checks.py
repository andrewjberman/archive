"""ar14_checks.py -- the mechanical checks of IRPT_ANLREQ round 14, workstream Y (the upload door's account and totals check).

Usage:  python ar14_checks.py <check> --root <workspace root> [--portal <portal root>]

  y141-ask      AR-y-141: the record of how the live provider is asked about a total label          -> Y141-ASK-OK
  y142-census   AR-y-142: the reader's seven named tests pass and both closed lists carry a record -> Y142-CENSUS-OK
  y142-keep     AR-y-142/143: the whole intake test folder passes                                  -> Y142-KEEP-OK
  y143-words    AR-y-143: every finding code has words; POST-decidable findings on the first answer -> Y143-WORDS-OK
  y144-form     AR-y-144: the form's four named tests pass and the folder passes (needs --portal)  -> Y144-FORM-OK
  y145-census   AR-y-145: the release census of the upload door is complete                        -> Y145-CENSUS-OK
  y146-mentions AR-y-146: every mention of parse.py as the form's door is listed with a disposition -> Y146-MENTIONS-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

INTAKE = "infra/aws/lambda/investor-reporting/intake"
D52 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r14/"
D53 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r14/"
D54 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~54/r14/"
READER_TESTS = (
    "test_account_column_with_two_values_is_turned_back_with_words",
    "test_account_column_with_one_value_is_accepted",
    "test_repeated_header_row_is_turned_back_with_words",
    "test_total_row_is_turned_back_with_its_row_number",
    "test_same_ticker_on_two_rows_is_not_several_accounts",
    "test_known_good_sheet_is_accepted",
    "test_accepted_answer_says_only_the_first_sheet_was_read",
)
WORDS_TESTS = (
    "test_every_finding_code_the_reader_can_emit_has_words",
    "test_post_decidable_findings_arrive_on_the_first_answer",
    "test_a_sheet_that_needs_pricing_still_answers_resolving_first",
)
FORM_TEST = "src/pages/TicketCenter/__tests__/analysis-request-repost.test.tsx"
FORM_NAMES = (
    "a finding on the first answer is shown without a second press",
    "a resolving answer is re-posted a bounded number of times",
    "after the bound the form says it is still working and files nothing",
    "a raw code is shown only inside closed details",
)
TOKENS = {"y141-ask": "Y141-ASK", "y142-census": "Y142-CENSUS", "y142-keep": "Y142-KEEP", "y143-words": "Y143-WORDS",
          "y144-form": "Y144-FORM", "y145-census": "Y145-CENSUS", "y146-mentions": "Y146-MENTIONS"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def pytest(root, target, names=()):
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


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y141-ask":
        doc = load(root, D53 + "TOTAL_LABEL_PROVIDER_ASK.json", problems)
        if doc is not None:
            provider = doc.get("provider") or {}
            if not (provider.get("file_function") and provider.get("what_it_calls")):
                problems.append("provider needs file_function and what_it_calls")
            if not doc.get("labels_to_ask") or not doc.get("symbol_each_label_becomes"):
                problems.append("labels_to_ask and symbol_each_label_becomes are required")
            seats = doc.get("who_can_ask") or []
            if not seats or any(not (row.get("identity") and row.get("how") and isinstance(row.get("new_grant_needed"), bool)) for row in seats):
                problems.append("who_can_ask needs at least one row with identity, how and new_grant_needed")
            if not doc.get("exact_invocation") or not isinstance(doc.get("not_read"), list):
                problems.append("exact_invocation and not_read are required")
            if doc.get("live_call_made") is not False:
                problems.append("live_call_made must be false: this cell asks nothing live")
        return finish(check, problems)
    if check == "y142-census":
        path = root / INTAKE / "tests/test_template_account_totals.py"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for name in READER_TESTS:
            if ("def %s(" % name) not in text:
                problems.append("the test %s is absent" % name)
        if text:
            rc, passed, failed = pytest(root, "tests/test_template_account_totals.py")
            print("account/totals tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < len(READER_TESTS):
                problems.append("the account/totals test file does not pass with at least %d tests" % len(READER_TESTS))
        doc = load(root, D52 + "CLOSED_LISTS_RULE24.json", problems)
        if doc is not None:
            for key in ("account_words", "total_words"):
                row = doc.get(key) or {}
                if not (row.get("members") and row.get("domain") and row.get("denominator") and isinstance(row.get("uncovered_by_subtraction"), list)
                        and row.get("where_in_code")):
                    problems.append("%s needs members, domain, denominator, uncovered_by_subtraction and where_in_code" % key)
        return finish(check, problems)
    if check == "y142-keep":
        rc, passed, failed = pytest(root, "tests")
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 292:
            problems.append("the intake test folder does not pass whole (292 passed at the base)")
        return finish(check, problems)
    if check == "y143-words":
        path = root / INTAKE / "tests/test_correction_words.py"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for name in WORDS_TESTS:
            if ("def %s(" % name) not in text:
                problems.append("the test %s is absent" % name)
        rc, passed, failed = pytest(root, "tests/test_correction_words.py")
        print("correction-words tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < len(WORDS_TESTS):
            problems.append("the correction-words test file does not pass")
        return finish(check, problems)
    if check == "y144-form":
        if "--portal" not in argv:
            print(__doc__)
            return 2
        portal = Path(argv[argv.index("--portal") + 1])
        text = (portal / FORM_TEST).read_text(encoding="utf-8") if (portal / FORM_TEST).is_file() else ""
        for name in FORM_NAMES:
            if name not in text:
                problems.append("the test named %r is absent" % name)
        if "setTimeout(" in text and "useFakeTimers" not in text and "wait:" not in text:
            problems.append("the test file waits on a real timer")
        got = subprocess.run(["bun", "test", "./src/pages/TicketCenter"], cwd=str(portal), capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
        passed, failed = re.search(r"(\d+) pass", out), re.search(r"(\d+) fail", out)
        print("TicketCenter folder: %s pass, %s fail (rc=%d)" % (passed.group(1) if passed else "?", failed.group(1) if failed else "?",
                                                                  got.returncode))
        if got.returncode != 0 or not failed or int(failed.group(1)) != 0 or not passed or int(passed.group(1)) < 62 + len(FORM_NAMES):
            problems.append("the TicketCenter folder does not pass whole with the four new tests (62 at the base)")
        return finish(check, problems)
    if check == "y145-census":
        doc = load(root, D53 + "UPLOAD_DOOR_RELEASE_CENSUS.json", problems)
        if doc is not None:
            functions = doc.get("functions_that_package_the_reader") or []
            if not functions or any(not (row.get("function") and row.get("live_code_sha256") and row.get("build_sha256")
                                         and isinstance(row.get("changed_members_vs_live"), list)) for row in functions):
                problems.append("functions_that_package_the_reader needs function, live_code_sha256, build_sha256 and changed_members_vs_live per row")
            consumers = doc.get("consumers_of_the_answer") or []
            if not consumers or any(not (row.get("file_function") and row.get("one_read_through_it") and isinstance(row.get("admits_new_answer"), bool)
                                         and row.get("deciding_line")) for row in consumers):
                problems.append("consumers_of_the_answer needs file_function, one_read_through_it, admits_new_answer and deciding_line per row")
            branches = doc.get("accepted_yesterday_turned_back_today") or {}
            if not (branches.get("branch_turned_back") and branches.get("branch_still_accepted") and branches.get("what_happens_to_inputs_already_accepted")):
                problems.append("accepted_yesterday_turned_back_today needs both branches and what happens to inputs already accepted")
            if not isinstance(doc.get("not_read"), list):
                problems.append("not_read must be a list")
        return finish(check, problems)
    doc = load(root, D54 + "PARSE_PY_MENTIONS.json", problems)
    if doc is not None:
        rows = doc.get("mentions") or []
        if not doc.get("searched") or not isinstance(doc.get("files_searched"), int):
            problems.append("searched and files_searched (the denominator) are required")
        if any(not (row.get("file") and row.get("line") and row.get("says") and row.get("disposition") in
                    ("NAMES_IT_AS_THE_FORMS_DOOR", "NAMES_IT_CORRECTLY", "QUOTES_ANOTHER_RECORD") and row.get("owner_lane")) for row in rows):
            problems.append("each mention needs file, line, says, disposition and owner_lane")
        if not rows:
            problems.append("mentions is empty; the issuer's own round-13 order is known to name it")
        print("mentions %d over %s files" % (len(rows), doc.get("files_searched")))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
