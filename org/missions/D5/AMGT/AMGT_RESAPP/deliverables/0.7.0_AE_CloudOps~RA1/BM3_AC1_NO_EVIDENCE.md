# AMGT-bm-3 -- AC1 reads NO (5 of 7): the failing arms are pool movement, not the code

**Seat:** 0.7.0_AE_CloudOps~RA1. **Apply:** 2026-10-14T13:00:37Z-13:01:39Z, LastModified 13:01:34Z, CodeSha256 `UIkRgr9gbz2RbsaOJq2uRe3aZPOgNE/YoCAG6j7HyO4=` (was `0pWc69Vd..`).
**Pre capture:** 12:58:25Z-12:59:17Z (95 names). **AC1 run:** 13:02:19Z-13:03:14Z, then re-run 13:03Z.

## AC1 as printed
`names 95 | captured forward P/E rows 278 | deployed 218 | withheld 60 (population 60) | names with a withheld row 20 | status not (200, 200): []`
PASS F1, PASS F3, PASS F4, PASS F6, PASS F7; **FAIL F2, FAIL F5**; `R106 FORWARD PE DEPLOYED: NO (5 of 7 arms)`, exit=1.
The withhold itself is exactly as signed: 218 served, 60 withheld on 20 names, equal to the population; PBR US names USD and BRL; the AI-fill hold is intact on all 95.

## Why F2 and F5 fail: the live pool was refreshed between the capture and the read
- A kept row, ADBE US FY1: capture `value 9.8914`, `vintage 2026-10-12T13:01:34Z`; live `value 9.6476`, `vintage 2026-10-14T13:02:29Z`. Its `check_face[4]` (header PX_LAST) moved 242.27 -> 236.28; 9.6476/9.8914 = 0.9754 and 236.28/242.27 = 0.9753.
- Capture versus deployed with the BEST_PE_RATIO rows set aside, read 13:12Z: **73 of 95 names differ**, on `fiscal_year_figures[].vintage` (48,972 paths), `header_figures[]`/`check_face[]` values, `model.cases.base.px_last`, `consensus_eps` and `ratio_to_px_last`. Of 176 kept P/E rows on those names, 154 move by the PX_LAST ratio within 0.5%; the rest follow a consensus-EPS change.
- The writer is the harvest runner `0.7.0_AE_CloudOps~ZW` armed with `--refresh-once` (its log `zw_harvst_bz10_refresh_once_repin.md`: "working through bbg, a job every ~2.5 minutes"). The order's "no other reader" holds; a concurrent WRITER was not in the pair.

## The same-pool control (deployed function against the pin's own handler, adjacent reads, 95 names)
`E3: names 95, status not (200,200): [], names with any non-clock/non-float diff: 95`, and the ONE distinct path is `.ai_fill.reason` on all 95 -- the Windows path-separator artefact the COO half names ("expected live: zero" on the function; the local handler on this box prints `\\`). **No other path differs.** The deployed function serves the pin's code, byte for byte on the same pool.

## What this seat has NOT done
Rolled back. Branch 2 reads "any other change ... rolls back the same hour unless the CTO names KEEP on the evidence". This seat reads the diff as data, not code, but KEEP is the CTO's to name. Rollback clock: apply 13:01Z, so 14:01Z. Rollback path, ready: the hash-checked reference package of the old function (`0pWc69Vd..`, S3 VersionId `rej6Dql_iS20E55Rw435SSXRw0Z78wRL`) or a rebuild from `0447f2df38`; applied with the hold-carrying Terraform (C1), one `safe-apply`.
AC2 and AC3 are run next and reported separately.
