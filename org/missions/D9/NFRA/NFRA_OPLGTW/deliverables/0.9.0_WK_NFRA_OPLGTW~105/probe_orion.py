"""NFRA_OPLGTW OG-cl-3 AC2 probe (round 37): the Orion adapter against the REAL silver, with the box's own credentials
and an Opal stand-in principal. Prints ONE line of booleans and counts; never a row, an account number or a name.

Fail-closed by construction. Every prefix comes from the DATA_CATALOG.yaml row whose key_template names the table
(ProbeCtx.prefix, per the A1 ruling); a table with no single live row raises no_catalog_row and the probe reads
nothing. The gateway's runtime index (app/graphql_plumbing/catalog_gate.py) does not carry these silver rows; that is
recorded in the surprise channel, not worked around here. Each boolean is True only when the measured fact holds:
- envelope_ok: a real answer (resolve, then holdings) carrying the envelope keys with a denominator;
- independent_count_equal: a boto3 plus pyarrow read of the same partition has the tool's partition_rows count;
- fence_negative_arm: the answer read at least one row, every read is under the firm's own segment, and a request for
  another firm is refused with zero reads (a refusal read nothing, so it is not a pass by itself).
account_numbers_printed counts account numbers this probe prints: the probe prints none, so it is 0.

Run from the repo root: python <this file> [--diag]. --diag writes the refusal code to stderr only.
"""

import contextlib
import io
import logging
import os
import re
import sys

logging.disable(logging.CRITICAL)     # the probe's one line is its only output; library logs are silenced

HERE = os.path.abspath(os.path.dirname(__file__))
SCRATCH_AUDIT = os.path.join(HERE, "..", "..", "..", "..", "..", "..", "..", ".scratch", "probe_orion_audit.jsonl")


def _repo_root():
    d = HERE
    while True:
        if os.path.isdir(os.path.join(d, "infra", "aws", "ec2", "opal-gateway")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


ROOT = _repo_root()
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway") if ROOT else None
DIAG = "--diag" in sys.argv
_state = {"reads": [], "error": None}


def _code_of(refusal):
    if isinstance(refusal, dict):
        if isinstance(refusal.get("code"), str):
            return refusal["code"]
        err = refusal.get("error")
        if isinstance(err, dict) and isinstance(err.get("code"), str):
            return err["code"]
    return "refused"


with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    os.environ["AUDIT_PATH"] = os.path.abspath(SCRATCH_AUDIT)
    if GW:
        sys.path.insert(0, GW)
    if ROOT:
        sys.path.insert(0, ROOT)
    try:
        from app import client_adapter_orion as orion
        from app import harvest_read, identity_scope, typed_scope
        from lib import trading_calendar
        _IMPORT_ERROR = None
    except Exception as exc:  # the probe reports the failure as a False boolean, never a traceback
        _IMPORT_ERROR = type(exc).__name__


class _Standin:
    """An Opal stand-in principal: the address is constructed here and never printed."""

    def __init__(self):
        self.email = "opal-probe-standin@" + identity_scope.OPAL_USERS_DOMAIN
        self.tid = "probe"
        self.oid = "probe"


class ProbeCtx:
    """The protocol ctx for this probe (the core's real Ctx is OG-cl-1's, on no ref held here). Prefixes come from the
    DATA_CATALOG.yaml row whose key_template matches (vendor, segment, layer, table) and which is not retired; the
    bucket is that row's own bucket field. Reads go through the typed_scope seam, admitted (principal, served prefix)
    before any S3 call. Counts and booleans only leave this class."""

    def __init__(self):
        self.reads = []
        self.bucket = None
        self._catalog = None

    def _rows(self):
        if self._catalog is None:
            import yaml
            with io.open(os.path.join(GW, "app", "refs", "DATA_CATALOG.yaml"), encoding="ascii") as fh:
                self._catalog = yaml.safe_load(fh)
        return self._catalog

    def prefix(self, vendor, segment, layer, table):
        template = "%s/%s/%s/%s/" % (vendor, segment, layer, table)
        hits = []
        for section in self._rows().values():
            if not isinstance(section, list):
                continue
            for row in section:
                if isinstance(row, dict) and row.get("key_template") == template and not row.get("retired"):
                    hits.append(row)
        if len(hits) != 1 or not hits[0].get("bucket") or not hits[0].get("prefix"):
            raise orion.AdapterRefusal("no_catalog_row", "%d live catalog rows match the table" % len(hits))
        self.bucket = hits[0]["bucket"]
        return hits[0]["prefix"]

    def _scope(self, prefix):
        return typed_scope.Scope("assets", self.bucket, (prefix,), lambda: _s3())

    def _admit(self, prefix, ref):
        deny = typed_scope.admit_scope(self._scope(prefix), "client_probe", ref)
        if deny is not None:
            raise orion.AdapterRefusal(_code_of(deny))

    def list_partitions(self, prefix):
        self._admit(prefix, prefix)
        scope = self._scope(prefix)
        found = set()
        for o in typed_scope.list_keys(scope, prefix):
            m = re.match(r"date=(\d{4}-\d{2}-\d{2})/", o["key"][len(prefix):])
            if m:
                found.add(m.group(1))
        return sorted(found)

    def newest_partition(self, prefix, as_of=None):
        ps = [p for p in self.list_partitions(prefix) if as_of is None or p <= as_of]
        return ps[-1] if ps else None

    def read_rows(self, prefix, partition, columns=None, filters=None):
        self.reads.append((prefix, partition))
        part_prefix = prefix + "date=" + partition + "/"
        self._admit(prefix, part_prefix)
        scope = self._scope(prefix)
        rows = []
        for o in typed_scope.list_keys(scope, part_prefix):
            if o["key"].endswith(".parquet"):
                got, _total, _n = typed_scope.read_parquet(scope, o["key"], columns=columns)
                rows.extend(got)
        return rows

    def freshness_td(self, partition_date):
        import datetime as dt
        frontier = trading_calendar.prev_trading_day(dt.date.today())
        return trading_calendar.trading_days_behind(partition_date, frontier)

    def firm_segments(self, vendor, firm):
        return {("orion", "inflection"): ["inflection"], ("eclipse", "inflection"): ["inflection"]}.get((vendor, firm), [])


def _s3():
    import boto3
    return boto3.client("s3")


def _independent_count(bucket, key):
    import boto3
    import pyarrow.parquet as pq
    body = boto3.client("s3").get_object(Bucket=bucket, Key=key)["Body"].read()
    return pq.read_table(io.BytesIO(body)).num_rows


def _measure():
    """(envelope_ok, independent_count_equal, fence_negative_arm, reason) -- every value is a measured fact or False."""
    if _IMPORT_ERROR is not None:
        return False, False, False, "import:" + _IMPORT_ERROR
    harvest_read.get_current_principal = lambda: _Standin()
    ctx = ProbeCtx()
    try:
        prefix = ctx.prefix("orion", "inflection", "silver", "fact_positions")
        part = ctx.newest_partition(prefix)
        if part is None:
            return False, False, False, "no_partition"
        full = ctx.read_rows(prefix, part, columns=["accountNumber", "accountId"])
        if not full:
            return False, False, False, "empty_partition"
        probe_last4 = re.sub(r"\D", "", str(full[0]["accountNumber"]).split("_", 1)[0])[-4:]
        resolved = orion.resolve_account(ctx, "inflection", probe_last4, as_of=part)
        ref = resolved["candidates"][0]["account_ref"]
        held = orion.get_holdings(ctx, "inflection", ref, as_of=part)
        envelope_ok = all(k in held for k in ("_as_of", "_partition_date", "_source_keys", "_denominator")) \
            and held["_partition_date"] == part and len(held["_source_keys"]) == 1
        count_ok = held["_denominator"]["partition_rows"] == len(full) == _independent_rows(ctx, prefix, part)
        under_firm = bool(ctx.reads) and all(p.startswith("orion/inflection/") for p, _ in ctx.reads)
        reads_before = len(ctx.reads)
        other_refused = False
        try:
            orion.get_holdings(ctx, "49financial", ref, as_of=part)
        except Exception as exc:
            other_refused = getattr(exc, "code", "") == "firm_not_served"
        fence_ok = under_firm and other_refused and len(ctx.reads) == reads_before
        return envelope_ok, count_ok, fence_ok, "answered"
    except Exception as exc:
        _state["error"] = getattr(exc, "code", type(exc).__name__)
        return False, False, False, _state["error"]


def _independent_rows(ctx, prefix, part):
    """The same partition read with boto3 and pyarrow, as a row count (no value leaves this function)."""
    part_prefix = prefix + "date=" + part + "/"
    import boto3
    client = boto3.client("s3")
    total = 0
    resp = client.list_objects_v2(Bucket=ctx.bucket, Prefix=part_prefix)
    for o in resp.get("Contents", []):
        if o["Key"].endswith(".parquet"):
            total += _independent_count(ctx.bucket, o["Key"])
    return total


def main():
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        envelope_ok, count_ok, fence_ok, reason = _measure()
    line = "probe orion: envelope_ok %s; independent_count_equal %s; fence_negative_arm %s; account_numbers_printed %d" \
        % (bool(envelope_ok), bool(count_ok), bool(fence_ok), 0)
    print(line)
    if DIAG:
        print(reason, file=sys.stderr)


if __name__ == "__main__":
    main()
