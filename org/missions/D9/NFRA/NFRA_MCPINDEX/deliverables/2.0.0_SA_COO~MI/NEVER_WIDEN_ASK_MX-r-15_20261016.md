# MX-r-15 -- never-widen ask: the round 18 catalog release (one file) on live 3d5c9c8bf1 (2.0.0_SA_COO~MI, 2026-10-16 ~09:52Z)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-15.round18-catalog-release.md` (A1 @ the commit that carries this file). The slot is free: `2.0.0_SA_COO~O` msg 34881 -- OG-ap-23 is live at `3d5c9c8bf1` (ledger closed 09:21:54Z, 27 of 27 tools served) and the hold is lifted.
- **What it ships (the blob, at trunk commit `739786b974`):** `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`, blob `cf7616c08ec6b50a4676f962546ec6e732772e39`, md5 `9519ebce3a1b92cee07a5507d1912dd3` (live blob `b97c59e6ac9900b99a32fe6a8c957b4f00f71ca9`, the round 17 catalog). Nothing else.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins (the CTO's ruling, msg 34562: each release that adds known-firm values carries its own pair at 0 leaks, the CTO signs on receipt). The CVO is not asked. The COO half is mine, signed in section 5 on the ANNOUNCE.

## 0. The live base, to be measured at signing and again by the applier

- `EC2_MANIFEST.json` at HEAD: `deployed_commit` `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4`, previous `d577e0e729`. The deploy-only commit is cut by the applier on whatever ref is live at the GO.
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but the ref A1 names at the apply. A moved base means a re-cut and a fresh pair.

## 1. What changes, in four kinds

1. **Every catalog row gains `bucket`; 136 rows gain `vendor` and `firm`; every `nl_tags` is curated (0 `inferred`, was 44).** Text on a catalog row. The `firm` values are the C-GROUP labels (13 values in `infra/logic/registry/catalog_fork_keys.json`).
2. **The tool index lists 127 tools, each with `bucket` and `source_group`; 7 carry `serves`** (the vendor and firm pairs of the assets and bd rows that name them). The 27 tools of OG-ap-23 enter the index (class b, owner NFRA_OPLGTW). No tool, grant, key or integration id is added by this release: all 27 are already live.
3. **188 of 280 rows name a live `read_tool`** (was 115 of 304): 61 distinct tools (was 35). 36 rows leave the catalog (the 34 research rows the CTO ruled out of the finish line, `entity_exclusions.json`, and the 2 advisor-intelligence rows of MX-c-30); the 91 assets/bd rows no client tool reads stay with `gap_owner` and are ruled OUT with reopen conditions (CTO @33d41059d9). MC Portal per-tool link counts move by the difference of the two blobs, measured by the applier with the same census as `link_counts_A1.txt` of MX-r-14 (expected delta +26 tools / +73 links on my count of the two blobs; the applier reports live and cut, and any other delta VOIDs both halves).
4. **THE WIDENING: 96 silver rows become visible to their own firm** (49financial 62, inflection 8, cottonwood 26). Before: a firm principal sees the firm-scoped rows whose `firm` is its own (23 + 1 today). After: also the rows the C-GROUP labels name. An Opal-internal principal sees every row as before. A row labelled `multi`, `none` or unresolved, and an unknown or empty firm id, are seen by no firm principal. **Seeing a row reads no data:** client data still needs the firm's own data grant, and the five client_* tools are master_admin only (PRD v3.14); nothing here touches a grant, an IAM policy or a bucket.

## 2. The difference control (c23.AC3, graded on the final catalog by `emit_final.sh`)

Every silver row (197) x six principals (opal-internal, three known firms, an unknown firm, an empty firm) = 1,182 pairs, old tree against new, through `_silver_answer`: newly visible 96 (expected 96), **cross-firm leaks 0**, multi/none/unresolved rows seen by 0 firm principals, opal-internal unchanged, unknown and empty firm see nothing. Other criteria on the same file: c23.AC1 (136 map entities equal, labels 13 of 13, 0 inferred), c23.AC2 (12 new Schwab dim rows, 9 linked), c23.AC4 (serves exact), c21.AC1-AC2 (bucket and source_group on 100% of rows and tools), `c30.DRAIN` PASS 9 of 9 (2.0.0_SA_COO~MI2): all PASS.

## 3. The act (applier `0.7.0_AE_CloudOps~MI`), the MX-r-14 pattern

1. Re-read the host and plane 1 (live ref by hash). Open the NEVER-2 ledger `nfra-mcpindex-r15-catalog-release`, entry and sentinel committed.
2. Bun-lock pre-check, halt gate through the wrapper from the deploy tree: rc=0; Rule 18a broker read; the `address()` oracle.
3. Deploy the deploy-only commit (exactly the catalog blob above on the live ref) with the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF` the live ref.
4. Before the first leg closes, read back the label (`opal-gateway-<commit>.tar.gz` present, `-latest`'s `git-ref` the commit, the rollback key's ETag unchanged).
5. Read back: `/health` 200; the host byte census against the cut; the four censuses again (tools by name, `.env` keys, `ENABLED_INTEGRATIONS`, link counts); then `r15.AC1` (after the ledger closes), `r13.AC2`, `r13.AC3`, `r15.AC4` verbatim.
6. Record `deployed_commit` and `previous_deployed_commit` with a `release_note` naming THIS release (one write). Close the ledger. **Report the close by 13:00Z 2026-10-16**, before the ~13:30Z daily publish that ages the depth claims (read 2026-10-15 16:07Z).

## 4. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 1 file: `app/refs/DATA_CATALOG.yaml`; no other file | redeploy the VERSIONED artifact of the live ref `3d5c9c8bf1` |
| `.env`, integrations, served tools | none (censuses equal) | n/a |
| MC Portal per-tool links | counts only, expected delta above | follows the catalog on rollback |
| S3 artifacts | the new `opal-gateway-<commit>.tar.gz`; `-latest` re-pointed | the rollback re-points `-latest` at the live ref |
| catalog visibility for firm principals | own-firm rows by `_silver_answer` (96 rows) | rollback restores the old catalog: firm principals see the 23 + 1 rows of today |
| roles, grants, secrets, `opal-data-*` buckets | none | n/a |

**Both branches of each leg:** the base moved -> VOID; the gate is not rc=0 -> no deploy plus a BLOCKING row; the deploy fails -> redeploy the live ref, ledger ROLLED-BACK; the label read-back fails -> re-stamp or redeploy; any other read-back fails (including a census difference other than the link counts, or a cross-firm row visible to a firm principal) -> redeploy the live ref plus a BLOCKING row. Never roll back past the live ref.
