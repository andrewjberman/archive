"""ar18_checks.py -- the mechanical checks of IRPT_ANLREQ round 18, workstream Y.

Usage:  python ar18_checks.py <check> --root <worker worktree root>

  y181-rule   AR-y-181: the account-header rule, widened, over the stored population: every identifier form matched (the new modifier, account and
              identifier words included), `No. of Accounts` (a COUNT) unmatched while `No. of Account` still matches, every attribute and non-account
              form unmatched, and each negative control (a header carrying a NEW word that is not an account column) unmatched      -> Y181-RULE-OK
  y181-keep   AR-y-181: the whole intake test folder passes (floor 317) and READER_VERSION differs from the round-17 one                -> Y181-KEEP-OK
  y183-bite   AR-y-183: the six named bite tests exist in _authz/tests and pass                                                      -> Y183-BITE-OK
  y183-keep   AR-y-183: the whole _authz test folder passes (floor 337)                                                              -> Y183-KEEP-OK
  y184-log    AR-y-184: the named caller-class log tests exist in _authz/tests and pass                                             -> Y184-LOG-OK
  y184-keep   AR-y-184: the whole _authz test folder passes (floor 337)                                                              -> Y184-KEEP-OK
  y185-read   AR-y-185: the eight-function record names each function that packages served.py, with its pin                         -> Y185-READ-OK
  y186-trace  AR-y-186: the trace record adds the Lambda's third reader to the four writer/reader pairs                              -> Y186-TRACE-OK

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
D = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%s/r18/"
ROUND17_VERSION = "irpt-template-reader.r17.1"
TOKENS = {"y181-rule": "Y181-RULE", "y181-keep": "Y181-KEEP", "y183-bite": "Y183-BITE", "y183-keep": "Y183-KEEP",
          "y184-log": "Y184-LOG", "y184-keep": "Y184-KEEP", "y185-read": "Y185-READ", "y186-trace": "Y186-TRACE"}
SEED_IDENTIFIERS = ("Accounts", "Acc #", "Acc No", "Custodian Acct", "Sub-Account", "Account-Number", "Client Account", "Account/Number",
                    "Account", "Account Number", "Account #", "Acct", "Account No", "No. of Account",
                    "Brokerage Account", "IRA Account", "Joint Account", "Subaccount", "Account Seq", "Account Sequence")
SEED_COUNT_FORMS = ("No. of Accounts",)
SEED_ATTRIBUTES = ("Account Holder", "Account Manager", "Account Value", "Account Status", "Account Opened", "Account Type", "Account Name",
                   "Account Balance")
SEED_NOT_ACCOUNT = ("Custodian", "Accounting", "Portfolio", "Sleeve", "Model")
NEW_WORDS = ("brokerage", "ira", "joint", "subaccount", "seq", "sequence")
BITE_TESTS = (
    "test_read_actor_arm_bites_when_its_named_check_alone_is_removed",
    "test_read_owner_arm_bites_when_its_named_check_alone_is_removed",
    "test_read_renderer_arm_bites_when_its_named_check_alone_is_removed",
    "test_prospect_actor_arm_bites_when_its_named_check_alone_is_removed",
    "test_prospect_owner_arm_bites_when_its_named_check_alone_is_removed",
    "test_prospect_renderer_arm_bites_when_its_named_check_alone_is_removed",
)
LOG_TESTS = (
    "test_a_caller_with_an_active_row_logs_the_class_row_present",
    "test_a_caller_with_no_row_logs_the_class_row_absent",
    "test_a_caller_with_a_non_active_row_logs_the_class_row_non_active",
    "test_the_caller_class_line_carries_no_identity",
)
EIGHT = ("irpt-performance-adapter", "irpt-directory-search", "irpt-narrative", "irpt-ycharts-generate", "irpt-export-render", "irpt-holdings",
         "irpt-status", "irpt-49f-reporting-read-lambda")


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
    spec = importlib.util.spec_from_file_location("ar18_template_reader", str(root / INTAKE / "template_reader.py"))
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(root / INTAKE))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print("usage: ar18_checks.py <%s> --root <worktree>" % "|".join(TOKENS))
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y181-rule":
        pop = load(root, D % "52" + "ACCOUNT_HEADER_POPULATION.json", problems)
        if pop:
            reader = reader_module(root)
            ident, counts = pop.get("identifier_forms", []), pop.get("count_forms", [])
            attr, other, neg = pop.get("attribute_forms", []), pop.get("not_account_forms", []), pop.get("word_negative_controls", [])
            for label, seeds, got in (("identifier_forms", SEED_IDENTIFIERS, ident), ("count_forms", SEED_COUNT_FORMS, counts),
                                      ("attribute_forms", SEED_ATTRIBUTES, attr), ("not_account_forms", SEED_NOT_ACCOUNT, other)):
                for seed in seeds:
                    if seed not in got:
                        problems.append("%s lacks the seed %r" % (label, seed))
            for form in ident:
                if not reader._is_account_header(form):
                    problems.append("identifier form not matched: %r" % form)
            for form in counts:
                if reader._is_account_header(form):
                    problems.append("a COUNT form is matched as an account header: %r" % form)
            for form in attr + other:
                if reader._is_account_header(form):
                    problems.append("attribute or non-account form turned back: %r" % form)
            if len(neg) < 5:
                problems.append("word_negative_controls must hold at least 5 headers (one for each new word that is not an account column)")
            for form in neg:
                if reader._is_account_header(form):
                    problems.append("a negative control is matched as an account header: %r" % form)
            seen = {w for form in neg for w in NEW_WORDS if re.search(r"\b%s\b" % w, form.lower())}
            for word in ("brokerage", "ira", "joint", "seq", "sequence"):
                if word not in seen:
                    problems.append("no negative control carries the new word %r" % word)
            print("population: %d identifier, %d count, %d attribute, %d non-account, %d negative controls" % (
                len(ident), len(counts), len(attr), len(other), len(neg)))
    elif check == "y181-keep":
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 317:
            problems.append("the intake folder must pass with at least 317 (the round-17 count)")
        version = getattr(reader_module(root), "READER_VERSION", None)
        print("READER_VERSION = %s" % version)
        if not version or version == ROUND17_VERSION:
            problems.append("READER_VERSION must change in the same commit as what the reader returns (still %r)" % version)
    elif check in ("y183-bite", "y184-log"):
        fname, names = (("test_final_release_bites.py", BITE_TESTS) if check == "y183-bite" else ("test_caller_class_log.py", LOG_TESTS))
        named(root / IR / "_authz/tests" / fname, names, problems)
        rc, passed, failed = pytest(root, "tests/" + fname, IR + "/_authz")
        print("%s: %d passed, %d failed (rc=%d)" % (fname, passed, failed, rc))
        if rc != 0 or failed or passed < len(names):
            problems.append("the named tests must all pass")
    elif check in ("y183-keep", "y184-keep"):
        rc, passed, failed = pytest(root, "tests", IR + "/_authz")
        print("_authz tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 337:
            problems.append("the _authz folder must pass with at least 337 (the round-17 count)")
    elif check == "y185-read":
        rec = load(root, D % "51" + "SERVED_PY_PACKAGERS.json", problems)
        if rec:
            funcs = {f.get("function"): f for f in rec.get("functions", [])}
            for name in EIGHT:
                if name not in funcs:
                    problems.append("the record lacks the function %s" % name)
                elif not funcs[name].get("pin") or not funcs[name].get("how_it_packages_served_py"):
                    problems.append("%s lacks its pin or how it packages served.py" % name)
            for member in ("map_denominator", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            extra = sorted(set(funcs) - set(EIGHT))
            print("functions: %d named of 8; extra named: %s" % (len(set(funcs) & set(EIGHT)), extra))
    elif check == "y186-trace":
        rec = load(root, D % "52" + "MIXED_VERSION_TRACE_THIRD_READER.json", problems)
        if rec:
            readers = {c.get("reader_version") for c in rec.get("cases", [])} | {c.get("writer_version") for c in rec.get("cases", [])}
            if "lambda_pinned" not in readers:
                problems.append("no case runs the Lambda's pinned reader (version name lambda_pinned)")
            for c in rec.get("cases", []):
                if not c.get("outcome") or not c.get("evidence"):
                    problems.append("a case lacks its outcome or evidence: writer=%s reader=%s" % (c.get("writer_version"), c.get("reader_version")))
            for member in ("pin", "claim", "not_read", "cases"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            print("cases: %d" % len(rec.get("cases", [])))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
