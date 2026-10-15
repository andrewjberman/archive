# ANNOUNCE -- MX-r-13 PHASE A: catalog v0.5 + discover, two blobs cut on live `ee23dd004c`

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-13.depth-every-tool-release.md` at **A3** (GO msg 34347).
Probes: `deliverables/0.7.0_AE_CloudOps~MI/probes_r13/` (every file named below is there).

**STATE: PHASE A ONLY.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no push.
AWS contact, all read-only and Opal's own: S3 `head-object` (3 keys), two SSM `AWS-RunShellScript` reads (file hashes,
`.env` KEY NAMES parsed in Python, `/health`; and the MC Portal reader's link counts). No `.env` value was read or
printed. No source file was edited.

## 0. THE ONE FINDING THE ISSUER MUST READ FIRST -- the MC Portal link counts DIFFER

The order (item "four censuses that stay EQUAL") and MX-r-12 A5 ("any difference makes BOTH halves VOID") both name
the per-tool link counts. Measured, each side read by ITS OWN reader against ITS OWN catalog (`link_counts_A1.txt`):

| | tools | links |
|---|---|---|
| LIVE `ee23dd004c` | 11 | **14** |
| CUT `d020bee315` | **33** | **112** |

**VERDICT: `per_tool_link_counts DIFFER`.** Tools added 22 (10 `harvest_*`, 4 `news_*`, 8 `portal_get_*`); the one
count changed is `etfs_get_positioning` 1 -> 2. Nothing removed. `admin_gateway_breakdown.py` is the SAME blob on both
sides (`b10782ca26`), so the reader did not change: the catalog did. This is the release's intent (78 harvest rows plus
the rows naming the 19 live tools), not drift, but it is a difference in a census the halves call EQUAL.

**The mechanism carries its control.** The host's REAL installed reader on the LIVE side reads `tools=11 links=14`
(SSM `e6e3fc32-8f37-4d26-ac9c-41f8553980e0`, `link_counts_REAL_host.txt`), equal to the off-host reading of the live
tree. The cut side cannot be taken on the host before the apply: the cut catalog is **1,059,657 bytes** and an SSM
inline command cannot carry it (my first attempt, the r12 shipping method, was stopped), so the cut side is the same
off-host reader on the cut's own files.

**Decision for the issuer, not for me:** whether the Andrew FWD-20 sitting / `NFRA_MCPORTAL.TO-MP-z-6` still constrains
this slot (r12 A1: the slot is conditional on MP-z-6 being closed or not yet started when the counts differ), and
whether the never-widen pair must name the difference as expected. I stop here.

## 1. WHAT THIS RELEASE IS -- exactly 2 files, at trunk `789ffd57b0`

| file (under `infra/aws/ec2/opal-gateway/`) | live blob (`ee23dd004c`) | shipped blob | lines +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `d180a6d86b` | **`11620b3c520175260a4662b803c1f6344b7a8eec`** | +19882 / -627 |
| `app/integrations/opal_discover/integration.py` | `cdf178e17f` | **`f3cf344cc315420f1e7d833657b07b504a246b1a`** | +69 / -21 |

Each shipped blob was **resolved from `789ffd57b0` with `git rev-parse`, never typed**, and equals the blob the GO
names. Both are also equal at `box/sitez` HEAD `019b28acc3`. The cut's file list is 2 of 2; files outside
`infra/aws/ec2/opal-gateway/`: **0**.

## 2. THE LIVE REF, READ FROM THE HOST BY HASH

| plane | read | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the tree at `ee23dd004c`** (sha256 per file, SSM `76b6c3c2-1d27-4ec7-81b0-190307c0c2ed`, 2026-10-15T05:55:00Z; `host_read_r13_PRECUT.txt`, `live_ref_by_hash_PRECUT.txt`) | tree 118 files, host non-dashboard 118, common 118, **byte-identical 118, DIFFER 0, cut-only 0, host-only 0** | **the host IS running `ee23dd004c`**, with no metadata trusted |
| 2. S3 `-latest` | 629,899 B, ETag `159fa4ead48d31a54cecd96af959a5a7`, LastModified 04:23:00Z | `git-ref` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` |
| 3. `EC2_MANIFEST.json` at `box/sitez` HEAD | `deployed_commit` `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` | AGREES |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 57 `.env` keys |

(The `EXPECTED CHANGED SET ... MISMATCH` line in the probe is the comparator's empty-expected-set artefact; the
counts above are the reading.)

## 3. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`ee23dd004c985c46d479908db46d2ad9b4f3b1c8`** |
| **DEPLOY-ONLY COMMIT** | **`d020bee315a4d0ed02e1b3ac4ce9fc48ef0648c1`** (single parent = the base; `git commit-tree` on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override) |
| deploy-only tree | `db8574656217037ae9be4da9db36c5bfc0cca2b6` |
| deploy tree | `C:/tmp/mx-dep-r13` -- **NEW**, sparse, detached, never merged, never pushed, `worktree lock`ed |
| cone | `.tools`, `data/transcripts/scripts/teams`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`**, `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps` |
| **deploy tree HEAD IS the deploy-only commit** | **YES** -- `rev-parse HEAD` = `d020bee315a4d0ed02e1b3ac4ce9fc48ef0648c1`; the two working files' `hash-object` equal the two shipped blobs exactly |
| cleanliness | `git status --porcelain` = **0 lines, whole tree** |
| closure files the deploy script reads | `lib/opal_naming.py`, `infra/logic/registry/systems.json`, `org/standards/NAMING_SCHEMA.json`, `data/transcripts/scripts/teams/meeting_allowlist.json`, `infra/aws/ec2/EC2_MANIFEST.json`, `data/firm_registry.json`: all PRESENT (the `address()` oracle is run at PHASE B, not reasoned) |
| `deploy-to-ec2.sh` in the cut | `4257417f96b5b8445af7cdc2f80ff70349dba51d`, **byte-equal to the live base's** |
| artifact keys the apply will write | `opal-gateway-d020bee315.tar.gz` and `-latest`. The versioned key is **404 today**, as it must be |
| **ROLLBACK ARTIFACT (versioned key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-ee23dd004c.tar.gz`: **629,899 B, ETag `159fa4ead48d31a54cecd96af959a5a7`, `git-ref` `ee23dd004c...`**, LastModified 04:22:58Z. Its ETag and size EQUAL `-latest`'s, so the handle is real and is what is serving (`rollback_and_target_keys_r13.txt`) |
| mcportal pin the dashboard build resolves | `17dcbb28624eab147318052f58bcc39b8eb8029c` (`MCPORTAL_RESOLVE_ONLY=1` from the cut tree, rc 0). It is the pin MP-pc-5 recorded. The host's dashboard files are NOT byte-compared in this ANNOUNCE (the census excludes them, as in r12). The bun-lock pre-check is a PHASE B step |
| Terraform | none |

## 4. THE CENSUS -- exactly 2 files differ from the live ref

`git diff ee23dd004c d020bee315`: **2** files, both the named ones; parent count **1** and the parent IS `ee23dd004c`.
A trunk merge was not used: the cut is a SINGLE-BLOB-SET OVERLAY on the live ref's tree (temporary `GIT_INDEX_FILE`
seeded from `ee23dd004c`, two `update-index --cacheinfo`, `write-tree`, `commit-tree`), so nothing else in the
worktree can ship.

## 5. THE FOUR CENSUSES (before = the live tree / the live host, after = the cut)

| census | before | after | verdict |
|---|---|---|---|
| **tools by name**, in-process (`MOCK_GRAPH=1`, the 7 live ids; `tools_census_r13.txt`) | native 69, integration 24, total **93** | native 69, integration 24, total **93** | added `[]` / removed `[]`, **EQUAL**. Negative control (drop `blackdiamond_list_fees` from the cut set): EQUAL reads **False** |
| **`.env` KEY set** (keys only), cut's own `deploy-to-ec2.sh` rendered vs the live host (`env_census_r13.txt`) | host 57 (distinct 57) | rendered 57 (distinct 57) | dropped `[]`, added `[]`, **EQUAL** |
| **`ENABLED_INTEGRATIONS`** | host: `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) | rendered: the same 7 | **EQUAL** |
| **MC Portal per-tool link counts** (section 0) | 11 tools / 14 links | 33 tools / 112 links | **DIFFER** |

Three of four are equal. The fourth is the finding in section 0.

**r13.AC4's last limb, checked early on the cut (`catalog_vs_cut_tools_r13.txt`):** the cut catalog reads
`version=0.5 harvest=78 table=216 key_template=216 retired=5`, md5 `89e754e152b56d97ac61003175c47293`; it names **29**
distinct `read_tool`s and the cut's 93-tool census serves **all of them** (not served: none). The host md5 comparison
that AC4 grades happens after the apply.

## 6. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 16 of 16 sentinels** (2026-10-15 ~06:10Z): **no gateway-host release
ledger is OPEN or HELD.** The OPLGTW ledgers the order's start condition names (OG-yr-1, OG-ap-18, OG-ap-19) are not
listed. Listed and not this act: `nfra-mcpindex-r7-bd-doc-retire` (this seat, OPEN by design, L5 date-gated to
2026-10-19/20); `nfra-oplgtw-harvest-runner-sa` (the harvest runner, another host); the dell/irpt/etfs/mdpf entries.
`nfra-mcpindex-r12-catalog-release` is the slug r13.AC1 grades: r12's real slug was `nfra-mcpindex-r11-catalog-release`
(+`-v2`), so see section 8. **The gateway slot is free.** The ledger this release opens is named at PHASE B.

## 7. TIME

Read 06:10Z. The order's limit is PHASE B before the ~13:30Z daily publish, otherwise report here and the issuer
re-measures. Nothing in this ANNOUNCE needs more than the issuer's reading and the never-widen pair.

## 8. NOT PROVED HERE, AND A SECOND NOTE FOR THE ISSUER

- The served effect: only the apply shows it. `r13.AC2` to `r13.AC4` are graded after PHASE B against deployed bytes.
- The never-widen pair: a fresh pair is signed on these pins before PHASE B, and per section 0 it must now say what it
  does about the link-count difference.
- **Ledger slug:** the order's section 3 and difference 2 name `nfra-mcpindex-r12-catalog-release`, and r13.AC1 grades
  that slug. Both predecessor releases used `nfra-mcpindex-r11-catalog-release` and `...-v2` (r12 inherited r11's
  slug). I will open the slug the order and AC1 name, `nfra-mcpindex-r12-catalog-release`, unless the issuer says
  otherwise. No such ledger exists yet.
- PHASE B steps, unchanged from r12 and listed there: host re-read of the live ref by hash (STOP if it moved), bun-lock
  pre-check at `17dcbb28`, halt-gate pair (`HALT_OVERRIDE` never), Rule 18a broker read, `address()` oracle from the
  deploy tree, ledger open (entry AND sentinel), `DEPLOY_BASE_REF=ee23dd004c985c46d479908db46d2ad9b4f3b1c8
  AGENT_NAME=0.7.0_AE_CloudOps~MI bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway
  infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from `C:/tmp/mx-dep-r13`, label read-back BEFORE the first leg closes,
  `/health`, host byte census against the cut, the censuses again, `r13.AC1` to `AC4`, manifest write
  (`deployed_commit`, `previous_deployed_commit` = `ee23dd004c`, and a `release_note` naming THIS release in the same
  write). On any failed read-back: roll back to `opal-gateway-ee23dd004c.tar.gz` only.

## 9. ROWS

None filed. The SSM size limit (section 0) is a method note, not a hazard: the real deploy ships through S3.
