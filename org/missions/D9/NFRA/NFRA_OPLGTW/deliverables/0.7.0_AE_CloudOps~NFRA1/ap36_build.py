#!/usr/bin/env python
"""OG-ap-36 Phase A step 3: assemble W/MEM_GATE_OG-ap-36.json from the host driver record (ap36_measure.driver.json), and the UNTRACKED W/PAGE_HASHES_OG-ap-36.json.
No value is typed here that the record does not hold. Prints each of the five measurements (a) to (e) with its pass line from the order.
usage: python ap36_build.py <release_sha>   (repository root of the worktree that holds the driver record)"""
from __future__ import annotations

import io
import json
import statistics
import sys

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
REL = sys.argv[1]
d = json.load(io.open(W + "ap36_measure.driver.json", encoding="utf-8"))
assert d.get("stage_removed") and d.get("resolve_ok"), "the scratch folders were not removed or no account resolved"
assert all(d["staged_md5_equals_release"].values()), "the staged candidate is not the release"
cc, cl = d["chain_cand"], d["chain_live"]
for k in ("chain_cand", "chain_live", "plateau_cand", "health_cand", "health_live"):
    assert d[k].get("exit_code") == 0 and not d[k].get("no_result"), (k, d[k])

# (a) the chain
pages = [{"page": p["page"], "rss_mb": p["rss_mb"], "host_pct": p["host_pct"], "wall_s": p["wall_s"]} for p in cc["pages"]]
rs = [p["rss_mb"] for p in pages]
growth = [rs[i] - rs[i - 1] for i in range(1, len(rs))]
median_growth = round(statistics.median(growth), 1)
peak = max([p["host_pct"] for p in pages] + [cc["host_pct_before"]])
a_ok = len(pages) == 6 and median_growth <= 20 and pages[0]["wall_s"] <= 45 and peak < 75
# (b) the plateau test
c1, c2 = d["plateau_cand"]["chains"][0], d["plateau_cand"]["chains"][1]
net = round(c2["rss_end_mb"] - c1["rss_end_mb"], 1)
maxwall = max(c1["max_page_wall_s"], c2["max_page_wall_s"])
b_ok = net <= 50 and d["plateau_cand"]["peak_host_pct"] < 80 and maxwall <= 55 and c1["ended_with_null_cursor"] and c2["ended_with_null_cursor"]
# (c) the first page wall, three alternating runs each: the median of each
lw = [r["first_page_wall_s"] for r in d["first_live"]]
cw = [r["first_page_wall_s"] for r in d["first_cand"]]
live_first, cand_first = round(statistics.median(lw), 2), round(statistics.median(cw), 2)
c_ok = cand_first < live_first and all(r["ok"] for r in d["first_live"] + d["first_cand"])
# (d) byte equality of the pages
pairs = list(zip(cc["pages"], cl["pages"]))
eq = [p["rows"] == q["rows"] and p["sha256"] == q["sha256"] and p["cursor_used"] == q["cursor_used"] and p["next_cursor"] == q["next_cursor"] for p, q in pairs]
d_ok = len(pairs) >= 3 and all(eq) and len(cc["pages"]) == len(cl["pages"])
# (e) health during a page
hc, hl = d["health_cand"], d["health_live"]
e_ok = hc["probes"] >= 3 and hc["max_probe_s"] < 1.0 and hc["all_200"] and hc["page_ok"]
body = {"release_sha": REL, "rss_before_mb": cc["rss_before_mb"], "pages": pages, "median_growth_mb": median_growth, "threshold_mb_per_page": 20, "peak_host_pct": peak,
        "plateau": {"net_growth_mb": net, "peak_host_pct": d["plateau_cand"]["peak_host_pct"], "max_page_wall_s": maxwall},
        "wall": {"live_first_page_s": live_first, "candidate_first_page_s": cand_first},
        "equality": {"pages_compared": len(pairs), "pages_equal": sum(1 for x in eq if x)},
        "health": {"probes": hc["probes"], "max_probe_s": hc["max_probe_s"]},
        "detail": {"first_page_walls_live_s": lw, "first_page_walls_candidate_s": cw, "plateau_chain_pages": [c1["pages"], c2["pages"]],
                   "plateau_chain_end_rss_mb": [c1["rss_end_mb"], c2["rss_end_mb"]], "plateau_partitions_read": [c1["partitions_read_total"], c2["partitions_read_total"]],
                   "live_health_longest_probe_s": hl["max_probe_s"], "live_health_probes": hl["probes"], "live_health_page_wall_s": hl["page_wall_s"],
                   "candidate_health_page_wall_s": hc["page_wall_s"], "idle_host_pct": d["idle_host_pct"], "host_total_mb": d["host_total_mb"],
                   "live_chain_median_growth_mb": round(statistics.median([cl["pages"][i]["rss_mb"] - cl["pages"][i - 1]["rss_mb"] for i in range(1, len(cl["pages"]))]), 1)},
        "memory_basis": "fresh_process"}
io.open(W + "MEM_GATE_OG-ap-36.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps({"body": body}, indent=1) + chr(10))
hashes = {"release_sha": REL, "candidate": [{k: p[k] for k in ("page", "rows", "sha256", "cursor_used", "next_cursor")} for p in cc["pages"]],
          "live": [{k: p[k] for k in ("page", "rows", "sha256", "cursor_used", "next_cursor")} for p in cl["pages"]], "page_equal": eq}
io.open(W + "PAGE_HASHES_OG-ap-36.json", "w", encoding="utf-8", newline=chr(10)).write(json.dumps(hashes, indent=1) + chr(10))
print("(a) chain: pages %d, median growth %s MB (<=20), first page %s s (<=45), host peak %s (<75): %s" % (len(pages), median_growth, pages[0]["wall_s"], peak, "PASS" if a_ok else "FAIL"))
print("(b) plateau: net growth %s MB (<=50), host peak %s (<80), longest page %s s (<=55), both chains null cursor: %s" % (net, d["plateau_cand"]["peak_host_pct"], maxwall, "PASS" if b_ok else "FAIL"))
print("(c) first page: live %s s %s, candidate %s s %s (want candidate < live): %s" % (live_first, lw, cand_first, cw, "PASS" if c_ok else "FAIL"))
print("(d) pages equal live row for row: %d of %d: %s" % (sum(1 for x in eq if x), len(pairs), "PASS" if d_ok else "FAIL"))
print("(e) health during a page: candidate %d probes, longest %s s (<1): %s; live code: %d probes, longest %s s" % (hc["probes"], hc["max_probe_s"], "PASS" if e_ok else "FAIL", hl["probes"], hl["max_probe_s"]))
print("ALL PASS" if all((a_ok, b_ok, c_ok, d_ok, e_ok)) else "NOT ALL PASS")
