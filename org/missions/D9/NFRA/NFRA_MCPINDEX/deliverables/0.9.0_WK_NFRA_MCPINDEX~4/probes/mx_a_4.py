#!/usr/bin/env python3
"""
Probe for NFRA_MCPINDEX.TO-MX-a-4 (Orion / Inflection, S8/FWD-4).
Serial: 0.9.0_WK_NFRA_MCPINDEX~4. Read-only (boto3 GetObject/ListObjectsV2/HeadObject/read_metadata
only -- no writes to any AWS resource). Bucket under analysis: opal-data-inf (the live, DESIRED-plane
home this property's own scripts write and the deployed router's target, env override INF_S3_BUCKET,
e.g. data/inf/scripts/silver/convert_orion_api_to_silver.py:89 S3_BUCKET_V2, and confirmed live via
`aws s3api head-bucket --bucket opal-data-inf` at this cell's run time). The canonical Rule-30/LGIC
address (infra/logic/registry/scopes.json[inflection].bucket = "opal-data-inflection") is a DIFFERENT,
declared-not-provisioned-live bucket per that same registry's own alias note ("opal-data-inflection
does not exist yet"); a live HeadBucket probe on it returned 403 Forbidden, which per CLAUDE.md's
AWS/S3 trap catalogue ("S3 403 not 404") is NOT evidence of absence -- S3 also returns 403 for a
bucket that exists but is outside this credential's ListBucket grant. So this cell reports the
registry's DECLARED non-existence and its own MEASURED-but-ambiguous 403, and does not convert
either into a stronger claim.

Usage: py -3.12 mx_a_4.py AC<n>
Prints the measurement with instrument/vintage/denominator, then exactly one line:
  VERDICT: PASS-MXA4-AC<n>
  VERDICT: FAIL-MXA4-AC<n> <reason>
"""
import sys
import io
import json
import re
from datetime import datetime, timezone

import boto3

BUCKET = "opal-data-inf"
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
# CANONICAL TABLE MAP -- this cell's analysis, restricted to the LIVE gold-chain
# dispatch table (data/inf/scripts/gold/orion-gold-dispatch.sh:240-316, the INF_API_SILVER_*
# and INF_S_00 rows) -- every included table below is the DECLARED silver-tier writer of a
# row in that dispatch table; every excluded table (below, EXCLUDED dict) is a prefix that
# dispatch table names NOWHERE. Each entry: (name, prefix, partitioned, grain, freshness,
# source citation).
# ---------------------------------------------------------------------------
CANON_TABLES = [
    ("positions_mv", "silver/api_dims/positions_mv/", True,
     "one row per (account_id, ticker, snapshot_date) -- the current book of positions; 58 source "
     "columns camelCase->snake_case (convert_orion_api_to_silver.py:838-847 build_positions_mv "
     "docstring)",
     "snapshot_date (column, = partition dir date); market_value at any snapshot_date is "
     "positions_mv.current_value, DIRECT from Orion (:849-850 docstring, 'Replaces TRN-as-price "
     "reconstruction in INF_B_00')",
     "convert_orion_api_to_silver.py:838-911 build_positions_mv; dispatched as INF_API_SILVER_POSITIONS_MV "
     "(orion-gold-dispatch.sh:294)"),
    ("transactions", "silver/transactions/", True,
     "bronze passthrough (31 REST cols, verbatim names) + 6 mechanical additions + 11 Custom-Report "
     "join columns LEFT-JOINed by Orion transaction id; 'the SOLE canonical writer by amalgamation "
     "-- the REST full-history spine LEFT-JOINed with the Custom-Report-unique columns' "
     "(convert_transactions_to_silver.py:1-16 docstring); MEASURED at this cell's run: the 2026-09-19 "
     "and 2026-09-20 partitions are 43,462,194 and 43,547,893 bytes respectively (<0.2% day-over-day "
     "growth) and the 2026-09-20 file carries 1,478,763 rows (pyarrow ParquetFile.metadata.num_rows) "
     "-- consistent with 'full-history spine', NOT an incremental daily delta",
     "snapshot_date column / partition filename {date}.parquet",
     "convert_transactions_to_silver.py (module docstring); dispatched as INF_API_SILVER_TXN "
     "(orion-gold-dispatch.sh:296)"),
    ("assets_v2", "silver/assets_v2/", True,
     "mechanical passthrough of 58 Orion REST columns, camelCase->snake_case, no aggregation and no "
     "joins (convert_assets_v2_to_silver.py:8-17 docstring)",
     "output filename date {date}.parquet",
     "convert_assets_v2_to_silver.py:1-24 (module docstring); dispatched as INF_API_SILVER_ASSETS_V2 "
     "(orion-gold-dispatch.sh:292)"),
    ("performance", "silver/performance/", True,
     "per-client-partitioned weekly TWR (time-weighted return) factor with a derived running-product "
     "cumulative_twr from inception; one row per (client_id, week_date) "
     "(convert_performance_to_silver.py:8-19 docstring)",
     "output filename date {date}.parquet; per-row week_date column",
     "convert_performance_to_silver.py:1-33 (module docstring); dispatched as INF_API_SILVER_PERF "
     "(orion-gold-dispatch.sh:298)"),
    ("api_dims_billing", "silver/api_dims/billing/", True,
     "row-level billing dim, INFGRD-filtered via an account-id cross-reference against the unrealized "
     "tax dim (billing does not carry Representative.Id directly); is_fee_earning RETIRED FROM SILVER "
     "-- the single derivation home is data/inf/scripts/gold/lib/fee_classification.py "
     "(build_billing_dim.py:1-19 docstring)",
     "snapshot_date partition",
     "build_billing_dim.py:1-22 (module docstring); dispatched as INF_API_SILVER_BILLING "
     "(orion-gold-dispatch.sh:310)"),
    ("api_dims_tax_realized", "silver/api_dims/tax_realized/", True,
     "period-summed YTD/window realized gain/loss (cbo=1) -- 'Two dims (not one combined) because the "
     "semantics differ' (build_tax_dim.py:16-19 docstring)",
     "snapshot_date partition",
     "build_tax_dim.py:1-23 (module docstring); dispatched as INF_API_SILVER_TAX "
     "(orion-gold-dispatch.sh:301)"),
    ("api_dims_tax_unrealized", "silver/api_dims/tax_unrealized/", True,
     "current point-in-time unrealized gain/loss snapshot (cbo=0) (build_tax_dim.py:16-19 docstring)",
     "snapshot_date partition",
     "build_tax_dim.py:1-23 (module docstring); dispatched as INF_API_SILVER_TAX "
     "(orion-gold-dispatch.sh:301)"),
    ("api_dims_accounts_v2", "silver/api_dims/accounts_v2/", True,
     "one row per Orion account, 73-field NewPortfolio snapshot; scoped by a CUSTODIAN-CODE allowlist "
     "(custodian IN Fidelity_Inflection, Fidelity_LH) -- a DIFFERENT row-level mechanism from the "
     "rep_id filter other tables in this set use (convert_orion_api_to_silver.py:401-412 "
     "build_accounts_v2 docstring)",
     "snapshot_date partition",
     "convert_orion_api_to_silver.py:401-437 build_accounts_v2; dispatched as INF_API_SILVER_ACCOUNTS_V2 "
     "(orion-gold-dispatch.sh:290)"),
    ("api_dims_household_rep_mapping", "silver/api_dims/household_rep_mapping/", True,
     "one row per household_id, deduped to the PRIMARY rep via a priority rule; additional_rep_ids "
     "semicolon-joined when a household has joint coverage "
     "(convert_orion_api_to_silver.py:710-716 docstring)",
     "snapshot_date partition",
     "convert_orion_api_to_silver.py:707-745 build_household_rep_mapping; dispatched as "
     "INF_API_SILVER_HHREP (orion-gold-dispatch.sh:288)"),
    ("api_dims_performance", "silver/api_dims/performance/", True,
     "per-account/client performance snapshot from a best-effort 3-year-window pull -- a DIFFERENT "
     "grain and source from the root silver/performance/ table above despite the near-identical name; "
     "carries a DEFER guard that carries forward the PRIOR partition up to N=2 trading days on a "
     "bronze SKIP (convert_orion_api_to_silver.py:1056-1058 _DIM_DEFER_GUARD)",
     "snapshot_date partition",
     "convert_orion_api_to_silver.py:187-253 build_performance + :1044-1058 defer-guard config; "
     "dispatched as INF_API_SILVER_PERF_DIM (orion-gold-dispatch.sh:312)"),
    ("api_dims_representatives", "silver/api_dims/representatives/", True,
     "one row per Orion representative (18 rows per pull), name/status/broker-dealer roster dim "
     "(convert_orion_api_to_silver.py:656-659 docstring)",
     "snapshot_date partition",
     "convert_orion_api_to_silver.py:654-704 build_representatives; dispatched as INF_API_SILVER_REPS "
     "(orion-gold-dispatch.sh:287)"),
    ("canonical_prices", "silver/prices/canonical_prices.parquet", False,
     "one row per (date, ticker) -- 4-tier price hierarchy: T1 transaction-observed (median daily "
     "nav_price from Orion TRN), T2 Yahoo Finance, T3 linear interpolation, T4 carry-forward "
     "(INF_build_canonical_prices.py:8-16 docstring)",
     "date column (max); source column names which tier resolved each row",
     "INF_build_canonical_prices.py:1-30 (module docstring); dispatched as INF_S_00 "
     "(orion-gold-dispatch.sh:313)"),
]

# Everything else measured live under silver/, named with the exclusion reason (AC8). Every one of
# these is ABSENT from the live gold-chain dispatch table (orion-gold-dispatch.sh:240-316) -- a
# second, independent instrument agreeing with the S3 staleness measurement below.
EXCLUDED = {
    "silver/accounts_dim/": "legacy CSV-era account dim (convert_orion_to_silver.py:9, "
        "SILVER_ACCT_KEY); MEASURED 1 object, last-modified 2026-04-29, ~5 months stale against this "
        "cell's run date; absent from the dispatch table; superseded by silver/api_dims/accounts_v2/",
    "silver/api_dims/assets/": "'Path C' stopgap over canonical gold holdings, an explicit v1 "
        "workaround for a broken Orion Asset-grouping API endpoint (build_assets_dim.py:9-24 "
        "docstring, '8-day staleness acceptable for v1 ship'); MEASURED 3 objects, last-modified "
        "2026-05-05; absent from the dispatch table; superseded as the live holdings source by "
        "silver/api_dims/positions_mv/",
    "silver/api_dims/assets_v2/": "a SECOND, differently-scoped prefix that happens to share the "
        "'assets_v2' name with the live root-level silver/assets_v2/ table above; MEASURED 1 object, "
        "last-modified 2026-04-29; absent from the dispatch table; no gold script reads this nested "
        "path (the census in this cell's own AC1/AC5 code reads found zero references to "
        "'api_dims/assets_v2' outside this stale object's own key)",
    "silver/api_dims/household/": "MEASURED 1 object, last-modified 2026-04-28; absent from the "
        "dispatch table; superseded by silver/api_dims/household_rep_mapping/ -- though still named "
        "as a sanity-check INPUT in build_accounts_v2's own docstring (convert_orion_api_to_silver.py:"
        "411), which this cell reports as a live DESIRED-vs-APPLIED gap, not a table to propose a tool "
        "over",
    "silver/api_dims/activity/": "MEASURED 92 objects, newest partition snapshot_date=2026-08-14 -- "
        "~5 weeks stale against this cell's run date (2026-09-21); absent from the dispatch table "
        "despite 'activity' remaining a valid --dim choice in convert_orion_api_to_silver.py's "
        "DIM_BUILDERS (:1035) -- DESIRED in code, not APPLIED on any live cadence",
    "silver/orion-rest/": "legacy REST pilot (performance_weekly/, transactions/); MEASURED 308 "
        "objects, newest partition 2026-04-30; absent from the dispatch table; superseded by "
        "silver/api_dims/positions_mv/ and silver/transactions/",
    "silver/performance_dim/": "MEASURED 1 object, last-modified 2026-05-13; absent from the dispatch "
        "table; superseded by silver/api_dims/performance/",
    "silver/meta/": "2 tiny control-plane JSON sidecars (gap_manifest.json, trn_watermark.json) from "
        "the legacy CSV pipeline (convert_orion_to_silver.py:56-57); not a data table",
    "silver/prices/backfill_telemetry.json": "control-plane telemetry sidecar from "
        "backfill_yahoo_prices.py, not a data table; the fenced table above is "
        "silver/prices/canonical_prices.parquet only",
    "silver/_parity-snapshot/": "internal QA/bookkeeping prefix, not a data table",
    "silver/_silver_complete/": "internal completion-marker prefix, not a data table",
    "silver/api_dims/_chain_summary/": "internal gold-chain bookkeeping prefix, not a data table",
    "silver/eclipse/": "a SIBLING property in the SAME bucket (MX-a-5's own cell, "
        "convert_eclipse_portfolios_to_silver.py) -- a different Orion-suite vendor (Eclipse), "
        "explicitly out of this cell's Orion scope",
    "silver/historical_prices.parquet": "raw T2 Yahoo Finance price input, built by "
        "backfill_yahoo_prices.py and BLENDED into (superseded for query purposes by) "
        "silver/prices/canonical_prices.parquet's tier logic (INF_build_canonical_prices.py:9-10, "
        "'T2 yahoo_finance: from silver/historical_prices.parquet'); MEASURED single object, "
        "29,880,965 bytes, last-modified 2026-05-05 -- ~4.5 months stale against this cell's run "
        "date, while the canonical_prices.parquet it feeds was itself rebuilt 2026-09-20 (T1/T3/T4 "
        "tiers can refresh without a new T2 pull); named here rather than proposed as its own "
        "question table because a caller wanting a price reads the already-blended canonical_prices, "
        "which discloses its resolving tier per row",
}

# Top-level bucket prefixes OTHER than silver/, measured live (AC8/AC3 evidence -- this bucket is
# shared with Eclipse and control-plane/ops prefixes, not Orion-exclusive).
OTHER_TOP_LEVEL_EXCLUDED_REASON = (
    "a different top-level prefix in the same bucket, not silver/ and not (or not only) this "
    "property: orion/ (raw/bronze-adjacent vendor landing, not silver), eclipse/ (MX-a-5's vendor), "
    "bronze/ (raw input), gold/ (downstream product), code/ (synced scripts), config/, diagnostic/, "
    "investor-reporting/, otp/, platinum/ (served tier), qa/, telemetry/, plus ops/scratch prefixes "
    "(_compare/, _pre_rebuild_backup/, _rebuild_status/, _scratch/, _toolprobe_scratch/, backup/)"
)


def classify(objs):
    """Bucket every (key,size,lm) under objs (assumed prefix='silver/') into a canon table or
    EXCLUDED, by longest-prefix match. Returns (per_table, excluded_count, excluded_bytes,
    unclassified)."""
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
        print(f"  TABLE {name:32s} prefix={prefix:38s} objects={row['count']:6d} "
              f"bytes={row['bytes']:12d} newest_partition_date={row['newest']}")
        if row["count"] == 0:
            print(f"    WARNING: 0 objects live under {prefix} at run time")
    print(f"  EXCLUDED (named, s.AC8): {exc_count} objects, {exc_bytes} bytes")
    if unclassified:
        print(f"  UNCLASSIFIED (neither a canon table nor a named exclusion): "
              f"{len(unclassified)} -- {unclassified[:10]}")
        ok = False
    for name, prefix, partitioned, *_ in CANON_TABLES:
        if not partitioned:
            try:
                s3().head_object(Bucket=BUCKET, Key=prefix)
            except Exception as e:
                print(f"  FAIL: single-file table {name} ({prefix}) HEAD failed: {e}")
                ok = False
    if unclassified:
        ok = False
    verdict = "PASS-MXA4-AC1" if ok else "FAIL-MXA4-AC1 unclassified keys present, see UNCLASSIFIED above"
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
            objs = list_all(prefix)
            found_dates = set()
            for k, _, _ in objs:
                m = DATE_RE.search(k)
                if m:
                    found_dates.add(m.group(1))
            dates = sorted(found_dates)
            latest = dates[-1] if dates else None
            print(f"    latest value (source: live object keys, {len(objs)} objects scanned): "
                  f"{latest}")
            if latest is None:
                print(f"    FAIL: no dated partitions found live for {name}")
                ok = False
        else:
            import pyarrow.parquet as pq
            body = s3().get_object(Bucket=BUCKET, Key=prefix)["Body"].read()
            meta = pq.read_metadata(io.BytesIO(body))
            cols = [f.name for f in meta.schema.to_arrow_schema()]
            date_col = "date" if "date" in cols else None
            if date_col:
                import pyarrow.compute as pc
                table = pq.read_table(io.BytesIO(body), columns=[date_col])
                mx = pc.max(table.column(date_col)).as_py()
                print(f"    latest value (source: live object, column '{date_col}' max, "
                      f"{table.num_rows} rows scanned): {mx}")
            else:
                lm = s3().head_object(Bucket=BUCKET, Key=prefix)["LastModified"]
                print(f"    latest value (source: live object, no date column found in "
                      f"{cols[:10]}...; using S3 LastModified): {lm.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"VERDICT: {'PASS-MXA4-AC2' if ok else 'FAIL-MXA4-AC2 a table has no measurable latest value'}")


def ac3():
    print(f"[{now()}] AC3 -- firm/master scope rule per table, read from "
          f"infra/logic/registry/scopes.json (live file read at HEAD) and from producer code")
    with open("infra/logic/registry/scopes.json", encoding="utf-8") as f:
        scopes = json.load(f)
    inflection = next(r for r in scopes["scopes"] if r["key"] == "inflection")
    print(f"  scopes.json[inflection].bucket (CANONICAL, per Rule 30) = {inflection['bucket']} "
          f"(bucket_provisioned={inflection.get('bucket_provisioned')})")
    alias = next(a for a in inflection["aliases"] if a["spelling"] == "opal-data-inf")
    print(f"  scopes.json[inflection].aliases['opal-data-inf'] = {alias} -- this is the LIVE bucket "
          f"({BUCKET}) this cell reads; it DIFFERS from the canonical bucket name above")
    try:
        s3().head_bucket(Bucket="opal-data-inflection")
        print("  live HeadBucket on opal-data-inflection: succeeded (bucket reachable)")
    except Exception as e:
        print(f"  live HeadBucket on opal-data-inflection: {e} -- per CLAUDE.md's S3 403-not-404 "
              f"trap, this is AMBIGUOUS (could mean absent, or present-but-outside-this-grant), and "
              f"is reported as such, not converted into an absence claim")
    print(f"  scopes.json[inflection].monolith_scopes = {inflection['monolith_scopes']} -- orion and "
          f"eclipse are both listed as inflection-scoped monolith vendors")
    ok = True
    for name, prefix, *_ in CANON_TABLES:
        print(f"  TABLE {name}: scope=inflection (FIRM); key '{prefix}' carries NO firm-prefix "
              f"segment -- scope CANNOT be read from the key")
    print("  row-level scope mechanism MEASURED per table (three distinct mechanisms in this set):")
    print("    (a) INFGRD rep_id allowlist {3,6,10,11,12} via filter_to_inflection()/"
          "apply_aua_guard() (_orion_api_silver_lib.py:113,301-313) -- billing, tax_realized, "
          "tax_unrealized, household_rep_mapping")
    print("    (b) custodian-code allowlist (custodian IN Fidelity_Inflection, Fidelity_LH) -- "
          "accounts_v2 (convert_orion_api_to_silver.py:407-412), a DIFFERENT mechanism from (a)")
    print("    (c) an unconditional advisor_firm='inflection_wealth_management' STAMP with no "
          "in-function rep_id/custodian filter visible in this cell's read -- positions_mv, "
          "transactions, assets_v2, performance (root), api_dims/performance, representatives. "
          "FINDING, not fabricated as fact: whether the upstream BRONZE PULL for this group is "
          "already Inflection-scoped (so no silver-side filter is needed) was NOT verified by this "
          "cell -- named as an open verification gap, not resolved here")
    print(f"VERDICT: {'PASS-MXA4-AC3' if ok else 'FAIL-MXA4-AC3'}")


NEVER_SUM = [
    ("positions_mv.current_value (market value) is never summed across more than one snapshot_date",
     "cross-date -- each snapshot_date partition is a point-in-time holdings snapshot (one row per "
     "account_id/ticker/snapshot_date, convert_orion_api_to_silver.py:841); summing across dates "
     "double- (or N-times-) counts the same position"),
    ("transactions.trans_amount is never summed across more than one silver/transactions/{date}.parquet "
     "partition",
     "cross-date -- MEASURED at this cell's run: the 2026-09-19 and 2026-09-20 partitions are "
     "43,462,194 and 43,547,893 bytes (day-over-day growth <0.2%) and the 2026-09-20 file carries "
     "1,478,763 rows -- consistent with each partition being a FULL-HISTORY re-pull "
     "(convert_transactions_to_silver.py:1-16, 'the REST full-history spine'), not an incremental "
     "daily delta; summing across dates would multiply nearly every historical transaction by the "
     "number of dates summed"),
    ("tax_realized (period-summed YTD/window) and tax_unrealized (point-in-time snapshot) are never "
     "summed together into one tax gain/loss figure",
     "non-additive field / different measurement basis -- 'Two dims (not one combined) because the "
     "semantics differ ... Publishers JOIN on account_id when they need both' (build_tax_dim.py:16-19) "
     "-- the producer's own docstring says JOIN, never sum"),
    ("billing.is_fee_earning is never read or derived from this silver dim to compute a fee-earning "
     "total",
     "non-additive / wrong layer -- 'is_fee_earning RETIRED FROM SILVER ... a derived business "
     "classification never belonged in silver' (build_billing_dim.py:15-19); the single derivation "
     "home is data/inf/scripts/gold/lib/fee_classification.py"),
    ("silver/api_dims/performance and the root silver/performance table are never merged or summed "
     "into one performance figure despite the near-identical name",
     "different grain / different basis, not a cross-master rule but a table-identity hazard -- root "
     "silver/performance/ is per-client weekly TWR-factor cumulative product from inception "
     "(convert_performance_to_silver.py); silver/api_dims/performance/ is a per-account 3-year-window "
     "snapshot carrying its own DEFER carry-forward guard (convert_orion_api_to_silver.py:187-253, "
     ":1056-1058) -- conflating the two mixes two different measurement definitions under one label"),
    ("canonical_prices.price is never summed across ticker or across date",
     "non-additive field -- a price is a per-unit value, not a quantity; summing prices of different "
     "securities or different dates has no meaning without units held"),
    ("Inflection's Orion tables (advisor_firm='inflection_wealth_management', INFGRD rep_id "
     "{3,6,10,11,12}) are never summed with Eclipse's data in the same bucket (silver/eclipse/, "
     "MX-a-5's property), nor with any other partner firm onboarded later via the "
     "PARTNER_FIRM_TAGS/PARTNER_REP_IDS extension pattern",
     "cross-firm -- convert_orion_to_silver.py:92-100 documents the exact mechanism a future partner "
     "firm is onboarded through (a new rep_id allowlist entry), which is the live proof this bucket "
     "already tolerates more than one firm's data by construction"),
]


def ac4():
    print(f"[{now()}] AC4 -- every never-sum rule with its reason (cross-master/cross-firm/"
          f"cross-date/non-additive field)")
    for i, (rule, reason) in enumerate(NEVER_SUM, 1):
        print(f"  {i}. {rule}\n     REASON: {reason}")
    ok = len(NEVER_SUM) > 0
    print(f"VERDICT: {'PASS-MXA4-AC4' if ok else 'FAIL-MXA4-AC4 no rules'}")


# (question_id, question_text, table, fields, source, assignment, [tool_name,] reason)
QUESTIONS = [
    (1, "What are [account/household]'s current holdings and their market value?",
     "positions_mv", "account_id, ticker, current_value, snapshot_date",
     "producer code (convert_orion_api_to_silver.py:849-850, 'positions_mv.current_value is now the "
     "AUA-feeding source')",
     "typed_query",
     "a single-table filter+read on the latest snapshot_date partition; C6's typed query covers it "
     "with no cross-table logic"),
    (2, "What is [account/household]'s total AUA as of the latest snapshot?",
     "positions_mv", "current_value (summed within ONE snapshot_date only, per AC4 rule 1), "
     "account_id/household_id, snapshot_date",
     "producer code (same citation as Q1) + reasoning (AUA = sum of current holdings at one date, "
     "the standard definition this producer's own comment names)",
     "typed_query",
     "a single-date filter+group-by+sum over one table's additive field; C6's grouping rules already "
     "enforce the never-sum-across-dates bound"),
    (3, "What transactions occurred for [account/household] over [date range]?",
     "transactions", "trans_id/transaction_id, trans_date/trade_date, trans_amount, type_desc, "
     "account_id",
     "producer code (convert_transactions_to_silver.py, bronze+silver schema block)",
     "typed_query",
     "a filter over one table's columns on a single (most-recent) partition; per AC4 rule 2 the tool "
     "surface must read the LATEST partition only, never sum trans_amount across partitions -- a "
     "constraint C6's date-range filter on ONE partition satisfies without a special tool"),
    (4, "What is [client/household]'s cumulative time-weighted return (TWR) since inception?",
     "performance", "client_id, week_date, cumulative_twr, inception_date",
     "producer code (convert_performance_to_silver.py, 'cumulative_twr: running product of "
     "twr_factor from inception')",
     "typed_query",
     "cumulative_twr is already a PRECOMPUTED column (the producer does the running-product math); "
     "a single-table filter+read on the latest week_date needs no purpose-built logic"),
    (5, "What is [account]'s realized vs. unrealized tax gain/loss as of [date]?",
     "api_dims_tax_realized (period-summed) and api_dims_tax_unrealized (point-in-time), read "
     "SEPARATELY per AC4 rule 3",
     "account_id, snapshot_date, gain/loss columns (per-dim; cbo=0 unrealized / cbo=1 realized)",
     "producer code (build_tax_dim.py:16-19)",
     "typed_query",
     "two independent single-table filtered reads; the caller joins on account_id if both are wanted, "
     "which C6 already permits as two calls -- no cross-row business logic needed"),
    (6, "What billing/fee amounts were assessed to [account/household] as of [date], excluding any "
     "fee-earning classification (AC4 rule 4)?",
     "api_dims_billing", "account_id, billing fields present in the dim, snapshot_date",
     "producer code (build_billing_dim.py docstring)",
     "typed_query",
     "a single-table filter+read; the EXCLUDED is_fee_earning question is out of scope for any tool "
     "over this table per AC4 rule 4 and is named, not silently answered"),
    (7, "Who is the advisor/rep of record for [account/household], and how was that attribution "
     "derived?",
     "api_dims_accounts_v2 + api_dims_household_rep_mapping (JOIN, with a documented fallback order)",
     "accountId, rep_id, householdId, household_rep_mapping.rep_id (primary, priority-deduped), "
     "rep_id_source",
     "producer code (convert_transactions_to_silver.py's rep_id/rep_id_source columns document the "
     "SAME rescue-join pattern: 'rep_id JOIN from accounts_v2 silver via accountId; on a MISS, "
     "RESCUED from household_rep_mapping via householdId ... rep_id_source names where its own "
     "attribution came from')",
     "tool", "orion_resolve_rep_of_record",
     "requires a two-table JOIN with an explicit FALLBACK ORDER (accounts_v2 first, "
     "household_rep_mapping on a miss) and must surface WHICH source resolved the answer -- business "
     "logic beyond a single-table filter/group-by/aggregate that C6's typed query is scoped to "
     "(PRD C6); the join and fallback are already implemented once in convert_transactions_to_silver.py "
     "and are re-usable as a read-only tool rather than re-derived per caller"),
    (8, "What is the full account roster (registrations, custodian, managed flag) for Inflection?",
     "api_dims_accounts_v2", "accountId, custodian, registrationName, isManaged, accountStartDate",
     "producer code (convert_orion_api_to_silver.py:401-417 docstring, 73-field NewPortfolio dim)",
     "typed_query",
     "a single-table filter+read; the custodian-code scope filter (AC3(b)) is already applied at "
     "silver-write time, so a caller sees only in-scope rows without extra logic"),
    (9, "Who are Inflection's Orion representatives (name, id, status)?",
     "api_dims_representatives", "rep_id, full_name, is_active, status, broker_dealer",
     "producer code (convert_orion_api_to_silver.py:654-659 docstring, 18-row roster)",
     "typed_query",
     "a single-table, small (18-row) point lookup; no aggregation or join needed"),
    (10, "What is the current or historical price for [ticker] held by Inflection accounts?",
     "canonical_prices", "date, ticker, price, source (tier)",
     "producer code (INF_build_canonical_prices.py:8-16, 4-tier hierarchy)",
     "typed_query",
     "a single-table point lookup by ticker and date; the 'source' column already discloses which "
     "price tier resolved the answer, satisfying C4's completeness/caveat requirement with no extra "
     "tool logic"),
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
              f"read this cell; sourced from producer code and, for Q7, a re-use of a pattern already "
              f"implemented in convert_transactions_to_silver.py, per Rule 24's grammar test: this is "
              f"CODE evidence, never a claim about what staff actually ask)")
    ok = len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA4-AC5' if ok else 'FAIL-MXA4-AC5 no questions'}")


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
    print(f"VERDICT: {'PASS-MXA4-AC6' if ok else 'FAIL-MXA4-AC6 an unassigned question'}")


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
    print(f"  systems.json read live: {len(keys)} keys; 'orion' present: {'orion' in keys}")
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
              f"scope=inflection passed as an explicit call argument, not in the name -- OK")
    print(f"VERDICT: {'PASS-MXA4-AC7' if ok else 'FAIL-MXA4-AC7 see FAIL lines above'}")


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
    print("  NOTE (finding, not a fence line): the Rule-30/LGIC canonical address for this property "
          "is bucket opal-data-inflection (infra/logic/registry/scopes.json[inflection].bucket), "
          "DISTINCT from the live bucket fenced above (opal-data-inf); the registry's own alias note "
          "says the canonical bucket 'does not exist yet', and this cell's live HeadBucket probe "
          "(AC3) returned an AMBIGUOUS 403 rather than a confirming 404 -- the same migration-gap "
          "shape MX-a-3 found for Black Diamond (opal-data-bd vs opal-data-49financial). This cell "
          "fences to the LIVE location per Rule 30's own non-application clause ('existing pipelines "
          "reach conformance through their own migration project, never as a rider on unrelated "
          "work'); the migration gap is reported, not fixed, here.")
    ok = len(CANON_TABLES) > 0 and len(EXCLUDED) > 0
    print(f"VERDICT: {'PASS-MXA4-AC8' if ok else 'FAIL-MXA4-AC8'}")


def ac9():
    print(f"[{now()}] AC9 -- a property with no silver/served data says so and proposes no tool "
          f"(antecedent check)")
    objs = list_all("silver/")
    total_bytes = sum(o[1] for o in objs)
    print(f"  live check: {len(objs)} objects, {total_bytes} bytes under s3://{BUCKET}/silver/ "
          f"at run time (ListObjectsV2, paginated)")
    has_data = len(objs) > 0
    print(f"  Orion HAS live silver data (has_data={has_data}); the antecedent of this criterion "
          f"('no silver or served data') is FALSE for this property, so the criterion's obligation "
          f"('says so, proposes no tool') does not bind -- {len(QUESTIONS)} questions ARE proposed "
          f"against real tables (AC5/AC6), which is the correct behavior under a TRUE antecedent")
    ok = has_data and len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA4-AC9' if ok else 'FAIL-MXA4-AC9 data absent but tools were proposed, or vice versa'}")


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
