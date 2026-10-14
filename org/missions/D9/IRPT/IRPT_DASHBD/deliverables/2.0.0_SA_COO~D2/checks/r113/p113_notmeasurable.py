"""IRPT_DASHBD round 113 (issuer 2.0.0_SA_COO~D2) -- DB-b-229, the NOT_MEASURABLE read (CTO round-113 analysis @1513e35eae).

  DB-b-229 (~184) the account_return_daily NOT_MEASURABLE rows of 2026-04-21 by the producer's reason codes and the input that is null, whether 2026-04-21 is a trading day in
                  lib/trading_calendar.py AND in the producer's own calendar, the next five dates by households broken, and every cause's share of round 112's 56,311 unmeasured
                  account-days. A READ: nothing is written.                                                                                       DB113-1-AC1

The checker grades FORM and INTERNAL CONSISTENCY, and RECOMPUTES from the private round-111 household table: the households broken on 2026-04-21 and on every later date, the five
highest dates after 2026-04-21, the library calendar's answer for 2026-04-21, and round 112's total from the merged record.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~184/RD_NOT_MEASURABLE_R113.json"
R112_REL = D + "0.9.0_WK_IRPT_DASHBD~183/RD_HOUSEHOLD_NONE_CAUSE_R112.json"
TABLE = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~179/household_return_daily.parquet"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~184/not_measurable_read_r113.py"
DAY = "2026-04-21"
CLAIMS = ("measured", "inferred", "held", "absent")
GUARDS = ("GRADED_AGREED", "GRADED_DISAGREED", "NOT_GRADED_OUTSIDE_DOMAIN", "NOT_GRADED_NO_NEIGHBOUR", "GUARD_NOT_REACHED")
NM_CODES = ("LINK_BREAK_BASE_ABSENT", "LINK_BREAK_BASE_NONPOSITIVE", "INELIGIBLE_AFTER_COMPUTE", "OTHER")
ALL_CODES = NM_CODES + ("NO_ROW",) + tuple("FLOW_UNRECONCILED:" + g for g in GUARDS)
INPUTS = ("price", "position", "flow", "calendar", "prior_value", "other")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item", "update_item", "write_table", "to_parquet")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "scope_words", "table_sha256")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


# ---------------------------------------------------------------- the recount from the private table (independent of the worker)
def broken_by_date(table):
    """date -> the number of households with an ACCOUNT_MISSING day on it."""
    seen = {}
    for h, t, q in zip(table["household_id"], table["business_date"], table["day_quality"]):
        if q == "ACCOUNT_MISSING":
            seen.setdefault(t, set()).add(h)
    return {t: len(v) for t, v in seen.items()}


def top_after(counts, day, n=5):
    rows = sorted(((c, t) for t, c in counts.items() if t > day), key=lambda x: (-x[0], x[1]))
    return [(t, c) for c, t in rows[:n]]


def load_table():
    need(Path(TABLE).is_file(), "the private round-111 household table is missing: %s" % TABLE)
    import pyarrow.parquet as pq
    return pq.read_table(TABLE, columns=["household_id", "business_date", "day_quality"]).to_pydict()


def lib_is_trading_day(root, day):
    sys.path.insert(0, str(Path(root) / "lib"))
    import trading_calendar as tc
    return bool(tc.is_trading_day(day))


# ---------------------------------------------------------------- the record
def check_split(x, total_key, label):
    need(isinstance(x.get("by_reason_code"), dict) and all(k in NM_CODES + ("NO_ROW",) + tuple("FLOW_UNRECONCILED:" + g for g in GUARDS) and is_int(v) and v >= 0 for k, v in x["by_reason_code"].items()),
         "%s.by_reason_code must map the producer's reason codes %s to counts" % (label, list(ALL_CODES)))
    need(sum(x["by_reason_code"].values()) == x[total_key], "%s.by_reason_code must sum to %s (%r)" % (label, total_key, x[total_key]))
    need(isinstance(x.get("by_null_input"), dict) and all(k in INPUTS and is_int(v) and v >= 0 for k, v in x["by_null_input"].items()), "%s.by_null_input must map %s to counts" % (label, list(INPUTS)))
    need(sum(x["by_null_input"].values()) == x[total_key], "%s.by_null_input must sum to %s (%r)" % (label, total_key, x[total_key]))
    need(x.get("claim") in CLAIMS, "%s must carry a claim in %s" % (label, list(CLAIMS)))


def check_record(r, root=None, table=None, r112=None, lib_answer=None):
    need(isinstance(r, dict), "the record is not an object")
    counts = broken_by_date(table) if table is not None else None
    if table is not None:
        need(r.get("as_of") == max(table["business_date"]), "as_of must equal the newest date of the private table (%s)" % max(table["business_date"]))
    need(ISO.match(str(r.get("as_of"))), "as_of must be an ISO date")
    d = r.get("date_0421")
    need(isinstance(d, dict) and d.get("date") == DAY and is_int(d.get("rows_not_measurable")) and d["rows_not_measurable"] >= 0 and is_int(d.get("households_broken")) and d["households_broken"] >= 0, "date_0421 must hold date %s, rows_not_measurable and households_broken (integers)" % DAY)
    check_split(d, "rows_not_measurable", "date_0421")
    if counts is not None:
        need(d["households_broken"] == counts.get(DAY, 0), "date_0421.households_broken %r must equal the checker's recount from the private table (%d)" % (d["households_broken"], counts.get(DAY, 0)))
    cal = r.get("calendars")
    need(isinstance(cal, dict) and cal.get("date") == DAY and isinstance(cal.get("lib_trading_calendar_is_trading_day"), bool), "calendars must hold date %s and a boolean lib_trading_calendar_is_trading_day" % DAY)
    if lib_answer is not None:
        need(cal["lib_trading_calendar_is_trading_day"] == lib_answer, "calendars.lib_trading_calendar_is_trading_day must equal lib/trading_calendar.py's answer (%r)" % lib_answer)
    pc = cal.get("producer_calendar_is_trading_day")
    need(pc is None or isinstance(pc, bool), "calendars.producer_calendar_is_trading_day must be true, false or null")
    need(nes(cal.get("producer_calendar_note")), "calendars.producer_calendar_note must say in words how the producer's day was found (or why it could not be)")
    src = cal.get("producer_calendar_source")
    need(isinstance(src, dict) and nes(src.get("file")) and is_int(src.get("line")) and src["line"] >= 1 and nes(src.get("words")), "calendars.producer_calendar_source must hold file, line and words")
    if root is not None:
        need((Path(root) / src["file"]).is_file(), "calendars.producer_calendar_source.file %s is not a file of the checkout" % src["file"])
    need(cal.get("agree") == (pc is not None and pc == cal["lib_trading_calendar_is_trading_day"]), "calendars.agree must be true only when both calendars answer and are equal")
    g = cal.get("gold_rows_by_date")
    need(isinstance(g, dict) and set(g.keys()) == {"2026-04-20", DAY, "2026-04-22"} and all(is_int(v) and v >= 0 for v in g.values()), "calendars.gold_rows_by_date must hold 2026-04-20, 2026-04-21 and 2026-04-22 as row counts")
    need(cal.get("claim") in CLAIMS, "calendars must carry a claim")
    nf = r.get("next_five")
    need(isinstance(nf, list) and len(nf) == 5, "next_five must hold exactly 5 dates")
    for i, x in enumerate(nf):
        need(isinstance(x, dict) and ISO.match(str(x.get("date"))) and x["date"] > DAY and is_int(x.get("households_broken")) and is_int(x.get("rows_not_measurable")) and x["rows_not_measurable"] >= 0, "next_five[%d] must hold a date after %s, households_broken and rows_not_measurable" % (i, DAY))
        check_split(x, "rows_not_measurable", "next_five[%d]" % i)
    if counts is not None:
        want = top_after(counts, DAY)
        got = [(x["date"], x["households_broken"]) for x in nf]
        need(got == want, "next_five must be the five dates after %s with the most households broken, descending (ties by the earlier date), counts as the checker recounts them: %s" % (DAY, want))
    sh = r.get("shares")
    need(isinstance(sh, dict) and is_int(sh.get("total_unmeasured_account_days")) and sh["total_unmeasured_account_days"] > 0 and sh.get("claim") in CLAIMS, "shares must hold total_unmeasured_account_days and a claim")
    if r112 is not None:
        need(sh["total_unmeasured_account_days"] == r112["unmeasured_account_days"]["total"], "shares.total_unmeasured_account_days must equal round 112's total (%r)" % r112["unmeasured_account_days"]["total"])
    bc = sh.get("by_cause")
    need(isinstance(bc, list) and len(bc) >= 1, "shares.by_cause must list at least one cause")
    seen = set()
    for i, c in enumerate(bc):
        need(isinstance(c, dict) and nes(c.get("cause")) and is_int(c.get("count")) and c["count"] >= 0 and isinstance(c.get("share"), float), "shares.by_cause[%d] must hold cause, count (integer) and share (float)" % i)
        code, _, inp = c["cause"].partition("/")
        need(code in ALL_CODES and (inp in INPUTS or (code == "NO_ROW" and inp == "calendar or position")), "shares.by_cause[%d].cause %r must be '<producer reason code>/<null input>' (codes %s; inputs %s; a day with no row reads 'NO_ROW/calendar or position')" % (i, c["cause"], list(ALL_CODES), list(INPUTS)))
        need(c["cause"] not in seen, "shares.by_cause repeats the cause %r" % c["cause"])
        seen.add(c["cause"])
        need(abs(c["share"] - round(c["count"] / float(sh["total_unmeasured_account_days"]), 4)) <= 1e-4, "shares.by_cause[%d].share must be count over the total to 4 decimals" % i)
    need(sum(c["count"] for c in bc) == sh["total_unmeasured_account_days"], "shares.by_cause counts must sum to the total (%d)" % sh["total_unmeasured_account_days"])
    need(abs(sum(c["share"] for c in bc) - 1.0) <= 0.001, "shares.by_cause shares must sum to 1.0 within 0.001")
    need([c["count"] for c in bc] == sorted((c["count"] for c in bc), reverse=True), "shares.by_cause must be sorted by count, largest first")
    pr = r.get("producer")
    need(isinstance(pr, dict) and nes(pr.get("file")) and nes(pr.get("words")) and isinstance(pr.get("reason_code_sites"), list) and len(pr["reason_code_sites"]) >= 2
         and all(isinstance(x, dict) and nes(x.get("code")) and is_int(x.get("line")) and x["line"] >= 1 for x in pr["reason_code_sites"]), "producer must hold file, words and at least 2 reason_code_sites {code, line}")
    if root is not None:
        need((Path(root) / pr["file"]).is_file(), "producer.file %s is not a file of the checkout" % pr["file"])
    pcn = r.get("positive_control")
    need(isinstance(pcn, dict) and nes(pcn.get("description")) and nes(pcn.get("expected")) and nes(pcn.get("observed")) and pcn.get("passed") is True, "positive_control must hold description, expected, observed and passed true")
    an = r.get("analysis")
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and re.fullmatch(r"[0-9a-f]{64}", str(an.get("sha256"))), "analysis must hold the tracked script %s with its sha256" % ANALYSIS_REL)
    if root is not None:
        p = Path(root) / ANALYSIS_REL
        need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == an["sha256"], "the analysis script must exist and match its recorded sha256")
        src = p.read_text(encoding="utf-8")
        need(not [t for t in FOREIGN if t in src.lower()] and not [t for t in WRITE_TOKENS if t in src], "the analysis script names no other firm's place and holds no write call")
    rd = r.get("reads")
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd["s3_reads"] >= 0 and all(rd.get(k) == 0 for k in ("s3_writes", "dynamodb_writes", "vendor_calls", "secret_reads")), "reads: s3_reads an integer; zero writes, vendor calls and secret reads")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    need(not digit_runs(r), "the record holds a run of 8 or more digits outside a hash, path, file, key, where or vintage field: %s" % digit_runs(r))


def check_all(root):
    r = load(root, REC_REL)
    table = load_table()
    r112 = load(root, R112_REL)
    check_record(r, root, table, r112, lib_is_trading_day(root, DAY))
    print("OK: NOT_MEASURABLE read: %s breaks %d households (recounted); %d NOT_MEASURABLE rows; lib calendar trading day %s, producer calendar %s; next five dates recounted; %d causes share the round-112 total of %d; positive control passed"
          % (DAY, r["date_0421"]["households_broken"], r["date_0421"]["rows_not_measurable"], r["calendars"]["lib_trading_calendar_is_trading_day"], r["calendars"]["producer_calendar_is_trading_day"], len(r["shares"]["by_cause"]), r["shares"]["total_unmeasured_account_days"]))


# ---------------------------------------------------------------- self-test
def synthetic_table():
    rows = []
    for i in range(10):
        rows.append(("H%d" % i, "2026-04-21", "ACCOUNT_MISSING"))
    for i in range(6):
        rows.append(("H%d" % i, "2026-07-02", "ACCOUNT_MISSING"))
    for i in range(6):
        rows.append(("K%d" % i, "2026-06-01", "ACCOUNT_MISSING"))
    for i in range(3):
        rows.append(("H%d" % i, "2026-05-01", "ACCOUNT_MISSING"))
    for i in range(8):
        rows.append(("H%d" % i, "2026-05-02", "ACCOUNT_MISSING"))
    for i in range(2):
        rows.append(("H%d" % i, "2026-05-04", "ACCOUNT_MISSING"))
    rows.append(("H0", "2026-05-05", "MEASURED"))
    rows.append(("H0", "2026-05-06", "ACCOUNT_MISSING"))
    rows.append(("H0", "2026-10-13", "ACCOUNT_MISSING"))
    return {"household_id": [x[0] for x in rows], "business_date": [x[1] for x in rows], "day_quality": [x[2] for x in rows]}


def split(total, a="LINK_BREAK_BASE_ABSENT", b="LINK_BREAK_BASE_NONPOSITIVE"):
    return {"by_reason_code": {a: total - 1, b: 1}, "by_null_input": {"prior_value": total}, "claim": "measured"}


def good_record(table):
    counts = broken_by_date(table)
    nf = []
    for t, c in top_after(counts, DAY):
        x = {"date": t, "households_broken": c, "rows_not_measurable": c + 1}
        x.update(split(c + 1))
        nf.append(x)
    d = {"date": DAY, "rows_not_measurable": 12, "households_broken": counts[DAY]}
    d.update(split(12))
    total = 100
    by = [{"cause": "LINK_BREAK_BASE_ABSENT/prior_value", "count": 60, "share": 0.6}, {"cause": "FLOW_UNRECONCILED:GUARD_NOT_REACHED/flow", "count": 39, "share": 0.39}, {"cause": "NO_ROW/calendar or position", "count": 1, "share": 0.01}]
    return {"as_of": max(table["business_date"]), "date_0421": d,
            "calendars": {"date": DAY, "lib_trading_calendar_is_trading_day": True, "producer_calendar_is_trading_day": True, "producer_calendar_note": "the producer takes its days from lib/trading_calendar.py", "producer_calendar_source": {"file": "x.py", "line": 12, "words": "the producer calls the shared calendar"}, "agree": True,
                          "gold_rows_by_date": {"2026-04-20": 10, DAY: 9, "2026-04-22": 10}, "claim": "measured"},
            "next_five": nf, "shares": {"total_unmeasured_account_days": total, "by_cause": by, "claim": "measured"},
            "producer": {"file": "x.py", "words": "the sites", "reason_code_sites": [{"code": "LINK_BREAK_BASE_ABSENT", "line": 1361}, {"code": "INELIGIBLE_AFTER_COMPUTE", "line": 1134}]},
            "positive_control": {"description": "a synthetic row per branch", "expected": "each lands in its code", "observed": "each landed in its code", "passed": True},
            "analysis": {"file": ANALYSIS_REL, "sha256": "a" * 64, "tracked": True},
            "reads": {"s3_reads": 1143, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}


def selftest():
    arms = []
    table = synthetic_table()
    r112 = {"unmeasured_account_days": {"total": 100}}

    def ok(name, cond):
        arms.append(name)
        if not cond:
            raise Fail("self-test arm failed: " + name)

    def refuses(name, mutate):
        r = good_record(table)
        mutate(r)
        try:
            check_record(r, None, table, r112, True)
        except Fail:
            arms.append(name)
            return
        raise Fail("self-test arm failed (accepted): " + name)
    counts = broken_by_date(table)
    ok("the recount counts the households broken on a date", counts[DAY] == 10 and counts["2026-07-02"] == 6)
    ok("the top five after the day exclude the day, descend and break ties by the earlier date", [t for t, _c in top_after(counts, DAY)] == ["2026-05-02", "2026-06-01", "2026-07-02", "2026-05-01", "2026-05-04"] or [t for t, _c in top_after(counts, DAY)][:3] == ["2026-05-02", "2026-06-01", "2026-07-02"])
    check_record(good_record(table), None, table, r112, True)
    arms.append("a good record passes")
    refuses("a wrong households_broken for the day", lambda r: r["date_0421"].update({"households_broken": 11}))
    refuses("next five not the top five", lambda r: r["next_five"].reverse())
    refuses("next five of the wrong length", lambda r: r["next_five"].pop())
    refuses("by_reason_code not summing to the rows", lambda r: r["date_0421"]["by_reason_code"].update({"OTHER": 5}))
    refuses("a reason code outside the producer's vocabulary", lambda r: r["date_0421"]["by_reason_code"].update({"MADE_UP": 0}))
    refuses("by_null_input outside the precedence list", lambda r: r["date_0421"]["by_null_input"].update({"weather": 0}))
    refuses("the lib calendar answer wrong", lambda r: r["calendars"].update({"lib_trading_calendar_is_trading_day": False, "agree": False}))
    refuses("agree true while the producer calendar is unknown", lambda r: r["calendars"].update({"producer_calendar_is_trading_day": None, "agree": True}))
    refuses("a missing gold partition count", lambda r: r["calendars"]["gold_rows_by_date"].pop("2026-04-22"))
    refuses("the total not equal to round 112", lambda r: r["shares"].update({"total_unmeasured_account_days": 99}))
    refuses("by_cause counts not summing to the total", lambda r: r["shares"]["by_cause"][0].update({"count": 59}))
    refuses("by_cause not sorted by count", lambda r: r["shares"]["by_cause"].reverse())
    refuses("a share that is not count over total", lambda r: r["shares"]["by_cause"][0].update({"share": 0.7}))
    refuses("a cause outside the code/input form", lambda r: r["shares"]["by_cause"][0].update({"cause": "LINK_BREAK_BASE_ABSENT"}))
    refuses("a repeated cause", lambda r: r["shares"]["by_cause"][1].update({"cause": r["shares"]["by_cause"][0]["cause"]}))
    refuses("a producer with one reason site", lambda r: r["producer"]["reason_code_sites"].pop())
    refuses("a failed positive control", lambda r: r["positive_control"].update({"passed": False}))
    refuses("a claim outside the four words", lambda r: r["date_0421"].update({"claim": "guessed"}))
    refuses("a write count above zero", lambda r: r["reads"].update({"s3_writes": 1}))
    refuses("a long digit run", lambda r: r["producer"].update({"words": "household 12345678901 broke"}))
    print("SELFTEST OK: %d arms: %s" % (len(arms), "; ".join(arms)))


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest()
        return 0
    if len(argv) != 3 or argv[2] != "DB113-1-AC1":
        print("usage: p113_notmeasurable.py <repo_root> DB113-1-AC1")
        return 2
    try:
        check_all(Path(argv[1]).resolve())
    except Fail as e:
        print("FAIL: %s" % e)
        print("DB113-1-AC1 FAIL")
        return 1
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, e))
        print("DB113-1-AC1 FAIL")
        return 1
    print("DB113-1-AC1 PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
