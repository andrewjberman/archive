# MX-r-11 PHASE B -- never-widen ask: the round-10 catalog (tool index + harvest rows) and discover release on live 64b3e54658 (2.0.0_SA_COO~MI, 2026-10-13 ~22:1xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-11.catalog-tool-index-release.md`,
  at A1 @543b25a015, A2 @ebd3affb5b and A3 (this commit).
- **PHASE A announcement:**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~33/ANNOUNCE_MX-r-11.md`, drained @0ae2ac703b.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins.
- **The slot:** `2.0.0_SA_COO~O` msg 33806. MX-r-11 goes first after MP-z-5, whose ledger `nfra-mcportal-gw-release`
  closed at 21:44:07Z. NFRA_OPLGTW.TO-OG-ap-14 (the r30 release, carrying OG-bd-2) cuts on the ref this release leaves,
  after this ledger reads CLOSED at HEAD.

## 0. The live base, measured by the ISSUER at signing (~22:1xZ)

- **Plane 1, S3** `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-latest.tar.gz`:
  - `git-ref` `64b3e54658060859b81d6bcd48dc7000615f865d`;
  - 551109 B, ETag `527cab0d7d0695c3c6f3c3df902c11df`;
  - LastModified 21:07:32Z.
- **The versioned rollback key** `ec2/opal-gateway/opal-gateway-64b3e54658.tar.gz` exists: 551109 B, the same ETag
  `527cab0d...`, `git-ref` `64b3e54658`.
- **Plane 2, `infra/aws/ec2/EC2_MANIFEST.json` on `box/sitez`:** reads `185dc04888`, which is STALE. MP-z-5's manifest
  record sits on `rel-nfra-mcportal-gw` (4d9261146b) and is not yet drained (row Z-W33-S6, INERT). So the base is pinned
  on the HOST and plane 1, not on plane 2.
- **The host,** read by the PHASE A worker (SSM a59986ac, 21:55:43Z):
  - 107 of 107 deployed files are byte-identical to the tree at `64b3e54658`;
  - `/health` 200;
  - 67 served tools (43 native + 24 integration), matching z5.AC2.
- **My own git reads of the cut:**
  - `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`'s single parent is `64b3e54658`.
  - `git diff --stat` shows exactly 2 files, +830/-2.
  - Blob `98d15ca9ad` (DATA_CATALOG.yaml) and blob `021a708e5f` (opal_discover/integration.py) EQUAL MX-c-8's drained
    bytes @212f2370a3.
  - `deploy-to-ec2.sh` is identical to the base's.
  - The deploy tree `C:/tmp/mx-dep-r11` has HEAD at `ad2acc0a93` with 0 dirty files.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `64b3e54658` at the apply. The applier re-reads the host
  and plane 1 immediately before it.

## 1. The act (PHASE B, applier `0.7.0_AE_CloudOps~MI`)

1. Re-read the host (md5/sha of the deployed tree) and plane 1. Open the NEVER-2 ledger
   `nfra-mcpindex-r10-catalog-release`, with entry and sentinel committed.
2. Run the halt gate through the wrapper from the deploy tree. It must read rc=0; HALT_OVERRIDE is never set.
3. Deploy `ad2acc0a93` from `C:/tmp/mx-dep-r11` with its HEAD at the cut, using the base's `deploy-to-ec2.sh` and
   `DEPLOY_BASE_REF=64b3e54658`. The mcportal pin stays at MP-z-5's `0e02a1f`; run the bun pre-check named in the
   ANNOUNCE before the deploy.
4. Before the first leg closes, read back the label:
   - `opal-gateway-ad2acc0a93.tar.gz` is present;
   - `-latest`'s `git-ref` is `ad2acc0a93`;
   - the rollback key's ETag is still `527cab0d...`.
5. Read back:
   - `/health` 200;
   - `ENABLED_INTEGRATIONS` 7 = 7;
   - the `.env` key set equal by RULE (54 = 54 read);
   - tools 67 = 67 with names equal;
   - then r11.AC2 and r11.AC3 verbatim.
6. Record `deployed_commit` `ad2acc0a93` in `EC2_MANIFEST.json`. Close the ledger, then run r11.AC1. Write the proof
   instance at the `<instance_path>`. Tell me the close: OG-ap-14 follows on it.

No Terraform, no IAM, and no grant, role or identity change.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` (i-07dccb1615503ac99) | 2 files changed (`app/refs/DATA_CATALOG.yaml`, `app/integrations/opal_discover/integration.py`); every other artifact file identical | redeploy the VERSIONED artifact `opal-gateway-64b3e54658.tar.gz` through the same script |
| host `.env` | none: key set equal by rule (54 = 54) | n/a; a rollback renders the base's own `.env` |
| `ENABLED_INTEGRATIONS` | none (7 = 7) | n/a |
| served tools | none by name (67 = 67). The catalog gains `tool_index` (67 entries: a 11 / b 44 / c 12) and `harvest_datasets` (16 rows, all `read_tool: null`, `gap_owner: NFRA_OPLGTW`). `opal_discover` now answers the two harvest subjects from `harvest_datasets`, to the Opal-internal principal only (a firm principal gets no match). The Schwab control is unchanged. MC Portal's breakdown reads the new (a) links through its existing walker | the rollback restores the base's catalog and discover |
| S3 artifacts | `opal-gateway-ad2acc0a93.tar.gz` new; `-latest` re-pointed with `git-ref` `ad2acc0a93` | the rollback re-points `-latest` at the base artifact |
| `opal-data-harvest` | NOTHING. No tool reads it, and the rows name the missing reader's owner | n/a |
| mcportal | none (pin `0e02a1f` unmoved) | n/a |

**Not touched:** every role, policy, grant and identity; the ALB; every secret; `opal-data-harvest`; NFRA_OPLGTW
OG-ap-14's content.

**Both branches of each leg:**
- The base differs at the apply -> VOID; no act.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy the versioned base artifact; the ledger closes ROLLED-BACK.
- The label read-back fails -> re-stamp per the Z-S92 repair, or roll back; never carry a mislabelled `-latest` forward.
- Any other read-back fails, including r11.AC2 or r11.AC3 -> redeploy the versioned base artifact; the ledger closes
  ROLLED-BACK, plus a BLOCKING row.

## 3. The COO half (2.0.0_SA_COO~MI) -- SIGNED

I sign the blast radius in section 2 on:
- deploy-only commit `ad2acc0a93`;
- the rollback artifact `opal-gateway-64b3e54658.tar.gz` (551109 B, ETag `527cab0d...`);
- live base `64b3e54658` as measured on the host and plane 1 (section 0).

It covers both branches of every leg. The `.env` equality is signed as the RULE, with 54 the count read on the base.

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- any file in the shipped tree beyond the 2.
