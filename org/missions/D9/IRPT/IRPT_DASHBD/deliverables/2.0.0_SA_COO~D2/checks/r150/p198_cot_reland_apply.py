"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- the APPLY of the signed RE-LAND pair: the Cottonwood gold days whose carrier delivery dell1's lane has now landed in full (a set of days out of 2026-07-22, 07-27, 07-29,
08-03) are REWRITTEN through the function's own explicit rewrite event, dry run first, and the series republished ONCE (CTO ruling, msg after 10575). WORLD, served output. The record is the applier's
(`0.7.0_AE_CloudOps~IB2`); the checker re-reads the gold days and their prior versions, and COMPARES each sampled series with the PREVIOUS VERSION of its own object (the bucket is versioned), so the invariant "only the
re-landed days are added and only the next trading day's three fields move" is graded on the data, not on the applier's report. The day set is the packet's `DAYS:` line (at least 2, a subset of the four).

  DBC198-1-AC1  the record: both halves signed at the packet's sha256, the ledger, the before reads, the dry run of every day in its band, the rewrites, the pre-write diff inside its STOP lines, the canary, the one republish, the after-read
  DBC198-2-AC1  FRESH live reads of the gold days: each current version holds the recorded rows, its prior version is kept, every other partition's row total is unchanged, both functions and both schedules are as before
  DBC198-3-AC1  FRESH live reads of the series: 939 prefixes, each day present in the recorded number of series, and 60 sampled series differ from their previous version ONLY by the added days and the three fields on each next trading day

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_198")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_RELAND_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_RELAND_PAIR.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_RELAND_PAIR_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_RELAND_PAIR_CTO_HALF.md"
LEDGER_SLUG = "irpt-dashbd-cottonwood-reland-pair-20261017"
NEXT = {"2026-07-22": "2026-07-23", "2026-07-27": "2026-07-28", "2026-07-29": "2026-07-30", "2026-08-03": "2026-08-04"}
GOLD_FN, PUB_FN = "irpt-cot-account-return-daily-lambda", "irpt-cot-reporting-publish-lambda"
GOLD_CODE, PUB_CODE = "+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=", "vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE="
BUCKET, GOLD_PREFIX, PUB_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/", "irpt/cottonwood/platinum/reporting/"
BAND = (840, 960)
PARTIAL_MAX = 500
REFUSED_MAX = 40
MAX_NM_PCT = 15
MOVABLE = ("total_return_daily", "day_quality", "return_basis")
SCHED = {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("packet_sha256", "account_digest12", "code_sha256", "invoked_utc")


def count(x, lo=0):
    return is_int(x) and x >= lo


def per_day(x, days, pred):
    return isinstance(x, dict) and sorted(x) == sorted(days) and all(count(x[d]) and pred(x[d]) for d in days)


def packet_days(packet_text):
    m = re.search(r"^\*\*DAYS:\*\* ([0-9, -]+)$", packet_text, re.M)
    need(m is not None, "the packet carries no DAYS line")
    days = [x.strip() for x in m.group(1).split(",")]
    need(days == sorted(days) and len(days) >= 2 and set(days) <= set(NEXT), "the packet's DAYS must be at least two of %s, ascending: %s" % (sorted(NEXT), days))
    return days


def alldays(days):
    """The gold days the pair rewrites: each re-landed day AND its next trading day (that day's rows were derived against the partial day, so they are NOT_MEASURABLE in the gold itself)."""
    return sorted(set(days) | {NEXT[x] for x in days})


def check_record(rec, packet_sha, packet_text, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "days", "before", "dry_run", "rewrite", "prewrite", "publish_dry", "canary", "publish_full", "after", "ledger_closed", "reads", "notes"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    days = packet_days(packet_text)
    ad = alldays(days)
    need(rec["days"] == days, "the record's days %s differ from the packet's DAYS %s" % (rec["days"], days))
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_sha256", "coo_half_signed", "cto_half_signed", "one_change_at_a_time", "live_matches_packet"}, "gates keys")
    need(g["packet_sha256"] == packet_sha and g["coo_half_signed"] is True and "SIGNED" in coo_text and packet_sha in coo_text, "the packet's sha256 or the COO half")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and packet_sha[:8] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and count(oc["worktrees_read"], 1) and oc["open_markers_naming_this_surface"] == 0 and g["live_matches_packet"] is True,
         "one change at a time; live matches the packet")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists and rec["applier"] == APPLIER, "the ledger %s exists; the applier is %s" % (LEDGER_SLUG, APPLIER))
    b = rec["before"]
    keys = {"day_rows", "day_versions", "full_day_rows", "gold_total_rows", "partitions", "series_prefixes", "series_objects", "series_versions", "gold_code_sha256", "publish_code_sha256", "schedules"}
    need(isinstance(b, dict) and set(b) == keys and per_day(b["day_rows"], ad, lambda n: n >= 1) and all(b["day_rows"][x] <= PARTIAL_MAX for x in days) and all(b["day_rows"][x] >= 850 for x in ad if x not in days)
         and per_day(b["day_versions"], ad, lambda n: n >= 1)
         and b["full_day_rows"] >= 850 and count(b["gold_total_rows"], 1) and count(b["partitions"], 1)
         and b["series_prefixes"] == 939 and count(b["series_objects"], 939) and count(b["series_versions"], 939) and b["gold_code_sha256"] == GOLD_CODE and b["publish_code_sha256"] == PUB_CODE
         and b["schedules"] == SCHED, "before: each re-landed day PARTIAL (at most %d rows), each next day full-sized (850 or more rows), a full neighbour, 939 prefixes, the two code hashes, the two schedule states" % PARTIAL_MAX)
    d = rec["dry_run"]
    need(isinstance(d, dict) and set(d) == {"ok", "days", "held", "rows", "gold_objects_before", "gold_objects_after", "gold_versions_before", "gold_versions_after"} and d["ok"] is True and d["days"] == ad and d["held"] == 0
         and per_day(d["rows"], ad, lambda n: BAND[0] <= n <= BAND[1]) and d["gold_objects_before"] == d["gold_objects_after"] and d["gold_versions_before"] == d["gold_versions_after"],
         "dry run: ok, one event per gold day (the re-landed days and their next days), held 0, each day's rows in %s, nothing written" % (BAND,))
    w = rec["rewrite"]
    need(isinstance(w, dict) and set(w) == {"rows", "day_versions_after", "prior_versions_kept", "other_partitions_unchanged"} and w["rows"] == d["rows"]
         and isinstance(w["day_versions_after"], dict) and all(w["day_versions_after"].get(x) == b["day_versions"][x] + 1 for x in ad) and sorted(w["day_versions_after"]) == sorted(ad)
         and w["prior_versions_kept"] is True and w["other_partitions_unchanged"] is True, "rewrite: each day's dry-run rows, its version count +1, the partial versions kept, every other partition unchanged")
    p = rec["prewrite"]
    nxt = sorted(NEXT[x] for x in days)
    need(isinstance(p, dict) and set(p) == {"accounts_gaining_by_day", "other_field_changes_on_common_days", "changed_dates", "days_removed", "refused"} and per_day(p["accounts_gaining_by_day"], days, lambda n: n >= 1)
         and p["other_field_changes_on_common_days"] == 0 and isinstance(p["changed_dates"], list) and set(p["changed_dates"]) <= set(nxt) and p["days_removed"] == 0 and count(p["refused"]) and p["refused"] <= REFUSED_MAX,
         "prewrite: only %s may change on a common day, in the three fields; nothing removed; refused at most %d" % (nxt, REFUSED_MAX))
    pd = rec["publish_dry"]
    need(isinstance(pd, dict) and set(pd) == {"published", "refused"} and pd["published"] == 939 and count(pd["refused"]) and pd["refused"] <= REFUSED_MAX, "publish dry run: 939 published, refused at most %d" % REFUSED_MAX)
    c = rec["canary"]
    need(isinstance(c, dict) and set(c) == {"account_digest12", "dates_gained", "common_fields_equal", "only_next_days_three_fields_differ", "manifest_unchanged_but_dates"} and re.fullmatch(r"[0-9a-f]{12}", str(c["account_digest12"]))
         and isinstance(c["dates_gained"], list) and c["dates_gained"] and set(c["dates_gained"]) <= set(days) and c["common_fields_equal"] is True and c["only_next_days_three_fields_differ"] is True
         and c["manifest_unchanged_but_dates"] is True, "canary: one account by digest; the dates gained are a non-empty subset of the days; common fields equal the previous version except each next day's three fields; the manifest keeps publisher version, scope and claim")
    f = rec["publish_full"]
    need(isinstance(f, dict) and set(f) == {"published", "refused", "objects_before", "objects_after", "versions_before", "versions_after"} and f["published"] == 939 and f["refused"] == pd["refused"]
         and f["objects_before"] == f["objects_after"] == b["series_objects"] and f["versions_after"] - f["versions_before"] >= 939 - pd["refused"], "full republish: 939 published, refused as in the dry run, the same objects, new versions")
    a = rec["after"]
    keys2 = {"gold_day_rows", "not_measurable", "gold_total_rows", "partitions", "gold_code_sha256", "publish_code_sha256", "schedules", "series_prefixes", "series_with_day", "sample_ok"}
    need(isinstance(a, dict) and set(a) == keys2 and a["gold_day_rows"] == d["rows"] and a["gold_total_rows"] == b["gold_total_rows"] - sum(b["day_rows"].values()) + sum(d["rows"].values()) and a["partitions"] == b["partitions"]
         and a["gold_code_sha256"] == GOLD_CODE and a["publish_code_sha256"] == PUB_CODE and a["schedules"] == b["schedules"] and a["series_prefixes"] == 939
         and per_day(a["series_with_day"], days, lambda n: n >= 1) and a["sample_ok"] is True
         and per_day(a["not_measurable"], ad, lambda n: True) and all(a["not_measurable"][x] * 100 <= MAX_NM_PCT * d["rows"][x] for x in ad),
         "after: each gold day holds the dry run's rows and at most %d percent NOT_MEASURABLE (a normal day holds about 3), the gold total moved by exactly (the new rows - the old rows), the partitions, codes and schedules equal, 939 series, a sample ok" % MAX_NM_PCT)
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0} and isinstance(rec["notes"], str) and 30 <= len(rec["notes"]) <= 3000
         and "YTD" in rec["notes"] and "Not measured" in rec["notes"], "the ledger left OPEN for the issuer; the reads block; notes that say the YTD return still reads Not measured while other days are absent")
    return True


def series_invariant(prev, cur, days):
    """prev and cur: decoded series.json.gz dicts of one account. True when cur differs from prev ONLY by added days (a subset of `days`) and the three movable fields on the next trading day of a re-landed day."""
    movable_days = {NEXT[x] for x in days}
    cols = [k for k in prev if isinstance(prev[k], list) and len(prev[k]) == len(prev["date"])]
    need(set(cols) == {k for k in cur if isinstance(cur[k], list) and len(cur[k]) == len(cur["date"])}, "the column set differs between the versions")
    pi = {x: i for i, x in enumerate(prev["date"])}
    ci = {x: i for i, x in enumerate(cur["date"])}
    need(set(pi) <= set(ci), "a day was REMOVED from the series")
    added = sorted(set(ci) - set(pi))
    need(set(added) <= set(days), "the dates gained must be a subset of %s, read %s" % (days, added))
    need(cur["date"] == sorted(cur["date"]), "the dates are not ascending")
    for x, i in pi.items():
        j = ci[x]
        for k in cols:
            if k == "date" or prev[k][i] == cur[k][j]:
                continue
            need(x in movable_days and k in MOVABLE, "a common day changed: %s on %s" % (k, x))
    return added


def check_live_gold(rec, cur_rows, prev_rows, versions, nm, total_rows_after, partitions, gold_cfg, pub_cfg, schedules):
    ad = alldays(rec["days"])
    need(cur_rows == rec["after"]["gold_day_rows"] == rec["rewrite"]["rows"], "the live gold days hold %s rows, the record says %s" % (cur_rows, rec["rewrite"]["rows"]))
    need(all(prev_rows[x] == rec["before"]["day_rows"][x] for x in ad) and versions == rec["rewrite"]["day_versions_after"], "each previous version must be kept and each version count must equal the record's")
    need(all(nm[x] * 100 <= MAX_NM_PCT * cur_rows[x] for x in ad) and nm == rec["after"]["not_measurable"], "a live gold day holds more than %d percent NOT_MEASURABLE rows, or the count differs from the record: %s" % (MAX_NM_PCT, nm))
    need(total_rows_after == rec["after"]["gold_total_rows"] and partitions == rec["after"]["partitions"], "the live gold total or partition count differs from the record")
    need(gold_cfg["CodeSha256"] == GOLD_CODE and pub_cfg["CodeSha256"] == PUB_CODE, "a function's code hash moved")
    need(schedules == SCHED, "a schedule state moved")
    return True


def check_live_series(rec, prefixes, with_day, results):
    need(prefixes == 939, "the live series prefix count is %s, not 939" % prefixes)
    need(with_day == rec["after"]["series_with_day"], "the live number of series holding each day is %s, the record says %s" % (with_day, rec["after"]["series_with_day"]))
    need(results and all(r is True for r in results), "a sampled series differs from its previous version beyond the allowed change")
    return True


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    packet_sha = hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest()
    packet_text = (root / PACKET_REL).read_text(encoding="utf-8")
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8") if (root / COO_HALF_REL).is_file() else ""
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8") if (root / CTO_HALF_REL).is_file() else ""
    ledger_exists = bool(list((root / "org/critical_paths/.open_deploys").glob(LEDGER_SLUG + "*.json"))) or bool(list((root / "org/critical_paths/change_management").glob("*" + LEDGER_SLUG + "*")))
    check_record(rec, packet_sha, packet_text, coo, cto, ledger_exists)
    scrub = dict(rec, notes=re.sub(r"[a-z][a-z0-9-]*-\d{8}", "ledger", str(rec["notes"])))
    need(not H.digit_runs(scrub), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(scrub)[:2])
    days = rec["days"]
    if cid == "DBC198-1-AC1":
        print("OK: both halves signed at the packet's sha256, the ledger, the before reads, every day's dry run in its band, the rewrites (version +1, partial versions kept), the pre-write diff inside its STOP lines, the canary, the one republish, the after-read, no id")
        return True
    import boto3
    s3 = boto3.client("s3")
    if cid == "DBC198-2-AC1":
        import pyarrow.parquet as pq
        lam, sch = boto3.client("lambda", region_name="us-east-1"), boto3.client("scheduler", region_name="us-east-1")
        cur, prev, vcount, nm = {}, {}, {}, {}
        for x in alldays(days):
            objs = [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=GOLD_PREFIX + "date=%s/" % x).get("Contents", []) if o["Key"].endswith(".parquet")]
            need(len(objs) == 1, "the gold day %s must hold exactly one object" % x)
            vs = sorted([v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=objs[0]).get("Versions", []) if v["Key"] == objs[0]], key=lambda v: v["LastModified"], reverse=True)

            def table_of(vid, key=objs[0]):
                return pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key, VersionId=vid)["Body"].read()))
            now_t = table_of(vs[0]["VersionId"])
            cur[x] = now_t.num_rows
            nm[x] = sum(1 for q in now_t.column("day_quality").to_pylist() if q == "NOT_MEASURABLE")
            prev[x] = table_of(vs[1]["VersionId"]).num_rows if len(vs) > 1 else -1
            vcount[x] = len(vs)
        total, parts, tok = 0, set(), None
        while True:
            r = s3.list_objects_v2(Bucket=BUCKET, Prefix=GOLD_PREFIX, **({"ContinuationToken": tok} if tok else {}))
            for o in r.get("Contents", []):
                if o["Key"].endswith(".parquet"):
                    parts.add(o["Key"].split("/")[-2])
                    total += pq.ParquetFile(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read())).metadata.num_rows
            tok = r.get("NextContinuationToken")
            if not tok:
                break
        sched = {"account_return_daily": sch.get_schedule(Name="irpt-cot-account-return-daily-daily")["State"], "publish_daily": sch.get_schedule(Name="irpt-cot-reporting-publish-daily")["State"]}
        check_live_gold(rec, cur, prev, vcount, nm, total, len(parts), lam.get_function_configuration(FunctionName=GOLD_FN), lam.get_function_configuration(FunctionName=PUB_FN), sched)
        print("OK: live: the %d gold days hold the recorded rows with few NOT_MEASURABLE, each earlier version is kept, the gold total and partition count equal the record's, both functions and both schedules are as before" % len(alldays(days)))
        return True
    if cid == "DBC198-3-AC1":
        prefixes = []
        tok = None
        while True:
            r = s3.list_objects_v2(Bucket=BUCKET, Prefix=PUB_PREFIX, Delimiter="/", **({"ContinuationToken": tok} if tok else {}))
            prefixes += [x["Prefix"] for x in r.get("CommonPrefixes", []) if "/account=" in x["Prefix"]]
            tok = r.get("NextContinuationToken")
            if not tok:
                break

        def load(key, vid=None):
            kw = {"Bucket": BUCKET, "Key": key}
            if vid:
                kw["VersionId"] = vid
            return json.loads(gzip.decompress(s3.get_object(**kw)["Body"].read()))
        with_day = {x: 0 for x in days}
        for p in prefixes:
            have = set(load(p + "series.json.gz")["date"])
            for x in days:
                if x in have:
                    with_day[x] += 1
        sample = sorted(prefixes)[:: max(1, len(prefixes) // 60)][:60]
        results = []
        for p in sample:
            key = p + "series.json.gz"
            vs = sorted([v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=key).get("Versions", []) if v["Key"] == key], key=lambda v: v["LastModified"], reverse=True)
            if len(vs) < 2:
                results.append(False)
                continue
            try:
                series_invariant(load(key, vs[1]["VersionId"]), load(key, vs[0]["VersionId"]), days)
                results.append(True)
            except Fail:
                results.append(False)
        check_live_series(rec, len(prefixes), with_day, results)
        print("OK: live: 939 series prefixes, each day present as recorded, and %d sampled series differ from their previous version only by the added days and the three fields on each next trading day" % len(sample))
        return True
    raise Fail("unknown criterion %s" % cid)


DAYS4 = ["2026-07-22", "2026-07-27", "2026-07-29", "2026-08-03"]
PACKET_TEXT = "**Packet.**\n**DAYS:** " + ", ".join(DAYS4) + "\n"


def synthetic(days=None):
    days = days or DAYS4
    ad = alldays(days)
    rows = {x: 880 + i for i, x in enumerate(ad)}
    old = {x: (3 + i if x in days else 879) for i, x in enumerate(ad)}
    ver = {x: 1 for x in ad}
    return {"claim": "measured", "gates": {"packet_sha256": "p" * 64, "coo_half_signed": True, "cto_half_signed": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
            "ledger_entry": LEDGER_SLUG, "applier": APPLIER, "days": list(days),
            "before": {"day_rows": dict(old), "day_versions": dict(ver), "full_day_rows": 879, "gold_total_rows": 60000, "partitions": 69, "series_prefixes": 939, "series_objects": 1878, "series_versions": 2800,
                       "gold_code_sha256": GOLD_CODE, "publish_code_sha256": PUB_CODE, "schedules": dict(SCHED)},
            "dry_run": {"ok": True, "days": list(ad), "held": 0, "rows": dict(rows), "gold_objects_before": 69, "gold_objects_after": 69, "gold_versions_before": 69, "gold_versions_after": 69},
            "rewrite": {"rows": dict(rows), "day_versions_after": {x: 2 for x in ad}, "prior_versions_kept": True, "other_partitions_unchanged": True},
            "prewrite": {"accounts_gaining_by_day": {x: 700 for x in days}, "other_field_changes_on_common_days": 0, "changed_dates": sorted(NEXT[x] for x in days), "days_removed": 0, "refused": 40},
            "publish_dry": {"published": 939, "refused": 40},
            "canary": {"account_digest12": "a" * 12, "dates_gained": list(days), "common_fields_equal": True, "only_next_days_three_fields_differ": True, "manifest_unchanged_but_dates": True},
            "publish_full": {"published": 939, "refused": 40, "objects_before": 1878, "objects_after": 1878, "versions_before": 2800, "versions_after": 3700},
            "after": {"gold_day_rows": dict(rows), "not_measurable": {x: 30 for x in ad}, "gold_total_rows": 60000 - sum(old.values()) + sum(rows.values()), "partitions": 69, "gold_code_sha256": GOLD_CODE, "publish_code_sha256": PUB_CODE, "schedules": dict(SCHED),
                      "series_prefixes": 939, "series_with_day": {x: 700 for x in days}, "sample_ok": True},
            "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0},
            "notes": "Counts and statuses only; the three days with no transactions were not touched; the YTD return still reads Not measured while any of those days is in the window."}


def selftest():
    rec = synthetic()
    coo, cto = "SIGNED " + "p" * 64, "SIGNED " + "p" * 8

    def go(r, **kw):
        return check_record(r, kw.get("sha", "p" * 64), kw.get("pk", PACKET_TEXT), kw.get("coo", coo), kw.get("cto", cto), kw.get("led", True))
    assert go(rec)
    two = synthetic(["2026-07-22", "2026-08-03"])
    assert go(two, pk="**DAYS:** 2026-07-22, 2026-08-03\n")
    n = 0

    def red(fn, label):
        nonlocal n
        try:
            fn()
        except Fail:
            n += 1
            return
        raise AssertionError("mutant passed: " + label)

    def mut(label, fn, base=None, **kw):
        r = copy.deepcopy(base or rec)
        fn(r)
        red(lambda: go(r, **kw), label)
    red(lambda: go(rec, sha="q" * 64), "packet sha")
    red(lambda: go(rec, coo="DRAFT"), "coo unsigned")
    red(lambda: go(rec, cto="SIGNED"), "cto unbound")
    red(lambda: go(rec, led=False), "ledger")
    red(lambda: go(rec, pk="**Packet.**\n"), "no DAYS line")
    red(lambda: go(rec, pk="**DAYS:** 2026-07-22\n"), "one day only")
    red(lambda: go(rec, pk="**DAYS:** 2026-07-22, 2026-08-19\n"), "a day outside the four")
    red(lambda: go(rec, pk="**DAYS:** 2026-08-03, 2026-07-22\n"), "days not ascending")
    red(lambda: go(two, pk=PACKET_TEXT), "record days differ from the packet")
    mut("claim", lambda r: r.update(claim="inferred"))
    mut("open legs", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1))
    mut("before not partial", lambda r: r["before"]["day_rows"].update({"2026-07-22": 879}))
    mut("before missing day", lambda r: r["before"]["day_rows"].pop("2026-08-03"))
    mut("before no full neighbour", lambda r: r["before"].update(full_day_rows=100))
    mut("before a next day partial", lambda r: r["before"]["day_rows"].update({"2026-07-23": 100}))
    mut("before code", lambda r: r["before"].update(gold_code_sha256="x="))
    mut("before schedule", lambda r: r["before"]["schedules"].update(publish_daily="ENABLED"))
    mut("dry band low", lambda r: r["dry_run"]["rows"].update({"2026-07-27": 800}))
    mut("dry band high", lambda r: r["dry_run"]["rows"].update({"2026-07-29": 1000}))
    mut("dry held", lambda r: r["dry_run"].update(held=1))
    mut("dry wrote", lambda r: r["dry_run"].update(gold_versions_after=70))
    mut("dry days", lambda r: r["dry_run"].update(days=DAYS4[:3]))
    mut("dry missing row", lambda r: r["dry_run"]["rows"].pop("2026-07-22"))
    mut("dry missing next day", lambda r: r["dry_run"]["rows"].pop("2026-07-28"))
    mut("dry only the re-landed days", lambda r: r["dry_run"].update(days=list(DAYS4)))
    mut("rewrite rows", lambda r: r["rewrite"]["rows"].update({"2026-07-22": 881}))
    mut("rewrite version", lambda r: r["rewrite"]["day_versions_after"].update({"2026-07-27": 3}))
    mut("prior not kept", lambda r: r["rewrite"].update(prior_versions_kept=False))
    mut("other partitions", lambda r: r["rewrite"].update(other_partitions_unchanged=False))
    mut("prewrite zero gain", lambda r: r["prewrite"]["accounts_gaining_by_day"].update({"2026-08-03": 0}))
    mut("prewrite other fields", lambda r: r["prewrite"].update(other_field_changes_on_common_days=1))
    mut("prewrite dates", lambda r: r["prewrite"].update(changed_dates=["2026-07-23", "2026-07-24"]))
    mut("prewrite removed", lambda r: r["prewrite"].update(days_removed=1))
    mut("prewrite refused", lambda r: r["prewrite"].update(refused=41))
    mut("publish dry refused", lambda r: r["publish_dry"].update(refused=300))
    mut("canary dates", lambda r: r["canary"].update(dates_gained=["2026-08-19"]))
    mut("canary empty", lambda r: r["canary"].update(dates_gained=[]))
    mut("canary common", lambda r: r["canary"].update(common_fields_equal=False))
    mut("canary digest", lambda r: r["canary"].update(account_digest12="short"))
    mut("full published", lambda r: r["publish_full"].update(published=938))
    mut("full refused differs", lambda r: r["publish_full"].update(refused=39))
    mut("notes without the YTD sentence", lambda r: r.update(notes="Counts and statuses only; nothing else changed in the window."))
    mut("full objects", lambda r: r["publish_full"].update(objects_after=1900))
    mut("full versions", lambda r: r["publish_full"].update(versions_after=2900))
    mut("after day rows", lambda r: r["after"]["gold_day_rows"].update({"2026-07-22": 879}))
    mut("after total", lambda r: r["after"].update(gold_total_rows=61000))
    mut("after code", lambda r: r["after"].update(publish_code_sha256="x="))
    mut("after series", lambda r: r["after"].update(series_prefixes=938))
    mut("after series with day zero", lambda r: r["after"]["series_with_day"].update({"2026-07-29": 0}))
    mut("after sample", lambda r: r["after"].update(sample_ok=False))
    mut("after still not measurable", lambda r: r["after"]["not_measurable"].update({"2026-07-28": 500}))
    mut("after no not_measurable count", lambda r: r["after"]["not_measurable"].pop("2026-08-04"))
    mut("ledger closed", lambda r: r.update(ledger_closed=True))
    mut("reads", lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}))
    mut("extra key", lambda r: r.update(z=1))
    days = DAYS4
    prev = {"date": ["2026-07-24", "2026-07-28", "2026-07-29"], "value": [1.0, 2.0, 3.0], "total_return_daily": [0.1, None, 0.2], "day_quality": ["MEASURED", "NOT_MEASURABLE", "MEASURED"], "return_basis": ["TWR", "NOT_MEASURABLE", "TWR"], "method_version": 1}
    cur = {"date": ["2026-07-24", "2026-07-27", "2026-07-28", "2026-07-29"], "value": [1.0, 1.5, 2.0, 3.0], "total_return_daily": [0.1, 0.05, 0.03, 0.2], "day_quality": ["MEASURED"] * 4, "return_basis": ["TWR"] * 4, "method_version": 1}
    assert series_invariant(prev, cur, days) == ["2026-07-27"]
    assert series_invariant(prev, prev, days) == []
    red(lambda: series_invariant(prev, dict(cur, value=[1.0, 1.5, 2.1, 3.0]), days), "a common day's value moved")
    red(lambda: series_invariant(prev, dict(cur, total_return_daily=[0.11, 0.05, 0.03, 0.2]), days), "a common day's return moved on another day")
    red(lambda: series_invariant(prev, {k: (v[1:] if isinstance(v, list) else v) for k, v in cur.items()}, days), "a day removed")
    red(lambda: series_invariant(prev, dict(cur, date=["2026-07-24", "2026-07-25", "2026-07-28", "2026-07-29"]), days), "another day added")
    red(lambda: series_invariant(prev, cur, ["2026-07-22", "2026-08-03"]), "a day added that is not a re-landed day")
    red(lambda: series_invariant(prev, dict(cur, external_flow=[0, 0, 0, 0]), days), "a column appeared")
    red(lambda: series_invariant(prev, dict(cur, date=["2026-07-24", "2026-07-28", "2026-07-27", "2026-07-29"]), days), "dates not ascending")
    cfg, pcfg = {"CodeSha256": GOLD_CODE}, {"CodeSha256": PUB_CODE}
    cur_rows, prev_rows = dict(rec["rewrite"]["rows"]), dict(rec["before"]["day_rows"])
    vers, tot = dict(rec["rewrite"]["day_versions_after"]), rec["after"]["gold_total_rows"]
    nm = dict(rec["after"]["not_measurable"])
    assert check_live_gold(rec, cur_rows, prev_rows, vers, nm, tot, 69, cfg, pcfg, SCHED)
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, vers, dict(nm, **{"2026-07-28": 500}), tot, 69, cfg, pcfg, SCHED), "live a day still mostly not measurable")
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, vers, dict(nm, **{"2026-07-28": 31}), tot, 69, cfg, pcfg, SCHED), "live not measurable differs from the record")
    red(lambda: check_live_gold(rec, dict(cur_rows, **{"2026-07-22": 879}), prev_rows, vers, nm, tot, 69, cfg, pcfg, SCHED), "live day rows")
    red(lambda: check_live_gold(rec, cur_rows, dict(prev_rows, **{"2026-07-27": 880}), vers, nm, tot, 69, cfg, pcfg, SCHED), "live prior version lost")
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, dict(vers, **{"2026-07-29": 3}), nm, tot, 69, cfg, pcfg, SCHED), "live versions")
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, vers, nm, 1, 69, cfg, pcfg, SCHED), "live total")
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, vers, nm, tot, 70, cfg, pcfg, SCHED), "live partitions")
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, vers, nm, tot, 69, {"CodeSha256": "x="}, pcfg, SCHED), "live gold code")
    red(lambda: check_live_gold(rec, cur_rows, prev_rows, vers, nm, tot, 69, cfg, pcfg, dict(SCHED, publish_daily="ENABLED")), "live schedule")
    wd = dict(rec["after"]["series_with_day"])
    assert check_live_series(rec, 939, wd, [True] * 60)
    red(lambda: check_live_series(rec, 938, wd, [True]), "live prefixes")
    red(lambda: check_live_series(rec, 939, dict(wd, **{"2026-08-03": 5}), [True]), "live with day")
    red(lambda: check_live_series(rec, 939, wd, [True, False]), "a sample differs")
    red(lambda: check_live_series(rec, 939, wd, []), "no sample")
    print("selftest: green on the synthetic record and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
