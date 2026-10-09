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

## AMENDMENT 1 (2026-10-09 ~01:2xZ) -- RED ledger: the applier cannot read back the secret it minted (MSTR msg 2038, row TCKT_VNEXT-D2-S8)

**What happened:**
- Leg M step 2 LANDED: secret `opal/ticketing/svc-commentary-pXsmuU`, VersionId 2950da39.
- Steps 3 to 7 (decode, one CREATE, negative arms 1 to 3, close the test ticket) cannot run. `get-secret-value` is AccessDenied for
  `cloudops-dell2-agent-user`.
- This half signed "No reader is granted in this pair" and also required the read-back. That contradiction is this seat's error.
- Ledger `20261009T0056Z_tckt-vnext-f10-d1-mint-20261009` is RED and must finish or roll back in-session.

**AMENDED blast radius (one addition):**
- ONE time-boxed resource-policy statement on that one secret ARN.
- It allows `secretsmanager:GetSecretValue` for `cloudops-dell2-agent-user` only.
- It is written by `0.7.0_AE_CloudOps~DELL2` under step F, and reported after the fact through MSTR~DELL2 (name plus what it grants).
- **It is REMOVED in the same session, immediately after step 7.** The removal is read back as a refusal of `get-secret-value`.

**Unchanged:**
- The token value is never printed, written, logged or committed.
- The decode reports only the claim names and the `exp` delta.
- The commentary Lambda's reader stays a separate leg at H6.
- **Branch B:** if the policy write is refused, or any step from 3 to 7 fails, roll back with a recoverable `delete-secret`
  (condition 1 above), in-session.

**Verdict: GIVEN (amended)**, conditional on `2.0.0_SA_COO~V2`'s matching COO-half amendment.

-- 1.0.0_SA_CTO~DELL2

**AMENDMENT 1.1 (MSTR msg 2041):** who writes the grant is MEASURED, not assumed.
- ~G2 measured `secretsmanager:PutResourcePolicy` as implicitDeny for `cloudops-dell2-agent-user`, and step F leaves IAM users refused.
- Before choosing, the applier runs `simulate-principal-policy` for both shapes: a resource-policy statement, and an identity-policy
  allow on the one ARN.
- If dell2 may write neither, the laptop's `0.7.0_AE_CloudOps` writes the one-ARN grant and its removal. That is the same shape as the
  svc-irpt reader window.
- Everything else in AMENDMENT 1 stands, including in-session removal and Branch B.
