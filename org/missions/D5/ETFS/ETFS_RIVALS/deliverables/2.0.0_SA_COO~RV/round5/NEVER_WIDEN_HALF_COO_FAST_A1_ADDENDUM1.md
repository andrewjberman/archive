# NEVER-WIDEN -- COO HALF, ADDENDUM 1: the CVO grade-2 fix redeploy (pin CLOUD fc80f776e4) and the 2026-10-01 rebuild

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~08:2xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum half (asked).
**Extends:** `round5/NEVER_WIDEN_HALF_COO_FAST_A1.md` @4df699fa92 and the CTO half @dd7d03eaed. Every gate, key and
condition there stands; this addendum adds ONE redeploy and ONE rebuild + republish, and widens nothing else.

**Why:** CVO~RV grade 2 (`org/tier1_exec/3.0.0_SA_CVO/deliverables/ETFS_RIVALS_FAST_GRADES_20261002.md` @9cca47a6cd)
FAILED the served 2026-10-01 page: F1 (P0) ETFT's YTD contributions sum to -188.51% (a zero valuation read as a -100%
day), plus F2-F5. The fix is drained at CLOUD **fc80f776e4** (commit 45c2563adf). The demo page carries F1 until this
lands, and the 10-02 page (07:00 ET fetch, 09:00 ET sweep) would carry it too.

## VERDICT: SIGNED (at pin CLOUD fc80f776e4)

## THE PLAN, MEASURED

`terraform plan` from `/c/tmp/rv-apply` detached at fc80f776e4, package staged by `rivalfunds_package.py`:
**Plan: 0 to add, 5 to change, 0 to destroy** -- the five `aws_lambda_function.stage[*]` in place, `source_code_hash` +
`last_modified` only. **No policy change** (gen_policies.py unchanged). The staged package differs from the deployed
7aa0186d45 in exactly six files: `gold_holding_contribution.py`, `gold_buying_trend.py`, `render.py`, `ai_accounts.py`
(prompt only; the Lambdas never call the AI client), `sweep.py` (`refresh_a1` passes through `trigger_event`),
`guardrails_config.json` (+ `contribution_implausible_move_band` 0.5, PROVISIONAL).

## THE SERVED DELTA, MEASURED (page day 2026-10-01)

Served `holding_contribution-20261002T073937Z-41b9f635cded` vs the fixed rk-1 over the same served inputs:
**102 of 3939 rows change, in 10 funds** (BIDD 8, CGIC 11, ETFT 42, IDVZ 4, INEQ 1, PCLG 4, PFOE 8, SCHY 16, TSEL 4,
WCMG 4); BASG, GQGU, TXUE unchanged.

| fund | YTD served | YTD fixed | cause |
|---|---|---|---|
| ETFT | **-188.51%** | +0.56% | F1: zero-valuation days 2026-02-04, 04-10 (quantity held, market_value 0) are no price, not -100% |
| SCHY | -1.83% | +5.85% | F1: implausible valuations on unchanged quantity refused |
| BIDD | +11.49% | +12.51% | F1, the same |
| CGIC, PFOE | +5.72%, -4.99% | +5.80%, -4.92% | F1 / F2 |
| IDVZ, PCLG, TSEL, WCMG, INEQ | equal YTD | equal | F2: the money-market line leaves the rankings (rows -4 / -1) |

`buying_trend` rows per fund move by at most one (CGIC 25 -> 26, IDVZ 18 -> 17, WCMG 18 -> 17: the money-market line
out); the marks before a fund's first report read `.`; windows start at the first report (IDVZ 08-21, PFOE 08-24,
WCMG 04-23). `input_census` and `research_hypotheses` are unchanged by the code.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| B1 | the five stage Lambdas' code | 7aa0186d45 (CodeSha256 daily PJr6l0z.., fetch XNCVRKjn.., canonical /xRX2KTZ.., silver ziEjx8Wm.., publish Rx7MAw7q..) | in place to fc80f776e4 | re-apply from a tree at 7aa0186d45, same window |
| B2 | gold `holding_contribution` / `buying_trend` / `input_census` date=2026-10-01 | the 07:39-07:40Z objects | ONE new object each, written by the daily Lambda's publish stage (`refresh_a1`), content-sha named; the 07:39Z objects stay (never overwritten); readers take the newest | the newer objects are unread once the page is re-put; no delete |
| B3 | platinum page 2026-10-01 | publish_page/3, batch fast-a1-publish-1001 | republished ONCE via `daily-lambda {"only": ["publish-page"], "refresh_a1": true}`, batch fast-a1-publish-1001b | the prior index/manifest kept under `revisions/<ts>/`; re-put |
| B4 | the 2026-10-02 scheduled runs and page | would run 7aa0186d45 | run fc80f776e4 | B1's rollback |

**Writers counted:** B1 `safe-apply` only; B2 and B3 the daily Lambda's publish stage (one rule, `produce_a1`); B4 the
scheduled chain. **Unmoved:** IAM, every G0-G6 object, the AI run objects, every other day's page.

## ACT-START GATES

1. The plan is exactly 0/5/0 above (no policy change); anything else STOPs.
2. The live base equals the CodeSha256 values in B1.
3. NEVER-2: a new entry `etfs-rivalfunds-fast-a1-r2`, opened and committed before the apply, after the union read.
4. No rivalfunds Lambda invocation in flight; act window now -> 10:45Z, else after the 09:00 ET sweep completes.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 10:45Z:** the 10-01 page republishes with ETFT YTD +0.56% and the F2-F4 displays; the 10-02 chain
  runs the fixed code. The post-act read compares the moved fields (CTO condition 3): ETFT / SCHY / BIDD YTD totals, the
  money-market lines absent from the rankings and trend, the trend window start and `.` marks, the sector panels.
- **Not applied by 10:45Z:** the 10-02 chain runs 7aa0186d45; the act follows the sweep, and B3 then also republishes
  2026-10-02 the same way. This half covers that branch with the same keys and rollbacks.
