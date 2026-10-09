"""IRPT_DASHBD TO-DB-b-13 -- WHY the three like-day pairs disagree: reconcile Black Diamond's stored round-4 account-level window
points (endpoints, additions, accruals) to the Schwab balance fields Opal's producer reads, and replay the window with the two
measured differences applied as COUNTERFACTUALS (never written anywhere). READS ONLY; no vendor call: Black Diamond's side is
RAW_BD_PERIOD_<account>.sanitised.json.gz in this folder.

Usage: python decompose_three_pairs_r6.py <repo_root> <remeasure_json> <out_json>
"""
import gzip
import importlib.util
import json
import sys
from pathlib import Path

import boto3

root = Path(sys.argv[1]).resolve()
rem = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("ard", root / "data/assets/scripts/gold/irpt_reporting/account_return_daily.py")
ard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ard)
HERE = Path(__file__).resolve().parent
s3 = boto3.client("s3")
doc = ard.load_declaration()
src = ard.source_entry(doc, ard.declared_sources(doc)[0])
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


INT_ADJ = {(_REAL("acct#89d0916a"), "2026-06-25"): 4429.53}   # INTRA/FC/IN CREDIT 'MARGIN INT ADJ', read from fact_trn 2026-06-25


def bd_point(acct, start, end):
    r = json.load(gzip.open(HERE / ("RAW_BD_PERIOD_%s.sanitised.json.gz" % acct)))
    for p in r["combinedLevels"][0]["dateRangePoints"]:
        if p["dateRange"]["startDate"][:10] == start and p["dateRange"]["endDate"][:10] == end:
            return p
    raise SystemExit("no BD point %s %s %s" % (acct, start, end))


def bal(acct, day):
    b = ard.read_partition(s3, src["bucket"], src["balance_prefix"], day,
                           columns=["account_id", "net_mv_plus_cash", "margin_balance"])
    b = b[b["account_id"].astype(str).str.zfill(10) == acct]
    return float(b["net_mv_plus_cash"].iloc[0]), float(b["margin_balance"].iloc[0])


out = []
for p in rem["pairs"]:
    acct, a, b_ = p["account"], p["start"], p["end"]
    days = [d["date"] for d in p["days"]]
    prev = str(ard.tc.prev_trading_day(days[0]))[:10]
    v, mb = {}, {}
    for d in [prev] + days:
        v[d], mb[d] = bal(acct, d)
    bd = bd_point(acct, a, b_)

    def chain(use_mb, adj):
        link, last = 1.0, prev
        for d in days:
            flow = next(x["flow"] for x in p["days"] if x["date"] == d) + adj.get(d, 0.0)
            now = v[d] + (mb[d] if use_mb else 0.0)
            before = v[last] + (mb[last] if use_mb else 0.0)
            link *= (now - flow) / before
            last = d
        return link - 1.0

    adj = {d: x for (ac, d), x in INT_ADJ.items() if ac == acct and d in days}
    bd_twr = bd["timeWeightedReturns"]["return"]
    now = p["opal_twr"]
    cf_mb = chain(True, {})
    cf_both = chain(True, adj) if adj else None
    out.append({
        "account": acct, "start": a, "end": b_, "bd_twr": bd_twr, "opal_twr_now": now, "abs_diff_now": abs(now - bd_twr),
        "bd": {"beginning_value": bd["beginningMarketValue"], "ending_value": bd["endingMarketValue"],
               "beginning_accrual": bd["beginningAccrual"], "ending_accrual": bd["endingAccrual"],
               "net_additions": bd["netAdditions"], "income": bd["income"], "net_gains": bd["netGains"]},
        "opal": {"value_before_window": v[prev], "value_at_end": v[days[-1]], "margin_balance_before": mb[prev],
                 "margin_balance_at_end": mb[days[-1]], "window_external_flow": round(sum(x["flow"] for x in p["days"]), 2),
                 "window_income_received_signed": round(sum(x["income"] for x in p["days"]), 2)},
        "reconciliation": {
            "bd_beginning_minus_opal_V_plus_margin_balance_plus_accrual":
                round(bd["beginningMarketValue"] - (v[prev] + mb[prev] + bd["beginningAccrual"]), 2),
            "bd_ending_minus_opal_V_plus_margin_balance_plus_accrual":
                round(bd["endingMarketValue"] - (v[days[-1]] + mb[days[-1]] + bd["endingAccrual"]), 2)},
        "counterfactual_V_plus_margin_balance": {"opal_twr": cf_mb, "abs_diff": abs(cf_mb - bd_twr)},
        "counterfactual_V_plus_margin_balance_and_int_adj_as_flow":
            ({"opal_twr": cf_both, "abs_diff": abs(cf_both - bd_twr), "int_adj": adj} if adj else None),
    })
    print(acct, a, "now %.4f%% cf_mb %.4f%% cf_both %s bd %.4f%%" % (
        100 * abs(now - bd_twr), 100 * abs(cf_mb - bd_twr), None if cf_both is None else "%.4f%%" % (100 * abs(cf_both - bd_twr)),
        100 * bd_twr), flush=True)
Path(sys.argv[3]).write_text(json.dumps({"pairs": out}, indent=1), encoding="utf-8")
