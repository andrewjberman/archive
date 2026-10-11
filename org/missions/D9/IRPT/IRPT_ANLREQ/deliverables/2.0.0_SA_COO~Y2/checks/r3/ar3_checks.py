"""IRPT_ANLREQ round 3, workstream Y (issuer 2.0.0_SA_COO~Y2) -- the mechanical checks of the round's five worker cells.

Usage:  python ar3_checks.py <check> [--root <workspace root>] [--portal <portal worktree>]
Each check prints its OK token as the LAST line and exits 0, or prints FAIL lines and `<CHECK>-FAIL`, exit 1.
Every subprocess is bounded (100 s) so an invocation ends inside a worker's 120 s limit. Nothing here calls AWS.

  y31-page      AR-y-31: the named tests of portal `package-report-reader.test.tsx` exist and pass            -> Y31-PAGE-OK
  y31-keep      AR-y-31: the package tests that must not move still pass (package-r2, commentary-package)     -> Y31-KEEP-OK
  y35-page      AR-y-35: the named tests of portal `analysis-firm-choice.test.tsx` exist and pass             -> Y35-PAGE-OK
  y32-ref       AR-y-32: `ops/tests/test_retained_ref_served.py`, named tests exist and pass                  -> Y32-REF-OK
  y32-history   AR-y-32: `ops/tests/test_history_row_client.py`, named tests exist and pass                   -> Y32-HISTORY-OK
  y32-dates     AR-y-32: `ops/tests/test_section_dates_by_branch.py`, named tests exist and pass              -> Y32-DATES-OK
  y32-contract  AR-y-32: both contract documents declare the new members; the `_contracts` failing SET is
                exactly the two ids known at the base                                                          -> Y32-CONTRACT-OK
  y33-store     AR-y-33: BUILD_ONLY of irpt-commentary-draft-store-lambda WITHOUT BAU_PARITY_SKIP prints its
                BUILD_ONLY line                                                                                -> Y33-STORE-OK
  y33-digest    AR-y-33: the source map records irpt-status's live digest, and a BUILD_ONLY still prints it    -> Y33-DIGEST-OK
  y36-order     AR-y-36: the reproducer the worker recorded (S31_REPRODUCER.json) runs green                   -> Y36-ORDER-OK
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LIMIT = 100
IR = "infra/aws/lambda/investor-reporting"
STATUS_LIVE = "6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc="
CONTRACT_RED = {
    "_contracts/tests/test_seam_paired.py::test_every_declared_route_has_a_response_contract_whose_refs_resolve",
    "_contracts/tests/test_seam_paired.py::"
    "test_control_a_known_good_document_conforms_and_a_known_bad_one_does_not[analysis-request-original]",
}
NAMES = {
    "y31-page": ("src/pages/TicketCenter/__tests__/package-report-reader.test.tsx", [
        "the package Report file opens the finished report through getOwnedAnalysisReport",
        "the opened report renders the retained sections and no request record",
        "the request id is carried on data-request-id and never in visible words",
        "a refused report read shows the reason and opens nothing"]),
    "y35-page": ("src/pages/TicketCenter/__tests__/analysis-firm-choice.test.tsx", [
        "the firm answer is a choice from the firms the profile allows",
        "a caller with one allowed firm has it chosen and cannot type another",
        "a firm outside the allowed list cannot be submitted"]),
    "y32-ref": (IR + "/ops/tests/test_retained_ref_served.py", [
        "test_ready_report_returns_retained_ref_in_the_performance_shape",
        "test_retained_ref_equals_the_ref_the_reader_checked",
        "test_other_firm_is_refused_and_no_ref_is_returned"]),
    "y32-history": (IR + "/ops/tests/test_history_row_client.py", [
        "test_history_row_states_the_client_its_selection_names",
        "test_upload_request_row_states_null_client",
        "test_single_read_wire_is_unchanged"]),
    "y32-dates": (IR + "/ops/tests/test_section_dates_by_branch.py", [
        "test_opal_engine_not_available_row_with_null_date_is_undated",
        "test_ycharts_branch_rule_is_unchanged",
        "test_opal_engine_null_date_beside_value_is_refused",
        "test_opal_engine_bad_date_beside_not_available_is_refused"]),
}


def run(cmd, cwd, env=None):
    try:
        done = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace",
                              timeout=LIMIT, env=env)
        return done.returncode, (done.stdout or "") + (done.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %d s: %s" % (LIMIT, " ".join(cmd))
    except FileNotFoundError as exc:
        return 127, "NOT FOUND: %s" % exc


def finish(check, problems):
    token = check.upper()
    if problems:
        for line in problems:
            print("FAIL: " + line)
        print(token + "-FAIL")
        return 1
    print(token + "-OK")
    return 0


def names_present(path, names):
    if not path.is_file():
        return ["no file %s" % path.as_posix()]
    text = path.read_text(encoding="utf-8")
    return ["test name absent: %s" % n for n in names if n not in text]


def portal_tests(check, portal, files):
    problems = []
    if check in NAMES:
        problems += names_present(portal / NAMES[check][0], NAMES[check][1])
    if problems:
        return problems
    rc, out = run(["bun", "test"] + ["./" + name for name in files], portal)  # bun reads a bare name as a filter, not a path
    tail = [line for line in out.splitlines() if line.strip()][-6:]
    print("\n".join(tail))
    if rc != 0:
        problems.append("bun test rc=%d on %s" % (rc, " ".join(files)))
    return problems


def pytest_file(check, root):
    rel, names = NAMES[check]
    problems = names_present(root / rel, names)
    if problems:
        return problems
    env = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="y", AWS_DEFAULT_REGION="us-east-1")
    rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", rel], root, env)
    print("\n".join([line for line in out.splitlines() if line.strip()][-4:]))
    return [] if rc == 0 else ["pytest rc=%d on %s" % (rc, rel)]


def contract(root):
    problems = []
    docs = root / "docs/contracts/investor-reporting/v1"
    report = json.loads((docs / "AnalysisReport.schema.json").read_text(encoding="utf-8"))
    perf = json.loads((docs / "PerformanceReport.schema.json").read_text(encoding="utf-8"))
    history = json.loads((docs / "OwnedAnalysisRequestHistory.schema.json").read_text(encoding="utf-8"))

    def find(node, key):
        if isinstance(node, dict):
            if key in node.get("properties", {}):
                yield node["properties"][key]
            for value in node.values():
                yield from find(value, key)
        elif isinstance(node, list):
            for value in node:
                yield from find(value, key)

    perf_ref = list(find(perf, "retained_ref"))
    report_ref = list(find(report, "retained_ref"))
    if not perf_ref:
        problems.append("PerformanceReport.schema.json declares no retained_ref (the control is broken)")
    if not report_ref:
        problems.append("AnalysisReport.schema.json declares no retained_ref")
    elif perf_ref:
        # The Performance shape, member for member, with ONE stated difference: report_kind is the const ANALYSIS.
        want = json.loads(json.dumps(perf_ref[0]))
        want.get("properties", {})["report_kind"] = {"const": "ANALYSIS"}
        got = json.loads(json.dumps(report_ref[0]))
        want.pop("description", None)
        got.pop("description", None)
        if got != want:
            problems.append("AnalysisReport retained_ref is not the Performance shape with report_kind const ANALYSIS")
    client = list(find(history, "client_id"))
    if not client:
        problems.append("OwnedAnalysisRequestHistory.schema.json declares no client_id on its row")
    elif sorted(str(t) for t in (client[0].get("type") if isinstance(client[0].get("type"), list)
                                 else [client[0].get("type")])) != ["null", "string"]:
        problems.append("client_id is not typed string-or-null: %r" % client[0].get("type"))
    single = json.loads((docs / "OwnedAnalysisRequest.schema.json").read_text(encoding="utf-8"))
    if "client_id" in json.dumps(single):
        problems.append("OwnedAnalysisRequest.schema.json (the SINGLE read) gained client_id; only the history row may")
    env = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="y", AWS_DEFAULT_REGION="us-east-1")
    rc, out = run([sys.executable, "-m", "pytest", "_contracts", "-q", "-p", "no:cacheprovider", "-rf", "--color=no"], root / IR, env)
    failed = set(item.replace("\\", "/") for item in re.findall(r"^FAILED (\S+)", out, re.M))  # Windows prints backslashes
    print("contract suite: rc=%d, failing set size %d" % (rc, len(failed)))
    if rc == 124:
        problems.append("the _contracts suite timed out")
    elif failed != CONTRACT_RED:
        problems.append("the _contracts failing SET moved: new %r, gone %r"
                        % (sorted(failed - CONTRACT_RED), sorted(CONTRACT_RED - failed)))
    return problems


def build_only(root, function, extra_env=None):
    env = dict(os.environ, BUILD_ONLY="1")
    env.pop("BAU_PARITY_SKIP", None)
    env.update(extra_env or {})
    import tempfile
    env["TMPDIR"] = tempfile.mkdtemp(prefix="ar3-build-")  # outside the tree: a build leaves nothing in the worktree
    rc, out = run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", function], root, env)
    line = [text for text in out.splitlines() if text.startswith("BUILD_ONLY:")]
    return rc, out, (line[-1] if line else "")


SEVEN = ("build_resident_package.py", "currency_authority.py", "custody_write.py", "generate_installed.py",
         "request_composition.py", "resident_installed.py", "status_installed.py")
STORE = "irpt-commentary-draft-store-lambda"


def store(root):
    import zipfile
    rc, out, line = build_only(root, STORE)
    print("\n".join([text for text in out.splitlines() if text.strip()][-5:]))
    if not line:
        return ["no BUILD_ONLY line without BAU_PARITY_SKIP (rc=%d)" % rc]
    zpath = line.split("BUILD_ONLY:", 1)[1].split(" sha256=", 1)[0].strip()
    if zpath.startswith("/tmp/") and not os.path.exists(zpath):  # an MSYS path printed by bash on Windows
        zpath = os.path.join(os.environ.get("TEMP", ""), zpath[len("/tmp/"):])
    try:
        members = set(zipfile.ZipFile(zpath).namelist())
    except (OSError, zipfile.BadZipFile) as exc:
        return ["cannot open the built zip %s: %s" % (zpath, type(exc).__name__)]
    packaged = sorted(name for name in SEVEN if name in members)
    print("built members %d; of the seven declared outside, packaged: %d" % (len(members), len(packaged)))
    return ["declared outside the package but packaged: %r" % packaged] if packaged else []


def control(root):
    """The difference control of y33-store: the parity check must still refuse a file nobody declared."""
    probe = root / IR / "reports" / "zz_ar3_parity_probe.py"
    if probe.exists():
        return ["the probe file already exists: %s" % probe.as_posix()]
    probe.write_text("# AR-y-33 parity control; removed by the check that wrote it\n", encoding="ascii")
    try:
        rc, out, line = build_only(root, STORE)
    finally:
        probe.unlink()
    named = "zz_ar3_parity_probe.py" in out and "parity check failed" in out
    print("probe build: rc=%d, BUILD_ONLY line %s, probe named in a parity refusal: %s"
          % (rc, "present" if line else "absent", named))
    problems = []
    if line:
        problems.append("the build went through with an undeclared file in the source dir")
    if not named:
        problems.append("the refusal does not name the undeclared file")
    return problems


def reads(root):
    result = root / "org/tier2_senior/0.7.0_AE_CloudOps~ANL/deliverables/Y1_reads_3_4_rev6_result.json"
    if not result.is_file():
        return ["no %s" % result.relative_to(root).as_posix()]
    doc = json.loads(result.read_text(encoding="utf-8"))
    problems = []
    under = (doc.get("release_under_test") or {})
    if under.get("code_sha256") != STATUS_LIVE or under.get("claim") != "measured":
        problems.append("release_under_test is not the live digest as MEASURED: %r" % under)
    got = doc.get("reads") or {}
    for key in ("3a", "3b", "4_record", "4_route"):
        if got.get(key) is not True:
            problems.append("read %s is %r" % (key, got.get(key)))
    if got.get("3c") is not True and not (got.get("3c") is None and isinstance(got.get("3c_reason"), str) and got["3c_reason"]):
        problems.append("read 3c is neither true nor null with a stated reason")
    writes = doc.get("original_read_writes") or {}
    before, after = writes.get("versions_before"), writes.get("versions_after")
    if type(before) is not int or type(after) is not int or before != after or before < 1:
        problems.append("original_read_writes: versions_before %r, versions_after %r" % (before, after))
    if not (isinstance(writes.get("keys_scope"), str) and writes["keys_scope"]):
        problems.append("original_read_writes.keys_scope (which keys were counted) is not stated")
    if "http" in json.dumps(doc).lower():
        problems.append("the result file carries a URL; a signed link is never written to a file")
    print("reads %r; versions %r -> %r" % ({k: got.get(k) for k in ("3a", "3b", "3c", "4_record", "4_route")}, before, after))
    return problems


def digest(root):
    problems = []
    source_map = json.loads((root / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))
    recorded = source_map["functions"]["irpt-status"].get("artifact_sha256")
    print("source map irpt-status artifact_sha256: %s" % recorded)
    if recorded != STATUS_LIVE:
        problems.append("the map records %r, the function runs %s" % (recorded, STATUS_LIVE))
    rc, out, line = build_only(root, "irpt-status")
    print(line or "\n".join([text for text in out.splitlines() if text.strip()][-3:]))
    if STATUS_LIVE not in line:
        problems.append("BUILD_ONLY of irpt-status does not print the live digest (rc=%d)" % rc)
    return problems


def order(root):
    worker_dirs = sorted((root / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables").glob("0.9.0_WK_IRPT_ANLREQ~*/S31_REPRODUCER.json"))
    if not worker_dirs:
        return ["no S31_REPRODUCER.json in any worker deliverables folder"]
    spec = json.loads(worker_dirs[-1].read_text(encoding="utf-8"))
    files = spec.get("files")
    if (not isinstance(files, list) or len(files) < 2 or any(not isinstance(f, str) for f in files)
            or not any(f.endswith("test_custody_retained.py") for f in files)):
        return ["S31_REPRODUCER.json `files` must list the polluting test file(s) then the custody file(s), in order"]
    if spec.get("fails_at_base") is not True:
        return ["S31_REPRODUCER.json must record fails_at_base true (the same sequence, run at the base commit)"]
    base = root / IR / "ycharts/generate/tests"
    missing = [f for f in files if not (base / f).is_file()]
    if missing:
        return ["reproducer names files that do not exist: %r" % missing]
    env = dict(os.environ, AWS_ACCESS_KEY_ID="x", AWS_SECRET_ACCESS_KEY="y", AWS_DEFAULT_REGION="us-east-1")
    rc, out = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + [str(Path(IR) / "ycharts/generate/tests" / f)
                                                                                for f in files], root, env)
    print("\n".join([line for line in out.splitlines() if line.strip()][-3:]))
    return [] if rc == 0 else ["the recorded reproducer still fails (rc=%d)" % rc]


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    check, root, portal = argv[1], Path("."), None
    rest = argv[2:]
    while rest:
        flag = rest.pop(0)
        if flag == "--root":
            root = Path(rest.pop(0))
        elif flag == "--portal":
            portal = Path(rest.pop(0))
        else:
            print("ERROR: unknown argument " + flag)
            return 2
    root = root.resolve()
    if check in ("y31-page", "y31-keep", "y35-page"):
        if portal is None:
            print("ERROR: --portal <portal worktree> is required")
            return 2
        files = {"y31-page": [NAMES["y31-page"][0]],
                 "y31-keep": ["src/pages/TicketCenter/__tests__/package-r2.test.tsx",
                              "src/pages/TicketCenter/__tests__/commentary-package.test.tsx"],
                 "y35-page": [NAMES["y35-page"][0]]}[check]
        return finish(check, portal_tests(check, portal.resolve(), files))
    if check in ("y32-ref", "y32-history", "y32-dates"):
        return finish(check, pytest_file(check, root))
    if check == "y32-contract":
        return finish(check, contract(root))
    if check == "y33-store":
        return finish(check, store(root))
    if check == "y33-digest":
        return finish(check, digest(root))
    if check == "y33-control":
        return finish(check, control(root))
    if check == "y34-reads":
        return finish(check, reads(root))
    if check == "y36-order":
        return finish(check, order(root))
    print("ERROR: unknown check %r" % check)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
