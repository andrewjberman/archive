# NEVER-WIDEN SIGN-OFF -- CTO HALF -- NFRA_TRNSPT: the Teams meeting pull, FIRST apply (`pull.tf`)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~08:4xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 2911
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_TEAMS_PULL_FIRST_APPLY_20261009.md`,
**blob 4bdcfb584a** (commit 7dcb3cc48f). Ordered by analysis ADDENDUM 7 @504e23e93f.

## Blast radius signed

- **Step 1 (read only) gates step 2:**
  - S04: one gateway transcript-tool call, status and count only.
  - S05: the token expiry printed, never its value.
  - The KMS key policy is read for CreateGrant. If the applying identity cannot create the grant, the grant goes to the laptop via `0.0.0_AB_MSTR~DELL2`, and
    step 2 waits for it.
- **Step 2:** one `safe-apply` of `infra/aws/terraform/transcripts`, `-target`ed to exactly pull.tf's 9 resources. The plan is 9 CREATES, and any other line
  means STOP.
- **The writer** is a third principal: it writes `teams/transcripts/*` for the 4 allowlisted series only, is not added to the reader list, and leaves the key
  policy unedited.
- **The schedule** is `cron(0 13-22 ? * MON-FRI *)`, with no alarm, SNS or SES.
- **Rollback:** a targeted destroy of each create. A destroy, and any deletion of landed objects, is Andrew's act.

## Conditions this half adds

1. **The shared-package hazard is measured, not assumed.** The applier prints `outlook-global-transcripts-pull-lambda`'s live CodeSha256 before and after
   step 2. They must be equal.
2. **The hazard outlives this act, so it is named for the NEXT applies of this root.** The rebuilt `dist/transcripts-pull.zip` changes its hash, so an
   untargeted plan will now show an UPDATE to the live mail pull and the commentary Lambda.
   - The commentary first apply (half @5e467d90af) is already a targeted step B, and the shared-root rule applies: any mail-pull line means STOP.
   - The mail pull moves only under its own pair.
3. **The seat invoke at apply** reports landing counts and stages only, with no transcript text and no token (the COO half's condition 2).
4. **The ledger names the pin and the zip sha256** (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.

**Verdict: GIVEN**, for steps 1 and 2 exactly, under conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
