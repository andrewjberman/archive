# Never-widen sign-off -- OG-rl-3, the /hx/teams opal-gateway release (IAM + ALB + narrow app release)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-02. Order:
`org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-3.hx-teams-release.md` @9c0dd7be13.
Authority: Andrew-direct today (laptop `0.0.0_AB_MSTR` bus d38d682f 17:17Z, relay msg 28592): "release the gateway
/hx/teams route TODAY". Spec and **CTO half** (blast radius, rollback per key):
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_20261002_NFRA_OPLGTW_HX_TEAMS_RELEASE.md` (msg 28599).
**This file is the COO half.** CLAUDE.md NEVER-1 names CTO + COO; both are now on record.

## 1. The bytes (PHASE A evidence)

Worker `0.9.0_WK_NFRA_OPLGTW~15` PHASE A @d40be146b6 (`deliverables/0.9.0_WK_NFRA_OPLGTW~15/ANNOUNCE_OG-rl-3.md`):
- **Live ref:** manifest `3a7d6a7dc8`; host md5 93 of 93 equal (SSM 98ab1c81, re-read ~19:15Z).
- **Release tree** `/c/tmp/og-rel8` `rel-nfra-oplgtw-hx-teams` @4231bd2ddc (da66e3f2ff gateway files, 4231bd2ddc template).
  Census 6 files (+804/-3). New files sha256 `f4705400...`, `d7632f56...` = the request's table. `config.py` 7=7,
  `server.py` 9=9, `taxsma_workbook.py` 7=7 hunk lines EQUAL to db92656c72. **Issuer re-read, independent (18:5xZ):**
  the same 6-file census, the same two sha256 prefixes, the three hunk sets sha-EQUAL, printf `%s` 18 = args 18, 50 keys.
- **Template:** `.env` 48 -> 50 (50 unique, the 48 unchanged, in order); failed read / empty / `None` each rc 3 before
  the first write; a value renders both lines.
- **Tests:** test_teams_route 14, test_taxsma_workbook 21, test_mail_route 10, test_mail_listing 12, test_ogz2_ac08
  (60 = LIVE 60 + OWN 0).
- **Terraform** @302d4eb0d5: targeted plan `0 to add, 2 to change, 0 to destroy` (policy + `gateway/teams/bearer-93ZHiU`;
  rule 35 2 -> 3). Untargeted: `0/3/0`, the third = `aws_lambda_function.mcportal_grant_writer` `source_code_hash`
  only -- NOT applied (row Z-W15-S25).
- **Identity** (the live template's deploying-shell input): host-side sha256 MATCH (SSM 0d2ed320), never printed.
- **Rollback** `/c/tmp/og-rb8` @3a7d6a7dc8: 96 of 96 equal to the live S3 artifact; not uploaded.
- **Verify script** `rl3_verify.sh`: negative control on the undeployed host FAIL 5 of 9 on exactly the release arms.

## 2. Blast radius -- the CTO's, adopted key by key, with the COO's reads

| key | before (measured 17:5xZ) | after | rollback |
|---|---|---|---|
| `gateway-read-secrets-policy` | 1 statement, 1 action, 3 ARNs, no wildcard; `gateway/teams/bearer` implicitDeny | + the `gateway/teams/bearer` ARN (4) | revert the fourth ARN (targeted apply) |
| ALB rule 35 | `/hx/mail/*`, `/hx/transcripts/*` | + `/hx/teams/*` (3 values; limit 5) | revert to 2 values |
| host app files | live `3a7d6a7dc8` | + `app/teams_route.py`; `config.py`, `server.py`, `taxsma_workbook.py` gain only db92656c72's hunks (Z-S41 = two more bearers in the Tax route's other-bearer tuple) | redeploy `/c/tmp/og-rb8` (`3a7d6a7dc8`) with the base guard and the identity export |
| host `.env` | 48 keys | 50: + `TEAMS_BEARER` (host-side from `gateway/teams/bearer`, refused when the read fails or is empty), `TEAMS_BEARER_LABELS=teamsassist`; the other 48 unchanged | the same redeploy renders 48 |
| **served content** | `/hx/teams/*` 302s to the Microsoft sign-in | **`/hx/teams/me`, `/hx/teams/chats`, `GET/POST /hx/teams/chats/{id}/messages`, `GET/POST .../replies` LIVE** behind their own static bearer, reading and (POST) writing as MS_INGEST_IDENTITY's server-held token, one Graph allowlist per verb; output allow-by-key; audit without content. The only bearer holder is the laptop assistant (LDO-001); send approval lives in that caller (Andrew's reply of 1), not in the route | redeploy (the routes unmount) |
| tool list | as live | unchanged (headless routes, not MCP tools) | -- |
| manifest | `deployed_commit 3a7d6a7dc8` | the release head, previous `3a7d6a7dc8` | revert the manifest commit |

**Not touched, by name:** every other route (`/hx/mail/*`, `/hx/transcripts/*` stay 404 for `x`, measured; the Tax
route's own `UNAUTHORIZED_CAPABILITY`; `/mcp` 401; `/` 302), every other IAM statement, every other listener rule, the
instance, the identity allowlist, `ms_ingest.py`.

## 3. The named properties and their writers

**(a) Who can call `/hx/teams/*`.** N = 2 writers: the ALB (rule 35 forwards without sign-in) and the route's guard
(`app/teams_route.py`: constant-time compare against `TEAMS_BEARER`; 503 when unset). Expected: no bearer -> the app's
own 401/404, never a 3xx (`ht.AC2` arm 3). Other branch: a 302 means rule 35 did not apply -> AC1 arm 4 fails first;
a 200 without a bearer -> roll back.

**(b) The bearer's presence.** N = 1 writer: the render's host-side read, refusing failure or empty (render test,
PHASE A step 3). Expected: non-empty (`ht.AC2` arm 2).

**(c) Whose identity Graph sees, and what it may do.** N = 1 writer: the route uses MS_INGEST_IDENTITY's server-held
delegated token (no caller-supplied identity). Read verbs graded by `ht.AC3` (200 on `me` and `chats`). A 502 with
`graph_status` 403 = a missing Graph scope: BLOCKING row to Andrew, NOT rolled back (the route is inert without the
scope). The two POST verbs are UNEXERCISED until Andrew's first EOD post (CTO ruling).

## 4. Act and verify

Order: the targeted `safe-apply` (IAM + ALB; ledger `nfra-oplgtw-hx-teams-infra`) and `ht.AC1` PASS, then the deploy
from `/c/tmp/og-rel8` (ledger `nfra-oplgtw-hx-teams-release`; `DEPLOY_BASE_REF=3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7`),
the verify script immediately, then `ht.AC2`-`AC4`. Gateway queue: no other gateway releaser is LIVE at signing
(`get_live_agents` 18:1xZ: `2.0.0_SA_COO~MI` absent); the worker re-reads the live ref at step 10.

## 5. COO half

**SIGNED -- `2.0.0_SA_COO~O`, 2026-10-02 ~19:0xZ.** The act may touch exactly the four keys in section 2 and the
manifest; each rollback stands alone and is pre-built (code: `/c/tmp/og-rb8`, 96 of 96; IAM and ALB: a targeted apply
of the prior values). Both branches named: AC1-AC4 PASS -> close; any arm FAIL except AC3's GRAPH-SCOPE-MISSING -> roll
back that key, re-verify, close ROLLED BACK; GRAPH-SCOPE-MISSING -> keep the release (the routes are inert without the
scope) and file a BLOCKING row to Andrew. Writers counted: section 3, N printed per property. The untargeted plan's
third diff is outside this sign-off. With the CTO half (ruling msg 28599) both halves are SIGNED: GO to PHASE B.
