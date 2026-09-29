# ANNOUNCE -- MX-r-5 PHASE A, opal-gateway narrow release: MX-d-4, MX-d-5, MX-t-9 and its entitlement

Deployer: 0.9.0_WK_NFRA_MCPINDEX~14 (issuer 2.0.0_SA_COO~MI). Order (CLOUD 0884771092, amended A1):
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-5.release-and-thread-rerun.md

STATE: PHASE A only. Nothing was deployed, no ledger is open, nothing was uploaded to S3, `deploy-to-ec2.sh:197` is
unchanged. AWS contact was read-only and all of it is Opal's own: `s3api list-objects-v2`, `s3 cp` download of two
artifact keys, `head-object` on the future key (404), and ONE SSM `AWS-RunShellScript` read of file hashes on the host.
MX-t-10 is not drained (issuer ruling under A1): no ETF file is in the release, and its uncommitted patch was not touched.

## A2 UPDATE (2.0.0_SA_COO~MI amendment A2, rulings on Z-W14-S5, S6, S8) -- READ THIS FIRST

Superseded by A2: the pin below is now **release 0001c9bb53, deploy-only ca48cd5482, gateway tree object
d2debddbd3e3977b0ed1ef0db00a4afd457be394**. Everything else in this file that names 510bf69089, b9e5c64437 or tree
3b35460af3 describes the FIRST pin; the base, the five carried commits, the rollback and the live-commit finding are unchanged.

- **PHASE A carrier recommitted** on the wk branch as 192df0755b: this file byte for byte from ed61b070e4, and rows
  Z-W14-S5..S8 appended to the end of CLOUD's channel (132 -> 136 rows; content-equal to the ed61b070e4 rows, `id` placed first).
- **Z-W14-S5 fixed, 33d2dd2fbf** (text and declaration only): opal_discover's module docstring, SPEC description and SPEC
  comment now state: no S3 object body is read; ONE S3 HEAD per servable row (`served_written_at`), under the gateway
  role's existing `json/*` and `platinum/*` grant; nothing leaves Opal's own AWS. `SPEC.hosts` is now
  `opal-data-portal-v2.s3.amazonaws.com` (was the never-resolving `no-egress.invalid`); base.py treats `hosts` as
  documentation and a non-empty check, so behaviour is unchanged. **The declaration now matches the behaviour.**
- **Z-W14-S6 fixed, a9092e0081:** `tests/test_entitlement_admin.py::test_ogz2_ac08` pins portal_index to 4 tools and the
  registered count to 52. It passes.
- **Z-W14-S8 CONFIRMED** for the rel- and dep- branches: two more uses of the audited override, both named: release commit
  0001c9bb53 (use 3) and deploy-only commit ca48cd5482 (use 4). The first two were 510bf69089 and b9e5c64437.
- **Release commit 0001c9bb53** = 510bf69089 + the gateway diff of 33d2dd2fbf and a9092e0081, applied with `git apply --3way`.
  test_entitlement_admin.py conflicted (the release base has an older text of the two lines than CLOUD) and the same
  one-pin, one-count change was made by hand on the release's text.
- **Deploy-only commit ca48cd5482** = b9e5c64437 + the gateway diff of 0001c9bb53 (31 files vs CLOUD 0c18ee586f, all under
  infra/aws/ec2/opal-gateway).

**Re-proof (A2 step 6):**
- Gateway tree object, dep vs release: `git rev-parse ca48cd5482:infra/aws/ec2/opal-gateway` =
  `0001c9bb53:infra/aws/ec2/opal-gateway` = **d2debddbd3e3977b0ed1ef0db00a4afd457be394**; `git diff --stat` between them is empty.
- Artifacts rebuilt (no upload) from the dep tree and the release tree: **79 of 79 byte-identical** (67 of 67 .py).
- Release vs the LIVE artifact: 75 of 79 identical, the same 4 shipped files differ (data_entitlement.py,
  opal_discover/integration.py, portal_index/integration.py, DATA_CATALOG.yaml). The SHIPPED delta did not grow.
- **Census: the git census is now 8 files, not 7** (`git diff --stat 4248b70b39 0001c9bb53 -- infra/aws/ec2/opal-gateway`,
  551 insertions, 49 deletions): the earlier 7 plus `tests/test_entitlement_admin.py` (+3 -2), which A2 step 3 puts on
  the branches. `tests/` is not in the artifact, so the artifact still differs from live in exactly 4 files. Row Z-W14-S9.
- `deploy-to-ec2.sh` is byte-identical to the live tree's (cmp); line 197 still carries the 5-id
  `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index`.
- Tests in the release tree: test_entitlement_admin, test_data_entitlement_guard, test_tool_classification_composition,
  test_opal_discover, test_portal_index: **50 passed, 4 failed**. The 4 are the ones already failing on the LIVE tree
  (test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08, and test_portal_tools_catalog_refs_resolve, whose source-file glob
  finds 3 catalog_entries yaml files while the catalog names 4 tools; the fourth yaml is outside the gateway tree and is
  not carried). **test_ogz2_ac08 now passes**, so the release adds no failing test. On the wk branch (CLOUD): test_ogz2_ac08,
  test_opal_discover, test_portal_index 27 passed.
- Artifact key at GO: `opal-gateway-ca48cd5482.tar.gz` (head-object: 404 now).

**G-A delta, restated:** item 1 (one new tool, 51 -> 52) is unchanged. Item 2 below (opal_discover's S3 HEAD) is now
DECLARED: the SPEC, its description and `hosts` state the one HEAD per servable row. Row Z-W14-S5's mismatch is closed
by 33d2dd2fbf; the disposition is the issuer's.

## THE RELEASE PIN (for the CTO's G-A arch-gate) -- FIRST PIN; see the A2 UPDATE above for the current one

| field | value |
|---|---|
| release branch | rel-nfra-mcpindex-r4-gateway (never merged, never pushed) |
| release commit (A2 pin) | 0001c9bb538ac24deb5dc5996b0006a9aba274c7 (first pin 510bf690896d8f70410901fc6cc7f4fe5fe40f4c, SUPERSEDED) |
| release worktree | /c/tmp/mx-rel5 |
| base = LIVE deployed commit | 4248b70b3911129588b96b32a4f74072151a8750 (NFRA_OPLGTW OG-x-3's release, deployed 2026-09-29T05:22:18Z) |
| gateway tree object, release = deploy-only | d2debddbd3e3977b0ed1ef0db00a4afd457be394 (first pin 3b35460af3, superseded) |
| deploy-only branch / commit | dep-nfra-mcpindex-r4-gateway (never merged, never pushed) / ca48cd548220a085581c5322c908c308772c0d95, on CLOUD 0c18ee586f (first deploy-only commit b9e5c64437019123a08b0fe6d8e5a644c39ebb46, SUPERSEDED) |
| deploy-only worktree | /c/tmp/mx-dep5 |
| rollback tree | /c/tmp/mx-rb5, detached at 4248b70b39 |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054, nested clone in all three trees, 0 status lines each, unchanged from the live deploy |
| artifact key at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-ca48cd5482.tar.gz (head-object: 404 now), plus `-latest` |
| worker branch (this file, rows, the A2 edits 33d2dd2fbf and a9092e0081) | wk-nfra_mcpindex-4-14 |


## Step 1: the live deployed commit, read BY CONTENT

The round-3 notes (0bce8d322a / gateway tree 3371f18803) are REFUTED. The host serves **4248b70b39**.
- `s3api list-objects-v2` on ec2/opal-gateway/: keys 0bce8d322a (2026-09-29T02:45Z), 7c7ebe14d3 (03:24Z), 4248b70b39
  (05:21Z), `-latest` (05:21:55Z). `-latest` is 406162 bytes, md5 a59f391592ae00f6725f4bbe2df2a6f8, identical to the
  4248b70b39 key. CLOUD's EC2_MANIFEST.json already reads deployed_commit 4248b70b39 (deployed_by 0.9.0_WK_NFRA_OPLGTW~11).
- Host read: one SSM `AWS-RunShellScript` on i-07dccb1615503ac99, sha256 of every file under app, deploy, dashboard,
  requirements.txt, identity_tool_allowlist.txt in /opt/opal-gateway, compared per file with the `-latest` artifact:
  **79 of 79 identical**, 0 only-host, 0 only-artifact.
- 4248b70b39 is a release-branch commit (f791522306 plus OG-x-3's 9 gateway files); it is not on CLOUD. Row Z-W14-S7.

## Step 2: the release tree and the census

Cut: `git worktree add -b rel-nfra-mcpindex-r4-gateway /c/tmp/mx-rel5 4248b70b39`. The five commits' GATEWAY files only,
applied oldest first with `git diff <c>^ <c> -- infra/aws/ec2/opal-gateway | git apply --3way --index`:

| order | commit | author | what | gateway files |
|---|---|---|---|---|
| 1 | 2984d17cc3 | ~14 | MX-d-4: next_tool names the purpose-built tool (R-13); served_written_at (R-14) | opal_discover/integration.py, tests/test_opal_discover.py |
| 2 | d2c9bb448f | ~14 | MX-d-5: weak-match rule, S&P vocabulary (emitter-regenerated catalog) | opal_discover/integration.py, app/refs/DATA_CATALOG.yaml, tests/test_opal_discover.py |
| 3 | 51dfc8879d | ~14 | MX-d-5 A1: harness compares by dataset | tests/routing/run_routing.py |
| 4 | 4278c7174f | ~15 | MX-t-9: mdpf_get_model_benchmarks (4th portal_index tool) | portal_index/integration.py, app/refs/DATA_CATALOG.yaml, tests/test_portal_index.py |
| 5 | 5a450314de | ~15 | INDEX_TOOLS names mdpf_get_model_benchmarks | app/data_entitlement.py, tests/test_portal_index.py |

Non-gateway files of those commits (proof instances, INVESTIGATION rows, EQUALITY_MX-t-9.md, the
catalog_entries/portal_mdpf_model_benchmarks.yaml source file, emit_catalog_v02.py) are NOT carried.

One conflict: DATA_CATALOG.yaml's two build-stamp lines (commit 2 stamped `c7e619aabb`, commit 4 stamped `120ff9b27f`).
The later commit's stamp (`120ff9b27f`) was kept. CLOUD carries a third stamp (`dba953e00c`) from a later regeneration;
the release catalog therefore differs from CLOUD's by exactly those 2 stamp lines.

Release commit 510bf69089, made under the audited `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_MCPINDEX~14`. Row Z-W14-S8.

**Census** `git diff --stat 4248b70b39 510bf69089 -- infra/aws/ec2/opal-gateway`: **7 files, 538 insertions, 40 deletions**:
app/data_entitlement.py (+1); app/integrations/opal_discover/integration.py (+168); app/integrations/portal_index/integration.py (+42);
app/refs/DATA_CATALOG.yaml (+33); tests/routing/run_routing.py (+35); tests/test_opal_discover.py (+168);
tests/test_portal_index.py (+131). The whole-tree diff is the same 7 files. That equals the union of the five commits'
gateway files: 0 extra, 0 missing. Six of the seven are byte-identical to CLOUD's blobs (the seventh is the catalog, above).
Only 4 of the 7 are in the shipped artifact (tests/ is not), and those 4 are the only per-file differences from the live
artifact: 75 of 79 identical, 4 differ.

`deploy-to-ec2.sh` is byte-identical (cmp) in the release, deploy-only and rollback trees. Line 197 keeps
`ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index` (5 ids).

Tests in the release tree (from infra/aws/ec2/opal-gateway): test_opal_discover, test_portal_index,
test_tool_classification_composition, test_entitlement_admin, test_data_entitlement_guard: **49 passed, 5 failed**.
The live tree (4248b70b39) on test_portal_index + test_entitlement_admin + test_data_entitlement_guard: 24 passed, 4 failed.
The 4 are already there: test_portal_tools_catalog_refs_resolve (a glob of source files outside the gateway tree),
test_ogz2_ac06, test_ogz1_ac05, test_ogz1_ac08. The release adds ONE: **test_ogz2_ac08**, whose pin names 3 portal_index
tools and `== 51`; it fails on CLOUD too (the file does not name the fourth tool). tests/ ships nothing. Row Z-W14-S6.

## Step 3: the rollback tree and the deploy-only tree

**Rollback, proven per file against the live artifact.** /c/tmp/mx-rb5 = detached 4248b70b39, mcportal a3bff71ffa cloned
beside it and built (`bun install --frozen-lockfile`, `bun run build`). A build-only mirror of deploy-to-ec2.sh:78-91 (the
same `tar -czf` and excludes, NO upload line) produced a 406160-byte artifact. Compared with the downloaded live
`-latest` artifact: **79 of 79 files byte-identical** (67 of 67 .py), 0 only-live, 0 only-rebuilt.

**Deploy-only tree** (the MX-r-4 A2 / OA-r-1 pattern). `git worktree add -b dep-nfra-mcpindex-r4-gateway /c/tmp/mx-dep5 CLOUD`
(CLOUD 0c18ee586f), then `git rm -r -q infra/aws/ec2/opal-gateway` and
`git checkout 510bf69089 -- infra/aws/ec2/opal-gateway`, ONE commit **b9e5c64437** (override use 2 of 2). Row Z-W14-S8.
- Tree-object equality: `git rev-parse HEAD:infra/aws/ec2/opal-gateway` in the dep tree = `510bf69089:infra/aws/ec2/opal-gateway`
  = **3b35460af3af112af72688a634fce760f4ef0dce**; `git diff --stat 510bf69089 HEAD -- infra/aws/ec2/opal-gateway` is empty.
- The commit touches 30 files, every one under infra/aws/ec2/opal-gateway.
- Artifact equality: artifacts rebuilt (no upload) from the dep tree and the release tree, per file: **79 of 79
  byte-identical**, 67 of 67 .py.
- Halt gate: at the dep tree's HEAD the MX-r-5 order has `<issued_to>0.9.0_WK_NFRA_MCPINDEX~14</issued_to>` and
  `<status>pending</status>`.
- N1 at the deploy reads: HEAD b9e5c64437, its gateway dir equal to 510bf69089's, mcportal a3bff71 with 0 status lines.
  `git status` of the dep tree shows ` M mcportal` (the CLOUD gitlink names another mcportal commit than the nested clone).
- The deploy-only tree carries CLOUD's `safe-ec2-deploy.sh`, which differs from the live tree's by one line (`| tr -d '\r'`
  on the manifest rewrite, a919c53f31); it is the script the deploy will run.

## THE G-A DELTA

Against the live gateway (4248b70b39) the release changes the shipped surface as follows.

**1. ONE new tool: `mdpf_get_model_benchmarks`** (`portal_index`, `mdpf_` prefix, MX-t-9). Live tool count 51 -> 52.
- Read-only, SAFE, `min_tier=read_only`; one S3 GetObject of `json/benchmarks/model_portfolio_benchmarks.json`
  (opal-data-portal-v2), whole object, host `opal-data-portal-v2.s3.amazonaws.com`.
- No new IAM: the role already reads `opal-data-portal-v2/json/*` and `platinum/*` (MX-r-4 announcement, `get-role-policy`).
- The key is read from the catalog row of accessor `getModelPortfolioBenchmarks` (a new `portal_datasets` row), never from the module.
- Firm gate: measured in the release tree, the opal-internal principal resolves the key; a firm principal
  (`49financial`) is REFUSED (`catalog_gate: row firm='opal-internal' is not visible to firm`). Nothing widens to a firm.
- Every answer carries a model-design caveat and the two-basis note.
- Entitlement: `data_entitlement.py` INDEX_TOOLS names it (5a450314de), so it is tier-classified on enable.

**2. `opal_discover` now performs one S3 HEAD per servable row it returns** (MX-d-4, R-14, `served_written_at`).
AS FIRST CUT its SPEC declared `hosts=("no-egress.invalid",)` and its description said it reads no S3 object (corrected by A2, see above). Measured on the
release catalog with the opal-internal principal: 24 servable rows, every HEAD key under `json/` (21) or `platinum/` (3),
inside the role's granted scope; a failed HEAD reads `absent` with an error class. **At the first cut the declaration and the
behaviour disagreed (row Z-W14-S5, ARMED); A2's 33d2dd2fbf makes the declaration state the HEAD, so they now agree.**

**3. Behavior changes with no new surface:** `next_tool` names the purpose-built tool (R-13); a weak one-word channel
match answers NOT_CATALOGUED (MX-d-5); S&P vocabulary on the market_regime_trending channel (mkt.01's channel, no new row).

Blast radius if the release is wrong: 1 new read-only tool and changed discover answers on the live surface; no data, IAM,
ALB, Terraform, secret or `.env` change. Rollback is below.

## THE ROLLBACK

- **Tree:** /c/tmp/mx-rb5 (detached 4248b70b39, mcportal a3bff71 built), rebuild proven 79 of 79 against the live artifact.
- **Command:** `cd /c/tmp/mx-rb5 && HALT_ACK=1 AGENT_NAME=<deployer serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
  (HALT_ACK=1 only when the halt gate reads 0 STOP). The rollback tree has no task order at HEAD, so the gate's
  worker-admission rule will refuse a worker there; the issuer or the deployer identity runs it.
- **What it restores:** the same artifact key `opal-gateway-4248b70b39.tar.gz` and `-latest`, and the `.env` value
  `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index` (line 197 is byte-identical in all three trees).
  Host tool count returns to 51.
- The rollback tree carries the older `safe-ec2-deploy.sh` (without the CR strip); it needs nothing from CLOUD.

## What PHASE B would read on the host after the deploy (nothing below has been done)

`/health` 200; `.env` key set and the 5-id ENABLED_INTEGRATIONS unchanged; tool count 51 -> 52 (exactly
mdpf_get_model_benchmarks); per-file host hashes equal to the release's 79 files (4 changed: data_entitlement.py,
opal_discover/integration.py, portal_index/integration.py, DATA_CATALOG.yaml); NEVER-2 ledger
`nfra-mcpindex-r4-gateway-release` opened first.

## Rows filed (channel INVESTIGATION_v1.md)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W14-S5 | OBSERVATION / ARMED (disarm 2.0.0_SA_COO~MI) | opal_discover's egress declaration was stale against its S3 HEAD; corrected in 33d2dd2fbf (A2) |
| NFRA_MCPINDEX-Z-W14-S6 | OBSERVATION / INERT | test_ogz2_ac08 needs the fourth tool in its pin (51 -> 52), on CLOUD and the release |
| NFRA_MCPINDEX-Z-W14-S7 | OBSERVATION / INERT | the live commit is 4248b70b39, not 0bce8d322a / 3371f18803 |
| NFRA_MCPINDEX-Z-W14-S8 | OBSERVATION / INERT | two audited overrides (rel and dep commits) on the MX-r-4 precedent |
| NFRA_MCPINDEX-Z-W14-S9 | OBSERVATION / INERT | A2 step 6 says the census is still 7 files; with test_entitlement_admin.py it is 8 in git, 4 shipped (unchanged) |
