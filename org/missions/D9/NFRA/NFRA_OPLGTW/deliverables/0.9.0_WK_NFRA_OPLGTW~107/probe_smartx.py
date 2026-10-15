#!/usr/bin/env python3
"""NFRA_OPLGTW OG-cl-5 probe (round 37, G2-BUILD, FWD-22): the SmartX adapter against the REAL silver, read only.

Runs with the box's own AWS credentials (INTERNAL_READER_ROLE_ARN is not used). Builds its own ProbeCtx
(protocol A1 item 2): prefixes from the DATA_CATALOG rows, partitions by list_objects_v2, rows by pyarrow on the newest
part, freshness through lib/trading_calendar.py, and the roster through ctx.firm_roster() built from the repo file
data/mdpf/config/partner_roster.json: {advisor_name: firm_id} from partners[].aliases.advisor_name (protocol A2, by name).

Asserts (AC2): (a) the envelope is complete on a real answer; (b) an independent boto3 + pyarrow read of the same
partition gives the row count the tool reports in its denominator; (c) the fence negative arm: a request naming another
canonical firm is refused (firm_not_served) with zero keys read; (d) no account number reaches the output.

Prints exactly one line of counts and booleans. Account numbers are read into memory only and never printed.
"""
import datetime as dt
import io
import json
import re
import sys
import warnings
from pathlib import Path

warnings.simplefilter("ignore")


def _find_root():
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / "infra" / "aws" / "ec2" / "opal-gateway").is_dir():
            return p
    raise SystemExit(1)


ROOT = _find_root()
GW = ROOT / "infra" / "aws" / "ec2" / "opal-gateway"
sys.path[:0] = [str(GW), str(ROOT)]

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
import yaml  # noqa: E402

from lib.trading_calendar import expected_last_trading_day, trading_days_behind  # noqa: E402
import app.client_adapter_smartx as smx  # noqa: E402

BUCKET = "opal-data-assets"
CATALOG = GW / "app" / "refs" / "DATA_CATALOG.yaml"
ROSTER_FILE = ROOT / "data" / "mdpf" / "config" / "partner_roster.json"
VEND, SEG, LAY = smx.VENDOR, smx.SEGMENT, smx.LAYER
ENVELOPE_KEYS = ("as_of", "partition_date", "source_keys", "denominator", "absent_reason",
                 "platform_label", "platform_label_source", "label_claim", "freshness_td")


class ProbeCtx:
    """The context side of the protocol, for this probe only (the core's real Ctx is OG-cl-1's)."""

    def __init__(self, s3, catalog_rows):
        self.s3, self.rows, self.reads, self._roster = s3, catalog_rows, [], {}
        self._pag = s3.get_paginator("list_objects_v2")

    def prefix(self, vendor, segment, layer, table):
        key = "%s/%s/%s/%s/" % (vendor, segment, layer, table)
        hits = [r for r in self.rows
                if r.get("bucket") == BUCKET and r.get("key_template") == key and not r.get("retired")]
        if len(hits) != 1:
            raise smx.AdapterRefusal("no_catalog_row")
        return key

    def list_partitions(self, prefix):
        out = []
        for page in self._pag.paginate(Bucket=BUCKET, Prefix=prefix, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []):
                name = cp["Prefix"][len(prefix):].rstrip("/")
                if name.startswith("date="):
                    out.append(name[len("date="):])
        return sorted(out)

    def newest_partition(self, prefix, as_of=None):
        ps = [p for p in self.list_partitions(prefix) if as_of is None or p <= as_of]
        return ps[-1] if ps else None

    def _part_key(self, prefix, partition):
        keys = []
        for page in self._pag.paginate(Bucket=BUCKET, Prefix="%sdate=%s/" % (prefix, partition)):
            keys += [o["Key"] for o in page.get("Contents", []) if o["Key"].endswith(".parquet")]
        if not keys:
            raise RuntimeError("no parquet part under the partition")
        return max(keys)

    def read_rows(self, prefix, partition, columns=None, filters=None):
        key = self._part_key(prefix, partition)
        body = self.s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
        self.reads.append(key)
        return pq.read_table(io.BytesIO(body)).to_pylist()

    def freshness_td(self, partition_date):
        return trading_days_behind(partition_date, expected_last_trading_day(dt.date.today()))

    def firm_roster(self):
        return dict(self._roster)

    def firm_segments(self, vendor, firm):
        return [SEG] if (vendor == VEND and firm in smx.FIRMS) else []


def build_roster():
    """{advisor_name: canonical firm id}: the repo roster file's partners[].aliases.advisor_name (protocol A2).
    A name the file does not carry is absent: the adapter drops it and counts it (no nearest-firm guess)."""
    cfg = json.loads(ROSTER_FILE.read_text(encoding="utf-8", errors="replace"))
    roster = {}
    for p in cfg.get("partners", []):
        for name in (p.get("aliases") or {}).get("advisor_name", []):
            roster[name] = p.get("firm_id")
    return roster


def envelope_of(ans):
    return {"as_of": ans.get("_as_of"), "partition_date": ans.get("_partition_date"),
            "source_keys": ans.get("_source_keys"), "denominator": ans.get("_denominator"),
            "absent_reason": ans.get("_absent_reason"), "platform_label": ans.get("_platform_label"),
            "platform_label_source": ans.get("_platform_label_source"), "label_claim": ans.get("_label_claim"),
            "freshness_td": ans.get("_freshness_td")}


def envelope_ok(ans):
    e = envelope_of(ans)
    return (all(k in e for k in ENVELOPE_KEYS)
            and isinstance(e["as_of"], str) and isinstance(e["partition_date"], str)
            and isinstance(e["source_keys"], list) and len(e["source_keys"]) > 0
            and isinstance(e["denominator"], dict) and isinstance(e["denominator"].get("partition_rows"), int)
            and e["absent_reason"] is None and isinstance(e["platform_label"], str)
            and bool(e["platform_label_source"]) and e["label_claim"] in ("measured", "inferred")
            and isinstance(e["freshness_td"], int)
            and isinstance(ans.get("positions"), list) and isinstance(ans.get("cash"), float))


def run():
    s3 = boto3.client("s3")
    with CATALOG.open(encoding="utf-8", errors="replace") as fh:
        doc = yaml.load(fh, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    rows = [r for r in doc.get("silver_datasets", []) if isinstance(r, dict)]
    ctx = ProbeCtx(s3, rows)
    ctx._roster = build_roster()

    map_prefix = ctx.prefix(VEND, SEG, LAY, smx.T_MAP)
    full_numbers, cand, ans = set(), None, None
    for part in reversed(ctx.list_partitions(map_prefix)):
        mrows = ctx.read_rows(map_prefix, part)
        if not mrows:
            continue
        full_numbers = {str(m.get("account_number")) for m in mrows if m.get("account_number")}
        for m in mrows[:50]:
            last4 = str(m.get("account_number") or "")[-4:]
            if len(last4) != 4:
                continue
            res = smx.resolve_account(ctx, "49financial", last4)
            if res["candidates"]:
                cand, ans = res["candidates"][0], res
                break
        break
    if cand is None:
        raise RuntimeError("no resolvable live account in the newest non-empty map partition")
    hold = smx.get_holdings(ctx, "49financial", cand["account_ref"])

    env_ok = envelope_ok(hold)

    pos_prefix = ctx.prefix(VEND, SEG, LAY, smx.T_POS)
    pos_key = [k for k in ctx.reads if k.startswith(pos_prefix)][-1]
    indep_body = s3.get_object(Bucket=BUCKET, Key=pos_key)["Body"].read()
    indep_rows = pq.read_table(io.BytesIO(indep_body)).num_rows
    indep_ok = indep_rows > 0 and indep_rows == hold["_denominator"]["partition_rows"]

    neg_ok, neg_outputs = True, []
    for other in ("inflection", "cottonwood"):
        before = len(ctx.reads)
        try:
            out = smx.get_holdings(ctx, other, cand["account_ref"])
            neg_ok = False
            neg_outputs.append(out)
        except smx.AdapterRefusal as e:
            neg_ok = neg_ok and e.code == "firm_not_served" and len(ctx.reads) == before
            neg_outputs.append(e.code)

    blob = json.dumps({"hold": hold, "cand": ans, "keys": ctx.reads, "neg": [str(x) for x in neg_outputs]},
                      default=str)
    printed = len(set(re.findall(r"\d{8,}", blob)) & full_numbers)
    return env_ok, indep_ok, neg_ok, printed


def main():
    try:
        env_ok, indep_ok, neg_ok, printed = run()
    except Exception as e:  # the probe prints booleans only; the error class name carries no digits
        print("probe smartx: envelope_ok False; independent_count_equal False; fence_negative_arm False; "
              "account_numbers_printed 0")
        sys.stderr.write("probe error: %s\n" % type(e).__name__)
        return 1
    print("probe smartx: envelope_ok %s; independent_count_equal %s; fence_negative_arm %s; "
          "account_numbers_printed %d" % (env_ok, indep_ok, neg_ok, printed))
    return 0 if (env_ok and indep_ok and neg_ok and printed == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
