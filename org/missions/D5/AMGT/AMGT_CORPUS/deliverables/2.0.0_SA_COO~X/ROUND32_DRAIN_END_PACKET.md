# AMGT_CORPUS round 32 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`.

**Decomposition:** v32.0 @`cc061e1d95`.

**Source:**
- `1.0.0_SA_CTO~Z` RULED msg 28540. Round-31 ruling 1 ended with the demo. The rectangle is the round-31 analysis s.3, less
  FWD-20 and FWD-22, which stay on Andrew's word.
- Z-W4-S6's Peers lookup was routed to RESAPP by ruling 2 of the same message.

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-ah-1` Z-S74 not-measured prefixes | LOCAL | DONE, direct act `75ea254ddc` | `checks/round32/ah1_check.py`: base build 0/4 + control 5/5 -> build 4/4 + control 5/5; 22 render-path tests passed |
| `CRPS-ah-2` BEST_DIV_YLD by its DPS / PX_LAST identity | LOCAL | DONE, direct act `b2aee0c0f2` | `checks/round32/ah2_check.py`: base build 0/4 + control 4/4 -> build 4/4 + control 4/4; 84 build_unit_map tests passed (10 new) |
| `CRPS-ah-3` scoped remeasure + 4 re-derives + dossiers | SERVED | DONE, ledger `amgt-corpus-r32-ah3` CLOSED (5 legs) | section 2 |

`fanout: 0 worker chains of 2, cap 3`. No task order was cut, and no worker was spawned.

## 2. The SERVED act ah-3 -- ledger `amgt-corpus-r32-ah3` (pair COO `c216d1a52f` / CTO `b859ebff4c`)

The serializing dry run over **every one of 100 keys** (`checks/round32/ah3_dryrun.py`) predicted:
`ah3 keys 100 move_blocks 4 map_entries 159 unit 15 sign 0 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0`.
The act's after-state equals it.

| leg | result | commit |
|---|---|---|
| gate | `field_map.json` == HEAD bytes. A temp remeasure re-run reproduced the signed map table. The 8 `lib/research` files RESAPP landed since `b2aee0c0f2` (peers, scoped_amgt) are outside the act's import closure: 0 of 486 modules. | `44baa06d07` (open) |
| a | `m32` vs HEAD: fields_unit 2, unit_evidence 146, raw_stamp 31, derived_by 31, value_sampled 7, status_moves 0, other_securities 0. This equals the signed table. | `7527f440e7` |
| b | map `7527f440e7` | `7527f440e7` |
| c | 4 stamps `20261002T154901Z..154906Z`, each equal to its captured block (vintage stripped); 0 value and 0 case-value moves; exactly 4 new block objects | `b540a1b480` |
| d | 4 dossiers, exactly one new object each, 0 other names; inputs_equal_now 4/4 | this commit |
| v | see section 3 | this commit |

**The GOOGL EQY_DVD_YLD_IND reach.** The scoped `--remeasure` re-read GOOGL's EQY_DVD_YLD_IND entry under the round-26
series-median rule. It moved 3 figures DECIMAL -> PERCENT: the right direction, and outside ah-2's rule. The COO half named it,
and the CTO half accepted it by name (msg 28557). Row `Z-S82` records it on `Z-S81`.

## 3. The real run (leg v, `evidence/r32_ah3_leg_v_census.txt`), with the census beside its negative arms

- **Census over the newest served block of 100 keys (37,746 figures), 16:09Z:**
  - BEST_DIV_YLD DECIMAL **12 -> 0**;
  - EQY_DVD_YLD_IND DECIMAL **16 -> 13**;
  - moved keys **exactly the 4** (BA, GOOGL, HEI, PWR);
  - value moves **0**.
- **Negative arms:** HEI `EQY_DVD_YLD_IND` stays DECIMAL; JD `OPER_MARGIN` is unchanged with its stamp not moved; the other 96
  newest stamps are unchanged.
- **ah-1's real run** (`evidence/r32_ah1_served_census.txt`), over the same 100 blocks:
  - the provenance predicates now read 10 ZERO-DOMINATED units + 1 UNRESOLVED-ON- unit, and 11 UNRESOLVED-ON- signs, as
    UNRESOLVED;
  - the other 37,735 units and signs are unchanged (MEASURED).
- **The page:** BA's Model tab prints the yield row by row type (`modelSheet.ts` reads no unit field). The face is unchanged:
  0.0% / 0.1% / 0.6%, proved percent by Z-S76. The served unit label now agrees with it.

## 4. Rows this round

- `Z-S77`..`Z-S80`: the armed census, adjudicated by this seat's CVO at `393e471ea9`.
- `Z-S81`: 92 DECIMAL-by-magnitude labels on 8 mnemonics.
- `Z-S82`: amends Z-S81 to 77 after ah-3.
- Z-S81 is the candidate enrichment item for the round-32 analysis.

**Judgment criteria:** none were cut; every criterion is mechanical. This is an all-mechanical round, so the CVO's own read of
section 3's artifact is its only plausibility check. That read should ask one question: does a percent label on a 0.25% yield
read right to an analyst? It is not a pre-graded criterion.

**Push state:** every round-32 commit is LOCAL on CLOUD. Origin CLOUD was `b5f93e9f16` at the last read. The push is
`0.0.0_AB_MSTR~Z`'s, on Andrew's word.
