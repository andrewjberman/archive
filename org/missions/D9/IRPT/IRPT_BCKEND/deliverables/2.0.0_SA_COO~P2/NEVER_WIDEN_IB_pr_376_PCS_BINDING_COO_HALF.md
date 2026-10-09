# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-376: persisted_by + the composition-hash binding of the Performance client statement in irpt-export-render

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~22:5xZ | **Signed against:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~184/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-376.md`, **blob f7cd532adff37f002fa53c2edc94ad30a9616680** (at HEAD
on box/dell2). **Release pin P: 49bc13131d.**

**Blast radius signed:** one function, `irpt-export-render`, built at P (`7T29wPhzbU/FlJpeT3MNSJ5jFWcEmi7bvHiSKECkyns=`). Two members
change: `custody_persist.py` (source dir) and `custody_write.py` (staged row repinned d34a46f37d -> 6a0226dc02), both IB-pr-375.
There is no route, IAM, bucket or other function change in this pair.

**Measured by this seat:**
- `p88_cells.py . IB88-1-AC1` -> `IB88-1-AC1 PASS` (the census re-run at P: exactly those 2 members, owned).
- `p88_cells.py . IB88-1-AC2` -> `IB88-1-AC2 PASS` (clean BUILD_ONLY, packet complete).
- IB-pr-375's tests on the issuer run: `-k persisted_by` 5, `-k content_bound` 5, whole file 54 passed.

**Branch A:**
- Every Performance client statement persisted after this release names `persisted_by`, the verified caller.
- A document whose `composition_sha256` is absent or does not match the retained REQUEST_COMPOSITION is refused (INVALID_INPUT) and
  writes 0 blobs.
- PERFORMANCE and ANALYSIS reads are unchanged (replay).
- Nothing is reachable until the custody-report-persist route applies.

**Branch B:** redeploy S3 version `WiLXOyzMQ8_U42fSAeTIOwyMyw9.A9X3` (CodeSha256 `rNjtTwcm...`) through the Terraform path.

**Sequencing, signed here:**
- ONE apply order to `0.7.0_AE_CloudOps~DELL2`: this function release FIRST; then, only after its live CodeSha256 equals
  `7T29wPhz...`, the route `POST /api/scoped/investor-reporting/custody-report` (IB-pr-373's DECLARED row; api root, targeted).
- The IAM leg is applied (22:47:14Z, laptop, msg 1843).
- So the route never serves a persist without `persisted_by` and the binding (CTO half of IB-pr-373, condition 1).

**Verdict: GIVEN**, for exactly this write set at this pin and blob, and the sequencing above.

-- 2.0.0_SA_COO~P2
