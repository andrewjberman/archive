"""ar19_checks.py -- the mechanical checks of IRPT_ANLREQ round 19, workstream Y.

Usage:  python ar19_checks.py <check> --root <worker worktree root>

  y191-scratch   AR-y-191: the start-state scratch-tree record covers the Lambda's door and re-open on the pinned pair, with the pins named and
                 each case carrying an outcome and its evidence                                                              -> Y191-SCRATCH-OK
  y192-census    AR-y-192: the release census names the map members, the four native unpinned members, the planned pin moves and the resident's
                 pin rule                                                                                                   -> Y192-CENSUS-OK
  y193-build     AR-y-193: the release build record names the package hash, a member manifest, and a planned-vs-actual member diff that agree  -> Y193-BUILD-OK
  y194-rule      AR-y-194: the widened rule and the value backstop over the stored population (every listed form matched, the count form
                 excluded only when its values are counts, every negative control unmatched)                                -> Y194-RULE-OK
  y194-backstop  AR-y-194: the named backstop tests exist and pass                                                            -> Y194-BACKSTOP-OK
  y194-keep      AR-y-194: the whole intake folder passes (floor 331) and READER_VERSION differs from r18.1                    -> Y194-KEEP-OK
  y195-delta     AR-y-195 (workstream YR): the resident package delta between the live resident's pin and the release pin names every differing
                 member with both hashes, the two reader members, and the other members grouped by owner                      -> Y195-DELTA-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

IR = "infra/aws/lambda/investor-reporting"
INTAKE = IR + "/intake"
D = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%s/r19/"
ROUND18_VERSION = "irpt-template-reader.r18.1"
TOKENS = {"y191-scratch": "Y191-SCRATCH", "y192-census": "Y192-CENSUS", "y193-build": "Y193-BUILD", "y194-rule": "Y194-RULE",
          "y194-backstop": "Y194-BACKSTOP", "y194-keep": "Y194-KEEP", "y195-delta": "Y195-DELTA"}
SHEETS = ("two_value_account_sheet", "total_row_sheet", "one_account_sheet", "two_sheet_workbook")
NATIVE_UNPINNED = ("acceptance.py", "submission.py", "submission_service.py", "durable_job.py")
S31_FORMS = ("Account Numbers", "Subaccounts", "Accnt", "Account Nos", "Account Seqno", "Account Serial", "Roth IRA Account", "Trust Account")
SEED_IDENTIFIERS = ("Account", "Account Number", "Acct", "Brokerage Account", "IRA Account", "Joint Account", "Subaccount", "Account Seq",
                    "Account Sequence", "No. of Account", "Sub-Account", "Custodian Acct", "Client Account") + S31_FORMS
SEED_ATTRIBUTES = ("Account Holder", "Account Manager", "Account Value", "Account Status", "Account Opened", "Account Type", "Account Name",
                   "Account Balance")
SEED_NOT_ACCOUNT = ("Custodian", "Accounting", "Portfolio", "Sleeve", "Model")
BACKSTOP_TESTS = (
    "test_an_account_root_header_with_two_identifier_values_is_read_as_an_account_column",
    "test_an_account_root_header_with_one_value_is_not_several_accounts",
    "test_no_of_accounts_holding_counts_is_excluded",
    "test_no_of_accounts_holding_identifiers_is_read_as_an_account_column",
    "test_the_backstop_words_say_what_is_seen_and_ask",
)


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def pytest(root, target, cwd):
    got = subprocess.run([sys.executable, "-m", "pytest", target, "-q", "-p", "no:cacheprovider"], cwd=str(root / cwd),
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
    passed, failed = re.search(r"(\d+) passed", out), re.search(r"(\d+) failed", out)
    return got.returncode, int(passed.group(1)) if passed else 0, int(failed.group(1)) if failed else 0


def load(root, rel, problems):
    if not (root / rel).is_file():
        problems.append("no %s" % rel)
        return None
    return json.loads((root / rel).read_text(encoding="utf-8"))


def reader_module(root):
    spec = importlib.util.spec_from_file_location("ar19_template_reader", str(root / INTAKE / "template_reader.py"))
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(root / INTAKE))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print("usage: ar19_checks.py <%s> --root <worktree>" % "|".join(TOKENS))
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y191-scratch":
        rec = load(root, D % "52" + "START_STATE_SCRATCH_RUN.json", problems)
        if rec:
            pins = rec.get("pins", {})
            for key in ("uploads.py", "template_reader.py"):
                if not pins.get(key):
                    problems.append("pins lacks %s" % key)
            cases = rec.get("door_cases", [])
            names = {c.get("sheet") for c in cases}
            for sheet in SHEETS:
                if sheet not in names:
                    problems.append("the door cases lack the sheet %s" % sheet)
            for c in cases + rec.get("reopen_cases", []):
                if not c.get("outcome") or not c.get("evidence"):
                    problems.append("a case lacks its outcome or evidence: %r" % c.get("sheet"))
            if not rec.get("reopen_cases"):
                problems.append("no re-open case (a pinned-stored template re-opened under the pinned pair and under the widened pair)")
            for member in ("scratch_tree", "claim", "not_read", "what_a_person_sees"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            print("door cases %d, re-open cases %d" % (len(cases), len(rec.get("reopen_cases", []))))
    elif check == "y192-census":
        rec = load(root, D % "51" + "YCHARTS_GENERATE_RELEASE_CENSUS.json", problems)
        if rec:
            native = {m.get("member") for m in rec.get("native_unpinned_members", [])}
            for name in NATIVE_UNPINNED:
                if name not in native:
                    problems.append("native_unpinned_members lacks %s" % name)
            for member in ("map_entry_members", "planned_pin_moves", "members_that_move", "resident", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            res = rec.get("resident") or {}
            for member in ("pin_rule", "current_pin", "builder", "deploy_path", "owner_lane"):
                if member not in res:
                    problems.append("resident lacks %r" % member)
            print("native unpinned named %d of 4; members that move %d" % (len(native & set(NATIVE_UNPINNED)), len(rec.get("members_that_move", []))))
    elif check == "y193-build":
        rec = load(root, D % "51" + "RELEASE_BUILD_RECORD.json", problems)
        if rec:
            for member in ("package_sha256", "member_manifest", "planned_members_that_move", "actual_members_that_differ_from_baseline", "baseline", "live_equivalent_baseline", "differs_from_unpatched_baseline", "base_commit", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if rec.get("planned_members_that_move") is not None and rec.get("actual_members_that_differ_from_baseline") is not None:
                if sorted(rec["planned_members_that_move"]) != sorted(rec["actual_members_that_differ_from_baseline"]):
                    problems.append("the planned members and the members that differ are not the same set")
            if not isinstance(rec.get("member_manifest"), dict) or len(rec.get("member_manifest", {})) < 20:
                problems.append("member_manifest must map at least 20 package members to their sha256")
            print("manifest members %d" % len(rec.get("member_manifest", {})))
    elif check == "y194-rule":
        pop = load(root, D % "56" + "ACCOUNT_HEADER_POPULATION.json", problems)
        if pop:
            reader = reader_module(root)
            ident, attr, other = pop.get("identifier_forms", []), pop.get("attribute_forms", []), pop.get("not_account_forms", [])
            neg = pop.get("word_negative_controls", [])
            for label, seeds, got in (("identifier_forms", SEED_IDENTIFIERS, ident), ("attribute_forms", SEED_ATTRIBUTES, attr),
                                      ("not_account_forms", SEED_NOT_ACCOUNT, other)):
                for seed in seeds:
                    if seed not in got:
                        problems.append("%s lacks the seed %r" % (label, seed))
            for form in ident:
                if not reader._is_account_header(form):
                    problems.append("identifier form not matched: %r" % form)
            for form in attr + other + neg:
                if reader._is_account_header(form):
                    problems.append("attribute, non-account or negative-control form matched: %r" % form)
            if len(neg) < 6:
                problems.append("word_negative_controls must hold at least 6 headers (one per new modifier or tail word, plus one for the backstop)")
            print("population: %d identifier, %d attribute, %d non-account, %d negative controls" % (len(ident), len(attr), len(other), len(neg)))
    elif check == "y194-backstop":
        path = root / INTAKE / "tests" / "test_account_value_backstop.py"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if not text:
            problems.append("no test_account_value_backstop.py")
        for name in BACKSTOP_TESTS:
            if text and ("def %s(" % name) not in text:
                problems.append("the test %s is absent" % name)
        rc, passed, failed = pytest(root, "tests/test_account_value_backstop.py", INTAKE)
        print("backstop tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < len(BACKSTOP_TESTS):
            problems.append("the named backstop tests must all pass")
    elif check == "y194-keep":
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 331:
            problems.append("the intake folder must pass with at least 331 (the round-18 count)")
        version = getattr(reader_module(root), "READER_VERSION", None)
        print("READER_VERSION = %s" % version)
        if not version or version == ROUND18_VERSION:
            problems.append("READER_VERSION must change in the same commit as what the reader returns (still %r)" % version)
    elif check == "y195-delta":
        rec = load(root, D % "55" + "RESIDENT_PACKAGE_DELTA.json", problems)
        if rec:
            for member in ("old_pin", "new_pin", "builder_args_source", "only_in_old", "only_in_new", "differing", "moved_by_this_release",
                           "other_differing_by_owner", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            moved = {m.get("member") if isinstance(m, dict) else m for m in rec.get("moved_by_this_release", [])}
            for name in ("uploads.py", "template_reader.py"):
                if not any(str(x).endswith(name) for x in moved):
                    problems.append("moved_by_this_release lacks %s" % name)
            for row in rec.get("differing", []):
                if not (row.get("member") and row.get("old_sha256") and row.get("new_sha256")):
                    problems.append("a differing row lacks its member or a hash: %r" % row.get("member"))
                    break
            print("differing %d, only in old %d, only in new %d" % (len(rec.get("differing", [])), len(rec.get("only_in_old", [])), len(rec.get("only_in_new", []))))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
