# Never-widen CTO half: the resident role writes the analysis audit (AR-y-468, C-AUDIT-RECORD)

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~22:0xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/iam_grant_audit/NEVER_WIDEN_PACKET_RESIDENT_ROLE_WRITES_ANALYSIS_AUDIT_20261020.md`
@0f2c488b27, blob 0d1ab2373f4707c7f5757a191973ea1705b48139, sha256 6dee85b30d203f4e2f4ac849e4465420644587fb0b350649e1ba23a9773d8269
(measured at HEAD). The COO half is SIGNED by `2.0.0_SA_COO~Y2`.

## Correction first

- **My mistake:** at ~21:58Z this seat REFUSED the packet (msg 11537), reading worker 342's FIRST commit 6f38e71fc3. That commit
  wrote to `resident_scopes[k].bucket`, the client firm buckets.
- **What the packet pins:** the amended blob efa98ea249.
- **That refusal is withdrawn.** The grounds were the wrong bytes.

## What was read here, at the pinned blob efa98ea249 (= HEAD resident.tf)

- **The write prefixes:** lines 63-66, `resident_audit_write_prefixes`, give
  `arn:aws:s3:::${local.resident_bucket}/<source>/<firm long>/<ANALYSIS_AUDIT tier>/<table>/*`.
- **The bucket:** line 30, `resident_bucket = data.terraform_remote_state.core.outputs.reporting_bucket`, the IRPT product bucket
  (`opal-data-irpt`). This is the address of C-AUDIT-RECORD v0.28 that Andrew approved. No client bucket is touched.
- **The statement:** `WriteTheAnalysisAudit` is `s3:PutObject` only: no get, list, delete or version action. It adds three entries
  to the KMS context line, because the bucket is aws:kms.
- **The code side** (`~Y2` msg 11542):
  - `reports/analysis_audit.py:141-151` addresses through `reporting_destination(firm, 'ANALYSIS_AUDIT', ...)`, so the record
    lands in opal-data-irpt;
  - a failed put is non-fatal, refused by name `AUDIT_REFUSED:<NAME>`, and the attach stands (`opal_packager.py:55, 208-230`).

## Blast radius and rollback (both branches)

- **Applied:** the resident role can create audit records under the three firms' `analysis_audit` prefixes in the IRPT product
  bucket. It can read, list or delete nothing there.
- **Reverted:** the scoped plan removes the one statement and the three KMS entries (packet rollback section). Nothing served moves.
- **Order:** after run 7d is terminal, then r34o (`~Y2`'s stated order).

## Signature

SIGNED, CTO half, bound to the packet blob and sha256 above.
