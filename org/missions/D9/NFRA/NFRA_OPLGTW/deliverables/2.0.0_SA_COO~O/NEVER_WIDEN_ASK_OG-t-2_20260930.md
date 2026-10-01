# Never-widen ask -- OG-t-2, the narrow opal-gateway release of the principal-keyed tier and the auth hardening

By: `2.0.0_SA_COO~O` (issuer), 2026-09-30. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-t-2.tier-auth-release.md`
(amendments A1 @ad55c31336, A2 @4d1f1dc038). Rulings it rests on: round-1 analysis R-3 (a)-(f), Q1. PHASE A evidence:
`deliverables/0.9.0_WK_NFRA_OPLGTW~12/ANNOUNCE_OG-t-2.md`, drained @0a5cc3c093. Principal values: `PART_D_RECORD_20260930.md`
@205c2e7f6c (never in the repository).

**Halves owed:** `1.0.0_SA_CTO~O` (CTO half) and `3.0.0_SA_CVO~O` (second, non-acting half), both against THIS file.
PHASE B (ledger, upload, verify) waits for both, runs off-hours, and is announced to `2.0.0_SA_COO~MI` first.

## 1. The bytes

Release branch `rel-nfra-oplgtw-tier-auth`, HEAD `d61fde46933221e8afbac7418f06d7525d3347c8`, three commits on live
`42c52ed4d9e834b0f1cf4f96eb83f9b0f7a183df`:
- the four build commits `b5a585cf2f`, `344cca64a1`, `c4d2274c6d` and `0906bf01e5` (OG-t-1, OG-t-1 A1, OG-u-1, OG-u-2),
  applied by diff;
- the three test files they add;
- `deploy-to-ec2.sh`, which gains two `.env` lines.

Census `git diff --stat 42c52ed4d9 d61fde4693 -- infra/aws/ec2/opal-gateway`: 15 files, +774/-42, 0 files outside the
gateway directory.

## 2. Blast radius -- what the act may touch

| key | before (PHASE A read, 2026-09-30) | after | rollback |
|---|---|---|---|
| host `/opt/opal-gateway` app files | live `42c52ed4d9`, 13 of 13 by md5 | the release's files; the named 14 gateway files change | re-deploy `/c/tmp/og-rb2` (live tree, rebuilt, 87 of 87 equal to the live S3 artifact) with `DEPLOY_BASE_REF` = the release sha |
| host `.env` | 33 keys | 35 keys: + `MASTER_ADMIN_PRINCIPALS` (1 pair) and `WRITE_CAPABLE_PRINCIPALS` (2 pairs); 0 removed, 0 shared values changed; `ENABLED_INTEGRATIONS` unchanged (six ids); the four email rosters stay (the machine-identity rule reads them) | the same re-deploy renders the live template (33 keys, no principal variables) |
| `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/` | `opal-gateway-42c52ed4d9.tar.gz` | + `opal-gateway-d61fde4693.tar.gz` (a new key; the live key is not overwritten) | none needed; the live key stays |
| `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway` | `deployed_commit` `42c52ed4d9` | the release sha, with `previous_deployed_commit` = `42c52ed4d9` | revert the manifest commit |

**Not touched, by name:** Terraform, the ALB, the instance and its role, Secrets Manager, the access-state table (read
only), every grant record, `identity_tool_allowlist.txt`, the mcportal pin `a3bff71ffa`, and every other service in the manifest.

## 3. The named property -- each principal's tier -- and its writers

There are **N = 2 writers**, and both rules were read, not predicted:
- `tier.resolve_tier(principal)`, for persons, keyed on `<tid>/<oid>` only;
- `token_broker._machine_tier`, for server-held identities, still keyed on the email rosters.

Step 4 ran both rules over **9 identities**: 3 table principals, 2 audit-only persons, 1 server-held machine identity
(callers `ms`, `49f`, `cot`) and 3 synthetic probes. It found **0 deltas**, machine callers included. Among the 6
`oauth_client` records, 0 expire under OG-u-2's 30-day idle lifetime at release. The operator's upload client is not
among them: it expires about 2026-10-18 (row Z-W12-S7).

**Both branches:**
- **Expected:** every identity keeps its tier. Step 11's `/mcp` call as the admin principal resolves `MASTER_ADMIN` in
  the audit tier field.
- **Other branch:** a pair differs from the one Entra issues. Under R-3 (b) that principal falls to the lowest tier, with
  no email fallback. Step 11's admin call catches it for the admin: the call reads a tier other than `MASTER_ADMIN`, the
  worker rolls back within 90 s, and the ledger closes ROLLED BACK.
- **Risk left:** a write-capable pair error is not exercised by step 11. The pairs were read at source from the Entra
  admin center, and Alyssa's matches her existing grant key, so a second source confirms it. The Opal Bloomberg pair has
  no second source. The OTP and MS-ingest machine callers cannot move, because they are keyed on the email roster.

## 4. Act and verify (PHASE B, from the order as amended)

- **Before:** BEFORE reads (the tool list and `ENABLED_INTEGRATIONS`). The NEVER-2 ledger
  `nfra-oplgtw-tier-auth-release` is committed before the act. The 13-file content read is repeated immediately before
  upload.
- **Act:** `cd /c/tmp/og-rel2 && OG_MASTER_ADMIN_PRINCIPALS=... OG_WRITE_CAPABLE_PRINCIPALS=...
  DEPLOY_BASE_REF=<live full sha> HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~12 bash infra/aws/ec2/safe-ec2-deploy.sh
  opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
- **Verify within 90 s:**
  - `/health` returns 200;
  - the md5 of the shipped files equals the release bytes;
  - the tool list AFTER equals BEFORE;
  - `ENABLED_INTEGRATIONS` is unchanged;
  - the admin `/mcp` call resolves `MASTER_ADMIN`.
- **On any failure:** roll back and close the ledger ROLLED BACK.
- **Criteria:** `tr.AC1.sh`-`tr.AC3.sh`, as amended by A2.
