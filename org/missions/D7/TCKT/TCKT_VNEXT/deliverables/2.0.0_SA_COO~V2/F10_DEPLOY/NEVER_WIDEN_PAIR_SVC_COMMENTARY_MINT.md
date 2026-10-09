# svc-commentary -- never-widen pair (COO half): mint ONE service token with no firm reach

**COO half SIGNED by** `2.0.0_SA_COO~V2`, 2026-10-08 ~22:5xZ. **CTO half: GIVEN** by `1.0.0_SA_CTO~DELL2` (msg 1837,
`deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SVC_COMMENTARY_MINT_CTO_HALF.md`); its two conditions are folded into section 4.

**Authority:**
- TCKT_VNEXT PRD ADDENDUM 1 @f8c019c28f (FWD-6 = NFRA_TRNSPT FWD-10 H5);
- CTO msgs 1826 ("svc-commentary is YOURS to mint ... fold it into the FWD-6 workstream cell under its own pair") and 1830 (the
  ruling quoted in section 2);
- laptop `2.0.0_SA_COO~C` msg 107421 via MSTR 1825 (an application-level service subject; not IAM; no laptop act).

**Executor:** `0.7.0_AE_CloudOps~DELL2` (dell2's applier, Andrew-direct msg 1758), as leg M of the F10 apply order. This seat reads no
private key.

## 1. Precedent (metadata only, `describe-secret`, read 22:5xZ)

`opal/ticketing/svc-analyst-intake`, created 2026-08-20. Its description reads: "RS256 iss=opal-portal-auth aud=opal-portal-api. TTL
30d ... Value is JSON {token,...}; consumer reads .token. Minted 0.7.0_AE_CloudOps per CTO~Z U4 spec." `opal/ticketing/svc-commentary`
does not exist (`ResourceNotFoundException`).

## 2. The token (CTO ruling msg 1830, verbatim)

> one svc-commentary token (userType service, tier service, NO firmId, explicit exp of 90 days or less with rotation noted).
> ticket_center clamps answers.firm to COMMENTARY_ALLOWED_FIRMS=49financial,cottonwood,inflection, never ALL.

**Claims, exactly these and no others:**

| claim | value |
|---|---|
| `sub` | `svc-commentary` |
| `userType` | `service` |
| `tier` | `service` |
| `name` | `svc-commentary` |
| `iss` | `opal-portal-auth` |
| `aud` | `opal-portal-api` |
| `iat` | now |
| `exp` | iat + 90 days |

**ABSENT:** `firmId`, `role`, `advisorId`, `allowedPages`, `allowedTabs`, `firmRole`. RS256, signed with the CURRENT slot of
`opal/auth/jwt-private-key` (read into memory, never printed or written).

**Why no firm reach is the whole point.** The authorizer builds a token's `allowedFirmIds` from its claims only
(`infra/aws/users/lambda/portal-authorizer/index.mjs:293-322`):
- `userType` here is `service`, not `Dev`, and `tier` is not `internal`, so the result is never `ALL`;
- with no `firmId` the set is empty;
- `role` is absent, so there is no descendant walk (and no firm has a parent: 6 META rows read 22:4xZ).

So on every `/api/scoped/*` route the token reaches no firm. The one place it acts is `ticket_center` CREATE, where AMENDMENT 1 of
TO-F10-l1 clamps the firm to the env list.

## 3. Custody

- **Secret:** `opal/ticketing/svc-commentary`, value JSON `{"token": "<jwt>", "sub": "svc-commentary", "exp": "<ISO>", "minted_by":
  "0.7.0_AE_CloudOps~DELL2"}`, with description `F10 svc-commentary service token (CREATE analysis_request only on opal-ticket-api;
  NO firm claim; ticket_center clamps to COMMENTARY_ALLOWED_FIRMS). RS256 iss=opal-portal-auth aud=opal-portal-api. TTL 90d minted
  <date>, rotate by <exp - 14d>. Consumer reads .token.`
- **Reader:** only `~T2`'s commentary Lambda role, named at H6's deploy. No reader is granted in this pair. The grant is one
  `secretsmanager:GetSecretValue` statement on this secret ARN in that role's policy (IAM, so a laptop leg while the Dells cannot
  write IAM). It is recorded on H6's pair, not here.
- **Credential rule (msg 1233 (2)):** the applier reports its first read of `opal/auth/jwt-private-key` to the laptop by secret name
  and run, like a deploy.
- **Rotation:** due 14 days before exp. Owner: `2.0.0_SA_COO~V2` (TCKT_VNEXT), carried in the F10 slug as an enrichment item.

## 4. Order (leg M, after leg D has deployed F10-l-1 with the env var)

1. Before-read: `describe-secret opal/ticketing/svc-commentary` must return `ResourceNotFoundException`. Otherwise STOP.
2. Mint per section 2; `create-secret` per section 3.
3. Read back: decode the stored token WITHOUT verifying; the claim set must equal section 2 exactly (no `firmId`, no `role`), and
   `exp - iat <= 90d`.
4. **Positive arm.** The token through the CloudFront API path does `POST /api/scoped/tickets` with an `analysis_request` for
   `cottonwood`, a `draft_commentary` (status DRAFT, text `[TEST TCKT_VNEXT F10] draft`) and a `report_request_id`
   `test-f10-<run>`. Expect 201; `created_by == svc-commentary`.
5. **Negative arm 1 (CTO):** the same token on two non-ticket routes, chosen by the applier from `comp-routes api-routes` and named
   in the ledger:
   - one Investor Reporting read under `/api/scoped/investor-reporting/*`, sent with `selected_tenant=cottonwood`;
   - one partner-data read the portal makes for a firm.

   Each must be refused (401/403) or return no firm's data. Print the route, the status and the row count. A route that answers
   200 with rows is a FAIL, whatever the rows hold.
6. **Negative arm 2 (CTO):** the same token creates an `analysis_request` for `demo` (off the list). Expect 400.
7. **Negative arm 3:** the same token on `GET /api/scoped/tickets` (LIST). Expect 403.
8. **Cleanup (CTO half condition, msg 1837):** the step-4 test ticket is CLOSED in the same session and its `ticket_id` is recorded
   in the ledger. It is closed by an internal principal through the claim and complete routes, never by a table delete.
   **Stated gap:** no seat holds an internal-human token (CLAIM/COMPLETE are INTERNAL-only, `lambda_function.py:114-115`). The
   closer is therefore an Opal person on the Ticket Center board, asked in the same session through the CTO. If no person is
   reachable, the ticket id is recorded OPEN with that reason, and the record does not claim it closed.

**Rollback (CTO half condition, msg 1837):** `delete-secret --secret-id opal/ticketing/svc-commentary` with the DEFAULT recovery
window -- never `--force-delete-without-recovery` (an unrecoverable delete is a human-confirmed act). Note the token itself
stays valid until exp unless the signing slot rotates. The real control is the code clamp plus the CREATE-only matrix, so a rollback
of the CODE (leg D) disarms the token's only write.

**Rollback triggers:**
- any claim mismatch at step 3;
- a step-5 call that returns firm data;
- a step-6 201;
- a CTO or Andrew word.

## 5. State coherence -- what this does NOT move

- No IAM.
- No user row in `opal-users-v2`.
- No change to `opal/auth/jwt-*`.
- No other service subject.
- The portal authorizer is unchanged.
- Every human principal's access is unchanged.

## COO-half AMENDMENT 1 (2026-10-09 ~01:2xZ): a time-boxed reader for the read-back -- matches the CTO half AMENDMENTS 1/1.1 (@ea79bdf486, msg 2043)

**The defect, which is mine.** Section 3 said "No reader is granted in this pair", yet section 4 step 3 orders the applier to decode the
stored token. So leg M half-landed: the secret exists (`...svc-commentary-pXsmuU`, VersionId 2950da39), and steps 3-7 could not run.
The ledger `20261009T0056Z_tckt-vnext-f10-d1-mint-20261009` is RED. Row TCKT_VNEXT-D2-S8 (@50a1eb9849).

**Measured (simulate-principal-policy, `cloudops-dell2-agent-user`, ~01:2xZ):**

| action | resource | decision |
|---|---|---|
| `secretsmanager:GetSecretValue` | the new secret ARN | implicitDeny |
| `secretsmanager:GetSecretValue` | `opal/ticketing/svc-analyst-intake` (positive control) | allowed |
| `secretsmanager:PutResourcePolicy` | the new secret ARN | implicitDeny |
| `iam:PutUserPolicy` | the dell2 user | explicitDeny |
| `iam:AttachUserPolicy` | the dell2 user | explicitDeny |
| `iam:PutGroupPolicy` | the dell2 user | implicitDeny |

The secret had no resource policy (`get-resource-policy`: None). Dell2 can write NEITHER shape of the grant, so per the CTO half the
writer is the laptop's `0.7.0_AE_CloudOps`.

**The grant, exactly (CTO half AMENDMENT 1.2, msg 2045, which supersedes the time-boxed form):** add the ONE ARN
`arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-commentary-pXsmuU` to dell2's existing
`secretsmanager:GetSecretValue` allow-list, the same list that admits `opal/ticketing/svc-analyst-intake`. No other action and no other
ARN. The read STANDS, at parity with svc-analyst-intake, and covers rotation by this project. The laptop's `0.7.0_AE_CloudOps` applies
it, because dell2's identity refuses both shapes (measured above).

**Order:**
1. The laptop applies the grant and reads it back by simulation: GetSecretValue on the ARN for the dell2 user returns allowed, and
   on an unlisted secret returns implicitDeny (negative control).
2. dell2's applier runs section 4 steps 3-7 itself.
3. dell2's applier closes the ledger.

**Rollback (branch B):** `delete-secret` with the DEFAULT recovery window, plus the ARN removed from the allow-list.

**COO-half AMENDMENT 1 -- SIGNED.** `2.0.0_SA_COO~V2`, 2026-10-09.

## COO-half AMENDMENT 2 (2026-10-09 ~02:2xZ): steps 4 and 6 carry an attachment -- answers row TCKT_VNEXT-D2-S10

**Defect (mine).** Steps 4 and 6 sent an `analysis_request` body with no `attachment`. The type requires `{upload_id, input_id}` for every
caller (`_validate_attachment`, `lambda_function.py:643-657`), so step 4 could not pass and step 6's 400 came from the attachment check,
not the firm clamp (CloudOps~DELL2 msg 2180).

**Fix.** Steps 4 and 6 add `attachment = {"upload_id": "test-f10-legm-<run>", "input_id":
"portfolio_abdbb292c2bf6f96b0db74468dcdd68a9383a2e4259be73c9cb1977fb3b2ba03"}`. The input_id is
sha256("TEST TCKT_VNEXT F10 leg M step 4 -- synthetic, no upload exists"). It is a deliberately synthetic, well-formed pointer:
the ticket service validates the reference's SHAPE only and never reads IRPT, and no upload by that id exists, so the test ticket
points at nothing. Step 6 PASSES only when its 400 body names the firm (`requester_firm 'demo' is outside`), proving the clamp fired;
any other 400 is a FAIL. Step 4 also sends `answers` without `household` (exercising F10-l-2's exemption). Step 8 unchanged.

This does not widen the blast radius: the same principal, the same route, the same single test ticket.

**COO-half AMENDMENT 2 -- SIGNED.** `2.0.0_SA_COO~V2`, 2026-10-09.
