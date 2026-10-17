"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- the APPLY of the signed ALL-DAYS rewrite pair: every landed Cottonwood gold day from the claim floor (66 days at the 2026-10-17 census) is REWRITTEN through the
function's explicit rewrite event with the late-posting reader, in events of landed trading days (at most 25 days each), a single-day scaling dry run first, and the series republished ONCE. WORLD, served output. The record is
the applier's (`0.7.0_AE_CloudOps~IB2`); the checker re-reads the gold days and their prior versions and COMPARES each sampled series with the PREVIOUS VERSION of its own object (the bucket is versioned), so the invariant
"only the five changed-row days are added and only the three movable fields move on common days" is graded on the data, not on the applier's report. The expected row counts come from the issuer's committed dry derivation
(`reads/RD_COT_ALLDAYS_DRY_20261017.json`), not from the applier.

  DBC201-1-AC1  the record: both halves signed at the packet's sha256, the ledger, the before reads, the scaling run, every event's dry run in its band, the rewrites, the pre-write diff inside its STOP lines, the canary, the one republish, the after-read
  DBC201-2-AC1  FRESH live reads of the gold days: each current version holds the recorded rows, its prior version is kept, the daily absolute flows fell on every day whose rows did not change, every other partition is unchanged, both functions and both schedules are as before
  DBC201-3-AC1  FRESH live reads of the series: 939 prefixes, each changed-row day present in the recorded number of series, and 60 sampled series differ from their previous version ONLY by the added days and the three movable fields

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


H = helper("r147/p151_pubapply.py", "p151_helper_201")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_ALLDAYS_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ALLDAYS_REWRITE_AND_REPUBLISH.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_ALLDAYS_REWRITE_AND_REPUBLISH_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_ALLDAYS_REWRITE_AND_REPUBLISH_CTO_HALF.md"
DRY_REL = D + "2.0.0_SA_COO~D2/reads/RD_COT_ALLDAYS_DRY_20261017.json"
LEDGER_RE = re.compile(r"irpt-dashbd-cottonwood-alldays-rewrite-\d{8}")
GOLD_FN, PUB_FN = "irpt-cot-account-return-daily-lambda", "irpt-cot-reporting-publish-lambda"
PUB_CODE = "vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE="
BUCKET, GOLD_PREFIX, PUB_PREFIX = "opal-data-cottonwood", "irpt/cottonwood/gold/account_return_daily/", "irpt/cottonwood/platinum/reporting/"
FLOOR = "2026-07-10"
UNLANDED = ("2026-08-19", "2026-09-24", "2026-09-25")
EVENT_MAX = 25
ROWS_TOL_PCT = 2
EXTRA_BAND = (840, 1000)
PROJECTED_MAX_S = 500
DURATION_MAX_S = 720
MEMORY_MAX_MB = 819
REFUSED_MAX = 40
MAX_NM_PCT = 15
MOVABLE = ("total_return_daily", "day_quality", "return_basis")
SCHED = {"account_return_daily": "ENABLED", "publish_daily": "DISABLED"}
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("packet_sha256", "account_digest12", "code_sha256", "invoked_utc", "abs_flow_cents", "abs_flow_after_cents")


def count(x, lo=0):
    return is_int(x) and x >= lo


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x > 0


def per_day(x, days, pred):
    return isinstance(x, dict) and sorted(x) == sorted(days) and all(count(x[d]) and pred(x[d]) for d in days)


def dry_expectations(dry):
    """From the issuer's committed dry derivation: {day: expected rows} and the set of days whose rows differ from the landed gold."""
    rows, changed = {}, set()
    for day, v in dry["days"].items():
        need("new" in v, "the dry derivation holds a held day: %s" % day)
        rows[day] = v["new"]["rows"]
        if v["new"]["rows"] != v["old"]["rows"]:
            changed.add(day)
    return rows, changed


def check_event(ev, days_slice, label):
    need(isinstance(ev, dict) and {"first", "last", "days"} <= set(ev) and ev["days"] == days_slice and ev["first"] == days_slice[0] and ev["last"] == days_slice[-1], "%s: event bounds differ from the record's days" % label)
    need(1 <= len(ev["days"]) <= EVENT_MAX, "%s: an event holds 1 to %d days" % (label, EVENT_MAX))
    need(not any(ev["first"] < d < ev["last"] for d in UNLANDED), "%s: an event spans an unlanded day" % label)
    return True


def check_run_events(events, rec_events, scaling, label):
    need(isinstance(events, list) and len(events) == len(rec_events), "%s: one entry per event" % label)
    for ev, base in zip(events, rec_events):
        check_event(ev, base["days"], label)
        need({"first", "last", "days", "held", "duration_s", "max_memory_mb"} == set(ev) and ev["held"] == 0 and num(ev["duration_s"]) and ev["duration_s"] <= DURATION_MAX_S and num(ev["max_memory_mb"]) and ev["max_memory_mb"] <= MEMORY_MAX_MB,
             "%s: held 0, duration at most %d s, memory at most %d MB" % (label, DURATION_MAX_S, MEMORY_MAX_MB))
        need(scaling["duration_s"] * len(ev["days"]) <= PROJECTED_MAX_S, "%s: the scaling run projects %.0f s for %d days, over the %d s line: the event had to be split" % (label, scaling["duration_s"] * len(ev["days"]), len(ev["days"]), PROJECTED_MAX_S))
    return True


def check_record(rec, packet_sha, packet_text, coo_text, cto_text, ledger_exists, exp_rows, changed):
    exp = {"claim", "gates", "ledger_entry", "applier", "days", "events", "before", "scaling", "dry_run", "rewrite", "prewrite", "publish_dry", "canary", "publish_full", "after", "ledger_closed", "reads", "notes"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    days = rec["days"]
    need(isinstance(days, list) and days == sorted(set(days)) and set(exp_rows) <= set(days) and all(d >= "2026-10-16" for d in days if d not in exp_rows) and not (set(days) & set(UNLANDED)),
         "days: ascending, holding every day of the dry derivation, any other day on or after 2026-10-16, none of %s" % (UNLANDED,))
    need(days[0] == FLOOR, "the first day must be the claim floor %s" % FLOOR)
    ev = rec["events"]
    need(isinstance(ev, list) and ev and sum((e["days"] for e in ev), []) == days, "the events must partition the days in order")
    for e in ev:
        check_event(e, e["days"], "events")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_sha256", "coo_half_signed", "cto_half_signed", "one_change_at_a_time", "live_matches_packet", "transaction_pair_ledger_closed"}, "gates keys")
    need(g["packet_sha256"] == packet_sha and g["coo_half_signed"] is True and "SIGNED" in coo_text and packet_sha in coo_text, "the packet's sha256 or the COO half")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and packet_sha[:8] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and count(oc["worktrees_read"], 1) and oc["open_markers_naming_this_surface"] == 0 and g["live_matches_packet"] is True and g["transaction_pair_ledger_closed"] is True,
         "one change at a time; live matches the packet; the transaction pair's ledger is closed")
    need(isinstance(rec["ledger_entry"], str) and LEDGER_RE.fullmatch(rec["ledger_entry"]) and ledger_exists and rec["applier"] == APPLIER, "the ledger exists and is named irpt-dashbd-cottonwood-alldays-rewrite-<date>; the applier is %s" % APPLIER)
    b = rec["before"]
    keys = {"day_rows", "day_versions", "not_measurable", "abs_flow_cents", "gold_total_rows", "partitions", "series_prefixes", "series_objects", "series_versions", "gold_code_sha256", "publish_code_sha256", "schedules"}
    need(isinstance(b, dict) and set(b) == keys and per_day(b["day_rows"], days, lambda n: n >= 1) and per_day(b["day_versions"], days, lambda n: n >= 1) and per_day(b["not_measurable"], days, lambda n: True)
         and per_day(b["abs_flow_cents"], days, lambda n: True) and count(b["gold_total_rows"], 1) and b["partitions"] >= len(days) and b["series_prefixes"] == 939 and count(b["series_objects"], 939) and count(b["series_versions"], 939)
         and isinstance(b["gold_code_sha256"], str) and b["gold_code_sha256"] in packet_text and b["publish_code_sha256"] == PUB_CODE and b["schedules"] == SCHED,
         "before: per-day rows, versions, NOT_MEASURABLE and absolute-flow counts for every day, 939 prefixes, the gold code hash printed in the packet, the publish code hash, the two schedule states")
    sc = rec["scaling"]
    need(isinstance(sc, dict) and set(sc) == {"day", "duration_s", "max_memory_mb"} and sc["day"] in days and num(sc["duration_s"]) and sc["duration_s"] <= DURATION_MAX_S and num(sc["max_memory_mb"]) and sc["max_memory_mb"] <= MEMORY_MAX_MB,
         "scaling: one day of the days, its duration and memory inside the lines")
    d = rec["dry_run"]
    need(isinstance(d, dict) and set(d) == {"ok", "events", "rows", "gold_objects_before", "gold_objects_after", "gold_versions_before", "gold_versions_after"} and d["ok"] is True
         and d["gold_objects_before"] == d["gold_objects_after"] and d["gold_versions_before"] == d["gold_versions_after"], "dry run: ok, nothing written")
    check_run_events(d["events"], ev, sc, "dry run")
    need(isinstance(d["rows"], dict) and sorted(d["rows"]) == sorted(days) and all(count(d["rows"][x]) for x in days), "dry run: one row count per day")
    for x in days:
        if x in exp_rows:
            need(abs(d["rows"][x] - exp_rows[x]) * 100 <= ROWS_TOL_PCT * exp_rows[x], "dry run: %s holds %d rows, the issuer's dry derivation says %d (more than %d percent apart)" % (x, d["rows"][x], exp_rows[x], ROWS_TOL_PCT))
        else:
            need(EXTRA_BAND[0] <= d["rows"][x] <= EXTRA_BAND[1], "dry run: a day beyond the census must hold %s rows" % (EXTRA_BAND,))
    w = rec["rewrite"]
    need(isinstance(w, dict) and set(w) == {"events", "rows", "day_versions_after", "prior_versions_kept", "other_partitions_unchanged", "not_measurable_after", "abs_flow_after_cents"} and w["rows"] == d["rows"]
         and isinstance(w["day_versions_after"], dict) and sorted(w["day_versions_after"]) == sorted(days) and all(w["day_versions_after"][x] == b["day_versions"][x] + 1 for x in days)
         and w["prior_versions_kept"] is True and w["other_partitions_unchanged"] is True, "rewrite: each day's dry-run rows, its version count +1, the prior versions kept, every other partition unchanged")
    check_run_events(w["events"], ev, sc, "rewrite")
    need(per_day(w["not_measurable_after"], days, lambda n: True) and per_day(w["abs_flow_after_cents"], days, lambda n: True), "rewrite: NOT_MEASURABLE and absolute-flow counts for every day")
    for x in days:
        if x != FLOOR:
            need(w["not_measurable_after"][x] * 100 <= MAX_NM_PCT * w["rows"][x], "rewrite: %s holds more than %d percent NOT_MEASURABLE" % (x, MAX_NM_PCT))
        if x not in changed:
            need(w["abs_flow_after_cents"][x] <= b["abs_flow_cents"][x], "rewrite: %s absolute flows ROSE (%d to %d cents) on a day whose rows did not change" % (x, b["abs_flow_cents"][x], w["abs_flow_after_cents"][x]))
    p = rec["prewrite"]
    need(isinstance(p, dict) and set(p) == {"accounts_gaining_by_day", "other_field_changes_on_common_days", "fields_changed", "days_removed", "refused"} and per_day(p["accounts_gaining_by_day"], sorted(changed & set(days)), lambda n: n >= 1)
         and p["other_field_changes_on_common_days"] == 0 and isinstance(p["fields_changed"], list) and set(p["fields_changed"]) <= set(MOVABLE) and p["days_removed"] == 0 and count(p["refused"]) and p["refused"] <= REFUSED_MAX,
         "prewrite: gains only on the changed-row days, only %s may change on a common day, nothing removed, refused at most %d" % (MOVABLE, REFUSED_MAX))
    pd = rec["publish_dry"]
    need(isinstance(pd, dict) and set(pd) == {"published", "refused"} and pd["published"] == 939 and count(pd["refused"]) and pd["refused"] <= REFUSED_MAX, "publish dry run: 939 published, refused at most %d" % REFUSED_MAX)
    c = rec["canary"]
    need(isinstance(c, dict) and set(c) == {"account_digest12", "dates_gained", "common_fields_equal_except_movable", "manifest_unchanged_but_dates"} and re.fullmatch(r"[0-9a-f]{12}", str(c["account_digest12"]))
         and isinstance(c["dates_gained"], list) and c["dates_gained"] and set(c["dates_gained"]) <= set(changed) and c["common_fields_equal_except_movable"] is True and c["manifest_unchanged_but_dates"] is True,
         "canary: one account by digest; the dates gained are a non-empty subset of the changed-row days; common fields equal the previous version except the three movable ones; the manifest unchanged but its dates")
    f = rec["publish_full"]
    need(isinstance(f, dict) and set(f) == {"published", "refused", "objects_before", "objects_after", "versions_before", "versions_after"} and f["published"] == 939 and f["refused"] == pd["refused"]
         and f["objects_before"] == f["objects_after"] == b["series_objects"] and f["versions_after"] - f["versions_before"] >= 939 - pd["refused"], "full republish: 939 published, refused as in the dry run, the same objects, new versions")
    a = rec["after"]
    keys2 = {"gold_day_rows", "gold_total_rows", "partitions", "gold_code_sha256", "publish_code_sha256", "schedules", "series_prefixes", "series_with_day", "sample_ok"}
    need(isinstance(a, dict) and set(a) == keys2 and a["gold_day_rows"] == d["rows"] and a["gold_total_rows"] == b["gold_total_rows"] - sum(b["day_rows"].values()) + sum(d["rows"].values()) and a["partitions"] == b["partitions"]
         and a["gold_code_sha256"] == b["gold_code_sha256"] and a["publish_code_sha256"] == PUB_CODE and a["schedules"] == b["schedules"] and a["series_prefixes"] == 939
         and per_day(a["series_with_day"], sorted(changed & set(days)), lambda n: n >= 1) and a["sample_ok"] is True,
         "after: each gold day holds the dry run's rows, the gold total moved by exactly (the new rows - the old rows), the partitions, codes and schedules equal, 939 series, each changed-row day in at least one series, a sample ok")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0} and isinstance(rec["notes"], str) and 30 <= len(rec["notes"]) <= 3000
         and "YTD" in rec["notes"] and "Not measured" in rec["notes"] and "external flows" in rec["notes"], "the ledger left OPEN for the issuer; the reads block; notes that say the external flows are no longer summed across partitions and the YTD return still reads Not measured while other days are absent")
    return True


def series_invariant(prev, cur, changed):
    """prev and cur: decoded series.json.gz dicts of one account. True when cur differs from prev ONLY by added days (a subset of `changed`) and the three movable fields on common days."""
    cols = [k for k in prev if isinstance(prev[k], list) and len(prev[k]) == len(prev["date"])]
    need(set(cols) == {k for k in cur if isinstance(cur[k], list) and len(cur[k]) == len(cur["date"])}, "the column set differs between the versions")
    pi = {x: i for i, x in enumerate(prev["date"])}
    ci = {x: i for i, x in enumerate(cur["date"])}
    need(set(pi) <= set(ci), "a day was REMOVED from the series")
    added = sorted(set(ci) - set(pi))
    need(set(added) <= set(changed), "the dates gained must be a subset of the changed-row days %s, read %s" % (sorted(changed), added))
    need(cur["date"] == sorted(cur["date"]), "the dates are not ascending")
    for x, i in pi.items():
        j = ci[x]
        for k in cols:
            if k == "date" or prev[k][i] == cur[k][j]:
                continue
            need(k in MOVABLE, "a common day changed a field that may not move: %s on %s" % (k, x))
    return added


def check_live_gold(rec, changed, cur_rows, prev_rows, versions, nm, flows, total_rows_after, partitions, gold_cfg, pub_cfg, schedules):
    days = rec["days"]
    need(cur_rows == rec["after"]["gold_day_rows"] == rec["rewrite"]["rows"], "the live gold days hold different rows than the record")
    need(all(prev_rows[x] == rec["before"]["day_rows"][x] for x in days) and versions == rec["rewrite"]["day_versions_after"], "each previous version must be kept and each version count must equal the record's")
    need(nm == rec["rewrite"]["not_measurable_after"] and all(nm[x] * 100 <= MAX_NM_PCT * cur_rows[x] for x in days if x != FLOOR), "a live gold day holds more than %d percent NOT_MEASURABLE rows, or the count differs from the record" % MAX_NM_PCT)
    need(flows == rec["rewrite"]["abs_flow_after_cents"] and all(flows[x] <= rec["before"]["abs_flow_cents"][x] for x in days if x not in changed), "a live day's absolute flows differ from the record or rose on an unchanged-row day")
    need(total_rows_after == rec["after"]["gold_total_rows"] and partitions == rec["after"]["partitions"], "the live gold total or partition count differs from the record")
    need(gold_cfg["CodeSha256"] == rec["after"]["gold_code_sha256"] and pub_cfg["CodeSha256"] == PUB_CODE, "a function's code hash moved")
    need(schedules == SCHED, "a schedule state moved")
    return True


def check_live_series(rec, prefixes, with_day, results):
    need(prefixes == 939, "the live series prefix count is %s, not 939" % prefixes)
    need(with_day == rec["after"]["series_with_day"], "the live number of series holding each changed-row day is %s, the record says %s" % (with_day, rec["after"]["series_with_day"]))
    need(results and all(r is True for r in results), "a sampled series differs from its previous version beyond the allowed change")
    return True


def load_dry(root):
    return dry_expectations(json.loads((Path(root) / DRY_REL).read_bytes().decode("utf-8")))


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    packet_sha = hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest()
    packet_text = (root / PACKET_REL).read_text(encoding="utf-8")
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8") if (root / COO_HALF_REL).is_file() else ""
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8") if (root / CTO_HALF_REL).is_file() else ""
    slug = str(rec.get("ledger_entry"))
    ledger_exists = bool(list((root / "org/critical_paths/.open_deploys").glob(slug + "*.json"))) or bool(list((root / "org/critical_paths/change_management").glob("*" + slug + "*")))
    exp_rows, changed = load_dry(root)
    check_record(rec, packet_sha, packet_text, coo, cto, ledger_exists, exp_rows, changed)
    scrub = dict(rec, notes=re.sub(r"[a-z][a-z0-9-]*-\d{8}", "ledger", str(rec["notes"])), ledger_entry="ledger")
    need(not H.digit_runs(scrub), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(scrub)[:2])
    days = rec["days"]
    if cid == "DBC201-1-AC1":
        print("OK: both halves signed at the packet's sha256, the ledger, the before reads, the scaling run, every event's dry run in its band against the issuer's dry derivation, the rewrites (version +1, prior versions kept, flows fell), the pre-write diff inside its STOP lines, the canary, the one republish, the after-read, no id")
        return True
    import boto3
    s3 = boto3.client("s3")
    if cid == "DBC201-2-AC1":
        import pyarrow.parquet as pq
        lam, sch = boto3.client("lambda", region_name="us-east-1"), boto3.client("scheduler", region_name="us-east-1")
        cur, prev, vcount, nm, flows = {}, {}, {}, {}, {}
        for x in days:
            objs = [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=GOLD_PREFIX + "date=%s/" % x).get("Contents", []) if o["Key"].endswith(".parquet")]
            need(len(objs) == 1, "the gold day %s must hold exactly one object" % x)
            vs = sorted([v for v in s3.list_object_versions(Bucket=BUCKET, Prefix=objs[0]).get("Versions", []) if v["Key"] == objs[0]], key=lambda v: v["LastModified"], reverse=True)

            def table_of(vid, key=objs[0]):
                return pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key, VersionId=vid)["Body"].read()))
            now_t = table_of(vs[0]["VersionId"])
            cur[x] = now_t.num_rows
            nm[x] = sum(1 for q in now_t.column("day_quality").to_pylist() if q == "NOT_MEASURABLE")
            flows[x] = int(round(sum(abs(v) for v in now_t.column("external_flow").to_pylist() if v) * 100))
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
        check_live_gold(rec, changed, cur, prev, vcount, nm, flows, total, len(parts), lam.get_function_configuration(FunctionName=GOLD_FN), lam.get_function_configuration(FunctionName=PUB_FN), sched)
        print("OK: live: the %d gold days hold the recorded rows with few NOT_MEASURABLE, each earlier version is kept, the absolute flows fell on every unchanged-row day, the gold total and partition count equal the record's, both functions and both schedules are as before" % len(days))
        return True
    if cid == "DBC201-3-AC1":
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
        ch = sorted(changed & set(days))
        with_day = {x: 0 for x in ch}
        for p in prefixes:
            have = set(load(p + "series.json.gz")["date"])
            for x in ch:
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
                series_invariant(load(key, vs[1]["VersionId"]), load(key, vs[0]["VersionId"]), changed)
                results.append(True)
            except Fail:
                results.append(False)
        check_live_series(rec, len(prefixes), with_day, results)
        print("OK: live: 939 series prefixes, each changed-row day present as recorded, and %d sampled series differ from their previous version only by the added days and the three movable fields" % len(sample))
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic_days():
    """A small census: the floor, ten ordinary days, one changed-row day and a day after an unlanded gap, in two events."""
    first = ["2026-07-10"] + ["2026-07-%02d" % d for d in (13, 14, 15, 16, 17)]
    second = ["2026-08-20", "2026-08-21", "2026-08-24"]
    return first, second


def synthetic():
    first, second = synthetic_days()
    days = first + second
    exp_rows = {x: 880 + i for i, x in enumerate(days)}
    changed = {"2026-07-14"}
    old = {x: (3 if x in changed else exp_rows[x]) for x in days}
    flows_old = {x: 1_000_000 + 13 * i for i, x in enumerate(days)}
    flows_new = {x: (flows_old[x] // 10 if x not in changed else 600_000) for x in days}
    ver = {x: 1 for x in days}
    ev = [{"first": first[0], "last": first[-1], "days": list(first)}, {"first": second[0], "last": second[-1], "days": list(second)}]
    run_ev = [dict(e, held=0, duration_s=30.0, max_memory_mb=700.0) for e in ev]
    nm_after = {x: (880 if x == FLOOR else 30) for x in days}
    rows_total = 60000
    rec = {"claim": "measured", "gates": {"packet_sha256": "p" * 64, "coo_half_signed": True, "cto_half_signed": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True,
                                          "transaction_pair_ledger_closed": True},
           "ledger_entry": "irpt-dashbd-cottonwood-alldays-rewrite-20261021", "applier": APPLIER, "days": list(days), "events": ev,
           "before": {"day_rows": dict(old), "day_versions": dict(ver), "not_measurable": {x: 30 for x in days}, "abs_flow_cents": dict(flows_old), "gold_total_rows": rows_total, "partitions": len(days) + 2, "series_prefixes": 939,
                      "series_objects": 1878, "series_versions": 2800, "gold_code_sha256": "CODEHASH=", "publish_code_sha256": PUB_CODE, "schedules": dict(SCHED)},
           "scaling": {"day": "2026-07-14", "duration_s": 12.0, "max_memory_mb": 600.0},
           "dry_run": {"ok": True, "events": copy.deepcopy(run_ev), "rows": dict(exp_rows), "gold_objects_before": 69, "gold_objects_after": 69, "gold_versions_before": 69, "gold_versions_after": 69},
           "rewrite": {"events": copy.deepcopy(run_ev), "rows": dict(exp_rows), "day_versions_after": {x: 2 for x in days}, "prior_versions_kept": True, "other_partitions_unchanged": True, "not_measurable_after": dict(nm_after),
                       "abs_flow_after_cents": dict(flows_new)},
           "prewrite": {"accounts_gaining_by_day": {"2026-07-14": 700}, "other_field_changes_on_common_days": 0, "fields_changed": ["total_return_daily", "day_quality"], "days_removed": 0, "refused": 40},
           "publish_dry": {"published": 939, "refused": 40},
           "canary": {"account_digest12": "a" * 12, "dates_gained": ["2026-07-14"], "common_fields_equal_except_movable": True, "manifest_unchanged_but_dates": True},
           "publish_full": {"published": 939, "refused": 40, "objects_before": 1878, "objects_after": 1878, "versions_before": 2800, "versions_after": 3700},
           "after": {"gold_day_rows": dict(exp_rows), "gold_total_rows": rows_total - sum(old.values()) + sum(exp_rows.values()), "partitions": len(days) + 2, "gold_code_sha256": "CODEHASH=", "publish_code_sha256": PUB_CODE, "schedules": dict(SCHED),
                     "series_prefixes": 939, "series_with_day": {"2026-07-14": 700}, "sample_ok": True},
           "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0},
           "notes": "Counts and statuses only; the external flows are no longer summed across overlapping partitions; the three days with no transactions were not touched; the YTD return still reads Not measured while any of those days is in the window."}
    return rec, exp_rows, changed


def selftest():
    rec, exp_rows, changed = synthetic()
    packet_text = "the deployed CodeSha256 CODEHASH= of the release bundle"
    coo, cto = "SIGNED " + "p" * 64, "SIGNED " + "p" * 8

    def go(r, **kw):
        return check_record(r, kw.get("sha", "p" * 64), kw.get("pk", packet_text), kw.get("coo", coo), kw.get("cto", cto), kw.get("led", True), kw.get("rows", exp_rows), kw.get("ch", changed))
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

    def mut(label, fn, **kw):
        r = copy.deepcopy(rec)
        fn(r)
        red(lambda: go(r, **kw), label)
    red(lambda: go(rec, sha="q" * 64), "packet sha")
    red(lambda: go(rec, coo="DRAFT"), "coo unsigned")
    red(lambda: go(rec, cto="SIGNED"), "cto unbound")
    red(lambda: go(rec, led=False), "ledger")
    red(lambda: go(rec, pk="no hash here"), "code hash not in the packet")
    mut("claim", lambda r: r.update(claim="inferred"))
    mut("extra key", lambda r: r.update(z=1))
    mut("days not from floor", lambda r: r.update(days=r["days"][1:]))
    mut("days miss a census day", lambda r: r["days"].remove("2026-07-15"))
    mut("days hold an unlanded day", lambda r: r["days"].insert(7, "2026-08-19"))
    mut("days extra before the 16th", lambda r: r["days"].append("2026-10-14"))
    mut("events do not partition", lambda r: r["events"][1]["days"].pop())
    mut("event over 25 days", lambda r: r["events"][0].update(days=["2026-07-%02d" % d for d in range(1, 27)]))
    mut("event spans an unlanded day", lambda r: r["events"][1].update(first="2026-08-17"))
    mut("open legs", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1))
    mut("transaction pair ledger open", lambda r: r["gates"].update(transaction_pair_ledger_closed=False))
    mut("ledger name", lambda r: r.update(ledger_entry="irpt-dashbd-cottonwood-reland-pair-20261017"))
    mut("before missing day", lambda r: r["before"]["day_rows"].pop("2026-08-24"))
    mut("before code", lambda r: r["before"].update(gold_code_sha256="OTHER="))
    mut("before publish code", lambda r: r["before"].update(publish_code_sha256="x="))
    mut("before schedule", lambda r: r["before"]["schedules"].update(publish_daily="ENABLED"))
    mut("before prefixes", lambda r: r["before"].update(series_prefixes=938))
    mut("before flows missing", lambda r: r["before"]["abs_flow_cents"].pop("2026-07-13"))
    mut("scaling day", lambda r: r["scaling"].update(day="2026-09-01"))
    mut("scaling memory", lambda r: r["scaling"].update(max_memory_mb=900.0))
    mut("scaling projects too long", lambda r: r["scaling"].update(duration_s=90.0))
    mut("dry held", lambda r: r["dry_run"]["events"][0].update(held=1))
    mut("dry wrote", lambda r: r["dry_run"].update(gold_versions_after=70))
    mut("dry duration", lambda r: r["dry_run"]["events"][1].update(duration_s=800.0))
    mut("dry memory", lambda r: r["dry_run"]["events"][1].update(max_memory_mb=850.0))
    mut("dry event bounds", lambda r: r["dry_run"]["events"][0].update(last="2026-07-16"))
    mut("dry rows far from the derivation", lambda r: r["dry_run"]["rows"].update({"2026-07-13": 700}))
    mut("dry row missing", lambda r: r["dry_run"]["rows"].pop("2026-07-17"))
    mut("rewrite rows", lambda r: r["rewrite"]["rows"].update({"2026-07-13": 899}))
    mut("rewrite version", lambda r: r["rewrite"]["day_versions_after"].update({"2026-07-14": 3}))
    mut("prior not kept", lambda r: r["rewrite"].update(prior_versions_kept=False))
    mut("other partitions", lambda r: r["rewrite"].update(other_partitions_unchanged=False))
    mut("rewrite not measurable high", lambda r: r["rewrite"]["not_measurable_after"].update({"2026-07-15": 500}))
    mut("floor day may be fully not measurable but another may not", lambda r: r["rewrite"]["not_measurable_after"].update({"2026-08-21": 880}))
    mut("flow rose on an unchanged day", lambda r: r["rewrite"]["abs_flow_after_cents"].update({"2026-07-13": 5_000_000}))
    mut("rewrite event duration", lambda r: r["rewrite"]["events"][0].update(duration_s=800.0))
    mut("prewrite zero gain", lambda r: r["prewrite"]["accounts_gaining_by_day"].update({"2026-07-14": 0}))
    mut("prewrite extra gain day", lambda r: r["prewrite"]["accounts_gaining_by_day"].update({"2026-07-15": 5}))
    mut("prewrite other fields", lambda r: r["prewrite"].update(other_field_changes_on_common_days=1))
    mut("prewrite field list", lambda r: r["prewrite"].update(fields_changed=["total_return_daily", "external_flow"]))
    mut("prewrite removed", lambda r: r["prewrite"].update(days_removed=1))
    mut("prewrite refused", lambda r: r["prewrite"].update(refused=41))
    mut("publish dry published", lambda r: r["publish_dry"].update(published=938))
    mut("canary dates", lambda r: r["canary"].update(dates_gained=["2026-07-13"]))
    mut("canary empty", lambda r: r["canary"].update(dates_gained=[]))
    mut("canary common", lambda r: r["canary"].update(common_fields_equal_except_movable=False))
    mut("canary digest", lambda r: r["canary"].update(account_digest12="short"))
    mut("canary manifest", lambda r: r["canary"].update(manifest_unchanged_but_dates=False))
    mut("full published", lambda r: r["publish_full"].update(published=938))
    mut("full refused differs", lambda r: r["publish_full"].update(refused=39))
    mut("full objects", lambda r: r["publish_full"].update(objects_after=1900))
    mut("full versions", lambda r: r["publish_full"].update(versions_after=2900))
    mut("after day rows", lambda r: r["after"]["gold_day_rows"].update({"2026-07-14": 3}))
    mut("after total", lambda r: r["after"].update(gold_total_rows=61000))
    mut("after code", lambda r: r["after"].update(gold_code_sha256="OTHER="))
    mut("after publish code", lambda r: r["after"].update(publish_code_sha256="x="))
    mut("after series", lambda r: r["after"].update(series_prefixes=938))
    mut("after series with day zero", lambda r: r["after"]["series_with_day"].update({"2026-07-14": 0}))
    mut("after sample", lambda r: r["after"].update(sample_ok=False))
    mut("ledger closed", lambda r: r.update(ledger_closed=True))
    mut("reads", lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}))
    mut("notes without the YTD sentence", lambda r: r.update(notes="Counts and statuses only; the external flows are no longer summed across overlapping partitions."))
    mut("notes without the flows sentence", lambda r: r.update(notes="Counts and statuses only; the YTD return still reads Not measured while any of those days is in the window."))
    prev = {"date": ["2026-07-13", "2026-07-15"], "value": [1.0, 3.0], "total_return_daily": [0.1, None], "day_quality": ["MEASURED", "NOT_MEASURABLE"], "return_basis": ["TWR", "NOT_MEASURABLE"], "method_version": 1}
    cur = {"date": ["2026-07-13", "2026-07-14", "2026-07-15"], "value": [1.0, 2.0, 3.0], "total_return_daily": [0.09, 0.05, 0.03], "day_quality": ["MEASURED"] * 3, "return_basis": ["TWR"] * 3, "method_version": 1}
    assert series_invariant(prev, cur, changed) == ["2026-07-14"]
    assert series_invariant(prev, prev, changed) == []
    red(lambda: series_invariant(prev, dict(cur, value=[1.1, 2.0, 3.0]), changed), "a common day's value moved")
    red(lambda: series_invariant(prev, {k: (v[1:] if isinstance(v, list) else v) for k, v in cur.items()}, changed), "a day removed")
    red(lambda: series_invariant(prev, cur, {"2026-08-03"}), "a day added that is not a changed-row day")
    red(lambda: series_invariant(prev, dict(cur, external_flow=[0, 0, 0]), changed), "a column appeared")
    red(lambda: series_invariant(prev, dict(cur, date=["2026-07-13", "2026-07-15", "2026-07-14"]), changed), "dates not ascending")
    cfg, pcfg = {"CodeSha256": "CODEHASH="}, {"CodeSha256": PUB_CODE}
    cur_rows, prev_rows = dict(rec["rewrite"]["rows"]), dict(rec["before"]["day_rows"])
    vers, tot, nm, fl = dict(rec["rewrite"]["day_versions_after"]), rec["after"]["gold_total_rows"], dict(rec["rewrite"]["not_measurable_after"]), dict(rec["rewrite"]["abs_flow_after_cents"])
    parts = len(rec["days"]) + 2
    assert check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, fl, tot, parts, cfg, pcfg, SCHED)
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, dict(nm, **{"2026-07-15": 500}), fl, tot, parts, cfg, pcfg, SCHED), "live a day mostly not measurable")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, dict(nm, **{"2026-07-15": 31}), fl, tot, parts, cfg, pcfg, SCHED), "live not measurable differs from the record")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, dict(fl, **{"2026-07-13": 1}), tot, parts, cfg, pcfg, SCHED), "live flows differ from the record")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, dict(fl, **{"2026-07-13": 9_000_000}), tot, parts, cfg, pcfg, SCHED), "live flows rose")
    red(lambda: check_live_gold(rec, changed, dict(cur_rows, **{"2026-07-13": 1}), prev_rows, vers, nm, fl, tot, parts, cfg, pcfg, SCHED), "live day rows")
    red(lambda: check_live_gold(rec, changed, cur_rows, dict(prev_rows, **{"2026-07-15": 1}), vers, nm, fl, tot, parts, cfg, pcfg, SCHED), "live prior version lost")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, dict(vers, **{"2026-07-15": 3}), nm, fl, tot, parts, cfg, pcfg, SCHED), "live versions")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, fl, 1, parts, cfg, pcfg, SCHED), "live total")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, fl, tot, parts + 1, cfg, pcfg, SCHED), "live partitions")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, fl, tot, parts, {"CodeSha256": "x="}, pcfg, SCHED), "live gold code")
    red(lambda: check_live_gold(rec, changed, cur_rows, prev_rows, vers, nm, fl, tot, parts, cfg, pcfg, dict(SCHED, publish_daily="ENABLED")), "live schedule")
    wd = dict(rec["after"]["series_with_day"])
    assert check_live_series(rec, 939, wd, [True] * 60)
    red(lambda: check_live_series(rec, 938, wd, [True]), "live prefixes")
    red(lambda: check_live_series(rec, 939, dict(wd, **{"2026-07-14": 5}), [True]), "live with day")
    red(lambda: check_live_series(rec, 939, wd, [True, False]), "a sample differs")
    red(lambda: check_live_series(rec, 939, wd, []), "no sample")
    dry = {"days": {"2026-07-13": {"old": {"rows": 880}, "new": {"rows": 880}}, "2026-07-14": {"old": {"rows": 3}, "new": {"rows": 890}}}}
    assert dry_expectations(dry) == ({"2026-07-13": 880, "2026-07-14": 890}, {"2026-07-14"})
    red(lambda: dry_expectations({"days": {"2026-07-13": {"old": {"rows": 880}, "held": "HOLD"}}}), "a held day in the dry derivation")
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
