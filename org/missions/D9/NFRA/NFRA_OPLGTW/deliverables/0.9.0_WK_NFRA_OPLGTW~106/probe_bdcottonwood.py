"""OG-cl-4 probe (round 37): the Black Diamond Cottonwood adapter against the REAL silver, with the box's credentials.

Builds its own ProbeCtx (the core's Ctx is OG-cl-1's, not on this ref) from the DATA_CATALOG silver rows, then asserts:
  (a) the envelope is complete on real answers (resolve, holdings, transactions, allocation, fees);
  (b) an independent boto3 + pyarrow read of the same holdings partition gives the row count the tool reports in its
      denominator, and the same partition date;
  (c) the fence negative arm: a request naming another canonical firm is refused with zero reads, and every read of a
      cottonwood request names only the cottonwood segment;
  (d) no custodian account number appears in any adapter return or refusal text.
It prints ONE line of counts and booleans and nothing that holds eight or more digits in a row.
Run from the repo root: python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~106/probe_bdcottonwood.py
"""
import datetime as _dt
import io
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[7]
GW = REPO / "infra" / "aws" / "ec2" / "opal-gateway"
for p in (str(GW), str(REPO)):
    if p not in sys.path:
        sys.path.insert(0, p)

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

from app import client_adapter_bdcottonwood as A  # noqa: E402
from app.integrations.portal_index.integration import runtime_catalog  # noqa: E402
from lib import trading_calendar as tc  # noqa: E402

VENDOR = "blackdiamond"
SEG = "cottonwood"
DATE_DIR = re.compile(r"date=(\d{4}-\d{2}-\d{2})/\Z")
ENVELOPE_KEYS = ("_as_of", "_partition_date", "_source_keys", "_denominator", "_platform_label",
                 "_platform_label_source", "_label_claim", "_freshness_td")


class ProbeCtx:
    """The Context side of G2_ADAPTER_PROTOCOL.md, built from the DATA_CATALOG silver rows and the live bucket."""

    def __init__(self):
        self.s3 = boto3.client("s3")
        self.rows = [r for r in runtime_catalog()["catalog"]["silver_datasets"] if not r.get("retired")]
        self.bucket_of = {}
        self.reads = []
        self.segments = {(VENDOR, SEG): [SEG]}
        self.expected = tc.expected_last_trading_day(_dt.datetime.now())

    def prefix(self, vendor, segment, layer, table):
        want = "%s/%s/%s/%s/" % (vendor, segment, layer, table)
        hits = [r for r in self.rows if r.get("key_template") == want and r.get("prefix") == want
                and r.get("layer") == layer]
        if len(hits) != 1:
            raise A.AdapterRefusal("no_catalog_row")
        self.bucket_of[want] = hits[0]["bucket"]
        return want

    def list_partitions(self, prefix):
        resp = self.s3.get_paginator("list_objects_v2").paginate(
            Bucket=self.bucket_of[prefix], Prefix=prefix, Delimiter="/")
        dates = []
        for page in resp:
            for cp in page.get("CommonPrefixes", []):
                m = DATE_DIR.search(cp["Prefix"])
                if m:
                    dates.append(m.group(1))
        return sorted(dates)

    def newest_partition(self, prefix, as_of=None):
        ps = [p for p in self.list_partitions(prefix) if as_of is None or p <= as_of]
        return ps[-1] if ps else None

    def read_rows(self, prefix, partition, columns=None, filters=None):
        self.reads.append((prefix, partition))
        bucket = self.bucket_of[prefix]
        keys = []
        for page in self.s3.get_paginator("list_objects_v2").paginate(
                Bucket=bucket, Prefix="%sdate=%s/" % (prefix, partition)):
            keys.extend(o["Key"] for o in page.get("Contents", []) if o["Key"].endswith(".parquet"))
        body = self.s3.get_object(Bucket=bucket, Key=sorted(keys)[-1])["Body"].read()
        table = pq.read_table(io.BytesIO(body), columns=columns)
        rows = table.to_pylist()
        for k, v in (filters or {}).items():
            rows = [r for r in rows if r.get(k) == v]
        return rows

    def freshness_td(self, partition_date):
        return tc.trading_days_behind(partition_date, self.expected)

    def firm_segments(self, vendor, firm):
        return self.segments.get((vendor, firm), [])


def _envelope_ok(out, need_absent_key=False):
    if not all(k in out for k in ENVELOPE_KEYS):
        return False
    if not isinstance(out["_partition_date"], str) or not out["_source_keys"]:
        return False
    if not isinstance(out["_denominator"], dict) or not all(isinstance(v, int) for v in out["_denominator"].values()):
        return False
    if not isinstance(out["_freshness_td"], int):
        return False
    if need_absent_key and "absent_reason" not in out:
        return False
    return True


def _custodian_numbers(ctx):
    """Every custodian Account Number of the newest allocations partition, as strings of eight or more digits."""
    p = ctx.prefix(VENDOR, SEG, "silver", "fact_allocations")
    part = ctx.newest_partition(p)
    rows = ctx.read_rows(p, part, columns=["Account Number"])
    nums = {str(r["Account Number"]) for r in rows if r.get("Account Number")}
    return {n for n in nums if len(re.sub(r"\D", "", n)) >= 8 and n.isdigit()}


def run():
    ctx = ProbeCtx()
    result = {"envelope_ok": False, "independent_count_equal": False, "fence_negative_arm": False, "leaks": -1}
    texts = []
    nums = _custodian_numbers(ctx)

    # choose one real account present in both the allocations and the holdings newest partitions (in memory)
    alloc_p = ctx.prefix(VENDOR, SEG, "silver", "fact_allocations")
    hold_p = ctx.prefix(VENDOR, SEG, "silver", "fact_holdings")
    ap = ctx.newest_partition(alloc_p)
    hp = ctx.newest_partition(hold_p)
    alloc_ids = {r["AccountID"]: r["Account Number"] for r in
                 ctx.read_rows(alloc_p, ap, columns=["AccountID", "Account Number"])
                 if str(r.get("AccountID", "")).startswith("z09")}
    hold_ids = {r["AccountID"] for r in ctx.read_rows(hold_p, hp, columns=["AccountID"])}
    common = sorted(set(alloc_ids) & hold_ids)
    if not common:
        return result, texts
    aid = common[0]
    last4 = A._last4(alloc_ids[aid])
    ctx.reads.clear()

    res = A.resolve_account(ctx, "cottonwood", last4)
    texts.append(repr(res))
    ref = next(c["account_ref"] for c in res["candidates"] if c["account_ref"].endswith("/" + aid))
    to_d = hp
    from_d = (_dt.date.fromisoformat(hp) - _dt.timedelta(days=60)).isoformat()

    hold = A.get_holdings(ctx, "cottonwood", ref)
    txn = A.get_transactions(ctx, "cottonwood", ref, from_date=from_d, to_date=to_d)
    alloc = A.get_allocation(ctx, "cottonwood", ref)
    fees = A.get_fees(ctx, "cottonwood", ref, from_date=from_d, to_date=to_d)
    for o in (hold, txn, alloc, fees):
        texts.append(repr(o))
    envelope_ok = (_envelope_ok(res) and _envelope_ok(hold, True) and _envelope_ok(txn, True)
                   and _envelope_ok(alloc, True) and _envelope_ok(fees, True)
                   and hold["_denominator"]["account_rows"] > 0)

    # (b) an independent read of the same holdings partition
    s3 = boto3.client("s3")
    bucket = ctx.bucket_of[hold_p]
    indep_dirs = sorted(p["Prefix"] for page in s3.get_paginator("list_objects_v2").paginate(
        Bucket=bucket, Prefix=hold_p, Delimiter="/") for p in page.get("CommonPrefixes", []))
    indep_date = DATE_DIR.search(indep_dirs[-1]).group(1)
    indep_keys = sorted(o["Key"] for page in s3.get_paginator("list_objects_v2").paginate(
        Bucket=bucket, Prefix=indep_dirs[-1]) for o in page.get("Contents", []) if o["Key"].endswith(".parquet"))
    indep_obj = s3.get_object(Bucket=bucket, Key=indep_keys[-1])["Body"].read()
    indep_rows = pq.read_table(io.BytesIO(indep_obj), columns=["AccountID"]).num_rows
    independent_count_equal = (indep_rows == hold["_denominator"]["partition_rows"]
                               and indep_date == hold["_partition_date"])

    # (c) the fence negative arm: another canonical firm is refused with zero reads
    before = len(ctx.reads)
    refused = []
    for firm in ("49financial", "inflection"):
        try:
            A.get_holdings(ctx, firm, ref)
            refused.append(False)
        except A.AdapterRefusal as e:
            refused.append(e.code == "firm_not_served")
            texts.append(e.code)
    zero_reads = len(ctx.reads) == before
    cottonwood_only = all(SEG in prefix.split("/")[1] and "/49f/" not in prefix and "/inflection/" not in prefix
                          for prefix, _ in ctx.reads[:before])
    fence_negative_arm = all(refused) and zero_reads and cottonwood_only

    # (d) no custodian number in any adapter return or refusal text
    blob = "".join(texts)
    leaks = sum(len(re.findall(r"(?<![0-9])%s(?![0-9])" % re.escape(n), blob)) for n in nums)
    result.update(envelope_ok=envelope_ok, independent_count_equal=independent_count_equal,
                  fence_negative_arm=fence_negative_arm, leaks=leaks)
    return result, texts


def main():
    try:
        result, _ = run()
    except Exception:  # noqa: BLE001 -- the probe reports booleans only; a failure reads False, never a traceback
        result = {"envelope_ok": False, "independent_count_equal": False, "fence_negative_arm": False, "leaks": -1}
    ok = bool(result["envelope_ok"] and result["independent_count_equal"] and result["fence_negative_arm"]
              and result["leaks"] == 0)
    print("probe bdcottonwood: envelope_ok %s; independent_count_equal %s; fence_negative_arm %s; "
          "account_numbers_printed %d" % (bool(result["envelope_ok"]), bool(result["independent_count_equal"]),
                                          bool(result["fence_negative_arm"]), max(result["leaks"], 0)))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
