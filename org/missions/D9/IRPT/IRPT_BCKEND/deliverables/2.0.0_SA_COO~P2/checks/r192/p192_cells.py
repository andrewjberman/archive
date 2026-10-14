"""IRPT_BCKEND round 192 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB192-1  IB-pr-533  the release re-measure HARNESS committed and replayed on pinned inputs, so the signed packet's stop rule is a deterministic comparison (READ ONLY)
    AC1  the harness: a committed Python file that compiles, makes no write call, and uses the producer's own build, rule and gate
    AC2  the replay: two runs per firm agree exactly (movers by layer, gate outcome and conditions, lost accounts listed) on a pinned source date; each firm compared with the signed packet's numbers with its deviations named; the first-fire business-date check recomputed against the trading calendar
    AC3  the record's honesty: a note per firm, no client identifier, no long digit run, uploaded false and the six bound counters 0
  IB192-2  IB-pr-534  49financial's missing 2026-10-08: why a long fire exceeds the SSM execution timeout (the numbers) and the one-date replay packet (READ ONLY)
    AC1  the timeout and the fires: the timeout values with their sources, the ten or more latest 49financial fires with start, end and duration, and their statistics recomputed
    AC2  the replay: what it writes, that every other date is untouched, the gate's answer to an older date, the route it therefore needs, and the rollback
    AC3  the packet and the counters: the one-date replay packet (both halves unsigned, ordered after the release's after-read), no client identifier, no long digit run, the six bound counters 0
"""
import json
import py_compile
import re
import statistics
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
HARNESS = D + "0.9.0_WK_IRPT_BCKEND~380/release_count_harness.py"
REC1 = D + "0.9.0_WK_IRPT_BCKEND~380/IB192-1_replay_record.json"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~381/IB192-2_timeout_and_replay.json"
PACKET2 = D + "0.9.0_WK_IRPT_BCKEND~381/ONE_DATE_REPLAY_PACKET_49F_20261008.md"
BOUND = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
FIRMS = ["49financial", "cottonwood", "inflection"]
PACKET_NUMBERS = {"49financial": (32, 0, "PUBLISHED", "PUBLISHED", 0), "cottonwood": (38, 211, "REFUSED", "PUBLISHED", 1), "inflection": (774, 67, "PUBLISHED", "PUBLISHED", 0)}
FORBIDDEN = re.compile(r"put_object|copy_object|delete_object|upload_file|upload_fileobj|send_command|\.invoke\(|invoke_function|publish_client|\.land\(|run_firm|start_execution|update_function|put_item|delete_item|update_item")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB192"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def no_long_digits(txt):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", txt):
        fail("a long digit run (an identifier or a figure) is present")


def counters(r):
    for k in BOUND:
        if r.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))


def harness_ac1():
    f = ROOT / HARNESS
    if not f.is_file():
        fail("no %s" % HARNESS)
    src = f.read_text(encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory() as td:
            py_compile.compile(str(f), cfile=str(Path(td) / "h.pyc"), doraise=True)
    except py_compile.PyCompileError as e:
        fail("the harness does not compile: %s" % e)
    bad = sorted(set(FORBIDDEN.findall(src)))
    if bad:
        fail("the harness must make no write, publish or invoke call; found %s" % bad)
    for tok in ("build_snapshot", "apply_cash_rule", "evaluate_publish_gate", "as_of", "directory_marks_no_closures", "VersionedInputs"):
        if tok not in src:
            fail("the harness must use the producer's own %s" % tok)
    print("OK: harness compiles, read-only by its text, uses the producer's functions")


def replay_ac2():
    r = load(REC1)
    firms = r.get("firms") or {}
    if sorted(firms) != FIRMS:
        fail("firms must hold exactly the three firms")
    for k, v in firms.items():
        a, b = v.get("run_a"), v.get("run_b")
        if not (isinstance(a, dict) and isinstance(b, dict)):
            fail("%s: run_a and run_b are required" % k)
        if not is_date(v.get("pinned_source_date")):
            fail("%s: pinned_source_date (the candidate's source date both runs were pinned to) is required" % k)
        for run in (a, b):
            for key in ("movers_canonical", "movers_fallback", "lost_accounts_listed_after"):
                if not (is_int(run.get(key)) and run[key] >= 0):
                    fail("%s: %s must be an integer >= 0 in both runs" % (k, key))
            for key in ("gate_before", "gate_after"):
                if run.get(key) not in ("PUBLISHED", "REFUSED"):
                    fail("%s: %s must be PUBLISHED or REFUSED" % (k, key))
            if not isinstance(run.get("conditions_after"), list) or not isinstance(run.get("conditions_before"), list):
                fail("%s: conditions_before and conditions_after must be lists" % k)
        if a != b:
            fail("%s: the two runs must agree exactly (a replay on pinned inputs is deterministic)" % k)
        if not re.fullmatch(r"[0-9a-f]{64}", str(v.get("receipts_digest", ""))):
            fail("%s: receipts_digest must be a 64-hex digest of the pinned source receipts" % k)
        can, fb, gb, ga, listed = PACKET_NUMBERS[k]
        got = (a["movers_canonical"], a["movers_fallback"], a["gate_before"], a["gate_after"], a["lost_accounts_listed_after"])
        dev = [n for n, x, y in zip(("canonical", "fallback", "gate_before", "gate_after", "listed"), got, PACKET_NUMBERS[k]) if x != y]
        if sorted(v.get("deviations_from_packet", [None])) != sorted(dev) if dev else v.get("deviations_from_packet") != []:
            fail("%s: deviations_from_packet must name exactly the fields that differ from the signed packet (%s)" % (k, dev))
        if v.get("matches_packet") is not (not dev):
            fail("%s: matches_packet must be %s" % (k, not dev))
    fc = r.get("first_fire_check") or {}
    sys.path.insert(0, str(ROOT / "lib"))
    try:
        import trading_calendar as tc
        import datetime as dt
        want = tc.prev_trading_day(dt.date.fromisoformat(str(fc.get("fire_date")))).isoformat()
    except Exception as e:  # noqa: BLE001
        fail("the first_fire_check could not be recomputed against the trading calendar: %s" % e)
    if fc.get("t_minus_1") != want:
        fail("first_fire_check.t_minus_1 must be the calendar's previous trading day of the fire date (%s)" % want)
    cd = fc.get("newest_candidate_dates") or {}
    if sorted(cd) != FIRMS or not all(is_date(x) for x in cd.values()):
        fail("first_fire_check.newest_candidate_dates needs the three firms' source dates")
    if fc.get("all_equal_to_t_minus_1") is not all(x == want for x in cd.values()):
        fail("all_equal_to_t_minus_1 must equal (every newest candidate date == t_minus_1)")
    print("OK: replay deterministic, packet deviations named, first-fire check recomputed")


def honesty1():
    r = load(REC1)
    for k, v in (r.get("firms") or {}).items():
        if not str(v.get("note", "")).strip():
            fail("%s: a note stating what the counts rest on and what was not read is required" % k)
    no_long_digits(json.dumps(r))
    if r.get("uploaded") is not False:
        fail("uploaded must be false")
    counters(r)
    print("OK: honest record")


def timeout_ac1():
    r = load(REC2)
    t = r.get("timeout") or {}
    if not (is_int(t.get("ssm_execution_timeout_seconds")) and t["ssm_execution_timeout_seconds"] > 0 and str(t.get("ssm_source", "")).strip()):
        fail("timeout needs ssm_execution_timeout_seconds (an integer above 0) and its ssm_source")
    dsp = t.get("dispatcher") or {}
    if not (str(dsp.get("function", "")).strip() and is_int(dsp.get("timeout_seconds")) and dsp["timeout_seconds"] > 0):
        fail("timeout.dispatcher needs the function name and its timeout_seconds")
    fires = r.get("fires_49financial")
    if not isinstance(fires, list) or len(fires) < 10:
        fail("fires_49financial needs at least 10 fires")
    durs = []
    for f in fires:
        if not (is_date(f.get("fire_date")) and f.get("status") in ("Success", "Failed", "TimedOut", "Cancelled") and is_num(f.get("duration_seconds")) and f["duration_seconds"] > 0):
            fail("each fire needs fire_date, a status and a duration_seconds above 0")
        durs.append(f["duration_seconds"])
    st = r.get("fire_statistics") or {}
    over = sum(1 for f in fires if f["duration_seconds"] >= t["ssm_execution_timeout_seconds"] or f["status"] == "TimedOut")
    if not (st.get("n") == len(durs) and abs(st.get("min", -1) - min(durs)) < 1 and abs(st.get("max", -1) - max(durs)) < 1
            and abs(st.get("median", -1) - statistics.median(durs)) < 1 and st.get("over_timeout") == over):
        fail("fire_statistics must equal n, min, max, median and over_timeout recomputed from the fires")
    print("OK: timeout values and fire statistics recomputed")


def replay_ac2b():
    r = load(REC2)
    s = r.get("source_for_2026_10_08") or {}
    if not (isinstance(s.get("silver_partitions_present"), bool) and str(s.get("evidence", "")).strip()):
        fail("source_for_2026_10_08 needs silver_partitions_present (true or false) and its evidence")
    p = r.get("replay") or {}
    for key in ("command_shape", "index_effect", "rollback", "route_needed"):
        if not str(p.get(key, "")).strip():
            fail("replay.%s is required" % key)
    if not (isinstance(p.get("writes"), list) and p["writes"] and all(str(x).strip() for x in p["writes"])):
        fail("replay.writes must list the key shapes the replay writes")
    if p.get("leaves_other_dates_untouched") is not True:
        fail("replay.leaves_other_dates_untouched must be true (a replay that touches another date is not this cell)")
    if not isinstance(p.get("gate_refuses_older_date"), bool):
        fail("replay.gate_refuses_older_date must be true or false")
    if p["gate_refuses_older_date"] and not re.search(r"gate|exemption|ruling|pair|operator|bypass|separate", p["route_needed"], re.I):
        fail("when the gate refuses an older date, route_needed must name the route (a ruling, a pair, an operator path)")
    print("OK: replay facts")


def packet_ac3():
    r = load(REC2)
    f = ROOT / PACKET2
    if not f.is_file():
        fail("no %s" % PACKET2)
    txt = f.read_text(encoding="utf-8")
    if len(txt) < 3000:
        fail("the packet must be at least 3,000 characters")
    low = txt.lower()
    for w in ("branch a", "branch b", "blast radius", "rollback", "every other date", "2026-10-08", "coo half", "cto half", "unsigned", "after the release", "source_frontier_older", "ledger"):
        if w not in low:
            fail("the packet must state %r" % w)
    no_long_digits(txt)
    no_long_digits(json.dumps(r))
    counters(r)
    if not (isinstance(r.get("notes"), list) and r["notes"] and all(str(n).strip() for n in r["notes"])):
        fail("notes are required")
    print("OK: packet and counters")


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if cell == "IB192-1":
        {"AC1": harness_ac1, "AC2": replay_ac2, "AC3": honesty1}[arm]()
    elif cell == "IB192-2":
        {"AC1": timeout_ac1, "AC2": replay_ac2b, "AC3": packet_ac3}[arm]()
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
