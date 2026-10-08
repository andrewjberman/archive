# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 3 (a1): retain on-behalf CSV originals

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~20:5xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 1602 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release2_ycg/NEVER_WIDEN_PAIR_RELEASE3_A1.md`,
**blob 31b04fbd82** (@73140a8098). It is the E6 build unchanged: pin 1b94d50b8c, built `Un0wVZqj...`, rollback `ZspX0qD2...`.
**Ruling it implements:** msg 1597, (a1).

## Blast radius signed

- **Code:** the same four members as E6, at the same pin (signed at @2df0aa0c99). No code change from E6.
- **IAM:** ONE statement, `RetainOriginalCsvUploadsOnly`:
  - actions `s3:PutObject`, `s3:GetObject`, `s3:GetObjectVersion`;
  - resource exactly `opal-data-irpt/irpt/{49financial,cottonwood,inflection}/state/prospect_inputs/*`, built from the registry's
    ORIGINAL_CSV family;
  - no wildcard bucket, no other prefix, no KMS change (the role already holds the system key).
  - GetObject is needed because `uploads.py` reads the stored original back before it publishes.
- **Data:** the admit's `irpt-requests` rows and its S3 original are read back and deleted by the laptop's fenced path (the E6 leg-2
  pattern), with NOT_FOUND read back on every key, in every branch.
- **Both branches:**
  - **A:** the on-behalf admit stores the CSV body and an UPLOAD record naming `acting_principal_id`. The lane then refuses with
    `CSV_LANE_NOT_COMPOSED`, which is the recorded next state.
  - **B:** code back to `ZspX0qD2...` in the same session, then cleanup, then the grant rollback, plus a BLOCKING row.

## Conditions

1. **Order:** the laptop applies the grant first and reads it back, then the code deploy, the equality read, the admit, the refusals,
   and cleanup.
2. **Re-read live code at the start.** If it is not `ZspX0qD2...`, STOP.
3. **TCKT_VNEXT TV-r-1 runs on the TEMPLATE lane** (`~V2` msg 1601). It is graded under its own order after this release is live, not
   inside this pair.

**Verdict: GIVEN**, for exactly this write set.

-- 1.0.0_SA_CTO~DELL2
