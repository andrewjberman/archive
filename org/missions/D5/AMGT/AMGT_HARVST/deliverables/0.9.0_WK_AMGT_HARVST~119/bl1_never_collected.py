"""HVST-bl-1: the covered list less the securities that ever had a collection job (read-only).

Reads only:
  S3 run records   -> publication_gold._iter_run_records()  (GET/list; no put)
  S3 gold snapshot -> publication_gold._latest_gold_snapshot_rows(GOLD_TABLE)
  device run records -> <shared tree>/.runtime/opal-data-harvest*/run_records/*.json  (opened read-only)
No job, collector, driver, emitter, publisher or vendor is run.

Run from the repo root of the worktree: PYTHONPATH=. python -u <this file> > bl1_never_collected.out
"""
import collections
import datetime
import glob
import json
import os
import re
import sys
import traceback

import lib.research.harvest.publication_gold as pg
import lib.research.harvest.store as store

HERE = os.path.dirname(os.path.abspath(__file__))
SHARED_RUNTIME = r"C:\Users\Opal Bloomberg\Desktop\ajb_workspace\.runtime"
COVERED_PATH = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round64/securities.universe.r64.json"
TITLES = {}
SECURITY_FILES_GLOB = "org/missions/D5/AMGT/AMGT_HARVST/**/*.security.json"
CONFIG_PATH = "lib/opal_data_harvest/config.json"
SOURCES = ["bbg", "wsj", "barrons", "sa", "ft"]
# The one status that stored articles. Every other status in the records (no_new_articles,
# no_acceptable_new_articles, listing_empty_200, error, cooldown, contract_unavailable, request_rejected,
# upstream_unavailable, sign_in_refused, bot_check, auth_failed_after_refresh, account_or_harvester_unavailable)
# is counted as "stored nothing" for item 6.
STORING_STATUSES = frozenset({"new_articles"})


def out(line=""):
    print(line)


def run_stamp(run_id):
    return str(run_id or "")[:8]


def read_device():
    """[(root_name, file_name, record)] for every parseable device run-record file; plus unreadable list."""
    rows, bad = [], []
    pattern = os.path.join(SHARED_RUNTIME, "opal-data-harvest*", "run_records", "*.json")
    files = sorted(glob.glob(pattern))
    for path in files:
        root = os.path.basename(os.path.dirname(os.path.dirname(path)))
        try:
            with open(path, "rb") as handle:
                rec = json.loads(handle.read().decode("utf-8"))
        except (OSError, ValueError) as exc:
            bad.append((path, repr(exc)))
            continue
        if isinstance(rec, dict):
            rows.append((root, os.path.basename(path), rec))
        else:
            bad.append((path, "not an object"))
    return files, rows, bad


def ticker_norm(ticker):
    return re.sub(r"\s+", "_", str(ticker or "").strip().upper())


def read_ticker_maps():
    """(job_id -> ticker, collector key -> ticker) from the device `runs/<job>.json` files (opened read-only)
    and the collector security files under the HARVST deliverables (`*.security.json`, key + ticker)."""
    by_job, by_key, n_runs, n_sec = {}, {}, 0, 0
    TITLES.clear()
    for path in glob.glob(os.path.join(SHARED_RUNTIME, "opal-data-harvest*", "runs", "*.json")):
        try:
            with open(path, "rb") as handle:
                doc = json.loads(handle.read().decode("utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(doc, dict):
            TITLES[doc.get("job_id")] = [str(a.get("title")) for a in (doc.get("accepted") or []) if isinstance(a, dict)]
        if not isinstance(doc, dict) or not doc.get("ticker"):
            continue
        n_runs += 1
        by_job[doc.get("job_id")] = doc["ticker"]
        by_key.setdefault(doc.get("security_key"), doc["ticker"])
    for path in glob.glob(SECURITY_FILES_GLOB, recursive=True):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                doc = json.load(handle)
        except (OSError, ValueError):
            continue
        if isinstance(doc, dict) and doc.get("key") and doc.get("ticker"):
            n_sec += 1
            by_key.setdefault(doc["key"], doc["ticker"])
    return by_job, by_key, n_runs, n_sec


def jobs_of(rec):
    jobs = rec.get("jobs")
    return [j for j in jobs if isinstance(j, dict)] if isinstance(jobs, list) else []


def describe_store(label, records):
    """records: [(tag, run_id, record)]. Prints the four counts and per-source jobs; returns a dict."""
    run_ids = set()
    jobs = 0
    secs = set()
    per_source = collections.Counter()
    for _tag, run_id, rec in records:
        run_ids.add(run_id)
        for job in jobs_of(rec):
            jobs += 1
            per_source[job.get("publisher")] += 1
            secs.add(job.get("gold_security_key") or job.get("security_key"))
    out("%s: records read %d, jobs %d, distinct run ids %d, distinct securities with a job %d (by gold_security_key "
        "else collector key)" % (label, len(records), jobs, len(run_ids), len(secs)))
    out("%s: jobs per source %s" % (label, json.dumps({s: per_source.get(s, 0) for s in sorted(per_source, key=str)})))
    return {"records": len(records), "jobs": jobs, "run_ids": run_ids, "securities": secs}


def main():
    out("BL1 started %s UTC" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    failures = []

    # ---- covered list and the collector's identity map (collector key -> pool key)
    with open(COVERED_PATH, "r", encoding="utf-8") as handle:
        covered = json.load(handle)
    covered_keys = [c["security_key"] for c in covered]
    company = {c["security_key"]: c.get("company") for c in covered}
    out("COVERED LIST: %s, %d securities, %d distinct security_key" % (COVERED_PATH, len(covered), len(set(covered_keys))))
    with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    with open(config["symbol_resolution_source"], "r", encoding="utf-8") as handle:
        identity = json.load(handle)["records"]
    collector_to_pool = {r["key"]: r["security_key"] for r in identity}
    out("IDENTITY MAP: %s, %d records, %d collector keys" % (config["symbol_resolution_source"], len(identity),
                                                              len(collector_to_pool)))

    # ---- store 1: S3
    s3_records = []
    s3_error = None
    try:
        client = store._default_client()
        prefix = store.table_prefix("amgt", "bronze", "run_record")
        n_keys = 0
        paginator = client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            n_keys += sum(1 for o in page.get("Contents", []) or [] if o["Key"].endswith(".json"))
        out("S3 run-record prefix s3://%s/%s : %d .json keys listed" % (store.HARVEST_BUCKET, prefix, n_keys))
        for rec in pg._iter_run_records(client):
            s3_records.append(("s3", rec.get("run_id"), rec))
    except Exception:
        s3_error = traceback.format_exc()
        out("FINDING: S3 run records could not be read:")
        out(s3_error)

    # ---- store 2: device
    files, device_rows, bad = read_device()
    out("DEVICE glob: %s : %d files matched, %d unreadable" % (
        os.path.join(SHARED_RUNTIME, "opal-data-harvest*", "run_records", "*.json"), len(files), len(bad)))
    for path, why in bad:
        out("FINDING: device file unreadable: %s : %s" % (path, why))
    device_records = [(root + "/" + name, rec.get("run_id"), rec) for root, name, rec in device_rows]
    root_of_run = {}
    for root, name, rec in device_rows:
        root_of_run.setdefault(rec.get("run_id"), set()).add(root)
    roots = collections.Counter(root for root, _n, _r in device_rows)
    out("DEVICE files per runtime root: %s" % json.dumps(dict(sorted(roots.items()))))

    out("")
    out("RECONCILE")
    s3 = describe_store("S3", s3_records)
    dev = describe_store("DEVICE", device_records)
    if not s3["records"]:
        failures.append("S3 store count is 0")
    if not dev["records"]:
        failures.append("device store count is 0")

    only_s3 = sorted(s3["run_ids"] - dev["run_ids"], key=str)
    only_dev = sorted(dev["run_ids"] - s3["run_ids"], key=str)
    both = s3["run_ids"] & dev["run_ids"]
    out("IN S3 ONLY: %d run ids" % len(only_s3))
    out("ON THIS DEVICE ONLY: %d run ids" % len(only_dev))
    out("IN BOTH: %d" % len(both))

    s3_by_run = collections.defaultdict(list)
    for _t, rid, rec in s3_records:
        s3_by_run[rid].append(rec)
    dev_by_run = collections.defaultdict(list)
    for _t, rid, rec in device_records:
        dev_by_run[rid].append(rec)

    def src_mix(by_run, ids):
        c = collections.Counter()
        for rid in ids:
            for rec in by_run[rid]:
                for job in jobs_of(rec):
                    c[job.get("publisher")] += 1
        return dict(c)

    def day_range(ids):
        days = sorted(run_stamp(i) for i in ids if i)
        return (days[0], days[-1]) if days else (None, None)

    def mode_mix(by_run, ids):
        c = collections.Counter()
        for rid in ids:
            for rec in by_run[rid]:
                c[rec.get("retrieval_mode")] += 1
        return dict(c)

    out("IN S3 ONLY examples: %s" % json.dumps(only_s3[:5]))
    out("IN S3 ONLY distinguishes: run-id date range %s; job sources %s; retrieval_mode %s" % (
        day_range(only_s3), json.dumps(src_mix(s3_by_run, only_s3)), json.dumps(mode_mix(s3_by_run, only_s3))))
    out("ON THIS DEVICE ONLY examples: %s" % json.dumps(only_dev[:5]))
    out("ON THIS DEVICE ONLY distinguishes: run-id date range %s; job sources %s; retrieval_mode %s; runtime roots %s" % (
        day_range(only_dev), json.dumps(src_mix(dev_by_run, only_dev)), json.dumps(mode_mix(dev_by_run, only_dev)),
        json.dumps(dict(collections.Counter(r for i in only_dev for r in root_of_run[i])))))
    out("IN BOTH distinguishes: run-id date range %s; job sources %s (device copy)" % (
        day_range(both), json.dumps(src_mix(dev_by_run, both))))
    dup_dev = sum(1 for rid, recs in dev_by_run.items() if len(recs) > 1)
    dup_s3 = sum(1 for rid, recs in s3_by_run.items() if len(recs) > 1)
    out("DUPLICATE run ids inside one store: S3 %d, DEVICE %d" % (dup_s3, dup_dev))
    shape = collections.Counter()
    for _t, _r, rec in s3_records + device_records:
        shape[type(rec.get("jobs")).__name__] += 1
    out("RECORD SHAPE: type of `jobs` field across both stores %s" % json.dumps(dict(shape)))

    # ---- union of jobs, deduped by (run_id, job_id)
    union = {}
    for tag, rid, rec in s3_records + device_records:
        for job in jobs_of(rec):
            union.setdefault((rid, job.get("job_id")), job)
    out("")
    out("UNION OF THE TWO STORES: %d distinct (run_id, job_id) jobs (S3 %d + DEVICE %d jobs read)" % (
        len(union), s3["jobs"], dev["jobs"]))

    # ---- join: gold_security_key, else the collector key mapped through the identity file, else the key itself
    route = collections.Counter()
    job_pool = {}
    unresolved = []
    ticker_by_job, ticker_by_key, n_runs, n_sec = read_ticker_maps()
    out("TICKER MAPS: %d device runs/<job>.json files carrying a ticker; %d collector security files carrying key+ticker; "
        "%d jobs and %d collector keys mapped to a ticker" % (n_runs, n_sec, len(ticker_by_job), len(ticker_by_key)))
    cov_by_ticker = {}
    for c in covered:
        cov_by_ticker[ticker_norm(c.get("ticker"))] = c["security_key"]
        sk = c["security_key"]
        cov_by_ticker.setdefault(sk[:-len("_Equity")] if sk.endswith("_Equity") else sk, sk)
    for ident, job in union.items():
        gold = job.get("gold_security_key")
        ck = job.get("security_key")
        tick = ticker_by_job.get(job.get("job_id")) or ticker_by_key.get(ck)
        if gold:
            pool, how = gold, "gold_security_key"
        elif ck in collector_to_pool:
            pool, how = collector_to_pool[ck], "collector key via identity file"
        elif ck and not str(ck).startswith("security-"):
            pool, how = ck, "security_key already a pool-form key"
        elif tick and ticker_norm(tick) in cov_by_ticker:
            pool, how = cov_by_ticker[ticker_norm(tick)], "ticker (runs file / collector security file) to covered list"
        else:
            pool, how = None, "UNRESOLVED"
            unresolved.append(job)
        route[how] += 1
        job_pool[ident] = pool
    out("JOIN FIELD: the job's `gold_security_key`; where absent, the collector `security_key` mapped to the pool key "
        "through the identity file's `key` -> `security_key`; where absent and the key is a pool-form key, the key itself; "
        "otherwise the job's ticker (from the device runs/<job>.json, else from a collector security file for that key) "
        "matched to a covered-list ticker")
    out("JOBS LACKING `gold_security_key`: %d of %d (resolved through a fallback: %d; UNRESOLVED: %d)" % (
        sum(1 for j in union.values() if not j.get("gold_security_key")), len(union),
        len(union) - route["gold_security_key"] - len(unresolved), len(unresolved)))
    out("JOIN ROUTE counts: %s" % json.dumps(dict(route)))
    if unresolved:
        keys = sorted({str(j.get("security_key")) for j in unresolved})
        out("UNRESOLVED jobs: %d jobs, %d distinct collector keys, publishers %s; keys: %s" % (
            len(unresolved), len(keys), json.dumps(dict(collections.Counter(j.get("publisher") for j in unresolved))),
            json.dumps(keys[:40])))
        out("UNRESOLVED jobs with a ticker known but not on the covered list: %s" % json.dumps(sorted({
            str(ticker_by_job.get(j.get("job_id")) or ticker_by_key.get(j.get("security_key")))
            for j in unresolved if (ticker_by_job.get(j.get("job_id")) or ticker_by_key.get(j.get("security_key")))})[:60]))

    # Evidence only (a heuristic, not a join): do the stored titles of the unresolved-key jobs name a never-collected company?
    unresolved_ids = [ident for ident in union if job_pool[ident] is None]
    covered_by_key = {c["security_key"]: c for c in covered}
    held = set(c["security_key"] for c in covered) - {job_pool[i] for i in union if job_pool[i]}
    out("TITLE EVIDENCE: for each of the %d covered securities with no resolved job, the unresolved-key jobs (%d) whose "
        "accepted-article titles (device runs files) name the company by an alias, word-bounded, case-insensitive:" % (
            len(held), len(unresolved_ids)))
    for key in sorted(held):
        aliases = [a for a in (covered_by_key[key].get("aliases") or []) if a] or [covered_by_key[key].get("company")]
        rx = re.compile("|".join(r"%s" % re.escape(a) for a in aliases), re.I)
        hits = [i for i in unresolved_ids if any(rx.search(t) for t in TITLES.get(i[1], []))]
        out("  %s aliases %s: %d unresolved-key jobs name it in a stored title" % (key, json.dumps(aliases), len(hits)))

    jobs_by_sec = collections.defaultdict(list)
    for ident, job in union.items():
        if job_pool[ident]:
            jobs_by_sec[job_pool[ident]].append(job)

    # ---- subtraction
    out("")
    out("SUBTRACTION (union of the two stores)")
    covered_set = set(covered_keys)
    n_cov = len(covered_set)
    with_job = {k for k in covered_set if jobs_by_sec.get(k)}
    never = sorted(covered_set - with_job)
    out("COVERED: %d" % n_cov)
    out("WITH AT LEAST ONE JOB: %d of %d" % (len(with_job), n_cov))
    out("NEVER COLLECTED: %d" % len(never))
    per_source_never = {}
    for src in SOURCES:
        wj = {k for k in covered_set if any(j.get("publisher") == src for j in jobs_by_sec.get(k, []))}
        per_source_never[src] = sorted(covered_set - wj)
        out("[%s] COVERED: %d" % (src, n_cov))
        out("[%s] WITH AT LEAST ONE JOB: %d of %d" % (src, len(wj), n_cov))
        out("[%s] NEVER COLLECTED: %d" % (src, n_cov - len(wj)))
    other_pubs = collections.Counter(j.get("publisher") for j in union.values() if j.get("publisher") not in SOURCES)
    out("JOBS WITH A PUBLISHER OUTSIDE THE FIVE SOURCES: %s" % json.dumps(dict(other_pubs)))
    not_covered = sorted(set(jobs_by_sec) - covered_set)
    out("SECURITIES WITH A JOB THAT ARE NOT ON THE COVERED LIST: %d (distinct securities with a job in the union: %d; "
        "unresolved jobs excluded: %d)" % (len(not_covered), len(jobs_by_sec), len(unresolved)))
    out("NOT-ON-COVERED-LIST examples: %s" % json.dumps(not_covered[:5]))

    # ---- served pairs per security from the newest gold part
    gold_error = None
    gold_counts = collections.Counter()
    gold_rows = []
    try:
        gold_rows = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
        for row in gold_rows:
            gold_counts[row.get("security_key")] += 1
    except Exception:
        gold_error = traceback.format_exc()
        out("FINDING: the newest gold part could not be read:")
        out(gold_error)
    out("")
    out("GOLD: newest part of %s, %d rows, %d distinct security_key, columns %s" % (
        pg.GOLD_TABLE, len(gold_rows), len(gold_counts), sorted(gold_rows[0]) if gold_rows else None))
    never_rows = [{"security_key": k, "company": company.get(k), "served_pairs": gold_counts.get(k, 0),
                   "sources_never_collected": [s for s in SOURCES if k in set(per_source_never[s])]} for k in never]
    never_rows.sort(key=lambda r: (-r["served_pairs"], r["security_key"]))
    out("NEVER COLLECTED, first 25 of %d by served pair count (security_key | company | served pairs):" % len(never_rows))
    for i, r in enumerate(never_rows[:25], 1):
        out("%2d. %s | %s | %d" % (i, r["security_key"], r["company"], r["served_pairs"]))
    out("NEVER COLLECTED: total served pairs %d of %d gold rows; with zero served pairs %d" % (
        sum(r["served_pairs"] for r in never_rows), len(gold_rows), sum(1 for r in never_rows if not r["served_pairs"])))

    # ---- named check
    out("")
    checks = []
    for key in ("CAT_US_Equity", "CSL_AU_Equity", "AIG_US_Equity", "NOKIA_FH_Equity"):
        checks.append("%s: jobs %d" % (key, len(jobs_by_sec.get(key, []))))
    out("; ".join(checks) + "   (reviewer: 0, 0, 6, 4)")

    # ---- collected but never stored
    out("")
    statuses = collections.Counter(j.get("status") for j in union.values())
    out("STATUS COUNTS in the union: %s" % json.dumps(dict(sorted(statuses.items(), key=lambda kv: str(kv[0])))))
    out("STATUSES COUNTED AS STORING: %s; every other status counts as stored nothing" % sorted(STORING_STATUSES))
    anomalies = sum(1 for j in union.values() if j.get("status") not in STORING_STATUSES and int(j.get("keys_fetched") or 0) > 0)
    out("JOBS OF A NON-STORING STATUS WITH keys_fetched > 0: %d" % anomalies)
    out("COLLECTED BUT NEVER STORED, per source (covered securities with a job in that source, every job of that "
        "source in a non-storing status):")
    cbn = {}
    for src in SOURCES:
        with_src = [k for k in covered_set if any(j.get("publisher") == src for j in jobs_by_sec.get(k, []))]
        never_stored = [k for k in with_src if not any(
            j.get("publisher") == src and j.get("status") in STORING_STATUSES for j in jobs_by_sec[k])]
        cbn[src] = {"with_job": len(with_src), "never_stored": len(never_stored)}
        out("[%s] %d of %d securities with a job" % (src, len(never_stored), len(with_src)))
    allsrc = [k for k in with_job if not any(j.get("status") in STORING_STATUSES for j in jobs_by_sec[k])]
    out("[any source] %d of %d securities with a job" % (len(allsrc), len(with_job)))

    # ---- artifacts
    payload = {"covered": n_cov, "with_job": len(with_job), "never_collected": len(never),
               "per_source": {s: {"with_job": n_cov - len(per_source_never[s]), "never": len(per_source_never[s])}
                              for s in SOURCES},
               "s3": {k: v for k, v in s3.items() if k not in ("run_ids", "securities")},
               "device": {k: v for k, v in dev.items() if k not in ("run_ids", "securities")},
               "in_s3_only": len(only_s3), "on_device_only": len(only_dev), "in_both": len(both),
               "never_collected_list": never_rows, "collected_but_never_stored": cbn}
    with open(os.path.join(HERE, "BL1_NEVER_COLLECTED.json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=1)
        handle.write("\n")
    lines = ["# BL1: covered securities with no collection job", "",
             "COVERED %d; WITH AT LEAST ONE JOB %d; NEVER COLLECTED %d (union of S3 run records and the device run records)." % (
                 n_cov, len(with_job), len(never)), "",
             "| # | security_key | company | served pairs | sources never collected |", "|---|---|---|---|---|"]
    for i, r in enumerate(never_rows, 1):
        lines.append("| %d | %s | %s | %d | %s |" % (i, r["security_key"], r["company"], r["served_pairs"],
                                                   ",".join(r["sources_never_collected"])))
    with open(os.path.join(HERE, "BL1_NEVER_COLLECTED.md"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")

    # ---- verdict
    if gold_error:
        failures.append("gold part unreadable")
    if len(with_job) + len(never) != 242:
        failures.append("WITH AT LEAST ONE JOB + NEVER COLLECTED != 242 (%d)" % (len(with_job) + len(never)))
    if n_cov != 242:
        failures.append("covered list is %d not 242" % n_cov)
    out("")
    if failures:
        out("CENSUS FAIL: " + "; ".join(failures))
    else:
        out("CENSUS OK")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        out("CENSUS FAIL: unhandled exception")
        out(traceback.format_exc())
        sys.exit(1)
