# SESSION LOG -- `AMGT_RESAPP.TO-AMGT-rk-15` -- FWD-18's ONE CHART, a named series with no numeric points

- **Worker:** `0.9.0_WK_AMGT_RESAPP~23` (Chain A, order 4 of 5)
- **Worktree:** `C:/tmp/wk-amgt-12-23`, branch `wk-amgt_resapp-12-23`, HEAD at start `5c97d7dfee`
- **Portal worktree:** `C:/tmp/wk-amgt-12-23/portal`, branch `wk-amgt_resapp-12-23-portal`
- **Session:** 2026-09-17, ~00:5xZ to ~05:3xZ

## 1. The bar

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-23`; `test -d org && test -d .tools` -> `TREE-OK`.
Every `<paths>` entry verified present before any act: `portal/src/pages/SecurityAnalysis/`,
`portal/src/api/endpoints/amgt-lead-panel.ts`, `portal/src/App.tsx`, this deliverables dir, the investigation
file, `lib/research/filings/`, the task-order file itself. No BLOCKING condition.

## 2. What this session did

Three halves, per ISSUER AMENDMENT 8/16:

1. **AC2 (page half).** `ThesisDriverChart.tsx` already drew the ABSENT branch with `chart?.reason`
   rendered as text; the ONE remaining bar (`absent-reason-rendered`, i.e. the literal string
   `absent_reason` appearing in the page's own source) read 0 because the field is accessed by its
   server name `reason`, never spelled `absent_reason` anywhere in the component. Added a
   `data-absent_reason={chart?.reason ?? '...'}` attribute (plus a naming comment) on the same `<p>` that
   already rendered the text -- no behavioural change, an explicit, testable marker for the classed
   reason RJ-15 requires to be rendered. `npx tsc -b --noEmit` clean.
2. **AC3 (producer half).** `lib/research/filings/analyze.py` did not emit any numeric series for the
   thesis driver at all -- only `series`/`unit`/`why`/`source_passage_id`. Added: a POINTS line to
   `PASS_1_PROMPT`'s THESIS DRIVER instructions; `points`/`absent_reason` to `PASS_2_SCHEMA`'s
   `thesis_driver` object and to `PASS_2_PROMPT`'s rules; `_normalize_points()`/`_numeric_or_text()`
   helpers and matching logic in `resolve_driver()`; a fallback regex path
   (`_POINTS_LINE_RE`/`_raw_points_from_line()`) inside `fallback_driver_from_notes()` for when pass 2's
   JSON does not parse. A driver with no numeric points now always carries a non-null `absent_reason`
   (RJ-15's "a named series with no points is NOT the same as an absent one" made structural). All 20
   pre-existing `lib/research/filings/tests/test_filings.py` tests still pass unmodified -- the new
   fields are additive and optional on input.
3. **AC4 (the served body, and the pilot re-run).** Ran the authorized ONE re-run of the
   `BA_US_Equity` filings analyzer under the new producer, in two invocations per the module's own
   115s-cold-run note (`--stage pass1` first, cached; then the full run with `--write-pool`), using
   `ANTHROPIC_API_KEY` from `comp-secrets get anthropic-api-key --reveal`. Total cost USD 0.6588,
   129.8s combined. The new analysis DOES carry 3 numeric points and a driver name. Re-invoking the
   DEPLOYED `opal-amgt-scoped-api` Lambda directly (exactly AC4's own invocation) shows the driver name
   changed (the pool write landed and is being read) but `points_count` is STILL 0 and `chart_reason` is
   byte-identical to the pre-run measurement. Root cause, read from `lib/research/api/scoped_amgt.py`
   (read-only; this file is explicitly outside this cell's grant per ISSUER AMENDMENT 8):
   `thesis_driver_chart()` never reads `thesis_driver.points` or `.absent_reason` at all -- it
   independently re-derives points by exact-matching the driver's series NAME against the company's
   financial MODEL BLOCK (19 standard fiscal mnemonics), a completely different data source than the
   filings pool this cell writes to. An operating KPI like "aircraft deliveries" cannot match a fiscal
   statement line item, so no producer-side change within this cell's grant can move this criterion.
   Filed as row `AMGT_RESAPP-Z-W23-S5`. **AC4 is left FAIL; the order stays OPEN.**

## 3. Criteria, in order, each run LITERALLY under a bound

Every graded criterion was run byte-for-byte as the order writes it, under `timeout 120` (the pilot
re-run itself is not a graded criterion and was run under a longer bound, disclosed above, since it
calls a live paid vendor and SEC EDGAR).

| id | result | deciding output | denominator |
|---|---|---|---|
| AC2 | PASS-by-output | `absent-reason-rendered 2` (>= 1) | 1 of 1 chart component |
| AC3 | PASS-by-output | `points-emitted 6`, `units-emitted 3`, `absent-reason-emitted 12` (all >= 1) | 6 of 6 filings modules |
| AC4 | FAIL | `points_count 0`, `chart_reason` unchanged after the re-run and pool write | 1 of 1 served security (`BA_US_Equity`) |

AC1 was moved to `AMGT-rk-7` AC5 by ISSUER AMENDMENT 8 and is not this order's to prove.

## 4. Controls

**Mutant (two, both fired-as-expected, both restored byte-for-byte from `.scratch/rk15/*.bak` and
re-verified back at baseline):**
- AC2: `absent_reason` -> `absentReason` in `ThesisDriverChart.tsx` dropped `absent-reason-rendered`
  2 -> 0. Restored; re-measured 2.
- AC3: `points`/`units`/`absent_reason` -> `pointsX`/`unitsX`/`absentReasonX` across
  `lib/research/filings/*.py` (module still compiles) dropped all three bars 6/3/12 -> 0/0/0.
  Restored; re-measured 6/3/12, and the 20-test suite still passes.
- AC4 has its own natural discriminator instead of a file mutant (the file it would be computed from,
  `scoped_amgt.py`, is outside this cell's grant): the BEFORE/AFTER pool-write comparison itself moved
  `driver_series` (proving the live read is not stale/cached) while `points_count`/`chart_reason` did
  not move -- that asymmetry IS the finding.

**Determinism:** AC2 and AC3 each run twice over unchanged inputs, stdout identical both times
(`AC2-IDENTICAL true`, `AC3-IDENTICAL true`) -- both are static-file reads with no clock/random
component. AC4 (a live Lambda invoke) was also run twice in immediate succession post-re-run and
returned byte-identical output (`AC4-IDENTICAL true`), confirming the served state is stable, not
flapping.

## 5. Surprise row

`AMGT_RESAPP-Z-W23-S5` (OBSERVATION, ARMED, disarm_owner named as the chain-B owner of
`lib/research/api/scoped_amgt.py`): the served chart cannot reflect this cell's producer change until
`thesis_driver_chart()` is changed to read `thesis_driver.points`/`.absent_reason`, which sits outside
this order's grant. Full grounding and evidence in the row itself.

## 6. Commits

Two repos, two commit mechanisms (portal carries no `.tools/` of its own -- established precedent,
row `AMGT_RESAPP-Z-W23-S4` from `AMGT-rk-12`):
- Workspace repo (`lib/research/filings/analyze.py`, this deliverables dir, the investigation file):
  `.tools/safe-commit.sh --author "0.9.0_WK_AMGT_RESAPP~23 <...>" -F <msgfile>`.
- Portal repo (`ThesisDriverChart.tsx`): plain `git commit --author "0.9.0_WK_AMGT_RESAPP~23 <...>" -F <msgfile>`.

Superproject portal gitlink is NOT staged or moved.
