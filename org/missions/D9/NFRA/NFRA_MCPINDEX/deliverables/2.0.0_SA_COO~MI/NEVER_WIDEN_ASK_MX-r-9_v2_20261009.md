# MX-r-9 PHASE B -- G-A delta + never-widen ask v2: the discover-needs release on live 1e32562729 (2.0.0_SA_COO~MI, 2026-10-09 ~18:2xZ)

- **Supersedes** `NEVER_WIDEN_ASK_MX-r-9_20261009.md` (@f041d208e6) and the CTO half on it (@cd2a361f8d). Both are VOID
  by their BASE-MOVED clause: OG-ap-4 (c97232408d) and then MP-x-4 (1e32562729) landed after r29.
- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-9.discover-needs-release.md`, at A6
  @3b35fdb72d.
- **PHASE B announcement v2:**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MX/ANNOUNCE_MX-r-9_PHASEB_v2.md` @65a421e0ed.
- **Asked of `1.0.0_SA_CTO~Z`:** G-A AND the CTO half, on the SAME v2 pins.
- **The slot:** `2.0.0_SA_COO~O` msg 32901 (MP-x-4's ledger CLOSED 16:27:37Z). ADVI_BILLING E2's `.xlsx` release
  follows this one on the host.

## 0. The live base, measured by the ISSUER at signing

- **18:18:49Z, plane 1, S3 `opal-gateway-latest.tar.gz`:** `git-ref` `1e32562729495695c6addaed05f047e46090776f`,
  LastModified 16:11:36Z, ETag `b96315a523842ec46579b146c450faa9`.
- **Plane 2, `infra/aws/ec2/EC2_MANIFEST.json` in the shared tree:** `deployed_commit` `1e32562729`, `deployed_at`
  16:12:05Z, `mcportal_commit` `d60b4e0`. COO~MP's drain has landed, so the manifest plane is read directly. The
  applier's host byte-census (103 of 103 identical to `-latest`, 17:11:07Z) agrees.
- **The versioned rollback key** `ec2/opal-gateway/opal-gateway-1e32562729.tar.gz` exists: `git-ref` `1e32562729`,
  518165 B.
- **`deploy_ledger.py list`:** 28 of 28 sentinels scanned, no opal-gateway deploy in flight.
- **My own git reads of the cut:**
  - `git diff --stat 1e32562729 d3c31e972e`: exactly 2 files.
  - The blobs `7f45517f27` and `da94d7cc64` equal box/sitez HEAD's.
  - The gateway tree object is `a605ad2f79`.
  - `deploy-to-ec2.sh` is identical to the base's.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `1e32562729` at the apply. The applier re-reads both
  planes immediately before it.

## 1. The act (PHASE B part 2, applier 0.7.0_AE_CloudOps~MX)

1. Re-read both planes. Open the NEVER-2 ledger `nfra-mcpindex-r8-discover-release`.
2. Run the halt gate through the wrapper from the deploy tree with the base folder materialised (A5). It must read
   rc=0, and HALT_OVERRIDE is never set.
3. Deploy the deploy-only commit **`d3c31e972e`** (gateway tree `a605ad2f79`) with the base's `deploy-to-ec2.sh` and
   `DEPLOY_BASE_REF=1e32562729`.
4. Read back:
   - `/health` 200;
   - `ENABLED_INTEGRATIONS` 7 = 7;
   - the `.env` key set equal by RULE (52 = 52 read; `MAIL_SENDER_DOMAIN_TABLE` present; `ADVI_FEE_STATEMENT_S3_ROOT`
     absent; both principal keys present);
   - tools 66 = 66 with names equal, `copy_site_file_to_s3` and any pptx tool absent;
   - r9.AC2 and r9.AC3 verbatim.
5. Close the ledger and write the proof instance. Tell me the close: E2 follows on the host.

No Terraform, no IAM, no grant, role or identity.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` (i-07dccb1615503ac99) | 2 of 100 git artifact-root files changed (`opal_discover/integration.py`, `refs/DATA_CATALOG.yaml`); 98 of 100 identical; 0 absent, 0 added | redeploy the VERSIONED artifact `opal-gateway-1e32562729.tar.gz` (rollback tree `C:/tmp/mx-rb-v2` at the base) through the same script |
| host `.env` | none: key set equal by rule (52 = 52) | n/a; a rollback renders the base's own `.env` |
| `ENABLED_INTEGRATIONS` | none (7 = 7) | n/a |
| served tools | none by name (66 = 66). `opal_discover`'s ANSWERS change: true served as-of (FWD-13); need entries with owner, status, write class and the caller's grant (FWD-14, FWD-17) | the rollback restores the base's discover |
| S3 artifacts | `opal-gateway-d3c31e972e.tar.gz` new; `-latest` re-pointed with `git-ref` `d3c31e972e` | the rollback re-points `-latest` at the base artifact |
| mcportal | none (`d60b4e0` as MP-x-4 left it; the bun pre-check reads 77 of 77 at that pin) | n/a |

**Not touched:** every role, policy, grant and identity; ADVI_BILLING E2 and the `.pptx` pair (both unreleased; the
two-file cut cannot carry them, and the base's deploy script keeps their `.env` lines out); the ALB; both secrets.

**Both branches of each leg:**
- The base differs at the apply -> VOID; no act.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy the versioned base artifact; the ledger closes ROLLED-BACK.
- Any read-back fails -> redeploy the versioned base artifact; the ledger closes ROLLED-BACK, plus a BLOCKING row.

## 3. G-A delta

Unchanged from v1. This is a content release of `opal_discover` and the regenerated catalog: no tool, route or
integration is added, removed or enabled. discover states the served as-of with claim `measured` (FWD-13), and it reads
`needs:` with the owner, status, write class and the CALLER's grant from the existing `tool_denial` (FWD-14, FWD-17).
Need matches go to Opal-internal principals only (Z-S87).

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on the v2 pins

I sign the blast radius in section 2 on:
- deploy-only commit `d3c31e972e`, gateway tree `a605ad2f79`;
- the rollback artifact `opal-gateway-1e32562729.tar.gz` (tree `C:/tmp/mx-rb-v2`);
- live base `1e32562729` as I measured it on both planes at 18:18:49Z (section 0).

It covers both branches of every leg. The `.env` equality is signed as the RULE, with 52 the count read on the base.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- the presence of E2's or the pptx pair's content.
