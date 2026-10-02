# NEVER-WIDEN -- COO HALF, ADDENDUM 2: CRO~RV CALL 6 conditions 1-2 + futures never priced (pin CLOUD 0d4b3f6e4d)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~08:3xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-2 half (asked).
**Extends:** the half @4df699fa92 and addendum 1 @e44181f7f1 (CTO halves @dd7d03eaed, @67df1f7aa7). Every gate, key and
condition stands; this adds ONE redeploy and ONE rebuild + republish of 2026-10-01, and widens nothing else.

**Why:** CRO~RV CALL 6 (`org/tier1_exec/4.0.0_SA_CRO/deliverables/ETFS_RIVALS_RULINGS_20261002.md`) accepted the 0.5 band
for the addendum-1 apply only, with conditions 1 (ratio-symmetric bands, amending CALL 1 condition 3) and 2 (refused
holding-days disclosed at row grain, in the caption and in the audit block) as the next FAST item, to land before or
with the 2026-10-02 republish. CVO grade 3 (@ea29c625e9, PASS on F1-F4) lists them open, with futures pricing. The fix
is drained at CLOUD **0d4b3f6e4d** (commit 6d2b71f724).

## VERDICT: SIGNED (at pin CLOUD 0d4b3f6e4d)

## THE PLAN, MEASURED

`terraform plan` from `/c/tmp/rv-apply` detached at 0d4b3f6e4d: **Plan: 0 to add, 5 to change, 0 to destroy**, the five
`aws_lambda_function.stage[*]` in place, `source_code_hash` + `last_modified` only; **no policy change**. The staged
package differs from the deployed fc80f776e4 in exactly two files: `gold_holding_contribution.py` and `render.py`.

## THE SERVED DELTA, MEASURED (page day 2026-10-01, in-process over the served inputs, no write)

| fund | YTD served (fc80f776e4) | YTD at 0d4b3f6e4d | cause |
|---|---|---|---|
| BASG | +9.33% | +9.77% | condition 1: a one-sided fault (drop kept / recovery refused, or the reverse) is now refused on both sides |
| CGIC | +5.80% | +5.99% | condition 1, the same |
| SCHY | +5.85% | +5.79% | futures (MESM6 / MFSU6, provider_security_type "Index") never priced |
| the other 10 | equal | equal | -- |

- `holding_contribution` gains `n_days_refused`, `refused_reasons`, `refused_days` (column-optional).
- 12 refused holding-days are disclosed in YTD (11 `corporate_action_suspected`, 1 `implausible_valuation`): the
  caption states them per fund and period; the audit block lists each (fund, holding, day, price ratio, reason).
- `buying_trend`, `input_census` and the AI rows are unchanged by the code.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| C1 | the five stage Lambdas' code | fc80f776e4 (daily jQjG+wnp.., fetch HvlPW4By.., canonical fStAOGBF.., silver KPYG8dcx.., publish /zIJNf1g..) | in place to 0d4b3f6e4d | re-apply from a tree at fc80f776e4, same window |
| C2 | gold `holding_contribution` date=2026-10-01 | the 08:24Z object | ONE new content-sha object via `refresh_a1` (buying_trend / input_census rebuilt to equal content write nothing) | the prior objects stay; no delete |
| C3 | platinum page 2026-10-01 | batch fast-a1-publish-1001b | republished ONCE via `daily-lambda {"only": ["publish-page"], "refresh_a1": true}`, batch fast-a1-publish-1001c | the prior page kept under `revisions/<ts>/` |
| C4 | the 2026-10-02 scheduled runs and page | would run fc80f776e4 | run 0d4b3f6e4d | C1's rollback |

**Writers counted:** C1 `safe-apply`; C2 / C3 the daily Lambda's publish stage; C4 the scheduled chain. **Unmoved:**
IAM, G0-G6, the AI run objects, every other day's page.

## ACT-START GATES

1. The plan is exactly 0/5/0; anything else STOPs.
2. The live base equals C1's CodeSha256 values.
3. NEVER-2: a new entry `etfs-rivalfunds-fast-a1-r3`, opened AND committed before the apply (the apply is chained
   with `&&` on the commit), after the union read.
4. No rivalfunds Lambda invocation in flight; act window to 10:45Z, else after the 09:00 ET sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 10:45Z:** the 10-01 page republishes with the YTD table above, the refused-day captions and the
  audit list; the 10-02 chain runs 0d4b3f6e4d. The post-act read prints the moved fields (BASG / CGIC / SCHY YTD, the
  refused-day count and reasons, 0 futures rows priced).
- **Not applied by 10:45Z:** the 10-02 chain runs fc80f776e4 (F1-F4 fixed, PASS by grade 3); the act follows the
  sweep and C3 also republishes 2026-10-02 the same way. Covered here with the same keys and rollbacks.
