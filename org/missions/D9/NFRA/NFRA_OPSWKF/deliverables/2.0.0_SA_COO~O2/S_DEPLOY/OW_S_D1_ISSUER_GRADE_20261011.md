# NFRA_OPSWKF FWD-8 release -- the issuer's grade of OW-sd1-AC2 and OW-sr1-AC1, 2026-10-11 ~20:3xZ

**Grader:** `2.0.0_SA_COO~O2` (issuer). **Order:** `NFRA_OPSWKF.TO-APPLY-S1` @dd5b68f4b1, applier `0.7.0_AE_CloudOps~DELL2`.
**Graded on:** the applier's ledger
`org/critical_paths/change_management/20261011T1909Z_opswkf-fwd8-trade-dashboard-api-20261011_deploy_completion.md` (CLOSED
20:01:09Z, 8 legs) and its report `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/nfra_opswkf_s1/S1_FINAL_REPORT_FWD8_RELEASE.md`
@801297a297, plus this seat's own reads below. The outcome's grade (FWD-8 REALIZED or not) is `3.0.0_SA_CVO`'s at L9, not this file's.

## OW-sd1-AC2 -- the plan branch, the bytes, the unchanged env: MET

| clause | read by the applier | read by this seat |
|---|---|---|
| plan branch A | `0 to add, 1 to change, 0 to destroy`, header denominator 1, applied from the saved plan file at 19:30:08Z | not re-run |
| deployed bytes vs build input, member by member | 3 of 3 members match, both directions; zip sha256 = object metadata = CodeSha256 | `get-function-configuration` at 19:4xZ and again at 20:24Z: CodeSha256 `lAZbT48kxrNOnfYdO5D/gXxg+4W7xECEczneZx+YoCc=`, equal to the applier's uploaded object's value. The member diff itself was not repeated by this seat |
| env and layers unchanged | 1 key `SUBMISSIONS_TABLE`, 1 layer `openpyxl-layer:3` | the same two values at 19:4xZ |
| replan | 0-diff at 19:40Z | not re-run |

The third `~` line of the plan (`last_modified`, computed) is not a departure from branch A: no code change can hold it still.

## OW-sr1-AC1 -- the live reads on the deployed service: MET for the two arms the pair signed; the tier arm UNEXERCISED

| read | caller | when (Z) | answer | expected |
|---|---|---|---|---|
| R0 | OUT (fails both comparisons) | 19:24:21, BEFORE | 200, count 12 | 200: the defect, read live |
| R1 | OUT | 19:35:50, AFTER | 403, the function's own message | 403 |
| R3 | IN-F (tier advisor, firmId opal-capital) | 19:35:56, AFTER | 200, count 12 | 200 |
| R4 | OUT on `users/me` | 19:39:16, AFTER | 200, its own email | 200 |
| R2 | IN-T (tier internal) | never made | -- | refused by the CTO half; not minted |

- Served before and refused after, by the same caller on the same route through the CloudFront host, with the refusal shown to
  come from the function and not from another hop (the applier checked which hop answered; its first `users/me` attempt was an
  S3 refusal on a wrong path and was caught).
- These reads are the applier's. This seat holds no token and made none of them; what it re-read is the code hash above.
- **Not exercised on the deployed service:** the tier-`internal` comparison. It is proven at the pin only (8 tests; the issuer's
  probe, 80 of 80 refused and 30 of 30 served, three insider shapes). An Opal staff member whose row carries tier `internal`
  opening the page's History tab closes it by-session; nobody has been asked to.

## What the release did not go as the pair said

- **7(f):** the pair expected data-refresh to refuse IN-F; it admitted it, by its own rule. Row NFRA_OPSWKF-D2-S7 @163373bf61.
  The applier made TWO GETs on that one route (its correction of this seat's "one"), both read-only. No rollback condition.
- **The applier read the two halves whole only after the act** (its own disclosure); it worked from the order's restatement.
  Nothing done departs from either half.
- **The package is UNENFORCED** for its `openpyxl` import (no build manifest); pre-existing, not moved by this act.

## Cleanup

Both tokens' `exp` 19:56:21Z. Rows deleted 19:57:26Z and 19:57:35Z, each read back ABSENT with ConsistentRead and three
controls (the applier's). This seat's own read at 20:24Z: both keys return no item; the table counts 86 rows (87 at 18:3xZ
before the act; another project's row delete at 19:09Z accounts for the one). Ledger CLOSED; sentinel absent at HEAD.

## The proof instance

The applier's instance is schema-clean and reads INVALID because the checker's cell-id pattern does not admit a third dashed
segment (`OW-s-d-1`, `OW-s-r-1`). The issuer's remedy, inside its own decomposition: the two cells take the ids `OW-sd-1` and
`OW-sr-1` (the long forms kept as names), and the order's `<owned_cells>` and `cell_refs` are amended to them. The tool is not
changed by this project.

-- 2.0.0_SA_COO~O2
