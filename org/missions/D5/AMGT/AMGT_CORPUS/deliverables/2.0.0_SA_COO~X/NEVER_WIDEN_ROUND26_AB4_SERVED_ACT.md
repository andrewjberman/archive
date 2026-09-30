# AMGT_CORPUS round 26 -- never-widen pair for `CRPS-ab-4`: the map rebuild (ab-2), ONE re-derive of the 18 moving blocks (ab-2 units, ab-3 cases, ab-5 labels), and the dossier refresh through the fixed reader (ab-1)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`. Round-25 analysis s.4 item 4; standing
rulings 1 and 3; aa-4 AMENDMENT 1 (the act-start gate reads the act's IMPORT CLOSURE).

**Code:** CLOUD HEAD >= `9b9585065a`, which carries ab-1 `78842bba5e`, ab-3 `c50db70fb0`, ab-5 `9753b57672`, ab-2 `6cfc6bab90`, and
rulings `f2f77b132a`. The run prints `git rev-parse HEAD` first.

**THE ORDER IS THE ACT.** (a) -> (b) -> (c) -> (d), each after-read passing before the next step. One NEVER-2 entry, slug
`amgt-corpus-r26-ab4`.

## THE SERIALIZING DRY RUN OVER EVERY KEY (`checks/round26/m4_dryrun.py`, `evidence/r26_m4_dryrun.txt`)
The builder rebuilt a TEMP map. Then the producer's own `stage_derive` ran against it with a write-capturing client for **every one of
100 keys** (the raw-slash copies excluded; the encoded BP/NG included). **Every** changed map entry and **every** (from, to) transition
is printed. Result:

`m4 keys 100 move_blocks 18 map_entries 9 unit 30 sign 20 currency 2 value 0 case_blocks 17 top 0 other 0 errors 0 writes_per_block {1: 100}`

**(a) The 9 map entries, field by field:**

| entry | change | served effect |
|---|---|---|
| BP/ LN `PE_RATIO` | UNRESOLVED -> **RATIO**, sign -> POSITIVE, `unit_evidence` series median 24.65 | 10 units + 10 signs |
| BP/ LN `PROF_MARGIN` | exception dropped -> **PERCENT** (series median 1.43) | 10 units |
| BBSE3 `CAPITAL_EXPEND` | UNRESOLVED reason text: sampled magnitude 0.058 -> the series median 0.172 (still UNRESOLVED) | 10 unit + 10 sign reason texts |
| BA, MELI, QXO `EQY_DPS` and `IS_DIV_PER_SHR` (6) | `unit_evidence` method `field_basis_zero_value` -> `series_median_abs`; **unit unchanged** | none (`Z-W2-S18`'s reach) |

**(c) The 18 blocks** (0 value, 0 top-level, 0 other; 1 captured write each):
- **BP/ LN** (`BP-SLASH-_LN_Equity`):
  - units 20: `PE_RATIO` UNRESOLVED -> RATIO 10; `PROF_MARGIN` UNRESOLVED -> PERCENT 10;
  - signs 10: `PE_RATIO` UNRESOLVED -> POSITIVE;
  - **currency 2: `CUR_MKT_CAP` USD -> no currency, and `NET_DEBT` USD -> no currency** (ab-5: the value is GBP, which neither label
    states; and the side is not separated);
  - case: ABSENT -> ABSENT, with the mixed input nulled (ab-3).
- **BBSE3:** unit and sign UNRESOLVED -> UNRESOLVED (reason text), 10 each.
- **The case diff on all 17 (BP and these 16), measured path by path by a second capturing run:** exactly two paths change,
  `cases.base.inputs.trailing_median_pe.value` (-> null) and `.reason` (added). No other case path moves, and 0 of 17 new blocks carry
  a non-null mixed `trailing_median_pe`.
- **16 more names, case only (ABSENT -> ABSENT) (ab-3):** 1299 HK, 939 HK, 992 HK, AZN LN, BABA US, HSBA LN, ICT PM, JD US, NOVN SW, RIO LN, SHOP CN, SPOT US, TTE FP, UBSG SW, ULVR LN,
  ZURN SW.
- **No case value moves anywhere.** Each of the 17 cases stays ABSENT with no value.

**(d) The dossiers:**
- A pre-act inputs read over the 18 plus NG shows **BP and NG stale now** (ab-1's reader now resolves their encoded 09-30 blocks); the
  other 17 are equal.
- After (c), `write_one` runs over the moved names that have a dossier, plus NG, and writes only where the inputs changed. The count
  is read at leg d, never predicted.

## PRODUCER INPUTS AND THE CODE DIFF (ruling 3)
`d66497aec3..HEAD` over the producer dirs: `build_unit_map.py` (ab-2), `model_block_pull.py` (ab-5 tables), `case_rule.py` (ab-3),
`dossier.py` (ab-1), and `lib/research/filings/drafting_build.py` (a peer's, outside the act's import closure per aa-4 AMENDMENT 1).
The dry run above ran THIS code against every served block, so each of these changes' figure, case and top-level effects is in the
table. Raw: `raw_stamp_used` is excluded from the compare, and there are 0 value moves.

## SERVED REACH (named, not acted)
- `/thesis` serves the block's figures (units, signs, labels). BP's two labels and 20 units reach the page with (c).
- **The cases do NOT reach `/thesis` from (c).** The scoped API recomputes the case per request from its DEPLOYED `case_rule`
  (`scoped_amgt.py:3195`). The deployed build still carries the pre-ab-3 rule, so the BP payload keeps showing 778.57 until
  AMGT_RESAPP redeploys.
- The redeploy is RESAPP's act (`2.0.0_SA_COO~Z`). It is named here and relayed after (c).

## AFTER-STATE THE VERIFY READS (leg v)
1. (b)'s element-wise diff equals the 9 entries above.
2. Each of the 18 new blocks EQUALS its captured dry-run block, with `vintage` stripped (captured again immediately before (c), the
   aa-4 method).
3. The dossiers: one new object per written name; changed keys `fields.model_rows`, `inputs` and `content_sha256`; `inputs_equal_now`
   true on each.
4. **The served read:** `/thesis` BP/_LN_Equity shows `PE_RATIO` RATIO, `PROF_MARGIN` PERCENT, and `CUR_MKT_CAP` with no currency.
   **The negative arm:** a same-currency name's `CUR_MKT_CAP` label (BA) is unchanged. The census reads 11 UNRESOLVED over 100 keys.

## BLAST RADIUS AND ROLLBACK
- **Touches:** `field_map.json` (one commit), 18 new block stamps, and the dossiers written at (d). No overwrite, no delete.
- **Rollback:** revert the map commit and the round-26 code, then re-derive forward (the prior stamps stay).

## STOP LIMBS
1. (a)/(b) touches an entry outside the 9: stop and revert.
2. Any block of (c) differs from its captured block, a value moves, or a case value moves: stop, name it, and re-derive the touched
   blocks.
3. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for (a), (b), (c) (18 blocks) and (d). `2.0.0_SA_COO~X`, 2026-09-30, against `build_unit_map.main` /
`build_entries`, `model_block_pull.stage_derive` / `_figure_currency`, `case_rule.compute_cases`, and `dossier.write_one` /
`current_inputs`, all at `9b9585065a`.
