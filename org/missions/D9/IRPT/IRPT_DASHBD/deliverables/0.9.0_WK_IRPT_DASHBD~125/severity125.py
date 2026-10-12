"""Read-only analysis over local copies. Prints counts and bands only; writes private detail to the private folder."""
import json
import re
import sys

import pandas as pd

P = sys.argv[1]
REPO = sys.argv[2]
MAXP = 100_000
def extract_t1_prices(txns):
    valid = txns[txns['asset_name'].notna() & txns['units'].notna() & (txns['units'].abs() > 1e-8) &
                 txns['market_value'].notna() & (txns['market_value'] != 0)].copy()
    valid['calc_price'] = valid['market_value'].abs() / valid['units'].abs()
    valid = valid[(valid['calc_price'] > 0) & (valid['calc_price'] < MAXP)]
    return valid.groupby('asset_name')['calc_price'].median().to_dict()
df = pd.read_parquet(P + "/txn_1009.parquet", columns=["transaction_id", "asset_name", "units", "market_value"])
orig = extract_t1_prices(df)
ded = extract_t1_prices(df.drop_duplicates(subset=["transaction_id"], keep="last"))
both = sorted(set(orig) & set(ded))
moved = {}
for a in both:
    o, d = round(float(orig[a]), 8), round(float(ded[a]), 8)
    if o != d:
        moved[a] = abs(d - o) / abs(o) if o else float("inf")
res = {"rows": len(df), "medians_original": len(orig), "compared": len(both), "moved": len(moved)}
over1 = {a for a, r in moved.items() if r > 0.01}
res["moved_over_1pct"] = len(over1)
res["bands"] = {"under_0.1": sum(1 for r in moved.values() if r < 0.001),
                "0.1_to_1": sum(1 for r in moved.values() if 0.001 <= r <= 0.01), "over_1": len(over1)}
# code override map keys (cross-check only), parsed from source text of the script path
src = open(REPO + "/data/black_diamond/scripts/silver/bd_price_update.py", encoding="utf-8").read()
code_ovr = set(re.findall(r"""['"]asset_name['"]\s*:\s*['"]([^'"]+)['"]""", src))
res["script_override_names_found_in_code"] = len(code_ovr)

def classify(servedfile, label):
    s = pd.read_parquet(servedfile)
    if "date" in s.columns:
        s = s[s["date"].astype(str).str[:10] == "2026-10-09"]
    res_l = {"rows_for_day": int(len(s)), "distinct_assets": int(s["asset_name"].nunique()),
             "dup_asset_rows": int(s["asset_name"].duplicated().sum()),
             "sources": {k: int(v) for k, v in s["source"].value_counts().items()}}
    sv = s.drop_duplicates("asset_name", keep="last").set_index("asset_name")
    cls = {}
    cnt = {"final_served": 0, "outranked_by_yahoo": 0, "outranked_by_override": 0, "not_placed": 0}
    not_placed_reason = {}
    equal_dedup = 0
    for a in moved:
        if a not in sv.index:
            c, why = "not_placed", "asset_absent_from_served_object"
        else:
            src_, pr = sv.at[a, "source"], float(sv.at[a, "price"])
            if src_ == "transaction_observed":
                if abs(pr - orig[a]) <= 1e-9 * max(1.0, abs(orig[a])):
                    c, why = "final_served", ""
                else:
                    c, why = "not_placed", "source_T1_but_price_differs_from_median"
                if abs(pr - ded[a]) <= 1e-9 * max(1.0, abs(ded[a])) and c == "final_served":
                    equal_dedup += 1
            elif src_ == "yahoo_finance":
                c, why = "outranked_by_yahoo", ""
            elif src_ == "scoped_override":
                c, why = "outranked_by_override", ""
            else:
                c, why = "not_placed", "source_" + str(src_)
        cls[a] = c
        cnt[c] += 1
        if why:
            not_placed_reason[why] = not_placed_reason.get(why, 0) + 1
    res_l["moved_classes"] = cnt
    res_l["not_placed_reasons"] = not_placed_reason
    res_l["final_served_also_equal_dedup_median"] = equal_dedup
    res_l["over1_classes"] = {k: sum(1 for a in over1 if cls[a] == k) for k in cnt}
    # all-160 context
    t1 = sv[sv["source"] == "transaction_observed"]
    res_l["all_served_T1_rows"] = int(len(t1))
    res_l["all_160_in_served"] = int(sum(1 for a in orig if a in sv.index))
    res_l["all_160_source_counts"] = {k: int(v) for k, v in sv.loc[[a for a in orig if a in sv.index], "source"].value_counts().items()}
    return cls, res_l
out = {"basis_counts": res}
# holdings keys
h = pd.read_parquet(P + "/hold_assets.parquet")["asset_name"].dropna().astype(str).str.strip().unique()
hs = set(h)
out["holdings_distinct_asset_keys"] = len(hs)
ALIAS = {'OPAL DIVIDEND INCOME ETF': 'POLEN DIVIDEND INCOME ETF', 'EVENTIDE HIGH DIVIDEND ETF': 'POLEN DIVIDEND INCOME ETF',
         'OPAL INTERNATIONAL DIVIDEND INCOME ETF': 'OPAL INTERNATIONAL DIVIDEND INCOME ETF'}
out["of_160_priced_assets_joined_exact"] = int(sum(1 for a in orig if a in hs))
out["of_34_moved_joined_exact"] = int(sum(1 for a in moved if a in hs))
out["of_34_moved_joined_alias"] = int(sum(1 for a in moved if ALIAS.get(a, a) in hs))
out["moved_names_that_are_alias_sources"] = int(sum(1 for a in moved if a in ALIAS))
out["code_override_names_in_34"] = int(sum(1 for a in moved if a in code_ovr))
for label, f in (("daily_1009", P + "/daily_1009.parquet"), ("canon_eod_2303", P + "/canon_eod_2303.parquet"),
                 ("canon_eod_2302", P + "/canon_eod_2302.parquet"), ("canon_first_0014", P + "/canon_first_0014.parquet")):
    cls, rl = classify(f, label)
    fin = {a for a, c in cls.items() if c == "final_served"}
    rl["final_served_held_exact"] = int(sum(1 for a in fin if a in hs))
    rl["final_served_held_alias"] = int(sum(1 for a in fin if ALIAS.get(a, a) in hs))
    rl["over1_final_held_exact"] = int(sum(1 for a in fin & over1 if a in hs))
    rl["over1_final"] = int(len(fin & over1))
    out[label] = rl
print(json.dumps(out, indent=1))
json.dump(out, open(P + "/severity125_result.json", "w"), indent=1)
