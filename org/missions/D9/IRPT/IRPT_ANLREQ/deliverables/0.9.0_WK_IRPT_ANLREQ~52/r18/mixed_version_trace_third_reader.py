"""AR-y-186 scratch harness: the mixed-version trace extended by the Lambda's third reader (pin 3f29017cfc).

Readers:
  lambda_pinned = intake/template_reader.py at pin 3f29017cfc (git show; written to .scratch/ar186/; NO READER_VERSION,
                  and read_template writes NO reader_version member).
  new           = intake/template_reader.py at the worktree HEAD (READER_VERSION irpt-template-reader.r18.1, AR-y-181).
Pairs (writer, reader): (lambda_pinned, lambda_pinned), (lambda_pinned, new), (new, lambda_pinned), and the same-version
control (new, new). Inputs: the seven AR-y-174 sheets plus one AR-y-181 vocabulary sheet (Brokerage Account, two accounts).

Two measurements per case, both in process and offline (no network, no AWS, no send, no deploy, no invoke):
  1. The upload door and the in-world re-open: the repository's offline upload world (intake/tests/test_template_uploads.py)
     with HEAD's uploads.py; only the reader module is swapped in sys.modules, as in AR-y-174.
  2. The reader-level re-open under the Lambda's own uploads.py (pin f09b802cdc), read as code: its read_input re-reads the
     retained original with the RUNNING reader and refuses (TEMPLATE_ORIGINAL_BINDING) when the result differs from the
     stored template in ANY member (no version gate). Computed as a direct comparison of the two reader outputs.

Run:  cd <worktree>/infra/aws/lambda/investor-reporting/intake && python -m pytest <this file> -q -p no:cacheprovider
Writes: MIXED_VERSION_TRACE_THIRD_READER.json beside this file.
"""
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
PIN = "3f29017cfc"
SCRATCH = WT / ".scratch" / "ar186"
OUT = Path(__file__).resolve().parent / "MIXED_VERSION_TRACE_THIRD_READER.json"
sys.path[:0] = [str(INTAKE / "tests"), str(INTAKE)]

import test_template_uploads as tu  # noqa: E402
from security_resolution import classify_batch  # noqa: E402
from test_template_reader import rows, workbook  # noqa: E402
from uploads import UploadRefused  # noqa: E402

PAIRS = [("lambda_pinned", "lambda_pinned"), ("lambda_pinned", "new"), ("new", "lambda_pinned"), ("new", "new")]
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
    ("brokerage_two_account", "csv", lambda: b"Ticker,Dollars,Brokerage Account\nAAA,100,ACCT-ONE\nBBB,200,ACCT-TWO\n"),
]
EXPECT_NEW = "irpt-template-reader.r18.1"

CLAIM = (
    "Four writer/reader pairs over eight synthetic sheets (32 cases), including the same-version control (new, new). "
    "The Lambda's reader (lambda_pinned, pin 3f29017cfc) has NO account check and NO total-row check: it returns no finding "
    "on the three two-account sheets (two_value_account_sheet, repair_header_two_values, brokerage_two_account) or on the "
    "total-row sheet, so it holds the file's rows with the account column ignored, and reads the total row as a holding "
    "named TOTAL. Reader r18.1 turns back the four of those (ACCOUNT_COLUMN_SEVERAL_VALUES or TOTAL_ROW_PRESENT) and "
    "accepts the four one-account and one-workbook inputs (NORMALIZED in the world). Re-open under the Lambda's pinned "
    "read_input (computed on the two reader outputs): a template stored by r18.1 is REFUSED (TEMPLATE_ORIGINAL_BINDING) "
    "in 4 of 4 valid cases (two_sheet_workbook, one_account_sheet, repair_header_one_value, attribute_header_one_account); "
    "in 3 of 4 the two reader outputs are equal except the reader_version member, so that member alone causes the "
    "refusal; the fourth also lacks the SHEETS_NOT_READ notice. A template stored by the pinned reader is ACCEPTED by "
    "r18.1's read_input in 8 of 8 (computed: the gate does not compare a template with no version member). With HEAD's "
    "uploads.py, the pinned reader raises ImportError on READER_VERSION in every case where it is writer or reader "
    "(24 of 24 in the world: a loud failure, not a silent one). The control (new, new) is accepted on every re-open. "
    "A READER-ONLY move (the pinned uploads with the r18.1 reader) refuses 8 of 8 templates stored by the pinned reader "
    "(computed: the pinned read_input compares every member, with no version gate). So the start state of the release pair "
    "must move uploads.py and template_reader.py together. NOT SHOWN: the Lambda's own door and its answers (uploads f09b802cdc is read as code, not run), the resident's "
    "installed copy, the queue between the two runtimes, the request_resolution path."
)

NOT_READ = [
    "the Lambda's own door: uploads.py at pin f09b802cdc (create :371-425, _normalized answer) was read as code only; its "
    "door answers for the eight sheets are INFERRED from the reader output, not run",
    "the Lambda's deployed bytes and package: no host call; the pinned file's sha256 (76795b75...) matches the source map, "
    "read through git show only",
    "the resident's installed package and its pin: ycharts/generate/install-resident.sh and reports/build_resident_package.py "
    "read as code only; the resident's installed template_reader.py was not read",
    "the queue between the Lambda and the resident (the resolution message and its replay): not run, not read",
    "the request_resolution path (uploads.py:400-402, _defer, resolve_deferred:521-567): not run",
    "the Lambda's uploads.py and its neighbours executed: the in-world harness runs HEAD's uploads.py; the pinned uploads "
    "read_input gate is applied to the two reader outputs in process, not run through the pinned module",
    "the live provider: resolve_template is mocked (every symbol FOUND); no securities_info call, no network",
    "any real upload, stored artifact or live row: none read",
    "two different accounts holding the SAME symbol (a DUPLICATE_SYMBOL_MERGED across accounts): not run; the synthetic "
    "sheets hold distinct symbols per account",
    "the words a portal shows for each code (only the state, the reason and the codes were recorded)",
    "other Lambdas that import template_reader without listing it (the source map's import-closure gate covers the listed ones)",
]

WHAT_A_PERSON_SEES = (
    "Lambda on the pinned pair (uploads f09b802cdc, reader 3f29017cfc) and the resident on r18.1. (1) A person who "
    "re-opens, submits or refreshes an input that r18.1 stored from a VALID single-account file sees a refusal, "
    "TEMPLATE_ORIGINAL_BINDING, computed on the two readers: 4 of 4 measured, 3 of them with no difference except the "
    "reader_version member. (2) A person who uploads a two-account file to the pinned reader gets no finding: the file is "
    "held as one account's rows with no account separation, and a total row is held as a holding named TOTAL (computed; the "
    "Lambda's own door answer is not run). (3) A person who re-opens an input the pinned reader stored, under r18.1 with HEAD's "
    "uploads, sees it accepted unchanged, with no re-read (8 of 8 computed; the gate does not compare a template with no "
    "version member), so the widening does not turn back inputs stored before the release. (4) HEAD's uploads with the pinned "
    "reader: every template answer raises an internal ImportError in the world (24 of 24 cases), a loud failure. "
    "Can an input accepted under one reader be refused under the other at re-open? YES, one direction: r18.1-stored valid "
    "inputs are refused by the pinned pair (4 of 4). The other direction refused none (8 of 8). "
    "Not measured: the words a portal shows for each code."
)

VERSIONS = {}
MODS = {}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_pinned():
    got = subprocess.run(["git", "-C", str(WT), "show", PIN + ":" + REL], capture_output=True)
    if got.returncode != 0 or not got.stdout:
        raise RuntimeError("git show failed: rc=%s" % got.returncode)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    path = SCRATCH / "template_reader_3f29017cfc.py"
    path.write_bytes(got.stdout)
    module = load("template_reader_lambda_pinned_under_test", path)
    VERSIONS["lambda_pinned"] = {
        "pin": PIN, "source": "git show " + PIN + ":" + REL + " written to .scratch/ar186/ (outside the product tree)",
        "sha256_of_file": hashlib.sha256(got.stdout).hexdigest(),
        "READER_VERSION_defined": hasattr(module, "READER_VERSION"),
        "reader_version_member_written": None,
    }
    return module


def load_new():
    path = INTAKE / "template_reader.py"
    module = load("template_reader_r18_under_test", path)
    VERSIONS["new"] = {
        "pin": "worktree HEAD (AR-y-181 commit da7b3b10bc)", "source": "worktree " + REL,
        "sha256_of_file": hashlib.sha256(path.read_bytes()).hexdigest(),
        "READER_VERSION_defined": hasattr(module, "READER_VERSION"),
        "reader_version": getattr(module, "READER_VERSION", None),
    }
    assert module.READER_VERSION == EXPECT_NEW, module.READER_VERSION
    return module


MODS["lambda_pinned"] = load_pinned()
MODS["new"] = load_new()


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


def reader_level(module, data, file_type):
    res = module.read_template(data, file_type)
    return res, ["%s:%s" % (f.get("code"), f.get("severity")) for f in res.get("findings", []) if isinstance(f, dict)]


def version_member(res):
    return res.get("reader_version", "ABSENT")


def strip_version(template):
    return {k: v for k, v in template.items() if k != "reader_version"}


def head_gate(w_res, R, r_res):
    """The HEAD read_input gate (uploads.py:633-641) applied to the two reader outputs, in process."""
    if not hasattr(R, "READER_VERSION"):
        return "ERROR ImportError (computed: the running reader has no READER_VERSION; uploads.py:633 imports it)"
    stored_version = w_res.get("reader_version", "before-C-STOREDINPUT")
    if stored_version == R.READER_VERSION:
        return "ACCEPTED" if r_res == w_res else "REFUSED TEMPLATE_ORIGINAL_BINDING"
    return "ACCEPTED (not compared: stored %s, running %s)" % (stored_version, R.READER_VERSION)


def pinned_uploads_gate(w_res, r_res):
    """The Lambda's own read_input (uploads.py at pin f09b802cdc, lines 533-541), read as code: no version gate."""
    return "ACCEPTED" if r_res == w_res else "REFUSED TEMPLATE_ORIGINAL_BINDING"


def run_case(writer, reader, label, file_type, data):
    W, R = MODS[writer], MODS[reader]
    case = fresh_case()
    body = tu.payload(data, file_type, upload_token="ar186-%s-%s-%s" % (writer, reader, label))
    w_res, w_codes = reader_level(W, data, file_type)
    r_res, r_codes = reader_level(R, data, file_type)
    with reader_as(W):
        first = attempt(lambda: case.create(body))
    row = {"writer_version": writer, "reader_version": reader, "input": label, "file_type": file_type,
           "writer_reader_version_member": version_member(w_res), "reader_reader_version_member": version_member(r_res),
           "writer_reader_level_codes": w_codes, "reader_reader_level_codes": r_codes,
           "writer_symbols": [r.get("symbol") for r in w_res.get("rows", [])],
           "reader_symbols": [r.get("symbol") for r in r_res.get("rows", [])],
           "reader_output_equal_ignoring_version_member": strip_version(r_res) == strip_version(w_res),
           "computed_reopen_lambda_pinned_uploads": pinned_uploads_gate(w_res, r_res),
           "computed_reopen_head_uploads_gate": head_gate(w_res, R, r_res)}
    row["writer_door"] = door_text(first)
    row["writer_codes"] = codes_of(first["answer"]) if first.get("ok") else []
    stored = bool(first.get("ok")) and first["answer"].get("state") == "NORMALIZED"
    if stored:
        answer = first["answer"]
        template = answer["portfolio"]["template"]
        row["stored_template_equals_writer_reader_level_output"] = (template == w_res)
        row["stored_reader_version_member"] = template.get("reader_version", "ABSENT")
        with reader_as(R):
            reopen = attempt(lambda: case.service.read_input(case.principal, case.owner, answer["input_id"]))
        equal = bool(reopen.get("ok")) and reopen["answer"]["document"] == answer["portfolio"]
        row["reopen_head_world"] = reopen_text(reopen, equal)
        row["reopen_lambda_pinned_uploads_reader_level"] = (
            "REFUSED TEMPLATE_ORIGINAL_BINDING" if r_res != template else "ACCEPTED")
    else:
        row["stored_template_equals_writer_reader_level_output"] = None
        row["stored_reader_version_member"] = None
        row["reopen_head_world"] = "not run: the writer stored nothing"
        row["reopen_lambda_pinned_uploads_reader_level"] = "not run: the writer stored nothing"
    with reader_as(R):
        repost = attempt(lambda: case.create(body))
    row["repost_same_token_under_reader"] = door_text(repost)
    row["repost_codes"] = codes_of(repost["answer"]) if repost.get("ok") else []
    row["outcome"] = (
        "%s writer, %s reader, %s: in-world door %s; reader-level codes %s; %s; re-open under the Lambda's pinned "
        "uploads (computed on the two reader outputs): %s; re-open under HEAD uploads gate (computed): %s; "
        "in-world re-open: %s; in-world same-token re-POST: %s"
        % (writer, reader, label, row["writer_door"], r_codes, "stored" if stored else "NOT STORED",
           row["computed_reopen_lambda_pinned_uploads"], row["computed_reopen_head_uploads_gate"],
           row["reopen_head_world"], row["repost_same_token_under_reader"]))
    row["evidence"] = ("in process, offline upload world (tests/test_template_uploads.py), synthetic sheet %s (%s); "
                       "writer %s = %s (member %s); reader %s = %s (member %s); writer reader-level codes %s; "
                       "reader-level codes %s; stored template equals writer output %s; stored member %s; "
                       "re-POST codes %s"
                       % (label, file_type, writer, MODS[writer].__name__, row["writer_reader_version_member"],
                          reader, MODS[reader].__name__, row["reader_reader_version_member"], w_codes, r_codes,
                          row["stored_template_equals_writer_reader_level_output"], row["stored_reader_version_member"],
                          row["repost_codes"]))
    return row


def test_the_pairs_in_process_and_the_trace_record():
    cases = []
    for writer, reader in PAIRS:
        for label, file_type, make in INPUTS:
            cases.append(run_case(writer, reader, label, file_type, make()))
    trace = {
        "to_id": "IRPT_ANLREQ.TO-AR-y-186",
        "cell": "AR-y-186",
        "pin": PIN,
        "pin_is_the_lambda_reader": ("irpt-ycharts-generate packages template_reader.py at 3f29017cfc (lambda-source-map.json "
                                     "lines 4559-4564) beside uploads.py at f09b802cdc (lines 4542-4546); sha256 of the "
                                     "pinned file 76795b75... matches the map; it has NO READER_VERSION and writes NO "
                                     "reader_version member"),
        "method": ("in-process runs of four writer/reader pairs over eight synthetic sheets (the seven AR-y-174 sheets "
                   "and a Brokerage Account two-account sheet). The in-world door and re-open use HEAD's uploads.py with the "
                   "version switch sys.modules['template_reader']. The reader-level columns are computed in process on the "
                   "two reader outputs: the Lambda's pinned read_input (f09b802cdc, read as code: full comparison, no version "
                   "gate) and HEAD's read_input gate (uploads.py:633-641). Nothing is called over a network."),
        "versions": VERSIONS,
        "cases": cases,
        "inferred": [
            "in-world door and re-open with the PINNED reader as writer or reader: HARNESS-ERROR ImportError, "
            "cannot import name 'READER_VERSION' (HEAD uploads.py:633 imports it; the pinned reader has none). This is a "
            "PAIRING artifact of HEAD's uploads with the pinned reader; the Lambda's own uploads.py (f09b802cdc) has no "
            "READER_VERSION import (read as code). Its door answer for these sheets is INFERRED from the reader output "
            "alone (no ERROR-severity finding on any of the eight sheets), not run",
            "the Lambda's own door (uploads.py f09b802cdc create, :371-425) and its own read_input: computed on the reader "
            "outputs, not run through that module",
            "stored-before-release templates (written by the pinned reader) re-opened under r18.1 in the HEAD world: the gate "
            "does not compare them (stored_version absent), so ACCEPTED is INFERRED from uploads.py:633-641, not run in "
            "the world (the pinned writer's door cannot run there)",
        ],
        "release_precondition": (
            "The release pair must state its START STATE as uploads.py at f09b802cdc plus template_reader.py at 3f29017cfc, "
            "with NO reader_version member on any stored template, and it must move BOTH files in ONE deploy to HEAD and "
            "r18.1. Each single-file move is measured as a failure: uploads-only (HEAD uploads with the pinned reader) raises "
            "ImportError on every template answer (24 of 24 in the world); reader-only (the pinned uploads with r18.1) refuses "
            "8 of 8 templates stored by the pinned reader at re-open (computed)."),
        "claim": CLAIM,
        "not_read": NOT_READ,
        "what_a_person_sees": WHAT_A_PERSON_SEES,
    }
    OUT.write_text(json.dumps(trace, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print("cases written: %d -> %s" % (len(cases), OUT.name))
    for row in cases:
        print("%s/%s %-30s door=%s | pinned-uploads-reopen=%s | head-reopen=%s | repost=%s" % (
            row["writer_version"], row["reader_version"], row["input"], row["writer_door"],
            row["reopen_lambda_pinned_uploads_reader_level"], row["reopen_head_world"],
            row["repost_same_token_under_reader"]))
    assert len(cases) == len(PAIRS) * len(INPUTS)
