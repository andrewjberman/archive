# Never-widen ask -- OG-rl-11, the r25 opal-gateway release on live 7d65a28db0 (round 24)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-07.
- **Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-11.gateway-release-r25.md` (@2cb25e2cf0).
- **Spec:** CTO R33 (`ledger/ROUND_ANALYSIS.round23.md` @c8a3b2911e, section 4 item 3) for part 1. For part 2, the
  release request of `2.0.0_SA_COO~AI` (OA-f-14 on CLOUD @af10f7d42b) and the CTO's msg 30365. Cut to
  `RELEASE_ORDER_FORM.md` (@0b894aa47d).
- **PHASE A evidence:** `deliverables/0.9.0_WK_NFRA_OPLGTW~28/ANNOUNCE_OG-rl-11.md`, worker commit `007e0b8e96`.
- **Release sha the halves sign:** `240ac2fe5abde944f15358ab563cb4b2ab63f09f`, branch `rel-nfra-oplgtw-r25`.

**Halves owed, all three against THIS file at its commit:**
- `1.0.0_SA_CTO~O` (CTO);
- `3.0.0_SA_CVO~O` (CVO), REQUIRED: a tool is added, a send's behaviour changes, and one identity's consent narrows;
- `2.0.0_SA_COO~O` (COO): signed in section 5.

## 1. The bytes

**Release branch.** `rel-nfra-oplgtw-r25` (`/c/tmp/og-rel20`), one commit on live `7d65a28db0`, 8 files (+873/-28).
Host md5 reads 96 of 96 equal to live. The issuer's own reads at 05:0xZ:
- `git diff --name-only 7d65a28db0 240ac2fe5a` lists 8 files, all in the gateway tree;
- `git diff --stat 240ac2fe5a CLOUD -- infra/aws/ec2/opal-gateway` is one line, the CLOUD-only runbook;
- `identity_tool_allowlist.txt` is unchanged.

| File | Ships to the host | Change | Cell |
|---|---|---|---|
| `app/integrations/opal_portal/integration.py` | yes | the send returns after `/trigger`; new read-only `opal_data_refresh_status`; idempotent re-send | OG-up-1 |
| `app/data_entitlement.py` | yes | the new tool joins `INTEGRATION_TOOLS` | OG-up-1 |
| `app/graph_scope_map.py` (new) | yes | Graph scopes per tool, and per non-tool caller; the new tool maps to none | OA-f-14, OG-up-1 |
| `app/identity_scope.py` | yes | `consent_scopes(email)`: None when unscoped, the union when scoped | OA-f-14 |
| `app/token_broker.py` | yes | consent, redeem and silent acquire use `consent_scopes` for a scoped identity | OA-f-14 |
| `tests/test_entitlement_admin.py` | no | the tool pin and count the new tool moves | OG-up-1 |
| `tests/test_opal_portal_send_split.py` | no | tests | OG-up-1 |
| `tests/test_scoped_consent_r253.py` | no | tests | OA-f-14 |

**Tests, each file in its own process.** Release tree: 74 files, 613 passed, 7 failed. Rollback tree: 72 files, 601
passed, 7 failed. The 7 ids are the same on both, so none is new. **R21:** one tool is added and no route;
`test_principal_cutover.py` 11 passed and `test_data_entitlement_guard.py` 12 passed.

**Rollback.** `/c/tmp/og-rb19` at `7d65a28db0`, 96 of 96 equal to the live S3 artifact. `.env` is unchanged in either
direction.

## 2. Blast radius -- what the act may touch

**Part 1: the data-refresh send (CTO R33).**
- Before: `opal_data_refresh_upload(confirm=True)` polls up to 15 minutes inside the call. 65 tools.
- After: it returns within 22 s of `/trigger` with the execution id. A new read-only tool,
  `opal_data_refresh_status`, reads the status and the manifest. 66 tools.
- An identical send (two files, same names and sizes) within 30 minutes returns the earlier execution id and does not
  POST `/trigger` again. The record is in-process; a gateway restart clears it.
- `dry_run=True` is unchanged.
- Rollback: redeploy `og-rb19`; the tool goes away and the send polls again.

**Part 2: the scoped identity's consent (OA-f-14).**
- Before: the one scoped identity, the Teams concierge, is sent to a consent of 17 Graph scopes.
- After: 9 scopes: `Channel.ReadBasic.All`, `ChannelMessage.Read.All`, `ChannelMessage.Send`, `Chat.ReadWrite`,
  `ChatMessage.Send`, `Files.ReadWrite.All`, `Sites.Read.All`, `Team.ReadBasic.All`, `User.Read`. It is 9 and not 8
  because the Tax workbook route mints under this identity (the pre-GO read, below), so `Files.ReadWrite.All` joins.
- An unscoped identity stays at 17.
- Rollback: redeploy `og-rb19`; consent returns to 17 for new sign-ins.

**Unchanged:** every other tool and route; the allowlist (no row is added); grants and the state store (0 writes);
`.env`; the S41 grant; Terraform, IAM, the ALB, secrets and the template. The service restarts once.

**Manifest.** `deployed_commit` moves; the previous value is `7d65a28db0`.

## 3. The named properties and their writers

**(a) How long a real send holds the call, and whether a repeat fires the pipeline.**
- Writers, N = 1 each: the send's return path; the in-process idempotency record.
- Expected: a return within 60 s (measured bound 22 s); a repeat within 30 minutes does not trigger.
- Other branch: a different file size, more than 30 minutes, or a restarted gateway DOES trigger. That is by design.
- Limit: both branches rest on offline fixtures. This project runs no `confirm=True` send. The first real send after
  the release is the first live exercise.

**(b) Which Graph scopes the scoped identity is asked for, and acquires silently.**
- Writers, N = 3 call sites (consent URL, redeem, silent acquire), all through one function, `consent_scopes`, over one
  map and one caller table.
- Expected (rehearsed on the host with the staged bytes): the silent acquire returns a token, and 9 of 9 read-only
  Graph probes answer 200, the SharePoint site resolve and the project-folder listing among them. Those two are the
  delegated leg of the daily Bloomberg send.
- Other branch: a scoped identity with no usable cached sign-in is sent to `/login` for the 9-scope consent. That
  branch rests on release-tree fixtures only.
- Limit (row Z-W28-S11): the narrowed silent acquire still returns a token that lists the identity's full prior
  consent. The narrowing takes hold at the concierge's next `/login`, not at the release. So the release is not the
  moment a missing scope would show.
- Limit: `ChatMessage.Send` and `ChannelMessage.Send` are POST-only and were not probed.

**(c) The three non-tool callers (CTO msg 30365), read on the live host before GO.**
- `TAXSMA_WORKBOOK_IDENTITY` names the scoped identity: TRUE, and its scope is in the union. The host key has no
  `OG_` prefix (row Z-W28-S12).
- `MS_INGEST_IDENTITY`: false. `OTP_MAILBOX`: false.

**(d) Every other property.** The floor holds on live (`rl4.AC1`, `ht.AC2`). The staged rehearsal re-read the two
standing fixes: the portal login is OK, and the real holder gets 2150 = 2150 = 2150 with 0 unheld on both paths.

## 4. Act and verify

1. Re-read live; if it moved, re-cut.
2. Open ledger `nfra-oplgtw-gateway-release-r25`, with entry and sentinel committed first.
3. Run `r25_verify.sh before`. Deploy from `/c/tmp/og-rel20` by the form's step 10 (the issuer-serial halt-gate route).
4. Run `r25_verify.sh after` immediately, then `r25_postdeploy.sh`: `RL11_SEND.json`, `RL11_SCOPES.json` and
   `RL11_FLOOR.json`, through the installed code, one host run at a time.
5. Rollback triggers: a scoped silent acquire that is not OK; any probe not 200; a status tool that errors; a portal
   login that is not OK; a real-holder read off its bar.
6. **No `/login` for the concierge between GO and the ledger close.** A 9-scope sign-in in that window would force a
   re-consent on rollback.
7. Run `rl11.AC1` to `AC3`. All three were exercised pre-GO, each with a pass form and negative controls.

## 5. Halves

**COO -- SIGNED, `2.0.0_SA_COO~O`, 2026-10-07.**
- The act may touch exactly the keys in section 2 and the manifest.
- The rollback is pre-built and proven.
- Both branches are named for each property in section 3, with each property's writers counted.
- Four limits are disclosed: the send's two branches are fixture-only; the narrowing bites at the next `/login`; the two
  send scopes were not probed; the no-cache branch is fixture-only.
- My reads of release vs live (8 files), release vs CLOUD (the runbook only) and the unchanged allowlist are
  independent of the worker's.
- Carried to Andrew, not decided here: whether the concierge may call the new read-only status tool.

**CTO -- owed.**

**CVO -- owed** (required).
