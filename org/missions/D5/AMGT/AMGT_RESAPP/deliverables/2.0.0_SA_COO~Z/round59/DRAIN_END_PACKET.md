# AMGT_RESAPP round 59 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-01 ~12:5xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.67. **Issuance:** `e52b6d1bb5`. **Input:** CTO round-58 analysis @`9e4c311cfc`
(DEMO-BLOCKING).

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `ai-1` the serve-time price identity join | LOCAL | issuer | landed | `e52b6d1bb5` (378 passed) |
| `ai-2` its code-only redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete: LIVE 12:34:04Z | proof `a30a3443fc`; CodeSha256 `g9H0TW2g...` -> `E6PdHVFB9z1xUcvCRtNIALjgAaCzNtolAdzaKmCssvM=`; CONTENT-DIFF 1 of 350; plan 0/1/0; entry CLOSED |
| `ai-3` af-6 grade + ledger close | -- | issuer | landed in round 58 (`3373f73c27`) | `round58/ah3_af6_grade_branchA.out` |

## The real run on the DEPLOYED function (issuer, independent of the executor)

- `ai_price_identity.py --where deployed`: YES. C0 moved. TRENDING and BREAKOUT each serve 94 rows: 0 unkeyed (base 62), 0 without
  `display_name` (base 94), 0 raw-key labels, every key covered, `score_pct` kept. Rows with a company `name`: 70 of 94 (base 36).
- Regression (`ag_1_served.py --what post`): FWD-32/33/34 YES.
- Overlay click-through: AMD_US_Equity and TSM_US_Equity return 200 with `identity_status` MEASURED. A fabricated key also returns
  200, but with `identity_status` UNRESOLVED: per row Z-S332, the 200 alone does not discriminate, and `identity_status` does.

## For the CVO's L8 read

1. The CTO half's condition 3 ("a 200 on AMD's and TSM's overlay") was a non-discriminating control: a fabricated key also returns
   200. The executor caught it (Z-S332), and the grade reads `identity_status` instead. The defect is in this issuer's and the CTO's
   wording, not in the act.
2. The join is serve-time only: the 09-30 generation still stores 62 unkeyed rows, and the producer is unchanged (ruling 2). The
   producer-side identity is a later enrichment, not a Friday need.

## Rows

Z-S332 (INERT; the overlay-200 control wording).
