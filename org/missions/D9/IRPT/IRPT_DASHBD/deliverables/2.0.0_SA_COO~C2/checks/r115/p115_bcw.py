"""IRPT_DASHBD round 115, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the producer read and the finalized pair packet.

  DB-c-4 (~403) what wrote Cottonwood's holdings_performance_daily gold, the 2026-06-09 prior-day input, the rewrite times of 2026-09-23..25. A READ.   DBC115-1-AC1
  DB-c-5 (~403) the pair packet finalized on DB-c-4: function, schedule at 08:15 New York with the frontier check, write-only principal, catch-up first. DBC115-2-AC1

Reuses the round-114 helpers of p114_bcw.py (same directory's sibling, loaded by path). RECOMPUTES: fresh LastModified of every recorded object, fresh version counts, the manifest key
sets by a GET of the manifest objects, the prior trading day from the library calendar, the catch-up set to the packet's as-of date, and every builder name and address. Writes nothing.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

D = p114.D
REC1 = D + "0.9.0_WK_IRPT_DASHBD~403/PRODUCER_READ_R115.json"
REC2J = D + "0.9.0_WK_IRPT_DASHBD~403/PACKET_FACTS_R115.json"
REC2M = D + "0.9.0_WK_IRPT_DASHBD~403/NEVER_WIDEN_PACKET_DB-c-5_R115.md"
VERDICTS = ("FUNCTION", "HOST_JOB", "AD_HOC", "NOT_ESTABLISHED")
REWRITE_DATES = ("2026-09-23", "2026-09-24", "2026-09-25")
HEADS = ("## Change set", "## Function", "## Catch-up first", "## Keys written", "## Both branches", "## Rollback", "## Questions for the CTO's half", "## Not in this packet")
TWO_TABLES = ("holdings_performance_daily", "holdings_performance_manifest")


def latest_lm(s3, bucket, prefix):
    best = None
    pg = s3.get_paginator("list_objects_v2")
    for page in pg.paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get("Contents", []):
            lm = o["LastModified"]
            best = lm if best is None or lm > best else best
    return best.strftime("%Y-%m-%dT%H:%M:%SZ") if best else None


def version_count(s3, bucket, prefix):
    n = 0
    pg = s3.get_paginator("list_object_versions")
    for page in pg.paginate(Bucket=bucket, Prefix=prefix):
        n += len(page.get("Versions", []))
    return n


def split(uri):
    m = re.match(r"s3://([^/]+)/(.*)$", uri)
    return m.group(1), m.group(2)


def ac_1(root):
    naming, cal = p114.lib(root)
    r = p114.load(root, REC1)
    p114.no_identifiers(r)
    need(r.get("claim") in p114.CLAIMS, "claim missing")
    pr = r["producer"]
    need(pr["verdict"] in VERDICTS, "producer verdict not in the enum")
    need(pr["words"].strip() != "" and pr["claim"] in p114.CLAIMS, "producer words or claim missing")
    if pr["verdict"] != "NOT_ESTABLISHED":
        need(pr["code_path"].strip() != "" and (Path(root) / pr["code_path"]).exists(), "the producer's code_path is not a repo path that exists")
    s3 = p114.s3client()
    gb, gp = p114.gold_prefix(naming, "holdings_performance_daily")
    mb, mp = p114.gold_prefix(naming, "holdings_performance_manifest")
    mk = r["manifests"]
    for d, keys in mk["by_date"].items():
        key = mp + "date=" + d + "/manifest.json"
        body = json.loads(s3.get_object(Bucket=mb, Key=key)["Body"].read().decode("utf-8"))
        need(sorted(body.keys()) == sorted(keys), "manifest key set differs from a fresh read for " + d)
    need(len(mk["by_date"]) >= 2, "two manifests are needed (the newest gold date and an earlier one)")
    d9 = r["date_0609"]
    prior = cal.prev_trading_day(p114.iso("2026-06-09")).isoformat()
    need(d9["prior_trading_day"] == prior, "prior trading day differs from the library calendar")
    sd = p114.list_dates(s3, p114.SILVER_BUCKET, p114.SILVER_PREFIX)
    need(d9["prior_day_silver_present"] == (prior in sd), "prior_day_silver_present differs from a fresh LIST")
    need(d9["rule_file"].strip() != "" and (Path(root) / d9["rule_file"]).is_file() and d9["can_compute_words"].strip() != "", "rule_file or can_compute_words missing")
    rw = r["rewrite"]
    need(sorted(rw["dates"]) == list(REWRITE_DATES), "rewrite dates are not the three named")
    for d in REWRITE_DATES:
        row = rw["dates"][d]
        need(row["silver_latest_lm_utc"] == latest_lm(s3, p114.SILVER_BUCKET, p114.SILVER_PREFIX + "date=" + d + "/"), "silver last-modified differs from a fresh read for " + d)
        need(row["gold_latest_lm_utc"] == latest_lm(s3, gb, gp + "date=" + d + "/"), "gold last-modified differs from a fresh read for " + d)
        need(row["gold_after_silver"] == (row["gold_latest_lm_utc"] > row["silver_latest_lm_utc"]), "gold_after_silver is not the comparison of the two instants for " + d)
        need(row["silver_versions"] == version_count(s3, p114.SILVER_BUCKET, p114.SILVER_PREFIX + "date=" + d + "/"), "silver version count differs from a fresh read for " + d)
    need(rw["words"].strip() != "", "rewrite words missing")
    rd = r["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes")), "a write is recorded")
    need(r.get("pushed") is False and r.get("deployed") is False, "side-effect flags")


def ac_2(root):
    naming, cal = p114.lib(root)
    f = p114.load(root, REC2J)
    p114.no_identifiers(f)
    need(f.get("claim") in p114.CLAIMS, "claim missing")
    c4 = p114.load(root, REC1)
    for key, args in (("schedule", f["schedule_builder_args"]), ("principal", f["principal_builder_args"])):
        try:
            got = naming.name(*args)
            need(f[key + "_name"] == got and not f.get(key + "_builder_refusal"), key + " name differs from the builder output")
        except ValueError as e:
            need(f[key + "_name"] is None and f.get(key + "_builder_refusal", "")[:40] == str(e)[:40], key + " refusal is not the builder's")
    need(f["fire_time_et"] == "08:15" and f["frontier_check"] is True, "fire time or frontier check is not as ruled")
    need(f["start_state"] == "DISABLED_UNTIL_CATCHUP_AFTER_READ", "the schedule must start disabled until the catch-up's after-read")
    fn = f["function"]
    need(fn["mode"] in ("ADOPT", "BUILD") and (fn["mode"] == "BUILD" or fn.get("name")), "function mode or name missing")
    need(c4["producer"]["verdict"] != "FUNCTION" or fn["mode"] == "ADOPT", "a FUNCTION producer must be adopted, not rebuilt")
    want_pref = []
    for t in TWO_TABLES:
        b, pfx = p114.gold_prefix(naming, t)
        want_pref.append("s3://" + b + "/" + pfx)
    need(sorted(f["principal_write_prefixes"]) == sorted(want_pref), "principal write prefixes are not exactly the two gold tables")
    gdb, gdp = p114.gold_prefix(naming, "holdings_performance_daily")
    need(sorted(f["principal_read_prefixes"]) == sorted(["s3://" + p114.SILVER_BUCKET + "/" + p114.SILVER_PREFIX, "s3://" + gdb + "/" + gdp]), "principal read prefixes are not the Black Diamond silver prefix and the daily gold prefix (the scheduled path lists it)")
    s3 = p114.s3client()
    sd = p114.list_dates(s3, p114.SILVER_BUCKET, p114.SILVER_PREFIX)
    gb, gp = p114.gold_prefix(naming, "holdings_performance_daily")
    gd = p114.list_dates(s3, gb, gp)
    asof = f["catch_up"]["as_of_date"]
    need(asof in sd, "the as-of date has no silver partition")
    all_dates = sorted(d for d in sd if d <= asof and cal.is_trading_day(p114.iso(d)) and d not in gd)
    ex = f["catch_up"].get("excluded", [])
    for e in ex:
        # a date is excludable only when its prior trading day has no silver partition (the producer's rule has no base for it) and the packet says why
        need(e["date"] in all_dates, "an excluded date is not a catch-up candidate: " + e["date"])
        prior = cal.prev_trading_day(p114.iso(e["date"])).isoformat()
        need(prior not in sd and e["reason"].strip() != "", "an excluded date needs a missing prior-day silver partition and a reason: " + e["date"])
    want_dates = [d for d in all_dates if d not in [e["date"] for e in ex]]
    ks = f["keys_written"]
    need(ks["dates"] == want_dates and f["catch_up"]["dates"] == want_dates, "catch-up dates differ from silver trading days to the as-of date minus gold minus the excluded dates")
    want = []
    for d in want_dates:
        want.append(naming.address("irpt", "cottonwood", "gold", "holdings_performance_daily", "date=" + d, "data.parquet"))
        for o in ("data.parquet", "manifest.json"):
            want.append(naming.address("irpt", "cottonwood", "gold", "holdings_performance_manifest", "date=" + d, o))
    need(ks["keys"] == want and ks["count"] == len(want) == 3 * len(want_dates), "keys differ from the builder's addresses, three per date")
    p = Path(root) / REC2M
    need(p.is_file(), "packet absent: " + REC2M)
    t = p.read_text(encoding="utf-8")
    need(len(t) >= 5000, "packet shorter than 5000 characters")
    pos = -1
    for h in HEADS:
        i = t.find(h)
        need(i > pos, "packet heading absent or out of order: " + h)
        pos = i
    need("UNSIGNED" in t or "unsigned" in t, "the packet must state that it is unsigned")
    need(not re.search(r"\bsigned by\b|\bapproved by\b", t), "the packet claims a signature")
    rd = f["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes", "terraform_apply")), "a write is recorded")
    need(f.get("pushed") is False and f.get("deployed") is False, "side-effect flags")


ARMS = {"DBC115-1-AC1": ac_1, "DBC115-2-AC1": ac_2}


def selftest(root):
    naming, cal = p114.lib(root)
    b, p = p114.gold_prefix(naming, "holdings_performance_manifest")
    need(b == "opal-data-cottonwood" and p.endswith("holdings_performance_manifest/"), "manifest prefix arm")
    need(split("s3://a/b/c")[0] == "a" and split("s3://a/b/c")[1] == "b/c", "split arm")
    need(cal.prev_trading_day(p114.iso("2026-06-09")).isoformat() == "2026-06-08", "prev_trading_day arm")
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
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
