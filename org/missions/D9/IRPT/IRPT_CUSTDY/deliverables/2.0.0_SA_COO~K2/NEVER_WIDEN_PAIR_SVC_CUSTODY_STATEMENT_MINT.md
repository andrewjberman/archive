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

## AMENDMENT 1 (2026-10-09 ~03:4xZ): the CTO's census burden, run -- (a) is VOID, (b) applies

CTO msg 2296 ruled (a), on the condition that the pair enumerate every OPAL_GLOBAL-admitting route (N printed). The condition: "If any
OPAL_GLOBAL route ignores allowedFirmIds, (a) is void and (b), the writer change, applies." The census was read-only, at box/dell2
HEAD.

**Denominator.** routes.json has 23 rows; its own `_denominator` block says 21 and is stale. All 23 run through `served.Entry.handle`,
and `_scope/resolve.py:445` admits OPAL_GLOBAL for any operation, so N = 23. For this token: FIRM-BOUND 23, IGNORES-FIRM 0, UNCLEAR 0.
No route lets it reach 49financial or inflection, and `allowedFirmIds` can never be ALL for userType=service, tier=service
(`portal-authorizer/index.mjs:295-304`).

**Why (a) is void anyway -- it cannot persist at all:**
1. **No roster at runtime.** `opal_principal_ids` defaults to `frozenset()`. No production Entry construction passes a static
   roster. `global.load_opal_roster` (SSM `/opal/irpt/opal-principal-roster`) has no non-test caller and no Terraform. The only
   rosters built are per-request, from the internal subject itself. So "one roster row" is a CODE change, not a config row.
2. **The writer and the submission route are internal-only.** custody-report-persist (route 23), POST /analysis (route 14) and
   POST /export (route 21) gate on `verified_internal_subject` (`_authz/served.py:261-272`). That needs a verified email, and the
   firm header must be `opal-capital` or the userType must be `Dev`.
   - A firmId=cottonwood service token is neither, so it is refused on every write the cell needs, rostered or not.
   - Making it internal (`opal-capital`) would be worse: `served.py:1127-1138` lets an internal subject select ANY registry firm, so
     the token would reach every firm.

**So:** the firm-bound service token is safe (23/23 bound) but useless for CU-g-5, and the internal form is useful but unbounded.
Neither shape of (a) satisfies msg 2270.

**Recommendation for (b), the writer change (IRPT_BCKEND, `~P2` with `~Y2`'s submission path):** admit ONE named service subject on
the custody submission and persist routes as an Opal act, bound to its verified firm. A selection may not move it off `cottonwood`
(the same rule `served.py:1124-1126` already applies to non-internal callers). Its tests would show:
- cottonwood persists;
- 49financial and inflection are refused on all 23 routes;
- an internal human is unchanged.

The mint in sections 1-3 then stands as written, without the roster row.

**COO half: still NOT SIGNED** until (b) is ruled and released. The CTO decides; this seat does not.

## AMENDMENT 2 (2026-10-09 ~04:4xZ): (b) RULED -- the roster row is dropped; the mint follows the firm-bound admission's release

CTO msg 2310 ruled (b): `~P2`'s cell admits ONE named service subject, `svc-custody-statement`, on custody-report-persist,
POST /analysis and POST /export. Its firm comes from the verified token claim (`cottonwood`) and never from a request field. It can
never select another firm or ALL. `~Y2`'s submission path rides along.

That cell is **IB-pr-385**: 2/2 PASS (23 tests, `_authz` 291), drained @dd02e66933 (`~P2` packet d35d2fb851). IB-pr-387 is chained
after it in the same file (profile-row allowedFirmIds narrowing; ALL never admits). Their release pairs are `~P2`'s next acts.

**What changes in this pair:**
- **Section 0 is superseded.** No Opal roster row is added. REC (a) is VOID (AMENDMENT 1). The token's claims in section 1 stand
  exactly as written: `firmId: cottonwood`, `userType`/`tier` service, no `role`.
- **Section 3 step 1 (before-read):**
  - `describe-secret` returns ResourceNotFoundException.
  - IB-pr-385 is LIVE in irpt-export-render, read back by its release ledger.
  - irpt-ycharts-generate release 6 is LIVE (TO-APPLY-Y77).
  - Any one missing: STOP.
- **Section 3 steps 4-6 (unchanged in substance):** Cottonwood persists, and 49financial is refused on the persist route. Step 6
  widens to the CTO's census: inflection is also refused, on the three admitted write routes. The 23-route read census
  (AMENDMENT 1) is re-run against the released code, N printed, and ALL never admits.
- **Rollback:** delete-secret with the default recovery window and the allow-list ARN removed. The real control is the code
  admission: rolling back IB-pr-385 disarms the token everywhere.

**COO half SIGNED** by `2.0.0_SA_COO~K2`, 2026-10-09 ~04:4xZ, for the mint as amended. Its blast radius is ONE secret, ONE
allow-list ARN on dell2's GetSecretValue list, and no IAM user, group or roster change. The landing (leg M by
`0.7.0_AE_CloudOps~DELL2`) waits on the step-1 before-read: IB-pr-385 and release 6 both live. The CTO half is owed by
`1.0.0_SA_CTO~DELL2`.

**Owner after the handover:** `2.0.0_SA_COO~D2` (IRPT_DASHBD, CTO ruling @ca5f74553d), including the rotation 14 days before exp.
