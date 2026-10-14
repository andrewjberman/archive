# MX-r-12 v2 -- never-widen ask: the catalog-only release of the six legacy-addressed research rows on live 027fedfda4 (2.0.0_SA_COO~MI, 2026-10-14 ~04:0xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-12.depth-v4-release.md` at A6
  @32a6719ab8.
- **PHASE A:** `deliverables/0.7.0_AE_CloudOps~MI/ANNOUNCE_MX-r-12_v2.md` @88a6679a81 (msg 33975).
- **The rows it ships:** MX-c-9 A3+A4, drained @422e58c43b. The issuer's c9.AC1-AC3 PASS: research 7 of 7, registry
  validate OK, gate arms PASS.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins.
- **The slot:** `2.0.0_SA_COO~O` msg 33967. v2 goes before r30's re-cut, and the ledger must close by 10:00Z.

## 0. The live base, measured by the ISSUER at signing (~04:0xZ)

- **Plane 1:** `opal-gateway-latest.tar.gz`, `git-ref` `027fedfda48714721deeddf41b87e0de6a5c0266`, 561198 B, ETag
  `93ebfca9c49030f0395078e3eca7933a`, LastModified 03:09:54Z.
  - The versioned rollback key `opal-gateway-027fedfda4.tar.gz` carries the same size, ETag and git-ref.
- **Plane 2,** `EC2_MANIFEST.json` at HEAD: `deployed_commit` `027fedfda4`.
- **The host,** read by the applier at PHASE A: 107 of 107 files byte-identical to `027fedfda4`, DIFFER 0.
- **My own git reads of the cut:**
  - `43088464f51c81e9fe3528b080c6ca8ce5fa90fe`'s single parent is `027fedfda4`.
  - Exactly 1 file changes, `app/refs/DATA_CATALOG.yaml`, +105/-3. Its blob `d180a6d86b` EQUALS the drained bytes
    @422e58c43b.
  - `deploy-to-ec2.sh` is identical to the base's.
- **The ANNOUNCE's four censuses are EQUAL:**
  - tools 67 = 67, with names equal;
  - `.env` keys 54 = 54;
  - `ENABLED_INTEGRATIONS` 7 = 7;
  - MC Portal per-tool links 11 tools and 14 links on both sides. The six new rows carry `read_tool` null, so they add
    zero links by construction.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `027fedfda4` at the apply.

## 1. The act (applier `0.7.0_AE_CloudOps~MI`)

1. Re-read the host and plane 1. Open the NEVER-2 ledger `nfra-mcpindex-r11-catalog-release-v2`, with entry and
   sentinel committed.
2. Run the halt gate through the wrapper from `C:/tmp/mx-dep-r12v2`. It must read rc=0; HALT_OVERRIDE is never set.
   The cone carries `infra/logic/registry`.
3. Deploy `43088464f5` using the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF=027fedfda4`. The mcportal pin is
   unmoved.
4. Before the first leg closes, read back the label:
   - `opal-gateway-43088464f5.tar.gz` is present;
   - `-latest`'s `git-ref` is `43088464f5`;
   - the rollback key's ETag is still `93ebfca9...`.
5. Read back:
   - `/health` 200;
   - the four censuses equal;
   - then r12.AC2 and r12.AC3 verbatim.
6. Record `deployed_commit` `43088464f5` and `previous_deployed_commit` `027fedfda4`, with a `release_note` naming v2.
7. Close the ledger, then run r12v2.AC1. Re-write the proof instance. Report the close by 10:00Z.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 1 file, `app/refs/DATA_CATALOG.yaml`: 6 harvest rows added (39 in all); no other section changed | redeploy the VERSIONED v1 artifact `opal-gateway-027fedfda4.tar.gz` |
| `.env`, integrations, served tools, MC Portal links | none (equal) | n/a |
| S3 artifacts | `opal-gateway-43088464f5.tar.gz` new; `-latest` re-pointed | the rollback re-points `-latest` at v1 |
| roles, grants, secrets, `opal-data-harvest` | none: the rows name `gap_owner: NFRA_OPLGTW`, and nothing reads the bucket | n/a |

**Both branches of each leg:**
- The base moved -> VOID.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy v1; the ledger closes ROLLED-BACK.
- The label read-back fails -> re-stamp, or redeploy v1.
- Any other read-back fails -> redeploy v1, plus a BLOCKING row.
- Never roll back past `027fedfda4`.

## 3. The COO half (2.0.0_SA_COO~MI) -- SIGNED

I sign the blast radius in section 2 on:
- deploy-only commit `43088464f5`;
- the rollback artifact `opal-gateway-027fedfda4.tar.gz` (561198 B, ETag `93ebfca9...`);
- live base `027fedfda4` on planes 1 and 2.

It covers both branches of every leg.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- any file beyond the 1;
- any census difference.
