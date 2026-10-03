# AMGT_CORPUS round 33 -- never-widen pair for `CRPS-ai-2`: the scoped remeasure of the 11 DECIMAL-by-magnitude names, and ONE re-derive of each of their blocks

The COO half is below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` (round-32 analysis ruling 3).

**Authority:** round-32 analysis @`ac45eeeef8`, rulings 1 and 2 (row Z-S81). Decomposition v33.0 @`62504f5f9c`, with its
AMENDMENT 1 @`f64efce667`.

**Code:** CLOUD HEAD >= `f64efce667`, which carries ai-1 (`_row_yield_identity`, the no-ground UNRESOLVED branch). The run prints
`git rev-parse HEAD` first. `PYTHONPATH=<root>;<root>/integrations/bloomberg/research`, in Windows form, is set on every leg.

**THE ORDER IS THE ACT:** gate -> (a) -> (b) -> (c) -> (d) -> (v), exactly as ah-3. There is one NEVER-2 entry,
`amgt-corpus-r33-ai2`, and the sentinel is committed after every leg close.

**The lever:** `build_unit_map --securities` with the 11 names below, plus `--remeasure`. It re-reads every mnemonic of those 11
names and never another security.

> HEI US, MELI US, PWR US, JD US, ORA FP, RWE GR, BP/ LN, AZN LN, RKT LN, TTE FP, ULVR LN

## THE SERIALIZING DRY RUN OVER EVERY KEY

Script: `checks/round33/ai2_dryrun.py`. Output: `evidence/r33_ai2_dryrun.txt`, run at HEAD `bd232ecca9`.

`ai2 keys 100 move_blocks 11 map_entries 374 unit 77 sign 8 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0 writes_per_block {1: 100}`

| transition | figures | names | why |
|---|---|---|---|
| RETURN_ON_INV_CAPITAL DECIMAL -> PERCENT | 20 | ORA, RWE | the series-median rule (ORA median 4.47; RWE's series is -18.2 .. 4.0). The entries were single samples. |
| RETURN_COM_EQY / RETURN_ON_ASSET / RETURN_ON_TANGIBLE_ASSETS DECIMAL -> PERCENT | 10 each | BP/ LN | series medians 3.78 / 1.33 / 1.48, against the 09-16 single samples |
| OPER_MARGIN DECIMAL -> PERCENT | 10 | JD | series median 1.06 |
| EQY_DVD_YLD_IND DECIMAL -> PERCENT | 9 | PWR | ai-1's row identity: 5 of 6 computable rows in the percent band |
| EQY_DVD_YLD_IND DECIMAL -> **UNRESOLVED** | 4 | HEI 1, MELI 3 | no per-share dividend in any fiscal row, so no ground (ruling 1) |
| SI_PERCENT_EQUITY_FLOAT DECIMAL -> **UNRESOLVED** | 4 | AZN, RKT, TTE, ULVR | no ground (ruling 1) |
| sign POSITIVE -> UNRESOLVED | 8 | the 8 UNRESOLVED units above | the standing classification split: a unit that does not discriminate forces its sign UNRESOLVED (`build_unit_map.py`, the M-DISAGREE-1(a) note) |

There are 0 value, currency, case and top-level moves. **The remeasure's reach beyond the 77 is 0 unit moves:** the 11 names'
other mnemonics re-read to the labels they already serve. The 8 sign moves are the only reach, and they are named above.

**The map, key by key** (a second temp rebuild, read by `checks/round33/m33.py`):

| change | count |
|---|---|
| field-level `unit` dicts | 7 mnemonics (13 per-security labels: EQY_DVD_YLD_IND 3, SI 4, the returns and margin 6) |
| `unit_status` / `sign_status` MEASURED -> UNRESOLVED | 12 (the 6 no-ground entries x unit and sign) |
| per-security `exception` added | 6 (the same 6 entries; the reason is carried) |
| field-level `sign` / `measured_on` | 2 + 2 (EQY_DVD_YLD_IND, SI_PERCENT_EQUITY_FLOAT) |
| `unit_evidence` added / `raw_stamp` / `value_sampled` re-read | 323 / 123 / 27 |
| entries of any other security | **0** |

**The negative arm the analysis names** ("a figure whose ground confirms DECIMAL stays DECIMAL"): **no member.** The dry run moves no
figure to DECIMAL and leaves none at DECIMAL among the 11 names. Over 100 keys, the only DECIMAL labels after the act would be none
(the census reads it at leg v). The arm is named as empty, with its count of 0, never as passed.

## THE DOSSIERS

After (c), leg (d) runs `write_one` for the 11 names only, writing only when inputs changed. The count is read at leg d.

## SERVED REACH (named, not acted)

- `/thesis` serves the block figures: 77 unit texts and 8 sign texts change, and every value is byte-unchanged.
- The Model tab prints a percent row by its row type (`modelSheet.ts` reads no unit field).
- An UNRESOLVED unit (the 8) is refused by the check face's not-measured bucket. This is the honest state Z-S81 asked for: a small
  value with no ground is no longer claimed MEASURED.

## AFTER-STATE THE VERIFY READS (leg v)

1. After (a), the committed map's per-key diff (`m33` vs the pre-act HEAD) equals the table above. The gate re-runs it immediately
   before (a). A moved count is re-signed, never absorbed.
2. Each of the 11 new blocks equals its captured dry-run block, `vintage` stripped. The capture is taken again immediately before (c).
3. Dossiers: at most one new object per name, and inputs_equal_now reads true.
4. The census over 100 keys reads:
   - DECIMAL-by-magnitude labels 77 -> 0;
   - UNRESOLVED +8 units;
   - moved keys exactly the 11;
   - value moves 0.
   **Negative arms:** BA's BEST_DIV_YLD stays PERCENT (ah-2); a name outside the 11 keeps its stamp; the DECIMAL-confirmed arm is
   printed with its count of 0.

## BLAST RADIUS AND ROLLBACK

- **Touches:**
  - `integrations/bloomberg/research/field_map.json` (one commit, the 11 names' entries only);
  - 11 new block stamps under `derived/model_block/<key>/` (BP at its slash-safe key);
  - at most 11 new dossier objects.
  - There is no overwrite and no delete (row Z-S4).
- **Rollback:** revert the map commit and ai-1 (`f64efce667`), then re-derive the 11 names forward. The prior stamps stay.

## STOP LIMBS

1. Stop and revert the map if (a) touches a security outside the 11, or moves a status other than the 12 named.
2. Stop and name it if (c) writes any block other than the 11, a block differs from its capture, or a value moves.
3. Stop on any `ERROR:` or a non-zero rc.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-02, for gate, (a), (b), (c) (11 blocks) and (d) (at most 11 dossiers). It is signed
against these functions, all at `f64efce667`:
- `build_unit_map.main` / `build_entries` / `_row_yield_identity`;
- `model_block_pull.stage_derive`;
- `dossier.write_one` / `current_inputs`.
