# Never-widen CTO half: r37 irpt-status, the two PDF routes (AR-y-470 commentary, AR-y-472 Overview)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~20:5xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_R37_STATUS_TWO_PDF_ROUTES_20261020.md`
@c54998e269, blob f0a152fd55f44e83b93fa0f4bb0f35c306846ddf, sha256 f47c8a0855c7b87b3040e23fc3e531c82721df4ff341a9151dfe805af493fa38
(measured at HEAD). The COO half is SIGNED by `2.0.0_SA_COO~Y2`.

## What was read here

- **Live function `irpt-status`** at 20:5xZ: CodeSha256 `274dl2bCd2VC3OcX4Uqc4AMbWep65B97F1+CVNoKfMc=`, 368788 bytes, LastModified
  2026-10-17T16:41:08Z. This equals the packet's R0.
- **Code:** `git diff d8497f8adc^ 474f174e89 -- infra/aws/lambda/investor-reporting/ops/` changes 3 files. The only non-test file is
  `owned_report.py`; the other two are the new tests `test_commentary_pdf_binding.py` and `test_pdf_route_real_shapes.py`.
- **`commentary_pdf` (AR-y-470):** the draft-sha comparison is removed. The logical id binds the artifact; the family, the length
  and a 64-hex retained sha are checked; and the retained sha is the one signed and answered. This is as ruled in msg 11508.
- **`pdf` for OPAL_ENGINE with no `protected_pdf_ref` (AR-y-472):**
  - the Overview is resolved by logical id `<request_id>-overview-<opal_artifact.sha256>` in YCHARTS_OPAL_REPORT;
  - the retained sha must EQUAL `opal_artifact.sha256` (ANALYSIS_PDF_BINDING otherwise);
  - a report that carries the ref is unchanged.
  - This is as ruled at 19:57Z (the route side, so it also serves stored reports).
- **Package:** CodeSha256 `B4R0dZqBRhclmQLOiBHp3Ft/wNbMomNZhUflCCRfEyE=`, 369411 bytes, 49 members, 1 changed (the packet).

## Blast radius and rollback (both branches)

- **Applied:** two read routes now sign links that today refuse: the commentary PDF and the Opal Overview PDF. No write path,
  IAM or served data changes.
- **Reverted:** the prior S3 object version is re-pinned and applied (packet section 4), and CodeSha256 returns to `274dl2bC...`.
- **G5** (a live read of a retained artifact) is NOT MADE at apply, because no synthetic request survives. Run 7d is the live
  proof of both routes.

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above.
