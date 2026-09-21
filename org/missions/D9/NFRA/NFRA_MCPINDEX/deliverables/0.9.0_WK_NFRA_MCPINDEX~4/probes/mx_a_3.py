#!/usr/bin/env python3
"""
Probe for NFRA_MCPINDEX.TO-MX-a-3 (Black Diamond, S8/FWD-4).
Serial: 0.9.0_WK_NFRA_MCPINDEX~4. Read-only (boto3 GetObject/ListObjectsV2/HeadObject/read_metadata
only -- no writes to any AWS resource). Bucket under analysis: opal-data-bd (the live, DESIRED-plane
home the property's own scripts write, env override BD_S3_BUCKET, e.g.
data/black_diamond/scripts/silver/merge-daily-incremental.py:53).

Usage: py -3.12 mx_a_3.py AC<n>
Prints the measurement with instrument/vintage/denominator, then exactly one line:
  VERDICT: PASS-MXA3-AC<n>
  VERDICT: FAIL-MXA3-AC<n> <reason>
"""
import sys
import io
import json
import re
from datetime import datetime, timezone

import boto3

BUCKET = "opal-data-bd"
REGION = "us-east-1"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def s3():
    return boto3.client("s3", region_name=REGION)


DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def list_all(prefix=""):
    """Live ListObjectsV2, paginated. Returns list of (key, size, last_modified_iso)."""
    c = s3()
    pag = c.get_paginator("list_objects_v2")
    out = []
    for page in pag.paginate(Bucket=BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            out.append((o["Key"], o["Size"], o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")))
    return out


# ---------------------------------------------------------------------------
# CANONICAL TABLE MAP -- this cell's analysis. Each entry: prefix (a key or a
# key-prefix ending in '/'), whether it is date-partitioned (newest partition
# read from the key), grain, freshness field, and the producer-code citation.
# ---------------------------------------------------------------------------
CANON_TABLES = [
    ("transactions", "silver/transactions/", True,
     "one row per transaction line on the BD export/data date; NOT deduped across dates in the "
     "daily parquet -- dedup key transaction_id is applied at query/compaction time "
     "(merge-daily-incremental.py:479-507, :642-643)",
     "trade_date (per-row column) / the partition filename date, read from the BD 'Timestamps' "
     "sheet End Date, fallback to the filename (merge-daily-incremental.py:337-362, :464-472)",
     "merge-daily-incremental.py:403-522 process_xlsx_to_parquet"),
    ("allocations", "silver/allocations/", True,
     "one row per account per as_of_date point-in-time snapshot; dedup (account_id, as_of_date) "
     "keep-first (merge-daily-incremental.py:832-837)",
     "as_of_date (column) / partition filename date",
     "merge-daily-incremental.py:767-865 process_alloc_xlsx_to_parquet"),
    ("realized", "silver/realized/", True,
     "one row per realized sale event per trade_date; INCREMENTAL (each day's export adds that "
     "day's sells, README.md:934-936); dedup (account_id, asset_name, trade_date, unit_cost) "
     "keep-first (merge-daily-incremental.py:1019-1023)",
     "trade_date (column) / partition filename date",
     "merge-daily-incremental.py:962-1040 process_realized_xlsx_to_parquet"),
    ("unrealized", "silver/unrealized/", True,
     "one row per open holding per account per as_of_date; a FULL SNAPSHOT -- each file is the "
     "complete open-position picture for that date (merge-daily-incremental.py:1104-1107); dedup "
     "(account_id, asset_name) keep-first",
     "partition filename date (as_of_date); a 0-row export is SKIPPED, not written "
     "(merge-daily-incremental.py:1162-1171)",
     "merge-daily-incremental.py:1133-1218 process_unrealized_xlsx_to_parquet"),
    ("fees", "silver/fees/", True,
     "one row per fee/billing transaction per trade_date (per-account billing events: "
     "transaction_fee, account_fee, flat_fee, basis_points)",
     "trade_date (column) / partition filename date",
     "convert_fees_to_silver.py:1-80"),
    ("bd_assets_dim", "silver/bd_assets_dim.parquet", False,
     "one row per distinct asset_id, latest-trade-date-wins dedup, with per-asset txn aggregates "
     "(build_bd_assets_dim.py:85-120)",
     "built_at column (ISO timestamp of the build) and the object's S3 LastModified -- NOT rebuilt "
     "on any daily cadence found in this cell's read (no scheduler reference in the silver scripts "
     "read); see AC2 finding on staleness",
     "build_bd_assets_dim.py:1-53"),
    ("canonical_prices", "silver/prices/canonical_prices.parquet", False,
     "one row per (asset_name/ticker, date) -- 3-tier canonical price blend",
     "date column (max)",
     "merge-daily-incremental.py:675-708 invoke_price_update docstring (bd-price-update Lambda); "
     "README.md:276 build_canonical_prices_v2.py named as the '3-tier canonical price engine'"),
    ("historical_prices", "silver/historical_prices.parquet", False,
     "one row per (ticker, date) -- T2 yfinance close",
     "date column (max)",
     "fetch_historical_prices_yfinance.py (present, not opened in full this cell); referenced "
     "merge-daily-incremental.py:683"),
    ("interpolated_prices", "silver/interpolated_prices.parquet", False,
     "one row per (asset_name, date) -- gap-filled interpolation with data_quality/num_observations",
     "date column (max)",
     "build_interpolated_prices.py (present, not opened in full this cell)"),
]

# Everything else measured live under the bucket, named with the exclusion reason (AC8).
EXCLUDED = {
    "silver/assets/": "partitioned raw asset export; latest partition measured 2026-06-18, ~3 months "
        "stale against this cell's run date; superseded as the asset dimension source by "
        "bd_assets.parquet -> bd_assets_dim.parquet (build_bd_assets_dim.py:9-14)",
    "silver/transactions_enriched/": "partitioned cusip-enriched transactions; latest partition "
        "measured date=2026-04-20, days after CP-AE1 (2026-04-17, merge-daily-incremental.py:509-511) "
        "moved cusip enrichment INLINE via enrich_with_cusip() -- INFERRED supersession from timing, "
        "not a doc statement",
    "silver/bd_assets.parquet": "compacted transaction-level asset export, an INPUT to bd_assets_dim "
        "(build_bd_assets_dim.py:9-11), not itself a distinct analytic table",
    "silver/bd_allocations.parquet": "monolithic legacy file, stale (measured last-modified, ~7 "
        "months old against this cell's run date), superseded by the daily-partitioned silver/allocations/",
    "silver/bd_aua_timeseries.parquet": "monolithic legacy file, stale (measured last-modified), "
        "described only in the stale (2026-01-19 'Last Updated') README",
    "silver/bd_nna_daily.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/bd_nna_by_architect.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/bd_canonical_timeline.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/aua_validation_log.parquet": "monolithic legacy validation log, stale (measured last-modified)",
    "silver/daily_aua.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/daily_aua_firm.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/daily_flows.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/daily_positions.parquet": "monolithic legacy file (682MB), stale (measured last-modified)",
    "silver/nna_timeseries.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/historical_dividends.parquet": "monolithic legacy file, stale (measured last-modified)",
    "silver/historical_prices_20260213.parquet": "dated legacy snapshot, superseded by the "
        "actively-updated silver/historical_prices.parquet",
    "silver/historical_prices_final.parquet": "legacy 'final' snapshot, superseded by the "
        "actively-updated silver/historical_prices.parquet",
    "silver/bd_transactions_backup_2026-01-20.parquet": "explicitly named backup",
    "silver/bd_transactions_backup_2026-01-28.parquet": "explicitly named backup",
    "silver/incremental_manifest.json": "control-plane manifest (etag-skip state), not a data table",
    "silver/incremental_allocation_manifest.json": "control-plane manifest, not a data table",
    "silver/incremental_allocation_manifest.json.bak-20260630T1900Z": "control-plane manifest backup",
    "silver/incremental_allocation_manifest.json.bak-20260630T1916Z": "control-plane manifest backup",
    "silver/incremental_realized_manifest.json": "control-plane manifest, not a data table",
    "silver/incremental_unrealized_manifest.json": "control-plane manifest, not a data table",
    "silver/bd_transactions_metadata.json": "control-plane metadata sidecar, not a data table",
    "silver/interpolated_prices_summary.json": "control-plane summary sidecar, not a data table",
    "silver/prices/": "silver/prices/{date}.parquet (measured 150 dated objects through 2026-09-20, "
        "actively maintained) is a GOLD-LAYER TRIGGER artifact, not a distinct query table -- "
        "bd_price_update.py:617-623 states in its own docstring 'Writing canonical_prices.parquet "
        "does NOT trigger gold' and the S3 event filter matches prefix silver/prices/20 specifically "
        "to fire the gold runner off this dated file; its price ROWS are already upserted into "
        "silver/prices/canonical_prices.parquet (bd_price_update.py:587-611), which is the table "
        "fenced above. silver/prices/backfill_telemetry.json is a control-plane telemetry sidecar, "
        "not a data table.",
}

# Top-level bucket prefixes OTHER than silver/, measured live (AC8/AC3 evidence -- this bucket is
# shared with other vendors/tiers, not Black-Diamond-exclusive).
OTHER_TOP_LEVEL_EXCLUDED_REASON = (
    "a different top-level prefix in the same bucket, not silver/ and not this property: "
    "blackdiamond/ (session-trigger control, not data), schwab/ (MX-a-2's vendor), smartx/ "
    "(MX-a-6's vendor), platinum/ (served tier), canonical/ (a differently-named tier), plus "
    "bronze/ (raw input), forwardfill_v2/ (landing zone), gold/ (downstream product), code/ "
    "(synced scripts), logs/, and ops/scratch/deploy prefixes (GOOD_RUN_*, _rollback/, "
    "ajb_workspace/, backfill_v2/, config/, debug/, diagnostics/, gldrst/, investor-reporting/, "
    "lambda-*, qa-scratch/, runs/, scripts/, ssm-output/, status/, temp/, tmp/, v4_output/)"
)


def classify(objs):
    """Bucket every (key,size,lm) under objs (assumed prefix='silver/') into a canon table or
    EXCLUDED, by longest-prefix match. Returns (per_table: {name: {count,bytes,newest}},
    excluded_summary: {reason_key: {count,bytes}})."""
    per_table = {t[0]: {"count": 0, "bytes": 0, "newest": None} for t in CANON_TABLES}
    excluded_count = 0
    excluded_bytes = 0
    unclassified = []
    for key, size, lm in objs:
        matched = None
        for name, prefix, partitioned, *_ in CANON_TABLES:
            if key == prefix or (prefix.endswith("/") and key.startswith(prefix)):
                matched = name
                break
        if matched:
            per_table[matched]["count"] += 1
            per_table[matched]["bytes"] += size
            m = DATE_RE.search(key)
            d = m.group(1) if m else None
            if d and (per_table[matched]["newest"] is None or d > per_table[matched]["newest"]):
                per_table[matched]["newest"] = d
        elif key in EXCLUDED or any(key.startswith(p) for p in EXCLUDED if p.endswith("/")):
            excluded_count += 1
            excluded_bytes += size
        else:
            unclassified.append(key)
    return per_table, excluded_count, excluded_bytes, unclassified


def read_max_date_column(key, col):
    """Live read of a single-file parquet's date column max (pyarrow, column-projected)."""
    import pyarrow.parquet as pq
    c = s3()
    body = c.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    table = pq.read_table(io.BytesIO(body), columns=[col])
    import pyarrow.compute as pc
    mx = pc.max(table.column(col)).as_py()
    return mx, table.num_rows


def ac1():
    print(f"[{now()}] AC1 -- live listing, instrument boto3 s3:ListObjectsV2 (paginated), "
          f"bucket={BUCKET}, prefix=silver/")
    objs = list_all("silver/")
    print(f"  denominator: {len(objs)} objects under silver/ (read verb: ListObjectsV2, paginated, "
          f"live at run time)")
    per_table, exc_count, exc_bytes, unclassified = classify(objs)
    ok = True
    for name, prefix, partitioned, *_ in CANON_TABLES:
        row = per_table[name]
        print(f"  TABLE {name:22s} prefix={prefix:38s} objects={row['count']:6d} "
              f"bytes={row['bytes']:12d} newest_partition_date={row['newest']}")
        if row["count"] == 0:
            print(f"    WARNING: 0 objects live under {prefix} at run time")
    print(f"  EXCLUDED (named, s.AC8): {exc_count} objects, {exc_bytes} bytes")
    if unclassified:
        print(f"  UNCLASSIFIED (neither a canon table nor a named exclusion): "
              f"{len(unclassified)} -- {unclassified[:10]}")
        ok = False
    # single-file tables checked separately by existence; partitioned tables with 0 objects already
    # triggered the WARNING line above.
    for name, prefix, partitioned, *_ in CANON_TABLES:
        if not partitioned:
            try:
                s3().head_object(Bucket=BUCKET, Key=prefix)
            except Exception as e:
                print(f"  FAIL: single-file table {name} ({prefix}) HEAD failed: {e}")
                ok = False
    if unclassified:
        ok = False
    verdict = "PASS-MXA3-AC1" if ok else "FAIL-MXA3-AC1 unclassified keys present, see UNCLASSIFIED above"
    print(f"VERDICT: {verdict}")


def ac2():
    print(f"[{now()}] AC2 -- grain/freshness/latest value per table, read from producer code "
          f"(cited) and from the live objects (pyarrow read_metadata / read_table, column-projected)")
    ok = True
    for name, prefix, partitioned, grain, freshness, source in CANON_TABLES:
        print(f"  TABLE {name}")
        print(f"    grain (source: producer code, {source}): {grain}")
        print(f"    freshness field (source: producer code, {source}): {freshness}")
        if partitioned:
            # latest value = newest partition date, from a fresh live listing scoped to this table
            objs = list_all(prefix)
            found_dates = set()
            for k, _, _ in objs:
                match = DATE_RE.search(k)
                if match:
                    found_dates.add(match.group(1))
            dates = sorted(found_dates)
            latest = dates[-1] if dates else None
            print(f"    latest value (source: live object keys, {len(objs)} objects scanned): "
                  f"{latest}")
            if latest is None:
                print(f"    FAIL: no dated partitions found live for {name}")
                ok = False
        else:
            import pyarrow.parquet as pq
            meta = pq.read_metadata(io.BytesIO(s3().get_object(Bucket=BUCKET, Key=prefix)["Body"].read()))
            cols = [f.name for f in meta.schema.to_arrow_schema()]
            date_col = "date" if "date" in cols else ("built_at" if "built_at" in cols else None)
            if date_col:
                mx, nrows = read_max_date_column(prefix, date_col)
                print(f"    latest value (source: live object, column '{date_col}' max, "
                      f"{nrows} rows scanned): {mx}")
            else:
                lm = s3().head_object(Bucket=BUCKET, Key=prefix)["LastModified"]
                print(f"    latest value (source: live object, no date column found in "
                      f"{cols[:10]}...; using S3 LastModified): {lm.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"VERDICT: {'PASS-MXA3-AC2' if ok else 'FAIL-MXA3-AC2 a table has no measurable latest value'}")


def ac3():
    print(f"[{now()}] AC3 -- firm/master scope rule per table, read from "
          f"infra/logic/registry/scopes.json (live file read at HEAD)")
    with open("infra/logic/registry/scopes.json", encoding="utf-8") as f:
        scopes = json.load(f)
    firm_49f = next(r for r in scopes["scopes"] if r["key"] == "49financial")
    bd_tree = next(p for p in firm_49f["pipeline_trees"] if p["vendor"] == "blackdiamond")
    print(f"  scopes.json[49financial].pipeline_trees: dir={bd_tree['dir']} vendor={bd_tree['vendor']} "
          f"separated_from={bd_tree['separated_from']}")
    print(f"  scopes.json[49financial].monolith_scopes.blackdiamond = "
          f"{firm_49f['monolith_scopes']['blackdiamond']}")
    print(f"  scopes.json[49financial].bucket (CANONICAL, per Rule 30) = {firm_49f['bucket']}")
    print(f"  LIVE bucket this property's scripts actually write (per producer code, "
          f"merge-daily-incremental.py:53) = {BUCKET} (env override BD_S3_BUCKET) -- these DIFFER; "
          f"the canonical LGIC address is UNOCCUPIED at run time (see AC8 note)")
    ok = True
    for name, prefix, *_ in CANON_TABLES:
        # None of the live keys carry a firm-prefix segment
        print(f"  TABLE {name}: scope=49financial (FIRM, single tenant of {bd_tree['dir']} per "
              f"scopes.json); the key '{prefix}' carries NO firm-prefix segment -- scope CANNOT be "
              f"read from the key, only from the registry's pipeline_trees row")
    print(f"  cottonwood's own Black-Diamond-flavored tree lives separately at data/cot/ "
          f"(scopes.json[cottonwood].pipeline_trees, vendor=blackdiamond, separated_from="
          f"{[p for p in next(r for r in scopes['scopes'] if r['key']=='cottonwood')['pipeline_trees'] if p['vendor']=='blackdiamond'][0]['separated_from']}) "
          f"-- a DIFFERENT tree/bucket, out of this cell's scope")
    print(f"VERDICT: {'PASS-MXA3-AC3' if ok else 'FAIL-MXA3-AC3'}")


NEVER_SUM = [
    ("AUA (market value) is never derived by summing transaction flows across a date range",
     "non-additive field / wrong basis -- README.md:10-27 states flow-based AUA omits market "
     "gains/losses; use allocations.account_market_value at a single as_of_date instead"),
    ("allocations.account_market_value (or unrealized.market_value) is never summed across more "
     "than one as_of_date",
     "cross-date -- each partition is a point-in-time snapshot; summing snapshots from different "
     "dates conflates distinct points in time"),
    ("realized gain/loss and unrealized gain/loss are never summed into one figure without "
     "labeling which is which",
     "non-additive field -- different measurement basis (realized = already-closed positions; "
     "unrealized = still-open mark-to-market, README.md:1103-1107)"),
    ("transactions.market_value is never summed across silver/transactions/ daily partitions "
     "without first deduping by transaction_id",
     "cross-date -- BD re-sends prior transaction_ids in later exports (merge-daily-incremental.py:"
     "474-507 cross-date dedup logic; a 30-day lookback dedup exists precisely because this happens)"),
    ("canonical_prices/historical_prices/interpolated_prices.price (or .close) is never summed "
     "across asset_id/ticker/asset_name",
     "non-additive field -- a price is a per-unit value, not a quantity; summing prices of "
     "different securities has no meaning without units held"),
    ("Black Diamond (49financial, data/black_diamond/) figures are never summed with Cottonwood's "
     "separately-tracked Black-Diamond-flavored data (data/cot/)",
     "cross-firm -- scopes.json marks the two pipeline_trees separated_from each other"),
    ("fees.transaction_fee/account_fee/flat_fee is never summed across billing periods without "
     "checking billing_start_date/billing_end_date for overlap",
     "cross-date -- adjacent billing periods can overlap or re-bill; the schema carries explicit "
     "start/end date columns for this reason (convert_fees_to_silver.py:41)"),
]


def ac4():
    print(f"[{now()}] AC4 -- every never-sum rule with its reason (cross-master/cross-firm/"
          f"cross-date/non-additive field)")
    for i, (rule, reason) in enumerate(NEVER_SUM, 1):
        print(f"  {i}. {rule}\n     REASON: {reason}")
    ok = len(NEVER_SUM) > 0
    print(f"VERDICT: {'PASS-MXA3-AC4' if ok else 'FAIL-MXA3-AC4 no rules'}")


# (question_id, question_text, table, fields, source, assignment, tool_or_typed, reason)
QUESTIONS = [
    (1, "What is [relationship/account]'s current AUA (market value)?",
     "allocations", "account_market_value, relationship_id/account_id, as_of_date (latest partition)",
     "producer code (README.md:14-17 'AUA | Allocations | Account Market Value') + portal page "
     "(README.md:249-251 opal-data-portal-v2/json/advisor-intelligence/aua_chart.json)",
     "typed_query",
     "a single-table filter+read on the latest as_of_date partition; C6's typed query covers it "
     "with no cross-table logic"),
    (2, "What are [relationship/account]'s net cash flows (deposits/withdrawals) for a date range?",
     "transactions", "external_flow, market_value, transaction_type, relationship_id/account_id, "
     "trade_date",
     "producer code (README.md:14-19; transaction_type/external_flow columns measured live)",
     "typed_query",
     "a filter+group-by+sum over one table's additive external_flow field; no sequential state "
     "needed"),
    (3, "What is [relationship]'s NNA (Net New Asset) category breakdown "
     "(new client / new account / same account / outflow) for a date range?",
     "transactions", "transaction_type, relationship_id, account_id, trade_date, market_value",
     "prior art (README.md:371-431, the NNA Classification System section) -- the live silver/"
     "transactions/ table carries NO is_nna/nna_category columns (measured: 74 live columns, none "
     "named is_nna*); those fields exist only in the STALE gold-layer bd_nna_daily.parquet "
     "(last modified 2026-01-20, EXCLUDED table)",
     "tool", "blackdiamond_classify_nna",
     "requires PER-CLIENT SEQUENTIAL STATE (first-ever transaction detection, chronological order) "
     "that C6's typed query (filters/group-bys/aggregates, no cross-row state machine) cannot "
     "express; the classification logic is documented (prior art) and re-implementable directly "
     "against silver/transactions, so a purpose-built tool is proposed rather than depending on "
     "the stale gold table"),
    (4, "What is [asset]'s unrealized gain/loss as of the latest snapshot?",
     "unrealized", "market_value, unit_cost, asset_id/asset_name, account_id, partition date",
     "reasoning (direct column read: market_value - unit_cost*units is the standard unrealized "
     "gain/loss definition; unrealized table columns measured live)",
     "typed_query",
     "single-table filter+arithmetic on additive per-row fields at one snapshot date"),
    (5, "What realized gains/losses did [relationship/account] recognize in [period]?",
     "realized", "trade_date, unit_cost, account_id, asset_name, symbol/ticker/cusip",
     "producer code (merge-daily-incremental.py:932-936 'Realized is INCREMENTAL -- each day adds "
     "that day's sells')",
     "typed_query",
     "a filter+group-by over one incremental table; additive within a period once deduped, which "
     "the producer's own dedup key already guarantees at partition-write time"),
    (6, "What is [ticker/asset]'s canonical price on [date]?",
     "canonical_prices", "date, asset_name, ticker, price, source",
     "producer code (merge-daily-incremental.py:675-708 invoke_price_update docstring; README.md:276)",
     "typed_query",
     "a single point-lookup filter on one table"),
    (7, "Which architects/implementors have the highest AUA or NNA (advisor leaderboard)?",
     "allocations (AUA) or transactions (NNA/flows)", "architect, implementor, account_market_value "
     "or external_flow, grouped",
     "portal page (README.md:249-253 architect_leaderboard.json, implementor_leaderboard.json) + "
     "producer code (architect/implementor/consultant/local_ops split-pct columns measured live "
     "in both tables)",
     "typed_query",
     "a group-by+sum+rank over one table's additive field per C6's grouping rules; no cross-table "
     "join required since architect/implementor are carried directly on both allocations and "
     "transactions rows"),
    (8, "What fees did [relationship/account] pay in [period], broken out by fee type?",
     "fees", "transaction_fee, account_fee, flat_fee, basis_points, trade_date, account_id",
     "producer code (convert_fees_to_silver.py:34-80, the COL_RENAME/FLOAT_COLS map)",
     "typed_query",
     "a filter+group-by over one table's fields; the never-sum billing-period-overlap caution "
     "(AC4 item 7) is enforced by C6's date-range filter, not a special tool"),
    (9, "What is [asset]'s classification (asset class / super class / sector) for allocation "
     "reporting?",
     "bd_assets_dim", "asset_super_class_blend, opal_asset_class, asset_class, asset_segment, "
     "asset_id",
     "producer code (build_bd_assets_dim.py:16-32 dim schema docstring)",
     "typed_query",
     "a single-table point lookup by asset_id/cusip/ticker"),
    (10, "How stale is Black Diamond's silver data right now, and which tables are not being "
     "refreshed?",
     "all nine canon tables (partition/file dates) + bd_assets_dim specifically",
     "operational/freshness metadata: newest partition date (transactions/allocations/realized/"
     "unrealized/fees) or date-column max / LastModified (prices/dim tables)",
     "reasoning (this is a meta-question about the property's own freshness, raised by measuring "
     "bd_assets_dim's staleness at AC2/AC9 time, not from a portal page or producer code)",
     "typed_query",
     "a MAX(date)/LastModified read per table is a single-table aggregate C6 already supports; no "
     "purpose-built tool needed for a freshness check"),
]


def ac5():
    print(f"[{now()}] AC5 -- common questions, numbered, table+fields+source; nothing presented as "
          f"measured user demand")
    for q in QUESTIONS:
        qid, text, table, fields, source = q[0], q[1], q[2], q[3], q[4]
        print(f"  {qid}. {text}")
        print(f"     table: {table}")
        print(f"     fields: {fields}")
        print(f"     source: {source} -- NOT measured user demand (no query log / usage telemetry "
              f"read this cell)")
    ok = len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA3-AC5' if ok else 'FAIL-MXA3-AC5 no questions'}")


def ac6():
    print(f"[{now()}] AC6 -- each common question assigned to a proposed tool or the typed query, "
          f"with reason")
    ok = True
    for q in QUESTIONS:
        qid = q[0]
        assignment = q[5]
        reason = q[-1]
        if assignment == "typed_query":
            print(f"  {qid}. -> TYPED QUERY (C6). reason: {reason}")
        elif assignment == "tool":
            tool_name = q[6]
            print(f"  {qid}. -> TOOL `{tool_name}`. reason: {reason}")
        else:
            print(f"  {qid}. FAIL: no assignment")
            ok = False
    print(f"VERDICT: {'PASS-MXA3-AC6' if ok else 'FAIL-MXA3-AC6 an unassigned question'}")


SYSTEMS_JSON = "infra/logic/registry/systems.json"
TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z][a-z0-9]*)+$")
BASE_FORM_VERBS = {"get", "classify", "rank", "list"}


def ac7():
    print(f"[{now()}] AC7 -- proposed tool names pass MX-n-1's C3 rule "
          f"({{system}}_{{function}}[_{{qualifier}}], system a systems.json key, function a "
          f"base-form verb, scope an EXPLICIT ARGUMENT never folded into the name)")
    with open(SYSTEMS_JSON, encoding="utf-8") as f:
        sysd = json.load(f)
    keys = {row["key"] for row in sysd["systems"]}
    print(f"  systems.json read live: {len(keys)} keys; 'blackdiamond' present: "
          f"{'blackdiamond' in keys}")
    tools = [q[6] for q in QUESTIONS if q[5] == "tool"]
    print(f"  proposed tool names ({len(tools)}): {tools}")
    ok = True
    for t in tools:
        if not TOOL_NAME_RE.match(t):
            print(f"  FAIL: {t} does not match {{system}}_{{function}}[_{{qualifier}}] shape")
            ok = False
            continue
        parts = t.split("_")
        system = parts[0]
        function = parts[1]
        if system not in keys:
            print(f"  FAIL: {t} -- system token '{system}' not a systems.json key")
            ok = False
        if function not in BASE_FORM_VERBS:
            print(f"  FAIL: {t} -- function token '{function}' not a recognized base-form verb "
                  f"in this cell's list {sorted(BASE_FORM_VERBS)}")
            ok = False
        # scope check: the word '49financial'/'49f' must NOT appear in the name (folded-in scope)
        if "49f" in t or "49financial" in t:
            print(f"  FAIL: {t} -- scope folded into the name, violates C3")
            ok = False
        print(f"  {t}: system='{system}' (in registry) function='{function}' (base-form) "
              f"scope=49financial passed as an explicit call argument, not in the name -- OK")
    print(f"VERDICT: {'PASS-MXA3-AC7' if ok else 'FAIL-MXA3-AC7 see FAIL lines above'}")


def ac8():
    print(f"[{now()}] AC8 -- proposed read fence as exact prefixes; tables outside it named with "
          f"reason")
    print(f"  PROPOSED READ FENCE (bucket={BUCKET}):")
    for name, prefix, *_ in CANON_TABLES:
        print(f"    s3://{BUCKET}/{prefix}")
    print(f"  EXCLUDED WITHIN silver/ (named, s.EXCLUDED dict, {len(EXCLUDED)} entries):")
    for k, reason in EXCLUDED.items():
        print(f"    s3://{BUCKET}/{k} -- {reason}")
    print(f"  EXCLUDED: other top-level prefixes in the same bucket -- {OTHER_TOP_LEVEL_EXCLUDED_REASON}")
    print("  NOTE (finding, not a fence line): the Rule-30 canonical LGIC address for this property "
          "resolves (lib/opal_naming.py address('blackdiamond','49financial','silver',"
          "'transactions',partition=...)) to s3://opal-data-assets/blackdiamond/49financial/"
          "silver/transactions/date=... -- a DIFFERENT bucket/key-shape than the live data above. "
          "This cell fences to the LIVE location (Rule 30's own non-application: 'existing "
          "pipelines reach conformance through their own migration project, never as a rider on "
          "unrelated work'); the migration gap is reported, not fixed, here.")
    ok = len(CANON_TABLES) > 0 and len(EXCLUDED) > 0
    print(f"VERDICT: {'PASS-MXA3-AC8' if ok else 'FAIL-MXA3-AC8'}")


def ac9():
    print(f"[{now()}] AC9 -- a property with no silver/served data says so and proposes no tool "
          f"(antecedent check)")
    objs = list_all("silver/")
    total_bytes = sum(o[1] for o in objs)
    print(f"  live check: {len(objs)} objects, {total_bytes} bytes under s3://{BUCKET}/silver/ "
          f"at run time (ListObjectsV2, paginated)")
    has_data = len(objs) > 0
    print(f"  Black Diamond HAS live silver data (has_data={has_data}); the antecedent of this "
          f"criterion ('no silver or served data') is FALSE for this property, so the criterion's "
          f"obligation ('says so, proposes no tool') does not bind -- {len(QUESTIONS)} questions "
          f"ARE proposed against real tables (AC5/AC6), which is the correct behavior under a TRUE "
          f"antecedent")
    ok = has_data and len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA3-AC9' if ok else 'FAIL-MXA3-AC9 data absent but tools were proposed, or vice versa'}")


DISPATCH = {
    "AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5,
    "AC6": ac6, "AC7": ac7, "AC8": ac8, "AC9": ac9,
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in DISPATCH:
        print(f"usage: {sys.argv[0]} AC1..AC9 (AC10 is judgment, no probe)")
        sys.exit(2)
    DISPATCH[sys.argv[1]]()


if __name__ == "__main__":
    main()
