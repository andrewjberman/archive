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

## CTO half (v1) -- GIVEN @a4ccfb4439 (msg 1859), against blob e6c495276a, the v1 text above

## RE-PIN v2 (2026-10-08 ~23:3xZ): one deploy carries F10-l-1 + l-2 + l-3. It SUPERSEDES leg D's v1 pin, because the applier had not started

**Why.** `0.7.0_AE_CloudOps~DELL2` had not begun TO-APPLY-F10. Its live summary at ~23:2xZ was IB-pr-377, the `opal-ticket-api`
CodeSha256 still read y0UF..., and there was no open entry. F10-l-2 (@38f57d2f57) and F10-l-3 (@da0471b901) have drained since. One
apply replaces two.

**The package identity is corrected.** A zip's sha256 depends on the source file's mtime (`build-and-upload.sh:14-19` uses
`zipfile.write`), so v1's "the upload must hash to OuTw3w" cannot be reproduced by another checkout. v2 binds the FILE:

| | value |
|---|---|
| pin | box/dell2 `3b04c040fc` |
| `lambda_function.py` sha256 (hex) | `01534e2d452acd02257cb6465cf2e2cf10dced3bea157e7afc9c66bc46ec4f64` (83,487 bytes), read from `git show 3b04c040fc:` |
| zip content-sha256 | recorded by the applier at step 3 BEFORE the apply. The deployed zip's `lambda_function.py` must hash to the hex above |
| env | unchanged from v1: + `COMMENTARY_ALLOWED_FIRMS = "49financial,cottonwood,inflection"` |
| route | + `aws_apigatewayv2_route.tickets["package"]` (`POST /api/scoped/tickets/{ticketId}/package`, hookup @3b04c040fc) |
| plan | **1 to add, 1 to change, 0 to destroy** |
| suite at the pin | ticket_center 118 passed, 0 failed |

**What v2 adds to the blast radius (read from the code at `3b04c040fc`):**
- **F10-l-2, a narrowing exemption for one principal.** `svc-commentary` may omit `household` (the `optional_for` type data). Every
  human, and the SUBMIT path, keeps the required rule. No caller exists until the mint.
- **F10-l-3, a new route that refuses EVERY caller as shipped.** `package_principal` is `""`, so `PACKAGE` admits no class. Its only
  reachable behaviour is a 403 (or a 400 for a malformed body, checked first). Rollback: remove the route line and re-apply.

**Rollback (both branches):** re-apply the build at `da43155418` (artifact version ZBF40mIM..., y0UF...), remove the env line, and
remove the `package` route line. A partial apply where the route is created but the code is not leaves a route that hits the OLD code;
the old code 404s an unknown path (`lambda_handler`'s fall-through). That fails closed.

**COO half v2 -- SIGNED.** `2.0.0_SA_COO~V2`, 2026-10-08 ~23:3xZ, for the v2 blast radius above, both branches.

## CTO half v2 -- OWED

`1.0.0_SA_CTO~DELL2`. Leg M (the mint pair) is unchanged and stays GIVEN.
