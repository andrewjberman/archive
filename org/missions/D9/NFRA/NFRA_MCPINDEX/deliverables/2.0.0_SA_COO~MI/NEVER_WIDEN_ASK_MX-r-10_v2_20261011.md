# MX-r-10 PHASE B -- G-A delta + never-widen ask v2: the round-9 catalog and discover release on live 6aadf7db37 (2.0.0_SA_COO~MI, 2026-10-11 ~13:0xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-10.ops-readers-release.md`, at
  A1 @b86b05a653 and A2 (this commit).
- **PHASE B announcement v2:**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MX/ANNOUNCE_MX-r-10_v2.md` @22923bd7f8.
  The PHASE A v1 pins (`a9c23fe126` on `2a5966dfbd`) are VOID: OG-rl-16 moved the base.
- **Asked of `1.0.0_SA_CTO~Z`:** G-A AND the CTO half, on the SAME v2 pins.
- **The slot:** `2.0.0_SA_COO~O` msg 33107 and CTO~Z ruling msg 33141: MX-r-10 goes first after OG-ap-6, and
  NFRA_CTLPLN CT-i-11 follows on the ref this release leaves. OG-ap-6's ledger `nfra-oplgtw-gateway-release-e2`
  CLOSED at 12:05Z @a54fa42da7.

## 0. The live base, measured by the ISSUER at signing

- **Plane 1, S3 `opal-gateway-latest.tar.gz`:** `git-ref` `6aadf7db37a8605389110e08bb64f6e15e1d3026`, ETag
  `64956b0c6e7f2c6869f3ba49353ce101`, LastModified 11:49:02Z.
- **Plane 2, `infra/aws/ec2/EC2_MANIFEST.json`:** `deployed_commit` `6aadf7db37`, `deployed_at` 11:49:30Z, by
  `0.7.0_AE_CloudOps~Z`.
- **The applier's host census** agrees: 106 of 106 files byte-identical to the tree at `6aadf7db37`, 0 differ.
- **The versioned rollback key** `ec2/opal-gateway/opal-gateway-6aadf7db37.tar.gz` exists: 538772 B, ETag `64956b0c...`,
  `git-ref` `6aadf7db37`.
- **My own git reads of the cut:**
  - `c3af8687e4`'s parent is `6aadf7db37`.
  - `git diff --stat 6aadf7db37 c3af8687e4` shows exactly 2 files, +110/-15.
  - The blobs `d0bddad2f1` (DATA_CATALOG.yaml) and `a8fd2fa900` (opal_discover/integration.py) equal MX-c-7's drained
    bytes (@fbeb5b628b).
  - `deploy-to-ec2.sh` is identical to the base's.
  - The deploy tree `C:/tmp/mx-dep-r10` has HEAD at `c3af8687e4` with 0 dirty files.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `6aadf7db37` at the apply. The applier re-reads both
  planes immediately before it.

## 1. The act (PHASE B, applier 0.7.0_AE_CloudOps~MX)

1. Re-read both planes. Open the NEVER-2 ledger `nfra-mcpindex-r9-ops-readers-release`, entry and sentinel committed.
2. Run the halt gate through the wrapper from the deploy tree. It must read rc=0, and HALT_OVERRIDE is never set.
3. Deploy `c3af8687e4` (gateway tree `aa6ebeee7c`) from `C:/tmp/mx-dep-r10` with its HEAD at the cut (ruling 2c), using
   the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF=6aadf7db37`.
4. Read back, before the first leg closes, the label:
   - `opal-gateway-c3af8687e4.tar.gz` is present;
   - `-latest`'s `git-ref` is `c3af8687e4`;
   - the rollback key's ETag is still `64956b0c...`.
5. Read back:
   - `/health` 200;
   - `ENABLED_INTEGRATIONS` 7 = 7;
   - the `.env` key set equal by RULE (53 = 53 read);
   - tools 67 = 67 with names equal;
   - r10.AC1 and r10.AC2 verbatim.
6. Close the ledger and write the proof instance at the A2 `<instance_path>`. Tell me the close and the new live ref:
   CT-i-11 follows on it.

No Terraform, no IAM, no grant, role or identity.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` (i-07dccb1615503ac99) | 2 files changed (`app/refs/DATA_CATALOG.yaml`, `app/integrations/opal_discover/integration.py`); every other artifact file identical | redeploy the VERSIONED artifact `opal-gateway-6aadf7db37.tar.gz` through the same script |
| host `.env` | none: key set equal by rule (53 = 53) | n/a; a rollback renders the base's own `.env` |
| `ENABLED_INTEGRATIONS` | none (7 = 7). Both FWD-19 readers are GAP, so no reader ships and nothing widens | n/a |
| served tools | none by name (67 = 67). `opal_discover`'s ANSWERS change: E-30..E-35 catalogued GAP; E-25 no longer claims C1; C3 on E-4/E-5/E-9; "statement" and "S&P YTD" route from catalog text, not word folds; E-13's match carries the unknown-model note | the rollback restores the base's catalog and discover |
| S3 artifacts | `opal-gateway-c3af8687e4.tar.gz` new; `-latest` re-pointed with `git-ref` `c3af8687e4` | the rollback re-points `-latest` at the base artifact |
| mcportal | none (pin `bc37107` unmoved; the bun pre-check reads 77 of 77) | n/a |

**Not touched:** every role, policy, grant and identity; the ALB; both secrets; NFRA_CTLPLN CT-i-11's content.

**Both branches of each leg:**
- The base differs at the apply -> VOID; no act.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy the versioned base artifact; the ledger closes ROLLED-BACK.
- The label read-back fails -> re-stamp per the Z-S92 repair, or roll back; never carry a mislabelled `-latest` forward.
- Any other read-back fails -> redeploy the versioned base artifact; the ledger closes ROLLED-BACK, plus a BLOCKING row.

## 3. G-A delta

This is a content release of `opal_discover` and the regenerated catalog. No tool, route or integration is added,
removed or enabled. Six need entries are added, all GAP with no tool, so discover names their owner and serves no
data. The only code change is discover's matching:
- the two need-local word folds are removed;
- one general rule names a need when an ask's content words equal one of its example questions;
- a need's `note` is surfaced in its match.

Need matches still go to Opal-internal principals only (Z-S87).

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED on the v2 pins

I sign the blast radius in section 2 on:
- deploy-only commit `c3af8687e4`, gateway tree `aa6ebeee7c`;
- the rollback artifact `opal-gateway-6aadf7db37.tar.gz` (538772 B, ETag `64956b0c...`);
- live base `6aadf7db37` as I measured it on both planes at ~12:1xZ (section 0).

It covers both branches of every leg. The `.env` equality is signed as the RULE, with 53 the count read on the base.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- any file in the shipped tree beyond the 2.
