"""PRF-a-2 -- COMPONENT TIE-OUT (ADVI_PERFRP TO-R1-DS, AC3, the assertion that CAN fail).

WHY A TIE-OUT AND NOT THE IDENTITY
----------------------------------
The identity AC3 names cannot fail: market_growth is the residual, so the check
reduces to d_aua - d_aua. Proven by mutant at @a84a8ca770 (6 of 6 mutants passed,
including total garbage). So the identity is not where correctness lives.

Correctness lives in whether each COMPONENT equals an INDEPENDENTLY-SOURCED figure.
This file ties the two fee/income taxonomies that the projection must reconcile:

  A. THE GAINS CORE'S taxonomy -- dim_transaction.sb_cd, amounts resolved by the
     core's OWN resolve_flow_amount (gross_amount magnitude x debit_credit sign).
     SB_INCOME = {DV, IN} ; SB_FEES_TAX = {FE, WH, WD}.
  B. THE CONTRACT'S netting taxonomy -- flow_ledger.final_class, per COO 66841.
     FEE-MANAGEMENT / FEE-ADMIN / EXTERNAL / INTERNAL / UNRESOLVED.

CORES ARE IMPORTED, NEVER COPIED (Build Ladder rung 2; the estate's copied-taxonomy
drift is a named defect class, and c00's own docstring imports build_nna_atomic for
exactly this reason). This file imports SB_INCOME, SB_FEES_TAX and
resolve_flow_amount rather than restating any of them -- so if the core's taxonomy
moves, this tie-out moves with it instead of silently disagreeing.

A CORRECTION THIS FILE EXISTS TO NOT REPEAT
----------------------------------------------
My first attempt summed `flow_ledger.signed_amount` grouped by `flow_ledger.sb_cd`
and reported a large dollar gap. THAT MEASUREMENT WAS INVALID and is withdrawn:
resolve_flow_amount requires `gross_amount` + `debit_credit`, which flow_ledger does
NOT carry, and on flow_ledger the DV (dividend) rows carry 0.00 in signed_amount --
so the income figure it produced was a sum over a field the core never reads.
Right question, wrong table, clean-looking answer. The row-level taxonomy divergence
survived that correction; the dollar quantification did not, and is re-derived here
from the table the core actually uses.
"""
from __future__ import annotations

import io
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3
import pandas as pd
import pyarrow.parquet as pq

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
from c00_account_gains import SB_FEES_TAX, SB_INCOME  # noqa: E402  IMPORTED, never copied
from c03_nna import resolve_flow_amount  # noqa: E402  the core's OWN amount resolver

ASSETS = "opal-data-assets"
GOLD = "opal-data-49financial"
DIM_TXN = "schwab/08335338/silver/dim_transaction/"
FLOW = "gold/advi/canonical/flow_ledger/"

s3 = boto3.client("s3")


def partitions(bucket, prefix):
    p = s3.get_paginator("list_objects_v2")
    out = set()
    for pg in p.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for c in pg.get("CommonPrefixes", []) or []:
            seg = c["Prefix"].rstrip("/").split("/")[-1]
            if seg.startswith("date="):
                out.add(seg.split("=", 1)[1])
    return sorted(out)


def _read(bucket, prefix, d):
    r = s3.list_objects_v2(Bucket=bucket, Prefix=f"{prefix}date={d}/")
    keys = [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".parquet")]
    if not keys:
        return None
    o = s3.get_object(Bucket=bucket, Key=keys[0])
    return pq.read_table(io.BytesIO(o["Body"].read())).to_pandas()


def core_side(d):
    """Income + fees_tax the way c00_account_gains does it, using its OWN resolver."""
    t = _read(ASSETS, DIM_TXN, d)
    if t is None or t.empty:
        return d, 0.0, 0.0, 0, None
    sb = t["sb_cd"].fillna("").astype(str).str.strip().str.upper()
    m_inc = sb.isin(SB_INCOME)
    m_fee = sb.isin(SB_FEES_TAX)
    if not bool((m_inc | m_fee).any()):
        return d, 0.0, 0.0, len(t), None
    try:
        signed = resolve_flow_amount(t, m_inc | m_fee)
    except Exception as e:  # the resolver REFUSES LOUD by design; record, never fabricate
        return d, None, None, len(t), f"{type(e).__name__}: {e}"
    income = float(signed[m_inc].sum())
    fees_tax = float(-signed[m_fee].sum())  # identity's "- fees_tax" wants the magnitude
    return d, income, fees_tax, len(t), None


def contract_side(d):
    """Fee buckets the way the contract's netting does it, from flow_ledger.final_class."""
    t = _read(GOLD, FLOW, d)
    if t is None or t.empty:
        return d, 0.0, 0.0
    fc = t["final_class"].fillna("").astype(str)
    amt = pd.to_numeric(t["signed_amount"], errors="coerce").fillna(0.0)
    return (d,
            float(-amt[fc.eq("FEE-MANAGEMENT")].sum()),
            float(-amt[fc.eq("FEE-ADMIN")].sum()))


def main() -> int:
    ds_txn = partitions(ASSETS, DIM_TXN)
    ds_flow = partitions(GOLD, FLOW)
    common = sorted(set(ds_txn) & set(ds_flow))

    print("PRF-a-2 COMPONENT TIE-OUT -- ADVI_PERFRP TO-R1-DS (AC3)")
    print("=" * 100)
    print("DENOMINATORS (printed before any figure, per Rule 22):")
    print("  dim_transaction partitions .......... %d  (%s..%s)" % (len(ds_txn), ds_txn[0], ds_txn[-1]))
    print("  flow_ledger     partitions .......... %d  (%s..%s)" % (len(ds_flow), ds_flow[0], ds_flow[-1]))
    print("  COMMON dates (the tie-out domain) ... %d" % len(common))
    print("  dim_transaction-only ................ %d" % len(set(ds_txn) - set(ds_flow)))
    print("  flow_ledger-only .................... %d" % len(set(ds_flow) - set(ds_txn)))
    print("  cores IMPORTED: SB_INCOME=%s SB_FEES_TAX=%s resolve_flow_amount=%s"
          % (sorted(SB_INCOME), sorted(SB_FEES_TAX), resolve_flow_amount.__module__))

    with ThreadPoolExecutor(16) as ex:
        core = list(ex.map(core_side, common))
        cont = list(ex.map(contract_side, common))

    refused = [(r[0], r[4]) for r in core if r[4]]
    refused_dates = {d for d, _ in refused}
    # DENOMINATOR ALIGNMENT. The resolver REFUSES LOUD on some partitions, so side A
    # covers fewer dates than side B. Summing each over its own domain and differencing
    # them compares two different populations -- a gap that is partly just the missing
    # dates. BOTH sides are therefore restricted to the SAME comparable domain, and the
    # excluded dates are reported rather than silently dropped.
    comparable = [d for d in common if d not in refused_dates]
    c_income = sum(r[1] for r in core if r[1] is not None and r[0] in set(comparable))
    c_fees = sum(r[2] for r in core if r[2] is not None and r[0] in set(comparable))
    k_fm = sum(r[1] for r in cont if r[0] in set(comparable))
    k_fa = sum(r[2] for r in cont if r[0] in set(comparable))
    # what side B alone would have said over the FULL domain, to size what exclusion costs
    k_fm_all = sum(r[1] for r in cont)
    k_fa_all = sum(r[2] for r in cont)

    print("\nA. GAINS-CORE TAXONOMY (dim_transaction.sb_cd, core's own resolver):")
    print("   income    sb_cd in {:<12} ....... {:>18,.2f}".format(str(sorted(SB_INCOME)), c_income))
    print("   fees_tax  sb_cd in {:<12} ....... {:>18,.2f}".format(str(sorted(SB_FEES_TAX)), c_fees))
    print("   partitions where the resolver REFUSED LOUD: %d" % len(refused))
    for d, why in refused[:5]:
        print("      %s  %s" % (d, why[:90]))

    print("\nB. CONTRACT NETTING TAXONOMY (flow_ledger.final_class, COO 66841):")
    print("   fees_management  FEE-MANAGEMENT ......... {:>18,.2f}".format(k_fm))
    print("   fees_admin       FEE-ADMIN .............. {:>18,.2f}".format(k_fa))
    print("   fees total       FM + FA ................ {:>18,.2f}".format(k_fm + k_fa))
    print("   [for scale only, side B over the FULL {} dates: {:,.2f} -- NOT used in the gap]"
          .format(len(common), k_fm_all + k_fa_all))

    print("\n" + "=" * 100)
    gap = (k_fm + k_fa) - c_fees
    print("TIE-OUT: contract fees (B) vs core fees_tax (A)")
    print("   B - A = {:,.2f}".format(gap))
    if abs(k_fm + k_fa) > 0:
        print("   A covers %.2f%% of B's magnitude" % (100 * abs(c_fees) / abs(k_fm + k_fa)))
    print("\n   THESE ARE NOT THE SAME QUANTITY, and the projection must not substitute one")
    print("   for the other. 'fees_tax' in the AUA identity is fees + tax withholding on the")
    print("   sb_cd axis; 'fees_management' on the client card is the advisory fee on the")
    print("   final_class axis. A client-facing Management Fees figure sourced from the")
    print("   identity's fees_tax term would be WRONG BY THE GAP ABOVE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
