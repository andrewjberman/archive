# AMGT_RESAPP round 60 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-01 ~14:3xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.68. **Issuance:** `9b4bf29d32`. **Input:** CTO round-59 analysis @`f03efb5e12`.

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `aj-1` the overlay carries the bar's label | LOCAL | issuer | landed | `9b4bf29d32` (379 passed) |
| `aj-2` its code-only redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete: LIVE 13:59:33Z | proof `1ccf6a59db`; CodeSha256 `E6PdHVFB...` -> `UnSqZgCDkSxM3J3roY8d+iVGZp+8JB1XnM/phfZrmeo=`; CONTENT-DIFF 1 of 350; plan 0/1/0; entry CLOSED |

## The real run on the DEPLOYED function (issuer, independent; round-59 ruling 1: moving fields, not HTTP status)

- `aj_overlay_name.py --where deployed` YES:
  - C0 moved.
  - 94 ranked rows, all keyed.
  - Every overlay's `display_name` equals its row's: 0 of 94 differ (base: 94 of 94 had none).
  - AMD "Advanced Micro Devices Inc" and TSM "Taiwan Semiconductor Manufacturing Co Ltd ADR" as `name`.
  - The shared `identity` block is unchanged (AMD/TSM MEASURED).
- Regressions on the same deploy: round 57's feed (FWD-32/33/34) YES; round 59's price identity YES.

## For the CVO's L8 read

1. The overlay label sits BESIDE the identity block, not inside it. The rj-1 contract (one identity block, identical across routes
   and resolved once) caught the first draft in the test suite. The issuer moved the fields out before the cut.
2. The executor's note: C4 prints no values. Read live, AMD and TSM are MEASURED and a fabricated key is UNRESOLVED, whose top-level
   `name` is None (no ticker fallback is served as a name).

## Rows

None.
