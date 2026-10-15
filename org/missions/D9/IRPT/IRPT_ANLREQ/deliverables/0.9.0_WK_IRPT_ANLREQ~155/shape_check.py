#!/usr/bin/env python3
"""AR-y-357 shape check: r41/PACKAGE_REFUSAL_READ.json carries every key the cell names, with allowed values.

Prints SHAPE-OK <top-level keys> (exit 0) or SHAPE-BAD <why> (exit 1). Every answer block must carry at least
one evidence item. ASCII only; reads the record beside this file; no AWS, no git.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD = HERE / "r41" / "PACKAGE_REFUSAL_READ.json"

TOP = ("base", "q1", "q2", "q3", "q4", "q5", "q6", "cause", "deciding_fact", "smallest_change", "evidence", "not_read")
TRI = ("yes", "no", "unknown")
ENUM = {
    ("q2", "reserved_row_raises"): TRI,
    ("q3", "can_leave_reserved"): TRI,
    ("q3", "packaging_path_expects_accepted"): TRI,
    ("q4", "first_two_refusals_same_family"): TRI,
    ("q5", "idempotent"): TRI,
    ("q5", "recommended_disposition"): ("leave", "redrive_after_fix", "discard_after_ruling"),
    ("q6", "owner_kind"): ("drafter", "resident", "retention_service", "unknown"),
    ("q6", "expires"): TRI,
}
CAUSE = ("RETENTION_RESERVED", "AUTHORITY", "BOTH", "UNDETERMINED")
REQUIRED = {
    "q1": ("steps", "report_refused_sites", "evidence"),
    "q2": ("sites", "reserved_row_raises", "admitted_retention_states", "journal_code_source", "evidence"),
    "q3": ("reserve_site", "accept_site", "can_leave_reserved", "what_moves_to_accepted",
           "packaging_path_expects_accepted", "evidence"),
    "q4": ("actor_not_found_site", "reads", "first_two_refusals_same_family", "owner_authority_rule", "evidence"),
    "q5": ("dlq_move_site", "redrive_policy", "redrive_would", "idempotent", "who_may_redrive",
           "recommended_disposition", "evidence"),
    "q6": ("owner", "owner_kind", "who_may_accept", "expires", "policy_revision", "evidence"),
}
SITE_KEYS = ("file", "line", "text")
SMALL_KEYS = ("file", "function", "change", "rides")


def bad(why):
    print("SHAPE-BAD " + why)
    sys.exit(1)


def main():
    try:
        rec = json.loads(RECORD.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        bad("record unreadable: " + type(exc).__name__)
    if not isinstance(rec, dict):
        bad("record is not an object")
    for key in TOP:
        if key not in rec:
            bad("missing top-level key " + key)
    if not isinstance(rec["evidence"], list) or not rec["evidence"]:
        bad("top-level evidence has no item")
    if not isinstance(rec["not_read"], str) or not rec["not_read"].strip():
        bad("not_read is empty")
    if not isinstance(rec["base"], str) or len(rec["base"]) < 7:
        bad("base is not a sha")
    for block, keys in REQUIRED.items():
        sub = rec[block]
        if not isinstance(sub, dict):
            bad(block + " is not an object")
        for key in keys:
            if key not in sub:
                bad("missing %s.%s" % (block, key))
        if not isinstance(sub["evidence"], list) or not sub["evidence"]:
            bad("%s.evidence has no item" % block)
    for (block, key), allowed in ENUM.items():
        if rec[block][key] not in allowed:
            bad("%s.%s=%r is not one of %s" % (block, key, rec[block][key], "/".join(allowed)))
    if rec["cause"] not in CAUSE:
        bad("cause=%r is not one of %s" % (rec["cause"], "/".join(CAUSE)))
    for key in ("steps", "report_refused_sites"):
        if not isinstance(rec["q1"][key], list) or not rec["q1"][key]:
            bad("q1.%s is empty" % key)
    if not isinstance(rec["q2"]["sites"], list) or not rec["q2"]["sites"]:
        bad("q2.sites is empty")
    if not isinstance(rec["q2"]["admitted_retention_states"], list) or not rec["q2"]["admitted_retention_states"]:
        bad("q2.admitted_retention_states is empty")
    for site in rec["q2"]["sites"]:
        if site.get("has_code") not in (True, False) or not isinstance(site.get("condition"), str):
            bad("q2.sites item lacks has_code or condition")
    for name, site in (("q1.step", rec["q1"]["steps"][0]), ("q3.reserve_site", rec["q3"]["reserve_site"]),
                       ("q3.accept_site", rec["q3"]["accept_site"]), ("q4.actor_not_found_site",
                       rec["q4"]["actor_not_found_site"]), ("q5.dlq_move_site", rec["q5"]["dlq_move_site"]),
                       ("q2.journal_code_source", rec["q2"]["journal_code_source"])):
        if not all(k in site for k in SITE_KEYS):
            bad("%s lacks file, line or text" % name)
    if not all(k in rec["smallest_change"] for k in SMALL_KEYS):
        bad("smallest_change lacks file, function, change or rides")
    print("SHAPE-OK " + ",".join(TOP))
    return 0


if __name__ == "__main__":
    sys.exit(main())
