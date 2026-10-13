"""ar21_checks.py -- the mechanical checks of IRPT_ANLREQ round 21, workstream Y.

Usage:  python ar21_checks.py <check> --root <worker worktree root>

  y221-allowlist  AR-y-221: the r19.3 backstop admits a root header only when every other word is an identifier-tail word (alias a tail word, primary a
                  modifier): the ten r19.2 negatives and the CVO's six neighbours return nothing, the positives (two-account controls, Acct Alias,
                  Primary Acct) are turned back, and the five named backstop tests pass                                  -> Y221-ALLOWLIST-OK
  y221-keep       AR-y-221: the whole intake folder passes (floor 364) and READER_VERSION differs from r19.2             -> Y221-KEEP-OK
  y222-verify     AR-y-222: the ci script's verify step is fixed and shown on two arms (a landed upload exits 0 and updates the map; a failing head-object
                  exits non-zero with the CLI's error printed and the map untouched)                                     -> Y222-VERIFY-OK
  y223-design     AR-y-223: the driven status-rule exercise is designed from the precedent and predicted offline for three identities
                                                                                                                         -> Y223-DESIGN-OK

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
D = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%s/r21/"
ROUND192_VERSION = "irpt-template-reader.r19.2"
TOKENS = {"y221-allowlist": "Y221-ALLOWLIST", "y221-keep": "Y221-KEEP", "y222-verify": "Y222-VERIFY", "y223-design": "Y223-DESIGN"}
NEGATIVES = (
    ("Acct Market Value", ("25000000", "31000000")), ("Acct CUSIP", ("912828ZT6", "38141G104")), ("Acct Lot", ("LOT1234", "LOT5678")),
    ("Accnt Value", ("12000000", "15000000")), ("Acct Status", ("AX1234", "BX5678")), ("Acct Type", ("IRA1234", "ROTH5678")),
    ("Acct Name", ("ACME-401K", "ACME-403B")), ("Acct Holder", ("SMITH2024", "JONES2023")), ("Acct Balance", ("10000000", "12000000")),
    ("Acct Opened", ("20200101", "20210202")),
    # the CVO's six neighbours (round-20 grade, AR211-y-AC3J)
    ("Acct Cost Basis", ("25000000", "31000000")), ("Acct Gain", ("12000000", "13000000")), ("Acct Weight", ("12345678", "87654321")),
    ("Acct Description", ("NOTE1234", "NOTE5678")), ("Acct Currency", ("USD2024", "EUR2024")), ("Acct Custodian", ("SCHWAB01", "FIDELITY1")),
)
POSITIVES = (
    ("Acct", ("A1B2C3D4", "E5F6G7H8")), ("Account Number", ("12345678", "87654321")), ("Accnt", ("AC123456", "AC654321")),
    ("Acct Alias", ("A1B2C3D4", "E5F6G7H8")), ("Primary Acct", ("A1B2C3D4", "E5F6G7H8")),
)
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
    spec = importlib.util.spec_from_file_location("ar21_template_reader", str(root / INTAKE / "template_reader.py"))
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(root / INTAKE))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def wide_of(header, values):
    return [("C", 1, header)] + [("C", i + 2, v) for i, v in enumerate(values)]


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print("usage: ar21_checks.py <%s> --root <worktree>" % "|".join(TOKENS))
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y221-allowlist":
        reader = reader_module(root)
        for header, values in NEGATIVES:
            got = reader._several_accounts(wide_of(header, values))
            if got:
                problems.append("a one-account file is turned back: header %r values %r -> %r" % (header, values, got))
        for header, values in POSITIVES:
            if not reader._several_accounts(wide_of(header, values)):
                problems.append("a two-account file is NOT turned back: header %r values %r" % (header, values))
        path = root / INTAKE / "tests" / "test_account_value_backstop.py"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for name in BACKSTOP_TESTS:
            if ("def %s(" % name) not in text:
                problems.append("the test %s is absent" % name)
        rc, passed, failed = pytest(root, "tests/test_account_value_backstop.py", INTAKE)
        print("negatives %d, positives %d; backstop tests: %d passed, %d failed (rc=%d)" % (len(NEGATIVES), len(POSITIVES), passed, failed, rc))
        if rc != 0 or failed or passed < len(BACKSTOP_TESTS):
            problems.append("the named backstop tests must all pass")
    elif check == "y221-keep":
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 364:
            problems.append("the intake folder must pass with at least 364 (the r19.2 count)")
        version = getattr(reader_module(root), "READER_VERSION", None)
        print("READER_VERSION = %s" % version)
        if not version or version == ROUND192_VERSION:
            problems.append("READER_VERSION must change in the same commit as what the reader returns (still %r)" % version)
    elif check == "y222-verify":
        rec = load(root, D % "68" + "CI_VERIFY_FIX.json", problems)
        if rec:
            for member in ("repro", "fix", "arms", "shell_syntax_ok", "tests", "scratch_arm_design", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            arms = {a.get("arm"): a for a in rec.get("arms") or []}
            ok = arms.get("landed_upload_verifies")
            bad = arms.get("head_object_fails")
            if not ok or ok.get("exit_code") != 0 or ok.get("map_updated") is not True:
                problems.append("arm landed_upload_verifies must exit 0 with the map updated (%r)" % ok)
            if not bad or bad.get("exit_code") in (0, None) or bad.get("cli_error_printed") is not True or bad.get("map_updated") is not False:
                problems.append("arm head_object_fails must exit non-zero, print the CLI's error and leave the map untouched (%r)" % bad)
            repro = rec.get("repro") or {}
            if not repro.get("cli_error_text"):
                problems.append("repro.cli_error_text must name the error the old verify call hit")
            if rec.get("shell_syntax_ok") is not True:
                problems.append("shell_syntax_ok must be true (bash -n on the script)")
            tests = rec.get("tests") or {}
            if tests.get("failed") not in (0, "0") or not tests.get("passed"):
                problems.append("the verify tests must pass (%r)" % tests)
            print("arms %s" % sorted(arms))
    elif check == "y223-design":
        rec = load(root, D % "69" + "EXERCISE_DESIGN.json", problems)
        if rec:
            for member in ("route", "precedent", "identities", "offline_run", "log", "removal", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            ids = {i.get("name"): i for i in rec.get("identities") or []}
            want = {"disabled": ("refused", "row_non_active"), "norow": ("refused", "row_absent"), "active": ("admitted", "row_present")}
            runs = {r.get("name"): r for r in (rec.get("offline_run") or {}).get("results") or []}
            for name, (outcome, klass) in want.items():
                i = ids.get(name)
                if not i:
                    problems.append("no identity %s" % name)
                    continue
                exp = i.get("expected") or {}
                if exp.get("outcome") != outcome or exp.get("class") != klass:
                    problems.append("identity %s: expected must be outcome %s and class %s (%r)" % (name, outcome, klass, exp))
                if i.get("selected_firm") in (None, "", i.get("home_firm")):
                    problems.append("identity %s must select a firm other than its own" % name)
                r = runs.get(name)
                if not r or r.get("outcome") != outcome or r.get("class") != klass:
                    problems.append("the offline run of %s does not give outcome %s and class %s (%r)" % (name, outcome, klass, r))
            if not (rec.get("log") or {}).get("group"):
                problems.append("log.group must name the log group the lines are counted in")
            if not (rec.get("removal") or {}).get("method"):
                problems.append("removal.method must say how the rows are removed and read ABSENT")
            print("identities %d, offline results %d" % (len(ids), len(runs)))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
