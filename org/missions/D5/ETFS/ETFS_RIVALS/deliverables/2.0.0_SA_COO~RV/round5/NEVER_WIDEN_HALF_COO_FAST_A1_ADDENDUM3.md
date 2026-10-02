# NEVER-WIDEN -- COO HALF, ADDENDUM 3: CRO~RV CALL 8 split guard (pin CLOUD 2a9a11a025) and the 2026-10-01 rebuild

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~09:0xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-3 half (asked).
**Extends:** the half @4df699fa92 and addenda 1 @e44181f7f1, 2 @c5a4b569a7 (CTO halves @dd7d03eaed, @67df1f7aa7,
@1c0206039d). Every gate, key and condition stands; this adds ONE redeploy and ONE rebuild + republish of 2026-10-01.

**Why:** CVO~RV grade 4 (@6aaf6b43f6, PASS on CALL 6 and futures) found G4-1 (P1): the split guard refused 7 REAL moves
because the fund traded that day, 2 of them in BASG, the demo fund (Datadog +31%, Intuit -20%), and the page labels them
"corporate_action_suspected". CRO~RV CALL 8 amended CALL 1 condition 3: refuse a split iff out(r) AND out(k) AND NOT out(v);
refuse implausible_valuation iff out(r, 0.5) with or without a quantity change; otherwise price. The fix is drained at
CLOUD **2a9a11a025** (commit 49241aa118); its tests carry the grade-4 table as a fixture.

## VERDICT: SIGNED (at pin CLOUD 2a9a11a025)

## THE PLAN, MEASURED

`terraform plan` from `/c/tmp/rv-apply` detached at 2a9a11a025: **Plan: 0 to add, 5 to change, 0 to destroy**, the five
Lambdas' `source_code_hash` + `last_modified` only; **no policy change**. The staged package differs from the deployed
0d4b3f6e4d in exactly `gold_holding_contribution.py` and `guardrails_config.json` (two notes restated; values unchanged).

## THE SERVED DELTA, MEASURED (page day 2026-10-01, in-process over the served inputs, no write)

**12 of 3906 contribution rows change.**

| fund | YTD served (0d4b3f6e4d) | YTD at 2a9a11a025 | cause |
|---|---|---|---|
| BASG | +9.77% | +10.15% | Datadog 05-07 (+31%) and Intuit 05-21 (-20%) priced: trades on real moves (Datadog now #2 YTD contributor, +2.09%) |
| GQGU | +6.00% | +6.35% | Snowflake 05-28 (+36%), Atlassian 05-01 (+30% on a buy) priced |
| CGIC | +5.99% | +5.87% | 8283 JP (+36%), VAL SJ (-22%), IMP SJ (-21%) priced |
| the other 10 | equal | equal | -- |

Refused holding-days YTD: 12 -> **5** (4 splits: KMB IN x2, Amphenol, AZN LN; 1 implausible: the CGIC IBE/D rights line).
Every fund's YTD sits in -4.92..+12.51%. `buying_trend`, `input_census` and the AI rows are unchanged by the code.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| D1 | the five stage Lambdas' code | 0d4b3f6e4d (daily b18Nz9gt.., fetch rrOC+3xa.., canonical V9jSOuwS.., silver I1Ba/c3H.., publish blyYySoH..) | in place to 2a9a11a025 | re-apply from a tree at 0d4b3f6e4d, same window |
| D2 | gold `holding_contribution` date=2026-10-01 | the 08:42Z object | ONE new content-sha object via `refresh_a1` | the prior objects stay; no delete |
| D3 | platinum page 2026-10-01 | batch fast-a1-publish-1001c | republished ONCE via `only: publish-page` + `refresh_a1`, batch fast-a1-publish-1001d | prior page kept under `revisions/<ts>/` |
| D4 | the 2026-10-02 scheduled runs and page | would run 0d4b3f6e4d | run 2a9a11a025 | D1's rollback |

**Writers counted:** D1 `safe-apply`; D2 / D3 the daily Lambda's publish stage; D4 the scheduled chain. **Unmoved:** IAM,
G0-G6, the AI run objects, every other day's page.

## ACT-START GATES

1. The plan is exactly 0/5/0; anything else STOPs.
2. The live base equals D1's CodeSha256 values.
3. NEVER-2: a new entry `etfs-rivalfunds-fast-a1-r4`, opened AND committed before the apply (`&&`), after the union read.
4. No rivalfunds Lambda invocation in flight; act window to 10:45Z, else after the 09:00 ET sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 10:45Z:** the 10-01 page republishes with the table above and 5 refused holding-days; the 10-02 chain
  runs 2a9a11a025. The post-act read prints BASG / GQGU / CGIC YTD, the 5 refused rows with reasons, and the 7 priced
  days' contributions.
- **Not applied by 10:45Z:** the 10-02 chain runs 0d4b3f6e4d (graded PASS by grade 4); the act follows the sweep and D3
  also republishes 2026-10-02 the same way. Covered here with the same keys and rollbacks.
