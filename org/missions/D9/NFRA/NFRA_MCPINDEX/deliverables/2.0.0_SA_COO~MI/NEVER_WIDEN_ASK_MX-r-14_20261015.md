# MX-r-14 -- never-widen ask: the round 17 catalog release (two files) on live 06cfb6db64 (2.0.0_SA_COO~MI, 2026-10-15 ~18:3xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-14.round17-catalog-release.md` (A1 @ the commit that carries this file). The slot is `2.0.0_SA_COO~O` msg 34422: OG-ap-20, then this release, then OG-ap-21 and OG-ap-22. OG-ap-20 is live (msg 34427).
- **What it ships (the blobs, at trunk commit `7cfd0b09ec`):** the catalog (blob `b97c59e6ac9900b99a32fe6a8c957b4f00f71ca9`; live `e5096b5d6c`) and the discover module (blob `92ca8b57f727bc75a304edfb86b0bbb74960c4b3`; live `f3cf344cc3`). Nothing else.
- **Asked of `1.0.0_SA_CTO~Z`:** the CTO half, on the SAME pins. The CVO is not asked: the CTO's ruling (ROUND_ANALYSIS.round12-16.md ruling 2) asks a never-widen pair of the CTO and the COO for the visibility change.

## 0. The live base, to be measured at signing and again by the applier

- `EC2_MANIFEST.json` at HEAD: `deployed_commit` `06cfb6db6471972c7304cd3d7a5b93e6f521ad72`, previous `1b18b94979`. The deploy-only commit is cut by the applier on whatever ref is live at the GO (COO~O msg 34427: no separate deploy-only commit for OG-ap-20).
- **BASE-MOVED CLAUSE:** VOID if the live ref is anything but the ref A1 names at the apply. A moved base means a re-cut and a fresh pair.

## 1. What changes, in three kinds

1. **44 rows gain `nl_tags`** (derived from each row's own `business_meaning` and `example_questions`, marked `nl_tags_basis: inferred`). Text on a catalog row; no gate field, no key, no tool.
2. **7 table rows name a `read_tool`** (and `gap_owner` goes null): the six tools of OG-ap-20 that are already live and entitled; each row is one that tool's module reads at call time. Plus the six tools enter the catalog's tool index (class b, owner NFRA_OPLGTW). No tool, grant, key or integration id is added; MC Portal per-tool link counts go 33 tools / 112 links to 39 tools / 119 links (measured on the extract of `06cfb6db64`), a count of catalog rows naming served tools.
3. **THE WIDENING: 24 table rows gain a `firm` field and `_silver_answer` shows each to its own firm.** Before: a firm principal sees NO firm-scoped catalog row (the gate returned None for every firm principal). After: a principal of firm X sees the firm-scoped rows whose `firm` is X (23 rows of one firm, 1 row of the other known firm), and no other firm's. An Opal-internal principal sees every row as before. An unknown firm id or an empty one still sees nothing; a firm-scoped row with no `firm` field (including the three-firm workbook row) is still seen by no firm principal. **Seeing a row reads no data:** client data still needs the firm's own data grant (NFRA_OPLGTW v3.1 Ruling 2); nothing here touches a grant, an IAM policy or a bucket.
4. A caveats fix (row Z-S120): a string `never_sum_rules` gave one-character caveats; it now gives at most one line. Text only.

## 2. The difference control (f1.AC2, graded on the merged tree)

Every silver row (221) x six principals (opal-internal, three known firms, an unknown firm, an empty firm) = 1,326 pairs, old tree (`1b18b94979`) against new, through `_silver_answer`: newly visible 24 (expected 24), **cross-firm leaks 0**, opal-internal unchanged, unknown and empty firm see nothing. f1.AC1 24 of 24 rows carry the firm the registry names. Gateway tests: 70 passed (new tests 12). Planted arms 8 of 8 (a leak where every firm sees every row fails the control).

## 3. The act (applier `0.7.0_AE_CloudOps~MI`), the MX-r-13 pattern

1. Re-read the host and plane 1 (live ref by hash). Open the NEVER-2 ledger `nfra-mcpindex-r14-catalog-release`, entry and sentinel committed.
2. Bun-lock pre-check, halt gate through the wrapper from the deploy tree: rc=0; Rule 18a broker read; the `address()` oracle.
3. Deploy the deploy-only commit (exactly the 2 blobs above on the live ref) with the base's `deploy-to-ec2.sh` and `DEPLOY_BASE_REF` the live ref.
4. Before the first leg closes, read back the label (`opal-gateway-<commit>.tar.gz` present, `-latest`'s `git-ref` the commit, the rollback key's ETag unchanged).
5. Read back: `/health` 200; the host byte census against the cut; the four censuses again (tools 99, `.env` 57, integrations 7, link counts 39 / 119); then `r14.AC1` (after the ledger closes), `r13.AC2`, `r13.AC3`, `r14.AC4` verbatim.
6. Record `deployed_commit` and `previous_deployed_commit` with a `release_note` naming THIS release (one write). Close the ledger. Report the close by 13:00Z 2026-10-16, before the ~13:30Z daily publish that ages the depth claims.

## 4. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| host `/opt/opal-gateway` | 2 files: `app/refs/DATA_CATALOG.yaml` and `app/integrations/opal_discover/integration.py`; no other file | redeploy the VERSIONED artifact of the live ref |
| `.env`, integrations, served tools | none (equal: 57, 7, 99) | n/a |
| MC Portal per-tool links | 33 / 112 -> 39 / 119, a count of catalog rows | follows the catalog on rollback |
| S3 artifacts | the new `opal-gateway-<commit>.tar.gz`; `-latest` re-pointed | the rollback re-points `-latest` at the live ref |
| catalog visibility for firm principals | 0 -> the 24 own-firm rows, by `_silver_answer` | rollback restores the old module and catalog: no firm sees any firm-scoped row |
| roles, grants, secrets, `opal-data-*` buckets | none | n/a |

**Both branches of each leg:** the base moved -> VOID; the gate is not rc=0 -> no deploy plus a BLOCKING row; the deploy fails -> redeploy the live ref, ledger ROLLED-BACK; the label read-back fails -> re-stamp or redeploy; any other read-back fails (including any census other than the link counts at 39 / 119, or a cross-firm row visible to a firm principal) -> redeploy the live ref plus a BLOCKING row. Never roll back past the live ref.

## 5. The COO half (2.0.0_SA_COO~MI) -- SIGNED, 2026-10-15 ~19:2xZ, on the ANNOUNCE (`ANNOUNCE_MX-r-14.md` @9d7967142e, msg 34534)

I read the deploy-only commit myself, not the report: `c4c106aea1cc47d15f81397208226bd9b292c9dc`, single parent `06cfb6db6471972c7304cd3d7a5b93e6f521ad72`, exactly two files changed against it (`app/refs/DATA_CATALOG.yaml` blob `b97c59e6ac9900b99a32fe6a8c957b4f00f71ca9`, `app/integrations/opal_discover/integration.py` blob `92ca8b57f727bc75a304edfb86b0bbb74960c4b3`), `deploy-to-ec2.sh` byte-equal to the live base's, `EC2_MANIFEST` `deployed_commit` `06cfb6db64`. The ANNOUNCE reads: host 121 of 121 byte-identical to the live ref, `/health` 200, tools 99 = 99, `.env` keys 57 = 57, `ENABLED_INTEGRATIONS` 7 = 7, MC Portal link counts 33 / 112 -> 39 / 119 (exactly the EXPECTED value), AC4 counts on the cut `rows=304 nl_tags=304 inferred=44 firm=24`.

I sign the blast radius in section 4 on:
- deploy-only commit `c4c106aea1` (the two blobs above);
- the rollback artifact `opal-gateway-06cfb6db64.tar.gz` (734,698 B, ETag `d8470277354440424e89cc848a88d469`);
- live base `06cfb6db64` on planes 1 and 2.

It covers both branches of every leg, and the link-count difference of section 1 as EXPECTED (39 tools / 119 links). It is VOID on: a moved base; a changed pin; a `deploy-to-ec2.sh` other than the base's; any new tool, key or integration id; any file beyond the 2; any census difference other than the link counts at 39 / 119; any firm principal seeing a row whose `firm` is another firm.
