"""HVST-co-3 -- drive the two unfired branches of the dossier-refresh driver on demand, in DRY mode, against live data.

Read-only by construction: every driver call is a dry run (never --write), and the only file written is co3_branches.out
(LF line endings, opened with newline="\\n"). Run from the worktree root with: python -u <this file>.
"""
import contextlib
import datetime as dt
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]  # <serial>/ -> deliverables -> AMGT_HARVST -> AMGT -> D5 -> missions -> org -> ROOT
if not (ROOT / "lib" / "research" / "corpus" / "dossier_refresh.py").exists():
    raise SystemExit("ERROR: repo root not derived correctly: %s" % ROOT)
sys.path.insert(0, str(ROOT))

from lib import trading_calendar  # noqa: E402
from lib.research.corpus import dossier_refresh as dr  # noqa: E402
from lib.research.harvest import store  # noqa: E402

OUT = HERE / "co3_branches.out"
NAME = "UNH_US_Equity"
PREFIX = "amgt/harvest/gold/research_dossier/security_key=UNH_US_Equity/"
NOW_NONTRADING = dt.datetime(2026, 10, 24, 14, 0, 0, tzinfo=dt.timezone.utc)  # Saturday
NOW_NOTODAY = dt.datetime(2026, 11, 2, 14, 0, 0, tzinfo=dt.timezone.utc)      # Monday, trading day, no block yet
NOW_REAL = dt.datetime(2026, 10, 20, 20, 0, 0, tzinfo=dt.timezone.utc)        # Tuesday, real day (controls)
WRITE_OPS = frozenset(("PutObject", "CopyObject", "DeleteObject", "DeleteObjects", "CreateMultipartUpload",
                       "UploadPart", "UploadPartCopy", "CompleteMultipartUpload", "AbortMultipartUpload",
                       "PutObjectAcl", "PutObjectTagging", "DeleteObjectTagging"))

TOT = {"req": 0, "bytes": 0, "writes": 0, "ops": {}, "bytes_unknown": 0}


def _on_before(model=None, **kwargs):
    name = getattr(model, "name", "?")
    TOT["req"] += 1
    TOT["ops"][name] = TOT["ops"].get(name, 0) + 1
    if name in WRITE_OPS:
        TOT["writes"] += 1
    return None  # a handler returning non-None would short-circuit the call


def _on_after(http_response=None, **kwargs):
    raw = None
    try:
        raw = http_response.headers.get("content-length")
    except AttributeError:
        raw = None
    if raw is None:
        TOT["bytes_unknown"] += 1
    else:
        TOT["bytes"] += int(raw)
    return None


_REAL_DEFAULT_CLIENT = store._default_client


def _counted_default_client():
    client = _REAL_DEFAULT_CLIENT()  # boto3.client(...) builds a fresh client on every call
    client.meta.events.register("before-call.s3", _on_before)
    client.meta.events.register("after-call.s3", _on_after)
    return client


store._default_client = _counted_default_client  # the driver calls store._default_client() at run time

FH = open(OUT, "w", encoding="utf-8", newline="\n")


def emit(line):
    print(line, flush=True)
    FH.write(line + "\n")
    FH.flush()


def iso_z(now):
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")


def drive(argv, now):
    """One driver call, dry. Returns its captured stdout lines and the S3 requests/bytes/writes it made."""
    if "--write" in argv:
        raise SystemExit("ERROR: this script never passes --write")
    before = (TOT["req"], TOT["bytes"], TOT["writes"], dict(TOT["ops"]))
    buf = io.StringIO()
    rc = None
    try:
        with contextlib.redirect_stdout(buf):
            rc = dr.main(argv, now=now)
    except BaseException as exc:  # a crash is a recorded result, not a silent gap
        rc = -1
        buf.write("EXCEPTION %s: %s\n" % (type(exc).__name__, exc))
    ops = {k: v - before[3].get(k, 0) for k, v in TOT["ops"].items() if v - before[3].get(k, 0)}
    return {
        "rc": rc,
        "lines": buf.getvalue().splitlines(),
        "req": TOT["req"] - before[0],
        "bytes": TOT["bytes"] - before[1],
        "writes": TOT["writes"] - before[2],
        "ops": ops,
    }


def list_prefix():
    """Key, size and ETag of every object under the name's stored-dossier prefix (read-only)."""
    client = store._default_client()
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=dr.gold.HARVEST_BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            out.append((obj["Key"], obj["Size"], obj["ETag"]))
    return sorted(out)


def census(lines):
    hits = [ln for ln in lines if ln.startswith("REFRESH-CENSUS ")]
    return hits[-1] if hits else "NONE"


def main():
    emit("NOTE repo_root=%s" % ROOT.as_posix())
    emit("NOTE harvest_bucket=%s pool_bucket=%s" % (dr.gold.HARVEST_BUCKET, dr.pool_reader.POOL_BUCKET))
    if dr.gold.HARVEST_BUCKET != "opal-data-harvest" or dr.pool_reader.POOL_BUCKET != "opal-data-harvest":
        raise SystemExit("ERROR: bucket premise differs from the face")
    emit("NOTE is_trading_day 2026-10-24=%s 2026-11-02=%s 2026-10-20=%s" % (
        trading_calendar.is_trading_day(dt.date(2026, 10, 24)),
        trading_calendar.is_trading_day(dt.date(2026, 11, 2)),
        trading_calendar.is_trading_day(dt.date(2026, 10, 20))))

    # 1. the skip branch: a Saturday, before any read
    r1 = drive(["--require-trading-day"], NOW_NONTRADING)
    skipped1 = "REFRESH-SKIPPED not_a_trading_day" in r1["lines"]
    emit("NOTE run_local_date(%s)=%s" % (iso_z(NOW_NONTRADING), dr.run_local_date(NOW_NONTRADING).isoformat()))
    emit("BRANCH-NONTRADING now=%s skipped=%s exit=%s s3_gets=%d s3_puts=%d" % (
        iso_z(NOW_NONTRADING), "yes" if skipped1 else "no", r1["rc"], r1["req"] - r1["writes"], r1["writes"]))
    for ln in r1["lines"]:
        emit("NOTE driver-line: %s" % ln)
    emit("NOTE call1 ops=%s bytes=%d" % (r1["ops"], r1["bytes"]))

    # 2. the no-today-block branch: a Monday with no model block for today; stored dossier must not move
    before_list = list_prefix()
    emit("NOTE listing-before objects=%d" % len(before_list))
    r2 = drive(["--only", NAME, "--require-trading-day"], NOW_NOTODAY)
    after_list = list_prefix()
    emit("NOTE run_local_date=%s" % dr.run_local_date(NOW_NOTODAY).isoformat())
    emit("BRANCH-NOTODAY %s" % census(r2["lines"]))
    for ln in r2["lines"]:
        emit("NOTE driver-line: %s" % ln)
    emit("NOTE call2 ops=%s bytes=%d writes=%d" % (r2["ops"], r2["bytes"], r2["writes"]))
    equal = before_list == after_list
    emit("BRANCH-NOTODAY-STORED before_after_equal=%s objects=%d" % ("yes" if equal else "no", len(after_list)))
    for key, size, etag in after_list:
        emit("NOTE object key=%s size=%s etag=%s" % (key, size, etag))

    # 3. controls: the same name on a real day. POSITIVE and NEGATIVE are one driver call (identical argv and now).
    r3 = drive(["--only", NAME, "--require-trading-day"], NOW_REAL)
    cen3 = census(r3["lines"])
    emit("NOTE control census: %s" % cen3)
    m = re.search(r"no_today_model_block=(\d+)", cen3)
    ntmb = m.group(1) if m else "NONE"
    skipped3 = any("REFRESH-SKIPPED" in ln for ln in r3["lines"])
    emit("CONTROL-POSITIVE now=%s only=%s no_today_model_block=%s skipped=%s" % (
        iso_z(NOW_REAL), NAME, ntmb, "yes" if skipped3 else "no"))
    emit("CONTROL-NEGATIVE now=%s require_trading_day skipped=%s" % (iso_z(NOW_REAL), "yes" if skipped3 else "no"))
    for ln in r3["lines"]:
        emit("NOTE driver-line: %s" % ln)
    emit("NOTE call3 ops=%s bytes=%d" % (r3["ops"], r3["bytes"]))

    total_req = r1["req"] + r2["req"] + r3["req"]
    total_bytes = r1["bytes"] + r2["bytes"] + r3["bytes"]
    emit("NOTE driver-call writes_total=%d listing-requests-not-counted-in-BRANCHES=%d bytes_unknown=%d" % (
        r1["writes"] + r2["writes"] + r3["writes"], TOT["req"] - total_req, TOT["bytes_unknown"]))
    emit("BRANCHES gets=%d bytes=%d" % (total_req, total_bytes))
    FH.close()


if __name__ == "__main__":
    main()
