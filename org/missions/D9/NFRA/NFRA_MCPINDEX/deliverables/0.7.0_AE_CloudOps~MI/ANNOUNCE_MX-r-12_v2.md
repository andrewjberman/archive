# ANNOUNCE -- MX-r-12 v2 PHASE A: the catalog-only release carrying the six research rows, cut on live `027fedfda4`

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-12.depth-v4-release.md` at **A6** (the
governing amendment). GO: msg 33971. Probes:
`deliverables/0.7.0_AE_CloudOps~MI/probes_r12v2/` (every file named below is there).

**STATE: PHASE A ONLY.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no apply, no
push. AWS contact, all read-only and Opal's own: S3 `head-object` (3 keys) and one SSM read (file hashes, `.env`
KEY NAMES parsed in Python, `/health`). No `.env` value was read or printed. No source file was edited.

## 0. WHAT v2 IS -- exactly 1 file, and what it closes

| file | live blob (at `027fedfda4`, v1) | shipped blob (MX-c-9 A3+A4, @`422e58c43b`) | +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `f15b34826312e3735a79b6c17dea7e0deea9ec81` | **`d180a6d86b339bedfd5aa72ee324159064f365fc`** | +105 / -3 |

The shipped blob was **resolved with `git rev-parse 422e58c43b:<path>`, never typed**, and the issuer's
abbreviation `d180a6d86b` then asserted as a prefix of what resolved. It is **equal at `box/sitez` HEAD**, so
nothing drifted since the drain.

**The cut's file list (printed, 1 of 1):**
1. `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`

**WHAT v2 CLOSES, measured from both catalogs rather than quoted** (`v2_substance.txt`): `harvest_datasets` goes
**33 -> 39 rows (+6)**, and the six new prefixes are exactly the hyphenated legacy-addressed research tables now
admitted by the naming-gate branch (`0fce89bb11`):

```
+ amgt/harvest/gold/research-backlog/
+ amgt/harvest/gold/research-continuation/
+ amgt/harvest/gold/research-dossier/
+ amgt/harvest/gold/research-fund-form/
+ amgt/harvest/gold/research-model-typecast/
+ amgt/harvest/gold/research-sector-template/
```

So FWD-21 moves from **1 of 7 research tables to 7 of 7** -- the gap A4 deliberately shipped short while the gate
had no owner, now closed. All six new rows carry **`read_tool: None`** (6 of 6), which is the CAUSE of the
link-count result in section 3 rather than a coincidence beside it.

## 1. THE LIVE REF, READ FROM THE HOST BY HASH

| plane | read (UTC) | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the tree at `027fedfda4`** (sha256 per file, SSM `fe40e796-6edd-4d6c-b421-ae21b8de995a`, 03:46:41Z; `host_read_v2_PRECUT.txt`) | 107 files, common 107, **byte-identical 107, DIFFER 0, cut-only 0, host-only 0** | **the host IS running v1 `027fedfda4`** |
| 2. S3 `-latest` | 561,198 B, ETag `93ebfca9c49030f0395078e3eca7933a` | `git-ref` `027fedfda48714721deeddf41b87e0de6a5c0266` |
| host service | same SSM read | `/health` **200**; 54 `.env` keys; 7 integration ids |

## 2. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`027fedfda48714721deeddf41b87e0de6a5c0266`** (v1, serving since 03:09:52Z) |
| **DEPLOY-ONLY COMMIT (v2)** | **`43088464f51c81e9fe3528b080c6ca8ce5fa90fe`** (single parent = the base; `git commit-tree` plumbing on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override) |
| deploy-only tree (repo root) | `ef1fe5c85530f7fb650ce77533750fe9541be477` |
| deploy tree | `C:/tmp/mx-dep-r12v2` -- **NEW**, as A6 requires, sparse, detached, never merged, never pushed, `worktree lock`ed |
| cone | `.tools`, `data/transcripts/scripts/teams`, `infra/aws/ec2/opal-gateway`, **`infra/logic/registry`**, `lib`, `org/mcp/inbox/0.7.0_AE_CloudOps`, `org/standards`, `org/tier2_senior/0.7.0_AE_CloudOps`. The closure oracle was EXERCISED, not inventoried: both `lib.opal_naming.address()` calls resolve from this tree |
| **deploy tree HEAD IS the deploy-only commit** | **YES** -- `rev-parse HEAD` = `43088464f51c81e9fe3528b080c6ca8ce5fa90fe`; the working catalog's `hash-object` = `d180a6d86b...`, so the label will name the shipped bytes (ruling 2c / row `Z-S92`) |
| deploy tree cleanliness | `git status --porcelain` = **0 lines, whole tree** |
| artifact keys the apply will write | `opal-gateway-43088464f5.tar.gz` and `-latest`, both `git-ref` = `43088464f51c81e9fe3528b080c6ca8ce5fa90fe`. The versioned key is **404 today** |
| **ROLLBACK ARTIFACT -- V1's ARTIFACT, never further back (A6)** | `opal-gateway-027fedfda4.tar.gz`: **561,198 B, ETag `93ebfca9c49030f0395078e3eca7933a`, `git-ref` `027fedfda4...`**. Its ETag and size EQUAL `-latest`'s today, so the handle is real and is what is serving |
| mcportal pin | `0e02a1f` unmoved; the bun clearance at that lockfile has read `77 of 77` rc=0 on every apply today, with a planted-package arm reading `77 of 78` rc=1 |
| `deploy-to-ec2.sh` in the cut | `2e9e3aed368ce0da2690f77deac3c688d1b90141` -- **byte-equal to the live base's**, so that VOID condition stays false |
| new NEVER-2 ledger | `nfra-mcpindex-r11-catalog-release-v2`, opened at PHASE B. AC1 is re-pointed to `round11/checks/r12v2.AC1.sh` -- **verified present, and the re-point is in the order's `<proof_of_spec>` at HEAD, not only in A6's prose** |
| Terraform | none |

## 3. THE CENSUSES -- all four EQUAL (`censuses_v2.txt`)

| census | live `027fedfda4` | cut `43088464f5` | verdict |
|---|---|---|---|
| served tools (in-process, `MOCK_GRAPH=1`) | 67 (native 43 + integration 24) | 67 (native 43 + integration 24) | **names EQUAL**, added `[]` removed `[]`; drop-one control reads `EQUAL False` |
| `.env` KEY set (keys only, never values) | host 54 (distinct 54) | rendered 54 (distinct 54) | **dropped `[]`, added `[]`** |
| `ENABLED_INTEGRATIONS` | 7 ids | 7 ids | **difference EMPTY, `EQUAL`** |
| **MC Portal per-tool link counts** | **11 tools / 14 links** | **11 tools / 14 links** | **`per_tool_link_counts EQUAL`** -- tools added `[]`, removed `[]`, counts changed `[]` |

**The link-count result has a cause, not just a reading:** all six new harvest rows carry `read_tool: None`, and
`_catalog_read_tool_rows()` only records a row when `read_tool` is a non-empty string. So a catalog that grows by
six rows adds zero links BY CONSTRUCTION -- which is worth stating because the opposite result would have made
the slot conditional on MP-z-6, and "the counts happened to match" is a weaker claim than "no new row can
contribute a link". Per-tool: `schwab_query` 4, the other ten 1 each.

**NOTE on the mechanism:** off-host the counts come from ast-extracting the reader's own
`_catalog_read_tool_rows` and exec'ing it with `CATALOG_YAML` bound per tree, because the gateway's `starlette`
exists only in the host venv. That mechanism was validated against the real module import on the host during v1
(11/14 both ways, per-tool `EQUAL True`), and the host-side control is taken again at the v2 apply. The `CONTROL
exec-vs-real-import EXC` line in `censuses_v2.txt` is the expected off-host reading, not a failure.

## 4. THE CUT METHOD, and its control

`git diff 027fedfda4 43088464f5`: **1 file**, `numstat 105 3`, **0 files outside the gateway dir**, parent count
**1** and the parent IS the live ref.

**NEGATIVE CONTROL:** `git diff --name-only 43088464f5 box/sitez -- infra/aws/ec2/opal-gateway` reads **37
paths**, `deploy-to-ec2.sh` among them. A merge of `box/sitez` would have shipped 37 files instead of 1 and voided
the halves on the deploy script alone. v2 is therefore a **single-blob overlay** on the live ref's tree -- a
temporary `GIT_INDEX_FILE` seeded from `027fedfda4`, one `update-index --cacheinfo`, `write-tree`, `commit-tree`.

## 5. PHASE B -- NOT STARTED; what it does

1. Re-read the live ref from the HOST by hash. If it is not `027fedfda4`, STOP: these pins are void.
2. Halt gate from the deploy tree as a PAIR, `HALT_OVERRIDE` forbidden. The valid negative arm defeats **both**
   limbs the gate reads (the session `.serial` file and the EXPORTED `$OPAL_AGENT_SERIAL`); arms built on
   `AGENT_NAME` or on the session id alone read rc=0 and prove nothing. Mail guard is Rule 18a's broker read.
3. Open `nfra-mcpindex-r11-catalog-release-v2` with entry AND sentinel **committed together** -- and read the
   tool's output, because its `open` staged nothing on the v1 run and only printed the safe-commit line.
4. `DEPLOY_BASE_REF=027fedfda48714721deeddf41b87e0de6a5c0266 AGENT_NAME=0.7.0_AE_CloudOps~MI bash
   infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from
   `C:/tmp/mx-dep-r12v2`.
5. **Labels read back BEFORE the first leg closes:** `opal-gateway-43088464f5.tar.gz` present, `-latest`'s
   `git-ref` equal to the cut, and the rollback key `opal-gateway-027fedfda4.tar.gz` unchanged at ETag
   `93ebfca9...`.
6. `/health`; the host census against the cut with the v1 tree as the negative control (expect **DIFFER 1** = the
   catalog); the four censuses equal again INCLUDING the link counts by real module import; then `r12.AC2` and
   `r12.AC3` verbatim.
7. Plane 2: `deployed_commit` `43088464f5...`, `previous_deployed_commit` `027fedfda4...`, and a `release_note`
   naming THIS release **in the same write as the commit fields** (row `NFRA_MCPORTAL-Z-S49`).
8. Close the ledger, then `r12v2.AC1`, write the proof instance, report the close by 10:00Z.
9. On any failed read-back, roll back to `opal-gateway-027fedfda4.tar.gz` and **never further**.

## 6. NOT PROVED HERE

- The served effect: only the apply shows it. `r12.AC2` and `r12.AC3` are re-run on v2 against the deployed bytes.
- That the six research rows are *served* as 7 of 7: measured here in the shipped catalog's bytes, but the host
  reads it only after the apply.
- The never-widen pair: a fresh pair is signed on these pins before the GO. This document is the ask's input.
- `r12v2.AC1`: its limbs grade a CLOSED ledger, and no v2 ledger is open yet.

## 7. ROWS

None new from PHASE A. v1 is complete and CLOSED (`nfra-mcpindex-r11-catalog-release`, 5 legs, @`0dc0ddac4c`), and
its proof instance records the standing rows this chain rests on.
