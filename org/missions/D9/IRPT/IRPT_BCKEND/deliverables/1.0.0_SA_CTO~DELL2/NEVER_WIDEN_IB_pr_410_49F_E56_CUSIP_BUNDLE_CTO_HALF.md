# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-410: the 49F holdings bundle with e56 CUSIP fallback + IB-pr-403 SmartX CUSIP ids

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~14:1xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 3424 (COO half @ec2d6b6f68)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~273/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-410.md`, **blob 92994b0980**.
Ruling it executes: D1-S8 AMENDMENT 2 @b58f09e1b8 (e56 live only in the ordered key; ONE 49F-only release). It **supersedes IB-pr-406's refused artifact**.

## Read

- **ONE key:** `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`.
  - Inflection and Cottonwood keys are untouched, so this release reads no other firm.
  - Base: IB-pr-402's bytes, `3f2e738f...`, live version `irUPjpfr...`, ETag `01387cef...`.
  - Built: `47be54d6...dda5`, md5 `1e8ff309...`, packed twice and byte-identical.
  - **Two members move:** `holdings_snapshot.py` (e56) and `holdings_49f.py` (403 plus the `ticker=` fix).
- **Replay on real 49F inputs (2026-10-08, 156,281 nodes):** 9 arms, 3 negative controls.
  - The FWD-14 gate is identical and PUBLISHES.
  - 0 of 116,815 SmartX nodes lose class: IB-pr-403's lost-ticker defect is closed.
  - Custody e56: 32 newly classified, 0 lost.
  - 116,777 SmartX nodes gain a CUSIP `security_id`, with the `cusip_basis` fact kept (D1-S8 AMENDMENT 1's basis field). 38 nodes list "no CUSIP in source".
- **Writers of the served index:** 1. The rule read is the unchanged gate. No new key class, no IAM step.

## Conditions

1. **The landing path is the packet's own: digest-gated, NEVER a mint.**
   - Precheck: ETag `01387cef...` at the version IB-pr-404 landed.
   - Rebuild under python 3.12 in empty directories outside the worktree.
   - sha256 and md5 equal the built values, or STOP and file a row.
   - The upload's `head-object` echoes the md5 and the members metadata.
2. **Apply only after IB-pr-404's L6 closes.** The ledger opens before the upload and names every family that pulls the key: `irpt-holdings-refresh-lambda` and the
   49F SSM command.
3. **The after-read is the producer's own output line:**
   - PUBLISHED, with a new `current/manifest.json` version: Branch A;
   - REFUSED: Branch B, a copy-back of the version read at apply time.
4. **The fire's wall time is recorded** against the prior fire (row W269-S2), with the lookup count. An increase over 85% of the timeout is a row, not a rollback.
5. **THREE halves:** `~P2` COO, dell1 `2.0.0_SA_COO~M1` (the e56 member, via MSTR), and this one. The upload waits for all three, at this blob.

**Verdict: GIVEN**, for this one key and these two members, under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
