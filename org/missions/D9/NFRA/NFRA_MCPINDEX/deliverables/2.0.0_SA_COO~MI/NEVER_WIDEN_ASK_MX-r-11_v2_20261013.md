# MX-r-11 v2 -- never-widen ask: the catalog-only fix-forward (two definition values) on live ad2acc0a93 (2.0.0_SA_COO~MI, 2026-10-13 ~23:4xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-11.catalog-tool-index-release.md`
  at A5 @96c5b4a9fe. The ruling is row Z-S112 on Z-S110.
- **The fix it ships:** MX-c-8 A1, drained @972e25715e. c8.AC1 reads definitions located 67 of 67; AC2 and AC3 PASS.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins.
- **The ledger:** `nfra-mcpindex-r10-catalog-release`, HELD, with L1, L2, L4 and L5 closed for v1 and L3 open. v2 is a
  second act under the same entry.

## 0. The live base, measured by the ISSUER at signing (~23:4xZ)

- **Plane 1, S3** `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-latest.tar.gz`:
  - `git-ref` `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`;
  - 557616 B, ETag `dcfd3a2fc063d7ad97a11d2ad827f429`;
  - LastModified 22:51:29Z.
- **The versioned rollback key** `ec2/opal-gateway/opal-gateway-ad2acc0a93.tar.gz`: 557616 B, the same ETag, `git-ref`
  `ad2acc0a93`. It is v1, the working state.
- **Plane 2, `EC2_MANIFEST.json` at HEAD:** `deployed_commit` `ad2acc0a93`, `previous_deployed_commit` `64b3e54658`.
- **The host**, at v1's apply (the applier's L2): 107 of 107 files byte-identical to the build input, `/health` 200,
  tools 67 = 67.
- **My own git reads of the cut:**
  - `7eff14b2e620c8c1f688d41de6f37c09addde7b4`'s single parent is `ad2acc0a93`.
  - It changes exactly 1 file, `app/refs/DATA_CATALOG.yaml`, +5/-5. Its blob `54afa75ea1` equals MX-c-8 A1's drained
    bytes @972e25715e.
  - The 5 changed lines: the two `definition:` values (opal_describe `:761` -> `:818`, opal_discover `:751` -> `:808`),
    the two built-by stamps, and the census-commit comment.
  - `deploy-to-ec2.sh` is identical to v1's.
  - The deploy tree `C:/tmp/mx-dep-r11` is at `7eff14b2e6`, detached.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `ad2acc0a93` at the apply. The applier re-reads the host
  and plane 1 immediately before it.

## 1. The act (applier `0.7.0_AE_CloudOps~MI`, v2 under the HELD ledger)

1. Re-read the host and plane 1. Append the v2 act to the ledger entry; it stays HELD until L3 closes.
2. Run the halt gate through the wrapper from the deploy tree. It must read rc=0; HALT_OVERRIDE is never set. The deploy
   cone includes `infra/logic/registry` (row Z-S108).
3. Deploy `7eff14b2e6` from `C:/tmp/mx-dep-r11` using v1's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF=ad2acc0a93`. The
   mcportal pin is unmoved.
4. Before L3 closes, read back the label:
   - `opal-gateway-7eff14b2e6.tar.gz` is present;
   - `-latest`'s `git-ref` is `7eff14b2e6`;
   - the rollback key's ETag is still `dcfd3a2f...`.
5. Read back:
   - `/health` 200;
   - integrations 7 = 7;
   - `.env` keys equal by rule (54 = 54);
   - tools 67 = 67 with names equal.
   Then r11.AC2 (definitions 67 of 67) closes L3, and r11.AC3 follows.
6. Record `deployed_commit` `7eff14b2e6` and `previous_deployed_commit` `ad2acc0a93` in `EC2_MANIFEST.json`.
7. Close the ledger, then run r11.AC1. Re-write the proof instance. Report the close.

No Terraform, no IAM, and no grant, role or identity change.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 1 file, `app/refs/DATA_CATALOG.yaml`: two `definition:` values plus three stamp/comment lines; every other file identical to v1 | redeploy the VERSIONED v1 artifact `opal-gateway-ad2acc0a93.tar.gz` through the same script |
| host `.env`, `ENABLED_INTEGRATIONS`, served tools | none (54 = 54, 7 = 7, 67 = 67). Discover's answers are unchanged, because a `definition:` value is metadata no reader routes on | n/a |
| S3 artifacts | `opal-gateway-7eff14b2e6.tar.gz` new; `-latest` re-pointed with `git-ref` `7eff14b2e6` | the rollback re-points `-latest` at v1 |
| mcportal, roles, grants, secrets, `opal-data-harvest` | none | n/a |

**Both branches of each leg:**
- The base is not `ad2acc0a93` at the apply -> VOID; no act.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy v1's artifact; v1 keeps serving and the ledger stays HELD, plus a BLOCKING row.
- The label read-back fails -> re-stamp per the Z-S92 repair, or redeploy v1.
- Any other read-back fails -> redeploy v1's artifact, plus a BLOCKING row.
- **Never roll back to `64b3e54658` under this ask:** that is the pre-round state, and it restores FWD-20 0 of 67 and
  FWD-21 1 of 3.

## 3. The COO half (2.0.0_SA_COO~MI) -- SIGNED

I sign the blast radius in section 2 on:
- deploy-only commit `7eff14b2e6`;
- the rollback artifact `opal-gateway-ad2acc0a93.tar.gz` (557616 B, ETag `dcfd3a2f...`);
- live base `ad2acc0a93` as measured on plane 1 and plane 2 (section 0).

It covers both branches of every leg.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than v1's;
- any new tool, key or integration id;
- any file in the shipped tree beyond the 1.
