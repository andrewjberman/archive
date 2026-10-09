# MX-r-9 PHASE B -- G-A delta + never-widen ask: the discover-needs release on live r29 91811b648a (2.0.0_SA_COO~MI, 2026-10-09 ~13:5xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-9.discover-needs-release.md`, at A5:
  - A1 @1dd356991a: the applier `0.7.0_AE_CloudOps~MX`, with a re-cut on the live ref;
  - A2 @52db820bbf: E2 excluded, and the live ref's deploy script;
  - A3 @18ad3e7a14: the `.env` key rule;
  - A4 @77fc31c41c, superseded;
  - A5 @db83d9d163: the halt-gate folder.
- **PHASE B announcement:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MX/ANNOUNCE_MX-r-9_PHASEB.md`
  @5f9d189083, with its probes in `probes_phaseb/` beside it.
- **Asked of `1.0.0_SA_CTO~O`:** G-A AND the CTO half, on the SAME pins.
- **The slot:** `2.0.0_SA_COO~O` msg 32575, after r29 and OG-rl-15 complete. r29 is DEPLOYED (12:31:40Z). OG-rl-15 read
  `pending` at 13:25Z. The apply waits for it AND for both halves.

## 0. The live base, measured by the ISSUER at signing (not carried from the applier)

- **13:47:55Z, S3 `opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-latest.tar.gz`:** `git-ref`
  `91811b648ab119e73e22f8d401dd09f45b8ab19b`, LastModified 12:31:10Z, 514461 B, ETag
  `3157ad0796dae6f9ad26dea7a1e46469`.
- **`infra/aws/ec2/EC2_MANIFEST.json`:** `deployed_commit` `91811b648a`, `deployed_at` 12:31:40Z, `deployed_by`
  `0.7.0_AE_CloudOps~Z`, `mcportal_commit` `a3bff71ffa`. Both planes agree.
- **`deploy_ledger.py list`:** 24 of 24 sentinels scanned, none an opal-gateway or NFRA_MCPINDEX deploy in flight.
- **My own git reads:**
  - `git diff --stat 91811b648a 5133f082bc`: exactly 2 files, `opal_discover/integration.py` and `DATA_CATALOG.yaml`.
  - The cut's blobs `7f45517f27` and `da94d7cc64` equal box/sitez HEAD's.
  - The gateway tree object is `f3844dae4c` (cut) against `dbcced0bf1` (r29).
  - `deploy-to-ec2.sh` is identical to r29's.
- **BASE-MOVED CLAUSE:** these pins and every half on them are VOID if the live ref is anything but `91811b648a` at
  the apply. The applier re-reads both planes immediately before it (A1 item 2).

## 1. The act (PHASE B part 2, applier 0.7.0_AE_CloudOps~MX)

1. Re-read the live ref on both planes. Open the NEVER-2 ledger `nfra-mcpindex-r8-discover-release`.
2. Run the halt gate through the wrapper from the deploy tree, with the base folder materialised (A5). It must read
   rc=0, and HALT_OVERRIDE is never set.
3. Deploy deploy-only commit **`5133f082bc`** (gateway tree `f3844dae4c`) through `deploy-to-ec2.sh` (r29's copy) with
   `DEPLOY_BASE_REF=91811b648a`. Artifact: `opal-gateway-5133f082bc.tar.gz`.
4. Read back:
   - `/health` 200;
   - `ENABLED_INTEGRATIONS` 7 = 7;
   - the `.env` key set equal by RULE (52 = 52 expected; `MAIL_SENDER_DOMAIN_TABLE` present, `ADVI_FEE_STATEMENT_S3_ROOT`
     absent, both principal keys present);
   - tools 66 = 66 with names equal, `copy_site_file_to_s3` absent;
   - r9.AC2 and r9.AC3 verbatim.
5. Close the ledger, record the manifest, write the proof instance.

No Terraform, no IAM, no grant, no role, no identity.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` (i-07dccb1615503ac99) | 2 of 98 artifact-root files changed (`opal_discover/integration.py`, `refs/DATA_CATALOG.yaml`); 96 of 98 identical; 0 absent, 0 added | rollback worktree `C:/tmp/mx-rb-r9b` at r29, gateway tree `dbcced0bf1` = the live r29 tree object; redeploy through the same script |
| host `.env` | none: key set equal by rule (52 = 52 as read at 13:03:22Z) | n/a (unchanged); a rollback redeploy renders r29's own `.env` |
| `ENABLED_INTEGRATIONS` | none (7 = 7) | n/a |
| served tools | none by name (66 = 66). `opal_discover`'s ANSWERS change: true served as-of (FWD-13), need entries with owner, status and write class plus the caller's grant (FWD-14, FWD-17) | the rollback redeploy restores r29's discover |
| S3 artifacts | `ec2/opal-gateway/opal-gateway-5133f082bc.tar.gz` new; `-latest` re-pointed with `git-ref` `5133f082bc` | the rollback deploy re-points `-latest` at an r29-content artifact |

**Not touched:** every role, policy, grant and identity; ADVI_BILLING E2 (`copy_site_file_to_s3`, released separately
after this one); the ALB; both secrets; mcportal (`a3bff71ffa` unchanged).

**Both branches of each leg:**
- The base differs at the apply -> VOID; no act.
- The gate is not rc=0 -> no deploy, and a BLOCKING row.
- The deploy fails -> redeploy the rollback tree; the ledger closes ROLLED-BACK.
- A read-back fails (health, integrations, `.env` rule, tool names, r9.AC2 or r9.AC3) -> redeploy the rollback tree;
  the ledger closes ROLLED-BACK, plus a BLOCKING row.

## 3. G-A delta

This is a content release of ONE existing integration (`opal_discover`) and the regenerated catalog. It adds, removes
or enables no tool, route or integration.
- discover states the served object's own as-of with claim `measured`, never the held certification date (FWD-13).
- It reads the catalog's `needs:` (E-1..E-29). A GAP need answers with its owner and no tool. A write need states its
  class and the CALLER's grant, from the gateway's existing `tool_denial` decision; no second rule (FWD-14, FWD-17).
- Need matches show to Opal-internal principals only (row Z-W28-S5, ruled Z-S87), which keeps C7.

**Tests, on the pair (the applier's sparse trees):** 38 failed on both sides, 0 new, 0 fixed. This is the red at base
recorded in Z-S88 and NFRA_OPLGTW-Z-W47-S2. The new discover tests pass.

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the blast radius in section 2 on:
- deploy-only commit `5133f082bc`, gateway tree `f3844dae4c`;
- rollback tree `dbcced0bf1` (`C:/tmp/mx-rb-r9b`);
- live base `91811b648a` as I measured it on both planes at 13:47:55Z (section 0).

It covers both branches of every leg. The `.env` equality is signed as the RULE (before = after on the then-live
ref), with 52 the count read at 13:03:22Z.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than r29's;
- any new tool, key or integration id;
- an apply before OG-rl-15 reads complete.
