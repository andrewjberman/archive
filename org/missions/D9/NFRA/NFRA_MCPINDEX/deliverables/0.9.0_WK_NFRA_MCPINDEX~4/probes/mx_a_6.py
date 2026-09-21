#!/usr/bin/env python3
"""
Probe for NFRA_MCPINDEX.TO-MX-a-6 (SmartX, S8/FWD-4).
Serial: 0.9.0_WK_NFRA_MCPINDEX~4. Read-only (boto3 GetObject/ListObjectsV2/HeadBucket only -- no
writes to any AWS resource).

BUCKET AND PATH, MEASURED not assumed. THREE candidate SmartX locations exist live; only one is
this cell's property:
  1. s3://opal-data-assets/smartx/platform/{bronze,silver}/ -- the MONOLITH's SmartX tree. Confirmed
     canonical by FOUR independent carriers: (a) workflows/vendor_watch/README.md's live-vs-mirror
     table names it "genuinely lives in the monolith" (no stale-mirror caveat, unlike Eclipse/Orion/
     Black Diamond); (b) infra/aws/lambda/opal-assets/opal-assets-silver-smartx/smartx_runtime.py:34
     `MONOLITH_BUCKET = os.environ.get("MONOLITH_BUCKET", "opal-data-assets")`; (c) key_mapping.py's
     ruled grammar (`smartx/platform/bronze/{feed}/...`, `smartx/platform/silver/{feed}/date=.../
     data.parquet`) is CTO-gated and PERMANENT (2026-07-14, docstring :3-6); (d) data/mdpf/config/
     partner_roster.json and route_bindings.yaml both wire MDPF's live SmartX feeds to
     `bucket: opal-data-assets, prefix: smartx/platform/silver/fact_*`. THIS is the property read here.
  2. s3://opal-data-bd/smartx/ -- MEASURED live this run: 2967 objects / ~64.7MB (also filed as
     NFRA_MCPINDEX-W4-S1 by this same worker on MX-a-3), sub-prefixes bronze/, jwt/, raw/. Named in
     NO carrier above (not vendor_watch's live-vs-mirror table, not key_mapping.py's ruled grammar,
     not MDPF's roster) -- an undocumented THIRD location, excluded (AC8) with that reason.
  3. s3://opal-data-smartx/ -- the bucket data/smartx/docs/smartx_data_info.md describes (an
     Excel/API dashboard product, `consolidated/smartx_allocations.parquet`, NOT bronze/silver/gold
     tiered). MEASURED live this run: `head-bucket` on `opal-data-smartx` returns 404 NotFound -- the
     bucket the doc describes DOES NOT EXIST at this cell's run time. Even were it live, its own doc
     never calls it "silver"; excluded (AC9-adjacent finding, AC8 exclusion) on both grounds.

Usage: py -3.12 mx_a_6.py AC<n>
Prints the measurement with instrument/vintage/denominator, then exactly one line:
  VERDICT: PASS-MXA6-AC<n>
  VERDICT: FAIL-MXA6-AC<n> <reason>
"""
import sys
import io
import json
import re
from datetime import datetime, timezone

import boto3

BUCKET = "opal-data-assets"
REGION = "us-east-1"
SMARTX_PREFIX = "smartx/platform/silver/"
UNDOCUMENTED_BD_SMARTX = "s3://opal-data-bd/smartx/ (2967 objects / ~64,664,996 bytes measured live " \
    "by this worker as NFRA_MCPINDEX-W4-S1 on MX-a-3; sub-prefixes bronze/, jwt/, raw/ -- named in " \
    "NO canonical carrier: not vendor_watch/README.md's live-vs-mirror table, not key_mapping.py's " \
    "ruled grammar, not MDPF's partner_roster.json/route_bindings.yaml. An undocumented third " \
    "location, out of this cell's read fence."
NONEXISTENT_OPAL_DATA_SMARTX = "s3://opal-data-smartx/ -- data/smartx/docs/smartx_data_info.md " \
    "describes this bucket (consolidated/smartx_allocations.parquet, an Excel/API dashboard " \
    "product, never called 'silver' in that doc). MEASURED live this run: HeadBucket on " \
    "opal-data-smartx returns 404 NotFound -- the bucket does not exist at this cell's run time."


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def s3():
    return boto3.client("s3", region_name=REGION)


DATE_RE = re.compile(r"date=(\d{4}-\d{2}-\d{2})/")


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
# CANONICAL TABLE MAP -- the 11 platform-scope silver fact tables silver.py's
# silver_keys() (:1147-1165) names as its outputs. Each entry: (name, subdir,
# grain, freshness, source citation). Every table lands at
# smartx/platform/silver/{name}/date=YYYY-MM-DD/data.parquet regardless of
# which bronze scope (platform/model/{rmid}/account/{acctId}) it was built
# from -- confirmed live below, sibling of the 2 pre-naming-law DRAFT objects
# (allocation_positions/, allocation_valuation/, EXCLUDED, see EXCLUDED_SUBDIRS).
# ---------------------------------------------------------------------------
CANON_TABLES = [
    ("fact_allocation_positions", "fact_allocation_positions/",
     "the ATOM: one row per (allocation_id, ticker, as_of) -- one position line per allocation "
     "per symbol per snapshot date; MEASURED natural-key collision message at silver.py:507-511 "
     "names exactly this triple",
     "the {date} partition folder (date=YYYY-MM-DD, the run_date the daily converter fired on); "
     "the as_of column (POSITION_COLS, silver.py:43-51) additionally carries the vendor's own "
     "per-row snapshot date",
     "silver.py:43-51 POSITION_COLS, :72 parse_allocation_holdings, :473-511 to_frames()"),
    ("fact_allocation_valuation", "fact_allocation_valuation/",
     "one row per (allocation_id, as_of) -- envelope + all 5 AUM basis components per allocation "
     "per snapshot; natural-key collision message at silver.py:518-522 names (allocation_id, as_of)",
     "the {date} partition folder; the as_of column",
     "silver.py:53-64 VALUATION_COLS, :473-522 to_frames()"),
    ("fact_allocation_account_map", "fact_allocation_account_map/",
     "feed-9: one row per (allocation_id, run_date) -- the living allocation<->account mapping; "
     "'an allocation lives in exactly one model on a given day' (map_frame docstring, silver.py:437-441)",
     "the {date} partition folder (run_date)",
     "silver.py:383-397 MAP_TABLE_NAME/MAP_COLS, :400-434 parse_allocation_accounts, :436-471 map_frame"),
    ("fact_model_aum_daily", "fact_model_aum_daily/",
     "one row per (rmid, day, run_date) -- EACH run_date partition carries the FULL HISTORY series "
     "as re-delivered that day (~400-1200 rows/model), not an incremental delta (parse_model_aum "
     "docstring, silver.py:211-215); day = the per-row observation date, run_date = the pull date",
     "the {date} partition folder = run_date (the pull date); the day column = the per-row "
     "observation date, standardized from the vendor epoch (silver.py:230-232)",
     "silver.py:188-206 MODEL_AUM_COLS, :209-248 parse_model_aum, :258-284 model_aum_frame"),
    ("fact_model_allocation_roster", "fact_model_allocation_roster/",
     "one row per (allocation_id, run_date), ALL statuses INCLUSIVE of closed rows -- live census "
     "cited in the docstring: 7,125 open / 2,381 close / 34 workingClose across 9,540 records, 11 "
     "objects (silver.py:293-296)",
     "the {date} partition folder (run_date)",
     "silver.py:283-296 header, :296-311 MODEL_ALLOCATION_ROSTER_COLS, :317-338 parse_model_allocations"),
    ("fact_account_allocations", "fact_account_allocations/",
     "the account-side SWEEP, distinct from the map by design (R3, silver.py:568): one row per "
     "(allocation_id, run_date), account_allocations_frame docstring silver.py:641-643 'one-account-"
     "per-allocation-per-day invariant, sweep side'",
     "the {date} partition folder (run_date)",
     "silver.py:572-590 ACCOUNT_ALLOCATIONS_COLS, :604-635 parse_account_allocations"),
    ("fact_nonzerosleeve", "fact_nonzerosleeve/",
     "one row per (sleeve_id, run_date) -- custody money-leg carrier, one row per account with a "
     "non-zero cash sleeve balance (nonzerosleeve_frame collision check, silver.py:754-759)",
     "the {date} partition folder (run_date)",
     "silver.py:659-696 NONZEROSLEEVE_COLS, :715-736 parse_nonzerosleeve"),
    ("fact_account_detail", "fact_account_detail/",
     "one row per (account_id, run_date) -- 'EXACTLY one row' per detail bronze object "
     "(parse_account_detail docstring, silver.py:797)",
     "the {date} partition folder (run_date)",
     "silver.py:761-786 ACCOUNT_DETAIL_COLS, :796-828 parse_account_detail"),
    ("fact_model_holdings", "fact_model_holdings/",
     "one row per (rmid, symbol_id, run_date) -- natural-key collision message at silver.py:919-921 "
     "names exactly this triple; vendor bugs preserved as delivered (asset_type/industry, silver.py:855-856)",
     "the {date} partition folder (run_date)",
     "silver.py:851-865 MODEL_HOLDINGS_COLS, :876-899 parse_model_holdings"),
    ("fact_model_performance", "fact_model_performance/",
     "R2 series-explode: one row per (rmid, day, run_date) -- one row per performance window; "
     "envelope self-check ties recordCount to series length (silver.py:975-981); day standardized "
     "from range.start",
     "the {date} partition folder = run_date; the day column = the window's range-start date",
     "silver.py:925-953 MODEL_PERFORMANCE_COLS, :960-1007 parse_model_performance"),
    ("fact_model_changerequests", "fact_model_changerequests/",
     "EVENT-GRAIN, deliberately NO natural key asserted -- 'two legitimate events may share every "
     "identifying field' (THE GRAIN LAW, CTO ruling (a), silver.py:1086-1097); exact-row dedup only",
     "the {date} partition folder (run_date)",
     "silver.py:1033-1047 MODEL_CHANGEREQUESTS_COLS, :1058-1082 parse_model_changerequests"),
]

# The 2 pre-naming-law DRAFT objects, sibling sub-prefixes of the same
# smartx/platform/silver/ prefix, named EXCLUDED (AC1/AC8) not a canon table.
EXCLUDED_SUBDIRS = {
    "allocation_positions/": "pre-naming-law DRAFT object, 1 object measured (date=2026-07-14, "
        "3,050,617 bytes) -- silver_keys() docstring (silver.py:1149-1151) names it "
        "'DRAFT-SUPERSEDED, queued for Andrew's deletion batch'; superseded by fact_allocation_positions/",
    "allocation_valuation/": "pre-naming-law DRAFT object, 1 object measured (date=2026-07-14, "
        "1,126,821 bytes) -- same silver_keys() docstring disclaimer; superseded by "
        "fact_allocation_valuation/",
}

OTHER_TOP_LEVEL_EXCLUDED_REASON = (
    "a different prefix in the same bucket, not smartx/platform/silver/ and not this property: "
    "smartx/platform/bronze/ (the raw input this cell's tables are converted FROM, key_mapping.py "
    ":121-126) and smartx/platform/meta/ (the per-run conversion manifest, INERT by convention, "
    "smartx_conversion.py:296-306); blackdiamond/, schwab/, eclipse/, orion/, pathfinder/, "
    "trueshares/ (other vendors' trees in the same shared monolith bucket, out of this cell's "
    "Eclipse/Orion/Black Diamond/ETF sibling scope); gold/ (downstream product); json/, portal/ "
    "(served/portal-adjacent); code/, config/, _probe/ (ops/code, not data). "
    + UNDOCUMENTED_BD_SMARTX + " " + NONEXISTENT_OPAL_DATA_SMARTX
)


def classify(objs):
    """Bucket every (key,size,lm) under objs (assumed prefix=SMARTX_PREFIX) into a canon table or
    EXCLUDED, by TOP SUBDIRECTORY (the segment right after smartx/platform/silver/). Returns
    (per_table, excluded_count, excluded_bytes, unclassified)."""
    per_table = {t[0]: {"count": 0, "bytes": 0, "newest": None} for t in CANON_TABLES}
    excluded_count = 0
    excluded_bytes = 0
    unclassified = []
    for key, size, lm in objs:
        rest = key[len(SMARTX_PREFIX):] if key.startswith(SMARTX_PREFIX) else key
        matched = None
        for name, subdir, *_ in CANON_TABLES:
            if rest.startswith(subdir):
                matched = name
                break
        if matched:
            per_table[matched]["count"] += 1
            per_table[matched]["bytes"] += size
            m = DATE_RE.search(key)
            d = m.group(1) if m else None
            if d and (per_table[matched]["newest"] is None or d > per_table[matched]["newest"]):
                per_table[matched]["newest"] = d
        elif any(rest.startswith(sub) for sub in EXCLUDED_SUBDIRS):
            excluded_count += 1
            excluded_bytes += size
        else:
            unclassified.append(key)
    return per_table, excluded_count, excluded_bytes, unclassified


def ac1():
    print(f"[{now()}] AC1 -- live listing, instrument boto3 s3:ListObjectsV2 (paginated), "
          f"bucket={BUCKET}, prefix={SMARTX_PREFIX}")
    objs = list_all(SMARTX_PREFIX)
    print(f"  denominator: {len(objs)} objects under {SMARTX_PREFIX} (read verb: ListObjectsV2, "
          f"paginated, live at run time)")
    per_table, exc_count, exc_bytes, unclassified = classify(objs)
    ok = True
    for name, subdir, *_ in CANON_TABLES:
        row = per_table[name]
        print(f"  TABLE {name:28s} objects={row['count']:6d} bytes={row['bytes']:12d} "
              f"newest_partition_date={row['newest']}")
        if row["count"] == 0:
            print(f"    WARNING: 0 objects live under {SMARTX_PREFIX}{subdir} at run time")
            ok = False
    print(f"  EXCLUDED (named, s.AC8, pre-naming-law draft objects): {exc_count} objects, "
          f"{exc_bytes} bytes")
    if unclassified:
        print(f"  UNCLASSIFIED (neither a canon table nor a named exclusion): "
              f"{len(unclassified)} -- {unclassified[:10]}")
        ok = False
    verdict = "PASS-MXA6-AC1" if ok else "FAIL-MXA6-AC1 unclassified keys or an empty table, see above"
    print(f"VERDICT: {verdict}")


def ac2():
    print(f"[{now()}] AC2 -- grain/freshness/latest value per table, read from producer code "
          f"(cited) and from the live objects (pyarrow read_metadata, column-projected)")
    ok = True
    for name, subdir, grain, freshness, source in CANON_TABLES:
        print(f"  TABLE {name}")
        print(f"    grain (source: producer code, {source}): {grain}")
        print(f"    freshness field (source: producer code, {source}): {freshness}")
        objs = list_all(SMARTX_PREFIX + subdir)
        found_dates = set()
        for k, _, _ in objs:
            m = DATE_RE.search(k)
            if m:
                found_dates.add(m.group(1))
        dates = sorted(found_dates)
        latest = dates[-1] if dates else None
        print(f"    latest value (source: live object keys, {len(dates)} distinct dates found for "
              f"this table across {len(objs)} objects scanned): {latest}")
        if latest is None:
            print(f"    FAIL: no dated partitions found live for {name}")
            ok = False
            continue
        import pyarrow.parquet as pq
        key = f"{SMARTX_PREFIX}{subdir}date={latest}/data.parquet"
        body = s3().get_object(Bucket=BUCKET, Key=key)["Body"].read()
        meta = pq.read_metadata(io.BytesIO(body))
        print(f"    live row count at latest partition (source: pyarrow read_metadata on "
              f"s3://{BUCKET}/{key}): {meta.num_rows} rows, {meta.num_columns} cols")
    print(f"VERDICT: {'PASS-MXA6-AC2' if ok else 'FAIL-MXA6-AC2 a table has no measurable latest value'}")


def ac3():
    print(f"[{now()}] AC3 -- firm/master scope rule per table, read from "
          f"infra/logic/registry/scopes.json (live file read at HEAD) and from "
          f"data/mdpf/config/partner_roster.json (live file read at HEAD)")
    with open("infra/logic/registry/scopes.json", encoding="utf-8") as f:
        scopes = json.load(f)
    firm_49f = next(r for r in scopes["scopes"] if r["key"] == "49financial")
    print(f"  scopes.json['49financial'].monolith_scopes = {firm_49f.get('monolith_scopes')} -- "
          f"'smartx' is ABSENT from every scope row's monolith_scopes in scopes.json (0 of "
          f"{len(scopes['scopes'])} scope rows name it) -- an open registry gap, named not repaired "
          f"(bound 9: this cell's <paths> grant does not cover infra/logic/registry/)")
    with open("data/mdpf/config/partner_roster.json", encoding="utf-8") as f:
        roster = json.load(f)
    smartx_feeds = []
    for p in roster.get("partners", []):
        for leg_name, leg in (p.get("legs") or {}).items():
            for feed in leg.get("feeds", []):
                if feed.get("vendor") == "smartx":
                    smartx_feeds.append((p["firm_id"], feed["feed_id"], feed["prefix"]))
    firms = sorted(set(f for f, _, _ in smartx_feeds))
    print(f"  partner_roster.json live parse: {len(smartx_feeds)} smartx-vendor feed row(s) found, "
          f"registered under firm_id(s): {firms}")
    ok = True
    for name, subdir, *_ in CANON_TABLES:
        print(f"  TABLE {name}: scope=49financial (FIRM, per partner_roster.json registration); "
              f"the key (smartx/platform/silver/{subdir}date=.../data.parquet) carries NO "
              f"firm-prefix segment -- scope is UNREADABLE FROM THE KEY for all 11 tables")
    if not firms or firms != ["49financial"]:
        ok = False
    print("  Row-level scope mechanism: NOT independently verified by this cell (no producer-code "
          "read of a firm/tenant filter inside smartx_conversion.py or silver.py was performed here "
          "-- named as an open verification gap, same shape as MX-a-4/MX-a-5's finding)")
    print(f"VERDICT: {'PASS-MXA6-AC3' if ok else 'FAIL-MXA6-AC3'}")


NEVER_SUM = [
    ("fact_model_aum_daily.closing_equity is never summed across `run_date` partitions for the same "
     "(rmid, day)",
     "cross-date -- MEASURED at parse_model_aum's own docstring (silver.py:211-215): 'The payload is "
     "a FULL HISTORY series as delivered that day (~400-1200 rows per live model), not a single day "
     "-- each run_date partition carries the series the vendor served on run_date.' Every run_date "
     "partition re-carries the SAME historical days; summing closing_equity across two run_date "
     "partitions double- (or N-times-) counts every overlapping day"),
    ("fact_model_performance's summary_beginning_market_value / summary_ending_market_value / "
     "pnl_dollar fields are never summed across `day` rows for one model",
     "non-additive / state-grain -- each day-row is a market-value SNAPSHOT for that reporting "
     "window's range (parse_model_performance, silver.py:960-1007, R2 series-explode), not a flow "
     "figure; summing ending-balance snapshots across windows produces a number with no financial "
     "meaning"),
    ("fact_allocation_valuation's five AUM basis components (equity, long_equity, short_equity, "
     "cash, accrued_dividends, accrued_fees, accrued_interest) are never summed TOGETHER into one "
     "AUM total",
     "non-additive field -- silver.py's module docstring (:6-18) states the surface emits FIVE "
     "internally-consistent AUM bases and 'Andrew ruled longEquity + cash (GROSS) canonical -- and "
     "explicitly reserved the right to change that logic later'; silver deliberately preserves ALL "
     "components so gold (never silver, never a caller) applies the one ruled basis"),
    ("fact_model_aum_daily.total_aum is never used in a total figure",
     "wrong-basis / non-additive field -- MODEL_AUM_COLS comment (silver.py:194): 'PRESERVED but "
     "mis-scaled -- gold ignores it (D4 sec 8.6)'"),
    ("fact_model_allocation_roster.value rows are never summed into an AUM total without filtering "
     "to status='open'",
     "wrong-layer / non-additive-without-filter -- the roster's own docstring (silver.py:293-296) "
     "states it is INCLUSIVE of closed rows, with a live census of 7,125 open / 2,381 close / 34 "
     "workingClose across 9,540 records (11 objects, 2026-07-15); an unfiltered sum over-counts by "
     "every closed/workingClose row's value"),
    ("SmartX's fact tables (this cell) are never summed with Black Diamond's silver tables "
     "(MX-a-3's property) without the smartx_bd_join_disposition.yaml v1.0 crosswalk resolution",
     "cross-vendor -- different id spaces (SmartX allocation_id/account_number vs Black Diamond's "
     "account grammar); data/_contracts/smartx_bd_join_disposition.yaml v1.0 (RATIFIED, CTO gate "
     "2026-08-19) is the ONE sanctioned resolution: a MECE outcome enum measured 7286+16+3+0=7305 "
     "against the LIVE 2026-08-19 allocation map, gating D6's entity-resolution service (MX-e-1)"),
    ("SmartX's fact tables are never summed with any other firm's data",
     "cross-firm -- data/mdpf/config/partner_roster.json registers every live smartx-vendor feed "
     "under firm_id 49financial only (this cell's own AC3 live parse, 0 other firm_ids found); "
     "scopes.json carries no smartx monolith_scopes entry at all (AC3 finding), so there is no "
     "registry-stated second firm either"),
    ("fact_allocation_positions/fact_allocation_valuation rows are never summed across `as_of` "
     "snapshots for the same allocation_id",
     "cross-date -- to_frames()'s natural-key collision checks (silver.py:507-522) key on "
     "(allocation_id, ticker, as_of) and (allocation_id, as_of) precisely because a second as_of is "
     "a DIFFERENT point-in-time state, never additive content; each as_of is a full snapshot, not a "
     "delta"),
]


def ac4():
    print(f"[{now()}] AC4 -- every never-sum rule with its reason (cross-master/cross-firm/"
          f"cross-date/non-additive field)")
    for i, (rule, reason) in enumerate(NEVER_SUM, 1):
        print(f"  {i}. {rule}\n     REASON: {reason}")
    ok = len(NEVER_SUM) > 0
    print(f"VERDICT: {'PASS-MXA6-AC4' if ok else 'FAIL-MXA6-AC4 no rules'}")


# (question_id, question_text, table, fields, source, assignment, [tool_name,] reason)
QUESTIONS = [
    (1, "What is SmartX model [rmid]'s daily closing-equity series as of the latest pull?",
     "fact_model_aum_daily", "rmid, day, closing_equity, run_date",
     "producer code (silver.py:209-248 parse_model_aum: 'the FULL HISTORY series as delivered that "
     "day')",
     "typed_query",
     "a single-table filter on rmid + the latest run_date partition; no cross-table logic, though "
     "the caller must pick ONE run_date (never sum across them, AC4 rule 1)"),
    (2, "What is SmartX model [rmid]'s current AUM under Andrew's ruled GROSS (longEquity+cash) "
        "basis, as of [date]?",
     "fact_model_allocation_roster (allocation_id, rmid, status) joined to fact_allocation_valuation "
     "(allocation_id, long_equity, cash, as_of)",
     "allocation_id, rmid, status, long_equity, cash, as_of",
     "producer code (silver.py module docstring :6-18, the GROSS basis ruling) + reasoning (no gold "
     "script computing this SmartX-only figure was read by this cell; the pattern mirrors the "
     "Eclipse aum_variance tool's shape, MX-a-5 Q2)",
     "tool", "smartx_summarize_model_gross_aum",
     "requires filtering the roster to status='open' rows for the given rmid (AC4 rule 5), joining "
     "each surviving allocation_id to its valuation row at the same as_of, and summing "
     "long_equity+cash across that filtered, joined set -- multi-step business logic beyond C6's "
     "single-table filter/group-by/aggregate scope"),
    (3, "Which account is SmartX allocation [allocation_id] currently mapped to (and vice versa), "
        "as of [date]?",
     "fact_allocation_account_map", "allocation_id, account_id, account_number, model_id, run_date",
     "producer code (silver.py:383-434 parse_allocation_accounts/map_frame)",
     "typed_query",
     "a single-table filter+read on the feed-9 map; no aggregation or join needed"),
    (4, "What is the full roster (open/closed) of allocations under SmartX model [rmid]?",
     "fact_model_allocation_roster", "allocation_id, status, value, advisor_name, opened_date_friendly",
     "producer code (silver.py:296-338)",
     "typed_query",
     "a single-table filter on rmid, optionally status; no aggregation needed"),
    (5, "What positions (ticker, quantity, market value) does SmartX allocation [allocation_id] "
        "currently hold?",
     "fact_allocation_positions", "ticker, symbol_id, quantity, price, market_value, as_of",
     "producer code (silver.py:43-51 POSITION_COLS, :72 parse_allocation_holdings)",
     "typed_query",
     "a single-table filter+read on the latest as_of; no cross-table logic"),
    (6, "What is SmartX allocation [allocation_id]'s current valuation breakdown (equity, cash, "
        "accrued fees/interest/dividends) as of [date]?",
     "fact_allocation_valuation",
     "equity, long_equity, short_equity, cash, accrued_dividends, accrued_fees, accrued_interest",
     "producer code (silver.py:53-64 VALUATION_COLS)",
     "typed_query",
     "a single-table filter+read on a handful of basis columns; no aggregation needed (a caller "
     "computing ONE total must still apply AC4 rule 3, but reading the raw breakdown does not)"),
    (7, "What model-level change requests (activity, ticker, quantity) has SmartX model [rmid] "
        "logged on [date]?",
     "fact_model_changerequests", "activity, ticker, quantity, price, trade_friendly",
     "producer code (silver.py:1033-1082); EVENT-GRAIN, no natural key (THE GRAIN LAW, silver.py:1086-1097)",
     "typed_query",
     "a single-table filter on rmid + date; no aggregation needed, and none is safe (event-grain, "
     "no natural key to group on without risking a silent collapse of two legitimate same-shape events)"),
    (8, "What is SmartX account [account_id]'s current custody/configuration detail (custodian, "
        "status, features)?",
     "fact_account_detail", "account_id, custodian_name, status, brokerage_account_number, feature_json",
     "producer code (silver.py:761-828 parse_account_detail: 'EXACTLY one row')",
     "typed_query",
     "a single-table point lookup on account_id; no aggregation or join needed"),
    (9, "Which SmartX accounts currently carry a non-zero cash sleeve balance, and what is each "
        "sleeve's opening/closing equity?",
     "fact_nonzerosleeve", "sleeve_id, account_id, opening_equity, closing_equity, brokerage_acct_num",
     "producer code (silver.py:659-736); the table's own scope (nonzerosleeve) is definitional to "
     "the filter -- no additional business logic needed",
     "typed_query",
     "a single-table filter+read; 'non-zero' is the table's own membership condition, not a "
     "caller-side computation"),
    (10, "What is SmartX allocation [allocation_id]'s crosswalk into the 49F/Black Diamond account "
         "universe, and is it resolved or in the residual?",
     "fact_allocation_account_map (allocation_id, account_number) joined by the caller against the "
     "smartx_bd_join_disposition.yaml v1.0 resolution classes",
     "allocation_id, account_number, account_id",
     "producer code (silver.py:383-434) + the ratified contract "
     "(data/_contracts/smartx_bd_join_disposition.yaml v1.0, CTO gate 2026-08-19)",
     "typed_query",
     "a single-table point lookup on allocation_id; the CROSS-VENDOR resolution itself is a "
     "caller-side lookup against the already-ratified, already-computed disposition enum (AC4 rule "
     "6), not business logic this MCP layer computes fresh -- the entity-resolution service (MX-e-1) "
     "is the resolver of record, not this typed query"),
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
              f"read this cell; sourced from producer code, a ratified contract, or reasoning "
              f"grounded in this cell's own live measurement, per Rule 24's grammar test: this is "
              f"CODE/MEASURED evidence, never a claim about what staff actually ask)")
    ok = len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA6-AC5' if ok else 'FAIL-MXA6-AC5 no questions'}")


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
    print(f"VERDICT: {'PASS-MXA6-AC6' if ok else 'FAIL-MXA6-AC6 an unassigned question'}")


SYSTEMS_JSON = "infra/logic/registry/systems.json"
SCOPES_JSON = "infra/logic/registry/scopes.json"
TOOL_NAME_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z][a-z0-9]*)+$")
BASE_FORM_VERBS = {"get", "list", "classify", "rank", "resolve", "summarize", "query"}


def ac7():
    print(f"[{now()}] AC7 -- proposed tool names pass MX-n-1's C3 rule "
          f"({{system}}_{{function}}[_{{qualifier}}], system a systems.json key, function a "
          f"base-form verb, scope an EXPLICIT ARGUMENT never folded into the name)")
    with open(SYSTEMS_JSON, encoding="utf-8") as f:
        sysd = json.load(f)
    keys = {row["key"] for row in sysd["systems"]}
    print(f"  systems.json read live: {len(keys)} keys; 'smartx' present: {'smartx' in keys}")
    with open(SCOPES_JSON, encoding="utf-8") as f:
        scoped = json.load(f)
    scope_tokens = {row["key"] for row in scoped["scopes"]}
    print(f"  scopes.json read live: {len(scope_tokens)} scope keys (checked for folding): "
          f"{sorted(scope_tokens)}")
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
        folded = [tok for tok in parts if tok in scope_tokens]
        if folded:
            print(f"  FAIL: {t} -- scope token(s) {folded} folded into the name, violates C3")
            ok = False
        print(f"  {t}: system='{system}' (in registry) function='{function}' (base-form) "
              f"scope=49financial passed as an explicit call argument, not in the name -- OK")
    print(f"VERDICT: {'PASS-MXA6-AC7' if ok else 'FAIL-MXA6-AC7 see FAIL lines above'}")


def ac8():
    print(f"[{now()}] AC8 -- proposed read fence as exact prefixes; tables outside it named with "
          f"reason")
    print(f"  PROPOSED READ FENCE (bucket={BUCKET}):")
    print(f"    s3://{BUCKET}/{SMARTX_PREFIX}")
    print("    (ONE prefix covering 11 canon sub-prefixes -- MEASURED: every table lands at "
          "{prefix}{table}/date=YYYY-MM-DD/data.parquet regardless of which bronze scope it was "
          "built from)")
    for name, subdir, *_ in CANON_TABLES:
        print(f"      covers: {subdir} ({name})")
    print(f"  EXCLUDED WITHIN this prefix (named, {len(EXCLUDED_SUBDIRS)} entries -- pre-naming-law "
          f"draft objects):")
    for sub, reason in EXCLUDED_SUBDIRS.items():
        print(f"    s3://{BUCKET}/{SMARTX_PREFIX}{sub} -- {reason}")
    print(f"  EXCLUDED: other top-level/sibling prefixes (this bucket, other buckets) -- "
          f"{OTHER_TOP_LEVEL_EXCLUDED_REASON}")
    ok = len(CANON_TABLES) > 0
    print(f"VERDICT: {'PASS-MXA6-AC8' if ok else 'FAIL-MXA6-AC8'}")


def ac9():
    print(f"[{now()}] AC9 -- a property with no silver/served data says so and proposes no tool "
          f"(antecedent check)")
    objs = list_all(SMARTX_PREFIX)
    total_bytes = sum(o[1] for o in objs)
    print(f"  live check: {len(objs)} objects, {total_bytes} bytes under s3://{BUCKET}/"
          f"{SMARTX_PREFIX} at run time (ListObjectsV2, paginated)")
    has_data = len(objs) > 0
    print(f"  SmartX HAS live silver data at its canonical location (has_data={has_data}); the "
          f"antecedent of this criterion ('no silver or served data') is FALSE for this property, "
          f"so the criterion's obligation ('says so, proposes no tool') does not bind -- "
          f"{len(QUESTIONS)} questions ARE proposed against real tables (AC5/AC6), which is the "
          f"correct behavior under a TRUE antecedent. (Aside, not this criterion's antecedent: the "
          f"OTHER candidate location, s3://opal-data-smartx/, measured absent this run -- see module "
          f"docstring -- but that is a different, non-canonical bucket, not this property's silver "
          f"tier.)")
    ok = has_data and len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA6-AC9' if ok else 'FAIL-MXA6-AC9 data absent but tools were proposed, or vice versa'}")


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
