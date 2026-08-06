"""MDPF_CANRTE P0-1 addendum -- the 14-pair SCHEMA BASELINE. READ-ONLY.

WHY THIS EXISTS (CTO~Z G4, relayed by COO~Z): doc 04 requires that platinum PRESERVE each
artifact's schema contract across the cutover, and doc 04 s.4's capture list records
VersionIds and manifests but NOT SCHEMAS. So the constraint's verification input is never
captured -- a constraint that cannot be checked is not a constraint. This captures the
observed field set and types so the post-cutover comparison has a before-image.

It is a BASELINE, not a spec. H6 says explicitly: do NOT "clean up" the schema
inconsistencies this will surface (as_of_date vs as_of_first/as_of_last, firm_id present,
scope=null). Recording them is the point; normalising them is out of scope and forbidden.

Timestamps via s3api/boto3 true UTC. Never an `aws s3 ls` column.
"""
from __future__ import annotations

import datetime as dt
import gzip
import json
import sys
from zoneinfo import ZoneInfo

import boto3
from botocore.exceptions import ClientError

UTC = ZoneInfo("UTC")
s3 = boto3.client("s3")

TARGETS = [
    ("platinum_served", "opal-data-portal-v2", "platinum/mdpf/"),
    ("json_bell",       "opal-data-portal-v2", "json/mdpf/"),
    ("gold_canonical",  "opal-data-assets",    "portal/gold/mdpf/"),
    ("aggregate_aua",   "opal-data-assets",    "gold/mdpf_revamp/_aggregate_aua/"),
]
DATED_TAIL = 15  # "YYYY-MM-DD.json"


def is_dated(key: str) -> bool:
    t = key.rsplit("/", 1)[-1]
    return len(t) == DATED_TAIL and t[4] == "-" and t[7] == "-" and t.endswith(".json")


def type_of(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        if not v:
            return "list[empty]"
        inner = sorted({type_of(x) for x in v[:25]})
        return f"list[{'|'.join(inner)}]"
    if isinstance(v, dict):
        return "object"
    return type(v).__name__


def shape(obj, prefix="", depth=0, max_depth=2, out=None):
    """Field-path -> observed type. Bounded depth; dict-of-dicts sampled, not exploded."""
    if out is None:
        out = {}
    if depth > max_depth:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else k
            out[path] = type_of(v)
            if isinstance(v, dict):
                # a date-keyed or id-keyed map explodes; sample ONE representative child
                keys = list(v.keys())
                if keys and all(_looks_like_key(x) for x in keys[:5]):
                    out[f"{path}.<key>"] = f"map[{len(keys)} entries]"
                    shape(v[keys[0]], f"{path}.<*>", depth + 1, max_depth, out)
                else:
                    shape(v, path, depth + 1, max_depth, out)
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                shape(v[0], f"{path}[0]", depth + 1, max_depth, out)
    return out


def _looks_like_key(k) -> bool:
    k = str(k)
    return (len(k) == 10 and k[4] == "-" and k[7] == "-") or k.isdigit() or len(k) > 12


def read_json(bucket, key):
    o = s3.get_object(Bucket=bucket, Key=key)
    raw = o["Body"].read()
    if key.endswith(".gz") or raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8")), o


def main():
    now = dt.datetime.now(UTC)
    art = {
        "artifact": "MDPF_CANRTE_P0-1_schema_baseline",
        "purpose": ("before-image of every served artifact's field set + types, so doc 04's "
                    "'platinum preserves each artifact's schema contract' has a verification "
                    "input. It had none."),
        "captured_at_utc": now.isoformat(),
        "captured_by": "0.7.0_AE_CloudOps~Z",
        "h6_warning": ("H6: do NOT normalise what this surfaces. Inconsistencies "
                       "(as_of_date vs as_of_first/as_of_last, firm_id, scope=null) are "
                       "RECORDED here, not fixed. Schema migration is out of scope."),
        "surfaces": {},
        "errors": [],
    }

    for label, bucket, prefix in TARGETS:
        keys, pages = [], 0
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
            pages += 1
            keys.extend(k["Key"] for k in page.get("Contents", []))
        undated = [k for k in keys if not is_dated(k)]
        dated = sorted(k for k in keys if is_dated(k))
        sample = undated + (dated[-1:] if dated else [])
        entry = {
            "bucket": bucket, "prefix": prefix,
            "denominator": (f"{len(keys)} objects across {pages} pages; "
                            f"{len(undated)} undated; {len(dated)} dated; "
                            f"schema sampled from {len(sample)} "
                            f"({len(undated)} undated + newest dated)"),
            "objects": {},
        }
        for key in sample:
            try:
                body, meta = read_json(bucket, key)
            except ClientError as e:
                entry["objects"][key] = {"ERROR": f"{type(e).__name__}: {str(e)[:160]}"}
                art["errors"].append({"key": f"{bucket}/{key}", "error": str(e)[:160]})
                continue
            except Exception as e:
                entry["objects"][key] = {"ERROR": f"{type(e).__name__}: {str(e)[:160]}",
                                         "note": "non-JSON or decode failure -- recorded, not skipped"}
                art["errors"].append({"key": f"{bucket}/{key}", "error": str(e)[:160]})
                continue
            fields = shape(body)
            asof = {k: v for k, v in fields.items()
                    if any(t in k.lower() for t in ("as_of", "asof", "date", "generated", "written"))}
            entry["objects"][key] = {
                "LastModified": meta["LastModified"].astimezone(UTC).isoformat(),
                "VersionId": meta.get("VersionId", "null"),
                "ETag": meta["ETag"].strip('"'),
                "ContentLength": meta["ContentLength"],
                "top_level_keys": sorted(body.keys()) if isinstance(body, dict) else f"<{type_of(body)}>",
                "field_count": len(fields),
                "as_of_family": asof,
                "schema": fields,
            }
        art["surfaces"][label] = entry

    path = sys.argv[1] if len(sys.argv) > 1 else "schema_baseline.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(art, f, indent=2)
    print(f"WROTE {path}\n")

    # ---- the H6 question, answered from the data rather than asserted ----
    print("SURFACE DENOMINATORS")
    for label, e in art["surfaces"].items():
        print(f"  {label:<18} {e['denominator']}")
    print("\nAS-OF FIELD FAMILY PER SERVED OBJECT  (H6: record, do not normalise)")
    fams = {}
    for label, e in art["surfaces"].items():
        for key, o in e["objects"].items():
            if "ERROR" in o:
                print(f"  ERROR {label}/{key}: {o['ERROR'][:80]}")
                continue
            names = tuple(sorted(k for k in o["as_of_family"] if "." not in k))
            fams.setdefault(names, []).append(f"{label}:{key.rsplit('/',2)[-2]}/{key.rsplit('/',1)[-1]}")
    for names, members in sorted(fams.items(), key=lambda x: -len(x[1])):
        print(f"\n  FAMILY {names if names else '(no top-level as-of/date field)'}  -- {len(members)} objects")
        for m in members[:8]:
            print(f"      {m}")
        if len(members) > 8:
            print(f"      ... +{len(members)-8} more")
    print(f"\nDISTINCT AS-OF FAMILIES: {len(fams)}  "
          f"(>1 means the served surface is NOT schema-uniform -- H6 says record it, not fix it)")
    print(f"ERRORS: {len(art['errors'])}")


if __name__ == "__main__":
    main()
