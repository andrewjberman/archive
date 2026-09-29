# ANNOUNCE -- OG-x-3, opal-gateway narrow release of OG-x-2's streaming export, PHASE A ONLY

**SUPERSEDED 2026-09-29 by `ANNOUNCE_OG-x-3_RECUT.md` (amendment A2): the base d287ffb346 and release 7b729821a9 below are STALE; do not deploy them.**

Deployer: 0.9.0_WK_NFRA_OPLGTW~11 (issuer 2.0.0_SA_COO~O). Task order:
org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-x-3.streaming-export-release.md (amendment A1 at 42631b4edb).

STATE: announced, NOT started. Nothing is uploaded, no ledger is open, no deploy has run. The only instance contact was
two read-only SSM `RunShellScript` commands (file md5s + `.env` key count and `ENABLED_INTEGRATIONS` value; the
tool-name list). Waiting for GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| live base (release base) | d287ffb346beb58911fdaae08b9a44427e98aafe (OA-r-1's release; NOT 6a98a0553a any more) |
| release branch | rel-nfra-oplgtw-stream-export (LOCAL), worktree /c/tmp/og-x3-rel |
| release commit | 7b729821a9 (author `0.9.0_WK_NFRA_OPLGTW~11 <...>`) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054, unchanged, nested clones in the release and rollback trees |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-7b729821a9.tar.gz (+ latest) |
| NEVER-2 ledger slug (PHASE B) | nfra-oplgtw-stream-export-release |
| rollback tree | /c/tmp/og-x3-rb, detached at d287ffb346 |
| this record | worktree /c/tmp/wk-oplgtw-11, branch wk-NFRA_OPLGTW-11 |
| CLOUD HEAD read at 2026-09-29T01:29Z | 2da2daa9b7 |

## Step 0: one-deployer census (A1), 2026-09-29T01:2xZ

- `git worktree list --porcelain`: 103 trees. Per-tree count of `git ls-tree -r --name-only HEAD
  org/critical_paths/.open_deploys/` is in `census_open_deploys_phaseA.txt` beside this file (103 lines; sum 1,076
  entries; range 3 to 15 per tree; the main tree 14, this worktree 14).
- Content scan of the 51 distinct sentinel blobs for the string `gateway`: five blobs mention it. Three are
  `.unindexed_red_state.json` (old change-management entry NAMES containing the word gateway, not sentinels), one is
  `opsec-s10c-session-analytics-act2.json` (an API-Gateway phrase in a Lambda deploy), and ONE is a gateway deploy:
  `nfra-oplgtw-og-r-1-first-release.json` at HEAD of `/c/tmp/mp-2-rb`, status OPEN, opened 2026-09-18, author
  0.9.0_WK_NFRA_OPLGTW~2. Working directories of 18 more rollback/release trees hold an uncommitted copy of it.
- Working-directory scan of all 103 trees for any `.open_deploys/*.json` mentioning `gateway`: only those 19
  rollback/release copies and the opsec file. No NFRA_OPALAI OA-r-1 or NFRA_MCPINDEX MX-r-4 sentinel is open.
- That OG-r-1 sentinel's ledger is CLOSED on CLOUD (entry closed 20260918T070646Z; the sentinel is absent from
  `git ls-tree CLOUD`). I judged it a stale copy in dead rollback trees, not another seat's deploy, and did not stop.
  This is row `NFRA_OPLGTW-Z-W11-S4` (ARMED, disarm_owner 2.0.0_SA_COO~O): **a literal reading of A1 step 0 stops here;
  the issuer decides.** PHASE B repeats the census.

## Step 1: the live commit, by content (SSM Success, command 68505f9a-fa74-4da7-9190-0c6ece1578fc)

`EC2_MANIFEST.json` `services.opal-gateway.deployed_commit`: at my HEAD `6a98a0553a` (2026-09-27T22:17:33Z); at CLOUD
`d287ffb346` (deployed_at 2026-09-29T00:45:15Z, deployed_by 0.9.0_WK_NFRA_OPALAI~10, previous `6a98a0553a`). The newer,
`d287ffb346`, is used; it resolves (`git cat-file -e`).

| file (/opt/opal-gateway/) | host md5 | d287ffb346 | 6a98a0553a |
|---|---|---|---|
| app/integrations/schwab/engine.py | 10b0417a192de2a3beda7cfba2b23a56 | match | match |
| app/integrations/schwab/integration.py | e8a45441e9e16281da8c380ab5fe28be | match | match |
| app/integrations/schwab/export.py | 28b5c7ffe1b367788d8912f18558d8fe | match | match |
| app/integrations/schwab/envelope.py | c4ade82d98c030868ba10752b3438c62 | match | match |
| app/download_routes.py | 74f8843ea829b520ddf7db436f9fe52d | match | match |
| app/asker_scope.py (discriminator) | 7e6bf35edb06099331f81561528a0ea8 | match | differs |
| app/tools.py (discriminator) | 7ead9892a2f75b5b3326c0c16a1bcd46 | match | differs |
| app/server.py | 1339aca9648e88ed754edcf902b7af26 | match | match |

5 of 5 named files match `d287ffb346`; the two discriminators (which change between `6a98a0553a` and `d287ffb346`) also
match `d287ffb346`, so the live commit is `d287ffb346`. `.env` key `SPRINT_VIEW_ALLOWED_EMAILS` count = 1 (no value printed).

## Step 2: this cell's commits

CLOUD commits touching `infra/aws/ec2/opal-gateway` with author exactly `0.9.0_WK_NFRA_OPLGTW~11 <`: one,
`0c3d545002` (OG-x-2's build; an ancestor of CLOUD). `34fb16cee3` (proof + result) touches no gateway path.

## Step 3: release tree, census, commit

`git worktree add -b rel-nfra-oplgtw-stream-export /c/tmp/og-x3-rel d287ffb346`; `git cherry-pick --no-commit 0c3d545002`.
One conflict, the surprise-channel `INVESTIGATION_v1.md` (a non-gateway path); pinned back with
`git checkout d287ffb346 -- <that path>`. Non-gateway paths changed after the pin: 0.

Commit `7b729821a9`. The first `safe-commit.sh` attempt was lane-refused (the release tree's HEAD predates this order, so no
order at that HEAD grants the path). **Override use: 1 of 1, `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~11`, this
release-branch commit only.**

Census, `git diff --stat d287ffb346 HEAD -- infra/aws/ec2/opal-gateway`: 9 files changed, 552 insertions, 97 deletions:
`schwab/engine.py`, `schwab/envelope.py`, `schwab/export.py`, `schwab/integration.py`,
`tests/acceptance/conftest.py`, `tests/test_schwab_engine.py`, `tests/test_schwab_export.py`,
`tests/test_schwab_export_stream.py` (new), `tests/test_schwab_query.py`. Exactly the files 0c3d545002 changed;
`download_routes.py` is not among them. Anything else: none.

## Step 4: tests on the release tree

`AUDIT_PATH=$(mktemp)`, in `/c/tmp/og-x3-rel/infra/aws/ec2/opal-gateway`, interpreter `.venv-og` (python 3.11.9;
`app` imported from the release tree): `pytest tests/test_schwab_export_stream.py tests/test_schwab_export.py
tests/test_schwab_engine.py tests/test_schwab_query.py -q -p no:cacheprovider` -> **68 passed, 0 failed, rc=0**
(2 + 27 + 13 + 26), 101.56 s.

## Step 5: mcportal pin

Copied `/c/tmp/og-s1-rel/mcportal` (a clone with node_modules, HEAD `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054`, clean)
to `/c/tmp/og-x3-rel/mcportal` and `/c/tmp/og-x3-rb/mcportal`. HEAD in both: `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054` =
the manifest's `mcportal_commit`. `node_modules/` present. `bun install --frozen-lockfile`: "77 installs across 128
packages (no changes)"; `bun run build`: `dist/index.html` produced.

## Step 6: rollback proven (built, not uploaded)

`/c/tmp/og-x3-rb`, HEAD `d287ffb346` (detached, unedited), mcportal at the pin. Build-only mirror of
`deploy-to-ec2.sh`'s tar step (app, deploy, requirements.txt, identity_tool_allowlist.txt + `dashboard/`, same excludes):
79 files. **The live artifact is `opal-gateway-54e26d66a0.tar.gz`, not `-d287ffb346`** (OA-r-1 deployed from a never-merged
deploy-only tree, HEAD `54e26d66a0`, whose gateway directory is identical to d287ffb346's; 402043 bytes, LastModified
2026-09-29T00:44:45Z; `-d287ffb346` is a 404): row `NFRA_OPLGTW-Z-W11-S5` (INERT). Downloaded and extracted: 79 files.
`diff -rq` of the two extracted trees: **empty, 79 of 79 identical.**

Re-deploy command: `cd /c/tmp/og-x3-rb && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~11 bash
infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
(it uploads `opal-gateway-d287ffb346.tar.gz` and `latest`).

## Step 7: the blast radius, measured (SSM Success, commands a4f45eb6-d4cd-442b-b38e-997e5391ab73 and 68505f9a-fa74-4da7-9190-0c6ece1578fc)

- `.env` `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph`. **`schwab` is NOT in it: DELTA=0** -- no caller can mint a
  download ticket, so no served answer changes.
- On-host tool-name list: **46** tools, sorted, in `tools_before_phaseA.txt` beside this file (includes
  `opal_asker_query`, added by OA-r-1). The release adds no tool.

## Surprise rows filed (INVESTIGATION_v1.md)

`NFRA_OPLGTW-Z-W11-S4` (stale gateway sentinel copies in 19 old rb/rel trees; ARMED, disarm_owner 2.0.0_SA_COO~O),
`NFRA_OPLGTW-Z-W11-S5` (live artifact key is 54e26d66a0; INERT).

## At GO (not done yet)

9. BEFORE reads over SSM: tool list = the 46 in `tools_before_phaseA.txt` (sorted diff empty), `ENABLED_INTEGRATIONS`
   value unchanged. Repeat the step-0 census AND re-read CLOUD's `EC2_MANIFEST.json` `deployed_commit` (still
   `d287ffb346`?); a moved base or another gateway sentinel means STOP and re-cut on the new base.
10. Open NEVER-2 ledger `nfra-oplgtw-stream-export-release`; commit entry + sentinel before the act.
11. From `/c/tmp/og-x3-rel`: `HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~11 bash infra/aws/ec2/safe-ec2-deploy.sh
    opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (mcportal HEAD must still be the pin).
12. Verify on the host within 90 s: `/health` 200; md5 of the 5 step-1 files = release commit 7b729821a9's bytes; tool
    list AFTER = BEFORE; `ENABLED_INTEGRATIONS` unchanged. Any failure: rollback, re-verify, close ROLLED BACK.
13. Record `EC2_MANIFEST.json` on an LF copy (deployed_commit = 7b729821a9 full, previous = d287ffb346 full), close the
    ledger, commit, run AC1-AC3.

Announced 2026-09-29T01:4xZ.
