"""IRPT_DASHBD round 1 AC (DB-b-1, FWD-9 / FWD-1 hop 1) -- the 49 Financial adapter's gold exists UNDER ITS CONTRACT.

Usage: python p1_1_ac1_gold_under_contract.py <worktree root>
Reads, at the worktree root:
  org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json   (columns: list of {name, type, nullable}; enums; rule24_record;
                                                                   schema_hash = sha256 over "name:type" sorted, joined by "\n")
  org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json       (columns incl. tolerance, large_flow_share, plausibility_band,
                                                                   flow_convention, income_basis, fee_basis, day_count)
  lib.opal_naming must load and validate the registry. (Issuer amendment 2, 2026-09-30: the gold policy-file half is removed --
  PRD v0.3 ruling 16, CTO 103361: gold tables need no reporting-policy row.)
Then, on S3 through lib.opal_naming.address() (never a typed key):
  gold account_return_daily: the FIRST, the LAST and three evenly spaced date partitions among those present must each carry
      the thread account (THREAD_ACCOUNT.json), every contract column with the contract's arrow type name, and a schema hash equal to the
      contract's; the partition count must be >= 250 (the sample's history is 2024-07-09 .. the frontier);
  gold dim_return_method/method_version=1: one row with every method-contract column non-null.
Pass line: DB-1-AC1 PASS. Base (at the cut): FAIL -- no contract file exists.
"""
import hashlib
import io
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(root))


def _thread_account(root):
    """The thread account: the seat's record deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json ({"thread_account": "..."}),
    chosen by census in DB-b-1 (issuer amendment 1, 2026-09-30 17:1xZ); the roster's first account is the fallback."""
    import json as _json
    p = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.4.0_DS_ClientPlatform~S/THREAD_ACCOUNT.json"
    try:
        return str(_json.loads(p.read_text(encoding="utf-8"))["thread_account"])
    except Exception:  # noqa: BLE001
        return "0027265115"
THREAD = _thread_account(root)


def fail(msg):
    print("DB-1-AC1 FAIL: " + msg)
    sys.exit(1)


def contract(path):
    p = root / path
    if not p.exists():
        fail("contract absent: %s" % path)
    d = json.loads(p.read_text(encoding="utf-8"))
    cols = d.get("columns")
    if not isinstance(cols, list) or not cols:
        fail("%s has no columns list" % path)
    for c in cols:
        if not all(k in c for k in ("name", "type", "nullable")):
            fail("%s column lacks name/type/nullable: %r" % (path, c))
    want = hashlib.sha256("\n".join(sorted("%s:%s" % (c["name"], c["type"]) for c in cols)).encode()).hexdigest()
    if d.get("schema_hash") != want:
        fail("%s schema_hash %r != computed %s" % (path, d.get("schema_hash"), want[:16]))
    return d


ard = contract("org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json")
if "rule24_record" not in ard:
    fail("account_return_daily contract carries no rule24_record (ADDENDUM ruling 12)")
for enum in ("history_scope", "day_quality", "return_basis"):
    if enum not in ard.get("enums", {}):
        fail("account_return_daily contract lacks enum %s" % enum)
drm = contract("org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json")
need_method = {"method_version", "tolerance", "large_flow_share", "plausibility_band_low", "plausibility_band_high",
               "flow_convention", "income_basis", "fee_basis", "day_count"}
have_method = {c["name"] for c in drm["columns"]}
if not need_method <= have_method:
    fail("dim_return_method contract lacks columns %s" % sorted(need_method - have_method))

try:
    from lib import opal_naming as on
    on.load_registry()
except Exception as exc:  # noqa: BLE001
    fail("lib.opal_naming refuses the registry after the edit: %s" % str(exc)[:200])

import boto3  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

s3 = boto3.client("s3", region_name="us-east-1")


def split(uri):
    b, k = uri[5:].split("/", 1)
    return b, k


table_uri = on.address("irpt", "49financial", "gold", "account_return_daily", "date=2000-01-01")
bucket, key0 = split(table_uri)
prefix = key0.rsplit("date=2000-01-01", 1)[0]
pag = s3.get_paginator("list_objects_v2")
dates = sorted({k.split("date=")[1][:10] for page in pag.paginate(Bucket=bucket, Prefix=prefix)
                for k in [o["Key"] for o in page.get("Contents", [])] if "date=" in k})
print("  partitions under %s: %d" % (prefix, len(dates)))
if len(dates) < 250:
    fail("only %d date partitions (need >= 250)" % len(dates))
picks = [dates[0], dates[len(dates) // 4], dates[len(dates) // 2], dates[3 * len(dates) // 4], dates[-1]]
want_hash = ard["schema_hash"]
for d in picks:
    b, k = split(on.address("irpt", "49financial", "gold", "account_return_daily", "date=%s" % d) + "/data.parquet")
    try:
        body = s3.get_object(Bucket=b, Key=k)["Body"].read()
    except Exception as exc:  # noqa: BLE001
        fail("GetObject %s: %s" % (k, str(exc)[:120]))
    t = pq.read_table(io.BytesIO(body))
    got = hashlib.sha256("\n".join(sorted("%s:%s" % (f.name, f.type) for f in t.schema)).encode()).hexdigest()
    if got != want_hash:
        fail("date=%s schema hash %s != contract %s (columns %s)" % (d, got[:12], want_hash[:12], t.column_names))
    if THREAD not in set(str(x) for x in t.column("account_id").to_pylist()):
        fail("date=%s carries no row for the thread account %s" % (d, THREAD))
    print("  date=%s OK: %d rows, schema hash matches, thread account present" % (d, t.num_rows))

b, k = split(on.address("irpt", "49financial", "gold", "dim_return_method", "method_version=1") + "/data.parquet")
try:
    body = s3.get_object(Bucket=b, Key=k)["Body"].read()
except Exception as exc:  # noqa: BLE001
    fail("dim_return_method/method_version=1 absent: %s" % str(exc)[:120])
m = pq.read_table(io.BytesIO(body)).to_pylist()
if len(m) != 1:
    fail("dim_return_method/method_version=1 has %d rows (want 1)" % len(m))
nulls = [c for c in need_method if m[0].get(c) is None]
if nulls:
    fail("dim_return_method row has null %s" % nulls)
print("  dim_return_method v1: tolerance=%s large_flow_share=%s band=[%s,%s] flow_convention=%s" % (
    m[0]["tolerance"], m[0]["large_flow_share"], m[0]["plausibility_band_low"], m[0]["plausibility_band_high"], m[0]["flow_convention"]))
print("DB-1-AC1 PASS")
