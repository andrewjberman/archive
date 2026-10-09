"""IRPT_DASHBD TO-DB-b-13 -- recompute OPAL's side of the three like-day windows beyond 0.35 pp, LOCALLY, with the producer in this
worktree (the one under test). READS ONLY (S3 get/list of the Schwab silver and the holdings gold the producer reads); nothing is
written to S3 and NO vendor call is made. Black Diamond's side is the stored round-4 record TIEOUT_49F_BLACKDIAMOND_R4.json.

Usage: python remeasure_three_pairs_r6.py <repo_root> <out_json>
Writes {"pairs": [{account,start,end,opal_twr,days:[{date,v,flow,income,income_return,total_return_daily,quality}]}]}.
"""
import importlib.util
import json
import sys
from pathlib import Path

import boto3
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("rg_handler", root / "infra/aws/lambda/investor-reporting/reporting-gold/handler.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
ard = h.ard

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


PAIRS = [(_REAL("acct#89d0916a"), "2026-06-25", "2026-07-06"),
         (_REAL("acct#ffa615d2"), "2026-08-21", "2026-10-01"),
         (_REAL("acct#89d0916a"), "2026-04-09", "2026-04-30")]

s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc = ard.load_declaration()
src = ard.source_entry(doc, ard.declared_sources(doc)[0])
firm = ard.firm_scope(src)
thresholds = h.load_thresholds()
table, keycols = ard.load_classification(src)
trn_days = ard.partition_days(s3, src["bucket"], src["transactions_prefix"])
bal_days = ard.partition_days(s3, src["bucket"], src["balance_prefix"])

res = []
for acct, a, b in PAIRS:
    days = [str(d)[:10] for d in ard.tc.trading_days_between(a, b)]
    flows = ard.FlowCache(s3, src, table, keycols, [acct])
    vc, hc = ard.prefetch(s3, src, firm, days, trn_days, accounts=[acct], flows=flows, workers=8)
    rows, notes, _ = ard.compute_range(s3, src, firm, days, trn_days, accounts=[acct], thresholds=thresholds, flows=flows,
                                       value_cache=vc, holdings_cache=hc, first_data={acct: "2026-01-01"}, bal_days=bal_days)
    daily, twr, gap = [], 1.0, False
    for r in rows:
        v = r.get("total_return_daily")
        if v is None or v != v:
            gap = True
        else:
            twr *= 1.0 + float(v)
        daily.append({"date": r["business_date"], "v": r["market_value_eod"], "flow": r["external_flow"],
                      "income": r["income_received"], "income_return": r.get("income_return"),
                      "total_return_daily": v, "quality": r.get("day_quality"), "carried_days": r.get("carried_days")})
    res.append({"account": acct, "start": a, "end": b, "opal_days": len(rows), "gap": gap,
                "opal_twr": (None if gap else twr - 1.0), "days": daily})
    print(acct, a, b, len(rows), "twr", None if gap else round(twr - 1.0, 6), flush=True)
out.write_text(json.dumps({"pairs": res}, indent=1), encoding="utf-8")
