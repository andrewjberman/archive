"""
validate_data_pkl.py -- pre-publication acceptance gate for the Yang data.pkl upload.

Born from the 2026-07-17 P0: the 07-15 pull carried a WRONG-SECURITY SUBSTITUTION
under '.ST Index' (Bloomberg CIX layer) -- full-history replacement of the Short
Term model NAV with an equity-like series (price ~1.9 vs base-100 NAV, daily ret
std ~1.5 vs 0.13). The Lambda math was correct on corrupt input; the defect was
only visible in the input's structure and magnitudes. These checks would each
have caught it independently:

  1. ROW-COUNT PARITY   -- all custom Term series in one pkl share one row count
                           (corrupt ST: 1438 rows vs 664 for the other 12).
  2. SPAN START MATCH   -- all custom Term series share one inception date
                           (2023-12-29; corrupt ST started 2021-01-04).
  3. MAGNITUDE CEILING  -- per-sleeve max |daily return| ceilings; a short-duration
                           sleeve emitting >2%/day refuses publication.
  4. LEVEL CONTINUITY   -- vs a prior-vintage pkl: overlapping-date returns must
                           match (a changed history is a redefinition, not an append).

Usage:
  python validate_data_pkl.py <candidate.pkl> [--prior <prior.pkl>] [--json]

Exit codes: 0 = PASS (publishable), 1 = FAIL (do NOT publish), 2 = usage/load error.
"""
from __future__ import annotations

import argparse
import json
import pickle
import sys

import pandas as pd

# Per-sleeve max |daily return| ceilings, percent -- calibrated ~1.5x each
# series' healthy-history max |daily ret| in data_20260712_v1.pkl (e.g. the
# 2025-04-09 shock day: INT 4.30, LTC 6.58, LTA 7.60). A breach is a
# wrong-security signal, not a market-moves signal (corrupt ST hit 13.37).
MAG_CEILINGS = {
    "Ultra Short Term": 1.0,
    "Ultra Short Term Benchmark": 1.5,
    "Ultra Short Term ETF": 1.5,
    "Short Term": 2.0,
    "Short Term Benchmark": 2.5,
    "Short Term ETF": 3.0,
    "Intermediate Term": 6.5,
    "Intermediate Term Benchmark": 5.0,
    "Intermediate Term ETF": 8.0,
    "Long Term Conservative": 10.0,
    "Long Term Benchmark": 7.5,
    "Long Term ETF": 11.5,
    "Long Term Agressive": 11.5,  # sic -- source spelling in return_daily
}
DEFAULT_CEILING = 12.0  # unlisted future series


def load_return_daily(path: str) -> pd.DataFrame:
    with open(path, "rb") as f:
        pkl = pickle.load(f)
    df = pkl["return_daily"].copy()
    df["date"] = pd.to_datetime(df["date"])
    return df


def term_series(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    term = df[df["index_name"].str.contains("Term", na=False)]
    return {name: g.sort_values("date") for name, g in term.groupby("index_name")}


def validate(candidate: str, prior: str | None) -> dict:
    findings = []
    df = load_return_daily(candidate)
    groups = term_series(df)
    if not groups:
        return {"pass": False, "findings": ["FAIL: no Term series found in return_daily"]}

    # 1. row-count parity
    counts = {n: len(g) for n, g in groups.items()}
    mode_count = pd.Series(list(counts.values())).mode()[0]
    for n, c in sorted(counts.items()):
        if c != mode_count:
            findings.append(
                f"FAIL row-count parity: {n!r} has {c} rows vs modal {mode_count}"
            )

    # 2. span start match
    starts = {n: g["date"].min() for n, g in groups.items()}
    mode_start = pd.Series(list(starts.values())).mode()[0]
    for n, s in sorted(starts.items()):
        if s != mode_start:
            findings.append(
                f"FAIL span start: {n!r} starts {s.date()} vs modal {mode_start.date()}"
            )

    # 3. magnitude ceilings
    for n, g in sorted(groups.items()):
        ceiling = MAG_CEILINGS.get(n, DEFAULT_CEILING)
        r = g["return"].dropna()
        worst = r.abs().max() if len(r) else 0.0
        if worst > ceiling:
            d = g.loc[g["return"].abs().idxmax(), "date"]
            findings.append(
                f"FAIL magnitude: {n!r} |daily ret| {worst:.2f}% > ceiling {ceiling}% on {d.date()}"
            )

    # 4. level continuity vs prior vintage
    if prior:
        dfp = load_return_daily(prior)
        gp = term_series(dfp)
        for n in sorted(set(groups) & set(gp)):
            m = groups[n].merge(gp[n], on="date", suffixes=("_new", "_old"))
            m = m.dropna(subset=["return_new", "return_old"])
            changed = (m["return_new"] - m["return_old"]).abs() > 1e-8
            if changed.any():
                findings.append(
                    f"FAIL continuity: {n!r} changed {int(changed.sum())}/{len(m)} "
                    f"overlapping-date returns vs prior vintage (redefinition, not append)"
                )

    return {
        "pass": not findings,
        "findings": findings or ["PASS: all checks clean"],
        "series_checked": sorted(groups),
        "modal_row_count": int(mode_count),
        "modal_start": str(mode_start.date()),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate")
    ap.add_argument("--prior", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        result = validate(args.candidate, args.prior)
    except Exception as e:
        print(f"ERROR: could not validate: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for line in result["findings"]:
            print(line)
        print(f"VERDICT: {'PASS' if result['pass'] else 'FAIL -- DO NOT PUBLISH'}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
