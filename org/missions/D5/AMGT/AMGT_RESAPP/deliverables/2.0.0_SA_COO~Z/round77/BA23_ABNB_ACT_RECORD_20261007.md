# AMGT_RESAPP round 77 -- `AMGT-ba-23` ACT RECORD: ABNB US Equity registered; BRANCH A; the act stands

`2.0.0_SA_COO~Z`, 2026-10-07 ~13:3xZ. Pair: COO half @a9775de871, CTO half @4eadefc95b (C1, C2, C3).

## C1 -- before the run

- `bloomberg_health` (a session open, no data request), read at 13:21Z under Python 3.11:
  `{'ok': True, 'endpoint': '127.0.0.1:8194', 'service': '//blp/refdata'}`.
- The vehicle: State Ready, LastTaskResult 0.
- `registrations.json` 71 rows; `lib/research/identity` clean in the shared tree.

## The run

`python -m lib.research.identity.add_security --bloomberg "ABNB US" --as-of 2026-10-07 --write-pool`, 13:22:09Z to 13:22:13Z, rc 0:

- `RAW LANDED: s3://opal-data-harvest/bloomberg/harvest/bronze/identity/security_key=ABNB_US_Equity/20261007T132211Z.json ContentLength=373`
- `MEASURED: security_key ABNB_US_Equity bloomberg 'ABNB US' name 'AIRBNB INC-CLASS A' lei '549300HMUDNO0RY56D37' cik 1559720 sec_id '0001559720' composite_figi 'BBG001Y2XS07' AGREES: id token 'US' == Bloomberg EXCH_CODE 'US'`
- `bloomberg_calls 1`, `mode APPEND`
- `OK: uploaded s3://opal-data-harvest/crosswalk/v1/2026-10-07.json ContentLength=748500 document-sha256=887af6e9...929337 schema-version=1 records=243 MEASURED=243 UNRESOLVED=0 registered=50 pool_puts=1`

**BRANCH A.** Not branch B (no UNRESOLVED row), not C (the exchange agrees), not D (no refusal).

## Read-back of the WRITTEN pool object against the re-mint's version `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib`

| read | value | the half's expectation |
|---|---|---|
| new version | **`Y6Tisihmmlm1lCHOO61ci9b726FLXBAI`**, 748,500 B, LastModified 13:22:15Z; the key now holds 2 versions | -- |
| records | 243 | 243 |
| added keys | `[ABNB_US_Equity]` | exactly that |
| missing keys | 0 | 0 |
| records changed among the other 242 | **0** | 0 |
| top-level differences | `denominators` (records, MEASURED, with_association_keys 242 -> 243; registered 49 -> 50) and `research_universe.read_at` (a timestamp) | -- |
| ABNB's record | `bloomberg ABNB US`, `exchange US`, `resolution MEASURED`, `raw_identifier ABNB US`, `source_row.folder None` | -- |
| `resolve()` | ABNB_US_Equity MEASURED (`model_key`); AMD_US_Equity MEASURED (control); CSCO_US_Equity UNRESOLVED (negative control) | -- |

`registrations.json`: 72 rows; the new row `bloomberg ABNB US`, `security_key ABNB_US_Equity`, `resolution MEASURED`, folder None.
Committed @855fdc7324 at once (the pool version and this row roll back together or not at all).

## C2 -- one served read of the new name through the live route (13:23Z)

`GET /api/scoped/amgt/security/ABNB_US_Equity/overlay` by direct invoke of `opal-amgt-scoped-api`, body saved as
`round77/BA23_ABNB_OVERLAY_AFTER_20261007.json`:

- status **200**; `name` `AIRBNB INC-CLASS A`;
- `identity`: `security_key ABNB_US_Equity`, `identity_status MEASURED`, `bloomberg ABNB US`, **`crosswalk_vintage 2026-10-07`**;
- 7 header figures, 7 of 7 `value null`, one reason: "We hold no stored company data for this name yet."

Branch (a): 200 with the uncovered state. It does not present ABNB as a covered name with figures.
**This also settles the re-mint record's open limit in one direction:** the deployed function answered from the 2026-10-07 pool
(it names that vintage and resolves a name only today's object holds), so it is not holding the earlier pool. Why the
`2317_TT_Equity` peers block was byte-equal across the re-mint is then the other reading (a stored peer set); that was not traced.
The body is saved for DSGN_AMGTV1 round 47's "an uncovered name says so once" read.

## C3 -- tomorrow's AMGT_CORPUS fire

Not this seat's read. `2.0.0_SA_COO~X` is told of the six names the key gained today (five by the re-mint, ABNB by this act) and of
the CTO's condition that it print the fire's planned population before 13:00Z on 2026-10-08 beside today's 96.

## What this act did and did not do

- Calls spent under the pair: 1. One identity bronze object, one registration row, one new version of the pool key. No S3 delete.
- ABNB is a pool name the page can resolve and search. It is NOT a covered name and has no model block, filings, peers or posture:
  FWD-2's "same pack" is not reached, exactly as the pair says. That pull is a later act under its own pair and its own
  Bloomberg word.
- Row `AMGT_RESAPP-Z-S363` (BLOCKING for this act): its blocker is cleared by the re-mint and this act; its disposition is the
  CVO's.
