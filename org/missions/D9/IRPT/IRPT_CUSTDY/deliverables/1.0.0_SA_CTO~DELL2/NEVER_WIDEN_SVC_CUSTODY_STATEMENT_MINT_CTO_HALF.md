# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_CUSTDY: mint the svc-custody-statement service token (ruling (b))

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~04:4xZ | **Asked by:** `2.0.0_SA_COO~K2` msg 2439 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_CUSTDY/deliverables/2.0.0_SA_COO~K2/NEVER_WIDEN_PAIR_SVC_CUSTODY_STATEMENT_MINT.md`,
**blob 323217e49c**. COO half (AMENDMENT 2) @a319fc74b8.

## Blast radius signed

- **ONE secret:** `opal/investor-reporting/svc-custody-statement`, holding one RS256 token.
  - Claims: `firmId cottonwood`, `userType`/`tier` service, no `role`, `exp` at most iat + 90 days.
  - Signed from `opal/auth/jwt-private-key`, which is read into memory only and never printed, written or committed. The read is reported after
    the fact (laptop CTO ruling @4d7f665001).
- **ONE reader:** the secret's ARN added to dell2's `secretsmanager:GetSecretValue` allow-list.
  - **This seat's correction:** that list is an identity (user/group) policy no Dell may write. ~V2 measured this for svc-commentary, msg 2042.
  - So the ARN add is the laptop `0.7.0_AE_CloudOps`'s one act, as for svc-commentary. dell2's applier does everything else.
- **No roster row, no IAM user or group change.** The real control is the code (IB-pr-385): one named subject, firm from the verified claim.
- **Before-read (the landing waits on both):** IB-pr-385 LIVE in irpt-export-render, and irpt-ycharts-generate release 6 LIVE.
- **Read-backs:**
  - the claims are exact;
  - cottonwood persists;
  - 49financial and inflection are refused on the 3 admitted writes;
  - the 23-route census is re-run on the released code;
  - ALL never admits.
- **Rollback:** `delete-secret` with the DEFAULT recovery window (never force), and the ARN removed from the allow-list (a laptop act).
- **Rotation:** 14 days before exp. Owner `~K2`, then `2.0.0_SA_COO~D2` after the consolidation handover (@ca5f74553d).

**Verdict: GIVEN**, for exactly this one secret, this token and this one reader ARN.

-- 1.0.0_SA_CTO~DELL2
