"""OPLGTW OG-ga-1 -- the grant state instrument (round 22). One instrument for the before-record and the grade.

  python ga1_state.py --before <out.json>   read-only: write the before-record (counts, hashes, operations; no identity)
  python ga1_state.py --grade <before.json>  read-only: grade the live store against that before-record

The grant IN FORCE for a principal is the data_entitlement record at its principal_profile's grant_revision.
Read: a strongly consistent, fully paginated scan of gateway-access-state-table, POLICY#<tid>#<oid> partitions only.
Never prints a tid, oid, email or account id: identities are reduced to sha256 digests inside this process.
"""
from __future__ import annotations

import hashlib
import json
import sys
from decimal import Decimal

TABLE = "gateway-access-state-table"
REQUIRED_OPS_AFTER = "download_filtered"


def _plain(v):
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() else str(v)
    if isinstance(v, dict):
        return {k: _plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set)):
        return [_plain(x) for x in v]
    return v


def _h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _scan():
    import boto3
    from boto3.dynamodb.types import TypeDeserializer
    des = TypeDeserializer()
    c = boto3.client("dynamodb", region_name="us-east-1")
    items, kw, pages = [], {"TableName": TABLE, "ConsistentRead": True}, 0
    while True:
        r = c.scan(**kw)
        pages += 1
        items += [{k: _plain(des.deserialize(v)) for k, v in it.items()} for it in r.get("Items", [])]
        if "LastEvaluatedKey" not in r:
            break
        kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    return items, pages


def _in_force():
    items, pages = _scan()
    by_pk = {}
    for it in items:
        pk, sk = str(it.get("pk", "")), str(it.get("sk", ""))
        parts = pk.split("#")
        if len(parts) != 3 or parts[0] != "POLICY" or parts[1] in ("EMAILDENY", "TENANT"):
            continue
        by_pk.setdefault(pk, {})[sk] = it
    rows = []
    for pk, recs in sorted(by_pk.items()):
        prof = recs.get("principal_profile")
        if not prof or prof.get("status") != "active" or prof.get("grant_revision") is None:
            continue
        g = recs.get("data_entitlement#%010d" % int(prof["grant_revision"]))
        if not g:
            rows.append({"who": _h(pk), "grant": None})
            continue
        scope = g.get("scope") or {}
        rows.append({"who": _h(pk), "grant_status": g.get("status"), "revision": int(g.get("revision", -1)),
                     "names_dim_asset": "dim_asset" in (scope.get("datasets") or []),
                     "operations": sorted(scope.get("operations") or []),
                     "scope_minus_ops": _h({k: v for k, v in scope.items() if k != "operations"}),
                     "whole_scope": _h(scope)})
    return rows, len(items), pages


def main(argv):
    if len(argv) != 3 or argv[1] not in ("--before", "--grade"):
        print(__doc__)
        return 2
    try:
        rows, n, pages = _in_force()
    except Exception as exc:  # an absent reader is a FAIL, never a zero
        print("instrument failure: %s: %s" % (type(exc).__name__, exc))
        print("RESULT: FAIL")
        return 1
    holders = [r for r in rows if r.get("grant_status") == "active" and r.get("names_dim_asset")]
    with_dl = [r for r in holders if REQUIRED_OPS_AFTER in r["operations"]]
    print("items scanned %d (pages %d, consistent); active profiles %d; in-force active dim_asset grants %d; "
          "of them carrying download_filtered %d" % (n, pages, len(rows), len(holders), len(with_dl)))
    if argv[1] == "--before":
        if len(holders) != 1:
            print("STOP: want exactly 1 in-force dim_asset holder, read %d" % len(holders))
            return 1
        h = holders[0]
        rec = {"holder": h["who"], "revision_before": h["revision"], "operations_before": h["operations"],
               "scope_minus_ops_before": h["scope_minus_ops"],
               "others_before": _h(sorted((r["who"], r.get("whole_scope"), r.get("grant_status")) for r in rows
                                          if r["who"] != h["who"])),
               "others_count": len(rows) - 1}
        with open(argv[2], "w", encoding="utf-8", newline="\n") as f:
            json.dump(rec, f, indent=1, sort_keys=True)
        print("before-record written: revision %d, operations %s, others %d" % (h["revision"], h["operations"],
                                                                                rec["others_count"]))
        return 0
    try:
        with open(argv[2], encoding="utf-8") as f:
            b = json.load(f)
    except Exception as exc:
        print("before-record unreadable: %s" % exc)
        print("RESULT: FAIL")
        return 1
    h = next((r for r in holders if r["who"] == b["holder"]), None)
    others = _h(sorted((r["who"], r.get("whole_scope"), r.get("grant_status")) for r in rows if r["who"] != b["holder"]))
    want_ops = sorted(set(b["operations_before"]) | {REQUIRED_OPS_AFTER})
    ok_rev = bool(h) and h["revision"] > b["revision_before"]
    ok_ops = bool(h) and h["operations"] == want_ops
    ok_rest = bool(h) and h["scope_minus_ops"] == b["scope_minus_ops_before"]
    ok_oth = others == b["others_before"]
    print("holder in force: %s; revision advanced %s; operations %s (want %s); other dimensions unchanged %s; "
          "other principals unchanged %s" % ("yes" if h else "no", ok_rev, h["operations"] if h else None, want_ops,
                                             ok_rest, ok_oth))
    if len(holders) == 1 and len(with_dl) == 1 and ok_rev and ok_ops and ok_rest and ok_oth:
        print("RESULT: PASS")
        return 0
    print("RESULT: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
