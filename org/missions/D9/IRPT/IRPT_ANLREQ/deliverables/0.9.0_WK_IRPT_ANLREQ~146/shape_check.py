"""AR342-y-AC1: shape check of the FWD-1 prerequisites record.

Usage: python shape_check.py [record_path]
Prints SHAPE-OK <keys> (rc 0) when every key is present with an allowed value and every answer block
carries at least one evidence item; otherwise SHAPE-BAD <why> (rc 1).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.join(HERE, "r41", "FWD1_PREREQ_READ.json")
YES_NO_UNKNOWN = ("yes", "no", "unknown")
RECOMMEND = ("MINT_AS_DESCRIBED", "CHANGE_ADDRESS", "NEEDS")
VERDICTS = ("admits", "refuses", "not_constrained")


def bad(why):
    print("SHAPE-BAD " + why)
    return 1


def need(block, key, name):
    if not isinstance(block, dict) or key not in block:
        raise ValueError("%s.%s missing" % (name, key))
    return block[key]


def main(path):
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        return bad("cannot load record: %s" % exc.__class__.__name__)
    try:
        for top in ("base", "q1", "q2", "q3", "q4", "not_read"):
            need(rec, top, "record")
        if not isinstance(rec["base"], str) or len(rec["base"]) < 7:
            raise ValueError("base is not a sha")
        if not isinstance(rec["not_read"], str) or not rec["not_read"].strip():
            raise ValueError("not_read empty")

        q1 = rec["q1"]
        rows = need(q1, "rows", "q1")
        if not isinstance(rows, list) or not rows:
            raise ValueError("q1.rows empty")
        for i, row in enumerate(rows):
            need(row, "place", "q1.rows[%d]" % i)
            if need(row, "verdict", "q1.rows[%d]" % i) not in VERDICTS:
                raise ValueError("q1.rows[%d].verdict not in enum" % i)
            ev = need(row, "evidence", "q1.rows[%d]" % i)
            for k in ("file", "line", "text"):
                need(ev, k, "q1.rows[%d].evidence" % i)
        if not isinstance(need(q1, "domain_rule_exists", "q1"), bool):
            raise ValueError("q1.domain_rule_exists not boolean")
        if need(q1, "invalid_domain_ok", "q1") not in YES_NO_UNKNOWN:
            raise ValueError("q1.invalid_domain_ok not in enum")

        q2 = rec["q2"]
        needs = need(q2, "needs", "q2")
        for k in ("userType", "class", "allowedFirmIds", "profile_scope", "other"):
            need(needs, k, "q2.needs")
            if not isinstance(needs[k], str):
                raise ValueError("q2.needs.%s not a string" % k)
        fns = need(q2, "functions", "q2")
        if not isinstance(fns, list) or not fns:
            raise ValueError("q2.functions empty")
        if not isinstance(need(q2, "ticket_center_visibility", "q2"), str):
            raise ValueError("q2.ticket_center_visibility not a string")
        if not isinstance(need(q2, "evidence", "q2"), list) or not q2["evidence"]:
            raise ValueError("q2.evidence empty")

        q3 = rec["q3"]
        if need(q3, "door_checks_firm", "q3") not in YES_NO_UNKNOWN:
            raise ValueError("q3.door_checks_firm not in enum")
        for k in ("door_requires_class", "submit_requires_class", "owner_stored", "firm_equality_check"):
            if not isinstance(need(q3, k, "q3"), str):
                raise ValueError("q3.%s not a string" % k)
        if need(q3, "one_record_passes_all_three", "q3") not in YES_NO_UNKNOWN:
            raise ValueError("q3.one_record_passes_all_three not in enum")
        ea = need(q3, "extra_attribute", "q3")
        if ea is not None and not isinstance(ea, str):
            raise ValueError("q3.extra_attribute not string or null")
        if not isinstance(need(q3, "evidence", "q3"), list) or not q3["evidence"]:
            raise ValueError("q3.evidence empty")

        q4 = rec["q4"]
        attrs = need(q4, "row_attributes", "q4")
        if not isinstance(attrs, list) or not attrs:
            raise ValueError("q4.row_attributes empty")
        for i, a in enumerate(attrs):
            need(a, "name", "q4.row_attributes[%d]" % i)
            need(a, "value_or_form", "q4.row_attributes[%d]" % i)
        for k in ("table", "token_method", "removal_and_absent_check", "deciding_fact"):
            if not isinstance(need(q4, k, "q4"), str):
                raise ValueError("q4.%s not a string" % k)
        if need(q4, "recommend", "q4") not in RECOMMEND:
            raise ValueError("q4.recommend not in enum")
        if not isinstance(need(q4, "evidence", "q4"), list) or not q4["evidence"]:
            raise ValueError("q4.evidence empty")
    except ValueError as exc:
        return bad(str(exc))

    print("SHAPE-OK keys=base,q1,q2,q3,q4,not_read answers=4 q1_rows=%d q2_functions=%d" % (len(rows), len(fns)))
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    sys.exit(main(target))
