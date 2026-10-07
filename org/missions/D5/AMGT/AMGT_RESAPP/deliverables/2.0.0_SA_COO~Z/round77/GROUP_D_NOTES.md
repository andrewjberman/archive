# AMGT_RESAPP round 77 -- GROUP D draft notes (ba-14 .. ba-18), for the issuer's assembly of s.85

Drafted by a fork of `2.0.0_SA_COO~Z`, 2026-10-07 ~00:5xZ. Nothing is committed. Base: the shared tree HEAD; deployed OVpDhfwD.

## The rectangle rows

| id | cell | slot | wave | class | risk | write surface |
|---|---|---|---|---|---|---|
| `AMGT-ba-14` | FWD-20: the trailing-trend house FCF forecast v1, the sd(D) gate, the reported correlation, the reference labelled bloomberg_reported_period | `~280` | 0 | worker | LOCAL | new `scores/house_fcf.py`; `scores/run_scores.py`; `scores/divergence.py`; new `scores/tests/test_house_fcf.py` |
| `AMGT-ba-15` | the identity grading read (keyed N of 89, residuals named, CORPUS the one resolver) and the ONE PAGER precedence | `~281` | 0 | worker | LOCAL (reads) | new `identity/covered_keyed.py`, `identity/one_pager_precedence.py`, two new tests |
| `AMGT-ba-16` | the comparable as a stated restricted selection with one company counted once; Peers V through one mapping table | `~282` | 0 | worker | LOCAL | `scores/peers_v.py`; `posture/comparable.py`; `posture/tests/test_posture.py`; new `scores/tests/test_peers_v_mapping.py` |
| `AMGT-ba-17` | the CSC contract: period or horizon, currency and source field on the PRESENT columns | `~283` | 0 | worker | LOCAL | `peers/csc.py`; new `peers/tests/test_csc_present_contract.py` |
| `AMGT-ba-18` | the export chart line mirrors the page (none on an undrafted thesis) | `~284` | after ba-11 | worker-light | LOCAL | `print/render_pack.py` (`_thesis_driver_chart_markdown` only); new `print/tests/test_ba18_chart_line.py` |

All paths are under `lib/research/`. Each cell also names its own deliverables directory and the investigation file.

## Measured at the cut

- ba-14: BA_US_Equity's newest model block (20261007T001051Z) carries 10 fiscal years of SALES_REV_TURN and CF_FREE_CASH_FLOW and
  BEST_ESTIMATE_FCF for FY1-FY3. It carries NO dispersion statistic (0 of the six CFPS / EPS statistic mnemonics among 24 header
  and 12 forecast mnemonics), so D cannot be measured from landed data. `house_fcf` does not exist; `score_divergence()` is ABSENT.
- ba-15: the served crosswalk `crosswalk/v1/2026-09-29.json` holds 237 records, 96 with a folder, all 96 keyed; 89 of 89 coverage
  folders are keyed in it. The coverage snapshot's own ticker cells read 34 MEASURED / 55 UNRESOLVED of 89 (the "33 of 89").
  CORPUS registered keys 96; `covered_security_keys()` 95.
- ba-16: a 12-peer set in the scanner vocabulary yields 0 measured z-scores; a deeper-rung member with no factor values is chosen as
  the comparable; the subject's second listing is chosen as its own comparable (fixtures). Row Z-S162: 33 of 33 ABSENT (not re-read).
- ba-17: 5 of 17 CSC columns PRESENT; 0 of 5 carry period_or_horizon, currency or source_field; 12 ABSENT carry derivable_from + reason.
- ba-18: the chart line prints on an undrafted thesis in 4 of 4 fixture states; 0 tests call the function today.

## Edges

- ba-14, ba-15, ba-16, ba-17: no inbound edge. Four chains.
- ba-11 -> ba-18: file contention on `lib/research/print/render_pack.py` (row Z-S218's `:750-757` against the chart line at
  `:1351-1361`). Not a data dependency; the order is staged one wave after ba-11, or folds into ba-11.

## Hookups

- For ba-11 (the adapter cell): NONE from this group. `scoped_amgt._plain_score_record` passes the stored scores record through,
  and the CSC map rides inside each stored peer set. ba-14 and ba-16 are bound to keep the five names it reads.
- For the issuer at the merge (one line, a file no cell of this group owns): `lib/research/identity/build_universe.py:145`
  returns `one_pager_precedence.ordered(folder_path, matches)` in place of `sorted(matches)`.

## Base lines for the issuance commit

```
ba-14 AC1 base: FAIL as expected
ba-14 AC2 base: FAIL as expected
ba-14 AC3 base: PASS as expected
ba-15 AC1 base: FAIL as expected
ba-15 AC2 base: FAIL as expected
ba-15 AC3 base: FAIL as expected
ba-16 AC1 base: FAIL as expected
ba-16 AC2 base: FAIL as expected
ba-16 AC3 base: PASS as expected
ba-17 AC1 base: FAIL as expected
ba-17 AC2 base: PASS as expected
ba-18 AC1 base: FAIL as expected
ba-18 AC2 base: PASS as expected
```

## What a later act owes (not in any cell here)

- The scores producer's real run (`python -m lib.research.scores.run_scores`, a pool write) after ba-14 and ba-16 drain: the served
  Model-tab scores move only then. It is a SERVED act.
- The peer sets' rebuild, for the CSC fields to reach the served table.

## Worker-folder reads in these cells' neighbourhood (row Z-W37-S2's cell)

- `lib/research/identity/crosswalk.py:79` (COVERAGE_PATH_DEFAULT, `0.9.0_WK_AMGT_RESAPP~4/universe.json`), read by ba-15's `run()`
  through `crosswalk.coverage_path()`; ba-15 does not write the file.
- `lib/research/identity/build_universe.py:56,81`; `lib/research/peers/engine.py:83`; `lib/research/posture/packs.py`
  (`0.9.0_WK_AMGT_RESAPP~1/model_block_<key>.json`). None is in a group D write set.

## Open questions for the issuer and the CTO

1. ba-15's premise is stale: the served crosswalk already keys 89 of 89. The cell is cut as the grading read. If the CTO meant a
   crosswalk change, none is left to make; the five identity rows can close on the printed figure.
2. ba-14: with no dispersion statistics landed, D is ABSENT on every name and the sd(D) gate cannot serve. The cell builds the
   forecast, U, Delta, the gate and the correlation, and files one row with the count. Pulling the six fields is a vendor call.
3. ba-17: "currency" for a ratio and for an unlabelled price is read as `none` + reason and `per member` + source.
4. ba-18: one wave after ba-11, or folded into it.
