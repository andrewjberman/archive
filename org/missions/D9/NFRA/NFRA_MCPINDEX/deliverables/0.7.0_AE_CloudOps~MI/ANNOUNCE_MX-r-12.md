# ANNOUNCE -- MX-r-12 PHASE A: MX-c-9's three gateway blobs, cut on live `b0c75d24f1`

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-12.depth-v4-release.md`, at **A2**
@`e13becfa37` and **A4** @`8607bd9a82` (A4 is the governing amendment; A3's wait is lifted by it). GO: msg 33939.
Probes: `deliverables/0.7.0_AE_CloudOps~MI/probes_r12/` (every file named below is there).

**STATE: PHASE A ONLY.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no
push. AWS contact, all read-only and Opal's own: S3 `head-object` (4 keys) and two SSM `AWS-RunShellScript` reads
(file hashes, `.env` KEY NAMES parsed in Python, `/health`, and the MC Portal reader's link counts). No `.env`
value was read or printed. No source file was edited.

## 0. WHAT THIS RELEASE IS -- exactly 3 files, MX-c-9's committed bytes

| file | live blob (at `b0c75d24f1`) | shipped blob (MX-c-9, @`435958cd7c`) | +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `54afa75ea1` | **`f15b34826312e3735a79b6c17dea7e0deea9ec81`** | +347 / -39 |
| `app/integrations/opal_discover/integration.py` | `021a708e5f` | **`cdf178e17fec8d285096d0538c57045c40d6ab39`** | +67 / -2 |
| `app/admin_gateway_breakdown.py` | `acfe8c8b06` | **`b10782ca26c16ca7a82e6f91eb000c3a1ea570b7`** | +1 / -1 |

(All three paths are under `infra/aws/ec2/opal-gateway/`.) Each shipped blob was **resolved from the drain commit
with `git rev-parse`, never typed**, and the issuer's abbreviation was then used as a CHECK on what resolved --
`f15b348263`, `cdf178e17f`, `b10782ca26` are each a prefix of the resolved id. All three are **equal at
`box/sitez` HEAD**, so nothing has drifted since the drain.

**The cut's file list (printed, 3 of 3):**
1. `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`
2. `infra/aws/ec2/opal-gateway/app/integrations/opal_discover/integration.py`
3. `infra/aws/ec2/opal-gateway/app/admin_gateway_breakdown.py`

**WHAT IS DELIBERATELY ABSENT, per A4.** MX-c-9 A3's six hyphenated research rows are NOT in this cut and cannot
be committed yet: `.tools/naming-gate.py` does not read `legacy_addresses.json`, so their emitted `prefix:` values
grade NEW OUT-OF-PATTERN (row `Z-W34-S7`; the ask is with `1.0.0_SA_CTO~Z`, and the gate is LGIC_ENFORCE's). So
this release delivers **FWD-20 depth and the durable `index` key**, and **FWD-21 at 24 of 24 top-level prefixes
with 1 of 7 research tables**. `r12.AC2` and `r12.AC3` grade FWD-20 and discover and do not count research tables,
so they stand as written. Per A4, if the gate fix lands and MX-c-9 A3 commits BEFORE the never-widen pair is
signed, this cut is re-made once on the new catalog blob; after the pair, the six rows ride the next gateway
release.

## 1. THE LIVE REF, READ FROM THE HOST BY HASH -- not from `-latest`'s label

| plane | read (UTC) | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the tree at `b0c75d24f1`** (sha256 per file, SSM `dad38918-3c9b-4df7-b03d-cbe16c614c7f`, 02:41:19Z; `host_read_r12_PRECUT.txt`) | cut/tree 107 files, host non-dashboard 107, common 107, **byte-identical 107, DIFFER 0, cut-only 0, host-only 0** | **the host IS running `b0c75d24f1`**, established without trusting any metadata |
| 2. S3 `-latest` metadata (`rollback_and_target_keys_r12.txt`) | 557,415 B, ETag `c9bce856c6bbf1003f40970a8a9d9fac`, LastModified 2026-10-14T01:20:59Z | `git-ref` `b0c75d24f11808d1de4f70fcca5d39216282054a` |
| 3. `EC2_MANIFEST.json` plane 2, `box/sitez` HEAD | `deployed_commit` `b0c75d24f1...` | AGREES |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 54 `.env` keys |

All three planes name `b0c75d24f1`, which is NFRA_MCPORTAL MP-n-4 (01:31Z) and matches A2.

## 2. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`b0c75d24f11808d1de4f70fcca5d39216282054a`** |
| **DEPLOY-ONLY COMMIT** | **`027fedfda48714721deeddf41b87e0de6a5c0266`** (single parent = the base; `git commit-tree` plumbing on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override) |
| deploy-only tree (repo root) | `3a55e7e43e0273adbda8b90ba1967506a9731962` |
| deploy tree | `C:/tmp/mx-dep-r12` -- **NEW**, as A2 requires (`mx-dep-r11` is kept and locked as MX-r-11 v2's rollback pin), sparse, detached, never merged, never pushed, `worktree lock`ed |
| cone | `.tools`, `data/transcripts/scripts/teams`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`** (order item 2 / round-10 analysis ruling 3), `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps` |
| **deploy tree HEAD IS the deploy-only commit** | **YES** -- `rev-parse HEAD` = `027fedfda48714721deeddf41b87e0de6a5c0266`; the three working files' `hash-object` equal the three shipped blobs exactly, so the label will name the shipped bytes (ruling 2c / row `Z-S92`) |
| deploy tree cleanliness | `git status --porcelain` = **0 lines, whole tree** (not merely the gateway dir) |
| artifact keys the apply will write | `opal-gateway-027fedfda4.tar.gz` and `-latest`, both `git-ref` = `027fedfda48714721deeddf41b87e0de6a5c0266`. The versioned key is **404 today** (absent), as it must be |
| **ROLLBACK ARTIFACT (the VERSIONED key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-b0c75d24f1.tar.gz`: **557,415 B, ETag `c9bce856c6bbf1003f40970a8a9d9fac`, `git-ref` `b0c75d24f1...`**, LastModified 01:20:57Z. Its ETag and size EQUAL `-latest`'s today, so the handle is real and is what is serving. One step back is `opal-gateway-7eff14b2e6.tar.gz` (557,605 B, ETag `c8b27c10...`), MX-r-11 v2, still present |
| mcportal pin the dashboard build resolves | `0e02a1f1ab56dae65b9df29bd78f1eab319ce6a2` (`MCPORTAL_RESOLVE_ONLY=1` from the cut tree, rc 0). **UNMOVED** since MP-z-5, so the bun-lock clearance measured twice earlier today on the same lockfile still stands (`77 of 77` rc=0, with a planted-package arm reading `77 of 78` rc=1). It is re-run at the apply regardless |
| `deploy-to-ec2.sh` in the cut | `2e9e3aed368ce0da2690f77deac3c688d1b90141` -- **byte-equal to the live base's**, so a "deploy script other than the base's" VOID condition stays false. It is NOT `box/sitez`'s copy (`76a4f20a6f`); see row `Z-S109` |
| Terraform | none |

## 3. THE CENSUS -- exactly 3 files differ from the live ref

`git diff b0c75d24f1 027fedfda4`:

| | |
|---|---|
| files changed | **3**, all three the named ones |
| lines | catalog **347/39**, discover **67/2**, breakdown **1/1** |
| files OUTSIDE `infra/aws/ec2/opal-gateway/` | **0** |
| parent count | **1**, and the parent IS `b0c75d24f1` |

**THE NEGATIVE CONTROL ON THE CUT METHOD, and it is not cosmetic.** The order (item 1) and the MX-r-11 v2 lesson
both forbid shipping a trunk tree. Measured: `git diff --name-only 027fedfda4 box/sitez -- infra/aws/ec2/opal-gateway`
reads **32 paths**. **A merge of `box/sitez` would have shipped 32 files instead of 3**, including
`deploy-to-ec2.sh`, which would void the halves on the deploy script alone. The cut is therefore a
SINGLE-BLOB-SET OVERLAY on the live ref's tree -- a temporary `GIT_INDEX_FILE` seeded from `b0c75d24f1`, three
`update-index --cacheinfo` calls, `write-tree`, `commit-tree` -- which also keeps anything else in the worktree
out of the shipped tree by construction rather than by care.

## 4. THE THREE EQUAL CENSUSES (before = the live tree / the live host, after = the cut)

**Tool census, in-process (`MOCK_GRAPH=1`, the 7 live ids; `tools_live_r12.json`, `tools_cut_r12.json`,
`censuses_r12.txt`):**

| | native | integration | total |
|---|---|---|---|
| live (`b0c75d24f1`) | 43 | 24 | **67** |
| cut (`027fedfda4`) | 43 | 24 | **67** |
| added / removed | | | **none / none**, names EQUAL |

**67 = 67. NEGATIVE CONTROL: dropping one name from the cut's set makes the same comparison read `EQUAL False`.**
Worth measuring rather than assuming here, because the cut changes `opal_discover/integration.py` -- a file that
registers tools -- not only data.

**`.env` KEY set (keys only, never values):** rendered from the cut's own `deploy-to-ec2.sh` **54** (distinct 54);
live host **54** (distinct 54); **dropped `[]`, added `[]`**.

**`ENABLED_INTEGRATIONS`:** before (live host, 02:41:19Z) `ycharts opal_portal globgrph opal_discover
portal_index schwab blackdiamond` (**7**); after (rendered from the cut) the same **7**; **difference EMPTY,
`EQUAL`**.

No widening on any of the three.

## 5. A1's MC PORTAL PER-TOOL LINK COUNTS -- LIVE vs CUT: **EQUAL**

A1 requires this because the release must not land between Andrew's FWD-20 read of the MC Portal breakdown page
and `NFRA_MCPORTAL.TO-MP-z-6`'s run unless the per-tool index link counts stay EQUAL.

`admin_gateway_breakdown._catalog_read_tool_rows()` (at `:98` in both trees -- A1 cites `:108` at HEAD, a line
shift only; the function is the same by name and signature), each side read by **ITS OWN reader against ITS OWN
catalog**, same mechanism both sides (`link_counts_host.py`, `link_counts_A1.txt`):

| | tools | links |
|---|---|---|
| LIVE `b0c75d24f1` | 11 | **14** |
| CUT `027fedfda4` | 11 | **14** |
| difference | tools added `[]`, tools removed `[]`, counts changed `[]` | |

**VERDICT: `per_tool_link_counts EQUAL`.** Per-tool: `schwab_query` 4; `blackdiamond_list_fees`,
`etfs_get_positioning`, `gateway_query_catalog`, `mdpf_get_account_distribution`, `mdpf_get_aggregate_aua`,
`mdpf_get_aum_metrics`, `mdpf_get_model_benchmarks`, `opal_asker_query`, `schwab_describe_dataset`,
`schwab_list_files` 1 each.

**So the slot is NOT conditional on MP-z-6**: this release leaves the breakdown page's link counts untouched.

**THE MECHANISM CARRIES ITS OWN CONTROL, because the counts are computed off-host.** The gateway's deps
(`starlette`) exist only in the host venv, so the module cannot be imported off-host; the reader's
`_catalog_read_tool_rows` source is therefore extracted by `ast` and exec'd with `CATALOG_YAML` bound per tree.
To show that mechanism reproduces the module's own answer, the LIVE side was ALSO taken on the host by importing
the real installed module (SSM `4699d0db-c395-47a8-81a6-fbdc3bce70e3`, `link_counts_REAL_host.txt`):

```
ast-exec LIVE: tools=11 links=14
real import  : tools=11 links=14      per-tool EQUAL: True
NEGATIVE CONTROL (bump one count by 1): EQUAL reads False
```

## 6. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 18 of 18 sentinels** (read at 02:2xZ): **no gateway-host release
ledger is OPEN or HELD.** `nfra-mcportal-c17r2-release` -- which MP-n-4 opened at the very commit this cut sits
on -- has CLOSED. `nfra-oplgtw-fd2-etf-drain` is HELD on a 23:30Z EventBridge sweep and is a data drain, not a
host release. `NFRA_OPLGTW.TO-OG-ap-14` has not opened an entry yet. `nfra-mcpindex-r7-bd-doc-retire` is OPEN
(stranded L5, 20.2 h into a 192 h window, this seat's author line) -- a bd-doc retire on another host, the
MX-s-19 surface, not this host and not this act. **The gateway slot is free.**
`nfra-mcpindex-r11-catalog-release` does not exist yet; it opens at PHASE B.

## 7. PHASE B -- NOT STARTED; what it does

1. Re-read the live ref from the HOST by hash. If it is not `b0c75d24f1`, STOP: these pins are void and the
   document is re-cut, not patched.
2. Re-run the bun-lock pre-check at `0e02a1f` (both arms).
3. Halt-gate proof from the deploy tree, as a PAIR. `HALT_OVERRIDE` is forbidden. **Note for whoever writes the
   negative arm:** `AGENT_NAME` and `CLAUDE_CODE_SESSION_ID` are NOT this gate's knobs -- it resolves from this
   checkout's `org/mcp/sessions/<session>.serial`, then the EXPORTED `$OPAL_AGENT_SERIAL`, then the shared
   checkout -- so an arm built on either reads rc=0 and proves nothing. The pre-apply mail guard is Rule 18a's
   PRIMARY limb, the broker read, never a HALTGT pass.
4. Open NEVER-2 ledger `nfra-mcpindex-r11-catalog-release` (entry AND `.open_deploys` sentinel, committed
   together). Legs: upload/ship, `/health` 200, then `r12.AC2` and `r12.AC3`.
5. `DEPLOY_BASE_REF=b0c75d24f11808d1de4f70fcca5d39216282054a AGENT_NAME=0.7.0_AE_CloudOps~MI bash
   infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, run from
   `C:/tmp/mx-dep-r12`.
6. **Read the labels back BEFORE the first leg closes:** `opal-gateway-027fedfda4.tar.gz` present and `-latest`'s
   `git-ref` equal to `027fedfda48714721deeddf41b87e0de6a5c0266`; confirm the rollback key
   `opal-gateway-b0c75d24f1.tar.gz` is unchanged (557,415 B, ETag `c9bce856...`).
7. Then `/health`, the host byte census against the cut with the live tree as the negative control, the three
   censuses equal again, `r12.AC2` and `r12.AC3`; plane 2 records `deployed_commit` `027fedfda4...` with
   `previous_deployed_commit` `b0c75d24f1...`; close the ledger; then `r12.AC1`; write the proof instance.
   **And `release_note` is rewritten for THIS release in the same write as the commit fields** -- leaving the
   prior release's note beside new commit fields is the defect `NFRA_MCPORTAL-Z-S49` raised against MX-r-11.
8. On any failed read-back, roll back to **the live ref you cut on** -- `opal-gateway-b0c75d24f1.tar.gz` -- and
   never further.

## 8. NOT PROVED HERE

- The served effect: only the apply shows it. `r12.AC2` (FWD-20 partition through MC Portal's reader, no row
  identity in `tool_index`, discover 3 of 3) and `r12.AC3` (measured depths verified by the AWS CLI, and the AUA
  answer's answer-time depth) are graded after PHASE B, against the deployed bytes.
- The six research rows: absent by A4, and the naming-gate ask is with `1.0.0_SA_CTO~Z` (row `Z-W34-S7`).
- The never-widen pair: a pair is signed on these pins before the GO. This document is the ask's input.
- `r12.AC1`: its limbs grade a CLOSED ledger, and no ledger is open yet.

## 9. ROWS

None new from PHASE A. The standing ones this cut rests on: `Z-S108` / `Z-S111` (the deploy cone's closure --
exercised clean in this tree: both `lib.opal_naming.address()` calls resolve, so the MX-r-11 failure cannot
recur) and `Z-S109` (the ANNOUNCE blob-figure correction). Measured and worth the round analysis: **the script
this release ships is `2e9e3aed36`, the same blob MX-r-11 shipped, and `grep -c '_pf_need'` on it reads 0** -- the
trunk's pre-flight loop has never reached the host, so cone protection remains entirely applier-side, which is
why the order now carries it as a cut-template rule.
