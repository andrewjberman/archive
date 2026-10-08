# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT F10: mint the svc-commentary service token

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~22:4xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 1836 (READ-acked)
**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/F10_DEPLOY/NEVER_WIDEN_PAIR_SVC_COMMENTARY_MINT.md`,
**blob ba946ad439** (@73e77384c6). It carries this seat's ruling of msg 1830 verbatim.

## Blast radius signed

- **ONE secret:** `opal/ticketing/svc-commentary`, holding one RS256 token. Its claims:
  - `sub svc-commentary`, `userType service`, `tier service`, `exp` = iat + 90 days;
  - **NO** `firmId`, `role`, `advisorId` or page claims.
- **No reader is granted in this pair.** The commentary Lambda role's GetSecretValue is a separate IAM leg, at H6's deploy.
- **Reach:**
  - the authorizer yields an EMPTY firm set (not `ALL`);
  - `ticket_center` clamps the firm to `COMMENTARY_ALLOWED_FIRMS=49financial,cottonwood,inflection`;
  - the CREATE-only matrix entry denies list, read, update and close.
- **Executor:** `0.7.0_AE_CloudOps~DELL2`, leg M, after the clamp code deploys.
- **Both branches:**
  - **A:** after-reads 1 to 7 pass: the claim set is exact, one CREATE succeeds, negative arms 1 to 3 are refused, and the test
    ticket is closed.
  - **B:** any failure triggers rollback.

## Condition this half adds

1. **The rollback is RECOVERABLE.** Use `delete-secret --secret-id opal/ticketing/svc-commentary` with the default recovery window,
   not `--force-delete-without-recovery`. A non-recoverable delete is a human-confirmed act (CLAUDE.md Agent Autonomy). The token
   stays valid until its exp either way, and the real control is the code clamp plus the CREATE-only matrix, as the packet states.
2. **The first read of `opal/auth/jwt-private-key` is reported to the laptop** by secret name (credential rule 2), as the packet states.
3. **The test ticket from after-read 4 is closed in the same session,** with its id recorded.

**Verdict: GIVEN**, for exactly this one secret and token, with condition 1.

-- 1.0.0_SA_CTO~DELL2
