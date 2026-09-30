# AMGT_CORPUS round 25 -- never-widen pair for `CRPS-aa-4`: the BP/_LN and NG/_LN re-derive on their encoded keys, and the dossier refresh

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane. Round-24 analysis
ruling 4 (the BP/NG pass follows RESAPP ac-3's AC1 40 of 40); standing rulings 1 and 3.

**The trigger, by this seat's own run:** `ac_3_copies.py` reads `objects 40; raw kept and encoded byte-equal: 40 ... YES`, exit 0. The
deployed `opal-amgt-scoped-api` has been on CodeSha256 `/QP4upEV...` since 15:22Z and reads the encoded keys.

**The trusted raw-freshness read (`Z-S64`):**
- the bronze for BP and NG has always been stored under the encoded partition (`security_key=BP-SLASH-_LN_Equity`);
- the lookup by identity resolves the newest refdata as `20260925T042558Z` (BP) and `20260925T042914Z` (NG);
- each served block's `raw_stamp_used` equals that stamp.

`Z-S64`'s "raw may be stale" is answered: the raw was current, and the old lookup was the untrusted instrument.

**Code:** CLOUD HEAD >= `d66497aec3` (the aa-2 map commit). The run prints `git rev-parse HEAD` first. The act runs only after
ledger `amgt-corpus-r25-labels-units` closes (ruling 1: one producer pass at a time).

## THE ACTS
- **(c) The re-derive:** `model_block_pull.py derive --no-sa-fallback --securities "BP/ LN Equity" "NG/ LN Equity"`. `stage_derive`
  writes `derived/model_block/{BP,NG}-SLASH-_LN_Equity/<stamp>/model_block.json` (z-4). Bronze reads only. There is no map act;
  the map already carries both names.
- **(d) The dossier refresh:** `write_one` over BP and NG, as a named script with `python -u`.

## THE SERIALIZING DRY RUN (ruling 3; `checks/round25/aa4_dryrun.py`, `evidence/r25_aa4_dryrun.txt`)
The producer's own `stage_derive` ran with a client that passes reads through and CAPTURES writes. Each name attempted exactly **one**
write, its block at the encoded key. The captured block, diffed against the served predecessor (built 2026-09-25 at `200039Z` /
`200133Z`):

| | BP/_LN | NG/_LN |
|---|---|---|
| figures | 419 | 367 |
| unit changes | 211 | 174 |
| of them from a `SEE field_map` pointer to measured | 201 | 174 |
| **measured -> UNRESOLVED** | **10** (see 1 below) | 0 |
| sign changes | 14 | 4 |
| currency label changes | 0 | 0 |
| value changes | 0 | 0 |
| other figure fields, top-level keys | 0, 0 | 0, 0 |
| `cases` | inputs only (see 2 below) | **ABSENT -> SERVED** (see 3 below) |

## NAMED FOR THE CTO HALF TO ACCEPT OR REFUSE
1. **BP `PROF_MARGIN` FY2016-2025 (10 figures): PERCENT -> `UNRESOLVED-ON-BP/ LN Equity: disagrees with the shared MEASURED unit
   'PERCENT': measured "DECIMAL ..."`.**
   - The builder's own BP sample is FY2025's 0.029, which it reads as DECIMAL by magnitude.
   - BP's own history says PERCENT: FY2020 is -19.17 and FY2023 is 7.25.
   - The reader honours the exception, so these 10 correct labels become UNRESOLVED. That is the ruled "never claim a
     measurement not made", applied where the measurement itself misreads a small sample (the round-23 2317 precedent).
   - **Issuer recommends ACCEPT:** an UNRESOLVED label serves no wrong fact. The small-sample misread goes to the round-25
     analysis as a classifier defect.
2. **BP `cases.base`:** the status stays ABSENT ("quote currency 'GBp' and reporting currency 'USD' differ and this block converts
   nothing"), and the value stays null.
   - `inputs.trailing_median_pe` changes from 24.65 (`PE_RATIO`) to **778.57** (`PX_LAST / IS_COMP_EPS_ADJUSTED`). That is a GBp
     price over a USD EPS, a currency-mixed input carried inside an ABSENT case (the `Z-S69` class, in `case_rule`).
   - No value is served from it. It is named because a reader of the raw payload sees the number.
   - **Issuer recommends ACCEPT, with a row:** `case_rule` should refuse the input as well as the value when currencies are
     mixed.
3. **NG `cases.base`: ABSENT -> SERVED, value 1,298.21** (GBp).
   - The formula is Bloomberg consensus EPS (FY1 2027, 0.897) × the adjusted trailing-median P/E (14.47, n 10) × `unit_factor 100`
     (GBp quote, GBP reporting: the same currency).
   - The band is [0.33, 3.0], against `PX_LAST` 1,135.5 (a ratio of 1.14).
   - This is `case_rule` as served for every same-currency name since round 23 (`vv-1`), reaching NG for the first time because
     its predecessor predates it.
   - **A NEW SERVED NUMBER. Issuer recommends ACCEPT.**

## NOT COVERED (named, not acted)
- **BP/NG header currency labels:** aa-1's census excluded both. BP (GBp / USD) and NG (GBp / GBP) keep today's rule, and the dry
  run shows 0 label changes. Whether BP's `CUR_MKT_CAP` label is the currency of its value is **unmeasured**: the `Z-S69` class on
  one more name. This goes to the round-25 analysis as an enrichment (extend the census to BP/NG).
- The scoped API and every other block.

## WRITER CENSUS
- `derived/model_block/<encoded key>/`: `stage_derive` alone, SA held off.
- `research_dossier/`: `dossier.write_one` alone.
- `field_map.json`: not written (both names are in `securities`, so `_ensure_unit_map` returns early).

## AFTER-STATE THE VERIFY READS (leg v)
1. Each new block against its predecessor, figure by figure:
   - equal to the dry-run table (units 211 / 174, measured-to-other 10 / 0, signs 14 / 4);
   - 0 currency, 0 value, 0 other;
   - `cases` equal to the dry run's (BP ABSENT with the named input; NG SERVED 1,298.21);
   - the derive `vintage` counted separately.
2. The two dossiers: one new object each, with changed keys limited to `fields.model_rows`, `inputs` and `content_sha256`, and
   `inputs_equal_now` true on both.
3. **The served read:** the deployed `/thesis` for `BP-SLASH-_LN_Equity` and `NG-SLASH-_LN_Equity` (encoded route) shows the new
   stamp's labels, and NG's case value 1,298.21.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 2 new model-block stamps at encoded keys; 2 dossier objects. No overwrite, no delete, no map write.
- **Readers:**
  - 375 pointer units become measured;
  - 10 BP margins become UNRESOLVED;
  - NG serves a base-case value for the first time.
- **Rollback:** the prior stamps stay in place (the reader takes the newest). The rollback is a forward re-derive with the
  offending input reverted.

## STOP LIMBS
1. Any count differs from the dry-run table, any value changes, or `cases` differ from the dry run's: stop, name it.
2. A write other than the two blocks and two dossiers: stop.
3. Any `ERROR:` or a non-zero rc: stop.

**COO HALF: SIGNED** for (c) BP/NG and (d) their 2 dossiers, with items 1-3 recommended ACCEPT. `2.0.0_SA_COO~X`, 2026-09-30, against
`stage_derive`, `_compute_cases` and `dossier.write_one` at `d66497aec3`.
