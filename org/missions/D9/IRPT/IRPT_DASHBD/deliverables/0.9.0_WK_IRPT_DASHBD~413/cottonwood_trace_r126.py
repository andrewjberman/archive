"""IRPT_DASHBD round 126, cell DB-c-21 (worker 0.9.0_WK_IRPT_DASHBD~413) -- the Cottonwood FWD-1 trace, read only.

Reads the Cottonwood silver (fact_holdings, fact_allocations), the Cottonwood gold (holdings_performance_daily,
account_dim) and the reporting-gold households source through ONE read-only reader class: ReadOnlyS3 has only
list_prefixes(bucket, prefix) and get(bucket, key). No put, delete, create, invoke or update exists in this file.

Usage: python <this file> <worktree root> <out json> <out note-facts json>
Writes the record JSON (no identifier value) and a facts JSON the note is written from.
"""
import datetime as dt
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT_RECORD = Path(sys.argv[2])
OUT_FACTS = Path(sys.argv[3])
sys.path.insert(0, str(ROOT))
import lib.opal_naming as naming  # noqa: E402  (the builder's own address() and lookup())

DATE = re.compile(r"date=(\d{4}-\d{2}-\d{2})/?$")
COT_DIR = ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"
REPORTING_HANDLER = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
BOUNDARY_TABLES = ("account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily", "account_class_daily")


def utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ReadOnlyS3(object):
    """GET and LIST only. The class has two data methods, list_prefixes and get, and no write method."""

    def __init__(self, client):
        self._s3 = client
        self.list_calls = 0
        self.get_calls = 0
        self.get_keys = []

    def list_prefixes(self, bucket, prefix):
        out = []
        for page in self._s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
            self.list_calls += 1
            out.extend(cp["Prefix"] for cp in page.get("CommonPrefixes", []) or [])
        return out

    def get(self, bucket, key):
        self.get_calls += 1
        self.get_keys.append(key)
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def partition_dates(prefixes):
    return sorted({m.group(1) for m in (DATE.search(p) for p in prefixes) if m})


def silver_prefixes():
    """(bucket, prefix) of the two silver tables, from silver_locations() of the account_dim producer (no AWS call)."""
    code = ("import json,sys; sys.path.insert(0,'infra/aws/lambda/investor-reporting/account-dim-cot'); "
            "import lambda_function as L; print(json.dumps(L.silver_locations('2000-01-03')))")
    r = subprocess.run([sys.executable, "-c", code], cwd=str(ROOT), capture_output=True, text=True, timeout=100)
    if r.returncode != 0:
        raise SystemExit("silver_locations failed: " + r.stderr.strip()[-300:])
    locs = json.loads(r.stdout.strip().splitlines()[-1])
    suffix = "date=2000-01-03/data.parquet"
    out = {}
    for t in ("fact_holdings", "fact_allocations"):
        b, k = locs[t]
        assert k.endswith(suffix), k
        out[t] = (b, k[: -len(suffix)])
    return out


def gold_prefix(table):
    addr = naming.address("irpt", "cottonwood", "gold", table, "date=2000-01-03", "data.parquet")
    m = re.match(r"s3://([^/]+)/(.*)date=2000-01-03/data\.parquet$", addr)
    assert m, addr
    return m.group(1), m.group(2)


def households_from_rows(rows):
    """The reader's grouping rule: distinct non-blank household_id among rows with a non-null account_id."""
    hh = {}
    for r in rows:
        h, a = r.get("household_id"), r.get("account_id")
        if h is None or str(h).strip() == "" or a is None:
            continue
        hh.setdefault(h, set()).add(a)
    return hh


def main():
    import boto3
    import pyarrow.parquet as pq

    reader = ReadOnlyS3(boto3.client("s3", region_name="us-east-1"))
    facts = {"silver": {}, "gold": {}, "reporting_gold": {}}

    # 1. silver: a fresh LIST of each table's date= partitions
    for t, (b, p) in silver_prefixes().items():
        d = partition_dates(reader.list_prefixes(b, p))
        facts["silver"][t] = {"partitions": len(d), "newest_date": d[-1] if d else None, "read_utc": utc(), "bucket": b, "prefix": p}

    # 2. gold: newest partition of the two Cottonwood tables, read through the same list/get pair
    gold_objs = {}
    for t in ("holdings_performance_daily", "account_dim"):
        b, p = gold_prefix(t)
        d = partition_dates(reader.list_prefixes(b, p))
        if not d:
            raise SystemExit("NOT_ESTABLISHED: no partition under " + t)
        key = p + "date=%s/data.parquet" % d[-1]
        tbl = pq.read_table(io.BytesIO(reader.get(b, key)))
        gold_objs[t] = tbl
        facts["gold"][t] = {"newest_date": d[-1], "rows": tbl.num_rows, "read_utc": utc(), "columns": tbl.column_names}

    # the holdings daily column that names the account (exactly one candidate name must be present)
    cands = [c for c in gold_objs["holdings_performance_daily"].column_names if c.lower() in ("account_id", "accountid", "account_number")]
    if len(cands) != 1:
        raise SystemExit("NOT_ESTABLISHED: account column candidates in holdings daily: %r" % cands)
    col = cands[0]
    ad_tbl = gold_objs["account_dim"]
    ad_rows = ad_tbl.select(["account_id", "household_id"]).to_pylist()
    hp_accts = {str(v).strip() for v in gold_objs["holdings_performance_daily"].column(col).to_pylist() if v is not None}
    ad_accts = {str(r["account_id"]).strip() for r in ad_rows if r.get("account_id") is not None}
    hh = households_from_rows(ad_rows)
    nohh = len({str(r["account_id"]).strip() for r in ad_rows if r.get("account_id") is not None
                and (r.get("household_id") is None or str(r.get("household_id")).strip() == "")})
    facts["gold"]["account_dim"].update({"households": len(hh), "accounts_without_household": nohh})
    facts["gold"]["crosswalk"] = {"holdings_account_column": col, "overlap": len(hp_accts & ad_accts),
                                  "only_in_holdings": len(hp_accts - ad_accts), "only_in_account_dim": len(ad_accts - hp_accts),
                                  "read_utc": utc()}
    facts["gold"]["crosswalk"]["holdings_distinct_accounts"] = len(hp_accts)
    facts["gold"]["crosswalk"]["account_dim_distinct_accounts"] = len(ad_accts)

    # 3. reporting gold: the households call the Cottonwood reader makes (its own newest-partition rule), read-only
    spec = importlib.util.spec_from_file_location("cottonwood_report_reader", str(COT_DIR / "cottonwood_report_reader.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    adapter = mod.CottonwoodAdapter(naming)
    before = len(reader.get_keys)
    next_hh = adapter.households(reader, None)
    got = reader.get_keys[before:]
    src_date = re.search(r"date=(\d{4}-\d{2}-\d{2})/", got[-1]) if got else None
    facts["reporting_gold"]["next_run_source_partition"] = src_date.group(1) if src_date else "NOT_ESTABLISHED"
    facts["reporting_gold"]["next_run_households"] = len(next_hh)
    facts["reporting_gold"]["read_utc"] = utc()
    facts["reporting_gold"]["absent_missing_tables"] = sorted(mod.MISSING_TABLES.keys())
    facts["reporting_gold"]["reader_table_names"] = list(mod.FIRM_TABLES)

    facts["reads"] = {"s3_list_calls": reader.list_calls, "s3_get_calls": reader.get_calls, "writes": 0, "invokes": 0}
    facts["holdings_column"] = col
    OUT_FACTS.write_text(json.dumps(facts, indent=2, sort_keys=True), encoding="ascii")
    print("facts written: list calls %d, get calls %d" % (reader.list_calls, reader.get_calls))


if __name__ == "__main__":
    main()
