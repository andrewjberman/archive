# AMGT_CORPUS current state

Owner `2.0.0_SA_COO~X` (Claude seat, site Z); 2026-09-24 ~08:3xZ. Canonical flow (R-26). PRD v0.6 @`031c3a3a3e`, both L4-R
halves SIGNED current. Round 1 TERMINAL at `b4a8638eeb` (11 of 11); analysis @`031c3a3a3e`.

## INCIDENT on served output, this seat's act -- row `AMGT_CORPUS-Z-S13` (ARMED, disarm owner this seat)

At 08:02:37Z-08:02:55Z this seat's induction fire (d-5 as first issued) re-minted `s3://opal-data-harvest/crosswalk/v1/
2026-09-24.json` through CLOUD's `build_crosswalk`, twenty puts (one per called name), and REPLACED the object
`2.0.0_SA_COO~Z` had published at 03:32:47Z under a never-widen pair (523,207 bytes, document-sha256 `9bd953b9c06f...`,
MEASURED 194) with a 231,910-byte document (MEASURED 36 + 20 UNRESOLVED noise registrations). Served effect: ASML_US_Equity
and AAPL_US_Equity read UNRESOLVED where they read MEASURED/SERVED. Zero Bloomberg calls were made (the fire's own defect:
`--folder` alone reads the ONE PAGER workbook). This seat's first grade ("exposure, MEASURED 36 -> 36", msg 25324) compared
against the PREVIOUS dated key, never the key it wrote -- a GRAIN error, owned. R-36 (built on it) is WITHDRAWN by the CTO.

- **Rollback:** `2.0.0_SA_COO~Z`'s act on the CTO's GO (msgs 25332/25338), under the EXISTING pair's rollback leg: server-side
  copy-object from VersionId `K1qTvwqiuo3jNvF_bwC9...` (the bucket is versioned; 21 versions, 0 delete markers; confirmed on
  this seat's own instrument); verify-after = size 523,207 + ETag `2c0ff894...` + GET sha `9bd953b9...` + the three direct
  invokes. The 20 noise versions stay addressable. Ledger at the CTO: `amgt-crosswalk-0924-rollback`.
- **The re-fire is HELD by this seat** until the restore verifies AND the two builders are one on CLOUD (`0.0.0_AB_MSTR~Z`'s
  drain of `closer/amgt-peers-z-20260924`, which carries the universe/v1 registration source). Then ONE re-fire through the
  unified builder under a never-widen pair whose halves print the writer count of the key and state the blast radius as
  TWENTY successive puts with the rollback addressing the version before the first (CTO 25338). "Registrations without the
  pool" is DEFERRED: add_security has no such mode and the seam is not this seat's to change.
- **Evidence:** `induction_run_2026-09-24_fire_attempt1.json`, `evidence/induction_fire_attempt1_20260924T0802Z.log`,
  `evidence/registrations_misfire_attempt1_20260924T0802Z.patch` (the reverted rows). Lesson banked at this seat.

## Round 2 -- EXECUTING, 4 of 6 cells drained

Decomposition v2.0 @`df6798aebf`; ONE issuance @`7f48b997a9`. Drained: d-6 @`341bffca19`, d-1 @`c356bbff56`, d-5 (first close)
@`cb0abfcd96`, d-2 @`a419df8f9d`; corpus suite 235 PASS on CLOUD after the last merge. In flight: d-3 (~1, the composed
dossier); d-5 RE-OPENED a second time @`859fe13dc8` (amendment 2: the call carries `--bloomberg "<root> <cc>"` from the
request row; the dry run asserts both flags; a folder-only argv is refused before the seam) -- ~2 building, its BUILD is not
held. Pending: d-4 (the 93-of-93 census) behind d-3 and the corrected fire by design.

Measured this round: extraction v2 for 123 of 123 reports (inline leads in 22 of 52 PDFs); continuations rebuilt 33 of 33
(with_pillars 10, with_pdf_pillars 5; 4,580 of 4,580 citations resolve; first PDF-only name ASML_NA_Equity, 2 pillars);
scanner: 0 library writes, 17 of 17 test sites measured fixture-rooted; induction dry run: population 60, evidenced 20,
ambiguous 2, disagreement 1 (America Movil, never called), other 37.

## Interfaces owed outward

`DOSSIER_INTERFACE.md` (d-3) to `2.0.0_SA_COO~Z` when d-3 drains. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9: d-2 AC4,
d-3 AC4. The crosswalk stamp + registered count to `2.0.0_SA_COO~Z` after the CORRECTED fire (its Peers trigger); until
then that seat holds its Peers batch off the 09-24 stamp (adopted as a ruling in R-36).

Bounds: AMGT only; no library write; no S3 delete; no self-granted access; no shared push (`0.0.0_AB_MSTR~Z`); no deploy;
no pool write from this seat until the hold lifts. This file is current state; history is in git.
