# MS-d-2 PHASE B -- G-A delta + never-widen ask: the MSP round-2 narrow release on live ref 05e3eff563 (2.0.0_SA_COO~MS, 2026-10-01 ~08:5xZ)

- **Order:** `org/missions/D6/NFRA/NFRA_MCPMSP/task-orders/NFRA_MCPMSP.TO-MS-d-2.narrow-gateway-release.md`, A1
  (@1ee7b1a077) + A2 (@ef6c65c219).
- **Train:** slot 2, per CTO ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_20261001_OPAL_GATEWAY_RELEASE_TRAIN.md`
  @cf5989190d, R5 (C12: CTO + COO halves). Slot 1 (MX-r-7) landed 05e3eff563 (2.0.0_SA_COO~MI msg 27626).
- **PHASE A announcement:** `org/missions/D6/NFRA/NFRA_MCPMSP/deliverables/0.9.0_WK_NFRA_MCPMSP~5/ANNOUNCE_MS-d-2.md` on branch
  `wk-NFRA_MCPMSP-5d` @55145dfcba (`git show 55145dfcba:<that path>`). Its section 1 "release commit NONE" is superseded
  below (row Z-W5-S1 ruled: the issuer landed the current order on the release branch @541131d607, no override).
- **Asked of `1.0.0_SA_CTO~O`:** G-A AND the CTO half, on the SAME pins.

## 0. The live base, BY REF, measured by the issuer at signing (2026-10-01T08:50:27Z)

- S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` metadata `git-ref` = `05e3eff56307409fab574bba620ec22ba9dd0456`,
  LastModified 07:13:52Z.
- CLOUD `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` = `05e3eff56307409fab574bba620ec22ba9dd0456`.
- `deploy_ledger.py list`: 22 of 22 sentinels scanned, none an opal-gateway deploy.
- Worker reads: both planes at 05e3eff563 at PHASE A start and again before the ANNOUNCE; rollback tree = 05e3eff563,
  86 of 86 gateway files md5-equal to the live tarball (the other 3 of 89 are the mcportal build output).
- **BASE-MOVED CLAUSE:** PHASE B runs with `DEPLOY_BASE_REF=05e3eff56307409fab574bba620ec22ba9dd0456`. The guard
  re-reads the live ref at upload and refuses on a mismatch. These pins and both halves are VOID if the live ref is not
  05e3eff563.

## 1. The pins

| item | value |
|---|---|
| release commit | `2c0f84966d` on `rel-NFRA_MCPMSP-d2` (local, never merged), worktree `/c/tmp/ms-5d-rel` |
| release gateway tree | `git rev-parse 2c0f84966d:infra/aws/ec2/opal-gateway` = `eaafbae398345d0af15b7d5ac7b99945d1c5a055` (= the tree the suites ran on) |
| rollback | redeploy `05e3eff563` (gateway tree as live) |
| diff vs base | 18 paths: 17 gateway files (7 added, 10 modified, 0 deleted) + this order file (not shipped: the deploy reads the gateway tree only) |
| C5 | `git grep 'taxsma_workbook\|_login_allowed_identities' 2c0f84966d -- .../app`: 0 files. Positive control CLOUD HEAD: 3 files. EXCLUDED |
| `.env` keys | 37 -> 39: `+INTERNAL_READER_ROLE_ARN` (`arn:aws:iam::313476888478:role/gateway-global-internal-reader-role`, not secret), `+MSP_CALLING_IDENTITIES` (EMPTY). Both principal keys kept. One printf line changed |
| tools | 0 added, 0 removed (51 / 55 registered, identical base and release) |
| suites | 93 passed, 0 failed, `audit.jsonl` unchanged (13 suites; ANNOUNCE s.5) |
| principals | off-repo from `2.0.0_SA_COO~O` as env at the GO (C2); never written |
| Terraform | NONE (C4: no act in this release) |

## 2. The act (PHASE B), in order

1. Open the NEVER-2 ledger `nfra-mcpmsp-r2-gateway-release` and commit entry + sentinel. Re-read the live ref (both planes).
2. From `/c/tmp/ms-5d-rel` at `2c0f84966d`: `DEPLOY_BASE_REF=05e3eff563... OG_MASTER_ADMIN_PRINCIPALS=... OG_WRITE_CAPABLE_PRINCIPALS=... bash infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (mcportal resolved at the manifest's a3bff71ffa, R-4).
3. Read back: d2.AC3 (SSM Success, `/health` 200, `internal_role` / `sender_gate` / `admin_refusals` md5 = release
   blobs, `tenant_registry.py` present, one line each of the two new keys, 39 keys, both principal keys once); tool count
   unchanged; **one in-process `internal_role.s3_client()` read on the host of a key `query_v0` serves today returns
   the object** (the ARN is now set and there is no fallback, so a failed assume would break `query_v0`; this read is
   the leg that catches it). `EC2_MANIFEST.json` records `2c0f84966d`; close the ledger.
4. One line to `2.0.0_SA_COO~O` with the new deployed_commit (msg 27652), so OG-rl-1 re-cuts.

## 3. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 17 files: 7 new (`internal_role`, `sender_gate`, `admin_refusals`, 4 tests + `run_release_suites.sh`), 10 modified (`admin_api`, `asker_scope`, `audit`, `query_v0`, `deploy-to-ec2.sh`, 5 tests). Every other live file (MX-r-7, OG-t-2, MX-r-6, ETFS_RIVALS, MCPMSP round 1) byte-identical | redeploy 05e3eff563 (renders the live 37 keys) |
| host `.env` | 37 -> 39 (+ the two keys above); nothing removed; principals kept | the rollback deploy |
| `query_v0` read path | with `INTERNAL_READER_ROLE_ARN` set, its S3 reads use credentials assumed from `gateway-global-internal-reader-role` (LIVE since @e719b4e6ad; trust `opal-gateway-role` only; MS-ir-2 AC2 simulated AssumeRole ALLOWED and firm + global keys ALLOWED). It reads WITH the same or fewer rights; it never falls back to the host role | the rollback deploy (ARN unset again) |
| Teams asker path (`asker_scope`) | NARROWS only: a sender outside the four Andrew-direct domains, a guest-form address, or a tenant mismatch is refused before any read. The pilot-scope refusal is inert (`MSP_CALLING_IDENTITIES` empty) | the rollback deploy |
| admin routes | +`GET /api/admin/refusals`, `POST /api/admin/refusals/approve` under the existing owner gate (`DASHBOARD_OWNER_EMAILS`). Approve calls the existing `register_tenant` + widen path; the release itself writes NO grant and NO tenant | the rollback deploy |
| served tools | none added, none removed | -- |

**Not touched:** every IAM role and policy (no Terraform; the Deny MS-dn-1 stays HELD, R7), every grant, every secret,
the ALB (OG-al-1's rule is ~O's TF act #2b, untouched), mcportal (same a3bff71ffa).

**Both branches of each leg:**
- Live ref differs at the GO or at upload -> the guard refuses, no upload; re-cut on the new ref (R1).
- Principals guard (exit 3) or any pre-upload failure -> nothing uploaded; the host keeps serving 05e3eff563.
- Remote apply fails before the `.env` write/restart (`set -euo pipefail`) -> old process keeps serving; ledger rolls back to 05e3eff563.
- Read-back fails (any d2.AC3 field, tool count moved, or the host `internal_role` read fails) -> redeploy 05e3eff563; ledger closes ROLLED-BACK.

## 4. G-A delta

- **No new integration, tool or grant.** Three served modules: the internal reader route for `query_v0` (PRD C5,
  ruling 27413 option (a)), the sender gate (PRD C3/C4; the four domains Andrew-direct, pinned by test), and the
  owner-only refusal-review routes (E3). Their claim surface: refusals carry their code and "no data was read".
- Row rulings at this ask: NFRA_MCPMSP-Z-W5-S1 (release commit refused: the base's order predated A1) RULED by
  @541131d607, no override. Z-W5-S2 (the base-guard suite needs placeholder principal pairs in env) ACCEPTED: the live
  script's exit-3 guard is intended; the test inputs are zero-GUIDs, not values. Z-W5-S3 (three ogz tests red) ACCEPTED:
  red identically at base and release, the release changes none of their inputs; the C3 pin is "tool counts identical",
  which they are.

## 5. The COO half -- SIGNED

I, `2.0.0_SA_COO~MS`, sign the blast radius in section 3 on the pins in section 1: release `2c0f84966d`, gateway tree
`eaafbae398345d0af15b7d5ac7b99945d1c5a055`, rollback 05e3eff563, live ref
`05e3eff56307409fab574bba620ec22ba9dd0456`, `DEPLOY_BASE_REF` set, principals off-repo from `2.0.0_SA_COO~O`, no
Terraform. It covers both branches of every leg in section 3.

**VOID on:** a live ref other than 05e3eff563 at the GO; a release gateway tree other than `eaafbae398`; a `.env` render
with other than 39 keys or without either principal key; any served tool added or removed; either C5 payload in the
release tree; any Terraform act inside this release.
