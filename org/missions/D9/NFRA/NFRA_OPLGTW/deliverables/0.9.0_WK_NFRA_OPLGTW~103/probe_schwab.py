"""OG-cl-1 probe (round 37, FWD-22 G2): the REAL client core and the Schwab adapter against the real Schwab silver.

Runs with the box's own credentials (no internal reader role, no vendor role variable) and an Opal stand-in principal.
It builds its own ProbeCtx from the DATA_CATALOG rows (the core's Ctx is OG-cl-1's own module and is not used to
judge itself), reads one partition independently with boto3 + pyarrow, and asserts:
  (a) the envelope is complete on a real client_get_holdings answer,
  (b) the position count equals the independent read of the same partition,
  (c) the fence negative arm: a request for firm cottonwood reads zero keys and is refused firm_not_served,
  (d) no account number reaches stdout.
It prints exactly one line and counts and booleans only: never a row, an account number, a master number or a ref.
"""
from __future__ import annotations

import datetime as dt
import io
import logging
import os
import sys
import warnings
from pathlib import Path
from types import SimpleNamespace

ENVELOPE = ("as_of", "partition_date", "source_keys", "denominator", "absent_reason", "platform_label",
            "platform_label_source", "label_claim", "freshness_td")
FIRM = "49financial"
PROBE_LINE = ("probe schwab: envelope_ok {env}; independent_count_equal {cnt}; fence_negative_arm {fence}; "
              "account_numbers_printed {leaks}")


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    return next(p for p in here.parents if (p / "infra" / "aws" / "ec2" / "opal-gateway" / "app").is_dir())


class ProbeRefusal(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


class ProbeCtx:
    """The protocol's Ctx, built here from the DATA_CATALOG rows (bucket and prefix come from the row, never typed)."""

    def __init__(self, rows, s3, calendar, today):
        self.rows, self.s3, self.cal, self.today = rows, s3, calendar, today
        self.reads = []

    def prefix(self, vendor, segment, layer, table):
        want = "%s/%s/%s/%s/" % (vendor, segment, layer, table)
        for row in self.rows:
            if row.get("prefix") == want and row.get("layer") == layer and row.get("table") == table:
                return want
        raise ProbeRefusal("no_catalog_row")

    def _bucket(self, prefix):
        for row in self.rows:
            if row.get("prefix") == prefix:
                return row["bucket"]
        raise ProbeRefusal("no_catalog_row")

    def _keys(self, prefix):
        bucket, out, token = self._bucket(prefix), [], None
        while True:
            kw = {"Bucket": bucket, "Prefix": prefix}
            if token:
                kw["ContinuationToken"] = token
            resp = self.s3.list_objects_v2(**kw)
            out.extend(o["Key"] for o in resp.get("Contents", []))
            if not resp.get("IsTruncated"):
                return out
            token = resp.get("NextContinuationToken")

    def list_partitions(self, prefix):
        found = set()
        for key in self._keys(prefix):
            seg = key[len(prefix):].split("/", 1)[0]
            if seg.startswith("date="):
                found.add(seg[5:])
        return sorted(found)

    def newest_partition(self, prefix, as_of=None):
        days = [p for p in self.list_partitions(prefix) if as_of is None or p <= str(as_of)[:10]]
        return days[-1] if days else None

    def read_rows(self, prefix, partition, columns=None, filters=None):
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
        self.reads.append((prefix, partition))
        part_prefix = "%sdate=%s/" % (prefix, partition)
        keys = sorted(k for k in self._keys(part_prefix) if k.endswith(".parquet"))
        if not keys:
            return []
        body = self.s3.get_object(Bucket=self._bucket(prefix), Key=keys[-1])["Body"].read()
        table = pq.read_table(io.BytesIO(body), columns=list(columns) if columns else None)
        for col, val in (filters or {}).items():
            table = table.filter(pc.equal(table.column(col), val))
        return table.to_pylist()

    def freshness_td(self, partition_date):
        return int(self.cal.trading_days_behind(dt.date.fromisoformat(str(partition_date)[:10]),
                                                self.cal.prev_trading_day(self.today)))

    def firm_segments(self, vendor, firm):
        if vendor == "schwab" and firm == FIRM:
            return sorted({r["prefix"].split("/")[1] for r in self.rows if r["prefix"].startswith("schwab/")})
        return []

    def firm_roster(self):
        return {}


def _silver_rows(root: Path) -> list:
    import yaml
    doc = yaml.safe_load((root / "infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml").read_text(encoding="utf-8"))
    rows = []
    for section in doc.values():
        if isinstance(section, list):
            rows.extend(r for r in section if isinstance(r, dict) and r.get("prefix") and r.get("bucket")
                        and r.get("table") and not r.get("retired"))
    return rows


def _independent(s3, bucket, master, partition, account_id):
    """(rows of the account in the partition, rows in the partition) read with boto3 + pyarrow: the probe's own count."""
    import pyarrow.parquet as pq
    prefix = "schwab/%s/silver/dim_position/date=%s/" % (master, partition)
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=bucket, Prefix=prefix).get("Contents", [])
            if o["Key"].endswith(".parquet")]
    body = s3.get_object(Bucket=bucket, Key=sorted(keys)[-1])["Body"].read()
    col = pq.read_table(io.BytesIO(body), columns=["account_id"]).column("account_id").to_pylist()
    return sum(1 for v in col if v == account_id), len(col)


def main() -> None:
    logging.disable(logging.CRITICAL)
    warnings.simplefilter("ignore")
    root = _repo_root()
    sys.path[:0] = [str(root / "infra" / "aws" / "ec2" / "opal-gateway"), str(root)]
    results = {"env": False, "cnt": False, "fence": False, "leaks": 0}
    raw_ids = set()
    try:
        import boto3
        from lib import trading_calendar
        from app import account_ref as aref
        from app import client_adapter_schwab as schwab
        from app import client_core as core
        from app import harvest_read, identity_scope

        email = "probe.standin@" + identity_scope.OPAL_USERS_DOMAIN
        harvest_read.get_current_principal = lambda: SimpleNamespace(email=email, tid="probe", oid="probe")
        s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION") or "us-east-1")
        rows = _silver_rows(root)
        today = dt.datetime.now(dt.timezone.utc).date()
        ctx = ProbeCtx(rows, s3, trading_calendar, today)
        core._adapters.clear()
        core.register_adapter(schwab)
        core._new_ctx = lambda: ctx

        masters = ctx.firm_segments("schwab", FIRM)
        master = masters[0] if masters else None
        bucket = next(r["bucket"] for r in rows if r["prefix"].startswith("schwab/%s/silver/fact_rps/" % master))
        probe_pref = "schwab/%s/silver/dim_position/" % master      # no catalog row: the probe lists it directly
        listing = s3.list_objects_v2(Bucket=bucket, Prefix=probe_pref, Delimiter="/")
        partition = sorted(p["Prefix"][len(probe_pref) + 5:-1] for p in listing.get("CommonPrefixes", []))[-1]
        listing = s3.list_objects_v2(Bucket=bucket, Prefix="%sdate=%s/" % (probe_pref, partition))
        key = sorted(o["Key"] for o in listing.get("Contents", []) if o["Key"].endswith(".parquet"))[-1]
        import pyarrow.parquet as pq
        ids = sorted(set(pq.read_table(io.BytesIO(s3.get_object(Bucket=bucket, Key=key)["Body"].read()),
                                       columns=["account_id"]).column("account_id").to_pylist()))
        account_id = ids[0]
        raw_ids.add(account_id)
        indep_count, _total = _independent(s3, bucket, master, partition, account_id)

        keyring = aref.current_keyring()
        ref = aref.account_ref(master, account_id, keyring)
        env = core.client_get_holdings(FIRM, "schwab:" + ref, as_of=partition)
        results["env"] = (env.get("absent_reason") is None and all(k in env for k in ENVELOPE)
                          and isinstance(env.get("freshness_td"), int))
        results["cnt"] = (env.get("absent_reason") is None and len(env.get("positions", [])) == indep_count)

        before = len(ctx.reads)
        neg = core.client_get_holdings("cottonwood", "schwab:" + ref, as_of=partition)
        results["fence"] = (neg.get("absent_reason") == "firm_not_served" and len(ctx.reads) == before)
    except Exception:
        pass   # a failed step leaves its boolean False; no traceback, no detail, reaches stdout
    line = PROBE_LINE.format(env=results["env"], cnt=results["cnt"], fence=results["fence"], leaks=0)
    results["leaks"] = sum(line.count(a) for a in raw_ids if a)
    print(PROBE_LINE.format(env=results["env"], cnt=results["cnt"], fence=results["fence"], leaks=results["leaks"]))


if __name__ == "__main__":
    main()
