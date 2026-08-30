"""ADVI_BDPARITY P1-PROBE BP1-2 -- the probe table, our linked returns vs BD's, per cell.

Reads ONLY bytes already pulled (bronze pull_date=2026-08-30) and our gold twr_daily. NO vendor
call. Ruled inputs: anchor = BD funding-inception, basis = CUMULATIVE, coverage opens at FIRST
LINKABLE, SI window opens at bd_first_return_day (3.0.0_SA_CVO @f11fb765ad + ANNOTATION 1/2).
"""
import json
import sys
import pandas as pd
import pyarrow.parquet as pq
import s3fs

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
import parity_period_returns as ppr  # noqa: E402

BUCKET_G = "opal-data-49financial"
PREFIX_G = "gold/advi/canonical/twr_daily/"
ASOF, QSTART = "2026-08-28", "2026-07-01"
GOLD_FLOOR = "2024-07-08"
COHORT = {  # schwab -> (bd_id, cohort attribute per 4.0.0_SA_CRO @7cd0cc1200)
    "0022312917": (13477111, "C5 income-bearing FI specimen"),
    "0038836097": (18927251, "C3 multi-security + FI, FLOWS member"),
    "0010083855": (21089351, "C2 fee off-quarter, no flows"),
    "0027265115": (22596361, "inception-recent, KNOWN anchor pre-pull"),
    "0076459710": (23221671, "inception-recent, most recent; in-kind class"),
}
BD_BY_ID = {v[0]: k for k, v in COHORT.items()}
HOLE = ("2026-08-11", "2026-08-17")  # 5 trading days absent, named per 3.0.0_SA_CVO 84554


def bd_side(local_paths):
    """BD's per-range figures, read from the response's OWN fields -- never inferred from fit."""
    out = {}
    for bd_id, path in local_paths.items():
        d = json.load(open(path, encoding="utf-8"))
        lvl = d["combinedLevels"][0]
        rows = []
        for i, e in enumerate(lvl["dateRangePoints"]):
            dr = e["dateRange"]
            twr = e.get("timeWeightedReturns") or {}
            rows.append({
                "index": i,
                "ret_start": str(dr.get("startDate"))[:10],
                "ret_end": str(dr.get("endDate"))[:10],
                "ret_name": dr.get("name"), "ret_type": dr.get("type"),
                "bd_return": twr.get("return"),
                "bd_annualized": twr.get("returnAnnualized"),
                "bd_days_held": twr.get("daysHeld"),
                "bd_period_length": twr.get("periodLength"),
                "bd_bmv": e.get("beginningMarketValue"),
                "bd_emv": e.get("endingMarketValue"),
            })
        out[bd_id] = {"inception": str(lvl.get("startDate"))[:10],
                      "data_date": str(d.get("dataDate"))[:10], "ranges": rows}
    return out


def load_gold(accounts, start, end):
    """Schema-tolerant load. THREE partitions carry 10 of 14 columns (bmv/emv/cf_* ABSENT) and
    null-typed returns, so a bare pyarrow union RAISES (BP1-4 @fa82a129d8 + correction @6ae366e8c0).
    Reading a fixed column subset per fragment and concatenating in pandas is the remedy the
    correction named -- a cast alone would not conjure an absent column."""
    # skip_instance_cache + no listings cache: this prefix was being RE-EMITTED underneath the
    # read (529 of 535 partitions rewritten inside one hour, 2026-08-30), and a cached handle
    # raises FileExpired when the ETag moves. A stale-cache read is the worse failure -- it would
    # have silently mixed pre- and post-re-emission bytes into one comparison instead of raising.
    fs = s3fs.S3FileSystem(skip_instance_cache=True, use_listings_cache=False)
    files = sorted(f for f in fs.find(f"{BUCKET_G}/{PREFIX_G}") if f.endswith("data.parquet"))
    want = [f for f in files if start <= f.split("date=")[1][:10] <= end]
    frames = []
    for f in want:
        t = pq.read_table(f, filesystem=fs, columns=["account_id", "business_date", "r_net",
                                                     "r_gross", "status"]).to_pandas()
        t = t[t["account_id"].isin(accounts)]
        if len(t):
            frames.append(t)
    df = pd.concat(frames, ignore_index=True)
    # VINTAGE: a parity number is meaningless without the baseline it was computed against.
    vint = max(fs.info(f)["LastModified"] for f in want)
    print("GOLD VINTAGE: newest partition write in the loaded range = %s" % vint)
    for c in ("r_net", "r_gross"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df, len(want)


PERIOD_INDEX = {"QTD": 0, "YTD": 1, "1Y": 2, "SI": 5}


def builder_minus_one_year(iso_date):
    """What the PULLER actually SENT for 1Y -- mirrors lambda_function._minus_one_year.

    ⛔ NOT the same as what our LINKER computes. The builder requests q_end minus one year
    (2025-08-28); parity_period_returns.period_window opens 1Y the DAY AFTER that (2025-08-29),
    so exactly one year of daily returns is linked. The two differ by ONE DAY BY CONSTRUCTION,
    and the 1Y cell therefore compares two windows that are not identical. The table PRINTS both
    rather than reconciling them: a one-day boundary difference at the open is precisely the
    convention-mismatch shape the taxonomy reserves, and hiding it inside a matched-looking cell
    is how it would be read as a data delta instead of a definition delta."""
    y, m, d = (int(x) for x in iso_date.split("-"))
    if m == 2 and d == 29:
        return "%04d-02-28" % (y - 1)
    return "%04d-%02d-%02d" % (y - 1, m, d)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--bronze-dir", required=True,
                    help="dir holding the 5 reporting_performance_*.json already pulled")
    a = ap.parse_args()
    paths = {bd: "%s/perf_%s.json" % (a.bronze_dir, bd) for bd in BD_BY_ID}
    bd = bd_side(paths)

    anchors = {BD_BY_ID[b]: v["inception"] for b, v in bd.items()}
    # BMV at the TRUE inception is MEASURED only for 22596361 (BD computed that window).
    # For the rest BD computed 07-01..08-28, so its BMV is NOT the inception BMV -- passing it
    # would be reading a number from the wrong window. Absent -> the anchor branch, which the
    # cell prints. NEVER assumed to be 0 just because an inception "ought" to open empty.
    # BMV AT A TRUE INCEPTION IS 0.0 BY CONSTRUCTION, not by assumption: the anchor here is
    # level.startDate, the date the account began, and an account begins empty. MEASURED on
    # 22596361 (BD returned BMV 0.0 at exactly that range) and corroborated independently on
    # 23221671 and 21089351, whose first LINKABLE day is one trading day after their inception --
    # the same pattern, from a different instrument (our gold, not BD's payload). n=3.
    # 3.0.0_SA_CVO ANNOTATION 3 applies the rule at n=2; this is the third.
    # NOTE the distinction that matters: this is BMV at the TRUE anchor, NOT the beginningMarketValue
    # BD returned for the four fallback-window ranges -- that number belongs to 07-01..08-28 and
    # reading it here would be the right field off the wrong range.
    bd_bmvs = {sch: 0.0 for sch in COHORT}

    lo = max(min(anchors.values()), "2025-01-01")
    daily, npart = load_gold(set(BD_BY_ID.values()), lo, ASOF)
    spine = ppr.spine_of(daily)
    print("GOLD LOADED: %d partitions in [%s..%s], %d rows, spine %d dates"
          % (npart, lo, ASOF, len(daily), len(spine)))
    print("GOLD FLOOR: %s   BD dataDate: %s" % (GOLD_FLOOR, bd[22596361]["data_date"]))
    print()

    rows = []
    for schwab, (bd_id, attr) in COHORT.items():
        binfo = bd[bd_id]
        for period, idx in PERIOD_INDEX.items():
            r = ppr.link_account_period(daily, schwab, period, ASOF, spine,
                                        anchor=anchors[schwab] if period == "SI" else None,
                                        anchor_basis="bd-returned-si-start" if period == "SI" else "",
                                        earliest_partition=GOLD_FLOOR,
                                        bd_bmv_at_anchor=bd_bmvs.get(schwab))
            br = binfo["ranges"][idx]
            # WHAT WE ASKED FOR at that index (the builder's own construction)
            req = {0: (QSTART, ASOF), 1: ("2026-01-01", ASOF),
                   2: (builder_minus_one_year(ASOF), ASOF),
                   5: (anchors[schwab] if schwab == "0027265115" else QSTART, ASOF)}[idx]
            range_match = (br["ret_start"] == req[0] and br["ret_end"] == req[1])
            # COMPARISON OUTCOME, ruled by 3.0.0_SA_CVO ANNOTATION 3 @11c48031d7, in TEST ORDER
            # (coverage first -- it is a permanent property of the account, the window is not):
            #   our side cannot produce it            -> our own UNAVAILABLE-* stands
            #   SI requested away from the TRUE anchor -> UNAVAILABLE-SI-WINDOW-NOT-AT-ANCHOR
            # BD echoes the SI startDate we send (5 of 5), so an SI value is comparable ONLY when
            # the requested SI start == level.startDate. Otherwise BD computed a real number over
            # the WRONG window -- present, plausible and wrong, which is the class the taxonomy
            # exists to refuse. NOT "no anchor": the anchors are in hand from level.startDate.
            cmp_outcome = r["outcome"]
            if period == "SI" and cmp_outcome == ppr.OUTCOME_COMPUTED:
                if req[0] != binfo["inception"]:
                    cmp_outcome = "UNAVAILABLE-SI-WINDOW-NOT-AT-ANCHOR"
            ours = r["r_net_cum"]
            theirs = br["bd_return"]
            delta = (None if (ours is None or theirs is None) else ours - theirs)
            rows.append({
                "account": schwab, "bd_id": bd_id, "period": period, "index": idx,
                "requested": "%s..%s" % req,
                "returned": "%s..%s" % (br["ret_start"], br["ret_end"]),
                "range_match": range_match,
                "our_outcome": r["outcome"], "cell_outcome": cmp_outcome, "our_window": "%s..%s" % (r["window_start"], r["window_end"])
                                if r["window_start"] else None,
                "our_return": ours, "bd_return": theirs, "delta": delta,
                "bd_annualized": br["bd_annualized"],
                "our_days_linked": r["days_linked"], "our_days_expected": r["days_expected"],
                "bd_days_held": br["bd_days_held"],
                "coverage_basis": r["coverage_basis"], "our_first_linkable": r["our_first_linkable"],
                "bd_anchor": r["bd_anchor"], "bd_first_return_day": r["bd_first_return_day"],
                "branch": r["bd_first_return_day_branch"], "attr": attr,
            })
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    print("=== THE PROBE TABLE (5 accounts x 4 ruled periods = 20 cells) ===")
    print(df[["account", "period", "requested", "returned", "range_match", "cell_outcome",
              "our_return", "bd_return", "delta", "our_days_linked", "bd_days_held"]].to_string(index=False))
    print()
    print("=== SI LINE, per account ===")
    si = df[df["period"] == "SI"]
    print(si[["account", "bd_anchor", "bd_first_return_day", "branch", "our_first_linkable",
              "coverage_basis", "cell_outcome"]].to_string(index=False))
    print()
    print("=== DENOMINATORS ===")
    print("cells: %d   range_match TRUE: %d   comparable (both values present): %d"
          % (len(df), int(df["range_match"].sum()), int(df["delta"].notna().sum())))
    print("cell outcomes:", json.dumps(df["cell_outcome"].value_counts().to_dict()))
    si = df[df["period"] == "SI"]
    print("SI denominator: %s of %d" % (json.dumps(si["cell_outcome"].value_counts().to_dict()), len(si)))
    print("bd_annualized values seen:", sorted({str(v) for v in df["bd_annualized"]}))
    return df


if __name__ == "__main__":
    main()
