"""IRPT_DASHBD round 110 (issuer 2.0.0_SA_COO~D2) -- the two reads of the CTO's ROUND-110 ANALYSIS (section 2 cell 3).

  DB110-5-AC1 (~177)  READ (a): is the Black Diamond holdings file's date the close the holdings reflect, or the day it was pulled?
                      Record: deliverables/0.9.0_WK_IRPT_DASHBD~177/RD_BD_DATE_R110.json
  DB110-6-AC1 (~178)  READ (b): Cottonwood's holdings_performance_daily: producer, schedule (DESIRED vs APPLIED), input frontier,
                      what a scheduled fire needs, and who writes Cottonwood's irpt holdings.
                      Record: deliverables/0.9.0_WK_IRPT_DASHBD~178/RD_COTTONWOOD_PRODUCER_R110.json

The checker grades FORM and INTERNAL CONSISTENCY only (a read's truth is the reader's and the CTO's), plus ONE independent offline re-measure:
the Cottonwood record's trading_days_behind is recomputed from lib/trading_calendar.py. Offline, stdlib only, terminates in seconds.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms
"""
import importlib.util
import io
import json
import re
import sys
import contextlib
import datetime as dt
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC5 = D + "0.9.0_WK_IRPT_DASHBD~177/RD_BD_DATE_R110.json"
REC6 = D + "0.9.0_WK_IRPT_DASHBD~178/RD_COTTONWOOD_PRODUCER_R110.json"
CLAIMS = ("measured", "inferred", "held", "absent")
MEANS = ("CLOSE_DATE", "PULL_DATE", "MIXED", "UNDETERMINED")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "scope_words")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "the record %s does not exist" % rel)
    try:
        return json.loads(p.read_bytes().decode("utf-8"))
    except Exception as e:
        raise Fail("the record %s is not UTF-8 JSON (%s)" % (rel, type(e).__name__))


def claim_ok(obj, where):
    need(isinstance(obj, dict) and obj.get("claim") in CLAIMS, "%s must carry a claim field of %s" % (where, "/".join(CLAIMS)))


def digit_runs(x, key=""):
    """paths of every string holding a run of 8 or more digits outside the allowed key fields."""
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += digit_runs(v, k)
    elif isinstance(x, list):
        for v in x:
            out += digit_runs(v, key)
    elif isinstance(x, str) and key not in DIGIT_OK_KEYS and LONG_DIGITS.search(x):
        out.append(key)
    return out


def zero_effects(r):
    rd = r.get("reads")
    need(isinstance(rd, dict) and all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads")), "reads must hold vendor_calls, s3_writes, dynamodb_writes and secret_reads all 0")
    need(is_int(rd.get("s3_reads")) and rd["s3_reads"] >= 0, "reads.s3_reads must be an integer")
    need(r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False and r.get("files_in_repo") is False, "served_values_changed, pushed, deployed and files_in_repo must be false")
    need(not digit_runs(r), "the record holds a run of 8 or more digits outside a sha256, path, file, key, where or vintage field: %s" % digit_runs(r))


def positive_control(r):
    pc = r.get("positive_control")
    need(isinstance(pc, dict) and nes(pc.get("description")) and nes(pc.get("expected")) and nes(pc.get("observed")) and pc.get("passed") is True,
         "positive_control must hold description, expected, observed (words) and passed true")


# ------------------------------------------------------------------ DB110-5-AC1
def check_bd(r):
    need(isinstance(r, dict), "the record is not an object")
    a = r.get("answer")
    need(isinstance(a, dict) and a.get("holdings_date_means") in MEANS and nes(a.get("words")), "answer must hold holdings_date_means (%s) and words" % "/".join(MEANS))
    claim_ok(a, "answer")
    ev = r.get("evidence")
    need(isinstance(ev, dict), "evidence must be an object")
    cs = ev.get("date_carriers")
    need(isinstance(cs, list) and len(cs) >= 2 and all(isinstance(c, dict) and nes(c.get("surface")) and nes(c.get("carries")) for c in cs), "evidence.date_carriers must list at least 2 {surface, carries, claim} entries (which file, key or column carries which date)")
    for i, c in enumerate(cs):
        claim_ok(c, "evidence.date_carriers[%d]" % i)
    den = ev.get("denominator")
    need(isinstance(den, dict) and is_int(den.get("dated_files")) and den["dated_files"] >= 1 and nes(den.get("scope_words")), "evidence.denominator must hold dated_files (>= 1) and scope_words")
    fc = ev.get("files_compared")
    need(is_int(fc) and 1 <= fc <= den["dated_files"], "evidence.files_compared must be an integer from 1 to denominator.dated_files (%r of %r)" % (fc, den["dated_files"]))
    need(nes(ev.get("offset_definition")), "evidence.offset_definition must say in words what an offset of 0 and of 1 mean")
    dist = ev.get("offset_distribution_days")
    need(isinstance(dist, dict) and dist and all(re.fullmatch(r"-?\d+", str(k)) and is_int(v) and v >= 0 for k, v in dist.items()), "evidence.offset_distribution_days must map an integer offset (as text) to a count")
    es = ev.get("offset_estimates")
    need(is_int(es) and es >= 4, "evidence.offset_estimates must be an integer of at least 4 (one offset estimate per security series compared with the independent series)")
    need(sum(dist.values()) == es, "the offset counts sum to %d, not offset_estimates %d" % (sum(dist.values()), es))
    claim_ok(ev, "evidence")
    z = dist.get("0", 0) / float(es)
    m = a["holdings_date_means"]
    if m == "CLOSE_DATE":
        need(z >= 0.8, "the answer says CLOSE_DATE but only %.0f%% of the offset estimates sit at offset 0 (80%% needed)" % (100 * z))
    elif m == "PULL_DATE":
        need(z <= 0.2, "the answer says PULL_DATE but %.0f%% of the offset estimates sit at offset 0 (20%% at most)" % (100 * z))
    elif m == "MIXED":
        need(0.2 < z < 0.8, "the answer says MIXED but %.0f%% of the offset estimates sit at offset 0 (between 20%% and 80%% needed)" % (100 * z))
    else:
        need(a["claim"] in ("held", "absent"), "UNDETERMINED must carry the claim held or absent")
    positive_control(r)
    ct = r.get("citation_today")
    need(isinstance(ct, dict) and nes(ct.get("file")) and is_int(ct.get("line")) and ct["line"] >= 1 and nes(ct.get("takes_date_from")) and nes(ct.get("words")), "citation_today must hold file, line, takes_date_from and words (where the holdings citation takes its date today)")
    claim_ok(ct, "citation_today")
    cq = r.get("consequence")
    need(isinstance(cq, dict) and isinstance(cq.get("citation_must_change"), bool) and nes(cq.get("words")), "consequence must hold citation_must_change (true or false) and words")
    if m == "PULL_DATE":
        need(cq["citation_must_change"] is True, "the answer says PULL_DATE, so the citation must carry the holdings' own date: citation_must_change must be true")
    if m == "CLOSE_DATE":
        need(cq["citation_must_change"] is False, "the answer says CLOSE_DATE, so the citation stands: citation_must_change must be false")
    zero_effects(r)


def run_bd(root):
    r = load(root, REC5)
    check_bd(r)
    root_p = Path(root)
    need((root_p / r["citation_today"]["file"]).is_file(), "citation_today.file %s is not a file of the repo at this checkout" % r["citation_today"]["file"])
    print("OK: the Black Diamond holdings date reads %s over %d of %d dated files (offset 0: %d); %d date carriers named; the citation is read at its file and line; %s"
          % (r["answer"]["holdings_date_means"], r["evidence"]["files_compared"], r["evidence"]["denominator"]["dated_files"], r["evidence"]["offset_distribution_days"].get("0", 0),
             len(r["evidence"]["date_carriers"]), "the citation must change" if r["consequence"]["citation_must_change"] else "the citation stands"))


# ------------------------------------------------------------------ DB110-6-AC1
def load_calendar(root):
    p = Path(root) / "lib" / "trading_calendar.py"
    need(p.is_file(), "lib/trading_calendar.py is missing at this checkout")
    spec = importlib.util.spec_from_file_location("tcal_p110", str(p))
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        spec.loader.exec_module(m)
    return m


def iso(x, where):
    need(isinstance(x, str) and ISO.fullmatch(x), "%s must be an ISO date YYYY-MM-DD" % where)
    return dt.date.fromisoformat(x)


def check_cot(r, cal):
    need(isinstance(r, dict), "the record is not an object")
    pr = r.get("producer")
    need(isinstance(pr, dict) and nes(pr.get("file")) and nes(pr.get("entry")) and pr.get("channel") == "blackdiamond_z09" and pr.get("table") == "holdings_performance_daily", "producer must hold file, entry, channel 'blackdiamond_z09' and table 'holdings_performance_daily'")
    claim_ok(pr, "producer")
    sc = r.get("schedule")
    need(isinstance(sc, dict) and nes(sc.get("why_none")) or (isinstance(sc, dict) and nes(sc.get("why_scheduled"))), "schedule must say why there is no schedule (why_none) or why one runs (why_scheduled)")
    for side in ("desired", "applied"):
        s = sc.get(side)
        need(isinstance(s, dict) and isinstance(s.get("exists"), bool) and nes(s.get("where")), "schedule.%s must hold exists (true or false) and where (words or a carrier path)" % side)
        claim_ok(s, "schedule.%s" % side)
    need(sc["applied"].get("plane") in ("served_graph", "live_describe"), "schedule.applied.plane must be served_graph or live_describe (the plane the applied state was read from)")
    claim_ok(sc, "schedule")
    fr = r.get("frontier")
    need(isinstance(fr, dict), "frontier must be an object")
    meas = iso(fr.get("measured_on"), "frontier.measured_on")
    ng = iso(fr.get("newest_gold_date"), "frontier.newest_gold_date")
    ni = iso(fr.get("newest_input_date"), "frontier.newest_input_date")
    t1 = iso(fr.get("t_minus_1"), "frontier.t_minus_1")
    need(t1 == cal.prev_trading_day(meas), "frontier.t_minus_1 must be the trading day before measured_on (the calendar says %s)" % cal.prev_trading_day(meas))
    need(ng <= t1 and ni <= t1, "a frontier date is later than T-1")
    need(ng <= ni, "the newest gold date is later than the newest input date it was built from")
    tdb = fr.get("trading_days_behind")
    need(is_int(tdb) and tdb == cal.trading_days_behind(ng, t1), "frontier.trading_days_behind must equal the calendar's count from newest_gold_date to t_minus_1 (the checker recomputes %d)" % cal.trading_days_behind(ng, t1))
    need(nes(fr.get("calendar_source")), "frontier.calendar_source must name the calendar used")
    claim_ok(fr, "frontier")
    nf = r.get("scheduled_fire_needs")
    need(isinstance(nf, list) and len(nf) >= 1 and all(isinstance(x, dict) and nes(x.get("need")) for x in nf), "scheduled_fire_needs must list at least one {need, claim}")
    for i, x in enumerate(nf):
        claim_ok(x, "scheduled_fire_needs[%d]" % i)
    w = r.get("irpt_holdings_writer")
    need(isinstance(w, dict) and nes(w.get("who_writes")), "irpt_holdings_writer must hold who_writes (words)")
    iso(w.get("newest_date"), "irpt_holdings_writer.newest_date")
    claim_ok(w, "irpt_holdings_writer")
    den = r.get("denominator")
    need(isinstance(den, dict) and is_int(den.get("nodes_scanned")) and den["nodes_scanned"] >= 1 and nes(den.get("vintage")) and nes(den.get("scope_words")), "denominator must hold nodes_scanned (>= 1), vintage and scope_words (what the schedule read looked through)")
    positive_control(r)
    rd = r.get("reads") or {}
    need(is_int(rd.get("aws_reads")) and rd["aws_reads"] >= 0 and rd.get("aws_writes") == 0 and rd.get("terraform_apply") == 0, "reads must hold aws_reads (integer), aws_writes 0 and terraform_apply 0")
    zero_effects(r)


def run_cot(root):
    r = load(root, REC6)
    cal = load_calendar(root)
    check_cot(r, cal)
    need((Path(root) / r["producer"]["file"]).is_file(), "producer.file %s is not a file of the repo at this checkout" % r["producer"]["file"])
    fr = r["frontier"]
    print("OK: producer %s read; schedule desired %s, applied %s; newest gold %s is %d trading days behind T-1 %s (the checker's own calendar count agrees); %d scheduled-fire need(s)"
          % (r["producer"]["entry"], r["schedule"]["desired"]["exists"], r["schedule"]["applied"]["exists"], fr["newest_gold_date"], fr["trading_days_behind"], fr["t_minus_1"], len(r["scheduled_fire_needs"])))


# ------------------------------------------------------------------ self-test
def good_bd():
    c = {"claim": "measured"}
    return {"answer": dict(c, holdings_date_means="CLOSE_DATE", words="the partition date is the close the prices reflect"),
            "evidence": dict(c, date_carriers=[dict(c, surface="a", carries="the partition key date"), dict(c, surface="b", carries="the pull time")], files_compared=10, offset_estimates=10,
                             denominator={"dated_files": 20, "scope_words": "the newest 20 partitions"}, offset_definition="0 means the prices equal the partition date's close; 1 means the prior trading day's",
                             offset_distribution_days={"0": 9, "1": 1}),
            "positive_control": {"description": "an anchor known to be a prior-day close", "expected": "offset 1", "observed": "offset 1", "passed": True},
            "citation_today": dict(c, file="portal/src/pages/InvestorReporting/index.tsx", line=429, takes_date_from="businessAsOf", words="the header reads the snapshot's business date"),
            "consequence": {"citation_must_change": False, "words": "the citation stands"},
            "reads": {"vendor_calls": 0, "s3_writes": 0, "dynamodb_writes": 0, "secret_reads": 0, "s3_reads": 5},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}


def good_cot(cal):
    c = {"claim": "measured"}
    return {"producer": dict(c, file="data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py", entry="main", channel="blackdiamond_z09", table="holdings_performance_daily"),
            "schedule": dict(c, why_none="no rule was ever declared", desired=dict(c, exists=False, where="no carrier"), applied=dict(c, exists=False, where="served graph rule list", plane="served_graph")),
            "frontier": dict(c, measured_on="2026-10-14", t_minus_1="2026-10-13", newest_gold_date="2026-09-25", newest_input_date="2026-09-27", trading_days_behind=cal.trading_days_behind("2026-09-25", "2026-10-13"), calendar_source="lib/trading_calendar.py"),
            "scheduled_fire_needs": [dict(c, need="a declared schedule, an input at T-1")],
            "irpt_holdings_writer": dict(c, who_writes="a named script", newest_date="2026-10-08"),
            "denominator": {"nodes_scanned": 40, "vintage": "served graph built 2026-10-14", "scope_words": "every schedule node of the served graph"},
            "positive_control": {"description": "a known scheduled producer is found", "expected": "found", "observed": "found", "passed": True},
            "reads": {"vendor_calls": 0, "s3_writes": 0, "dynamodb_writes": 0, "secret_reads": 0, "s3_reads": 0, "aws_reads": 2, "aws_writes": 0, "terraform_apply": 0},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}


def selftest(root):
    cal = load_calendar(root)
    arms = 0

    def must_fail(fn, rec, why):
        nonlocal arms
        try:
            fn(rec)
        except Fail:
            arms += 1
            return
        raise SystemExit("SELFTEST FAIL: not refused: %s" % why)

    check_bd(good_bd())
    check_cot(good_cot(cal), cal)
    b = good_bd()
    b["answer"]["claim"] = "sure"
    must_fail(check_bd, b, "a claim outside the enum")
    b = good_bd()
    b["evidence"]["offset_distribution_days"] = {"0": 3, "1": 1}
    must_fail(check_bd, b, "offset counts that do not sum to files_compared")
    b = good_bd()
    b["answer"]["holdings_date_means"] = "PULL_DATE"
    must_fail(check_bd, b, "PULL_DATE over a distribution at offset 0")
    b = good_bd()
    b["consequence"]["citation_must_change"] = True
    must_fail(check_bd, b, "CLOSE_DATE with a changed citation")
    b = good_bd()
    b["positive_control"]["passed"] = False
    must_fail(check_bd, b, "a failed positive control")
    b = good_bd()
    b["evidence"]["date_carriers"][0]["carries"] = "account 12345678901"
    must_fail(check_bd, b, "an identifier-length digit run")
    c = good_cot(cal)
    c["frontier"]["trading_days_behind"] += 1
    must_fail(lambda r: check_cot(r, cal), c, "a trading_days_behind the calendar disagrees with")
    c = good_cot(cal)
    del c["schedule"]["applied"]["plane"]
    must_fail(lambda r: check_cot(r, cal), c, "no plane for the applied schedule state")
    c = good_cot(cal)
    c["denominator"]["nodes_scanned"] = 0
    must_fail(lambda r: check_cot(r, cal), c, "an empty denominator")
    print("OK: selftest %d refusal arms and 2 passing arms" % arms)


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(argv[2] if len(argv) > 2 else ".")
        return 0
    if len(argv) != 3:
        print("usage: p110_reads.py <repo_root> <criterion_id> | --selftest [<repo_root>]")
        return 2
    root, cid = argv[1], argv[2]
    fns = {"DB110-5-AC1": run_bd, "DB110-6-AC1": run_cot}
    if cid not in fns:
        print("unknown criterion %s" % cid)
        return 2
    try:
        fns[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
