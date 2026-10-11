# ANNOUNCE -- MX-r-10 PHASE B v2: the operations-lead catalog release, RE-CUT on live ref `6aadf7db37`

**By:** `0.7.0_AE_CloudOps~MX`, site Z, 2026-10-11 ~12:2x-12:4xZ.
**Order:** `NFRA_MCPINDEX.TO-MX-r-10.ops-readers-release.md`, AMENDMENT A1 `@b86b05a653`, `<risk>WORLD</risk>`.
**GO:** `2.0.0_SA_COO~MI` msg 33268 (A1 at-the-slot items 1-3): re-cut, write this ANNOUNCE, then STOP.
**Supersedes:** PHASE A v1 `deliverables/0.9.0_WK_NFRA_MCPINDEX~30/ANNOUNCE_MX-r-10.md` (drained `@11cb1ee6e9`),
whose deploy-only commit `a9c23fe126` on base `2a5966dfbd` is **VOID by its BASE-MOVED clause**: OG-rl-16 moved the
live ref.

**NOTHING WAS UPLOADED AND NOTHING WAS DEPLOYED.** No artifact was built, no S3 key written, no SSM run beyond
read-only probes, no ledger opened. The target key is still 404. This is the cut and its censuses only.

## 0. WHAT THIS RELEASE IS

MX-c-7's regenerated catalog plus its `opal_discover` change (E2: the folds retired, E-13's note surfaced), cut on
the live tree. **Exactly 2 files**, unchanged in content from v1 -- only the base moved.

| file | live base blob | shipped blob (MX-c-7, box/sitez HEAD) | +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `da94d7cc64456915f00d9825f716b2ce7c4a9d32` | `d0bddad2f11ae0983171f82304bb239b842d8298` | +95 / -4 |
| `app/integrations/opal_discover/integration.py` | `7f45517f274ee7cf323fc2126e492d57c0f3abe0` | `a8fd2fa900d331121d51ea0f20a5cec4a5ef3dbe` | +15 / -11 |

Those two base blobs are MX-r-9's own shipped bytes, so the chain from round 8 is unbroken.

**NO READER SHIPS.** Order section 1 item 2 anticipates `ENABLED_INTEGRATIONS` widening "by exactly the SERVED
readers' ids", and **A1 superseded that**: MX-o-1 and MX-o-2 both landed as GAP readers, so no reader folder and no
registry hookup line ship, and the id difference is EMPTY. This release has **no widening at all** -- the halves
should read it as a content release of one existing integration plus its catalog, not as a widening to be bounded.

## 1. THE LIVE REF, READ FROM THE HOST BY HASH -- not from `-latest`'s label

Order item 0 and the GO both require the live ref be read from the host, because a label is exactly what MX-r-9's
row `Z-S92` proved can lie. The decisive read is the first row: **the host's own bytes against the git tree at the
candidate ref.** The label rows are corroboration, printed because they agree.

| plane | read (UTC) | value |
|---|---|---|
| **1. HOST BYTE CENSUS vs the TREE at `6aadf7db37`** (sha256 per file, SSM `3c00486d-f472-4df0-8a1e-e1b1fbf6d9b0`, 12:20:15Z) | **106 of 106 common files byte-identical, 0 DIFFER, 0 cut-only, 0 host-only** | **the host IS running `6aadf7db37`**, established without trusting any metadata |
| 2. host vs the extracted `-latest` artifact | artifact 109 files, host 113, common 109, **109 byte-identical, 0 DIFFER, 0 artifact-only**, 4 host-only (all `dashboard/assets/`) | agrees |
| 3. S3 `-latest` metadata `git-ref` | 538772 B, ETag `64956b0c6e7f2c6869f3ba49353ce101`, LastModified 2026-10-11T11:49:02Z | `6aadf7db37a8605389110e08bb64f6e15e1d3026` |
| 4. `EC2_MANIFEST.json` `services.opal-gateway` | `deployed_at` 2026-10-11T11:49:30Z by `0.7.0_AE_CloudOps~Z` | `deployed_commit` `6aadf7db37...`, `previous_deployed_commit` `2a5966dfbd...`, `mcportal_commit` `bc37107` |
| host service | same SSM read | `/health` **200**; `ENABLED_INTEGRATIONS` 7 ids; 113 files censused |

All four planes name `6aadf7db37`. The base is `6aadf7db37a8605389110e08bb64f6e15e1d3026` -- OG-rl-16 3/3
(`rel-nfra-oplgtw-r16b`), the E2 carry, whose ledger `nfra-oplgtw-gateway-release-e2` CLOSED 12:05Z `@a54fa42da7`.

**The 4 host-only dashboard assets are row `NFRA_MCPINDEX-Z-S94`, behaving exactly as that row predicted.** They
were 2 when I filed it after MX-r-9 (`index-BP6X9XJd.js`, `index-BqfQgt7G.css`); MP-r-2's rebuild replaced the live
bundle and left its predecessor behind too, so they are now 4 (`+ index-CrZMj-00.js`, `+ index-a6wjv_wv.css`). The
deploy extracts over the directory and prunes nothing, so the set grows by one pair per mcportal content-hash
change. None is referenced by the served `index.html`. The difference is **one-directional** -- artifact is a subset
of host, 0 artifact-only -- which is the only reason the preservation census above is sound as an equality claim.
Remedy remains the gateway surface's, not this order's.

## 2. THE PINS (v2)

| field | value |
|---|---|
| base = LIVE ref | **`6aadf7db37a8605389110e08bb64f6e15e1d3026`** |
| base gateway tree | `1e829eac3eeb5f04f341c45c1aa181dabf0b17e2` |
| **DEPLOY-ONLY COMMIT** | **`c3af8687e44a1e641259b37f992033ae02cdce3d`** |
| its parent | `6aadf7db37...` (the base), single parent |
| deploy-only tree (repo root) | `dfa22ce071a8f63aeb1309012a632a2afc96a0f1` |
| cut gateway tree | `aa6ebeee7cc65861468bb7850422eae402c61600` |
| author / committer | `0.7.0_AE_CloudOps~MX <0.7.0_AE_CloudOps~MX@opal.agent>`, `git commit-tree` plumbing, no hook, no override |
| deploy tree | `C:/tmp/mx-dep-r10`, sparse cone (`infra/aws/ec2/opal-gateway`, `.tools`, `data/transcripts/scripts/teams`), detached, **`git status --porcelain` = 0 lines**, NOT merged into `box/sitez` (`is-ancestor` rc=1), never pushed |
| **deploy tree HEAD IS the deploy-only commit** | **YES** -- `rev-parse HEAD` = `c3af8687e4...`, `rev-parse --short HEAD` = `c3af8687e4`. This is order item 0 / ruling 2c / row `Z-S92`, and it is the whole reason the artifact will be named and stamped correctly |
| artifact keys the apply will write | `opal-gateway-c3af8687e4.tar.gz` and `-latest`, both to carry `git-ref` = `c3af8687e44a1e641259b37f992033ae02cdce3d` |
| **ROLLBACK ARTIFACT (the VERSIONED key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-6aadf7db37.tar.gz`: **538772 B, ETag `64956b0c6e7f2c6869f3ba49353ce101`, `git-ref` `6aadf7db37...`**, LastModified 11:49:00Z. Its ETag and size equal `-latest`'s today, so the handle is real. One step back: `opal-gateway-2a5966dfbd.tar.gz` (535420 B, ETag `8a06aaa1...`) |
| target key today | `opal-gateway-c3af8687e4.tar.gz` -- **404, absent**, as it must be before the apply |
| mcportal pin the dashboard build uses | `bc37107aa587d487aac57fcc3def0557523498ac` (`MCPORTAL_RESOLVE_ONLY=1`, rc 0, nothing built or uploaded). **UNMOVED** from v1 |
| Terraform | none |

## 3. THE CENSUS -- exactly 2 files differ from the host

`host_vs_cut.py` against the deploy tree at the cut, over the SSM host read (dashboard excluded on the host side,
since the artifact's dashboard is rebuilt at the pin and is covered by section 5):

| | |
|---|---|
| cut files / host non-dashboard files | **106 / 106**, common 106, cut-only **0**, host-only **0** |
| byte-identical | **104 of 106** |
| DIFFER | **2: `app/integrations/opal_discover/integration.py`, `app/refs/DATA_CATALOG.yaml`** |
| expected changed set (exactly those 2) | **MATCH** |

The same probe against the deploy tree at the BASE read **0 DIFFER over the same 106**, which is simultaneously the
live-ref confirmation in section 1 and the proof that these 2 files are the entire delta this release introduces.
Every other live file is preserved by construction: the cut is the base tree with two blobs replaced.

## 4. `ENABLED_INTEGRATIONS`, the `.env` key rule, the tool census

`.env` rendered from **the cut's own `deploy-to-ec2.sh`**, keys only, never values:

| | value |
|---|---|
| `ENABLED_INTEGRATIONS` before (host, 12:20:15Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7**) |
| after (rendered from the cut) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (**7**) |
| **difference** | **EMPTY** -- `EQUAL`. No reader ships (both are GAP), so there is no widening |
| `.env` KEY SET | **53 rendered = 53 host**, distinct 53 both sides; **0 dropped, 0 added** |
| both principal keys | `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS` present on both sides |

**The key count is 53, not MX-r-9's 52, and this release did not move it.** `ADVI_FEE_STATEMENT_S3_ROOT` arrived
with OG-rl-16's E2 carry and is present on BOTH sides here. This is why the bound is A3's **rule** -- before equals
after, read from the then-live ref at the act -- and never a remembered count: a half carrying "52" forward from
round 8 would false-alarm on a key this release never touched.

**Tool census, in-process at `MOCK_GRAPH=1` over the 7 live ids** (`tools_census.py`, live = the extracted
`-latest` artifact, cut = the deploy tree):

| | native | integration | total |
|---|---|---|---|
| live | 43 | 24 | **67** |
| cut | 43 | 24 | **67** |
| added by the cut | | | **none** |
| removed by the cut | | | **none** |

**67, not MX-r-9's 66, and `copy_site_file_to_s3` is now present on BOTH sides.** MX-r-9's halves required that
tool ABSENT because E2 was then unreleased; OG-rl-16 released it. A half applying round 8's expectation here would
read a correct state as a violation. What this release must show -- and does -- is that the sorted tool-name sets
are **equal**, difference empty in both directions.

**The deploy script is the live base's own copy, not `box/sitez` HEAD's** (A2's rule): cut blob
`9dde5ab993e06d34db8bddceb2557f80e1c33283` == base blob, byte-identical (`git diff --quiet` rc=0), while
`box/sitez` HEAD's is `a020fbf456823e8a371a1f131e7fa514497ab46c` -- a different blob. The positive control runs
both ways, so this is an identity, not an unread assumption.

## 5. THE DASHBOARD BUILD -- clearance re-measured on the v2 pins

The pin did not move (`bc37107`), but the clearance is re-measured here because the halves sign the v2 pins:

| arm | input | reading | exit |
|---|---|---|---|
| PASS | `bun.lock` at `bc37107aa5...`, git blob `0f4b0c92f1`, **30903 B, sha256 `7e6b71c2ea387656...`** | **77 of 77** | **0** |
| NEGATIVE CONTROL | the same lockfile with `react@19.3.0` altered to `react@19.9.99` (2 places) | **75 of 77**, naming `react@19.9.99 absent` and `@types/react@19.9.99 absent` | **1** |

So no package would be fetched from the internet at build time (OG-bi-1), and the precheck discriminates rather
than passing vacuously.

**One reading note for anyone reproducing this on site Z:** the same lockfile reads **31181 B** on disk in a fresh
worktree here, not 30903. The delta is exactly 278 bytes and the file is exactly 278 lines -- the checkout applies
CRLF. The figures above are the **git blob's** (LF, content-addressed), which is what v1 recorded and what any
device reproduces; the precheck passes 77 of 77 against either form.

## 6. OPEN LEDGERS

`deploy_ledger.py check`, **SCAN DENOMINATOR 22 of 22 sentinels scanned**:

- **No entry exists for `nfra-mcpindex-r9-ops-readers-release`** -- correct, PHASE B has not started. It is opened
  at PHASE B start, per order item 3.
- **`nfra-oplgtw-gateway-release-e2` is absent from the open set** -- i.e. closed, agreeing with the issuer's
  12:05Z `@a54fa42da7`. The gateway slot is genuinely free.
- Other entries in that output (OPEN and HELD) belong to other seats and other projects; none is this order's and
  none is this seat's to touch. Reported as read, not acted on.

## 7. WHAT PHASE B WILL DO -- NOT STARTED

On the halves plus the full GO, in this order:
1. Re-read the live ref from the host by hash. **If it moved, STOP** -- these pins go VOID by the same clause that
   voided v1's.
2. Open the NEVER-2 ledger `nfra-mcpindex-r9-ops-readers-release`. Legs: upload/ship, `/health` 200, r10.AC2.
3. Apply through `deploy-to-ec2.sh` from the deploy tree with `DEPLOY_BASE_REF=6aadf7db37...`, HEAD at the cut.
   Materialise the base agent folder in the sparse cone first (MX-r-9 A5) and print the halt gate's verdict with its
   negative control. `HALT_OVERRIDE` is forbidden.
4. **Read the labels back BEFORE the first leg closes** (order item 0): `opal-gateway-c3af8687e4.tar.gz` present and
   `-latest`'s `git-ref` equal to `c3af8687e4...`. A correct service under a wrong label is the round-8 defect and
   is not acceptable here.
5. `/health` 200, then r10.AC1 and r10.AC2 verbatim. Roll back to the versioned base artifact on any failed leg.
6. Proof instance at the order's `<instance_path>`.

**One thing PHASE B should expect to refuse as written:** the order's `<instance_path>` names
`deliverables/0.9.0_WK_NFRA_MCPINDEX~30/`, worker ~30's folder. The owned-paths lane rule
(`TREE_DELIVERABLES`, clause 4) permits only the serial named by the sub-folder, so this lane cannot write there --
the identical conflict MX-r-9 hit, which the issuer resolved by amendment A7 moving the path. Flagging it now so it
can be amended with the halves rather than discovered at the close.

## 8. REPORTED

Deploy-only sha **`c3af8687e44a1e641259b37f992033ae02cdce3d`**; this ANNOUNCE at
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MX/ANNOUNCE_MX-r-10_v2.md`; probes beside it in
`probes_r10_v2/`. Now stopping for the two never-widen halves and the full GO, per the GO's item 3.
