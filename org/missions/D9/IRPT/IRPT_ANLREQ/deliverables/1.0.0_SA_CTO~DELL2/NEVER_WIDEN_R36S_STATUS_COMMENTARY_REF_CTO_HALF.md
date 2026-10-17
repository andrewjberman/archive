# CTO half -- r36 irpt-status: package the acceptance module that carries get_commentary_ref

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~16:1xZ.

**Packet:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/irpt_status_release/NEVER_WIDEN_PACKET_R36S_STATUS_COMMENTARY_REF_20261017.md`, blob `b659221aa11028990e95d0f95c957405a7dc5732`, sha256 `4cb45989b9556d580336397805cae3e63853af8c920febbc9da829962fe5de77` (6,696 bytes), commit 7a2c9ef89f. Ledger `irpt-status-r36s-20261017`. Applier: `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

## Blast radius (section 2, accepted as read)

- **One code object version, and the irpt-status function's code only.** The plan is 0/1/0, with `last_modified`, `s3_object_version` and `source_code_hash` only.
- **One member moves out of 49:** `acceptance.py` (live `06425d4731b7`, built `0c4acec625b7`). Three commits ride in it:
  - `get_commentary_ref`, which is the purpose;
  - `accept(acting_principal_id)`;
  - an optional `commentary_requested`.

  The status Lambda never calls `accept()`, so the latter two are inert on this function. The writer count is stated: the issuing Lambda and a test only.
- **Served output moved:** a ticket's commentary PDF route answers 200 for a request that carries a retained commentary ref, where it was refused before. No principal class gains access, and the creator/assignee check (`lambda_function.py:1750-1753`) is untouched.

**Rollback:** the prior S3 VersionId, recorded at R0, through the scoped plan.

## Conditions

- **R0 prints the live role policy.** Any difference from the source the packet read is recorded before the upload.
- **G2 must read exactly 1 of 49 members changed.** Any second mover STOPS.
- **G5 uses a synthetic request only.** Andrew's ticket is not touched by this pair; its commentary is read after his own Retry.
- **Timing:** outside the weekday 11:30Z to 14:15Z band. Today is Saturday, so it may run now.
