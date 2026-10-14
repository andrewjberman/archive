# TCKT_VNEXT round 18 -- the ticket service release (meeting route, trade-form routes, permission): never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~V2` (dell2), 2026-10-14. **Executor:** `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R18-REL` (staged until this pair is SIGNED on both halves and the laptop's
bucket apply reads back). **Outcome served:** FWD-10 and FWD-11 (PRD v0.6), due 2026-10-24. **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.

## 1. What is released, bound to bytes (not to a commit that moves)

The release builds from the TREE whose three source files equal these blobs (`git rev-parse <rev>:<path>`, first 12 shown; the applier prints the full ids and compares):

| file | blob | where it came from |
|---|---|---|
| `infra/aws/lambda/ticket_center/lambda_function.py` | `b51d9ab912da` | chain A, merge `fb3734e380` (cells R18-mt-1, R18-tf-2) |
| `infra/aws/terraform/ticket-center/main.tf` | `17298d3fb7d9` | chain B, merge `6d0d42f08e` (cells R18-mt-2, R18-tf-3) |
| `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/0.9.0_WK_TCKT_VNEXT~43/ATTACH_ADDRESS.json` | `8cde2e8c07cf` | cell R18-tf-1: builder output, state tier (doctrine R21), table `ticket_attachments` |

A later commit that changes any of the three voids this pair until it is re-read. The ticket service test folder on the merged tree reads `383 passed`.

**Live baseline read by the issuer (read-only, 2026-10-14):** function `opal-ticket-api` `CodeSha256` `Fg8MdfvCvcB8at9K+Bh+IpmuNel8TNWXaKth0W2pv4A=`, last modified `2026-10-14T15:10:00Z`, state Active; its
environment already carries `IRPT_REQUESTS_TABLE` (so `2.0.0_SA_COO~Y2`'s owner-check release is LIVE) and does NOT carry `TICKET_ATTACH_BUCKET_TEMPLATE` or `TICKET_ATTACH_KEY_TEMPLATE`. The applier re-reads it at STEP 1.

## 2. What the release makes possible that was not (the widening, stated)

1. `POST /api/scoped/tickets/{ticketId}/meeting`: an INTERNAL human whose address is in the ticket's `routing.primary` can record a confirm or a propose on a `meeting_request` ticket. No client login, no service subject.
2. `POST /api/scoped/tickets/attachment-upload` and `GET /api/scoped/tickets/{ticketId}/attachment`: an INTERNAL human can obtain a 300-second presigned PUT and GET URL for a trade form (PDF, XLSX, CSV, at most 10 MB) under a firm they are scoped to
   (`_create_firm_allowed`); the GET applies the ticket read's fence. Bytes never pass through the Lambda.
3. `ROUTING_MATRIX.meeting_request.primary` changes from `manav@opalinvest.com` and `alyssa@opalinvest.com` to `jeanette@opalinvest.com` ALONE (the coordinator Andrew named; the CTO confirmed her users row). New meeting requests route to her; tickets already filed keep the routing stored on their row.
4. The ticket Lambda role gains ONE statement, `TicketAttachmentsTradeForm`, in the policy named `opal-ticket-attachments-trade-form-policy`: `s3:PutObject` and `s3:GetObject` on `portal/<firm>/state/ticket_attachments/trade-form/*` in `opal-data-49financial`, `opal-data-inflection` and `opal-data-cottonwood` (bucket and firm taken from the `opal_name` module, not typed). Nothing else: no List, no Delete, no other prefix, no other bucket.

**Not newly possible:** any CLIENT login using any of it; any object outside the three prefixes; deleting or listing; any change to the analysis request, the package, commentary, claim, complete or report routes.

## 3. Preconditions, each read by the applier before the apply (a failed one is a STOP, reported first)

1. **The laptop's bucket change is live** (ruling `1.0.0_SA_CTO` `RULING_20261014_195xZ_TCKT_TRADE_FORM_FIRM_BUCKET_ACCESS_ROUTE.md` @ee287446e1 with Amendment 1 @bc7493406e; its own pair is `2.0.0_SA_COO~B1`'s and the laptop CTO's). Read-only `get-bucket-policy` and
   `get-bucket-cors` on EACH of the three buckets: the ticket role admitted for the two actions on the prefix only; the prefix read from the statements is `portal/<firm>/state/ticket_attachments/trade-form/` (snake_case: a statement built from the earlier kebab-case
   rows, which existed for a short window in `exemptions.json` on box/dell1 at 89beb84dd9, is a STOP); CORS present with the portal's DEV and PROD origins exactly (no `*`), `PUT` and `GET`.
2. **No open ledger names `opal-ticket-api`** in any live worktree (`git worktree list --porcelain`, then `ls-tree` of `org/critical_paths/.open_deploys/` per tree; print the denominator), and the live `CodeSha256` still reads the baseline above or an explained successor.
3. **The package differs from the live one by exactly this round:** build from the three blobs, compare member by member with the live package; the members that differ are the ticket Lambda's source only.
4. **`terraform` and `safe-apply` are available to the applier on dell2.** The worker that wrote the source reports the binary absent from its shell; if the applier cannot run `safe-apply` for this stack, STOP and report: no hand edit, no `aws lambda update-function-code` (Terraform only).

## 4. The expected plan, exactly

`safe-apply` plan for `infra/aws/terraform/ticket-center`: three `aws_apigatewayv2_route` additions (the keys in 2.1 and 2.2); the Lambda's environment gains `TICKET_ATTACH_BUCKET_TEMPLATE` (`opal-data-{firm}`) and `TICKET_ATTACH_KEY_TEMPLATE`
(`portal/{firm}/state/ticket_attachments/trade-form/`) and `ROUTING_MATRIX` changes only in `meeting_request.primary`; one IAM policy addition (the statement in 2.4); the function code update from the package. **Both branches:** if the plan shows any other resource or any other attribute, STOP before apply. If the apply
fails part-way, the applier re-applies the pre-release tree and package (section 5) and reports the state it left, first.

## 5. Blast radius and rollback per key

| key | what the release touches | rollback |
|---|---|---|
| Lambda `opal-ticket-api` code | replaced by the package of section 1 | the applier saves the live package (S3 object version or a copy named by its sha) BEFORE the upload; restore by re-applying the pre-release tree with that package |
| Lambda environment | +2 variables, `ROUTING_MATRIX` value | re-apply the pre-release `main.tf` blob (`git show <the parent of the round's first Terraform commit>:...`) |
| API `7k3ed8px20` routes | +3 | re-apply the pre-release tree (the routes are removed by Terraform) |
| role `opal-ticket-api-role` | +1 policy | re-apply the pre-release tree |
| tickets | none written by the release | -- |

The release creates no ticket, reads no ticket in detail and writes nothing to a bucket. The synthetic run that exercises it is `TO-R18-RUN` under its own pair.

## 6. The act's evidence (what makes it done)

`R18_REL_RESULT.json` (keys in the order) and the issuer's check `R18_CHECKS/r18_rel_check.py` printing `REL-OK`: it re-reads the live function (CodeSha256 equals the recorded after-hash and differs from the before-hash; the two variables equal the builder record; the routing value), the route table (each key once) and the role's statement (two actions, three ARNs derived from the record). A change-management ledger entry is opened at the start and closed after `REL-OK`.

## COO half -- SIGNED 2026-10-14 by `2.0.0_SA_COO~V2`

I read the three blobs above, the live baseline and the plan; the widening in section 2 is the whole of it. The CTO half is owed. The GO to `TO-R18-REL` is an amendment to that order citing this file's blob and the CTO's signature.
