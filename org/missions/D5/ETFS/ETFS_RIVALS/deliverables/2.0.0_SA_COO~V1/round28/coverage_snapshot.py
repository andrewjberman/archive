"""WS2/WS3 deploy pair, COO condition 5 and CTO condition 8 -- snapshot, and later compare, the served holdings-coverage objects.

    python coverage_snapshot.py take <out dir> [<end day, default 2026-10-09>] [<n trading days, default 20>]
    python coverage_snapshot.py compare <snapshot dir> [<lookback trading days allowed to change, default 10>]

take:    downloads rivalfunds/etfs/gold/holdings_coverage/date=<D>/holdings_coverage.parquet for the n trading days ending
         <end day> (lib/trading_calendar) into <out dir>, and writes <out dir>/manifest.json: key, bytes, sha256, rows and
         the status counts of each object. A missing key is recorded as absent. Read-only on S3.
compare: re-reads every manifest key live and prints each as unchanged / changed / absent, with the status counts before and
         after. A key that changed and lies OUTSIDE the last <lookback> trading days of the snapshot is a STOP line.
"""
import datetime as dt
import hashlib
import io
import json
import os
import pathlib
import sys

import boto3
import pandas as pd

sys.path.insert(0, os.getcwd())
from lib import trading_calendar as tc  # noqa: E402

B = "opal-data-etfs"
PRE = "rivalfunds/etfs/gold/holdings_coverage/date={d}/holdings_coverage.parquet"
s3 = boto3.client("s3", region_name="us-east-1")


def trading_days(end, n):
    out, d = [], dt.date.fromisoformat(end)
    while len(out) < n:
        if tc.is_trading_day(d):
            out.append(d.isoformat())
        d -= dt.timedelta(days=1)
    return sorted(out)


def read(key):
    try:
        b = s3.get_object(Bucket=B, Key=key)["Body"].read()
    except s3.exceptions.NoSuchKey:
        return None
    return b


def counts(b):
    df = pd.read_parquet(io.BytesIO(b))
    col = "status" if "status" in df.columns else None
    return len(df), (df[col].astype(str).value_counts().to_dict() if col else {})


mode = sys.argv[1]
if mode == "take":
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    days = trading_days(sys.argv[3] if len(sys.argv) > 3 else "2026-10-09", int(sys.argv[4]) if len(sys.argv) > 4 else 20)
    man = []
    for d in days:
        key = PRE.format(d=d)
        b = read(key)
        if b is None:
            man.append({"day": d, "key": key, "absent": True})
            print(f"{d}: ABSENT")
            continue
        (out / f"{d}.parquet").write_bytes(b)
        n, st = counts(b)
        man.append({"day": d, "key": key, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "rows": n, "status": st})
        print(f"{d}: {len(b)} bytes sha256 {hashlib.sha256(b).hexdigest()[:12]} rows {n} {st}")
    (out / "manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
    print(f"SNAPSHOT: {sum(1 for m in man if not m.get('absent'))} of {len(man)} keys saved to {out}")
elif mode == "compare":
    snap = pathlib.Path(sys.argv[2])
    man = json.loads((snap / "manifest.json").read_text(encoding="utf-8"))
    look = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    allowed = {m["day"] for m in man[-look:]}
    stops = 0
    for m in man:
        b = read(m["key"])
        if m.get("absent"):
            print(f"{m['day']}: was absent, now {'absent' if b is None else 'PRESENT'}")
            continue
        if b is None:
            print(f"{m['day']}: ABSENT NOW (was {m['bytes']} bytes)")
            stops += 1
            continue
        same = hashlib.sha256(b).hexdigest() == m["sha256"]
        n, st = counts(b)
        line = f"{m['day']}: {'unchanged' if same else 'CHANGED'} rows {m['rows']}->{n} status {m['status']} -> {st}"
        if not same and m["day"] not in allowed:
            line += "   <-- STOP: changed outside the last %d trading days (restore same day)" % look
            stops += 1
        print(line)
    print(f"COMPARE RESULT: {stops} stop line(s) over {len(man)} keys")
    sys.exit(1 if stops else 0)
