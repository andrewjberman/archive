"""HVST-cb-9 step 5 / C-c2: read token_source and status from the run records of the new pass. Read only.

Usage: python cb9_token_source.py <runtime runs dir> <T0 ISO Z> [<publisher> ...]
Prints one line per run record whose file mtime is at or after T0: run id, publisher, status, token_source,
request_attempts length. token_source is found wherever it sits in the record; a record with no token_source field prints NONE.
"""
from __future__ import annotations

import datetime
import json
import os
import sys


def find_all(obj, key, path=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                out.append((path + "/" + k, v))
            out.extend(find_all(v, key, path + "/" + k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:200]):
            out.extend(find_all(v, key, path + "[%d]" % i))
    return out


def main(runs, t0_iso, publishers):
    t0 = datetime.datetime.strptime(t0_iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()
    names = [n for n in os.listdir(runs) if n.endswith(".json")]
    rows = []
    for n in names:
        p = os.path.join(runs, n)
        if os.path.getmtime(p) >= t0:
            rows.append((os.path.getmtime(p), n, p))
    rows.sort()
    print("RUNS_DIR=%s files_total=%d at_or_after_T0=%d" % (runs, len(names), len(rows)))
    for _, n, p in rows:
        d = json.load(open(p, encoding="utf-8"))
        pub = d.get("publisher") or (d.get("publishers") or [None])[0]
        if publishers and pub not in publishers:
            continue
        ts = find_all(d, "token_source")
        vals = sorted({repr(v) for _, v in ts}) if ts else ["NONE"]
        print("%s publisher=%s status=%s token_source=%s request_attempts=%d" % (
            n, pub, d.get("status"), ",".join(vals), len(d.get("request_attempts") or [])))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
