"""Row W12-S2 relay (2.0.0_SA_COO~C2): list the two USABLE buckets the dell2 identity is denied, for CB4d1-AC3's completeness grade.

Run on the laptop (dell2 is fenced from both). Read-only: ListObjectsV2 with Delimiter='/' only, two levels deep, no Get or Head.
Bucket names are read from the round-4 census result committed at
org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~12/PRICE_CENSUS_20261007.json (the rows whose listing was denied),
never typed here.
Writes ONE file: org/missions/D8/ADVI/ADVI_COTBKF/deliverables/<--seat>/UNLISTED_USABLE_BUCKETS_<YYYYMMDD>.json, and prints its path.

    python org/missions/D8/ADVI/ADVI_COTBKF/deliverables/2.0.0_SA_COO~C2/list_unlisted_usable_buckets.py --seat 1.0.0_SA_CTO
"""
import argparse
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[7]
PROJECT = ROOT / "org/missions/D8/ADVI/ADVI_COTBKF"
CENSUS = PROJECT / "deliverables/0.9.0_WK_ADVI_COTBKF~12/PRICE_CENSUS_20261007.json"


def denied_buckets(census: dict) -> list:
    """Buckets graded USABLE whose listing failed in the census (list_status == 'list_failed')."""
    return sorted(r["name"] for r in census.get("buckets", [])
                  if isinstance(r, dict) and r.get("grade") == "USABLE" and r.get("list_status") == "list_failed")


def prefixes(s3, bucket: str, prefix: str = "") -> list:
    found, token = [], None
    while True:
        kw = {"Bucket": bucket, "Delimiter": "/", "Prefix": prefix, "MaxKeys": 1000}
        if token:
            kw["ContinuationToken"] = token
        page = s3.list_objects_v2(**kw)
        found += [p["Prefix"] for p in page.get("CommonPrefixes", [])]
        if not page.get("IsTruncated"):
            return found
        token = page["NextContinuationToken"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", required=True, help="the running seat's serial; names the deliverables folder")
    a = ap.parse_args()
    import boto3

    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    buckets = denied_buckets(census)
    s3 = boto3.client("s3")
    result = {"generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
              "row": "ADVI_COTBKF-W12-S2", "source": str(CENSUS.relative_to(ROOT)), "buckets": {}}
    for b in buckets:
        try:
            top = prefixes(s3, b)
            result["buckets"][b] = {"top": top, "second": {p: prefixes(s3, b, p) for p in top}}
        except Exception as exc:  # noqa: BLE001 -- the failure is the result for this bucket
            result["buckets"][b] = {"error": "%s: %s" % (type(exc).__name__, exc)}
    out = PROJECT / "deliverables" / a.seat / ("UNLISTED_USABLE_BUCKETS_%s.json" % datetime.date.today().strftime("%Y%m%d"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("UNLISTED-USABLE buckets=%d written=%s" % (len(buckets), out.relative_to(ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
