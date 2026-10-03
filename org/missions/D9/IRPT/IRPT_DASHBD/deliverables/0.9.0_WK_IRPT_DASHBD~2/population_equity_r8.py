"""IRPT_DASHBD TO-DB-b-15 -- the population figure and the guard on 2026-10-01 under BOTH value bases. READS ONLY: S3 get/list; nothing is
written to S3; no vendor call.

The "before" producer is the file at the base commit (git show <base>:account_return_daily.py + its sources.json), run as-is; the "after"
producer is the worktree's. Both read the SAME balance bytes (the cache scan_balance_history_r8.py wrote) through their own
read_partition, and the SAME transaction and holdings reads, so a difference between the two result sets is the value basis alone.

Usage: python population_equity_r8.py <repo_root> <balance_cache_dir> <base_commit> <out_json> [day]
"""
import importlib.util
import io
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

import boto3
import pandas as pd
import pyarrow.parquet as pq
from botocore.config import Config

root = Path(sys.argv[1]).resolve()
cache = Path(sys.argv[2]).resolve()
base = sys.argv[3]
out = Path(sys.argv[4])
day = sys.argv[5] if len(sys.argv) > 5 else "2026-10-01"
sys.path.insert(0, str(root))
REL = "data/assets/scripts/gold/irpt_reporting/"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# the base-commit producer, placed beside its own declaration, with the one path anchor repointed at this worktree
old_dir = root / ".scratch" / "old_v1"
old_dir.mkdir(parents=True, exist_ok=True)
for fn in ("account_return_daily.py", "sources.json"):
    blob = subprocess.run(["git", "show", "%s:%s%s" % (base, REL, fn)], cwd=str(root), capture_output=True, check=True).stdout
    (old_dir / fn).write_bytes(blob)
code = (old_dir / "account_return_daily.py").read_text(encoding="utf-8")
assert "_ROOT = _HERE.parents[5]" in code
(old_dir / "account_return_daily.py").write_text(code.replace("_ROOT = _HERE.parents[5]", "_ROOT = Path(%r)" % str(root)), encoding="utf-8")
new = load("ard_new", root / REL / "account_return_daily.py")
old = load("ard_old", old_dir / "account_return_daily.py")
assert new.METHOD_VERSION == 2 and old.METHOD_VERSION == 1, (new.METHOD_VERSION, old.METHOD_VERSION)

hspec = importlib.util.spec_from_file_location("rg_handler", root / "infra/aws/lambda/investor-reporting/reporting-gold/handler.py")
h = importlib.util.module_from_spec(hspec)
hspec.loader.exec_module(h)
thresholds = h.load_thresholds()

s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
doc_new = new.load_declaration()
src_new = new.source_entry(doc_new, new.declared_sources(doc_new)[0])
doc_old = old.load_declaration()
src_old = old.source_entry(doc_old, old.declared_sources(doc_old)[0])
assert "account_value_column" in src_old and "account_value_columns" in src_new
firm = new.firm_scope(src_new)

summary = json.loads((cache / "_summary.json").read_text(encoding="utf-8"))
cached_days = summary["days"]


def serve(mod, src):
    orig = mod.read_partition

    def rp(s3_, bucket, prefix, d, columns=None):
        if prefix == src["balance_prefix"]:
            f = cache / (d + ".parquet")
            if not f.is_file():
                return None
            fr = pd.read_parquet(f)
            return fr[columns].copy() if columns else fr
        return orig(s3_, bucket, prefix, d, columns=columns)
    mod.read_partition = rp
    mod.partition_days = lambda s3_, bucket, prefix: (list(cached_days) if prefix == src["balance_prefix"]
                                                      else _real_days(s3_, bucket, prefix))


_real_days = new.partition_days
serve(new, src_new)
serve(old, src_old)

# the population: the holdings gold's newest partition, as DB-b-11 read it
uri = new.opal_naming.address("irpt", firm, "gold", new.HOLDINGS_TABLE, "date=" + day)
bucket, key = new._split(uri)
hbase = key.rsplit("/date=", 1)[0] + "/"
keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix="%sdate=%s/" % (hbase, day)).get("Contents", []) if o["Key"].endswith(".parquet")]
frames = [pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=k)["Body"].read()), columns=["account_id"]).to_pandas() for k in keys]
population = sorted(set(pd.concat(frames)["account_id"].astype(str).str.strip()))
print("population", len(population), flush=True)

# --- positive counts on the day, from the balance bytes
bal = pd.read_parquet(cache / (day + ".parquet"))
bal["_a"] = bal["account_id"].astype(str).str.strip().str.zfill(10)
bal_p = bal[bal["_a"].isin(set(population))]
net = pd.to_numeric(bal_p["net_mv_plus_cash"], errors="coerce")
mb = pd.to_numeric(bal_p["margin_balance"], errors="coerce")
eq = net + mb
positive_before = int((net > 0).sum())
positive_after = int((eq > 0).sum())
print("population rows in dim_balance:", len(bal_p), "positive before", positive_before, "after", positive_after, flush=True)

# --- inception under each basis, over every cached partition, through each producer's own first_data_dates
fd_old = old.first_data_dates(s3, src_old, day, accounts=population, workers=1)
fd_new = new.first_data_dates(s3, src_new, day, accounts=population, workers=1)
print("first_data accounts old/new:", len(fd_old), len(fd_new), flush=True)

trn_days = new.partition_days(s3, src_new["bucket"], src_new["transactions_prefix"])
bal_days = list(cached_days)
table, keycols = new.load_classification(src_new)
flows = new.FlowCache(s3, src_new, table, keycols, population)
value_new, hold = new.prefetch(s3, src_new, firm, [day], trn_days, accounts=population, flows=flows, workers=8)
value_old = {}
for d in value_new:
    value_old[d] = old.account_values(s3, src_old, d, accounts=population)
rows_new, notes_new, _ = new.compute_range(s3, src_new, firm, [day], trn_days, accounts=population, thresholds=thresholds, flows=flows,
                                           value_cache=value_new, holdings_cache=hold, first_data=fd_new, bal_days=bal_days)
rows_old, notes_old, _ = old.compute_range(s3, src_old, firm, [day], trn_days, accounts=population, thresholds=thresholds, flows=flows,
                                           value_cache=value_old, holdings_cache=hold, first_data=fd_old, bal_days=bal_days)
by_new = {r["account_id"]: r for r in rows_new}
by_old = {r["account_id"]: r for r in rows_old}
print("rows old/new:", len(rows_old), len(rows_new), flush=True)

common = sorted(set(by_new) & set(by_old))
only_old, only_new = sorted(set(by_old) - set(by_new)), sorted(set(by_new) - set(by_old))
gs_before_all, gs_after_all = Counter(r["guard_state"] for r in rows_old), Counter(r["guard_state"] for r in rows_new)
gs_before_c, gs_after_c = Counter(by_old[a]["guard_state"] for a in common), Counter(by_new[a]["guard_state"] for a in common)

# --- the one rule: margin_balance 0 on the day AND on the prior trading day (its whole input) computes identical rows
prev = str(new.tc.prev_trading_day(day))[:10]
bprev = pd.read_parquet(cache / (prev + ".parquet"))
bprev["_a"] = bprev["account_id"].astype(str).str.strip().str.zfill(10)
mb_prev = dict(zip(bprev["_a"], pd.to_numeric(bprev["margin_balance"], errors="coerce")))
mb_day = dict(zip(bal_p["_a"], mb))


def same(a, b):
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, float) and isinstance(b, float) and a != a and b != b:
        return True
    return a == b


def diff_fields(a):
    return [k for k in by_new[a] if k != "method_version" and not same(by_new[a][k], by_old[a][k])]


zero_both = [a for a in common if mb_day.get(a) == 0 and mb_prev.get(a) == 0]
zero_day_only = [a for a in common if mb_day.get(a) == 0 and mb_prev.get(a) != 0]
zero_changed = [a for a in zero_both if diff_fields(a)]
zero_day_only_changed = [a for a in zero_day_only if diff_fields(a)]
nonzero = [a for a in common if mb_day.get(a) != 0]
nonzero_changed = [a for a in nonzero if diff_fields(a)]
null_day = int(bal["margin_balance"].isna().sum())
null_pop = int(mb.isna().sum())
null_net_day = int(bal["net_mv_plus_cash"].isna().sum())
hist_null = 0
hist_null_net = 0
hist_rows = 0
no_margin_col = [d for d, (st, _n) in summary["status"].items() if st == "NO_MARGIN_COLUMN"]
for d in cached_days:
    f = cache / (d + ".parquet")
    if f.is_file():
        fr = pd.read_parquet(f, columns=["net_mv_plus_cash", "margin_balance"])
        hist_rows += len(fr)
        hist_null += int(fr["margin_balance"].isna().sum())
        hist_null_net += int(fr["net_mv_plus_cash"].isna().sum())

rec = {
    "day": day, "accounts": len(population), "positive_before": positive_before, "positive_after": positive_after,
    "guard_state_before": dict(sorted(gs_before_c.items())), "guard_state_after": dict(sorted(gs_after_c.items())),
    "zero_margin_accounts": len(zero_both), "zero_margin_rows_changed": len(zero_changed),
    "null_margin_balance_rows": null_day,
    "detail": {
        "row_basis": "guard_state counted over the %d rows both versions emit; rows emitted only by one version are listed in rows_only_before/after" % len(common),
        "rows_before_all": len(rows_old), "rows_after_all": len(rows_new),
        "guard_state_before_all_rows": dict(sorted(gs_before_all.items())), "guard_state_after_all_rows": dict(sorted(gs_after_all.items())),
        "rows_only_before": len(only_old), "rows_only_after": len(only_new),
        "zero_margin_definition": "margin_balance exactly 0 on %s AND on the prior trading day %s (the two inputs of one daily row)" % (day, prev),
        "zero_margin_on_day_only_prior_nonzero": len(zero_day_only), "zero_margin_on_day_only_rows_changed": len(zero_day_only_changed),
        "nonzero_margin_rows": len(nonzero), "nonzero_margin_rows_changed": len(nonzero_changed),
        "null_margin_balance_rows_population": null_pop, "null_net_mv_plus_cash_rows_day": null_net_day,
        "history_partitions": len(cached_days), "history_rows": hist_rows,
        "history_null_margin_balance_rows": hist_null, "history_null_net_mv_plus_cash_rows": hist_null_net,
        "partitions_without_margin_column": no_margin_col,
        "population_accounts_in_dim_balance": int(len(bal_p)),
        "first_data_accounts_before": len(fd_old), "first_data_accounts_after": len(fd_new),
        "positive_to_nonpositive_under_equity": int(((net > 0) & ~(eq > 0)).sum()),
        "nonpositive_to_positive_under_equity": int((~(net > 0) & (eq > 0)).sum()),
        "vendor_calls": 0,
    },
}
out.write_text(json.dumps(rec, indent=1, default=str), encoding="utf-8")
print(json.dumps({k: v for k, v in rec.items() if k != "detail"}), flush=True)
print(json.dumps(rec["detail"]), flush=True)
