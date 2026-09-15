# AMGT_RESAPP.TO-AMGT-rj-7 -- session log, `0.9.0_WK_AMGT_RESAPP~21`

Worktree `C:/tmp/wk-amgt-11-4`, branch `wk-amgt_resapp-11-4`, start tip `10c74d0efb` (equal to `SITEZ`).
One order, chain D, cell `AMGT-rj-7`. Every act below is in this worktree; nothing was pushed.

## 1. The bar, first

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-4`; `org/`, `.tools/`, `lib/research/peers/`,
`lib/research/identity/` and `lib/opal_data_harvest/` all present. TREE-OK.

## 2. Re-grounding the order's premises (measured, before any build)

| premise as the order states it | measured |
|---|---|
| `engine.py` 222 lines, `:176-184` returns `absent` because no candidate universe was ever loaded | TRUE -- read at HEAD; the derived path `:191-213` was complete and unfed |
| the six scanner files under `json/security_scanner/latest/universes/` | TRUE -- all six present; sizes sp500 3,724,005 / r1000 7,559,246 / r1000v 6,426,590 / acwx 13,333,778 (the order said 12.4 MB) / eafe 4,797,450 / eafev 2,895,078 |
| `asOf` 2026-08-06 | TRUE -- 6 of 6 files carry it |
| the `~1` model blocks are the subject read | TRUE -- 4 `model_block_<key>.json` files, 3 carrying `GICS_SECTOR_NAME`; the 4th (`BABACVOCTRL_US_Equity`) carries `security_key: null` and 2 figures, so it is skipped BY THE RULE (no classification), never by its name |
| U-1 at `universe/v1/2026-09-15.json` with 256 names | TRUE -- 256 names, 33 carrying a `security_key`, 223 UNRESOLVED |
| X-1 at `crosswalk/v1/2026-09-15.json` | TRUE -- `crosswalk.resolve()` reads the pool; used for every identity emitted |
| Adam's CSC columns (card 3) | TRUE -- quoted verbatim from `SUBSTRATE_CARDS.md:73-76`, 17 per-peer columns |
| a Seeking Alpha comparables endpoint | FALSE -- see section 5 |

## 3. What was built

1. `lib/research/peers/universe.py` -- the loader. Six boto3 GetObject calls, folded to one row per
   ticker, UNION the model-block header scalars. Denominators printed per file, for the union, for
   the duplicates folded and for the model-block half. The folded set is cached beside this log as
   `candidate_universe.json` -- that cache IS the read vintage.
2. `lib/research/peers/taxonomy.py` -- the two vocabulary maps (GICS sector -> scanner sector, ISO2
   -> scanner country), each with its basis, its denominators and its named residue, plus
   `residue_over_database()` which re-measures both against whatever database is loaded.
3. `lib/research/peers/csc.py` -- Adam's 17 columns against the scanner's 289-factor registry and the
   284 codes a row carries. PRESENT 5, ABSENT 12 by subtraction.
4. `lib/research/peers/engine.py` -- the four rungs, the exclusive-depth MECE accounting, the
   log-market-cap tiebreak, the R-1 object, the pool writer with read-back, and the batch CLI.
5. `lib/research/peers/tests/test_peers.py` -- 26 unittest cases (was 4 bare pytest functions, which
   `python -m unittest` collects as ZERO).

## 4. Three seams the order did not name, all measured, all filed

* **Two sector vocabularies** (row `AMGT_RESAPP-Z-W21-S1`). 2849 rows speak the scanner's 13-value
  taxonomy, 3 speak GICS. `'Consumer Discretionary'` and `'Information Technology'` appear in ZERO
  scanner rows, so rung 1 on raw strings gives BABA and SAP an empty set.
* **Two market-cap units** (row `-W21-S2`). `mktVal` is USD millions; `CUR_MKT_CAP` is full currency
  units, and the model block's own basis definition says so: *"Current market capitalization, full
  currency units (not millions)."* The raw ratio is 2.5e-7. Normalised by 1e6; the mutant control
  below is exactly this defect re-injected.
* **A subject as its own peer** (row `-W21-S3`). SAP SE is in the database twice, as `SAP` (the model
  block) and as `484628` (the scanner), and X-1 resolves neither scanner identifier. Measured: SAP's
  own row was its top peer at rung 3. Disarmed in-code by an exact normalised-name arm; the residual
  (a cross-listing whose name string differs) is stated, not closed.

## 5. The Seeking Alpha input candidate -- measured, not called

`lib/opal_data_harvest/publishers.py:191 seeking_alpha()` loads
`org/tier1_exec/4.0.0_SA_CRO/scripts/sa_rest_fetch.py` through `legacy()`. That module defines 11
functions; minus the 6 that are not endpoints (`_secret`, `build_session`, `_headers`, `get_json`,
`check`, `main`) it exposes 5: `symbol`, `news`, `report`, `analysis`, `article`. None returns a
comparables list. Independently, `build_session()` reads the parked session bundle from Secrets
Manager `seeking-alpha/session` (`:43`, `:74-80`) -- the CRO's session vault. Verdict **ABSENT-ACCESS**,
recorded in every R-1 object's `sa_candidates`, and NO call was made.

## 6. Controls

* **MUTANT** -- `universe.MODEL_BLOCK_CAP_DIVISOR` 1e6 -> 1.0 (the `-W21-S2` defect re-injected).
  FIRED-AS-EXPECTED: 2 of 26 tests fail and the live BABA set collapses to `basis=absent`,
  `members=0`, *"no candidate reaches rung 2: 254 of 2850 candidate(s) share the subject's sector
  ... and NONE sits inside the 0.2x-5.0x size band"*.
* **DETERMINISM** -- two same-input runs of `peers()` for BABA and BA, the run stamp removed, compared
  by sha256: `9b01e06381cc872f` twice and `e8bac37470d1b12c` twice; member lists identical. STABLE.

## 7. What this order did NOT do

No Bloomberg call (AC6 measures 0). No portal edit -- the Peers tab over R-1 is `rj-9`'s. No deploy,
no Terraform, no schedule. `scoped_amgt.py` (chain A's route) untouched. No write outside
`lib/research/peers/`, this deliverables folder and the project's investigation file.
