# AMGT_RESAPP round 77 -- `AMGT-ba-23` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~13:3xZ

**The act:** the first pull of a company the firm has never covered: `ABNB US Equity` (chosen by CTO ruling msg 30758; the three
reads are in row `AMGT_RESAPP-Z-S363`). ONE command by this seat, in the shared tree at CLOUD HEAD, under the vehicle's
interpreter (Python 3.11 with `blpapi`; row Z-S366):
`python -m lib.research.identity.add_security --bloomberg "ABNB US" --as-of 2026-10-07 --write-pool`

It is step 3 of CTO ruling msg 30760. Step 2, the pool re-mint, landed at 13:15Z (`POOL_REMINT_ACT_RECORD_20261007.md`), so this
act's pool put differs from the served object by ABNB's one record.

## Authority

Andrew-direct 2026-10-06 ~21:1xZ, ruling 1: "the first pull of a company the firm has never covered (FWD-2)", one of three
one-time Bloomberg research pulls, after the firm's 7:00 AM ET pull, one at a time. The vehicle completed today (LastTaskResult 0);
ba-21 and ba-22 are finished.

## What the step does, read from its own code (`lib/research/identity/add_security.py:471-600`, `_mint_pool :395`)

1. No registration exists for ABNB (`_find_existing`): 0 of 71 rows; 0 pool records; 0 identity bronze objects (row Z-S363).
2. Discovery from `"ABNB US"` gives `security_key ABNB_US_Equity`. It is not in today's pool, so no collision branch is taken.
3. **ONE `reference_data(["ABNB US Equity"], IDENTITY_FIELDS)` call**, nine fields: NAME, EXCH_CODE, LEGAL_ENTITY_IDENTIFIER,
   CENTRAL_INDEX_KEY_NUMBER, COMPOSITE_ID_BB_GLOBAL, ID_BB_GLOBAL, ID_ISIN, ID_SEDOL1, COMPANY_WEB_ADDRESS.
4. RAW BEFORE DERIVED: the response lands first at
   `s3://opal-data-harvest/bloomberg/harvest/bronze/identity/security_key=ABNB_US_Equity/<stamp>.json` (a conditional put).
5. One row is appended to `lib/research/identity/registrations.json` (71 -> 72), only after an in-memory crosswalk build with it
   succeeds (`_persist_registration`).
6. **ONE pool put** of the complete document at `crosswalk/v1/2026-10-07.json`: the SAME key the re-mint wrote, overwritten.

"NO DOWNSTREAM STAGE RUNS HERE" (the module's own words): no model block, no battery, no analyzer, peers or posture, and
`universe/v1` is not touched.

## What moves

- **Vendor:** 1 call.
- **Store:** 1 new identity bronze object; the pool key gains a new version.
- **Repo:** `registrations.json` +1 row, committed by this seat right after the run.
- **Served:** the pool object goes from 242 to 243 records; `resolve("ABNB_US_Equity")` reads MEASURED where it reads UNRESOLVED;
  the `/resolve` name search can find the name. ABNB is NOT a covered name (no research folder), so it reads on the page as an
  uncovered pool name does: the header figures are reasoned nulls ("We hold no stored company data for this name yet", row
  Z-S364), until a model block is pulled, which is a different act. FWD-2's "same pack" is NOT reached by this act; it registers
  identity and stops.

## Both branches

- **A. `OK: uploaded ... records=243 ... registered=50 pool_puts=1`.** Read-back by this seat: the new object against VersionId
  `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib`: added keys exactly `[ABNB_US_Equity]`, 0 missing, **0 fields changed on the other 242**;
  `resolve()` on ABNB (MEASURED), AMD (control) and CSCO (negative control); the identity row's name, exchange finding, LEI and CIK
  printed.
- **B. Bloomberg returns no row or an error for the security:** the step prints UNRESOLVED and, under `--write-pool`, registers an
  UNRESOLVED row (`_register_one`, the `"__error__" in sec_data` branch returns `_unresolved_row`); whether `main` then mints
  with it was read from the docstring ("the caller persists rows and mints the pool once per run"), not traced. That would put an UNRESOLVED ABNB row in `registrations.json` and the pool. If it
  happens it is reported at once and comes back to the CTO; the row is not removed by this seat.
- **C. the exchange token disagrees with EXCH_CODE:** recorded by the step, "never smoothed"; the row still lands. Reported.
- **D. the build refuses** (a collision, a schema violation): nothing is put and `registrations.json` is byte-unchanged; if the call
  was already made, its raw object stays as evidence. Reported; not retried.
- **E. any other record differs on the read-back, or the count is not 243:** a wrong object. Rollback the same hour.
- **TERMINAL_DOWN-shaped failure before the call:** the step loads `blp_client` directly; under the wrong interpreter it raises
  rather than calls. It runs under Python 3.11.

## The base, read at signing

| object | value |
|---|---|
| served pool | `crosswalk/v1/2026-10-07.json`, VersionId `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib`, 745,570 B, 242 records |
| `registrations.json` | 71 rows at HEAD; denominators `registered 49` in the pool |
| ABNB identity bronze | 0 objects |
| same-day writers of the key | `2.0.0_SA_COO~X` was told at 13:15Z; its induction step read `pool_puts 0` today |

## Writers counted (NEVER-1)

The pool key: one rule (`crosswalk.write_pool`), this run its only caller for the put. `registrations.json`: one writer,
`_write_registrations`, this run. The identity bronze prefix for ABNB: this run.

## Rollback per key

- **Pool:** copy-object of VersionId `1b0PNH1yqkGnLoyRbOHwEZTxBleOBxib` onto the same key (the bucket is versioned; no delete). Not
  exercised.
- **`registrations.json`:** revert the one-row commit. The two must roll back together: a pool without the row, or a row without
  the pool, makes the next mint by any seat re-add or drop ABNB.
- **Identity bronze:** kept; it is evidence and nothing reads it but the registration.
- **The call:** cannot be rolled back.

## Not covered

- ABNB's model block, filings, peers or posture: FWD-2's pack is a later act with its own pair and its own Bloomberg word.
- Any second security. Any `--retire`. Any S3 delete.

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~13:3xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`.
