"""AR343-y-AC1: shape check of r41/FWD1_RUN_MECHANICS_READ.json.

Prints SHAPE-OK <top-level keys> only when every required key is present with an allowed value
and every answer block carries at least one {file, line, text} evidence item; otherwise
SHAPE-BAD <why> and exit 1.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC = os.path.join(HERE, "r41", "FWD1_RUN_MECHANICS_READ.json")

TOP = ["base", "q1", "q2", "q3", "q4", "not_read"]
DEV_IS = {"deployed_site", "local_dev_build", "both", "unknown"}
TOKEN = {"yes", "no", "unknown"}
DRIVE = {"api", "browser"}
RECOMMEND = {"BROWSER_DRIVE", "API_DRIVE", "NEEDS"}


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def need(block, keys, where):
    if not isinstance(block, dict):
        bad("%s is not an object" % where)
    for k in keys:
        if k not in block:
            bad("%s missing key %s" % (where, k))


def evidence(block, where):
    ev = block.get("evidence")
    if not isinstance(ev, list) or len(ev) < 1:
        bad("%s evidence is empty" % where)
    for i, e in enumerate(ev):
        if not isinstance(e, dict) or not all(k in e for k in ("file", "line", "text")):
            bad("%s evidence[%d] is not a file/line/text cite" % (where, i))


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

    q1 = rec["q1"]
    need(q1, ["dev_is", "url", "api_base_source", "build_deploy_path", "prd_quote", "evidence"], "q1")
    if q1["dev_is"] not in DEV_IS:
        bad("q1.dev_is not in enum: %r" % (q1["dev_is"],))
    if q1["url"] is not None and not isinstance(q1["url"], str):
        bad("q1.url is neither string nor null")
    need(q1["api_base_source"], ["file", "line", "text"], "q1.api_base_source")
    evidence(q1, "q1")

    q2 = rec["q2"]
    need(q2, ["session_store", "token_stand_in_possible", "earlier_drivers", "browser_drive_documented",
              "recipe", "smallest_honest_drive", "evidence"], "q2")
    if q2["token_stand_in_possible"] not in TOKEN:
        bad("q2.token_stand_in_possible not in enum: %r" % (q2["token_stand_in_possible"],))
    if not isinstance(q2["earlier_drivers"], list) or not q2["earlier_drivers"]:
        bad("q2.earlier_drivers is empty")
    for i, d in enumerate(q2["earlier_drivers"]):
        need(d, ["name", "drove"], "q2.earlier_drivers[%d]" % i)
        if d["drove"] not in DRIVE:
            bad("q2.earlier_drivers[%d].drove not in enum: %r" % (i, d["drove"]))
    if not isinstance(q2["browser_drive_documented"], bool):
        bad("q2.browser_drive_documented is not a bool")
    evidence(q2, "q2")

    q3 = rec["q3"]
    need(q3, ["form_fields", "submit_call_order", "attachment_controls", "holdings_file", "evidence"], "q3")
    if not isinstance(q3["form_fields"], list) or not q3["form_fields"]:
        bad("q3.form_fields is empty")
    for i, f in enumerate(q3["form_fields"]):
        need(f, ["label", "data_slot", "kind"], "q3.form_fields[%d]" % i)
    if not isinstance(q3["submit_call_order"], list) or not all(isinstance(s, str) for s in q3["submit_call_order"]):
        bad("q3.submit_call_order is not a list of strings")
    if not isinstance(q3["attachment_controls"], list) or not q3["attachment_controls"]:
        bad("q3.attachment_controls is empty")
    for i, a in enumerate(q3["attachment_controls"]):
        need(a, ["item", "data_slot", "route"], "q3.attachment_controls[%d]" % i)
    need(q3["holdings_file"], ["path", "firm", "columns"], "q3.holdings_file")
    evidence(q3, "q3")

    q4 = rec["q4"]
    need(q4, ["preconditions", "recommend", "deciding_fact", "evidence"], "q4")
    if not isinstance(q4["preconditions"], list) or not q4["preconditions"]:
        bad("q4.preconditions is empty")
    for i, p in enumerate(q4["preconditions"]):
        need(p, ["fact", "check", "expected", "source"], "q4.preconditions[%d]" % i)
    if q4["recommend"] not in RECOMMEND:
        bad("q4.recommend not in enum: %r" % (q4["recommend"],))
    evidence(q4, "q4")

    if not isinstance(rec["not_read"], str) or not rec["not_read"].strip():
        bad("not_read is empty")

    print("SHAPE-OK " + ",".join(TOP))


if __name__ == "__main__":
    main()
