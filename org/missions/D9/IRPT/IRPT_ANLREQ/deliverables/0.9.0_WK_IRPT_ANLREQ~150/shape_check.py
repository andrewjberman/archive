"""Shape check for the AR-y-348 record r41/STAFF_FIRMS_CATALOGUE_READ.json.

Prints SHAPE-OK <keys> when every required key is present with an allowed value and every
answer block carries at least one evidence item; otherwise SHAPE-BAD <why> and exit 1.
ASCII only. Run as: python <this file>
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "r41", "STAFF_FIRMS_CATALOGUE_READ.json")

ENUM_Q2_LOAD = ("loads", "refused", "unknown")
ENUM_Q2_BEFORE = ("yes", "no", "unknown")
ENUM_Q4_GLOBAL = ("ready_firms", "empty", "error", "unknown")
ENUM_Q4_RECOMMEND = ("RUN_AS_MINTED", "MINT_NEEDS", "BLOCKED")
ENUM_Q4_PARTNER = ("yes", "no", "unknown")


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def need(obj, key, where):
    if not isinstance(obj, dict) or key not in obj:
        bad("missing key %s.%s" % (where, key))
    return obj[key]


def nonempty_str(value, where):
    if not isinstance(value, str) or not value.strip():
        bad("%s must be a non-empty string" % where)


def nonempty_list(value, where):
    if not isinstance(value, list) or len(value) == 0:
        bad("%s must be a non-empty list" % where)


def cite_ok(cite, where):
    if not isinstance(cite, dict):
        bad("%s must be a {file, line, text} object" % where)
    for k in ("file", "line", "text"):
        if k not in cite:
            bad("%s lacks %s" % (where, k))
    if not isinstance(cite["line"], int) or cite["line"] < 1:
        bad("%s line must be a positive integer" % where)


def evidence_ok(block, where):
    ev = need(block, "evidence", where)
    nonempty_list(ev, where + ".evidence")
    for i, c in enumerate(ev):
        cite_ok(c, "%s.evidence[%d]" % (where, i))


def main():
    if not os.path.isfile(RECORD):
        bad("record not found at r41/STAFF_FIRMS_CATALOGUE_READ.json")
    try:
        with open(RECORD, "r", encoding="utf-8") as fh:
            rec = json.load(fh)
    except ValueError as exc:
        bad("record is not valid JSON: %s" % exc)

    base = need(rec, "base", "root")
    if not isinstance(base, str) or not re.match(r"^[0-9a-f]{40}$", base):
        bad("base must be a full 40-hex sha")

    q1 = need(rec, "q1", "root")
    cite_ok(need(q1, "handler", "q1"), "q1.handler")
    nonempty_str(need(q1, "returns_for_staff_global", "q1"), "q1.returns_for_staff_global")
    for k in ("firms_null_not_failed_when", "firms_failed_when", "firms_empty_when"):
        nonempty_list(need(q1, k, "q1"), "q1." + k)
    evidence_ok(q1, "q1")

    q2 = need(rec, "q2", "root")
    cite_ok(need(q2, "refusal_site", "q2"), "q2.refusal_site")
    if need(q2, "staff_no_selected_tenant", "q2") not in ENUM_Q2_LOAD:
        bad("q2.staff_no_selected_tenant not in %s" % (ENUM_Q2_LOAD,))
    if need(q2, "staff_with_partner_firm", "q2") not in ENUM_Q2_LOAD:
        bad("q2.staff_with_partner_firm not in %s" % (ENUM_Q2_LOAD,))
    if need(q2, "catalogue_loads_before_firm_chosen", "q2") not in ENUM_Q2_BEFORE:
        bad("q2.catalogue_loads_before_firm_chosen not in %s" % (ENUM_Q2_BEFORE,))
    evidence_ok(q2, "q2")

    q3 = need(rec, "q3", "root")
    for k in ("prod_has_staff_not_filing_sentence", "prod_has_staff_firm_chooser",
              "prod_catalogue_sends_selected_tenant"):
        if not isinstance(need(q3, k, "q3"), bool):
            bad("q3.%s must be true or false" % k)
    diffs = need(q3, "differences", "q3")
    nonempty_list(diffs, "q3.differences")
    for i, c in enumerate(diffs):
        cite_ok(c, "q3.differences[%d]" % i)
        if "ref" not in c:
            bad("q3.differences[%d] lacks ref" % i)
    nonempty_list(need(q3, "searched", "q3"), "q3.searched")
    evidence_ok(q3, "q3")

    q4 = need(rec, "q4", "root")
    if need(q4, "global_firms_for_minted_row", "q4") not in ENUM_Q4_GLOBAL:
        bad("q4.global_firms_for_minted_row not in %s" % (ENUM_Q4_GLOBAL,))
    deps = need(q4, "depends_on", "q4")
    nonempty_list(deps, "q4.depends_on")
    for i, d in enumerate(deps):
        for k in ("attribute", "value_form"):
            nonempty_str(need(d, k, "q4.depends_on[%d]" % i), "q4.depends_on[%d].%s" % (i, k))
        evidence_ok(d, "q4.depends_on[%d]" % i)
    if need(q4, "catalogue_loads_with_partner_firm", "q4") not in ENUM_Q4_PARTNER:
        bad("q4.catalogue_loads_with_partner_firm not in %s" % (ENUM_Q4_PARTNER,))
    if need(q4, "recommend", "q4") not in ENUM_Q4_RECOMMEND:
        bad("q4.recommend not in %s" % (ENUM_Q4_RECOMMEND,))
    nonempty_str(need(q4, "deciding_fact", "q4"), "q4.deciding_fact")
    evidence_ok(q4, "q4")

    nonempty_str(need(rec, "not_read", "root"), "not_read")

    keys = sorted(rec.keys())
    print("SHAPE-OK " + ", ".join(keys))
    sys.exit(0)


if __name__ == "__main__":
    main()
