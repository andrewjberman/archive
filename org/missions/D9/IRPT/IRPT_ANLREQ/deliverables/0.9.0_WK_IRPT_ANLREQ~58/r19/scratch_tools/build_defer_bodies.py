"""r19 AR-y-203: build the _defer first answer of the template lane from the REAL functions of one intake folder.

Usage: python -I build_defer_bodies.py <intake_dir> <arm AFTER|BEFORE> <out.json>

The body literal is the one uploads.py `_defer` returns on an ERROR finding (moved uploads.py at 069b8f797e, lines 459-475):
  {upload_id, input_id: None, state: NEEDS_CORRECTION, reason: TEMPLATE_FINDINGS,
   findings: _with_correction_words(findings[:MAX_STORED_FINDINGS]), findings_total: len(findings), template}
Every name in it is imported from the intake folder given on the command line: read_template (template_reader.py),
_with_correction_words (uploads.py), MAX_STORED_FINDINGS and NEEDS_CORRECTION (upload_resolution.py). Nothing is retyped.
Sheet bytes are the round-18 harness INPUTS (AST-extracted, not retyped), except header_repeated_csv, which the r19
harness constructed (same literal as the prior cell's dump harness, line 93).
Upload ids are the door's own values from the prior cell's answer bodies (run_hr/answer_bodies.json, key <sheet>|<arm>).
"""
import ast
import copy
import json
import sys
from pathlib import Path

INTAKE, ARM, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
HARNESS = Path(sys.argv[4])
DOOR = Path(sys.argv[5])
assert ARM in ("AFTER", "BEFORE"), ARM
sys.path.insert(0, str(INTAKE))

import template_reader  # noqa: E402
from template_reader import read_template  # noqa: E402
from upload_resolution import MAX_STORED_FINDINGS, NEEDS_CORRECTION  # noqa: E402
from uploads import _with_correction_words  # noqa: E402

SHEETS = ["total_row_sheet", "two_value_account_sheet", "repair_header_two_values", "brokerage_two_account",
          "header_repeated_csv"]

ns = {"workbook": None, "rows": None}
for node in ast.parse(HARNESS.read_text(encoding="utf-8")).body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "INPUTS":
        exec(compile(ast.Module([node], []), str(HARNESS), "exec"), ns)
INPUTS = {label: (ft, make) for label, ft, make in ns["INPUTS"]}
INPUTS["header_repeated_csv"] = ("csv", lambda: b"Ticker,Dollars\nAAA,100\nTicker,Dollars\nBBB,200\n")

door = json.loads(DOOR.read_text(encoding="utf-8"))
door_arm = "moved" if ARM == "AFTER" else "pinned"

out = []
for label in SHEETS:
    file_type, make = INPUTS[label]
    data = make()
    template = read_template(data, file_type)
    errors = [f for f in template["findings"] if f.get("severity") == "ERROR"]
    door_answer = door[f"{label}|{door_arm}"]["answer"]
    rec = {"case": label, "arm": ARM, "file_type": file_type, "reader_module": template_reader.__file__,
           "reader_version": getattr(template_reader, "READER_VERSION", None), "upload_id": door_answer["upload_id"],
           "all_finding_codes": [f["code"] for f in template["findings"]],
           "error_codes": [f["code"] for f in errors], "has_error": bool(errors)}
    if not errors:
        rec.update(body=None, body_keys=None, reason=None, findings_total=None, codes=[], words={})
        out.append(rec)
        continue
    body = {"upload_id": door_answer["upload_id"], "input_id": None, "state": NEEDS_CORRECTION,
            "reason": "TEMPLATE_FINDINGS",
            "findings": _with_correction_words(copy.deepcopy(template["findings"][:MAX_STORED_FINDINGS])),
            "findings_total": len(template["findings"]), "template": template}
    words = {}
    for f in body["findings"]:
        words.setdefault(f["code"], f.get("description"))
    rec.update(body=json.loads(json.dumps(body)), body_keys=sorted(body.keys()), reason=body["reason"],
               findings_total=body["findings_total"], codes=sorted({f["code"] for f in body["findings"]}), words=words,
               state=body["state"], max_stored_findings=MAX_STORED_FINDINGS)
    if ARM == "AFTER":
        rec["findings_equal_to_prior_door_answer"] = body["findings"] == door_answer.get("findings")
        rec["door_answer_state"] = door_answer.get("state")
    out.append(rec)

OUT.write_text(json.dumps(out, indent=1, ensure_ascii=True) + "\n", encoding="utf-8")
for r in out:
    print(ARM, r["case"], "has_error=%s" % r["has_error"], "codes=%s" % r.get("codes"),
          "keys=%s" % (r.get("body_keys") or "-"), "total=%s" % r.get("findings_total"),
          "equal_to_prior_door=%s" % r.get("findings_equal_to_prior_door_answer", "n/a"))
print("reader", template_reader.__file__, "version", getattr(template_reader, "READER_VERSION", None))
