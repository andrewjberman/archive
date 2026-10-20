"""HVST-co-3 (amended by the issuer) -- drive the two unfired branches of the dossier-refresh driver on demand, dry mode,
against live data.

Read-only by construction: every driver call and every wrapped run is dry (write=False, never --write, no writer passed),
and the only file written is co3_branches.out (LF line endings, opened with newline="\\n").
Run from the worktree root with: python -u <this file>.

Amended item 2: the no-today branch is reachable only by a name whose build DIFFERS from its served dossier, so the
served side is UNH's real OLDER dossier (greatest as_of strictly earlier than 2026-10-20, same tie-break as the driver's
served read); every other dependency is the real one.
"""
import contextlib
import datetime as dt
import gzip
import io
import json
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
OLDER_CUTOFF = "2026-10-20"  # the older served dossier has as_of strictly earlier than this
NOW_NONTRADING = dt.datetime(2026, 10, 24, 14, 0, 0, tzinfo=dt.timezone.utc)  # Saturday
NOW_NOTODAY = dt.datetime(2026, 11, 2, 14, 0, 0, tzinfo=dt.timezone.utc)      # Monday, trading day, no block yet
NOW_REAL = dt.datetime(2026, 10, 20, 20, 0, 0, tzinfo=dt.timezone.utc)        # Tuesday, real day (controls)
# The first pass's census for the same name on the same day, carried verbatim (first pass, commit a92834eb31): the level
# name's build equals its served dossier, so the driver returned UNCHANGED before the today-block check.
FIRST_PASS_CENSUS = ("REFRESH-CENSUS names=1 written=0 would_write=0 unchanged=1 no_new_model_block=0 "
                     "no_today_model_block=0 skipped_allowed=0 skipped_guard=0 errors=0 mode=dry-run")
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


def measured(fn):
    """Runs fn and returns its value (or its error text) with the S3 requests, bytes and writes it made."""
    before = (TOT["req"], TOT["bytes"], TOT["writes"], dict(TOT["ops"]))
    value, err = None, None
    try:
        value = fn()
    except BaseException as exc:  # a crash is a recorded result, not a silent gap
        err = "%s: %s" % (type(exc).__name__, exc)
    ops = {k: v - before[3].get(k, 0) for k, v in TOT["ops"].items() if v - before[3].get(k, 0)}
    return {"value": value, "err": err, "req": TOT["req"] - before[0], "bytes": TOT["bytes"] - before[1],
            "writes": TOT["writes"] - before[2], "ops": ops}


def drive(argv, now):
    """One real driver call through main(), dry. Returns its captured stdout lines and its S3 cost."""
    if "--write" in argv:
        raise SystemExit("ERROR: this script never passes --write")

    def go():
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = dr.main(argv, now=now)
        return rc, buf.getvalue().splitlines()

    m = measured(go)
    if m["err"] is not None:
        m["rc"], m["lines"] = -1, ["EXCEPTION %s" % m["err"]]
    else:
        m["rc"], m["lines"] = m["value"]
    return m


class OlderServedDeps(dr.RealDeps):
    """The real RealDeps with ONE change: served() returns the older dossier. build, guard and the read-only client are real.
    No writer is passed, and the run is always dry."""

    def __init__(self, reader, older_doc):
        dr.RealDeps.__init__(self, reader, None)
        self._older_doc = older_doc

    def served(self, security_key):
        if security_key != NAME:
            raise AssertionError("the older-served wrapper serves %s only, not %r" % (NAME, security_key))
        return self._older_doc


def older_served(reader):
    """The UNH dossier the driver would serve if its newest stamp were strictly earlier than OLDER_CUTOFF: greatest such
    as_of, then the driver's own tie-break (last_modified, key) within it. Parsed as RealDeps.served parses."""
    prefix = dr.gold.table_prefix(dr.dossier.TABLE) + dr.store.entity_partition("security_key", NAME) + "/"
    rows = []
    for page in reader.get_paginator("list_objects_v2").paginate(Bucket=dr.gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            rows.append({"key": obj["Key"], "last_modified": dr.utc_text(obj.get("LastModified"))})
    listed = [r for r in rows if r["key"].endswith(dr.GATEWAY_SUFFIXES)]
    stamps = set()
    for r in listed:
        m = dr._AS_OF.search(r["key"])
        if m is not None and m.group(1) < OLDER_CUTOFF:
            stamps.add(m.group(1))
    if not stamps:
        raise SystemExit("ERROR: no stored dossier with as_of earlier than %s" % OLDER_CUTOFF)
    as_of = max(stamps)
    picked = dr.pick_dossier(listed, as_of)
    candidates = sorted((r["last_modified"] or "", r["key"]) for r in listed if ("as_of=%s." % as_of) in r["key"])
    raw = dr.gold.gold_get("s3://%s/%s" % (dr.gold.HARVEST_BUCKET, picked["key"]), client=reader)
    if picked["key"].endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8")), picked, as_of, candidates


def wrapped_run(older_doc, now):
    """One dry run of the real driver over NAME with the older served side. Returns (results, refresh lines, cost)."""
    lines = []

    def go():
        reader = dr.ReadOnlyClient(store._default_client(), dr.BUDGET_REQUESTS, dr.BUDGET_BYTES)
        deps = OlderServedDeps(reader, older_doc)
        return dr.run_names([NAME], deps, False, lines.append, now=now)

    m = measured(go)
    return m, lines


def list_prefix():
    """Key, size, ETag and LastModified of every object under the name's stored-dossier prefix (read-only)."""
    client = store._default_client()
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=dr.gold.HARVEST_BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            out.append((obj["Key"], obj["Size"], obj["ETag"], dr.utc_text(obj.get("LastModified"))))
    return sorted(out)


def census_from(results):
    return dr.census_line(results, "dry-run")


def find_census(lines):
    hits = [ln for ln in lines if ln.startswith("REFRESH-CENSUS ")]
    return hits[-1] if hits else "NONE"


def main():
    if dr.gold.HARVEST_BUCKET != "opal-data-harvest" or dr.pool_reader.POOL_BUCKET != "opal-data-harvest":
        raise SystemExit("ERROR: bucket premise differs from the face")
    emit("NOTE repo_root=%s" % ROOT.as_posix())
    emit("NOTE harvest_bucket=%s pool_bucket=%s" % (dr.gold.HARVEST_BUCKET, dr.pool_reader.POOL_BUCKET))
    emit("NOTE is_trading_day 2026-10-24=%s 2026-11-02=%s 2026-10-20=%s" % (
        trading_calendar.is_trading_day(dt.date(2026, 10, 24)),
        trading_calendar.is_trading_day(dt.date(2026, 11, 2)),
        trading_calendar.is_trading_day(dt.date(2026, 10, 20))))

    # 1. the skip branch: a Saturday, before any read
    r1 = drive(["--require-trading-day"], NOW_NONTRADING)
    skipped1 = any("REFRESH-SKIPPED not_a_trading_day" == ln for ln in r1["lines"])
    emit("NOTE run_local_date(%s)=%s" % (iso_z(NOW_NONTRADING), dr.run_local_date(NOW_NONTRADING).isoformat()))
    emit("BRANCH-NONTRADING now=%s skipped=%s exit=%s s3_gets=%d s3_puts=%d" % (
        iso_z(NOW_NONTRADING), "yes" if skipped1 else "no", r1["rc"], r1["req"] - r1["writes"], r1["writes"]))
    for ln in r1["lines"]:
        emit("NOTE driver-line: %s" % ln)
    emit("NOTE call1 ops=%s bytes=%d" % (r1["ops"], r1["bytes"]))

    # 2. the no-today branch with the REAL OLDER served dossier (amended item 2)
    before_list = list_prefix()
    emit("NOTE listing-before objects=%d" % len(before_list))
    helper = measured(lambda: older_served(dr.ReadOnlyClient(store._default_client(), dr.BUDGET_REQUESTS,
                                                              dr.BUDGET_BYTES)))
    if helper["err"] is not None:
        raise SystemExit("ERROR: older served read failed: %s" % helper["err"])
    older_doc, picked, older_as_of, candidates = helper["value"]
    emit("NOTE older-served as_of=%s key=%s last_modified=%s" % (older_as_of, picked["key"], picked["last_modified"]))
    for lm, key in candidates:
        emit("NOTE older-candidate as_of=%s last_modified=%s key=%s" % (older_as_of, lm, key))
    emit("NOTE direct-UNH-2026-11-02 census=%s" % FIRST_PASS_CENSUS)
    w2, w2_lines = wrapped_run(older_doc, NOW_NOTODAY)
    if w2["err"] is not None:
        census2 = "EXCEPTION %s" % w2["err"]
    else:
        census2 = census_from(w2["value"])
    emit("NOTE run_local_date=%s" % dr.run_local_date(NOW_NOTODAY).isoformat())
    emit("BRANCH-NOTODAY %s" % census2)
    for ln in w2_lines:
        emit("NOTE driver-line: %s" % ln)
    emit("NOTE call2 ops=%s bytes=%d writes=%d" % (w2["ops"], w2["bytes"], w2["writes"]))
    after_list = list_prefix()
    equal = [t[:3] for t in before_list] == [t[:3] for t in after_list]
    emit("BRANCH-NOTODAY-STORED before_after_equal=%s objects=%d" % ("yes" if equal else "no", len(after_list)))
    for key, size, etag, lm in after_list:
        emit("NOTE object key=%s size=%s etag=%s last_modified=%s" % (key, size, etag, lm))

    # 3. controls
    wp, wp_lines = wrapped_run(older_doc, NOW_REAL)
    if wp["err"] is not None:
        census_p = "EXCEPTION %s" % wp["err"]
    else:
        census_p = census_from(wp["value"])
    emit("NOTE control-positive census: %s" % census_p)
    m_ntmb = re.search(r"no_today_model_block=(\d+)", census_p)
    m_ww = re.search(r"would_write=(\d+)", census_p)
    ntmb = m_ntmb.group(1) if m_ntmb else "NONE"
    ww = m_ww.group(1) if m_ww else "NONE"
    skipped_p = not trading_calendar.is_trading_day(dr.run_local_date(NOW_REAL))  # the gate's own predicate (main, line 514)
    emit("CONTROL-POSITIVE now=%s only=%s served=older no_today_model_block=%s would_write=%s skipped=%s" % (
        iso_z(NOW_REAL), NAME, ntmb, ww, "yes" if skipped_p else "no"))
    for ln in wp_lines:
        emit("NOTE driver-line: %s" % ln)

    rn = drive(["--require-trading-day", "--only", NAME], NOW_REAL)
    skipped_n = any(ln.startswith("REFRESH-SKIPPED") for ln in rn["lines"])
    emit("NOTE control-negative census: %s" % find_census(rn["lines"]))
    emit("CONTROL-NEGATIVE now=%s require_trading_day skipped=%s" % (iso_z(NOW_REAL), "yes" if skipped_n else "no"))

    # totals: the driver calls that reached S3 (the first-pass line is carried, not re-run)
    calls = [r1, w2, wp, rn]
    total_req = sum(c["req"] for c in calls)
    total_bytes = sum(c["bytes"] for c in calls)
    total_writes = sum(c["writes"] for c in calls)
    emit("NOTE driver-calls writes_total=%d non_driver_requests_not_in_BRANCHES=%d bytes_unknown=%d" % (
        total_writes, TOT["req"] - total_req, TOT["bytes_unknown"]))
    emit("BRANCHES gets=%d bytes=%d" % (total_req, total_bytes))
    FH.close()


if __name__ == "__main__":
    main()
