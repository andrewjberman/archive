# AMGT_CORPUS round 25 -- never-widen pair for `CRPS-aa-2`: the map rebuild with aa-3's families, ONE re-derive of the 22 moving blocks carrying aa-1's label rule, and the dossier refresh that consumes them

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Round-24 analysis ruling 1 (`Z-S69` leads: the re-derive under a pair is the fix) and
standing rulings 1 and 3. aa-3's families join this act rather than a second pair: one producer pass, and the order is the act.

**Code:** CLOUD HEAD >= `0d73289a8e`, which carries:
- aa-1, the census and label rule wired at all 4 call sites (`3e87486db2`);
- aa-3, families R1, R2 and R4 (`a6b6c8506f`).

The run prints `git rev-parse HEAD` first. Evidence:
- `evidence/r25_m3_measure.txt` (`checks/round25/m3_measure.py`): per figure and per scope, through the producer's own
  `_resolved_unit`, `_resolved_sign` and `_figure_currency(..., security=)`, against a temp map rebuild.

**THE ORDER IS THE ACT (ruling 1).** (a) and (b) complete before (c), and (c) completes before (d). Each after-read passes before the
next step begins. One NEVER-2 entry, slug `amgt-corpus-r25-labels-units`, legs a, b, c, d and v.

## THE ACTS
- **(a) The map rebuild:** `python integrations/bloomberg/research/build_unit_map.py --population crosswalk` on the committed
  map, with `PYTHONPATH` at the repo root. It reads S3 raw only.
- **(b) The commit:** `field_map.json` alone.
- **(c) The re-derive of 22 blocks:** `model_block_pull.py derive --no-sa-fallback --securities <3 per call>`, in Bloomberg form,
  over the 22 `BLOCK` lines of the m3 evidence:
  - 1299 HK, 6861 JP, 939 HK, 992 HK, AZN LN, BABA US, BA US, BZLFY US, HSBA LN, ICT PM, JD US, NOVN SW, PBR US, RIO LN, SHOP CN,
    SPOT US, TSM US, TTE FP, UBSG SW, ULVR LN, UNVGY US, ZURN SW.
  - Bronze reads only; no vendor call.
- **(d) The dossier refresh:** `write_one` over the 21 of the 22 that have a dossier (6861 JP has none). It runs as a NAMED script
  with `python -u`, and a survivor check matches on CreationDate (round-24 ruling 2).

## PRODUCER INPUTS AND THE CODE DIFF (ruling 3)
The 22 served predecessors were built at three points:
- 8 at round 23 leg c (code at `67568b59c4`, 08Z);
- 8 at round 23 leg s (`94301d5a9c`, 09Z);
- 6 at round 24 leg c (`04b89561ce`, 12Z).

The reachable producer diff `67568b59c4..HEAD`, excluding tests and the map, touches 6 files:

| file | change since the oldest predecessor | effect on (c), read per figure by m3 |
|---|---|---|
| `build_unit_map.py` | z-1 F1-F6 (already served on round 24's 28), aa-3 R1/R2/R4 | the map entries of (a): 6 fields change; 38 units close on 6861 / 939 / BA |
| `model_block_pull.py` | y-5 per-figure sign (already served on every block since round 23 s), z-4 path via `slash_safe_key` (identity on these 22), aa-1 `_figure_currency(..., security=)` at the 4 call sites | 53 currency labels on 20 blocks; 38 signs follow the 38 units; 0 other sign moves |
| `unit_anchor.py` | z-2 reason text | none on these 22 beyond the map |
| `pull_consumer.py`, `derive_fye_fixed.py` | z-4 path sites | not run |
| `crosswalk.py` | a marker comment | none |

The other inputs are unchanged:
- `case_rule` / `_compute_cases`: no diff.
- Raw: `same_raw` on 22 of 22 (each block's `raw_stamp_used` is its newest refdata stamp).
- `filled_by_sa 0` on all 22.

## WRITER CENSUS (read at `0d73289a8e`)
- `field_map.json`: `build_unit_map.main` (a); `apply_discriminated` (not run); `_ensure_unit_map` (a new name only; none).
- `derived/model_block/<key>/`: `stage_derive` alone, with its SA path held off.
- `research_dossier/`: `dossier.write_one` alone.
- No working-tree scheduled task runs these producers.

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' OWN RULES (`evidence/r25_m3_measure.txt`)
- **(a) The map diff:** 6 fields change (`BEST_EPS BEST_PE_RATIO BOOK_VAL_PER_SH BS_TOTAL_LIABILITIES CURR_ENTP_VAL
  REVENUE_PER_SH`), with 0 top-level changes and 0 securities added. The entry count is read at leg a against the pre-image.
- **(c) Per figure:** 22 blocks.
  - **38 unit changes:** all from UNRESOLVED to measured (6861 JP 26, 939 HK 10, BA US 2), **0 measured-to-other**.
  - **38 sign changes:** the same 38 figures (a sign follows its unit), with 0 contradicting their value.
  - **53 currency changes, all `scope: header`, 0 in any other scope:**
    - 12 `CUR_MKT_CAP` move from the reporting label to the measured quote currency, TSM's TWD -> USD among them;
    - 41 figures (`CUR_MKT_CAP` 8, `NET_DEBT` 20, `CURR_ENTP_VAL` 13) move from a reporting label to NO currency, basis
      `UNMEASURED:`, per the ruling;
    - 0 basis-only changes.
  - **0 value changes, 0 case changes.**
  - Not-measured units on the 98 keys go from 49 to 11.
- **(d) The dossier refresh:** 21 puts. The expected diff per dossier is `fields.model_rows` (units, signs and currency labels),
  `inputs` and `content_sha256`.

## AFTER-STATE THE VERIFY READS (leg v)
1. (b)'s element-wise diff against the pre-image: the 6 fields named; 0 shared; 0 top-level.
2. Every block of (c) against its recorded predecessor, figure by figure:
   - unit, sign and currency counts equal to its m3 line;
   - 0 value, 0 case, 0 measured-to-other;
   - 0 sign contradicting its value;
   - `filled_by_sa 0`;
   - the derive `vintage` stamp counted separately.
3. `aa3_check` over the 98 keys: `measured_before 11`.
4. (d): exactly one new object for each of 21 names; 0 other names; changed keys limited to `fields.model_rows`, `inputs` and
   `content_sha256`; `inputs_equal_now` 21 of 21.
5. **The served read:** the deployed `opal-amgt-scoped-api` `/thesis` for TSM_US_Equity serves `CUR_MKT_CAP` labelled USD, and
   `NET_DEBT` with no currency. The CodeSha256 is printed.

## BLAST RADIUS AND ROLLBACK
- **Touches:** one committed file; 22 new model-block stamps; 21 new dossier objects. No overwrite and no delete.
- **Readers:** the page and the export read the newest block stamp.
  - 38 unit labels move from UNRESOLVED to measured.
  - 12 market caps show the quote currency.
  - **41 header figures stop printing a currency they never measured.** This is the ruling's intent; a reader that required
    a currency on those figures now reads none.
- **Rollback:**
  - revert the `field_map.json` commit and the aa-1 wiring (`3e87486db2`), then re-derive the 22 (forward-only new stamps);
  - `write_one` then refreshes the 21;
  - the prior stamps stay in place.

## STOP LIMBS
1. (a)/(b)'s diff touches a field outside the 6 named, or any top-level key: stop before (c), and revert.
2. Any block in (c) shows any of the following: stop, name the figures, revert (b), and re-derive the touched blocks.
   - a value or case change;
   - a unit, sign or currency count other than its m3 line;
   - a measured-to-other unit;
   - a label move outside `scope: header`;
   - a sign contradicting its value;
   - `filled_by_sa` > 0.
3. (d) writes any name outside the 21, or any change outside `fields.model_rows`: stop and name it.
4. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for (a), (b), (c) (22 blocks) and (d) (21 dossiers). BP and NG are EXCLUDED in either form (`Z-S64`, aa-4).
`2.0.0_SA_COO~X`, 2026-09-30, against `build_unit_map.main` / `build_entries`, `model_block_pull.stage_derive` /
`_figure_currency` / `_resolved_unit` / `_resolved_sign`, and `dossier.write_one`, all at `0d73289a8e`. If any of these moves before
the act, this half does not travel with it.
