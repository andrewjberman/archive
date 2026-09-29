# ANNOUNCE -- OG-x-3 RE-CUT (amendment A2), opal-gateway narrow release of OG-x-2's streaming export, PHASE A ONLY

Deployer: 0.9.0_WK_NFRA_OPLGTW~11 (issuer 2.0.0_SA_COO~O). Supersedes `ANNOUNCE_OG-x-3.md` (cut on d287ffb346, now stale).
Task order: org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-x-3.streaming-export-release.md (A2 at edada1279c).

STATE: announced, NOT started. Nothing is uploaded, no ledger is open, no deploy has run. Instance contact: two read-only
SSM `RunShellScript` commands (a full md5 manifest of the host's shipped files + `.env` counts; the tool-name list).
Waiting for PHASE B GO.

| field | value |
|---|---|
| service / instance | opal-gateway / i-07dccb1615503ac99 |
| live commit (host serves) | DEPLOY-ONLY 7c7ebe14d320766af06abafabc2d21fa4cbb195f; its gateway tree 01264d4d90 = release f791522306ded5a95e72839d119dd99e96db5513 (OA-e-3) = 3371f18803 + 7 files |
| release base | f791522306 (same gateway tree as the live commit) |
| release branch / worktree | rel-nfra-oplgtw-stream-export-v2 (LOCAL), /c/tmp/og-x3-rel2 |
| release commit | 4248b70b3911129588b96b32a4f74072151a8750 (author `0.9.0_WK_NFRA_OPLGTW~11 <...>`) |
| mcportal (dashboard bundle) | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054, unchanged (= CLOUD manifest `mcportal_commit`) |
| artifact to upload at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-4248b70b39.tar.gz (+ latest) |
| rollback tree | /c/tmp/og-x3-rb2, detached at 7c7ebe14d3 |
| stale tree | /c/tmp/og-x3-rel @7b729821a9 (branch rel-nfra-oplgtw-stream-export): DISCARDED, never deployed, left in place undeleted |
| CLOUD manifest at 2026-09-29T04:19Z | `deployed_commit` f791522306 (CLOUD HEAD aa999ff9fc); `mcportal_commit` a3bff71ffa |

## Step 0: one-deployer census (A1), repeated for the re-cut

`git worktree list --porcelain`: 116 trees. Per-tree `ls-tree` counts in `census_open_deploys_phaseA_recut.txt` (116 lines, sum
1,230 entries). Content scan of the 54 distinct sentinel blobs for `gateway`: the same five as before -- three
`.unindexed_red_state.json` (old entry names), `opsec-s10c-session-analytics-act2.json` (an API-Gateway phrase), and the
superseded `nfra-oplgtw-og-r-1-first-release.json` (closed on CLOUD at 45d1e43657, ruled stale). Working-directory scan of
all 116 trees: no other `.open_deploys/*.json` mentions gateway. No other open gateway sentinel; MX-r-4 and OA-e-3 have
closed. Repeated immediately before PHASE B's act.

## Step 1: the live commit, resolved BY CONTENT (SSM Success, command e405d1cd-505a-490a-ac18-33021a6d6193)

Host manifest (`host_manifest_recut.txt`): md5 of every file under `/opt/opal-gateway/app` and `deploy` (excluding
`__pycache__`/`.pyc`) plus `requirements.txt` and `identity_tool_allowlist.txt`: 76 files.

| candidate | files matching the host | differ |
|---|---|---|
| 7c7ebe14d3 (deploy-only) | **76 of 76** | 0 |
| f791522306 (release) | **76 of 76** | 0 |
| 3371f18803 (MX-r-4 pin) | 74 of 76 | app/asker_scope.py, app/identity_scope.py |

`git diff f791522306 7c7ebe14d3 -- infra/aws/ec2/opal-gateway` is empty. Host `.env`: `ENABLED_INTEGRATIONS=ycharts
opal_portal globgrph opal_discover portal_index`; 27 keys; `SPRINT_VIEW_ALLOWED_EMAILS` count 1 (no value printed);
`dashboard/` 3 files; `/health` 200; `opal-gateway` active since 2026-09-29 03:25:06 UTC.

## Step 2: this cell's commits

One CLOUD commit touching the gateway tree with author `0.9.0_WK_NFRA_OPLGTW~11 <`: `0c3d545002` (OG-x-2's build).

## Step 3: release tree, census, commit

`git worktree add -b rel-nfra-oplgtw-stream-export-v2 /c/tmp/og-x3-rel2 f791522306`; `git cherry-pick --no-commit 0c3d545002`;
one conflict, the surprise-channel `INVESTIGATION_v1.md` (non-gateway), pinned back to f791522306. Non-gateway paths changed:
0. Commit `4248b70b39` under `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~11` (issuer-authorized; **1 use, this release-branch
commit only**; used directly because the first PHASE A attempt at the previous base was lane-refused for the same reason).

Census: `git diff --stat f791522306 HEAD -- infra/aws/ec2/opal-gateway`: 9 files, 552 insertions, 97 deletions;
the changed-file set equals `0c3d545002`'s (`diff` of the two name lists is empty): `schwab/{engine,envelope,export,integration}.py`,
`tests/acceptance/conftest.py`, `tests/test_schwab_{engine,export,export_stream,query}.py`. **`deploy-to-ec2.sh` is unchanged**
(`git diff --cached f791522306 -- deploy-to-ec2.sh` empty; its line writes `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph
opal_discover portal_index`, the host's current value). `download_routes.py` and `identity_scope.py`/`asker_scope.py` unchanged.

## Step 4: tests on the release tree

`AUDIT_PATH=$(mktemp)`, `/c/tmp/og-x3-rel2/infra/aws/ec2/opal-gateway`, `.venv-og` (python 3.11.9, `app` imported from the
release tree), modules run one by one: test_schwab_export_stream **2 passed** (86.8 s), test_schwab_export **27 passed**,
test_schwab_engine **13 passed**, test_schwab_query **26 passed**: **68 passed, 0 failed, rc=0 each.** (A first single
invocation of the four modules hit my own 550 s bound, rc 124, on a heavily loaded box; the split runs are the record.
The export_stream module took 86.8 s here against 44.9 s on OG-x-2's run: a `timeout 110` on it has little margin.)

## Step 5: mcportal pin

`/c/tmp/og-s1-rel/mcportal` (clean clone with node_modules) copied to `/c/tmp/og-x3-rel2/mcportal` and `/c/tmp/og-x3-rb2/mcportal`.
HEAD in both: `a3bff71ffa3f5c73aa0fb7ea1e7386434e233054` = the manifest's `mcportal_commit`. At 7c7ebe14d3 `mcportal` is a
tracked gitlink (empty dir); the clone sits in that directory (a first `cp` nested it one level too deep and was moved up).
`bun install --frozen-lockfile`: 77 installs, no changes; `bun run build`: `dist/index.html`.

## Step 6: rollback proven against the NEW live artifact (built, not uploaded)

`/c/tmp/og-x3-rb2` at 7c7ebe14d3 (unedited), mcportal at the pin. Build-only mirror of `deploy-to-ec2.sh`'s tar step: 79
files. Live artifact `opal-gateway-7c7ebe14d3.tar.gz` (403158 bytes, 2026-09-29T03:24:49Z; the key names the live commit
this time). Extracted: 79 files. `diff -rq`: **empty, 79 of 79 identical.**
Re-deploy command: `cd /c/tmp/og-x3-rb2 && HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~11 bash
infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`.

## Step 7: blast radius, measured (SSM commands 90a68317-5f17-47ff-9311-f1ab810a1e13 and e405d1cd-...)

- `ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index`. **`schwab` is NOT in it: DELTA=0.**
- On-host tool-name list: **51** tools (was 46 at the last cut: +`mdpf_get_account_distribution`, `mdpf_get_aggregate_aua`,
  `mdpf_get_aum_metrics`, `opal_describe`, `opal_discover`), sorted, in `tools_before_phaseA_recut.txt`. The release adds no tool.

## At GO (not done yet)

9. BEFORE reads: tool list = the 51 in `tools_before_phaseA_recut.txt` (sorted diff empty), `ENABLED_INTEGRATIONS` value
   unchanged, CLOUD/live base unchanged (host 76 of 76 = 7c7ebe14d3). Repeat the census; another open gateway sentinel or a
   moved base means STOP and re-cut.
10. Open a FRESH NEVER-2 ledger, slug `nfra-oplgtw-stream-export-release`, new timestamp (the earlier entry stays ABANDONED);
    commit entry + sentinel before the act.
11. From `/c/tmp/og-x3-rel2`: `HALT_ACK=1 AGENT_NAME=0.9.0_WK_NFRA_OPLGTW~11 bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway
    infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`; mcportal HEAD must still be the pin.
12. Verify on the host within 90 s: `/health` 200; md5 of the 5 schwab/download files = 4248b70b39's bytes; tool list AFTER =
    BEFORE (51); `ENABLED_INTEGRATIONS` unchanged; on-host 76-file manifest = 4248b70b39's tree. Failure: rollback, re-verify, close
    ROLLED BACK.
13. Record `EC2_MANIFEST.json` (LF copy): deployed_commit = 4248b70b3911129588b96b32a4f74072151a8750, previous_deployed_commit =
    the manifest's current value at that time (f791522306 now; the host serves its deploy-only twin 7c7ebe14d3), mcportal
    unchanged, release_note. Close the ledger, commit, run AC1-AC3. Any criterion that reads `xr.AC*.sh` runs against the
    record then.

Announced 2026-09-29T04:2xZ.
