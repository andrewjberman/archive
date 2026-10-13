"""ar20_checks.py -- the mechanical checks of IRPT_ANLREQ round 20, workstream Y.

Usage:  python ar20_checks.py <check> --root <worker worktree root>

  y211-repair   AR-y-211: the r19.1 account-header backstop no longer turns back a one-account file whose ABBREVIATED-root attribute header
                (Acct Market Value, Acct CUSIP, Acct Lot, ...) holds distinct identifier-like or 8+-digit values, and the five named
                backstop tests still pass                                                                                 -> Y211-REPAIR-OK
  y211-keep     AR-y-211: the whole intake test folder passes (floor 347) and READER_VERSION differs from r19.1              -> Y211-KEEP-OK
  y212-rebase   AR-y-212: the status-rule release rebased on the LIVE packages of pin group A (performance-adapter, narrative, status)
                                                                                                                           -> Y212-REBASE-OK
  y213-rebase   AR-y-213: the same for pin group B (directory-search, ycharts-generate, export-render, holdings, 49f-reporting-read-lambda)
                                                                                                                           -> Y213-REBASE-OK
  y216-expect   AR-y-216 (workstream YR): the expectations of the three function suites (narrative, directory-search, export-render) that encode the
                pre-rule binding moved to the status rule, test files only, no test removed                              -> Y216-EXPECT-OK
  y217-status   AR-y-217 (workstream YR): irpt-status released with served.py AND the current ops/status.py (the 24 correction words), on the live package,
                the status.py difference being words only                                                              -> Y217-STATUS-OK
  y214-portal   AR-y-214: the portal candidate that shows the SHEETS_NOT_READ notice on the upload answer's face              -> Y214-PORTAL-OK

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
D = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~%s/r20/"
ROUND19_VERSION = "irpt-template-reader.r19.1"
TOKENS = {"y211-repair": "Y211-REPAIR", "y211-keep": "Y211-KEEP", "y212-rebase": "Y212-REBASE", "y213-rebase": "Y213-REBASE", "y214-portal": "Y214-PORTAL", "y216-expect": "Y216-EXPECT", "y217-status": "Y217-STATUS"}
GROUPS = {"y212-rebase": ("61", "STATUS_RULE_REBASE_GROUP_A.json", ("irpt-performance-adapter", "irpt-narrative", "irpt-status")),
          "y213-rebase": ("64", "STATUS_RULE_REBASE_GROUP_B.json",
                          ("irpt-directory-search", "irpt-ycharts-generate", "irpt-export-render", "irpt-holdings", "irpt-49f-reporting-read-lambda"))}
NEGATIVES = (
    ("Acct Market Value", ("25000000", "31000000")),
    ("Acct CUSIP", ("912828ZT6", "38141G104")),
    ("Acct Lot", ("LOT1234", "LOT5678")),
    ("Accnt Value", ("12000000", "15000000")),
    ("Acct Status", ("AX1234", "BX5678")),
    ("Acct Type", ("IRA1234", "ROTH5678")),
    ("Acct Name", ("ACME-401K", "ACME-403B")),
    ("Acct Holder", ("SMITH2024", "JONES2023")),
    ("Acct Balance", ("10000000", "12000000")),
    ("Acct Opened", ("20200101", "20210202")),
)
POSITIVES = (
    ("Acct", ("A1B2C3D4", "E5F6G7H8")),
    ("Account Number", ("12345678", "87654321")),
    ("Accnt", ("AC123456", "AC654321")),
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
    spec = importlib.util.spec_from_file_location("ar20_template_reader", str(root / INTAKE / "template_reader.py"))
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
        print("usage: ar20_checks.py <%s> --root <worktree>" % "|".join(TOKENS))
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y211-repair":
        reader = reader_module(root)
        for header, values in NEGATIVES:
            got = reader._several_accounts(wide_of(header, values))
            if got:
                problems.append("a one-account file is turned back: header %r values %r -> %r" % (header, values, got))
        for header, values in POSITIVES:
            got = reader._several_accounts(wide_of(header, values))
            if not got:
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
    elif check == "y211-keep":
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 347:
            problems.append("the intake folder must pass with at least 347 (the r19.1 count)")
        version = getattr(reader_module(root), "READER_VERSION", None)
        print("READER_VERSION = %s" % version)
        if not version or version == ROUND19_VERSION:
            problems.append("READER_VERSION must change in the same commit as what the reader returns (still %r)" % version)
    elif check in GROUPS:
        slot, fname, functions = GROUPS[check]
        rec = load(root, D % slot + fname, problems)
        if rec:
            for member in ("served_pin", "functions", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get("served_pin", ""))):
                problems.append("served_pin must be a full commit sha")
            rows = {f.get("function"): f for f in rec.get("functions") or []}
            for fn in functions:
                f = rows.get(fn)
                if not f:
                    problems.append("no row for %s" % fn)
                    continue
                for member in ("live_code_sha256", "live_member_manifest", "base_commit", "holds_only_control", "release", "carries_status_rule", "tests"):
                    if member not in f:
                        problems.append("%s lacks %r" % (fn, member))
                live = f.get("live_member_manifest") or {}
                control = f.get("holds_only_control") or {}
                if control.get("code_sha256") != f.get("live_code_sha256"):
                    problems.append("%s: the holds-only control does not reproduce the live CodeSha256 (%r against %r)" % (fn, control.get("code_sha256"), f.get("live_code_sha256")))
                rel = (f.get("release") or {}).get("member_manifest") or {}
                if len(live) < 5 or len(rel) < 5:
                    problems.append("%s: both manifests must map the package members to sha256" % fn)
                else:
                    differ = sorted(k for k in set(live) | set(rel) if live.get(k) != rel.get(k))
                    moved = {m.get("member"): m for m in f.get("must_move_with") or []}
                    extra = [k for k in differ if k != "served.py" and not (moved.get(k) or {}).get("reason")]
                    if "served.py" not in differ or extra:
                        problems.append("%s: the release must differ from the live package in served.py (and only members named in must_move_with with a reason); differs in %s" % (fn, differ))
                if f.get("carries_status_rule") is not True:
                    problems.append("%s: the release's served.py must carry the status rule" % fn)
                tests = f.get("tests") or {}
                if tests.get("failed") not in (0, "0"):
                    # AMENDMENT 1 (issuer): a failure that ALSO fails with the original bytes is pre-existing and does not count against the release;
                    # it must be named (failed_names) and shown failing in the control run (control_failed_names).
                    names, control = set(tests.get("failed_names") or []), set(tests.get("control_failed_names") or [])
                    if not names or not names <= control or tests.get("failed") != len(names):
                        problems.append("%s: the function's own tests must pass against the release except failures that also fail with the original bytes (passed %r failed %r)" % (fn, tests.get("passed"), tests.get("failed")))
                elif not tests.get("passed"):
                    problems.append("%s: the function's own tests ran no passing test (%r)" % (fn, tests))
                # AMENDMENT 2 (issuer, row W64-S6): collection or setup ERRORS count like failures; they pass only when the control run shows the same number
                if tests.get("errors") not in (0, "0", None) and tests.get("errors") != tests.get("control_errors"):
                    problems.append("%s: the function's own tests report %r errors against the release and %r with the original bytes" % (fn, tests.get("errors"), tests.get("control_errors")))
            print("functions in the record %d of %d" % (len([fn for fn in functions if fn in rows]), len(functions)))
    elif check == "y214-portal":
        rec = load(root, D % "63" + "PORTAL_NOTICE_CANDIDATE.json", problems)
        if rec:
            for member in ("dev_tip", "branch", "commit", "files_changed", "tests", "before_arm", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            for key in ("dev_tip", "commit"):
                if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get(key, ""))):
                    problems.append("%s is not a full commit sha" % key)
            if rec.get("commit"):
                got = subprocess.run(["git", "-C", str(root / "portal") if (root / "portal" / ".git").exists() else "C:/dev/ajb_workspace/portal", "cat-file", "-t", str(rec["commit"])],
                                     capture_output=True, text=True)
                if got.stdout.strip() != "commit":
                    problems.append("the portal commit %s is not in the portal repository" % rec.get("commit"))
            files = rec.get("files_changed") or []
            if not files or any(not str(x).startswith("src/") for x in files):
                problems.append("files_changed must be non-empty and under src/ only (got %r)" % files)
            tests = rec.get("tests") or {}
            if not tests.get("added") or tests.get("failed") not in (0, "0") or not tests.get("passed"):
                problems.append("the portal tests must add at least one test and all pass (%r)" % tests)
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: the new test must FAIL on the DEV tip without the change")
            print("files %d, tests %s" % (len(files), tests))
    elif check == "y216-expect":
        rec = load(root, D % "65" + "RULE_EXPECTATIONS.json", problems)
        if rec:
            for member in ("suites", "authz_tests", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            want = {"narrative": "narrative/tests", "directory-search": "directory/tests", "export-render": "export/tests"}
            rows = {s.get("suite"): s for s in rec.get("suites") or []}
            for name, folder in want.items():
                s = rows.get(name)
                if not s:
                    problems.append("no row for the suite %s" % name)
                    continue
                for member in ("files_changed", "tests_edited", "before", "after", "control_failed_names", "collected_before", "collected_after"):
                    if member not in s:
                        problems.append("%s lacks %r" % (name, member))
                for path in s.get("files_changed") or []:
                    if not str(path).startswith(IR + "/" + folder + "/"):
                        problems.append("%s: %s is outside the suite's tests folder" % (name, path))
                if not s.get("files_changed") or not s.get("tests_edited"):
                    problems.append("%s: no test file or no edited test is named" % name)
                for e in s.get("tests_edited") or []:
                    if e.get("how") not in ("expectation", "fixture") or not e.get("why"):
                        problems.append("%s: an edited test lacks how (expectation or fixture) or why: %r" % (name, e.get("name")))
                after = s.get("after") or {}
                if not set(after.get("failed_names") or []) <= set(s.get("control_failed_names") or []):
                    problems.append("%s: after the edit a test fails that does not also fail with the original bytes" % name)
                if after.get("errors") not in (0, "0", None):
                    problems.append("%s: collection or setup errors remain (%r)" % (name, after.get("errors")))
                if (s.get("collected_after") or 0) < (s.get("collected_before") or 1):
                    problems.append("%s: fewer tests are collected after the edit (%r against %r): none may be removed" % (name, s.get("collected_after"), s.get("collected_before")))
            az = rec.get("authz_tests") or {}
            if az.get("failed") not in (0, "0") or not az.get("passed"):
                problems.append("the two _authz status tests must pass unchanged (%r)" % az)
            print("suites in the record %d of 3" % len([n for n in want if n in rows]))
    elif check == "y217-status":
        rec = load(root, D % "66" + "IRPT_STATUS_STATUS_PY_RELEASE.json", problems)
        if rec:
            for member in ("live_code_sha256", "live_member_manifest", "base_commit", "holds_only_control", "release", "status_py_pin",
                           "status_py_diff_words_only", "correction_words", "tests", "parity", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("holds_only_control") or {}).get("code_sha256") != rec.get("live_code_sha256"):
                problems.append("the holds-only control does not reproduce the live CodeSha256")
            live, rel = rec.get("live_member_manifest") or {}, (rec.get("release") or {}).get("member_manifest") or {}
            if len(live) < 5 or len(rel) < 5:
                problems.append("both manifests must map the package members to sha256")
            else:
                differ = sorted(k for k in set(live) | set(rel) if live.get(k) != rel.get(k))
                moved = {m.get("member"): m for m in rec.get("must_move_with") or []}
                extra = [k for k in differ if k not in ("served.py", "status.py") and not (moved.get(k) or {}).get("reason")]
                if "served.py" not in differ or "status.py" not in differ or extra:
                    problems.append("the release must differ from the live package in served.py and status.py (and members named in must_move_with with a reason); differs in %s" % differ)
            if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get("status_py_pin", ""))):
                problems.append("status_py_pin must be a full commit sha")
            if rec.get("status_py_diff_words_only") is not True:
                problems.append("status_py_diff_words_only must be true: the pinned and the released status.py differ in the CORRECTION_WORDS literal only")
            cw = rec.get("correction_words") or {}
            if not (isinstance(cw.get("after"), int) and isinstance(cw.get("before"), int) and cw["after"] - cw["before"] >= 24):
                problems.append("correction_words must show at least 24 more words after than before (%r)" % cw)
            tests = rec.get("tests") or {}
            if tests.get("failed") not in (0, "0"):
                names, control = set(tests.get("failed_names") or []), set(tests.get("control_failed_names") or [])
                if not names or not names <= control or tests.get("failed") != len(names):
                    problems.append("the ops tests must pass against the release except failures that also fail with the original bytes (%r)" % tests)
            elif not tests.get("passed"):
                problems.append("the ops tests ran no passing test")
            if (rec.get("parity") or {}).get("passed") is not True:
                problems.append("the correction-words parity test (uploads against status) must pass against the release members")
            print("differs from live: %s" % (differ if len(live) >= 5 and len(rel) >= 5 else "?"))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
