"""OG-cl-2 probe (task order AC2): the Black Diamond 49F adapter against the REAL silver, read only.

Run from anywhere: python <this file>. It prints exactly one line:
  probe bd49f: envelope_ok <bool>; independent_count_equal <bool>; fence_negative_arm <bool>; account_numbers_printed <int>
It prints no row, no account number, no name and no amount. Reads use the box's own credentials.

The adapter's context is the core's (app/client_core.py, OG-cl-1), which is not on any ref of this checkout (surprise
NFRA_OPLGTW-Z-W104-S2). This probe supplies a PROBE-LOCAL context with the protocol's six methods: prefixes come from the
DATA_CATALOG rows (the live opal-data-bd rows by their bucket and prefix fields), partitions are the dated names only,
every read goes through typed_scope.admit_scope and typed_scope.read_parquet, and the principal is an Opal stand-in.
"""
import datetime as _dt
import io
import os
import re
import sys
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, *([os.pardir] * 7)))
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
AUDIT_DIR = os.path.join(ROOT, ".scratch")
os.makedirs(AUDIT_DIR, exist_ok=True)
os.environ["AUDIT_PATH"] = os.path.join(AUDIT_DIR, "probe_bd49f_audit.jsonl")
sys.path.insert(0, GW)
sys.path.insert(0, os.path.join(ROOT, "lib"))

FIREWALL_LINE = "probe bd49f: envelope_ok {e}; independent_count_equal {c}; fence_negative_arm {f}; account_numbers_printed {n}"
KEYS = ("_as_of", "_partition_date", "_source_keys", "_denominator", "_platform_label", "_platform_label_source",
        "_label_claim", "_freshness_td", "_cadence")
DATED_KEY = re.compile(r"(\d{4}-\d{2}-\d{2})(?:/data)?\.parquet$")
LAST4 = re.compile(r"^[A-Za-z0-9]{4}$")


def _last4(number):
    alnum = re.sub(r"[^A-Za-z0-9]", "", str(number or ""))
    return alnum[-4:].upper() if len(alnum) >= 4 else None


class ProbeCtx:
    """The protocol's ctx, probe-local: catalog prefixes, dated partitions, admitted reads, a read log of keys."""

    def __init__(self, adapter, s3, ts, catalog_rows, freshness):
        self.A, self.s3, self.ts, self.rows, self._freshness = adapter, s3, ts, catalog_rows, freshness
        self.bucket_of, self.key_of, self.reads = {}, {}, []

    def _scope(self, bucket):
        served = tuple(sorted(p for p, b in self.bucket_of.items() if b == bucket))
        return self.ts.Scope(bucket.rsplit("-", 1)[-1], bucket, served, lambda: self.s3)

    def prefix(self, vendor, segment, layer, table):
        rule = KEY_RULE.get((segment, table))
        if rule is None:
            raise self.A.AdapterRefusal("no_catalog_row")
        bucket, key_stem = rule
        hits = [r for r in self.rows if r.get("bucket") == bucket and not r.get("retired")
                and str(r.get("key_template") or "").startswith(key_stem)]
        if len(hits) != 1:
            raise self.A.AdapterRefusal("no_catalog_row")
        prefix = key_stem
        self.bucket_of[prefix] = bucket
        return prefix

    def list_partitions(self, prefix):
        bucket = self.bucket_of[prefix]
        refusal = self.ts.admit_scope(self._scope(bucket), "probe_list", prefix)
        if refusal:
            raise RuntimeError("admission refused the listing")
        found = {}
        for item in self.ts.list_keys(self._scope(bucket), prefix):
            rel = item["key"][len(prefix):]
            match = DATED_KEY.search(rel)
            if match:
                found[match.group(1)] = item["key"]
        for date, key in found.items():
            self.key_of[(prefix, date)] = key
        return sorted(found)

    def read_rows(self, prefix, partition, columns=None, filters=None):
        bucket = self.bucket_of[prefix]
        key = self.key_of[(prefix, partition)]
        refusal = self.ts.admit_scope(self._scope(bucket), "probe_read", key)
        if refusal:
            raise RuntimeError("admission refused the read")
        self.reads.append((bucket, key))
        rows, _total, _nbytes = self.ts.read_parquet(self._scope(bucket), key, columns=columns)
        for k, v in (filters or {}).items():
            rows = [r for r in rows if r.get(k) == v]
        return rows

    def freshness_td(self, partition_date):
        return self._freshness(partition_date)

    def firm_segments(self, vendor, firm):
        return ["49f"] if firm == "49financial" else []


# (segment, table) -> (bucket, key_template stem). A catalog row matches when its bucket and key_template start with
# the stem, and exactly one row must match (ruling A1 2 of G2_ADAPTER_PROTOCOL.md). The live tables are addressed as
# the firm segment plus -live, which the adapter derives; the stems are the census's live and assets prefixes.
KEY_RULE = {
    ("49f", "dim_account_xref"): ("opal-data-assets", "blackdiamond/49f/silver/dim_account_xref/"),
    ("49f", "fact_bd_allocation"): ("opal-data-assets", "blackdiamond/49f/silver/fact_bd_allocation/"),
    ("49f-live", "unrealized"): ("opal-data-bd", "silver/unrealized/"),
    ("49f-live", "transactions"): ("opal-data-bd", "silver/transactions/"),
    ("49f-live", "fees"): ("opal-data-bd", "silver/fees/"),
    ("49f-live", "allocations"): ("opal-data-bd", "silver/allocations/"),
}


def _catalog_rows():
    """Every catalog row (dict) of the runtime catalog, read once; the probe matches them by bucket and key_template."""
    from app.integrations.portal_index import integration
    loaded = integration.runtime_catalog()
    root = loaded.get("catalog", loaded) if isinstance(loaded, dict) else loaded
    rows = []

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("entity"), str) and "bucket" in node:
                rows.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(root)
    return rows


def _freshness_fn():
    import trading_calendar as tc
    frontier = tc.prev_trading_day(_dt.date.today())

    def fresh(partition_date):
        return tc.trading_days_behind(partition_date, frontier)

    return fresh


def _window(frontier_day):
    end = frontier_day
    start = end - _dt.timedelta(days=45)
    return start.isoformat(), end.isoformat()


def run():
    import boto3
    import pyarrow.parquet as pq
    from app import harvest_read, identity_scope
    from app import typed_scope as ts
    from app import client_adapter_bd49f as A

    stand_in = SimpleNamespace(email="opal.probe@%s" % identity_scope.OPAL_USERS_DOMAIN, tid="probe", oid="probe")
    harvest_read.get_current_principal = lambda: stand_in
    s3 = boto3.client("s3")
    ctx = ProbeCtx(A, s3, ts, _catalog_rows(), _freshness_fn())

    # 1. a real last-4 from the newest dimension partition (read in memory, never printed)
    dim_prefix = ctx.prefix(A.VENDOR, "49f", "silver", "dim_account_xref")
    newest = ctx.list_partitions(dim_prefix)[-1]
    sample = ctx.read_rows(dim_prefix, newest, columns=["bd_account_number"])
    last4 = _last4(sample[0]["bd_account_number"])
    known_ids = set()

    # 2. the real answers, each through the adapter
    res = A.resolve_account(ctx, "49financial", last4)
    for c in res["candidates"]:
        known_ids.add(c["account_ref"].split("|", 1)[1])
    envelope_ok = all(k in res for k in KEYS) and res["_partition_date"] is not None and res["candidates"]
    ref = res["candidates"][0]["account_ref"]
    frontier = _dt.date.today() - _dt.timedelta(days=1)
    start, end = _window(frontier)
    answers = [res]
    for call in (
        lambda: A.get_holdings(ctx, "49financial", ref),
        lambda: A.get_transactions(ctx, "49financial", ref, from_date=start, to_date=end),
        lambda: A.get_fees(ctx, "49financial", ref, from_date=start, to_date=end),
        lambda: A.get_allocation(ctx, "49financial", ref),
    ):
        try:
            answers.append(call())
        except A.AdapterRefusal:
            pass    # a refusal is not an answer; the envelope is judged on the answers that were returned
    for ans in answers:
        if not all(k in ans for k in KEYS):
            envelope_ok = False
        if ans.get("_partition_date") is not None and ans.get("_freshness_td") is None:
            envelope_ok = False
    envelope_ok = bool(envelope_ok)

    # 3. independent count: footer row count and distinct matching accounts of the same dimension partition
    key = ctx.key_of[(dim_prefix, newest)]
    body = s3.get_object(Bucket=ctx.bucket_of[dim_prefix], Key=key)["Body"].read()
    footer_rows = pq.ParquetFile(io.BytesIO(body)).metadata.num_rows
    table = pq.read_table(io.BytesIO(body), columns=["bd_account_id", "bd_account_number"]).to_pylist()
    independent = {r["bd_account_id"] for r in table
                   if _last4(r["bd_account_number"]) == last4 and str(r["bd_account_id"] or "").startswith("z08")}
    for r in table:
        known_ids.add(str(r["bd_account_id"]))
    independent_ok = (footer_rows == res["_denominator"]["partition_rows"]
                      and len(independent) == res["_denominator"]["candidates"])

    # 4. fence negative arm: another firm reads nothing, and no read key leaves the 49F keys
    before = len(ctx.reads)
    neg_refused = False
    try:
        A.resolve_account(ctx, "cottonwood", last4)
    except A.AdapterRefusal as exc:
        neg_refused = exc.code == "firm_not_served"
    neg_reads = len(ctx.reads) - before
    stray = [k for b, k in ctx.reads if b == "opal-data-assets" and not k.startswith("blackdiamond/49f/")]
    fence_ok = neg_refused and neg_reads == 0 and not stray

    # 5. no account number reaches the line
    line = FIREWALL_LINE.format(e=envelope_ok, c=independent_ok, f=fence_ok, n=0)
    leaked = sum(1 for value in known_ids if value and value in line)
    return envelope_ok, independent_ok, fence_ok, leaked


def main():
    try:
        e, c, f, n = run()
    except Exception as exc:    # the line still prints; the class name is the only detail, never a value
        sys.stderr.write("probe error: %s\n" % type(exc).__name__)
        e, c, f, n = False, False, False, 0
    print(FIREWALL_LINE.format(e=e, c=c, f=f, n=n))


if __name__ == "__main__":
    main()
