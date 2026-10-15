# D1-S7 resolution evidence -- the 2026-10-14 Bloomberg pull landed (read by 2.0.0_SA_COO~H1, 2026-10-15 ~21:3xZ)

Row: `MDPF_SECHIST-D1-S7` (surfaced 2026-10-15T13:05Z; disarm condition: the first scheduled manifest for as_of 2026-10-14, read by this seat).

## Measured (single named keys, s3://opal-data-etfs/bbg/2026-10-14/)

- `run_manifest.json` head-object: LastModified 2026-10-15T14:33:58Z, 5183 bytes. Body: `as_of` "2026-10-14", `run_class` "scheduled",
  `generated_utc` 2026-10-15T14:33:57Z, `objects_failed` [], 7 objects written. About 3.5 hours after the usual ~11:07Z landing; cause still not read.
- `history_topup.csv`: 180 rows (denominator), columns date, PX_LAST, DAY_TO_DAY_TOT_RETURN_GROSS_DVDS, security. FXFXX rows: 2.
  `FXFXX US Equity` 2026-10-12: PX_LAST 1.0, return 0.0 (the day FWD-9 asked to have filled); 2026-10-14: PX_LAST 1.0, return 0.0105.

## Consequence

- The vendor data carries the FXFXX 2026-10-12 fill. The served page does not yet: the 2026-10-15 13:00Z gold run predates the manifest (14:33Z), so the
  fill reaches the served page at the next scheduled run, 2026-10-16 13:00Z, the same run that opens the FWD-9 served-week read.
- No ad-hoc gold run was taken (the issuer's ruling in the row stands). Read owed at 2026-10-16 13:0xZ+: `r6_week_read.py` and the FXFXX 2026-10-12 cell on the served page.
- The row is the CVO's to dismiss; this file is the evidence, as for D1-S5.
