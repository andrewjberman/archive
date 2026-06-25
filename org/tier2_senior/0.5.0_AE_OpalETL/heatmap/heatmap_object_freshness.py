#!/usr/bin/env python3
"""HEATMAP_OBJECT O1 -- estate write-freshness producer (NFRA_HEATMAP, Andrew-direct via COO).

The OBJECT-side substrate producer: materialize the per-path WRITE-FRESHNESS of the
ajb_workspace estate from git history (authoritative for tracked files) + filesystem
mtime (untracked/generated), and emit a hot/warm/cold heat snapshot. A DERIVED view
from git -- NO new store (COO 212340Z): the snapshot is the git-history projected
through a recency-decay score. HOURLY cadence (a write-activity time-series).

LANE SPLIT (coordinated with DS 213948Z): S0 (DS) owns the shared heat_map analytic
PRIMITIVE -- the decay/score + clustering math, domain-parameterized. O1 (this, AE)
owns the OBJECT-substrate extraction + emit. The scoring is isolated in score_band()
so it swaps to S0's pinned contract with zero extraction change.

ADVISORY-ONLY note: this produces FRESHNESS SCORES only. The archive/delete
RECOMMENDATION (O3) + the verify-before-recommend blast-radius chain (inherit
NFRA_DEBTSCAN never-auto-delete) are SEPARATE layers. O1 never recommends a delete.

Usage:
    python heatmap_object_freshness.py                 # snapshot to stdout summary
    python heatmap_object_freshness.py --out snap.json # full per-path snapshot JSON
    python heatmap_object_freshness.py --top 30        # the N coldest paths
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time

# --- decay/banding: PLACEHOLDER pending DS's S0 score() contract (213948Z) ---
# O1 calls score_band(age_days) -> swap this body for S0.score() when DS pins the
# decay/half-life + band thresholds. Defaults: exponential recency, week/month bands.
HOT_DAYS = 7      # < 7d  -> hot
WARM_DAYS = 30    # < 30d -> warm; >= 30d -> cold
HALF_LIFE_DAYS = 14.0


def score_band(age_days: float) -> tuple[float, str]:
    """Per-path heat: exp recency score (1.0=just-written -> 0=ancient) + a band.
    TODO(S0): replace with DS's pinned score()/decay when the contract lands."""
    score = 0.5 ** (age_days / HALF_LIFE_DAYS)
    band = "hot" if age_days < HOT_DAYS else ("warm" if age_days < WARM_DAYS else "cold")
    return round(score, 4), band


def _git(args: list[str]) -> str:
    return subprocess.run(
        ["git"] + args, capture_output=True, text=True, check=True,
    ).stdout


def tracked_last_write() -> dict[str, int]:
    """Per-tracked-path last-commit epoch, from one git-log walk (authoritative for
    tracked files). Reuses git as the write-history substrate (not re-derived)."""
    last: dict[str, int] = {}
    # %x00-delimited: each commit line is "<ct>", then its changed paths follow.
    out = _git(["log", "--no-merges", "--name-only", "--format=%x00%ct"])
    ct = 0
    for line in out.splitlines():
        if line.startswith("\x00"):
            ct = int(line[1:]) if line[1:].isdigit() else ct
        elif line.strip():
            # first time we see a path (log is newest-first) = its last write
            if line not in last:
                last[line] = ct
    return last


def untracked_mtime() -> dict[str, int]:
    """Per-untracked-path mtime (generated/uncommitted files). git ls-files honors
    .gitignore so we don't heat-score ignored build slop."""
    out = _git(["ls-files", "--others", "--exclude-standard"])
    mt: dict[str, int] = {}
    for p in out.splitlines():
        if not p.strip():
            continue
        try:
            mt[p] = int(os.path.getmtime(p))
        except OSError:
            continue
    return mt


def build_snapshot(now: int) -> dict:
    tracked = tracked_last_write()
    untracked = untracked_mtime()
    rows = []
    for path, ts in {**tracked, **{k: v for k, v in untracked.items() if k not in tracked}}.items():
        age_days = (now - ts) / 86400.0
        score, band = score_band(age_days)
        rows.append({
            "path": path,
            "last_write_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts)),
            "source": "git" if path in tracked else "mtime",
            "age_days": round(age_days, 2),
            "score": score,
            "band": band,
        })
    rows.sort(key=lambda r: r["age_days"], reverse=True)  # coldest first
    bands = {"hot": 0, "warm": 0, "cold": 0}
    for r in rows:
        bands[r["band"]] += 1
    return {
        "schema_version": "0.1",
        "analytic": "heatmap_object_write_freshness",
        "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "path_count": len(rows),
        "band_counts": bands,
        "decay": {"half_life_days": HALF_LIFE_DAYS, "hot_days": HOT_DAYS, "warm_days": WARM_DAYS,
                  "note": "PLACEHOLDER -- swaps to S0.score() when DS pins the contract"},
        "paths": rows,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="HEATMAP_OBJECT O1 write-freshness producer")
    ap.add_argument("--out", default="", help="write the full snapshot JSON here")
    ap.add_argument("--top", type=int, default=20, help="show the N coldest paths in the summary")
    args = ap.parse_args()

    now = int(time.time())
    snap = build_snapshot(now)

    if args.out:
        with open(args.out, "w") as f:
            json.dump(snap, f, indent=2)
        print("OK: snapshot -> %s (%d paths)" % (args.out, snap["path_count"]))

    print("HEATMAP_OBJECT write-freshness @ %s" % snap["run_utc"])
    print("  paths=%d  hot=%d warm=%d cold=%d"
          % (snap["path_count"], snap["band_counts"]["hot"],
             snap["band_counts"]["warm"], snap["band_counts"]["cold"]))
    print("  (ADVISORY substrate only -- archive/delete recs are O3, with the DEBTSCAN verify-before-recommend chain)")
    print("  coldest %d:" % args.top)
    for r in snap["paths"][:args.top]:
        print("    %-7s %6.0fd  %s" % (r["band"], r["age_days"], r["path"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
