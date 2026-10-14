# IRPT_DASHBD round 97, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-14 ~00:4xZ)

**One cell, LOCAL:** `DB-b-182` (~148), order `IRPT_DASHBD.TO-DB-b-182.filled-report-shape-stated-and-sample-conformed` (issued @f18be701b9), status `complete`, round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 97`: orders=1, judgment=0). Drained @bf78c7b6bf. On worker ~146's row IRPT_DASHBD-D2-W146-S1. S3 GET and LIST only; zero vendor calls; no served byte moved; counts and hashes only, no client data in the repo.

## What was wrong, and what the cell did

The report contract's `document` layout (0.2.0) never said how a filled report names its accounts or keys its per-account values, so the sample builder and the tested components read it two ways and the real sample could not be rendered. The contract now states the components' reading (version 0.3.0, `document.filled_report`: top-level keys `household` and `values`; account entries `{account_id, last4, first_data_date, window_status}`; per-account and per-class values as `{"by_row": {...}}`; the rule for each window's status and for the first data date), with the 0.1.0 and 0.2.0 bytes in its lineage. The builder (`~141/build_sample.py`) emits it. The private sample was rebuilt for the SAME household (the order asserts the reference hash) and the old file kept beside it.

## What this seat re-ran

- `DB97-1-AC1` PASS; and `DB94-1`, `DB94-2`, `DB94-3`, `DB94-4`, `DB94-5`, `DB94-6` and `DB96-2` all PASS on the shared tree after the drain (the gap-table binding needed my fix below).
- **The builder re-run from fresh S3 reads** (590 reads, no write) gave a sample EQUAL to the worker's rebuilt sample, and the same independent identity tally: 30 of 30 within a dollar (9 of 9, 12 of 12, 9 of 9), window residual checks 16 of 16 recorded apart. The sample holds 3 accounts, 36 per-row members, 117 members (44 filled, 73 absent), window statuses 9 `MEASURED` and 3 `BREAK` (none `NOT_SPANNED`).
- The shape checks of `DB97-1-AC1` were dry-run on 16 synthetic arms.

## Issuer defect found by the worker (row W148-S1), amended

`DB94-1` and `DB94-6` required the gap table's `contract_sha256` to equal the CURRENT contract bytes, so any later contract version failed both though the 117 members and every source were unchanged. The binding now accepts the current bytes or a lineage version, and the totals, per-section counts and the resourced-member count are still compared with the current contract (commit `ac24632028`, no gate limb graded: a check file).

## Worker's other rows (OBSERVATION, INERT)

S2: the order named no chart series; the series are reshaped to name and points with no real-data run, because all three chart members are absent for this household. S3: the `BREAK` rule also covers a `SOURCE_LAG` opening anchor, which the order's sentence did not name.

## Open

- Round 96: `DB-b-180` (the local render of the real sample) is re-seated on the rebuilt sample; `DB-b-181` is drained and its pair is with the CTO. Ledger leg L7 held to the 2026-10-14T11:41Z fire.
- Push state: LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
