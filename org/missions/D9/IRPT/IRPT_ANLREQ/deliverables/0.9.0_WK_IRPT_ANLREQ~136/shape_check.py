"""AR-y-328 shape check: loads r41/RESIDENT_BINDINGS_READ.json and checks every key the cell requires.

Prints SHAPE-OK <keys> (exit 0) or SHAPE-BAD <why> (exit 1). ASCII only. Reads no AWS and no source file.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RECORD = os.path.join(HERE, "r41", "RESIDENT_BINDINGS_READ.json")

TOP = ("base", "q1", "q2", "q3", "q4", "host_env_file", "install_mechanism", "mechanism_evidence", "not_read")
WIRINGS = ("analysis_ready_send", "drafter_consumer", "commentary_ready_send", "packager_consumer", "packager_ports")
VALUE_CLASSES = ("queue_url", "queue_name", "secret_name", "base_url", "flag", "other")
WHEN_UNSET = ("skip", "warn", "raise", "refuse", "other")
R29_STATES = ("set", "unset", "absent")
TARGETS = ("analysis_ready_queue", "commentary_ready_queue", "dead_letter_queue", "packager_secret",
           "packager_principal_row")
NEEDS = ("worker_buildable", "applier_live_read", "andrew_act")


class Bad(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Bad(why)


def cite(obj, where):
    need(isinstance(obj, dict), where + ": cite is not an object")
    need(isinstance(obj.get("file"), str) and obj["file"].strip(), where + ": cite file missing")
    need(isinstance(obj.get("line"), int) and not isinstance(obj.get("line"), bool) and obj["line"] >= 1,
         where + ": cite line is not a positive integer")
    need(isinstance(obj.get("text"), str) and obj["text"].strip(), where + ": cite text missing")


def cites(lst, where):
    need(isinstance(lst, list) and len(lst) >= 1, where + ": no evidence item")
    for i, c in enumerate(lst):
        cite(c, "%s[%d]" % (where, i))


def check(doc):
    for k in TOP:
        need(k in doc, "missing key " + k)
    need(isinstance(doc["base"], str) and re.fullmatch(r"[0-9a-f]{40}", doc["base"]) is not None,
         "base is not a full 40-hex sha")

    q1 = doc["q1"]
    need(isinstance(q1, list) and q1, "q1 is not a non-empty list")
    seen = set()
    for i, row in enumerate(q1):
        w = "q1[%d]" % i
        need(isinstance(row, dict), w + " is not an object")
        need(row.get("wiring") in WIRINGS, w + " wiring not in the five")
        seen.add(row["wiring"])
        need(isinstance(row.get("name"), str) and row["name"].strip(), w + " name missing")
        cite(row.get("read_at"), w + ".read_at")
        need(row.get("value_class") in VALUE_CLASSES, w + " value_class not in enum")
        need(row.get("when_unset") in WHEN_UNSET, w + " when_unset not in enum")
        cite(row.get("when_unset_evidence"), w + ".when_unset_evidence")
    need(seen == set(WIRINGS), "q1 does not cover all five wirings: missing %s" % sorted(set(WIRINGS) - seen))

    q2 = doc["q2"]
    need(isinstance(q2, list) and q2, "q2 is not a non-empty list")
    for i, row in enumerate(q2):
        w = "q2[%d]" % i
        need(isinstance(row, dict) and isinstance(row.get("name"), str) and row["name"].strip(), w + " name missing")
        need(row.get("r29_state") in R29_STATES, w + " r29_state not in enum")
        cites(row.get("evidence"), w + ".evidence")
    need(isinstance(doc["host_env_file"], str) and doc["host_env_file"].strip(), "host_env_file missing")
    need(isinstance(doc["install_mechanism"], str) and doc["install_mechanism"].strip(), "install_mechanism missing")
    cites(doc["mechanism_evidence"], "mechanism_evidence")

    q3 = doc["q3"]
    need(isinstance(q3, list) and q3, "q3 is not a non-empty list")
    seen = set()
    for i, row in enumerate(q3):
        w = "q3[%d]" % i
        need(isinstance(row, dict) and row.get("target") in TARGETS, w + " target not in enum")
        seen.add(row["target"])
        need(isinstance(row.get("declared"), bool), w + " declared is not a boolean")
        cites(row.get("evidence"), w + ".evidence")
        if row["declared"] is False:
            need(isinstance(row.get("searched"), str) and row["searched"].strip(), w + " declared false without searched")
        need(row.get("needs") in NEEDS, w + " needs not in enum")
    need(seen == set(TARGETS), "q3 does not cover all five targets: missing %s" % sorted(set(TARGETS) - seen))

    q4 = doc["q4"]
    need(isinstance(q4, dict), "q4 is not an object")
    cite(q4.get("edit_site"), "q4.edit_site")
    need(isinstance(q4.get("must_agree"), list) and q4["must_agree"], "q4.must_agree is empty")
    for i, row in enumerate(q4["must_agree"]):
        cite(row, "q4.must_agree[%d]" % i)
        need(isinstance(row.get("why"), str) and row["why"].strip(), "q4.must_agree[%d] why missing" % i)
    need(isinstance(q4.get("comment_change"), str) and q4["comment_change"].strip(), "q4.comment_change missing")

    need(isinstance(doc["not_read"], str) and doc["not_read"].strip(), "not_read missing")


def main():
    try:
        with open(RECORD, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        print("SHAPE-BAD cannot load record: %s" % type(exc).__name__)
        return 1
    if not isinstance(doc, dict):
        print("SHAPE-BAD record is not an object")
        return 1
    try:
        check(doc)
    except Bad as exc:
        print("SHAPE-BAD %s" % exc)
        return 1
    print("SHAPE-OK " + ",".join(sorted(k for k in doc if k in TOP + ("cell", "reading_root", "recommendation",
                                                                  "surprises"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
