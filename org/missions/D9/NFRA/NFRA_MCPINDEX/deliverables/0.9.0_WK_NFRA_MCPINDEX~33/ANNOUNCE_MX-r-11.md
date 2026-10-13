# ANNOUNCE -- MX-r-11 PHASE A: the catalog tool-index release, cut on live ref `64b3e54658`

Deployer of PHASE A: `0.9.0_WK_NFRA_MCPINDEX~33` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-11.catalog-tool-index-release.md`, as amended A1-A2.
Pattern: `deliverables/0.7.0_AE_CloudOps~MX/ANNOUNCE_MX-r-10_v2.md`. Probes: `deliverables/0.9.0_WK_NFRA_MCPINDEX~33/probes_r11/`
(every file named below is there).

**STATE: PHASE A only.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no push.
AWS contact, all read-only and Opal's own: S3 `head-object` (3 keys), one `-latest`-equivalent download
(`opal-gateway-64b3e54658.tar.gz`), one SSM `AWS-RunShellScript` read (file hashes, `.env` KEY NAMES parsed in Python,
`/health`). No `.env` value was read or printed. No source file was edited.

## 0. WHAT THIS RELEASE IS -- exactly 2 files, MX-c-8's bytes

| file | live base blob (at 64b3e54658) | shipped blob (MX-c-8, @212f2370a3) | +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `d0bddad2f11ae0983171f82304bb239b842d8298` | `98d15ca9ad038e2e3d8c3f2b0dbf5b365d16fd45` | +773 / -2 |
| `app/integrations/opal_discover/integration.py` | `a8fd2fa900d331121d51ea0f20a5cec4a5ef3dbe` | `021a708e5fd3405c221d0d9afa7249222678fef8` | +57 / -0 |

(Both paths are under `infra/aws/ec2/opal-gateway/`.) Blob identity (`probes_r11/blob_identity.txt`): for each file the
deploy tree's working-file `git hash-object`, the deploy commit's blob and `git rev-parse 212f2370a3:<path>` are all equal
(2 of 2). `git diff --name-status 64b3e54658 HEAD` in the deploy tree: `M` `M`, 2 files; files outside the gateway
dir = 0 (`probes_r11/numstat.txt`). The base blobs are MX-c-7's bytes, shipped by MX-r-10 v2, so the chain is unbroken.
`deploy-to-ec2.sh` in the cut is the live ref's own copy (`cmp` identical to the base; blob `76a4f20a6f`).

**The cut's file list (printed, 2 of 2):**
1. `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`
2. `infra/aws/ec2/opal-gateway/app/integrations/opal_discover/integration.py`

## 1. THE LIVE REF, READ FROM THE HOST BY HASH -- not from `-latest`'s label

| plane | read (UTC) | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the git tree at `64b3e54658`** (sha256 per file, SSM `a59986ac-4f4d-4f52-842b-ebef572407ef`, 21:55:43Z; `host_vs_cut.py`, `live_ref_by_md5_PRECUT.txt`) | cut/tree 107 files, host non-dashboard 107, common 107, **byte-identical 107, DIFFER 0, tree-only 0, host-only 0** | **the host IS running `64b3e54658`**, established without trusting any metadata. (The "MISMATCH" line in that file is the empty expected-set control, as in MX-r-10 v2.) |
| 2. host vs the extracted `opal-gateway-64b3e54658.tar.gz` (`plane2_host_vs_latest_PHASEA.txt`) | artifact 111 files, host 117, common 111, **111 byte-identical, 0 DIFFER, 0 artifact-only**, 6 host-only (all `dashboard/assets/` orphans of older bundles) | agrees |
| 3. S3 `-latest` metadata (`rollback_and_target_keys_PHASEA.txt`) | 551109 B, ETag `527cab0d7d0695c3c6f3c3df902c11df`, LastModified 2026-10-13T21:07:32Z | `git-ref` `64b3e54658060859b81d6bcd48dc7000615f865d` |
| 4. `EC2_MANIFEST.json` plane 2 | on `box/sitez`: `185dc048881d`. On release branch `rel-nfra-mcportal-gw` (4d9261146b): `64b3e54658` | **NOT AGREEING on box/sitez**: MP-z-5's record is not drained. Row `NFRA_MCPINDEX-Z-W33-S6`. The host is the authority, so no pin below rests on this plane |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 54 `.env` keys |

Planes 1-3 name `64b3e54658` (matches the issuer's A2). The 6 host-only dashboard assets are the standing orphans of row
`NFRA_MCPINDEX-Z-S94` (the deploy extracts over the directory and prunes nothing); the difference is one-directional
(artifact is a subset of host, 0 artifact-only), which is the only reason plane 2 is sound as an equality claim.

## 2. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`64b3e54658060859b81d6bcd48dc7000615f865d`** (MP-z-5, `nfra-mcportal-gw-release` CLOSED 21:44:07Z per A2) |
| **DEPLOY-ONLY COMMIT** | **`ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`** (single parent = the base; `git commit-tree` plumbing, author and committer `0.9.0_WK_NFRA_MCPINDEX~33`, no hook, no override) |
| deploy-only tree (repo root) | `f9b34e1b6372d4d6ffb535ba83a84439f253a9dc` |
| deploy tree | `C:/tmp/mx-dep-r11` (NEW; `mx-dep-r10` not reused), sparse cone (`infra/aws/ec2/opal-gateway`, `.tools`, `data/transcripts/scripts/teams`), detached, never merged, never pushed |
| **deploy tree HEAD IS the deploy-only commit** | **YES** -- `git -C C:/tmp/mx-dep-r11 rev-parse HEAD` = `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`; `git status --porcelain` = 0 lines (order item 0 / ruling 2c / row Z-S92) |
| artifact keys the apply will write | `opal-gateway-ad2acc0a93.tar.gz` and `-latest`, both `git-ref` = `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`. The versioned key is **404 today** (absent), as it must be |
| **ROLLBACK ARTIFACT (the VERSIONED key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-64b3e54658.tar.gz`: **551109 B, ETag `527cab0d7d0695c3c6f3c3df902c11df`, `git-ref` `64b3e54658...`**, LastModified 21:07:30Z. Its ETag and size equal `-latest`'s today, so the handle is real. One step back: `opal-gateway-185dc04888.tar.gz` |
| mcportal pin the dashboard build resolves | `0e02a1f1ab56dae65b9df29bd78f1eab319ce6a2` (`MCPORTAL_RESOLVE_ONLY=1` from the deploy tree, rc 0, `mcportal_resolve_only_PHASEA.txt`). MOVED from `bc37107` (MX-r-10) by MP-z-5. The resolve created one temp mcportal worktree under `/tmp` and built nothing. The bun-lock clearance (77 of 77 style precheck) was NOT re-run here: it is PHASE B's pre-apply item, since the pin moved |
| Terraform | none |

## 3. THE CENSUS -- exactly 2 files differ from the host

`probes_r11/host_vs_cut_PHASEA.txt` (host sha256 against the cut's `app/`, `deploy/` and two root files; dashboard excluded):

| | |
|---|---|
| cut files / host non-dashboard files | **107 / 107**, common 107, cut-only 0, host-only 0 |
| byte-identical | **105 of 107** |
| DIFFER | **2: `app/integrations/opal_discover/integration.py`, `app/refs/DATA_CATALOG.yaml`** |
| expected changed set (exactly those 2) | **MATCH** |

The same instrument against the BASE tree read DIFFER 0 over the same 107 (section 1), which is both the live-ref
confirmation and the proof that these 2 files are the entire delta.

## 4. THE THREE EQUAL CENSUSES (before = host now, after = rendered from / run on the cut)

**`ENABLED_INTEGRATIONS`** (ids, not secret; `env_keys_PHASEA.txt`):

| | ids |
|---|---|
| before (host, 21:55:43Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7**) |
| after (rendered from the cut's own `deploy-to-ec2.sh`) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7**) |
| **difference** | **EMPTY** -- `EQUAL`. 7 = 7 |

**`.env` KEY set (keys only, never values):** host **54** keys (54 distinct); rendered from the cut **54** (54 distinct);
**dropped `[]`, added `[]`**. `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS` both present on the host (and
rendered). The 54 is this base's reading, not a pin (MX-r-10 v2 read 53; the delta predates this order, and the rule is
equality before and after). The `printf` line comes from the live ref's own script, which the cut keeps.

**Tool census, in-process (`MOCK_GRAPH=1`, the 7 ids; `tools_delta_PHASEA.txt`):** live = the extracted
`opal-gateway-64b3e54658.tar.gz` (byte-identical to the host), cut = the deploy tree.

| | native | integration | total |
|---|---|---|---|
| live | 43 | 24 | **67** |
| cut | 43 | 24 | **67** |
| added / removed | | | **none / none**, names EQUAL |

67 = 67 (issuer's A2 reading of the host: 67). No widening.

## 5. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 12 of 12 sentinels** (`open_ledgers_PHASEA.txt`; rc 1 because OPEN entries
exist): 5 OPEN lines, none a gateway release. The one for this project is `nfra-mcpindex-r7-bd-doc-retire`
(a bd-doc retire, stranded L5, author `0.7.0_AE_CloudOps~MI`; not this host, not this seat's). `nfra-mcportal-gw-release`
is not in the open set, agreeing with A2's CLOSED 21:44:07Z. `nfra-mcpindex-r10-catalog-release` does not exist yet
(opened at PHASE B start). The gateway slot is free.

## 6. PHASE B -- NOT STARTED; what it does (re-addressed to `0.7.0_AE_CloudOps~MI`)

1. Re-read the live ref from the HOST by md5 (the `host_read.py` + `host_vs_cut.py` pair). If it is not
   `64b3e54658`, STOP: these pins are void and the document is re-cut, not patched (a gateway release by `OG-ap-14` or any
   other seat moves it).
2. Re-run the bun-lock precheck at `0e02a1f` (positive and negative control); the pin moved with MP-z-5.
3. Halt-gate proof from the deploy tree (A5 of MX-r-9): materialise the base agent folder in the sparse cone, print the
   negative control (rc=3) then the positive (rc=0). `HALT_OVERRIDE` is forbidden.
4. Open NEVER-2 ledger `nfra-mcpindex-r10-catalog-release` (entry AND `.open_deploys` sentinel). Legs: upload/ship,
   `/health` 200, r11.AC2, r11.AC3.
5. `DEPLOY_BASE_REF=64b3e54658060859b81d6bcd48dc7000615f865d HALT_ACK=1 AGENT_NAME=0.7.0_AE_CloudOps~MI bash
   infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, run from `C:/tmp/mx-dep-r11`.
6. **Read the labels back BEFORE the first leg closes:** `opal-gateway-ad2acc0a93.tar.gz` present and `-latest`'s
   `git-ref` equal to `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`; confirm the rollback key is unchanged (551109 B, ETag
   `527cab0d...`).
7. Then `/health`, `r11.AC2`, `r11.AC3` (graded against the deployed catalog's bytes), `r11.AC1` at close; the three
   censuses equal again (tools 67, `.env` 54 keys, ids 7); roll back to the versioned base key on any failed leg.
8. Plane 2: record `deployed_commit` `ad2acc0a93...` in `infra/aws/ec2/EC2_MANIFEST.json`. **Row Z-W33-S6:** on
   `box/sitez` the manifest still reads `185dc04888`, so write `previous_deployed_commit` `64b3e54658` from the host read and
   expect a merge on the manifest when `rel-nfra-mcportal-gw` drains.
9. The never-widen halves (CTO + COO) are asked on THESE pins before any of this. Ask content: the delta is 2 files, the
   three censuses are equal, so there is no widening to bound; the blast radius is the gateway host and the rollback is
   the versioned key above.

## 7. NOT PROVED HERE

- The served effect (r11.AC2/AC3 against the host): only the apply shows it. AC1-AC3 are graded after PHASE B.
- The bun-lock clearance at `0e02a1f` (section 2).
- The suite on this base (the issuer reports MX-c-8's drain; not re-run).

## 8. ROWS

`NFRA_MCPINDEX-Z-W33-S6` (OBSERVATION, INERT): plane-2 manifest on `box/sitez` lags the host; MP-z-5's record is on its
undrained release branch.
