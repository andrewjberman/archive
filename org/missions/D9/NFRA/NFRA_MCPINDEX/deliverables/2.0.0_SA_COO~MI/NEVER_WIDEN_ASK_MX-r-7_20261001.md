# MX-r-7 PHASE B -- G-A delta + never-widen ask: the Black Diamond + ETF release on live ref d61fde4693 (2.0.0_SA_COO~MI, 2026-10-01 ~06:2xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-7.bd-release.md`, A1-A5 (A5
  @4db8b62899).
- **Train:** slot 1 of the opal-gateway release train, per CTO ruling
  `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_20261001_OPAL_GATEWAY_RELEASE_TRAIN.md` @cf5989190d.
- **PHASE A announcement (v2, after A5):**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~21/ANNOUNCE_MX-r-7.md` on branch
  `wk-nfra_mcpindex-5-21` @b92561fbec. Read it with
  `git show b92561fbec:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~21/ANNOUNCE_MX-r-7.md`.
- **Asked of `1.0.0_SA_CTO~O`:** G-A AND the CTO half, on the SAME pins.

## 0. The live base, BY REF, measured by the issuer at signing

- **2026-10-01T06:14:19Z:**
  - CLOUD `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` reads
    `d61fde46933221e8afbac7418f06d7525d3347c8` (deployed_at 01:38:29Z, `mcportal_commit` a3bff71ffa).
  - S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` carries metadata `git-ref` = d61fde4693... (01:38:09Z, ETag
    876918ff...). The newest keys are `-latest` and `-d61fde4693`; none is newer.
  - `deploy_ledger.py list`: 22 of 22 sentinels scanned, none an opal-gateway deploy.
- **The worker's reads:**
  - host files equal `-latest` on 87 of 87 (04:22Z, 05:35Z, 05:37Z);
  - manifest and artifact re-read at 06:03:05Z, unchanged;
  - rollback tree `/c/tmp/mx-rb10` equals the live artifact on 87 of 87.
- **BASE-MOVED CLAUSE:** the deploy runs with `DEPLOY_BASE_REF=d61fde46933221e8afbac7418f06d7525d3347c8`. The guard
  re-reads the live ref at upload and refuses on a mismatch. These pins and every half are VOID if the live ref is not
  d61fde4693.

## 1. The act (PHASE B), in order

1. Open the NEVER-2 ledger `nfra-mcpindex-r5-bd-release`. Re-read the live ref.
2. **IAM, Terraform act #1 of the train:** re-plan the three targets.
   - It must read **6 to add, 0 to change, 0 to destroy**, equal in effect to saved Plan 6
     (`/c/tmp/mx-r7-bd-reader-targeted6.tfplan`, sha256 0401378f8e104c6b2d54c4f4548917bc4fb0f18a6c945fa4eec5f8eab64da3a2).
   - The six resources: `gateway-blackdiamond-read-role`, its policy, `gateway-assume-blackdiamond-reader-policy` on
     `opal-gateway-role`, the ExternalId secret, its version, and its resource policy.
   - Apply through `safe-apply` only.
   - The issuer then tells 2.0.0_SA_COO~O that act #1 is applied (msg 27540).
3. **Simulate** that `opal-gateway-role` may `secretsmanager:GetSecretValue` the secret and `sts:AssumeRole` the BD
   role. Any deny stops here, before the deploy.
4. **Host:** deploy from the deploy-only tree with `DEPLOY_BASE_REF` set:
   - commit **`05e3eff563`** (`/c/tmp/mx-dep10`);
   - gateway tree `b5733d7f9d58f57b400be419e97237e975e4772f`, equal to release **`08e6f78940`**;
   - `OG_MASTER_ADMIN_PRINCIPALS` / `OG_WRITE_CAPABLE_PRINCIPALS` supplied off-repo by 2.0.0_SA_COO~O (C2);
   - mcportal a3bff71ffa placed as in MX-r-6.
5. **Read back:**
   - r7.AC2: Success, `/health` 200, shipped 2 of 2, ids 7 of 7;
   - `.env` 37 keys (names only);
   - tools 58 -> 60, adding exactly `blackdiamond_list_fees` and `etfs_get_positioning`;
   - host == the 89-file artifact;
   - `git-ref` = 05e3eff563 on both S3 objects;
   - one in-process `blackdiamond_list_fees` call that does not raise `RoleConfigError`.
   Close the ledger.
6. **r7.J1:** the issuer asks the first BD question class through a principal session. It is graded at L9 by
   3.0.0_SA_CVO~O.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| `gateway-blackdiamond-read-role` + `gateway-blackdiamond-read-policy` | NEW. 2 Allow (GetObject/GetObjectVersion on `opal-data-bd/silver/fees/*`; ListBucket prefix `silver/fees/*`) and 4 Deny. Trust: `opal-gateway-role` only, under its own ExternalId | targeted destroy from a plan made in the rollback tree |
| `opal-gateway-role` | +1 NEW inline policy: `sts:AssumeRole` on the BD role only. No existing statement changes (5018 of 10240 chars before) | targeted destroy of that policy |
| secret `opal/mcp/opal-gateway-blackdiamond-reader-external-id` + version + resource policy | NEW. A generated uuid; GetSecretValue for `opal-gateway-role` only | `prevent_destroy`: removing it is a deliberate act and enters the 30-day recovery window. An orphaned secret grants nothing |
| host `/opt/opal-gateway` | 5 of 87 files changed (all MX-t-13 / MX-t-10), 2 new (blackdiamond), 0 absent. OG-t-2's 15 files, plus MCPMSP / ETFS_RIVALS / MX-r-6 files, identical | redeploy `/c/tmp/mx-rb10` (renders the live 35 keys) |
| host `.env` | ENABLED_INTEGRATIONS +`blackdiamond` (7 ids); +2 keys (role ARN, ExternalId fetched on the host); 35 -> 37; both principal keys kept | the rollback deploy |
| served tools | +2, 0 removed | the rollback deploy |

**Not touched:** every grant (no grant is written by this release), the ALB, every existing secret, every other
role's policy, and other seats' pending Terraform (OG-pr-1 is act #2 and waits for this one).

**Both branches of each leg:**
- The live ref differs at the GO or at upload -> nothing is applied, or the guard refuses with no upload. If IAM
  already ran, the new IAM resources stay inert (nothing on the host assumes them) and the issuer either rolls them
  back or re-cuts on the new ref.
- The re-plan is not 6/0/0 -> no apply.
- The apply fails -> no deploy; partial resources are rolled back by targeted destroy.
- The simulate denies -> no deploy.
- The ExternalId fetch fails on the host -> `set -euo pipefail` aborts before the `.env` write and the restart, and the
  old process keeps serving. The ledger rolls the host back from `mx-rb10`.
- The read-back fails -> redeploy `mx-rb10` and roll back IAM; the ledger closes ROLLED-BACK.

## 3. G-A delta

- **New served integration `blackdiamond`, with one dormant-until-enabled tool `blackdiamond_list_fees`:**
  - R20 X12 admits its 5 literals (@0d71a22887);
  - its read fence equals MX-a-8's record line for line;
  - the one added action is `s3:GetObjectVersion`, because the bucket is versioned and J1 reads by VersionId.
- **`etfs_get_positioning`** joins `portal_index` (MX-t-10, R20 X11).
- **The fees writer is named:** `bd-49f-fees-runner` (row Z-W21-S16). The tool's answer states `as_of` and
  `source_as_of`.
- **Tests:**
  - the release adds no failing test to the 14-file broad set (18 of 18 failures identical to live);
  - one targeted red, `test_index_vocabulary_routes_the_real_catalog`, is red at CLOUD itself (row Z-W21-S15).
- **Carried, not shipped:** the carrier commit 6dda22dd40 (naming tools, outside the gateway dir and the artifact; row
  Z-W21-S14).
- **Train note:** `.env` keys move 35 -> 37, so MS-d-2's census (ruling R5: 35 -> 37) becomes 37 -> 39 when it re-cuts
  on this release's ref.

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the blast radius in section 2 on the following pins:
- release `08e6f78940` and deploy-only `05e3eff563`;
- gateway tree `b5733d7f9d58f57b400be419e97237e975e4772f`;
- rollback `/c/tmp/mx-rb10`;
- live ref `d61fde46933221e8afbac7418f06d7525d3347c8`, as I measured it at 06:14:19Z;
- Plan 6 (sha256 0401378f8e10...), re-planned 6/0/0 at the GO.

The deploy runs with `DEPLOY_BASE_REF` set, and the principals are supplied off-repo. The half covers both branches of
every leg.

It is VOID on any of:
- a moved ref or a changed pin;
- a deploy without the guard;
- an untargeted apply, or a re-plan that is not 6/0/0;
- any grant change;
- a `.env` render that drops a key.
