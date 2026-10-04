# AMGT_CORPUS round 35 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`.

**Decomposition:** v35.0 @`17a5893472`.

**Source:** `1.0.0_SA_CTO~Z` round-34 analysis @`83cd052a9c` s.3, the enrichment list (relay msg 29092). The resume after the
03:22Z stall is Andrew-direct (msg 29176); the loop re-arm after the 18:58Z site-Z crash is Andrew-direct "2.) Yes" (msg 29201,
record @3166fec43e).

Serves FWD-22 (the scheduled refresh) and FWD-20 (the V3 fields, now with measured units).

## 1. The cells

| cell | `<risk>` | state | evidence (re-run by the issuer at HEAD, 2026-10-04 ~20:1xZ) |
|---|---|---|---|
| `CRPS-ak-1` unit families for the 52 | LOCAL | DONE, worker `0.9.0_WK_AMGT_CORPUS~1`, drained @`7c43d48775` | `ak1 build 2/2 control 2/2` (156 landed entries, 0 no-family; 68 base families and 204 base units unmoved); `-k families` 47 passed; proof VALID |
| `CRPS-ak-2` the re-pin script names its interpreter | LOCAL | DONE, worker `0.9.0_WK_AMGT_CORPUS~2`, drained @`61c58e31bc` | `ak2 build 2/2`: b1 a Python314-first PATH plans Python311; b2 `REFUSED: ...Python314\python.exe cannot import blpapi`; proof VALID |
| `CRPS-ak-3` the scheduled dry run reads rc 0 | LOCAL | DONE, worker `0.9.0_WK_AMGT_CORPUS~3`, drained @`a5a561d96b` | `ak3 build 2/2 control 1/1`: admit rc 0, refresh rc 0, closing rc 0; aws_writes_attempted 0; proof VALID |
| `CRPS-ak-4` map rebuild, 96 re-derives, re-pin | SERVED | DONE, ledger `amgt-corpus-r35-ak4` CLOSED (5 legs, Branch A) @`66a15668e1` | section 2 |

`fanout: 3 of 3 chains, cap 8`. All checks FAILed at the base, as expected (decomposition s.1).

**Issuer act inside the decomposition:** row Z-W1-S30 disarm @`1ed823496d`. `CRNCY_ADJ_MKT_CAP`'s `FIELD_BASIS` now reads
"millions of that currency". Every landed value is the header's `CUR_MKT_CAP / 1e6`.

## 2. The SERVED act ak-4 -- ledger `amgt-corpus-r35-ak4` (pair COO `36ad5a67f9` / CTO `5eebfe43f1`, 5 conditions)

The act was interrupted by the 18:58Z site-Z crash before leg 0 finished; nothing had been written. It ran whole after the relaunch,
19:43-20:12Z.

| leg | result |
|---|---|
| L0 gate | The 2026-10-04 13:00Z scheduled fire closed clean: run log line 329 `induction_scheduled mode fire as_of 2026-10-04 rc 0`, line 327 `refresh population registered 96 with_block 96 already_current 0 pulled 96 bloomberg_calls 768`, 0 REFRESH FAILED. `ak4_dryrun.py` on the post-fire raw (stamps `20261004T13xxZ`) is line-identical to the pre-fire run. `-Plan -Commit HEAD` names Python311 (source: live-task). |
| Lm map | Commit `74e00624b0`, `field_map.json` alone: 66 -> 118 fields (+52, -0), 100 securities. Over 6,600 base per-security entries, 0 units moved. The only base text changes are the two predicted UNRESOLVED re-samples (TSM `CURR_ENTP_VAL`, RKT `SI_PERCENT_EQUITY_FLOAT`) and 615 `raw_stamp` refreshes. |
| Ld re-derive | `checks/round35/ak4_leg_d.py`: registered 96, with_block 96, derived 96, failed 0. Each name derived on its newest raw with `sa_fallback=False`, so there were no Bloomberg or Seeking Alpha calls. `field_map.json` blob was unchanged by the derive. |
| Lr re-pin | `-Plan -Commit 74e00624b0` named Python311, then `REGISTERED`. Start In `opal-pinned/amgt-induction-daily/74e00624b074` (checkout HEAD 74e00624b0), Python311, daily 13:00Z, next 2026-10-05 13:00Z. |
| Lv verify | section 3 |

## 3. The real run (leg v)

The census is `checks/round35/v35.py 20261004T195` -> `evidence/r35_ak4_leg_v_census.txt`.
- **v1:** registered 96, redone 96, not redone 0.
- **v2 (CTO condition 3):** 0 base values moved over 96 names. The denominator is 36,864 base value keys. The positive control
  (`evidence/r35_ak4_leg_v_control.txt`) compares BA, GOOGL and TSM against their pre-10-03 blocks: 37, 34 and 35 moved. The
  comparison therefore discriminates.
- **v3 (CTO condition 4):** the 52 hold 32,826 figures and 5,381 unresolved entries; 0 figures carry the pointer unit. There are
  no Branch-B exclusions. In round 34 all 32,826 carried the pointer unit.

**The page** (`evidence/r35_ak4_leg_v_page.md`; ui-walk `20261004T200520Z`, 24 BA requests, all 200; disarm REFUSED):
- BA's Model tab lists "The version of October 4th, 2026, 19:56 UTC" newest of 22, which is this act's block.
- "566 figures added, 0 removed, 7 changed, 172 unchanged" against September 10th. These are the same counts as round 34, which
  agrees with v2. The raw from 10-03 and 10-04 carries Friday's close.
- The pointer-unit or raw-list count on the page is 0.

**Not measured here:** whether the 4,398 MEASURED units are RIGHT per field. ak-1's families were decided on the landed values
(AC1). A semantic read of a sample of the 52 against Bloomberg's definitions is a JUDGMENT for L9.

## 4. Rows, and what the round-35 analysis receives

| row | standing | disarm / evidence |
|---|---|---|
| `Z-S85` re-pin script resolves Python314 off PATH | ARMED | Disarmed by ak-2 @`61c58e31bc`. `ak2 build 2/2` at HEAD, and ak-4's two plans read `source: live-task`. |
| `Z-W1-S29` unit-family census test RED | ARMED | Disarmed by ak-1 @`7c43d48775` (the census test is green; `-k families` 47 passed). ak-4 served the result: 0 pointer-unit figures. |
| `Z-W1-S30` `CRNCY_ADJ_MKT_CAP` basis text wrong | ARMED | Disarmed @`1ed823496d` (the basis reads millions) before the map write. |
| `Z-S84` dry-run admit/refresh rc 1 under the poison | INERT | Repaired by ak-3 @`a5a561d96b`. The 10-04 log's two later dry runs read rc 0. |
| `Z-S86` `DE_US_Equity` thesis/peers 404 | INERT | Unchanged: 6 DE 404s on today's walk. Deere is not registered. This is RESAPP's surface. |
| `Z-W1-S31` four dividend-yield fields put in `ZERO_VALUE_UNIT_FROM_BASIS` (an exemption from ZERO-DOMINATED) | INERT | Open for the analysis: an exemption the order did not name. |
| `Z-W1-S32` `EQY_FUND_YEAR` YEAR family untested on any landed value | INERT | Open for the analysis: the field still lands no value (round-34 item 3). |

**Candidates for the enrichment list, mine to name and the CTO's to rule:**
1. A JUDGMENT read of the 52's units: a sample per family against Bloomberg's definitions (section 3, "not measured here").
2. The 802 UNRESOLVED entries for the 52: 656 read "no value returned", the rest are zero-dominated or magnitude
   non-discriminations. The question is whether any family has a ground that would resolve them.
3. Round-34 items 2 and 3, still open: the 49 V3 rows on the Model tab (`modelSheet.ts`, portal), and `EQY_FUND_YEAR`'s request
   placement (Z-W1-S32).
4. Z-W1-S31: rule the dividend-yield exemption, or revert it.

FWD-22 graded on the 2026-10-04 13:00Z fire (rc 0, 96 pulled) is the CVO's read. The first fire on the new pin is
2026-10-05 13:00Z.

Push state: LOCAL (ls-remote read at commit time, below).
