"""SmartX model-backfill VARIANCE OVERLAY (Andrew-direct via COO 154049Z).

NEW series   = the silver-sourced backfill: fact_model_aum_daily LATEST partition,
               intra-partition day-series (F1 law, load_aum_daily @9bd23d904),
               rmid -> canonical key via the F5 crosswalk bridge.
LEGACY series = what is ACTUALLY DISPLAYING: s3://opal-data-portal-v2/
               platinum/mdpf/aggregate_aua_timeseries.json partners.49financial
               (model_aua[] + by_model), the v0.9 rederived family per its own
               meta.backfill_methods -- verified against the SERVED artifact,
               never a producer self-report.

Diagnostic overlay ONLY -- informs the backfill go/no-go; not a fix, not a serve
step. Prints every denominator (common dates/models, and what each side covers
that the other does not). Aggregate line compared = the 5-core model sum (the
served model_aua[] IS the 5-core line: last == the served_baseline_5core pin).
"""
from __future__ import annotations

import json
import os
import sys

import boto3

_HERE = os.path.dirname(os.path.abspath(__file__))
_GOLD = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..",
                                     "data", "mdpf", "scripts", "gold"))
sys.path.insert(0, _GOLD)

import dim_mdpf_aggregate_aua_timeseries as spine  # noqa: E402

SERVED_BUCKET = "opal-data-portal-v2"
SERVED_KEY = "platinum/mdpf/aggregate_aua_timeseries.json"


def load_served_49f():
    body = boto3.client("s3").get_object(Bucket=SERVED_BUCKET, Key=SERVED_KEY)["Body"].read()
    j = json.loads(body)
    p49 = j["partners"]["49financial"] if isinstance(j["partners"], dict) else \
        next(p for p in j["partners"] if p.get("firm_id") == "49financial")
    print(f"SERVED (displaying): {SERVED_KEY} n_dates={j['n_dates']} "
          f"[{j['as_of_first']}..{j['as_of_last']}] "
          f"backfill_methods={j['meta']['backfill_methods']}")
    return j["dates"], p49


def build_new_series():
    roster = spine.load_roster_49f_open()
    aum = spine.load_aum_daily()
    bridge = spine.build_rmid_bridge(roster)
    days = sorted({d for d in aum["_day"] if d and d >= spine.SERVED_AS_OF_FIRST})
    hist = spine.historical_model_value(aum, bridge, days)
    agg = []
    for i in range(len(days)):
        vals = [hist[k][i] for k in spine.CORE_MODEL_KEYS if hist.get(k)]
        agg.append(round(sum(v for v in vals if v is not None), 2))
    return days, agg, hist


def main() -> int:
    s_dates, p49 = load_served_49f()
    s_agg = dict(zip(s_dates, p49["model_aua"]))
    n_days, n_agg_list, n_hist = build_new_series()
    n_agg = dict(zip(n_days, n_agg_list))

    common = [d for d in n_days if d in s_agg and s_agg[d] is not None]
    only_served = sorted(set(s_dates) - set(n_days))
    only_new = sorted(set(n_days) - set(s_dates))
    print(f"\nDENOMINATOR: served={len(s_dates)} new={len(n_days)} common={len(common)}")
    print(f"  served-only dates ({len(only_served)}): {only_served[:8]}"
          f"{'...' if len(only_served) > 8 else ''}  <- rederived business-day fills "
          f"+ any frontier the new side lacks")
    print(f"  new-only dates ({len(only_new)}): {only_new[:8]}"
          f"{'...' if len(only_new) > 8 else ''}  <- real trading days the legacy axis omits "
          f"+ the new frontier")

    rows = []
    for d in common:
        sv, nv = s_agg[d], n_agg[d]
        delta = round(nv - sv, 2)
        pct = (delta / sv * 100.0) if sv else None
        rows.append((d, sv, nv, delta, pct))

    absmax = max(rows, key=lambda r: abs(r[3]))
    pctmax = max((r for r in rows if r[4] is not None), key=lambda r: abs(r[4]))
    n_beyond_1pct = sum(1 for r in rows if r[4] is not None and abs(r[4]) > 1.0)
    n_beyond_5pct = sum(1 for r in rows if r[4] is not None and abs(r[4]) > 5.0)
    print(f"\nAGGREGATE 5-CORE MODEL LINE (new - served), {len(rows)} common dates:")
    print(f"  max |$| delta: {absmax[0]}  served={absmax[1]:,.2f} new={absmax[2]:,.2f} "
          f"delta={absmax[3]:+,.2f} ({absmax[4]:+.2f}%)")
    print(f"  max |%| delta: {pctmax[0]}  served={pctmax[1]:,.2f} new={pctmax[2]:,.2f} "
          f"delta={pctmax[3]:+,.2f} ({pctmax[4]:+.2f}%)")
    print(f"  dates beyond |1%|: {n_beyond_1pct}   beyond |5%|: {n_beyond_5pct}")

    print("\n  top 12 divergences by |$|:")
    for d, sv, nv, delta, pct in sorted(rows, key=lambda r: -abs(r[3]))[:12]:
        print(f"    {d}: served={sv:>18,.2f}  new={nv:>18,.2f}  "
              f"delta={delta:>+15,.2f} ({pct:+.2f}%)")

    # quarter-ish sampling for the shape
    print("\n  overlay sample (first, quarterlies, last):")
    marks = [common[0]] + [d for d in common if d.endswith(("-03-31", "-06-30", "-09-30", "-12-31"))] + [common[-1]]
    seen = set()
    for d in marks:
        if d in seen:
            continue
        seen.add(d)
        sv, nv = s_agg[d], n_agg[d]
        print(f"    {d}: served={sv:>18,.2f}  new={nv:>18,.2f}  delta={nv - sv:>+15,.2f}")

    # per-model overlay
    s_bm = p49["by_model"]
    print("\nPER-MODEL (common dates where BOTH sides carry the model):")
    for mkey in spine.SERVED_MODEL_KEYS:
        s_series = dict(zip(s_dates, s_bm.get(mkey, {}).get("model_value", [])))
        n_series = dict(zip(n_days, n_hist.get(mkey, [])))
        both = [d for d in common
                if s_series.get(d) is not None and n_series.get(d) is not None]
        if not both:
            print(f"  {mkey:28s} no common coverage")
            continue
        deltas = [(d, n_series[d] - s_series[d],
                   ((n_series[d] - s_series[d]) / s_series[d] * 100.0) if s_series[d] else None)
                  for d in both]
        worst = max(deltas, key=lambda r: abs(r[1]))
        frontier = deltas[-1]
        print(f"  {mkey:28s} n={len(both):3d}  worst {worst[0]} {worst[1]:>+15,.2f}"
              f" ({(worst[2] or 0):+.2f}%)   frontier {frontier[0]} {frontier[1]:>+15,.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
