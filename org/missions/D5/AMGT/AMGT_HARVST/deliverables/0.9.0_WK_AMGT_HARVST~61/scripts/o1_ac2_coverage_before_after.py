"""o1_ac2_coverage_before_after.py -- HVST-o-1 AC2 (READ-ONLY, IN MEMORY).

WHAT IT DOES (no vendor call, no S3 write or delete, no Lambda invoke, no env change)
  Over the 191 covered names (org/.../0.9.0_WK_AMGT_HARVST~46/securities.universe.json) and the SERVED
  30-day window (the 30 days ending on the newest day of the served gold chatter_daily snapshot -- the
  same window the chatter producer's gold branch reads):

  1. Builds gold chatter_daily rows IN MEMORY twice from the SAME inputs -- the served
     article_security_mention snapshot and every silver listing_hit (S3 GET/LIST) -- with
        BEFORE = the merged-base rule  (publisher_coverage over listing hits alone), and
        AFTER  = this rule             (listing hits + every run record found).
  2. Run records are read from S3 (amgt/harvest/bronze/run_record/, the store's own prefix) AND from the
     local runtime root (main tree, READ-ONLY). Counts are printed; a zero is named as a zero.
  3. Prints the COMPLETE / PARTIAL / DENIED name-day distribution and the per-publisher covered name-days,
     BEFORE and AFTER side by side, plus a fidelity check of BEFORE-rebuilt against the SERVED snapshot.
  4. Runs the chatter producer's OWN gold branch (chatter_axis.compute_chatter_axis, count_fn =
     gold_daily_mention_scores, write_fn=None) on the same as-of/window over: the SERVED table, the
     BEFORE rows, the AFTER rows -- the table is swapped in memory by replacing pool_reader's snapshot
     reader; nothing is written.
  5. A PLANTED CONTROL (clearly labelled, never counted as a measurement of the estate): the same AFTER
     rule fed one synthetic successful zero-article job per (name, publisher) over the window, to show the
     rule moves the numbers and what the guard then does.

Writes only o1_ac2_result.json beside this script's parent folder.
"""
import collections
import datetime
import glob
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 8)))
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, REPO)
os.chdir(REPO)

MAIN_TREE_RUNTIME = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"
UNIVERSE = os.path.join(REPO, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json")

import lib.research.harvest.publication_gold as gold  # noqa: E402
import lib.research.harvest.store as store  # noqa: E402
from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.metrics import chatter_axis as ca  # noqa: E402

D = datetime.date
STATUSES = ("COMPLETE", "PARTIAL", "DENIED")


def local_run_records(root):
    """(records, files_found, files_unreadable) from <root>/run_records/*.json."""
    folder = os.path.join(root, "run_records")
    if not os.path.isdir(folder):
        return [], None, 0
    paths = sorted(glob.glob(os.path.join(folder, "*.json")))
    records, bad = [], 0
    for path in paths:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                value = json.load(fh)
        except (OSError, ValueError):
            bad += 1
            continue
        if isinstance(value, dict):
            records.append(value)
    return records, len(paths), bad


def describe_records(label, records):
    jobs = [j for r in records for j in (r.get("jobs") or []) if isinstance(j, dict)]
    with_span = [j for j in jobs if isinstance(j.get("reached_span"), dict)]
    ok = [j for j in with_span if j.get("status") in gold.SUCCESSFUL_RUN_STATUSES]
    print("  %-34s run records=%d  job entries=%d  with reached_span=%d  successful-with-span (would cover)=%d"
          % (label, len(records), len(jobs), len(with_span), len(ok)))
    return {"records": len(records), "jobs": len(jobs), "with_reached_span": len(with_span), "would_cover": len(ok)}


def window_distribution(rows, start, end):
    """({status: name-days}, {publisher: covered name-days}, name-days) over [start, end]."""
    status, per_pub, total = collections.Counter(), collections.Counter(), 0
    for r in rows:
        if start <= r["day"] <= end:
            total += 1
            status[r["data_status"]] += 1
            for code in r["publishers_covered_codes"]:
                per_pub[code] += 1
    return status, per_pub, total


def producer_gold_run(label, rows, as_of):
    """The producer's own gold branch over `rows` as the chatter_daily table (in memory, write_fn=None)."""
    original = pool_reader._gold_latest_snapshot_rows
    pool_reader._gold_latest_snapshot_rows = lambda table, client=None: list(rows)
    try:
        pool_reader.clear_caches()
        summary = ca.compute_chatter_axis(as_of_date=as_of, count_fn=ca.gold_daily_mention_scores, write_fn=None)
    finally:
        pool_reader._gold_latest_snapshot_rows = original
        pool_reader.clear_caches()
    cov = summary.get("input_coverage") or {}
    products = [(p["axis"], p["state"], p["rows_ranked"], p.get("reason_code")) for p in summary["products"]]
    print("  %-30s RESOLVED %s of %s %s (%s days each); unresolved names=%d; states=%s"
          % (label, cov.get("resolved"), cov.get("required"), cov.get("unit"), cov.get("window_days"),
             len(cov.get("unresolved", [])), json.dumps(summary["states"], sort_keys=True)))
    for p in products:
        print("      product %-18s state=%-7s rows_ranked=%-3s reason_code=%s" % p)
    return {"resolved": cov.get("resolved"), "required": cov.get("required"), "unresolved": len(cov.get("unresolved", [])),
            "states": summary["states"], "products": products}


def main():
    result = {}
    securities = json.load(open(UNIVERSE, "r", encoding="utf-8"))
    print("COVERED UNIVERSE: %d names from %s (distinct security_key: %d)"
          % (len(securities), os.path.relpath(UNIVERSE, REPO), len({s["security_key"] for s in securities})))
    assert len(securities) == 191

    # ---- inputs (S3 GET/LIST only) ------------------------------------------------------------------
    served_daily = pool_reader._gold_latest_snapshot_rows(gold.GOLD_DAILY_TABLE)
    as_of = max(r["day"] for r in served_daily)
    start = as_of - datetime.timedelta(days=ca.WINDOW_DAYS - 1)
    print("SERVED chatter_daily snapshot: %d rows; newest day %s -> as_of=%s; served window %s..%s (%d days) x %d names = %d name-days"
          % (len(served_daily), as_of, as_of, start, as_of, ca.WINDOW_DAYS, len(securities), ca.WINDOW_DAYS * len(securities)))
    mention = gold._latest_gold_snapshot_rows(gold.GOLD_TABLE)
    listing_hits = list(gold._iter_all_listing_hits())
    print("SERVED article_security_mention snapshot: %d rows; silver listing_hit rows (all publishers): %d %s"
          % (len(mention), len(listing_hits), dict(collections.Counter(r.get("publisher") for r in listing_hits))))

    s3_records = list(gold._iter_run_records())
    local_records, local_files, local_bad = local_run_records(MAIN_TREE_RUNTIME)
    print("\nRUN RECORDS FOUND:")
    print("  S3 prefix %s%s : %d object(s) parsed%s" % (store.HARVEST_BUCKET + "/", store.table_prefix("amgt", "bronze", "run_record"),
                                                     len(s3_records), "  (ZERO: no run record has been persisted to S3 yet)" if not s3_records else ""))
    if local_files is None:
        print("  local %s/run_records : DIRECTORY ABSENT (ZERO run records: no collection has run since the n-1 record landed)" % MAIN_TREE_RUNTIME)
    else:
        print("  local %s/run_records : %d file(s), %d unreadable%s" % (MAIN_TREE_RUNTIME, local_files, local_bad,
                                                                     "  (ZERO)" if not local_files else ""))
    result["run_records"] = {"s3": describe_records("S3", s3_records),
                             "local": describe_records("local runtime root", local_records),
                             "local_dir_present": local_files is not None}
    real_records = s3_records + local_records

    # ---- coverage BEFORE / AFTER (in memory) --------------------------------------------------------
    cov_before = gold.publisher_coverage(listing_hits, securities)
    cov_after = gold.publisher_coverage(listing_hits, securities, run_records=real_records)
    rows_before = gold.daily_rows(mention, securities, start=gold.BACKFILL_FLOOR, end=as_of, coverage=cov_before)
    rows_after = gold.daily_rows(mention, securities, start=gold.BACKFILL_FLOOR, end=as_of, coverage=cov_after)

    served_window = [r for r in served_daily if start <= r["day"] <= as_of and r["security_key"] in {s["security_key"] for s in securities}]
    served_dist = collections.Counter(r["data_status"] for r in served_window)
    b_status, b_pub, b_total = window_distribution(rows_before, start, as_of)
    a_status, a_pub, a_total = window_distribution(rows_after, start, as_of)
    assert b_total == a_total == ca.WINDOW_DAYS * len(securities)

    print("\n=== COVERAGE DISTRIBUTION, name-days over the served window (denominator %d = %d names x %d days) ===" % (b_total, len(securities), ca.WINDOW_DAYS))
    print("  %-10s | %-22s | %-22s | %-22s" % ("status", "SERVED snapshot", "BEFORE (base rule)", "AFTER (this rule)"))
    for st in STATUSES:
        print("  %-10s | %-22d | %-22d | %-22d" % (st, served_dist.get(st, 0), b_status.get(st, 0), a_status.get(st, 0)))
    print("  %-10s | %-22d | %-22d | %-22d" % ("total", sum(served_dist.values()), b_total, a_total))
    print("  fidelity: BEFORE-rebuilt status counts equal the SERVED snapshot's over the window: %s" % (dict(b_status) == dict(served_dist)))
    print("\n  covered name-days PER PUBLISHER (a name-day counts once for each publisher in its covered set; of %d):" % b_total)
    print("  %-10s | %-10s | %-10s" % ("publisher", "BEFORE", "AFTER"))
    for pub in gold.ENABLED_PUBLISHERS:
        print("  %-10s | %-10d | %-10d" % (pub, b_pub.get(pub, 0), a_pub.get(pub, 0)))
    moved = sum(1 for rb, ra in zip(rows_before, rows_after) if rb["data_status"] != ra["data_status"])
    print("  name-days whose data_status changed BEFORE -> AFTER (all %d built days x names): %d%s"
          % (len(rows_before), moved, "  (ZERO: there is no run record with a reached_span to add coverage)" if moved == 0 else ""))
    result["window"] = {"start": str(start), "end": str(as_of), "name_days": b_total}
    result["distribution"] = {"served": dict(served_dist), "before": dict(b_status), "after": dict(a_status),
                              "per_publisher_before": dict(b_pub), "per_publisher_after": dict(a_pub), "changed_days": moved}

    # ---- the producer's gold branch, in memory --------------------------------------------------------
    identities = [e["identity"] for e in ca.read_universe_names(as_of=str(as_of))[0]]
    print("\nPRODUCER UNIVERSE (pool): %d covered names; equal to the 191-name file: %s"
          % (len(identities), set(identities) == {s["security_key"] for s in securities}))
    print("\n=== CHATTER PRODUCER GOLD BRANCH, as_of=%s window=%s..%s, write_fn=None (nothing written) ===" % (as_of, start, as_of))
    result["producer"] = {
        "served_table": producer_gold_run("SERVED chatter_daily", served_daily, str(as_of)),
        "before": producer_gold_run("BEFORE (base rule, rebuilt)", rows_before, str(as_of)),
        "after": producer_gold_run("AFTER (this rule, real records)", rows_after, str(as_of)),
    }

    # ---- planted control -------------------------------------------------------------------------------
    print("\n=== PLANTED CONTROL (SYNTHETIC -- not a measurement of the estate) ===")
    print("  one successful zero-article job per (name, publisher) reaching the whole served window is fed to the AFTER rule; "
          "then only 'sa' does.")
    def plant(publishers):
        return [{"run_id": "planted", "jobs": [
            {"publisher": p, "security_key": s["security_key"], "status": "no_new_articles",
             "reached_span": {"start": str(start), "end": str(as_of), "basis": "listing_dates"}}
            for s in securities for p in publishers]}]
    control = {}
    for label, pubs in (("all five publishers", gold.ENABLED_PUBLISHERS), ("sa only", ("sa",))):
        cov = gold.publisher_coverage(listing_hits, securities, run_records=plant(pubs))
        rows = gold.daily_rows(mention, securities, start=gold.BACKFILL_FLOOR, end=as_of, coverage=cov)
        st, pp, tot = window_distribution(rows, start, as_of)
        print("  control [%s]: COMPLETE=%d PARTIAL=%d DENIED=%d of %d name-days; per publisher %s"
              % (label, st.get("COMPLETE", 0), st.get("PARTIAL", 0), st.get("DENIED", 0), tot, dict(pp)))
        control[label] = {"status": dict(st), "per_publisher": dict(pp),
                          "producer": producer_gold_run("CONTROL [%s]" % label, rows, str(as_of))}
    result["planted_control"] = control

    with open(os.path.join(OUT_DIR, "o1_ac2_result.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, sort_keys=True, default=str)
    print("\nwrote o1_ac2_result.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
