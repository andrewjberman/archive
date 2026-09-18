"""NFRA_OPLGTW OG-i-5 -- shared helpers for the access-state table rename probe (og_i5.py).

Digest-only evidence: no item content (pk/sk value or attribute payload) is ever written to a file.
Only sha256 digests of a canonical attribute map, and counts, leave the table (order BOUNDS).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from decimal import Decimal
from pathlib import Path

import boto3
from boto3.dynamodb.types import TypeDeserializer

REGION = "us-east-1"
OLD_TABLE = "opal-gateway-access-state"
NEW_TABLE = "gateway-access-state-table"

_DESER = TypeDeserializer()


def _canon(value):
    """Canonicalize a deserialized DynamoDB value for stable digesting."""
    if isinstance(value, Decimal):
        # canonical decimal text, no trailing zeros ambiguity
        return "D:" + format(value.normalize(), "f") if value == value.to_integral_value() else "D:" + str(value)
    if isinstance(value, (bytes, bytearray)):
        return "B:" + value.hex()
    if isinstance(value, set):
        return sorted(_canon(v) for v in value)
    if isinstance(value, dict):
        return {k: _canon(value[k]) for k in sorted(value.keys())}
    if isinstance(value, list):
        return [_canon(v) for v in value]
    return value


def item_digest(raw_item: dict) -> str:
    """sha256 of the canonical attribute map for one low-level DynamoDB item (excluding pk/sk keys
    themselves, which are compared separately as the identity, not digested as payload -- but included
    here for a whole-item digest since pk/sk are stable and their presence is part of item identity)."""
    deser = {k: _DESER.deserialize(v) for k, v in raw_item.items()}
    canon = _canon(deser)
    blob = json.dumps(canon, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def namespace_of(pk: str) -> str:
    if pk.startswith("RUNTIME#"):
        return "RUNTIME#"
    if pk.startswith("POLICY#"):
        return "POLICY#"
    return "OTHER#"


def scan_table_digest(table_name: str, region: str = REGION) -> dict:
    """Consistent full scan. Returns counts by namespace (RUNTIME#, POLICY#, operator_audit, OTHER#)
    and a map of (pk,sk) -> sha256 digest. No raw content returned."""
    ddb = boto3.client("dynamodb", region_name=region)
    digests = {}
    counts = {"RUNTIME#": 0, "POLICY#": 0, "operator_audit": 0, "OTHER#": 0}
    scanned = 0
    kwargs = {"TableName": table_name, "ConsistentRead": True}
    while True:
        resp = ddb.scan(**kwargs)
        for raw in resp.get("Items", []):
            pk = raw["pk"]["S"]
            sk = raw["sk"]["S"]
            scanned += 1
            ns = namespace_of(pk)
            counts[ns] += 1
            rtype = raw.get("record_type", {}).get("S")
            if rtype == "operator_audit":
                counts["operator_audit"] += 1
            digests[f"{pk}␟{sk}"] = item_digest(raw)
        if "LastEvaluatedKey" not in resp:
            break
        kwargs["ExclusiveStartKey"] = resp["LastEvaluatedKey"]
    return {
        "table": table_name,
        "region": region,
        "taken_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "item_count": scanned,
        "counts_by_namespace": counts,
        "digests": digests,
    }


def describe_table(table_name: str, region: str = REGION) -> dict:
    ddb = boto3.client("dynamodb", region_name=region)
    return ddb.describe_table(TableName=table_name)["Table"]


def table_exists(table_name: str, region: str = REGION) -> bool:
    ddb = boto3.client("dynamodb", region_name=region)
    try:
        ddb.describe_table(TableName=table_name)
        return True
    except ddb.exceptions.ResourceNotFoundException:
        return False


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run(cmd, timeout=90, **kw):
    print(f"+ {' '.join(cmd)}", file=sys.stderr)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)


def git_head(ws: Path) -> str:
    r = run(["git", "-C", str(ws), "rev-parse", "HEAD"])
    return r.stdout.strip()


def git_commit_time(ws: Path, ref: str) -> str:
    r = run(["git", "-C", str(ws), "show", "-s", "--format=%cI", ref])
    return r.stdout.strip()
