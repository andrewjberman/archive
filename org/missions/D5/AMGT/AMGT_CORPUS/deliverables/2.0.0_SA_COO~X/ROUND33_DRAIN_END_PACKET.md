# AMGT_CORPUS round 33 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`.

**Decomposition:** v33.0 @`62504f5f9c`, with AMENDMENT 1 @`f64efce667`.

**Source:** round-32 analysis @`ac45eeeef8`, rulings 1-3 (row Z-S81).

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-ai-1` ground reads in `build_unit_map` | LOCAL | DONE, direct act `f64efce667` | `checks/round33/ai1_check.py`: base build 0/4 + control 4/4 -> build 4/4 + control 4/4; 93 build_unit_map tests passed (9 new; 4 assertions that pinned the ruled-away DECIMAL guess updated on purpose) |
| `CRPS-ai-2` scoped remeasure of 11 names + 11 re-derives + dossiers | SERVED | DONE, ledger `amgt-corpus-r33-ai2` CLOSED (5 legs) | section 2 |

`fanout: 0 worker chains of 1, cap 3`.

**AMENDMENT 1:** the EQY_DVD_YLD_IND ground is a band (0.5, 2.0) on indicated yield / (dividend per share / PX_LAST x 100), not a
tolerance. Measured on real rows: PWR 1.07 .. 1.18, BA 1.00 .. 1.14, GOOGL 1.01 .. 1.33. The band spans 4x against a 100x gap, it
decides on a 2/3 majority, and IS_DIV_PER_SHR is the second dividend field.

## 2. The SERVED act ai-2 -- ledger `amgt-corpus-r33-ai2` (pair COO `e748581d10` / CTO `45a11d1ea8`)

The serializing dry run over **every one of 100 keys** (`checks/round33/ai2_dryrun.py`) predicted:
`ai2 keys 100 move_blocks 11 map_entries 374 unit 77 sign 8 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0`.
The act's after-state equals it.

| leg | result | commit |
|---|---|---|
| gate | 0 producer diff since the dry run; map == HEAD; temp remeasure == the signed table; pre-act census DECIMAL 77, UNRESOLVED 11 | `d74a0daa46` (open) |
| a | `m33` vs HEAD == the signed table: fields_unit 7, status_moves 12, other_keys 10, other_securities 0. RESAPP am-1 (`scoped_amgt.py`), which landed after the gate, is outside the import closure (re-read). | `31c1e10888` |
| b | map `31c1e10888` | `31c1e10888` |
| c | 11 stamps `20261002T180207Z..180226Z`, each equal to its capture (vintage stripped); 0 value moves; exactly 11 new block objects | `795cf57788` |
| d | 11 dossiers, exactly one new object each, 0 other names; inputs_equal_now 11/11 | this commit |
| v | section 3 | this commit |

## 3. The real run (leg v, `evidence/r33_ai2_leg_v_census.txt`), with the census beside its negative arms

- **Census over the newest served block of 100 keys (37,746 figures), 19:05Z:**
  - DECIMAL **77 -> 0**;
  - UNRESOLVED units **11 -> 19** (+8, the named no-ground figures);
  - moved keys **exactly the 11**;
  - value moves **0**.
- **Negative arms:**
  - BA BEST_DIV_YLD stays PERCENT, and its stamp did not move;
  - stamps outside the 11 moved: **0 of 89**;
  - the DECIMAL-confirmed arm has **count 0**. It was named empty in both halves and is not claimed as passed.
- **One served figure per series-median family (CTO msg 28595):**

  | figure | served value | unit | reads as |
  |---|---|---|---|
  | ORA `RETURN_ON_INV_CAPITAL` FY2025 | 0.2237 | PERCENT | 0.22% |
  | BP `RETURN_COM_EQY` FY2025 | 0.0962 | PERCENT | 0.096% |
  | JD `OPER_MARGIN` FY2025 | 0.2119 | PERCENT | 0.21% |

- **Z-S81 decided** (row `Z-S83`): 69 PERCENT and 8 UNRESOLVED.

## 4. For the CVO's plausibility read (this round cut no judgment criterion)

**ORA's FY2025 ROIC serves 0.22% against its own FY2016-2024 history of 3.7 .. 7.3%.**
- The unit is the key's by the series rule. Bloomberg serves one unit per field per name, and the series median is 4.47.
- So the label is right. Whether FY2025's magnitude is a real low year (or a partial-year figure) is a VALUE question that this
  round did not touch, and the answer may belong to a row of yours.
- BP's 0.096% ROE and JD's 0.21% margin are low but plausible for those years (BP's low 2025 earnings; JD's 2025 delivery losses).

**Push state:** every round-33 commit is LOCAL on CLOUD. The push is `0.0.0_AB_MSTR~Z`'s, on Andrew's word.
