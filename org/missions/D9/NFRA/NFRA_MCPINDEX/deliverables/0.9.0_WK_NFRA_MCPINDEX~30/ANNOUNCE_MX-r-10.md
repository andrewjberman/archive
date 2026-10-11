# ANNOUNCE -- MX-r-10 PHASE A: the operations-lead catalog release, cut on live ref `2a5966dfbd`

Deployer of PHASE A: `0.9.0_WK_NFRA_MCPINDEX~30` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-10.ops-readers-release.md`, which follows
`TO-MX-r-9` as amended A1-A7. Pattern: `deliverables/0.7.0_AE_CloudOps~MX/ANNOUNCE_MX-r-9_PHASEB_v2.md`.
Probes: `deliverables/0.9.0_WK_NFRA_MCPINDEX~30/probes_r10/` (every file named below is there).

**STATE: PHASE A only.** Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no grant, role or
sign-in created or changed, no push, `HALT_OVERRIDE` never set. AWS contact, all read-only and Opal's own: S3
`head-object` (4 keys), one `-latest` download, two SSM `AWS-RunShellScript` reads of file hashes and `.env` KEY
NAMES (the host `.env` parsed in Python, never shell-sourced, row Z-S73). No source file was edited.

## 0. WHAT THIS RELEASE IS

**Both readers are GAP, so no reader folder ships, no registry hookup line is needed, and `ENABLED_INTEGRATIONS` does
not widen.** The order's item 2 (a widening by the SERVED readers' ids) therefore has an EMPTY difference. What ships
by content is exactly two files, MX-c-7's output on top of the live ref:

| file | live base blob | shipped blob (MX-c-7 `26e4cee860`) | +/- |
|---|---|---|---|
| `app/refs/DATA_CATALOG.yaml` | `da94d7cc64456915f00d9825f716b2ce7c4a9d32` | `d0bddad2f11ae0983171f82304bb239b842d8298` | +95 / -4 |
| `app/integrations/opal_discover/integration.py` | `7f45517f274ee7cf323fc2126e492d57c0f3abe0` | `a8fd2fa900d331121d51ea0f20a5cec4a5ef3dbe` | +15 / -11 |

(`git diff --stat` base to cut: 2 files, 110 insertions, 15 deletions (numstat 15/11 and 95/4); `probes_r10/diff_base_vs_deployonly_PHASEA.txt`.)
The live blobs equal the blobs MX-r-9 shipped (`da94d7cc`, `7f45517f`), so nothing since MX-r-9 touched either file.
Censuses: E-30 trade reconciliation GAP unowned; E-31 billing GAP `ADVI_BILLING`; E-32..E-35 GAP unowned.

## 1. BASE-MOVED CLAUSE, by REF

**Every pin below is valid ONLY while the live ref is `2a5966dfbd89be9fe6cc0ef3566831e502b81d42`** (NFRA_MCPORTAL
MP-r-2, released 2026-10-10T23:04:36Z, after MX-r-9's `d3c31e972e`). The label was never trusted: the base was read from
the HOST.

| plane | read (UTC) | value |
|---|---|---|
| 1. S3 `-latest` metadata `git-ref` | 01:10:05Z (final re-read); LastModified 2026-10-10T23:04:06Z, 535420 B, ETag `8a06aaa1ee91460aa1ece9f44911f6a5` | `2a5966dfbd89be9fe6cc0ef3566831e502b81d42` |
| 2a. HOST BYTE CENSUS (SSM, sha256 of every deployed file vs the extracted `-latest` artifact) | 00:53:47Z and again 01:10:09Z | **107 of 107 common files byte-identical, 0 DIFFER, 0 artifact-only**; 4 host-only dashboard assets (2 orphans of an older bundle and the 2 of the prior bundle MP-r-2's rebuild replaced; none is in the artifact's `index.html`, which references `index-CKTlb93s.js` and `index-BTe-mgyF.css`) |
| 2b. `EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` at box/sitez `fbeb5b628b` | landed by `9a072fa60a` | `2a5966dfbd89be9fe6cc0ef3566831e502b81d42` (`previous_deployed_commit` `d3c31e972e`, `mcportal_commit` `bc37107`) |

Both planes name `2a5966dfbd`, read twice (00:53Z start, 01:10Z immediately before this ANNOUNCE), all equal. A method
control: the same census run against the live artifact as if it were the cut reads 104 of 104 identical (the
instrument reads 0 DIFFER on the base and 2 on the cut). Its "MISMATCH" line there is an artifact of passing an empty
expected set and is not a finding.

## 2. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`2a5966dfbd89be9fe6cc0ef3566831e502b81d42`** |
| deploy-only tree | `C:/tmp/mx-dep-r10`, sparse cone (`infra/aws/ec2/opal-gateway`, `.tools`, `data/transcripts/scripts/teams`), detached, never merged, never pushed; `git status --porcelain` = 0 lines |
| **DEPLOY-ONLY COMMIT** | **`a9c23fe126de5668a50218360f3485587fadd5b9`** (parent = the base; `git commit-tree` plumbing, author = this serial, no hook, no override) |
| deploy-only tree object (repo root) | `b19e26cf9e6313f70d0c9368a36981df688e012c` |
| artifact keys the apply will write | `opal-gateway-a9c23fe126.tar.gz` and `-latest`, both `git-ref` = `a9c23fe126de5668a50218360f3485587fadd5b9` (the versioned key is absent today, 404) |
| **ROLLBACK ARTIFACT (the VERSIONED key, never `-latest`)** | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-2a5966dfbd.tar.gz`: 535420 B, ETag `8a06aaa1ee91460aa1ece9f44911f6a5`, `git-ref` `2a5966dfbd`; its ETag and size equal `-latest`'s today. The untouched older key `opal-gateway-d3c31e972e.tar.gz` (525792 B, ETag `8e81c942...`) is one step further back |
| mcportal pin the dashboard build uses | `bc37107aa587d487aac57fcc3def0557523498ac` (resolved by `MCPORTAL_RESOLVE_ONLY=1`, rc 0; MOVED from `d60b4e0` by MP-r-2) |
| Terraform | none |

## 3. THE CENSUS -- exactly 2 files differ from the host

`probes_r10/host_vs_cut_PHASEA.txt` and `host_vs_cut_FINAL.txt` (host sha256 against the cut tree's `app/`, `deploy/`
and the two root files):

| | |
|---|---|
| cut files / host non-dashboard files | **104 / 104**, common 104, cut-only 0, host-only 0 |
| byte-identical | **102 of 104** |
| DIFFER | **2: `app/integrations/opal_discover/integration.py`, `app/refs/DATA_CATALOG.yaml`** |
| expected changed set (exactly those 2) | **MATCH**, in both reads |

Git-level preservation (`preservation_PHASEA.txt`, by blob): artifact-root denominator 104 in the base, 104 in the cut,
absent 0, only-in-cut 0, **IDENTICAL 102 of 104, CHANGED 2** (the pair). The whole gateway dir changes in 2 files of
360; files outside `infra/aws/ec2/opal-gateway/` = **0**. Each file was written with `git cat-file blob` and checked by
`git hash-object` against the source blob: 2 of 2 equal.

**What is deliberately NOT cut.** box/sitez HEAD's gateway dir differs from the live base in 35 files (+2556/-175),
including `app/tools.py`, `app/server.py`, `app/destructive_ops.py`, `app/data_entitlement.py`, the unreleased
ADVI_BILLING `site_to_s3.py`, tests and `deploy-to-ec2.sh`. None ships. The deploy script in the cut is the LIVE
REF's copy (byte-identical to the base's; `cmp` IDENTICAL), and HEAD's copy DIFFERS from it (the control), which keeps
HEAD's `.env` and tool changes out of this release.

## 4. `ENABLED_INTEGRATIONS`, the `.env` key rule, the tool census

**ids before and after, and their difference:**

| | ids |
|---|---|
| before (host, 01:10:09Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |
| after (rendered from the cut's own `deploy-to-ec2.sh`) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |
| **difference** | **EMPTY** (`env_keys_AFTER_PHASEA.txt`: `EQUAL`) |

**`.env` keys (keys only, never values; the A3 RULE, before == after, read from the then-live ref):** host 52 keys
(52 distinct), rendered 52 (52 distinct); dropped `[]`, added `[]`. `MASTER_ADMIN_PRINCIPALS` and
`WRITE_CAPABLE_PRINCIPALS` both present on the host; `ADVI_FEE_STATEMENT_S3_ROOT` absent (0 occurrences). The 52 is
this base's reading, not a pin.

**Tool census, in-process (`MOCK_GRAPH=1`, the 7 ids), live artifact vs the cut:** native 42 + integration 24 =
**66 both sides; added `[]`, removed `[]`, names EQUAL.** No `ops_*` tool exists in the cut (0) and
`copy_site_file_to_s3` is absent.

## 5. WHAT THE CUT SERVES, proved offline against the DEPLOY-ONLY tree

`probes_r10/inprocess_deployonly_PHASEA.txt`: `ops lead asks routed 10 of 10 on the first try`;
`FWD18 served 3 of 14 (C2 W5 W6)`; `C3 carried by E-4/E-5/E-9: 3 of 3`; `E25 claims C1: False`; `FOLDS references: 0`;
`GUIDE first=E-13 five model codes in the match: 5 of 5`. These are the issuer's `c7.AC2`/`c7.AC3` instruments pointed at
`C:/tmp/mx-dep-r10`, not at my branch. Expected `r10.AC2` read-back after the apply: `/health=200; SERVED readers
graded good 0 of 0` (both censuses GAP, so the reader branch is skipped by design); `routes first 4 of 4`;
`fwd18 served,c3=3 3`; `guide=E-13 5`.

## 6. THE DASHBOARD BUILD -- the pin moved, so the clearance was re-measured

MP-r-2 moved `mcportal_commit` to `bc37107`, so the earlier clearance (at `d60b4e0`) does not cover it.

| arm | input | reading | exit |
|---|---|---|---|
| PASS | `bun.lock` at `bc37107aa5...` (30903 B, sha256 `7e6b71c2...c4bc`) | **77 of 77** | **0** |
| NEGATIVE CONTROL | same lockfile with `react@19.3.0` altered to `react@19.9.99` | **75 of 77**, `react@19.9.99 absent` | **1** |

The denominator held at 77 in both arms. The lockfile is byte-identical to the one at `d60b4e0`.

## 7. OPEN LEDGERS

Union of `.open_deploys/` across 28 worktrees at HEAD: 76 entries (`open_ledgers_PHASEA.txt`). Two are named for this
host or this project: `nfra-mcportal-cp2-release` (MP-r-2; its `change_management` entry reads `CLOSED` at
20261010T231237Z, 4 legs) and `nfra-mcpindex-r6-bd-merge-retire` (entry `CLOSED` 20261002T002841Z; a bd-merge act, not
this host; the sentinel is a stale file of a CLOSED entry). No OPEN or HELD gateway release stands, so the host takes
this release. `nfra-mcpindex-r9-ops-readers-release` does not exist yet.

## 8. THE LABEL PROCEDURE (order item 0; ruling 2c, row Z-S92) -- WRITTEN, NOT YET DONE

`deploy-to-ec2.sh` names the artifact and stamps `git-ref` from `git rev-parse HEAD` of the CALLING tree (`:203-204`,
`:241-242`). Therefore:
1. The deploy tree's HEAD IS the deploy-only commit: **`git -C C:/tmp/mx-dep-r10 rev-parse HEAD` reads
   `a9c23fe126de5668a50218360f3485587fadd5b9` and `git status --porcelain` reads 0 lines.** The two files are committed,
   never left as working-tree edits over the base. Re-assert both immediately before the apply.
2. After the upload, BEFORE the ledger's first leg closes, read back with `head-object`: `opal-gateway-a9c23fe126.tar.gz`
   PRESENT, and `-latest`'s `git-ref` EQUAL to `a9c23fe126de5668a50218360f3485587fadd5b9`. Also confirm
   `opal-gateway-2a5966dfbd.tar.gz` (the rollback key) is unchanged: 535420 B, ETag `8a06aaa1...`.
3. If either differs, STOP and repair labels before closing a leg.

## 9. PHASE B -- NOT STARTED; what it does

Held for the never-widen halves (CTO + COO) on THESE pins, the slot agreed by the issuer with `2.0.0_SA_COO~O`, and the
site-Z CloudOps lane `0.7.0_AE_CloudOps~MX`.

1. Re-read BOTH planes (section 1). If either is not `2a5966dfbd`, STOP: these pins are void and the document is
   re-cut, not patched.
2. A5's halt-gate proof from the deploy tree: `git -C C:/tmp/mx-dep-r10 sparse-checkout add
   org/tier2_senior/0.7.0_AE_CloudOps` after printing the NEGATIVE control (rc=3 `unknown-base`) and then the
   POSITIVE (rc=0). `HALT_OVERRIDE` is forbidden. NOTE for the applier: the cone this tree carries is
   `infra/aws/ec2/opal-gateway`, `.tools`, `data/transcripts/scripts/teams`. The third entry is required, because the
   deploy script reads `data/transcripts/scripts/teams/meeting_allowlist.json` in-repo (`:36`) and refuses without it
   (measured: a first cone without it refused with "meeting_allowlist.json unreadable"). A cone that also contains
   `infra/aws/ec2/smartx-exporter` reads 12 permanently-modified files (committed CRLF blobs under `eol=lf`); this
   cone avoids them.
3. Open NEVER-2 ledger `nfra-mcpindex-r9-ops-readers-release` (entry AND `.open_deploys` sentinel). It is an S3
   tarball plus SSM deploy, not an image move, so the task-family sweep does not apply.
4. `DEPLOY_BASE_REF=2a5966dfbd89be9fe6cc0ef3566831e502b81d42 HALT_ACK=1 AGENT_NAME=0.7.0_AE_CloudOps~MX bash
   infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`, run from
   `C:/tmp/mx-dep-r10`.
5. Read back, each independent of the deploy rc: the section 8 labels; `/health` 200; `r10.AC2` verbatim; the host
   `.env` key set equal before and after with 0 dropped and both principal keys present; the id set equal (difference
   EMPTY); tool count 66 to 66 with equal names; host app files equal to the cut's (102 identical, the 2 changed ones
   now equal the cut). Then close the ledger and run `r10.AC1`.
6. Roll back on ANY failed leg, never half-landed, through the same script from a clean tree at the base, restoring
   the VERSIONED `opal-gateway-2a5966dfbd.tar.gz`, never `-latest`.
7. The applier writes the proof instance at `<instance_path>` and reports the ledger close to `2.0.0_SA_COO~MI`.

## 10. NOT PROVED HERE

- The suite on this base (the issuer reports new 0 against baseline 41 at MX-c-7's drain; not re-run).
- The served effect on the host's own `.env` and IAM: only the apply shows it (`r10.AC2`).
- FWD-19's trade reconciliation and billing legs are NOT done: both are GAP, owners unowned and `ADVI_BILLING`. This
  release makes them discoverable as GAP, nothing more.

## 11. ROWS

None filed by this order. (`NFRA_MCPINDEX-Z-W30-S1` was filed by MX-o-1 and is unaffected.)
