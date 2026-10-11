# Packet -- R3-rf-2 deploy: the ticket's report path also admits the ticket's creator, once (TCKT_VNEXT round 3)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~13:0xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** CTO rulings msg 4921 item 2 (one build cell for hop 16), msg 4945 (the design stands; what the pair must name) and
msg 4954 (the deploy is not held on row TCKT_VNEXT-D2-S40; the pair says so in words). Decomposition
`decompositions/TCKT_VNEXT_DECOMP_R3.md` ADDENDUM 2, cell `R3-rf-1` (built); this apply is `R3-rf-2`, an issuer cell under this
pair. The drain: `R3-rf-1` merged @8ef21584f8. On the merged tree this seat re-ran `RF-FILER-OK passed=6 of 6` and
`RF-REGRESS-OK passed=169 (min 167) failed=0`; `commit-gate.sh` clean on the handler and the new test file.

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant, no matrix change. **THIS APPLY WIDENS A WRITER.**

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `8ef21584f8`; file sha256 `dc0cd973c61f4b037e7181f4675ec8ffe2ec68414cfd9e036c01f4096f386a15` (`git show HEAD:<file> \| sha256sum` and `sha256sum`, this seat) |
| the diff from the live build's file | `git diff --numstat be67d1fd38 HEAD -- <file>` reads 36 added / 10 removed, all inside `report_ticket`; **every hunk was read by this seat** (the branch decision, the creator's four refusals, the two conditions, the changed-under-write answer, the docstring) |
| live now | `opal-ticket-api` CodeSha256 `t1EoiJRZ...`, LastModified 2026-10-11T09:47:09Z (this seat, 13:00Z); deployed file `cf10e19e...` (pin `be67d1fd38`; the source map names it, commit `861c9bba65`) |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |

## 2. Blast radius, by branch

**Behaviour that moves:** ONE route, `POST /api/scoped/tickets/{ticketId}/report`. The matrix row is unchanged: internal callers
only, inside their firm scope.
- **The assignee's path is unchanged**: an `in_progress` ticket with an attachment; it may still record over an existing value;
  its answers and its conditional write are the same bytes.
- **NEW: the ticket's creator** (`created_by` equals the caller's email), when it is not the assignee, may record `report_ref`
  on its own ticket when the ticket is an `analysis_request`, is not completed, carries an attachment and has NO `report_ref`.
  Write-once: the pre-check answers 409 `REPORT_ALREADY_RECORDED`, and the write's own condition carries
  `attribute_not_exists(report_ref)`, so a race answers 409 `REPORT_TICKET_CHANGED`. Neither body carries the ticket.
- **One answer changes for a caller admitted by neither branch:** on a ticket that is not `in_progress`, a caller who is neither
  assignee nor creator now gets 403 where it got the status 409 before (the branch is decided first). Nothing is written either way.

**In the CTO's words (msg 4954), and they are the condition of this half: every reader of these tickets is internal and may
already open any request; the creator's write is unbound until the binding cell lands.** Read by this seat:
`infra/aws/lambda/investor-reporting/_scope/interactive_access.py:115-116` admits an Opal-internal reader to any owner's request;
lines 117-119 hold an ordinary viewer to its own. So a creator who records another person's request id widens no access; it can
make its own ticket show a report that is not that ticket's. The binding (the report read refused when the request's stored
`ticket_id` differs) is `2.0.0_SA_COO~Y2`'s cell. Row TCKT_VNEXT-D2-S40 stays open until it lands.

**Who can reach the new branch today: nobody by a product path.** The portal's form does not yet call this route for a one-step
ticket; that call is `2.0.0_SA_COO~Y2`'s cell and its candidate goes to the CTO. Callers of the route in the portal checkout on
this box (`portal/src`, not re-read against `origin/DEV`): 1 site, `pages/TicketCenter/analysisRequest.ts:169`, the assignee's
flow. The journey runner calls it as an assignee. An internal caller could reach the new branch by hand on a ticket it created.

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code | re-apply the build of `be67d1fd38` (file `cf10e19e...`), same method |
| apply fails partway | nothing else to land (code only) | as above; the ledger stays open until one holds |
| step 1 finds the live file is NOT `cf10e19e...` | nothing: STOP before any plan | none; reported to the CTO |
| the deploy recorder half-lands (the source map written, its notice not sent, or the reverse) | the source map entry | STOP and report; the map is corrected in the same sitting (row TCKT_VNEXT-D2-S36) |

Rows the new branch can write: only `opal-tickets` items whose `created_by` is the caller, one attribute (`report_ref`) and one
event row, once per ticket. A wrong value recorded by a creator cannot be replaced by that creator; an assignee can record over it.

## 3. The act and its after-reads

0. Open the NEVER-2 ledger entry FIRST; read every live worktree's `.open_deploys/`, union them, print the per-tree denominator; an
   open entry naming `opal-ticket-api` other than this one and the fourth run's is a STOP. **The fourth run's entry
   (`tckt-vnext-r3-tr1-fwd1-fourth-run-20261011`) is expected OPEN until its row delete at 13:19:00Z; this apply starts after it
   is closed**, so the two acts never overlap on one function.
1. Before the apply: download the live `opal-ticket-api` package and show the deployed `lambda_function.py` sha256 is
   `cf10e19e...`. Anything else is a STOP.
2. Apply through `safe-apply` (Terraform only), plan read first: exactly 1 to change.
3. After: CodeSha256 equals the uploaded zip, and the deployed file is `dc0cd973...`.
4. An unauthenticated POST to the report route returns 401.
5. `opal-tickets` ItemCount unchanged; `TCK-20261009-a1052909` reads the same status fields as before (positive control).
6. The replan is 0-diff.
7. `record-terraform-deploy.sh` for `opal-ticket-api`; then `clamp_precheck.py` reads `READ27 27/27` with the ticket host CLAMPED
   on the new build (the precheck decides from the source map, so it has no hand list to edit).

**The live arms of the creator branch are NOT exercised by this apply.** They need an internal token on a ticket the caller
created; this pair mints no identity and writes no ticket. They are exercised by the form's call when `2.0.0_SA_COO~Y2`'s cell
lands, or by a later run under its own pair. No request is sent down the YCharts path by this act (CTO msg 4918).

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11: SIGNED for the blast radius above and all four branches, on the ordering condition (after the
fourth run's ledger entry is closed).

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
