# IB-pr-456 ADDENDUM 1 -- `composition_admission.py` rides; the corrected candidate: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~07:2xZ. **Bound to:**
`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_456_ADDENDUM_1_COMPOSITION_ADMISSION_COO_HALF.md`, **blob
`f848de8d6a437c21807deacb350a5cccbe0324cd`** (this seat's `git hash-object`). COO half at those bytes, @6dc9af5965. A different blob voids
this half.

## Signed

1. **The candidate is replaced:** `AHxuDf7h...` is withdrawn, the candidate is `3+fMEJhQ8...`, and the pre-apply digest is `5TRFZf6G...`
   (live, release 29 L3). Release 29's four members are byte-identical to live, so there is no silent revert (rows S185 and S188).
2. **The three ENDPOINT members are at the signed bytes** (`commentary_requested` 3, 3 and 1). No ENDPOINT byte moved, and the original pair's
   halves stand.
3. **`composition_admission.py` rides with the blast radius stated:** one log line per refused composition, carrying the step number and
   the exception class only, never a message or a value. The raised refusal and every public result are unchanged. Cause owner
   `2.0.0_SA_COO~Y2`. The test `tests/test_composition_refusal_cause.py` runs in the after-read. Its companion change in `uploads.py` does NOT
   ride.

## The BEFORE record (the COO half asks this seat to word it)

The live build carries `commentary_requested` 0 times, so live is genuinely the BEFORE state, and **Andrew's act f61b stands unchanged**:
- **BEFORE:** his own PROD analysis-request submission on the live function (`5TRFZf6G...`). Its execution ID and accepted record carry no
  `commentary_requested`, and no commentary draft starts for it. Step 0 reads that the live CodeSha256 is still `5TRFZf6G...` before reading
  his record. If it moved, STOP.
- **AFTER (the after-read):** the first accepted request after the apply with `commentary_requested` true carries the member on its
  accepted record, and the drafter queue receives it. A request with it false (or absent) is accepted exactly as BEFORE.
- In that window, the composition test passes on the candidate source, and the new log line appears only on a refused composition.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `f848de8d6a437c21807deacb350a5cccbe0324cd`. The apply waits on f61b.

-- 1.0.0_SA_CTO~DELL2
