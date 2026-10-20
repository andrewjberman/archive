#!/usr/bin/env python
"""OG-rl-19 Phase A (b): compare the old-form reads of the live tree with the candidate's, from W/rl19_pa/host_leg.json -> W/rl19_pa/oldform_compare.json. The live tree's read is its private _read_marker; the candidate's is the public read_marker
(or its private one if it still exists). Equal = the same answer, the same S3 calls, and the state bucket never called. usage: python rl19_oldform_compare.py   (repository root)"""
import json

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
d = json.load(open(W + "rl19_pa/host_leg.json"))
live, cand = d["oldform_live"], d["oldform_candidate"]
res = {}
for m in ("08242234", "08335338"):
    a, b = live["masters"][m], cand["masters"][m]
    cm = b["read_marker"] if b["read_marker"] is not None else b["legacy_read_marker"]
    cc = b["read_marker_calls"] if b["read_marker"] is not None else b["legacy_read_marker_calls"]
    res[m] = {"marker_answer_equal": a["legacy_read_marker"] == cm, "marker_calls_equal": a["legacy_read_marker_calls"] == cc, "list_dates_equal": a["list_dates"] == b["list_dates"],
              "list_dates_calls_equal": a["list_dates_calls"] == b["list_dates_calls"], "candidate_state_bucket_called": b["state_bucket_called"], "candidate_marker_locations": b["marker_locations"],
              "live_calls": a["legacy_read_marker_calls"], "cand_has_private_read_marker": b["legacy_read_marker"] is not None}
ok = all(v["marker_answer_equal"] and v["marker_calls_equal"] and v["list_dates_equal"] and v["list_dates_calls_equal"] and not v["candidate_state_bucket_called"] for v in res.values())
json.dump({"old_form_unchanged": ok, "per_master": res}, open(W + "rl19_pa/oldform_compare.json", "w", newline="\n"), indent=1)
print("old_form_unchanged", ok)
