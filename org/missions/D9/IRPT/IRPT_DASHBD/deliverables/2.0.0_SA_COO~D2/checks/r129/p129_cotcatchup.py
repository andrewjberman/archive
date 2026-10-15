"""IRPT_DASHBD round 129, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- the ACT 3 order of the signed Cottonwood landing pair (packet revision 2, sha256 a1b080c5fe06...): explicit
`days` events of at most 25 trading days each, naming ONLY days after 2026-07-10 that have BOTH Black Diamond silver tables, oldest first, one synchronous invocation and one after-read
per event, the schedule left DISABLED and the ledger left OPEN. Written BEFORE Act 2 has run, so that the order can be cut the moment the issuer has read Act 2's record; it grades
nothing until its record exists.

  the Act 3 order (0.7.0_AE_CloudOps~DB2)  DBD129-1-AC1 (the record: gates, the event list against a fresh silver recount, each event's result),
                                    DBD129-2-AC1 (FRESH reads: every named day holds its two objects, history untouched, the function and schedule unchanged, the REPORT lines equal the record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the record clauses on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~DB2/COT_CATCHUP_RECORD.json"
APPLY_REC_REL = D + "0.7.0_AE_CloudOps~DB2/COT_LANDING_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md"
PACKET_SHA = "a1b080c5fe065f90f4ad356c95301e59437637e95ce40afade93726eeaa392df"
LEDGER_SLUG = "irpt-dashbd-cottonwood-account-return-daily-20261015"
FUNCTION = "irpt-cot-account-return-daily-lambda"
LOG_GROUP = "/aws/lambda/" + FUNCTION
SILVER_BUCKET, SILVER_ROOT = "opal-data-assets", "blackdiamond/cottonwood/silver/"
SILVER_TABLES = ("fact_allocations", "fact_transactions")
GOLD_BUCKET, GOLD_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/"
HISTORY_COUNT, HISTORY_LAST, FIRST_DAY = 3325, "2026-06-22", "2026-07-10"
MAX_DAYS, MEM_LINE_MB = 25, 717
CRON, ZONE = "cron(15 8 ? * MON-FRI *)", "America/New_York"
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "packet_sha256", "invoked_utc", "request_id", "ledger_entry", "days", "payload", "held")


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


def git(root, *a):
    return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True).stdout


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_events(events, silver_days):
    """events: the record's event list; silver_days: sorted days that have BOTH silver tables (a fresh recount). Returns the sorted list of days the events named."""
    need(isinstance(events, list) and events, "events must be a non-empty list")
    named, last = [], FIRST_DAY
    for i, e in enumerate(events):
        ek = {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "report", "over_threshold", "request_id"}
        need(isinstance(e, dict) and set(e) == ek, "event %d keys differ: %s" % (i, sorted(set(e) ^ ek) if isinstance(e, dict) else "?"))
        p = e["payload"]
        need(isinstance(p, dict) and set(p) == {"days"} and isinstance(p["days"], list) and 1 <= len(p["days"]) <= MAX_DAYS, "event %d payload must be {days: [1..%d days]}" % (i, MAX_DAYS))
        ds = p["days"]
        need(all(isinstance(d, str) and ISO.match(d) for d in ds) and ds == sorted(set(ds)), "event %d days must be ascending distinct ISO dates" % i)
        need(ds[0] > last, "event %d starts at %s, not after %s (order, and never a day at or before %s)" % (i, ds[0], last, FIRST_DAY))
        need(all(d in silver_days for d in ds), "event %d names days without BOTH silver tables: %s" % (i, [d for d in ds if d not in silver_days][:3]))
        need(UTC.match(str(e["invoked_utc"])) and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and e["function_error"] is None, "event %d must be synchronous, 200, no function error" % i)
        r = e["returned"]
        need(isinstance(r, dict) and r.get("ok") is True and r.get("days") == ds and r.get("held") == [], "event %d: the returned body must be ok, the same days, nothing held: %s" % (i, r))
        rp = e["report"]
        need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"} and is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] > 0 and rp["memory_size_mb"] == 1024
             and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] < 900000, "event %d report: Max Memory Used (int MB), duration under 900 s, memory size 1024" % i)
        need(e["over_threshold"] is (rp["max_memory_used_mb"] > MEM_LINE_MB) and e["over_threshold"] is False, "event %d: Max Memory Used %s is over %d MB; the order stops there, this record cannot pass" % (i, rp["max_memory_used_mb"], MEM_LINE_MB))
        need(nes(e["request_id"]), "event %d request_id" % i)
        named += ds
        last = ds[-1]
    expect = [d for d in silver_days if FIRST_DAY < d <= named[-1]]
    need(named == expect, "the named days are not exactly the silver days after %s up to %s: missing %s, extra %s" % (FIRST_DAY, named[-1], sorted(set(expect) - set(named))[:3], sorted(set(named) - set(expect))[:3]))
    return named


def check_record(rec, packet_blob_ok, apply_ok, ledger_exists, silver_days):
    exp = {"claim", "gates", "ledger_entry", "events", "partitions_after", "ledger_closed", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_sha256", "act2_recorded_and_passing", "one_change_at_a_time"}, "gates keys")
    need(g["packet_sha256"] == PACKET_SHA and packet_blob_ok, "the packet's sha256 differs from the signed one")
    need(g["act2_recorded_and_passing"] is True and apply_ok, "Act 2's apply record must exist and pass its own checks before any Act 3 event")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] in (0, 1),
         "one_change_at_a_time: the denominator and the markers (the one allowed is this pair's own open ledger)")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    named = check_events(rec["events"], silver_days)
    pa = rec["partitions_after"]
    need(isinstance(pa, dict) and set(pa) == {"new_days", "last_day", "history_partitions"} and pa["new_days"] == len(named) + 1 and pa["last_day"] == named[-1] and pa["history_partitions"] == HISTORY_COUNT,
         "partitions_after: new_days must be the named days plus %s, last_day the last named, history %d" % (FIRST_DAY, HISTORY_COUNT))
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return named


# ------------------------------------------------------------------------------------------------ the live reads
def silver_both_days():
    import boto3
    s3 = boto3.client("s3")
    sets = []
    for t in SILVER_TABLES:
        got, tok = set(), None
        while True:
            kw = {"Bucket": SILVER_BUCKET, "Prefix": SILVER_ROOT + t + "/", "Delimiter": "/"}
            if tok:
                kw["ContinuationToken"] = tok
            r = s3.list_objects_v2(**kw)
            got |= {c["Prefix"].split("date=")[1].strip("/") for c in r.get("CommonPrefixes", []) if "date=" in c["Prefix"]}
            if not r.get("IsTruncated"):
                break
            tok = r.get("NextContinuationToken")
        sets.append(got)
    return sorted(d for d in (sets[0] & sets[1]) if d >= FIRST_DAY)


def live(root):
    import boto3
    lam, sch, logs, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("scheduler", region_name="us-east-1"), boto3.client("logs", region_name="us-east-1"), boto3.client("s3")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    sc = sch.get_schedule(Name="irpt-cot-account-return-daily-daily")
    objs, tok = [], None
    while True:
        kw = {"Bucket": GOLD_BUCKET, "Prefix": GOLD_PREFIX}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        objs += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            break
        tok = r.get("NextContinuationToken")
    reports, ftok = [], None
    while True:
        kw = {"logGroupName": LOG_GROUP, "filterPattern": "REPORT"}
        if ftok:
            kw["nextToken"] = ftok
        r = logs.filter_log_events(**kw)
        for ev in r.get("events", []):
            m = re.search(r"Duration: ([\d.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ev["message"], re.S)
            if m:
                reports.append((float(m.group(1)), int(m.group(2)), int(m.group(3))))
        ftok = r.get("nextToken")
        if not ftok:
            break
    return {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")},
            "objects": objs, "reports": reports}


def run(root, cid):
    root = Path(root)
    rec = load(root, REC_REL)
    apply_rec = load(root, APPLY_REC_REL)
    packet_ok = hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest() == PACKET_SHA
    apply_ok = apply_rec.get("event", {}).get("function_error", "x") is None and apply_rec.get("event", {}).get("over_717_mb") is False and apply_rec.get("ledger_closed") is False
    ledger_exists = bool(list((root / "org/critical_paths/change_management").glob("*%s*" % LEDGER_SLUG))) or (root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file()
    silver = silver_both_days()
    named = check_record(rec, packet_ok, apply_ok, ledger_exists, silver)
    if cid == "DBD129-1-AC1":
        print("OK: %d catch-up days in %d event(s) of at most %d, exactly the silver days after %s up to %s, each event synchronous, nothing held, Max Memory Used under %d MB; Act 2's record passes; ledger %s open" %
              (len(named), len(rec["events"]), MAX_DAYS, FIRST_DAY, named[-1], MEM_LINE_MB, LEDGER_SLUG))
        return True
    lv = live(root)
    if cid == "DBD129-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 900 and lv["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "the function or the schedule changed: %s %s %s" % (lv["memory"], lv["timeout"], lv["schedule"]))
        by_day = {}
        for k, _ in lv["objects"]:
            by_day.setdefault(k[len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15], []).append(k.rsplit("/", 1)[1])
        want = [FIRST_DAY] + named
        for d in want:
            need(sorted(by_day.get(d, [])) == ["data.parquet", "manifest.json"], "partition %s holds %s" % (d, sorted(by_day.get(d, []))))
        hist = [d for d in by_day if d <= HISTORY_LAST]
        need(len(hist) == HISTORY_COUNT and max(hist) == HISTORY_LAST, "history: %d partitions to %s expected, read %d" % (HISTORY_COUNT, HISTORY_LAST, len(hist)))
        later = sorted(d for d in by_day if d > HISTORY_LAST)
        need(set(later) >= set(want) and all(d >= FIRST_DAY for d in later), "partitions after history must include exactly the named days and start at %s: %s" % (FIRST_DAY, later[:3]))
        for i, e in enumerate(rec["events"]):
            rp = e["report"]
            need([r for r in lv["reports"] if r[2] == rp["max_memory_used_mb"] and abs(r[0] - rp["duration_ms"]) < 1.0 and r[1] == 1024], "no REPORT line equals event %d (Max Memory Used %s, duration %s)" % (i, rp["max_memory_used_mb"], rp["duration_ms"]))
        print("OK: %d named days plus %s each hold their two objects; history %d partitions to %s untouched; function and schedule unchanged (DISABLED); a REPORT line equals each of the %d events" %
              (len(named), FIRST_DAY, len(hist), HISTORY_LAST, len(rec["events"])))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    silver = ["2026-07-10"] + ["2026-07-%02d" % d for d in range(13, 32) if d % 7 not in (0, 6)] + ["2026-08-%02d" % d for d in range(3, 32)]
    silver = sorted(set(silver))
    rest = [d for d in silver if d > FIRST_DAY]
    chunks = [rest[i:i + 25] for i in range(0, len(rest), 25)]

    def ev(days, mem=640):
        return {"payload": {"days": days}, "invoked_utc": "2026-10-16T02:00:00Z", "invocation_type": "RequestResponse", "status_code": 200, "function_error": None,
                "returned": {"ok": True, "days": days, "held": []}, "report": {"max_memory_used_mb": mem, "duration_ms": 30000.5, "memory_size_mb": 1024}, "over_threshold": mem > MEM_LINE_MB, "request_id": "r"}
    good = {"claim": "measured", "gates": {"packet_sha256": PACKET_SHA, "act2_recorded_and_passing": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 1}},
            "ledger_entry": LEDGER_SLUG, "events": [ev(c) for c in chunks], "partitions_after": {"new_days": len(rest) + 1, "last_day": rest[-1], "history_partitions": HISTORY_COUNT},
            "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}

    def grade(r, packet=True, apply=True, ledger=True, sd=silver):
        try:
            check_record(r, packet, apply, ledger, sd)
            return True
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    arms = (("packet", lambda r: r["gates"].update(packet_sha256="x")), ("act2", lambda r: r["gates"].update(act2_recorded_and_passing=False)),
            ("ledger closed", lambda r: r.update(ledger_closed=True)), ("extra key", lambda r: r.update(z=1)),
            ("too many days", lambda r: r["events"][0]["payload"].update(days=rest[:26])),
            ("first day named", lambda r: r["events"][0]["payload"].update(days=[FIRST_DAY] + chunks[0][:-1])),
            ("history day named", lambda r: r["events"][0]["payload"].update(days=["2026-06-22"] + chunks[0])),
            ("unsorted", lambda r: r["events"][0]["payload"].update(days=list(reversed(chunks[0])))),
            ("no silver pair", lambda r: r["events"][0]["payload"].update(days=["2026-07-14"] + chunks[0][1:])),
            ("skipped day", lambda r: r["events"].pop(0)), ("async", lambda r: r["events"][0].update(invocation_type="Event")),
            ("function error", lambda r: r["events"][0].update(function_error="Unhandled")), ("held", lambda r: r["events"][0]["returned"].update(held=[chunks[0][0]])),
            ("over line", lambda r: r["events"][0].update(report={"max_memory_used_mb": 800, "duration_ms": 1.0, "memory_size_mb": 1024}, over_threshold=True)),
            ("memory size", lambda r: r["events"][0]["report"].update(memory_size_mb=8192)), ("status", lambda r: r["events"][0].update(status_code=500)),
            ("new_days", lambda r: r["partitions_after"].update(new_days=3)), ("history", lambda r: r["partitions_after"].update(history_partitions=3324)),
            ("marker", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=2)), ("digits", lambda r: r["events"][0]["returned"].update(note="id 1234567890")))
    for name, f in arms:
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False, "red arm %s passed" % name
    assert grade(copy.deepcopy(good), packet=False) is False and grade(copy.deepcopy(good), apply=False) is False and grade(copy.deepcopy(good), ledger=False) is False
    assert grade(copy.deepcopy(good), sd=sorted(silver + ["2026-08-02"])) is False
    print("selftest: one green and %d red record arms behave" % (len(arms) + 4))


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Exception as e:  # a failed live read is a FAIL, not a traceback
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
