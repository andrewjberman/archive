"""HVST-bk-1: articles collected per source per day over 90 days, from what is ALREADY HELD (read-only).

Reads (S3 GET / list only, no put, no publisher/vendor host):
  silver articles  -> publication_gold._iter_latest_articles()
  run records      -> publication_gold._iter_run_records()
  bronze articles  -> store.table_prefix(source, "bronze", "article"), listed; the day is the stamp in the key.

Run from the repo root: PYTHONPATH=. python -u <this file> > bk1_per_source_per_day.out
"""
import collections
import datetime
import json
import os
import re
import statistics
import sys
import traceback

import lib.research.harvest.publication_gold as pg
import lib.research.harvest.store as store
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = ["bbg", "wsj", "barrons", "sa", "ft"]
ONE_DAY = datetime.timedelta(days=1)
PROGRESS_EVERY = 2000
STAMP_RE = re.compile(r"^(\d{8})T\d{6}Z")
BACKFILL_MIN_SECURITIES = 10
NAME_PATTERNS = {
    "Caterpillar": re.compile(r"\bcaterpillar\b", re.I),
    "CSL": re.compile(r"\b(?:CSL\s+Limited|CSL\s+Ltd\.?|CSL\s+Behring|Seqirus)\b", re.I),
    "AIG": re.compile(r"\bAIG\b", re.I),
    "Nokia": re.compile(r"\bnokia\b", re.I),
}


def out(line=""):
    print(line)


def to_dt(value):
    """tz-aware UTC datetime from a datetime or ISO string; None when absent or unparseable."""
    if value is None:
        return None
    try:
        parsed = pg._coerce_utc_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed is None:
        return None
    return parsed.astimezone(datetime.timezone.utc)


def text_of(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=True, default=str)
    except (TypeError, ValueError):
        return str(value)


def day_range(start, end):
    days = []
    d = start
    while d <= end:
        days.append(d)
        d += ONE_DAY
    return days


def median(values):
    if not values:
        return 0
    return statistics.median(values)


def fmt(number):
    if isinstance(number, float):
        if number == int(number):
            return str(int(number))
        return "%.2f" % number
    return str(number)


def thinned_line(source, label, counts, start, end):
    """The mechanical line for one source and one table (A or B)."""
    days = day_range(start, end)
    total = sum(counts.get(d, 0) for d in days)
    older = [counts.get(d, 0) for d in days[:60]]
    last30 = [counts.get(d, 0) for d in days[60:]]
    m = median(older)
    per_day_last = sum(last30) / 30.0

    def trailing(d):
        return sum(counts.get(d - datetime.timedelta(days=k), 0) for k in range(7)) / 7.0

    half = m / 2.0
    first_below = None
    for d in reversed(days):
        if trailing(d) < half:
            first_below = d
        else:
            break
    if m == 0 or first_below is None:
        verdict = "NEVER"
    else:
        verdict = first_below.isoformat()
        if first_below == days[0]:
            verdict += " (below from the first day of the window)"
    line = ("%s (%s): 90-day total %d, median per day over days 31 to 90 %s, per day over the last 30 days %s, "
            "THINNED ON %s" % (source, label, total, fmt(float(m)), fmt(round(per_day_last, 2)), verdict))
    return line


def weeks_of(start, end):
    """Monday-start weeks fully begun inside the window: [(monday, [days in window])]; plus the leading stub."""
    days = day_range(start, end)
    stub = [d for d in days if d.weekday() != 0 and d < _first_monday(start)]
    weeks = {}
    for d in days:
        if d < _first_monday(start):
            continue
        monday = d - datetime.timedelta(days=d.weekday())
        weeks.setdefault(monday, []).append(d)
    return stub, sorted(weeks.items())


def _first_monday(start):
    return start + datetime.timedelta(days=(7 - start.weekday()) % 7)


def compress_days(days):
    if not days:
        return "none"
    ranges = []
    run_start = prev = days[0]
    for d in days[1:]:
        if d - prev == ONE_DAY:
            prev = d
            continue
        ranges.append((run_start, prev))
        run_start = prev = d
    ranges.append((run_start, prev))
    return ", ".join(a.isoformat() if a == b else "%s..%s" % (a.isoformat(), b.isoformat()) for a, b in ranges)


def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    end = now.date()
    start = end - datetime.timedelta(days=89)
    window = day_range(start, end)
    failures = []
    out("BK1 started %s UTC; window %s to %s (90 days ending today UTC, both inclusive)" % (
        now.strftime("%Y-%m-%dT%H:%M:%SZ"), start.isoformat(), end.isoformat()))

    # ---- silver ----
    pub = {s: collections.Counter() for s in SOURCES}
    fet = {s: collections.Counter() for s in SOURCES}
    n_silver = 0
    lack_pub = 0
    lack_fet = 0
    unknown_pub = collections.Counter()
    publisher_from_column = 0
    publisher_from_key = 0
    naming = {k: 0 for k in NAME_PATTERNS}
    naming_substr = {k: 0 for k in NAME_PATTERNS}
    last30_start = end - datetime.timedelta(days=29)
    in_window_published = 0
    try:
        for row in pg._iter_latest_articles():
            n_silver += 1
            if n_silver % PROGRESS_EVERY == 0:
                out("PROGRESS silver rows read %d" % n_silver)
            code = row.get("publisher")
            if code is not None:
                publisher_from_column += 1
            else:
                code = pg._publisher_of(row.get("article_key"))
                publisher_from_key += 1
            if code not in SOURCES:
                unknown_pub[code] += 1
                continue
            p = to_dt(row.get("published_utc"))
            f = to_dt(row.get("fetched_at"))
            if p is None:
                lack_pub += 1
            else:
                pub[code][p.date()] += 1
                if p.date() >= last30_start and p.date() <= end:
                    in_window_published += 1
                    hay = text_of(row.get("title")) + "\n" + "\n".join(text_of(b) for b in (row.get("text_blocks") or []))
                    low = hay.lower()
                    for name, pattern in NAME_PATTERNS.items():
                        if pattern.search(hay):
                            naming[name] += 1
                        needle = "seqirus" if name == "CSL" else name.lower()
                        if needle in low or (name == "CSL" and "csl" in low):
                            naming_substr[name] += 1
            if f is None:
                lack_fet += 1
            else:
                fet[code][f.date()] += 1
    except Exception:
        failures.append("silver read failed")
        out("FINDING: silver read refused or raised, printed whole:")
        out(traceback.format_exc())

    # ---- run records ----
    run_stats = {s: {"runs": collections.Counter(), "jobs": collections.Counter(), "keys": collections.Counter(),
                     "status": collections.defaultdict(collections.Counter)} for s in SOURCES}
    n_runs = 0
    runs_no_finished = 0
    runs_bad_day = 0
    job_finished_present = 0
    jobs_total = 0
    per_run_sec = {s: [] for s in SOURCES}  # per run: (jobs, distinct security keys, finish day)
    span_info = {s: {"jobs": 0, "with_span": 0, "lengths": [], "recent": 0, "deep": 0} for s in SOURCES}
    retrieval_modes = collections.Counter()
    try:
        for rec in pg._iter_run_records():
            n_runs += 1
            if n_runs % PROGRESS_EVERY == 0:
                out("PROGRESS run records read %d" % n_runs)
            retrieval_modes[rec.get("retrieval_mode")] += 1
            fin = to_dt(rec.get("finished_at"))
            if fin is None:
                runs_no_finished += 1
                fin = to_dt(rec.get("started_at"))
            if fin is None:
                runs_bad_day += 1
                continue
            day = fin.date()
            per_source_jobs = collections.defaultdict(list)
            for job in rec.get("jobs") or []:
                if not isinstance(job, dict):
                    continue
                jobs_total += 1
                if job.get("finished_at"):
                    job_finished_present += 1
                code = job.get("publisher")
                if code in SOURCES:
                    per_source_jobs[code].append(job)
            for code, jobs in per_source_jobs.items():
                st = run_stats[code]
                st["runs"][day] += 1
                st["jobs"][day] += len(jobs)
                keys = 0
                for job in jobs:
                    kf = job.get("keys_fetched")
                    if isinstance(kf, int):
                        keys += kf
                    st["status"][day][job.get("status")] += 1
                    info = span_info[code]
                    info["jobs"] += 1
                    span = pg._job_reached_span(job)
                    if span is not None:
                        info["with_span"] += 1
                        info["lengths"].append((span[1] - span[0]).days + 1)
                        if (day - span[1]).days <= 3:
                            info["recent"] += 1
                        if (day - span[0]).days >= 30:
                            info["deep"] += 1
                st["keys"][day] += keys
                distinct = len({j.get("security_key") for j in jobs})
                per_run_sec[code].append((len(jobs), distinct, day))
    except Exception:
        failures.append("run record read failed")
        out("FINDING: run record read refused or raised, printed whole:")
        out(traceback.format_exc())

    # ---- bronze ----
    bron = {s: collections.Counter() for s in SOURCES}
    n_bronze = 0
    bronze_no_stamp = 0
    try:
        client = store._default_client()
        paginator = client.get_paginator("list_objects_v2")
        for code in SOURCES:
            source = SOURCE_FOR_PUBLISHER[code]
            prefix = store.table_prefix(source, "bronze", "article")
            out("BRONZE listing prefix for %s: s3://%s/%s" % (code, store.HARVEST_BUCKET, prefix))
            for page in paginator.paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
                for obj in page.get("Contents", []) or []:
                    n_bronze += 1
                    if n_bronze % PROGRESS_EVERY == 0:
                        out("PROGRESS bronze objects listed %d" % n_bronze)
                    name = obj["Key"].rsplit("/", 1)[-1]
                    m = STAMP_RE.match(name)
                    if not m:
                        bronze_no_stamp += 1
                        continue
                    bron[code][datetime.datetime.strptime(m.group(1), "%Y%m%d").date()] += 1
    except Exception:
        failures.append("bronze list failed")
        out("FINDING: bronze list refused or raised, printed whole:")
        out(traceback.format_exc())

    # ---- output ----
    out("")
    out("DENOMINATOR: silver articles %d, run records %d, bronze objects listed %d, window %s to %s" % (
        n_silver, n_runs, n_bronze, start.isoformat(), end.isoformat()))
    out("FIELDS: silver publisher day from `publisher` column on %d rows, from the article_key prefix on %d rows; "
        "unknown publisher %s" % (publisher_from_column, publisher_from_key, dict(unknown_pub) or "none"))
    out("FIELD (A): `published_utc`, rows lacking it: %d" % lack_pub)
    out("FIELD (B): `fetched_at`, rows lacking it: %d" % lack_fet)
    out("FIELD (C): run record `finished_at` (fallback `started_at`), records lacking finished_at: %d, "
        "lacking both: %d; jobs read %d, jobs carrying their own `finished_at`: %d; retrieval_mode %s" % (
            runs_no_finished, runs_bad_day, jobs_total, job_finished_present, dict(retrieval_modes)))
    out("FIELD (D): bronze article object key `.../<YYYYMMDD>T<HHMMSS>Z.<ext>` stamp day; keys lacking a stamp: %d "
        "(bronze articles are partitioned by article_hash, not by date, so the day comes from the object name)" % bronze_no_stamp)
    out("SILVER used fields: article_key, publisher, published_utc, fetched_at, title, text_blocks")

    thinned = []
    for label, tables in (("A", pub), ("B", fet)):
        out("")
        out("THINNED RULE: m = median per day (zero days included) over the earlier 60 days of the window "
            "(days 31 to 90 back from today); a source is THINNED ON the first day d from which the trailing 7-day mean "
            "(day d-6 to d) stays below m/2 on every day through the last day of the window; NEVER if the last day's "
            "trailing mean is not below m/2 or m is 0. A description of counts, not a cause." if label == "A" else
            "THINNED RULE: same as (A), over table (B) fetched day.")
        for s in SOURCES:
            line = thinned_line(s, label, tables[s], start, end)
            thinned.append(line)
            out(line)

    stub, weeks = weeks_of(start, end)
    out("")
    out("WEEKLY SUMMARY (Monday-start weeks; %d rows per source; the leading stub %s is in the 90-day totals, not a row; "
        "the last week is partial, ending %s)" % (len(weeks), compress_days(stub), end.isoformat()))

    def weekly(title, counters):
        out("")
        out(title)
        out("week_of     " + " ".join("%8s" % s for s in SOURCES))
        for monday, wdays in weeks:
            out("%s  " % monday.isoformat() + " ".join("%8d" % sum(counters[s].get(d, 0) for d in wdays) for s in SOURCES))

    weekly("TABLE (A) silver articles by PUBLISHED day, per week", pub)
    weekly("TABLE (B) silver articles by FETCHED day, per week", fet)
    weekly("TABLE (C1) run records finished, per week (runs with at least one job for the source)",
           {s: run_stats[s]["runs"] for s in SOURCES})
    weekly("TABLE (C2) jobs, per week", {s: run_stats[s]["jobs"] for s in SOURCES})
    weekly("TABLE (C3) keys fetched (sum of job keys_fetched), per week", {s: run_stats[s]["keys"] for s in SOURCES})
    out("")
    out("TABLE (C4) jobs by status over the whole window, per source")
    c_lines_ok = 0
    for s in SOURCES:
        agg = collections.Counter()
        for d in window:
            agg.update(run_stats[s]["status"].get(d, {}))
        out("%s: %s" % (s, dict(agg) or "none"))
        c_lines_ok += 1
    weekly("TABLE (D) bronze article objects by key-stamp day, per week", bron)
    out("D out-of-window bronze objects by source (stamp day before %s or after %s): %s" % (
        start.isoformat(), end.isoformat(),
        {s: sum(v for d, v in bron[s].items() if d < start or d > end) for s in SOURCES}))

    out("")
    out("RUN RECORDS PER SOURCE (day = run finished_at day)")
    run_lines = []
    for s in SOURCES:
        days_with = sorted(d for d in window if run_stats[s]["runs"].get(d, 0) > 0)
        if days_with:
            first, last = days_with[0], days_with[-1]
            missing = [d for d in window if run_stats[s]["runs"].get(d, 0) == 0]
            span_days = (last - first).days + 1
            coverage = 100.0 * len(days_with) / span_days
        else:
            first = last = None
            missing = list(window)
            coverage = 0.0
        runs = per_run_sec[s]
        big = sum(1 for _j, dist, _d in runs if dist >= BACKFILL_MIN_SECURITIES)
        small = len(runs) - big
        info = span_info[s]
        med_lengths = median(info["lengths"])
        if big and small:
            kind = "both"
        elif big:
            kind = "backfill pass"
        elif small:
            kind = "small runs (below %d securities)" % BACKFILL_MIN_SECURITIES
        else:
            kind = "no run records"
        line = ("%s: first finished run in window %s, last %s, days with a finished run %d of %d, days with no finished run "
                "%d; runs with jobs for it (all time) %d, of which >=%d distinct security_key %d and fewer %d, median jobs per "
                "such run %s, median distinct security_key per run %s; jobs %d, with a valid reached_span %d, median "
                "reached_span length %s days, reached_span ending within 3 days of the run's finish %d, starting 30 or more "
                "days before it %d; coverage of days between first and last %.0f%%; READS AS: %s" % (
                    s, first.isoformat() if first else "none", last.isoformat() if last else "none", len(days_with),
                    len(window), len(missing), len(runs), BACKFILL_MIN_SECURITIES, big, small,
                    fmt(float(median([j for j, _x, _d in runs]))), fmt(float(median([x for _j, x, _d in runs]))),
                    info["jobs"], info["with_span"], fmt(float(med_lengths)), info["recent"], info["deep"], coverage, kind))
        run_lines.append(line)
        out(line)
        out("  days with no finished run: %s" % compress_days(missing))
    out("FIELDS READ for the run-record reading: run `finished_at`, `started_at`, `retrieval_mode`; job `publisher`, "
        "`security_key`, `status`, `keys_fetched`, `reached_span`. Rule: BACKFILL PASS = a run holding at least %d distinct "
        "security_key jobs for the source; a run with fewer is a small run; `both` when the source has runs of each kind." %
        BACKFILL_MIN_SECURITIES)

    out("")
    naming_line = "IN-WINDOW ARTICLES NAMING: Caterpillar %d, CSL %d, AIG %d, Nokia %d" % (
        naming["Caterpillar"], naming["CSL"], naming["AIG"], naming["Nokia"])
    out(naming_line)
    out("  over %d silver articles published %s to %s; whole-word case-insensitive match of title and text_blocks; "
        "CSL = CSL Limited, CSL Ltd, CSL Behring, Seqirus; loose substring counts (reference only): %s" % (
            in_window_published, last30_start.isoformat(), end.isoformat(), naming_substr))

    # ---- files ----
    def table_json(counters):
        return {s: {d.isoformat(): counters[s].get(d, 0) for d in window} for s in SOURCES}

    payload = {
        "denominator": {"silver": n_silver, "run_records": n_runs, "bronze": n_bronze,
                        "window": [start.isoformat(), end.isoformat()]},
        "A_silver_by_published_day": table_json(pub),
        "B_silver_by_fetched_day": table_json(fet),
        "C_run_records_by_finished_day": {
            s: {d.isoformat(): {"runs": run_stats[s]["runs"].get(d, 0), "jobs": run_stats[s]["jobs"].get(d, 0),
                                "keys_fetched": run_stats[s]["keys"].get(d, 0),
                                "jobs_by_status": dict(run_stats[s]["status"].get(d, {}))} for d in window}
            for s in SOURCES},
        "D_bronze_by_key_stamp_day": table_json(bron),
        "thinned_lines": thinned,
        "run_record_lines": run_lines,
        "in_window_naming": naming_line,
    }
    with open(os.path.join(HERE, "BK1_PER_SOURCE_PER_DAY.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    md = ["# BK1 per source per day (HVST-bk-1)", "",
          "Window %s to %s (90 days ending today UTC). Silver %d, run records %d, bronze objects %d." % (
              start.isoformat(), end.isoformat(), n_silver, n_runs, n_bronze), "",
          "THINNED rule: m = median per day (zero days counted) over the earlier 60 days (days 31 to 90 back from today). "
          "A source is THINNED ON the first day from which its trailing 7-day mean (that day and the 6 before) stays below "
          "m/2 on every day to the end of the window; NEVER if the last day is not below m/2 or m is 0. It describes the "
          "counts; it is not a verdict on the cause.", ""]
    md.extend("- " + line for line in thinned)
    md.append("")
    md.append("## Run records per source")
    md.extend("- " + line for line in run_lines)
    md.append("")
    md.append("- " + naming_line)
    for title, counters in (("A silver by published day", pub), ("B silver by fetched day", fet),
                            ("D bronze objects by key-stamp day", bron)):
        md.extend(["", "## Table " + title, "", "| day | " + " | ".join(SOURCES) + " |", "|---|" + "---|" * len(SOURCES)])
        for d in window:
            md.append("| %s | " % d.isoformat() + " | ".join(str(counters[s].get(d, 0)) for s in SOURCES) + " |")
    md.extend(["", "## Table C run records by finished day (runs / jobs / keys fetched)", "",
               "| day | " + " | ".join(SOURCES) + " |", "|---|" + "---|" * len(SOURCES)])
    for d in window:
        md.append("| %s | " % d.isoformat() + " | ".join(
            "%d/%d/%d" % (run_stats[s]["runs"].get(d, 0), run_stats[s]["jobs"].get(d, 0), run_stats[s]["keys"].get(d, 0))
            for s in SOURCES) + " |")
    with open(os.path.join(HERE, "BK1_PER_SOURCE_PER_DAY.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(md) + "\n")

    # ---- verdict ----
    problems = list(failures)
    if n_silver <= 0:
        problems.append("N (silver) is 0")
    if n_runs <= 0:
        problems.append("R (run records) is 0")
    if len(thinned) != 10:
        problems.append("THINNED lines printed %d of 10" % len(thinned))
    if len(run_lines) != 5 or c_lines_ok != 5:
        problems.append("table (C) printed fewer than five sources")
    out("")
    if problems:
        out("CENSUS FAIL: " + "; ".join(problems))
        return 1
    out("CENSUS OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
