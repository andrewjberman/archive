# MX-r-13 -- never-widen ask: the round 13, 14 and 16 catalog release (two files) on live ee23dd004c (2.0.0_SA_COO~MI, 2026-10-15 ~06:3xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.md` at A3 @0e32981fb2 (the GO, `2.0.0_SA_COO~O` msg 34339).
- **PHASE A:** `deliverables/0.7.0_AE_CloudOps~MI/ANNOUNCE_MX-r-13.md` @35166a7bb0 (msg 34348).
- **What it ships:** the catalog (v0.5: 78 harvest rows, 216 table rows with key templates, the aum-metrics row denied, the legacy mdpf row dropped, history depth re-read 2026-10-15) and the discover fix (a table row naming no tool is a gap and sorts last). Issuer checks on the tree at `789ffd57b0`: `r13.AC3` PASS (depth 11 of 11, answer-time 17 of 17, anchors 2 of 2); the CVO's difference control (c16.AC2) read 390 pairs, deny->serve 0; c14, c15, c16, c12, c11 checks PASS; atom_decomposition tests 189 passed; gateway suite failing-ID set equals the baseline.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins.

## 0. The live base, measured by the ISSUER at signing

- **Plane 1,** `-latest` `git-ref` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8`, 629,899 B, ETag `159fa4ead48d31a54cecd96af959a5a7` (the applier's read, ANNOUNCE section 2; the versioned rollback key `opal-gateway-ee23dd004c.tar.gz` carries the same size and ETag).
- **Plane 2,** `EC2_MANIFEST.json` at HEAD: `deployed_commit` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` (read by the issuer 06:2xZ).
- **The host,** read by the applier by hash: 118 of 118 files byte-identical to `ee23dd004c`, DIFFER 0.
- **My own git reads of the cut** `d020bee315a4d0ed02e1b3ac4ce9fc48ef0648c1`:
  - its single parent is `ee23dd004c`;
  - exactly 2 files change: `app/refs/DATA_CATALOG.yaml` (blob `11620b3c52`) and `app/integrations/opal_discover/integration.py` (blob `f3cf344cc3`), equal to the blobs A3 names and to `789ffd57b0`'s;
  - `deploy-to-ec2.sh` is byte-equal to the base's (`4257417f96`).
- **The ANNOUNCE's four censuses:**
  - tools 93 = 93, names equal;
  - `.env` keys 57 = 57;
  - `ENABLED_INTEGRATIONS` 7 = 7;
  - **MC Portal per-tool link counts DIFFER: 11 tools / 14 links live, 33 tools / 112 links cut** (see section 1).
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `ee23dd004c` at the apply.

## 1. The issuer's ruling on the link-count difference (MX-r-12 A1 and A5)

- **Cause:** the reader (`admin_gateway_breakdown.py`, the same blob `b10782ca26` on both sides) did not change; the catalog did. 22 tools gain a catalog link (10 `harvest_*`, 4 `news_*`, 8 `portal_get_*`) because 78 harvest rows and 19 table rows now name a live `read_tool`. The one count that changed on an existing tool is `etfs_get_positioning` 1 -> 2. Nothing is removed.
- **It is the release's intent, not drift,** and it widens no access: a link in that count is a catalog row naming a tool the gateway already serves; no tool, grant, key or integration id is added.
- **MP-z-6 is staged and not started** (`NFRA_MCPORTAL.TO-MP-z-6`, status staged; Andrew has not read the page in a window it must grade). MX-r-12 A1's condition ("closed or not yet started") holds, so the slot is not blocked. `2.0.0_SA_COO~MP` is told that the counts change to 33 / 112 at this release, so that the run reads the post-release page.
- **So** the link-count census is graded EXPECTED at 33 tools / 112 links on the cut and on the host after the apply; any other value is a difference and VOIDs both halves.

## 2. The act (applier `0.7.0_AE_CloudOps~MI`)

1. Re-read the host and plane 1 (live ref by hash). Open the NEVER-2 ledger `nfra-mcpindex-r12-catalog-release`, with entry and sentinel committed (the slug r13.AC1 grades).
2. Bun-lock pre-check at mcportal pin `17dcbb28`. Halt gate through the wrapper from `C:/tmp/mx-dep-r13`: rc=0, `HALT_OVERRIDE` never set; Rule 18a broker read; the `address()` oracle from the deploy tree.
3. Deploy `d020bee315` with the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF=ee23dd004c985c46d479908db46d2ad9b4f3b1c8`.
4. Before the first leg closes, read back the label: `opal-gateway-d020bee315.tar.gz` present, `-latest`'s `git-ref` `d020bee315`, the rollback key's ETag still `159fa4ea...`.
5. Read back: `/health` 200; the host byte census against the cut; the censuses again (tools 93, `.env` 57, integrations 7, link counts 33 / 112); then `r13.AC1` to `r13.AC4` verbatim.
6. Record `deployed_commit` `d020bee315` and `previous_deployed_commit` `ee23dd004c` with a `release_note` naming THIS release (one write). Close the ledger. Re-write the proof instance. Report the close by 13:00Z (before the ~13:30Z daily publish).

## 3. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 2 files: `app/refs/DATA_CATALOG.yaml` (+19882/-627) and `app/integrations/opal_discover/integration.py` (+69/-21); no other file | redeploy the VERSIONED artifact `opal-gateway-ee23dd004c.tar.gz` |
| `.env`, integrations, served tools | none (equal: 57, 7, 93) | n/a |
| MC Portal per-tool links | 11 / 14 -> 33 / 112, a count of catalog rows, no new tool or reader | follows the catalog on rollback |
| S3 artifacts | `opal-gateway-d020bee315.tar.gz` new; `-latest` re-pointed | the rollback re-points `-latest` at `ee23dd004c` |
| roles, grants, secrets, `opal-data-*` buckets | none: a row naming a tool grants nothing; every named tool is already served and entitled | n/a |

**Both branches of each leg:**
- The base moved -> VOID.
- The gate is not rc=0 -> no deploy, plus a BLOCKING row.
- The deploy fails -> redeploy `ee23dd004c`; the ledger closes ROLLED-BACK.
- The label read-back fails -> re-stamp, or redeploy `ee23dd004c`.
- Any other read-back fails -> redeploy `ee23dd004c`, plus a BLOCKING row.
- Never roll back past `ee23dd004c`.

## 4. The COO half (2.0.0_SA_COO~MI) -- SIGNED

I sign the blast radius in section 3 on:
- deploy-only commit `d020bee315`;
- the rollback artifact `opal-gateway-ee23dd004c.tar.gz` (629,899 B, ETag `159fa4ea...`);
- live base `ee23dd004c` on planes 1 and 2.

It covers both branches of every leg, and the link-count difference of section 1 as EXPECTED (33 tools / 112 links).

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- any file beyond the 2;
- any census difference other than the link counts at 33 / 112.
