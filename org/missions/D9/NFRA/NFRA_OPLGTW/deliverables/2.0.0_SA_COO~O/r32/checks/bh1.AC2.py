"""OPLGTW OG-bh-1 AC2 (Andrew-direct 2026-10-09 ~06:3xZ, FWD-13): 08403355's full history is served or named.

Denominator: every date in the census record's `served_dates` (re-read from SSM by AC1). For each date, live S3:
  - the completion record schwab/08403355/meta/complete/date=<D>.json QUALIFIES under the gateway's own record-level
    rules (catalog.membership_findings with no REJECTED class, catalog.validate_closure QUALIFIED), the contract read in
    memory with 08403355, its four served prefixes and its completion prefix added (as tm1.AC2.py does); or
  - the date is listed in the backfill record's `unavailable` with a non-empty reason.
PASS when no date is open, every date the backfill record lists under `backfilled` qualifies, and at least one was
backfilled.

  python bh1.AC2.py <census_record.json> <backfill_record.json> <repo_root>
"""
import json
import sys
from pathlib import Path

import boto3

BUCKET, NEW = "opal-data-assets", "08403355"
SERVED = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def main(argv):
    if len(argv) != 4:
        print(__doc__)
        return 2
    try:
        census = json.load(open(argv[1], encoding="utf-8"))
        rec = json.load(open(argv[2], encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("record unreadable (%s)" % type(exc).__name__)
        print("RESULT: FAIL")
        return 1
    root = Path(argv[3])
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
    served = sorted(census.get("served_dates") or [])
    unavailable = {d: r for d, r in (rec.get("unavailable") or {}).items() if isinstance(r, str) and r.strip()}
    backfilled = sorted(rec.get("backfilled") or [])
    classes = {}
    for d in sorted(set(served) | set(backfilled)):
        key = "schwab/%s/meta/complete/date=%s.json" % (NEW, d)
        try:
            marker = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
        except s3.exceptions.NoSuchKey:
            classes[d] = "ABSENT"
            continue
        closure = marker.get("closure") if isinstance(marker, dict) else None
        if not isinstance(closure, dict):
            classes[d] = "LEGACY"
            continue
        f = cat.membership_findings(marker, closure, NEW, d, contract)
        v = cat.validate_closure(closure, contract.masters)
        classes[d] = "QUALIFIED" if (not any(x["class"] in rejected for x in f)
                                     and v["status"] == cat.RESULT_QUALIFIED) else "NONQUALIFYING"
    open_dates = [d for d in served if classes.get(d) != "QUALIFIED" and d not in unavailable]
    not_now = [d for d in backfilled if classes.get(d) != "QUALIFIED"]
    print("%s: served dates %d (%s..%s); qualified %d; backfilled %d; unavailable named %d; open %d; "
          "backfilled-but-not-qualified %d" % (
              NEW, len(served), served[0] if served else None, served[-1] if served else None,
              sum(classes.get(d) == "QUALIFIED" for d in served), len(backfilled), len(unavailable), len(open_dates),
              len(not_now)))
    ok = True
    if not served:
        print("FAIL: census lists no served date")
        ok = False
    if open_dates or not_now:
        print("FAIL: open %s; backfilled but not qualified %s" % (open_dates[:10], not_now[:10]))
        ok = False
    if not backfilled:
        print("FAIL: no date was backfilled")
        ok = False
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
