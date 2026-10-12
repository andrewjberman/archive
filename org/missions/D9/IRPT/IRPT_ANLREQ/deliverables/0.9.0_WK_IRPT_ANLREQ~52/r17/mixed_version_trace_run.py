"""AR-y-174 scratch harness: a trace, not a product test.

The round-16 reader (commit aaf156e8eb, "old") and the repaired reader (worktree, AR-y-171, READER_VERSION r17.1, "new")
are each run as WRITER (the upload door stores a template) and as READER (read_input re-opens it, and a same-token
re-POST answers again), in process, through the repository's own offline upload world (intake/tests/test_template_uploads.py).
Synthetic sheets only. Offline: no network, no AWS, no send, no deploy, no invoke.

Version switch: the upload door and read_input import template_reader at call time, so the module is swapped in
sys.modules for the writer's acceptance and for the reader's re-open (the mechanism of intake/tests/test_stored_input_contract.py).

Run:  cd <worktree>/infra/aws/lambda/investor-reporting/intake && python -m pytest <this file> -q -p no:cacheprovider
Writes: MIXED_VERSION_TRACE.json beside this file.
"""
import base64  # noqa: F401  (kept: the payload helper in test_template_uploads encodes with base64)
import hashlib
import importlib.util
import json
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock

WT = Path(__file__).resolve().parents[8]
INTAKE = WT / "infra/aws/lambda/investor-reporting/intake"
REL = "infra/aws/lambda/investor-reporting/intake/template_reader.py"
OLD_COMMIT = "aaf156e8eb"
OUT = Path(__file__).resolve().parent / "MIXED_VERSION_TRACE.json"
sys.path[:0] = [str(INTAKE / "tests"), str(INTAKE)]

import test_template_uploads as tu  # noqa: E402
from security_resolution import classify_batch  # noqa: E402
from test_template_reader import rows, workbook  # noqa: E402
from uploads import UploadRefused  # noqa: E402

PAIRS = [("old", "old"), ("new", "new"), ("old", "new"), ("new", "old")]
INPUTS = [
    ("two_sheet_workbook", "xlsx",
     lambda: workbook([("holdings_template", rows("AAPL", "Dollars", "10.01")), ("notes", rows("VNQ", "Dollars", "2.02"))])),
    ("total_row_sheet", "csv", lambda: b"Ticker,Dollars\nAAA,100\nBBB,200\nTotal,300\n"),
    ("two_value_account_sheet", "csv", lambda: b"Ticker,Dollars,Account\nAAA,100,ACCT-ONE\nBBB,200,ACCT-TWO\n"),
    ("one_account_sheet", "csv", lambda: b"Ticker,Dollars,Account\nAAA,100,ACCT-ONE\nBBB,200,ACCT-ONE\n"),
    ("repair_header_two_values", "csv", lambda: b"Ticker,Dollars,Account-Number\nAAA,100,ACCT-ONE\nBBB,200,ACCT-TWO\n"),
    ("repair_header_one_value", "csv", lambda: b"Ticker,Dollars,Account-Number\nAAA,100,ACCT-ONE\nBBB,200,ACCT-ONE\n"),
    ("attribute_header_one_account", "csv",
     lambda: b"Ticker,Dollars,Account,Account Value\nAAA,100,ACCT-ONE,100\nBBB,200,ACCT-ONE,200\n"),
]

CONSUMERS = [
    "intake/template_reader.py:34 READER_VERSION (the one member reader_version is written at :277 by read_template)",
    "intake/template_reader.py:37 READER_PINS (pin test: intake/tests/test_stored_input_contract.py:180-189)",
    "intake/uploads.py:159 from template_reader import WORDS (inside _with_correction_words)",
    "intake/uploads.py:460-465 _defer: read_template is the door's FIRST answer when request_resolution is wired (ERROR sheets stop here)",
    "intake/uploads.py:515-516 _answer NEEDS_CORRECTION: re-reads the template with the RUNNING reader (answer shown on re-POST)",
    "intake/uploads.py:523 resolve_deferred: TemplateRefused, finding (the resident's resolve path)",
    "intake/uploads.py:570-572 _freeze_template: read_template (the synchronous door and the resident's resolve)",
    "intake/uploads.py:362 create with supersedes_input_id -> read_input (re-read under the running reader)",
    "intake/uploads.py:599 _normalized_response -> read_input (every NORMALIZED answer and every re-POST)",
    "intake/uploads.py:633-641 read_input: imports READER_VERSION and read_template; stored_version = document template reader_version (absent = before-C-STOREDINPUT); the full re-read is compared ONLY when stored_version == READER_VERSION",
    "intake/portfolio.py:357 from template_reader import finding, _number (freeze_template_portfolio)",
    "intake/upload_suggestions.py:27 docstring mention only (no import)",
    "ycharts/generate/resident_worker.py:1008, :1015, :1024 from template_reader import finding (the RESIDENT: its own installed copy, not this worktree file)",
    "ycharts/generate/prospect_submission.py:68, :79 uploads.read_input (submit of an analysis request on a held input, in irpt-ycharts-generate)",
    "_scope/retained_input_authorizer.py:47, :63 read_input (CSV lane only; a template-lane input is not served through it, census row :67)",
    "ops/prospect_dates.py:102 comment; :141, :143 read the STORED document['template'] (no read_template call)",
    "tests only: intake/tests/test_stored_input_contract.py:49, :94, :106, :137-141; intake/tests/test_template_reader.py:14; intake/tests/test_correction_words.py:18, :114, :126, :138; intake/tests/test_template_uploads.py; intake/tests/test_template_account_totals.py; intake/tests/test_deferred_resolution.py:214; ops/tests/test_prospect_dates.py:368-369; ycharts/generate/tests/test_resolution_retry.py:16, :23",
    "PACKAGING lambda-source-map.json (infra/aws/lambda/ci): irpt-ycharts-generate entry at line 3988 packages uploads.py (pin f09b802cdc, sha256 47f89e0b...) at lines 4542-4546 and template_reader.py (pin 3f29017cfc, sha256 76795b75...) at lines 4559-4564, and also upload_resolution.py, portfolio.py, security_resolution.py; irpt-status (entry line 5293) packages ops/status.py (line 5582) and NO reader module; irpt-intake-poller (entry line 3875) names no template_reader.py in its files[] (text search of the map)",
    "PACKAGING reports/build_resident_package.py (DIRS include intake and ycharts/generate; ONE backend pin via git show): the RESIDENT carries template_reader.py at its build pin; installed by ycharts/generate/install-resident.sh. The resident's installed pin was NOT read",
]

CLAIM = (
    "In process, on the repository's offline upload world with seven synthetic sheets (28 writer/reader cases), every "
    "template that was stored was re-opened by read_input and re-POSTed under the reader that ran the re-open: 16 of 16 "
    "ACCEPTED (8 same-version, 8 mixed). The 8 mixed re-opens ran no full re-read comparison (compare_runs_on_reopen "
    "false in 8 of 8), which is the only reason none of them refused; the 8 same-version re-opens ran it and passed. "
    "So in this set no input accepted under one version was refused by the other at re-open. The versions differ at the "
    "upload DOOR, not at re-open: the same bytes can be stored by one version and turned back by the other. Two valid "
    "one-account files were checked: the repaired reader accepts both, and the round-16 reader turns back the one with "
    "an 'Account Value' column (a false refusal). The two inputs the repaired reader turns back (a total row, a two-value "
    "Account column) are turned back by the round-16 reader too, except the hyphenated 'Account-Number' two-value sheet, "
    "which the round-16 reader stores. NOT shown: the deployed Lambda's own bytes, the resident's installed package, the "
    "resolve path with request_resolution wired, and the queue between the two runtimes."
)

WHAT_A_PERSON_SEES = (
    "Upload door, mixed state. The answer depends on which reader answers the POST, not on the file alone. A total-row "
    "sheet and a two-value 'Account' column are turned back by both versions. A two-value 'Account-Number' sheet is turned "
    "back by the repaired reader only: the round-16 reader stores it as NORMALIZED, so a person uploading it through an "
    "old runtime sees a success for a file with two accounts. A one-account file with an 'Account Value' column is turned "
    "back by the round-16 reader (ACCOUNT_COLUMN_SEVERAL_VALUES on a column that is not an account number) and accepted "
    "by the repaired reader. Same-token re-POST: when the first answer was NORMALIZED, the re-POST returns the stored "
    "NORMALIZED under either reader, because the normalization row is not judged again; when the first answer was a "
    "turn-back, the re-POST is judged afresh by the reader that answers it. So one two-account file can read NORMALIZED "
    "on a same-token re-POST and NEEDS_CORRECTION on a fresh-token POST under the repaired reader (measured: writer "
    "round-16, repaired reader, repair_header_two_values). Re-open (portfolio, submit, refresh): a person sees no refusal "
    "caused by a version change; an input stored under either version opens under the other, and it is shown as the "
    "version that stored it decided it. The SHEETS_NOT_READ notice is stored by both versions on a two-sheet workbook. "
    "Not measured here: the words a portal shows for each code (only the state, reason and codes were recorded)."
)

NOT_READ = [
    "the resident's INSTALLED package: its pin, its bytes and whether it runs now (no host call; install-resident.sh and build_resident_package.py were read as code only)",
    "the resident path with request_resolution wired (uploads.py:400-402 _defer and resolve_deferred:521-567): NOT run; the harness uses the synchronous door (uploads.py:402-407) and the same read_input",
    "the queue between the Lambda and the resident (the resolution message and its replay): not run, not read",
    "the reader the deployed irpt-ycharts-generate actually carries: the map pins template_reader.py at 3f29017cfc (before the AR-y-142 and AR-y-162 changes; it writes no reader_version member). That third version is NOT one of the four pairs and was not run",
    "the pinned neighbours of uploads.py (f09b802cdc) and upload_resolution.py (3f29017cfc): the harness runs HEAD's uploads.py for both sides; only the reader module is swapped",
    "the reverse half-release on the resident (resident new, Lambda old) as a separate process: inferred from the code, not run",
    "the live provider: resolve_template is mocked (every symbol FOUND); no securities_info call, no network",
    "any real upload, stored artifact or live row: none read",
    "the portal's reading of the envelope (census rows): not re-read here",
    "other Lambdas that might import the changed modules without listing them (the map's import-closure gate covers the listed ones)",
]

VERSIONS = {
    "old": {"reader_version": "irpt-template-reader.r16.1", "source": "git show aaf156e8eb:" + REL,
            "blob_sha256_of_file": None},
    "new": {"reader_version": "irpt-template-reader.r17.1", "source": "worktree " + REL + " (HEAD ccbed3339b, the AR-y-171 commit; the same blob as drain b09e84971f)",
            "blob_sha256_of_file": None},
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_old():
    got = subprocess.run(["git", "-C", str(WT), "show", OLD_COMMIT + ":" + REL], capture_output=True)
    if got.returncode != 0 or not got.stdout:
        raise RuntimeError("git show failed: rc=%s" % got.returncode)
    path = WT / ".scratch" / "r17" / "template_reader_r16.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(got.stdout)
    VERSIONS["old"]["blob_sha256_of_file"] = hashlib.sha256(got.stdout).hexdigest()
    return load("template_reader_r16_under_test", path)


def load_new():
    path = INTAKE / "template_reader.py"
    VERSIONS["new"]["blob_sha256_of_file"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return load("template_reader_r17_under_test", path)


OLD = load_old()
NEW = load_new()
MODS = {"old": OLD, "new": NEW}


@contextmanager
def reader_as(module):
    saved = sys.modules.get("template_reader")
    sys.modules["template_reader"] = module
    try:
        yield
    finally:
        if saved is None:
            sys.modules.pop("template_reader", None)
        else:
            sys.modules["template_reader"] = saved


def fresh_case():
    case = tu.legacy.UploadIntegrationTests(methodName="runTest")
    case.setUp()
    case.service.artifacts.families |= {"ORIGINAL_HOLDINGS"}

    def resolve(principal, owner, symbols):
        receipt = {"http_status": 200, "complete": True,
                   "final_url_path": "/securities/securities_info", "account_id": "offline-account",
                   "source_revision": "offline-receipt", "requested": symbols, "observed_at": "2026-09-23T00:00:00Z",
                   "json": [{"id": s, "security_id": s, "securitylist_security_id": "S:" + s,
                             "security_name": s, "detailed_security_type": "stock", "features_needed": []}
                            for s in symbols if s != "MISSING"]}
        return classify_batch(symbols, receipt, account_id="offline-account", source_revision="offline-receipt")

    case.service.resolve_template = Mock(side_effect=resolve)
    case.service.resolve_security = Mock(side_effect=AssertionError("template cannot use legacy identity guesses"))
    case.service.parse_mapping = Mock(side_effect=AssertionError("template cannot use mail parser mapping"))
    return case


def attempt(call):
    try:
        return {"ok": True, "answer": call()}
    except UploadRefused as exc:
        return {"ok": False, "refused": str(exc)}
    except Exception as exc:  # recorded, never hidden: a harness error is an outcome to read
        return {"ok": False, "error": "%s: %s" % (type(exc).__name__, str(exc)[:200])}


def door_text(res):
    if "error" in res:
        return "HARNESS-ERROR " + res["error"]
    if not res["ok"]:
        return "REFUSED " + res["refused"]
    answer = res["answer"]
    state = answer.get("state", "?")
    reason = answer.get("reason")
    return state if not reason else "%s (%s)" % (state, reason)


def reopen_text(res, document_equal):
    if "error" in res:
        return "HARNESS-ERROR " + res["error"]
    if not res["ok"]:
        return "REFUSED " + res["refused"]
    return "ACCEPTED (document equal to stored portfolio: %s)" % document_equal


def codes_of(answer):
    found = answer.get("findings") or (answer.get("portfolio") or {}).get("findings") or []
    return ["%s:%s" % (f.get("code"), f.get("severity")) for f in found if isinstance(f, dict)]


def strip_version(template):
    return {k: v for k, v in template.items() if k != "reader_version"}


def run_case(writer, reader, label, file_type, data):
    W, R = MODS[writer], MODS[reader]
    case = fresh_case()
    body = tu.payload(data, file_type, upload_token="ar174-%s-%s-%s" % (writer, reader, label))
    with reader_as(W):
        first = attempt(lambda: case.create(body))
    row = {"writer_version": writer, "reader_version": reader, "input": label, "file_type": file_type,
           "writer_reader_version_string": W.READER_VERSION, "reader_reader_version_string": R.READER_VERSION}
    row["writer_door"] = door_text(first)
    row["writer_codes"] = codes_of(first["answer"]) if first.get("ok") else []
    stored = bool(first.get("ok")) and first["answer"].get("state") == "NORMALIZED"
    if stored:
        answer = first["answer"]
        template = answer["portfolio"]["template"]
        stored_version = template.get("reader_version", "ABSENT")
        row["stored_reader_version"] = stored_version
        row["compare_runs_on_reopen"] = stored_version == R.READER_VERSION
        row["reread_under_reader_equals_stored_ignoring_version"] = (
            strip_version(R.read_template(data, file_type)) == strip_version(template))
        with reader_as(R):
            reopen = attempt(lambda: case.service.read_input(case.principal, case.owner, answer["input_id"]))
        equal = bool(reopen.get("ok")) and reopen["answer"]["document"] == answer["portfolio"]
        row["reopen"] = reopen_text(reopen, equal)
    else:
        row["stored_reader_version"] = None
        row["compare_runs_on_reopen"] = None
        row["reread_under_reader_equals_stored_ignoring_version"] = None
        row["reopen"] = "not run: the writer stored nothing"
    with reader_as(R):
        repost = attempt(lambda: case.create(body))
    row["repost_same_token_under_reader"] = door_text(repost)
    row["repost_codes"] = codes_of(repost["answer"]) if repost.get("ok") else []
    if stored:
        row["outcome"] = ("STORED by the %s writer; RE-OPEN under the %s reader: %s; full re-read compared: %s; "
                          "same-token RE-POST under the %s reader: %s"
                          % (writer, reader, row["reopen"], "YES" if row["compare_runs_on_reopen"] else "NO",
                             reader, row["repost_same_token_under_reader"]))
    else:
        row["outcome"] = ("NOT STORED: the %s writer's door answered %s; no re-open; same-token RE-POST under the %s "
                          "reader: %s" % (writer, row["writer_door"], reader, row["repost_same_token_under_reader"]))
    row["evidence"] = ("in process, tests/test_template_uploads.py offline world, synthetic sheet %s (%s); writer %s = %s; "
                       "reader %s = %s; writer door %s; writer codes %s; stored reader_version %s; compare on re-open %s; "
                       "re-read under reader equals stored ignoring version %s; re-open %s; re-POST %s; repost codes %s"
                       % (label, file_type, writer, W.READER_VERSION, reader, R.READER_VERSION, row["writer_door"],
                          row["writer_codes"], row["stored_reader_version"], row["compare_runs_on_reopen"],
                          row["reread_under_reader_equals_stored_ignoring_version"], row["reopen"],
                          row["repost_same_token_under_reader"], row["repost_codes"]))
    return row


def test_the_four_pairs_in_process_and_the_trace_record():
    cases = []
    for writer, reader in PAIRS:
        for label, file_type, make in INPUTS:
            cases.append(run_case(writer, reader, label, file_type, make()))
    trace = {
        "to_id": "IRPT_ANLREQ.TO-AR-y-174",
        "cell": "AR-y-174",
        "method": ("in-process runs of the four writer/reader pairs over seven synthetic sheets; the version switch is "
                   "sys.modules['template_reader'] for the writer's acceptance and for the reader's re-open and re-POST"),
        "versions": VERSIONS,
        "consumers": CONSUMERS,
        "cases": cases,
        "claim": CLAIM,
        "not_read": NOT_READ,
        "what_a_person_sees": WHAT_A_PERSON_SEES,
    }
    OUT.write_text(json.dumps(trace, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print("cases written: %d -> %s" % (len(cases), OUT.name))
    for row in cases:
        print("%s/%s %-30s door=%s | reopen=%s | repost=%s" % (row["writer_version"], row["reader_version"], row["input"],
              row["writer_door"], row.get("reopen"), row["repost_same_token_under_reader"]))
    assert len(cases) == len(PAIRS) * len(INPUTS)
