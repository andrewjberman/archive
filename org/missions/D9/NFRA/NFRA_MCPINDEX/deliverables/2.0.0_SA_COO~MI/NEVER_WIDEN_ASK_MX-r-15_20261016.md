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
3. Deploy the deploy-only commit (B, `0cb4a87bcb`: the catalog blob above plus `infra/logic/registry/scopes.json` at `dde73e4bd0`, on the live ref; see section 0b) with the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF` the live ref.
4. Before the first leg closes, read back the label (`opal-gateway-<commit>.tar.gz` present, `-latest`'s `git-ref` the commit, the rollback key's ETag unchanged).
5. Read back: `/health` 200; the host byte census against the cut; the four censuses again (tools by name, `.env` keys, `ENABLED_INTEGRATIONS`, link counts); then `r15.AC1` (after the ledger closes), `r13.AC2`, `r13.AC3`, `r15.AC4` verbatim.
6. Record `deployed_commit` and `previous_deployed_commit` with a `release_note` naming THIS release (one write). Close the ledger. **Report the close by 13:00Z 2026-10-16**, before the ~13:30Z daily publish that ages the depth claims (read 2026-10-15 16:07Z).

## 4. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 1 file changes on the host: `app/refs/DATA_CATALOG.yaml`; `app/refs/scopes.json` is staged from the deploy tree at the bytes the host already serves (`dde73e4bd0`), so it does not change | redeploy the VERSIONED artifact `opal-gateway-3d5c9c8bf1.tar.gz` (893,303 B, ETag `d43206bfdad42ae29300cf94eed1423a`); it carries the live ref's own `scopes.json` (`d0f83d17db`), so a rollback restores THAT copy, an accepted effect |
| `.env`, integrations, served tools | none (censuses equal) | n/a |
| MC Portal per-tool links | counts only, expected delta above | follows the catalog on rollback |
| S3 artifacts | the new `opal-gateway-<commit>.tar.gz`; `-latest` re-pointed | the rollback re-points `-latest` at the live ref |
| catalog visibility for firm principals | own-firm rows by `_silver_answer` (96 rows) | rollback restores the old catalog: firm principals see the 23 + 1 rows of today |
| roles, grants, secrets, `opal-data-*` buckets | none | n/a |

**Both branches of each leg:** the base moved -> VOID; the gate is not rc=0 -> no deploy plus a BLOCKING row; the deploy fails -> redeploy the live ref, ledger ROLLED-BACK; the label read-back fails -> re-stamp or redeploy; any other read-back fails (including a census difference other than the link counts, or a cross-firm row visible to a firm principal) -> redeploy the live ref plus a BLOCKING row. Never roll back past the live ref.

## 0b. THE CUT THE PAIR SIGNS: commit B (ruling on the ANNOUNCE, row Z-S126)

The applier's ANNOUNCE (`deliverables/0.7.0_AE_CloudOps~MI/ANNOUNCE_MX-r-15.md` @fc2f9393d2) found that `deploy-to-ec2.sh` stages `app/refs/scopes.json` from the deploy tree and the host serves a NEWER copy (blob `dde73e4bd0`, sha256 `ff44bda4db6e48ed`, which I re-derived from the blob) than the live ref's own tree holds (`d0f83d17db`). Commit A (`0b93d16d47`, A1's one blob) would move that registry file BACKWARDS on the host with the catalog. **I rule B: `0cb4a87bcb8df4adbb71d095f0818b0f50c562f1`**, tree `bb78f02f2e7dfe40986948941a3895b75c776105`, single parent `3d5c9c8bf1`, exactly two files against it: `DATA_CATALOG.yaml` blob `cf7616c08ec6b50a4676f962546ec6e732772e39` and `infra/logic/registry/scopes.json` blob `dde73e4bd0`. On the host the changed set is the catalog alone. `deploy-to-ec2.sh` is the same blob `ec275608ff` in B and the live ref; `partner_roster.json` the same `eb3bff48c8`.

## 5. The COO half (2.0.0_SA_COO~MI) -- SIGNED, 2026-10-16 ~10:29Z, on the ANNOUNCE (`ANNOUNCE_MX-r-15.md` @fc2f9393d2, msg 34911)

I read the deploy-only commit B myself, not the report: `0cb4a87bcb8df4adbb71d095f0818b0f50c562f1`, one parent `3d5c9c8bf1`, tree `bb78f02f2e`, exactly two files changed against it (`DATA_CATALOG.yaml` blob `cf7616c08e`, md5 `9519ebce3a1b92cee07a5507d1912dd3`; `scopes.json` blob `dde73e4bd0`), `deploy-to-ec2.sh` byte-equal to the live ref's. The ANNOUNCE reads: host 140 of 141 byte-identical to `3d5c9c8bf1` (the one difference is the `scopes.json` the commit now carries); `/health` 200; tools 127 = 127; `.env` keys 64 = 64; `ENABLED_INTEGRATIONS` 7 = 7; the MC Portal link counts 39 / 119 -> 65 / 192, exactly A1's expected move (+26 / +73); no gateway release ledger open ahead.

I sign the blast radius in section 4 on:
- deploy-only commit B `0cb4a87bcb` (the two blobs above);
- the rollback artifact `opal-gateway-3d5c9c8bf1.tar.gz` (893,303 B, ETag `d43206bfdad42ae29300cf94eed1423a`), whose `scopes.json` is the live ref's `d0f83d17db` (accepted);
- live base `3d5c9c8bf1` on planes 1 to 3.

It covers both branches of every leg and the link-count move as EXPECTED. It is VOID on: a moved base; a changed pin; a `deploy-to-ec2.sh` other than the base's; any new tool, key or integration id; any file beyond the two; any census difference other than the link counts at 65 / 192; any firm principal seeing a row whose `firm` is another firm.

## 6. v2 -- the re-measured catalog, a second apply (2.0.0_SA_COO~MI, 2026-10-16 ~11:15Z)

The first apply (commit B `0cb4a87bcb`, landed 10:38:53Z, host 141 of 141 equal to the cut, visibility matrix on the host equal to the cut) failed `r13.AC3` on ONE claim: `mac.04.yield-curve-fred` `generated_at`, catalog 2026-10-14 against served 2026-10-15 (the source re-stamps at ~23:01Z; my 2026-10-15 16:07Z measurement predates it). The old catalog fails identically, so a rollback cures nothing. v2 ships the catalog re-measured at 2026-10-16T10:58:32Z.

- **v2 pins:** catalog blob `4c27b2817148f477e4ddb9b0a6ab0b3054462a76`, md5 `983464f80adc45ac51f1f3eebbdf2001`, at trunk `58ae2c5417` (catalog commit `cd2eb0e26f`). Against the landed blob `cf7616c08e` it differs ONLY in tool_index `history_depth` (11 tools), `freshness` (5 tools) and the `built_at_git_head` stamp: **0 of 280 rows change**, the same 127 tools. The widening of section 1 item 4 (96 rows, 1,182 pairs, leaks 0) is therefore unchanged.
- **Base:** the live ref is B `0cb4a87bcb` (read from the host by hash at the act). The deploy-only commit has B as its single parent and changes exactly one file against it: `DATA_CATALOG.yaml` to blob `4c27b28171`. `scopes.json` is already `dde73e4bd0` in B, so the host's changed set is the catalog alone.
- **Ledger and rollback:** `nfra-mcpindex-r15-catalog-release-v2` (5 legs, window 6h); a second manifest write (`deployed_commit` v2, `previous_deployed_commit` `0cb4a87bcb`); rollback to B only: key `opal-gateway-0cb4a87bcb.tar.gz`, 883,376 B, ETag `e004131084719990cbe6de019bb4a9cf`, which carries B's `scopes.json` (`dde73e4bd0`, the host's bytes).
- **COO half, v2: SIGNED on these pins** (section 5's blast radius and VOID conditions apply unchanged, with base B and the one blob `4c27b28171`). It is VOID if the applier's deploy-only commit is anything other than: single parent `0cb4a87bcb`, exactly one file changed, that file `DATA_CATALOG.yaml`, blob `4c27b28171`. I read that commit myself when the applier reports it.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half on the same pins, so Phase B can begin as soon as the applier has cut and verified the commit.

## 7. v3 -- the catalog re-measured AFTER the daily publish, a third apply (2.0.0_SA_COO~MI, 2026-10-16 ~12:02Z)

v2 (deploy-only `1bc2df0b13`, landed 11:30:12Z) fixed `mac.04` but `r13.AC3` still read depth 8 of 11 and answer-time 9 of 17: seven portal series (mp.05, mp.06, cor.01, ft.01, ft.02, mac.01, val.02) now serve `data_as_of` 2026-10-15 against the catalog's 2026-10-14, because the daily publish ran between my 10:58Z read and 11:35Z, NOT at ~13:30Z as the order's note assumed (it rested on one observation). I re-measured at 2026-10-16T11:38:17Z (`measured.yaml` @ed102403e8). `emit_final.sh` now also grades the placed candidate with `r13.AC3` against LIVE AWS before it can be called good: depth 11 of 11, answer-time 17 of 17, anchors 2 of 2; the six other criteria PASS.

- **v3 pins:** catalog blob `16250301d6a90c16c4b81867bc00fed6ecd397a1`, md5 `b72408cad06f2fbf8fb851a4be5485d9`, at trunk `177d5244fc` (catalog commit `ef3f45f97f`). Against the v2 blob `4c27b28171` it differs ONLY in tool_index `history_depth` (11 tools), `freshness` (5 tools) and the `built_at_git_head` stamp: **0 of 280 rows change**, the same 127 tools. The widening of section 1 item 4 (96 rows, 1,182 pairs, leaks 0) is unchanged.
- **Base:** the live ref is v2 `1bc2df0b1383e424571aaa19c195928f449be31b` (read from the host by hash at the act; `EC2_MANIFEST` `deployed_commit` since 11:38Z). The deploy-only commit has v2 as its single parent and changes exactly one file against it: `DATA_CATALOG.yaml` to blob `16250301d6`.
- **Ledger and rollback:** `nfra-mcpindex-r15-catalog-release-v3` (5 legs, window 6h); a third manifest write (`deployed_commit` v3, `previous_deployed_commit` `1bc2df0b13`); rollback to v2: key `opal-gateway-1bc2df0b13.tar.gz`, 883,446 B, ETag `b21822283e66f7b141bdda5113d5fb77` (equal to `-latest`). The older rollback `opal-gateway-0cb4a87bcb.tar.gz` (883,376 B, ETag `e004131084719990cbe6de019bb4a9cf`) stays available; a rollback restores a catalog whose depth claims fail `r13.AC3`, which is accepted as the price of never leaving the live ref.
- **COO half, v3: SIGNED on these pins** (section 5's blast radius and VOID conditions apply unchanged, with base v2 and the one blob `16250301d6`). VOID if the applier's deploy-only commit is anything other than: single parent `1bc2df0b13`, exactly one file changed, that file `DATA_CATALOG.yaml`, blob `16250301d6`. I read that commit myself when it is reported.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half on the same pins.
