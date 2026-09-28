# ANNOUNCE -- MX-r-4 PHASE A, opal-gateway narrow release that ENABLES opal_discover and portal_index

Deployer: 0.9.0_WK_NFRA_MCPINDEX~10 (issuer 2.0.0_SA_COO~MI). Order:
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-4.thread-live-enable.md

STATE: PHASE A only. Nothing was deployed, no ledger is open, no `.env` was changed, nothing was uploaded to S3.
AWS contact was read-only: `s3 ls`, `head-object` x2, one `s3 cp` download of the LIVE artifact (to compare), and
IAM `list-role-policies` / `get-role-policy`. All of it is Opal's own AWS.

## THE RELEASE PIN (for the CTO's G-A arch-gate)

| field | value |
|---|---|
| release branch | rel-nfra-mcpindex-r3-gateway |
| release commit | 2f14e38af917aa0ca3b1e2af68fdd0a88956d72a |
| release worktree | /c/tmp/mx-rel3 (Windows: C:\tmp\mx-rel3) |
| base = live deployed commit | 6a98a0553a0a01c7e1acc6aea2b2ce5b82fc0f9b (NFRA_OPLGTW OG-s-1's release branch commit, read from EC2_MANIFEST.json `services.opal-gateway.deployed_commit` at this cut; not an ancestor of CLOUD) |
| the release's whole delta over the base | 2 files, +95: opal_discover/integration.py, tests/test_opal_discover.py |
| the enable delta (PHASE B, NOT in the pin) | ONE line in deploy-to-ec2.sh, section 3 below |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054, nested clone in both trees, unchanged from the live deploy |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-<short sha of the release HEAD>.tar.gz (head-object on the 2f14e38af9 key: 404 now). The short sha changes when the enable commit lands. |
| worker branch (ledger, manifest) | wk-nfra_mcpindex-3-10, worktree C:\Users\Opal Bloomberg\Desktop\wk-mcpindex-r3-10, cut from CLOUD 29fc9b1e32 |

## Step 1: this project's gateway commits since the deployed commit, oldest first

Method: commits on CLOUD (29fc9b1e32) touching infra/aws/ec2/opal-gateway whose author is
`0.9.0_WK_NFRA_MCPINDEX~<n>`, then each one read against the deployed tree by content, because the deployed commit is
a release-branch commit and `--is-ancestor` cannot answer it.

By author there are 13 on CLOUD:
650c9a99cb, 119a49eef0, 37f208249f, 4bfab1bcf2, 8829b066d1, 81d37aafda, 2c25c4c831, 84a725073b, d36d31f8c5,
bc0cde67f0, e1cdb12550, bcb48cf626 (the 12 MX-r-3 released, in 110d93fb73, and the live base descends from it:
110d93fb73 is an ancestor of fe94911257, which is an ancestor of 6a98a0553a), then
**85e1158e6e (0.9.0_WK_NFRA_MCPINDEX~10, MX-d-3, opal_discover ranking)**.

Content check: `git diff --stat 6a98a0553a HEAD -- infra/aws/ec2/opal-gateway` on CLOUD is 11 files. Only two are this
project's, and they are exactly MX-d-3's: opal_discover/integration.py (+29) and tests/test_opal_discover.py (+66). The
other nine are other projects' work CLOUD holds unreleased (config.py, server.py, taxsma_workbook.py,
tests/conftest.py, tests/test_entitlement_admin.py, tests/test_principal_cutover.py, tests/test_taxsma_workbook.py,
tests/acceptance/onhost_bench.py, runbooks/SCHWAB_PILOT_RUNBOOK.md). So the 12 MX-r-3 commits are already live, and
**85e1158e6e is the only one to carry**. MX-d-3's commit is among them, as required. The drain merge 1328566f78 is
authored 2.0.0_SA_COO~MI and its gateway content is 85e1158e6e's, so it is not carried separately.

Other projects' gateway commits CLOUD holds UNRELEASED, for the release_note (by the file diff above, latest per file):
NFRA_MCPORTAL 98ad7e253f and 31b9d1975e, MDPF_TAXSMA 6abf60e5d5, NFRA_OPLGTW 9e4074c33a, 6c37cc6b00 and 5550877e79
(the last is a floor; at least these).

### The cherry-pick census: what is on CLOUD at my cut, and MX-x-2

**MX-x-2 (worker ~13, portal_index and catalog): its GATEWAY WORK has NOT drained to CLOUD.** Measured twice.
- At my cut (29fc9b1e32): 0 commits by 0.9.0_WK_NFRA_MCPINDEX~13 touch the gateway.
- Re-read at send time, CLOUD tip 9e1efbd2d1: `git log 29fc9b1e32..CLOUD -- infra/aws/ec2/opal-gateway` is 0 commits.
  What ~13 has on CLOUD is one rows-only commit, 8be837699f (Z-W13-S1, -S2 and BLOCKING -S3, 1 file, the
  investigation channel), drained as 58924e1530. Its subject says the work itself is re-cut by amendment A1.
- Branch wk-nfra_mcpindex-3-13 has no gateway file change beyond CLOUD.
- Branches ~8, ~11 and ~12 carry 0 gateway commits ahead of CLOUD (~8 has commits ahead, none touching the gateway).

So the release carries 85e1158e6e alone. When MX-x-2 re-cuts and drains, it is a separate narrow release and does not
change this pin.

## Step 2: the release tree, census, override

`git worktree add -b rel-nfra-mcpindex-r3-gateway /c/tmp/mx-rel3 6a98a0553a...` then
`cherry-pick --no-commit 85e1158e6e`. One conflict: the commit's INVESTIGATION_v1.md edit (row Z-W10-S1) is
"deleted in HEAD" because the file does not exist at the base. It is a non-gateway path, so it was dropped
(`git rm`), the same pin-back to base MX-r-3 applied. Nothing else conflicted.

Census, `git -C /c/tmp/mx-rel3 diff --stat 6a98a0553a HEAD -- infra/aws/ec2/opal-gateway`: 2 files, 95
insertions, 0 deletions. The whole-tree diff is the same 2 files. It equals 85e1158e6e's gateway files: 0 extra,
0 missing.

Tests in the release tree, from infra/aws/ec2/opal-gateway: test_opal_discover 8 passed; test_tool_classification_composition
7 passed; test_portal_index 6 passed, 1 failed. The failure is `test_portal_tools_catalog_refs_resolve` at line 264,
`sorted(refs.values()) == sources`, where `sources` is the glob of
workflows/atom_decomposition/catalog_entries/portal_*.yaml. Those source files are outside the gateway tree and are
not shipped, so the glob is empty. It is the same failure MX-r-3 recorded (row NFRA_MCPINDEX-Z-W1-S8). On CLOUD the
same file reads 7 passed. The shipped catalog resolves; only the test's source-file glob does not.

**Override use: 1 of 1.** Release commit 2f14e38af9 was made with
`GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_MCPINDEX~10` under `.tools/safe-commit.sh` in /c/tmp/mx-rel3. The PHASE B
enable edit, if the issuer amends the paths, is a second release commit and a second use (not made).

## Step 3: the enable mechanism

- **File and line:** `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` line 197. It is one `printf '...' ...` that writes the
  host `/opt/opal-gateway/.env` (`sudo -u ec2-user tee` path, chmod 600). The literal is
  `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph`, at `\nENABLED_INTEGRATIONS=...\nDASHBOARD_OWNER_EMAILS=`.
- **Read by:** `app/config.py:227-228` (`os.environ.get("ENABLED_INTEGRATIONS")`, split on space or comma), then
  `app/server.py:85` `integrations.register_enabled(mcp, _cfg.ENABLED_INTEGRATIONS)`.
- **The one change:** on line 197, `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph` becomes
  `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index`. Both ids are registered factories
  (`registry.py` `register_factory("portal_index", ...)` and `("opal_discover", ...)`). It adds no `%s`: the printf keeps
  9 `%s` and 9 arguments, so no argument shifts. It is a deploy path, not a hand edit on the host: the deploy script
  regenerates the whole `.env` on every run.
- **The mechanism does exist, so this is not a BLOCKING row. But it needs an amendment before PHASE B:**
  1. `deploy-to-ec2.sh` is not in `<paths>`, and bound 1 says it is "READ, never edited". The enable IS an edit to it.
     The order's own closing paragraph of section 3 says the issuer amends `<paths>`. Bound 1 needs the same
     exception, for that one line.
  2. The edit has to land in TWO places: the release branch (so the deployed tree carries it) and CLOUD, via my worker
     branch, so CLOUD does not later revert the enable. NFRA_OPLGTW OG-s-1 did the same (CLOUD 14f5219039, release
     6a98a0553a). Both are the same one-line change.
  3. The release commit hash, and so the artifact key, changes when the enable commit lands. The CTO's G-A is
     therefore graded on 2f14e38af9 plus the one named line, and the GO should name the final hash.
- **What the enable changes on the host:** `.env` key set unchanged at 26 keys (the value of one changes). The
  on-host tool list goes from 46 to 51 (2 discover tools + 3 portal_index tools; 51 is the pin CLOUD's
  test_entitlement_admin carries). Read on-host before and after at PHASE B.

## Step 4: rollback, built and compared before any act (NOT uploaded)

- Clean tree: /c/tmp/mx-rb3, detached HEAD at 6a98a0553a (the live commit), mcportal a3bff71ffa cloned beside it.
- A build-only mirror of deploy-to-ec2.sh:78-91 was run: `bun install --frozen-lockfile`, `bun run build`, the same
  `tar -czf` with the same excludes. It has no upload line. It produced a 398879-byte
  opal-gateway-6a98a0553a.tar.gz in the worker's `.scratch/rb/`, rc=0.
- Compared per file with the LIVE artifact, downloaded from
  s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-6a98a0553a.tar.gz (398872 bytes,
  LastModified 2026-09-27T22:17:12Z): **79 of 79 files byte-identical**, 67 of 67 .py files identical, 0 only-live, 0
  only-rebuilt. (Sizes differ by 7 bytes: gzip and tar framing, not content.)
- **Re-deploy command:**
  `cd /c/tmp/mx-rb3 && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_MCPINDEX~10 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
  (HALT_ACK=1 only when the halt gate reads 0 STOP.) Its line 197 is byte-identical to the release tree's before the
  edit, so it writes **`ENABLED_INTEGRATIONS=ycharts opal_portal globgrph`**, which is the value the host carries now.
  deploy-to-ec2.sh and safe-ec2-deploy.sh are byte-identical (`cmp`) between /c/tmp/mx-rel3 and /c/tmp/mx-rb3.
- The rollback re-uploads the same key, opal-gateway-6a98a0553a.tar.gz, and the `-latest` key.

## Step 5: the integration checklist (NFRA_INTEGRATIONS_STANDARD.md, docs/architecture/, s.5 and s.8.1)

Found with Glob (`comp-find` piped into a filter was refused by the rail). Grounding: the release tree's own code, and
live IAM read-only calls. **G-A is the CTO's to sign; this is where each one stands, not a grade.**

Machine gate, both integrations, run in /c/tmp/mx-rel3: `validate_integration_spec(SPEC) == []`.

### s.5 add-checklist (steps 1-5)

| step | opal_discover | portal_index |
|---|---|---|
| 1 author | done: `app/integrations/opal_discover/`, 2 tools `opal_discover`, `opal_describe` | done: `app/integrations/portal_index/`, 3 tools `mdpf_get_aum_metrics`, `mdpf_get_account_distribution`, `mdpf_get_aggregate_aua` |
| 2 register factory | done: `registry.py` `register_factory("opal_discover", ...)` | done: `register_factory("portal_index", ...)` |
| 3 provision secret | N/A: AuthKind.NONE, no secret | N/A: AuthKind.NONE, no secret (the instance role reads the bucket) |
| 4 grant IAM | N/A: reads no S3 object; its only egress is none | LIVE-GROUNDED: `get-role-policy opal-gateway-queryv0-portal-read` allows `s3:GetObject` on exactly `opal-data-portal-v2/json/*` and `opal-data-portal-v2/platinum/*`. comp-iam DESIRED shows the same (statement 8). No new grant needed. |
| 5 enable + deploy | PHASE B, gated on G-A | PHASE B, gated on G-A |

### s.8.1 G1-G8

| # | opal_discover | portal_index |
|---|---|---|
| G1 read-only | `read_only=True`; both tools declared SAFE; reads the catalog only | `read_only=True`; all 3 tools declared SAFE, each is one S3 GetObject |
| G2 egress minimal | `hosts=("no-egress.invalid",)` (RFC 2606, never resolves; the validator refuses an empty allowlist) | `hosts=("opal-data-portal-v2.s3.amazonaws.com",)`, one exact host, no wildcard |
| G3 tool surface | 2 tools, `opal_` prefix, all read-only | 3 tools, `mdpf_` prefix, all read-only |
| G4 secret + IAM scoped | no secret, no grant | no secret; the live role policy above is scoped to 2 prefixes of 1 bucket. NOTE: `json-tiered/` is NOT covered, so a `json-tiered/...` key (the market-overview all-returns row) is not readable by this role. The catalog already marks that row BLOCKED-BY-ALLOWLIST. |
| G5 min_tier + below-tier deny | `min_tier="read_only"`: every verified caller passes, so there is no below-tier caller to deny. This is the read-only default the standard allows; the CTO rules whether a live below-tier probe applies. | same |
| G6 audit wired | both tools run through `run_integration_tool()` (credential_provider None), which writes `audit.log_call`. Served audit records are read live post-enable. | same |
| G7 fail-closed enablement | grounded: the MX-r-3 release shipped both dormant and the on-host tool list read 46 = 46 (row/ledger of that act); the host `.env` today carries `ycharts opal_portal globgrph` only | same |
| G8 enable = arch-gated deploy | this order: the change is env (line 197) + deploy, no IAM; CTO signs G1-G8 before, the CVO live-certs G5/G6/G7 after | same |

Other facts a reviewer needs for the two never-widen halves:
- Firm gate: both call `query_v0._principal()` and `catalog_gate.gate()`. A firm principal is shown only what the
  catalog lets it read; discover shows a non-servable row only to the opal-internal principal.
- The new tool names are in `data_entitlement.py` (INDEX_TOOLS, MX-t-8 item 10), so they are tier-classified on enable.
- Blast radius if the enable is wrong: 5 read-only tools appear on the live surface, 46 to 51. Rollback is the command
  in Step 4. No data, IAM, ALB, Terraform or secret changes.

## Rows

None filed in this phase. The two departures from the order's letter are stated above and are the issuer's to place:
(a) `deploy-to-ec2.sh` needs to be in `<paths>` for PHASE B, and bound 1's "never edited" needs the same exception for
line 197; (b) the same one-line change must also land on CLOUD.

## What PHASE B would do, once the issuer says GO (nothing below has been done)

1. Amended `<paths>`; edit line 197 in /c/tmp/mx-rel3 and commit as release commit 2 (override use 2); the same edit
   on the worker branch. Re-run AC-relevant tests. Announce the final release hash.
2. Read on-host over SSM: tool list (expect 46), `.env` ENABLED_INTEGRATIONS value only, `/health`.
3. NEVER-2 ledger `nfra-mcpindex-r3-gateway-enable` on the worker branch, entry and sentinel committed first.
4. `cd /c/tmp/mx-rel3 && bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.
5. Read `/health`, the tool list (expect 51), and the `.env` key set (26 = 26). Roll back at once if any read fails.
6. Record the manifest by hand on an LF copy if the Step-3 auto-commit fails, then the close run (one live question per
   surface: platinum/mdpf, platinum/etfs, platinum/advi, json/*), then close the ledger.
