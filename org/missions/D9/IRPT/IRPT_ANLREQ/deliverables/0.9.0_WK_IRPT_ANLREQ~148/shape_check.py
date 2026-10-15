"""AR344-y-AC1: shape check of r41/FWD1_LOGIN_DRIVER_READ.json.

Prints SHAPE-OK <top-level keys> only when every required key is present with an allowed value
and every answer block carries at least one {file, line, text} evidence item; otherwise
SHAPE-BAD <why> and exit 1.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, "r41", "FWD1_LOGIN_DRIVER_READ.json")

TOP = ["base", "q1", "q2", "q3", "q4", "not_read"]
YES_NO_UNK = {"yes", "no", "unknown"}
APPLIES = {"applies", "skipped", "not_at_login"}
RECOMMEND = {"MINT_WITH_PASSWORD", "API_DRIVE_ONLY", "NEEDS"}


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def need(block, keys, where):
    if not isinstance(block, dict):
        bad("%s is not an object" % where)
    for k in keys:
        if k not in block:
            bad("%s missing key %s" % (where, k))


def cite_ok(c, where):
    if not isinstance(c, dict) or not all(k in c for k in ("file", "line", "text")):
        bad("%s is not a file/line/text cite" % where)
    if not isinstance(c["file"], str) or not c["file"]:
        bad("%s has no file" % where)
    if not isinstance(c["line"], int) or isinstance(c["line"], bool):
        bad("%s line is not an integer" % where)
    if not isinstance(c["text"], str) or not c["text"].strip():
        bad("%s text is empty" % where)


def evidence_list(block, where):
    ev = block.get("evidence")
    if not isinstance(ev, list) or len(ev) < 1:
        bad("%s evidence is empty" % where)
    for i, e in enumerate(ev):
        cite_ok(e, "%s evidence[%d]" % (where, i))
    return len(ev)


def str_list(block, key, where):
    val = block.get(key)
    if not isinstance(val, list) or not val:
        bad("%s.%s is empty" % (where, key))
    for i, v in enumerate(val):
        if not isinstance(v, (str, dict)):
            bad("%s.%s[%d] is neither a string nor an object" % (where, key, i))


def main():
    try:
        with open(REC, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as exc:
        bad("cannot load record: %s" % exc)
    if not isinstance(rec, dict):
        bad("record is not an object")
    for k in TOP:
        if k not in rec:
            bad("top-level key missing: %s" % k)
    if not isinstance(rec["base"], str) or len(rec["base"]) < 7:
        bad("base is not a sha")

    # q1: the login gates
    q1 = rec["q1"]
    need(q1, ["origin_localhost_passes", "gates"], "q1")
    if q1["origin_localhost_passes"] not in YES_NO_UNK:
        bad("q1.origin_localhost_passes not in enum: %r" % (q1["origin_localhost_passes"],))
    if not isinstance(q1["gates"], list) or not q1["gates"]:
        bad("q1.gates is empty")
    n_q1 = 0
    for i, g in enumerate(q1["gates"]):
        need(g, ["gate", "applies", "condition", "evidence"], "q1.gates[%d]" % i)
        if g["applies"] not in APPLIES:
            bad("q1.gates[%d].applies not in enum: %r" % (i, g["applies"]))
        if not isinstance(g["condition"], str) or not g["condition"].strip():
            bad("q1.gates[%d].condition is empty" % i)
        cite_ok(g["evidence"], "q1.gates[%d].evidence" % i)
        n_q1 += 1
    if n_q1 < 1:
        bad("q1 carries no gate evidence")

    # q2: the row a login accepts, and the claims
    q2 = rec["q2"]
    need(q2, ["row_attributes", "token_claims", "test_filer_gets_tier_internal", "walker_differences",
              "evidence"], "q2")
    if q2["test_filer_gets_tier_internal"] not in YES_NO_UNK:
        bad("q2.test_filer_gets_tier_internal not in enum: %r" % (q2["test_filer_gets_tier_internal"],))
    str_list(q2, "row_attributes", "q2")
    for i, a in enumerate(q2["row_attributes"]):
        need(a, ["name", "value_or_form"], "q2.row_attributes[%d]" % i)
    str_list(q2, "token_claims", "q2")
    str_list(q2, "walker_differences", "q2")
    evidence_list(q2, "q2")

    # q3: the password hash
    q3 = rec["q3"]
    need(q3, ["hash_scheme", "helper_exists", "helper", "strength_checked_on_direct_write",
              "password_in_memory_only_possible", "evidence"], "q3")
    if not isinstance(q3["hash_scheme"], str) or not q3["hash_scheme"].strip():
        bad("q3.hash_scheme is empty")
    if not isinstance(q3["helper_exists"], bool):
        bad("q3.helper_exists is not a bool")
    if q3["helper"] is not None and not isinstance(q3["helper"], str):
        bad("q3.helper is neither string nor null")
    if q3["strength_checked_on_direct_write"] not in YES_NO_UNK:
        bad("q3.strength_checked_on_direct_write not in enum: %r" % (q3["strength_checked_on_direct_write"],))
    if q3["password_in_memory_only_possible"] not in YES_NO_UNK:
        bad("q3.password_in_memory_only_possible not in enum: %r" % (q3["password_in_memory_only_possible"],))
    evidence_list(q3, "q3")

    # q4: the page driver and the recommendation
    q4 = rec["q4"]
    need(q4, ["driver_library", "signin_method", "guard_changes_needed", "existing_filing_driver",
              "smallest_honest_driver", "recommend", "deciding_fact", "evidence"], "q4")
    if q4["recommend"] not in RECOMMEND:
        bad("q4.recommend not in enum: %r" % (q4["recommend"],))
    if not isinstance(q4["existing_filing_driver"], bool):
        bad("q4.existing_filing_driver is not a bool")
    str_list(q4, "guard_changes_needed", "q4")
    evidence_list(q4, "q4")

    if not isinstance(rec["not_read"], str) or not rec["not_read"].strip():
        bad("not_read is empty")

    print("SHAPE-OK " + ",".join(TOP))


if __name__ == "__main__":
    main()
