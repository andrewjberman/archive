"""AR335-y-AC1: the shape of r41/PACKAGER_DOOR_READ.json (IRPT_ANLREQ.TO-AR-y-335).

Prints SHAPE-OK <keys> and exits 0 only when every required key is present with an allowed value
and every answer block carries at least one evidence item. Otherwise prints SHAPE-BAD <why> and exits 1.
Reads only the record beside this script; no AWS call, no network, no source file.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD = HERE / "r41" / "PACKAGER_DOOR_READ.json"

TOKEN_ENUM = {"hashed_table", "secret_by_id", "signed_claim", "other"}
SECRET_ENUM = {"yes", "no", "unknown"}
VALUE_SHAPE_ENUM = {"bare_token", "json_field", "other"}
NEEDS_ENUM = {"SECRET_VALUE_SHAPE", "USERS_ROW", "ENV_FIRM_LIST", "IAM_STATEMENT", "TF_IMPORT", "NOTHING"}
CITE_KEYS = {"file", "line", "text"}


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def need(block, name, label):
    if not isinstance(block, dict) or name not in block:
        bad("missing %s.%s" % (label, name))
    return block[name]


def nonempty_list(value, label):
    if not isinstance(value, list) or not value:
        bad("%s is not a non-empty list" % label)


def cite_ok(value, label):
    if not isinstance(value, dict) or not CITE_KEYS <= set(value):
        bad("%s is not a file/line/text cite" % label)


def main():
    if not RECORD.is_file():
        bad("record absent: %s" % RECORD.name)
    try:
        rec = json.loads(RECORD.read_text(encoding="utf-8"))
    except ValueError as exc:
        bad("record is not JSON: %s" % exc)
    if not isinstance(rec, dict):
        bad("record is not an object")
    for key in ("base", "q1", "q2", "q3", "q4", "not_read"):
        if key not in rec:
            bad("missing top-level key %s" % key)
    if not re.fullmatch(r"[0-9a-f]{40}", str(rec["base"])):
        bad("base is not a full 40-hex sha")
    if not isinstance(rec["not_read"], list) or not rec["not_read"]:
        bad("not_read is not a non-empty list")

    q1 = rec["q1"]
    for name in ("authenticator", "recognised_by", "unknown_subject", "evidence"):
        need(q1, name, "q1")
    if need(q1, "token_compared_with", "q1") not in TOKEN_ENUM:
        bad("q1.token_compared_with outside enum")
    if need(q1, "existing_secret_enough", "q1") not in SECRET_ENUM:
        bad("q1.existing_secret_enough outside enum")
    nonempty_list(q1["evidence"], "q1.evidence")
    for i, item in enumerate(q1["evidence"]):
        cite_ok(item, "q1.evidence[%d]" % i)

    q2 = rec["q2"]
    for name in ("format", "when_unset", "when_all", "when_firm_missing", "declared_in", "searched",
                 "followed_lines", "evidence"):
        need(q2, name, "q2")
    cite_ok(need(q2, "read_at", "q2"), "q2.read_at")
    if not isinstance(q2["followed_lines"], list) or not all(type(x) is int for x in q2["followed_lines"]):
        bad("q2.followed_lines is not a list of ints")
    nonempty_list(q2["evidence"], "q2.evidence")
    for i, item in enumerate(q2["evidence"]):
        cite_ok(item, "q2.evidence[%d]" % i)

    q3 = rec["q3"]
    for name in ("subject_admitted", "class_check", "error_codes", "writes", "evidence"):
        need(q3, name, "q3")
    cite_ok(need(q3, "handler", "q3"), "q3.handler")
    fields = need(q3, "fields", "q3")
    if not isinstance(fields, list) or not fields:
        bad("q3.fields is not a non-empty list")
    for i, field in enumerate(fields):
        if not isinstance(field, dict) or "name" not in field or "check" not in field:
            bad("q3.fields[%d] lacks name or check" % i)
    nonempty_list(q3["evidence"], "q3.evidence")
    for i, item in enumerate(q3["evidence"]):
        cite_ok(item, "q3.evidence[%d]" % i)

    q4 = rec["q4"]
    for name in ("api_base_form", "secret_name_form", "json_field", "iam_needed", "deciding_fact", "evidence"):
        need(q4, name, "q4")
    if need(q4, "secret_value_shape", "q4") not in VALUE_SHAPE_ENUM:
        bad("q4.secret_value_shape outside enum")
    if not isinstance(need(q4, "iam_declared", "q4"), bool):
        bad("q4.iam_declared is not true or false")
    iam = need(q4, "iam_evidence", "q4")
    if isinstance(iam, str):
        if "not declared" not in iam or "searched" not in q4:
            bad("q4.iam_evidence is text but not 'not declared' with searched")
    elif isinstance(iam, list) and iam:
        for i, item in enumerate(iam):
            cite_ok(item, "q4.iam_evidence[%d]" % i)
    else:
        bad("q4.iam_evidence is neither a cite list nor a not-declared text")
    needs = need(q4, "needs", "q4")
    if not isinstance(needs, list) or not needs or not set(needs) <= NEEDS_ENUM:
        bad("q4.needs is not a non-empty list drawn from the enum")
    nonempty_list(q4["evidence"], "q4.evidence")
    for i, item in enumerate(q4["evidence"]):
        cite_ok(item, "q4.evidence[%d]" % i)

    print("SHAPE-OK " + ",".join(sorted(rec)) + " q1-q4 each with evidence; q4.needs=" + "|".join(needs))
    sys.exit(0)


if __name__ == "__main__":
    main()
