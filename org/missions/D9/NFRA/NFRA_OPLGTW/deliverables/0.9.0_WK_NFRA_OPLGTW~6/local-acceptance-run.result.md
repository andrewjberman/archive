# NFRA_OPLGTW.TO-OG-v-2 -- local integrated acceptance run: result (RE-HAND, LAST)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~6` | **Worktree:** `C:/tmp/wk-oplgtw-6f` (branch `wk-nfra_oplgtw-6f`, HEAD @e3d6c48ffd)
**Proof:** `NFRA_OPLGTW.TO-OG-v-2.local-acceptance-run.proof_of_spec.json` (this folder) -- validate with
`py -3.12 .tools/proof-of-spec-check.py <instance> OGV2-AC1,OGV2-AC2,OGV2-AC3,OGV2-AC4,OGV2-AC5` (VALID rc=0).
**Order `<status>`: left `pending`** -- OGV2-AC4 FAILS by output (a real defect in code outside this cell's
`<paths>` grant); BOUNDS: "Flip `complete` only when every MECHANICAL criterion PASSES by output."

## What this (last) re-hand did

Everything OGV2-AC2 was waiting on had already landed at this cell's HEAD; two items in this cell's own
`<paths>` needed repair against the now-current app behaviour:

1. **`test_ogv2_a06`'s post-revocation assertion** (`:488` at the prior HEAD) read the query-engine's nested
   `{"error": {"code": ...}}` shape. `OG-z-4` (this cell's own earlier order) wired the dispatch guard
   (`app/tools.py` `_PolicyGuardedMCP.call_tool()`) to set MCP `isError=True` on a guard denial; a **full
   revoke** now denies **at the guard** (`app/data_entitlement.py`'s flat `_denial()` dict: `{"error": "<reason
   text>", "guard_denied": true, "code": "<snake_case>", "error_code": "<CONTRACT CODE>"}`), not inside the
   query engine, so `payload["error"]` is a STRING there, not a dict -- `payload["error"]["code"]` raised
   `TypeError: string indices must be integers, not 'str'`. Fixed by reading `payload["error_code"]` instead,
   the guard's own contract-code field (confirmed by measurement: `payload={'error': "the principal's
   restricted profile is revoked (revision 5) does not include tool 'schwab_query'", 'guard_denied': True,
   'code': 'entitlement_denied', 'error_code': 'ENTITLEMENT_DENIED'}`).
2. **`test_ogv2_a18`'s empty-match aggregate control** asserted an ungrouped `sum(quantity_settled_unsettled)`
   succeeds with a null total. `OG-q-4`'s `semantics.assert_quantity_sum_grouped` wiring now refuses that
   shape outright (`INVALID_REQUEST`/`quantity_sum_ungrouped`) before the (empty) match is ever evaluated --
   PRD C3: "Quantity sums require grouping by CUSIP and long/short indicator." Flipped to expect the refusal,
   citing the same clause `test_schwab_query.py::test_ogq2_ac07` (`:503`) and `::test_ogq2_ac15` (`:762`)
   already cite for their own ungrouped-sum controls (R-OG-15, row `NFRA_OPLGTW-W5-S10`).
3. **Re-graded OGV2-AC2 WHOLE** against all 13 machine A-rows at this HEAD, and re-ran AC1, AC3, AC4, AC5 so
   every row in the proof instance is one vintage (`@e3d6c48ffd`).

## Criteria

| id | invocation (relative to `<WS>`) | result |
|---|---|---|
| OGV2-AC1 | `pytest .../test_local_acceptance.py::test_ogv2_ac01` | **PASS** -- `1 passed` |
| OGV2-AC2 | `pytest .../test_local_acceptance.py -k "test_ogv2_a"` | **PASS** -- `14 passed`, 0 failed |
| OGV2-AC3 | `pytest .../test_local_acceptance.py::test_ogv2_ac03` | **PASS** -- `1 passed` |
| OGV2-AC4 | per-module loop over `tests/test_*.py` (25 modules) | **FAIL** -- `MODULES: 25 FAILED-MODULES: 1` (`test_schwab_query.py::test_ogq2_ac06`, `::test_ogq2_ac20`) |
| OGV2-AC5 | `pytest .../test_local_acceptance.py::test_ogv2_ac05` | **PASS** -- `1 passed`, 56 S3 calls, 0 violations |

### OGV2-AC2 -- the A-row census, now clean

**Denominator: 13 of 13** OG-v-1 census rows marked `operated_by: machine` whose instrument is `OG-v-2`
are built as tests and pass (A2 as `OGV2-AC3`; A3,A4,A5,A6,A8,A9,A10,A11,A12,A17,A18 as `test_ogv2_a<nn>`,
plus OGV2-AC1/AC3/AC5 swept in by the `-k "test_ogv2_a"` substring). **A14 stays correctly out of scope**:
its machine half is graded_by BOTH `OG-v-2` AND `OG-r-2` (a host measurement `OG-v-2` alone cannot make).

Both of the prior round's two open A-row defects are now closed:

- **A6** (`test_ogv2_a06`): the partial-grant `dim_asset` CUSIP restriction now matches EXPECTED exactly
  (`['SYN000001', 'SYN000002']`) -- `NFRA_OPLGTW-W6-S8`'s gap has been wired by an intervening cell. The
  post-revocation sub-check (this round's own repair, above) now also passes.
- **A8** (`test_ogv2_a08`): not separately re-verified this round beyond the full `-k "test_ogv2_a"` sweep,
  which shows it passing with no assertion output flagged -- `NFRA_OPLGTW-W6-S6`'s refusal gap has also been
  wired by an intervening cell (OG-q-4).
- **A18** (`test_ogv2_a18`): this round's own repair (above) -- Unicode measure, paging, and paged/un-paged
  aggregate agreement all still match EXPECTED; the empty-match ungrouped-sum sub-case now correctly expects
  a refusal instead of a null-sum success.

## OGV2-AC4 -- still blocked, outside this cell's grant

`MODULES: 25 FAILED-MODULES: 1`, invariant across a same-session re-run for determinism: `test_schwab_query.py`
fails on `test_ogq2_ac06` and `test_ogq2_ac20` both times. This is **not a new defect** -- it is the same
class rows `NFRA_OPLGTW-W5-S19` and `NFRA_OPLGTW-W5-S20` already ground and ARMED (disarm_owner
`2.0.0_SA_COO~O`): `TO-OG-q-6`'s R20/R24 wiring correctly refuses the pre-wiring shapes those two tests still
assert succeed (a `group_by` including `business_date` inside the 10-field limit, and a one-page duplicate
source grain). This worker's HEAD already carries `2.0.0_SA_COO~O`'s own `reopen+amend(NFRA_OPLGTW.TO-OG-q-6)`
commit granting `test_schwab_query.py` back for exactly this pair (`@1529bcd131`), but that order's fix has
not drained at this HEAD. `test_schwab_query.py` is **not** in this cell's `<paths>` grant
(`infra/aws/ec2/opal-gateway/tests/acceptance/test_local_acceptance.py`,
`infra/aws/ec2/opal-gateway/tests/acceptance/conftest.py`, and this cell's own investigation file only), so it
cannot be repaired here. Recorded as a FAIL measurement; filed as row `NFRA_OPLGTW-W6-S10` (BLOCKING for
this criterion, citing W5-S19/W5-S20 rather than re-diagnosing the same class).

A second run this session, for determinism, reproduced the same `test_schwab_query.py` pair **plus** one
additional, different module failing on a pre-existing, already-filed flaky cause: `test_schwab_export.py`'s
`test_ogx1_ac01` (`NFRA_OPLGTW-W6-S9`, OBSERVATION/INERT -- a `secrets.token_urlsafe(32)` ticket occasionally
contains the substring `s3`/`amazonaws` by pure chance). The `test_schwab_query.py` pair is the STABLE,
reproducible failure both runs; the export flake is not, and is not re-filed here since S9 already grounds it
exactly.

## Surprise rows filed this order

- `NFRA_OPLGTW-W6-S10` -- OGV2-AC4's whole-glob sweep is still blocked by the already-ARMED `W5-S19`/`W5-S20`
  defect (`test_schwab_query.py::test_ogq2_ac06`/`::test_ogq2_ac20`), re-measured at this cell's HEAD.
  BLOCKING (for OGV2-AC4), ARMED, disarm_owner `2.0.0_SA_COO~O` (carried from W5-S19/S20, not a new hazard).
- (Not re-filed, already grounded: `NFRA_OPLGTW-W6-S6`, `NFRA_OPLGTW-W6-S8` -- both now disarmed on the live
  path, confirmed by this round's own green A6/A8 measurements; `NFRA_OPLGTW-W6-S9` -- reconfirmed identically
  on this round's second AC4 run, not re-filed.)

## Mutant / determinism controls

See `controls` in the proof-of-spec instance: the single-edit mutant on `test_ogv2_ac01` (carried unchanged
from every prior round) still fires and restores byte-identical (sha256
`75ce95163b592c42f3bc326be11eb1fbd0efc907764ad13590a5f83611fcb1e5`). This round's own two fixes are each a
live discriminator: `test_ogv2_a06`'s `payload["error_code"]` read raises `KeyError` if that field is ever
dropped from the guard's denial shape; `test_ogv2_a18`'s flipped assertion fails if the ungrouped-sum refusal
is ever removed and the old null-sum success shape returns. OGV2-AC1/AC3/AC5 and the AC2 selection were each
run standalone; OGV2-AC4's full loop was run twice -- the graded defect (`test_schwab_query.py`) is STABLE
across both runs; the unrelated `test_schwab_export.py` flake is not, matching `W6-S9`'s prior finding on the
same test.
