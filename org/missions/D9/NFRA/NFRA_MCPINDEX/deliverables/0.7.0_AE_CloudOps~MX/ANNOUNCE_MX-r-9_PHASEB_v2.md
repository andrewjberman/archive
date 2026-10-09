# ANNOUNCE v2 -- MX-r-9 PHASE B: the discover-needs release RE-CUT on live ref `1e32562729`

Applier: `0.7.0_AE_CloudOps~MX` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-9.discover-needs-release.md` at
**A6** (`3b35fdb72d`), which SUPERSEDES A4's mechanism via A5 and voids every r29 pin.
Authorisation: **GO (re-cut) msg 32902 -- the re-cut and this document only. The APPLY and the LEDGER
remain HELD** until both never-widen halves are re-signed on these v2 pins and the issuer sends the full GO.
Probes: `deliverables/0.7.0_AE_CloudOps~MX/probes_phaseb_v2/`.

**THIS DOCUMENT SUPERSEDES `ANNOUNCE_MX-r-9_PHASEB.md` @`5f9d189083`** (cut on r29 `91811b648a`). Its pins
-- deploy commit `5133f082bc`, gateway tree `f3844dae4c`, rollback tree `dbcced0bf1` -- and both halves on
them (`@f041d208e6`, `@cd2a361f8d`) are VOID by their BASE-MOVED clause, exactly as that document's own
section 12 item 1 required. The r29 worktrees `C:/tmp/mx-dep-r9b` and `C:/tmp/mx-rb-r9b` are superseded and
are not the apply's source; the v2 trees below are.

**STATE: PHASE B part 1 (v2) only. NOTHING deployed. No ledger opened. Nothing uploaded to S3. No
Terraform. No grant, identity, role or sign-in created, changed or tested. No push. `HALT_OVERRIDE` never
set, in any run, at any point this session** -- instrument: `org/halt-gate-override-audit.log` contains
`0.7.0_AE_CloudOps~MX` **0 times**.
AWS contact, all read-only and all Opal's own: `s3api head-object` on two keys, one `s3 cp` of the
`-latest` artifact for the plane-2 census, one SSM `AWS-RunShellScript` probe reading file hashes and
`.env` KEY NAMES.

## 1. THE STOP GATE (A1 item 2, as A6 re-specifies the planes)

The base moved twice while this order was held: **r29 `91811b648a` -> OG-tl-1/OG-ap-4 `c97232408d`
(15:07:17Z) -> MP-x-4 `1e32562729` (16:12:05Z, ledger CLOSED 16:27:37Z @`e9a1bf5127`)**.

| plane | read | value |
|---|---|---|
| **1** -- S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` metadata `git-ref` | LastModified 2026-10-09T16:11:36Z, 518165 B, ETag `b96315a523842ec46579b146c450faa9` | **`1e32562729495695c6addaed05f047e46090776f`** |
| **2a** -- the HOST BYTE-CENSUS (A6's plane 2 while the manifest lagged) | SSM probe 2026-10-09T17:11:07Z vs the downloaded `-latest` artifact | **103 of 103 common files byte-identical, 0 DIFFER, 0 artifact-only** |
| **2b** -- `EC2_MANIFEST.json` `deployed_commit` at HEAD (COO~MP's drain has since landed, `e9a1bf5127`) | deployed_at 2026-10-09T16:12:05Z by `0.7.0_AE_CloudOps~MP` | **`1e32562729495695c6addaed05f047e46090776f`** |

**BOTH PLANES NAME `1e32562729`. The gate PASSES, and it passes on BOTH forms of plane 2** -- the host
census A6 specified for the lag, and the manifest itself, whose drain landed between my census and this
write. No BLOCKING row is owed.

- The 2 host-only files in census 2a are `dashboard/assets/index-BP6X9XJd.js` and
  `index-BqfQgt7G.css`: **orphans of a PRIOR dashboard bundle, referenced by nothing**. The live
  `dashboard/index.html` references `assets/index-a6wjv_wv.css` and `assets/index-CrZMj-00.js`, both
  present in the artifact and byte-identical on the host. So the host is the `-latest` artifact plus two
  unreferenced leftovers -- not a divergence of any shipped file.
- METHOD NOTE, recorded because it produced a false verdict first: the plane-2 census initially read
  `artifact files = 0` and therefore `NOT CLEAN`. **That was a ZERO DENOMINATOR, not an absence** -- the
  artifact root was passed to native Python as an MSYS `/c/...` path, which it cannot read. Re-run with
  the native `C:/...` form it reads 103. The probe now asserts a non-zero denominator before comparing.

## 2. THE v2 PINS

| field | value |
|---|---|
| base = LIVE ref | **`1e32562729495695c6addaed05f047e46090776f`** (r29 + OG-tl-1 allowlist + MP-x-4 Control Plane) |
| live base gateway tree object | `aa74888f584aff18a235f8dc33cdb8693661120c` |
| deploy-only worktree | `C:/tmp/mx-dep-v2`, sparse cone, detached at the base, never merged, never pushed |
| **deploy-only commit** | **`d3c31e972e8c6fdb26dda98a1d9ff55ced0ced89`** (parent = the base; `git commit-tree` plumbing, author = this serial, no hook, no `GIT_COMMIT_AUTHOR_OVERRIDE`) |
| **deploy-only gateway tree object** | **`a605ad2f7977adb4639476988509eb60723944eb`** |
| rollback worktree | `C:/tmp/mx-rb-v2`, sparse cone, detached at the base, porcelain EMPTY |
| **ROLLBACK ARTIFACT (A6: the VERSIONED key, never `-latest`)** | **`s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-1e32562729.tar.gz`** -- exists, `git-ref` = `1e32562729...`, ETag `b96315a523842ec46579b146c450faa9` and size 518165 **identical to `-latest`'s**, so the versioned key and the live artifact are the same bytes today and the versioned key is the stable handle after `-latest` moves |
| mcportal | **`d60b4e0a2771a114b5e7291e4163f8cf54de4969`** -- **MOVED** from `a3bff71ffa` by MP-x-4 (section 7) |
| artifact keys at the apply | `opal-gateway-d3c31e972e.tar.gz` (+ `-latest`), both to carry `git-ref` = `d3c31e972e8c6fdb26dda98a1d9ff55ced0ced89` |
| Terraform | **none.** No plan, no IAM change. |
| NEVER-2 ledger | `nfra-mcpindex-r8-discover-release` -- **NOT opened.** It opens at the apply. |

## 3. THE CONTENT -- exactly two files, unchanged in intent from v1

| file | live base blob | box/sitez HEAD blob | +/- |
|---|---|---|---|
| `app/integrations/opal_discover/integration.py` | `0b56455e8431a3645c129d3f65fd26dfe25fb1b2` | `7f45517f274ee7cf323fc2126e492d57c0f3abe0` | +308 / -40 |
| `app/refs/DATA_CATALOG.yaml` | `51bd7936426f69249f6d93bdf2a0fc8de1ffba83` | `da94d7cc64456915f00d9825f716b2ce7c4a9d32` | +411 / -2 |

**NEITHER SHIPPED FILE WAS TOUCHED BY EITHER PREDECESSOR.** The live-tree blob of each is BYTE-IDENTICAL
at r29 and at `1e32562729` (`0b56455e84...` and `51bd793642...` both times), which is why the delta is the
same +308/-40 and +411/-2 as v1's against a different base. OG-tl-1 and MP-x-4 did not enter my surface.

**LINEAGE PROOF.** HEAD's blob for each file is byte-identical to the blob its named commit produced:
`integration.py` at MX-d-8 `4b0ff635e9`, `DATA_CATALOG.yaml` at MX-c-6 `e7f52df685`. (MX-d-7 `6584b623fa`
edits `integration.py` first; MX-d-8 edits lines it added, hence the net rather than the sum.) No later
commit on `box/sitez` has touched either file.

Each file was written into the cut with `git cat-file blob <sha> >` (binary-safe) and **verified by
`git hash-object`, not by filename**: 2 of 2 returned the expected blob. The deploy commit's whole-repo
diff against the base is exactly these two files; **files outside `infra/aws/ec2/opal-gateway/` = 0.**

## 4. PRESERVATION -- every other live file is byte-equal

Artifact roots (`app/`, `deploy/`, `requirements.txt`, `identity_tool_allowlist.txt`) of the live base
tree against the deploy commit's, path by path, by git BLOB:

| | |
|---|---|
| ARTIFACT-ROOT DENOMINATOR | **100** live, **100** in the cut (98 at r29 -- the predecessors added 2 files) |
| absent from the cut / only in the cut | **0 / 0** |
| **IDENTICAL** | **98 of 100** |
| **CHANGED** | **2** -- the shipped pair above |
| `.py` | **84 identical of 85** |

**PRESERVATION: PASS.** GRAIN NOTE: this is the GIT TREE's artifact roots (100 files). The host and the
extracted tar hold 103 (+ the dashboard bundle, built at deploy time and absent from git). Section 1's
census reconciles the two grains against the real artifact.

## 5. THE TWO EXCLUSIONS -- A6 requires both printed

### E2 -- ADVI_BILLING `copy_site_file_to_s3`, unreleased

1. **Not in either shipped file.** Occurrences at HEAD: `integration.py` 0, `DATA_CATALOG.yaml` 0.
2. **E2 lives entirely elsewhere.** The 9 gateway files carrying it at HEAD are `app/data_entitlement.py`,
   `app/destructive_ops.py`, `app/integrations/advi_billing/site_to_s3.py`, `app/tools.py`,
   `deploy-to-ec2.sh` and 4 tests -- **none is one of my two**, so a two-file cut cannot carry E2.
3. **Tool census:** `copy_site_file_to_s3` present in the live census **False**, in the cut's **False**.
4. **`.env`:** `ADVI_FEE_STATEMENT_S3_ROOT` is **ABSENT** from the host's 52 keys and appears **0** times
   in the rendered AFTER key set.

### The `.pptx` pair, unreleased

1. **Tool census:** pptx-named tools in the live census `[]`, in the cut's `[]`.
2. **The one pptx string inside a shipped file is PRE-EXISTING, not the pair.**
   `DATA_CATALOG.yaml:1266` reads
   `read_document: 'RENDITION ONLY, NO TEXT (v1) -- pdf/docx/pptx convert + size, ...'` -- and that line is
   **byte-identical at the live base and at HEAD**. It is prose describing an already-released
   `read_document` boundary. Shipping HEAD's `DATA_CATALOG.yaml` therefore introduces no pptx behaviour.
   **Stated explicitly because the naive proof ("no pptx in the shipped files") is FALSE and would have
   been caught by a reviewer**: the sound proof is identity-across-refs plus the census.
3. **Denominator:** gateway files mentioning pptx = **2 at the live base** (`DATA_CATALOG.yaml`,
   `app/tools.py`), **6 at box/sitez HEAD**. The 4 HEAD adds -- `app/destructive_ops.py`,
   `app/integrations/advi_billing/site_to_s3.py`, `deploy-to-ec2.sh`,
   `tests/test_og_ab2_pairs.py` -- are **none of my two**.

### The deploy script is the LIVE ref's, which is what keeps both exclusions out of `.env`

`cmp` of the cut's `deploy-to-ec2.sh` against `git show <base>:.../deploy-to-ec2.sh` -> **IDENTICAL**;
against `git show HEAD:.../deploy-to-ec2.sh` -> **DIFFERS** (the control). HEAD's would add E2's
`ADVI_FEE_STATEMENT_S3_ROOT` line and the pptx hunk.

## 6. A3's `.env` KEY RULE and `ENABLED_INTEGRATIONS` (keys only, never values)

**BEFORE -- the SERVED host** (`probes_phaseb_v2/host_read_BEFORE_v2.txt`, SSM, parsed in Python, never
shell-sourced per row Z-S73; probe time **2026-10-09T17:11:07Z**):

- `/health` **200**
- `---ENVLINES 52 KEYS 52 DISTINCT 52`
- `MAIL_SENDER_DOMAIN_TABLE` **PRESENT** | `ADVI_FEE_STATEMENT_S3_ROOT` **ABSENT**
- `MASTER_ADMIN_PRINCIPALS` **PRESENT** | `WRITE_CAPABLE_PRINCIPALS` **PRESENT** (both principal keys stay)

**AFTER -- rendered from the cut's own script** with dummy inputs (`env_keys_AFTER_v2.txt`):

```
rendered keys: 52 (distinct 52); host keys: 52 (distinct 52)
host keys NOT rendered (dropped): []
rendered keys NOT on host (added): []
```

**52 == 52. Dropped: none. Added: none. THE RULE HOLDS.** The count is reported as the RULE's reading on
THIS base, never as a pin: A3 made the equality a rule precisely so a base move cannot invalidate it, and
the count has already moved once this round (51 at r28 -> 52 once OG-md-1's `MAIL_SENDER_DOMAIN_TABLE`
rode r29). That was row `NFRA_MCPINDEX-Z-S90`, adopted by A3 and disarmed by the issuer's `Z-S91`.

| `ENABLED_INTEGRATIONS` | ids |
|---|---|
| before (host, 17:11:07Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |
| after (the cut's rendered `.env`) | same 7 |

**EQUAL.** `opal_discover` was already enabled; this release moves no id.

## 7. THE TOOL CENSUS -- in-process, `MOCK_GRAPH=1`, the 7 live ids

| tree | native | integration | total |
|---|---|---|---|
| live base `1e32562729` artifact | 42 | 24 | **66** |
| deploy-only cut artifact | 42 | 24 | **66** |

**added `[]`, removed `[]`, delta 0, sorted name lists EQUAL.** ac08 (train C3) = LIVE + OWN = **66 + 0**:
this release registers no tool. (PHASE A's 66 was against r28 and void as a pin; this one is measured
against `1e32562729`.)

## 8. THE DASHBOARD BUILD -- the pin MOVED, so the clearance was re-measured, not carried

**MP-x-4 moved `mcportal_commit` from `a3bff71ffa` to `d60b4e0`.** `MCPORTAL_WANT` comes from the manifest
(`deploy-to-ec2.sh:46`), so the dashboard build at my apply uses `d60b4e0`, and the clearance I recorded in
v1 no longer covered the operative pin. A cache miss refuses BEFORE any upload (OG-bi-1), so this was
re-run rather than inherited:

| arm | input | reading | exit |
|---|---|---|---|
| **PASS** | `bun.lock` at `d60b4e0a2771a114b5e7291e4163f8cf54de4969` (30903 B) | **77 of 77** | **0** |
| **NEGATIVE CONTROL** | same lockfile, one well-formed-but-uncached spec planted (`react@19.9.99`) | **76 of 77**, `react@19.9.99 absent` | **1** |

**The denominator HELD at 77 across both arms, so the pass is a real pass.** Exit codes were read without
a pipe in the way, after a first reading where `$?` had captured `tail`'s status instead of the script's.

The new pin's lockfile is **byte-identical** to the old pin's (both sha256
`7e6b71c2ea3876561f18e2df606203a78b48bd7013404bf26d614ea70d10c4bc`), so the dependency set did not change
and the earlier control transfers; the re-run is nonetheless the measurement this document rests on.
`d60b4e0` carries a `bun.lock`, which the gitlink `fa1ff9693b` does not -- and the gitlink is never a
deploy input, because nothing writes `mcportal_commit` (`comp-find`: 8 hits across 539 files scanned;
`deploy-to-ec2.sh:46` reads it, `EC2_MANIFEST.json` declares it).

## 9. A5's HALT-GATE PROOF -- both verdicts, from the v2 deploy tree, through the WRAPPER's path

A5 supersedes A4: `safe-ec2-deploy.sh:57` sets `HALT_GATE_REPO_ROOT` to the CALLING worktree
unconditionally (R-53), so exporting it cannot reach the predicate; the remedy is to make the predicate's
premise TRUE in the deploy tree. The wrapper has no dry-run mode, so its gate environment was replicated
from `:38-62` and `:167-171` -- repo root = the calling toplevel, context file and audit log pinned to the
MAIN tree, `HALT_GATE_INBOX_ROOT` left UNSET to default, sourcing the DEPLOY TREE's own gate copy, then
`halt_gate_check "safe-ec2-deploy:opal-gateway"`.

| | state of `C:/tmp/mx-dep-v2` | resolved serial | `HALT_GATE_INBOX_ROOT` | verdict |
|---|---|---|---|---|
| **NEGATIVE CONTROL** | base folder ABSENT (cone narrowed) | `0.7.0_AE_CloudOps~MX` | `<shared>/org/mcp/inbox` | **rc=3** `unknown-base` |
| **POSITIVE** | after `git sparse-checkout add org/tier2_senior/0.7.0_AE_CloudOps` | `0.7.0_AE_CloudOps~MX` | `<shared>/org/mcp/inbox` | **rc=0** |

The serial resolves to `~MX` in BOTH arms, so the rc=3 is the FOLDER predicate failing, not serial
resolution; and the inbox root defaults to the SHARED inbox, so the gate scans THIS lane's real mail
(A6: the inbox limb needs no export). The cone change moved no content -- after narrowing and re-adding,
the two shipped files are still the only modifications in the gateway dir. A sparse cone controls
CHECKOUT, not CONTENT.

## 10. NOT PROVED HERE

- **The suite.** PHASE A's BEFORE/AFTER pair was measured on r28 and is void; a fresh pair on this base is
  not in the re-cut GO's scope and is not claimed. Rows `NFRA_OPLGTW-Z-W47-S2` (3 gateway suites already
  failing on `box/sitez`) and `Z-S88` are the BEFORE red to read alongside it.
- **The served effect** of the 29 catalog needs and discover's true as-of reads under the host's own
  `.env` and IAM: only the apply shows it. `r9.AC2` and `r9.AC3` are the apply's read-back; `r9.AC1`
  follows the ledger close.
- **J1 and J2** are L9 judgments for `3.0.0_SA_CVO~Z` and carry no verdict anywhere in this record.

## 11. WHAT PHASE B PART 2 DOES -- NONE OF IT HAS BEEN DONE

Held on both halves re-signed on these v2 pins and the issuer's full GO.

1. **Re-read BOTH planes. If either is not `1e32562729`, STOP** -- these pins are then void exactly as
   r29's were, and this document is re-cut rather than patched. (It has already happened twice.)
2. Open NEVER-2 ledger `nfra-mcpindex-r8-discover-release`: the `change_management/` entry AND the
   `.open_deploys/` sentinel, both named in the commit. No IMAGE act and no task family pulls a tag -- an
   S3 tarball + SSM deploy, not an ECS image move -- so NEVER-2's `describe-task-definition` sweep does not
   apply, and the entry says so.
3. Re-assert `git -C C:/tmp/mx-dep-v2 sparse-checkout add org/tier2_senior/0.7.0_AE_CloudOps` and re-print
   both gate verdicts at the act, then deploy from the deploy-only tree:
   `DEPLOY_BASE_REF=1e32562729495695c6addaed05f047e46090776f HALT_ACK=1
   AGENT_NAME=0.7.0_AE_CloudOps~MX bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway
   infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`. No off-repo input: both principal rosters are read
   host-side from Secrets Manager (OG-rl-1). **`HALT_OVERRIDE` is forbidden and will not be used.**
4. Read back: `/health` 200; `r9.AC2` and `r9.AC3` verbatim from
   `deliverables/2.0.0_SA_COO~MI/round8/checks/`; the host `.env` key set equal before and after with 0
   dropped and both principal keys present; the id set equal; tool count 66 -> 66 with equal names; host
   files equal to the deploy-only artifact's; both S3 objects carrying `git-ref` = `d3c31e972e...`. Then
   close the ledger, and `r9.AC1` after the close.
5. **Roll back on ANY failed leg, never half-landed:** from `C:/tmp/mx-rb-v2` (clean at the base) through
   the SAME script, restoring the **VERSIONED** artifact
   `opal-gateway-1e32562729.tar.gz` -- never `-latest`, which will by then name my own release. No
   Terraform to undo.
6. Write the proof instance at the order's `<instance_path>`. J1 and J2 carry no verdict there.
7. **Report the ledger close to `2.0.0_SA_COO~MI`** -- A6: E2's `.xlsx` release follows mine on the host,
   so the queue needs my close, not just my completion.

## 12. ROWS

No new row is owed by this part. `NFRA_MCPINDEX-Z-S90` (this seat, `97e3d138be`) was adopted by A3 and is
disarmed by the issuer's `NFRA_MCPINDEX-Z-S91`, which `adjudicates: ["NFRA_MCPINDEX-Z-S90"]`. Z-S90 still
reads ARMED in place, which is correct: a surprise row supersedes by a NEW citing row, never by an
in-place edit.
