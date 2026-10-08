"""OPLGTW OG-tm-1 AC2 (PRD v2.0 item 5(c), acceptance A24): one 08403355 day landed, converted and qualified.

  - at least one raw .zip under s3://opal-data-assets/schwab/08403355/bronze/;
  - at least one completion record schwab/08403355/meta/complete/date=<D>.json that QUALIFIES under the gateway's own
    record-level rules (catalog.membership_findings with no REJECTED class, catalog.validate_closure QUALIFIED), the
    contract read in memory with 08403355 and its four served prefixes and completion prefix added;
  - every served-dataset object that record names (catalog.head_set) exists at the exact VersionId it names.

  python tm1.AC2.py <repo_root>
"""
import json
import re
import sys
from pathlib import Path

import boto3

BUCKET, NEW = "opal-data-assets", "08403355"
SERVED = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def main(argv):
    root = Path(argv[1])
    sys.path.insert(0, str(root / "infra/aws/ec2/opal-gateway"))
    from app.integrations.schwab import catalog as cat
    raw = json.loads((root / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8"))
    raw["masters"] = dict(raw["masters"], **{NEW: raw["masters"].get(NEW, "TaxSMA")})
    for ds in SERVED:
        p = "schwab/%s/silver/%s/" % (NEW, ds)
        if p not in raw["data_prefixes"]:
            raw["data_prefixes"].append(p)
    if "schwab/%s/meta/complete/" % NEW not in raw["completion_prefixes"]:
        raw["completion_prefixes"].append("schwab/%s/meta/complete/" % NEW)
    contract = cat.parse_contract(raw)
    rejected = {cat.F_REJECTED_BUCKET, cat.F_REJECTED_MASTER, cat.F_REJECTED_DATASET, cat.F_REJECTED_DATE,
                cat.F_REJECTED_KEY}
    s3 = boto3.client("s3", region_name="us-east-1")
    zips = s3.list_objects_v2(Bucket=BUCKET, Prefix="schwab/%s/bronze/" % NEW, MaxKeys=1000).get("Contents") or []
    nzip = sum(1 for o in zips if o["Key"].endswith(".zip"))
    print("bronze .zip objects (first page): %d" % nzip)
    prefix = "schwab/%s/meta/complete/" % NEW
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix).get("Contents") or []]
    qualified = []
    for key in keys:
        m = re.match(re.escape(prefix) + r"date=(\d{4}-\d{2}-\d{2})\.json$", key)
        if not m:
            continue
        marker = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
        closure = marker.get("closure") if isinstance(marker, dict) else None
        if not isinstance(closure, dict):
            print("%s: LEGACY (no closure)" % m.group(1))
            continue
        f = cat.membership_findings(marker, closure, NEW, m.group(1), contract)
        v = cat.validate_closure(closure, contract.masters)
        good = not any(x["class"] in rejected for x in f) and v["status"] == cat.RESULT_QUALIFIED
        heads_ok, named = True, cat.head_set(closure, contract)   # the gateway's own HEAD set (served datasets)
        for ref in named:
            try:
                s3.head_object(Bucket=BUCKET, Key=ref["key"], VersionId=ref["version_id"] or "")
            except Exception:
                heads_ok = False
        print("%s: %s; named objects %d, all HEAD at their VersionId: %s"
              % (m.group(1), "QUALIFIED" if good else "NONQUALIFYING", len(named), heads_ok))
        if good and heads_ok and named:
            qualified.append(m.group(1))
    print("completion records %d; qualified with every object present %d" % (len(keys), len(qualified)))
    ok = nzip > 0 and len(qualified) > 0
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
