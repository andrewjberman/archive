# Packet -- TV-d-1: the ticket service's round-1 code and one new route reach DEV's served API (TCKT_VNEXT round 1)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author and operator:** `2.0.0_SA_COO~V2` (dell2), 2026-10-07 ~19:0xZ.
**Authority:** PRD v0.2 @99eb4053c2 (ADMITTED); decomposition `decompositions/TCKT_VNEXT_DECOMP.md` cell TV-d-1; drains @23759c51d2,
@4e28d4d77f; hookups @da43155418. **COO half: SIGNED below.** No vendor call, no alarm, no SNS, no new SES path, no grant, no
`aws_lambda_permission`, no bucket, no IAM change.

## 1. What ships (one function, one route)

| | value |
|---|---|
| code | CLOUD `da43155418`, `infra/aws/lambda/ticket_center/lambda_function.py` (LOCAL). Since the deployed build (`481dde1dbf`) exactly two commits touch it: `53575b1cfd` (worker ~1) and `da43155418` (the fee default) |
| package | `BUILD_ONLY=1 build-and-upload.sh ticket-center opal-ticket-api` at `da43155418`: 28K, sha256 `y0UFtRIfZxu3x6BCFSGLjXsNgScCl/GPuWNHbmZV7BI=`. Deployed today (read from dell2 ~19:0xZ): `/38KUtP9qHaUJMJi55+bSk7X6qBgtfkbH+iOK9ajVSA=`, LastModified 2026-08-21T20:39:07Z, equal to the source map's `artifact_sha256` at `481dde1dbf` |
| plan (read from dell2 ~18:5xZ, before the upload) | **1 to add, 1 to change, 0 to destroy**: `aws_apigatewayv2_route.tickets["report"]` created (`POST /api/scoped/tickets/{ticketId}/report`, CUSTOM authorizer `naqxlm`, the existing integration); `module.opal_ticket_api.aws_lambda_function.this` in place: `ROUTING_MATRIX` gains `analysis_request` (primary manav@, alyssa@). The code hash moves only after the upload, so the apply re-plans and must read 1/1/0 with `source_code_hash` /38K... -> y0UF... added |
| suite | ticket_center 89 passed / 43 subtests at `da43155418` (run with invalid AWS keys -- row D2-W1-S4); commit-gate clean 3 of 3 |

## 2. Blast radius, by branch

**Writers of the named property.** The `opal-tickets` table's items: 1 writer, this function (every other party writes through its
routes). The new item fields `answers`, `attachment`, `report_ref` and the `report_recorded` event have 1 writer, this function.
`ROUTING_MATRIX` has 1 writer, Terraform from `main.tf`. The function's IAM role and its SES path are unchanged.

**Behaviour that moves for existing traffic (read from the producer's own code at `da43155418`, both branches):**
- **Self-claim (the one widening).** `_sod_block` no longer refuses a requester claiming or completing their own ticket. CLAIM and
  COMPLETE stay INTERNAL-only in `MATRIX`, so the widening reaches internal users only: an internal person may now claim and complete
  a ticket they filed. A client-filed ticket's requester is a client, who still cannot claim. This is Andrew's ruling (2026-09-30,
  "that rule of no one can file and run their own ticket is nonsensical", all tickets; PRD C-SELF-CLAIM). The complete-by-non-holder
  refusal is unchanged.
- **The four existing types:** unchanged. Unknown fields on them are ignored and not stored, as today (row D2-W1-S2).
- **New:** `analysis_request` on the INTERNAL CREATE route only; `POST .../report` INTERNAL, assignee-only. The client SUBMIT path
  and its authorization are unchanged (`SUBMIT_ALLOWED_FIELDS` untouched).

| branch | what the apply writes | rollback per key |
|---|---|---|
| apply succeeds | the function's code (y0UF...) and its `ROUTING_MATRIX` value; one API route | re-apply the build at `481dde1dbf` (`/38K...`) and remove the `report` route line; the table items created meanwhile with `answers`/`attachment`/`report_ref` stay readable by the old code (extra attributes are ignored) |
| apply fails partway (route created, function not updated, or the reverse) | at most one of the two | finish in-session or roll back to the row above; the ledger stays OPEN until one of them holds |

## 3. Sequence and grading

1. Ledger entry opened (`.tools/` open-deploy form; legs L1 upload, L2 apply 1/1/0, L3 verify CodeSha256 y0UF... + route present, L4
   0-diff plan, L5 record-terraform-deploy) before the upload.
2. `build-and-upload.sh ticket-center opal-ticket-api` (uploads `ticket-center/opal-ticket-api.zip`, updates the source map).
3. `.tools/safe-apply.sh -chdir=infra/aws/terraform/ticket-center apply`, re-planned at apply.
4. `get-function-configuration` reads CodeSha256 y0UF...; `get-routes` shows the report route; `terraform plan` reads No changes.
5. The served behaviour is graded by TV-r-1 (the real run), which also waits on X-1 (IRPT_BCKEND's door, not live yet).

**Which machine applies:** dell2. No Lambda permission, no bucket policy, no grant. `terraform plan` from dell2 read state and the
whole module without refusal.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-07: SIGNED for the blast radius above, both branches: the function's code at `da43155418` (y0UF...), its
`ROUTING_MATRIX` value, and one API route; rollback = the build at `481dde1dbf` (/38K...) and the route line removed.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
