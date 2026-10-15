"""AR350-y-AC1: shape check of r41/FILING_HINT_DESIGN_READ.json (AR-y-350, worker 0.9.0_WK_IRPT_ANLREQ~151).

Prints SHAPE-OK <keys> only when every key of the record is present with an allowed value and every answer block
carries at least one evidence item; otherwise SHAPE-BAD <why> and exit 1. ASCII only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "r41", "FILING_HINT_DESIGN_READ.json")
ENUM_YNU = ("yes", "no", "unknown")
ENUM_RECOMMEND = ("PORTAL_ONLY", "BACKEND_AND_PORTAL", "CONTRACT_NEEDED")


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def need(block, name, kind, where):
    if not isinstance(block, dict) or name not in block:
        bad("missing %s.%s" % (where, name))
    value = block[name]
    if kind is str and (not isinstance(value, str) or not value.strip()):
        bad("%s.%s is not a non-empty string" % (where, name))
    if kind is list and not isinstance(value, list):
        bad("%s.%s is not a list" % (where, name))
    return value


def check_evidence(block, where):
    ev = need(block, "evidence", list, where)
    if len(ev) < 1:
        bad("%s.evidence has no item" % where)
    for i, item in enumerate(ev):
        if not isinstance(item, dict):
            bad("%s.evidence[%d] is not an object" % (where, i))
        for k, t in (("file", str), ("line", int), ("text", str)):
            if k not in item or not isinstance(item[k], t) or (t is str and not item[k].strip()):
                bad("%s.evidence[%d].%s missing or wrong type" % (where, i, k))
        if item["line"] < 1:
            bad("%s.evidence[%d].line is below 1" % (where, i))


def main():
    if not os.path.isfile(RECORD):
        bad("record not found at r41/FILING_HINT_DESIGN_READ.json")
    with open(RECORD, encoding="utf-8") as fh:
        rec = json.load(fh)
    if not isinstance(rec, dict):
        bad("record is not an object")
    for key in ("base", "q1", "q2", "q3", "q4", "not_read"):
        if key not in rec:
            bad("missing top key " + key)
    need(rec, "base", str, "record")
    need(rec, "not_read", str, "record")

    q1 = rec["q1"]
    v = need(q1, "page_holds_rows", str, "q1")
    if v not in ENUM_YNU:
        bad("q1.page_holds_rows not in enum: " + v)
    need(q1, "response_members", list, "q1")
    codes = need(q1, "unresolved_finding_codes", list, "q1")
    for i, c in enumerate(codes):
        if not isinstance(c, dict) or not isinstance(c.get("code"), str) or not c.get("code"):
            bad("q1.unresolved_finding_codes[%d] lacks code" % i)
        if not isinstance(c.get("evidence"), list) or not c["evidence"]:
            bad("q1.unresolved_finding_codes[%d] lacks evidence" % i)
    check_evidence(q1, "q1")

    q2 = rec["q2"]
    need(q2, "entry_members", list, "q2")
    need(q2, "universe", str, "q2")
    v = need(q2, "entry_has_cusip_or_isin", str, "q2")
    if v not in ENUM_YNU:
        bad("q2.entry_has_cusip_or_isin not in enum: " + v)
    v = need(q2, "exact_id_match_possible", str, "q2")
    if v not in ENUM_YNU:
        bad("q2.exact_id_match_possible not in enum: " + v)
    check_evidence(q2, "q2")

    q3 = rec["q3"]
    v = need(q3, "per_holding_ui_exists", str, "q3")
    if v not in ENUM_YNU:
        bad("q3.per_holding_ui_exists not in enum: " + v)
    v = need(q3, "override_member_exists", str, "q3")
    if v not in ENUM_YNU:
        bad("q3.override_member_exists not in enum: " + v)
    need(q3, "how_acceptance_reaches_backend", str, "q3")
    check_evidence(q3, "q3")

    q4 = rec["q4"]
    changes = need(q4, "change_set", list, "q4")
    for i, c in enumerate(changes):
        for k in ("file", "function", "change"):
            if not isinstance(c, dict) or not isinstance(c.get(k), str) or not c.get(k):
                bad("q4.change_set[%d].%s missing" % (i, k))
    tests = need(q4, "tests_to_add", list, "q4")
    if not all(isinstance(t, str) and t for t in tests):
        bad("q4.tests_to_add holds a non-string")
    points = need(q4, "points_not_met", list, "q4")
    for i, p in enumerate(points):
        if not isinstance(p, dict) or not isinstance(p.get("point"), str) or not isinstance(p.get("why"), str):
            bad("q4.points_not_met[%d] lacks point or why" % i)
    v = need(q4, "recommend", str, "q4")
    if v not in ENUM_RECOMMEND:
        bad("q4.recommend not in enum: " + v)
    need(q4, "deciding_fact", str, "q4")
    check_evidence(q4, "q4")

    print("SHAPE-OK " + ",".join(["base", "q1", "q2", "q3", "q4", "not_read"]))


if __name__ == "__main__":
    main()
