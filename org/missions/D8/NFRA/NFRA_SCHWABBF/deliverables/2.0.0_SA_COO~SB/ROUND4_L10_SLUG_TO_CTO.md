# NFRA_SCHWABBF round 4 -- L10 slug to 1.0.0_SA_CTO

**From:** `2.0.0_SA_COO~SB`, 2026-10-20 ~18:2xZ. **Round:** 4 (the SILVER tier on the firm form; decomposition `decompositions/NFRA_SCHWABBF_DECOMP_R4.md`, issuance `0429204ae7`).
`round-close-check --round 4`: 5 orders, 5 complete, proofs 5 of 5 valid, `verdict=MAY-CLOSE`. Nothing deployed, applied or moved.

## Delivered (merged on `box/laptop`)

| cell | merge | what exists |
|---|---|---|
| BF-s-4 | `cdce7d6d13` | the converter family writes, reads back, lists and guards silver at `schwab/<firm>/silver/<table>/date=D/<master>.parquet` for the five firm-form masters; 0824/0833 byte-for-byte as before (proven against the pre-round code); five vendored twins byte-equal; `silver_registry.py` (shared) untouched; 16 new tests, family suite 161 passed |
| BF-m-4 | `f6078a5d99` | the move tool carries the silver tier for 08403355 (copy with rename, sha-verified, no delete); live read-only plan: **7,581 silver keys over 18 tables, 0 unrecognized** (per-table counts in the order report) |
| BF-e-4 | `625a8f12c6` | the equality tool captures old-form silver and reads firm-form silver after the cutover; 25 tests |
| BF-t-4 | `c2fff0d006` | the trace locates silver by the same form rule and flags a silver second form; 32 tests |
| BF-i-4 | `16d4ae3ea0` | the converter role's firm silver write grant, enumerated per master (08403355 and the four Cottonwood), no folder wildcard, no delete |

Merged-tree checks: `data/canonical/schwab/tests` 820 passed; converter-side 161 passed; `py_compile` clean; five twins equal.

## Rows and rulings

0 ARMED. Ruled inside the decomposition: W4-S8 (my AC3 expectation did not match the verdict line's real shape; amended `81c1eba37d`), W1-S5 (the silver key rule lives in `conversion_manifest.py`, not a pyarrow leaf), W2-S8 (the silver plan also lists the destination so a re-plan reports `already`). Carried for round 5: the bronze live plan has the same destination-listing gap (`already` is unreachable in a live bronze re-plan); BF-x-5 fixes it.
Process finding: another lane's uncommitted row in the shared channel file blocked every merge until it was committed (`75954ecb20`); line-ending churn in the channel file from the Edit tool had to be reverted on two worker branches.

## Next

Round 5 (meta and `_ops` as the state tier in the firm bucket) is cut now against the merged code; its contract is in `decompositions/NFRA_SCHWABBF_DECOMP_R5.md` (your rulings 109966 and 109970). The release acts follow rounds 5's merge, the gateway edit and Andrew's confirmation of the old-key delete.
