# ADVI_BDPARITY P1-PROBE -- rider-4 COHORT CANDIDATES (input to CRO's selection, not a selection)

**Author:** `0.4.0_DS_ClientPlatform~C` -- 2026-08-29 ~18:4xZ. **Status: CANDIDATES ONLY.**
**Pre-registration rider 4 puts probe account selection at `4.0.0_SA_CRO` methodology.** This file
supplies the evidence that selection needs and stops there. Nothing here is a chosen probe set, and
no probe has been fired -- a live BD pull is vendor egress and is held as P1's gate.

**Why it exists:** rider 4 asks for "at least one fee-bearing account off-quarter (C2), one
multi-security account with fixed income (C3), and -- if in the 49F population -- a
Mitch-Johnson-case account (C4)", and the 08-19 amendment adds an income-bearing fixed-income
account so C5 separates. Selecting against those cohorts requires knowing which accounts HAVE those
properties. That was unmeasured.

---

## 1. THE CONSTRAINT THAT SHOULD DRIVE SELECTION: THE C5 COHORT IS TINY

Measured on `canonical_positions` `date=2026-08-28` (6,185 accounts carrying positions):

| population | count | of 6,185 |
|---|---|---|
| holds **>= 1 rate-bearing position** | **38** | 0.61% |
| `rb_share` (rate-bearing MV / total MV) **> 0.20** | **8** | 0.13% |
| `rb_share` **> 0.50** | **7** | 0.11% |

**This is the single most consequential number in this file and it is not a P1 fact, it is a P2
fact.** C5 is the valuation-accrual-basis convention, and only 38 accounts in the whole population
can express it. A census that reports "C5: N accounts" without this denominator invites the reading
that C5 is rare because the convention rarely bites, when the truth is that almost nothing in the
book is rate-bearing. **The C5 class denominator is 38, not 6,185, and the census must print it.**

`rate_bearing` also carries **39 NULL** rows on that date. They are counted as neither True nor
False here and are named rather than folded into False -- an unknown is not a negative.

---

## 2. THE PRE-NAMED C5 SPECIMEN IS CORROBORATED FROM A SECOND INSTRUMENT

Pre-registration Addendum A3 item 4 named account **...2917** as the C5 rider specimen, selected by
`4.0.0_SA_CRO~A` on **largest accrual ($22.47K)**.

Measured here independently, on position composition rather than on accrual:

```
  schwab 0022312917  ->  bd_account_id z0813477111  ->  bd_internal_id 13477111   (xref tier-1)
  n_positions 2 | rate-bearing 1 | rb_share 0.8982 | mv_total $790,249.11
```

**89.8% of its market value is rate-bearing.** That is corroboration and not repetition: CRO~A
selected on the accrual quantity, this reads position composition, and the two derivations do not
share an input. **The specimen is also BD-addressable with zero egress** -- the tier-1 xref
fast-path resolves it, so it needs no roster enrolment.

---

## 3. CANDIDATE TABLE

Window: **37 `twr_daily` partitions, 2026-07-01..2026-08-28.** Positions as of **2026-08-28**.
`bd_internal_id` derived by the tier-1 rule (`taxsma_resolver` -- `int(bd_account_id[3:])`), so
every row below is pullable without a resolution egress.

| cohort | account | bd_internal_id | fee_days | flow_days | n_pos | rate_bearing | rb_share | mv_total | days_ok |
|---|---|---|---|---|---|---|---|---|---|
| **C5 (pre-named)** | 0022312917 | 13477111 | 2 | 0 | 2 | 1 | 0.8982 | 790,249.11 | 36 |
| C5-alt | 0079954642 | 14052861 | 3 | 0 | 21 | 20 | 0.9402 | 499,496.60 | 36 |
| C5-alt | 0056652077 | 12889441 | 2 | 3 | 21 | 1 | 0.8420 | 356,059.13 | 36 |
| C5-alt | 0058177364 | 14294421 | 2 | 1 | 19 | 1 | 0.6226 | 8,128.89 | 36 |
| C3 multi-security + FI | 0038836097 | 18927251 | 2 | 4 | 80 | 1 | 0.0694 | 22,913,948.45 | 36 |
| C3 multi-security + FI | 0020919976 | 13358001 | 2 | 3 | 46 | 4 | 0.0114 | 12,745,547.37 | 36 |
| C3 multi-security + FI | 0080410420 | 13092251 | 2 | 0 | 24 | 2 | 0.0247 | 206,033.94 | 36 |
| C2 fee, no flows | 0010066510 | 12898101 | 1 | 0 | 15 | 0 | 0.0000 | 57,773.25 | 36 |
| C2 fee, no flows | 0010083855 | 21089351 | 2 | 0 | 15 | 0 | 0.0000 | 172,732.71 | 36 |
| flows, fee-bearing | 0045774644 | 21929881 | 1 | 15 | 13 | 0 | 0.0000 | 1,075,699.42 | 36 |

**`0079954642` is arguably the stronger C5 specimen than the pre-named one** -- 20 rate-bearing
positions at `rb_share` 0.9402 versus 1 at 0.8982, so an accrual delta decomposes across holdings
instead of resting on a single bond. **That is CRO's call and not mine**, and the pre-named specimen
is listed first because it is the one already registered.

### Rows deliberately WITHHELD from the table

Three otherwise-qualifying candidates (`0099965452`, `0065688849`, `0097064646`) appear in
`twr_daily` but carry **NO row in `canonical_positions` on 2026-08-28**, so their composition is
uncharacterised and their C3/C5 cohort membership is unknown rather than zero. They are excluded
from the recommendation and named here instead of silently dropped. **That gap is itself a
P2-relevant observation** -- an account present in the return plane and absent from the position
plane -- and it is surfaced, not chased.

---

## 4. POPULATION DENOMINATORS (window 2026-07-01..2026-08-28)

| | count |
|---|---|
| accounts in `twr_daily` | 7,441 |
| BD-addressable via xref (`seed-xref`, 1:1) | 5,351 |
| fee-bearing (>= 1 fee-management day) | 6,193 |
| flow-bearing (>= 1 external-flow day) | 1,510 |
| **no external flows at all** | **5,931** |
| holds >= 1 rate-bearing position | 38 |
| first seen after the window opened (inception-recent PROXY) | 356 |

**The "no-flows" cohort is the overwhelming majority (5,931 of 7,441), not a hard-to-find case.**
The scarce cohorts are flows (1,510) and rate-bearing (38). Rider 4's diversity ask is therefore
easy on three axes and binding on one.

⚠ **`first_seen` is a WINDOW-BOUNDED PROXY, NOT AN INCEPTION.** It is the earliest date an account
appears in the 37 partitions loaded here; an account trading since 2024 and one opened on 2026-07-01
both read `first_seen = 2026-07-01`. **The 356 figure is an upper bound on inception-recent accounts
within this window and says nothing about the other 7,085.** A real inception needs either the
TaxSMA roster's `trade_start_date` (3 active accounts have one) or a first-appearance sweep over all
535 partitions, which this pass did not run. **Do not select the "inception-recent" rider member off
this column.**

---

## 5. BOUNDS -- what this file does NOT establish

1. **No C4 candidate is identified.** C4 is the BD-vs-Schwab source-divergence case and its live
   named instance is Mitch Johnson's book. **Nothing in our gold carries that mapping**, and rider 4
   itself hedges it ("if in the 49F population"). Identifying a C4 account needs the 49F-side
   contact, not a query.
2. **Composition is a ONE-DATE read** (2026-08-28). An account that held fixed income earlier in the
   window and does not today reads as non-rate-bearing here.
3. **`fee_days` counts days where `cf_gross != cf_net`**, which the identity
   `r_net - r_gross == (cf_gross - cf_net)/bmv` proves is exactly a fee-management flow day
   (11,705/11,705, max residual 4.4e-16; negative control: 214,930/214,930 non-fee days have
   `r_net == r_gross` exactly). It is a fee-EVENT count, not a fee-magnitude measure.
4. ⛔ **RESOLVED 2026-08-29 ~21:0xZ, AND IT RESOLVED AGAINST THE CURRENT SIGN. THIS CLAUSE WAS A
   CONDITIONAL WHEN WRITTEN AND IS NOW A FACT.** I filed the gross leg as an OPEN OBSERVATION
   (msg 83549-51): our `r_gross` is arithmetically LOWER than `r_net` by the fee rate on every fee
   day, where gross-of-fee must be higher. **`2.0.0_SA_COO` has since ruled outcome (a) CODE WRONG**
   on `ADVI_49F.c02-GROSSLEG`, against a RATIFIED spec rather than a reading:
   `SPEC_49F_GROUP_C_TWR_ENGINE_20260811.md:34` @`bfaa0a6e6e`, row `C_02`, verbatim
   *"gross adds back FEE-MANAGEMENT (VERIFIED family: MGFEE/TPFEE/SMFEE)"*. My own bound at filing
   ("I have NOT established intent") is discharged by that citation.
   ⛔ **CONSEQUENCE FOR THIS FILE, STATED SO NOBODY BUILDS A C2 TEST ON IT: the C2 cohort picks
   below stay valid, and the C2 TEST DOES NOT.** Prereg C2's classifier is *"compare gross-of-fee
   FIRST"*, and the gross leg is inverted across the whole 534-date history. **The fix does not
   retro-correct the data** -- COO's ruling explicitly authorizes NO re-emission and NO backfill, so
   **a C2 parity cell computed against today's stored `r_gross` would be inverted before it was
   classified.** C2 waits on a corrected leg reaching the history; `r_net` (the SERVED leg) is
   untouched and correct, so every other cohort and every net-of-fee comparison is unaffected.
5. **Nothing here has been compared to BD.** No BD value appears in this file because no BD pull has
   been made.

---

## 6. WHAT IS ASKED OF `4.0.0_SA_CRO`

Select the 3-5 probe accounts from (or outside) the table above, and rule the two methodology cells
that gate the first pull, both filed 2026-08-29 (msg 83415, queued -- the seat was dark):

1. **Which inception anchors the SI cell** -- trade-start, BD funding-inception, or our chain's
   first-linked-date. They are three different numbers, and the puller silently defaults to the
   window start when none is supplied.
2. **Whether QTD/YTD cells compare on cumulative or annualised returns** -- BD's request block
   carries `returnMethod: "Annualized"`; our linker emits cumulative and carries the annualisation
   inputs, so either is producible until this is ruled.

**Instruments:** `canonical_positions`/`twr_daily`/`flow_ledger` at
`opal-data-49financial/gold/advi/canonical/` (read 2026-08-29); `dim_account_xref` `date=2026-08-28`
at `opal-data-assets/blackdiamond/49f/silver/`; `taxsma_resolver.py` tier-1 rule at source.
Linker: `data/assets/scripts/gold/runners_49f/parity_period_returns.py` @`8ae7a3ab82`.
