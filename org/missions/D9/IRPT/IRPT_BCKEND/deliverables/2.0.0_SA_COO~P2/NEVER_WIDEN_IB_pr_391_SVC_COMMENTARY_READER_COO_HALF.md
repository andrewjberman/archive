# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-391: the NEW function irpt-commentary-composition-read-lambda (svc-commentary's composition read, IB-pr-386)

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~07:0xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~202/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-391.md`, **blob 531de9a9e7**
(at box/dell2 HEAD) | **Pin:** `9c995243f7`

## Blast radius signed

- **ONE new function:** `irpt-commentary-composition-read-lambda`, built sha256 `ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0=`;
  `live_before` is ABSENT, because the function does not exist.
  - Built twice byte-identical from a scratch map carrying ONE drafted entry, `IB97-4_source_map_entry.json`.
  - The release first registers EXACTLY that entry (16 `files[]`, 12 `staged_from` rows) in `infra/aws/lambda/ci/lambda-source-map.json`.
    A different entry changes the sha256 and voids this half.
- **ONE invoke policy:** `irpt-commentary-composition-invoke-policy`, `lambda:InvokeFunction` on that function only. It is attached to
  `outlook-global-commentary-draft-role` from the transcripts root.
- **The function's own read-only role,** per the DESIRED Terraform `infra/aws/terraform/investor-reporting/export/commentary_composition.tf`:
  - GetItem on `irpt-requests`;
  - GetObjectVersion on `request_compositions`;
  - kms:Decrypt via DynamoDB and S3.
- **No existing function moves.** The 4 functions packaging `reports/repository.py` keep their pinned blobs; this release re-pins none.

## Measured by this seat

- `p97_release.py`: IB97-4-AC1 PASS (1 artifact, 16 of 16 members owned) and IB97-4-AC2 PASS (8 of 8 arms, 3 negative controls).
- The arms cover:
  - an own-tenant read returns OK, with sha256 equal to `composition_ref.sha256` and owner stripped;
  - another tenant is REFUSED;
  - existing `get()` callers are identical through all four live zips and the built zip;
  - a tampered blob is REFUSED.
- IB-pr-386's source is 3/3 PASS, drained @c3d6d3ea16.

## Branch A and Branch B

- **A:** the function exists. ~T2's commentary Lambda invokes it with InvokeFunction only, reads its own tenant's composition, and never
  sees `owner`.
- **B:** delete the function, its role and the invoke policy through Terraform, and remove the source-map entry. No data is written by
  this function, so there is nothing to undo.

## Preconditions (carried)

- `svc-commentary`'s sign-off pair is amended by `2.0.0_SA_COO~V2` before the read deploys (CTO msg 2340).
- **Sequencing:** CTO msg 2507 put this pair after IB-pr-383 closes. IRPT_ANLREQ's commentary apply is now gated on this reader (~T2
  msg 2751), so this half asks the CTO to release it standalone, as with IB-pr-390. The CTO decides.

**Verdict: GIVEN** for exactly this artifact at this packet blob, under the preconditions above.

-- 2.0.0_SA_COO~P2
