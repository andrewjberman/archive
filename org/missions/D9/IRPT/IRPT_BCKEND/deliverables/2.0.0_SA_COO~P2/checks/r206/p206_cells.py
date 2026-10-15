"""IRPT_BCKEND workstream ~PO round 5 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell on the CTO's Orion ruling @1dca8c9e4d.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB206-1  IB-pr-565  the chain read, the per-feed spans and the T-1 completeness read (no date token on the chain; backfill once with the same pull code plus a date)
    AC1  the chain's three pull steps against the manual_api scripts (invoked or byte-identical, hashes compared; the repo script's sha256 recomputed), the control owed when neither holds, and the silver aggregator's source status (row W404-S5)
    AC2  the denominator recomputed per feed span against lib/trading_calendar.py: trading days in the span, flat present, parquet only and missing partition the span; the missing days listed
    AC3  the T-1 completeness read from the last 20 trading days' pulls per feed (landing time, the as-of field and its day, recomputed against the calendar), the data-ready field, the earliest measured-complete time; the trigger does not move now; notes, counters 0
"""
import datetime as dt
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~409/IB206-1_orion_chain_read.json"
FEEDS = ("positions", "transactions", "performance")
STEPS = {"positions": "INF_API_PULL_POSITIONS_DAILY", "transactions": "INF_API_PULL_TXN", "performance": "INF_API_PULL_PERF"}
CLAIMS = ("measured", "inferred", "absent")
READ_DATE_RE = r"\d{4}-\d\d-\d\d"
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def iso(x, what):
    if not isinstance(x, str) or not re.fullmatch(READ_DATE_RE, x):
        fail("%s must be an ISO date" % what)
    try:
        return dt.date.fromisoformat(x)
    except ValueError:
        fail("%s is not a real date" % what)


def calendar():
    f = P6.ROOT / "lib" / "trading_calendar.py"
    if not f.is_file():
        fail("no lib/trading_calendar.py in the tree: the denominator cannot be recomputed")
    spec = importlib.util.spec_from_file_location("tcal_p206", str(f))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    ci = r.get("chain_invocation")
    if not isinstance(ci, dict) or sorted(ci.get("steps") or {}) != sorted(FEEDS):
        fail("chain_invocation.steps must hold %s" % ", ".join(FEEDS))
    need = False
    for feed, s in ci["steps"].items():
        if s.get("step") != STEPS[feed]:
            fail("%s: step must be %s" % (feed, STEPS[feed]))
        script = s.get("script")
        if not isinstance(script, str) or not script.endswith(".py") or "/" in script:
            fail("%s: script must be the manual_api script's file name" % feed)
        repo = P6.ROOT / "data" / "inf" / "manual_api" / script
        if not repo.is_file():
            fail("%s: data/inf/manual_api/%s is not in the tree" % (feed, script))
        h = hashlib.sha256(repo.read_bytes()).hexdigest()
        if s.get("repo_cli_sha256") != h:
            fail("%s: repo_cli_sha256 is not the sha256 of the script in the tree" % feed)
        c = s.get("chain_copy_sha256")
        if not (isinstance(c, str) and re.fullmatch(r"[0-9a-f]{64}", c)):
            fail("%s: chain_copy_sha256 must be a sha256" % feed)
        if s.get("identical") is not (c == h):
            fail("%s: identical must equal (the chain copy's hash equals the repo script's)" % feed)
        if not isinstance(s.get("invokes_manual_api"), bool):
            fail("%s: invokes_manual_api must be a boolean" % feed)
        text(s.get("evidence"), 40, "%s evidence (the dispatch line number and the identifier on it)" % feed)
        need = need or (not s["invokes_manual_api"] and not s["identical"])
    if ci.get("positive_control_needed") is not need:
        fail("positive_control_needed must be %s (true when a step neither invokes the manual_api script nor runs a byte-identical copy)" % need)
    text(ci.get("positive_control_plan"), 30, "positive_control_plan ('not needed: ..' when no step needs it)")
    text(ci.get("cli_retirement_scope"), 40, "cli_retirement_scope (only a bronze write the chain does not reach is retired)")
    sa = r.get("silver_aggregator")
    if not isinstance(sa, dict) or sa.get("function") != "inf-silver-aggregator":
        fail("silver_aggregator.function must be inf-silver-aggregator")
    if not (isinstance(sa.get("code_sha256_b64"), str) and re.fullmatch(r"[A-Za-z0-9+/]{43}=", sa["code_sha256_b64"])):
        fail("silver_aggregator.code_sha256_b64 must be the live CodeSha256")
    if not isinstance(sa.get("source_in_repo"), bool) or not isinstance(sa.get("source_map_entry"), bool):
        fail("silver_aggregator.source_in_repo and source_map_entry must be booleans")
    if sa["source_in_repo"]:
        rp = sa.get("repo_path")
        if not isinstance(rp, str) or not (P6.ROOT / rp).exists():
            fail("silver_aggregator.repo_path must name a path in the tree")
    elif sa.get("repo_path") is not None:
        fail("silver_aggregator.repo_path must be null when the source is not in the repository")
    text(sa.get("gap_statement"), 40, "silver_aggregator.gap_statement")
    print("OK: the chain's pull steps against the manual_api scripts, the control owed, the silver aggregator's source status")


def c2():
    r = load(REC)
    cal = calendar()
    sp = r.get("spans")
    if not isinstance(sp, dict) or sorted(sp) != sorted(FEEDS):
        fail("spans must hold %s" % ", ".join(FEEDS))
    total = 0
    for feed, s in sp.items():
        a, b = iso(s.get("first_key_day"), feed + ".first_key_day"), iso(s.get("last_key_day"), feed + ".last_key_day")
        if a > b:
            fail("%s: first_key_day after last_key_day" % feed)
        days = [d.isoformat() for d in cal.trading_days_between(a, b)]
        if s.get("trading_days_in_span") != len(days):
            fail("%s: trading_days_in_span is %r; the calendar holds %d trading days from %s to %s" % (feed, s.get("trading_days_in_span"), len(days), a, b))
        miss = s.get("missing")
        if not isinstance(miss, list) or miss != sorted(set(miss)) or any(x not in days for x in miss):
            fail("%s: missing must be sorted, unique trading days inside the span" % feed)
        if s.get("missing_count") != len(miss):
            fail("%s: missing_count must equal the length of missing" % feed)
        if not (is_int(s.get("flat_present")) and is_int(s.get("parquet_only"))) or s["flat_present"] + s["parquet_only"] + len(miss) != len(days):
            fail("%s: flat_present + parquet_only + missing_count must equal trading_days_in_span (%d)" % (feed, len(days)))
        if not is_int(s.get("keys_listed")) or s["keys_listed"] < s["flat_present"]:
            fail("%s: keys_listed (the denominator of the S3 listing) must be a count of at least flat_present" % feed)
        text(s.get("out_of_span_note"), 20, "%s out_of_span_note (days before the first key are out of span, not missing)" % feed)
        total += len(miss)
    if r.get("absent_total") != total:
        fail("absent_total must equal the sum of the three missing lists (%d)" % total)
    print("OK: the denominator recomputed per feed span, %d absent trading days in all" % total)


def c3():
    r = load(REC)
    cal = calendar()
    rd = iso(r.get("read_date"), "read_date")
    end = cal.prev_trading_day(rd)
    want = [d.isoformat() for d in cal.trading_days_between(end - dt.timedelta(days=45), end)][-20:]
    t1 = r.get("t1_completeness")
    if not isinstance(t1, dict) or sorted(t1.get("feeds") or {}) != sorted(FEEDS):
        fail("t1_completeness.feeds must hold %s" % ", ".join(FEEDS))
    all_ok = True
    for feed, rows in t1["feeds"].items():
        if not isinstance(rows, list) or [x.get("day") for x in rows] != want:
            fail("%s: the rows must be the last 20 trading days up to %s, in order" % (feed, end))
        present = 0
        for x in rows:
            if x.get("key_present") is False:
                if x.get("landed_at_utc") is not None or x.get("asof_day") is not None:
                    fail("%s %s: a day with no flat key carries no landing time and no as-of day" % (feed, x.get("day")))
                continue
            present += 1
            if not (isinstance(x.get("landed_at_utc"), str) and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", x["landed_at_utc"])) or x["landed_at_utc"][:10] != x["day"]:
                fail("%s %s: landed_at_utc must be an ISO UTC time on the key's day" % (feed, x.get("day")))
            if not isinstance(x.get("asof_field"), str) or not x["asof_field"]:
                fail("%s %s: asof_field must name the field read inside the pulled content" % (feed, x["day"]))
            ad = iso(x.get("asof_day"), "%s %s asof_day" % (feed, x["day"]))
            ok = ad == cal.prev_trading_day(dt.date.fromisoformat(x["day"]))
            if x.get("asof_is_prior_trading_day") is not ok:
                fail("%s %s: asof_is_prior_trading_day must be %s (as-of %s against the calendar)" % (feed, x["day"], ok, ad))
            all_ok = all_ok and ok
        if present < 12 and r.get("earliest_measured_complete", {}).get("claim") == "measured":
            fail("%s: a measured claim needs at least 12 of the 20 days to hold a flat key (found %d)" % (feed, present))
    dr = r.get("data_ready_field")
    if not isinstance(dr, dict) or not isinstance(dr.get("found"), bool) or (dr["found"] and not dr.get("name")):
        fail("data_ready_field must state found true with the name, or found false")
    text(dr.get("note"), 20, "data_ready_field.note")
    e = r.get("earliest_measured_complete")
    if not isinstance(e, dict) or e.get("claim") not in CLAIMS or not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", str(e.get("clock_ny"))):
        fail("earliest_measured_complete needs a claim (%s) and clock_ny as HH:MM" % "|".join(CLAIMS))
    text(e.get("reason"), 40, "earliest_measured_complete.reason")
    if e["claim"] == "measured" and not all_ok:
        fail("a measured completeness claim needs every as-of day equal to the prior trading day; some do not")
    if r.get("trigger_moves_now") is not False:
        fail("trigger_moves_now must be false: the trigger does not move until the completeness is read (CTO ruling)")
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters (what each fact rests on, what was not read, the objects read counted, never a value)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the T-1 completeness read over %d trading days per feed; the trigger does not move" % len(want))


CHECKS = {"IB206-1-AC1": c1, "IB206-1-AC2": c2, "IB206-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p206_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
