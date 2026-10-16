# ANNOUNCE -- MX-r-15 PHASE A: the round 18 catalog, one blob, cut on live `3d5c9c8bf1` -- WITH ONE FINDING THE ISSUER MUST RULE ON (section 0)

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-15.round18-catalog-release.md` at **A1** (GO ~09:52Z).
Probes: `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/probes_r15/` (every file named below is there).

**STATE: PHASE A ONLY.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no push.
AWS contact, all read-only and Opal's own: S3 `head-object` (4 keys) and three SSM `AWS-RunShellScript` reads (file hashes
and `.env` KEY NAMES parsed in Python, `/health`; the installed link-count reader). No `.env` value was read or printed.
No source file was edited.

## 0. THE FINDING -- the deploy stages `scopes.json` from the deploy tree, and the host does not hold the live ref's copy

`deploy-to-ec2.sh` (OG-ap-23 A2, lines 255-264) copies `data/mdpf/config/partner_roster.json` and
`infra/logic/registry/scopes.json` from `WORKSPACE_ROOT` (the tree the script runs in) into the artifact as
`app/refs/partner_roster.json` and `app/refs/scopes.json`. `app/client_core.py:148` reads `app/refs/scopes.json` as the
registry fallback for the client tools. Measured on the host at ~10:05Z against the tree at the live ref:

| file | host sha256 (first 16) | tree at live `3d5c9c8bf1` | trunk `739786b974` |
|---|---|---|---|
| `app/refs/partner_roster.json` | `4c104d9bb8509b89` | equal | equal |
| **`app/refs/scopes.json`** | **`ff44bda4db6e48ed`** | blob `d0f83d17db` (`8fcd28d3e2b339bd`) -- **DIFFERENT** | blob `dde73e4bd0` -- **EQUAL to the host** |

So the host serves the NEWER registry copy (the trunk file's latest change is `21c6720238`, 2026-10-16 03:16 EDT, TCKT_MTADTA; the
diff between the two blobs adds `tier_live` and `product_live` blocks, `restricted_prefix_hosts`, a `4698` master, and changes
`routed` flags and pages lists), not the one in the live ref's own tree. I did not attribute each hunk to a commit. I did not establish which tree the OG-ap-23 apply ran from. The other 140 of 141 host files are
byte-identical to the live ref's tree (section 2), including `lib/opal_naming.py` and `lib/trading_calendar.py`.

**Consequence for the pinned commit.** An apply from a deploy tree whose HEAD is the A1-exact one-blob commit stages
`d0f83d17db`, and the host's `app/refs/scopes.json` would move BACKWARDS from `dde73e4bd0` to `d0f83d17db` (33 lines added, 2
removed between the two) alongside the catalog. That is a second changed file on the host, in the client tools' fallback
data, and A1 says "nothing else ships". Pre-apply byte census, host against each candidate (`host_vs_cut_r15_PRECUT.txt`):

| candidate | commit | files differing from the live ref | host-level changed set |
|---|---|---|---|
| **A -- A1 exactly (PINNED, deploy tree HEAD)** | `0b93d16d47053398b5254edd472c7d148ad925e1` | 1 (the catalog) | **2: the catalog AND `scopes.json` (regress)** |
| **B -- catalog plus `scopes.json` at `dde73e4bd0`** | `0cb4a87bcb8df4adbb71d095f0818b0f50c562f1` | 2 (the catalog; `infra/logic/registry/scopes.json`) | **1: the catalog only** |

**The ask, one decision for `2.0.0_SA_COO~MI`: which commit does the never-widen pair sign?** My recommendation is **B**: the
host's changed set is then the catalog alone, which is what A1 intends, and `scopes.json` keeps the bytes the host already
serves. B adds one file to the git diff that A1 does not name, so it needs your amendment, and
the pair must name that file. If you choose A, the pair must name the `scopes.json` regression as an accepted effect. Either way
the deploy tree moves with your A2 (HEAD to `0cb4a87bcb` for B); nothing is re-cut, both commits exist now.

## 1. WHAT THIS RELEASE IS -- A1's one blob, at trunk `739786b974`

| file (under `infra/aws/ec2/opal-gateway/`) | live blob (`3d5c9c8bf1`) | shipped blob | lines +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `b97c59e6ac9900b99a32fe6a8c957b4f00f71ca9` | **`cf7616c08ec6b50a4676f962546ec6e732772e39`** | +5363 / -5408 |

The shipped blob was **resolved from `739786b974` with `git rev-parse`, never typed**, and equals the blob A1 names; `739786b974`
is an ancestor of `box/sitez` HEAD. md5 of the file in the deploy tree: `9519ebce3a1b92cee07a5507d1912dd3`, equal to A1's.

**The r15.AC4 counts, read with the issuer's own `r15_ac4_host.py` on both catalogs (`ac4_counts_cut_vs_live_r15.txt`):**

| | version | harvest | table | key_template | retired | rows | nl_tags | inferred | bucket | vendor | firm | tool_index | tool_bucket | serves |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LIVE `b97c59e6ac` | 0.5 | 78 | 216 | 216 | 5 | 304 | 304 | 44 | 294 | 0 | 24 | 99 | 0 | 0 |
| **CUT `cf7616c08e`** | 0.5 | 78 | **192** | **192** | **1** | **280** | **280** | **0** | **280** | **136** | **136** | **127** | **127** | **7** |

The cut equals A1's expected line (rows 280, nl_tags 280, inferred 0, bucket 280, vendor and firm 136, tool_index bucket 127 of
127, serves on 7). The cut has 24 FEWER rows than the live catalog (table 216 -> 192, retired 5 -> 1, rows 304 -> 280): that is
A1's own figure, and I note it because the pair's "newly visible rows" count is a difference, not an addition. The cut names 61
distinct `read_tool`s and the cut's 127-tool census serves all of them (not served: **none**, `catalog_vs_cut_tools_r15.txt`).

## 2. THE LIVE REF, READ FROM THE HOST BY HASH

| plane | read | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the tree at `3d5c9c8bf1`** (sha256 per file, SSM `37703725-95fd-45d1-8462-775caf260c1d`, ~10:05Z; `host_read_r15_PRECUT.txt`, `live_ref_by_hash_PRECUT.txt`) | 141 files (app, deploy, the two staged refs, the two staged `lib` files); common 141; **byte-identical 140, DIFFER 1 (`app/refs/scopes.json`, section 0)**, cut-only 0, host-only 0 | **the host runs `3d5c9c8bf1` except that one registry copy** |
| 2. S3 `-latest` | 893,303 B, ETag `d43206bfdad42ae29300cf94eed1423a`, LastModified 09:13:53Z | `git-ref` `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4` |
| 3. `EC2_MANIFEST.json` at `box/sitez` HEAD | `deployed_commit` `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4`, previous `d577e0e729`, `deployed_at` 2026-10-16T09:14:19Z | AGREES |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 64 `.env` keys |

The first read of the pass (`db19079d`, 10:01:12Z) had the same `/health` 200 and 64 keys; I re-read with `lib/` added to the census
because the staged `lib` files ship from the tree too. The dashboard bundle (mcportal) is not in the census, as in earlier rounds.

## 3. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4`** (the release commit is itself the deployed one; the deploy tree head `ed5d4541a8` named in A1 is the wrapper's manifest commit and differs from it in `EC2_MANIFEST.json` only, 4 lines) |
| **DEPLOY-ONLY COMMIT A (PINNED)** | **`0b93d16d47053398b5254edd472c7d148ad925e1`**, tree `5c43d65084241cc15517c3fb92a75c0cde58931e`; single parent = the base; `git commit-tree` on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override |
| deploy-only commit B (offered, section 0) | `0cb4a87bcb8df4adbb71d095f0818b0f50c562f1`, tree `bb78f02f2e7dfe40986948941a3895b75c776105`; same parent; one more file |
| deploy tree | `C:/tmp/mx-dep-r15` -- **NEW**, sparse, detached, never merged, never pushed, `worktree lock`ed |
| cone | `.tools`, `data/transcripts/scripts/teams`, `data/mdpf/config`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`**, `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps` |
| cone difference from MX-r-14 | **`data/mdpf/config` is NEW**: the deploy script now refuses (no upload) when `data/mdpf/config/partner_roster.json` is missing from the tree |
| deploy tree HEAD IS the deploy-only commit | **YES (A)**; the working catalog's `hash-object` equals the shipped blob; `git status --porcelain` = **0 lines** |
| `deploy-to-ec2.sh` in the cut | `ec275608ff78a85655196f8977a97ba156910d3a`, **byte-equal to the live ref's** |
| artifact keys the apply will write | `opal-gateway-0b93d16d47.tar.gz` (A) or `opal-gateway-0cb4a87bcb.tar.gz` (B) and `-latest`. Both versioned keys are **404 today**, as they must be |
| **ROLLBACK ARTIFACT (versioned key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-3d5c9c8bf1.tar.gz`: **893,303 B, ETag `d43206bfdad42ae29300cf94eed1423a`, `git-ref` `3d5c9c8bf1...`**, LastModified 09:13:52Z. Its size and ETag EQUAL `-latest`'s (`rollback_and_target_keys_r15.txt`) |
| Terraform | none |

The rollback key is NOT the one MX-r-14 left (`opal-gateway-06cfb6db64`). The pair must name `opal-gateway-3d5c9c8bf1.tar.gz` at the
size and ETag above. Rolling back restores the live ref's tarball, which carries the live ref's own `scopes.json` (`d0f83d17db`),
so a rollback after commit A or B restores THAT copy, not the `dde73e4bd0` the host serves today.

## 4. THE CENSUS -- what differs from the live ref

`git diff 3d5c9c8bf1 0b93d16d47`: **1** file (`DATA_CATALOG.yaml`), parent count **1**, and the parent IS `3d5c9c8bf1`. The cut is a
single-blob overlay on the live ref's tree (temporary `GIT_INDEX_FILE` seeded from `3d5c9c8bf1`, `update-index --cacheinfo`,
`write-tree`, `commit-tree`), so nothing else in the worktree can ship through git. `scopes.json` and `partner_roster.json` ship
through the script's staging step, which is why section 0 exists.

## 5. THE FOUR CENSUSES (before = the live tree / the live host, after = the cut)

| census | before | after | verdict |
|---|---|---|---|
| **tools by name**, in-process (`MOCK_GRAPH=1`, the 7 live ids; `tools_census_r15.txt`) | native 103, integration 24, total **127** | native 103, integration 24, total **127** | added `[]` / removed `[]`, **EQUAL**; dropping one name (`blackdiamond_list_fees`) reads **False** |
| **`.env` KEY set**, the cut's own `deploy-to-ec2.sh` rendered vs the live host (`env_census_r15.txt`) | host 64 (distinct 64) | rendered 64 (distinct 64) | dropped `[]`, added `[]`, **EQUAL** |
| **`ENABLED_INTEGRATIONS`** | host: `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) | rendered: the same 7 | **EQUAL** |
| **MC Portal per-tool link counts** (`link_counts_A1.txt`) | 39 tools / 119 links | **65 tools / 192 links** | **DIFFER, EXPECTED** (+26 tools / +73 links = A1's figure) |

Three of four are equal; the fourth is the ruled expected value. Link-count detail: tools added 26 (`client_get_allocation`,
`client_get_fees`, `client_get_holdings`, `client_get_transactions`, `client_resolve_account`, `etfs_compare_peers`,
`etfs_get_coverage`, `etfs_get_fund_bloomberg_characteristics`, `etfs_get_fund_flows`, `etfs_get_fund_snapshot`,
`etfs_get_fund_trades`, `etfs_get_new_securities`, `etfs_get_peer_group_members`, `etfs_get_research_notes`,
`etfs_get_rival_fund_holdings`, `etfs_get_rival_page_status`, `etfs_get_security_reference`, `etfs_who_holds`,
`mdpf_get_model_composition`, `portal_get_cma_assumptions`, `portal_get_correlations`, `portal_get_etf_returns`,
`portal_get_factor_tilts`, `portal_get_model_portfolio_timeseries`, `portal_get_peer_performance`, `portal_get_trending`); removed
none; six existing tools gained one link each (`etfs_get_positioning` 2 -> 3, `mdpf_get_account_distribution`,
`mdpf_get_aggregate_aua`, `mdpf_get_aum_metrics`, `mdpf_get_model_benchmarks` and `news_market_mood` 1 -> 2). `admin_gateway_breakdown.py`
is the SAME blob `f09b559b7a` on both sides, so the catalog is the cause. Each side is read by its OWN reader against its OWN catalog; the
CONTROL ran on the host: the real installed `app.admin_gateway_breakdown` reads **39 / 119** on the live side
(`link_counts_REAL_host_PRECUT.txt`), the same as the off-host mechanism.

## 6. THE VISIBILITY CHANGE THE PAIR MUST NAME (order difference 3)

After this release a principal of firm X sees the rows the C-GROUP labels name; A1 and the issuer's `c23.AC3` give 96 newly visible
(49financial 62, inflection 8, cottonwood 26) over 1,182 pairs, cross-firm leaks 0. **What I measured is only that the catalog
carries `firm=136` and `vendor=136` (section 1).** I did not run the visibility behaviour: the discover module is unchanged
between the live ref and the cut, `r15.AC4` grades the catalog fields, and the firm-visibility matrix on the host is the issuer's own
run after the apply. No check in this order puts a firm principal in front of the host.

## 7. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 23 of 23 sentinels** (~10:10Z; `open_ledgers_r15.txt`): **no gateway-host release
ledger is OPEN or HELD.** The one OPEN entry is this seat's `nfra-mcpindex-r7-bd-doc-retire` (L5, date-gated), not a gateway release.
`nfra-mcpindex-r15-catalog-release`, this release's slug, does not exist yet; it opens at PHASE B. **The gateway slot is free.**

## 8. TIME, AND NOT PROVED HERE

- Read ~10:05Z-10:20Z. PHASE B must close before **13:00Z** (the depth claims were read 2026-10-15 16:07Z and hold until the ~13:30Z
  daily publish). The pair and A2 are the critical path.
- **The served effect:** only the apply shows it. `r13.AC2`, `r13.AC3` and `r15.AC4` are graded after the first leg against
  deployed bytes. `r15.AC1` grades a CLOSED ledger and needs the close committed.
- **Python:** these probes ran under Python 3.14.8 from Git Bash `python`; stdlib-only apart from `yaml`, every comparison has its
  negative control where noted.
- **Not verified:** which tree the OG-ap-23 apply ran from (section 0); a firm principal's view on the host (section 6); the
  dashboard bundle build, which is a PHASE B step.
- PHASE B, as MX-r-14 listed: host re-read of the live ref by hash (STOP if it moved: BASE-MOVED), bun-lock pre-check at the mcportal
  pin (both arms), halt-gate pair, Rule 18a broker read, the `address()` oracle, ledger open (entry AND sentinel),
  `DEPLOY_BASE_REF=3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4 AGENT_NAME=0.7.0_AE_CloudOps~MI bash
  infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from `C:/tmp/mx-dep-r15`, label read-back
  BEFORE the first leg closes, host byte census against the cut (live tree as the negative control), the censuses again,
  `r13.AC2`/`AC3`, `r15.AC4`, then `r15.AC1` after the close, the manifest write (`deployed_commit` the pinned commit,
  `previous_deployed_commit` `3d5c9c8bf1`, a `release_note` naming THIS release, in one write). On any failed read-back, roll back to
  `opal-gateway-3d5c9c8bf1.tar.gz` only.

## 9. ROWS

One filed: `NFRA_MCPINDEX-Z-S126` (section 0). The order names `Z-W35-S<k>`, but the row gate refuses a W coordinate from a committer that is not a worker ("a seat's row on the main index carries no W"), so it is the next free Z-S number after Z-S125, OBSERVATION / INERT, `disarm_owner` `2.0.0_SA_COO~MI`. It turns ARMED only if PHASE B
runs on commit A without your ruling.
