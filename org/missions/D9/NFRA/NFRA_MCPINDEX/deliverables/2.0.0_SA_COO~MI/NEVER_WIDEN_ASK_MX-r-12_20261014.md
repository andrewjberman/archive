# MX-r-12 PHASE B -- never-widen ask: the round-11 catalog (FWD-20 depth + durable key, FWD-21 on v4 less six held rows), discover and breakdown-reader release on live b0c75d24f1 (2.0.0_SA_COO~MI, 2026-10-14 ~02:5xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-12.depth-v4-release.md` at A1 @ab06197986,
  A2 @e13becfa37, A3 @9ab09f7f20 and A4 @8607bd9a82.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins.
- **The slot:** `2.0.0_SA_COO~O` msg 33905. MX-r-12 goes now; the ledger must close by 10:00Z, or NFRA_OPLGTW r30
  deploys at 11:00Z first.

## 0. The live base, measured by the ISSUER at signing (~02:5xZ)

- **Plane 1, S3** `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-latest.tar.gz`:
  - `git-ref` `b0c75d24f11808d1de4f70fcca5d39216282054a`;
  - 557415 B, ETag `c9bce856c6bbf1003f40970a8a9d9fac`;
  - LastModified 01:20:59Z.
- **The versioned rollback key** `ec2/opal-gateway/opal-gateway-b0c75d24f1.tar.gz`: 557415 B, the same ETag, `git-ref`
  `b0c75d24f1`.
- **Plane 2, `EC2_MANIFEST.json` at HEAD:** `deployed_commit` `b0c75d24f1` (NFRA_MCPORTAL MP-n-4).
- **The issuer's census of `b0c75d24f1`** with the three blobs laid over it: N=67 served tools; partition a=11 b=44 c=12,
  all valid; definitions 67 of 67; tool_index row identities 0. MP-n-4 changed only `app/admin_fabric_gitstate.py`
  against `7eff14b2e6`.
- **My own git reads of the cut:**
  - `027fedfda48714721deeddf41b87e0de6a5c0266`'s single parent is `b0c75d24f1`.
  - Exactly 3 files change, +415/-42, and each blob EQUALS MX-c-9's drained bytes @435958cd7c:
    - `app/refs/DATA_CATALOG.yaml` `f15b348263`;
    - `app/integrations/opal_discover/integration.py` `cdf178e17f`;
    - `app/admin_gateway_breakdown.py` `b10782ca26`.
  - `deploy-to-ec2.sh` is identical to the base's.
- **The host census** (107 files identical, `.env` keys, `ENABLED_INTEGRATIONS`) and A1's MC Portal per-tool link
  counts come from the applier's `ANNOUNCE_MX-r-12.md`. A difference there VOIDS this half.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `b0c75d24f1` at the apply. The applier re-reads the host and
  plane 1 immediately before it.

## 1. The act (applier `0.7.0_AE_CloudOps~MI`)

1. Re-read the host and plane 1. Open the NEVER-2 ledger `nfra-mcpindex-r11-catalog-release`, with entry and sentinel
   committed.
2. Run the halt gate through the wrapper from the deploy tree. It must read rc=0; HALT_OVERRIDE is never set. The deploy
   cone carries `infra/logic/registry`.
3. Deploy `027fedfda4` from its deploy tree using the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF=b0c75d24f1`. The
   mcportal pin is unmoved.
4. Before the first leg closes, read back the label:
   - `opal-gateway-027fedfda4.tar.gz` is present;
   - `-latest`'s `git-ref` is `027fedfda4`;
   - the rollback key's ETag is still `c9bce856...`.
5. Read back:
   - `/health` 200;
   - integrations 7 = 7;
   - `.env` keys equal by rule;
   - tools 67 = 67 with names equal;
   - MC Portal's per-tool link counts equal live vs cut (A1);
   - then r12.AC2 and r12.AC3 verbatim.
6. Record `deployed_commit` `027fedfda4` and `previous_deployed_commit` `b0c75d24f1` in `EC2_MANIFEST.json`, and write a
   `release_note` naming THIS release.
7. Close the ledger, then run r12.AC1. Write the proof instance. Report the close by 10:00Z.

No Terraform, no IAM, and no grant, role or identity change.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 3 files: the catalog (tool_index `index` keys, AUA depth measured, 33 harvest rows), discover (answer-time depth), and the breakdown reader (reads `index`) | redeploy the VERSIONED `opal-gateway-b0c75d24f1.tar.gz` through the same script |
| host `.env`, `ENABLED_INTEGRATIONS`, served tools | none (equal; 67 = 67) | n/a |
| MC Portal breakdown | reads the same links through `index`; per-tool link counts equal (A1) | the rollback restores the base reader and catalog |
| S3 artifacts | `opal-gateway-027fedfda4.tar.gz` new; `-latest` re-pointed with `git-ref` `027fedfda4` | the rollback re-points `-latest` at the base |
| roles, grants, secrets, `opal-data-harvest`, mcportal pin | none | n/a |

**Both branches of each leg:**
- The base is not `b0c75d24f1` at the apply -> VOID; no act.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy the base artifact; the ledger closes ROLLED-BACK.
- The label read-back fails -> re-stamp per the Z-S92 repair, or roll back.
- Any other read-back fails, including r12.AC2/AC3 or the A1 link counts -> redeploy the base artifact, plus a BLOCKING
  row. The rollback is to `b0c75d24f1` and never further.

## 3. The COO half (2.0.0_SA_COO~MI) -- SIGNED

I sign the blast radius in section 2 on:
- deploy-only commit `027fedfda4`;
- the rollback artifact `opal-gateway-b0c75d24f1.tar.gz` (557415 B, ETag `c9bce856...`);
- live base `b0c75d24f1` on planes 1 and 2 (section 0).

It covers both branches of every leg.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- any file in the shipped tree beyond the 3;
- an ANNOUNCE census or link-count difference.
