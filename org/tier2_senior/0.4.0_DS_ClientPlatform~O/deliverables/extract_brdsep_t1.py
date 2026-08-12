"""OPAL_BRDSEP.T1 -- deterministic extraction of the Opal asset base by segment.

Window 2026-04-01 -> 2026-08-11. Reads ONLY local mirrors of landed S3 artifacts
(synced in the acquisition step); no live calls, so the run is reproducible.

Run twice and diff -- T1-A9 determinism control.
Emits a single JSON blob of every figure the deliverable quotes.
"""
from __future__ import annotations

import glob
import json

import pandas as pd

WIN_START = "2026-04-01"
WIN_END = "2026-08-11"
OPAL_ETFS = ["DIVZ", "IDVZ", "PFDE", "PFOE"]

ANDREW_18 = [
    "Anna *9237", "Anna *9238", "Blended Opal / Satellite 50",
    "Moderate Income Portfolio", "Opal - Beecherl Legg",
    "Opal - Cash + Satellite 50", "Opal - Income",
    "Opal 66% Long Term / 34% UST", "Opal Satellite 15", "Opal Satellite 30",
    "Opal Satellite 40", "Opal Satellite 50", "Opal Satellite 60",
    "Opal Satellite 70", "Opal Satellite 80", "Opal Satellite 98",
    "Opal Ultra Short Term", "Opal UST/ Sat 70",
]

out: dict = {"window": {"start": WIN_START, "end": WIN_END}, "denominators": {}}


def norm(s: str) -> str:
    return " ".join(str(s).split()).strip().lower()


# ---------------------------------------------------------------- ETF leg (3a)
files = sorted(glob.glob("netassets/*.parquet"))
na = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
na["date"] = pd.to_datetime(na["date"])
out["denominators"]["etf_netassets_partitions"] = len(files)
out["denominators"]["etf_netassets_rows"] = len(na)

etf = {"per_ticker_coverage": {}, "endpoints": {}}
for t in OPAL_ETFS:
    s = na[na.ticker == t].sort_values("date")
    obs = s[~s["inferred"].astype(bool)]
    etf["per_ticker_coverage"][t] = {
        "n_dates": len(s),
        "first": str(s["date"].min().date()),
        "last": str(s["date"].max().date()),
        "first_genuine_observation": str(obs["date"].min().date()) if len(obs) else None,
        "n_genuine_observations": len(obs),
        "n_interpolated": int(s["inferred"].astype(bool).sum()),
    }

for d in (WIN_START, WIN_END):
    w = na[na.date == d].sort_values("ticker")
    etf["endpoints"][d] = {
        "tickers_present": sorted(w.ticker.tolist()),
        "tickers_absent": sorted(set(OPAL_ETFS) - set(w.ticker)),
        "per_ticker": {
            r.ticker: {
                "net_assets": float(r.net_assets),
                "inferred": bool(r.inferred),
                "source": r.source,
                "shares_basis": r.shares_basis,
            }
            for _, r in w.iterrows()
        },
        "total_net_assets_present_tickers": float(w["net_assets"].sum()),
    }

# like-for-like: only tickers present at BOTH endpoints
both = sorted(set(etf["endpoints"][WIN_START]["per_ticker"]) &
              set(etf["endpoints"][WIN_END]["per_ticker"]))
lfl_s = sum(etf["endpoints"][WIN_START]["per_ticker"][t]["net_assets"] for t in both)
lfl_e = sum(etf["endpoints"][WIN_END]["per_ticker"][t]["net_assets"] for t in both)
etf["like_for_like"] = {
    "tickers": both, "start": lfl_s, "end": lfl_e,
    "delta": lfl_e - lfl_s,
    "pct": (lfl_e / lfl_s - 1) * 100 if lfl_s else None,
}
no_base = sorted(set(etf["endpoints"][WIN_END]["per_ticker"]) - set(both))
etf["no_april1_baseline"] = {
    "tickers": no_base,
    "value_at_end": sum(etf["endpoints"][WIN_END]["per_ticker"][t]["net_assets"] for t in no_base),
    "inception": "2025-12-30",
    "coverage_onset": "2026-05-18",
}
# nearest genuine observation on/before window start
anchor = {}
for t in both:
    s = na[(na.ticker == t) & (na.date <= WIN_START) & (~na["inferred"].astype(bool))].sort_values("date")
    if len(s):
        r = s.iloc[-1]
        anchor[t] = {"date": str(r["date"].date()), "net_assets": float(r.net_assets)}
etf["nearest_genuine_anchor_at_or_before_start"] = anchor
etf["nearest_genuine_anchor_total"] = sum(v["net_assets"] for v in anchor.values())
out["etf"] = etf

# ------------------------------------------------- firm model legs (3b/3c/3d)
firms = {}
for firm in ["49financial", "inflection", "cottonwood"]:
    d = json.load(open(f"mdpf/{firm}_ts.json"))
    dates = d["dates"]
    rec = {
        "as_of_first": d["as_of_first"], "as_of_last": d["as_of_last"],
        "n_dates": len(dates), "partner_name": d["partner_name"], "endpoints": {},
    }
    for target in (WIN_START, WIN_END, "2026-08-10"):
        if target in dates:
            i = dates.index(target)
            rec["endpoints"][target] = {
                "present": True,
                "model_aua": d["model_aua"][i],
                "non_model_aua": d["non_model_aua"][i],
                "opal_aggregate_aua": d["opal_aggregate_aua"][i],
                "partner_custody_total": d["partner_custody_total"][i],
                "account_count_total": d["account_count_total"][i],
                "count_basis": d["count_basis"][i],
                "point_class": d["point_class"][i],
            }
        else:
            rec["endpoints"][target] = {"present": False}
    firms[firm] = rec

# cottonwood coverage truth
cw = json.load(open("mdpf/cottonwood_ts.json"))
firms["cottonwood"]["first_tracked_date"] = cw["meta"]["first_tracked_date"]
firms["cottonwood"]["covered_dates_n"] = len(cw["meta"]["covered_dates"])
firms["cottonwood"]["measured_dates_n"] = sum(1 for p in cw["point_class"] if p != "absent")
firms["cottonwood"]["count_axis_note"] = cw["meta"]["count_axis_note"]
inf = json.load(open("mdpf/inflection_ts.json"))
firms["inflection"]["launch_seam"] = inf["meta"]["launch_seam"]
out["firms"] = firms

# ------------------------------------------- Cottonwood strategy reconciliation
r = json.load(open("bd/models/page_000.json"))
rows = r["pagedResults"]
by = {norm(x["name"]): x for x in rows}
matched, notfound, resolution = set(), [], []
for n in ANDREW_18:
    k = norm(n)
    if k in by:
        m = by[k]
        matched.add(m["id"])
        resolution.append({"listed": n, "roster_name": m["name"], "match": "exact",
                           "accounts": m["accountCount"]})
    else:
        cand = [x for x in rows if k in norm(x["name"]) or norm(x["name"]) in k]
        if len(cand) == 1:
            m = cand[0]
            matched.add(m["id"])
            resolution.append({"listed": n, "roster_name": m["name"], "match": "normalized",
                               "accounts": m["accountCount"]})
        else:
            notfound.append(n)
extra = [x for x in rows if "opal" in x["name"].lower() and x["id"] not in matched]
out["cottonwood_strategies"] = {
    "roster_total_declared": r["totalResultCount"],
    "roster_rows_read": len(rows),
    "page_count": r["pageCount"],
    "andrew_list_n": len(ANDREW_18),
    "resolution": resolution,
    "on_list_not_found": notfound,
    "found_not_on_list_opal_named": [
        {"name": x["name"], "accounts": x["accountCount"], "id": x["id"]}
        for x in sorted(extra, key=lambda z: z["name"])
    ],
    "roster_opal_named_total": sum(1 for x in rows if "opal" in x["name"].lower()),
    "accounts_on_matched": sum(x["accountCount"] for x in rows if x["id"] in matched),
    "composition_details_landed": len(glob.glob("bd/detail/*.json")),
}

# ------------------------------------------------------- ETF Float (step 2)
float_leg = {"per_firm_subtrahend": {}}
for firm, day in [("49financial", "2026-08-11"), ("inflection", "2026-08-11"),
                  ("cottonwood", "2026-08-10")]:
    rowsj = json.load(open(f"etfdaily/{firm}_{day}.json"))
    float_leg["per_firm_subtrahend"][firm] = {
        "as_of": day,
        "per_ticker": {x["etf_ticker"]: x["ownership_value"] for x in rowsj},
        "total": sum(x["ownership_value"] for x in rowsj),
        "source_artifact": rowsj[0]["source_artifact"],
    }
gross = out["etf"]["endpoints"][WIN_END]["total_net_assets_present_tickers"]
sub = sum(v["total"] for v in float_leg["per_firm_subtrahend"].values())
float_leg["gross_etf_net_assets"] = gross
float_leg["total_subtrahend"] = sub
float_leg["etf_float"] = gross - sub
out["etf_float"] = float_leg

# ------------------------------------------------ counts per segment (step 3)
counts = {}
rps = {}
for lbl, pat in [(WIN_START, "cnt/rps_0401/*.parquet"), (WIN_END, "cnt/rps_0811/*.parquet")]:
    df = pd.concat([pd.read_parquet(f) for f in glob.glob(pat)], ignore_index=True)
    rps[lbl] = {"rows": len(df), "accounts": int(df["account_id"].nunique()),
                "clients": None, "client_note": "fact_rps carries no client/household key"}
counts["49financial"] = {"source": "s3://opal-data-assets/schwab/08242234/silver/fact_rps",
                         "endpoints": rps,
                         "account_delta": rps[WIN_END]["accounts"] - rps[WIN_START]["accounts"]}

infc = {}
for lbl, pat in [(WIN_START, "cnt/inf_0401/*.parquet"), (WIN_END, "cnt/inf_0811/*.parquet")]:
    df = pd.concat([pd.read_parquet(f) for f in glob.glob(pat)], ignore_index=True)
    o = df[df["modelName"].astype(str).str.lower().str.contains("opal", na=False)]
    infc[lbl] = {
        "rows": len(df),
        "firm_accounts": int(df["accountId"].nunique()),
        "firm_clients": int(df["clientId"].nunique()),
        "opal_model_rows": len(o),
        "opal_model_accounts": int(o["accountId"].nunique()),
        "opal_model_clients": int(o["clientId"].nunique()),
        "opal_model_value": float(o["currentValue"].sum()),
        "opal_model_names": sorted(o["modelName"].dropna().unique().tolist()),
    }
counts["inflection"] = {
    "source": "s3://opal-data-assets/orion/inflection/silver/fact_positions",
    "endpoints": infc,
    "opal_account_delta": infc[WIN_END]["opal_model_accounts"] - infc[WIN_START]["opal_model_accounts"],
    "opal_client_delta": infc[WIN_END]["opal_model_clients"] - infc[WIN_START]["opal_model_clients"],
}
counts["cottonwood"] = {
    "source": "s3://opal-data-assets/blackdiamond/cottonwood/silver/fact_holdings",
    "endpoints": {WIN_START: {"present": False,
                              "reason": "silver partitions begin 2026-06-09; no 2026-04-01"},
                  WIN_END: {"present": False,
                            "reason": "silver last partition 2026-08-10; no 2026-08-11"}},
}
out["counts"] = counts

print(json.dumps(out, indent=2, default=str))
