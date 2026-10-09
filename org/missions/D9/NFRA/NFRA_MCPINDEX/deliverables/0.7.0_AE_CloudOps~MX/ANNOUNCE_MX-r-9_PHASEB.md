# ANNOUNCE -- MX-r-9 PHASE B: the discover-needs release RE-CUT on the live ref r29 `91811b648a`

Applier: `0.7.0_AE_CloudOps~MX` (issuer `2.0.0_SA_COO~MI`). Order:
`org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-9.discover-needs-release.md` at
**A5** (A1 `1dd356991a`, A2 `52db820bbf`, A3 `18ad3e7a14`, A4 `77fc31c41c`, A5 `db83d9d163`).
Authorisation: GO (partial) msg 32753 -- **A1 item 2 only; the APPLY and the LEDGER are HELD.**
Probes: `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MX/probes_phaseb/`.
PHASE A's ANNOUNCE (`deliverables/0.9.0_WK_NFRA_MCPINDEX~28/ANNOUNCE_MX-r-9.md`) is the pattern; **every one
of its pins is VOID** (row Z-W28-S7) because it was cut on r28 `aa75078e1b` and r29 landed over it.

**STATE: PHASE B part 1 only. NOTHING deployed. No ledger opened. Nothing uploaded to S3. No Terraform. No
grant, identity, role or sign-in created, changed or tested. No push. `HALT_OVERRIDE` never set.**
AWS contact, all read-only and all Opal's own: one `s3api head-object`, one SSM `AWS-RunShellScript` probe
reading file hashes and `.env` KEY NAMES, `sts get-caller-identity`, `ec2 describe-instances`,
`ssm describe-instance-information`.

## 1. THE STOP GATE (A1 item 2) -- the live ref read on BOTH planes

| plane | read | time |
|---|---|---|
| S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` metadata `git-ref` | `91811b648ab119e73e22f8d401dd09f45b8ab19b` | LastModified 2026-10-09T12:31:10Z, 514461 B |
| `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` | `91811b648ab119e73e22f8d401dd09f45b8ab19b` | deployed_at 2026-10-09T12:31:40Z, deployed_by `0.7.0_AE_CloudOps~Z` |

**BOTH PLANES EQUAL r29's sha -- proceed.** No BLOCKING row is owed.

One earlier read (12:4xZ) caught the planes DISAGREEING: S3 already at r29 while the manifest on this disk
still read `aa75078e1b`. That was the ~30-second mid-deploy window of another seat's release, not A1's STOP,
which is graded at the act. Recorded so a future applier does not convert a transient into a BLOCKING row
against a healthy release.

## 2. THE PINS

| field | value |
|---|---|
| base = LIVE ref | **`91811b648ab119e73e22f8d401dd09f45b8ab19b`** (NFRA_OPLGTW OG-rl-15, r29) |
| live r29 gateway tree object | `dbcced0bf1df341ed6bab11d9011eb80d0587fe3` |
| deploy-only worktree | `C:/tmp/mx-dep-r9b`, sparse cone, detached at r29, never merged, never pushed |
| **deploy-only commit** | **`5133f082bc67057083b13570f8e48ac4d6a1ef04`** (parent r29; `git commit-tree` plumbing, author = this serial, no hook, no `GIT_COMMIT_AUTHOR_OVERRIDE`) |
| **deploy-only gateway tree object** | **`f3844dae4cb80abfd34c08c342da8001ba48838c`** |
| rollback worktree | `C:/tmp/mx-rb-r9b`, sparse cone, detached at r29, porcelain EMPTY |
| **rollback gateway tree object** | **`dbcced0bf1df341ed6bab11d9011eb80d0587fe3`** -- byte-identical to the live r29 tree object, so the rollback target IS the live artifact |
| mcportal | `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054` -- the live manifest's `mcportal_commit`, UNCHANGED across r29 |
| artifact keys at the apply | `s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-5133f082bc.tar.gz` (+ `-latest`), both to carry `git-ref` = `5133f082bc67057083b13570f8e48ac4d6a1ef04`, written by the deploy script |
| Terraform | **none.** This release has no plan and no IAM change. |
| NEVER-2 ledger | `nfra-mcpindex-r8-discover-release` -- **NOT opened.** It opens at the apply, which is held. Verified absent: 0 hits for that sentinel across 48+ live worktrees, per-tree denominator printed. |

## 3. THE CONTENT, by CONTENT -- exactly two files

A1 item 2: the live tree plus ONLY the two shipped files' content at `box/sitez` HEAD.

| file | live r29 blob | box/sitez HEAD blob | +/- |
|---|---|---|---|
| `app/integrations/opal_discover/integration.py` | `0b56455e8431a3645c129d3f65fd26dfe25fb1b2` | `7f45517f274ee7cf323fc2126e492d57c0f3abe0` | +308 / -40 |
| `app/refs/DATA_CATALOG.yaml` | `51bd7936426f69249f6d93bdf2a0fc8de1ffba83` | `da94d7cc64456915f00d9825f716b2ce7c4a9d32` | +411 / -2 |

**LINEAGE PROOF -- nothing but the three named commits reaches these bytes.** HEAD's blob for each file is
BYTE-IDENTICAL to the blob the named commit produced:
- `integration.py` at MX-d-8 `4b0ff635e9` = `7f45517f27...` = HEAD's. (MX-d-7 `6584b623fa` edits the same
  file first; MX-d-8 edits lines MX-d-7 added, which is why the net is +308/-40 and not the sum of both.)
- `DATA_CATALOG.yaml` at MX-c-6 `e7f52df685` = `da94d7cc64...` = HEAD's.

So no later commit on `box/sitez` has touched either file, and taking HEAD's content is exactly taking the
three cells' content. Each file was written into the cut with `git cat-file blob <sha> >` (binary-safe, no
text-mode CRLF hazard) and then **verified by hash, not by filename**: `git hash-object` returned the
expected blob for 2 of 2.

**The whole-repo diff of the deploy commit against r29 is exactly these two files; files outside
`infra/aws/ec2/opal-gateway/` = 0.**

## 4. A2 -- ADVI_BILLING E2's UNRELEASED TOOL IS EXCLUDED, proven three ways

1. **Neither shipped file carries it.** `copy_site_file_to_s3` occurrences at HEAD:
   `integration.py` 0, `DATA_CATALOG.yaml` 0.
2. **E2 lives entirely in OTHER files.** The 9 gateway files carrying `copy_site_file_to_s3` at HEAD are
   `app/data_entitlement.py`, `app/destructive_ops.py`, `app/integrations/advi_billing/site_to_s3.py`,
   `app/tools.py`, `deploy-to-ec2.sh` and 4 tests -- **none is one of my two**, so a two-file cut cannot
   carry E2 even in principle.
3. **The tool census confirms the effect** (section 7): absent on both sides.

**The deploy script is the LIVE REF's copy, by construction.** The cut is a checkout of r29 with two files
overwritten, so `deploy-to-ec2.sh` is r29's untouched. Proven both directions:
`cmp` against `git show 91811b648a:.../deploy-to-ec2.sh` -> **IDENTICAL**; `cmp` against
`git show HEAD:.../deploy-to-ec2.sh` -> **DIFFERS** (the control). HEAD's would have added E2's
`ADVI_FEE_STATEMENT_S3_ROOT` line and OG-md-1's `rm -f .../mail_sender_domain_table.txt`.

## 5. PRESERVATION -- every other live file is byte-equal

Compared the ARTIFACT ROOTS (`app/`, `deploy/`, `requirements.txt`, `identity_tool_allowlist.txt` -- the
tar roots) of the live r29 tree against the deploy commit's, path by path, by git BLOB:

| | |
|---|---|
| ARTIFACT-ROOT DENOMINATOR | **98** files live, **98** files in the cut |
| absent from the cut | **0** |
| only in the cut | **0** |
| **IDENTICAL** | **96 of 98** |
| **CHANGED** | **2** -- `app/integrations/opal_discover/integration.py`, `app/refs/DATA_CATALOG.yaml` |
| `.py` | **83 identical of 84** |

**PRESERVATION: PASS.** GRAIN NOTE, stated rather than smoothed: this count is the GIT TREE's artifact
roots (98 files). PHASE A's "100 files / 84 .py" was its EXTRACTED-TAR grain, which also holds the
deploy-time dashboard bundle. The two numbers measure different objects and neither is wrong; section 8
reconciles them against the host (98 git files + 3 dashboard files = the 101 the host hashes).

## 6. A3's `.env` KEY RULE -- before == after, read on the THEN-LIVE ref (keys only, never values)

A3: the `.env` key equality is a RULE, never a count; the ANNOUNCE's 51 is void.

**BEFORE -- read from the SERVED host** (SSM `AWS-RunShellScript`, parsed in Python, never shell-sourced,
row Z-S73; `probes_phaseb/host_read_BEFORE.txt`, probe time 2026-10-09T13:03:22Z):

- `/health` **200**
- `---ENVLINES 52 KEYS 52 DISTINCT 52` -- **52 keys, 52 distinct**
- `MAIL_SENDER_DOMAIN_TABLE` **PRESENT**
- `ADVI_FEE_STATEMENT_S3_ROOT` **ABSENT**
- `MASTER_ADMIN_PRINCIPALS` **PRESENT**, `WRITE_CAPABLE_PRINCIPALS` **PRESENT** (both principal keys stay)
- `MAIL_SENDER_TABLE` SET, len=69, items=3 (a host state, not a deploy input; no value printed)

**AFTER -- rendered from the cut's own script** with dummy inputs (`probes_r9/env_render.py`;
`probes_phaseb/env_keys_AFTER.txt`):

```
rendered keys: 52 (distinct 52); host keys: 52 (distinct 52)
host keys NOT rendered (dropped): []
rendered keys NOT on host (added): []
```

**52 == 52. Dropped: none. Added: none. THE RULE HOLDS.**

**This is the finding of row `NFRA_MCPINDEX-Z-S90` (adopted by A3, disarmed by the issuer's `Z-S91`)
confirmed on the real plane.** Z-S90 predicted 52 from the commit graph -- `MAIL_SENDER_DOMAIN_TABLE`
occurrences in `deploy-to-ec2.sh` being 0 at `aa75078e1b`, 9 at r29, 9 at HEAD -- before any host was read.
The host now reads 52 with that key live. **Had a never-widen half been signed on the ANNOUNCE's 51, it
would have refused this correct deploy.**

### `ENABLED_INTEGRATIONS` -- before and after

| | ids |
|---|---|
| before (host, 13:03:22Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |
| after (the cut's rendered `.env`) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |

**EQUAL.** `opal_discover` was already enabled; this release moves no id.

## 7. THE TOOL CENSUS (A2) -- in-process, `MOCK_GRAPH=1`, the 7 live ids

Both trees materialised from git with `git archive` (350 files each) and censused in-process with
`probes_r9/tools_census.py`:

| tree | native | integration | total |
|---|---|---|---|
| live r29 artifact | 42 | 24 | **66** |
| deploy-only cut artifact | 42 | 24 | **66** |

**added `[]`, removed `[]`, delta 0, sorted name lists EQUAL.**
`copy_site_file_to_s3` in the live census: **False**. In the cut's census: **False**.
The ac08 pin (release-train C3) is LIVE + OWN = **66 + 0**: this release registers no tool.
PHASE A's 66 was measured against r28 and is void as a pin; this 66 is measured against r29.

## 8. THE HOST IS RUNNING r29's BYTES -- not merely labelled with them (CLAUDE.md 22a, CODE layer)

A manifest field and an S3 tag are LABELS. The deployed bytes were compared directly: the host's sha256 of
every deployed file (`---HASHES`, 101 files) against the live r29 tree materialised from git.

| | |
|---|---|
| host files carrying a sha256 | **101** |
| COMMON paths | **98** |
| **IDENTICAL** | **98** |
| **DIFFER** | **0** |
| host-only | **3** -- `dashboard/index.html`, `dashboard/assets/index-BP6X9XJd.js`, `dashboard/assets/index-BqfQgt7G.css` (the deploy-time mcportal bundle, built on the applier's device, correctly not in the gateway git tree) |
| tree-only | **251** -- tests, routing harnesses and workflow inputs that the tar roots exclude |

So the BEFORE state is r29 exactly, and this release is a true 2-file delta against what is actually
serving. 98 + 3 = the 101 the host hashes, which reconciles section 5's git grain with PHASE A's tar grain.

## 9. A5's HALT-GATE PROOF -- both verdicts, from THIS deploy tree, through the WRAPPER's path

A5 supersedes A4: `infra/aws/ec2/safe-ec2-deploy.sh:57` sets `HALT_GATE_REPO_ROOT` to the CALLING worktree
unconditionally (R-53), so exporting it cannot reach the predicate. The remedy is to make the gate's premise
TRUE in the deploy tree. The wrapper has NO dry-run or gate-only mode (0 hits for
`DRY_RUN`/`GATE_ONLY`/`CHECK_ONLY`/`RESOLVE_ONLY`), so running it would have deployed; its gate environment
was instead replicated exactly from `:38-62` and `:167-171` -- `HALT_GATE_REPO_ROOT` = the calling toplevel,
`HALT_GATE_CONTEXT_FILE` and `HALT_GATE_AUDIT_LOG` pinned to the MAIN tree, `HALT_GATE_INBOX_ROOT` left
UNSET to default, sourcing the DEPLOY TREE's own gate copy, then `halt_gate_check
"safe-ec2-deploy:opal-gateway"`.

| | state of `C:/tmp/mx-dep-r9b` | `HALT_GATE_REPO_ROOT` | resolved serial | verdict |
|---|---|---|---|---|
| **NEGATIVE CONTROL** | base folder ABSENT (cone narrowed) | `C:/tmp/mx-dep-r9b` | `0.7.0_AE_CloudOps~MX` | **rc=3** `unknown-base` |
| **POSITIVE** | after `git sparse-checkout add org/tier2_senior/0.7.0_AE_CloudOps` | `C:/tmp/mx-dep-r9b` | `0.7.0_AE_CloudOps~MX` | **rc=0** |

The serial resolves to `~MX` in BOTH runs -- the rc=3 is the FOLDER predicate failing, not serial
resolution. In the positive, `HALT_GATE_SHARED_ROOT` resolved to the shared checkout and
`HALT_GATE_INBOX_ROOT` defaulted to `<shared>/org/mcp/inbox`, so the gate scanned THIS lane's real inbox --
A5's point that the inbox limb already reads the shared root (`halt-gate-check.sh:55`).

- **`HALT_OVERRIDE` was never set, in any run.** Instrument: `org/halt-gate-override-audit.log` contains
  `0.7.0_AE_CloudOps~MX` **0 times**; its only entries are from 2026-07-13 by another seat.
- **The cone change moved no content:** after narrowing and re-adding, the two shipped files are still the
  only modifications in the gateway dir. A sparse cone controls CHECKOUT, not CONTENT.
- The gate also resolves correctly with `OPAL_AGENT_SERIAL` UNSET -- precedence step (1), the shared
  checkout's `org/mcp/sessions/f4a24c98-9ed7-44e2-adcd-06810d9d5d8c.serial`. It never falls through to
  `.comp-graph/.agent_context`, which is shared and last-writer-wins and read `0.7.0_AE_CloudOps~CA` at
  12:0xZ.

## 10. THE DASHBOARD BUILD -- the refusal that would land latest, pre-cleared

`bun install --frozen-lockfile && bun run build` runs at the apply on this device, and OG-bi-1's pre-check
(`ops/bun_cache_precheck.py`) refuses BEFORE any upload on a cache miss.

- `bun` 1.3.14 resolves via profile (not a baked path); `python` 3.14.7 on PATH, which the pre-check needs.
- Pre-check against the REAL lockfile at the live manifest's pin `a3bff71ffa`: **77 of 77, exit=0**, re-run
  after r29 landed rather than inferred from the earlier run (the pin did not move across r29).
- **Negative control:** planting one well-formed-but-uncached spec (`react@19.9.99`) reads **76 of 77**,
  `react@19.9.99 absent`, **exit=1**, with the denominator HELD at 77. So the pass is a real pass.
- `fa1ff9693b`, the mcportal GITLINK carried by both r29's tree and `box/sitez` HEAD, has **no lockfile of
  any known name** -- but it is never a deploy input: `comp-find 'mcportal_commit' infra/aws/ec2 --limit 30`
  reads 8 hits across 539 files scanned and NOTHING writes the field; `deploy-to-ec2.sh:46` READS it and
  `EC2_MANIFEST.json:518` DECLARES it. `MCPORTAL_WANT` comes from the manifest, so the gitlink divergence
  cannot reach the build.
- The deploy-only tree has no nested `mcportal/` checkout; the script resolves the pin itself and cuts a
  detached worktree when the main checkout's HEAD differs (`deploy-to-ec2.sh:54-63`), which it does
  (`mcportal` HEAD is `fa1ff9693b`).

## 11. NOT PROVED HERE

- **The suite.** PHASE A's BEFORE/AFTER pair (38 failed both sides, 0 new, on sparse trees) was measured on
  r28 and is void as a pin. Row `NFRA_OPLGTW-Z-W47-S2` lists 3 gateway suites already failing on
  `box/sitez`, to be read as part of the BEFORE red beside `Z-S88`. A fresh pair on r29 is not part of the
  partial GO's scope and is not claimed here.
- **The served effect** of the 29 catalog needs and discover's as-of reads under the host's own `.env` and
  IAM: only the apply shows it. r9.AC2 and r9.AC3 are the apply's read-back, and r9.AC1 follows the ledger
  close.
- **J1 and J2** are L9 judgments for `3.0.0_SA_CVO~Z` and carry no verdict anywhere in this record.

## 12. WHAT PHASE B PART 2 DOES -- NONE OF IT HAS BEEN DONE

Held per GO msg 32753 on OG-rl-15 completing (`2.0.0_SA_COO~O`) and on BOTH never-widen halves, which the
issuer writes from this ANNOUNCE.

1. **Re-read the live ref on both planes. If it is not `91811b648a`, STOP** -- every pin above is then void
   exactly as PHASE A's were, and this document is re-cut rather than patched.
2. Open NEVER-2 ledger `nfra-mcpindex-r8-discover-release`: the entry under
   `org/critical_paths/change_management/` AND the sentinel
   `org/critical_paths/.open_deploys/nfra-mcpindex-r8-discover-release.json`, both named in the commit.
   (No IMAGE act and no task family pulls a tag here: this is an S3 tarball + SSM deploy, not an ECS image
   move, so NEVER-2's `describe-task-definition` sweep does not apply and the entry says so.)
3. `git -C C:/tmp/mx-dep-r9b sparse-checkout add org/tier2_senior/0.7.0_AE_CloudOps` (already in the cone;
   re-assert and re-print both gate verdicts at the act), then deploy from the deploy-only tree:
   `DEPLOY_BASE_REF=91811b648ab119e73e22f8d401dd09f45b8ab19b HALT_ACK=1
   AGENT_NAME=0.7.0_AE_CloudOps~MX bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway
   infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`. No off-repo input is needed: both principal rosters are
   read host-side from Secrets Manager (OG-rl-1). **`HALT_OVERRIDE` is forbidden and will not be used.**
4. Read back: `/health` 200; `r9.AC2` and `r9.AC3` verbatim from
   `deliverables/2.0.0_SA_COO~MI/round8/checks/`; host `.env` 52 keys before == 52 after with 0 dropped and
   both principal keys present; the id set equal; tool count 66 -> 66 with equal names; host files equal to
   the deploy-only artifact's; both S3 objects carrying `git-ref` =
   `5133f082bc67057083b13570f8e48ac4d6a1ef04`. Then close the ledger, and `r9.AC1` after the close.
5. **Roll back on ANY failed leg, never half-landed:** from `C:/tmp/mx-rb-r9b` (clean at r29, gateway tree
   `dbcced0bf1d...` = the live artifact's) through the SAME script with `DEPLOY_BASE_REF` set to the
   then-live ref. No Terraform to undo.
6. Write the proof instance at the order's `<instance_path>`. J1 and J2 carry no verdict there.

## 13. ROWS

No new row is owed by this part. `NFRA_MCPINDEX-Z-S90` (this seat, `97e3d138be`) is adopted by A3 and
disarmed by the issuer's `NFRA_MCPINDEX-Z-S91`, which `adjudicates: ["NFRA_MCPINDEX-Z-S90"]`; Z-S90 still
reads ARMED in place, which is correct, because a surprise row supersedes by a NEW citing row and never by
an in-place edit.
