# MDPF_TAXSMA.TO-TX-a-1 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-a-1` (decomp s.3, S06, FWD-6) · **branch**
`wk-mdpf_taxsma-1-2f` in `C:/tmp/wk-taxsma-2c` · **cut base** `f8d419c9f0` (the COO's working branch CLOUD at
spawn, per the identity line; `TX-m-4`'s `data/mdpf/scripts/gold/taxsma_assets.py` is drained and present at
this HEAD). **Spec:** `org/missions/D8/MDPF/MDPF_TAXSMA/decompositions/MDPF_TAXSMA_DECOMP.md`@7f65001ab3
(s.3 TX-a-1, s.6 gates, s.8 bounds) and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` v0.5.0 `categories`,
whose enumerations are the only vocabulary used. **Input:** `TX-m-4`'s typed output
(`taxsma_assets.DatedAssetsResult`, imported directly, never re-typed) and `mdpf_category_registry`'s
`sma_basis_of("tax")` / `resolve("tax").view_path`.

Every value below names its instrument, the UTC time it was measured and its denominator.

## 1. What was built

This cell **edits an existing production Gold script**
(`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`) by APPENDING new, pure functions -- **zero
existing lines were changed or removed** (verified by `git diff`, TXA1-AC4 below). Two new sibling imports
(`mdpf_category_registry`, `taxsma_assets`, both same-directory) and `import hashlib` were added; nothing
else at the top of the file moved.

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` (edited, additions only) | `tax_additive_overlay()` -- the TX-a-1 overlay: folds Tax's per-date dollar contribution additively onto a caller-supplied `base_excluding_tax` series, returning the contract's 4 `timeseries_extension_fields` (`aggregate_basis`, `base_excluding_tax_aua`, `tax_additive_aua`, `tax_coverage`) plus a derived `aua_including_tax` (this cell's own field -- see surprise row below); `tax_coverage_entry()` -- one dated coverage cell (`business_active_accounts` + dated expected/covered/unresolved, each with its own date); `tax_additive_for_global()` / `apply_tax_to_global()` -- Global's fixed-key date-join of the one 49financial Tax leaf onto Global's (wider) date axis, preserving `source_basis` through a reconstruction-path lookup; `tax_arithmetic_control()` -- the before/after control with input hashes; `_tax_source_basis_or_raise()` -- an independent re-check of the registry's declared basis, refusing a missing/incompatible one | `git diff --unified=0 HEAD -- <path>`: 0 removed/changed lines |
| `data/mdpf/tests/taxsma/test_taxsma_aggregate.py` (new) | 10 tests, `test_ac1_`..`test_ac10_`, one per criterion; AC6/AC7 are the "(difference)" criteria, each asserting both arms in one test body; synthetic dates and round dollar fixtures only, no real account | `py -3.12 -m pytest data/mdpf/tests/taxsma/test_taxsma_aggregate.py -q`: `10 passed in 1.30s`, 2026-09-21T07:53Z |
| `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_a_1.py` (new) | the criterion probe: one AC per invocation, fresh subprocess, vacuous-pass refused (mirrors `TX-m-4`'s `tx_m_4.py` shape) | 10 of 10 `AC1`..`AC10` invocations below |

**Design decisions this cell makes that the contract does not fix (declared, not hidden -- Rule 24(i)/(iii);
also filed as surprise row `MDPF_TAXSMA-W2-S1`):**
- This file's write surface is the firm/Global AGGREGATE grain only; it carries no SMA/ALT Strategies node
  series of its own (that grain is `mdpf_aggregate_aua.py`/category_views, outside this cell's `<paths>`
  grant). Tax's registered `view_path` (`mdpf_category_registry.SMA_MEMBERS`) is the single unbranched path
  `"SMA > ALT Strategies"`, so "added exactly once at Tax, SMA, ALT Strategies and 49financial" is
  implemented and tested as ONE arithmetic identity on that one path, verified against the registry rather
  than assumed.
- The contract's `timeseries_extension_fields` names 4 fields and no combined total at this grain; this cell
  adds a 5th, `aua_including_tax`, because TXA1-AC2/AC3's "added exactly once" arithmetic is otherwise
  unrepresented and unverifiable.
- These are PURE functions -- no S3 read, no live data (worker bound). `TX-a-2` ("the Tax prelude inside the
  Gold handler, status propagation, run control", S07) is the sequencing cell that reads S02/S19/S03/S04/S05
  and hands the resulting `DatedAssetsResult`s to these functions before 49financial/Global shaping; this
  cell does not read `taxsma_assets`' Gold parquet itself, and `build_firm_timeseries`/`build_global_artifact`
  are not modified or called by these functions.
- `_tax_source_basis_or_raise()` independently re-derives and re-checks `categories.source_basis` at this
  layer rather than trusting `taxsma_assets.check_sma_basis()`'s upstream read alone (contract
  `categories.firm_rule`: "refuse missing or incompatible basis").
- The overlap check (`overlap_dates`) is a caller-supplied set: this cell APPLIES the `overlap_rule` (blocks
  the date), it does not DETECT the overlap (that account-level reconciliation is a different cell's job, not
  reachable from this file's existing aggregated-dollar inputs).

## 2. Gold-suite regression check (bound 17 / worker face instruction)

Measured myself at cell HEAD `f8d419c9f0`, rather than assumed from the decomposition's own number:

| When | Scope | Instrument | Result |
|---|---|---|---|
| BEFORE first edit | `data/mdpf/scripts/gold/tests` | `py -3.12 -m pytest data/mdpf/scripts/gold/tests -q`, 2026-09-21T07:37:53Z | **92 collected, 89 passed, 3 failed** -- exactly the decomposition's stated baseline (s.7/bound 17), same 3 ids: `test_global_fold_flag2.py::test_carry_within_window_carries_and_labels`, `::test_carry_beyond_window_absent_for_real`, `::test_carry_source_is_measured_never_interpolated` |
| BEFORE first edit | `data/mdpf` (full tree) | same instrument, 2026-09-21T07:37:57Z | 196 collected, **193 passed, 3 failed** (same 3 ids) |
| AFTER last edit | `data/mdpf/scripts/gold/tests` | same instrument, 2026-09-21T08:03:06Z | **92 collected, 89 passed, 3 failed** (identical -- this cell adds no file under `gold/tests`) |
| AFTER last edit | `data/mdpf` (full tree) | same instrument, 2026-09-21T08:03:09Z | 206 collected, **203 passed, 3 failed** (+10 = this cell's own new test file; same 3 pre-existing ids, 0 new failures) |

**No regression.** The 3 pre-existing `test_global_fold_flag2.py` failures are unchanged in identity and
count before and after; this cell's 10 new tests all pass; no other test's outcome moved (confirmed by the
identical 89/3 split on the unmodified `gold/tests` scope, and the +10/+0 delta on the full scope).

## 3. Criteria -- 10 of 10 PASS by output

Instrument: `cd C:/tmp/wk-taxsma-2c && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_a_1.py AC<n>`,
run at HEAD `f8d419c9f0` (2 of the 2 files under test dirty -- new/edited, pre-commit; committed in this
order's own commit below), 2026-09-21T08:0xZ. Each run prints its vintage, its measurement, its denominator
and exactly one `VERDICT:` line; rc 0 on all 10.

| id | what | measurement | verdict |
|---|---|---|---|
| TXA1-AC1 | changed 49financial/Global series carry the 4 contract fields, aligned to dates | `test_ac1_...`: 1 passed | PASS |
| TXA1-AC2 | Tax added exactly once at Tax/SMA/ALT Strategies/49financial (single registered path) | `test_ac2_...`: 1 passed | PASS |
| TXA1-AC3 | Global's Tax = sum of firm Tax leaves; Global's total adds Tax exactly once | `test_ac3_...`: 1 passed | PASS |
| TXA1-AC4 | Client and every other firm's series byte-equal to a run without the change | `test_ac4_...`: `git diff --unified=0 HEAD` on the production module shows 0 removed/changed lines: 1 passed | PASS |
| TXA1-AC5 | `source_basis` survives the Global fixed-key + reconstruction path | `test_ac5_...`: 1 passed | PASS |
| TXA1-AC6 (difference) | missing `aggregate_basis` = schema failure; declared path succeeds | `test_ac6_...`: 1 passed | PASS |
| TXA1-AC7 (difference) | overlapping full ID blocks; same fixture without overlap completes | `test_ac7_...`: 1 passed | PASS |
| TXA1-AC8 | unknown/stale Tax nulls dependent totals with coverage; unaffected firms/dates keep values | `test_ac8_...`: 1 passed | PASS |
| TXA1-AC9 | `tax_coverage` carries `business_active_accounts` + dated expected/covered/unresolved, each separately dated | `test_ac9_...`: 1 passed | PASS |
| TXA1-AC10 | same-vintage before/after arithmetic control recorded with input hashes | `test_ac10_...`: 1 passed | PASS |

Full probe transcripts are reproducible via the invocation above; each run's own printed vintage line names
the HEAD short-hash, UTC time and dirty-file count at the moment it ran.

## 4. Surprises

- `MDPF_TAXSMA-W2-S1` (OBSERVATION, INERT) -- filed for the reading of TXA1-AC2 described in s.1's "Design
  decisions" above: the criterion's literal four rollup levels collapse to one arithmetic identity because
  this file carries no SMA/ALT Strategies series, and a 5th field beyond the contract's declared four was
  added to make the addition checkable. `org/missions/D8/MDPF/MDPF_TAXSMA/surprise-channel/investigations/INVESTIGATION_v1.md`.

## 5. Bounds discipline

No egress off Opal infrastructure; no S3 read/write of any kind (every function above is pure, taking data as
parameters); no deploy of any kind (no `aws s3 cp`, `safe-deploy.sh`, Lambda or Terraform touched); no run
against live data (every test uses synthetic dates and round-dollar fixtures, no real account number, name
or balance anywhere in code, fixtures, deliverables or this record); write surface limited to the `<paths>`
grant (the production module, the new test file, and the surprise-channel file) plus this deliverables
folder.
