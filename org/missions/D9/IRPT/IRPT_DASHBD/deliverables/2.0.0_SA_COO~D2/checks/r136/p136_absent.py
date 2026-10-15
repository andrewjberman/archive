"""IRPT_DASHBD round 136, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- the READ of the three absent trading days of the Cottonwood landing (CTO ROUND ANALYSIS rounds 130-132 @b3dc83e664, msg
8511, enrichment item 2): for the day after each absent day, is the stored return measured from the last PRESENT day, so that no return is lost, or is a day's return missing? The three days
(2026-08-19, 2026-09-24, 2026-09-25) have a Black Diamond silver `fact_allocations` partition but no `fact_transactions` partition, so the landing's presence hold wrote no gold partition for them.
READ ONLY: S3 LIST and GET of the Cottonwood gold and the Black Diamond silver; prints COUNTS and verdict words only; the issuer takes it on the direct-act path (a LOCAL read under the size floor).

  the issuer (direct act)   RD_COT_ABSENT_DAYS_READ_R136.json
                            DB136-1-AC1 (the record: the form, the verdicts follow from the counts by the stated rule)
                            DB136-1-AC2 (FRESH: the checker recounts the absent days, the silver presence, and every count of the record from S3)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the record clauses on synthetic arms
"""
import datetime as dt
import io
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "2.0.0_SA_COO~D2/RD_COT_ABSENT_DAYS_READ_R136.json"
FIRST_DAY, LAST_DAY = "2026-07-10", "2026-10-14"
GOLD_BUCKET, SILVER_BUCKET = "opal-data-cottonwood", "opal-data-assets"
GOLD_PREFIX, SILVER_ROOT = "irpt/cottonwood/gold/account_return_daily/", "blackdiamond/cottonwood/silver/"
SIDECAR_PREFIX = "irpt/cottonwood/gold/account_return_daily_blank_reasons/"
RATE_FLOOR = 0.9
LONG_DIGITS = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


# ------------------------------------------------------------------------------------------------ the pure clauses
def verdict(absent_has_alloc, absent_has_txn, next_rate, base_rate):
    """The stated rule. A day with values but no flows has no return of its own (flows are needed to measure it); the next present day's return is measured from the absent day's
    value when its measured-return rate keeps pace with the following day's (at least RATE_FLOOR of it)."""
    if absent_has_alloc and not absent_has_txn:
        own = "ABSENT_DAY_RETURN_MISSING"
    elif not absent_has_alloc and not absent_has_txn:
        own = "ABSENT_DAY_NO_SILVER"
    else:
        own = "ABSENT_DAY_HAS_BOTH_TABLES"
    nxt = "NEXT_DAY_RETURN_MEASURED" if (base_rate > 0 and next_rate >= RATE_FLOOR * base_rate) else "NEXT_DAY_RETURN_LOST"
    return own, nxt


def check_record(rec):
    exp = {"absent_days", "per_day", "stored_return_rule", "sidecar", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    ad = rec["absent_days"]
    need(isinstance(ad, list) and ad and ad == sorted(ad) and all(isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) for x in ad), "absent_days must be ascending ISO dates")
    pd_ = rec["per_day"]
    need(isinstance(pd_, dict) and sorted(pd_) == ad, "per_day must hold exactly the absent days")
    for d, e in pd_.items():
        keys = {"alloc_present", "txn_present", "next_present_day", "next_stats", "following_day", "following_stats", "verdict_own", "verdict_next"}
        need(isinstance(e, dict) and set(e) == keys, "per_day %s keys" % d)
        for sk in ("next_stats", "following_stats"):
            s = e[sk]
            need(isinstance(s, dict) and set(s) == {"rows", "return_non_null", "day_quality"} and is_int(s["rows"]) and s["rows"] > 0 and is_int(s["return_non_null"]) and 0 <= s["return_non_null"] <= s["rows"]
                 and isinstance(s["day_quality"], dict) and sum(s["day_quality"].values()) == s["rows"], "per_day %s %s form" % (d, sk))
        need(e["next_present_day"] > d and e["following_day"] > e["next_present_day"], "per_day %s: the next present day follows the absent day and the following day follows it" % d)
        nr = e["next_stats"]["return_non_null"] / e["next_stats"]["rows"]
        br = e["following_stats"]["return_non_null"] / e["following_stats"]["rows"]
        own, nxt = verdict(e["alloc_present"], e["txn_present"], nr, br)
        need((e["verdict_own"], e["verdict_next"]) == (own, nxt), "per_day %s: the verdicts %s do not follow from the counts by the stated rule (%s)" % (d, (e["verdict_own"], e["verdict_next"]), (own, nxt)))
    need(isinstance(rec["stored_return_rule"], str) and 60 <= len(rec["stored_return_rule"]) <= 900, "stored_return_rule: the adapter's rule in words")
    sc = rec["sidecar"]
    need(isinstance(sc, dict) and set(sc) == {"prefix", "files", "columns", "landing_function_writes_it"} and sc["prefix"] == SIDECAR_PREFIX and is_int(sc["files"]) and sc["files"] >= 1
         and isinstance(sc["columns"], list) and sc["columns"] and sc["landing_function_writes_it"] is False, "sidecar form")
    need(isinstance(rec["words"], str) and 120 <= len(rec["words"]) <= 2200 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 120 to 2200 characters with no long digit run")
    return True


def compare_recount(rec, fresh):
    need(rec["absent_days"] == fresh["absent_days"], "absent_days differ from the checker's recount: %s vs %s" % (rec["absent_days"], fresh["absent_days"]))
    for d in rec["absent_days"]:
        need(rec["per_day"][d] == fresh["per_day"][d], "per_day %s differs from the checker's recount" % d)
    need(rec["sidecar"]["files"] == fresh["sidecar"]["files"] and rec["sidecar"]["columns"] == fresh["sidecar"]["columns"], "the sidecar's files or columns differ from the recount")
    return True


# ------------------------------------------------------------------------------------------------ the fresh recount
def _list_days(s3, bucket, prefix):
    got, tok = set(), None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix, "Delimiter": "/"}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        got |= {c["Prefix"].split("date=")[1].strip("/") for c in r.get("CommonPrefixes", []) if "date=" in c["Prefix"]}
        if not r.get("IsTruncated"):
            break
        tok = r.get("NextContinuationToken")
    return got


def fresh(root):
    sys.path.insert(0, str(root))
    import collections

    import boto3
    import pyarrow.parquet as pq

    from lib import trading_calendar as tc
    s3 = boto3.client("s3")
    gold = _list_days(s3, GOLD_BUCKET, GOLD_PREFIX)
    land = sorted(d for d in gold if d >= FIRST_DAY)
    tr = [d.isoformat() for d in tc.trading_days_between(dt.date.fromisoformat(FIRST_DAY), dt.date.fromisoformat(LAST_DAY))]
    absent = [d for d in tr if d not in gold]
    alloc, txn = _list_days(s3, SILVER_BUCKET, SILVER_ROOT + "fact_allocations/"), _list_days(s3, SILVER_BUCKET, SILVER_ROOT + "fact_transactions/")

    def stats(d):
        body = s3.get_object(Bucket=GOLD_BUCKET, Key=GOLD_PREFIX + "date=%s/data.parquet" % d)["Body"].read()
        t = pq.read_table(io.BytesIO(body))
        r, q = t["total_return_daily"].to_pylist(), t["day_quality"].to_pylist()
        return {"rows": t.num_rows, "return_non_null": sum(1 for x in r if x is not None), "day_quality": dict(sorted(collections.Counter(q).items()))}
    per = {}
    for d in absent:
        nxt = next(x for x in land if x > d)
        fol = next(x for x in land if x > nxt)
        ns, fs = stats(nxt), stats(fol)
        own, nv = verdict(d in alloc, d in txn, ns["return_non_null"] / ns["rows"], fs["return_non_null"] / fs["rows"])
        per[d] = {"alloc_present": d in alloc, "txn_present": d in txn, "next_present_day": nxt, "next_stats": ns, "following_day": fol, "following_stats": fs, "verdict_own": own, "verdict_next": nv}
    r = s3.list_objects_v2(Bucket=GOLD_BUCKET, Prefix=SIDECAR_PREFIX)
    keys = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".parquet")]
    cols = []
    if keys:
        import pyarrow.parquet as pq2
        body = s3.get_object(Bucket=GOLD_BUCKET, Key=keys[0])["Body"].read()
        cols = pq2.read_schema(io.BytesIO(body)).names
    return {"absent_days": absent, "per_day": per, "sidecar": {"files": len(keys), "columns": cols}}


def run(root, cid):
    root = Path(root)
    rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
    check_record(rec)
    if cid == "DB136-1-AC1":
        print("OK: record: %d absent trading days %s; per day the verdicts follow from the counts by the stated rule: %s" %
              (len(rec["absent_days"]), rec["absent_days"], sorted({(e["verdict_own"], e["verdict_next"]) for e in rec["per_day"].values()})))
        return True
    if cid == "DB136-1-AC2":
        f = fresh(root)
        compare_recount(rec, f)
        print("OK: fresh: the checker recounted the absent days %s, the silver presence of each, the next and following days' rows, measured-return counts and day-quality words, and the sidecar (%d file(s)); every recorded number equals its own" %
              (f["absent_days"], f["sidecar"]["files"]))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy

    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    assert verdict(True, False, 0.96, 0.96) == ("ABSENT_DAY_RETURN_MISSING", "NEXT_DAY_RETURN_MEASURED")
    assert verdict(True, False, 0.2, 0.96) == ("ABSENT_DAY_RETURN_MISSING", "NEXT_DAY_RETURN_LOST")
    assert verdict(False, False, 0.96, 0.96)[0] == "ABSENT_DAY_NO_SILVER" and verdict(True, True, 0.9, 0.9)[0] == "ABSENT_DAY_HAS_BOTH_TABLES"

    def stats(rows, nn):
        return {"rows": rows, "return_non_null": nn, "day_quality": {"MEASURED": nn, "NOT_MEASURABLE": rows - nn}}
    good = {"absent_days": ["2026-08-19"], "per_day": {"2026-08-19": {"alloc_present": True, "txn_present": False, "next_present_day": "2026-08-20", "next_stats": stats(100, 96), "following_day": "2026-08-21",
                                                                      "following_stats": stats(100, 96), "verdict_own": "ABSENT_DAY_RETURN_MISSING", "verdict_next": "NEXT_DAY_RETURN_MEASURED"}},
            "stored_return_rule": "The adapter measures a day's return from the previous trading day's value over the day's flows; an absent day has values but no flows, so its own return is missing.",
            "sidecar": {"prefix": SIDECAR_PREFIX, "files": 1, "columns": ["a", "b"], "landing_function_writes_it": False}, "words": "w" * 150}
    assert check_record(copy.deepcopy(good))
    arms = (("absent order", lambda r: r.update(absent_days=["2026-09-01", "2026-08-19"])), ("per_day keys", lambda r: r["per_day"].update(extra={})),
            ("verdict own", lambda r: r["per_day"]["2026-08-19"].update(verdict_own="ABSENT_DAY_NO_SILVER")), ("verdict next", lambda r: r["per_day"]["2026-08-19"].update(verdict_next="NEXT_DAY_RETURN_LOST")),
            ("order of days", lambda r: r["per_day"]["2026-08-19"].update(next_present_day="2026-08-18")), ("stats form", lambda r: r["per_day"]["2026-08-19"]["next_stats"].update(rows=0)),
            ("quality sum", lambda r: r["per_day"]["2026-08-19"]["next_stats"]["day_quality"].update(MEASURED=1)), ("rule", lambda r: r.update(stored_return_rule="short")),
            ("sidecar prefix", lambda r: r["sidecar"].update(prefix="x")), ("sidecar writer", lambda r: r["sidecar"].update(landing_function_writes_it=True)), ("sidecar files", lambda r: r["sidecar"].update(files=0)),
            ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)), ("digits", lambda r: r.update(words="w" * 150 + " 123456789")))
    for label, fn in arms:
        r = copy.deepcopy(good)
        fn(r)
        red(lambda: check_record(r), label)
    fr = {"absent_days": ["2026-08-19"], "per_day": copy.deepcopy(good["per_day"]), "sidecar": {"files": 1, "columns": ["a", "b"]}}
    assert compare_recount(good, copy.deepcopy(fr))
    for label, fn in (("absent", lambda f: f.update(absent_days=["2026-08-20"])), ("per day", lambda f: f["per_day"]["2026-08-19"]["next_stats"].update(return_non_null=95)), ("sidecar", lambda f: f["sidecar"].update(files=2))):
        f2 = copy.deepcopy(fr)
        fn(f2)
        red(lambda: compare_recount(good, f2), label)
    print("selftest: record (%d red arms) and recount (3 red arms) clauses behave" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or recount is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
