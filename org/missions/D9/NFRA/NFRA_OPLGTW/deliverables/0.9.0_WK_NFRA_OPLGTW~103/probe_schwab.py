"""OG-cl-1 probe (round 37, FWD-22 G2): the REAL client core and the Schwab adapter against the real Schwab silver.

Runs with the box's own credentials (no internal reader role, no vendor role variable) and an Opal stand-in principal.
Rulings applied (A1 items 2, 3, 5; A2 S2-S5, S7):
  * ProbeCtx builds its own prefixes from the DATA_CATALOG rows. A dim_* table with NO catalog row falls back, for that
    row only, to the served-key form schwab/<master>/silver/<table>/ in the bucket the catalog gives for the neighbouring
    fact_* row of the same master. No fact_* table is ever read in place of a dim_* table.
  * The alias key is a THROWAWAY Keyring made in-process and installed through account_ref.current_keyring (the seam
    the adapter reads the key by). It is never printed and never written.
  * The account_ref is the protocol form "****<last4>/schwab/<alias>", minted by the adapter's own mint for one account
    that this probe finds INDEPENDENTLY (boto3 + pyarrow).
  * The negative arm: a request for firm cottonwood is refused firm_not_served with zero S3 calls.

It asserts (a) the envelope is complete on a real client_get_holdings answer, (b) the position count equals the
independent read of the same partition, (c) the fence negative arm, (d) no account number reaches stdout or the
diagnostics. It prints exactly one line on stdout (the PROBE_LINE). Diagnostics go to stderr: counts, booleans and
refusal codes only, never a row, an account number, a master number or a ref.
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
TABLES = ("dim_position", "dim_balance", "dim_transaction")
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
    """The protocol's Ctx, built here from the DATA_CATALOG rows (bucket and prefix come from the rows, never typed)."""

    def __init__(self, rows, s3, calendar, today):
        self.rows, self.s3, self.cal, self.today = rows, s3, calendar, today
        self.reads = []
        self.s3_calls = 0
        self.fallbacks = set()

    def _row_for(self, prefix):
        for row in self.rows:
            if row.get("prefix") == prefix:
                return row
        return None

    def _neighbour_bucket(self, prefix):
        """The bucket the catalog gives for the neighbouring fact_* row of the same master (A2 S2), or no_catalog_row."""
        master = prefix.split("/")[1]
        for row in self.rows:
            if str(row.get("prefix", "")).startswith("schwab/%s/silver/fact_" % master):
                return row["bucket"]
        raise ProbeRefusal("no_catalog_row")

    def prefix(self, vendor, segment, layer, table):
        want = "%s/%s/%s/%s/" % (vendor, segment, layer, table)
        for row in self.rows:
            if row.get("prefix") == want and row.get("layer") == layer and row.get("table") == table:
                return want
        if vendor == "schwab" and layer == "silver" and table in TABLES:
            self._neighbour_bucket(want)          # the fallback needs its neighbour, else no_catalog_row
            self.fallbacks.add(want)
            return want
        raise ProbeRefusal("no_catalog_row")

    def _bucket(self, prefix):
        row = self._row_for(prefix)
        if row is not None:
            return row["bucket"]
        if prefix in self.fallbacks:
            return self._neighbour_bucket(prefix)
        raise ProbeRefusal("no_catalog_row")

    def _keys(self, bucket, prefix):
        out, token = [], None
        while True:
            kw = {"Bucket": bucket, "Prefix": prefix}
            if token:
                kw["ContinuationToken"] = token
            self.s3_calls += 1
            resp = self.s3.list_objects_v2(**kw)
            out.extend(o["Key"] for o in resp.get("Contents", []))
            if not resp.get("IsTruncated"):
                return out
            token = resp.get("NextContinuationToken")

    def list_partitions(self, prefix):
        found = set()
        for key in self._keys(self._bucket(prefix), prefix):
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
        bucket = self._bucket(prefix)
        part_prefix = "%sdate=%s/" % (prefix, partition)
        keys = sorted(k for k in self._keys(bucket, part_prefix) if k.endswith(".parquet"))
        if not keys:
            return []
        self.s3_calls += 1
        body = self.s3.get_object(Bucket=bucket, Key=keys[-1])["Body"].read()
        table = pq.read_table(io.BytesIO(body), columns=list(columns) if columns else None)
        for col, val in (filters or {}).items():
            table = table.filter(pc.equal(table.column(col), val))
        return table.to_pylist()

    def freshness_td(self, partition_date):
        return int(self.cal.trading_days_behind(dt.date.fromisoformat(str(partition_date)[:10]),
                                                self.cal.prev_trading_day(self.today)))

    def firm_segments(self, vendor, firm):
        if vendor == "schwab" and firm == FIRM:
            return sorted({r["prefix"].split("/")[1] for r in self.rows if str(r.get("prefix", "")).startswith("schwab/")})
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


def _newest_part_rows(s3, bucket, prefix, columns):
    """(newest partition, rows of its newest part): the probe's own read, straight from boto3 + pyarrow."""
    import pyarrow.parquet as pq
    listing = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
    partition = sorted(p["Prefix"][len(prefix) + 5:-1] for p in listing.get("CommonPrefixes", []))[-1]
    listing = s3.list_objects_v2(Bucket=bucket, Prefix="%sdate=%s/" % (prefix, partition))
    key = sorted(o["Key"] for o in listing.get("Contents", []) if o["Key"].endswith(".parquet"))[-1]
    body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    return partition, pq.read_table(io.BytesIO(body), columns=columns).to_pylist()


def main() -> None:
    logging.disable(logging.CRITICAL)
    warnings.simplefilter("ignore")
    root = _repo_root()
    sys.path[:0] = [str(root / "infra" / "aws" / "ec2" / "opal-gateway"), str(root)]
    results = {"env": False, "cnt": False, "fence": False}
    diag = {}
    raw_ids = set()
    try:
        import boto3
        from lib import trading_calendar
        from app import account_ref as aref
        from app import client_adapter_schwab as schwab
        from app import client_core as core
        from app import data_entitlement as de
        from app import harvest_read, identity_scope

        email = "probe.standin@" + identity_scope.OPAL_USERS_DOMAIN
        harvest_read.get_current_principal = lambda: SimpleNamespace(email=email, tid="probe", oid="probe")
        # A2 S3: a THROWAWAY alias key, made in-process and installed through the seam the adapter reads the key by.
        throwaway = aref.Keyring("v1", os.urandom(32))
        aref.current_keyring = lambda: throwaway
        s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION") or "us-east-1")
        rows = _silver_rows(root)
        today = dt.datetime.now(dt.timezone.utc).date()
        ctx = ProbeCtx(rows, s3, trading_calendar, today)
        core._adapters.clear()
        core.register_adapter(schwab)
        core._new_ctx = lambda: ctx

        masters = ctx.firm_segments("schwab", FIRM)
        diag["firm_segments"] = len(masters)
        diag["catalog_rows_absent"] = sum(1 for m in masters for t in TABLES
                                          if ctx._row_for("schwab/%s/silver/%s/" % (m, t)) is None)
        master = masters[0]
        bucket = ctx._neighbour_bucket("schwab/%s/silver/dim_position/" % master)
        prefix = ctx.prefix("schwab", master, "silver", "dim_position")
        partition, pos_rows = _newest_part_rows(s3, bucket, prefix, ["account_id"])
        ids = sorted({r["account_id"] for r in pos_rows if r.get("account_id")})
        account_id = ids[0]
        raw_ids.add(account_id)
        indep_count = sum(1 for r in pos_rows if r.get("account_id") == account_id)
        diag["independent_rows_of_account"] = indep_count
        diag["partition_rows"] = len(pos_rows)

        ref = schwab.mint_account_ref(master, account_id)     # "****<last4>/schwab/<alias>", via the adapter's mint
        env = core.client_get_holdings(FIRM, ref, as_of=partition)
        diag["absent_reason"] = env.get("absent_reason")
        results["env"] = (env.get("absent_reason") is None and all(k in env for k in ENVELOPE)
                          and isinstance(env.get("freshness_td"), int))
        results["cnt"] = (env.get("absent_reason") is None and indep_count > 0
                          and len(env.get("positions", [])) == indep_count)

        before_s3, before_reads = ctx.s3_calls, len(ctx.reads)
        neg = core.client_get_holdings("cottonwood", ref, as_of=partition)
        results["fence"] = (neg.get("absent_reason") == "firm_not_served" and ctx.s3_calls == before_s3
                            and len(ctx.reads) == before_reads)
        diag["fence_absent_reason"] = neg.get("absent_reason")
        diag["fallback_prefixes_used"] = len(ctx.fallbacks)

        # Diagnostic (not on the AC2 line): an account of a master the registry does not hold is refused at the mint.
        unregistered = [m for m in masters if m not in de.MASTERS]
        diag["unregistered_masters"] = len(unregistered)
        if unregistered:
            um = unregistered[0]
            upart, urows = _newest_part_rows(s3, ctx._neighbour_bucket("schwab/%s/silver/dim_position/" % um),
                                             ctx.prefix("schwab", um, "silver", "dim_position"), ["account_id"])
            uids = sorted({r["account_id"] for r in urows if r.get("account_id")})
            if uids:
                raw_ids.add(uids[0])
                try:
                    schwab.mint_account_ref(um, uids[0])
                    diag["unregistered_mint_refused"] = False
                except schwab.AdapterRefusal as exc:
                    diag["unregistered_mint_refused"] = exc.code == "master_not_registered"
    except Exception as exc:   # a failed step leaves its boolean False; the class or refusal code only, never a message
        diag["error"] = getattr(exc, "code", None) or type(exc).__name__
    diag_text = "probe diagnostics: " + " ".join("%s %s" % (k, v) for k, v in sorted(diag.items()))
    leaks = sum(diag_text.count(a) for a in raw_ids if a)
    print(PROBE_LINE.format(env=results["env"], cnt=results["cnt"], fence=results["fence"], leaks=leaks))
    print(diag_text, file=sys.stderr)


if __name__ == "__main__":
    main()
