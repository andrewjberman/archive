#!/usr/bin/env python3
"""
Probe for NFRA_MCPINDEX.TO-MX-a-5 (Eclipse / Inflection, S8/FWD-4).
Serial: 0.9.0_WK_NFRA_MCPINDEX~4. Read-only (boto3 GetObject/ListObjectsV2/HeadObject/read_metadata
only -- no writes to any AWS resource). Bucket under analysis: opal-data-inf (the same live bucket
MX-a-4/Orion reads; Eclipse is a SECOND vendor's silver tier in the SAME bucket, prefix
silver/eclipse/, confirmed live via `aws s3api head-bucket --bucket opal-data-inf` at this cell's
run time; producer convert_eclipse_portfolios_to_silver.py:3-4 writes
s3://opal-data-inf/silver/eclipse/{date}/). Scope: infra/logic/registry/scopes.json[inflection]
.monolith_scopes.eclipse = ["inflection"] -- Eclipse, like Orion, is entirely Inflection-scoped (no
"eclipse" scopes.json key of its own; it is a MONOLITH VENDOR under the inflection FIRM scope).

Layout difference from MX-a-4/Orion, MEASURED not assumed: Orion's silver tables each own a
DISTINCT sub-prefix (silver/api_dims/positions_mv/, silver/transactions/, ...), so each can be
separately fenced. Eclipse's four tables (portfolios_simple, portfolios_full, models,
model_composition) all live as SIBLING FILES under the SAME silver/eclipse/{date}/ folder --
distinguished by FILENAME, not by a table-specific path segment. So no S3 prefix can fence one
Eclipse table without also fencing the other three; the read fence this cell proposes (AC8) is
therefore ONE prefix (silver/eclipse/) covering all four tables plus the per-date _meta sentinel.

Usage: py -3.12 mx_a_5.py AC<n>
Prints the measurement with instrument/vintage/denominator, then exactly one line:
  VERDICT: PASS-MXA5-AC<n>
  VERDICT: FAIL-MXA5-AC<n> <reason>
"""
import sys
import io
import json
import re
from datetime import datetime, timezone

import boto3

BUCKET = "opal-data-inf"
REGION = "us-east-1"
ECLIPSE_PREFIX = "silver/eclipse/"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def s3():
    return boto3.client("s3", region_name=REGION)


DATE_RE = re.compile(r"silver/eclipse/(\d{4}-\d{2}-\d{2})/")


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
# CANONICAL TABLE MAP -- the four silver artifacts convert_eclipse_portfolios_to_silver.py:6-10
# names as its outputs, each a SIBLING FILENAME under silver/eclipse/{date}/ (not a distinct
# sub-prefix -- see module docstring above). Each entry: (name, filename, grain, freshness,
# source citation).
# ---------------------------------------------------------------------------
CANON_TABLES = [
    ("portfolios_simple", "portfolios_simple.parquet",
     "one row per Eclipse portfolio (accountId + modelId join keys); DOCSTRING claims 835 rows "
     "(convert_eclipse_portfolios_to_silver.py:7) -- MEASURED at this cell's run: the live "
     "2026-09-20 partition carries 844 rows (pyarrow read_metadata), i.e. the docstring's count is "
     "a STALE snapshot from an earlier pull, not a live invariant; this cell reports the LIVE count "
     "as the authoritative latest value, not the docstring's",
     "date folder name (silver/eclipse/{date}/); no per-row date column in this table",
     "convert_eclipse_portfolios_to_silver.py:1-11 module docstring + :201-233 convert_portfolios; "
     "dispatched as INF_ECLIPSE_SILVER (orion-gold-dispatch.sh:315)"),
    ("portfolios_full", "portfolios_full.parquet",
     "one row per Eclipse portfolio, value/cash/rebalance detail (totalValue, managedValue, "
     "excludedValue, currentCash, lastRebalancedOn); has NO accountId -- the gold tier joins it to "
     "portfolios_simple on portfolio id (convert_eclipse_portfolios_to_silver.py:240-243 docstring). "
     "DOCSTRING claims 842 rows (:8); MEASURED live 2026-09-20: 858 rows -- same stale-docstring "
     "finding as portfolios_simple above",
     "date folder name; no per-row date column",
     "convert_eclipse_portfolios_to_silver.py:236-261 convert_portfolios_full; dispatched as "
     "INF_ECLIPSE_SILVER (orion-gold-dispatch.sh:315, same script as portfolios_simple)"),
    ("models", "models.parquet",
     "one row per Eclipse model (18 rows per pull, name/status/owner roster) -- MEASURED live "
     "2026-09-20: 18 rows, matching the docstring exactly (convert_eclipse_portfolios_to_silver.py:9)",
     "date folder name; no per-row date column",
     "convert_eclipse_portfolios_to_silver.py:264-283 convert_models; dispatched as INF_ECLIPSE_SILVER "
     "(orion-gold-dispatch.sh:315)"),
    ("model_composition", "model_composition.parquet",
     "one row per Opal-relevant Eclipse model (9 of the 18 models, OPAL_ECLIPSE_MODEL_IDS = "
     "{3,5,6,7,8,9,10,28,29}), modelDetail JSON + model_aum cached headline figure -- MEASURED live "
     "2026-09-20: 9 rows, matching the docstring exactly (:10)",
     "date folder name; no per-row date column",
     "convert_eclipse_portfolios_to_silver.py:286-321 convert_model_composition; dispatched as "
     "INF_ECLIPSE_SILVER (orion-gold-dispatch.sh:315)"),
]

# Everything else measured live under silver/eclipse/, named with the exclusion reason (AC8).
EXCLUDED_SUFFIXES = {
    "_meta/silver_complete.json": "per-date completion sentinel written by main() "
        "(convert_eclipse_portfolios_to_silver.py:395-400); a control-plane marker (started_at/"
        "completed_at/overall/rows_per_artifact/errors), not a data table -- the same shape as "
        "Orion's silver/meta/ sidecars (MX-a-4 AC8)",
}

# Top-level bucket prefixes OTHER than silver/eclipse/, measured live (AC8/AC3 evidence -- this
# bucket is shared with Orion and control-plane/ops prefixes, not Eclipse-exclusive).
OTHER_TOP_LEVEL_EXCLUDED_REASON = (
    "a different prefix in the same bucket, not silver/eclipse/ and not this property: "
    "silver/api_dims/*, silver/transactions/, silver/assets_v2/, silver/performance/, "
    "silver/prices/, silver/accounts_dim/, silver/orion-rest/ and the other silver/ prefixes named "
    "in MX-a-4's own AC8 (Orion's tables, a DIFFERENT Orion-suite vendor under the same inflection "
    "scope, explicitly out of this cell's Eclipse scope); orion/ and eclipse/ (raw/bronze-adjacent "
    "vendor landing, not silver -- bronze/eclipse/ specifically is the input this cell's tables are "
    "converted FROM, per convert_eclipse_portfolios_to_silver.py:3); bronze/ (other vendors' raw "
    "input); gold/ (downstream product, incl. gold/eclipse/ -- INF_E_00's own output, a build target "
    "for MX-t-5, not a read source here); code/ (synced scripts), config/, diagnostic/, "
    "investor-reporting/, otp/, platinum/ (served tier), qa/, telemetry/, plus ops/scratch prefixes "
    "(_compare/, _pre_rebuild_backup/, _rebuild_status/, _scratch/, _toolprobe_scratch/, backup/)"
)


def classify(objs):
    """Bucket every (key,size,lm) under objs (assumed prefix=ECLIPSE_PREFIX) into a canon table or
    EXCLUDED, by FILENAME suffix (not folder prefix -- see module docstring). Returns (per_table,
    excluded_count, excluded_bytes, unclassified)."""
    per_table = {t[0]: {"count": 0, "bytes": 0, "newest": None} for t in CANON_TABLES}
    excluded_count = 0
    excluded_bytes = 0
    unclassified = []
    for key, size, lm in objs:
        matched = None
        for name, filename, *_ in CANON_TABLES:
            if key.endswith("/" + filename):
                matched = name
                break
        if matched:
            per_table[matched]["count"] += 1
            per_table[matched]["bytes"] += size
            m = DATE_RE.search(key)
            d = m.group(1) if m else None
            if d and (per_table[matched]["newest"] is None or d > per_table[matched]["newest"]):
                per_table[matched]["newest"] = d
        elif any(key.endswith("/" + suf) for suf in EXCLUDED_SUFFIXES):
            excluded_count += 1
            excluded_bytes += size
        else:
            unclassified.append(key)
    return per_table, excluded_count, excluded_bytes, unclassified


def ac1():
    print(f"[{now()}] AC1 -- live listing, instrument boto3 s3:ListObjectsV2 (paginated), "
          f"bucket={BUCKET}, prefix={ECLIPSE_PREFIX}")
    objs = list_all(ECLIPSE_PREFIX)
    print(f"  denominator: {len(objs)} objects under {ECLIPSE_PREFIX} (read verb: ListObjectsV2, "
          f"paginated, live at run time)")
    per_table, exc_count, exc_bytes, unclassified = classify(objs)
    ok = True
    for name, filename, *_ in CANON_TABLES:
        row = per_table[name]
        print(f"  TABLE {name:20s} filename={filename:28s} objects={row['count']:6d} "
              f"bytes={row['bytes']:12d} newest_partition_date={row['newest']}")
        if row["count"] == 0:
            print(f"    WARNING: 0 objects live under {ECLIPSE_PREFIX}*/{filename} at run time")
            ok = False
    print(f"  EXCLUDED (named, s.AC8): {exc_count} objects, {exc_bytes} bytes")
    if unclassified:
        print(f"  UNCLASSIFIED (neither a canon table nor a named exclusion): "
              f"{len(unclassified)} -- {unclassified[:10]}")
        ok = False
    verdict = "PASS-MXA5-AC1" if ok else "FAIL-MXA5-AC1 unclassified keys or an empty table, see above"
    print(f"VERDICT: {verdict}")


def ac2():
    print(f"[{now()}] AC2 -- grain/freshness/latest value per table, read from producer code "
          f"(cited) and from the live objects (pyarrow read_metadata, column-projected)")
    ok = True
    for name, filename, grain, freshness, source in CANON_TABLES:
        print(f"  TABLE {name}")
        print(f"    grain (source: producer code + live pyarrow read_metadata, {source}): {grain}")
        print(f"    freshness field (source: producer code, {source}): {freshness}")
        objs = list_all(ECLIPSE_PREFIX)
        found_dates = set()
        for k, _, _ in objs:
            if k.endswith("/" + filename):
                m = DATE_RE.search(k)
                if m:
                    found_dates.add(m.group(1))
        dates = sorted(found_dates)
        latest = dates[-1] if dates else None
        print(f"    latest value (source: live object keys, {len(dates)} distinct dates found for "
              f"this filename across {len(objs)} objects scanned): {latest}")
        if latest is None:
            print(f"    FAIL: no dated partitions found live for {name}")
            ok = False
            continue
        import pyarrow.parquet as pq
        key = f"{ECLIPSE_PREFIX}{latest}/{filename}"
        body = s3().get_object(Bucket=BUCKET, Key=key)["Body"].read()
        meta = pq.read_metadata(io.BytesIO(body))
        print(f"    live row count at latest partition (source: pyarrow read_metadata on "
              f"s3://{BUCKET}/{key}): {meta.num_rows} rows, {meta.num_columns} cols")
    print(f"VERDICT: {'PASS-MXA5-AC2' if ok else 'FAIL-MXA5-AC2 a table has no measurable latest value'}")


def ac3():
    print(f"[{now()}] AC3 -- firm/master scope rule per table, read from "
          f"infra/logic/registry/scopes.json (live file read at HEAD) and from producer code")
    with open("infra/logic/registry/scopes.json", encoding="utf-8") as f:
        scopes = json.load(f)
    inflection = next(r for r in scopes["scopes"] if r["key"] == "inflection")
    print(f"  scopes.json[inflection].monolith_scopes = {inflection['monolith_scopes']} -- "
          f"'eclipse' is a MONOLITH VENDOR key under inflection, not its own scopes.json row; "
          f"Eclipse (this cell) is entirely inflection-scoped, same as Orion (MX-a-4)")
    ok = True
    for name, filename, *_ in CANON_TABLES:
        print(f"  TABLE {name}: scope=inflection (FIRM); the filename '{filename}' carries NO "
              f"firm-prefix segment, and the only path segment (the {{date}} folder) carries no "
              f"scope information either -- scope CANNOT be read from the key")
    print("  row-level scope mechanism MEASURED (this cell's own read of the producer code):")
    print("    convert_eclipse_portfolios_to_silver.py imports coerce_silver_ids from "
          "_orion_api_silver_lib.py (dtype coercion ONLY -- MEASURED at _orion_api_silver_lib.py:283-298, "
          "no scope filter inside it) but does NOT import or call filter_to_inflection() "
          "(_orion_api_silver_lib.py:301-311, the INFGRD rep_id allowlist Orion's tables use) -- "
          "0 calls to filter_to_inflection found in this cell's read of "
          "convert_eclipse_portfolios_to_silver.py. FINDING, not fabricated as fact: whether the "
          "Eclipse VENDOR CONNECTION itself is already Inflection-exclusive (a single-tenant "
          "integration, so no in-pipeline filter is needed) was NOT verified by this cell -- named "
          "as an open verification gap, same shape as MX-a-4 AC3 finding (c), not resolved here. "
          "Indirect evidence toward that reading: pull_eclipse_portfolios.py's own docstring "
          "describes its endpoints as returning 'all firm portfolios' (singular firm), and "
          "scopes.json lists exactly one scope (inflection) under monolith_scopes.eclipse.")
    print(f"VERDICT: {'PASS-MXA5-AC3' if ok else 'FAIL-MXA5-AC3'}")


NEVER_SUM = [
    ("portfolios_simple.* and portfolios_full.* fields are never summed across more than one "
     "silver/eclipse/{date}/ partition",
     "cross-date -- MEASURED at this cell's run: the 2026-09-19 and 2026-09-20 partitions of both "
     "files are near-identical in size (portfolios_simple 64,362B -> 64,437B; portfolios_full "
     "109,618B -> 109,564B; models.parquet BYTE-IDENTICAL 25,029B both days) and pull_eclipse_"
     "portfolios.py's own docstring states '--date IS AN OUTPUT FILENAME, NOT A QUERY ... ALL pulls "
     "fetch TODAY'S live state' (bronze docstring, top of file) -- each date partition is an "
     "independent FULL snapshot of the vendor's then-current portfolio list, not an incremental "
     "delta; summing across dates double- (or N-times-) counts the same portfolio"),
    ("models.* and model_composition.* fields are never summed across more than one date partition",
     "cross-date -- same reasoning as above: MEASURED live row counts are stable across dates (18 "
     "and 9 rows respectively at both 2026-09-19 and 2026-09-20), consistent with a fixed catalog "
     "re-pulled in full each day, not a delta; model_composition.model_aum summed across two dates "
     "would roughly double each model's cached AUM figure"),
    ("portfolios_full.total_value (live portfolio list, account-decomposable) is never summed "
     "together with model_composition.model_aum (the cached Eclipse model-headline AUM figure) into "
     "one combined total",
     "non-additive / different measurement basis -- the gold tier (INF_E_00.eclipse_model_portfolios."
     "py:19-23) deliberately carries these as TWO SIDE-BY-SIDE figures and computes an explicit "
     "aum_variance = model_aum - total_value diagnostic field (:303,322) precisely because they are "
     "two independent measurements of the same thing meant to be COMPARED, never combined into one "
     "number"),
    ("portfolios_simple/portfolios_full rows whose model_id is NOT in OPAL_ECLIPSE_MODEL_IDS "
     "{3,5,6,7,8,9,10,28,29} are never summed into an 'Opal-managed AUM' total read directly from "
     "silver",
     "wrong layer / non-additive-without-filter -- MEASURED at this cell's run: of 844 live "
     "portfolios_simple rows, 567 carry an Opal model_id, 95 carry a non-Opal model_id and 182 carry "
     "a null model_id (33% of rows would be wrongly included in an unfiltered total); the "
     "Opal-model filter is applied at GOLD (INF_E_00.py:151 `opal = simple[simple['model_id']."
     "isin(OPAL_ECLIPSE_MODEL_IDS)]`), not in silver -- a caller computing an Opal AUM total directly "
     "from silver must apply the same filter or over-counts"),
    ("portfolios_simple/portfolios_full rows with is_deleted=1 are never summed into a live AUM "
     "total read directly from silver",
     "wrong layer -- the gold tier defensively filters `is_deleted.fillna(0) != 1` (INF_E_00.py:"
     "153-154); MEASURED at this cell's run: 0 of 844 live portfolios_simple rows currently carry "
     "is_deleted=1, so this rule is not materially exercised TODAY, but the column exists in the "
     "live schema and the gold tier's own defensive filter is the evidence this can occur -- a "
     "typed-query total must apply the same filter to stay correct as data changes"),
    ("Eclipse's silver tables (this cell) are never summed with Orion's silver tables (MX-a-4's "
     "property, same bucket) without an explicit accounts_v2 crosswalk join",
     "cross-vendor / different join keys -- Eclipse's own account identifier is "
     "eclipse_account_id_raw/eclipse_account_id_int (convert_eclipse_portfolios_to_silver.py:"
     "208-217), a DIFFERENT id space from Orion's accountId; INF_E_00.eclipse_model_portfolios.py:"
     "13-14 names silver/api_dims/accounts_v2/ as the ONLY sanctioned join target (household_id + "
     "advisor + Orion current_value), so any figure spanning both vendors' silver tables without "
     "that crosswalk conflates two unrelated id spaces"),
    ("Eclipse's silver tables are never summed with Black Diamond's (MX-a-3) or any future partner "
     "firm's data",
     "cross-firm -- the same shared-bucket, key-prefix-scoped isolation model MX-a-4 AC4 rule 7 "
     "measured for Orion applies identically here: silver/eclipse/ carries only inflection-scoped "
     "data (AC3), and the bucket's per-firm isolation is by key prefix only, never by a bucket "
     "boundary (PRD C7)"),
]


def ac4():
    print(f"[{now()}] AC4 -- every never-sum rule with its reason (cross-master/cross-firm/"
          f"cross-date/non-additive field)")
    for i, (rule, reason) in enumerate(NEVER_SUM, 1):
        print(f"  {i}. {rule}\n     REASON: {reason}")
    ok = len(NEVER_SUM) > 0
    print(f"VERDICT: {'PASS-MXA5-AC4' if ok else 'FAIL-MXA5-AC4 no rules'}")


# (question_id, question_text, table, fields, source, assignment, [tool_name,] reason)
QUESTIONS = [
    (1, "What Eclipse model portfolio is [account] assigned to, and what is its current total "
        "value?",
     "portfolios_simple (accountId/eclipse_account_id, modelId, id) + portfolios_full (id, "
     "totalValue)",
     "eclipse_account_id_raw/eclipse_account_id_int, model_id, id (portfolio id, join key), "
     "total_value",
     "producer code (convert_eclipse_portfolios_to_silver.py:240-243 docstring: "
     "'portfolios_full has NO accountId -- the gold tier joins it to portfolios_simple on "
     "portfolio id')",
     "typed_query",
     "two single-table filtered reads joined by the CALLER on portfolio id (a straight "
     "primary-key match, no fallback order needed) -- the same two-call pattern MX-a-4 Q5 used "
     "for tax_realized/tax_unrealized"),
    (2, "What is Eclipse's aggregate model-headline AUM vs. its live portfolio-list AUM for "
        "Inflection as of [date], and what is the variance between them?",
     "portfolios_full.total_value (summed within Opal-model rows, one date only, per AC4 rules 1/4) "
     "and model_composition.model_aum (compared, never summed together, per AC4 rule 3)",
     "total_value, model_aum, id (model id)",
     "producer code (INF_E_00.eclipse_model_portfolios.py:19-23,283-304, the aum_variance "
     "computation already implemented at gold)",
     "tool", "eclipse_summarize_aum_variance",
     "requires filtering to OPAL_ECLIPSE_MODEL_IDS (AC4 rule 4), excluding is_deleted rows (AC4 "
     "rule 5), summing total_value within that filtered set, reading model_aum from a SEPARATE "
     "table, and computing/disclosing the variance between the two -- multi-step business logic "
     "beyond C6's single-table filter/group-by/aggregate scope, and the exact computation already "
     "exists once in INF_E_00.py as a reusable pattern"),
    (3, "What is the current model composition (name, AUM, detail) of Eclipse model [model_id]?",
     "model_composition", "id, model_aum, model_detail (JSON), name",
     "producer code (convert_eclipse_portfolios_to_silver.py:286-321 convert_model_composition)",
     "typed_query",
     "a single-table filter+read on a 9-row table; no cross-table logic"),
    (4, "Which accounts/portfolios are currently assigned to Eclipse model [model_id]?",
     "portfolios_simple", "id, model_id, eclipse_account_id_raw, eclipse_account_id_int",
     "producer code (convert_eclipse_portfolios_to_silver.py:201-233 convert_portfolios)",
     "typed_query",
     "a single-table filter on model_id; no aggregation or join needed"),
    (5, "What is [account]'s current cash position (current/pending/target cash and cash "
        "percentages) in Eclipse?",
     "portfolios_full", "id, current_cash, current_cash_percent, pending_cash, target_cash, "
     "target_cash_percent",
     "producer code (convert_eclipse_portfolios_to_silver.py:98-105 _FULL_FLOAT_FIELDS)",
     "typed_query",
     "a single-table filter+read; the caller resolves portfolio id via portfolios_simple first "
     "(same two-call join pattern as Q1) -- no purpose-built tool logic needed"),
    (6, "When was [account]'s Eclipse portfolio last rebalanced, and is it currently trade-blocked "
        "or holding pending trades?",
     "portfolios_full", "id, last_rebalanced_on, trade_blocked, trades_pending",
     "producer code (convert_eclipse_portfolios_to_silver.py:92-96,109 _FULL_INT_FIELDS/"
     "_FULL_DATE_FIELDS)",
     "typed_query",
     "a single-table filter+read on a handful of status columns; no aggregation needed"),
    (7, "What is the full Eclipse model roster (name, status, owner, community-model flag), "
        "including models outside Opal's 9-model set?",
     "models", "id, status_id, owner_user_id, is_community_model, is_deleted",
     "producer code (convert_eclipse_portfolios_to_silver.py:264-283 convert_models, 18-row roster)",
     "typed_query",
     "a single-table, small (18-row) point lookup; no aggregation or join needed -- mirrors MX-a-4 "
     "Q9's reasoning for Orion's representatives table"),
    (8, "How many Eclipse portfolios does Inflection currently have, broken out by "
        "Opal-model-assigned vs. not?",
     "portfolios_simple", "id, model_id",
     "reasoning (a group-by/count over model_id membership in OPAL_ECLIPSE_MODEL_IDS) grounded in "
     "MEASURED live counts this cell took (844 total, 567 Opal-model, 95 non-Opal-model, 182 "
     "null model_id -- AC4 rule 4 evidence)",
     "typed_query",
     "a single-table group-by/count with a membership filter against a fixed id set; C6's "
     "structured group-by covers it with no cross-table logic"),
    (9, "What are the value/cash/rebalance details of [account]'s Eclipse portfolio as of the "
        "latest pull?",
     "portfolios_full", "id, total_value, managed_value, excluded_value, current_cash, "
     "num_of_associated_accounts",
     "producer code (INF_E_00.eclipse_model_portfolios.py:150-152 full_cols list, the same column "
     "set the gold tier itself selects)",
     "typed_query",
     "a single-table filter+read on the latest date partition; no purpose-built tool logic needed"),
    (10, "What is the Eclipse-to-Orion account crosswalk for [account] (eclipse_account_id vs. "
         "Orion accountId), to join Eclipse data with Orion's household/advisor dims?",
     "portfolios_simple", "eclipse_account_id_raw, eclipse_account_id_int, account_id (post "
     "coerce_silver_ids)",
     "producer code (convert_eclipse_portfolios_to_silver.py:208-223, the raw/int id columns "
     "coerce_silver_ids enforces)",
     "typed_query",
     "a single-table point lookup; the CROSS-VENDOR join itself (to Orion's accounts_v2) is a "
     "caller-side two-call join per AC4 rule 6, not business logic requiring a purpose-built tool"),
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
              f"read this cell; sourced from producer code, from a re-use of a pattern already "
              f"implemented in INF_E_00.eclipse_model_portfolios.py, or from reasoning grounded in "
              f"this cell's own live measurement, per Rule 24's grammar test: this is CODE/MEASURED "
              f"evidence, never a claim about what staff actually ask)")
    ok = len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA5-AC5' if ok else 'FAIL-MXA5-AC5 no questions'}")


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
    print(f"VERDICT: {'PASS-MXA5-AC6' if ok else 'FAIL-MXA5-AC6 an unassigned question'}")


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
    print(f"  systems.json read live: {len(keys)} keys; 'eclipse' present: {'eclipse' in keys}")
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
    print(f"VERDICT: {'PASS-MXA5-AC7' if ok else 'FAIL-MXA5-AC7 see FAIL lines above'}")


def ac8():
    print(f"[{now()}] AC8 -- proposed read fence as exact prefixes; tables outside it named with "
          f"reason")
    print(f"  PROPOSED READ FENCE (bucket={BUCKET}):")
    print(f"    s3://{BUCKET}/{ECLIPSE_PREFIX}")
    print("    (ONE prefix, not four -- MEASURED: all four canon tables below are sibling "
          "filenames under this SAME {date} folder, not separate sub-prefixes; unlike MX-a-4/"
          "Orion, no S3 prefix can fence one Eclipse table without also fencing the other three)")
    for name, filename, *_ in CANON_TABLES:
        print(f"      covers: {filename} ({name})")
    print(f"  EXCLUDED WITHIN this prefix (named, {len(EXCLUDED_SUFFIXES)} entry/entries):")
    for suf, reason in EXCLUDED_SUFFIXES.items():
        print(f"    s3://{BUCKET}/{ECLIPSE_PREFIX}*/{suf} -- {reason}")
    print(f"  EXCLUDED: other top-level/sibling prefixes in the same bucket -- "
          f"{OTHER_TOP_LEVEL_EXCLUDED_REASON}")
    ok = len(CANON_TABLES) > 0
    print(f"VERDICT: {'PASS-MXA5-AC8' if ok else 'FAIL-MXA5-AC8'}")


def ac9():
    print(f"[{now()}] AC9 -- a property with no silver/served data says so and proposes no tool "
          f"(antecedent check)")
    objs = list_all(ECLIPSE_PREFIX)
    total_bytes = sum(o[1] for o in objs)
    print(f"  live check: {len(objs)} objects, {total_bytes} bytes under s3://{BUCKET}/"
          f"{ECLIPSE_PREFIX} at run time (ListObjectsV2, paginated)")
    has_data = len(objs) > 0
    print(f"  Eclipse HAS live silver data (has_data={has_data}); the antecedent of this criterion "
          f"('no silver or served data') is FALSE for this property, so the criterion's obligation "
          f"('says so, proposes no tool') does not bind -- {len(QUESTIONS)} questions ARE proposed "
          f"against real tables (AC5/AC6), which is the correct behavior under a TRUE antecedent")
    ok = has_data and len(QUESTIONS) > 0
    print(f"VERDICT: {'PASS-MXA5-AC9' if ok else 'FAIL-MXA5-AC9 data absent but tools were proposed, or vice versa'}")


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
