"""IRPT_BCKEND workstream ~PO round 13 (issuer 2.0.0_SA_COO~N2) -- the checks of the WORLD order IB-pn-8: the one-time Scope history backfill
under Orion pair (b) ADDENDUM 5 (raw replies once per run; ADDENDUM 2's rules for the call).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.
Grades the record the seat writes at deliverables/0.7.0_AE_CloudOps~IB2/IBN8-1_backfill_record.json (counts, hashes, dates and flags only).

  IBN8-AC1  the gates read before the first call: ADDENDUM 5 at its blob with both halves, the first scheduled run of the new writer passed
            (IBN7-AC3), the repository script hashing to the addendum's sha256 (read by this check), the live script object re-hashed to
            it immediately before the run, the household count within the bound, the earliest start date and the partition count (2326)
            stated before the first call, no other act open, the run started outside the CTO's band and not on 2026-10-20, and the run
            host chosen by the CTO's rule
  IBN8-AC2  the run: calls within the bound, the call phase within 20 minutes, days written plus days skipped as existing equal the stated
            partition count, no zero, no key outside the feed's prefixes, the daily factor stored, exactly one run object written and every
            envelope v2 without responses, peak memory printed and below the host's limit, no 429 left standing, no day overwritten
  IBN8-AC3  the check after the run: every written day read back, at least 5 accounts each printed with its window and error, every window
            at most 237 days and every error within 0.5 bp, and no window named readable
"""
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
ADD5 = D + "2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL.md"
ADD5_COO = D + "2.0.0_SA_COO~N2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL_COO_HALF.md"
ADD5_CTO = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL_CTO_HALF.md"
RECORD = D + "0.7.0_AE_CloudOps~IB2/IBN8-1_backfill_record.json"
PN7_CHECK = D + "2.0.0_SA_COO~N2/checks/r12/pn7_cells.py"
SCRIPT = "data/inf/manual_api/pull_inflection_scope_account_returns.py"
ADD5_BLOB = "619dbf431bc578cf22bb59114f5e289d7f9c4c94"
SCRIPT_SHA = "acfe390bda5af03e3c38330ece8f18d32a87f122594f593f855fc6d802eb21a3"
BOUND = 294
PARTITIONS = 2326
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def need(cid, cond, why):
    if not cond:
        fail(cid, why)


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load(root, cid):
    path = root / RECORD
    if not path.is_file():
        fail(cid, "backfill record absent: " + RECORD)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        fail(cid, "backfill record is not JSON: %s" % exc)


def schedule_ok(stamp):
    """Outside the weekday 11:30Z to 14:15Z band and not Tuesday 2026-10-20 (the Inflection transaction day)."""
    try:
        when = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return False
    if when.date() == dt.date(2026, 10, 20):
        return False
    minutes = when.hour * 60 + when.minute
    return not (when.weekday() < 5 and 11 * 60 + 30 <= minutes < 14 * 60 + 15)


def ac1(root):
    cid = "IBN8-AC1"
    rec = load(root, cid)
    add = root / ADD5
    need(cid, add.is_file() and blob(add) == ADD5_BLOB, "ADDENDUM 5 is not at blob " + ADD5_BLOB)
    for half in (ADD5_COO, ADD5_CTO):
        p = root / half
        need(cid, p.is_file() and ADD5_BLOB[:10] in p.read_text(encoding="utf-8"), "half absent or not bound to the blob: " + half)
    out = subprocess.run([sys.executable, str(root / PN7_CHECK), str(root), "IBN7-AC3"], capture_output=True, text=True, timeout=60)
    need(cid, out.returncode == 0, "the first scheduled run of the new writer has not passed (IBN7-AC3)")
    script = root / SCRIPT
    need(cid, script.is_file() and hashlib.sha256(script.read_bytes()).hexdigest() == SCRIPT_SHA, "the repository script does not hash to " + SCRIPT_SHA)
    g = rec.get("gates", {})
    need(cid, g.get("addendum_blob") == ADD5_BLOB and g.get("both_halves_signed") is True, "record: addendum blob or halves")
    need(cid, g.get("live_script_sha256") == SCRIPT_SHA and g.get("live_hash_read_immediately_before_run") is True,
         "record: the live script object was not re-hashed to " + SCRIPT_SHA + " immediately before the run")
    hc = g.get("household_count")
    need(cid, type(hc) is int and 0 < hc <= BOUND, "record: household count above the bound or absent")
    need(cid, g.get("earliest_start_date_read") is True and g.get("partition_count_stated") == PARTITIONS and g.get("stated_before_first_call") is True,
         "record: the earliest start date and the partition count %d were not stated before the first call" % PARTITIONS)
    need(cid, g.get("other_act_open_on_chain") is False, "record: another act of the seat is open on the chain")
    need(cid, schedule_ok(rec.get("run", {}).get("started_at_utc")), "record: the run started inside the weekday 11:30Z-14:15Z band or on 2026-10-20")
    host = g.get("host", {})
    if host.get("kind") == "ib2_host":
        need(cid, host.get("every_check_allowed_as_is") is True and host.get("grants_added") == 0,
             "record: IB2's host needs every check allowed AS IS and no grant added")
    elif host.get("kind") == "runner":
        need(cid, host.get("started_once") is True and host.get("shutdown_command_sent") is False
             and host.get("idle_hours_recorded") is True, "record: runner path needs one start, no shutdown command, idle hours recorded")
    else:
        fail(cid, "record: host kind must be ib2_host or runner")


def num(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def ac2(root):
    cid = "IBN8-AC2"
    rec = load(root, cid)
    run = rec.get("run", {})
    stated = rec.get("gates", {}).get("partition_count_stated")
    need(cid, type(run.get("calls_made")) is int and 0 < run["calls_made"] <= BOUND, "record: calls exceed the bound")
    need(cid, type(run.get("call_phase_seconds")) is int and 0 < run["call_phase_seconds"] <= 1200, "record: call phase over 20 minutes")
    w, s = run.get("days_written"), run.get("days_skipped_existing")
    need(cid, type(w) is int and type(s) is int and w >= 0 and s >= 0 and w + s == stated and w > 0,
         "record: days written plus days skipped as existing must equal the stated partition count")
    need(cid, run.get("zero_returns") == 0 and run.get("keys_outside_feed_prefixes") == 0, "record: a zero return or a key outside the feed's prefixes")
    need(cid, run.get("stored_value") == "daily_factor" and run.get("calc_gross_of_fees_false_on_every_request") is True,
         "record: stored value or fee basis")
    need(cid, run.get("run_objects_written") == 1 and run.get("envelopes_v2_without_responses") is True,
         "record: exactly one run object and every envelope v2 without responses are required")
    need(cid, num(run.get("peak_memory_mb")) and num(run.get("host_memory_limit_mb")) and 0 < run["peak_memory_mb"] < run["host_memory_limit_mb"],
         "record: peak memory must be printed and below the host's limit")
    need(cid, type(run.get("write_phase_seconds")) is int and run["write_phase_seconds"] > 0, "record: write phase time not printed")
    need(cid, run.get("persistent_429") is False and run.get("overwrote_existing_day") is False, "record: a standing 429 or an overwritten day")


def ac3(root):
    cid = "IBN8-AC3"
    rec = load(root, cid)
    ck = rec.get("check", {})
    run = rec.get("run", {})
    need(cid, ck.get("days_read_back") == run.get("days_written"), "record: every written day must be read back")
    accounts = ck.get("accounts")
    need(cid, isinstance(accounts, list) and len(accounts) >= 5, "record: fewer than 5 accounts printed")
    for a in accounts:
        need(cid, isinstance(a, dict) and set(a) == {"window_days", "error_bp"}, "record: each account holds exactly window_days and error_bp")
        need(cid, type(a["window_days"]) is int and 0 < a["window_days"] <= 237, "record: an account's window must be at most 237 days")
        need(cid, num(a["error_bp"]) and 0 <= a["error_bp"] <= 0.5, "record: an account's chained factors differ from the period return by over 0.5 bp")
    need(cid, ck.get("window_named_readable") is False, "record: no window may be named readable by this run")


CHECKS = {"IBN8-AC1": ac1, "IBN8-AC2": ac2, "IBN8-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn8_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
