#!/usr/bin/env python
"""OG-rl-17 Phase B: assemble W/RL17_PROOFS.json and W/rl17_memory_at_peak.json from the proof records in W/rl17_pb/proofs/ (no value is typed here that a record holds). Counts and flags only; no account number or last-4.
  proofs/d1.json            {"orion": {answered, absent_reason, candidate_count}, "eclipse": {...}, "commonwealth": {...}, "control_unserved_pair": {absent_reason}}   (written by the applier from the served answers)
  proofs/d2.json            {"transactions": n}
  proofs/load_calls.json    {"calls": 8, "completed": c, "gateway_busy": b, "other_errors": e}
  proofs/projection.json    {"aggregate_aua_bytes": n, "opal_discover_bytes": n}
  mem_load.json             rz2_mem.py collect output for the load window;  health.jsonl  the /health sampler;  indexpairs.json  rl17_indexpairs.py output
usage: python rl17_proofs_build.py <load_start_utc> <load_end_utc>   (repository root; the /health samples counted are those inside the load window)"""
from __future__ import annotations

import io
import json
import sys

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
R = W + "rl17_pb/"
START, END = sys.argv[1:3]


def load(path):
    return json.load(io.open(path, encoding="utf-8"))


d1, d2, lc, pj = (load(R + "proofs/%s.json" % n) for n in ("d1", "d2", "load_calls", "projection"))
mem, ip = load(R + "mem_load.json"), load(R + "indexpairs.json")
samples = [json.loads(ln) for ln in io.open(R + "health.jsonl", encoding="utf-8") if ln.strip()]
inwin = [s for s in samples if START <= s["t"] <= END]
ok = sum(1 for s in inwin if s["code"] == 200)
bad = len(inwin) - ok
peak, before = mem["max_mb"], mem["before_mb"]
per_call = (peak - before) / 8.0
scaled = before + per_call * 26
proofs = {"d1": d1, "d2": d2,
          "load": {"calls": lc["calls"], "completed": lc["completed"], "gateway_busy": lc["gateway_busy"], "other_errors": lc["other_errors"], "health_200_samples": ok, "health_non_200_samples": bad,
                   "service_peak_mb": peak, "service_before_mb": before, "memory_high_mb": mem["memory_high_mb"], "load_window_utc": [START, END], "health_slowest_ms": max((s["ms"] for s in inwin), default=None)},
          "projection": pj,
          "index_pairs": {"segmented_tools": ip["segmented_tools"], "with_index_pairs": ip["with_index_pairs"], "segmented_buckets": ip["segmented_buckets"], "guard": ip["guard"]}}
io.open(W + "RL17_PROOFS.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": proofs}, indent=1) + "\n")
atpeak = {"method": "MemoryCurrent of the gateway service's cgroup sampled every 0.5 s during the 8-call load (rz2_mem.py); per-call growth = (peak - before) / 8; scaled to 26 concurrent calls = before + 26 x per-call growth (a linear bound, the CVO's note)",
          "before_mb": before, "peak_mb_at_8_calls": peak, "per_call_mb": round(per_call, 1), "scaled_to_26_mb": round(scaled, 1), "memory_high_mb": mem["memory_high_mb"], "memory_max_mb": mem["memory_max_mb"],
          "scaled_below_memory_high": scaled < mem["memory_high_mb"], "scaled_below_memory_max": scaled < mem["memory_max_mb"], "cgroup_peak_mb": mem.get("cgroup_peak_mb"), "calls_completed": lc["completed"], "gateway_busy": lc["gateway_busy"]}
io.open(W + "rl17_memory_at_peak.json", "w", encoding="utf-8", newline="\n").write(json.dumps(atpeak, indent=1) + "\n")
print(json.dumps(proofs["load"]), json.dumps({k: atpeak[k] for k in ("before_mb", "peak_mb_at_8_calls", "per_call_mb", "scaled_to_26_mb", "scaled_below_memory_high")}))
