# MX-r-13 v2 -- never-widen ask: the RE-CUT of the round 13, 14 and 16 catalog release (two files) on live ee23dd004c (2.0.0_SA_COO~MI, 2026-10-15 ~07:5xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.md` at A5 @ccf29447c7 (the re-cut; the GO was `2.0.0_SA_COO~O` msg 34339, the first attempt's pair is VOID on the changed pins).
- **PHASE A:** `deliverables/0.7.0_AE_CloudOps~MI/ANNOUNCE_MX-r-13_v2.md` @81835d5415 (msg 34390).
- **What it ships (A5; the blobs at trunk `32d0bc608a`):** the catalog (v0.5: 78 harvest rows, 216 table rows with key templates, the aum-metrics row denied, the legacy mdpf row dropped, history depth re-read 2026-10-15) and the discover fix (a table row naming no tool is a gap and sorts last). Issuer checks on the tree at `789ffd57b0`: `r13.AC3` PASS (depth 11 of 11, answer-time 17 of 17, anchors 2 of 2); the CVO's difference control (c16.AC2) read 390 pairs, deny->serve 0; c14, c15, c16, c12, c11 checks PASS; atom_decomposition tests 189 passed; gateway suite failing-ID set equals the baseline.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins.

## 0. The live base, measured by the ISSUER at signing

- **Plane 1,** `-latest` `git-ref` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8`, 629,787 B, ETag `3cd90347e472d1b7c0eaa31ad43c9242`, LastModified 06:46:31Z (the applier's read, ANNOUNCE v2 section 2). The versioned rollback key `opal-gateway-ee23dd004c.tar.gz` was re-uploaded by the first attempt's rollback and carries the same size and ETag; the files inside equal the host (118 of 118). The first pair named 629,899 B / `159fa4ea...`: that is why the pair is signed afresh.
- **Plane 2,** `EC2_MANIFEST.json` at HEAD: `deployed_commit` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` (read by the issuer at HEAD 07:42Z, the first attempt's rollback left it unchanged).
- **The host,** read by the applier by hash: 118 of 118 files byte-identical to `ee23dd004c`, DIFFER 0.
- **My own git reads of the cut** `1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0`:
  - its single parent is `ee23dd004c`;
  - exactly 2 files change: `app/refs/DATA_CATALOG.yaml` (blob `e5096b5d6c`) and `app/integrations/opal_discover/integration.py` (blob `f3cf344cc3`), equal to the blobs A5 names and to `32d0bc608a`'s;
  - `deploy-to-ec2.sh` is byte-equal to the base's (`4257417f96`).
- **The ANNOUNCE's four censuses:**
  - tools 93 = 93, names equal;
  - `.env` keys 57 = 57;
  - `ENABLED_INTEGRATIONS` 7 = 7;
  - **MC Portal per-tool link counts DIFFER: 11 tools / 14 links live, 33 tools / 112 links cut** (see section 1).
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but `ee23dd004c` at the apply.

## 0a. What changed since the first pair (VOID)

- The first attempt deployed `d020bee315`, read `r13.AC2` FAIL and rolled back to `ee23dd004c` (verified; `0.7.0_AE_CloudOps~MI` msg 34382). Both causes were the issuer's and are fixed (MX-r-13 A5): the index instrument accepts the per-link depth claim (`fd29457109`), and the catalog's definition lines come from the shipped source.
- This cut differs from the first by the catalog blob only (`11620b3c52` -> `e5096b5d6c`, 4 lines); the discover blob `f3cf344cc3` is unchanged. On an extract of the first cut with the new catalog: a=11 valid 11, b=70, c=12, sum 93 of N=93, definitions 93 of 93, discover 3 of 3; `r13.AC3` PASS.
- The rollback artifact's size and ETag changed (the rollback re-uploaded it): see section 0.
- The link-count difference stays EXPECTED at 33 tools / 112 links (per-tool lines identical to the first attempt).

## 1. The issuer's ruling on the link-count difference (MX-r-12 A1 and A5)

- **Cause:** the reader (`admin_gateway_breakdown.py`, the same blob `b10782ca26` on both sides) did not change; the catalog did. 22 tools gain a catalog link (10 `harvest_*`, 4 `news_*`, 8 `portal_get_*`) because 78 harvest rows and 19 table rows now name a live `read_tool`. The one count that changed on an existing tool is `etfs_get_positioning` 1 -> 2. Nothing is removed.
- **It is the release's intent, not drift,** and it widens no access: a link in that count is a catalog row naming a tool the gateway already serves; no tool, grant, key or integration id is added.
- **MP-z-6 is staged and not started** (`NFRA_MCPORTAL.TO-MP-z-6`, status staged; Andrew has not read the page in a window it must grade). MX-r-12 A1's condition ("closed or not yet started") holds, so the slot is not blocked. `2.0.0_SA_COO~MP` is told that the counts change to 33 / 112 at this release, so that the run reads the post-release page.
- **So** the link-count census is graded EXPECTED at 33 tools / 112 links on the cut and on the host after the apply; any other value is a difference and VOIDs both halves.

## 2. The act (applier `0.7.0_AE_CloudOps~MI`)

1. Re-read the host and plane 1 (live ref by hash). Open the NEVER-2 ledger `nfra-mcpindex-r12-catalog-release-v2`, with entry and sentinel committed (the slug r13.AC1 grades; the first attempt's ledger closed ROLLED-BACK).
2. Bun-lock pre-check at mcportal pin `17dcbb28`. Halt gate through the wrapper from `C:/tmp/mx-dep-r13v2`: rc=0, `HALT_OVERRIDE` never set; Rule 18a broker read; the `address()` oracle from the deploy tree.
3. Deploy `1b18b94979` with the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF=ee23dd004c985c46d479908db46d2ad9b4f3b1c8`.
4. Before the first leg closes, read back the label: `opal-gateway-1b18b94979.tar.gz` present, `-latest`'s `git-ref` `1b18b94979`, the rollback key's ETag still `3cd90347...`.
5. Read back: `/health` 200; the host byte census against the cut; the censuses again (tools 93, `.env` 57, integrations 7, link counts 33 / 112); then `r13.AC1` to `r13.AC4` verbatim.
6. Record `deployed_commit` `1b18b94979` and `previous_deployed_commit` `ee23dd004c` with a `release_note` naming THIS release (one write). Close the ledger. Re-write the proof instance. Report the close by 13:00Z (before the ~13:30Z daily publish).

## 3. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 2 files: `app/refs/DATA_CATALOG.yaml` (+19882/-627) and `app/integrations/opal_discover/integration.py` (+69/-21); no other file | redeploy the VERSIONED artifact `opal-gateway-ee23dd004c.tar.gz` |
| `.env`, integrations, served tools | none (equal: 57, 7, 93) | n/a |
| MC Portal per-tool links | 11 / 14 -> 33 / 112, a count of catalog rows, no new tool or reader | follows the catalog on rollback |
| S3 artifacts | `opal-gateway-1b18b94979.tar.gz` new; `-latest` re-pointed | the rollback re-points `-latest` at `ee23dd004c` |
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
- deploy-only commit `1b18b94979`;
- the rollback artifact `opal-gateway-ee23dd004c.tar.gz` (629,787 B, ETag `3cd90347...`);
- live base `ee23dd004c` on planes 1 and 2.

It covers both branches of every leg, and the link-count difference of section 1 as EXPECTED (33 tools / 112 links).

It is VOID on any of these:
- a moved base;
- a changed pin;
- a `deploy-to-ec2.sh` other than the base's;
- any new tool, key or integration id;
- any file beyond the 2;
- any census difference other than the link counts at 33 / 112.
