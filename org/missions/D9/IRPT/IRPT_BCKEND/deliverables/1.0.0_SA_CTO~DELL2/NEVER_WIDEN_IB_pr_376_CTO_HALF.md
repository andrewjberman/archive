# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-376: irpt-export-render carries persisted_by and the composition-hash binding

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~22:5xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 1847 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~184/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-376.md`,
**blob f7cd532adf**. The COO half is @66c617a5c7. Pin P = `49bc13131d`.

## Measured by this seat

| Read | Result |
|---|---|
| `release-census.py irpt-export-render --pin 49bc13131d` | 66 built, 66 live, `changed_members=2`: custody_persist.py and custody_write.py. Matches the packet; no rider |
| live `get-function-configuration` | CodeSha256 `rNjtTwcm...Xvf6Ek=`, LastModified 22:11:43Z, CodeSize 414177. Matches the packet's Branch B |
| `list-object-versions` on the artifact key | latest is `WiLXOyzMQ8_U42fSAeTIOwyMyw9.A9X3` (22:07:05Z, 414177 bytes), which is the rollback version the packet names |
| IAM leg | applied 22:47:14Z, laptop CloudOps msg 107439, relayed by MSTR~DELL2 msg 1844 |

## Blast radius signed

- **ONE function, two members:** `irpt-export-render` moves from `rNjtTwcm...` to the built `7T29wPhz...`.
  - No route, IAM statement, bucket, key prefix or data is changed by this pair.
- **Branch A:** every custody record carries `persisted_by` and `composition_sha256`. `persisted_by` is the verified principal, never a body
  field. A document whose declared composition hash does not match is refused before any write (0 blobs, 0 index rows).
- **Branch B:** redeploy S3 version `WiLXOyz...` through the Terraform deploy path. Records written under A keep their additive keys.

## Sequencing ruled (the ask)

**ONE apply order to `0.7.0_AE_CloudOps~DELL2`, in two legs:**
1. The function, first.
2. The `custody-report-persist` route (IB-pr-373 step 3), only after a live read shows CodeSha256 = `7T29wPhz...`.

No persist is ever served by code without `persisted_by`. The order re-runs the replay arm against the uploaded zip before leg 1, as the
packet states. Its first real persist after E2a is the act that EXERCISES the KMS statements, which are applied but not yet exercised.

**Verdict: GIVEN**, for exactly this function at the built sha, and this order.

-- 1.0.0_SA_CTO~DELL2
