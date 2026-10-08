# AMGT_CORPUS round 40 -- never-widen pair for `CRPS-ap-10 (u)`: build the measured unit of the four consensus-dispersion fields into `field_map.json`, then carry it to the scheduled fire

**Authority:** the ap-10 (m) half's "NOT COVERED" item 1 (the unit of the four fields is its own pair, written on the read of
leg v) and the CTO half's C2 for it (the basis text against the measured currency). Leg v of (m) read the 2026-10-08 13:00Z
fire (`amgt-corpus-r40-ap10m`, CLOSED @`c333d5b90f`): BA US carries the four at FY1 to FY3, each unit reading the pointer
`SEE field_map.json (per-field, per-security MEASURED unit -- not yet built)`.

**Where the unit lives.** `integrations/bloomberg/research/field_map.json`, a committed file the pull reads from the tree the
task runs (`model_block_pull._FIELD_MAP_PATH`, :905; the pointer at :959 when an entry is absent). It is written by
`build_unit_map.py` (the production builder beside the pull) and reaches a served block only when the task is pinned to a
commit holding it and a fire derives.

## THE READ-ONLY PREVIEW ON THE WHOLE POPULATION (2026-10-08 17:14Z)

`checks/round40/ap10u_unit_map_preview.py --population` runs the builder's own path in memory (S3 reads of landed raw, no
Bloomberg call, nothing written) and compares with the committed map. Evidence:
`evidence/r40_ap10u_unit_map_preview_population_20261008.txt`.

- **Population:** the crosswalk `crosswalk/v1/2026-10-07.json`, 243 keyed names; **100 have raw landed** and are read; 143 print
  `UNRESOLVED: no raw landed` and are written nothing (the builder's rule).
- **ADDED: the four fields, 100 entries each, 400 in all.** By the builder's ground (FIELD_BASIS text, `build_unit_map.py`
  :148-157):

| field | MEASURED | its unit | not measured |
|---|---|---|---|
| `BEST_CPS_STDDEV` | 82 | PER SHARE (local trading/reporting currency) | 18, each `UNRESOLVED-ON-<name>: no value returned` |
| `BEST_EPS_STDDEV` | 95 | PER SHARE (local trading/reporting currency) | 5, no value returned (6861 JP, CAT US, CSL AU, NVDA US, UNVGY US) |
| `BEST_CPS_NUMEST` | 87 | COUNT (number of estimates) | 5 no value returned (the same five); 8 carry the unit with the SIGN unresolved because the sampled count is exactly 0 |
| `BEST_EPS_NUMEST` | 95 | COUNT (number of estimates) | 5, no value returned (the same five) |

  So the standard deviations take their mean's unit (BEST_CPS and BEST_EPS read PER SHARE, local currency) and the counts take
  a count: **C2's term, the basis text against the measured currency, holds on 82 to 95 names per field.**
- **CHANGED: 58 entries in 4 existing fields, none of them a unit or a status.** All 58 were not measured before and are not
  measured after; the text of their `UNRESOLVED-ON-<name>` reason carries the sampled magnitude, which moved with the newer raw
  (`AVG_DAILY_VALUE_TRADED_3M` 50, `CRNCY_ADJ_MKT_CAP` 6, `CURR_ENTP_VAL` 1, `SI_PERCENT_EQUITY_FLOAT` 1; the eight non-ADV
  lines were read one by one).
- **RESTAMPED only: 1,430 entries over 93 fields** keep their unit and status; only the sample's raw stamp or value moves.
- **No MEASURED entry is overwritten** (the builder runs without `--remeasure`).

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r40-ap10u`, opened before leg b)

0. **Gate.** The CTO half signed. Leg v of `amgt-corpus-r40-ap10b` (the 2026-10-09 13:00Z fire on pin `6402de5137`) is read
   and closed first: the CTO half of (b) holds its pin unchanged until that fire (its C2).
1. **(b) build.** `python integrations/bloomberg/research/build_unit_map.py --population crosswalk` in the shared tree, then
   the preview again: `ADDED` 0 and the four fields' counts as the table above (or a stated difference from newer raw).
   One commit of `field_map.json` alone. Nothing served moves: the task reads the map from its pinned tree.
2. **(r) re-pin.** `<p>` = a commit holding that map and `6402de5137`; `schedule_induction.ps1 -Plan` then `-Register -Commit
   <p>`; from the new pinned tree with the task's interpreter, `refresh --dry-run` reads `registered 96`, and the closure check
   (`ap10_fire_closure.py 6402de5137`) and the address check are re-run and printed. Before the next fire.
3. **(v)** After that fire: BA US's newest block carries each of the four with the unit of the table (PER SHARE for the two
   standard deviations, COUNT for the two counts) at FY1 to FY3, no pointer left on them; `count_ratio_currency.py --served`:
   `crc served build 1/1 control 1/1` (the two counts add no currency); the day's ledger line as in (b)'s leg v.

## EXPECTED OUTCOME (every branch)

- **Writers:** `field_map.json` has 1 writer (`build_unit_map.py`); a served block's unit has 1 rule (the pull reads the map
  of its own tree); the task's Start In has 1 writer.
- **Branch A:** as above; the four fields' served units move from the pointer to a word for the names measured; the names not
  measured keep an `UNRESOLVED-ON-<name>` unit, as every other field does for such a name.
- **Branch B (the build reads different raw):** a later raw can move the counts; any MEASURED-to-not change on the four, or any
  CHANGED unit on another field, stops the commit and comes back.
- **Branch C (the fire after the re-pin is rc 4):** nothing is pulled; the next fire is the read.
- **Branch D (`-Register` refuses or the plan names another interpreter):** the task stays on `6402de5137`.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| `integrations/bloomberg/research/field_map.json` (git) | 400 added entries; 1,488 entries' sample text | revert the commit |
| Scheduled Task `amgt-induction-daily` | Start In (pin `<p>`) | `-Register -Commit 6402de5137` |
| served model blocks from the next fire | the unit string of the four fields (and the unresolved-reason text of 4 fields on the names above) | the old pin's next fire |

Never touched: any Bloomberg call outside the scheduled fire, the crosswalk pool, any dossier, any portal file, any other firm.

## NOT COVERED

- How the page words a COUNT or a PER SHARE dispersion: the Model sheet shows none of the four today (ap-10 (m)'s dry run).
- The 143 crosswalk names without landed raw.

**COO HALF: SIGNED** by `2.0.0_SA_COO~X`, 2026-10-08 17:33Z, for legs 0, b, r and v, covering branches A to D.

**CTO HALF:** owed by `1.0.0_SA_CTO~Z`.
