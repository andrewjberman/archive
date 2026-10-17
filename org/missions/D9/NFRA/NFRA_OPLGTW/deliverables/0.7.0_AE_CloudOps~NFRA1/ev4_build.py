#!/usr/bin/env python
"""OG-ev-4: assemble W/MEMORY_RETENTION.json from the host driver record (ev4_driver.json). Numbers and fixed words only.
median_growth_mb = the median of the page-to-page RSS growth over pages 2 to n; flattening_variant = among B to F the lowest median when it is 20 MB per page or less, else none.
usage: python ev4_build.py   (repository root of the worktree that holds the record)"""
from __future__ import annotations

import datetime
import io
import json
import statistics

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
THRESHOLD = 20
d = json.load(io.open(W + "ev4_driver.json", encoding="utf-8"))
variants = {}
for letter in "ABCDEF":
    v = d["variants"][letter]
    pages = [{"page": p["page"], "rss_mb": p["rss_mb"], "host_pct": p["host_pct"], "wall_s": p["wall_s"]} for p in v["pages"]]
    rs = [p["rss_mb"] for p in pages]
    growth = [round(rs[i] - rs[i - 1], 1) for i in range(1, len(rs))]
    variants[letter] = {"label": v["label"], "rss_before_mb": v["rss_before_mb"], "pages": pages, "median_growth_mb": round(statistics.median(growth), 1) if growth else None,
                        "stopped_at_host_pct": bool(v.get("stopped_at_host_pct")), "page_to_page_growth_mb": growth, "host_pct_at_start": v.get("host_pct_at_start"),
                        "pyarrow_imported": bool(v.get("pyarrow_imported"))}
cands = {k: v["median_growth_mb"] for k, v in variants.items() if k != "A" and v["median_growth_mb"] is not None}
best = min(cands, key=cands.get)
flat = best if cands[best] <= THRESHOLD else "none"
body = {"read_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "release_sha": "b124377b41caf5665b999378fd0ca08ad8a1fb7d",
        "host_total_mb": d["host_total_mb"], "idle_host_pct": d["idle_host_pct"], "threshold_mb_per_page": THRESHOLD, "variants": variants, "flattening_variant": flat,
        "lowest_median_variant_among_b_to_f": best, "staged_app_md5_equals_release": all(d["staged_md5_equals_release"].values()), "stage_removed": d["stage_removed"]}
io.open(W + "MEMORY_RETENTION.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({"medians": {k: v["median_growth_mb"] for k, v in variants.items()}, "flattening_variant": flat, "lowest_b_to_f": best, "idle": d["idle_host_pct"],
                  "starts": {k: v["host_pct_at_start"] for k, v in variants.items()}}))
