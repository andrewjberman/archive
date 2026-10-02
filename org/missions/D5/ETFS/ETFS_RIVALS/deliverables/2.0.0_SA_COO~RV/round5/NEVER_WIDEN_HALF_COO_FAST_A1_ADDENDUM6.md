# NEVER-WIDEN -- COO HALF, ADDENDUM 6: trend sector panel honesty (G6-1) + sector_source (CALL 9) at pin CLOUD 93227704b7

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~10:0xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-6 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-5. Every gate, key and condition stands; the served delta is measured
through each stage's own `handler_entry` (`round5/served_delta_a1.py`, the CTO~Z condition of addendum 5).

**Why:** CVO~RV grade 6 (@bcac012fe7, PASS on addenda 4-5) G6-1 (P2): "No GICS sector in the source" is 48-100% of
gross in six funds' trend sector panels, which lack the ranking panels' "Sectors not shown" rule. CRO~RV CALL 9
condition: a trend row carries `sector_source` own | other_fund. Drained at CLOUD **93227704b7** (commit 1b3d226cc8).

## VERDICT: SIGNED (at pin CLOUD 93227704b7)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** from `/c/tmp/rv-apply` at 93227704b7: the five Lambdas' `source_code_hash` +
`last_modified` only; no policy change. Package diff vs the deployed c2b9023fc6: `gold_buying_trend.py`, `render.py`.

## THE SERVED DELTA, MEASURED THROUGH THE HANDLERS (page day 2026-10-01)

`served_delta_a1.py --day 2026-10-01` at the candidate code, vs the served newest objects:
- `holding_contribution`: 0 of 3906 rows changed; `buying_trend`: **0 of 319 values changed** (the table gains the
  nullable `sector_source` column); `input_census`: 0 of 1568.
- The page (overlay publish over the served tables): the trend sector panels of **ETFT, GQGU, IDVZ, PCLG** read "Sectors
  not shown" in place of their tables (no-GICS gross > 50%); every other component unchanged; 1,580,780 -> 1,577,692
  bytes; no script.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| G1 | the five stage Lambdas' code | c2b9023fc6 (daily NxzDgawd.., fetch wyjN9iLx.., canonical 4/gQVR41.., silver sV9HR/d0.., publish OHI9KQj5..) | in place to 93227704b7 | re-apply from a tree at c2b9023fc6 |
| G2 | gold `buying_trend` date=2026-10-01 | the 09:45Z object | ONE new content-sha object via `refresh_a1` (the new column) | prior objects stay |
| G3 | platinum page 2026-10-01 | batch fast-a1-publish-1001f | republished ONCE, batch fast-a1-publish-1001g | prior page kept under `revisions/<ts>/` |
| G4 | the 2026-10-02 scheduled runs and page | would run c2b9023fc6 | run 93227704b7 | G1's rollback |

## ACT-START GATES

1. Plan exactly 0/5/0. 2. Live base equals G1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r7` opened AND
committed before the apply (`&&`). 4. Nothing in flight; window to 10:45Z, else after the 09:00 ET sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 10:45Z:** the served trend carries `sector_source`; the served page hides the trend sector tables of
  ETFT, GQGU, IDVZ, PCLG. The post-act read prints both from the SERVED objects.
- **Not applied by 10:45Z:** the 10-02 chain runs c2b9023fc6 (PASS by grade 6); the act follows the sweep and G3 also
  republishes 2026-10-02. Covered with the same keys and rollbacks.
