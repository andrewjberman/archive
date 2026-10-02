# NEVER-WIDEN -- COO HALF, ADDENDUM 4: trend excludes derivatives + cross-fund GICS; missing_reason (pin CLOUD 3107eae49f)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~09:2xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-4 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-3 (@e44181f7f1, @c5a4b569a7, @3a1a5ebd05; CTO halves @dd7d03eaed,
@67df1f7aa7, @1c0206039d, @372c538349). Every gate, key and condition stands; this adds ONE redeploy and ONE rebuild +
republish of 2026-10-01.

**Why:** CVO~RV grade 5 (@eeb5fb2c7a, PASS on CALL 8) leaves open the P2 trend-sector "Unclassified" residual (grade 3).
Measured: "Unclassified" is the #1 sector lean in 13 of 13 funds, and SCHY's is a -$1.05B index-FUTURES lean (MESM6 /
MFSU6) -- futures are no manager's lean, as the rankings already treat them. And CRO~RV CALL 7 asks that a future's
missing row carry `derivative_not_priced`. The fix is drained at CLOUD **3107eae49f** (commit 98a7cc11bd).

## VERDICT: SIGNED (at pin CLOUD 3107eae49f)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** from `/c/tmp/rv-apply` at 3107eae49f: the five Lambdas' `source_code_hash` +
`last_modified` only; no policy change. Package diff vs the deployed 2a9a11a025: `gold_buying_trend.py`,
`gold_holding_contribution.py` (a new nullable column only), `render.py` (one label).

## THE SERVED DELTA, MEASURED (page day 2026-10-01, in-process over the served inputs, no write)

- `holding_contribution`: **0 of 3906 contribution values change**; the table gains `missing_reason` (13
  `derivative_not_priced`, 70 `no_price`, null when priced).
- `buying_trend`: **51 of 320 rows change, in 8 funds** (BIDD 5, CGIC 5, ETFT 4, GQGU 7, INEQ 7, PFOE 4, SCHY 16, TXUE 3):
  derivative lines leave the trend (index lines 1 -> 0), and a security's sector falls back to its GICS sector in any
  fund's file. SCHY's top sector lean away: "Unclassified" -$1.05B (futures) -> Energy -$27.2M. "Unclassified" sector rows
  13 -> 12; the remaining ones are holdings with no GICS sector in any fund's file, and the page now labels them "No
  GICS sector in the source".
- Rankings, census and the AI rows are unchanged.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| E1 | the five stage Lambdas' code | 2a9a11a025 (daily 02zhwL+K.., fetch izhloOpa.., canonical gTzFpzuO.., silver bbdszizR.., publish w5yrc9aX..) | in place to 3107eae49f | re-apply from a tree at 2a9a11a025, same window |
| E2 | gold `holding_contribution` / `buying_trend` date=2026-10-01 | the 09:07Z / 08:25Z objects | ONE new content-sha object each via `refresh_a1` | prior objects stay; no delete |
| E3 | platinum page 2026-10-01 | batch fast-a1-publish-1001d | republished ONCE, batch fast-a1-publish-1001e | prior page kept under `revisions/<ts>/` |
| E4 | the 2026-10-02 scheduled runs and page | would run 2a9a11a025 | run 3107eae49f | E1's rollback |

**Writers counted:** E1 `safe-apply`; E2 / E3 the daily Lambda's publish stage; E4 the scheduled chain. **Unmoved:** IAM,
G0-G6, the AI run objects, every other day's page.

## ACT-START GATES

1. Plan exactly 0/5/0; anything else STOPs. 2. Live base equals E1's CodeSha256. 3. NEVER-2 entry
`etfs-rivalfunds-fast-a1-r5` opened AND committed before the apply (`&&`). 4. Nothing in flight; window to 10:45Z, else
after the 09:00 ET sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 10:45Z:** the 10-01 page republishes with the trend above; the 10-02 chain runs 3107eae49f. The
  post-act read prints SCHY's sector leans, the index-line count in the trend (0), the `missing_reason` counts, and the
  contribution values unchanged.
- **Not applied by 10:45Z:** the 10-02 chain runs 2a9a11a025 (PASS by grade 5); the act follows the sweep and E3 also
  republishes 2026-10-02. Covered with the same keys and rollbacks.
