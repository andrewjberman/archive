# AMGT_CORPUS round 34 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`.

**Decomposition:** v34.0 @`bcd3b35abc`.

**Source:**
- Andrew-direct 2026-10-03 ~20:3xZ, verbatim "yes to all recommendations". Card 3 is "one daily pull for all of it" (earnings
  dates, the V3 fields, a long name); record @`9fe6e6f111`, relay msg 29002.
- Round-33 analysis @`e55e3b5152` s.2.

Serves FWD-22 (the scheduled refresh) and FWD-20 (the V3 fields). It supplies RESAPP FWD-37's earnings dates.

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-aj-1` refresh stage + 52 appended mnemonics + scheduled refresh step | LOCAL | DONE, worker `0.9.0_WK_AMGT_CORPUS~1`, drained @`a864e82a5c` | AC1 `aj1 build 5/5 control 3/3`; AC2 `AJ1-REFRESH-DRY PASS registered=96 with_block=96 fields=120`; AC3 `AJ1-SCHED-DRY PASS order admit:6 refresh:8 closing:9`; proof VALID |
| `CRPS-aj-2` re-pin `amgt-induction-daily` + one on-demand fire | WORLD | DONE, ledger `amgt-corpus-r34-aj2` CLOSED (4 legs) | section 2 |

`fanout: 1 of 1 chains, cap 8`. All three checks FAILed at the base, as expected.

**Issuer acts inside the decomposition, each recorded in its own commit:**
- **Amendment `22eb07e64c`:** refresh derives with `sa_fallback=False`. The daily pull is a Bloomberg pull, and the Seeking
  Alpha fallback is a live vendor GET no word covers for recurrence. Measured: 0 SA_FALLBACK figures in 102 latest served blocks.
- **Row Z-W1-S29 disarm `68f09dce81`:** four test pins follow the appended lists. The fifth, the unit-family census, stays RED by
  design (section 4).

## 2. The WORLD act aj-2 -- ledger `amgt-corpus-r34-aj2` (pair COO `5454d04761` / CTO `ebd3ea8aff`)

| leg | result |
|---|---|
| L0 gate | In a Python311-first session the plan names Python311. Without the prepend it resolves Python314, which has no blpapi (row Z-S85). |
| Lr re-pin | `REGISTERED`. Start In `opal-pinned/amgt-induction-daily/a864e82a5c4b` (HEAD a864e82a5c), Task To Run Python311 `induction_scheduled --mode fire`, daily 13:00Z. |
| Lf fire | `schtasks /run` at 23:25:12Z; closing line 23:37:49Z `mode fire as_of 2026-10-03 rc 0`. Refresh read `registered 96 with_block 96 already_current 0 pulled 96 bloomberg_calls 768`, with 0 REFRESH FAILED. This is branch A exactly: 96 x 8 = 768 calls predicted. |
| Lv verify | section 3 |

## 3. The real run (leg v)

The newest-block census (`checks/round34/v34.py` -> `evidence/r34_aj2_leg_v_census.txt`):
- **v1:** registered 96, of which 96 have a newest block at 20261003 and 0 do not. The mid-fire control at 23:33Z read 65/96,
  so the census discriminates.
- **v2:** over 96 blocks the 52 new mnemonics hold 32,826 figures and 5,381 unresolved entries. Every figure carries the pointer
  unit, because the map has no family for them yet (section 4).
  - Served on all 96 names: `LONG_COMP_NAME`, `EXPECTED_REPORT_DT`, `ERN_ANN_DT_AND_PER`, `SHORT_NAME`, `COUNTRY_FULL_NAME` and
    `CRNCY_ADJ_MKT_CAP`. `AVG_DAILY_VALUE_TRADED_3M` is served on 95, with 1 empty.
  - The price-dated range fields (AVERAGE_/HIGH_/LOW_, DIVIDEND_YIELD, PX_ERN_RATIO_WITH_*) are unresolved for non-December
    fiscal-year names only. The reason is "not dated at the fiscal period end (non-December FYE, fye_join)", the existing join
    rule.
  - `BEST_CPS` holds 253 figures, with 35 gaps "HELD_OFF: SA fallback held off" (the amendment).
  - **`EQY_FUND_YEAR`: 0 figures and 0 unresolved.** It was requested and is absent from both lists (section 4).
- **v3:** the API's own reader (`scoped_amgt.read_model_block`) serves BA, GOOGL and BP/ LN at vintage 2026-10-03.

The page (`evidence/r34_aj2_leg_v_page.md`; ui-walk `20261003T235538Z`, every BA request 200) shows BA's Model tab:
- the 17-row sheet;
- the newest version "October 3rd, 2026, 23:27 UTC";
- "566 figures added, 0 removed, 7 changed, 172 unchanged". All seven changed lines are base header figures, e.g. share price
  USD 204.80 to USD 193.56.

**The CTO half's added condition** (0 pointer-unit or raw-list values for the 52 on BA's Model tab) **reads 0.**

## 4. Rows, and what the round-34 analysis receives

| row | class / standing | what |
|---|---|---|
| `Z-S84` | OBSERVATION, INERT | The scheduled entry's dry-run admit (and now refresh) step reads rc 1: induction_run's dry-run boto3 poison is still installed. The fire path is not poisoned. |
| `Z-S85` | OBSERVATION, ARMED, disarmed at the act | `schedule_induction.ps1` resolves the first python on PATH, which is now Python314 (no blpapi). The durable repair is an explicit interpreter parameter. |
| `Z-W1-S29` | OBSERVATION, ARMED, partly disarmed | Four pins fixed. `test_build_unit_map_families::test_census_covers_every_pulled_mnemonic` is RED because none of the 52 has a unit family, so their figures read the pointer unit, which the page treats as NOT measured. |
| `Z-S86` | OBSERVATION, INERT | `DE_US_Equity` thesis/peers 404 on the live API (they were 200 on 10-01). Deere has no block and is not in the refresh population, so this is outside aj-2's radius. RESAPP's surface. |

**Candidates for the enrichment list, mine to name and the CTO's to rule:**
1. The unit families for the 52 in `build_unit_map.py`, measured on this fire's values, then one map rebuild and re-derive (a
   SERVED pair). This turns 32,826 pointer-unit figures into measured or UNRESOLVED-with-reason entries, and clears Z-W1-S29.
2. The 49 V3 rows on the Model tab: `modelSheet.ts` maps none of them yet, so FWD-20's "every row the team's sheet carries"
   still reads short until the rows exist (portal).
3. `EQY_FUND_YEAR`: a request-type placement repair (it is probably a reference field) plus the silent-absence path on the
   December branch.
4. The Z-S85 and Z-S84 repairs.

FWD-22's acceptance is the NEXT scheduled fire, 2026-10-04 13:00Z (09:00 ET), read the day after. A REFUSED day is recorded and
the sign-in carded, never retried in a loop (CTO half).

Push state: LOCAL.
