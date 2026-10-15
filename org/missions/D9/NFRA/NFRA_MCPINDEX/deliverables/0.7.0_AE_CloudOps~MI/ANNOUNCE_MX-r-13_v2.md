# ANNOUNCE -- MX-r-13 PHASE A again (v2): the re-cut catalog and discover, two blobs cut on live `ee23dd004c`

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.md` at **A5** @`ccf29447c7`
(GO msg 34388). It replaces `ANNOUNCE_MX-r-13.md` (the first attempt, `d020bee315`, deployed and rolled back).
Probes: `deliverables/0.7.0_AE_CloudOps~MI/probes_r13v2/`.

**STATE: PHASE A ONLY.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no push.
AWS contact, all read-only and Opal's own: S3 `head-object` (4 keys) and one SSM `AWS-RunShellScript` read (file hashes,
`.env` KEY NAMES parsed in Python, `/health`). No `.env` value was read or printed. No source file was edited.

## 0. WHAT CHANGED SINCE THE FIRST ATTEMPT

Only the catalog blob. The discover blob is unchanged, so the cut differs from the rolled-back `d020bee315` by 4 catalog
lines. Every census reads as it did at the first attempt:

| | first attempt `d020bee315` | this cut `1b18b94979` |
|---|---|---|
| tools by name | 93 = 93 | 93 = 93, EQUAL |
| `.env` keys | 57 = 57 | 57 = 57, EQUAL |
| `ENABLED_INTEGRATIONS` | 7 = 7 | 7 = 7, EQUAL |
| MC Portal per-tool link counts | 11/14 -> 33/112 | 11/14 -> **33/112**, the per-tool lines IDENTICAL to the first attempt's |

The link-count difference is EXPECTED at exactly 33 tools / 112 links, as ruled in A4 and carried by A5.

## 1. WHAT THIS RELEASE IS -- exactly 2 files, at trunk `32d0bc608a`

| file (under `infra/aws/ec2/opal-gateway/`) | live blob (`ee23dd004c`) | shipped blob | lines +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `d180a6d86b` | **`e5096b5d6c1b7819d9b1aa742b2c2136cc547758`** | +19884 / -629 |
| `app/integrations/opal_discover/integration.py` | `cdf178e17f` | **`f3cf344cc315420f1e7d833657b07b504a246b1a`** | +69 / -21 |

Each shipped blob was **resolved from `32d0bc608a` with `git rev-parse`, never typed**, and equals the blob the GO names.
Both are equal at `box/sitez` HEAD. Files outside `infra/aws/ec2/opal-gateway/`: **0**. The cut catalog reads
`version=0.5 harvest=78 table=216 key_template=216 retired=5`, md5 `5e11a65fca98ce9f570c9aaade49e58c`; it names 29 distinct
`read_tool`s and the cut's 93-tool census serves all of them (not served: none).

## 2. THE LIVE REF, READ FROM THE HOST BY HASH

| plane | read | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the tree at `ee23dd004c`** (sha256 per file, SSM `0754ef1c-1ac1-4eb5-99cc-0fa89445873f`, 2026-10-15T07:32:13Z; `host_read_v2_PRECUT.txt`, `live_ref_by_hash_v2_PRECUT.txt`) | 118 files, host non-dashboard 118, common 118, **byte-identical 118, DIFFER 0, cut-only 0, host-only 0** | **the host IS running `ee23dd004c`** |
| 2. S3 `-latest` | 629,787 B, ETag `3cd90347e472d1b7c0eaa31ad43c9242`, LastModified 06:46:31Z | `git-ref` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` |
| 3. `EC2_MANIFEST.json` at `box/sitez` HEAD | `deployed_commit` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` | AGREES |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 57 `.env` keys |

## 3. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`ee23dd004c985c46d479908db46d2ad9b4f3b1c8`** |
| **DEPLOY-ONLY COMMIT** | **`1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0`** (single parent = the base; `git commit-tree` on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override). `d020bee315` is not reused |
| deploy-only tree | `4b458714e98f3d2221b1134bdd13505b501a8bdf` |
| deploy tree | `C:/tmp/mx-dep-r13v2` -- **NEW**, sparse, detached, never merged, never pushed, `worktree lock`ed. `C:/tmp/mx-dep-r13` (the first cut) and `C:/tmp/mx-dep-r13-rb` (the rollback tree at `ee23dd004c`) are kept and locked |
| cone | `.tools`, `data/transcripts/scripts/teams`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`**, `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps` |
| **deploy tree HEAD IS the deploy-only commit** | **YES**; the two working files' `hash-object` equal the two shipped blobs exactly; `git status --porcelain` = **0 lines**; the `address()` oracle resolves from this tree; the closure files are present |
| `deploy-to-ec2.sh` in the cut | `4257417f96b5b8445af7cdc2f80ff70349dba51d`, **byte-equal to the live base's** |
| artifact keys the apply will write | `opal-gateway-1b18b94979.tar.gz` and `-latest`. The versioned key is **404 today**, as it must be |
| **ROLLBACK ARTIFACT (versioned key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-ee23dd004c.tar.gz`: **629,787 B, ETag `3cd90347e472d1b7c0eaa31ad43c9242`, `git-ref` `ee23dd004c...`**, LastModified 06:46:29Z. Its size and ETag EQUAL `-latest`'s, so the handle is real and is what is serving. **It is NOT the bytes the first attempt's halves named:** they named 629,899 B / ETag `159fa4ea...`, and the first attempt's rollback redeploy re-uploaded this key. The files inside are byte-identical to the host (118 of 118), so the rollback target is the same content; only the tar differs. The fresh pair must name THIS size and ETag |
| mcportal pin the dashboard build resolves | `17dcbb28624eab147318052f58bcc39b8eb8029c` (`MCPORTAL_RESOLVE_ONLY=1` from the cut tree, rc 0), unmoved. The bun-lock pre-check is re-run at PHASE B |
| Terraform | none |

## 4. THE CENSUS -- exactly 2 files differ from the live ref

`git diff ee23dd004c 1b18b94979`: **2** files, both the named ones; parent count **1**, and the parent IS `ee23dd004c`.
The cut is a SINGLE-BLOB-SET OVERLAY on the live ref's tree, so nothing else can ship.

## 5. THE FOUR CENSUSES (before = the live tree / the live host, after = the cut)

| census | before | after | verdict |
|---|---|---|---|
| **tools by name**, in-process (`MOCK_GRAPH=1`, the 7 live ids; `tools_census_v2.txt`) | native 69, integration 24, total **93** | native 69, integration 24, total **93** | added `[]` / removed `[]`, **EQUAL**; dropping one name (`blackdiamond_list_fees`) reads **False** |
| **`.env` KEY set**, the cut's own `deploy-to-ec2.sh` rendered vs the live host (`env_census_v2.txt`) | host 57 (distinct 57) | rendered 57 (distinct 57) | dropped `[]`, added `[]`, **EQUAL** |
| **`ENABLED_INTEGRATIONS`** | host: `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) | rendered: the same 7 | **EQUAL** |
| **MC Portal per-tool link counts**, each side by its OWN reader against its OWN catalog (`link_counts_A1_v2.txt`) | 11 tools / 14 links | **33 tools / 112 links** | **DIFFER, EXPECTED** at 33 / 112; per-tool lines identical to the first attempt's |

The reader (`admin_gateway_breakdown.py`) is the same blob `b10782ca26` on both sides. The host's real installed reader
on the live side read `11 / 14` at the first attempt and again after the rollback, which is the control for the off-host
reading.

## 6. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 17 of 17 sentinels** (07:3xZ): **no gateway-host release ledger is OPEN or
HELD** (`open_ledgers_v2.txt`). `nfra-mcpindex-r12-catalog-release` is CLOSED (rolled back) and
`nfra-mcpindex-r12-catalog-release-v2`, this attempt's slug, does not exist yet; it opens at PHASE B. **The gateway slot
is free.**

## 7. WHAT I DID NOT PROVE, AND WHAT PHASE B ADDS

- **`r13.AC2` is the criterion that failed last time and it cannot be read before the apply.** The issuer's reading on an
  extract of the first cut with this catalog is `sum 93 of 93, a=11 valid 11, definitions 93 of 93, discover 3 of 3`;
  mine on the deployed bytes will be the one that counts.
- Never-widen pair: a fresh pair is signed on `1b18b94979` before PHASE B (the old pair is void).
- PHASE B, unchanged from the first attempt: host re-read of the live ref by hash (STOP if it moved), bun-lock pre-check at
  `17dcbb28` (both arms), halt-gate pair, Rule 18a broker read, `address()` oracle, ledger open (entry AND sentinel),
  `DEPLOY_BASE_REF=ee23dd004c985c46d479908db46d2ad9b4f3b1c8 AGENT_NAME=0.7.0_AE_CloudOps~MI bash
  infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from `C:/tmp/mx-dep-r13v2`,
  label read-back BEFORE the first leg closes, host byte census against the cut (live tree as the negative control), the
  censuses again, `r13.AC1` to `AC4`, the manifest write (`deployed_commit` `1b18b94979`, `previous_deployed_commit`
  `ee23dd004c`, a `release_note` naming THIS release, in one write). On any failed read-back, roll back to
  `opal-gateway-ee23dd004c.tar.gz` only.
- **Time:** read 07:37Z; the close is due by 13:00Z.

## 8. ROWS

None new. (Z-S118 and Z-S119 are the issuer's, ruled in A5.)
