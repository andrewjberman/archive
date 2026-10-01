# AMGT_CORPUS -- round 22 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~06:1xZ.** Two orders were issued in ONE issuance (decomposition v22.0, `7ab1c1ff42`, merged
`d43930b5b1`) on `1.0.0_SA_CTO~Z`'s round-21 analysis (`0bf907bee8`). Both are complete, re-graded and merged. The round's three
WORLD acts ran under signed pairs:
- x-3: the r-1 register;
- x-1: the `pack_shape` rewrite;
- x-2: the unit apply and the re-derive of three blocks.

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 2 of 2 complete, drained

| order | cell | worker tip | drain | this seat's run at the tip |
|---|---|---|---|---|
| `TO-CRPS-x-1` | dossier `METHOD_VERSION` `/4` -> `/5` (the three `/4` test literals follow) | `16a44c6403` | `a51adaeeda` | proof VALID; AC1 `x1 code_method amgt-corpus-dossier/5 stored_differs 3 of 3`; AC2 `58 passed` |
| `TO-CRPS-x-2` | `build_unit_map.apply_discriminated` | `25eacf0210` | `98b0cb59c4` | proof VALID; AC1 on a temp copy `x2 applied 8 of 9 skipped 1 changed_entries 8 other_changed 0 expected_set True reads_stated 8 tsm_unchanged True reader_6501_best_sales MILLIONS`; AC2 `23 passed` |

Drain hygiene after both merges: ruff py39 clean; 193 passed.

## 2. The WORLD acts, each under its pair and a NEVER-2 entry

**x-3 -- `amgt-induction-daily` REGISTERED.**
- Pair: COO `0d437b429d`, CTO `be2cf27545`. Ledger: opened `319f947374`, closed `c8ad550b64`.
- Pinned to `33c1d096a3`, which carries the `zz-1` pool union and the `admit` step. The pinned tree is clean.
- The ad-hoc QA fire at 05:00:50Z returned LastTaskResult 0 in 11 s on branch 1:
  - registration population 0, `bloomberg_calls 0`, `pool_puts 0`;
  - `admit population registered 96 without_block 0 pulled 0 bloomberg_calls 0`;
  - closing `mode fire as_of 2026-09-30 rc 0`.
- The crosswalk is byte-unchanged.
- **The acceptance is the first scheduled fire, 2026-09-30T13:00:00Z (09:00 ET).**

**x-1 and x-2 -- the served acts.** Pair: COO `5757501e0d`, CTO `951082ff8d`; AMENDMENT 1 `921b124dea`. One ledger entry,
`0794dfd10f`, with legs D, M, R and V.
- **Leg M:** the unit apply on the committed `field_map.json`, committed `0982a0767d`.
  - The element-wise diff against the pre-image is exactly the 8 entries, with `other_changed 0`, TSM unchanged, and LF only.
  - Every entry states `unit_evidence.reads 1`. The CTO withdrew round-21 ruling 3's "2 reads" on this measurement.
- **Leg R:** the re-derive of 6501, 9433 and 8035 (c1), from the same raw.
  - Figure by figure against the predecessor stamps: **15 / 1 / 1 unit flips (= expected), 0 value moves, 0 other unit
    changes, 0 sign changes outside the facts, `filled_by_sa 0`.**
  - The round-19 reader now returns MEASURED for 6501 BEST_SALES.
- **Leg D:** the `pack_shape` rewrite: **95 puts, 0 errors, objects 190 -> 285**, all at `/5`.
- **THIS SEAT'S DEFECT, caught and repaired:** leg D ran concurrently with leg R.
  - The rewrite reached 9433 and 8035 before their re-derives, so their `/5` dossiers named the pre-flip block stamps.
  - The verify re-read showed `pack_shape_only 93 other_moves 2` (`model_rows` on exactly those two).
  - The CTO signed AMENDMENT 1: 2 `write_one` puts, gated on an `inputs_equal_now` census.
  - The gate read `names 95 false 2 errors 0 false_names [8035_JP_Equity, 9433_JP_Equity]`.
  - Both were rewritten: objects **285 -> 287**; each now reads `inputs_equal_now True` and names the new stamp.
  - The CTO's rule for next time: finish act 2 before act 1 starts, when one act's output is the other's input.
- **Leg V:** the final `other_moves 0` re-read over the 95 is running at this packet's commit. Its line goes to the
  entry and to `evidence/r22_final_expected_moves.txt` when it lands. The entry closes on it.

**Served effect.** Pages move on the three blocks now: 17 labels UNRESOLVED -> MILLIONS. `pack_shape` reaches no page until
AMGT_RESAPP r52 redeploys `read_dossier` at `/5`.

## 3. `c2` -- NOT run (the CTO refused the SA branch)

8316 and 8766 carry 9 SA gaps each, with SESSION_ERROR on their served blocks. A re-derive would retry the Seeking Alpha
fallback and could move values. Round 23 cuts `derive --no-sa-fallback`. Their map entries are already applied (leg M), so the
re-derive under that flag is a 13-flip, 0-value act.

## 4. The finding the round produced (the CTO's round-23 lead cell)

`evidence/r22_unresolved_unit_census.txt`:
- **9612 of 37746 served figures (25%) carry an UNRESOLVED unit, on 69 of 100 blocks.**
- **9176 of them (63 names) are mnemonics outside every field family:** BS_CASH_NEAR_CASH_ITEM, IS_ADJUSTED_OPERATING_INCOME,
  NET_INCOME, RETURN_ON_INV_CAPITAL, RETURN_ON_TANGIBLE_ASSETS, BS_TOTAL_LIABILITIES, RETURN_ON_CAP, EQY_DPS, and more.
- 363 are the magnitude class, where the per-share band misses IS_DIV_PER_SHR 177, REVENUE_PER_SH and BOOK_VAL_PER_SH.
- 64 are EQY_FUND_CRNCY: a currency code classified as a non-numeric unit, not TEXT.

This round's acts moved 17 of them.

## 5. Rows

- None new this round.
- `Z-W2-S16` (TSM with no same-currency anchor) is carried.
- The CTO's r-1 condition stands: a branch-2 fire files a row the same day naming its new keys.

## 6. Enrichment candidates for the round-22 analysis

1. The unit-family cell: the census-found unfamilied mnemonics, `EQY_FUND_CRNCY` as TEXT, and the per-share band.
2. `derive --no-sa-fallback`, then the c2 re-derive of 8316 and 8766 under it.
3. The r-1 acceptance read at the 13:00Z fire.

## 7. Bounds and residue

- No Bloomberg call, no Seeking Alpha call, and no vendor call this round. The ad-hoc fire made 0 calls by the producer's own
  count.
- Drained worktrees `wk-crps22-1/2` were removed with their branches kept (Andrew 02:5xZ, record `8c4f79e531`).
- The pinned checkout `opal-pinned\amgt-induction-daily\33c1d096a343` is the scheduled task's working directory and stays.
