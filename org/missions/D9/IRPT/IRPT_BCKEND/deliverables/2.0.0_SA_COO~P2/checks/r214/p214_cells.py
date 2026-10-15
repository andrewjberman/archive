"""IRPT_BCKEND workstream ~PE round 2 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: 49 Financial's lost ACTIVE account across the dim_balance partitions (CTO msg 8274).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB214-1  IB-pr-575  the account's presence in the dim_balance partitions 2026-10-08 to 2026-10-14 and the upstream writer's run for 2026-10-13
    AC1  one row per trading day 2026-10-08 to 2026-10-14 (recomputed against the calendar): the partition present, its row count, the account present (id private); the gap located
    AC2  the upstream writer read in the code (file, line, identifier verified), its run for 2026-10-13 (failed, truncated or succeeded, with the row counts around it) and the claim
    AC3  whether the refusal clears on its own (from the 2026-10-14 partition), the remedy named, notes, the six counters 0, no long digit run
"""
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~418/IB214-1_49f_presence_read.json"
CLAIMS = ("measured", "inferred", "absent")
STATUS = ("succeeded", "failed", "truncated", "not_found", "unknown")
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def iso(x, what):
    if not isinstance(x, str) or not re.fullmatch(r"\d{4}-\d\d-\d\d", x):
        fail("%s must be an ISO date" % what)
    try:
        return dt.date.fromisoformat(x)
    except ValueError:
        fail("%s is not a real date" % what)


def calendar():
    f = P6.ROOT / "lib" / "trading_calendar.py"
    if not f.is_file():
        fail("no lib/trading_calendar.py in the tree")
    spec = importlib.util.spec_from_file_location("tcal_p214", str(f))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def site(s, what):
    if not isinstance(s, dict) or not isinstance(s.get("file"), str) or not is_int(s.get("line")) or not isinstance(s.get("identifier"), str) or not s["identifier"]:
        fail("%s: needs file, line and the identifier on that line" % what)
    f = P6.ROOT / s["file"]
    if not f.is_file():
        fail("%s: %s is not in the tree" % (what, s["file"]))
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if not 1 <= s["line"] <= len(lines) or s["identifier"] not in lines[s["line"] - 1]:
        fail("%s: line %s of %s does not hold %r" % (what, s["line"], s["file"], s["identifier"]))


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    iso(r.get("read_date"), "read_date")
    cal = calendar()
    want = [d.isoformat() for d in cal.trading_days_between("2026-10-08", "2026-10-14")]
    rows = r.get("partitions")
    if not isinstance(rows, list) or [x.get("day") for x in rows] != want:
        fail("partitions must hold one row per trading day %s, in order" % ", ".join(want))
    for x in rows:
        if not isinstance(x.get("partition_present"), bool) or not isinstance(x.get("account_present"), bool):
            fail("%s: partition_present and account_present must be booleans" % x["day"])
        if x["partition_present"]:
            if not is_int(x.get("row_count")) or x["row_count"] < 1:
                fail("%s: a present partition needs row_count as a count of at least 1" % x["day"])
        else:
            if x.get("row_count") is not None or x["account_present"]:
                fail("%s: an absent partition has no row_count and no account" % x["day"])
    if r.get("served_snapshot_day") != "2026-10-12" or r.get("candidate_day_refused") != "2026-10-13":
        fail("served_snapshot_day must be 2026-10-12 and candidate_day_refused 2026-10-13")
    byd = {x["day"]: x for x in rows}
    if not byd["2026-10-12"]["account_present"] or byd["2026-10-13"]["account_present"] or not byd["2026-10-13"]["partition_present"]:
        fail("the account must be present on 2026-10-12 and absent from a present 2026-10-13 partition (the finding of IB-pr-573); re-check the read if not")
    gap = r.get("gap")
    if not isinstance(gap, dict) or gap.get("first_absent_day") != "2026-10-13" or gap.get("claim") not in CLAIMS:
        fail("gap needs first_absent_day 2026-10-13 and a claim")
    print("OK: the account across %d trading days located in the partitions" % len(rows))


def c2():
    r = load(REC)
    w = r.get("upstream_writer") or {}
    site(w.get("site"), "upstream_writer.site (the code that writes the dim_balance partition)")
    text(w.get("name"), 10, "upstream_writer.name (the job or function and its owner, no bucket name)")
    run = w.get("run_2026_10_13") or {}
    if run.get("status") not in STATUS or run.get("claim") not in CLAIMS:
        fail("run_2026_10_13 needs a status (%s) and a claim" % "|".join(STATUS))
    rc = run.get("row_counts")
    if not isinstance(rc, dict) or not all(is_int(rc.get(k)) and rc[k] >= 0 for k in ("prior_day", "day", "next_day")):
        fail("run_2026_10_13.row_counts needs prior_day, day and next_day as counts (the partitions' own row counts)")
    if not isinstance(run.get("truncation_signal"), bool):
        fail("run_2026_10_13.truncation_signal must be a boolean (a row count far below its neighbours, a partial file, a failed step)")
    text(run.get("statement"), 60, "run_2026_10_13.statement (what the run evidence says and what it does not, no id)")
    print("OK: the upstream writer read in the code; its 2026-10-13 run %s" % run["status"])


def c3():
    r = load(REC)
    of = r.get("other_files") or {}
    want = ["2026-10-12", "2026-10-13", "2026-10-14"]
    dp = of.get("dim_position")
    if not isinstance(dp, list) or [x.get("day") for x in dp] != want:
        fail("other_files.dim_position needs one row per day %s" % ", ".join(want))
    for x in dp:
        if not isinstance(x.get("partition_present"), bool) or not (x["partition_present"] is False or (is_int(x.get("account_positions")) and x["account_positions"] >= 0)):
            fail("%s: dim_position needs partition_present and, when present, account_positions as a count" % x["day"])
    ft = of.get("fact_trn")
    if not isinstance(ft, list) or [x.get("day") for x in ft] != want:
        fail("other_files.fact_trn needs one row per day %s" % ", ".join(want))
    for x in ft:
        codes = x.get("codes")
        if not is_int(x.get("account_rows")) or x["account_rows"] < 0 or not isinstance(codes, list) or not all(isinstance(c, dict) and all(isinstance(c.get(k), str) and c[k] for k in ("tran_srcde", "tr_cd", "sb_cd")) and is_int(c.get("count")) for c in codes):
            fail("%s: fact_trn needs account_rows and codes as [{tran_srcde, tr_cd, sb_cd, count}] (codes only, no ids)" % x.get("day"))
        if x["account_rows"] != sum(c["count"] for c in codes):
            fail("%s: account_rows must equal the sum of the code counts" % x["day"])
    cl = of.get("classification")
    if cl not in ("closed_at_source", "balance_file_gap", "undetermined"):
        fail("other_files.classification must be closed_at_source, balance_file_gap or undetermined")
    text(of.get("statement"), 60, "other_files.statement (the evidence in words: a closing or transfer-out code or no positions means closed at the source; positions still present means a balance-file gap)")
    if cl == "balance_file_gap":
        text(of.get("balance_writer_owner"), 20, "other_files.balance_writer_owner (name the dim_balance writer and its owner)")
        if not any(x.get("partition_present") and x.get("account_positions", 0) > 0 for x in dp):
            fail("a balance_file_gap needs positions still present in some dim_position day")
    if cl == "closed_at_source" and not (any(c["tr_cd"] for x in ft for c in x["codes"]) or all((not x["partition_present"]) or x.get("account_positions") == 0 for x in dp)):
        fail("closed_at_source needs a closing or transfer-out code in fact_trn, or no positions in dim_position")
    sc = r.get("self_clears") or {}
    if sc.get("claim") not in CLAIMS or not isinstance(sc.get("account_present_on_2026_10_14"), (bool, type(None))):
        fail("self_clears needs a claim and account_present_on_2026_10_14 (boolean, or null when the partition is absent)")
    text(sc.get("statement"), 60, "self_clears.statement")
    rm = r.get("remedy") or {}
    text(rm.get("path"), 40, "remedy.path (return of the row, or a custodian-confirmed TERMINATED mark as a partner-firm contact to draft for Andrew)")
    if not isinstance(rm.get("partner_contact_needed"), bool):
        fail("remedy.partner_contact_needed must be a boolean")
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: whether it clears, the remedy, notes, counters 0")


CHECKS = {"IB214-1-AC1": c1, "IB214-1-AC2": c2, "IB214-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p214_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
