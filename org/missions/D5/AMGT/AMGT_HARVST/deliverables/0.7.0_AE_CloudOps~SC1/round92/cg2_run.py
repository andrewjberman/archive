"""HVST-cg-2 driver, run from the pinned worktree (C:/tmp/cg2-build at a9aecdd593). ASCII only.

Usage (each date is a SEPARATE foreground command, always `python -u`, output appended to cg2_run.log by the caller):
  python -u cg2_run.py --date 2026-09-25 --plan    read only: build the date's rows, print counts, put nothing
  python -u cg2_run.py --date 2026-09-25           the write of that date, then the read-back (C-3) and Branch A checks
There is NO loop, NO retry and NO background mode (COO half C-5, CTO round-90 rule D1-S44).

Row selection is cg1_rebuild_plan.py's: the newest row per (security_key, report_id) by the gateway's rule (the part KEY that
sorts highest), the two misfiled KMB rows excluded, dict(row) plus fund_relation = classify(fund, fund_evidence), restricted
to the rows whose fetched_at date is the date asked for. The write is store.silver_append("amgt", "research-report", rows,
("security_key", "report_id"), run_stamp, client=<the real client>) with a fresh run_stamp.

Guards: the tree is a9aecdd593 with an empty lib/research diff; UTC now is inside 2026-10-18 00:30Z to 02:30Z; the canary date
2026-09-25 goes first; a date already in the manifest is refused; the date's planned row count is 84, 121 or 148 (else STOP);
silver_append must report skipped_unchanged=0 and exactly one part.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import os
import re
import subprocess
import sys
from collections import Counter

WT = r"C:\tmp\cg2-build"
sys.path.insert(0, WT)
os.chdir(WT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.corpus import fund_relation  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PIN = "a9aecdd593"
OUT = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round92"
MANIFEST = os.path.join(OUT, "cg2_written.out")
WIN_START = datetime.datetime(2026, 10, 18, 0, 30, tzinfo=datetime.timezone.utc)
WIN_END = datetime.datetime(2026, 10, 18, 2, 30, tzinfo=datetime.timezone.utc)
PLANNED = {"2026-09-25": 84, "2026-09-23": 121, "2026-09-24": 148}
CANARY = "2026-09-25"
CENSUS = {"holding": 121, "candidate": 14, "initiate": 2, "interest": 2, "template": 1, "unclassified": 0, "none": 213}
KEEP_COLUMNS_NOT_COMPARED = ("fund_relation", "record_hash")


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp_text():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args):
    return subprocess.run(["git", "-C", WT] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def manifest_lines():
    if not os.path.exists(MANIFEST):
        return []
    return open(MANIFEST, encoding="ascii").read().splitlines()


def written_dates():
    out = {}
    for ln in manifest_lines():
        m = re.search(r" WROTE part date=(\S+) rows=(\d+) ", ln)
        if m:
            out[m.group(1)] = int(m.group(2))
    return out


def kept_rows(client):
    """The newest row per (security_key, report_id) by the gateway rule, MISFILED excluded (as cg1_rebuild_plan.py)."""
    prefix = store.table_prefix(typed.SOURCE, "silver", typed.TABLE)
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        keys.extend(obj["Key"] for obj in (page.get("Contents", []) or []) if obj["Key"].endswith(".parquet"))
    keys.sort()
    newest = {}
    rows_read = 0
    for key in keys:
        resp = client.get_object(Bucket=store.HARVEST_BUCKET, Key=key)
        part_rows = pq.read_table(io.BytesIO(resp["Body"].read())).to_pylist()
        rows_read += len(part_rows)
        for row in part_rows:
            ident = (row.get("security_key"), row.get("report_id"))
            prev = newest.get(ident)
            if prev is None or key > prev[0]:
                newest[ident] = (key, row)
    excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    rows = [dict(newest[ident][1]) for ident in sorted(newest, key=lambda x: (str(x[0]), str(x[1])))
            if ident not in excluded]
    return rows, keys, rows_read


def build(date_text, client):
    rows, keys, rows_read = kept_rows(client)
    for row in rows:
        row["fund_relation"] = fund_relation.classify(row.get("fund"), row.get("fund_evidence"))
    day = [r for r in rows if r["fetched_at"].date().isoformat() == date_text]
    print("DENOMINATOR old_parts=%d rows_read=%d kept=%d date=%s date_rows=%d relations_all=%s" % (
        len(keys), rows_read, len(rows), date_text, len(day), dict(sorted(Counter(r["fund_relation"] for r in rows).items()))))
    return rows, day


def record(client, uri, date_text, nrows, relations):
    bucket, key = uri[len("s3://"):].split("/", 1)
    head = client.head_object(Bucket=bucket, Key=key)
    body = client.get_object(Bucket=bucket, Key=key)["Body"].read()
    line = "%s WROTE part date=%s rows=%d key=%s VersionId=%s bytes=%d sha256=%s relations=%s" % (
        stamp_text(), date_text, nrows, key, head.get("VersionId"), len(body), hashlib.sha256(body).hexdigest(),
        dict(sorted(relations.items())))
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
    print(line)
    return bucket, key, body


def readback(date_text, day, body):
    """C-3 / Branch A: the part read back equals the plan. Returns True on PASS."""
    new_rows = pq.read_table(io.BytesIO(body)).to_pylist()
    problems = []
    if len(new_rows) != len(day):
        problems.append("row count %d != planned %d" % (len(new_rows), len(day)))
    if new_rows and "fund_relation" not in new_rows[0]:
        problems.append("column fund_relation absent")
    ident = lambda r: (r.get("security_key"), r.get("report_id"))  # noqa: E731
    planned = {ident(r): r for r in day}
    got = {ident(r): r for r in new_rows}
    if set(planned) != set(got) or len(got) != len(new_rows):
        problems.append("key set differs: missing=%d extra=%d dup=%d" % (
            len(set(planned) - set(got)), len(set(got) - set(planned)), len(new_rows) - len(got)))
    diffs = Counter()
    bad_rel = 0
    for k, new in got.items():
        old = planned.get(k)
        if old is None:
            continue
        for col in set(old) | set(new):
            if col in KEEP_COLUMNS_NOT_COMPARED:
                continue
            if old.get(col) != new.get(col):
                diffs[col] += 1
        if new.get("fund_relation") != fund_relation.classify(new.get("fund"), new.get("fund_evidence")):
            bad_rel += 1
        if new.get("fund_relation") != old.get("fund_relation"):
            bad_rel += 1
    if diffs:
        problems.append("columns differing from the superseded row: %s" % dict(diffs))
    if bad_rel:
        problems.append("fund_relation mismatch on %d row(s)" % bad_rel)
    rel_new = Counter(r.get("fund_relation") for r in new_rows)
    rel_plan = Counter(r["fund_relation"] for r in day)
    if rel_new != rel_plan:
        problems.append("per-relation counts differ: part %s plan %s" % (dict(rel_new), dict(rel_plan)))
    for p in problems:
        print("READBACK-PROBLEM %s" % p)
    print("READBACK date=%s rows=%d relations=%s" % (date_text, len(new_rows), dict(sorted(rel_new.items()))))
    ok = not problems
    print("READBACK date=%s rows=%d equal=%s" % (date_text, len(new_rows), "PASS" if ok else "FAIL"))
    return ok


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--plan", action="store_true")
    args = ap.parse_args(argv[1:])
    d = args.date
    if d not in PLANNED:
        print("STOP: %s is not one of the three planned dates" % d)
        return 2
    head = git("rev-parse", "HEAD")
    if not head.startswith(PIN):
        print("STOP: worktree HEAD %s is not %s" % (head, PIN))
        return 2
    if git("diff", PIN, "HEAD", "--", "lib/research"):
        print("STOP: lib/research differs from %s" % PIN)
        return 2
    real = store._default_client()
    print("=== %s date=%s plan_only=%s start %s HEAD=%s ===" % (os.path.basename(__file__), d, args.plan, stamp_text(), head[:10]))
    rows, day = build(d, real)
    if len(day) != PLANNED[d]:
        print("STOP: date %s plans %d rows, the order says %d; nothing written" % (d, len(day), PLANNED[d]))
        return 4
    counts = {k: v for k, v in Counter(r["fund_relation"] for r in rows).items() if v}
    if len(rows) != 353 or counts != {k: v for k, v in CENSUS.items() if v}:
        print("STOP: the 353-row plan no longer equals the census: %s" % counts)
        return 4
    if args.plan:
        print("PLAN-ONLY date=%s rows=%d relations=%s; nothing put" % (d, len(day), dict(sorted(Counter(r["fund_relation"] for r in day).items()))))
        return 0
    if not (WIN_START <= now() < WIN_END):
        print("STOP: now %s is outside the window 00:30Z to 02:30Z" % stamp_text())
        return 3
    done = written_dates()
    if d in done:
        print("STOP: date %s is already in the manifest" % d)
        return 2
    if d != CANARY and CANARY not in done:
        print("STOP: the canary %s must be written and read back first" % CANARY)
        return 2
    run_stamp = store.stamp(now())
    try:
        result = store.silver_append(typed.SOURCE, typed.TABLE, day, typed.RECORD_KEY_FIELDS, run_stamp, client=real)
    except Exception as exc:  # noqa: BLE001
        print("STOP (silver_append): %s: %s -- the bucket state of this date is UNKNOWN until read" % (type(exc).__name__, exc))
        return 5
    print("SILVER_APPEND result written_rows=%s skipped_unchanged=%s parts=%s run_stamp=%s" % (
        result.get("written_rows"), result.get("skipped_unchanged"), result.get("parts"), run_stamp))
    if result.get("skipped_unchanged") != 0 or len(result.get("parts", [])) != 1 or result.get("written_rows") != len(day):
        print("STOP: the append is not the one part of %d rows with 0 skipped; READ the bucket before anything else" % len(day))
        return 5
    try:
        _b, _k, body = record(real, result["parts"][0], d, len(day), Counter(r["fund_relation"] for r in day))
    except Exception as exc:  # noqa: BLE001
        print("STOP (record/readback fetch): %s: %s" % (type(exc).__name__, exc))
        return 5
    ok = readback(d, day, body)
    done = written_dates()
    line = "%s WRITTEN parts=%d rows=%d" % (stamp_text(), len(done), sum(done.values()))
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
    print(line)
    print("=== date=%s done %s readback=%s ===" % (d, stamp_text(), "PASS" if ok else "FAIL"))
    return 0 if ok else 6


if __name__ == "__main__":
    sys.exit(main(sys.argv))
