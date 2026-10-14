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
D22 = D.replace("/r21/", "/r22/")
D23 = D.replace("/r21/", "/r23/")
D24 = D23
D26 = D23
ROUND192_VERSION = "irpt-template-reader.r19.2"
TOKENS = {"y221-allowlist": "Y221-ALLOWLIST", "y221-keep": "Y221-KEEP", "y222-verify": "Y222-VERIFY", "y223-design": "Y223-DESIGN",
          "y226-effect": "Y226-EFFECT", "y227-resident": "Y227-RESIDENT", "y228-lambda": "Y228-LAMBDA", "y229-stderr": "Y229-STDERR",
          "y242-portal": "Y242-PORTAL", "y243-portal": "Y243-PORTAL", "y244-read": "Y244-READ", "y245-server": "Y245-SERVER",
          "y246-qa": "Y246-QA", "y247-swap": "Y247-SWAP", "y248-portal": "Y248-PORTAL",
          "y249-swap": "Y249-SWAP", "y250-qa": "Y250-QA", "y251-swap": "Y251-SWAP", "y252-portal": "Y252-PORTAL",
          "y261-read": "Y261-READ", "y262-portal": "Y262-PORTAL", "y263-portal": "Y263-PORTAL", "y264-portal": "Y264-PORTAL", "y265-portal": "Y265-PORTAL", "y266-live": "Y266-LIVE",
          "y271-j2": "Y271-J2", "y272-j5": "Y272-J5", "y273-portal": "Y273-PORTAL", "y274-portal": "Y274-PORTAL", "y275-portal": "Y275-PORTAL",
          "y276-design": "Y276-DESIGN", "y277-revert": "Y277-REVERT", "y278-read": "Y278-READ",
          "y279-portal": "Y279-PORTAL", "y280-submit": "Y280-SUBMIT", "y281-list": "Y281-LIST", "y282-portal": "Y282-PORTAL", "y283-portal": "Y283-PORTAL",
          "y291-known": "Y291-KNOWN", "y292-checker": "Y292-CHECKER", "y293-kept": "Y293-KEPT",
          "y284-pkg-server": "Y284-PKG-SERVER", "y285-pkg-sender": "Y285-PKG-SENDER", "y294-stack": "Y294-STACK", "y295-census": "Y295-CENSUS", "y296-armed": "Y296-ARMED", "y297-build": "Y297-BUILD", "y298-build": "Y298-BUILD", "y299-build": "Y299-BUILD", "y300-build": "Y300-BUILD", "y301-scripts": "Y301-SCRIPTS", "y306-ordinary": "Y306-ORDINARY", "y308-words": "Y308-WORDS", "y309-build": "Y309-BUILD", "y310-build": "Y310-BUILD", "y311-build": "Y311-BUILD", "y320-build": "Y320-BUILD", "y323-build": "Y323-BUILD", "y324-build": "Y324-BUILD"}
READER_R181_SHA = "83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58"
UPLOADS_SHA = "176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea"
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


def portal_candidate(root, rel, problems):
    """A portal candidate record: a full portal commit under src/ only, added tests that fail on the DEV tip without the change and pass with it."""
    rec = load(root, rel, problems)
    if not rec:
        return None
    for member in ("dev_tip", "branch", "commit", "files_changed", "tests", "before_arm", "what_a_person_sees", "claim", "not_read"):
        if member not in rec:
            problems.append("the record lacks %r" % member)
    for key in ("dev_tip", "commit"):
        if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get(key, ""))):
            problems.append("%s is not a full commit sha" % key)
    if rec.get("commit"):
        got = subprocess.run(["git", "-C", "C:/dev/ajb_workspace/portal", "cat-file", "-t", str(rec["commit"])], capture_output=True, text=True)
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
    return rec


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
    elif check == "y226-effect":
        rec = load(root, D % "70" + "REOPEN_AND_EFFECT.json", problems)
        if rec:
            for member in ("pinned", "moved", "reopen_matrix", "effect_table", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("pinned") or {}).get("template_reader_sha256") != READER_R181_SHA:
                problems.append("pinned.template_reader_sha256 must be the live r18.1 reader (%s)" % READER_R181_SHA[:12])
            if (rec.get("pinned") or {}).get("uploads_sha256") != UPLOADS_SHA or (rec.get("moved") or {}).get("uploads_sha256") != UPLOADS_SHA:
                problems.append("uploads.py must be the same bytes on both sides (%s)" % UPLOADS_SHA[:12])
            moved_version = (rec.get("moved") or {}).get("reader_version")
            if moved_version != "irpt-template-reader.r19.3":
                problems.append("moved.reader_version must read irpt-template-reader.r19.3 (got %r)" % moved_version)
            cells = {(c.get("stored_by"), c.get("reopened_by")): c for c in rec.get("reopen_matrix") or []}
            for key in (("pinned", "pinned"), ("pinned", "moved"), ("moved", "pinned"), ("moved", "moved")):
                c = cells.get(key)
                if not c or not isinstance(c.get("cases"), int) or c.get("cases") < 1 or c.get("accepted", -1) + c.get("refused", -1) != c.get("cases"):
                    problems.append("reopen_matrix cell %s must give cases = accepted + refused (%r)" % (key, c))
            if cells.get(("pinned", "moved")) and cells[("pinned", "moved")].get("refused") != 0:
                problems.append("an input the PINNED pair stored must be accepted by the MOVED pair (the order of the legs rests on it)")
            rows = {str(r.get("header")): r for r in rec.get("effect_table") or []}
            for header, _values in NEGATIVES:
                r = rows.get(header)
                if not r or "NORMALIZED" not in str(r.get("after")):
                    problems.append("one-account header %r must read NORMALIZED after the move (%r)" % (header, r and r.get("after")))
            for header, _values in POSITIVES:
                r = rows.get(header)
                if not r or "ACCOUNT_COLUMN_SEVERAL_VALUES" not in str(r.get("after")):
                    problems.append("two-account header %r must read ACCOUNT_COLUMN_SEVERAL_VALUES after the move (%r)" % (header, r and r.get("after")))
            print("matrix cells %d, effect rows %d" % (len(cells), len(rows)))
    elif check == "y227-resident":
        rec = load(root, D % "71" + "RESIDENT_ONE_MEMBER_RELEASE.json", problems)
        if rec:
            for member in ("base_tarball", "delta_vs_r19_tarball", "tarball", "root_naming", "host_script", "tests", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("base_tarball") or {}).get("sha256") != "84df6479655c07ae6000af40404e53eb056b4c403aa9134bbe9c1521317d497a":
                problems.append("base_tarball.sha256 must be the release-19 tarball (84df6479...)")
            delta = rec.get("delta_vs_r19_tarball") or {}
            names = sorted(str(r.get("member") if isinstance(r, dict) else r).rsplit("/", 1)[-1] for r in delta.get("differing") or [])
            if names != ["SHA256SUMS", "resident_bindings.json", "template_reader.py"]:
                problems.append("the release must differ from the release-19 tarball in exactly template_reader.py, resident_bindings.json and SHA256SUMS (differs in %s)" % names)
            if delta.get("only_in_old") or delta.get("only_in_new"):
                problems.append("the release must add and remove no member (only_in_old %r, only_in_new %r)" % (delta.get("only_in_old"), delta.get("only_in_new")))
            tar = rec.get("tarball") or {}
            if not re.fullmatch(r"[0-9a-f]{64}", str(tar.get("sha256", ""))):
                problems.append("tarball.sha256 must be a 64-hex digest")
            if not (rec.get("host_script") or {}).get("sha256"):
                problems.append("host_script must carry its sha256")
            tests = rec.get("tests") or {}
            accepted = ("test_the_readers_output_on_the_fixtures_is_pinned_to_its_version", "test_correction_words_are_the_envelopes_words")
            explained = [str(x) for x in tests.get("failures_explained") or []]
            if tests.get("failed") not in (0, "0"):
                ok = (isinstance(tests.get("failed"), int) and tests.get("failed") == len(explained)
                      and all(any(e.find(name) >= 0 for name in accepted) for e in explained))
                if not ok:
                    problems.append("the reader's tests must pass on the build except the two CTO-accepted, explained failures (failed=%r)" % tests.get("failed"))
            print("differing %s; tests passed %s failed %s" % (names, tests.get("passed"), tests.get("failed")))
    elif check == "y228-lambda":
        rec = load(root, D % "72" + "LAMBDA_LEG_R193.json", problems)
        if rec:
            for member in ("live_read", "release_build", "differ_from_live", "holds_only_control", "patch", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            live = rec.get("live_read") or {}
            if not live.get("code_sha256") or not live.get("read_at") or not live.get("member_manifest"):
                problems.append("live_read needs code_sha256, read_at and member_manifest (read from AWS in the run)")
            lman = live.get("member_manifest") or {}
            rman = (rec.get("release_build") or {}).get("member_manifest") or {}
            if len(lman) < 20 or len(rman) < 20:
                problems.append("both manifests must map at least 20 members to their sha256 (live %d, release %d)" % (len(lman), len(rman)))
            else:
                differ = sorted(k for k in set(lman) | set(rman) if lman.get(k) != rman.get(k))
                if differ != ["template_reader.py"]:
                    problems.append("the release package must differ from the live package in exactly template_reader.py (differs in %s)" % differ)
                if sorted(rec.get("differ_from_live") or []) != differ:
                    problems.append("differ_from_live does not equal the manifests' difference")
            ctl = rec.get("holds_only_control") or {}
            if ctl.get("code_sha256") != live.get("code_sha256") or ctl.get("differs_from_live") != []:
                problems.append("the control build (no reader move) must reproduce the live CodeSha256 and differ in no member (%r)" % ctl)
            if not (rec.get("release_build") or {}).get("code_sha256_base64"):
                problems.append("release_build.code_sha256_base64 must carry the expected CodeSha256")
            print("live members %d, release members %d" % (len(lman), len(rman)))
    elif check == "y229-stderr":
        script = root / "infra/aws/lambda/ci/build-and-upload.sh"
        text = script.read_text(encoding="utf-8") if script.is_file() else ""
        merged = [ln.strip() for ln in text.splitlines() if "head-object" in ln and "2>&1" in ln]
        merged += [ln.strip() for ln in text.splitlines() if re.search(r"--query\s+'(ContentLength|Metadata\.\"content-sha256\")'.*2>&1", ln)]
        if merged:
            problems.append("a head-object value still merges stderr into stdout: %r" % merged[:3])
        got = subprocess.run(["bash", "infra/aws/lambda/ci/tests/test_build_and_upload_verify.sh"], cwd=str(root),
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (got.stdout or "") + (got.stderr or "")
        print("verify tests rc=%d" % got.returncode)
        for arm in ("landed_upload_verifies", "head_object_fails", "stderr_warning_ignored", "mutant"):
            if not re.search(r"^PASS %s" % arm, out, re.M):
                problems.append("the test arm %s did not print PASS" % arm)
        if got.returncode != 0 or "ALL PASS" not in out:
            problems.append("the verify tests must exit 0 and print ALL PASS")
    elif check == "y242-portal":
        # AMENDMENT 1 (the state line): the continuation worker could not commit under ~74's folder (lane gate, row W78-S3), so the
        # issuer attached the amended record under its own deliverables; when it is present it is the record the check reads.
        amend = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/r22/PORTAL_FILE_NAME_CANDIDATE_AMEND1.json"
        rec242 = amend if (root / amend).is_file() else D22 % "74" + "PORTAL_FILE_NAME_CANDIDATE.json"
        portal_candidate(root, rec242, problems)
    elif check == "y243-portal":
        rec = portal_candidate(root, D22 % "75" + "PORTAL_PRICE_DATE_CANDIDATE.json", problems)
        if rec and not (rec.get("server_reads") or {}).get("what_the_server_does_without_a_price_date"):
            problems.append("server_reads.what_the_server_does_without_a_price_date must say what the serving path does when no date is sent")
    elif check == "y244-read":
        rec = load(root, D22 % "76" + "PROXY_SUGGESTION_READ.json", problems)
        if rec:
            for member in ("where_suggestion_comes_from", "why_timxx_got_none", "options", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            opts = rec.get("options") or []
            if len(opts) < 2 or any(not o.get("source") or not o.get("cost") for o in opts):
                problems.append("options needs at least two sources of a similar security, each with its source and cost")
            print("options %d" % len(opts))
    elif check == "y245-server":
        rec = load(root, D22 % "77" + "PRICE_DATE_DEFAULT.json", problems)
        if rec:
            for member in ("trading_day_source", "packaging", "behaviour", "tests", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            pack = rec.get("packaging") or {}
            for where in ("ycharts_generate", "resident"):
                if where not in pack:
                    problems.append("packaging must say whether %s can carry the calendar source" % where)
        test = root / INTAKE / "tests" / "test_price_date_default.py"
        if not test.is_file():
            problems.append("no intake/tests/test_price_date_default.py")
        else:
            rc, passed, failed = pytest(root, "tests/test_price_date_default.py", INTAKE)
            print("new test file: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < 3:
                problems.append("the new test file must pass with at least 3 tests")
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 365:
            problems.append("the intake folder must pass with at least 365 (the r19.3 count)")
    elif check == "y246-qa":
        rec = load(root, D22 % "79" + "KIMI_QA_HARNESS.json", problems)
        if rec:
            for member in ("gate", "harness", "tests", "live_qa", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            harness = rec.get("harness") or {}
            if not re.fullmatch(r"[0-9a-f]{64}", str(harness.get("sha256", ""))) or len(harness.get("cases") or []) < 6:
                problems.append("harness needs a 64-hex sha256 and at least 6 cases")
            tests = rec.get("tests") or {}
            if not tests.get("added") or tests.get("failed") not in (0, "0") or not tests.get("passed"):
                problems.append("the harness tests must be added and all pass (%r)" % tests)
        path = root / "infra/aws/lambda/investor-reporting/ycharts/generate/kimi_search_qa.py"
        if not path.is_file():
            problems.append("no ycharts/generate/kimi_search_qa.py")
        else:
            rc, passed, failed = pytest(root, "tests/test_kimi_search_qa.py", IR + "/ycharts/generate")
            print("qa tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < 5:
                problems.append("tests/test_kimi_search_qa.py must pass with at least 5 tests")
    elif check == "y247-swap":
        rec = load(root, D22 % "80" + "SWAP_SUGGESTIONS.json", problems)
        if rec:
            for member in ("where_wired", "how_the_capability_would_arrive", "behaviour", "wire_shape", "tests", "before_arm", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: case (b) must FAIL at HEAD without the change")
        rc, passed, failed = pytest(root, "tests/test_swap_suggestions.py", IR + "/ycharts/generate")
        print("swap tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 6:
            problems.append("tests/test_swap_suggestions.py must pass with at least 6 tests")
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 365:
            problems.append("the intake folder must pass with at least 365")
    elif check == "y248-portal":
        portal_candidate(root, D22 % "81" + "PORTAL_SUGGESTED_SWAPS_CANDIDATE.json", problems)
    elif check == "y249-swap":
        rec = load(root, D22 % "82" + "SWAP_FROM_SEARCH.json", problems)
        if rec:
            for member in ("read", "transport", "advisory", "tests", "before_arm", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
        for rel, cwd, floor in (("tests/test_swap_from_search.py", INTAKE, 10), ("tests/test_kimi_search_port.py", IR + "/ycharts/generate", 5)):
            if not (root / cwd / rel).is_file():
                problems.append("no %s/%s" % (cwd, rel))
                continue
            rc, passed, failed = pytest(root, rel, cwd)
            print("%s: %d passed, %d failed (rc=%d)" % (rel, passed, failed, rc))
            if rc != 0 or failed or passed < floor:
                problems.append("%s must pass with at least %d tests" % (rel, floor))
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 365:
            problems.append("the intake folder must pass with at least 365")
        text = (root / IR / "intake/resolution_kimi.py").read_text(encoding="utf-8") if (root / IR / "intake/resolution_kimi.py").is_file() else ""
        if "request_fields" in text and "REFUSED" not in text.upper() and "refuse" not in text.lower():
            problems.append("resolution_kimi.py still reads request_fields without refusing the old capability shape")
    elif check == "y250-qa":
        rec = load(root, D22 % "83" + "KIMI_SEARCH_QA_HARNESS.json", problems)
        if rec:
            for member in ("read", "harness", "tests", "live_qa", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            harness = rec.get("harness") or {}
            cases = harness.get("cases") or []
            if not re.fullmatch(r"[0-9a-f]{64}", str(harness.get("sha256", ""))) or len(cases) < 8:
                problems.append("harness needs a 64-hex sha256 and at least 8 cases (TIMXX, 4 funds, a nonsense symbol, 2 injection strings)")
            if not any("TIMXX" in json.dumps(c) for c in cases):
                problems.append("the fixed case list must hold TIMXX")
        path = root / IR / "ycharts/generate/kimi_search_qa.py"
        if not path.is_file():
            problems.append("no ycharts/generate/kimi_search_qa.py")
        else:
            rc, passed, failed = pytest(root, "tests/test_kimi_search_qa.py", IR + "/ycharts/generate")
            print("qa tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < 7:
                problems.append("tests/test_kimi_search_qa.py must pass with at least 7 tests")
    elif check == "y251-swap":
        rec = load(root, D22 % "84" + "SWAP_SUGGESTIONS_R2.json", problems)
        if rec:
            for member in ("where_wired", "capability_carrier", "behaviour", "wire_shape", "tests", "before_arm", "release_size", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: case (b) must FAIL at HEAD without the change")
        rc, passed, failed = pytest(root, "tests/test_swap_suggestions.py", IR + "/ycharts/generate")
        print("swap tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 7:
            problems.append("tests/test_swap_suggestions.py must pass with at least 7 tests")
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 365:
            problems.append("the intake folder must pass with at least 365")
    elif check == "y252-portal":
        portal_candidate(root, D22 % "85" + "PORTAL_PROXY_PLACEHOLDER_CANDIDATE.json", problems)
    elif check == "y261-read":
        rec = load(root, D22 % "86" + "ULTRA_SHORT_TERM_READ.json", problems)
        if rec:
            for member in ("server", "models_in_the_estate", "why_missing", "canonical_order", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            why = rec.get("why_missing") or {}
            for member in ("verdict", "evidence", "fix", "risk"):
                if not why.get(member):
                    problems.append("why_missing.%s must be stated" % member)
            if not (rec.get("server") or {}).get("catalogue_source"):
                problems.append("server.catalogue_source must name where the catalogue is sourced")
            print("verdict: %s" % str(why.get("verdict"))[:80])
    elif check == "y262-portal":
        rec = portal_candidate(root, D22 % "87" + "PORTAL_FORM_ORDER_COLOR_CANDIDATE.json", problems)
        if rec and not (rec.get("reuse") or {}).get("color_function"):
            problems.append("reuse.color_function must name the estate's color function (file:line)")
    elif check == "y263-portal":
        rec = portal_candidate(root, D22 % "88" + "PORTAL_FORM_NO_FEE_CANDIDATE.json", problems)
        if rec and not (rec.get("server_reads") or {}).get("default_when_absent"):
            problems.append("server_reads.default_when_absent must say what the ticket service does without a fee")
    elif check == "y264-portal":
        rec = portal_candidate(root, D22 % "89" + "PORTAL_FORM_COMMENTARY_CANDIDATE.json", problems)
        if rec and not (rec.get("trace") or {}).get("where_it_breaks"):
            problems.append("trace.where_it_breaks must name the first hop where a checked box stops reaching commentary_requested")
    elif check == "y265-portal":
        rec = portal_candidate(root, D22 % "90" + "PORTAL_SUBMIT_SILENCE_CANDIDATE.json", problems)
        if rec:
            trace = rec.get("trace") or {}
            if not trace.get("silent_exits") or not trace.get("where_it_stops"):
                problems.append("trace must list every silent exit (file:line) and where the submit stops")
            if not rec.get("reproduction"):
                problems.append("reproduction must say which hops end with no message on screen (RUN, with test names)")
    elif check == "y266-live":
        rec = load(root, D22 % "91" + "KIMI_SEARCH_QA_LIVE_RUNNER.json", problems)
        if rec:
            for member in ("read", "runner", "tests", "before_arm", "runbook", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not re.fullmatch(r"[0-9a-f]{64}", str((rec.get("runner") or {}).get("sha256", ""))):
                problems.append("runner.sha256 must be a 64-hex digest")
        path = root / IR / "ycharts/generate/kimi_search_qa_live.py"
        if not path.is_file():
            problems.append("no ycharts/generate/kimi_search_qa_live.py")
        else:
            rc, passed, failed = pytest(root, "tests/test_kimi_search_qa_live.py", IR + "/ycharts/generate")
            print("live runner tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < 6:
                problems.append("tests/test_kimi_search_qa_live.py must pass with at least 6 tests")
    elif check in ("y271-j2", "y272-j5"):
        name, members, worker, rel = (("J2", ("trace", "options", "chosen", "authorization_change", "tests", "claim", "not_read"), "92", "J2_REQUEST_ID.json")
                                      if check == "y271-j2" else
                                      ("J5", ("trace", "chosen_principal", "order_rule", "authorization_change", "tests", "claim", "not_read"), "93", "J5_PACKAGER.json"))
        rec = load(root, D23 % worker + rel, problems)
        if rec:
            for member in members:
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not (rec.get("authorization_change") or "").strip():
                problems.append("authorization_change must state in a paragraph who may now write what (or that nothing widens)")
            built = rec.get("built")
            if built and (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: the new tests must FAIL at HEAD without the change")
            print("%s: built=%s" % (name, bool(built)))
    elif check == "y273-portal":
        rec = portal_candidate(root, D23 % "94" + "J6_FORM_ATTACHMENT.json", problems)
        if rec and not rec.get("chosen"):
            problems.append("chosen must name the design of the fourth item")
    elif check == "y274-portal":
        rec = portal_candidate(root, D23 % "95" + "PORTAL_C_FIRM_CANDIDATE.json", problems)
        if rec and not (rec.get("read") or {}).get("firm_source"):
            problems.append("read.firm_source must name where the firm comes from (file:line)")
    elif check == "y275-portal":
        rec = portal_candidate(root, D23 % "96" + "PORTAL_VARIANT_CANDIDATE.json", problems)
        if rec and not (rec.get("read") or {}).get("receiver_member"):
            problems.append("read.receiver_member must name the member the receiver reads for the variant")
    elif check == "y276-design":
        rec = load(root, D23 % "97" + "SYNTHETIC_ADVISOR_DESIGN.json", problems)
        if rec:
            for member in ("read", "identity", "drive", "offline_run", "removal", "bounds", "blast_radius", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            drive = rec.get("drive")
            if not isinstance(drive, list) or len(drive) < 5:
                problems.append("drive must list the ordered calls from Submit to the package (at least 5)")
            print("drive calls: %s" % (len(drive) if isinstance(drive, list) else drive))
    elif check == "y277-revert":
        rec = load(root, D23 % "98" + "KIMI_SWAP_REVERT.json", problems)
        base = "6bca581cd1"
        restored = ("intake/resolution_kimi.py", "intake/tests/test_resolution_kimi.py", "ycharts/generate/kimi_port.py", "intake/upload_suggestions.py", "ycharts/generate/resident_worker.py")
        removed = ("intake/tests/test_swap_from_search.py", "ycharts/generate/tests/test_kimi_search_port.py", "ycharts/generate/kimi_search_qa.py",
                   "ycharts/generate/tests/test_kimi_search_qa.py", "ycharts/generate/tests/test_swap_suggestions.py")
        for f in restored:
            got = subprocess.run(["git", "-C", str(root), "diff", "--quiet", base, "--", IR + "/" + f], capture_output=True)
            if got.returncode != 0:
                problems.append("%s is not equal to its content at %s" % (f, base))
        for f in removed:
            if (root / IR / f).exists():
                problems.append("%s still exists" % f)
        if rec:
            for member in ("restored", "removed", "guard", "tests", "commit", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed != 370:
            problems.append("the intake suite must read 370 passed (got %d)" % passed)
    elif check == "y278-read":
        rec = load(root, D23 % "99" + "C_SWAP_STEPS_1_2_READ.json", problems)
        if rec:
            for member in ("door", "estate", "design", "cells", "measurement", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not (rec.get("door") or {}).get("where_ticker_not_found_is_made"):
                problems.append("door.where_ticker_not_found_is_made must name file:line")
            if not rec.get("cells"):
                problems.append("cells must list the cells the design splits into")
    elif check == "y279-portal":
        portal_candidate(root, D23 % "100" + "PORTAL_COMMENTARY_ONLY_WHEN_TRUE_CANDIDATE.json", problems)
    elif check in ("y280-submit", "y281-list"):
        worker, rel, testfile, floor = (("101", "SUBMIT_ANALYSIS_REQUEST.json", "tests/test_submit_analysis_request.py", 12) if check == "y280-submit"
                                        else ("102", "LIST_SCOPED.json", "tests/test_list_scoped_firm.py", 10))
        if check == "y281-list" and (root / (D24 % "108" + rel)).is_file():
            worker = "108"  # the continuation worker's record (AMENDMENT 1); the first worker (102) stopped at the build gate
        if check == "y281-list" and (root / (D24 % "112" + rel)).is_file():
            worker = "112"  # AMENDMENT 3: the third worker, on a branch cut from the trunk (the ~108 branch could not merge: row-id collision)
        rec = load(root, D24 % worker + rel, problems)
        if rec:
            for member in ("read", "authorization_change", "tests", "before_arm", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not (rec.get("authorization_change") or "").strip():
                problems.append("authorization_change must state in a paragraph who may now do what")
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: the new tests must FAIL at HEAD without the change")
        tc = "infra/aws/lambda/ticket_center"
        if not (root / tc / testfile).is_file():
            problems.append("no %s/%s" % (tc, testfile))
        else:
            rc, passed, failed = pytest(root, testfile, tc)
            print("%s: %d passed, %d failed (rc=%d)" % (testfile, passed, failed, rc))
            if rc != 0 or failed or passed < floor:
                problems.append("%s must pass with at least %d tests" % (testfile, floor))
        rc, passed, failed = pytest(root, "tests", tc)
        print("ticket service folder: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 206:
            problems.append("the ticket service folder must pass with at least 206 tests")
    elif check == "y282-portal":
        rec = portal_candidate(root, D24 % "103" + "PORTAL_PARTNER_REACH_CANDIDATE.json", problems)
        if rec and not (rec.get("read") or {}).get("requiresDev_pattern"):
            problems.append("read.requiresDev_pattern must name the estate's existing DEV-only pattern")
    elif check == "y283-portal":
        rec = portal_candidate(root, D24 % "104" + "PORTAL_PARTNER_VIEW_CANDIDATE.json", problems)
        if rec and not (rec.get("read") or {}).get("how_filing_is_sent"):
            problems.append("read.how_filing_is_sent must name file:line")
    elif check in ("y291-known", "y292-checker", "y293-kept"):
        spec = {"y291-known": ("105", "KNOWN_REGISTRY_PORT.json", ("read", "port", "tests", "before_arm", "release_needs", "claim", "not_read"),
                               (("ycharts/generate", "tests/test_registry_identity_port.py", 8),)),
                "y292-checker": ("106", "YFINANCE_CHECKER.json", ("read", "module", "tests", "measurement", "release_needs", "claim", "not_read"),
                                 (("intake", "tests/test_yfinance_check.py", 12),)),
                "y293-kept": ("107", "KEPT_STATE.json", ("read", "state", "freeze_branch", "words", "tests", "before_arm", "shares_status", "claim", "not_read"),
                              (("intake", "tests/test_kept_holding.py", 14),))}[check]
        if check == "y293-kept" and (root / (D24 % "110" + spec[1])).is_file():
            spec = ("110",) + spec[1:]  # the continuation worker's record (AMENDMENT 1)
        rec = load(root, D24 % spec[0] + spec[1], problems)
        if rec:
            for member in spec[2]:
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if check != "y292-checker" and (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: the new test must FAIL at HEAD without the change")
            if check == "y292-checker" and not re.fullmatch(r"[0-9a-f]{64}", str((rec.get("module") or {}).get("sha256", ""))):
                problems.append("module.sha256 must be a 64-hex digest")
        for sub, rel, floor in spec[3]:
            cwd = IR + "/" + sub
            if not (root / cwd / rel).is_file():
                problems.append("no %s/%s" % (cwd, rel))
                continue
            rc, passed, failed = pytest(root, rel, cwd)
            print("%s: %d passed, %d failed (rc=%d)" % (rel, passed, failed, rc))
            if rc != 0 or failed or passed < floor:
                problems.append("%s must pass with at least %d tests" % (rel, floor))
        rc, passed, failed = pytest(root, "tests", INTAKE)
        print("intake tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 370:
            problems.append("the intake folder must pass with at least 370")
    elif check == "y284-pkg-server":
        rec = load(root, D26 % "108" + "PACKAGE_REQUEST_ID_SERVER.json", problems)
        if rec:
            for member in ("read", "built", "authorization_change", "tests", "before_arm", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not (rec.get("authorization_change") or "").strip():
                problems.append("authorization_change must state what the package principal may now write")
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: case (a) must FAIL at HEAD without the change")
        tc = "infra/aws/lambda/ticket_center"
        if not (root / tc / "tests/test_package_request_id.py").is_file():
            problems.append("no ticket_center/tests/test_package_request_id.py")
        else:
            rc, passed, failed = pytest(root, "tests/test_package_request_id.py", tc)
            print("package request id tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < 10:
                problems.append("tests/test_package_request_id.py must pass with at least 10 tests")
        rc, passed, failed = pytest(root, "tests", tc)
        print("ticket service folder: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
        if rc != 0 or failed or passed < 221:
            problems.append("the ticket service folder must pass with at least 221 tests")
    elif check == "y285-pkg-sender":
        rec = load(root, D26 % "109" + "PACKAGER_REQUEST_ID.json", problems)
        if rec:
            for member in ("read", "built", "tests", "before_arm", "release_needs", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: case (a) must FAIL at HEAD without the change")
        t = root / IR / "ycharts/research/tests/test_opal_packager_request_id.py"
        if not t.is_file():
            problems.append("no ycharts/research/tests/test_opal_packager_request_id.py")
        else:
            rc, passed, failed = pytest(root, "tests/test_opal_packager_request_id.py", IR + "/ycharts/research")
            print("packager request id tests: %d passed, %d failed (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed or passed < 6:
                problems.append("tests/test_opal_packager_request_id.py must pass with at least 6 tests")
    elif check == "y294-stack":
        rec = load(root, D26 % "111" + "PORTAL_PARTNER_STACK.json", problems)
        if rec:
            for member in ("prod_tip", "branch", "head", "merges", "after_each", "conflicts", "test_edits", "final_counts", "typecheck",
                           "what_a_person_sees", "route_gate", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            portal = "C:/dev/ajb_workspace/portal"

            def git(*args):
                return subprocess.run(["git", "-C", portal] + list(args), capture_output=True, text=True).stdout.strip()

            for key in ("prod_tip", "head"):
                if not re.fullmatch(r"[0-9a-f]{40}", str(rec.get(key, ""))):
                    problems.append("%s is not a full commit sha" % key)
            if rec.get("branch") != "cand/dell2/partner-firm-stack":
                problems.append("branch must be cand/dell2/partner-firm-stack")
            merges = rec.get("merges") or []
            want = ["794b7df4", "9ef6a359b8", "62d455f5", "6d117bfe85", "80d7c70a7d", "ab6ede6989", "e82daf4c98", "46a49e57e3"]
            if len(merges) != len(want):
                problems.append("merges must list the eight in order (got %d)" % len(merges))
            else:
                for m, w in zip(merges, want):
                    if not str(m.get("branch_tip", m.get("branch", ""))).startswith(w) and w not in json.dumps(m):
                        problems.append("merge order: expected %s at this position, got %r" % (w, m))
            if rec.get("head") and git("cat-file", "-t", rec["head"]) != "commit":
                problems.append("the head commit is not in the portal repository")
            elif rec.get("head"):
                if git("rev-parse", "cand/dell2/partner-firm-stack") != rec["head"]:
                    problems.append("the branch cand/dell2/partner-firm-stack is not at the recorded head")
                if rec.get("prod_tip") and subprocess.run(["git", "-C", portal, "merge-base", "--is-ancestor", rec["prod_tip"], rec["head"]]).returncode != 0:
                    problems.append("prod_tip is not an ancestor of head")
                if subprocess.run(["git", "-C", portal, "merge-base", "--is-ancestor", "9892130cfd", rec["head"]]).returncode == 0:
                    problems.append("the held commentary candidate (AR-y-279, 9892130cfd) must NOT be in the stack")
                if subprocess.run(["git", "-C", portal, "merge-base", "--is-ancestor", "46a49e57e3", rec["head"]]).returncode != 0:
                    problems.append("the route gate (AR-y-282, 46a49e57e3) must be in the stack")
            ae = rec.get("after_each") or []
            if len(ae) < len(want):
                problems.append("after_each must carry at least one row per merge (got %d)" % len(ae))
            # an intermediate merge may strand a test (that is why the order has a reconciliation step): every row must
            # typecheck clean, and the LAST row (after the reconciliation commit) must have no failing test.
            for row in ae:
                if str(row.get("typecheck_rc", row.get("typecheck", "x"))) not in ("0",):
                    problems.append("after_each row does not typecheck (typecheck_rc 0): %r" % row)
                    break
            if ae and str(ae[-1].get("failed", "x")) not in ("0",):
                problems.append("the last after_each row (after the reconciliation) must have failed 0: %r" % ae[-1])
    elif check == "y295-census":
        rec = load(root, D.replace("/r21/", "/r28/") % "113" + "FWD1_RELEASE_CENSUS.json", problems)
        if rec:
            for member in ("cells", "packages", "member_writers", "order_constraints", "status_words_leg", "calendar_member",
                           "checker_wiring", "legs", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            cells = rec.get("cells") or []
            want = ["AR-y-245", "AR-y-280", "AR-y-281", "AR-y-284", "AR-y-285", "AR-y-291", "AR-y-292", "AR-y-293"]
            got = [str(c.get("cell", c) if isinstance(c, dict) else c) for c in cells]
            for w in want:
                if not any(w in g for g in got):
                    problems.append("cells lacks %s" % w)
            pkgs = rec.get("packages") or []
            if len(pkgs) < 3:
                problems.append("packages must name at least the ticket service, irpt-ycharts-generate and the resident (got %d)" % len(pkgs))
            for pk in pkgs:
                for member in ("name", "kind", "diff_command", "diff_path_count", "members_in_release", "live"):
                    if member not in pk:
                        problems.append("package %r lacks %r" % (pk.get("name"), member))
                if not isinstance(pk.get("diff_path_count"), int):
                    problems.append("package %r: diff_path_count must be an integer (a zero is a count)" % pk.get("name"))
            if not (rec.get("legs") or []):
                problems.append("legs must be non-empty")
            if not (rec.get("order_constraints") or []):
                problems.append("order_constraints must be non-empty (the packager follows the ticket service)")
            ws = rec.get("member_writers") or {}
            if not ws or any(not isinstance(v, (list, dict)) for v in ws.values()):
                problems.append("member_writers must map each member to its writers")
    elif check == "y296-armed":
        rec = load(root, D.replace("/r21/", "/r29/") % "114" + "ARMED_ROWS_CENSUS.json", problems)
        chan = root / "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md"
        text = chan.read_text(encoding="utf-8", errors="replace")
        rows = []
        # a fenced block holds one row (an object) or several (an array of objects): parse both (the first version of this
        # check read objects only and missed 117 rows in 86 array blocks, row W114-S1)
        for block in re.findall(r"```json\n(.*?)\n```", text, flags=re.S):
            try:
                got = json.loads(block)
            except ValueError:
                continue
            for r in (got if isinstance(got, list) else [got]):
                if isinstance(r, dict):
                    rows.append(r)
        owned = [(i, r) for i, r in enumerate(rows) if r.get("hazard_standing") == "ARMED" and "Y2" in str(r.get("disarm_owner", ""))]
        left = []
        for i, r in owned:
            if not any("DISARMS" in str(x.get("one_line", "")) and str(r.get("id")) in str(x.get("one_line", "")) for x in rows[i + 1:]):
                left.append(str(r["id"]))
        print("rows parsed %d, ARMED-OWNED %d, left %d" % (len(rows), len(owned), len(left)))
        if rec:
            for member in ("denominator", "rows", "groups", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            got = {str(r.get("id")): r for r in (rec.get("rows") or [])}
            missing = [i for i in left if i not in got]
            if missing:
                problems.append("no verdict for %d row(s), first: %s" % (len(missing), missing[:5]))
            for i, r in got.items():
                if r.get("verdict") not in ("RESOLVED", "STILL_ARMED", "UNCLEAR"):
                    problems.append("%s: verdict must be RESOLVED, STILL_ARMED or UNCLEAR" % i)
                elif r.get("verdict") == "RESOLVED" and not (r.get("evidence") or []):
                    problems.append("%s: a RESOLVED verdict needs evidence" % i)
    elif check in ("y297-build", "y298-build", "y299-build", "y300-build"):
        # a release BUILD record: the staged artifact is RE-HASHED here; the delta against the live package is compared
        # with the expected members; nothing removed; the tests ran with no unexplained failure.
        import hashlib
        spec = {"y297-build": ("115", "OPAL_TICKET_API_BUILD.json", {"lambda_function.py"}, {"lambda_function.py"}, set()),
                "y298-build": ("116", "IRPT_STATUS_BUILD.json", {"status.py"}, {"status.py"}, set()),
                "y299-build": ("117", "IRPT_YCHARTS_GENERATE_BUILD.json",
                               {"template_reader.py", "portfolio.py", "uploads.py", "security_resolution.py"},
                               {"template_reader.py", "portfolio.py", "uploads.py", "security_resolution.py"}, {"trading_calendar.py"}),
                # AMENDMENT 1 of AR-y-300: opal_packager.py is already in the release-19 tarball, so it is REPLACED (a differing
                # member), not added; only the calendar is added (worker row W118-S2 was right)
                "y300-build": ("118", "RESIDENT_BUILD.json",
                               {"template_reader.py", "portfolio.py", "uploads.py", "security_resolution.py", "status.py", "resident_worker.py",
                                "opal_packager.py"},
                               {"template_reader.py", "portfolio.py", "uploads.py", "security_resolution.py", "status.py", "resident_worker.py",
                                "opal_packager.py", "resident_bindings.json", "SHA256SUMS"}, {"trading_calendar.py"})}[check]
        worker, name, need, allowed, add_need = spec
        rec = load(root, D.replace("/r21/", "/r30/") % worker + name, problems)
        if rec:
            for member in ("artifact", "delta_vs_live", "only_in_live", "only_in_release", "rollback", "tests", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            art = rec.get("artifact") or {}
            ap = art.get("path", "")
            if not ap.startswith("C:/dev/irpt-release-r28/"):
                problems.append("the artifact must be staged under C:/dev/irpt-release-r28/ (got %r)" % ap)
            elif not Path(ap).is_file():
                problems.append("the staged artifact %s does not exist" % ap)
            else:
                digest = hashlib.sha256(Path(ap).read_bytes()).hexdigest()
                print("artifact %s sha256 %s" % (ap, digest))
                if digest != str(art.get("sha256", "")).lower():
                    problems.append("the staged artifact hashes to %s, the record says %s" % (digest, art.get("sha256")))
            names = {str(x).replace("\\", "/").split("/")[-1] for x in (rec.get("delta_vs_live") or [])}
            missing = need - names
            extra = names - allowed
            if missing:
                problems.append("delta_vs_live lacks the expected member(s) %s" % sorted(missing))
            if extra:
                problems.append("delta_vs_live names member(s) outside the release %s" % sorted(extra))
            added = {str(x).replace("\\", "/").split("/")[-1] for x in (rec.get("only_in_release") or [])}
            if add_need - added:
                problems.append("only_in_release lacks the added member(s) %s" % sorted(add_need - added))
            if rec.get("only_in_live"):
                problems.append("only_in_live must be empty (nothing removed): %r" % (rec.get("only_in_live"),))
            if check == "y300-build":
                if rec.get("removed_members_count") not in (0, "0"):
                    problems.append("removed_members_count must be 0")
                if not (rec.get("host_script") or {}).get("member_checks_equal_tarball"):
                    problems.append("host_script.member_checks_equal_tarball must be true")
            else:
                ctl = rec.get("no_move_control") or {}
                if ctl.get("differs_from_live") not in ([], None) or not ctl.get("code_sha256"):
                    problems.append("no_move_control must reproduce the live package (differs_from_live [] and a code_sha256)")
            tests = rec.get("tests") or {}
            if str(tests.get("failed", "x")) != "0" and not tests.get("failures_explained"):
                problems.append("tests: failures must be zero or explained one by one")
            if not tests.get("passed"):
                problems.append("tests.passed must be a positive count")
    elif check == "y301-scripts":
        import hashlib
        import tarfile
        rec = load(root, D.replace("/r21/", "/r31/") % "119" + "RESIDENT_APPLY_SCRIPTS.json", problems)
        HOST_SHA = "bbead0d2b560ca49be3ab1e758d3111c22174e755771a46bce23ae3977122832"
        TARBALL = "C:/dev/irpt-release-r28/irpt-resident-0485393f3a-r28.tar.gz"
        SUMS = "C:/dev/irpt-release-r28/irpt-resident-0485393f3a-r28.package.SHA256SUMS"
        if rec:
            for member in ("scripts", "sums_file", "host_script", "tarball", "guard_dry_run", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not Path(SUMS).is_file():
                problems.append("the staged sums file %s does not exist" % SUMS)
                sums_sha = None
            else:
                sums_sha = hashlib.sha256(Path(SUMS).read_bytes()).hexdigest()
                with tarfile.open(TARBALL, "r:gz") as t:
                    inner = [m for m in t.getmembers() if m.isfile() and m.name.split("/", 1)[-1] == "SHA256SUMS"]
                    inner_bytes = t.extractfile(inner[0]).read() if inner else b""
                if hashlib.sha256(inner_bytes).hexdigest() != sums_sha:
                    problems.append("the staged sums file is not the tarball's own SHA256SUMS member")
                nlines = len(Path(SUMS).read_text(encoding="utf-8").splitlines())
                print("sums file sha256 %s lines %d" % (sums_sha, nlines))
                if nlines != 298:
                    problems.append("the sums file must have 298 lines (got %d)" % nlines)
                if str((rec.get("sums_file") or {}).get("sha256", "")).lower() != sums_sha:
                    problems.append("the record's sums_file.sha256 is not the staged file's")
            got = {x.get("name"): x for x in (rec.get("scripts") or [])}
            for name in ("pre_read_r28.sh", "install_r28.sh", "rollback_r28.sh"):
                x = got.get(name)
                if not x:
                    problems.append("no script record for %s" % name)
                    continue
                fp = root / x.get("path", "")
                if not fp.is_file():
                    problems.append("%s does not exist at %s" % (name, x.get("path")))
                    continue
                data = fp.read_bytes()
                if hashlib.sha256(data).hexdigest() != str(x.get("sha256", "")).lower():
                    problems.append("%s hashes to %s, the record says %s" % (name, hashlib.sha256(data).hexdigest(), x.get("sha256")))
                if any(b > 127 for b in data):
                    problems.append("%s carries non-ASCII bytes" % name)
                rc = subprocess.run(["bash", "-n", str(fp)], capture_output=True, text=True).returncode
                if rc != 0:
                    problems.append("bash -n %s rc %d" % (name, rc))
                text = data.decode("utf-8", errors="replace")
                if name == "install_r28.sh":
                    if HOST_SHA not in text:
                        problems.append("install_r28.sh does not carry the signed host script sha256")
                    if sums_sha and sums_sha not in text:
                        problems.append("install_r28.sh does not carry the staged sums file's real sha256")
                    if "0485393f3a-r28" not in text or "0485393f3a-r19" not in text:
                        problems.append("install_r28.sh must name the new and the rollback root")
                if name == "pre_read_r28.sh" and text.count("STOP-READ") < 5:
                    problems.append("pre_read_r28.sh must carry the five stop-reads")
            if not (rec.get("guard_dry_run") or {}).get("one_byte_change_refused"):
                problems.append("guard_dry_run.one_byte_change_refused must be true")
    elif check == "y306-ordinary":
        w306 = "121" if (root / (D.replace("/r21/", "/r36/") % "121" + "ORDINARY_AUTHORIZER.json")).is_file() else "120"  # AMENDMENT 1: the continuation worker
        rec = load(root, D.replace("/r21/", "/r36/") % w306 + "ORDINARY_AUTHORIZER.json", problems)
        if rec:
            for member in ("read", "rule", "principal_shape", "wiring", "iam_needs", "tests", "before_arm", "authorization_change",
                           "release_needs", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if not (rec.get("authorization_change") or "").strip():
                problems.append("authorization_change must state in a paragraph who gains upload")
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: the new tests must FAIL at HEAD without the module")
        mod = root / IR / "_scope/ordinary_viewer.py"
        if not mod.is_file():
            problems.append("no _scope/ordinary_viewer.py")
        for relpath, floor in (("_scope/tests/test_ordinary_viewer.py", 14), ("reports/tests/test_generate_installed.py", 1)):
            if not (root / IR / relpath).is_file():
                problems.append("no %s" % relpath)
                continue
            best = None
            for cwd in (IR, IR + "/" + relpath.split("/")[0]):
                target = relpath if cwd == IR else "/".join(relpath.split("/")[1:])
                rc, passed, failed = pytest(root, target, cwd)
                if rc == 0 and not failed and passed >= floor:
                    best = (rc, passed, failed)
                    break
                best = best or (rc, passed, failed)
            print("%s: %d passed, %d failed (rc=%d)" % (relpath, best[1], best[2], best[0]))
            if best[0] != 0 or best[2] or best[1] < floor:
                problems.append("%s must pass with at least %d tests" % (relpath, floor))
    elif check == "y308-words":
        rec = load(root, D.replace("/r21/", "/r38/") % "122" + "SHARES_WORDS.json", problems)
        if rec:
            for member in ("read", "codes_census", "words", "ast_words_only", "tests", "before_arm", "release_needs", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            if (rec.get("before_arm") or {}).get("failed") in (None, 0, "0"):
                problems.append("before_arm: the new tests must FAIL at HEAD")
        probe = (
            "import sys, json\n"
            "sys.path[:0] = [%r, %r, %r]\n"
            "import uploads\n"
            "import status\n"
            "code = 'SHARES_PRICE_SOURCE_NOT_COMPOSED'\n"
            "a = uploads.CORRECTION_WORDS.get(code)\n"
            "b = status.CORRECTION_WORDS.get(code)\n"
            "print(json.dumps({'a': a, 'b': b, 'equal': a == b and a is not None, 'tables_equal': uploads.CORRECTION_WORDS == status.CORRECTION_WORDS}))\n"
            % (str(root / INTAKE), str(root / IR / "ops"), str(root / IR)))
        got = subprocess.run([sys.executable, "-I", "-c", probe], capture_output=True, text=True, cwd=str(root / INTAKE))
        try:
            info = json.loads(got.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            info = {}
            problems.append("could not read the words tables: %s" % (got.stderr or got.stdout)[-300:])
        if info:
            print("words equal in both tables: %s; whole tables equal: %s" % (info.get("equal"), info.get("tables_equal")))
            if not info.get("equal"):
                problems.append("SHARES_PRICE_SOURCE_NOT_COMPOSED must have byte-equal words in uploads.py and ops/status.py")
            if not info.get("tables_equal"):
                problems.append("the two CORRECTION_WORDS tables must be equal")
            text = str(info.get("a") or "").lower()
            if "market value" not in text or "share" not in text:
                problems.append("the words must mention shares and ask for a Market Value column")
            if any(ord(ch) > 127 for ch in str(info.get("a") or "")):
                problems.append("the words must be ASCII")
        for relpath, floor in (("tests/test_shares_not_composed_words.py", 6), ("tests/test_correction_words.py", 1)):
            if not (root / INTAKE / relpath).is_file():
                problems.append("no intake/%s" % relpath)
                continue
            rc, passed, failed = pytest(root, relpath, INTAKE)
            print("%s: %d passed, %d failed (rc=%d)" % (relpath, passed, failed, rc))
            if rc != 0 or failed or passed < floor:
                problems.append("%s must pass with at least %d tests" % (relpath, floor))
    elif check in ("y309-build", "y310-build", "y311-build", "y320-build", "y323-build", "y324-build"):
        # release 29 BUILD records: the staged artifact is RE-HASHED here; the delta against the live package (or the release-28
        # tarball) is compared with the expected members; the resident record also carries three scripts and the staged sums.
        import hashlib
        spec = {"y309-build": ("123", "IRPT_STATUS_BUILD.json", {"status.py"}, {"status.py"}, set(), "C:/dev/irpt-release-r29/"),
                "y310-build": ("124", "IRPT_YCHARTS_GENERATE_BUILD.json", {"uploads.py", "generate_installed.py"},
                               {"uploads.py", "generate_installed.py"}, {"ordinary_viewer.py"}, "C:/dev/irpt-release-r29/"),
                "y311-build": ("125", "RESIDENT_BUILD.json", {"uploads.py", "status.py"},
                               {"uploads.py", "status.py", "resident_bindings.json", "SHA256SUMS"}, set(), "C:/dev/irpt-release-r29/"),
                # release 29b (the ticket service, round 40): the record lives under r40/ of the worker's folder
                "y320-build": ("130", "OPAL_TICKET_API_BUILD.json", {"lambda_function.py"}, {"lambda_function.py"}, set(),
                               "C:/dev/irpt-release-r29b/"),
                # release 30 (the intake package: AR-y-318 and AR-y-319): the Lambda and the resident carry the same three members
                "y323-build": ("131", "IRPT_YCHARTS_GENERATE_BUILD.json",
                               {"uploads.py", "interactive_access.py", "composition_admission.py"},
                               {"uploads.py", "interactive_access.py", "composition_admission.py"}, set(), "C:/dev/irpt-release-r30/"),
                "y324-build": ("132", "RESIDENT_BUILD.json",
                               {"uploads.py", "interactive_access.py", "composition_admission.py"},
                               {"uploads.py", "interactive_access.py", "composition_admission.py", "resident_bindings.json", "SHA256SUMS"},
                               set(), "C:/dev/irpt-release-r30/")}[check]
        worker, name, need, allowed, add_need, stage = spec
        rec = load(root, D.replace("/r21/", "/r40/" if check in ("y320-build", "y323-build", "y324-build") else "/r39/") % worker + name, problems)
        if rec:
            for member in ("artifact", "delta_vs_live", "only_in_live", "only_in_release", "rollback", "tests", "claim", "not_read"):
                if member not in rec:
                    problems.append("the record lacks %r" % member)
            art = rec.get("artifact") or {}
            ap = art.get("path", "")
            if not ap.startswith(stage):
                problems.append("the artifact must be staged under %s (got %r)" % (stage, ap))
            elif not Path(ap).is_file():
                problems.append("the staged artifact %s does not exist" % ap)
            else:
                digest = hashlib.sha256(Path(ap).read_bytes()).hexdigest()
                print("artifact %s sha256 %s" % (ap, digest))
                if digest != str(art.get("sha256", "")).lower():
                    problems.append("the staged artifact hashes to %s, the record says %s" % (digest, art.get("sha256")))
            names = {str(x).replace("\\", "/").split("/")[-1] for x in (rec.get("delta_vs_live") or [])}
            if need - names:
                problems.append("delta_vs_live lacks the expected member(s) %s" % sorted(need - names))
            if names - allowed:
                problems.append("delta_vs_live names member(s) outside the release %s" % sorted(names - allowed))
            added = {str(x).replace("\\", "/").split("/")[-1] for x in (rec.get("only_in_release") or [])}
            if add_need - added:
                problems.append("only_in_release lacks the added member(s) %s" % sorted(add_need - added))
            if not add_need and added:
                problems.append("only_in_release must be empty (nothing added): %r" % sorted(added))
            if rec.get("only_in_live"):
                problems.append("only_in_live must be empty (nothing removed): %r" % (rec.get("only_in_live"),))
            if check not in ("y311-build", "y324-build"):
                ctl = rec.get("no_move_control") or {}
                if ctl.get("differs_from_live") not in ([], None) or not ctl.get("code_sha256"):
                    problems.append("no_move_control must reproduce the live package (differs_from_live [] and a code_sha256)")
            else:
                if rec.get("removed_members_count") not in (0, "0"):
                    problems.append("removed_members_count must be 0")
                if not (rec.get("host_script") or {}).get("member_checks_equal_tarball"):
                    problems.append("host_script.member_checks_equal_tarball must be true")
                sums = rec.get("sums_file") or {}
                sp = sums.get("path", "")
                if not Path(sp).is_file() or hashlib.sha256(Path(sp).read_bytes()).hexdigest() != str(sums.get("sha256", "")).lower():
                    problems.append("the staged sums file is missing or does not hash to the record")
                got = {x.get("name"): x for x in (rec.get("scripts") or [])}
                for sname in (("pre_read_r30.sh", "install_r30.sh", "rollback_r30.sh") if check == "y324-build"
                              else ("pre_read_r29.sh", "install_r29.sh", "rollback_r29.sh")):
                    x = got.get(sname)
                    if not x:
                        problems.append("no script record for %s" % sname)
                        continue
                    fp = root / x.get("path", "")
                    if not fp.is_file():
                        problems.append("%s does not exist at %s" % (sname, x.get("path")))
                        continue
                    data = fp.read_bytes()
                    if hashlib.sha256(data).hexdigest() != str(x.get("sha256", "")).lower():
                        problems.append("%s does not hash to the record" % sname)
                    if any(b > 127 for b in data):
                        problems.append("%s carries non-ASCII bytes" % sname)
                    if subprocess.run(["bash", "-n", str(fp)], capture_output=True, text=True).returncode != 0:
                        problems.append("bash -n %s failed" % sname)
            tests = rec.get("tests") or {}
            if str(tests.get("failed", "x")) != "0" and not tests.get("failures_explained"):
                problems.append("tests: failures must be zero or explained one by one")
            if not tests.get("passed"):
                problems.append("tests.passed must be a positive count")
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
