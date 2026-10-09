# svc-custody-statement -- never-widen pair (COO half, DRAFT): mint ONE service token for the Performance client statement writer, Cottonwood only

**Status: DRAFT, not signed.** Drafter `2.0.0_SA_COO~K2`, 2026-10-09 ~03:3xZ, on `1.0.0_SA_CTO~DELL2` msg 2270 ("draft the never-widen
mint pair for svc-custody-statement, following the svc-commentary pattern"). CTO release-6 half @96e03f8ba1. Pattern:
`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/F10_DEPLOY/NEVER_WIDEN_PAIR_SVC_COMMENTARY_MINT.md` (and its two
amendments, whose lessons are folded in here: the reader grant is written up front, and every test body is well-formed).

**Executor:** `0.7.0_AE_CloudOps~DELL2`, dell2's applier. This seat reads no private key. **Order:** after irpt-ycharts-generate
release 6 is live. The token's one use is IRPT_CUSTDY CU-g-5 (TO-CU-g-2a), run by the applier, which holds the token.

## 0. PRECONDITION FOR THE CTO -- the writer accepts only OPAL_GLOBAL, and OPAL_GLOBAL is never minted from a token

This was measured at box/dell2 HEAD and it is the reason this half is not signed:

- `export/custody_persist.py:152-153` refuses `CustodyPersistNotOpal` unless the verified principal's `principal_class ==
  "OPAL_GLOBAL"`.
- `_scope/resolve.py:47` says "OPAL_GLOBAL IS NEVER MINTED FROM HEADERS. It requires `opal_principal_ids`, an explicit
  server-side roster", and that roster is empty by default (`_authz/served.py:541`, passed into `_scope.resolve` at
  `_scope/global.py:253`).
- `portal-authorizer/index.mjs:293-322` builds `allowedFirmIds` from claims only: `firmId` gives that firm, and there is no `role`
  so there is no descendant walk.

So a token carrying `firmId: cottonwood` alone resolves to a firm class, and the writer refuses it NOT_AUTHORIZED. For the token to
persist a statement it must ALSO be on the Opal principal roster that the export function's enforcer reads. This pair cannot name
that roster's live home: the drafter traced it to `served.enforcer_for(..., opal_principal_ids=...)` and no further.

**REC (a):** the token carries `firmId: cottonwood`, which keeps `allowedFirmIds` at "cottonwood" so no other firm's tenant is ever
reachable. In addition, `svc-custody-statement` is added as ONE row to the export function's Opal principal roster, as a rider
by IRPT_BCKEND (`~P2`, who owns the writer). The read-backs below prove both halves: Cottonwood persists, another firm is refused.
**Alternative (b):** no roster row; instead IRPT_BCKEND changes the writer to admit a named service class. That is a code release and
a wider design change. Not recommended.

## 1. The token (as msg 2270 specifies, plus REC (a))

| claim | value |
|---|---|
| `sub` / `name` | `svc-custody-statement` |
| `userType` / `tier` | `service` / `service` |
| `firmId` | `cottonwood` |
| `iss` / `aud` | `opal-portal-auth` / `opal-portal-api` |
| `iat` / `exp` | now / iat + 90 days or less |

**ABSENT:** `role`, `advisorId`, `allowedPages`, `allowedTabs`, `firmRole`. It is RS256, signed with the CURRENT slot of
`opal/auth/jwt-private-key`, read into memory and never printed or written. `userType` is not `Dev` and `tier` is not `internal`, so
`allowedFirmIds` is never `ALL`. It is exactly `cottonwood`.

## 2. Custody

- **Secret:** `opal/investor-reporting/svc-custody-statement`, value `{"token","sub","exp","minted_by"}`. The description states the
  single use (the statement submission and persist routes), firm `cottonwood` only, the TTL and the rotate-by date.
  - The secret NAME is from the svc-* family and is not a builder output. Before the apply, the applier runs it through
    `lib/opal_naming.py`. The naming gate now REFUSES (rule 30, c55a7b39cd); a refusal there is a registry row to add, never a
    hand-typed workaround.
- **Reader, written UP FRONT (svc-commentary AMENDMENT 1's lesson):** add this ONE ARN to dell2's existing
  `secretsmanager:GetSecretValue` allow-list, the list that already admits `opal/ticketing/svc-analyst-intake`. Since Step F (applied
  23:24:52Z), dell2's applier writes this itself and reports it after the fact to `0.0.0_AB_MSTR~DELL2` (name and grant). Nothing else
  reads it.
- **Credential rule:** the applier reports its read of the signing key by secret name and run, like a deploy.
- **Rotation:** due 14 days before exp. Owner `2.0.0_SA_COO~K2`, carried in the round-7 slug.

## 3. Order (leg M, after release 6 is live and the roster rider is applied)

1. **Before-read:** `describe-secret` returns ResourceNotFoundException; the roster row is present (its read-back is named by the
   rider). Otherwise STOP.
2. Mint per section 1, then `create-secret` and the reader grant per section 2.
3. **Read back:** decode the token without verifying. The claims must equal section 1 exactly, and `exp - iat <= 90d`.
   A `GetSecretValue` simulation on the ARN must return allowed for the dell2 user and implicitDeny on an unlisted secret.
4. **Positive arm = CU-g-5 itself:** one real Cottonwood statement submission, then one persist through
   `POST /api/scoped/investor-reporting/custody-report` with `selected_tenant=cottonwood`. Expect 2xx and a retained `CUSTODY_REPORT`
   reference (TO-CU-g-2a, criteria CU21-AC1/AC2).
5. **Negative arm 1:** the same token, the same persist route, with `selected_tenant=49financial`. Expect a refusal (401/403 or
   NOT_AUTHORIZED / OBJECT_NOT_COVERED) and nothing written.
6. **Negative arm 2:** the same token on one unrelated scoped read, which the applier picks from `comp-routes api-routes` and names in
   the ledger. Expect a refusal or zero rows; 200 with rows is a FAIL.

**Rollback:** `delete-secret` with the DEFAULT recovery window (never force-delete), remove the ARN from the allow-list, and the rider
removes the roster row. The token stays valid until exp, but off the roster the writer refuses it, so the roster row is the real control.
**Triggers:** any claim mismatch; a step-5 write; a step-6 200 with rows; a CTO or Andrew word.

## 4. State coherence -- what this does NOT move

- It does not touch `opal/auth/jwt-*`, the portal authorizer or any human principal.
- It adds no user row in `opal-users-v2` unless the roster rider says the roster lives there. If it does, the rider names it, and it
  is still one row.
- It grants no other firm and adds no other service subject.
- The Performance client statement's code ids (`CUSTODY_REPORT`, `irpt-custody-x10-v1`) are unchanged.

**COO half: NOT SIGNED until the CTO rules section 0** (REC (a) + the `~P2` roster rider). The signature follows the ruling.
