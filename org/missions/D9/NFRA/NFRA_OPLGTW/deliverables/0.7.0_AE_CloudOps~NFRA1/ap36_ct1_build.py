#!/usr/bin/env python
"""OG-ap-36 PHASE A ADDENDUM 4c: assemble W/CT1_CONCURRENT_OG-ap-36.json from the host driver record (ap36_ct1.driver.json) and append the two per-page counts of the candidate and of the
LIVE code to the untracked, git-excluded W/PAGE_HASHES_OG-ap-36.json (for Phase B's e11). No value is typed here that the record does not hold.
usage: python ap36_ct1_build.py <release_sha>   (repository root of the worktree that holds the driver record)"""
from __future__ import annotations

import io
import json
import sys

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
REL = sys.argv[1]
d = json.load(io.open(W + "ap36_ct1.driver.json", encoding="utf-8"))
assert d.get("stage_removed") and d.get("resolve_ok") and all(d["staged_md5_equals_release"].values()), "scratch not removed, no account, or the staged candidate is not the release"
for k in ("counts_cand", "counts_live", "ct1_real", "ct1_short"):
    assert d[k].get("exit_code") == 0 and not d[k].get("no_result"), (k, d[k])
cc, cl = d["counts_cand"]["pages"], d["counts_live"]["pages"]
keys = ("rows", "sha256", "partition_rows", "fence_excluded", "cursor_used", "next_cursor")
eq = [all(p[k] == q[k] for k in keys) and p["partition_rows"] is not None and p["fence_excluded"] is not None for p, q in zip(cc, cl)]
real, short = d["ct1_real"], d["ct1_short"]
probes = real["probes"] + short["probes"]
maxp = max(real["max_probe_s"], short["max_probe_s"])
body = {"release_sha": REL, "first_equals_solo": bool(real["first_equals_solo"] and short["first_equals_solo"]),
        "second_real_gate": real["second_outcome"], "second_short_gate": short["second_outcome"],
        "health": {"probes": probes, "max_probe_s": maxp}, "counts": {"pages_compared": len(eq), "pages_equal": sum(1 for x in eq if x)},
        "detail": {"real": {k: real[k] for k in ("rss_before_mb", "rss_after_solo_mb", "rss_after_pair_mb", "gate_wait_s", "solo_wall_s", "solo_rows", "first_equals_solo", "second_busy_key", "second_absent_reason", "second_retry_after_seconds", "first_done_s", "second_done_s", "probe_interval_s", "probes", "max_probe_s", "all_200")},
                   "short": {k: short[k] for k in ("rss_before_mb", "rss_after_solo_mb", "rss_after_pair_mb", "gate_wait_s", "solo_wall_s", "solo_rows", "first_equals_solo", "second_busy_key", "second_absent_reason", "second_retry_after_seconds", "first_done_s", "second_done_s", "probe_interval_s", "probes", "max_probe_s", "all_200")},
                   "pages_with_nonzero_fence_excluded": sum(1 for p in cl if p["fence_excluded"]), "partition_rows_total_live": sum(p["partition_rows"] or 0 for p in cl),
                   "fence_excluded_total_live": sum(p["fence_excluded"] or 0 for p in cl)},
        "memory_basis": "fresh_process"}
io.open(W + "CT1_CONCURRENT_OG-ap-36.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
ph = json.load(io.open(W + "PAGE_HASHES_OG-ap-36.json", encoding="utf-8"))
ph["live_counts"] = [{"page": p["page"], "partition_rows": p["partition_rows"], "fence_excluded": p["fence_excluded"]} for p in cl]
ph["candidate_counts"] = [{"page": p["page"], "partition_rows": p["partition_rows"], "fence_excluded": p["fence_excluded"]} for p in cc]
ph["counts_page_equal"] = eq
io.open(W + "PAGE_HASHES_OG-ap-36.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps(ph, indent=1) + chr(10))
ok_real = body["second_real_gate"] in ("waited_then_equal_solo", "window_read_busy")
ok = body["first_equals_solo"] and ok_real and body["second_short_gate"] == "window_read_busy" and probes >= 3 and maxp < 1.0 and len(eq) >= 6 and all(eq)
print("first equals solo (real, short): %s, %s" % (real["first_equals_solo"], short["first_equals_solo"]))
print("second under the real 15 s gate wait: %s (solo page %s s; second done at %s s)" % (real["second_outcome"], real["solo_wall_s"], real["second_done_s"]))
print("second under a 0.5 s gate wait: %s (second done at %s s)" % (short["second_outcome"], short["second_done_s"]))
print("health through both pairs: %d probes, longest %s s (limit 1)" % (probes, maxp))
print("partition_rows, fence_excluded, rows and sha per page, candidate against live: %d of %d equal" % (sum(1 for x in eq if x), len(eq)))
print("ALL PASS" if ok else "NOT ALL PASS")
