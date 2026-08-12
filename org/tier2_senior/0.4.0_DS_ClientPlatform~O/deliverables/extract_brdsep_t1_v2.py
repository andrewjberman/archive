"""OPAL_BRDSEP.T1 v2 -- Opal asset base by segment, ANDREW-RULED framing (2026-08-12 ~1855Z).

Three rulings applied vs v1:
  1. 49 Financial = THE ENTIRE Schwab 08242234 account, not the Opal model slice.
     Grounded on the account's own silver (dim_balance.net_mv_plus_cash), not the
     platinum aggregate alone -- his words were "the full total from that account".
  2. Cottonwood start = 0 (sovereign framing ruling; the DATA still has no 2026-04-01
     measurement -- coverage remains 21 of 132 days and the caveat travels with the number).
  3. ETF leg window = first-available -> now, not 2026-04-01.

Reads ONLY local mirrors of landed S3 artifacts; run twice and diff (T1-A9).
"""
from __future__ import annotations

import glob
import json

import pandas as pd

W_START, W_END = "2026-04-01", "2026-08-11"
OPAL_ETFS = ["DIVZ", "IDVZ", "PFDE", "PFOE"]

out: dict = {
    "framing": "ANDREW-DIRECT 2026-08-12 ~1855Z: 49F=entire account; Cottonwood start=0; ETF=first-available->now",
    "window_requested": {"start": W_START, "end": W_END},
    "denominators": {},
}


# ------------------------------------------------ 49F: THE ENTIRE ACCOUNT (ruling 1)
bal = {}
for lbl, pat in [(W_START, "cnt/bal0401/*.parquet"), (W_END, "cnt/bal0811/*.parquet")]:
    df = pd.concat([pd.read_parquet(f) for f in glob.glob(pat)], ignore_index=True)
    bal[lbl] = {
        "rows": len(df),
        "net_mv_plus_cash": float(pd.to_numeric(df["net_mv_plus_cash"], errors="coerce").sum()),
    }
plat49 = json.load(open("mdpf/49financial_ts.json"))
i0, i1 = plat49["dates"].index(W_START), plat49["dates"].index(W_END)
out["49financial"] = {
    "account": "08242234",
    "measure": "ENTIRE ACCOUNT (net market value + cash), per Andrew 2026-08-12",
    "start": {"as_of": W_START, "value": bal[W_START]["net_mv_plus_cash"]},
    "end": {"as_of": W_END, "value": bal[W_END]["net_mv_plus_cash"]},
    "delta": bal[W_END]["net_mv_plus_cash"] - bal[W_START]["net_mv_plus_cash"],
    "pct": (bal[W_END]["net_mv_plus_cash"] / bal[W_START]["net_mv_plus_cash"] - 1) * 100,
    "tie_out": {
        "platinum_partner_custody_total_start": plat49["partner_custody_total"][i0],
        "platinum_partner_custody_total_end": plat49["partner_custody_total"][i1],
        "diff_start": bal[W_START]["net_mv_plus_cash"] - plat49["partner_custody_total"][i0],
        "diff_end": bal[W_END]["net_mv_plus_cash"] - plat49["partner_custody_total"][i1],
    },
    "model_slice_for_contrast": {
        "start": plat49["model_aua"][i0], "end": plat49["model_aua"][i1],
        "note": "the v1 headline -- NOT the segment number under the ruling",
    },
    "denominator": f"dim_balance rows {bal[W_START]['rows']} (start) / {bal[W_END]['rows']} (end)",
}

# ------------------------------------------------------------- Inflection (unchanged)
inf = json.load(open("mdpf/inflection_ts.json"))
j0 = inf["dates"].index(W_START)
j1 = inf["dates"].index("2026-08-10")
out["inflection"] = {
    "measure": "Opal MODEL AUA (Eclipse-crosswalked basis), per his original methodology",
    "start": {"as_of": W_START, "value": inf["model_aua"][j0], "accounts": inf["account_count_total"][j0]},
    "end": {"as_of": "2026-08-10", "value": inf["model_aua"][j1], "accounts": inf["account_count_total"][j1]},
    "delta": inf["model_aua"][j1] - inf["model_aua"][j0],
    "firm_wide_for_contrast": inf["partner_custody_total"][j1],
    "endpoint_note": "series as_of_last is 2026-08-10; 2026-08-11 absent, not substituted",
}

# -------------------------------------------------- Cottonwood: start = 0 (ruling 2)
cot = json.load(open("mdpf/cottonwood_ts.json"))
k1 = cot["dates"].index("2026-08-10")
out["cottonwood"] = {
    "measure": "Opal MODEL AUA",
    "start": {"as_of": W_START, "value": 0.0,
              "basis": "ANDREW-RULED ZERO -- not a measurement. point_class at 2026-04-01 is 'absent'."},
    "end": {"as_of": "2026-08-10", "value": cot["model_aua"][k1], "accounts": cot["account_count_total"][k1]},
    "delta": cot["model_aua"][k1] - 0.0,
    "coverage_caveat": {
        "first_tracked_date": cot["meta"]["first_tracked_date"],
        "measured_dates": sum(1 for p in cot["point_class"] if p != "absent"),
        "axis_dates": len(cot["dates"]),
    },
}

# ---------------------------------------------- ETF gross: first-available (ruling 3)
na = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob("netassets/*.parquet"))], ignore_index=True)
na["date"] = pd.to_datetime(na["date"])
piv = na.pivot_table(index="date", columns="ticker", values="net_assets", aggfunc="sum")
full = piv.dropna(how="any")
first_all4 = str(full.index.min().date())
etf = {"first_date_all_four": first_all4, "his_named_date": "2026-05-15", "cohorts": {}}
s4 = float(na[na.date == first_all4]["net_assets"].sum())
e4 = float(na[na.date == W_END]["net_assets"].sum())
etf["cohorts"]["all_four"] = {
    "start": {"as_of": first_all4, "value": s4}, "end": {"as_of": W_END, "value": e4},
    "delta": e4 - s4, "pct": (e4 / s4 - 1) * 100,
}
s2 = float(na[(na.date == "2026-05-15")]["net_assets"].sum())
e2 = float(na[(na.date == W_END) & (na.ticker.isin(["DIVZ", "IDVZ"]))]["net_assets"].sum())
etf["cohorts"]["divz_idvz_from_his_date"] = {
    "start": {"as_of": "2026-05-15", "value": s2}, "end": {"as_of": W_END, "value": e2},
    "delta": e2 - s2, "pct": (e2 / s2 - 1) * 100,
}
etf["per_ticker_delta"] = {}
for t in OPAL_ETFS:
    a = na[(na.date == first_all4) & (na.ticker == t)]["net_assets"]
    b = na[(na.date == W_END) & (na.ticker == t)]["net_assets"]
    if len(a) and len(b):
        etf["per_ticker_delta"][t] = {"start": float(a.iloc[0]), "end": float(b.iloc[0]),
                                      "delta": float(b.iloc[0] - a.iloc[0])}
etf["denominator"] = f"{len(piv)} dates in series; {len(full)} carry all four tickers"
out["etf_gross"] = etf


# ----------------------------------------- ETF Float: first COMPLETE subtrahend
def firm_total(firm: str, day: str) -> float | None:
    path = f"cotdaily/{day}.json" if firm == "cottonwood" else f"etfdaily/{firm}_{day}.json"
    try:
        return float(sum(x["ownership_value"] for x in json.load(open(path))))
    except FileNotFoundError:
        return None


FLOAT_START = "2026-07-20"
flo = {"start_date_basis": (
    "Cottonwood's ETF-ownership feed exists from 2026-06-08 but is RAMPING -- 5 accounts / $194,520 "
    "at onset vs 309 accounts / $52,007,439 at the end, with a 5->293 account jump in the week of "
    "2026-07-08..07-15. An incomplete subtrahend INFLATES the float. Start is taken at the producer's "
    "own declared first_tracked_date 2026-07-20, not at feed onset.")}
for day, key in [(FLOAT_START, "start"), (W_END, "end")]:
    gross = float(na[na.date == day]["net_assets"].sum())
    subs = {}
    for f in ["49financial", "inflection", "cottonwood"]:
        v = firm_total(f, day)
        if v is None and f == "cottonwood" and day == W_END:
            v = firm_total(f, "2026-08-10")
            subs[f] = {"value": v, "as_of": "2026-08-10", "note": "no 2026-08-11 partition"}
        else:
            subs[f] = {"value": v, "as_of": day}
    tot = sum(s["value"] for s in subs.values())
    flo[key] = {"as_of": day, "gross": gross, "subtrahend_per_firm": subs,
                "subtrahend_total": tot, "float": gross - tot}
flo["delta"] = flo["end"]["float"] - flo["start"]["float"]
flo["pct"] = (flo["end"]["float"] / flo["start"]["float"] - 1) * 100
naive_g = float(na[na.date == "2026-06-08"]["net_assets"].sum())
flo["naive_feed_onset_control"] = {
    "date": "2026-06-08", "gross": naive_g,
    "note": ("CONTROL, not a result: 2026-06-08 carries NO netassets partition (gross reads 0.00) AND "
             "the cottonwood subtrahend is ramping. Computing the float there yields a large positive "
             "delta that is entirely a coverage artifact."),
}
out["etf_float"] = flo

# ------------------------------------------------------------------ combination
end_total = (out["49financial"]["end"]["value"] + out["inflection"]["end"]["value"]
             + out["cottonwood"]["end"]["value"] + out["etf_float"]["end"]["float"])
growth = (out["49financial"]["delta"] + out["inflection"]["delta"]
          + out["cottonwood"]["delta"] + out["etf_float"]["delta"])
out["combination"] = {
    "end_total": end_total, "growth_sum": growth,
    "note": "segments + arithmetic only; no single headline rate (TO section 6)",
}

print(json.dumps(out, indent=2, default=str))
