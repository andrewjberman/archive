"""Local driver (scratch, not committed): the round-21 sample's 61 accounts through the TABLE-based class producer, and the same
rows re-classified from the module's dictionary, so the two unclassified shares sit on the same positions."""
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting"))
import account_class_daily as acd  # noqa: E402
import etf_classification as module  # noqa: E402  (read-only, for the comparison only)
import boto3  # noqa: E402
from botocore.config import Config  # noqa: E402

rec21 = json.loads((ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~18/CLASS_DAILY_LOCAL_RUN.json").read_text(encoding="utf-8"))
accounts = rec21["accounts"]
days = rec21["days"]
s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))

captured = {}
orig = acd.compute_classes


def spy(*a, **k):
    captured["a"], captured["k"] = a, k
    return orig(*a, **k)


acd.compute_classes = spy
table = acd.ClassTable()
rows, run = acd.compute_local(s3, days, accounts, workers=12, table=table)
acd.compute_classes = orig


class ModTable:
    def get(self, ident, default=None):
        v = module.ETF_CLASSIFICATIONS.get(ident)
        return default if v is None else v


a, k = captured["a"], dict(captured["k"])
k["table"] = ModTable()
k["log"] = lambda m: None
mrows_by_day, mfail, _aud, mhold = orig(*a, **k)
assert not mfail, mfail
mrows = [r for d in days for r in mrows_by_day.get(d, [])]


def share_on(rs, day):
    return acd.unclassified_share([r for r in rs if r["business_date"] == day])


def census(rs):
    out = {}
    for r in rs:
        out[r["asset_class"]] = out.get(r["asset_class"], 0) + 1
    return out


hold = run["holdings"]
d_last = days[-1]
res = {
    "days": days, "accounts": len(accounts), "population": rec21.get("population"),
    "share_day": d_last,
    "table_share": share_on(rows, d_last), "module_share": share_on(mrows, d_last),
    "table_class_row_census": census(rows), "module_class_row_census": census(mrows),
    "class_rows_table": len(rows), "class_rows_module": len(mrows),
    "holdings_distinct": len(hold),
    "holdings_cash_position": sum(1 for v in hold.values() if v[1]),
    "holdings_table_held": sum(1 for v in hold.values() if v[0] is not None),
    "holdings_table_class_in_six": sum(1 for v in hold.values() if v[0] in acd.TABLE_CLASSES),
    "holdings_table_value_outside_six": sorted({v[0] for v in hold.values() if v[0] is not None and v[0] not in acd.TABLE_CLASSES}),
    "holdings_not_in_table": sum(1 for v in hold.values() if v[0] is None and not v[1]),
    "getitem_reads": table.reads,
    "coverage_account_days": {},
    "round21_recorded": {"class_rows": len(rec21["class_rows"]), "account_days": len(rec21["account_days"]),
                         "unclassified_class_rows": sum(1 for r in rec21["class_rows"] if r["class"] == "unclassified"),
                         "holdings_distinct": len(rec21["holding_map"])},
}
for a_ in run["audit"]:
    res["coverage_account_days"][a_["coverage"]] = res["coverage_account_days"].get(a_["coverage"], 0) + 1
# the identity on the MEASURED account-days
acct = {(a_["account_id"], a_["business_date"]): a_["account_daily_return"] for a_ in run["audit"] if a_["coverage"] == acd.COV_MEASURED}
sums = {}
for r in rows:
    if r["class_return_daily"] is not None:
        sums[(r["account_id"], r["business_date"])] = sums.get((r["account_id"], r["business_date"]), 0.0) + r["class_return_daily"]
res["measured_account_days"] = len(acct)
res["max_identity_gap"] = max((abs(sums[x] - float(v)) for x, v in acct.items()), default=None)
# the same shares by day, for the record
res["table_share_by_day"] = {d: share_on(rows, d)["value"] for d in days}
res["module_share_by_day"] = {d: share_on(mrows, d)["value"] for d in days}
Path(sys.argv[2]).write_text(json.dumps(res, indent=1, default=str), encoding="utf-8")
print(json.dumps({k_: v for k_, v in res.items() if k_ not in ("table_share_by_day", "module_share_by_day")}, default=str))
