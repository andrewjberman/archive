"""IRPT_BCKEND workstream ~PB round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one ACT cell: the signed Orion pair V3, pair (a), the one-time 33-day backfill.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB208-1  IB-pr-568  the one-time dated backfill of the absent flat bronze keys (positions 4, transactions 7, performance 22), by the same pull code the chain runs
    AC1  the gates (the packet's sha256 and both halves signed on it, the ledger opened before the first write) and the performance positive control, committed BEFORE any performance day was written
    AC2  the days: exactly the packet's lists (positions 4 trading days that hold a parquet key and no flat key), each read ABSENT first, each WRITTEN (version, size, row count, as-of) or ABSENT-AT-SOURCE (status, no key); none left over
    AC3  the read-back of every written key, the requests counted, and the eleven bound counters (no delete, no other write, no catalog or code-object change, no empty key, no secret printed)
"""
import datetime as dt
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB208-1_orion_backfill_record.json"
PACKET_SHA = "03a77b33174c3fb9e84d925dcbf32bfbdb7fb366efa9470fae01cc7afac2dc1c"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_ORION_PAIRS_V3_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ORION_PAIRS_V3_CTO_HALF.md"
TXN = ["2026-07-01", "2026-07-13", "2026-07-14", "2026-07-15", "2026-08-06", "2026-09-28", "2026-09-29"]
PERF = ["2026-05-04", "2026-05-05", "2026-05-06", "2026-05-07", "2026-05-08", "2026-05-11", "2026-07-01", "2026-07-02", "2026-07-06", "2026-07-07", "2026-07-09",
        "2026-07-13", "2026-07-14", "2026-07-15", "2026-07-21", "2026-07-22", "2026-07-23", "2026-08-06", "2026-09-28", "2026-09-29", "2026-09-30", "2026-10-13"]
FEEDS = {"positions": 4, "transactions": len(TXN), "performance": len(PERF)}
COUNTERS = ("files_deleted", "other_bucket_writes", "catalog_changes", "s3_code_objects_changed", "lambda_invokes", "iam_changes", "schedule_changes",
            "terraform_changes", "empty_keys_written", "secrets_printed", "functions_started_or_stopped")
fail, load, is_int = P6.fail, P6.load, P6.is_int
ISO = r"\d{4}-\d\d-\d\d"
TS = r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ"


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def calendar():
    f = P6.ROOT / "lib" / "trading_calendar.py"
    if not f.is_file():
        fail("no lib/trading_calendar.py in the tree")
    spec = importlib.util.spec_from_file_location("tcal_p208", str(f))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def c1():
    r = load(REC)
    if r.get("stop") is not None:
        fail("the record carries a stop: %r (the criteria are not run on a stopped act)" % (r.get("stop"),))
    g = r.get("gates") or {}
    if g.get("packet_sha256") != PACKET_SHA:
        fail("gates.packet_sha256 must be the signed packet's sha256 %s" % PACKET_SHA)
    for rel, who in ((COO_HALF, "COO"), (CTO_HALF, "CTO")):
        f = P6.ROOT / rel
        if not f.is_file() or PACKET_SHA[:12] not in f.read_text(encoding="utf-8", errors="replace"):
            fail("the %s half is not in the tree bound to the packet's sha256" % who)
    if g.get("coo_half_signed") is not True or g.get("cto_half_signed") is not True:
        fail("both halves must read signed in the record")
    if g.get("no_open_ledger_or_marker") is not True or g.get("one_change_at_a_time") is not True:
        fail("the one-change-at-a-time gate must read true")
    led = r.get("ledger") or {}
    lp = led.get("entry")
    if not isinstance(lp, str) or not lp.startswith("org/critical_paths/change_management/") or not (P6.ROOT / lp).is_file():
        fail("ledger.entry must name an entry under org/critical_paths/change_management/ in the tree")
    if led.get("opened_before_first_write") is not True:
        fail("the ledger must be opened before the first write")
    c = r.get("control") or {}
    if c.get("performed") is not True or c.get("branch") not in ("repo_script_matches", "chain_copy_runs_with_date"):
        fail("the performance control must be performed and name its branch (repo_script_matches | chain_copy_runs_with_date)")
    if not re.fullmatch(r"[0-9a-f]{40}", str(c.get("committed_commit", ""))):
        fail("control.committed_commit must be the 40-hex commit that holds the control result")
    if subprocess.run(["git", "-C", str(P6.ROOT), "cat-file", "-e", c["committed_commit"] + "^{commit}"], capture_output=True, timeout=60).returncode != 0:
        fail("control.committed_commit is not a commit in the tree")
    if not re.fullmatch(TS, str(c.get("committed_at_utc", ""))):
        fail("control.committed_at_utc must be an ISO UTC time")
    d = c.get("byte_diff")
    if not isinstance(d, dict) or not all(is_int(d.get(k)) and d[k] >= 0 for k in ("repo_bytes", "chain_bytes", "differing_lines")):
        fail("control.byte_diff needs repo_bytes, chain_bytes and differing_lines as counts")
    if c.get("dry_run_compared_day") != "2026-10-14" or not isinstance(c.get("shape_match"), bool):
        fail("control.dry_run_compared_day must be 2026-10-14 and shape_match a boolean")
    if c["branch"] == "repo_script_matches" and c["shape_match"] is not True:
        fail("branch repo_script_matches needs shape_match true")
    if c["branch"] == "chain_copy_runs_with_date" and (r.get("counters") or {}).get("s3_code_objects_changed") != 0:
        fail("the chain's copy must run with the date WITHOUT changing an S3 code object (else STOP and a new pair)")
    first_perf = sorted(x["written_at_utc"] for x in (r.get("days") or {}).get("performance", []) if x.get("outcome") == "WRITTEN")
    if first_perf and first_perf[0] <= c["committed_at_utc"]:
        fail("a performance day was written at or before the control's commit time")
    print("OK: the gates, the ledger and the performance control committed before any performance write")


def c2():
    r = load(REC)
    if r.get("stop") is not None:
        fail("the record carries a stop")
    cal = calendar()
    days = r.get("days")
    if not isinstance(days, dict) or sorted(days) != sorted(FEEDS):
        fail("days must hold %s" % ", ".join(sorted(FEEDS)))
    total = 0
    for feed, rows in days.items():
        if not isinstance(rows, list) or len(rows) != FEEDS[feed]:
            fail("%s: exactly %d day rows are required" % (feed, FEEDS[feed]))
        got = [x.get("day") for x in rows]
        if got != sorted(set(got)):
            fail("%s: day rows must be sorted and unique" % feed)
        if feed == "transactions" and got != TXN:
            fail("transactions: the days must be exactly the packet's seven")
        if feed == "performance" and got != PERF:
            fail("performance: the days must be exactly the packet's 22")
        for x in rows:
            d = dt.date.fromisoformat(x["day"]) if re.fullmatch(ISO, str(x.get("day"))) else None
            if d is None or not cal.is_trading_day(d):
                fail("%s %s: not a trading day" % (feed, x.get("day")))
            if x.get("absent_before") is not True:
                fail("%s %s: the key must be read ABSENT first" % (feed, x["day"]))
            if feed == "positions" and x.get("parquet_key_present") is not True:
                fail("positions %s: the backfill days hold a parquet key and no flat key" % x["day"])
            if x.get("outcome") == "WRITTEN":
                if not (isinstance(x.get("version_id"), str) and x["version_id"]) or not is_int(x.get("content_length")) or x["content_length"] <= 0 \
                        or not is_int(x.get("row_count")) or x["row_count"] <= 0 or not re.fullmatch(ISO, str(x.get("asof_day"))) or not re.fullmatch(TS, str(x.get("written_at_utc"))):
                    fail("%s %s: a WRITTEN day needs version_id, content_length > 0, row_count > 0, asof_day and written_at_utc (an empty key is never written)" % (feed, x["day"]))
            elif x.get("outcome") == "ABSENT_AT_SOURCE":
                if x.get("response_status") in (None, "") or x.get("version_id") is not None:
                    fail("%s %s: ABSENT_AT_SOURCE needs the response status and no key" % (feed, x["day"]))
            else:
                fail("%s %s: outcome must be WRITTEN or ABSENT_AT_SOURCE (every day is dispositioned)" % (feed, x["day"]))
            total += 1
    if total != sum(FEEDS.values()):
        fail("33 days must be dispositioned")
    print("OK: %d days dispositioned, each read ABSENT first" % total)


def c3():
    r = load(REC)
    if r.get("stop") is not None:
        fail("the record carries a stop")
    rows = [x for v in (r.get("days") or {}).values() for x in v]
    written = [x for x in rows if x.get("outcome") == "WRITTEN"]
    for x in written:
        if x.get("read_back_ok") is not True:
            fail("%s: a written key needs its read-back (head-object length, content type and row count)" % x.get("day"))
    if r.get("keys_written") != len(written):
        fail("keys_written must equal the WRITTEN rows (%d)" % len(written))
    req = r.get("requests_made")
    if not is_int(req) or not 0 <= req <= 16000:
        fail("requests_made must be a count (about 14,300 expected, one script run per day; above 16,000 is a stop)")
    c = r.get("counters")
    if not isinstance(c, dict):
        fail("counters are required")
    for k in COUNTERS:
        if c.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, c.get(k)))
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters (where it ran, what was not read, the objects touched counted)")
    scrub = json.dumps({k: v for k, v in r.items() if k != "days"})
    P6.no_long_digits(scrub)
    print("OK: %d written keys read back, %d requests, the counters 0" % (len(written), req))


CHECKS = {"IB208-1-AC1": c1, "IB208-1-AC2": c2, "IB208-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p208_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
