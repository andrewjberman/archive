"""AR-y-191: the Lambda's start state RUN in a scratch tree (in-process, offline; no network, no AWS, no send, no deploy).

Usage: python start_state_run.py <scratch_root> <worktree_root> <record_out.json>
  <scratch_root>/mirror   the 88 staged_from members at their map pins, at repo-relative paths, plus the offline test world
  <scratch_root>/head     HEAD uploads.py and template_reader.py (the planned move's two files; READER_VERSION r18.1)
The door and the re-opens run the REAL pinned uploads.py (f09b802cdc) through its UploadService.create / read_input, with the
pinned reader (3f29017cfc) swapped in as sys.modules['template_reader'] (as the round-18 harness did). The fixtures (the
offline storage doubles, payload, fresh_case, the four-plus-four sheets) are extracted by AST from the round-18 harness and
from the HEAD test modules, not retyped.
"""
import ast
import base64
import copy
import hashlib
import importlib.util
import json
import re
import sys
import types
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock, patch

SCR, WT, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
MIRROR, HEAD_DIR = SCR / "mirror", SCR / "head"
INTAKE = MIRROR / "infra/aws/lambda/investor-reporting/intake"
HARNESS = WT / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r18/mixed_version_trace_third_reader.py"
PINS_MANIFEST = json.load(open(SCR / "tools" / "tree_manifest.json", encoding="utf-8"))
MIRROR_MANIFEST = json.load(open(SCR / "tools" / "mirror_manifest.json", encoding="utf-8"))

sys.path[:] = [p for p in sys.path if not p or Path(p).resolve() != (SCR / "tools").resolve()]
sys.path.insert(0, str(INTAKE / "tests"))
import test_uploads as legacy  # noqa: E402  (inserts mirror intake, _authz, _scope, _ids; loads mirror reports/repository.py)
from security_resolution import classify_batch  # noqa: E402
from test_template_reader import rows, workbook  # noqa: E402


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


uploads_pinned = load("uploads_pinned_f09b802cdc", INTAKE / "uploads.py")
reader_pinned = load("template_reader_pinned_3f29017cfc", INTAKE / "template_reader.py")
uploads_head = load("uploads_head", HEAD_DIR / "uploads_HEAD.py")
reader_head = load("template_reader_head", HEAD_DIR / "template_reader_HEAD.py")
assert not hasattr(reader_pinned, "READER_VERSION"), "pinned reader must carry no READER_VERSION"
assert reader_head.READER_VERSION == "irpt-template-reader.r18.1", reader_head.READER_VERSION
controls = {
    "uploads_pinned_file": str(uploads_pinned.__file__), "uploads_pinned_sha256": sha(uploads_pinned.__file__),
    "reader_pinned_file": str(reader_pinned.__file__), "reader_pinned_sha256": sha(reader_pinned.__file__),
    "reader_pinned_has_READER_VERSION": hasattr(reader_pinned, "READER_VERSION"),
    "uploads_head_file": str(uploads_head.__file__), "uploads_head_sha256": sha(uploads_head.__file__),
    "reader_head_file": str(reader_head.__file__), "reader_head_sha256": sha(reader_head.__file__),
    "reader_head_READER_VERSION": reader_head.READER_VERSION,
    "uploads_pinned_matches_map": sha(uploads_pinned.__file__) == PINS_MANIFEST["members"]["uploads.py"]["sha256"],
    "reader_pinned_matches_map": sha(reader_pinned.__file__) == PINS_MANIFEST["members"]["template_reader.py"]["sha256"],
    "uploads_head_matches_HEAD_bytes": sha(uploads_head.__file__) == sha(HEAD_DIR / "uploads_HEAD.py"),
}
assert controls["uploads_pinned_matches_map"] and controls["reader_pinned_matches_map"], controls


# --- the harness's own fixtures, extracted by AST from the round-18 harness and from the HEAD test module ---
def extract(path, names, ns, assigns=()):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    got = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module([node], []), str(path), "exec"), ns)
            got.append(node.name)
        elif isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) in assigns:
            exec(compile(ast.Module([node], []), str(path), "exec"), ns)
            got.append(node.targets[0].id)
    missing = set(names) | set(assigns)
    missing -= set(got)
    assert not missing, missing
    return got


ns = {"Mock": Mock, "classify_batch": classify_batch, "workbook": workbook, "rows": rows, "base64": base64, "copy": copy,
      "json": json, "re": re}
extract(HARNESS, ("fresh_case", "door_text", "reopen_text", "codes_of", "version_member"), ns, assigns=("INPUTS",))
tu_ns = {"base64": base64}
extract(INTAKE / "tests" / "test_template_uploads.py", ("payload",), tu_ns)
ns["tu"] = types.SimpleNamespace(legacy=legacy, payload=tu_ns["payload"])
fresh_case, door_text, reopen_text, codes_of = ns["fresh_case"], ns["door_text"], ns["reopen_text"], ns["codes_of"]
INPUTS = list(ns["INPUTS"]) + [("header_repeated_csv", "csv", lambda: b"Ticker,Dollars\nAAA,100\nTicker,Dollars\nBBB,200\n")]  # r19 ADDED HERE: constructed, not in the ~52 record


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


def attempt(call):
    try:
        return {"ok": True, "answer": call()}
    except Exception as exc:  # recorded, never hidden
        if type(exc).__name__ == "UploadRefused":
            return {"ok": False, "refused": str(exc)}
        return {"ok": False, "error": "%s: %s" % (type(exc).__name__, str(exc)[:200])}


PINNED = {"name": "pinned pair (uploads f09b802cdc + reader 3f29017cfc)", "short": "pinned pair",
          "uploads": uploads_pinned, "reader": reader_pinned}
MOVED = {"name": "moved pair (uploads HEAD + reader HEAD r18.1)", "short": "moved pair",
         "uploads": uploads_head, "reader": reader_head}
READER_ONLY = {"name": "reader-only move (uploads f09b802cdc + reader HEAD r18.1)", "short": "reader-only",
               "uploads": uploads_pinned, "reader": reader_head}


def make_case(config):
    with patch.object(legacy, "UploadService", config["uploads"].UploadService):
        return fresh_case()


def door(config, file_type, data, token):
    case = make_case(config)
    body = ns["tu"].payload(data, file_type, upload_token=token)
    with reader_as(config["reader"]):
        res = attempt(lambda: case.create(body))
    return case, body, res


def reader_codes(module, data, file_type):
    res = module.read_template(data, file_type)
    return res, ["%s:%s" % (f.get("code"), f.get("severity")) for f in res.get("findings", []) if isinstance(f, dict)]


def code_of(text):
    m = re.search(r"\b([A-Z][A-Z_]{5,})\b", text)
    return m.group(1) if m else text[:80]


door_cases, reopen_cases, all_rows = [], [], []
BODIES = {}
stored = {}
for label, file_type, make in INPUTS:
    data = make()
    rd, rcodes = reader_codes(reader_pinned, data, file_type)
    case, body, res = door(PINNED, file_type, data, "ar191-door-pinned-%s" % label)
    outcome = door_text(res)
    ans = res.get("answer") if res.get("ok") else None
    evidence = {
        "reader_level_pinned_codes": rcodes,
        "reader_level_pinned_symbols": [r.get("symbol") for r in rd.get("rows", [])],
        "reader_level_pinned_sheet": rd.get("sheet"),
        "reader_level_pinned_reader_version_member": rd.get("reader_version", "ABSENT"),
        "uploads_pinned_file_sha256": controls["uploads_pinned_sha256"][:12],
        "reader_pinned_file_sha256": controls["reader_pinned_sha256"][:12],
        "door_answer_codes": codes_of(ans) if ans else [],
        "door_error": res.get("error"),
        "door_refused": res.get("refused"),
    }
    if ans:
        evidence["state"] = ans.get("state")
        evidence["reason"] = ans.get("reason")
        evidence["stored_template_reader_version_member"] = (ans.get("portfolio") or {}).get("template", {}).get("reader_version", "ABSENT")
        evidence["total_dollars"] = ((ans.get("portfolio") or {}).get("holdings") or {}).get("total_dollars")
        evidence["row_count"] = len(((ans.get("portfolio") or {}).get("rows")) or [])
        stored[label] = (file_type, data, body, ans)
    if ans:
        prow = (ans.get("portfolio") or {}).get("rows") or []
        evidence["row_keys"] = sorted(prow[0].keys()) if prow else []
        evidence["row_account_values"] = sorted({str(r.get("account")) for r in prow if "account" in r})
    BODIES[(label, "pinned")] = {"res": res, "answer": ans}
    door_cases.append({"sheet": label, "file_type": file_type, "door": "pinned pair", "outcome": outcome,
                       "evidence": "pinned door, in-world offline upload world: %s; %s" % (
                           outcome, json.dumps(evidence, sort_keys=True))})

    # the moved pair's writer door on the same sheet (r18.1 stores; needed for the write-with-r18.1 re-open)
    mcase, mbody, mres = door(MOVED, file_type, data, "ar191-door-moved-%s" % label)
    mans = mres.get("answer") if mres.get("ok") else None
    mrd, mrcodes = reader_codes(reader_head, data, file_type)
    mevidence = {"reader_level_moved_codes": mrcodes, "door_answer_codes": codes_of(mans) if mans else [],
                 "door_error": mres.get("error"), "door_refused": mres.get("refused"),
                 "state": (mans or {}).get("state"), "reason": (mans or {}).get("reason")}
    BODIES[(label, "moved")] = {"res": mres, "answer": mans}
    door_cases.append({"sheet": label, "file_type": file_type, "door": "moved pair", "outcome": door_text(mres),
                       "evidence": "moved door (HEAD uploads, r18.1 reader), in-world offline upload world: %s; %s" % (
                           door_text(mres), json.dumps(mevidence, sort_keys=True))})
    if mans and mans.get("state") == "NORMALIZED":
        stored.setdefault(("moved", label), (file_type, data, mbody, mans, mcase))

    # the four re-open pairs (writer -> reader), each on the same fake storage
    for wlabel, writer_cfg, wans, wcase, wbody in (
            ("pinned pair", PINNED, ans, case, body),
            ("moved pair", MOVED, mans, mcase, mbody)):
        if not wans or wans.get("state") != "NORMALIZED":
            continue
        for rconfig in (PINNED, MOVED, READER_ONLY):
            svc_case = wcase
            with patch.object(legacy, "UploadService", rconfig["uploads"].UploadService):
                svc = svc_case.new_service()
            svc.artifacts.families |= {"ORIGINAL_HOLDINGS"}
            with reader_as(rconfig["reader"]):
                reopen = attempt(lambda: svc.read_input(svc_case.principal, svc_case.owner, wans["input_id"]))
                repost = attempt(lambda: svc.create(svc_case.principal, svc_case.owner, wbody))
            if reopen.get("ok"):
                equal = reopen["answer"]["document"] == wans["portfolio"]
                rout = "ACCEPTED (document equal to stored portfolio: %s)" % equal
            elif "refused" in reopen:
                rout = "REFUSED %s" % code_of(reopen["refused"])
            else:
                rout = "HARNESS-ERROR %s" % reopen.get("error")
            rep = door_text(repost)
            member = (wans.get("portfolio") or {}).get("template", {}).get("reader_version", "ABSENT")
            reopen_cases.append({
                "sheet": label, "file_type": file_type, "writer": writer_cfg["name"], "reader": rconfig["name"],
                "writer_stored_reader_version_member": member, "outcome": rout,
                "evidence": ("writer %s stored %s (input %s, reader_version member %s); re-open read_input under %s = %s; "
                             "re-POST same token under the reader: %s" % (
                                 writer_cfg["short"], label, wans["input_id"], member, rconfig["short"], rout, rep)),
                "reopen_raw": reopen.get("refused") or reopen.get("error") or "ok",
            })

from collections import OrderedDict  # noqa: E402
matrix = OrderedDict()
for r in reopen_cases:
    key = "%s -> %s" % (r["writer"].split(" (")[0], r["reader"].split(" (")[0])
    cell = matrix.setdefault(key, {"accepted": 0, "refused": 0, "other": 0, "total": 0})
    cell["total"] += 1
    if r["outcome"].startswith("ACCEPTED"):
        cell["accepted"] += 1
    elif r["outcome"].startswith("REFUSED"):
        cell["refused"] += 1
    else:
        cell["other"] += 1
CLAIM = (
    "RUN, not inferred, on python 3.12.10 (the Lambda's runtime). The start state is uploads.py f09b802cdc with template_reader.py "
    "3f29017cfc, staged from git show of the map's pins: 88 of 88 staged members sha256-match lambda-source-map.json. The upload "
    "door's import closure is 27 members, every one staged; no import reached from the door is unstaged. "
    "DOOR, the pinned pair (UploadService.create of the real pinned uploads.py, in the round-18 offline world, fakes extracted by AST): "
    "NORMALIZED on 8 of 8 synthetic sheets with NO finding. The three two-account sheets are not turned back; their held rows carry "
    "no account field (row_account_values empty) and the total is the sum across both accounts (300). total_row_sheet is NORMALIZED "
    "with three holdings (AAA, BBB, TOTAL) and total 600, the file's total row counted as a holding. "
    "RE-OPEN (read_input of the real pinned uploads.py and of HEAD uploads.py): see reopen_matrix. A template stored by the pinned pair "
    "is ACCEPTED under the pinned pair and under the moved pair (uploads HEAD + reader r18.1), and REFUSED TEMPLATE_ORIGINAL_BINDING "
    "under the reader-only move. A template stored by the moved pair is REFUSED TEMPLATE_ORIGINAL_BINDING under the pinned pair (the "
    "four sheets the moved door stores) and ACCEPTED under the moved pair. The moved door turns back four sheets (two_value_account_sheet, "
    "repair_header_two_values, brokerage_two_account: ACCOUNT_COLUMN_SEVERAL_VALUES; total_row_sheet: TOTAL_ROW_PRESENT). "
    "AGAINST ROUND 18: every comparable case agrees with the round-18 trace on its leading outcome (44 of 44 compared cases, the "
    "comparison script in r19/scratch_tools). The round-18 computed rows for the four inputs the moved door does not store have no "
    "stored template to re-open; the round-18 claim covered the four valid inputs only, and those match. The Lambda's own door, "
    "INFERRED in round 18, is now RUN and answers NORMALIZED on all eight sheets, as inferred. "
    "NOT SHOWN: the deployed Lambda's bytes and package (no host call, no live object read; the package zip was not built or hashed; the "
    "map's artifact_sha256 is the map's own claim); the HTTP route upload_entry.handle; the resident's installed copy; the queue between "
    "the runtimes; the request_resolution path."
)
NOT_READ = [
    "the deployed Lambda: no host call, no live object read, the package zip not built or hashed here; the map's artifact_sha256 and "
    "deployed_code_sha256 are taken from the map and are not measured by this run",
    "the HTTP route: the door was run as UploadService.create (the offline harness's own entry, as round 18 did); upload_entry.handle and "
    "its guard were not run",
    "the resident's installed package (ycharts/generate/install-resident.sh and reports/build_resident_package.py) and its template_reader "
    "copy: not read",
    "the queue between the Lambda and the resident, and the request_resolution path (uploads.py 400-402, _defer, resolve_deferred): not run",
    "door-closure members that differ between their pins and HEAD: ids.py, loaders.py, repository.py and served.py, in addition to uploads.py "
    "and template_reader.py. The moved pair keeps those four at their pins, as the planned move names only two files; the HEAD-complete "
    "world was not run (surprise row IRPT_ANLREQ-D2-W52-S37)",
    "unstaged names: acceptance.py, submission.py, submission_service.py, durable_job.py, comparison_catalogue.py, recipe_snapshot.py and "
    "custody_submission.py are not staged and are not on the door's closure; they are reached only from generate_installed.py and entry.py, "
    "which the door does not import. opal_naming is imported lazily by served.py:279 (served.py inserts lib/ itself) and by "
    "maintained_sources.py:660 (not checked); neither is on the template door path that ran",
    "the live provider: resolve_template is mocked with the offline receipt; no securities_info call, no network",
    "any real upload, stored artifact or live row: none read",
    "the words a portal shows for each code (codes and states only were recorded)",
    "the runtime: the run used python 3.12.10 (the Lambda's runtime); a run on the default python 3.14.7 gave identical door and re-open outcomes",
]
WHAT_A_PERSON_SEES = (
    "Today, through the pinned door (uploads f09b802cdc, reader 3f29017cfc), a person who uploads a two-account file (two_value_account_sheet: "
    "AAA 100 on ACCT-ONE, BBB 200 on ACCT-TWO) is told NORMALIZED with no finding. The answer holds two holdings with no account on either "
    "row, and a total of 300, the sum across both accounts; nothing says the file held two accounts. A person who uploads a file with a total "
    "row (total_row_sheet) is told NORMALIZED with three holdings, the third named TOTAL, and a total of 600, which counts the file's own "
    "total of 300 as a holding. A person who re-opens an input the pinned pair stored sees it accepted unchanged under the pinned pair and "
    "under the moved pair. An input the moved pair stored (r18.1) is refused on re-open under the pinned pair with TEMPLATE_ORIGINAL_BINDING. "
    "Not measured: the words a portal shows for each code, and the HTTP route's answer."
)
record = {
    "to_id": "IRPT_ANLREQ.TO-AR-y-191",
    "cell": "AR-y-191",
    "issued_to": "0.9.0_WK_IRPT_ANLREQ~52",
    "scratch_tree": str(SCR),
    "scratch_tree_layout": {"lambda_flat": str(SCR / "lambda_flat"), "mirror_repo_paths": str(MIRROR),
                            "head_files": str(HEAD_DIR), "tools": str(SCR / "tools")},
    "pins": {k: PINS_MANIFEST["members"][k]["pin"] for k in PINS_MANIFEST["door_closure"]},
    "door_closure": PINS_MANIFEST["door_closure"],
    "door_closure_members_differing_from_head": MIRROR_MANIFEST["door_members_differing_from_head"],
    "controls": controls,
    "runtime": "python %s (%s)" % (sys.version.split()[0], "the Lambda's runtime python3.12" if sys.version.startswith("3.12") else "NOT the Lambda's python3.12"),
    "door_cases": door_cases,
    "reopen_cases": reopen_cases,
    "reopen_matrix": matrix,
    "claim": CLAIM,
    "not_read": NOT_READ,
    "what_a_person_sees": WHAT_A_PERSON_SEES,
    "inferred": [
        "the deployed Lambda's code equals the staged pins: INFERRED from lambda-source-map.json (artifact_sha256 and deployed_code_sha256 "
        "as the map records them); no live CodeSha256 was read and the package was not built, because the order makes no AWS call. "
        "Every door and re-open case in this record was RUN in process; none is inferred.",
    ],
}
BODIES_OUT = OUT.parent / "answer_bodies.json"
BODIES_OUT.write_text(json.dumps({"%s|%s" % k: v for k, v in BODIES.items()}, indent=1, sort_keys=True, default=str, ensure_ascii=True) + chr(10), encoding="utf-8")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(record, indent=1, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
print("door cases %d, re-open cases %d -> %s" % (len(door_cases), len(reopen_cases), OUT))
for d in door_cases:
    print("door  %-28s %s" % (d["sheet"], d["outcome"]))
for r in reopen_cases:
    print("reopen %-28s writer=%-12s reader=%-11s -> %s" % (r["sheet"], r["writer"][:12], r["reader"][:11], r["outcome"]))
