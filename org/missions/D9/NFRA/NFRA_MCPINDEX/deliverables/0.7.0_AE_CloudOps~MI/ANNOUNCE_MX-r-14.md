# ANNOUNCE -- MX-r-14 PHASE A: the round 17 catalog + discover, two blobs cut on live `06cfb6db64`

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-14.round17-catalog-release.md` at **A1** (GO msg 34527).
Probes: `deliverables/0.7.0_AE_CloudOps~MI/probes_r14/` (every file named below is there).

**STATE: PHASE A ONLY.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no push.
AWS contact, all read-only and Opal's own: S3 `head-object` (5 keys) and one SSM `AWS-RunShellScript` read (file hashes,
`.env` KEY NAMES parsed in Python, `/health`). No `.env` value was read or printed. No source file was edited.

## 0. THE ONE CENSUS THAT MOVES -- the MC Portal link counts, at exactly the expected value

| | tools | links |
|---|---|---|
| LIVE `06cfb6db64` | 33 | 112 |
| CUT `c4c106aea1` | **39** | **119** |

**VERDICT: `per_tool_link_counts DIFFER`, and the value is the one A1 names: 33 / 112 -> 39 / 119.** Tools added 6
(`etfs_get_fund_holdings`, `etfs_get_fund_nav_history`, `etfs_get_monthly_report`, `etfs_get_ownership_rollup`,
`etfs_get_partner_ownership`, `mdpf_get_category_views`); tools removed none; no existing tool's count changed (7 links added over
the 6 tools). `admin_gateway_breakdown.py` is the SAME blob `b10782ca26` on both sides, so the catalog is the cause. Each
side is read by its OWN reader against its OWN catalog (`link_counts_A1.txt`); the host's real installed reader read
`33 / 112` on the live side at the close of the last release, and the same off-host mechanism is used here.

## 1. WHAT THIS RELEASE IS -- exactly 2 files, at trunk `7cfd0b09ec`

| file (under `infra/aws/ec2/opal-gateway/`) | live blob (`06cfb6db64`) | shipped blob | lines +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `e5096b5d6c` | **`b97c59e6ac9900b99a32fe6a8c957b4f00f71ca9`** | +597 / -268 |
| `app/integrations/opal_discover/integration.py` | `f3cf344cc3` | **`92ca8b57f727bc75a304edfb86b0bbb74960c4b3`** | +20 / -7 |

Each shipped blob was **resolved from `7cfd0b09ec` with `git rev-parse`, never typed**, and equals the blob A1 names. Both are
also equal at `box/sitez` HEAD, and `7cfd0b09ec` is an ancestor of it. Files outside `infra/aws/ec2/opal-gateway/`: **0**.

**The r14.AC4 counts, read on the CUT catalog with the same script the host will run (`ac4_counts_cut_vs_live_r14.txt`):**
`version=0.5 harvest=78 table=216 key_template=216 retired=5 rows=304 nl_tags=304 inferred=44 firm=24`, md5
`49b7a6e9656ddfe753e156f6df347b8c`. The same script on the LIVE catalog reads `nl_tags=260 inferred=0 firm=0`, so the three
round-17 fields (44 inferred tags, 24 firm-scoped rows, 304 rows with tags) are the delta, and the counts the order's
criterion expects are met by the cut. The cut names 35 distinct `read_tool`s and the cut's 99-tool census serves all of them
(not served: none).

## 2. THE LIVE REF, READ FROM THE HOST BY HASH

| plane | read | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the tree at `06cfb6db64`** (sha256 per file, SSM `e9ce5a28-aa03-4611-8138-a2cb48d86dfb`, 2026-10-15T18:37:54Z; `host_read_r14_PRECUT.txt`, `live_ref_by_hash_PRECUT.txt`) | 121 files, host non-dashboard 121, common 121, **byte-identical 121, DIFFER 0, cut-only 0, host-only 0** | **the host IS running `06cfb6db64`** |
| 2. S3 `-latest` | 734,698 B, ETag `d8470277354440424e89cc848a88d469`, LastModified 10:49:08Z | `git-ref` `06cfb6db6471972c7304cd3d7a5b93e6f521ad72` |
| 3. `EC2_MANIFEST.json` at `box/sitez` HEAD | `deployed_commit` `06cfb6db6471972c7304cd3d7a5b93e6f521ad72` | AGREES |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 57 `.env` keys |

Pre-apply, the host against the cut reads DIFFER 2 = exactly the two files, EXPECTED CHANGED SET MATCH
(`host_vs_cut_r14_PRECUT.txt`), the mirror image of the post-apply reading that PHASE B will take.

## 3. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`06cfb6db6471972c7304cd3d7a5b93e6f521ad72`** (per A1, the release commit is itself the deployed one; there is no separate deploy-only commit beneath it) |
| **DEPLOY-ONLY COMMIT** | **`c4c106aea1cc47d15f81397208226bd9b292c9dc`** (single parent = the base; `git commit-tree` on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override) |
| deploy-only tree | `733e63f1d7765dc1136564a0ef786170f71bb155` |
| deploy tree | `C:/tmp/mx-dep-r14` -- **NEW**, sparse, detached, never merged, never pushed, `worktree lock`ed |
| cone | `.tools`, `data/transcripts/scripts/teams`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`**, `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps` |
| **deploy tree HEAD IS the deploy-only commit** | **YES**; the two working files' `hash-object` equal the two shipped blobs exactly; `git status --porcelain` = **0 lines**; the `address()` oracle resolves from this tree; the closure files are present |
| `deploy-to-ec2.sh` in the cut | `4257417f96b5b8445af7cdc2f80ff70349dba51d`, **byte-equal to the live base's** |
| artifact keys the apply will write | `opal-gateway-c4c106aea1.tar.gz` and `-latest`. The versioned key is **404 today**, as it must be |
| **ROLLBACK ARTIFACT (versioned key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-06cfb6db64.tar.gz`: **734,698 B, ETag `d8470277354440424e89cc848a88d469`, `git-ref` `06cfb6db64...`**, LastModified 10:49:06Z. Its size and ETag EQUAL `-latest`'s, so the handle is real and is what is serving (`rollback_and_target_keys_r14.txt`) |
| mcportal pin the dashboard build resolves | `17dcbb28624eab147318052f58bcc39b8eb8029c` (`MCPORTAL_RESOLVE_ONLY=1` from the cut tree, rc 0), unmoved since MX-r-13. The bun-lock pre-check is a PHASE B step |
| Terraform | none |

The rollback key is NOT the one MX-r-13 left: that release's rollback key was `opal-gateway-ee23dd004c`. The pair must name
`opal-gateway-06cfb6db64.tar.gz` at the size and ETag above.

## 4. THE CENSUS -- exactly 2 files differ from the live ref

`git diff 06cfb6db64 c4c106aea1`: **2** files, both the named ones; parent count **1**, and the parent IS `06cfb6db64`.
The cut is a SINGLE-BLOB-SET OVERLAY on the live ref's tree (temporary `GIT_INDEX_FILE` seeded from `06cfb6db64`, two
`update-index --cacheinfo`, `write-tree`, `commit-tree`), so nothing else in the worktree can ship.

## 5. THE FOUR CENSUSES (before = the live tree / the live host, after = the cut)

| census | before | after | verdict |
|---|---|---|---|
| **tools by name**, in-process (`MOCK_GRAPH=1`, the 7 live ids; `tools_census_r14.txt`) | native 75, integration 24, total **99** | native 75, integration 24, total **99** | added `[]` / removed `[]`, **EQUAL**; dropping one name (`blackdiamond_list_fees`) reads **False** |
| **`.env` KEY set**, the cut's own `deploy-to-ec2.sh` rendered vs the live host (`env_census_r14.txt`) | host 57 (distinct 57) | rendered 57 (distinct 57) | dropped `[]`, added `[]`, **EQUAL** |
| **`ENABLED_INTEGRATIONS`** | host: `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) | rendered: the same 7 | **EQUAL** |
| **MC Portal per-tool link counts** (`link_counts_A1.txt`) | 33 tools / 112 links | **39 tools / 119 links** | **DIFFER, EXPECTED** at 39 / 119 |

Three of four are equal; the fourth is the ruled expected value.

## 6. THE VISIBILITY CHANGE THE PAIR MUST NAME (order difference 3)

The order says the pair covers a catalog-row visibility change: after this release a principal of firm X sees the 24 table
rows whose `firm` is X and no other firm's. **What I measured is only that the 24 `firm` fields are in the shipped catalog
(`firm=24` above) and that the discover module is the blob A1 names.** I did not run the visibility behaviour: the issuer's
`f1.AC1` to `f1.AC3` (1,326 pairs, 24 newly visible, cross-firm leaks 0) are theirs, and `r14.AC4` grades the catalog
fields, not the principal-scoped view. PHASE B grades `r13.AC2`/`AC3` and `r14.AC4`; none of them exercises a firm
principal against the deployed host. That is a gap in what is verified live, not a defect found.

## 7. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 18 of 18 sentinels** (~19:0xZ; `open_ledgers_r14.txt`): **no gateway-host
release ledger is OPEN or HELD.** `nfra-oplgtw-gateway-release-g5a`, which A1 calls a leg left to close, is not listed, so I
read it as already closed; I did not open it. Listed and not this act: `nfra-mcpindex-r7-bd-doc-retire` (this seat, OPEN by
design, L5 date-gated to 2026-10-19/20); the `nfra-oplgtw-harvest-runner-*` entries (the harvest runner, another host); the
dell/irpt/etfs/mdpf/advi/secclass entries. `nfra-mcpindex-r14-catalog-release`, this release's slug, does not exist yet; it
opens at PHASE B. **The gateway slot is free.**

## 8. TIME, AND NOT PROVED HERE

- Read ~19:05Z. The close is due by 13:00Z tomorrow (the depth claims were read 2026-10-15 16:07Z and hold until the
  ~13:30Z daily publish). OPLGTW's `OG-ap-21` is released on the live ref if this release is not live by 21:00Z tonight; then
  this release re-cuts on its ref. Nothing here needs more than the issuer's reading and the never-widen pair.
- **The served effect:** only the apply shows it. `r13.AC2`, `r13.AC3` and `r14.AC4` are graded after the first leg against
  deployed bytes. `r14.AC1` grades a CLOSED ledger and needs the close committed.
- **Python:** these probes ran under Python 3.14.8 resolved from Git Bash `python` (the CTO's FYI named a 3.11.9 stopgap;
  `python --version` here printed 3.14.8, so the install appears repaired). I did not establish when. The scripts are
  stdlib-only apart from `yaml`, which loaded, and every comparison has its negative control.
- PHASE B, unchanged from MX-r-13 and listed there: host re-read of the live ref by hash (STOP if it moved), bun-lock
  pre-check at `17dcbb28` (both arms), halt-gate pair, Rule 18a broker read, the `address()` oracle, ledger open (entry AND
  sentinel), `DEPLOY_BASE_REF=06cfb6db6471972c7304cd3d7a5b93e6f521ad72 AGENT_NAME=0.7.0_AE_CloudOps~MI bash
  infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from `C:/tmp/mx-dep-r14`, label
  read-back BEFORE the first leg closes, host byte census against the cut (live tree as the negative control), the censuses
  again, `r13.AC2`/`AC3`, `r14.AC4`, then `r14.AC1` after the close, the manifest write (`deployed_commit` `c4c106aea1`,
  `previous_deployed_commit` `06cfb6db64`, a `release_note` naming THIS release, in one write). On any failed read-back,
  roll back to `opal-gateway-06cfb6db64.tar.gz` only.

## 9. ROWS

None filed.
