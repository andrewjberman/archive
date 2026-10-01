"""Shared reads for HVST-ac-3's issuer checks (2.0.0_SA_COO~H): the paired chatter_daily rebuild. Read-only against S3.

`dry_build()` runs the producer's OWN `publication_gold.build_daily` for the as-of through the real `write_gold` against a
pass-through client that CAPTURES the put, so the parquet really serializes (the aa-3 lesson). 52k rows are too many to
sign row by row in git, so the signed expectation is: the row count, the put bytes, a sha256 over the sorted canonical rows,
and EVERY (row, field) that differs from the served snapshot, listed.
"""
import datetime
import hashlib
import io
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HARVST = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST")
UNIVERSE = os.path.join(HARVST, "deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json")
WK = os.path.join(HARVST, "deliverables/0.9.0_WK_AMGT_HARVST~86")
SIGNING = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round30/ac3_signing_expected.json")
LENOVO = "992_HK_Equity"
IN_WINDOW_DAYS = ("2026-08-13", "2026-09-01")
ROLLING = {"trailing_7d_sum", "trailing_30d_sum", "cumulative_ytd", "baseline_30d_sum", "breakout_ratio", "z_score"}


class CapturingClient:
    """Pass-through S3 client that captures puts instead of sending them."""

    def __init__(self, real):
        self._real = real
        self.puts = {}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts[Key] = {"body": Body}
        return {"ETag": '"captured"'}

    def head_object(self, Bucket, Key, **kw):
        if Key in self.puts:
            return {"ContentLength": len(self.puts[Key]["body"])}
        return self._real.head_object(Bucket=Bucket, Key=Key, **kw)

    def __getattr__(self, name):
        return getattr(self._real, name)


def securities():
    with open(UNIVERSE, encoding="utf-8") as fh:
        return json.load(fh)


def today():
    return datetime.datetime.now(datetime.timezone.utc).date()


def daily_prefix():
    return store.table_prefix("amgt", "gold", pg.GOLD_DAILY_TABLE)


def list_parts(cl=None):
    cl = cl or store._default_client()
    out = {}
    for page in cl.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=daily_prefix()):
        for obj in page.get("Contents", []) or []:
            out[obj["Key"]] = [obj["ETag"].strip('"'), obj["Size"]]
    return out


def key_of(r):
    return "%s|%s" % (r["security_key"], str(r["day"])[:10])


def canon(rows):
    return {key_of(r): json.dumps(r, sort_keys=True, default=str) for r in rows}


def digest(canon_rows):
    h = hashlib.sha256()
    for k in sorted(canon_rows):
        h.update(k.encode("utf-8") + b"\x00" + canon_rows[k].encode("utf-8") + b"\n")
    return h.hexdigest()


def dry_build(as_of=None):
    cl = CapturingClient(store._default_client())
    summary = pg.build_daily(securities(), as_of or today(), client=cl)
    if len(cl.puts) != 1:
        raise SystemExit("dry build captured %d puts, expected exactly 1" % len(cl.puts))
    key, put = next(iter(cl.puts.items()))
    return summary, key, pq.read_table(io.BytesIO(put["body"])).to_pylist(), len(put["body"])


def served():
    return pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)


def field_diffs(new_rows, old_rows):
    """Every (row key, field) whose value differs, plus keys new/gone."""
    N = {key_of(r): r for r in new_rows}
    S = {key_of(r): r for r in old_rows}
    moved = []
    for k in sorted(set(N) & set(S)):
        for f in sorted(set(N[k]) | set(S[k])):
            if json.dumps(N[k].get(f), default=str) != json.dumps(S[k].get(f), default=str):
                moved.append("%s|%s" % (k, f))
    return {"new_keys": sorted(set(N) - set(S)), "gone_keys": sorted(set(S) - set(N)), "moved": moved}


AB2_SIGNING = os.path.join(HARVST, "deliverables/2.0.0_SA_COO_H/round29/ab2_signing_expected.json")


def expected_rows():
    """The (security, day) rows the rebuild is expected to move: every pair ab-2 ADDED (round29/ab2_signing_expected.json,
    diff.new) whose publication day is on or after the page floor. Co-mentioned securities are included by construction."""
    with open(AB2_SIGNING, encoding="utf-8") as fh:
        s = json.load(fh)
    out = set()
    for k in s["diff"]["new"]:
        r = json.loads(s["expected_rows"][k])
        day = str(r.get("published_utc"))[:10]
        if day >= pg.BACKFILL_FLOOR.isoformat():
            out.add((r["security_key"], day))
    return out


def classify(moved, expected=None):
    """Split the moved (row, field) list: fields on an expected (security, day) row; rolling fields on a LATER day of an
    expected security (the consequence); and anything else (outside the expected diff)."""
    expected = expected if expected is not None else expected_rows()
    first = {}
    for sec, day in expected:
        first[sec] = min(day, first.get(sec, day))
    in_day, rolling_later, other = [], [], []
    for m in moved:
        sec, day, field = m.split("|")
        if (sec, day) in expected:
            in_day.append(m)
        elif sec in first and day > first[sec] and field in ROLLING:
            rolling_later.append(m)
        else:
            other.append(m)
    return in_day, rolling_later, other


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, default=str)
