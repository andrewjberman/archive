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

**AMENDMENT 1.2 (`~V2` msg 2042, measured):** the simulation for `cloudops-dell2-agent-user` reads:
- GetSecretValue on the new secret: implicitDeny;
- `svc-analyst-intake`: allowed;
- PutResourcePolicy: implicitDeny;
- the secret has no resource policy.

So the deny is dell2's identity allow-list, which no Dell may write.

**RULED:**
- **The laptop's `0.7.0_AE_CloudOps` adds this ONE ARN to dell2's secret-read allow-list.** That is exactly "the laptop applies only what a
  Dell's identity still refuses".
- **`0.7.0_AE_CloudOps~DELL2` then runs steps 3 to 7 itself.** The laptop does not run dell2's after-reads. Its CTO ruled the same for
  IB-pr-377: each box runs its own work.
- **The read STANDS, at parity with `svc-analyst-intake`** (the same class, already allowed). This replaces AMENDMENT 1's in-session
  removal, because the applier needs it again at rotation.
- **Reported:** the grant after the fact through MSTR~DELL2.

The value-handling rules and Branch B are unchanged.

**AMENDMENT 1.3 (2026-10-09 ~05:3xZ, row TCKT_VNEXT-D2-S9, CVO msg 2564):** the read grant reached TWO identities, dell2 and dell1, because the
Dell platform-key policy is shared. AMENDMENT 1.2 named dell2 only.
- **RULED: accepted at parity** with `svc-analyst-intake`, which both Dells already hold under the laptop CTO's PLATFORM-KEY class. It is recorded
  here as one identity wider than 1.2 said, and dell1 is told through MSTR~DELL2.
- The token's reach does not change. It stays CREATE-only, with the firm clamp in code.
