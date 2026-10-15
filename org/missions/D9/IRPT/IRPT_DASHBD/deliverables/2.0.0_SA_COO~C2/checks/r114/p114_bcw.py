"""IRPT_DASHBD round 114, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the Cottonwood landing/frontier read, its schedule packet, and the readers read.

  DB-c-1 (~401) the Black Diamond silver landing times of the last 15 trading days, the gold frontier and the catch-up set. A READ.            DBC114-1-AC1
  DB-c-2 (~401) the never-widen packet for the Cottonwood holdings_performance_daily schedule, principal and catch-up keys. A PACKET.          DBC114-2-AC1
  DB-c-3 (~402) the readers of the three Cottonwood gold tables and the fallback calendar's equality. A READ.                               DBC114-3-AC1

The checker grades FORM and INTERNAL CONSISTENCY and RECOMPUTES: the 15 trading days and each landing's New York time from the recorded UTC instant; a fresh S3 LIST of the silver
partitions (count, newest landing per recorded date) and the gold partitions (newest date, catch-up set); the builder outputs (lib/opal_naming name() and address()) for every recorded
name and key; each recorded reader file exists and names its table. It writes nothing.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import datetime as dt
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC1 = D + "0.9.0_WK_IRPT_DASHBD~401/LANDING_AND_FRONTIER_R114.json"
REC2J = D + "0.9.0_WK_IRPT_DASHBD~401/PACKET_FACTS_R114.json"
REC2M = D + "0.9.0_WK_IRPT_DASHBD~401/NEVER_WIDEN_PACKET_DB-c-2_R114.md"
REC3 = D + "0.9.0_WK_IRPT_DASHBD~402/READERS_AND_CALENDAR_R114.json"
SILVER_BUCKET = "opal-data-assets"
SILVER_PREFIX = "blackdiamond/cottonwood/silver/fact_holdings/"
CLAIMS = ("measured", "inferred", "held", "absent")
TABLES = ("account_dim", "account_return_daily", "holdings_performance_daily")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "keys", "prefix", "where", "date", "dates", "landing_utc", "landing_et", "newest_date", "name", "address")
FOREIGN = ("inflection", "orion", "schwab", "49financial", "opal-data-49financial", "opal-data-inflection")
PACKET_HEADS = ("## Change set", "## Keys written", "## Both branches", "## Rollback", "## Questions for the CTO's half", "## Not in this packet")
ET = None


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "record absent: " + rel)
    return json.loads(p.read_text(encoding="utf-8"))


def walk(o, key=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)
    else:
        yield key, o


def no_identifiers(rec):
    for k, v in walk(rec):
        if isinstance(v, str):
            low = v.lower()
            for f in FOREIGN:
                need(f not in low or k in ("where", "prefix", "words", "basis_words", "note"), "foreign firm token in field " + k)
            if k not in DIGIT_OK_KEYS:
                need(not LONG_DIGITS.search(v), "a run of 8 or more digits in field " + k)


def lib(root):
    sys.path.insert(0, str(Path(root)))
    import lib.opal_naming as naming
    import lib.trading_calendar as cal
    return naming, cal


def iso(d):
    return dt.date.fromisoformat(d)


def et_of(utc_s):
    from zoneinfo import ZoneInfo
    t = dt.datetime.strptime(utc_s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return t.astimezone(ZoneInfo("America/New_York"))


def last_n_trading_days(cal, end, n):
    days = cal.trading_days_between(end - dt.timedelta(days=60), end)
    return [x.isoformat() for x in days[-n:]]


def list_dates(s3, bucket, prefix):
    out = {}
    pg = s3.get_paginator("list_objects_v2")
    for page in pg.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []):
            m = re.search(r"date=(\d{4}-\d{2}-\d{2})/$", cp["Prefix"])
            if m:
                out[m.group(1)] = None
    return out


def landing_of(s3, bucket, prefix, d):
    best = None
    pg = s3.get_paginator("list_objects_v2")
    for page in pg.paginate(Bucket=bucket, Prefix=prefix + "date=" + d + "/"):
        for o in page.get("Contents", []):
            lm = o["LastModified"].astimezone(dt.timezone.utc)
            best = lm if best is None or lm > best else best
    return best.strftime("%Y-%m-%dT%H:%M:%SZ") if best else None


def gold_prefix(naming, table):
    # the table root, from the builder: address() of a dummy partition with the partition tail cut
    a = naming.address("irpt", "cottonwood", "gold", table, "date=2000-01-03")
    m = re.match(r"s3://([^/]+)/(.*)date=2000-01-03$", a)
    need(m is not None, "address() shape unexpected for " + table)
    return m.group(1), m.group(2)


def s3client():
    import boto3
    return boto3.client("s3")


def ac_1(root):
    naming, cal = lib(root)
    r = load(root, REC1)
    no_identifiers(r)
    need(r.get("claim") in CLAIMS and r.get("silver", {}).get("claim") in CLAIMS, "claim field missing")
    sv = r["silver"]
    need(sv.get("bucket") == SILVER_BUCKET and sv.get("prefix") == SILVER_PREFIX, "silver place wrong")
    newest = sv["newest_date"]
    want = last_n_trading_days(cal, iso(newest), 15)
    land = r["landings"]
    need([x["date"] for x in land] == want, "landings are not the last 15 trading days to the newest silver date")
    for x in land:
        e = et_of(x["landing_utc"])
        need(x["landing_et"] == e.strftime("%Y-%m-%dT%H:%M"), "landing_et is not the New York time of landing_utc for " + x["date"])
        need(x["after_0600_et"] == (e.hour >= 6), "after_0600_et wrong for " + x["date"])
    latest = max(et_of(x["landing_utc"]).strftime("%H:%M") for x in land)
    need(r["latest_landing_et_time"] == latest, "latest_landing_et_time is not the maximum time of day")
    need(r["proposed_fire_time_et"] > latest, "proposed fire time does not clear the latest landing")
    need(r["basis_words"].strip() != "", "basis_words empty")
    s3 = s3client()
    sdates = list_dates(s3, SILVER_BUCKET, SILVER_PREFIX)
    need(sv["partition_count"] == len(sdates), "silver partition_count differs from a fresh LIST")
    need(max(sdates) >= newest, "a fresh LIST holds a newer silver date than recorded: " + max(sdates))
    for x in land:
        need(landing_of(s3, SILVER_BUCKET, SILVER_PREFIX, x["date"]) == x["landing_utc"], "landing differs from a fresh read for " + x["date"])
    gb, gp = gold_prefix(naming, "holdings_performance_daily")
    gdates = list_dates(s3, gb, gp)
    need(r["gold"]["holdings_performance_daily"]["newest_date"] == max(gdates), "gold newest_date differs from a fresh LIST")
    cu = sorted(d for d in sdates if cal.is_trading_day(iso(d)) and d not in gdates)
    need(r["catch_up"]["dates"] == cu and r["catch_up"]["count"] == len(cu), "catch-up set differs from silver minus gold on the library calendar")
    rd = r["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads")), "a write or vendor call is recorded")
    need(r.get("files_in_repo_private") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "side-effect flags")


def ac_2(root):
    naming, cal = lib(root)
    f = load(root, REC2J)
    no_identifiers(f)
    c1 = load(root, REC1)
    need(f.get("claim") in CLAIMS, "claim field missing")
    for key, args in (("schedule", f["schedule_builder_args"]), ("principal", f["principal_builder_args"])):
        try:
            got = naming.name(*args)
            need(f[key + "_name"] == got, key + " name differs from the builder output")
            need(not f.get(key + "_builder_refusal"), key + " refusal recorded though the builder returned")
        except ValueError as e:
            need(f[key + "_name"] is None and f.get(key + "_builder_refusal", "")[:40] == str(e)[:40], key + " refusal not the builder's refusal")
    ks = f["keys_written"]
    dates = c1["catch_up"]["dates"]
    need(ks["dates"] == dates, "keys_written.dates is not DB-c-1's catch-up set")
    want = []
    for d in dates:
        want.append(naming.address("irpt", "cottonwood", "gold", "holdings_performance_daily", "date=" + d, "data.parquet"))
        for o in ("data.parquet", "manifest.json"):
            want.append(naming.address("irpt", "cottonwood", "gold", "holdings_performance_manifest", "date=" + d, o))
    need(ks["keys"] == want and ks["count"] == len(want) == 3 * len(dates), "keys differ from the builder's addresses (3 objects per date)")
    s3 = s3client()
    gb, gp = gold_prefix(naming, "holdings_performance_daily")
    gd = list_dates(s3, gb, gp)
    need(not any(d in gd for d in dates), "a catch-up date already has a gold partition (the key set would overwrite, not add)")
    t = (Path(root) / REC2M).read_text(encoding="utf-8") if (Path(root) / REC2M).is_file() else None
    need(t is not None, "packet absent: " + REC2M)
    need(len(t) >= 4000, "packet shorter than 4000 characters")
    for h in PACKET_HEADS:
        need(h in t, "packet heading absent: " + h)
    need(not any(tok in t for tok in ("approved by", "SIGNED")), "the packet claims a signature")
    rd = f["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes", "terraform_apply")), "a write is recorded")
    need(f.get("pushed") is False and f.get("deployed") is False, "side-effect flags")


def ac_3(root):
    naming, cal = lib(root)
    r = load(root, REC3)
    no_identifiers(r)
    need(set(r["tables"]) == set(TABLES), "tables are not the three Cottonwood gold tables")
    for t, v in r["tables"].items():
        need(v.get("claim") in CLAIMS, "claim missing for " + t)
        need(v["reader_count"] == len(v["readers"]), "reader_count differs from the list for " + t)
        for rd in v["readers"]:
            p = Path(root) / rd["file"]
            need(p.is_file(), "reader file absent: " + rd["file"])
            need(t in p.read_text(encoding="utf-8", errors="replace"), "reader file does not name " + t)
        if v["reader_count"] == 0:
            need(v["claim"] in ("absent", "inferred") and v.get("none_words", "").strip() != "", "zero readers need none_words and a claim of absent or inferred: " + t)
    c = r["calendar"]
    try:
        import pandas_market_calendars  # noqa: F401
        have = True
    except Exception:
        have = False
    if c["ran"]:
        need(isinstance(c["compared_days"], int) and c["compared_days"] > 0 and isinstance(c["mismatches"], int), "ran needs integer counts")
    else:
        need(not have and c["not_runnable_reason"].strip() != "", "not_runnable_reason needs the package to be absent now")
    need(c["range"] == ["2026-06-23", "2026-10-13"], "calendar range wrong")
    need(c["source"] == cal.calendar_source() if callable(getattr(cal, "calendar_source", None)) else True, "calendar source differs")
    rd = r["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes")), "a write is recorded")
    need(r.get("pushed") is False and r.get("deployed") is False, "side-effect flags")


ARMS = {"DBC114-1-AC1": ac_1, "DBC114-2-AC1": ac_2, "DBC114-3-AC1": ac_3}


def selftest(root):
    naming, cal = lib(root)
    days = last_n_trading_days(cal, dt.date(2026, 10, 13), 15)
    need(len(days) == 15 and days[-1] == "2026-10-13", "last_n_trading_days arm")
    e = et_of("2026-10-14T11:46:00Z")
    need(e.strftime("%H:%M") == "07:46" and (e.hour >= 6), "et_of arm")
    need(naming.name("irpt", "cottonwood", "holdings-performance", "daily") == "irpt-cot-holdings-performance-daily", "name() arm")
    b, p = gold_prefix(naming, "holdings_performance_daily")
    need(b == "opal-data-cottonwood" and p.endswith("holdings_performance_daily/"), "gold_prefix arm")
    refused = False
    try:
        no_identifiers({"basis_words": "account 12345678 moved"})
    except Fail:
        refused = True
    need(refused, "no_identifiers negative arm: a long digit run in a words field passed")
    no_identifiers({"basis_words": "none", "path": "a/20261015/b"})
    print("SELFTEST PASS")


def main(argv):
    if argv and argv[0] == "--selftest":
        try:
            selftest(argv[1] if len(argv) > 1 else ".")
        except Fail as e:
            print("SELFTEST FAIL: " + str(e))
            return 1
        return 0
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:  # a checker that cannot read must not pass
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
