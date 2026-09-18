# NFRA_OPLGTW.TO-OG-v-2 -- local integrated acceptance run: result (RE-GRADE, ALL PASS)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~6` | **Worktree:** `C:/tmp/wk-oplgtw-6f` (branch `wk-nfra_oplgtw-6f`, HEAD @372b1d653d)
**Proof:** `NFRA_OPLGTW.TO-OG-v-2.local-acceptance-run.proof_of_spec.json` (this folder) -- validate with
`py -3.12 .tools/proof-of-spec-check.py <instance> OGV2-AC1,OGV2-AC2,OGV2-AC3,OGV2-AC4,OGV2-AC5` (VALID rc=0).
**Order `<status>`: flipped to `complete`** -- every mechanical criterion PASSES by output at this HEAD.

## What this re-grade did

No amendment was made to this order and no criterion changed. This worker's blocker from the prior round,
row `NFRA_OPLGTW-W6-S10` (OGV2-AC4 blocked by `test_schwab_query.py::test_ogq2_ac06`/`::test_ogq2_ac20`,
the same class as the already-ARMED `NFRA_OPLGTW-W5-S19`/`W5-S20`), is REPAIRED at this worker's new HEAD:
`TO-OG-q-6`'s re-open commit `244771637d` flipped both tests to expect the contract's refusal, its drain
landed at `e58d9d2b04` (issuer-measured `test_schwab_query.py` 25 passed, `test_schwab_c3_rules.py` 4
passed, `tests/acceptance/test_local_acceptance.py` 14 passed, all on the shared tree). This worker's
worktree fast-forwarded to `CLOUD @372b1d653d` carries that drain.

No files in this cell's own `<paths>` grant needed further change. All five criteria were re-run fresh at
this one HEAD so every row in the proof instance is measured at one vintage.

## Criteria (all re-run at HEAD @372b1d653d)

| id | invocation (relative to `<WS>`) | result |
|---|---|---|
| OGV2-AC1 | `pytest .../test_local_acceptance.py::test_ogv2_ac01` | **PASS** -- `1 passed in 2.39s` |
| OGV2-AC2 | `pytest .../test_local_acceptance.py -k "test_ogv2_a"` | **PASS** -- `14 passed in 21.75s`, 0 failed |
| OGV2-AC3 | `pytest .../test_local_acceptance.py::test_ogv2_ac03` | **PASS** -- `1 passed in 2.11s` |
| OGV2-AC4 | per-module loop over `tests/test_*.py` (25 modules) | **PASS** -- `MODULES: 25 FAILED-MODULES: 0` |
| OGV2-AC5 | `pytest .../test_local_acceptance.py::test_ogv2_ac05` | **PASS** -- `1 passed in 3.23s`, 56 S3 calls, 0 violations |

### OGV2-AC2 -- the A-row census, unchanged from the prior round's clean state

**Denominator: 13 of 13** OG-v-1 census rows marked `operated_by: machine` whose instrument is `OG-v-2`
are built as tests and pass (A2 as `OGV2-AC3`; A3,A4,A5,A6,A8,A9,A10,A11,A12,A17,A18 as `test_ogv2_a<nn>`,
plus OGV2-AC1/AC3/AC5 swept in by the `-k "test_ogv2_a"` substring). A14 stays correctly out of scope
(machine half graded_by BOTH `OG-v-2` AND `OG-r-2`, a host measurement this cell alone cannot make).

### OGV2-AC4 -- now clean: `MODULES: 25 FAILED-MODULES: 0`

The prior round's blocker (`test_schwab_query.py::test_ogq2_ac06`, `::test_ogq2_ac20`, rows
`NFRA_OPLGTW-W5-S19`/`W5-S20`/`W6-S10`) is repaired at this HEAD by `TO-OG-q-6`'s own re-open and drain
(`244771637d` -> `e58d9d2b04`), which this worktree's fast-forward to `CLOUD @372b1d653d` carries. The
per-module loop over all 25 glob-derived `tests/test_*.py` modules (the one known red test of row
`NFRA_OPLGTW-S1` deselected by name, as the criterion's own amended invocation requires) reads
`MODULES: 25 FAILED-MODULES: 0` -- 0 of 25 modules failed. No repair was made in this cell; the fix
belongs entirely to `TO-OG-q-6`'s own grant.

## Surprise rows filed this order

None. No new surprise this round. The prior round's row `NFRA_OPLGTW-W6-S10` is not edited (rows are
append-only and never edited); its blocking condition no longer holds at this HEAD per the re-measurement
above, and its own disarm (disarm_owner `2.0.0_SA_COO~O`) remains that seat's act, not this worker's.

## Determinism

OGV2-AC1, AC2 (selection), AC3, AC4 (full loop) and AC5 were each run once this round -- unlike the prior
round, no second AC4 run was needed to distinguish a deterministic regression from an unrelated flake,
because AC4 passed cleanly on its one run. The mutant/determinism controls recorded in the proof
instance's `controls` block for this round's AC1 (byte-identical sha256 before/after a reverted mutation
on `test_ogv2_ac01`) are carried unchanged from the prior round -- the file was not touched this round.
