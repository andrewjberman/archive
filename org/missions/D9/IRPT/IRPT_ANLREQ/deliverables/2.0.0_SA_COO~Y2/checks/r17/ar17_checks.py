"""ar17_checks.py -- the mechanical checks of IRPT_ANLREQ round 17, workstream Y.

Usage:  python ar17_checks.py <check> --root <worker worktree root>

  y171-rule     AR-y-171: the account-header rule, run over the stored population, has 0 identifier forms unmatched and 0 attribute
                forms turned back, plus one new form of each class not in the seeds                       -> Y171-RULE-OK
  y171-keep     AR-y-171: the whole intake test folder passes (floor 311) and the reader version differs from the round-16 one -> Y171-KEEP-OK
  y172-status   AR-y-172: the named status tests exist in _authz/tests and pass                            -> Y172-STATUS-OK
  y172-keep     AR-y-172: the whole _authz test folder passes (floor 320, the base)                        -> Y172-KEEP-OK
  y173-census   AR-y-173: the census script self-tests offline, holds no write-shaped call, and its record is complete -> Y173-CENSUS-OK
  y174-trace    AR-y-174: the mixed-version trace record covers all four writer/reader version pairs       -> Y174-TRACE-OK

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
DEL52 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r17/"
DEL51 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~51/r17/"
DEL54 = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~54/r17/"
ROUND16_VERSION = "irpt-template-reader.r16.1"
TOKENS = {"y171-rule": "Y171-RULE", "y171-keep": "Y171-KEEP", "y172-status": "Y172-STATUS", "y172-keep": "Y172-KEEP",
          "y173-census": "Y173-CENSUS", "y174-trace": "Y174-TRACE"}
# SEEDS: the forms the round-16 census named (row IRPT_ANLREQ-D2-W52-S20). The worker's population must CONTAIN them; it may add more.
SEED_IDENTIFIERS = ("Accounts", "Acc #", "Acc No", "Custodian Acct", "Sub-Account", "Account-Number", "Client Account",
                    "Account/Number", "No. of Accounts", "Account", "Account Number", "Account #", "Acct", "Account No")
SEED_ATTRIBUTES = ("Account Holder", "Account Manager", "Account Value", "Account Status", "Account Opened", "Account Type",
                   "Account Name")
SEED_NOT_ACCOUNT = ("Custodian", "Accounting", "Portfolio", "Sleeve", "Model")
STATUS_TESTS = (
    "test_internal_caller_with_an_active_row_is_admitted",
    "test_internal_caller_with_a_disabled_row_is_refused",
    "test_internal_caller_with_a_row_and_no_status_is_refused",
    "test_internal_caller_with_no_row_is_refused",
    "test_service_and_client_callers_are_unchanged",
)
CASES = {("old", "old"), ("new", "new"), ("old", "new"), ("new", "old")}
FORBIDDEN_CALLS = re.compile(
    r"\.(put_item|update_item|delete_item|batch_write_item|transact_write_items|put_object|delete_object|copy_object|"
    r"send_message|send_message_batch|publish|put_events|start_execution|create_\w+|update_function_\w+|invoke|"
    r"put_parameter|put_secret_value|admin_\w+)\(")


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


def named(path, names, problems):
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    if not text:
        problems.append("no %s" % path.name)
    for name in names:
        if text and ("def %s(" % name) not in text:
            problems.append("the test %s is absent from %s" % (name, path.name))


def reader_module(root):
    path = root / INTAKE / "template_reader.py"
    spec = importlib.util.spec_from_file_location("ar17_template_reader", str(path))
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(root / INTAKE))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print("usage: ar17_checks.py <%s> --root <worktree>" % "|".join(TOKENS))
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y171-rule":
        pop = load(root, DEL52 + "ACCOUNT_HEADER_POPULATION.json", problems)
        if pop:
            reader = reader_module(root)
            ident, attr, other = pop.get("identifier_forms", []), pop.get("attribute_forms", []), pop.get("not_account_forms", [])
            new_i, new_a = pop.get("new_identifier_form"), pop.get("new_attribute_form")
            for label, seeds, got in (("identifier_forms", SEED_IDENTIFIERS, ident), ("attribute_forms", SEED_ATTRIBUTES, attr),
                                      ("not_account_forms", SEED_NOT_ACCOUNT, other)):
                for seed in seeds:
                    if seed not in got:
                        problems.append("%s lacks the seed %r" % (label, seed))
            for form in ident:
                if not reader._is_account_header(form):
                    problems.append("identifier form not matched: %r" % form)
            for form in attr + other:
                if reader._is_account_header(form):
                    problems.append("attribute or non-account form turned back as an account header: %r" % form)
            for label, form, seeds in (("new_identifier_form", new_i, SEED_IDENTIFIERS), ("new_attribute_form", new_a, SEED_ATTRIBUTES)):
                if not form or form in seeds or form in ident or form in attr:
                    problems.append("%s must be a form NOT in the seeds or the population lists" % label)
            if new_i and not reader._is_account_header(new_i):
                problems.append("the new identifier control is not matched: %r" % new_i)
            if new_a and reader._is_account_header(new_a):
                problems.append("the new attribute control is turned back: %r" % new_a)
            print("population: %d identifier, %d attribute, %d non-account forms" % (len(ident), len(attr), len(other)))
    elif check == "y171-keep":
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 311:
            problems.append("the intake folder must pass with at least 311 (it was 311 at the round base)")
        reader = reader_module(root)
        version = getattr(reader, "READER_VERSION", None)
        print("READER_VERSION = %s" % version)
        if not version or version == ROUND16_VERSION:
            problems.append("READER_VERSION must change in the same commit as what the reader returns (still %r)" % version)
    elif check == "y172-status":
        named(root / IR / "_authz/tests/test_internal_status_active.py", STATUS_TESTS, problems)
        rc, passed, failed = pytest(root, "tests/test_internal_status_active.py", IR + "/_authz")
        print("status tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < len(STATUS_TESTS):
            problems.append("the status tests must all pass")
    elif check == "y172-keep":
        rc, passed, failed = pytest(root, "tests", IR + "/_authz")
        print("_authz tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 320:
            problems.append("the _authz folder must pass with at least 320 (the base count)")
    elif check == "y173-census":
        script = root / (DEL51 + "count_internal_callers.py")
        rec = load(root, DEL51 + "CENSUS_SCRIPT_RECORD.json", problems)
        if not script.is_file():
            problems.append("no count_internal_callers.py")
        else:
            text = script.read_text(encoding="utf-8")
            if any(ord(ch) > 127 for ch in text):
                problems.append("the script holds non-ASCII")
            for match in FORBIDDEN_CALLS.finditer(text):
                problems.append("a write-shaped or invoke call in the script: %s" % match.group(0))
            done = subprocess.run([sys.executable, "-I", str(script), "--self-test"], capture_output=True, text=True, timeout=300)
            if done.returncode != 0 or "CENSUS-SELFTEST-OK" not in done.stdout:
                problems.append("--self-test rc=%s" % done.returncode)
        if rec:
            for member in ("script_blob", "what_it_reads", "what_it_cannot_read", "output_members", "no_address_in_output"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
    elif check == "y174-trace":
        rec = load(root, DEL52 + "MIXED_VERSION_TRACE.json", problems)
        if rec:
            cases = {(c.get("writer_version"), c.get("reader_version")) for c in rec.get("cases", [])}
            for missing in sorted(CASES - cases):
                problems.append("the trace lacks the case writer=%s reader=%s" % missing)
            for c in rec.get("cases", []):
                if not c.get("outcome") or not c.get("evidence"):
                    problems.append("a case lacks its outcome or its evidence: writer=%s reader=%s" % (c.get("writer_version"), c.get("reader_version")))
            for member in ("consumers", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            print("cases: %d" % len(rec.get("cases", [])))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
