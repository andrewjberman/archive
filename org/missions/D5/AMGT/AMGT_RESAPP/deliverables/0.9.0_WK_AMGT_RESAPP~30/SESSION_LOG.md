# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~30 -- AMGT_RESAPP.TO-AMGT-rk-18

## What this order asked

ONE run of the filings analyzer and ONE run of the drafting batch over the 33 keyed-coverage names in
`crosswalk/v1/2026-09-15.json`, at approximately USD 36, per ANDREW-DIRECT 2026-09-16 ~19:2xZ ("Yes on all
four, execute them.") -- never the 89-record population, never a cadence, never touching `BA_US_Equity`'s
existing filings document (that regeneration belongs to `AMGT-rk-15`).

## What was measured before running anything

- `crosswalk/v1/2026-09-15.json`: 89 records, 33 carrying a `security_key`.
- Of those 33, only 12 carry a usable EDGAR filing identity (`filing_identity.source == "edgar"` with a
  `cik` and `form_expected`) via `universe/v1/2026-09-16.json`. The other 21 are non-US listings with no
  SEC CIK and were never going to be fetchable by this producer -- `lib/research/filings/batch.py`'s own
  `plan()` partitions them as UNRESOLVED-SOURCE with the reason `"filing_identity.source is 'none': no cik
  and expected form to fetch by"`.
- Of the 12 fetchable names, `BA_US_Equity` already has a document (from the 5-name pilot) and is this
  order's one explicit exclusion.

## The run

Built a local universe document (`.scratch/universe_32_no_ba.json`, never committed -- scratch only) as the
33 keyed names minus `BA_US_Equity`, matching `universe/v1/2026-09-16.json`'s own per-name records. Ran:

```
export ANTHROPIC_API_KEY="$(comp-secrets get anthropic-api-key --reveal | grep '^value:' | sed 's/^value:[[:space:]]*//')"
python -m lib.research.filings.batch --universe .scratch/universe_32_no_ba.json --write-pool
```

`lib/research/filings/batch.py`'s `run_one()` performs BOTH deliverables per name in one pass: it fetches
the filing from SEC EDGAR, calls Anthropic to analyze it (writing `filings/v1/<key>/<accession>.{source,
analysis}.json`), and immediately builds and writes the drafting document
(`lib/research/filings/drafting_build.py`, `drafting/v1/<key>.json`) from that analysis -- so "one run of
the analyzer" and "one run of the drafting batch" are the same invocation here, as the launcher
(`run_batch.cmd`) already does weekly (disabled).

Result (`.scratch/batch_run.log`, never committed): **11 of 11 analyzed, 0 UNRESOLVED-SOURCE, USD 6.2791**
-- ASML_NA_Equity, BABA_US_Equity, COST_US_Equity, HAL_US_Equity, HD_US_Equity, INTU_US_Equity,
KMB_US_Equity, NU_US_Equity, PBR_US_Equity, SAP_GY_Equity, VLO_US_Equity. Well under the ~USD 36 authorized.
`BA_US_Equity`'s filings and drafting objects carry their pre-existing 2026-09-15 timestamps, unchanged.

## Grading

AC1-AC4 PASS as measured (see the proof instance). AC5 (the scheduled-task census) reads **10**, not the
issuer's measured **11**, though none of the three named failure shapes (a new task, a count of 12, or a
previously-DISABLED task found ENABLED) occurred -- confirmed nothing in this order's own session called
`schtasks` at all. Filed as row `AMGT_RESAPP-Z-W30-S1` and graded FAIL per the order's own REFUSAL CLAUSE
(never repaired, widened, or silently passed). The order is left OPEN on AC5; `<status>` is not flipped to
`complete`.

## Commits

One commit: the surprise-channel row (`INVESTIGATION_v1.md`) and this deliverables directory (proof
instance + this log). No `lib/research/filings/` or `lib/research/drafting/` file was edited -- the run used
the producers exactly as they stand.
