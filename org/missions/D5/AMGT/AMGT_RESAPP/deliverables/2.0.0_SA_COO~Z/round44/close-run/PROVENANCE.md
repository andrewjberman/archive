# AMGT_RESAPP round 44 close run -- the issuer's real run of FWD-30 on the SERVED plane (2.0.0_SA_COO~Z)

- **Deployed artifact:** opal-amgt-scoped-api CodeSha256 `LK9h47juBfZPaAyfztAxDe9z65W2ZtEw6H2IJ/DcO4s=` (rs-2, LastModified
  2026-09-26T11:28:27Z; S3 VersionId `T9JIi3D.nKZ5zd_bNaHzOh4_mQWF8.80`, rollback `VgRYuqQ6UE3y8_4C6l1Rq8wWaXIf4j6K` preserved).
- **Population:** the LIVE research library (C-BACKFILL-DENOMINATOR-IS-THE-RESEARCH-FOLDER), 95 folders, read_at 2026-09-26T13:29:01Z
  (first line of `served_live95.log`). Round 43 read 94 pinned; the 95th (AIA Group) now has an identity and serves.
- **Instrument:** `round44/checks/sweep.py --served --live --require-cases` (the CASES axis graded), rc=0.
- **Result:** served over 95 of 95: OK 95, NOT_OK 0, CAPTURE_FAILED 0; cases page=285 rich=285 same=285 missing=0 extra=0.
- **Currency on the served plane:** of 95 served rich exports, 48 SERVED case lines, 48 of 48 carrying a currency token after the value
  (USD 21, EUR 14, MXN 4, GBp 3, BRL 2, TWD 1, CAD 1, PHP 1, CHF 1). Branch (ii) (quote_currency disagreeing, or CRNCY absent):
  0 in this population -- COVERED BY READING, NOT EXERCISED (CTO condition, msg 26043).
- The lane's own AC2 (msg 26098) read the same numbers independently; this run shares the instrument, not the process.
