# AMGT_CORPUS round 32 -- never-widen pair for `CRPS-ah-3`: the map remeasure of the 4 DECIMAL-labelled BEST_DIV_YLD names, and ONE re-derive of each of their blocks

The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z`.

**Authority:**
- `1.0.0_SA_CTO~Z` RULED msg 28540, ruling 1 item (2): "the BEST_DIV_YLD label DECIMAL -> PERCENT, SERVED, which brings its
  never-widen half to this seat".
- Decomposition v32.0 @`cc061e1d95`.

**Code:** CLOUD HEAD >= `b2aee0c0f2`, which carries ah-2 (`_yield_identity`). The run prints `git rev-parse HEAD` first.
`PYTHONPATH=<root>;<root>/integrations/bloomberg/research`, in Windows form, is set on every leg.

**THE ORDER IS THE ACT:** gate -> (a) -> (b) -> (c) -> (d) -> (v). Each after-read must pass before the next step. There is one
NEVER-2 entry, slug `amgt-corpus-r32-ah3`, and the sentinel is committed after every leg close.

## WHY A SCOPED REMEASURE

The four entries are clean MEASURED, so `build_entries` skips them unless `--remeasure` is passed. The builder's only lever is
`--securities "BA US Equity" "GOOGL US Equity" "HEI US Equity" "PWR US Equity" --remeasure`. It re-reads EVERY mnemonic of those
four names, never another security. Its whole reach is measured below; nothing is assumed from the code change alone.

## THE SERIALIZING DRY RUN OVER EVERY KEY

Script: `checks/round32/ah3_dryrun.py`. Output: `evidence/r32_ah3_dryrun.txt`, run at HEAD `9b12f6159b`. No commit has touched
`integrations/bloomberg/research/` or `lib/research/` since then.

The builder rebuilt a TEMP map with the scoped remeasure. Against it, the producer's own `stage_derive` ran for **every one of 100
keys** with a write-capturing client. Raw-slash copies were excluded; encoded BP and NG were included.

`ah3 keys 100 move_blocks 4 map_entries 159 unit 15 sign 0 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0 writes_per_block {1: 100}`

| block | unit moves | transitions |
|---|---|---|
| `BA_US_Equity` | 3 | BEST_DIV_YLD DECIMAL -> PERCENT (FY2026-2028) |
| `GOOGL_US_Equity` | 6 | BEST_DIV_YLD DECIMAL -> PERCENT 3; **EQY_DVD_YLD_IND DECIMAL -> PERCENT 3** |
| `HEI_US_Equity` | 3 | BEST_DIV_YLD DECIMAL -> PERCENT |
| `PWR_US_Equity` | 3 | BEST_DIV_YLD DECIMAL -> PERCENT |
| the other 96 keys | 0 | nothing |

There are 0 value, sign, currency, case and top-level moves.

**The 3 EQY_DVD_YLD_IND moves on GOOGL are the remeasure's own reach, not ah-2's rule.**
- The cause: GOOGL's entry was measured from one sample before CRPS-ab-2 (round 26). It re-reads now under the series-median rule.
- The direction is the correction row Z-S81 names: a percent read as a decimal.
- They are named here because the act carries them. HEI's and PWR's EQY_DVD_YLD_IND stay DECIMAL; their series median is under
  0.3, which leaves them for the analysis of Z-S81.

**The map, key by key** (a second temp rebuild, diffed per key):

| change | count |
|---|---|
| field-level `unit` labels | 2 (BEST_DIV_YLD, EQY_DVD_YLD_IND) |
| per-security `unit_evidence` added (the series-median evidence the remeasure records) | 146 |
| `raw_stamp` re-read | 31 |
| `derived_by` re-read | 31 |
| `value_sampled` re-read | 7 |
| `unit_status` / `sign_status` moves | **0** |
| entries of any other security | **0** |

## THE DOSSIERS

After (c), leg (d) runs `write_one` for the 4 names only. It writes only when inputs changed. The count is read at leg d, never
predicted. No other name is written.

## SERVED REACH (named, not acted)

- `/thesis` serves the block figures. The 15 unit texts change; every value is byte-unchanged.
- `modelSheet.ts` reads no unit field. The Model tab prints a yield row by its row type, so BA's 0.0% / 0.1% / 0.6% print
  unchanged. Row Z-S76 proved them percent.
- Row Z-S81's other 77 DECIMAL-by-magnitude figures are **not** moved: 80 non-BEST_DIV_YLD figures, less GOOGL's 3.

## AFTER-STATE THE VERIFY READS (leg v)

1. After (a), the committed map's per-key diff against the pre-act bytes equals the table above. The gate re-runs that diff
   immediately before (a). A count that has moved since (new raw landed) is re-signed, never absorbed.
2. Each of the 4 new blocks EQUALS its captured dry-run block, `vintage` stripped. The capture is taken again immediately before (c).
3. Dossiers: at most one new object per name, and `inputs_equal_now` reads true for all 4.
4. The census over 100 keys:
   - BEST_DIV_YLD DECIMAL 12 -> 0.
   - EQY_DVD_YLD_IND DECIMAL 16 -> 13.
   - Every value is unchanged.
   - **Negative arms:** HEI `EQY_DVD_YLD_IND` stays DECIMAL; JD `OPER_MARGIN` keeps its unit byte-unchanged; the 96 other
     newest blocks keep their stamps.

## BLAST RADIUS AND ROLLBACK

- **Touches:**
  - `integrations/bloomberg/research/field_map.json` (one commit, the 4 names' entries only);
  - 4 new block stamps under `derived/model_block/{BA,GOOGL,HEI,PWR}_US_Equity/`;
  - at most 4 new dossier objects.
  - There is no overwrite and no delete (row Z-S4).
- **Rollback:** revert the map commit and ah-2 (`b2aee0c0f2`), then re-derive the 4 names forward. Their prior stamps stay.

## STOP LIMBS

1. Stop and revert the map if (a) touches a security outside the four, or moves a `unit_status` / `sign_status`.
2. Stop and name it if (c) writes any block other than the four, a block differs from its capture, or a value moves.
3. Stop on any `ERROR:` or a non-zero rc.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-02, for gate, (a), (b), (c) (4 blocks) and (d) (at most 4 dossiers). It is signed
against these functions, all at `b2aee0c0f2`:
- `build_unit_map.main` / `build_entries` / `_yield_identity`;
- `model_block_pull.stage_derive`;
- `dossier.write_one` / `current_inputs`.
