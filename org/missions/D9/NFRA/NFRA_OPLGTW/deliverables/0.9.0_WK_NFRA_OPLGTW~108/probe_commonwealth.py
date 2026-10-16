"""OG-cl-6 probe (round 37, NFRA_OPLGTW): the Commonwealth adapter against the REAL silver.

Runs with the box's own AWS credentials (INTERNAL_READER_ROLE_ARN must be unset) and an Opal stand-in principal.
Prints exactly one line of counts and booleans. It never prints an account number, a row or an amount.

The real Ctx lives in OG-cl-1's app/client_core.py, which this ref does not hold, so this file carries its own
ProbeCtx built to G2_ADAPTER_PROTOCOL.md (amendment A1, item 2): prefix from the DATA_CATALOG row, partitions through
boto3 list_objects_v2, rows through pyarrow, freshness through lib/trading_calendar.py.
"""
import io
import os
import re
import sys
import datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[7]
GW = REPO / "infra" / "aws" / "ec2" / "opal-gateway"
sys.path.insert(0, str(GW))
sys.path.insert(0, str(REPO / "lib"))

VENDOR = "commonwealth"
SEGMENT = "cottonwood"
BUCKET_EXPECTED = "opal-data-assets"
PARTITION_RE = re.compile(r"/date=([0-9]{4}-[0-9]{2}-[0-9]{2})/")


class ProbeCtx:
    """The protocol's Ctx, served from the catalog and the bucket. Records every key it reads."""

    def __init__(self, s3, adapter_mod):
        import yaml
        import trading_calendar as tc
        self.s3, self.cw, self.tc = s3, adapter_mod, tc
        self.frontier = tc.prev_trading_day(dt.date.today()).isoformat()   # T-1 frontier
        self.reads = []
        self.bucket = {}
        with open(str(REPO / "infra" / "aws" / "ec2" / "opal-gateway" / "app" / "refs" / "DATA_CATALOG.yaml"),
                  encoding="utf-8") as fh:
            cat = yaml.safe_load(fh)
        self.rows = [r for r in cat.get("silver_datasets", []) or [] if isinstance(r, dict)]

    def prefix(self, vendor, segment, layer, table):
        want = "%s/%s/%s/%s/" % (vendor, segment, layer, table)
        hits = [r for r in self.rows if r.get("key_template") == want and r.get("bucket") == BUCKET_EXPECTED
                and r.get("retired") is False]
        if len(hits) != 1:
            raise self.cw.AdapterRefusal("no_catalog_row")
        pfx = hits[0]["prefix"]
        self.bucket[pfx] = hits[0]["bucket"]
        return pfx

    def _keys(self, prefix):
        out, tok = [], None
        while True:
            kw = {"Bucket": self.bucket.get(prefix, BUCKET_EXPECTED), "Prefix": prefix}
            if tok:
                kw["ContinuationToken"] = tok
            r = self.s3.list_objects_v2(**kw)
            out += [o["Key"] for o in r.get("Contents", [])]
            if not r.get("IsTruncated"):
                return out
            tok = r["NextContinuationToken"]

    def list_partitions(self, prefix):
        return sorted({m.group(1) for k in self._keys(prefix) for m in [PARTITION_RE.search(k)] if m})

    def newest_partition(self, prefix, as_of=None):
        ps = [p for p in self.list_partitions(prefix) if as_of is None or p <= as_of]
        return ps[-1] if ps else None

    def read_rows(self, prefix, partition, columns=None, filters=None):
        import pyarrow.parquet as pq
        import pyarrow.compute as pc
        keys = sorted(k for k in self._keys(prefix)
                      if "/date=%s/" % partition in k and k.endswith(".parquet"))
        out = []
        for k in keys:
            self.reads.append(k)
            body = self.s3.get_object(Bucket=self.bucket.get(prefix, BUCKET_EXPECTED), Key=k)["Body"].read()
            names = set(pq.read_schema(io.BytesIO(body)).names)
            want = [c for c in (columns or sorted(names)) if c in names]
            fcols = list((filters or {}).keys())
            read_cols = list(dict.fromkeys(want + [c for c in fcols if c in names]))
            t = pq.read_table(io.BytesIO(body), columns=read_cols)
            for col, val in (filters or {}).items():
                t = t.filter(pc.equal(t.column(col), val))
            out += t.select(want).to_pylist()
        return out

    def freshness_td(self, partition_date):
        return self.tc.trading_days_behind(partition_date, self.frontier)

    def firm_segments(self, vendor, firm):
        return [SEGMENT] if (vendor, firm) == (VENDOR, SEGMENT) else []


def _independent(s3, prefix_parts_key, want_account):
    """boto3 + pyarrow, outside the adapter: (partition rows, rows of the account, first crosswalk row ordinal)."""
    import pyarrow.parquet as pq
    pos_keys = [o["Key"] for o in s3.list_objects_v2(
        Bucket=BUCKET_EXPECTED, Prefix="commonwealth/cottonwood/silver/positions/date=2026-06-23/").get("Contents", [])
        if o["Key"].endswith(".parquet")]
    rows, mine_acct = 0, []
    for k in pos_keys:
        body = s3.get_object(Bucket=BUCKET_EXPECTED, Key=k)["Body"].read()
        t = pq.read_table(io.BytesIO(body), columns=["AccountNumber"])
        rows += t.num_rows
        mine_acct += t.column("AccountNumber").to_pylist()
    return rows, mine_acct


def main():
    if os.environ.get("INTERNAL_READER_ROLE_ARN"):
        return False, None
    import boto3
    from app import client_adapter_commonwealth as cw
    s3 = boto3.client("s3", region_name="us-east-1")
    ctx = ProbeCtx(s3, cw)

    # Stand-in principal: a synthetic Opal-domain identity gates the probe's use of the real silver.
    from app import query_v0
    standin = "probe-standin@" + query_v0.INTERNAL_DOMAINS[0]
    principal_ok = standin.rsplit("@", 1)[-1] in query_v0.INTERNAL_DOMAINS

    # Choose one account with positions (independent read; the account number is never printed).
    import pyarrow.parquet as pq
    pos_key = [k for k in ctx._keys("commonwealth/cottonwood/silver/positions/")
               if "/date=2026-06-23/" in k and k.endswith(".parquet")][0]
    t = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET_EXPECTED, Key=pos_key)["Body"].read()),
                      columns=["AccountNumber"])
    raw = sorted(set(t.column("AccountNumber").to_pylist()))[0]
    indep_partition_rows, indep_mine = _independent(s3, None, raw)
    indep_account_rows = sum(1 for a in indep_mine if a == raw)

    # Independent crosswalk ordinal of that account (same parquet row order the adapter reads).
    xw_key = [k for k in ctx._keys("commonwealth/cottonwood/silver/crosswalk/")
              if "/date=2026-06-23/" in k and k.endswith(".parquet")][0]
    xw = pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET_EXPECTED, Key=xw_key)["Body"].read()),
                       columns=["commonwealth_account"]).column("commonwealth_account").to_pylist()
    ordinal = xw.index(raw)

    cands = cw.resolve_account(ctx, SEGMENT, raw[-4:])["candidates"]
    ref = [c["account_ref"] for c in cands if c["account_ref"].endswith("|%05d" % ordinal)][0]
    out = cw.get_holdings(ctx, SEGMENT, ref)

    # Envelope: the fields the core's envelope needs, plus the freshness the core derives from the partition.
    d = out.get("_denominator") or {}
    env = {
        "as_of": out.get("_as_of"),
        "partition_date": out.get("_partition_date"),
        "source_keys": out.get("_source_keys"),
        "denominator": d,
        "absent_reason": None,
        "platform_label": out.get("_platform_label"),
        "platform_label_source": out.get("_platform_label_source"),
        "label_claim": out.get("_label_claim"),
        "freshness_td": ctx.freshness_td(out.get("_partition_date")),
    }
    envelope_ok = (bool(env["as_of"]) and bool(env["partition_date"]) and bool(env["source_keys"])
                   and isinstance(d, dict) and bool(d) and env["platform_label"] == "commonwealth"
                   and env["label_claim"] == "inferred" and isinstance(env["freshness_td"], int)
                   and env["freshness_td"] > 0 and principal_ok)

    counts_equal = (d.get("rows") == indep_partition_rows and d.get("rows_of_account") == indep_account_rows
                    and len(out.get("positions") or []) == indep_account_rows)

    # Fence negative arm: keys read name only this firm's segment; other canonical firms are refused, read nothing.
    before = len(ctx.reads)
    refused = 0
    for other in ("inflection", "49financial"):
        try:
            cw.get_holdings(ctx, other, ref)
        except cw.AdapterRefusal as e:
            refused += 1 if e.code == "firm_not_served" else 0
    only_own = all(k.startswith("commonwealth/cottonwood/silver/") for k in ctx.reads)
    fence_ok = (refused == 2 and len(ctx.reads) == before and only_own)

    # No account number reaches stdout: the printed line carries counts and booleans only.
    line = ("probe commonwealth: envelope_ok %s; independent_count_equal %s; fence_negative_arm %s; "
            "account_numbers_printed %d" % (envelope_ok, counts_equal, fence_ok, 0))
    assert raw not in line
    return None, line


if __name__ == "__main__":
    try:
        res = main()
    except Exception as e:  # no traceback: a botocore message can carry an ARN with a 12-digit account id
        res = None
        print("probe commonwealth: envelope_ok False; independent_count_equal False; fence_negative_arm False; "
              "account_numbers_printed 0 (error %s)" % type(e).__name__)
        sys.exit(1)
    if res and res[0] is False:
        print("probe commonwealth: envelope_ok False; independent_count_equal False; fence_negative_arm False; "
              "account_numbers_printed 0")
        sys.exit(1)
    print(res[1])
    sys.exit(0)
