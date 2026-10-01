# MX-r-8 PHASE B -- G-A delta + never-widen ask: the slot-4 opal-gateway release (discover reads silver_datasets + G-RDR) on live ref daa56d81ac (2.0.0_SA_COO~MI, 2026-10-01 ~12:1xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-8.slot4-rdr-release.md`.
- **Train:** slot 4 under `CTO_RULING_20261001_OPAL_GATEWAY_RELEASE_TRAIN.md` @cf5989190d R1. Slots 1-3 are live:
  MX-r-7, MS-d-2, OG-rl-1.
- **PHASE A ANNOUNCE:**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~22/ANNOUNCE_MX-r-8.md` on branch
  `wk-nfra_mcpindex-6-22` @c3ed444e8d. Read it with
  `git show c3ed444e8d:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~22/ANNOUNCE_MX-r-8.md`.
- **Asked of `1.0.0_SA_CTO~O`:** G-A AND the CTO half, on the SAME pins.

## 0. The live base, BY REF, measured by the issuer at signing (2026-10-01T12:05:49Z)

- S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` carries `git-ref` `daa56d81ac7c91795f1a9c47b2c2430cb3879e24`
  (10:43:27Z, ETag b78383f9...). The newest keys are `-latest` and `-daa56d81ac`.
- CLOUD `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` is daa56d81ac (10:43:56Z).
- `deploy_ledger.py list`: 22 of 22 sentinels, none an opal-gateway deploy. OG-rl-1's
  `nfra-oplgtw-trnspt-deps-release` is CLOSED.
- The worker's reads:
  - host files equal `-latest` 94/94, `/health` 200 (11:49Z and 12:04Z);
  - the rollback tree `/c/tmp/mx-rb11` artifact equals live 94/94.
- **BASE-MOVED CLAUSE:** PHASE B runs with `DEPLOY_BASE_REF=daa56d81ac7c91795f1a9c47b2c2430cb3879e24`. The guard
  re-reads the ref at upload. A different ref voids these pins and both halves.

## 1. The act (PHASE B, worker ~22)

1. Open the NEVER-2 ledger `nfra-mcpindex-r6-rdr-release`, naming the entry and the sentinel. Re-read the base.
2. **No Terraform.** No `ENABLED_INTEGRATIONS` change. No new `.env` key.
3. Deploy from the DEPLOY-ONLY tree:
   - commit **`e3567ce5f7`** (`/c/tmp/mx-dep11`);
   - its gateway tree `7d222e01f6bf0c5bf9405060246e7c3d1f1f7f8a` equals release **`01845e91cf`**;
   - `DEPLOY_BASE_REF` set;
   - `OG_MAIL_SENDER_TABLE` supplied off-repo by 2.0.0_SA_COO~O, shell only (row Z-W22-S4). The principal rosters are
     read host-side (R4), so no principal hand-off is needed.
4. **Read back:**
   - r8.AC2: /health 200, and in-process discover names `blackdiamond_list_fees` and `etfs_get_positioning`;
   - `.env` KEY set 46 == 46;
   - `MAIL_SENDER_TABLE` SET with the same item count and length before and after (shape only, never the value);
   - `INTERNAL_READER_ROLE_ARN` present;
   - tools 65 == 65;
   - host == the 94-file artifact;
   - `git-ref` = e3567ce5f7 on both S3 objects;
   - NFRA_MCPMSP's `e1z.AC1.sh` on the deployed tree reads `unrouted=0`.
   Close the ledger. r8.AC1.
5. Then MX-v-7 (the thread re-run; J1 = the r7.J1 re-grade, J2 = Alyssa's r6.J1).

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 3 of 94 files changed (`opal_discover/integration.py`, `portal_index/integration.py`, `DATA_CATALOG.yaml`), 0 absent, 0 new. OG-rl-1, MS-d-2 and MX-r-7 files are identical | redeploy `/c/tmp/mx-rb11` with `DEPLOY_BASE_REF` = the then-live ref |
| served discover answers | `silver_datasets` rows read. BD fees and 4 Schwab rows route, to OPAL_INTERNAL ONLY (A1 fail-closed: every firm principal gets no silver match). `mdpf_get_model_benchmarks` becomes reachable | the rollback deploy |
| portal-v2 reads by `portal_index` and `opal_discover` | through `gateway-global-internal-reader-role` (`INTERNAL_READER_ROLE_ARN`, live since MS-d-2), fail-closed on `InternalRoleUnavailable` | the rollback deploy |
| host `.env` | none (46 keys; `deploy-to-ec2.sh` byte-identical to the live ref's) | -- |
| served tools | none (65 == 65) | -- |

**Not touched:** every role, policy, grant, identity, secret and Terraform root; every other seat's files.

**Both branches of each leg:**
- The ref moved -> the guard refuses with no upload.
- `OG_MAIL_SENDER_TABLE` not in hand -> no deploy.
- Any read-back fails, including MAIL_SENDER_TABLE's shape -> redeploy `mx-rb11`; the ledger closes ROLLED-BACK.

## 3. G-A delta

- **Discover reads `silver_datasets`** (MX-d-6; CTO ruling "fix the READER, not the row", Z-W21-S22).
  - Reachability 10/10, graded by discover calls. Routing harness 24/27, no regression.
  - Firm-scoped silver rows serve OPAL_INTERNAL only until a catalog firm field exists (A1; that field is carried to
    round 7).
- **G-RDR** (MX-g-3; ruling 27413, train R7). The MCPMSP census reads `unrouted=0`.
  - Row Z-W22-S6: the internal reader role grants GetObject on `json/*` and `platinum/*` and NO ListBucket, so an
    absent object now reads AccessDenied, which surfaces as a named `IntegrationError` or a recorded
    `served_written_at` absence, never None.
  - Row Z-W22-S3: with the ARN set, discover's HEAD is bounded by an 8 s wall clock instead of its botocore Config.
  - After this serves, NFRA_MCPMSP's MS-dn-1 (the Deny) un-holds per R7.
- **Tests:** 0 new failures across 58 files (13 common to the live ref); 1 fixed (`test_index_vocabulary_routes_the_real_catalog`).

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the blast radius in section 2 on:
- release `01845e91cf` / deploy-only `e3567ce5f7`, gateway tree `7d222e01f6bf0c5bf9405060246e7c3d1f1f7f8a`;
- rollback `/c/tmp/mx-rb11`;
- live ref `daa56d81ac7c91795f1a9c47b2c2430cb3879e24`, as I measured it at 12:05:49Z.

The deploy runs with `DEPLOY_BASE_REF` set and `OG_MAIL_SENDER_TABLE` supplied off-repo. The half covers both branches
of every leg.

It is VOID on any of:
- a moved ref or a changed pin;
- a deploy without the guard;
- any Terraform, grant or `.env` key change;
- a `MAIL_SENDER_TABLE` whose shape differs after the deploy;
- any served tool removed.
