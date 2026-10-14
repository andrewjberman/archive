#!/usr/bin/env python3
"""shape_check -- the shape of r41/C_SWITCH_READ.json (AR-y-326, criterion AR326-y-AC1).

Prints SHAPE-OK q1 q2 q3 q4 only when every required key is present with an allowed value, q1.kind, q2.set_by,
q3.could_read_by_id and q4.recommend are in their enums, each of q1, q2, q3 has at least one evidence item, and
q4.deciding_fact is a non-empty string. Otherwise prints SHAPE-BAD <why> and exits 1.
"""
import json
import os
import sys

KIND = ("email", "user_id", "service", "other")
SET_BY = ("client", "server")
COULD_READ = ("yes", "no", "unknown")
RECOMMEND = ("A", "B", "NEITHER")


def bad(why):
    print("SHAPE-BAD " + why)
    return 1


def nonempty_str(value):
    return isinstance(value, str) and value.strip() != ""


def evidence_ok(block, name):
    items = block.get("evidence")
    if not isinstance(items, list) or not items:
        return "%s.evidence must be a non-empty list" % name
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return "%s.evidence[%d] is not an object" % (name, i)
        if not nonempty_str(item.get("file")) or not isinstance(item.get("line"), int) or not nonempty_str(item.get("text")):
            return "%s.evidence[%d] needs file, line (int) and text" % (name, i)
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "r41", "C_SWITCH_READ.json")
    try:
        with open(path, encoding="utf-8") as fh:
            record = json.load(fh)
    except (OSError, ValueError) as exc:
        return bad("record unreadable (%s)" % exc.__class__.__name__)
    if not isinstance(record, dict):
        return bad("record is not an object")
    for key in ("base", "q1", "q2", "q3", "q4", "not_read"):
        if key not in record:
            return bad("missing key: " + key)
    if not nonempty_str(record["base"]):
        return bad("base must be a non-empty string")
    q1, q2, q3, q4 = record["q1"], record["q2"], record["q3"], record["q4"]
    for name, block in (("q1", q1), ("q2", q2), ("q3", q3), ("q4", q4)):
        if not isinstance(block, dict):
            return bad(name + " must be an object")
    for key in ("principal_id_value", "kind", "setter", "evidence"):
        if key not in q1:
            return bad("q1 missing key: " + key)
    if q1["kind"] not in KIND:
        return bad("q1.kind not in enum: %r" % (q1["kind"],))
    if not nonempty_str(q1["setter"]):
        return bad("q1.setter must be a non-empty string")
    msg = evidence_ok(q1, "q1")
    if msg:
        return bad(msg)
    for key in ("set_by", "evidence"):
        if key not in q2:
            return bad("q2 missing key: " + key)
    if q2["set_by"] not in SET_BY:
        return bad("q2.set_by not in enum: %r" % (q2["set_by"],))
    msg = evidence_ok(q2, "q2")
    if msg:
        return bad(msg)
    for key in ("reader_exists", "reader", "identity", "could_read_by_id", "evidence"):
        if key not in q3:
            return bad("q3 missing key: " + key)
    if not isinstance(q3["reader_exists"], bool):
        return bad("q3.reader_exists must be a boolean")
    if q3["reader"] is not None and not nonempty_str(q3["reader"]):
        return bad("q3.reader must be null or a non-empty string")
    if q3["could_read_by_id"] not in COULD_READ:
        return bad("q3.could_read_by_id not in enum: %r" % (q3["could_read_by_id"],))
    if not nonempty_str(q3["identity"]):
        return bad("q3.identity must be a non-empty string")
    msg = evidence_ok(q3, "q3")
    if msg:
        return bad(msg)
    for key in ("a", "b", "recommend", "deciding_fact"):
        if key not in q4:
            return bad("q4 missing key: " + key)
    if not nonempty_str(q4["a"]) or not nonempty_str(q4["b"]):
        return bad("q4.a and q4.b must be non-empty strings")
    if q4["recommend"] not in RECOMMEND:
        return bad("q4.recommend not in enum: %r" % (q4["recommend"],))
    if not nonempty_str(q4["deciding_fact"]):
        return bad("q4.deciding_fact must be a non-empty string")
    if not nonempty_str(record["not_read"]):
        return bad("not_read must be a non-empty string")
    print("SHAPE-OK q1 q2 q3 q4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
