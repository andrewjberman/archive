#!/usr/bin/env python3
"""shape_check.py -- AR329-y-AC1 for IRPT_ANLREQ.TO-AR-y-329.

Loads r41/COMMENTARY_PDF_ROUTE_READ.json (or the path given as argv[1]) and prints
SHAPE-OK <keys> only when every required key is present with an allowed value and every
answer block (q1..q4) carries at least one evidence item. Otherwise SHAPE-BAD <why>, exit 1.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "r41", "COMMENTARY_PDF_ROUTE_READ.json")

TOP = ["base", "q1", "q2", "q3", "q4", "not_read"]
KEYS = {
    "q1": ["handler", "serves", "keyed_by", "callers", "returns", "evidence"],
    "q2": ["can_serve_commentary_pdf", "serves_instead", "change_needed", "rides", "evidence"],
    "q3": ["client_has_getAnalysisRequestPdf", "client_has_getAnalysisRequestOriginal", "op_table",
           "missing", "tests_to_repin", "evidence"],
    "q4": ["change_set", "recommend", "deciding_fact", "evidence"],
}
ENUM = {
    ("q1", "serves"): {"overview_pdf", "package_pdf", "by_ref", "other"},
    ("q2", "can_serve_commentary_pdf"): {"yes", "no", "unknown"},
    ("q2", "rides"): {"resident", "lambda", "portal", "none", "unknown"},
    ("q4", "recommend"): {"PORTAL_ONLY", "BACKEND_AND_PORTAL", "OTHER"},
}


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def cite_ok(node):
    return (isinstance(node, dict) and isinstance(node.get("file"), str) and node["file"]
            and isinstance(node.get("line"), int) and node["line"] >= 1
            and isinstance(node.get("text"), str) and node["text"].strip())


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        bad("unreadable record: %s" % type(exc).__name__)
    if not isinstance(rec, dict):
        bad("record is not an object")
    for key in TOP:
        if key not in rec:
            bad("missing top key %s" % key)
    base = rec["base"]
    if not isinstance(base, str) or not re.fullmatch(r"[0-9a-f]{7,40}", base):
        bad("base is not a sha")
    if not isinstance(rec["not_read"], str) or not rec["not_read"].strip():
        bad("not_read empty")
    for block, keys in KEYS.items():
        answer = rec[block]
        if not isinstance(answer, dict):
            bad("%s is not an object" % block)
        for key in keys:
            if key not in answer:
                bad("missing %s.%s" % (block, key))
        evidence = answer.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            bad("%s has no evidence item" % block)
        if not all(cite_ok(item) for item in evidence):
            bad("%s evidence item is not a file/line/text cite" % block)
    for (block, key), allowed in ENUM.items():
        value = rec[block][key]
        if value not in allowed:
            bad("%s.%s=%r not in enum" % (block, key, value))
    for key in ("client_has_getAnalysisRequestPdf", "client_has_getAnalysisRequestOriginal"):
        if not isinstance(rec["q3"][key], bool):
            bad("q3.%s is not boolean" % key)
    if not cite_ok(rec["q1"]["handler"]):
        bad("q1.handler is not a file/line/text cite")
    if not cite_ok(rec["q3"]["op_table"]):
        bad("q3.op_table is not a file/line/text cite")
    if not isinstance(rec["q3"]["tests_to_repin"], list) or not rec["q3"]["tests_to_repin"]:
        bad("q3.tests_to_repin empty")
    change_set = rec["q4"]["change_set"]
    if not isinstance(change_set, list) or not change_set:
        bad("q4.change_set empty")
    for row in change_set:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) and row.get(k) for k in ("file", "function", "change")):
            bad("q4.change_set row lacks file/function/change")
    if not isinstance(rec["q4"]["deciding_fact"], str) or not rec["q4"]["deciding_fact"].strip():
        bad("q4.deciding_fact empty")
    for key in ("keyed_by", "callers", "returns"):
        if not isinstance(rec["q1"][key], str) or not rec["q1"][key].strip():
            bad("q1.%s empty" % key)
    print("SHAPE-OK " + " ".join(TOP + ["q1.evidence=%d" % len(rec["q1"]["evidence"]),
                                         "q2.evidence=%d" % len(rec["q2"]["evidence"]),
                                         "q3.evidence=%d" % len(rec["q3"]["evidence"]),
                                         "q4.evidence=%d" % len(rec["q4"]["evidence"])]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
