# ANNOUNCE -- MX-r-11 v2: the two re-derived `definition:` citations, cut on live `ad2acc0a93`

Cut by `0.7.0_AE_CloudOps~MI` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-11.catalog-tool-index-release.md`, **A5 step 2**
(ruling `Z-S112` @`96c5b4a9fe`). Continuation: msg 33831. Probes:
`deliverables/0.7.0_AE_CloudOps~MI/probes_r11_phaseb/` (every file named below is there).

**STATE: THE CUT ONLY.** Nothing deployed, nothing uploaded to S3, no new ledger, no Terraform, no apply, no push.
The ledger `nfra-mcpindex-r10-catalog-release` stays **HELD** with **L3 open** -- v2's apply closes it as a second act
on the SAME entry, per A5. AWS contact since the v1 apply, all read-only and Opal's own: S3 `head-object` (4 keys) and
two SSM `AWS-RunShellScript` reads (file hashes, `.env` KEY NAMES parsed in Python, `/health`). No `.env` value was
read or printed. No source file was edited.

## 0. WHAT V2 IS -- exactly 1 file, 5 lines, MX-c-8 A1's bytes

| file | v1 blob (at `ad2acc0a93`) | shipped blob (MX-c-8 A1, @`972e25715e`) | +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `98d15ca9ad038e2e3d8c3f2b0dbf5b365d16fd45` | **`54afa75ea14bce0e88709b2e1fa04f14d5a960c1`** | +5 / -5 |

(The path is under `infra/aws/ec2/opal-gateway/`.) The blob the issuer named, the blob at the A1 drain and the blob at
`box/sitez` HEAD are all `54afa75ea1...` -- three reads, one value.

**The cut's file list (printed, 1 of 1):**
1. `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml`

**The 5 lines, printed in full** (`git diff 98d15ca9ad 54afa75ea1`):

```
-    definition: app/integrations/opal_discover/integration.py:761     (opal_describe)
+    definition: app/integrations/opal_discover/integration.py:818
-    definition: app/integrations/opal_discover/integration.py:751     (opal_discover)
+    definition: app/integrations/opal_discover/integration.py:808
-# BUILT BY: workflows/atom_decomposition/emit_catalog_v02.py at git HEAD edc544ba75
+# BUILT BY: workflows/atom_decomposition/emit_catalog_v02.py at git HEAD 96c5b4a9fe
-built_at_git_head: edc544ba75
+built_at_git_head: 96c5b4a9fe
-  # one entry per tool served by the gateway at services.opal-gateway.deployed_commit (185dc04888): the denominator
+  # one entry per tool served by the gateway at services.opal-gateway.deployed_commit (ad2acc0a93): the denominator
```

That is the issuer's specification exactly: the two `definition:` values (`:818`, `:808`), the two built-by stamps and
the census-commit comment. **The two new values are the +57 shift this seat measured when it refused `r11.AC2` on v1**
(`761 -> 818`, `751 -> 808`; cited lines read `hit=False`, cited+57 read `hit=True`, and the definition file's own
`numstat` against the base read `57 0`). So the fix is the measurement, not a guess.

## 1. THE LIVE REF, READ FROM THE HOST BY HASH -- not from `-latest`'s label

| plane | read (UTC) | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the deploy tree at `ad2acc0a93`** (sha256 per file, SSM `62336125-f8f2-44bf-999e-6d6baed5e27f`, 23:32:16Z; `host_read_V2_PRECUT.txt`) | cut/tree 107 files, host non-dashboard 107, common 107, **byte-identical 107, DIFFER 0, cut-only 0, host-only 0** | **the host IS running v1 `ad2acc0a93`**, established without trusting any metadata |
| 2. S3 `-latest` metadata (`rollback_and_target_keys_V2.txt`) | 557,616 B, ETag `dcfd3a2fc063d7ad97a11d2ad827f429`, LastModified 2026-10-13T22:51:29Z | `git-ref` `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203` |
| 3. `EC2_MANIFEST.json` plane 2, `box/sitez` | `deployed_commit` `ad2acc0a93...`, `previous_deployed_commit` `64b3e54658...`, `mcportal_commit` `0e02a1f` | AGREES (committed `62079e4a4c`; row `Z-W33-S6`'s lag is resolved -- MP-z-5's record drained) |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 54 `.env` keys |

All three planes name `ad2acc0a93`. Unlike v1's cut, plane 2 agrees this time.

## 2. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`** (v1, serving since 22:51:28Z) |
| **DEPLOY-ONLY COMMIT (v2)** | **`7eff14b2e620c8c1f688d41de6f37c09addde7b4`** (single parent = the base; `git commit-tree` plumbing on a TEMPORARY index, author and committer `0.7.0_AE_CloudOps~MI`, no hook, no override) |
| deploy-only tree (repo root) | `9710202e858c772dabac58eede72c2a56cd426d8` (v1's tree was `f9b34e1b63`) |
| deploy tree | `C:/tmp/mx-dep-r11` (the same tree v1 shipped from, as A5 directs), sparse, detached, never merged, never pushed |
| **deploy tree HEAD IS the deploy-only commit** | **YES** -- `rev-parse HEAD` = `7eff14b2e620c8c1f688d41de6f37c09addde7b4`; the working `DATA_CATALOG.yaml`'s `hash-object` = `54afa75ea1...`, so the label will name the shipped bytes (ruling 2c / row `Z-S92`) |
| deploy tree cleanliness | `git status --porcelain -- infra/aws/ec2/opal-gateway/` = **0 lines**. One tracked file is modified outside `$SRC` (`infra/aws/ec2/EC2_MANIFEST.json`, the v1 wrapper's own write, left uncommitted on purpose) -- it is outside the tar and outside the newer script's dirty-tree limb |
| artifact keys the apply will write | `opal-gateway-7eff14b2e6.tar.gz` and `-latest`, both `git-ref` = `7eff14b2e620c8c1f688d41de6f37c09addde7b4`. The versioned key is **404 today** (absent), as it must be |
| **ROLLBACK ARTIFACT -- V1's ARTIFACT, never the base** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-ad2acc0a93.tar.gz`: **557,616 B, ETag `dcfd3a2fc063d7ad97a11d2ad827f429`, `git-ref` `ad2acc0a9305456e5bac4d7fd2cc5cd42642b203`**, LastModified 22:51:28Z. Its ETag and size EQUAL `-latest`'s today, so the handle is real and is what is serving. A5: v1 is the working state. One step back is `opal-gateway-64b3e54658.tar.gz` (551,109 B, ETag `527cab0d...`), still present and unchanged |
| mcportal pin the dashboard build resolves | `0e02a1f1ab56dae65b9df29bd78f1eab319ce6a2` (`MCPORTAL_RESOLVE_ONLY=1` from the v2 tree, rc 0). **UNMOVED** from v1 and from MP-z-5, so the bun-lock clearance measured during v1's apply still stands on the same lockfile (`77 of 77` rc=0, with a planted-package negative control reading `77 of 78` rc=1). It is re-run at the apply regardless, since it costs one read |
| `deploy-to-ec2.sh` in the cut | `2e9e3aed368ce0da2690f77deac3c688d1b90141` -- **byte-equal to the base's and to v1's**, so the halves' VOID condition "a `deploy-to-ec2.sh` other than the base's" stays false. Note this is NOT `box/sitez`'s copy (`76a4f20a6f`); see row `Z-S109` |
| Terraform | none |

## 3. THE CENSUS -- exactly 1 file differs from the live host

`git diff ad2acc0a93 7eff14b2e6`:

| | |
|---|---|
| files changed | **1**: `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml` |
| lines | **5 insertions, 5 deletions** (`numstat` `5 5`) |
| files OUTSIDE `infra/aws/ec2/opal-gateway/` in the diff | **0** |
| parent count | **1**, and the parent IS `ad2acc0a93` |
| v2's blob at that path | `54afa75ea14bce0e88709b2e1fa04f14d5a960c1` = the A1 drain's |

**THE NEGATIVE CONTROL THAT MATTERS, and it is not cosmetic.** The issuer warned that the trunk carries other
projects' gateway changes. Measured: `git diff --name-only 7eff14b2e6 box/sitez -- infra/aws/ec2/opal-gateway` reads
**44 paths**, among them `app/tools.py`, `app/audit.py`, `app/destructive_ops.py`, `app/data_entitlement.py`,
`app/harvest_read.py`, `app/identity_scope.py`, `app/refs/silver_families.json` and `deploy-to-ec2.sh` itself. **A
merge of `box/sitez` would have shipped 44 files instead of 1** and would have voided both halves on the deploy script
alone. v2 was therefore cut as a SINGLE-BLOB overlay on v1's tree -- a temporary `GIT_INDEX_FILE` seeded from
`ad2acc0a93`, one `update-index --cacheinfo`, `write-tree`, `commit-tree` -- which also kept the deploy tree's
modified `EC2_MANIFEST.json` out of the tree by construction rather than by care.

## 4. THE THREE EQUAL CENSUSES (before = the LIVE host at v1, after = rendered from / run on the v2 cut)

**Tool census, in-process (`MOCK_GRAPH=1`, the 7 live ids; `tools_v2.json`, `censuses_v2.txt`):**

| | native | integration | total |
|---|---|---|---|
| live host (serving v1), served names | 43 | 24 | **67** |
| v1 cut | 43 | 24 | **67** |
| **v2 cut** | 43 | 24 | **67** |
| added / removed (v2 vs live host) | | | **none / none**, names EQUAL |
| added / removed (v2 vs v1 cut) | | | **none / none**, names EQUAL |

**67 = 67. NEGATIVE CONTROL: dropping one name from v2's set makes the same comparison read `EQUAL False`**, so the
equality is a measurement. v2 changes a YAML data file and no Python, so the tool set *cannot* move -- and it was
measured anyway rather than argued.

**`.env` KEY set (keys only, never values; `censuses_v2.txt`):** rendered from the v2 cut's own `deploy-to-ec2.sh`
**54** (distinct 54); live host **54** (distinct 54); **dropped `[]`, added `[]`**.

**`ENABLED_INTEGRATIONS`:**

| | ids |
|---|---|
| before (live host, 23:32:16Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7**) |
| after (rendered from the v2 cut's own script) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7**) |
| **difference** | **EMPTY** -- `EQUAL`. 7 = 7 |

No widening on any of the three.

## 5. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 13 of 13 sentinels** (`open_ledgers_V2.txt`): 4 OPEN and 5 HELD, and the
only gateway-host entry is **this project's own** `nfra-mcpindex-r10-catalog-release` [HELD-SOVEREIGN-GATED, L3 open],
which is the entry v2's apply closes. `nfra-mcpindex-r7-bd-doc-retire` is also listed (OPEN, stranded L5, in-window at
17.6 h of 192 h, this seat's author line) -- a bd-doc retire, not this host and not this act. No other seat holds the
gateway slot. **No new ledger is opened for v2**, per A5: the apply is a second act on the same entry.

## 6. THE V2 APPLY -- NOT STARTED; what it does

1. Re-read the live ref from the HOST by hash. If it is not `ad2acc0a93`, STOP: these pins are void and the document is
   re-cut, not patched.
2. Re-run the bun-lock pre-check at `0e02a1f` with both arms (the pin has not moved; one read).
3. Halt-gate proof from the deploy tree as a PAIR (negative rc=3, positive rc=0). `HALT_OVERRIDE` is forbidden. The
   pre-apply mail guard is Rule 18a's PRIMARY limb, the broker read -- never a HALTGT pass.
4. `DEPLOY_BASE_REF=ad2acc0a9305456e5bac4d7fd2cc5cd42642b203 AGENT_NAME=0.7.0_AE_CloudOps~MI bash
   infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, run from
   `C:/tmp/mx-dep-r11`. The sparse cone already carries the closure the deploy needs (`lib`, `infra/logic/registry`,
   `org/standards`) -- rows `Z-S108` / `Z-S111`, so the v1 failure does not recur.
5. **Read the labels back BEFORE L3 closes:** `opal-gateway-7eff14b2e6.tar.gz` present and `-latest`'s `git-ref` equal
   to `7eff14b2e620c8c1f688d41de6f37c09addde7b4`; confirm the ROLLBACK key `opal-gateway-ad2acc0a93.tar.gz` is
   unchanged (557,616 B, ETag `dcfd3a2f...`).
6. Then `/health` 200, the host byte census against the v2 cut with v1's tree as the negative control, the three
   censuses equal again, and **`r11.AC2` -- which must now read `definitions located 67 of 67` and `index rc=0`** --
   then `r11.AC3`.
7. **L3 closes on those read-backs**; then plane 2 records `deployed_commit` `7eff14b2e6...` with
   `previous_deployed_commit` `ad2acc0a93...`; then the ledger CLOSES; then `r11.AC1`.
8. On any failed leg, roll back to **v1's artifact** `opal-gateway-ad2acc0a93.tar.gz`, never the base.

## 7. NOT PROVED HERE

- The served effect: only the apply shows it. `r11.AC2` on v2 (definitions 67 of 67) and `r11.AC3` are graded after the
  apply, against the deployed bytes.
- That `:818` and `:808` satisfy `definition_ok()` **on the host**. They satisfy it against the shipped file in this
  tree, and MX-c-8 A1's `c8.AC1` reads `definitions located 67 of 67` on the re-derived catalog -- but both are
  pre-apply reads of the same bytes, not a read of the running gateway.
- The never-widen pair: a FRESH pair is signed on these pins before the GO. This document is the ask's input, not a
  substitute for it.
- `r11.AC1`: its limbs grade a CLOSED ledger, and the ledger is correctly still HELD.

## 8. ROWS

None new. `Z-S108`, `Z-S109`, `Z-S111` are INERT as filed and their durable fixes go to the round-10 analysis per A5
(the deploy tree's sparse cone must include `infra/logic/registry`; the ANNOUNCE blob figure; the `_pf_need` loop that
stats `lib/opal_naming.py` without reading a registry JSON). `Z-S110` is ruled by `Z-S112` and this cut is its remedy.
