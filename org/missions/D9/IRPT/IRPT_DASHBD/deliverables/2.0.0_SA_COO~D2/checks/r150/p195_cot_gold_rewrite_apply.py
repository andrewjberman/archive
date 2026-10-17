"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- the APPLY of the signed pair that rewrites the Cottonwood gold day 2026-07-27 from the now-full carrier delivery and republishes the series (packet
NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md, sha256 8596f43f; COO half 3a3680e93e). WORLD, served output. The record is the applier's (`0.7.0_AE_CloudOps~IB2`); the checker re-reads the gold day
and its prior version, and COMPARES each sampled series with the PREVIOUS VERSION of its own object (the bucket is versioned), so the invariant "only 2026-07-27 is added and only 2026-07-28's three fields move" is graded
on the data, not on the applier's report.

  DBC195-1-AC1  the record: both halves signed at the packet's sha256, the ledger, the before reads, the dry run in its band, the rewrite, the pre-write diff inside its STOP lines, the canary, the full republish, the after-read
  DBC195-2-AC1  FRESH live reads of the gold day: the current version holds the recorded rows, the 3-row version is kept as the previous one, every other partition's row total is unchanged, both functions and both schedules are as before
  DBC195-3-AC1  FRESH live reads of the series: 939 prefixes, the day is present in the recorded number of series, and 60 sampled series differ from their previous version ONLY by the added day 2026-07-27 and the three fields on 2026-07-28

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


H = helper("r147/p151_pubapply.py", "p151_helper_195")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_GOLD_REWRITE_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_GOLD_REWRITE_20260727_AND_REPUBLISH_CTO_HALF.md"
LEDGER_SLUG = "irpt-dashbd-cottonwood-gold-rewrite-20260727-and-republish-20261017"
DAY, NEXT_DAY = "2026-07-27", "2026-07-28"
GOLD_FN, PUB_FN = "irpt-cot-account-return-daily-lambda", "irpt-cot-reporting-publish-lambda"
GOLD_CODE, PUB_CODE = "+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=", "vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE="
BUCKET, GOLD_PREFIX, PUB_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/", "irpt/cottonwood/platinum/reporting/"
BAND = (840, 920)
MOVABLE = ("total_return_daily", "day_quality", "return_basis")
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("packet_sha256", "account_digest12", "code_sha256", "invoked_utc")


def count(x, lo=0):
    return is_int(x) and x >= lo


def check_record(rec, packet_sha, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "dry_run", "rewrite", "prewrite", "publish_dry", "canary", "publish_full", "after", "ledger_closed", "reads", "notes"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_sha256", "coo_half_signed", "cto_half_signed", "one_change_at_a_time", "live_matches_packet"}, "gates keys")
    need(g["packet_sha256"] == packet_sha and g["coo_half_signed"] is True and "SIGNED" in coo_text and packet_sha in coo_text, "the packet's sha256 or the COO half")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and packet_sha[:8] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and count(oc["worktrees_read"], 1) and oc["open_markers_naming_this_surface"] == 0 and g["live_matches_packet"] is True, "one change at a time; live matches the packet")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists and rec["applier"] == APPLIER, "the ledger %s exists; the applier is %s" % (LEDGER_SLUG, APPLIER))
    b = rec["before"]
    keys = {"day_rows", "day_objects", "day_versions", "full_day_rows", "gold_total_rows", "partitions", "series_prefixes", "series_objects", "series_versions", "gold_code_sha256", "publish_code_sha256", "schedules"}
    need(isinstance(b, dict) and set(b) == keys and b["day_rows"] == 3 and b["day_objects"] == 1 and count(b["day_versions"], 1) and b["full_day_rows"] == 879 and count(b["gold_total_rows"], 1) and count(b["partitions"], 1)
         and b["series_prefixes"] == 939 and count(b["series_objects"], 939) and count(b["series_versions"], 939) and b["gold_code_sha256"] == GOLD_CODE and b["publish_code_sha256"] == PUB_CODE
         and b["schedules"] == {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}, "before: the packet's section 2 (3 rows on the day, 879 on the full day, 939 prefixes, the two code hashes, the two schedule states)")
    d = rec["dry_run"]
    need(isinstance(d, dict) and set(d) == {"ok", "days", "held", "rows", "gold_objects_before", "gold_objects_after", "gold_versions_before", "gold_versions_after"} and d["ok"] is True and d["days"] == [DAY] and d["held"] == 0
         and count(d["rows"]) and BAND[0] <= d["rows"] <= BAND[1] and d["gold_objects_before"] == d["gold_objects_after"] and d["gold_versions_before"] == d["gold_versions_after"], "dry run: ok, the one day, held 0, rows in %s, nothing written" % (BAND,))
    w = rec["rewrite"]
    need(isinstance(w, dict) and set(w) == {"rows", "day_versions_after", "prior_version_kept", "other_partitions_unchanged"} and w["rows"] == d["rows"] and w["day_versions_after"] == b["day_versions"] + 1
         and w["prior_version_kept"] is True and w["other_partitions_unchanged"] is True, "rewrite: the dry run's rows, the version count +1, the 3-row version kept, every other partition unchanged")
    p = rec["prewrite"]
    need(isinstance(p, dict) and set(p) == {"accounts_gaining_the_day", "other_field_changes_on_common_days", "changed_dates", "days_removed", "refused"} and count(p["accounts_gaining_the_day"], 1)
         and p["other_field_changes_on_common_days"] == 0 and isinstance(p["changed_dates"], list) and set(p["changed_dates"]) <= {NEXT_DAY} and p["days_removed"] == 0 and p["refused"] == 0,
         "prewrite: only %s may change on a common day, in the three fields; nothing removed; refused 0" % NEXT_DAY)
    pd = rec["publish_dry"]
    need(isinstance(pd, dict) and set(pd) == {"published", "refused"} and pd["published"] == 939 and pd["refused"] == 40, "publish dry run: 939 published, refused exactly 40 (CTO condition, msg 10363)")
    c = rec["canary"]
    need(isinstance(c, dict) and set(c) == {"account_digest12", "dates_gained", "common_fields_equal", "only_next_day_three_fields_differ", "manifest_unchanged_but_dates"} and re.fullmatch(r"[0-9a-f]{12}", str(c["account_digest12"]))
         and c["dates_gained"] == [DAY] and c["common_fields_equal"] is True and c["only_next_day_three_fields_differ"] is True and c["manifest_unchanged_but_dates"] is True,
         "canary: one account by digest; the date gained is exactly %s; common fields equal the previous version except the next day's three fields; the manifest keeps publisher version, scope and claim" % DAY)
    f = rec["publish_full"]
    need(isinstance(f, dict) and set(f) == {"published", "refused", "objects_before", "objects_after", "versions_before", "versions_after"} and f["published"] == 939 and f["refused"] == 40
         and f["objects_before"] == f["objects_after"] == b["series_objects"] and f["versions_after"] - f["versions_before"] >= 939 - pd["refused"], "full republish: 939 published, refused exactly 40, the same objects, new versions")
    a = rec["after"]
    keys2 = {"gold_day_rows", "gold_total_rows", "partitions", "gold_code_sha256", "publish_code_sha256", "schedules", "series_prefixes", "series_with_day", "sample_ok"}
    need(isinstance(a, dict) and set(a) == keys2 and a["gold_day_rows"] == d["rows"] and a["gold_total_rows"] == b["gold_total_rows"] - b["day_rows"] + d["rows"] and a["partitions"] == b["partitions"]
         and a["gold_code_sha256"] == GOLD_CODE and a["publish_code_sha256"] == PUB_CODE and a["schedules"] == b["schedules"] and a["series_prefixes"] == 939 and count(a["series_with_day"], 1) and a["sample_ok"] is True,
         "after: the gold day holds the dry run's rows, the gold total moved by exactly (rows - 3), the partitions, codes and schedules equal, 939 series, a sample ok")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0} and isinstance(rec["notes"], str) and 30 <= len(rec["notes"]) <= 3000
         and "YTD" in rec["notes"] and "Not measured" in rec["notes"], "the ledger left OPEN for the issuer; the reads block; notes that say the YTD return still reads Not measured while other days are absent (CTO condition, msg 10363)")
    return True


def series_invariant(prev, cur):
    """prev and cur: decoded series.json.gz dicts of one account. True when cur differs from prev ONLY by the added day and the three movable fields on the next day."""
    cols = [k for k in prev if isinstance(prev[k], list) and len(prev[k]) == len(prev["date"])]
    need(set(cols) == {k for k in cur if isinstance(cur[k], list) and len(cur[k]) == len(cur["date"])}, "the column set differs between the versions")
    pi = {d: i for i, d in enumerate(prev["date"])}
    ci = {d: i for i, d in enumerate(cur["date"])}
    need(set(pi) <= set(ci), "a day was REMOVED from the series")
    added = sorted(set(ci) - set(pi))
    need(added in ([], [DAY]), "the dates gained must be exactly [] or [%s], read %s" % (DAY, added))
    need(cur["date"] == sorted(cur["date"]), "the dates are not ascending")
    for d, i in pi.items():
        j = ci[d]
        for k in cols:
            if k == "date" or prev[k][i] == cur[k][j]:
                continue
            need(d == NEXT_DAY and k in MOVABLE, "a common day changed: %s on %s" % (k, d))
    return added


def check_live_gold(rec, cur_rows, prev_rows, prev_versions, total_rows_after, partitions, gold_cfg, pub_cfg, schedules):
    need(cur_rows == rec["after"]["gold_day_rows"] == rec["rewrite"]["rows"], "the live gold day holds %s rows, the record says %s" % (cur_rows, rec["rewrite"]["rows"]))
    need(prev_rows == 3 and prev_versions == rec["rewrite"]["day_versions_after"], "the previous (3-row) version must be kept and the version count must equal the record's")
    need(total_rows_after == rec["after"]["gold_total_rows"] and partitions == rec["after"]["partitions"], "the live gold total or partition count differs from the record")
    need(gold_cfg["CodeSha256"] == GOLD_CODE and pub_cfg["CodeSha256"] == PUB_CODE, "a function's code hash moved")
    need(schedules == {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}, "a schedule state moved")
    return True


def check_live_series(rec, prefixes, with_day, results):
    need(prefixes == 939, "the live series prefix count is %s, not 939" % prefixes)
    need(with_day == rec["after"]["series_with_day"], "the live number of series holding %s is %s, the record says %s" % (DAY, with_day, rec["after"]["series_with_day"]))
    need(results and all(r is True for r in results), "a sampled series differs from its previous version beyond the allowed change")
    return True


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    packet_sha = hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest()
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8") if (root / COO_HALF_REL).is_file() else ""
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8") if (root / CTO_HALF_REL).is_file() else ""
    ledger_exists = bool(list((root / "org/critical_paths/.open_deploys").glob(LEDGER_SLUG + "*.json"))) or bool(list((root / "org/critical_paths/change_management").glob("*" + LEDGER_SLUG + "*")))
    check_record(rec, packet_sha, coo, cto, ledger_exists)
    scrub = dict(rec, notes=re.sub(r"[a-z][a-z0-9-]*-\d{8}", "ledger", str(rec["notes"])))
    need(not H.digit_runs(scrub), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(scrub)[:2])
    if cid == "DBC195-1-AC1":
        print("OK: both halves signed at the packet's sha256, the ledger, the before reads, the dry run in its band, the rewrite (version +1, prior kept), the pre-write diff inside its STOP lines, the canary, the full republish, the after-read, no id")
        return True
    import boto3
    s3 = boto3.client("s3")
    if cid == "DBC195-2-AC1":
        import pyarrow.parquet as pq
        lam, sch = boto3.client("lambda", region_name="us-east-1"), boto3.client("scheduler", region_name="us-east-1")
        key_prefix = GOLD_PREFIX + "date=%s/" % DAY
        objs = [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=key_prefix).get("Contents", []) if o["Key"].endswith(".parquet")]
        need(len(objs) == 1, "the gold day must hold exactly one object")
        vs = sorted([v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=objs[0]).get("Versions", []) if v["Key"] == objs[0]], key=lambda v: v["LastModified"], reverse=True)

        def rows_of(vid):
            body = s3.get_object(Bucket=BUCKET, Key=objs[0], VersionId=vid)["Body"].read()
            return pq.ParquetFile(io.BytesIO(body)).metadata.num_rows
        cur, prev = rows_of(vs[0]["VersionId"]), rows_of(vs[1]["VersionId"]) if len(vs) > 1 else -1
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
        check_live_gold(rec, cur, prev, len(vs), total, len(parts), lam.get_function_configuration(FunctionName=GOLD_FN), lam.get_function_configuration(FunctionName=PUB_FN), sched)
        print("OK: live: the gold day holds %d rows as recorded, its 3-row version is kept (%d versions), the gold total and partition count equal the record's, both functions and both schedules are as before" % (cur, len(vs)))
        return True
    if cid == "DBC195-3-AC1":
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
        with_day = 0
        for p in prefixes:
            if DAY in load(p + "series.json.gz")["date"]:
                with_day += 1
        sample = sorted(prefixes)[:: max(1, len(prefixes) // 60)][:60]
        results = []
        for p in sample:
            key = p + "series.json.gz"
            vs = sorted([v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=key).get("Versions", []) if v["Key"] == key], key=lambda v: v["LastModified"], reverse=True)
            if len(vs) < 2:
                results.append(False)
                continue
            try:
                series_invariant(load(key, vs[1]["VersionId"]), load(key, vs[0]["VersionId"]))
                results.append(True)
            except Fail:
                results.append(False)
        check_live_series(rec, len(prefixes), with_day, results)
        print("OK: live: 939 series prefixes, %d hold %s as recorded, and %d sampled series differ from their previous version only by the added day and the three fields on %s" % (with_day, DAY, len(sample), NEXT_DAY))
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic():
    return {"claim": "measured", "gates": {"packet_sha256": "p" * 64, "coo_half_signed": True, "cto_half_signed": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
            "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
            "before": {"day_rows": 3, "day_objects": 1, "day_versions": 1, "full_day_rows": 879, "gold_total_rows": 60000, "partitions": 69, "series_prefixes": 939, "series_objects": 1878, "series_versions": 2800,
                       "gold_code_sha256": GOLD_CODE, "publish_code_sha256": PUB_CODE, "schedules": {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}},
            "dry_run": {"ok": True, "days": [DAY], "held": 0, "rows": 880, "gold_objects_before": 69, "gold_objects_after": 69, "gold_versions_before": 69, "gold_versions_after": 69},
            "rewrite": {"rows": 880, "day_versions_after": 2, "prior_version_kept": True, "other_partitions_unchanged": True},
            "prewrite": {"accounts_gaining_the_day": 877, "other_field_changes_on_common_days": 0, "changed_dates": [NEXT_DAY], "days_removed": 0, "refused": 0},
            "publish_dry": {"published": 939, "refused": 40},
            "canary": {"account_digest12": "a" * 12, "dates_gained": [DAY], "common_fields_equal": True, "only_next_day_three_fields_differ": True, "manifest_unchanged_but_dates": True},
            "publish_full": {"published": 939, "refused": 40, "objects_before": 1878, "objects_after": 1878, "versions_before": 2800, "versions_after": 3700},
            "after": {"gold_day_rows": 880, "gold_total_rows": 60000 - 3 + 880, "partitions": 69, "gold_code_sha256": GOLD_CODE, "publish_code_sha256": PUB_CODE, "schedules": {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"},
                      "series_prefixes": 939, "series_with_day": 877, "sample_ok": True},
            "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}, "notes": "Counts and statuses only; the six other absent days were not touched; the YTD return still reads Not measured while any of the 6 other absent days is in the window."}


def selftest():
    rec = synthetic()
    coo, cto = "SIGNED " + "p" * 64, "SIGNED " + "p" * 8

    def go(r, **kw):
        return check_record(r, kw.get("sha", "p" * 64), kw.get("coo", coo), kw.get("cto", cto), kw.get("led", True))
    assert go(rec)
    n = 0

    def red(fn, label):
        nonlocal n
        try:
            fn()
        except Fail:
            n += 1
            return
        raise AssertionError("mutant passed: " + label)

    def mut(label, fn):
        r = copy.deepcopy(rec)
        fn(r)
        red(lambda: go(r), label)
    red(lambda: go(rec, sha="q" * 64), "packet sha")
    red(lambda: go(rec, coo="DRAFT"), "coo unsigned")
    red(lambda: go(rec, cto="SIGNED"), "cto unbound")
    red(lambda: go(rec, led=False), "ledger")
    mut("claim", lambda r: r.update(claim="inferred"))
    mut("open legs", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1))
    mut("before day rows", lambda r: r["before"].update(day_rows=4))
    mut("before code", lambda r: r["before"].update(gold_code_sha256="x="))
    mut("before schedule", lambda r: r["before"]["schedules"].update(publish_daily="ENABLED"))
    mut("dry band low", lambda r: (r["dry_run"].update(rows=800), r["rewrite"].update(rows=800), r["after"].update(gold_day_rows=800, gold_total_rows=60000 - 3 + 800)))
    mut("dry band high", lambda r: (r["dry_run"].update(rows=1000), r["rewrite"].update(rows=1000), r["after"].update(gold_day_rows=1000, gold_total_rows=60000 - 3 + 1000)))
    mut("dry held", lambda r: r["dry_run"].update(held=1))
    mut("dry wrote", lambda r: r["dry_run"].update(gold_versions_after=70))
    mut("dry day", lambda r: r["dry_run"].update(days=["2026-07-28"]))
    mut("rewrite rows", lambda r: r["rewrite"].update(rows=881))
    mut("rewrite version", lambda r: r["rewrite"].update(day_versions_after=3))
    mut("prior not kept", lambda r: r["rewrite"].update(prior_version_kept=False))
    mut("other partitions", lambda r: r["rewrite"].update(other_partitions_unchanged=False))
    mut("prewrite other fields", lambda r: r["prewrite"].update(other_field_changes_on_common_days=1))
    mut("prewrite dates", lambda r: r["prewrite"].update(changed_dates=[NEXT_DAY, "2026-07-29"]))
    mut("prewrite removed", lambda r: r["prewrite"].update(days_removed=1))
    mut("prewrite refused", lambda r: r["prewrite"].update(refused=2))
    mut("publish dry refused", lambda r: r["publish_dry"].update(refused=300))
    mut("canary dates", lambda r: r["canary"].update(dates_gained=[DAY, NEXT_DAY]))
    mut("canary common", lambda r: r["canary"].update(common_fields_equal=False))
    mut("canary digest", lambda r: r["canary"].update(account_digest12="short"))
    mut("full published", lambda r: r["publish_full"].update(published=938))
    mut("full refused", lambda r: r["publish_full"].update(refused=41))
    mut("dry refused 39", lambda r: r["publish_dry"].update(refused=39))
    mut("dry refused 41", lambda r: r["publish_dry"].update(refused=41))
    mut("notes without the YTD sentence", lambda r: r.update(notes="Counts and statuses only; the six other absent days were not touched; nothing else changed in the window."))
    mut("full objects", lambda r: r["publish_full"].update(objects_after=1900))
    mut("full versions", lambda r: r["publish_full"].update(versions_after=2900))
    mut("after day rows", lambda r: r["after"].update(gold_day_rows=879))
    mut("after total", lambda r: r["after"].update(gold_total_rows=61000))
    mut("after code", lambda r: r["after"].update(publish_code_sha256="x="))
    mut("after series", lambda r: r["after"].update(series_prefixes=938))
    mut("after sample", lambda r: r["after"].update(sample_ok=False))
    mut("ledger closed", lambda r: r.update(ledger_closed=True))
    mut("reads", lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}))
    mut("extra key", lambda r: r.update(z=1))
    prev = {"date": ["2026-07-24", "2026-07-28", "2026-07-29"], "value": [1.0, 2.0, 3.0], "total_return_daily": [0.1, None, 0.2], "day_quality": ["MEASURED", "NOT_MEASURABLE", "MEASURED"], "return_basis": ["TWR", "NOT_MEASURABLE", "TWR"], "method_version": 1}
    cur = {"date": ["2026-07-24", DAY, "2026-07-28", "2026-07-29"], "value": [1.0, 1.5, 2.0, 3.0], "total_return_daily": [0.1, 0.05, 0.03, 0.2], "day_quality": ["MEASURED", "MEASURED", "MEASURED", "MEASURED"], "return_basis": ["TWR", "TWR", "TWR", "TWR"], "method_version": 1}
    assert series_invariant(prev, cur) == [DAY]
    assert series_invariant(prev, prev) == []
    red(lambda: series_invariant(prev, dict(cur, value=[1.0, 1.5, 2.1, 3.0])), "a common day's value moved")
    red(lambda: series_invariant(prev, dict(cur, total_return_daily=[0.11, 0.05, 0.03, 0.2])), "a common day's return moved on another day")
    red(lambda: series_invariant(prev, {k: (v[1:] if isinstance(v, list) else v) for k, v in cur.items()}), "a day removed")
    red(lambda: series_invariant(prev, dict(cur, date=["2026-07-24", "2026-07-25", "2026-07-28", "2026-07-29"])), "another day added")
    red(lambda: series_invariant(prev, dict(cur, external_flow=[0, 0, 0, 0])), "a column appeared")
    red(lambda: series_invariant(prev, dict(cur, income=[0, 0, 0, 0], **{k: cur[k] for k in cur})), "a column appeared (income)")
    red(lambda: series_invariant(prev, dict(cur, date=["2026-07-24", "2026-07-28", DAY, "2026-07-29"])), "dates not ascending")
    cfg = {"CodeSha256": GOLD_CODE}
    pcfg = {"CodeSha256": PUB_CODE}
    sch = {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}
    assert check_live_gold(rec, 880, 3, 2, rec["after"]["gold_total_rows"], 69, cfg, pcfg, sch)
    red(lambda: check_live_gold(rec, 879, 3, 2, rec["after"]["gold_total_rows"], 69, cfg, pcfg, sch), "live day rows")
    red(lambda: check_live_gold(rec, 880, 880, 2, rec["after"]["gold_total_rows"], 69, cfg, pcfg, sch), "live prior version lost")
    red(lambda: check_live_gold(rec, 880, 3, 3, rec["after"]["gold_total_rows"], 69, cfg, pcfg, sch), "live versions")
    red(lambda: check_live_gold(rec, 880, 3, 2, 1, 69, cfg, pcfg, sch), "live total")
    red(lambda: check_live_gold(rec, 880, 3, 2, rec["after"]["gold_total_rows"], 70, cfg, pcfg, sch), "live partitions")
    red(lambda: check_live_gold(rec, 880, 3, 2, rec["after"]["gold_total_rows"], 69, {"CodeSha256": "x="}, pcfg, sch), "live gold code")
    red(lambda: check_live_gold(rec, 880, 3, 2, rec["after"]["gold_total_rows"], 69, cfg, pcfg, dict(sch, publish_daily="ENABLED")), "live schedule")
    assert check_live_series(rec, 939, 877, [True] * 60)
    red(lambda: check_live_series(rec, 938, 877, [True]), "live prefixes")
    red(lambda: check_live_series(rec, 939, 870, [True]), "live with day")
    red(lambda: check_live_series(rec, 939, 877, [True, False]), "a sample differs")
    red(lambda: check_live_series(rec, 939, 877, []), "no sample")
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
