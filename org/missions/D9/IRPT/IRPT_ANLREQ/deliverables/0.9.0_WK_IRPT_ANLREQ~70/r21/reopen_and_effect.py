"""AR-y-226: the re-open matrix and the effect table of the r18.1 reader (pinned) against the r19.3 reader (moved).

Usage: python reopen_and_effect.py <scratch_root> <worktree_root> <record_out.json>
  <scratch_root>/pinned/infra/aws/lambda/investor-reporting  a copy of HEAD with intake/template_reader.py at the r18.1 blob
  <scratch_root>/moved/infra/aws/lambda/investor-reporting   a copy of HEAD (template_reader.py at the r19.3 blob)
Both trees carry intake/uploads.py at HEAD (sha256 176682cb...). The scratch copies are made by git archive (see the record).
Run in process. Nothing is uploaded, deployed, applied or called. The door, the stores and the re-opens run the REAL
uploads.py through UploadService.create and read_input, with the offline storage doubles of the round-18 harness
(fresh_case, payload and the eight INPUTS are extracted by AST from that harness, not retyped).
"""
import ast
import base64
import csv
import hashlib
import importlib.util
import io
import json
import platform
import sys
import types
from collections import OrderedDict
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock, patch

sys.dont_write_bytecode = True
SCR, WT, OUT = (Path(a) for a in sys.argv[1:4])
TREE = "infra/aws/lambda/investor-reporting"
PIN, MOV = SCR / "pinned" / TREE / "intake", SCR / "moved" / TREE / "intake"
DELIV = WT / "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables"
HARNESS = DELIV / "0.9.0_WK_IRPT_ANLREQ~52/r18/mixed_version_trace_third_reader.py"
CHECKS = DELIV / "2.0.0_SA_COO~Y2/checks/r21/ar21_checks.py"
R181_SHA = "83ab9b45d59065f53c640803df9fd07a0ddfcc97d89c13540c20622a6bf7bd58"
UPLOADS_SHA = "176682cb1545435eec084376b3c37a578ca70d05f9ad5a376c0f2275f62b05ea"
R181_COMMIT = "da7b3b10bce3953f7b7072d9775a8f82961b5fac"
R193_COMMIT = "55d1755d3934f362702797e034cee032b8be6247"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- the two readers and the two uploads.py files, from the scratch trees ---
sys.path[:0] = [str(MOV / "tests"), str(MOV)]
import test_uploads as legacy  # noqa: E402  (the round-18 test module: fixtures and the offline storage double)
from security_resolution import classify_batch  # noqa: E402
from test_template_reader import rows, workbook  # noqa: E402

uploads_pinned = load("uploads_pinned_tree", PIN / "uploads.py")
reader_pinned = load("template_reader_pinned_tree", PIN / "template_reader.py")
uploads_moved = load("uploads_moved_tree", MOV / "uploads.py")
reader_moved = load("template_reader_moved_tree", MOV / "template_reader.py")
CONTROLS = {
    "pinned_reader_sha256": sha(PIN / "template_reader.py"), "pinned_uploads_sha256": sha(PIN / "uploads.py"),
    "moved_reader_sha256": sha(MOV / "template_reader.py"), "moved_uploads_sha256": sha(MOV / "uploads.py"),
    "pinned_reader_version": reader_pinned.READER_VERSION, "moved_reader_version": reader_moved.READER_VERSION,
    "harness_sha256": sha(HARNESS), "checks_sha256": sha(CHECKS), "python": platform.python_version(),
}
assert CONTROLS["pinned_reader_sha256"] == R181_SHA, CONTROLS
assert CONTROLS["pinned_uploads_sha256"] == UPLOADS_SHA and CONTROLS["moved_uploads_sha256"] == UPLOADS_SHA, CONTROLS
assert CONTROLS["pinned_reader_version"] == "irpt-template-reader.r18.1", CONTROLS
assert CONTROLS["moved_reader_version"] == "irpt-template-reader.r19.3", CONTROLS


# --- the round-18 harness's own fixtures, extracted by AST (the AR-y-191 method) ---
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
    missing = (set(names) | set(assigns)) - set(got)
    assert not missing, missing
    return got


ns = {"Mock": Mock, "classify_batch": classify_batch, "workbook": workbook, "rows": rows, "base64": base64,
      "json": json, "legacy": legacy}
extract(HARNESS, ("fresh_case", "door_text", "reopen_text", "codes_of", "version_member"), ns, assigns=("INPUTS",))
tu_ns = {"base64": base64}
extract(MOV / "tests" / "test_template_uploads.py", ("payload",), tu_ns)
ns["tu"] = types.SimpleNamespace(legacy=legacy, payload=tu_ns["payload"])
fresh_case, codes_of = ns["fresh_case"], ns["codes_of"]
# AR-y-226 adds the repeated-header and the two-account / one-account CSV cases to the eight of AR-y-191.
EXTRA = [
    ("repeated_header_csv", "csv", lambda: b"Ticker,Dollars\nAAA,100\nTicker,Dollars\nBBB,200\n"),
    ("one_account_csv", "csv", lambda: b"Ticker,Dollars,Account\nAAA,100,ACC-1\nBBB,200,ACC-1\n"),
    ("two_account_csv", "csv", lambda: b"Ticker,Dollars,Account\nAAA,100,ACC-1\nBBB,200,ACC-2\n"),
]
CASES = list(ns["INPUTS"]) + EXTRA


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


CONF = {
    "pinned": {"name": "pinned (r18.1 reader + uploads HEAD)", "uploads": uploads_pinned, "reader": reader_pinned},
    "moved": {"name": "moved (r19.3 reader + uploads HEAD)", "uploads": uploads_moved, "reader": reader_moved},
}


def door(side, file_type, data, token):
    cfg = CONF[side]
    with patch.object(legacy, "UploadService", cfg["uploads"].UploadService):
        case = fresh_case()
    body = ns["tu"].payload(data, file_type, upload_token=token)
    with reader_as(cfg["reader"]):
        res = attempt(lambda: case.create(body))
    return case, body, res


# --- STORE: each case through each door ---
stored = {"pinned": OrderedDict(), "moved": OrderedDict()}
door_cases = []
for label, file_type, make in CASES:
    data = make()
    for side in ("pinned", "moved"):
        case, body, res = door(side, file_type, data, "ar226-%s-%s" % (side, label))
        ans = res.get("answer") if res.get("ok") else None
        state = (ans or {}).get("state") or ("REFUSED" if "refused" in res else "ERROR")
        door_cases.append({"sheet": label, "file_type": file_type, "stored_by": side, "state": state,
                           "answer_codes": codes_of(ans) if ans else [], "refused": res.get("refused"),
                           "error": res.get("error")})
        if ans and state == "NORMALIZED":
            stored[side][label] = {"case": case, "answer": ans}


# --- RE-OPEN: each stored input through each reader pair ---
def reopen(writer, label, side):
    entry = stored[writer][label]
    case, ans = entry["case"], entry["answer"]
    cfg = CONF[side]
    with patch.object(legacy, "UploadService", cfg["uploads"].UploadService):
        svc = case.new_service()
    svc.artifacts.families |= {"ORIGINAL_HOLDINGS"}
    with reader_as(cfg["reader"]):
        got = attempt(lambda: svc.read_input(case.principal, case.owner, ans["input_id"]))
    if got.get("ok"):
        return {"outcome": "ACCEPTED", "code": None, "document_equal_to_stored": got["answer"]["document"] == ans["portfolio"]}
    if "refused" in got:
        return {"outcome": "REFUSED", "code": got["refused"], "document_equal_to_stored": None}
    return {"outcome": "ERROR", "code": got.get("error"), "document_equal_to_stored": None}


matrix, reopen_cases = [], []
for writer in ("pinned", "moved"):
    for side in ("pinned", "moved"):
        cell = {"stored_by": writer, "reopened_by": side, "cases": 0, "accepted": 0, "refused": 0, "other": 0,
                "refusal_codes": [], "case_labels": []}
        for label in stored[writer]:
            got = reopen(writer, label, side)
            reopen_cases.append({"sheet": label, "stored_by": writer, "reopened_by": side, **got})
            cell["case_labels"].append(label)
            if got["outcome"] == "ACCEPTED":
                cell["accepted"] += 1
            elif got["outcome"] == "REFUSED":
                cell["refused"] += 1
                if got["code"] not in cell["refusal_codes"]:
                    cell["refusal_codes"].append(got["code"])
            else:
                cell["other"] += 1
        cell["cases"] = len(stored[writer])
        matrix.append(cell)


# --- EFFECT: the two readers' own outcomes over the header cases and the sheets ---
checks = load("ar21_checks_module", CHECKS)


def reader_read(reader, data, file_type):
    res = reader.read_template(data, file_type)
    fs = res.get("findings") or []
    state = "NEEDS_CORRECTION" if any(f.get("severity") == "ERROR" for f in fs) else "NORMALIZED"
    return {"outcome": state, "codes": ["%s:%s" % (f.get("code"), f.get("severity")) for f in fs],
            "reader_version": res.get("reader_version")}


def header_csv(header, values):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["Ticker", "Dollars", header])
    w.writerow(["AAA", "100", values[0]])
    w.writerow(["BBB", "200", values[1]])
    return buf.getvalue().encode("utf-8")


effect = []
for kind, pairs in (("negative", checks.NEGATIVES), ("positive", checks.POSITIVES)):
    for header, values in pairs:
        data = header_csv(header, values)
        row = {"header": header, "kind": kind, "file_type": "csv", "values": list(values)}
        for name, mod in (("before", reader_pinned), ("after", reader_moved)):
            row[name] = reader_read(mod, data, "csv")
            row[name]["several_accounts"] = [list(x) for x in mod._several_accounts(checks.wide_of(header, values))]
        row["changed"] = row["before"]["outcome"] != row["after"]["outcome"] or row["before"]["codes"] != row["after"]["codes"]
        effect.append(row)
for label, file_type, make in CASES:
    data = make()
    row = {"header": label, "kind": "sheet", "file_type": file_type, "values": "fixture of the round-18 harness or AR-y-226"}
    for name, mod in (("before", reader_pinned), ("after", reader_moved)):
        row[name] = reader_read(mod, data, file_type)
    row["changed"] = row["before"]["outcome"] != row["after"]["outcome"] or row["before"]["codes"] != row["after"]["codes"]
    effect.append(row)


def headers(kind, outcome=None, code=None, where="before"):
    out = []
    for r in effect:
        if r["kind"] != kind:
            continue
        if outcome is not None and r[where]["outcome"] != outcome:
            continue
        if code is not None and code not in " ".join(r[where]["codes"]):
            continue
        out.append(r["header"])
    return out


PM = next(c for c in matrix if c["stored_by"] == "pinned" and c["reopened_by"] == "moved")
flip_to_turned_back = [r["header"] for r in effect if r["kind"] == "negative" and r["before"]["outcome"] == "NORMALIZED" and r["after"]["outcome"] != "NORMALIZED"]
flip_to_accepted = [r["header"] for r in effect if r["kind"] == "negative" and r["before"]["outcome"] != "NORMALIZED" and r["after"]["outcome"] == "NORMALIZED"]
findings = [
    "matrix: " + "; ".join("stored %s -> reopened %s: %d/%d accepted, %d refused %s, %d other" % (
        c["stored_by"], c["reopened_by"], c["accepted"], c["cases"], c["refused"], c["refusal_codes"], c["other"]) for c in matrix),
    "pinned-stored inputs accepted by the moved pair: %d of %d" % (PM["accepted"], PM["cases"]),
    "effect rows: %d; rows whose outcome or finding codes change: %d" % (len(effect), sum(1 for r in effect if r["changed"])),
    "inputs stored per side: pinned %d, moved %d; of %d cases (the rest turned back at the door and store nothing)" % (
        len(stored["pinned"]), len(stored["moved"]), len(CASES)),
    "re-opened documents equal to the stored portfolio: %d of %d" % (
        sum(1 for r in reopen_cases if r["document_equal_to_stored"] is True), len(reopen_cases)),
    "NEGATIVE headers r18.1 turns back (before NEEDS_CORRECTION): %s" % headers("negative", outcome="NEEDS_CORRECTION", where="before"),
    "NEGATIVE headers r19.3 turns back (after NEEDS_CORRECTION): %s" % headers("negative", outcome="NEEDS_CORRECTION", where="after"),
    "NEGATIVE headers accepted before and turned back after (finding): %s" % flip_to_turned_back,
    "NEGATIVE headers turned back before and accepted after: %s" % flip_to_accepted,
    "POSITIVE headers r18.1 already turns back (ACCOUNT_COLUMN_SEVERAL_VALUES before): %s" % headers("positive", code="ACCOUNT_COLUMN_SEVERAL_VALUES", where="before"),
    "POSITIVE headers r19.3 turns back (ACCOUNT_COLUMN_SEVERAL_VALUES after): %s" % headers("positive", code="ACCOUNT_COLUMN_SEVERAL_VALUES", where="after"),
    "sheets: %s" % [(r["header"], r["before"]["outcome"], r["after"]["outcome"]) for r in effect if r["kind"] == "sheet"],
]
CLAIM = (
    "RUN in process on python %s. The pinned pair is the r18.1 reader (sha256 %s, from git blob of commit %s, READER_VERSION "
    "irpt-template-reader.r18.1) with uploads.py at HEAD (sha256 %s). The moved pair is the reader at HEAD (sha256 %s, commit %s, "
    "READER_VERSION irpt-template-reader.r19.3) with uploads.py at HEAD. Each pair is a copy of the intake package from git archive. "
    "Every case of the eight round-18 INPUTS and of three added CSV cases was STORED through each pair (UploadService.create) and "
    "every stored input was RE-OPENED (read_input) through each pair; the matrix is run, not recalled. The effect rows are "
    "read_template and _several_accounts of each reader over the header cases of ar21_checks.py NEGATIVES and POSITIVES and over "
    "every sheet case. The stores use the offline storage doubles of the round-18 harness."
    % (CONTROLS["python"], R181_SHA, R181_COMMIT, UPLOADS_SHA, CONTROLS["moved_reader_sha256"], R193_COMMIT)
)
NOT_READ = [
    "the deployed Lambda and the resident: no host call, no live object, no package built or hashed",
    "the HTTP route (upload_entry.handle) and the request_resolution / resolve_deferred path: not run; the door is UploadService.create",
    "the other door-closure members (ids.py, loaders.py, repository.py, served.py) are at HEAD in both pairs; their live pins are not run here (the AR-y-191 record names them)",
    "the live provider: resolve_template is the offline receipt; no securities call, no network",
    "any real upload, stored artifact or live row: none read; the sheets are the synthetic fixtures",
    "the words a portal shows for each code: codes and states only were recorded",
    "the template-level re-POST (create on a stored token) under each pair: not run; the re-open is read_input",
]
record = {
    "cell": "AR-y-226",
    "to_id": "IRPT_ANLREQ.TO-AR-y-226",
    "issued_to": "0.9.0_WK_IRPT_ANLREQ~70",
    "pinned": {"template_reader_sha256": CONTROLS["pinned_reader_sha256"], "uploads_sha256": CONTROLS["pinned_uploads_sha256"],
               "reader_version": CONTROLS["pinned_reader_version"], "source_commit": R181_COMMIT,
               "source_path": TREE + "/intake/template_reader.py (git blob of that commit)"},
    "moved": {"template_reader_sha256": CONTROLS["moved_reader_sha256"], "uploads_sha256": CONTROLS["moved_uploads_sha256"],
              "reader_version": CONTROLS["moved_reader_version"], "source_commit": R193_COMMIT,
              "source_path": TREE + "/intake/template_reader.py (git blob of that commit; HEAD of the worktree carries the same blob)"},
    "controls": CONTROLS,
    "scratch_tree": str(SCR),
    "reopen_matrix": matrix,
    "reopen_cases": reopen_cases,
    "door_cases": door_cases,
    "effect_table": effect,
    "findings": findings,
    "claim": CLAIM,
    "not_read": NOT_READ,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(record, indent=1, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
print("cases %d, effect rows %d, reopen rows %d -> %s" % (len(CASES), len(effect), len(reopen_cases), OUT))
for c in matrix:
    print("matrix stored=%-7s reopened=%-7s cases=%d accepted=%d refused=%d other=%d codes=%s" % (
        c["stored_by"], c["reopened_by"], c["cases"], c["accepted"], c["refused"], c["other"], c["refusal_codes"]))
