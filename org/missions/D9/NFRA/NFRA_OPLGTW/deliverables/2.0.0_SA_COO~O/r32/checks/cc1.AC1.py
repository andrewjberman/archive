"""OPLGTW OG-cc-1 AC1 (round 32 item 5, with item 4's marker clause; PRD v2.0 item 4): the 13-month closure census.

Recomputes, per master, from live S3 and the gateway's own record-level qualification, and compares with the worker's
record:
  - every completion record under schwab/<m>/meta/complete/date=<D>.json, classed QUALIFIED (catalog.membership_findings
    empty of REJECTED classes and catalog.validate_closure QUALIFIED), LEGACY (no `closure` object), or NONQUALIFYING;
    object heads are NOT re-checked (record-level qualification, stated in the record);
  - oldest and newest QUALIFIED date overall;
  - the window: the newest QUALIFIED date back to the same calendar day 13 months earlier, month-end clamped;
  - silver dates in the window: the union of `date=<D>/` partitions of the four served datasets;
  - missing: the silver dates in the window with no QUALIFIED record, as an exact sorted list.

  python cc1.AC1.py <record.json> <repo_root>
"""
import calendar
import datetime as dt
import json
import re
import sys
from pathlib import Path

import boto3

BUCKET = "opal-data-assets"
MASTERS = ("08242234", "08335338")
SERVED = ("dim_position", "dim_balance", "dim_asset", "dim_transaction")


def months_back(d, n):
    y, m = d.year, d.month - n
    while m <= 0:
        m += 12
        y -= 1
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def list_all(s3, prefix, delimiter=None):
    out, token = [], None
    while True:
        args = {"Bucket": BUCKET, "Prefix": prefix}
        if delimiter:
            args["Delimiter"] = delimiter
        if token:
            args["ContinuationToken"] = token
        page = s3.list_objects_v2(**args)
        out += [cp["Prefix"] for cp in page.get("CommonPrefixes") or []] if delimiter else \
            [o["Key"] for o in page.get("Contents") or []]
        token = page.get("NextContinuationToken") if page.get("IsTruncated") else None
        if not token:
            return out


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        rec = json.load(open(argv[1], encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("record unreadable: %s (%s)" % (argv[1], type(exc).__name__))
        print("RESULT: FAIL")
        return 1
    root = Path(argv[2])
    sys.path.insert(0, str(root / "infra/aws/ec2/opal-gateway"))
    from app.integrations.schwab import catalog as cat
    contract = cat.parse_contract(json.loads((root / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8")))
    rejected = {cat.F_REJECTED_BUCKET, cat.F_REJECTED_MASTER, cat.F_REJECTED_DATASET, cat.F_REJECTED_DATE,
                cat.F_REJECTED_KEY}
    s3 = boto3.client("s3", region_name="us-east-1")
    ok = True
    for m in MASTERS:
        got = (rec.get("masters") or {}).get(m)
        prefix = "schwab/%s/meta/complete/" % m
        classes = {}
        for key in list_all(s3, prefix):
            mm = re.match(re.escape(prefix) + r"date=(\d{4}-\d{2}-\d{2})\.json$", key)
            if not mm:
                continue
            d = mm.group(1)
            marker = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
            closure = marker.get("closure") if isinstance(marker, dict) else None
            if not isinstance(closure, dict):
                classes[d] = "LEGACY"
                continue
            f = cat.membership_findings(marker, closure, m, d, contract)
            v = cat.validate_closure(closure, contract.masters)
            classes[d] = "QUALIFIED" if (not any(x["class"] in rejected for x in f)
                                         and v["status"] == cat.RESULT_QUALIFIED) else "NONQUALIFYING"
        qual = sorted(d for d, c in classes.items() if c == "QUALIFIED")
        if not qual:
            print("FAIL: %s: no QUALIFIED completion record at all (%d records)" % (m, len(classes)))
            ok = False
            continue
        end = dt.date.fromisoformat(qual[-1])
        start = months_back(end, 13)
        by_ds, silver = {}, set()
        for ds in SERVED:
            p = "schwab/%s/silver/%s/" % (m, ds)
            ds_dates = {re.match(re.escape(p) + r"date=(\d{4}-\d{2}-\d{2})/$", cp).group(1)
                        for cp in list_all(s3, p, "/") if re.match(re.escape(p) + r"date=\d{4}-\d{2}-\d{2}/$", cp)}
            ds_dates = {d for d in ds_dates if start.isoformat() <= d <= end.isoformat()}
            by_ds[ds] = len(ds_dates)
            silver |= ds_dates
        missing = sorted(d for d in silver if classes.get(d) != "QUALIFIED")
        in_win = {d: c for d, c in classes.items() if start.isoformat() <= d <= end.isoformat()}
        mine = {
            "window": {"from": start.isoformat(), "to": end.isoformat()},
            "silver_dates": len(silver),
            "silver_dates_by_dataset": by_ds,
            "markers_total": len(classes),
            "markers_in_window": {"qualified": sum(c == "QUALIFIED" for c in in_win.values()),
                                  "legacy": sum(c == "LEGACY" for c in in_win.values()),
                                  "nonqualifying": sum(c == "NONQUALIFYING" for c in in_win.values())},
            "oldest_qualified": qual[0],
            "newest_qualified": qual[-1],
            "missing_count": len(missing),
            "missing": missing,
        }
        print("%s: window %s..%s; silver dates %d %s; records %d (in window %s); qualified %s..%s; missing %d"
              % (m, mine["window"]["from"], mine["window"]["to"], mine["silver_dates"], by_ds, mine["markers_total"],
                 mine["markers_in_window"], mine["oldest_qualified"], mine["newest_qualified"], len(missing)))
        if not isinstance(got, dict):
            print("FAIL: %s: absent from the record" % m)
            ok = False
            continue
        diff = [k for k in mine if got.get(k) != mine[k]]
        if diff:
            print("FAIL: %s: the record differs on %s" % (m, diff))
            ok = False
    if "object heads" not in str(rec.get("qualification", "")):
        print("FAIL: the record does not state that object heads are not re-checked ('qualification')")
        ok = False
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
