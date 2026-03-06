#!/usr/bin/env python3
"""
PHASE 1: Data Collection & Verification — BD vs Model vs Schwab (3/4/2026)

Pull exact totals from:
1. BD allocations for 3/4/2026 (file: 2026-03-03.parquet)
2. Our gold layer client_performance for 3/4/2026
3. Schwab reported figure (known: $1.510B)

Then validate with:
- Row counts, unique accounts
- Duplicate detection
- Column inspection
"""

import pandas as pd
from io import BytesIO
import boto3
import sys

s3 = boto3.client("s3", region_name="us-east-1")
BUCKET = "opal-data-bd"

print("="*100)
print("PHASE 1: DATA COLLECTION & VERIFICATION")
print("Target date: 3/4/2026 (Schwab reported yesterday)")
print("="*100)

# ============================================================================
# SECTION 1: BD ALLOCATIONS (2026-03-03.parquet = 3/4/2026 data)
# ============================================================================

print("\n" + "-"*100)
print("SECTION 1: BD ALLOCATIONS")
print("-"*100)

allocation_key = "silver/allocations/2026-03-03.parquet"
print(f"\nLoading: s3://{BUCKET}/{allocation_key}")

try:
    resp = s3.get_object(Bucket=BUCKET, Key=allocation_key)
    bd_alloc = pd.read_parquet(BytesIO(resp['Body'].read()))
    print(f"OK: Loaded successfully")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# Identify AUA column - prioritize account-level values over portfolio group aggregates
numeric_cols = bd_alloc.select_dtypes(include=["number"]).columns.tolist()
aua_col = None
for col in ['account_market_value', 'market_value', 'total_value', 'total_market_value', 'aua', 'balance', 'current_value']:
    if col in bd_alloc.columns:
        aua_col = col
        break
if not aua_col:
    aua_col = max(numeric_cols, key=lambda x: bd_alloc[x].sum())

bd_total = bd_alloc[aua_col].sum()

print(f"\n[BD ALLOCATIONS]")
print(f"  Total rows:              {len(bd_alloc):,}")
print(f"  AUA column used:         {aua_col}")
print(f"  Total AUA:               ${bd_total:,.2f}")
print(f"  Total AUA (billions):    ${bd_total/1e9:.3f}B")

if 'account_id' in bd_alloc.columns:
    unique_accts = bd_alloc['account_id'].nunique()
    print(f"  Unique account_ids:      {unique_accts:,}")
    print(f"  Rows per account (avg):  {len(bd_alloc)/unique_accts:.2f}")

if 'as_of_date' in bd_alloc.columns:
    dates = pd.to_datetime(bd_alloc['as_of_date'], errors='coerce')
    print(f"  as_of_date range:        {dates.min()} to {dates.max()}")
    print(f"  Unique dates:            {dates.nunique()}")

# Check for duplicates
if 'account_id' in bd_alloc.columns:
    dupes = bd_alloc[bd_alloc.duplicated(subset=['account_id'], keep=False)]
    if len(dupes) > 0:
        unique_acct_count = len(dupes['account_id'].unique())
        print(f"  WARN: DUPLICATES: {len(dupes)} rows, {unique_acct_count} accounts")
    else:
        print(f"  OK: No duplicates on account_id")

# Check for cash
if 'security_name' in bd_alloc.columns:
    cash_mask = bd_alloc['security_name'].str.contains('cash|money market|sweep', case=False, na=False)
    if cash_mask.any():
        cash_total = bd_alloc[cash_mask][aua_col].sum()
        print(f"  Cash/MM positions:       ${cash_total:,.2f} ({(cash_total/bd_total)*100:.1f}%)")

print(f"\n  - BD TOTAL: ${bd_total:,.2f}")

# ============================================================================
# SECTION 2: OUR GOLD LAYER (client_performance for date 2026-03-04)
# ============================================================================

print("\n" + "-"*100)
print("SECTION 2: OUR GOLD LAYER (client_performance)")
print("-"*100)

# Note: client_performance is a merged table, not daily partitions
# We need to filter to the target date

print("\nLoading: s3://opal-data-bd/gold/client_performance.parquet")
try:
    resp = s3.get_object(Bucket=BUCKET, Key="gold/client_performance.parquet")
    client_perf = pd.read_parquet(BytesIO(resp['Body'].read()))
    print(f"OK: Loaded successfully")
except Exception as e:
    print(f"ERROR: Error loading client_performance: {e}")
    # Try legacy path
    try:
        resp = s3.get_object(Bucket=BUCKET, Key="silver/daily_aua_firm.parquet")
        client_perf = pd.read_parquet(BytesIO(resp['Body'].read()))
        print(f"OK: Loaded from legacy path (daily_aua_firm.parquet)")
    except Exception as e2:
        print(f"ERROR: Error loading legacy path: {e2}")
        sys.exit(1)

# Filter to target date
if 'date' in client_perf.columns:
    client_perf['date'] = pd.to_datetime(client_perf['date'], errors='coerce')
    target_date = pd.to_datetime('2026-03-04')
    cp_target = client_perf[client_perf['date'] == target_date]
    print(f"\nDate filter: 2026-03-04")
    print(f"  Rows matching target date: {len(cp_target):,}")

    if len(cp_target) == 0:
        print(f"  WARN: No rows for exact date. Trying closest date...")
        available_dates = client_perf['date'].dropna().unique()
        available_dates = sorted(available_dates)
        closest = available_dates[-1]
        print(f"     Closest available: {closest}")
        cp_target = client_perf[client_perf['date'] == closest]
        target_date = closest
else:
    print(f"  Note: no 'date' column, using all data")
    cp_target = client_perf

# Identify AUA column — total_aua is market value; nna is cumulative flows (NOT AUA)
numeric_cols_cp = cp_target.select_dtypes(include=["number"]).columns.tolist()
aua_col_cp = None
for col in ['total_aua', 'aua', 'market_value', 'total_value']:
    if col in cp_target.columns:
        aua_col_cp = col
        break
if not aua_col_cp:
    aua_col_cp = max(numeric_cols_cp, key=lambda x: cp_target[x].sum())

our_total = cp_target[aua_col_cp].sum() if len(cp_target) > 0 else 0

print(f"\n[OUR GOLD LAYER]")
print(f"  Target date:             {target_date}")
print(f"  Total rows (at date):    {len(cp_target):,}")
print(f"  AUA column used:         {aua_col_cp}")
print(f"  Total AUA:               ${our_total:,.2f}")
print(f"  Total AUA (billions):    ${our_total/1e9:.3f}B")

if 'relationship_id' in cp_target.columns:
    unique_rels = cp_target['relationship_id'].nunique()
    print(f"  Unique relationships:    {unique_rels:,}")

print(f"\n  - OUR MODEL TOTAL: ${our_total:,.2f}")

# ============================================================================
# SECTION 3: SCHWAB REPORTED (known value)
# ============================================================================

print("\n" + "-"*100)
print("SECTION 3: SCHWAB REPORTED")
print("-"*100)

schwab_total = 1_510_000_000

print(f"\n[SCHWAB REPORTED]")
print(f"  Date:                    2026-03-04 (from CEO report)")
print(f"  Source:                  49 Financial Business Review Dashboard")
print(f"  Total AUA:               ${schwab_total:,.2f}")
print(f"  Total AUA (billions):    ${schwab_total/1e9:.3f}B")
print(f"\n  - SCHWAB TOTAL: ${schwab_total:,.2f}")

# ============================================================================
# SECTION 4: GAP ANALYSIS
# ============================================================================

print("\n" + "="*100)
print("SECTION 4: GAP ANALYSIS")
print("="*100)

bd_to_schwab = bd_total - schwab_total
model_to_schwab = our_total - schwab_total
bd_to_model = bd_total - our_total

print(f"\n[RAW GAPS]")
print(f"  BD to Schwab:            ${bd_to_schwab:>+15,.2f}  ({(bd_to_schwab/schwab_total)*100:>+6.2f}%)")
print(f"  Our Model to Schwab:     ${model_to_schwab:>+15,.2f}  ({(model_to_schwab/schwab_total)*100:>+6.2f}%)")
print(f"  BD to Our Model:         ${bd_to_model:>+15,.2f}  ({(bd_to_model/our_total)*100:>+6.2f}%)")

print(f"\n[RECONCILIATION]")
print(f"""
  BD Allocations:   ${bd_total:>15,.2f}
  Our Model:        ${our_total:>15,.2f}  (-${abs(bd_to_model):>15,.0f})
  Schwab:           ${schwab_total:>15,.2f}  (-${abs(model_to_schwab):>15,.0f})

  KEY INSIGHT:
  Our model is ${abs(bd_to_model):,.0f} BELOW BD but only ${abs(model_to_schwab):,.0f} ABOVE Schwab.
  This suggests we're applying ~${abs(bd_to_model):,.0f} in filters/adjustments
  that bring us closer to Schwab's number.
""")

# ============================================================================
# SECTION 5: NEXT PHASE RECOMMENDATIONS
# ============================================================================

print("\n" + "="*100)
print("SECTION 5: PHASE 2 READY")
print("="*100)

print(f"""
OK: Phase 1 Complete. Ready to proceed with Phase 2.

Confirmed numbers for investigation:
  - BD allocations: ${bd_total:,.2f}
  - Our model: ${our_total:,.2f}
  - Schwab: ${schwab_total:,.2f}

Next: Execute Phase 2 hypothesis tracks in parallel:
  A. Pricing differences (top 20 holdings)
  B. Deduplication completeness
  C. Settlement/pending trades

Estimated time: 60 minutes
""")

print("="*100)
