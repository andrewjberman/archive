"""OPLGTW OG-bf-1 AC1 (round 32 item 8, PRD v2.0 item 4 / C3, FWD-12): the 13-month closure gap is closed or named.

Recomputes, per existing master (08242234, 08335338), with the same reader as cc1.AC1.py (live S3 + the gateway's
record-level qualification): the 13-month window and every silver date in it. PASS when, for each master, every such
date is QUALIFIED or is listed in the worker's record under `unavailable` with a non-empty reason (no proven-complete
source), every date the record lists under `backfilled` now reads QUALIFIED, and at least one date was backfilled.

  python bf1.AC1.py <record.json> <repo_root>
"""
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

import boto3


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
    spec = importlib.util.spec_from_file_location("cc1", str(Path(__file__).with_name("cc1.AC1.py")))
    cc1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc1)
    sys.path.insert(0, str(root / "infra/aws/ec2/opal-gateway"))
    from app.integrations.schwab import catalog as cat
    contract = cat.parse_contract(json.loads((root / "org/standards/NFRA_OPLGTW_CONTRACT.json").read_text(encoding="utf-8")))
    rejected = {cat.F_REJECTED_BUCKET, cat.F_REJECTED_MASTER, cat.F_REJECTED_DATASET, cat.F_REJECTED_DATE,
                cat.F_REJECTED_KEY}
    s3 = boto3.client("s3", region_name="us-east-1")
    ok, total_backfilled = True, 0
    for m in cc1.MASTERS:
        prefix = "schwab/%s/meta/complete/" % m
        classes = {}
        for key in cc1.list_all(s3, prefix):
            mm = re.match(re.escape(prefix) + r"date=(\d{4}-\d{2}-\d{2})\.json$", key)
            if not mm:
                continue
            marker = json.loads(s3.get_object(Bucket=cc1.BUCKET, Key=key)["Body"].read())
            closure = marker.get("closure") if isinstance(marker, dict) else None
            if not isinstance(closure, dict):
                classes[mm.group(1)] = "LEGACY"
                continue
            f = cat.membership_findings(marker, closure, m, mm.group(1), contract)
            v = cat.validate_closure(closure, contract.masters)
            classes[mm.group(1)] = "QUALIFIED" if (not any(x["class"] in rejected for x in f)
                                                   and v["status"] == cat.RESULT_QUALIFIED) else "NONQUALIFYING"
        qual = sorted(d for d, c in classes.items() if c == "QUALIFIED")
        if not qual:
            print("FAIL: %s: no qualified record" % m)
            ok = False
            continue
        end = dt.date.fromisoformat(qual[-1])
        start = cc1.months_back(end, 13)
        silver = set()
        for ds in cc1.SERVED:
            p = "schwab/%s/silver/%s/" % (m, ds)
            for cp in cc1.list_all(s3, p, "/"):
                g = re.match(re.escape(p) + r"date=(\d{4}-\d{2}-\d{2})/$", cp)
                if g and start.isoformat() <= g.group(1) <= end.isoformat():
                    silver.add(g.group(1))
        mrec = (rec.get("masters") or {}).get(m) or {}
        unavailable = {d: r for d, r in (mrec.get("unavailable") or {}).items() if isinstance(r, str) and r.strip()}
        backfilled = list(mrec.get("backfilled") or [])
        open_dates = sorted(d for d in silver if classes.get(d) != "QUALIFIED" and d not in unavailable)
        not_now = sorted(d for d in backfilled if classes.get(d) != "QUALIFIED")
        total_backfilled += len(backfilled)
        print("%s: window %s..%s; silver dates %d; qualified in window %d; backfilled %d; unavailable named %d; "
              "open %d; backfilled-but-not-qualified %d" % (
                  m, start, end, len(silver), sum(classes.get(d) == "QUALIFIED" for d in silver), len(backfilled),
                  len(unavailable), len(open_dates), len(not_now)))
        if open_dates or not_now:
            print("FAIL: %s: open %s; backfilled but not qualified %s" % (m, open_dates[:10], not_now[:10]))
            ok = False
    if total_backfilled == 0:
        print("FAIL: no date was backfilled")
        ok = False
    print("RESULT: " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
