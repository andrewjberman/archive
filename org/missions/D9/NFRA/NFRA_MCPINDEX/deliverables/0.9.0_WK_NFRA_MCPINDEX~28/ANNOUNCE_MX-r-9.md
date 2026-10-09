# ANNOUNCE -- MX-r-9 PHASE A: the discover-needs release on the live ref aa75078e1b (MX-d-7 true as-of, MX-c-6 the 29 needs, MX-d-8 discover answers needs)

Deployer: 0.9.0_WK_NFRA_MCPINDEX~28 (issuer 2.0.0_SA_COO~MI). Order:
org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-r-9.discover-needs-release.md. Pattern: MX-r-8 PHASE A (ANNOUNCE_MX-r-8.md in deliverables/0.9.0_WK_NFRA_MCPINDEX~22) and MX-r-6's order, as amended.
Probes: org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~28/probes_r9/ (every file named below is there).

STATE: PHASE A only. Nothing deployed, no ledger opened, nothing uploaded to S3, no Terraform, no grant, identity, role or sign-in created or changed, no push.
AWS contact: read-only, Opal's own: S3 `head-object`, `list-objects-v2` and one `-latest` download; SSM `AWS-RunShellScript` reads of file hashes and `.env` KEY NAMES (the host `.env` parsed in Python by `probes_r9/host_read.py`, never shell-sourced: row Z-S73); local in-process reads of three served S3 objects under my own credentials.

## BASE-MOVED CLAUSE, by REF

**Every pin below is valid ONLY while the live ref is `aa75078e1b72a28219e6148d3ec8e9bf705ea111` (NFRA_OPLGTW OG-rl-14, r28b).** Three reads, all equal:

| read | time (UTC) | live ref |
|---|---|---|
| 1. PHASE A start | 2026-10-09T08:26:00Z (S3), 08:34:23Z (host) | aa75078e1b |
| 2. mid-PHASE A | 2026-10-09T09:10:25Z (S3), 09:10:35Z (host) | aa75078e1b |
| 3. **immediately before this ANNOUNCE** | **2026-10-09T09:42:01Z (S3), 09:42:12Z (host)** | **aa75078e1b** |

Read three ways at read 3 (probes_r9/live_ref_reread_FINAL.txt):
- S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` metadata `git-ref` = aa75078e1b72a28219e6148d3ec8e9bf705ea111 (LastModified 2026-10-07T21:48:40Z, 509420 bytes, ETag 58f375cd26242c93b78b075eccb0ff94). The newest keys are `-aa75078e1b` (21:48:34Z) and `-latest` (21:48:40Z); none newer.
- `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway.deployed_commit` = aa75078e1b72a28219e6148d3ec8e9bf705ea111 on CLOUD (e43ee663be) and on box/sitez (c225bcc74e); deployed_at 2026-10-07T21:49:10Z, deployed_by 0.9.0_WK_NFRA_OPLGTW~28, `mcportal_commit` a3bff71ffa3f5c73aa0fb7ea1e7386434e233054.
- The host `/opt/opal-gateway`, by content: 100 of 100 files byte-identical to `-latest` (host_vs_latest_PHASEA.txt at read 1; the same 100 of 100 at read 3), `/health` 200, 51 `.env` keys (51 distinct), `ENABLED_INTEGRATIONS` = `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7 ids).

**No release landed between the reads.** The queue is the hazard (row NFRA_MCPINDEX-Z-W28-S7, ARMED, disarm_owner 2.0.0_SA_COO~MI): NFRA_OPLGTW's OG-rl-15 is cut on this same base (branch `rel-nfra-oplgtw-r29` @91811b648a, worktree C:/tmp/og-rel29, 1 commit over aa75078e1b, not deployed; no gateway ledger is open in the shared tree: 0 gateway sentinels under `.open_deploys/`, probes_r9/open_ledgers_PHASEA.txt). Whichever of the two lands second re-cuts on the first's ref, and if the live ref is anything else at the GO or at PHASE B's first act, every pin below is VOID. PHASE B passes the base to the guard (`DEPLOY_BASE_REF=aa75078e1b72a28219e6148d3ec8e9bf705ea111`), which refuses at UPLOAD time with nothing written.

## THE PINS (for the never-widen halves)

| field | value |
|---|---|
| base = LIVE ref | **aa75078e1b72a28219e6148d3ec8e9bf705ea111** |
| release branch | `rel-nfra-mcpindex-r9-discover-release`, worktree C:/tmp/mx-rel-r9 (sparse), never merged, never pushed |
| **release commit** | **bf7988eab99150e2a5e1b494a21ca47eaf382691** (parent aa75078e1b; 5 files, +1003 -47, all inside infra/aws/ec2/opal-gateway; 0 files outside) |
| deploy-only branch | `dep-nfra-mcpindex-r9-discover-release`, worktree C:/tmp/mx-dep-r9 (sparse), on CLOUD e43ee663be, never merged, never pushed |
| **deploy-only commit** | **7eeb4423f893deb104a78297b9eab2b4807868e6** (parent CLOUD e43ee663be) |
| **gateway tree object, release = deploy-only** | **39d274dee7aee89e9f07b74a8938d90259e1b525** (`git rev-parse bf7988eab9:infra/aws/ec2/opal-gateway` = `git rev-parse 7eeb4423f8:infra/aws/ec2/opal-gateway`; `git diff --stat bf7988eab9 7eeb4423f8 -- infra/aws/ec2/opal-gateway` is 0 lines) |
| **rollback tree** | C:/tmp/mx-rb-r9, detached at aa75078e1b, gateway tree **2d1a4f143cd995fe07262729b03f105ea7c1d761**; its artifact equals the live artifact **100 of 100 files (84 of 84 .py)** (rollback_vs_live_PHASEA.txt) |
| mcportal | a3bff71ffa3f5c73aa0fb7ea1e7386434e233054 (the live manifest's, unchanged). The artifacts built here carry the LIVE artifact's `dashboard/` directory, because the commit is the same; the real bun build happens at PHASE B (see "Not proved here"). |
| artifact keys at GO | s3://opal-313476888478-lambda-artifacts/ec2/opal-gateway/opal-gateway-7eeb4423f8.tar.gz (+ `-latest`), both written with `git-ref` = 7eeb4423f893deb104a78297b9eab2b4807868e6 by the deploy script |
| Terraform | none. `ENABLED_INTEGRATIONS` unchanged. `deploy-to-ec2.sh` untouched: byte-identical to the live ref's (`cmp` equal, release vs live ref and deploy-only vs live ref) |
| NEVER-2 ledger at GO | `nfra-mcpindex-r8-discover-release`: entry under `org/critical_paths/change_management/` AND sentinel `org/critical_paths/.open_deploys/nfra-mcpindex-r8-discover-release.json`, opened at PHASE B start (not now) |
| manifest edit | none by me; the deploy wrapper records its own. No other seat's release-branch manifest commit is merged or cherry-picked. |

The release and deploy-only commits were made with `git commit-tree` (plumbing, author = my serial, no hook, no `GIT_COMMIT_AUTHOR_OVERRIDE`), on scratch branches. Their trees are the object ids above.

## Step 1: the content, by CONTENT

The project's three gateway commits (box/sitez, landing order), applied onto the live ref with `git diff <c>^ <c> -- infra/aws/ec2/opal-gateway | git apply --3way --index`: **0 conflicts, every patch "applied cleanly".**

## Step 2: the CENSUS, per commit (inside the gateway dir; outside it is not shipped)

| commit | cell | file | + / - | in the artifact |
|---|---|---|---|---|
| 6584b623fa | MX-d-7 (~28) | app/integrations/opal_discover/integration.py | +172 -39 | yes |
| 6584b623fa | MX-d-7 | tests/test_opal_discover.py | +120 -5 | no |
| e7f52df685 | MX-c-6 (~29) | app/refs/DATA_CATALOG.yaml | +411 -2 | yes |
| 4b0ff635e9 | MX-d-8 (~28) | app/integrations/opal_discover/integration.py | +138 -3 | yes |
| 4b0ff635e9 | MX-d-8 | tests/routing/questions.yaml | +56 -0 | no |
| 4b0ff635e9 | MX-d-8 | tests/routing/run_routing.py | +4 -0 | no |
| 4b0ff635e9 | MX-d-8 | tests/test_opal_discover.py | +104 -0 | no |

Net against the live ref (`git diff --numstat aa75078e1b bf7988eab9`): **5 files, +1003 -47** (integration.py +308/-40, because MX-d-8 edits lines MX-d-7 added; DATA_CATALOG.yaml +411/-2; test_opal_discover.py +224/-5; questions.yaml +56; run_routing.py +4). **Blob equality:** the 5 shipped-content files are each byte-equal to box/sitez HEAD (blob compare, 5 of 5).
- MX-c-6's other 30 files are outside the gateway dir (`workflows/atom_decomposition/`: 29 `catalog_entries/need_E-*.yaml` inputs, the emitter `emit_catalog_v02.py` and its test): repo-level emitter inputs, not in the artifact, not shipped. 0 files outside the gateway dir for MX-d-7 and MX-d-8.
- **Foreign payload excluded by content:** 57 other non-merge commits touch the gateway path between the live ref and box/sitez HEAD (60 in all, 3 ours): NFRA_OPLGTW (the r29 cells, held), ETFS_RIVALS, NFRA_CTLPLN, NFRA_MCPORTAL, NFRA_OPALAI, 2.0.0_SA_COO~O, 4.0.0_SA_CRO. None is in the release (list: census_gateway_commits_since_live_PHASEA.txt).
- The deploy-only tree differs from CLOUD e43ee663be in 11 files, all in the gateway dir: our 5, plus 6 CLOUD-side held bytes that the live ref does not carry and this release does not ship (app/config.py, app/mail_route.py, deploy-to-ec2.sh, deploy/mail_sender_domain_table.txt, runbooks/SCHWAB_PILOT_RUNBOOK.md, tests/test_mail_route_domain.py). They are replaced by the live ref's bytes.

## THE SHIPPED-FILE LIST (the artifact: 100 files, 84 .py; the same count as the live artifact)

**Shipped files that change: 2** (preservation_live_vs_release_PHASEA.txt, preservation_live_vs_deployonly_PHASEA.txt):
1. `app/integrations/opal_discover/integration.py` (MX-d-7 + MX-d-8)
2. `app/refs/DATA_CATALOG.yaml` (MX-c-6)

The other 3 changed files (`tests/test_opal_discover.py`, `tests/routing/questions.yaml`, `tests/routing/run_routing.py`) are not in the artifact: its tar roots are `app deploy requirements.txt identity_tool_allowlist.txt` plus `dashboard`. No tests or routing files ship beyond what the deploy script ships today.

**THE PRESERVATION PROOF.** Every file in the LIVE artifact (100) against the release artifact (100) and against the deploy-only artifact (100), file by file, sha256:
- **0 absent, 0 only-in-new.**
- **98 of 100 identical (83 of 84 .py). 2 changed, each ours:** the two files above.
- OG-rl-14's content (transcript and mail tools, /hx routes, rosters host-side), MS-d-2's, MX-r-7's and MX-r-8's, and the Schwab host inputs are all among the 98 identical.
- Release artifact vs deploy-only artifact: **100 of 100 identical**.

## `ENABLED_INTEGRATIONS` and the live `.env` KEY set (keys only, never values)

| | ids |
|---|---|
| **before** (host, 2026-10-09T08:34:23Z and 09:42:12Z) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |
| **after** (the deploy-only script's rendered `.env`) | `ycharts opal_portal globgrph opal_discover portal_index schwab blackdiamond` (7) |

**EQUAL.** `opal_discover` is already enabled; this release changes no id. `deploy-to-ec2.sh` is byte-identical to the live ref's, so its `.env` printf is the live one (no hand merge needed).

`.env` KEY set, **before: 51 keys, 51 distinct** (host read twice, the key lists are equal across 08:34Z and 09:42Z):
AUDIT_S3_BUCKET AWS_REGION BIND_HOST BIND_PORT BLACKDIAMOND_READER_EXTERNAL_ID BLACKDIAMOND_READER_ROLE_ARN CLIENT_ID CLIENT_SECRET DASHBOARD_OWNER_EMAILS ENABLED_INTEGRATIONS FERNET_KEY FIRM_ROLE_ARNS GATEWAY_JWT_PRIVATE_KEY_FILE GATEWAY_WORKERS GRANT_WRITER_FUNCTION_NAME GRAPH_READ_BEARER IDENTITY_PROVIDER INTERNAL_READER_ROLE_ARN MAIL_BEARER MAIL_BEARER_LABELS MAIL_PDF_MAX_BYTES MAIL_SENDER_TABLE MASTER_ADMIN_EMAILS MASTER_ADMIN_PRINCIPALS MCPORTAL_CHANGES_TABLE MOCK_GRAPH MSP_CALLING_IDENTITIES MS_INGEST_BEARER MS_INGEST_BEARER_LABELS MS_INGEST_IDENTITY NFRA_OPLGTW_CONTRACT_PATH OTP_BEARER OTP_BEARER_LABELS OTP_MAILBOX PUBLIC_BASE_URL SCHWAB_ACCOUNT_REF_SECRET_ID SCHWAB_CATALOG_ROLE_ARN SCHWAB_EXTERNAL_IDS_SECRET_ID SCHWAB_READER_ROLE_ARN SPRINT_VIEW_ALLOWED_EMAILS TAXSMA_WORKBOOK_BEARER TAXSMA_WORKBOOK_IDENTITY TEAMS_BEARER TEAMS_BEARER_LABELS TENANT_ID TRANSCRIPT_BEARER TRANSCRIPT_BEARER_LABELS TRANSCRIPT_MEETING_ALLOWLIST WRITE_CAPABLE_EMAILS WRITE_CAPABLE_PRINCIPALS YEARINREVIEW_VIEW_ALLOWED_EMAILS

**After: 51 keys, 51 distinct** (the deploy-only script's `.env` printf, rendered with dummy inputs by `probes_r9/env_render.py`; env_keys_PHASEA.txt). **Dropped: none. Added: none. Keys before == after.** Control: the live ref's own script (the rollback tree) renders the same 51 (env_keys_control_liveref_PHASEA.txt); the two scripts are byte-identical.
- **Both principal keys stay:** `MASTER_ADMIN_PRINCIPALS` and `WRITE_CAPABLE_PRINCIPALS` are in the set. Both are non-empty on the host, as is `INTERNAL_READER_ROLE_ARN`. They are read host-side from Secrets Manager at deploy (OG-rl-1), so nothing is needed in the deploying shell. The rosters need no off-repo hand-off.
- `MAIL_SENDER_TABLE` is a host state, not a deploy input: the table ships in the artifact (`deploy/mail_sender_table.txt`), the live and deploy-only copies are the same file (3 items, 67 characters joined; the host `.env` line reads 69 because the value is quoted), and the script refuses on an empty table.
- No value is in any file here: the render uses dummy inputs and the host read prints names and state lines only.

## The tool count (in-process on the extracted artifacts, MOCK_GRAPH=1, the 7 live ids; tools_delta_PHASEA.txt)

| | native | integration | total |
|---|---|---|---|
| live aa75078e1b artifact | 42 | 24 | **66** |
| deploy-only artifact | 42 | 24 | **66** |

**0 added, 0 removed, delta 0; the sorted name lists are equal.** The ac08 pin (train C3) is LIVE + OWN = 66 + 0: this release registers no tool.

## THE SUITE: BEFORE and AFTER (the opal-gateway `tests/` directory, `python -m pytest tests -q`, same command, both trees; row Z-S88 stands)

| | collected | failed | passed | errors | file |
|---|---|---|---|---|---|
| **BEFORE: live ref aa75078e1b (rollback tree)** | 642 | **38** | **600** | 4 | tests_full_liveref_run2_PHASEA.txt |
| **AFTER: release bf7988eab9** | 648 | **38** | **606** | 4 | tests_full_release_run2_PHASEA.txt |

- The 38 failing ids are the same in both trees: **0 new failures, 0 fixed.** The 6 extra passes are the 6 new tests in `tests/test_opal_discover.py` (26 pass there against 20 at the live ref, 0 failures either side).
- This is Z-S88's red (schwab_*, asker_scope, portal_grant, data_entitlement_*, principal_cutover, local_acceptance), at the live ref, outside this project. The figures differ from Z-S88's 34 failed / 657 passed because the sparse trees collect 642 tests, not 691 (they hold no CLOUD-only tests): read them as a pair.
- Run 1 (same command, two trees sharing the machine) read two extra failures on the release only, `test_schwab_denial_envelope::test_ogz4_ac01` and `test_schwab_engine::test_ogq1_ac03`. They pass alone and behind `test_opal_discover.py` in both trees (isolation_ogz4_ogq1_PHASEA.txt) and did not recur in run 2: order or load dependent, not this release. Row NFRA_MCPINDEX-Z-W28-S8 (OBSERVATION, INERT).
- Routing harness on the release tree: **33 of 36 routed to the expected tool**; Q28-Q36 (Alyssa's six phrasings and the three write asks) 9 of 9; the misses are Q05, Q07, Q22, the same as MX-d-8's drain (routing_release_PHASEA.txt).

## A PREVIEW of r9.AC2 and r9.AC3 (NOT the acceptance read: my credentials, not the host; the deploy-only artifact extracted locally)

In-process on the extracted deploy-only artifact (`r9_inprocess_deployonly_artifact_PHASEA.txt`; the issuer's `r9_host.py` with the root moved and the env set to MOCK_GRAPH=1):
- FRESH: stated as-of equals the served object's own vintage_field, claim `measured`, **3 of 3** (model benchmarks 2026-10-07, aum-metrics 2026-10-07, aggregate-aua-timeseries 2026-10-07). The live host states 2026-08-10 `held` today (issuer's dry run).
- ROUTE: first match **9 of 9** as r9.AC3 expects (Q28 E-16, Q29 E-4, Q30 E-9, Q31 E-20, Q32 E-21, Q33 E-19, Q34 E-21, Q35 E-23, Q36 E-24); write asks with class and grant **3 of 3** (Q34, Q35, Q36: op_class write, grant False).
The acceptance reads are PHASE B's, on the host under its own role and `.env`.

## Not proved here (read-only limits)

- The dashboard bundle: the artifacts above carry the live artifact's `dashboard/`. The real build (`bun install --frozen-lockfile && bun run build`, with the bun-cache pre-check from OG-bi-1) runs at PHASE B on the applier's device; a cache miss refuses before any upload.
- The deploy-only worktree (C:/tmp/mx-dep-r9, sparse: infra/aws/ec2, .tools, org/mcp, org/critical_paths) has no nested `mcportal/` checkout: place a3bff71ffa there as MX-r-7's PHASE B did. A fresh applier lane may rebuild the tree from the pins above; the deploy-only commit is a closed object.
- The host's served effect of the catalog (29 needs) and discover's as-of reads under the host's `.env` and IAM: only PHASE B shows it.

## What PHASE B does (NOTHING below has been done; it waits on the issuer's amendment, the slot with 2.0.0_SA_COO~O and the applier)

1. Re-read the live ref (the clause above); if not aa75078e1b, STOP. Open the ledger `nfra-mcpindex-r8-discover-release` (NEVER-2; entry AND sentinel named in the commit; the entry names every task family that pulls the tag).
2. Halt gate in a worktree: if `safe-ec2-deploy.sh` resolves the issuer's serial, write the applier's serial into the worktree's gitignored `org/mcp/sessions/<session>.serial` (row Z-W21-S21).
3. Deploy from the deploy-only tree: `cd C:/tmp/mx-dep-r9 && DEPLOY_BASE_REF=aa75078e1b72a28219e6148d3ec8e9bf705ea111 HALT_ACK=1 AGENT_NAME=<applier serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`. No off-repo input is needed.
4. Read back: `/health` 200; r9.AC2 and r9.AC3 (the issuer's `round8/checks/`); host `.env` KEY names 51 before == 51 after, 0 dropped, both principal keys present; the id set equal; tool count 66 -> 66, names equal; host files equal to the deploy-only artifact's 100; both S3 objects carry `git-ref` = 7eeb4423f893deb104a78297b9eab2b4807868e6; r9.AC1 once the ledger is closed.
5. Rollback on any failed leg (never half-landed): `cd C:/tmp/mx-rb-r9 && DEPLOY_BASE_REF=<the then-live ref> HALT_ACK=1 AGENT_NAME=<serial> bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`. No Terraform to undo.

## Rows (channel INVESTIGATION_v1.md; fabric site-z; disarm_owner 2.0.0_SA_COO~MI)

| id | class / hazard | what |
|---|---|---|
| NFRA_MCPINDEX-Z-W28-S7 | OBSERVATION / **ARMED** | OG-rl-15 is cut on the same base; the second lander re-cuts; the pins are void on any other live ref. Disarm: the issuer agrees the slot with 2.0.0_SA_COO~O. |
| NFRA_MCPINDEX-Z-W28-S8 | OBSERVATION / INERT | the suite BEFORE/AFTER pair is 38/600 vs 38/606 on sparse trees (comparable as a pair); two schwab failures in run 1 were order or load dependent; the first sparse trees lacked org/standards and lib and were corrected. |
