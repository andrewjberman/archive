# AMGT_RESAPP.TO-AMGT-s-1 -- THE MODEL BLOCK: session record

**Worker:** `0.9.0_WK_AMGT_RESAPP~1` | **Cell:** AMGT-s-1 | **Outcome:** FWD-1 | **Manifest row:** S1

## What was built

- `integrations/bloomberg/research/model_block_pull.py` -- the two-stage pull/derive script
  (`pull` and `derive` subcommands, each independently re-runnable, C-STAGE-PERSISTS).
- `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~1/`:
  - `select_securities.py` -- the stated, re-runnable rule that picked the two non-control
    securities from AMGT-s-12's universe.json.
  - `build_field_map.py` -- re-measures every mapped field's unit and sign on the three
    securities, reading the RAW bytes back from S3 (F4's method).
  - `field_map.json` -- the re-measured map (32 fields; 28 measured-on-3 for both unit and sign;
    0 fields with an unresolved/inferred status among those 28; 1 reporting-currency finding).
  - `check_landing.py` (AC2), `check_join.py` (AC4) -- read-back-from-S3 checkers.
  - `pull_log.json` -- every security requested (AC7: 3, never more).
  - `model_block_SAP_GY_Equity.json`, `model_block_BA_US_Equity.json`,
    `model_block_BABA_US_Equity.json` -- copies of each security's latest landed derived block
    (AC5).

## The three securities and the selection rule

Per bound (d): the control is named directly by this task order's own text and the CRO's field
map (`SAP GY Equity`) -- **not** read from AMGT-s-12's universe.json, whose own `SAP GY` row is
one of 16 folders sharing an identical, wrong `bloomberg_ticker` value (`AAPL US`; see the
surprise row `AMGT_RESAPP-Z-W1-S1` and `select_securities.py`'s `dropped_as_duplicate_defect`).

The US-domiciled name and the ADR were picked by `select_securities.py`'s stated, re-runnable
rule: keep only `MEASURED` universe.json entries, drop every value shared by more than one
folder (the defect above), classify the survivors by hand-checked domicile/listing-type fact,
and take the alphabetically-first folder in each category. Result: **Boeing (`BA US Equity`)**
for the US-domiciled name, **Alibaba (`BABA US Equity`)** for the ADR.

## Raw-before-derived, the fiscal-year join, and the field map

Both stages ran under the DAPI health check (AC1, re-run immediately before `pull`, per the
bound that "up" is perishable). `pull` landed 6 raw objects (2 per security: `refdata.json`,
`histdata.json`) at `raw/bloomberg/<security_key>/<stamp>/`. `derive` reads those bytes BACK from
S3 (never the in-process pull result), merges the historical rows on the calendar year of `date`
(the fiscal-year join key), and lands `derived/model_block/<security_key>/<stamp>/model_block.json`.
`derive` was re-run twice after the first landing -- once so `model_block.json` could carry the
actual per-field MEASURED unit/sign from `field_map.json` instead of a placeholder pointer, once
more after `build_field_map.py`'s currency-mismatch detector was fixed (see below) -- each re-run
minted a fresh stamp (STORE_CONTRACT.md section 4 rule 1: never overwrite an existing key).
`check_landing.py` reads the CURRENT state (the latest raw and latest derived stamp per security,
STORE_CONTRACT.md section 4 rule 2's own "a consumer reads the latest stamp" rule) and confirms:
raw 6 objects / derived 3 objects / raw-before-derived True / overwrites 0 (AC2).

`check_join.py` independently re-derives the fiscal-year join straight from the raw
`histdata.json` in S3 (never from the derived block) and confirms 10 FY rows and 0 orphan price
rows on all three securities (AC4) -- SAP's own raw response reproduces the CRO's F5 finding
exactly (14 raw rows for 10 fiscal years, 4 years split on the date string; the join merges them
back to 10).

## Two findings this session surfaced (both filed as surprise-channel rows)

1. **`AMGT_RESAPP-Z-W1-S1`** -- AMGT-s-12's universe.json has a measurement defect: 16 of its 48
   `MEASURED` `bloomberg_ticker` entries, across unrelated folders, all read the identical string
   `AAPL US` -- including the folder for this order's own control company, SAP GY. Not this
   worker's to fix (outside `<paths>`); `select_securities.py` excludes every duplicate-valued
   entry before picking, so it never propagated into this order's three securities.
2. **`AMGT_RESAPP-Z-W1-S2`** -- For the ADR (BABA US Equity, fiscal year end 31 March), Bloomberg's
   raw historical response never carries a single row with both a price field and a fundamentals
   field: every year splits a March-dated fundamentals row from a December-dated price/ratio row.
   Grouping by the calendar year of `date` (this order's join rule) satisfies AC4's row-count and
   orphan-count bar exactly, but for this specific security it merges each fiscal year's
   fundamentals with a price observation roughly nine months later, not one at the fiscal period
   end. A self-consistent check (Bloomberg's own `PE_RATIO` vs a naive `PX_LAST/IS_EPS` computed
   from the SAME fiscal-year-merged group) reconciles to 6 decimal places on the control (SAP,
   December FYE) and disagrees by a factor of ~5.9x on BABA -- consistent with a currency
   difference, the ~9-month timing gap, an ADR share-ratio effect, or some combination; **not**
   isolated to one cause here, and not reconciled further (bound (f): state the finding, do not
   guess past what was measured).

## AC8 (judgment) -- answered here, graded at L9

**Pick one figure from the ADR's block: BABA US Equity, fiscal year 2025, `EBITDA_ADJUSTED`.**
The record alone states: `value: 209364.0`, `unit: "MILLIONS"`, `sign: "POSITIVE"`,
`basis: {"mnemonic": "EBITDA_ADJUSTED", "definition": "Bloomberg's adjusted EBITDA (Bloomberg's
own methodology for excluding certain one-off items), millions of the reporting currency."}`,
`vintage: "2026-09-10T23:20:18Z"`, `source: "bloomberg-dapi"`, and (because `EBITDA_ADJUSTED` is
in the currency-sensitive field set) `currency_caveat`, carrying the finding above verbatim.
An analyst challenged "where is that from, on what basis, as of when" can answer all three from
this one record: **where** = Bloomberg DAPI `//blp/refdata`, mnemonic `EBITDA_ADJUSTED`; **basis**
= Bloomberg's own adjusted-EBITDA definition, stated, never a FactSet-style reconstruction;
**as of** = the vintage timestamp, fiscal year 2025. What the record does **not** resolve on its
own -- and says so, via `currency_caveat`, rather than presenting a bare `209364.0 MILLIONS` that
reads as USD because the header block two fields away carries `CRNCY: USD` -- is which currency
those millions are actually in.

**Did a UNIT differ between SAP and the US name or the ADR, and is that recorded per-security
rather than smoothed?** In this measurement, no field's classified UNIT (percent/decimal,
absolute/millions, per-share, ratio) actually differed across the three securities once the
classifier's percent-vs-decimal threshold was corrected (see `build_field_map.py`'s
`classify_unit` docstring: the original `>1.5` cutoff mis-read `EQY_DVD_YLD_IND` on SAP (1.4013)
and `RETURN_ON_ASSET` on Boeing (1.3771) as ambiguous; a real, low, genuine percent reading, fixed
by widening the plausible-percent band to `>=0.3`). `field_map.json`'s `cross_security_findings`
and every field's `finding` key are the mechanism that WOULD record a per-security unit split if
one existed (see `build`'s `unit_out = ... dict(unit_by_sec)` branch) -- it produced zero for
`unit`, and one for the currency/basis question above, which this deliverable treats as the more
consequential difference an ADR can show and did not smooth into one shared convention.
