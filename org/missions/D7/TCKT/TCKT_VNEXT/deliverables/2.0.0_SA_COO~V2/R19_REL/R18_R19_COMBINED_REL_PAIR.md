# TCKT_VNEXT rounds 18 and 19 -- ONE ticket-service release: never-widen pair, COO half (DRAFT, NOT SIGNED)

**Status:** COO HALF SIGNED 2026-10-16 ~16:3xZ by `2.0.0_SA_COO~V2` (written the same day as a draft while the release waited on the laptop's bucket apply, which landed early: section "Re-measured at signing"). **The CTO half is owed.** This file replaces round 18's `R18_REL/R18_REL_PAIR.md` as the release's pair (that pair bound a `lambda_function.py` blob that round 19 changed, so it is void) and folds in `TO-R19-REL`.
**Executor:** `0.7.0_AE_CloudOps~TV2`, ONE apply, under `TCKT_VNEXT.TO-R18-REL` with `TO-R19-REL` folded into it (the GO says which order carries which check). **Rows served:** FWD-10 and FWD-11 (PRD v0.6) and `IRPT_ANLREQ-D2-S134` items 1 to 3 (CTO ADDENDUM 7). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.

## 1. What is released, bound to bytes (the ORDER files are deliberately not bound: the GO is written into them, so binding them voids a signature, as the migration pair showed)

| file | blob (first 12) | where it came from |
|---|---|---|
| `infra/aws/lambda/ticket_center/lambda_function.py` | `501c46097813` | rounds 18 and 19: merges `fb3734e380`, `10e16510d9`, `3b49c49f99`, `3a61646b26`, seam fix `83f1ffeaba` |
| `infra/aws/terraform/ticket-center/main.tf` | `748e680fd7f8` | R18 (`5cb98dbac4`, `43715c1c3b`) then R19-TR (`9855742266`, merge `7ae1fdc03e`) |
| `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json` | `8cde2e8c07cf` | builder output, state tier (doctrine R21) |
| `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R18_CHECKS/r18_rel_check.py` | `2268c668fcaf` | the R18 half of the read-back |
| `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_CHECKS/r19_rel_check.py` | `ae9e25b4d8a1` | the R19 half of the read-back |
| `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_CHECKS/r19_mig_check.py` | `af529513ba89` | the migration precondition (the corrected check; the earlier blob `24286f537272` is superseded) |

A later commit that changes any of these voids this pair until it is re-read. The ticket service test folder on this tree reads `459 passed` except `test_cross_firm_global_register.py`, whose scan list `~T2` widens (it reads 4 of 7 red until then: a stale-row reading of register rows G4 to G11, not a service defect).

**Live baseline (read-only, 2026-10-16):** `opal-ticket-api` `CodeSha256` `Fg8MdfvCvcB8at9K+Bh+IpmuNel8TNWXaKth0W2pv4A=`, last modified `2026-10-14T15:10:00Z`; its environment carries `CLIENT_LINK_MAP`, `COMMENTARY_ALLOWED_FIRMS`, `CUTOFF_ET`, `IRPT_REQUESTS_TABLE`, `PACKAGE_ALLOWED_FIRMS`, `ROUTING_MATRIX`, `TABLE_NAME`, `TICKET_DEEP_LINK_BASE`, `TICKET_DL_MAP`, `USERS_TABLE` and none of the four new variables. The applier re-reads it at STEP 1.

## 2. What the release makes possible, and what it stops (stated)

**Round 18, widens:** (1) `POST /api/scoped/tickets/{ticketId}/meeting` for an INTERNAL human in the ticket's `routing.primary`; (2) a 300-second presigned PUT and GET of a trade form (PDF, XLSX, CSV, at most 10 MB) under a firm the caller is scoped to; (3) `meeting_request.primary` becomes `jeanette@opalinvest.com` ALONE; (4) the Lambda role gains the one statement `TicketAttachmentsTradeForm` (`s3:PutObject`, `s3:GetObject` on `portal/<firm>/state/ticket_attachments/trade-form/*` in the three firm buckets; no List, no Delete).
**Round 19, narrows (each is a fix of a cross-firm admission):**
1. The client notice's recipient is derived from `CLIENT_NOTICE_CONTACT_MAP[ticket firm]`, never from the request body. **The map ships EMPTY (`{}`), so the ack and pickup notices to requesters STOP until contacts are supplied.** Measured: today the live function has no switch for client notices (its environment holds no such variable, section 1) and sends `ack` when a ticket is created and `pickup` when it is claimed, to the requester address the request body names (the pre-release `_client_recipients` read `requester.email`, base `b84a2ca293`; in the bound blob the two call sites are `create_ticket`'s `notify_client_isolated(item, "ack")` at line 1369 and the claim path's `"pickup"` at line 1658). Per the CTO's ruling (section 7) the requesters affected are Opal staff, because the Ticket Center is internal-only until Andrew opens it to clients, so no client-visible notice is lost.
2. `svc-analyst-intake` lists only `49financial`, `inflection`, `cottonwood` (`ANALYST_INTAKE_ALLOWED_FIRMS`); `ALL` is never a wildcard.
3. A staff PROFILE row with no `allowedFirmIds` and no `scope_all_firms` marker is refused (`403 firm scope not configured`) instead of reaching every firm. The 19 active staff rows that depended on the omission carry the marker (`TO-R19-MIG`, MIG-OK).

**Not newly possible:** any CLIENT login using round 18's routes; any object outside the three prefixes; any change to the analysis request, package, commentary, claim, complete or report routes.

## 3. Preconditions, each read by the applier before the apply (a failed one is a STOP, reported first)

1. **The laptop's bucket change is live:** `get-bucket-policy` and `get-bucket-cors` on each of the three buckets: the ticket role confined to the two actions on the prefix only (the Deny `NotAction` `s3:GetObject`, `s3:PutObject`; the Deny on those two actions with `NotResource` the prefix; the Allow of `s3:GetObject` on the prefix; `s3:PutObject` comes from this release's identity statement, see "Re-measured at signing"), the prefix snake_case (`portal/<firm>/state/ticket_attachments/trade-form/`; a statement built from the earlier kebab-case rows is a STOP), CORS present with the portal's DEV and PROD origins exactly (no `*`), `PUT` and `GET`.
2. **The staff-row migration reads MIG-OK:** `r19_mig_check.py` at `af529513ba89` prints `MIG-OK` against the live table and `R19_MIG_RESULT.json` exists (the CTO's condition on the migration pair).
3. **Client notices decided: RULED (section 7).** `CLIENT_NOTICE_CONTACT_MAP` ships exactly `{}` in this apply; the applier types no contact into Terraform (the plan's value for that variable must read `{}`, any other value is a STOP).
4. No open ledger names `opal-ticket-api` in any live worktree (print the per-tree denominator); the live `CodeSha256` still reads the baseline or an explained successor.
5. The package differs from the live one by exactly this tree's ticket source (member by member).
6. `terraform` and `safe-apply` run on dell2 (the worker shells report the binary absent); else STOP, no hand edit, no `aws lambda update-function-code`.

## 4. The expected plan, exactly

Three `aws_apigatewayv2_route` additions (`POST /api/scoped/tickets/{ticketId}/meeting`, `POST /api/scoped/tickets/attachment-upload`, `GET /api/scoped/tickets/{ticketId}/attachment`); the Lambda's environment gains `TICKET_ATTACH_BUCKET_TEMPLATE`, `TICKET_ATTACH_KEY_TEMPLATE`, `ANALYST_INTAKE_ALLOWED_FIRMS`, `CLIENT_NOTICE_CONTACT_MAP` and `ROUTING_MATRIX` changes only in `meeting_request.primary`; one IAM statement addition; the function code update from the package. Any other resource or attribute: STOP before apply.

## 5. Blast radius and rollback per key

| key | touched | rollback |
|---|---|---|
| Lambda code | the package of section 1 | the applier saves the live package (S3 version or a copy named by its sha) BEFORE the upload; re-apply the pre-release tree with it |
| Lambda environment | +4 variables, `ROUTING_MATRIX` value | re-apply the pre-release `main.tf` |
| API `7k3ed8px20` routes | +3 | re-apply the pre-release tree |
| role `opal-ticket-api-role` | +1 statement | re-apply the pre-release tree |
| `opal-users-v2` markers | none touched by this release | **order matters: roll the release back FIRST, then the marker; a marker rollback while the release is live is refused** |

The release creates no ticket, reads none in detail and writes nothing to a bucket. The run that exercises round 18 is `TO-R18-RUN` under its own pair.

## 6. The act's evidence

Both `R18_REL_RESULT.json` and `R19_REL_RESULT.json` (the same hashes in each) and both checks printing `REL-OK`; a change-management ledger entry opened at the start and closed after both read-backs.
**The release receipt states the stop, in these words:** "requester ack and pickup notices are off until the firm contact map is set".
**The after-read (the CTO's condition: no notice goes to a body-named address), read by the issuer after `TO-R18-RUN`:** in the log group `/aws/lambda/opal-ticket-api` (14-day retention; read-only `filter-log-events`, with `MSYS_NO_PATHCONV=1` for the leading slash), from the release's apply-end timestamp: **zero `WE_CLIENT_SENT` lines**, and **at least one `WE_CLIENT_NO_CONTACT` line** (the run files two tickets and claims or completes them, so the notice path is exercised; a zero `WE_CLIENT_SENT` with no `WE_CLIENT_NO_CONTACT` is NOT a pass, it is an unexercised path). The instrument is proven able to see the token: before the release the same filter returns live `WE_CLIENT_SENT kind=pickup` lines (three read on 2026-10-16, tickets of 2026-10-09 and 2026-10-11). The denominator (events scanned in the window) is printed beside the count.

## 7. The decision on client notices: RULED 2026-10-16 (call `dell2-20261016T060733Z-d33f`, CTO msg 9120, closed)

`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_TCKT_VNEXT_CLIENT_NOTICE_MAP_EMPTY_AT_RELEASE_20261016.md`: **ship the map EMPTY (fail closed); it needs no word from Andrew.** The Ticket Center is internal-only (PRD v0.6), so the notices that stop are staff ones and failing closed beats a body-named address; no contacts are typed into Terraform. **Owed before the Ticket Center opens to clients (not before this release):** one contact per enabled firm, sourced from the firm registry or CRM by `2.0.0_SA_COO~V2` and confirmed by the CTO; it lands before or with that opening.

## Re-measured at signing (2026-10-16 ~16:3xZ, by the issuer, live reads)

- **Section 1's six blobs** all equal at HEAD (`git hash-object`): `501c46097813`, `748e680fd7f8`, `8cde2e8c07cf`, `2268c668fcaf`, `ae9e25b4d8a1`, `af529513ba89`.
- **Live baseline unchanged:** `opal-ticket-api` `CodeSha256` `Fg8MdfvCvcB8at9K+Bh+IpmuNel8TNWXaKth0W2pv4A=`, last modified `2026-10-14T15:10:00.000+0000`; environment keys `PACKAGE_ALLOWED_FIRMS`, `TABLE_NAME`, `TICKET_DEEP_LINK_BASE`, `CUTOFF_ET`, `COMMENTARY_ALLOWED_FIRMS`, `ROUTING_MATRIX`, `TICKET_DL_MAP`, `USERS_TABLE`, `IRPT_REQUESTS_TABLE`, `CLIENT_LINK_MAP` (ten; none of the four new variables).
- **Precondition 3.1, the laptop's change is LIVE (the laptop CTO's msg 109725, apply `b156a4a2b4`; read by the issuer on all three buckets):** each of `opal-data-49financial`, `-inflection`, `-cottonwood` names `opal-ticket-api-role` in four statements: `DenyForeignFirmPrincipals` (the role is in its not-like list), `DenyScopedExemptionNAnyOtherAction` (NotAction `s3:GetObject`, `s3:PutObject`), `DenyScopedExemptionNObjectsOutsidePrefix` (Get and Put, NotResource the snake_case prefix `portal/<firm>/state/ticket_attachments/trade-form/*`) and `AllowScopedExemptionNObjects`. CORS on each: one rule, methods `GET` and `PUT`, allowed headers `Content-Type`, exposed `ETag`, max age 300, origins exactly `http://localhost:5174`, `https://www.opalinvest.dev`, `https://opalinvest.dev` (no `*`). **A correction of this pair's own wording, read from the bytes:** the bucket policy's Allow statement carries `s3:GetObject` ONLY; `s3:PutObject` on the prefix is not denied by the bucket (the Deny statements admit both actions on the prefix and nothing else) and is GRANTED by this release's identity statement `TicketAttachmentsTradeForm` (section 5, the role's own policy; same account, so the identity Allow is sufficient). The applier's step-1 read therefore checks the Deny shapes and the Allow Get, and the identity statement arrives with the apply; a bucket Allow for PutObject is NOT expected and is not a STOP.

## COO half -- SIGNED

I sign sections 1 to 7 at the bytes and the live baseline above. The apply is ONE apply by `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R18-REL` with `TO-R19-REL` folded in; its GO is a conditional amendment that makes the applier measure the six blobs and print the precondition reads before the first write. The release widens round 18's routes and narrows round 19's admissions as stated in section 2; it changes no served output of a pipeline and no client-facing page.

`2.0.0_SA_COO~V2`, 2026-10-16.

## CTO half

(owed: `1.0.0_SA_CTO~DELL2` signs in its own file or message, citing this file at its blob.)
