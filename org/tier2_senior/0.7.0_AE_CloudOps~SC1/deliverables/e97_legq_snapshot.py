"""Leg Q snapshot + compare (MDPF_SECCLASS TO-SC-e97b, 0.7.0_AE_CloudOps~SC1).

  python -I e97_legq_snapshot.py snap <out.json>      BEFORE/AFTER key lists with ETag + VersionId (latest versions)
  python -I e97_legq_snapshot.py cmp <before> <after>  DELTA verdict: same key set, every ETag equal
Key set is defined by the 06:19Z BEFORE file's groups: two prefix groups, the rest single keys.
Read-only. Pagination is counted client side (pages printed).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

import boto3

B49 = "opal-data-49financial"
BBD = "opal-data-bd"
P49 = "advi/49financial/platinum/"
GROUPS = [
    ("gold/entities/clients/", B49, P49 + "entities/clients/", True),
    ("gold/client_timeseries/", BBD, "gold/client_timeseries/", True),
    ("gold/artifacts/firm_mix_views.json", B49, P49 + "artifacts/firm_mix_views.json", False),
    ("gold/artifacts/firm_mix_views_daily.json", B49, P49 + "artifacts/firm_mix_views_daily.json", False),
    ("gold/views/mix_daily_summary.json", B49, P49 + "views/mix_daily_summary.json", False),
    ("platinum/firm/mix_summary.json", B49, P49 + "firm/mix_summary.json", False),
    ("gold/meta/client_timeseries_watermark.json", BBD, "gold/meta/client_timeseries_watermark.json", False),
]


def snap(out: str) -> None:
    s3 = boto3.client("s3")
    keys: dict = {}
    groups: dict = {}
    for name, bucket, prefix, is_prefix in GROUPS:
        pages = 0
        n = 0
        for page in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=prefix):
            pages += 1
            for v in page.get("Versions", []):
                if not v["IsLatest"]:
                    continue
                if not is_prefix and v["Key"] != prefix:
                    continue
                keys[f"{bucket}/{v['Key']}"] = {
                    "ETag": v["ETag"].strip('"'),
                    "LastModified": v["LastModified"].isoformat(),
                    "Size": v["Size"],
                    "VersionId": v["VersionId"],
                }
                n += 1
        groups[name] = {"bucket": bucket, "prefix": prefix, "keys": n, "pages": pages}
    doc = {
        "taken_utc": datetime.now(timezone.utc).isoformat(),
        "groups": groups,
        "total_keys": len(keys),
        "keys_with_no_versionid": sum(1 for v in keys.values() if v["VersionId"] in (None, "null")),
        "keys": keys,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
    print(f"snap {out}: total_keys={len(keys)} taken={doc['taken_utc']}")
    for g, v in groups.items():
        print(f"  {g}: keys={v['keys']} pages={v['pages']}")


def cmp(b: str, a: str) -> int:
    B = json.load(open(b, encoding="utf-8"))["keys"]
    A = json.load(open(a, encoding="utf-8"))["keys"]
    only_b = sorted(set(B) - set(A))
    only_a = sorted(set(A) - set(B))
    both = sorted(set(A) & set(B))
    etag_diff = [k for k in both if A[k]["ETag"] != B[k]["ETag"]]
    ver_only = [k for k in both if A[k]["ETag"] == B[k]["ETag"] and A[k]["VersionId"] != B[k]["VersionId"]]
    print(f"before={len(B)} after={len(A)} common={len(both)} only_before={len(only_b)} only_after={len(only_a)}")
    print(f"ETAG_DIFFERS={len(etag_diff)}  NEW_VERSION_EQUAL_ETAG={len(ver_only)}")
    for k in only_b[:20]:
        print("  ONLY-BEFORE", k)
    for k in only_a[:20]:
        print("  ONLY-AFTER", k)
    for k in etag_diff[:50]:
        print("  ETAG-DIFF", k, B[k]["VersionId"], "->", A[k]["VersionId"])
    for k in ver_only[:50]:
        print("  NEWVER-SAME-ETAG", k, B[k]["VersionId"], "->", A[k]["VersionId"])
    ok = not only_b and not only_a and not etag_diff
    print("DELTA=0 (same key set, every ETag equal)" if ok else "DELTA!=0")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "snap":
        snap(sys.argv[2])
    else:
        sys.exit(cmp(sys.argv[2], sys.argv[3]))
