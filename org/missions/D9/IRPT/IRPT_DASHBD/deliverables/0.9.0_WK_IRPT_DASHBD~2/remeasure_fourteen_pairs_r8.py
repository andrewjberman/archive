"""IRPT_DASHBD TO-DB-b-15 -- re-measure ALL 14 like-day pairs under the EQUITY basis (CTO RULINGS batch 193), LOCALLY, with the producer in
this worktree. READS ONLY (S3 get/list of the Schwab silver and the holdings gold the producer reads); nothing is written to S3 and NO
vendor call is made. Black Diamond's side is the stored round-4 responses: TIEOUT_49F_BLACKDIAMOND_R4.json (its time-weighted return) and
RAW_BD_PERIOD_<account>.sanitised.json.gz (its window values and accruals), both in the ~1 folder.

Usage: python remeasure_fourteen_pairs_r8.py <repo_root> <out_json>
Writes {"method_version", "pairs": [{account,start,end,bd_twr,opal_twr_now,abs_diff_now,...,counterfactual}], "sign_check", "null_counts"}.
"""
import gzip
import importlib.util
import json
import sys
from pathlib import Path

import boto3
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(root))
D1 = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1"
spec = importlib.util.spec_from_file_location("rg_handler", root / "infra/aws/lambda/investor-reporting/reporting-gold/handler.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
ard = h.ard

s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc = ard.load_declaration()
src = ard.source_entry(doc, ard.declared_sources(doc)[0])
firm = ard.firm_scope(src)
thresholds = h.load_thresholds()
table, keycols = ard.load_classification(src)
trn_days = ard.partition_days(s3, src["bucket"], src["transactions_prefix"])
bal_days = ard.partition_days(s3, src["bucket"], src["balance_prefix"])
def _REAL(token):
    """Resolve an acct# token to the real account id at run time from the private evidence dir (outside the repo)."""
    import json as _json
    import os as _os
    d = _os.environ.get("IRPT_PRIVATE_EVIDENCE_DIR")
    if not d:
        raise SystemExit("REFUSE: IRPT_PRIVATE_EVIDENCE_DIR is not set; this historical script needs the private account map")
    p = _os.path.join(d, "account_map_49financial.json")
    if not _os.path.isfile(p):
        raise SystemExit("REFUSE: account_map_49financial.json is absent from IRPT_PRIVATE_EVIDENCE_DIR")
    with open(p, encoding="utf-8") as fh:
        m = _json.load(fh)
    if token not in m:
        raise SystemExit("REFUSE: token %s is not in the account map" % token)
    return m[token]


INT_ADJ = {(_REAL("acct#89d0916a"), "2026-06-25"): 4429.53}   # INTRA/FC/IN CREDIT 'MARGIN INT ADJ' (row W1-S20; batch 195 ruled RETURN)

r4 = json.loads((D1 / "TIEOUT_49F_BLACKDIAMOND_R4.json").read_text(encoding="utf-8"))
by_acct = {}
for p in r4["pairs"]:
    by_acct.setdefault(p["account"], []).append(p)

# record every balance partition the producer reads, so the sign check and the null counts use the same bytes
BAL = {}
_orig = ard.read_partition


def _rp(s3_, bucket, prefix, day, columns=None):
    fr = _orig(s3_, bucket, prefix, day, columns=columns)
    if prefix == src["balance_prefix"] and fr is not None:
        BAL[day] = fr.copy()
    return fr


ard.read_partition = _rp


def bd_point(acct, start, end):
    r = json.load(gzip.open(D1 / ("RAW_BD_PERIOD_%s.sanitised.json.gz" % acct)))
    for p in r["combinedLevels"][0]["dateRangePoints"]:
        if p["dateRange"]["startDate"][:10] == start and p["dateRange"]["endDate"][:10] == end:
            return p
    raise SystemExit("no BD point %s %s %s" % (acct, start, end))


def bal(acct, day):
    fr = BAL[day]
    fr = fr[fr["account_id"].astype(str).str.zfill(10) == acct]
    return float(fr["net_mv_plus_cash"].iloc[0]), float(fr["margin_balance"].iloc[0])


res = []
for acct, pairs in sorted(by_acct.items()):
    a0, b0 = min(p["start"] for p in pairs), max(p["end"] for p in pairs)
    days = [str(d)[:10] for d in ard.tc.trading_days_between(a0, b0)]
    flows = ard.FlowCache(s3, src, table, keycols, [acct])
    vc, hc = ard.prefetch(s3, src, firm, days, trn_days, accounts=[acct], flows=flows, workers=12)
    rows, notes, _ = ard.compute_range(s3, src, firm, days, trn_days, accounts=[acct], thresholds=thresholds, flows=flows,
                                       value_cache=vc, holdings_cache=hc, first_data={acct: "2026-01-01"}, bal_days=bal_days)
    byday = {r["business_date"]: r for r in rows}
    for p in sorted(pairs, key=lambda x: x["start"]):
        wdays = [str(d)[:10] for d in ard.tc.trading_days_between(p["start"], p["end"])]
        wrows = [byday[d] for d in wdays if d in byday]
        gap, twr = len(wrows) != len(wdays), 1.0
        for r in wrows:
            v = r.get("total_return_daily")
            if v is None or v != v:
                gap = True
            else:
                twr *= 1.0 + float(v)
        prev = str(ard.tc.prev_trading_day(wdays[0]))[:10]
        v_prev, mb_prev = bal(acct, prev)
        v_end, mb_end = bal(acct, wdays[-1])
        bd = bd_point(acct, p["start"], p["end"])
        bd_twr = bd["timeWeightedReturns"]["return"]
        opal = None if gap else twr - 1.0
        # the one counterfactual the S22 pair needs: the 4,429.53 INTRA/FC/IN credit treated as a flow, as Black Diamond does
        adj = {d: x for (ac, d), x in INT_ADJ.items() if ac == acct and d in wdays}
        cf = None
        if adj:
            link, last = 1.0, prev
            for r in wrows:
                d = r["business_date"]
                eq_now = bal(acct, d)[0] + bal(acct, d)[1]
                eq_before = bal(acct, last)[0] + bal(acct, last)[1]
                link *= (eq_now - (r["external_flow"] + adj.get(d, 0.0))) / eq_before
                last = d
            cf = {"opal_twr": link - 1.0, "abs_diff": abs(link - 1.0 - bd_twr), "int_adj": adj}
        res.append({
            "account": acct, "start": p["start"], "end": p["end"], "bd_twr": bd_twr, "opal_twr_now": opal,
            "abs_diff_r4": p["abs_diff"], "abs_diff_now": None if opal is None else abs(opal - bd_twr),
            "opal_days": len(wrows), "window_days": len(wdays), "gap": gap,
            "bd_accrual_beginning": bd["beginningAccrual"], "bd_accrual_ending": bd["endingAccrual"],
            "bd_accrual": round(bd["endingAccrual"] - bd["beginningAccrual"], 2),
            "bd_net_additions": bd["netAdditions"], "bd_income": bd["income"],
            "sign_check": {
                "net_mv_plus_cash_before": v_prev, "margin_balance_before": mb_prev,
                "net_mv_plus_cash_end": v_end, "margin_balance_end": mb_end,
                "bd_beginning_minus_equity_plus_accrual": round(bd["beginningMarketValue"] - (v_prev + mb_prev + bd["beginningAccrual"]), 2),
                "bd_ending_minus_equity_plus_accrual": round(bd["endingMarketValue"] - (v_end + mb_end + bd["endingAccrual"]), 2),
                "bd_beginning_minus_net_mv_alone": round(bd["beginningMarketValue"] - v_prev, 2),
                "bd_ending_minus_net_mv_alone": round(bd["endingMarketValue"] - v_end, 2)},
            "counterfactual_int_adj_as_flow": cf,
            "quality_days": sorted({r.get("day_quality") for r in wrows}),
            "guard_states": sorted({r.get("guard_state") for r in wrows}),
        })
        print(acct, p["start"], p["end"], "now", None if opal is None else round(abs(opal - bd_twr), 6),
              "r4", round(p["abs_diff"], 6), flush=True)

# null counts over every balance partition the run read for the three accounts
accts = set(by_acct)
nulls = {"days_read": len(BAL), "account_rows": 0, "null_margin_balance_rows": 0, "null_net_mv_plus_cash_rows": 0}
for day, fr in BAL.items():
    fr = fr[fr["account_id"].astype(str).str.zfill(10).isin(accts)]
    nulls["account_rows"] += len(fr)
    nulls["null_margin_balance_rows"] += int(fr["margin_balance"].isna().sum())
    nulls["null_net_mv_plus_cash_rows"] += int(fr["net_mv_plus_cash"].isna().sum())
out.write_text(json.dumps({"method_version": ard.METHOD_VERSION, "pairs": res, "null_counts": nulls}, indent=1), encoding="utf-8")
print("nulls", nulls, flush=True)
