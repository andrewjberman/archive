# ADVI_INFFEE TO-1 AUDIT -- billing-dim coverage + fee/non-fee grain

**Owner:** 0.6.1_AE_PartnerETL (partner-ETL billing-domain lane)
**Date:** 2026-07-06
**Gates:** ADVI_INFFEE.TO-2 (DS~A gold revise) grain choice; CTO arch-gate on TO-2.
**Grounding:** live inf S3 artifacts @ 07-06 16:00Z fresh nightly + served platinum @ 16:59Z + source (`build_billing_dim.py`, `INF_D_04.client_portal_summary.py`). Rule-22: mechanism source+data-confirmed, not inferred.

---

## 0. Headline (the load-bearing corrections)

The PRD/DE-brief numbers (868 custody / 790 billing / **78 custody accts with NO billing row** / $67M-in-1-non-fee) came from the **stale 07-06 12:55Z build**. Re-grounded against the **fresh 07-06 16:00Z nightly** (produced by today's un-freeze), two PRD premises are **factually overturned**:

1. **The "78" is a HOLDINGS gap, NOT a billing-coverage gap.** Every account that holds positions already has a billing row (`holdings - billing = 0`). The 78 = **868 account-master minus 790 funded (holdings) accounts = 78 active accounts holding $0**.
2. **The ~$47M is NEITHER "fee-earning-but-unbilled" NOR "genuinely non-fee."** The 78 gap accounts hold **$0** (not $47M). The $67M "non_fee_earning_aua" residual is a **cross-source valuation artifact**: **$61.1M** = 268 real fee-earning accounts whose `billing.ending_mv` is **blank/$0 in the Orion feed** + **$5.9M** = the genuine positively-measured non-fee. ($61.1M + $5.9M = $67.0M, matches served $67,001,038.85 exactly.)

**New root cause the PRD missed (the real mechanism):** `fee_earning_aua` is sourced from `billing.ending_mv`, which the Orion Billing Dim export returns **blank for 268 of 711 funded fee accounts** (with `Included In Billing and Fees = "Error:Not supported"`). The fee-AUA numerator must move to `holdings.market_value`; the billing `is_fee_earning` *flag* stays as the classifier.

---

## 1. The three (four) account universes -- live, 07-06

| Universe | Source artifact | Count | Meaning |
|---|---|---|---|
| **A -- account master** | `silver/api_dims/accounts_v2` (all `is_active=True`, "Normal Downloading") | **868** | every open Inflection account |
| **H -- holdings (funded)** | `gold/canonical/holdings_2026-07-06.parquet` | **790** | accounts holding positions; SUM(market_value)=**$202,542,849.81** = canonical total_aua |
| **B -- billing** | `silver/api_dims/billing` (07-06 snapshot) | **890** | accounts with a billing row (789 `is_fee_earning` / 101 not) |
| **Bf -- fee-billed** | subset of B | **789** | positively fee-flagged |

Set algebra (live):
```
A - H (master, NO holdings)   = 78   <- THE "78" (zero-value active accts)
H - A                         = 0    (every funded acct is in the master)
H - B (holdings, NO billing)  = 0    (every funded acct IS billed)
A - B (master, NO billing)    = 31   (all 31 are inside the zero-value 78)
Bf - H (fee-billed, no hold)  = 78
```

## 2. Q1 -- WHY the 78 have no [holdings] row (corrected question)

The 78 = **868 master - 790 funded**. Characterized (accounts_v2):
- **All 78 hold current_value = $0** (78/78; median $0; none > $0) and have **zero canonical holdings**.
- All `is_managed=True`, `is_trading_blocked=False`, status "Normal Downloading".
- Real retail registrations: 28 IRA, 15 Joint, 14 Beneficiary IRA, 9 Transfer-on-Death, 5 Roth, 4 SEP, 1 IRA Rollover, 1 Simple.
- Opened 2020-06-04 .. 2026-05-05 -- **none in the last 30 days** (so NOT "newly opened, not-yet-funded").
- Billing coverage of the 78: **45 still fee-billed** (carrying ~$85,852 residual `fee_amount` on $0 ending-MV), 2 non-fee-billed, **31 with no billing row**.

**Cause:** these are **emptied / fully-withdrawn / transferred-out accounts still flagged active** in the Orion account master. They are an operational **open-but-zero-balance** population, not a billing feed gap. The PRD's "78 custody accts with no billing row" mis-attributed a holdings-gap to a billing-gap because it compared the master count (868) against a *stale* billing count (790 @ 12:55Z; billing is now 890).

## 3. Q2 -- is the ~$47M fee-earning-but-unbilled or genuinely non-fee?

**NEITHER. The premise ($47M hiding in the gap) is false.** The 78 gap accounts hold **$0**. The served `non_fee_earning_aua = $67,001,038.85` decomposes **exactly**:

| Component | Amount | What it actually is |
|---|---|---|
| Billing `ending_mv` blank for real fee accts | **$61,098,206** | 268 funded, `is_fee_earning=True` accounts whose Orion billing `Activity: Ending Market Value` is **blank/NaN** (feed returns `Included In Billing = "Error:Not supported"` for 253 of them). They carry valid "Inflection" fee schedules + real `fee_amount` -> genuinely **fee-earning**, mis-valued to $0 by the billing column. |
| Genuine non-fee | **$5,902,832** | 79 funded accounts positively marked `is_fee_earning=False`. |
| **Total** | **$67,001,038** | = served residual. |

Mechanism grounded: 443 of 711 funded fee accounts have `billing.ending_mv` within 1% of `holdings.market_value` (median ratio 1.000); the other 268 are **exactly** the ones with blank bronze Ending-MV. The residual `total_aua(holdings) - fee_aua(billing.ending_mv)` therefore misattributes $61.1M of **fee-earning** AUA into "non-fee."

**Verdict:** the true genuine non-fee AUA is **$5.9M / 79 accounts** -- even below the code's anticipated $19.6M. There is **no unbilled fee-earning AUA to recover**; there IS a billing-column-valuation defect to route around.

## 4. Q3 -- RECOMMENDED canonical grain

**Grain = HOLDINGS (790, the funded / AUA-bearing universe). Positively measured, valued from holdings.market_value.**

```
fee-earning:   711 accts | $196,640,017.10   (holdings.market_value; classified by billing.is_fee_earning)
non-fee:        79 accts | $  5,902,832.71
unbilled:        0 accts | $          0.00
------------------------------------------------
TOTAL:         790 accts | $202,542,849.81    (= canonical total_aua, reconciles EXACTLY on count AND AUA)
```

Rules for TO-2 (informing its implementation):
1. **Classify by `billing.is_fee_earning` (reliable flag); VALUE by `holdings.market_value` (NOT `billing.ending_mv`, which is $0 for 268 real fee accts).** This is the single most important fix -- it kills the $61.1M artifact at the source.
2. **Non-fee POSITIVELY measured** = SUM(holdings.market_value WHERE account in billing AND NOT is_fee_earning). Never `total_aua - fee_aua`.
3. **`fee + non_fee = 790 = total` on both count and AUA. No residual, no clip, no `residual_clipped_pending_canonical_rerun` flag.**
4. **"868 total open accounts"** = a SEPARATELY-LABELED operational stat (account master incl. 78 zero-balance), shown outside the fee/non-fee=total identity -- never stitched into the same reconciling row (this is the Books-868-vs-Distribution-790 disagreement; both should render the funded 790 for the fee-split, with 868 labeled "open accounts incl. zero-balance").

This refines the PRD's Option 1 (custody-868 grain + unclassified bucket): a 78-account "unclassified" bucket would carry **$0 AUA**, which is honest-but-misleading as a "bucket." The funded-790 grain makes fee+non-fee=total hold on **both** axes, and relegates the zero-value 78 to a labeled count.

## 5. Lane notes / out-of-scope

- **49F / INF_C_08 residual check (AC5):** 49F is a **bd-pipeline (separate firm)** concern -- out of my INF partner-ETL lane (CLAUDE.md firm-separation rule; never cross bd<->inf). The CTO source-check already established 49F/`D_00c` uses a positive tagged-role invariant (not a cross-grain residual). Deferred to TO-2 / the bd owner; I do NOT touch 49F artifacts. Flagged, not actioned.
- The billing `ending_mv=blank` / `Included In Billing = "Error:Not supported"` is an **Orion feed limitation**, not a `build_billing_dim.py` bug -- the silver builder faithfully parses blank->$0 and correctly derives `is_fee_earning` via its documented fee-schedule workaround. **No silver fix is required in my lane** for the grain defect; the fix is the gold-side value-source change (TO-2). (A separate, optional robustness item: `build_billing_dim` could carry a `billing_mv_missing` flag so gold can see the 268 explicitly -- offered to TO-2 if useful, not required.)

## 6. Evidence index (reproducible)

- Set algebra + characterization: `scratchpad/inffee_setalgebra.py` (868/790/890; A-H=78 all $0; 268 blank-emv).
- Valuation decomposition: `scratchpad/inffee_period2.py` ($196.6M holdings vs $135.5M billing for 711 fee accts; 268 emv=0 = $61.1M; 443 within 1%).
- Bronze attribution: `scratchpad/inffee_bronze.py` (268/268 bronze Ending-MV blank; 253 "Error:Not supported"; valid Inflection fee schedules + fee_amounts).
- Served reconcile: `scratchpad/inffee_reconcile.py` (header_metrics 790/789/1/$67.0M; clients_tab 868/300; accounts_v2 868 all active).
- comp-freshness inf: `inf_orion_api_billing` PASS 5.4h (feed fresh -> gap is structural, not stale-feed masquerade).
- Source: `data/inf/scripts/silver/build_billing_dim.py`, `data/inf/scripts/gold/INF_D_04.client_portal_summary.py:714-812,819-828,1200-1250`.
