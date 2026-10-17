#!/usr/bin/env python
"""OG-ap-35 Phase A: merge AG1_BEFORE_state.json and AG1_usage.json into W/AG1_BEFORE.json (the order's shape). Counts, names and hashes only.
usage: python ag1_merge.py   (repository root of the worktree that holds the records)"""
import io
import json
import os

W = os.path.join("org", "missions", "D9", "NFRA", "NFRA_OPLGTW", "deliverables", "0.7.0_AE_CloudOps~NFRA1")
s = json.load(io.open(os.path.join(W, "AG1_BEFORE_state.json"), encoding="utf-8"))
u = json.load(io.open(os.path.join(W, "AG1_usage.json"), encoding="utf-8"))
a, b = u["sources"]["A_general_lake"], u["sources"]["B_schwab_prefix"]
usage = {
    "download_filtered_calls_since_grant": b["her_download_calls"],
    "last_use": b["last_download_use"],
    "window_start": u["window_start"],
    "source": "the Schwab acknowledged audit prefix of the gateway audit lake: every release awaits its receipt there, events carry the principal as a hash and the operation as a fixed word",
    "window_end_day": u["window_end_day"],
    "days_listed": u["days_listed"],
    "events_by_her_principal_in_the_window": b["her_records"],
    "distinct_operations_among_her_events": b["her_other_tools_distinct"],
    "download_events_by_any_principal_in_the_window": b["any_principal_download_calls"],
    "schwab_prefix_objects_listed_and_read": [b["objects_listed"], b["objects_read"]],
    "schwab_prefix_read_errors_and_malformed": [b["read_errors"], b["malformed"]],
    "general_lake_objects_listed_and_read": [a["objects_listed"], a["objects_read"]],
    "general_lake_records_by_her_principal": a["her_records"],
    "general_lake_used_as_evidence": False,
    "general_lake_note": "the general audit lake holds no record carrying her principal in the window (the control that it can see her failed), so its zero is reported and not relied on",
    "positive_control": {"her_events_seen_in_the_schwab_prefix": u["positive_control"]["her_principal_seen_in_schwab_prefix"],
                         "a_download_event_seen_for_some_principal": b["any_principal_download_calls"] > 0},
    "download_filtered_added_to_her_grant_at": u["download_filtered_added_at"],
    "calls_since_added_to_her_grant": b["her_download_calls_since_added"],
}
body = {"read_at": s["read_at"], "denominator": s["denominator"], "method": s["method"], "alyssa": s["alyssa"], "usage": usage, "others_hash": s["others_hash"],
        "others_state": s["others_state"], "alyssa_grant_timeline": s["alyssa_grant_timeline"], "side_write_state": s["side_write_state"]}
io.open(os.path.join(W, "AG1_BEFORE.json"), "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({"alyssa": body["alyssa"], "usage_since_grant": usage["download_filtered_calls_since_grant"], "last_use": usage["last_use"], "her_events": usage["events_by_her_principal_in_the_window"]}))
