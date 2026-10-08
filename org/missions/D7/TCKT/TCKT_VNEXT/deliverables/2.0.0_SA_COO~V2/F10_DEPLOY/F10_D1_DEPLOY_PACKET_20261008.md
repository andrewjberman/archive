# Packet -- F10-d-1: the ticket service's svc-commentary code and its firm list reach the served API (TCKT_VNEXT workstream F10)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2` (dell2), 2026-10-08 ~22:5xZ.

**Applier:** `0.7.0_AE_CloudOps~DELL2`, which deploys for dell2 (Andrew-direct msg 1758).

**Authority:**
- PRD ADDENDUM 1 @f8c019c28f;
- decomposition `decompositions/TCKT_VNEXT_DECOMP_F10.md`, cell F10-d-1;
- drain @49c04cd4b2 (TO-F10-l1, 3 of 3 criteria re-run by the issuer);
- hookup @2c70e239fa.

**COO half: SIGNED below.** No vendor call, no alarm, no SNS, no new SES path, no route, no grant, no Lambda permission, no IAM.

## 1. What ships (one function's code and one environment value)

| | value |
|---|---|
| code | box/dell2 `2c70e239fa`, `infra/aws/lambda/ticket_center/lambda_function.py` (+88/-8 since the deployed `da43155418`; the only code commit is worker ~3's `8ae7ed7dad`) |
| env | ONE added key on `opal-ticket-api`: `COMMENTARY_ALLOWED_FIRMS = "49financial,cottonwood,inflection"` (`main.tf`, hookup @2c70e239fa). The other 7 keys are unchanged. |
| package | built at `2c70e239fa`: content-sha256 `OuTw3wWmtsxa5bAf/k4244hGDoCucyfb2KGd+mo3xc4=`. The artifact key was restored to the deployed `y0UF...` at ~22:51Z after an unintended upload (row D2-S7), so the applier's upload is the real one. |
| live now (read 22:5xZ) | CodeSha256 `y0UFtRIfZxu3x6BCFSGLjXsNgScCl/GPuWNHbmZV7BI=`, LastModified 2026-10-07T19:21:15Z; `opal-tickets` ItemCount 12 |
| suite | ticket_center 104 passed / 43 subtests at `49c04cd4b2`; commit-gate clean |

## 2. Blast radius, by branch

**Writers.** The `opal-tickets` items have 1 writer, this function. The new item fields `draft_commentary` and `report_ref` (the
create-time form of `report_ref`) also have 1 writer, this function. The env value has 1 writer, Terraform.

**Behaviour that moves for existing traffic, read from the producer's code at `2c70e239fa`:**
- **The one widening:** a fourth CREATE principal, `svc-commentary`. It may create `analysis_request` only, for the three listed firms
  only, and has no other action. No token for it exists until leg M of the mint pair
  (`F10_DEPLOY/NEVER_WIDEN_PAIR_SVC_COMMENTARY_MINT.md`, both halves GIVEN). Between legs D and M the widening is therefore
  unreachable.
- **One narrowing:** `draft_commentary` and `report_request_id` sent by ANY other principal (an internal human included) now return
  400. Today they are ignored. No deployed caller sends either. Census at 22:5xZ:
  - workspace `*.{py,ts,tsx,mjs,js}`: 6 files, which are the handler, its test, this checks file, and `~T2`'s
    `data/transcripts/scripts/commentary/{entry,ticket_client}.py` plus its test (H6, not deployed, coded against the stub);
  - portal `origin/DEV` `src`: 0 hits.
- **The DL email** loses nothing it sends today. `draft_commentary` is added to its prohibited list.
- **Unchanged:** the four untyped types, the client SUBMIT path, human CREATE, CLAIM, COMPLETE, REPORT and LIST.

| branch | what the apply writes | rollback per key |
|---|---|---|
| apply succeeds | the function code (OuTw3w...) and one env key | re-apply the build at `da43155418` (artifact version `ZBF40mIM...` = y0UF...) and remove the env line; any svc-commentary ticket stays an ordinary `analysis_request` item |
| apply fails partway (code updated, env not, or the reverse) | at most one of the two | code without env = svc-commentary refused for every firm (fails closed); env without code = an unread value. Finish in-session or roll back to the row above. The ledger stays OPEN until one holds |

## 3. Sequence (leg D; leg M follows per the mint pair)

1. Ledger entry opened before the upload. NEVER-2 family sweep: `opal-ticket-api` is the only function on this artifact key.
2. Before-read: CodeSha256 `y0UF...`; env keys (7); the `opal-tickets` count.
3. `build-and-upload.sh ticket-center opal-ticket-api` at the order's pinned commit. The content-sha256 must equal `OuTw3w...`;
   otherwise STOP (branch B).
4. `safe-apply` in `infra/aws/terraform/ticket-center`. Expect **0 to add, 1 to change, 0 to destroy**: `module.opal_ticket_api`'s
   function, with source_code_hash plus `environment.variables` gaining exactly `COMMENTARY_ALLOWED_FIRMS`. Anything else is
   branch B: STOP.
5. After-reads:
   - (a) CodeSha256 `OuTw3w...`;
   - (b) env holds 8 keys, the new one exactly `49financial,cottonwood,inflection`;
   - (c) the deployed zip's `lambda_function.py` sha256 equals the file at the pinned commit;
   - (d) the 08-12 read on deployed bytes: an unauthenticated `POST /api/scoped/tickets` through CloudFront is refused at the
     authorizer;
   - (e) `opal-tickets` count unchanged;
   - (f) a 0-diff plan.
6. Leg M (the mint pair) runs only after 5 passes.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-08: SIGNED for the blast radius above, both branches: the function's code at `2c70e239fa` (OuTw3w...)
and one env key. Rollback is the build at `da43155418` (artifact version ZBF40mIM..., y0UF...) with the env line removed.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
