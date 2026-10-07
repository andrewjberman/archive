# ANNOUNCE_OG-rl-12 -- the r26 release (re-cut by amendment A3): three cells, Phase A complete, nothing deployed

`0.9.0_WK_NFRA_OPLGTW~28`, 2026-10-07, Phase A of `OG-rl-12`. Read-only on the host: SSM runs one at a time, each in its own scratch directory (`/tmp/og_r26_<tag>_<pid>`), `SCRATCH_REMOVED=yes` and 0 leftovers on every run. Nothing was uploaded or deployed. No ledger or sentinel was opened; no manifest or `LINEAGE_R18.json` edit. No grant, state-store, `.env`, secret, Terraform or IAM write; no S3 object written; no `/login` for the concierge; no `/trigger`, no `confirm=True`. No email, tid, oid, account id, execution id or token is in any deliverable written this session. Local only; nothing pushed.

**Release sha (the sha the three halves sign): `feddb372443adbcf139febab35b69f109e49b664`**, branch `rel-nfra-oplgtw-r26`, worktree `/c/tmp/og-rel21`, ONE commit on live `240ac2fe5abde944f15358ab563cb4b2ab63f09f` (r25). It replaces `f1a6582ee1` (6 files), which A3 declared four files short. Rollback tree `/c/tmp/og-rb20`, detached at `240ac2fe5a`.
R13 (a): `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~28`, 10 files within the release set, `org/git-author-override-audit.log` lines 24112-24113 (2026-10-07T10:13:55Z and :58Z, the shared workspace's log, read only). The branch was moved from `f1a6582ee1` to `240ac2fe5a` with `FORCE_HEADMOVE=1 git reset --soft` (the order directs the re-cut); the guard printed that this override is NOT recorded: row `NFRA_OPLGTW-Z-W28-S16`.

## The release set: live..CLOUD at the hand-off, CLOUD-only runbook excluded = exactly the expected set, nothing else
Ten files, +467/-10, 0 paths outside `infra/aws/ec2/opal-gateway/`. `git diff --name-only feddb37244 e3beea0b5c -- infra/aws/ec2/opal-gateway` lists `runbooks/SCHWAB_PILOT_RUNBOOK.md` only (`r26_equality.out`); the same holds against CLOUD's tip now (`b3a369e53e`): the runbook only. No other gateway difference appeared.

| file | cell | ships to the host | md5 live -> release |
|---|---|---|---|
| `app/integrations/opal_portal/integration.py` | OG-al-2 (id shape) + OG-up-2 (dedupe) | yes | `239f74db` -> `483977be` |
| `identity_tool_allowlist.txt` (gateway root; installs through the deploy tarball, `deploy-to-ec2.sh:217`) | OG-al-2 (one row + comments) | yes | `19f4fef5` -> `fbe94252` |
| `app/rivalfunds_view.py` | RIV-rt-1 (`valid_fund`, `chart_key`, `rivalfunds_chart`) | yes | `65135e70` -> `b04d528a` |
| `app/server.py` | RIV-rt-1 (ONE Route line) | yes | `2cc22c05` -> `2dcb0a53` |
| `app/tests/test_rivalfunds_view.py` | RIV-rt-1 (+61 lines of tests; under `app/`, so it is on the host) | yes | `b7b7511c` -> `c1f6390f` |
| `tests/test_identity_scope_status_row.py` | OG-al-2 | source only | new |
| `tests/test_opal_portal_status_id_shape.py` | OG-al-2 + OG-up-2 (one fake given a hash) | source only | new |
| `tests/test_opal_portal_dedupe_content.py` | OG-up-2 | source only | new |
| `tests/test_opal_portal_send_split.py` | OG-up-2 (fakes given a hash) | source only | -- |
| `tests/test_principal_cutover.py` | RIV-rt-1 (the ROUTE_CLASS line) | source only | -- |

Hunk equality (`r26_hunk_equality.out`): changed-line multisets EQUAL on 10 of 10 against the cells (OG-al-2 = `82da719ba2` + `d1f9077190`; OG-up-2 = `a7bf684bcd`; the files touched by more than one of those are compared against the net diff `82da719ba2^..a7bf684bcd`; RIV-rt-1 = `git diff f7f2cb7c2e^1 f7f2cb7c2e`, which the COO half on the handler requires byte for byte); each release blob equals the `refs/heads/CLOUD` blob. The host md5 list is regenerated: 97 files, 5 differ from live (`r26_release_md5.txt`).

## Steps (A3: steps 1-7 and 7a re-run on the new sha)
| step | status | evidence |
|---|---|---|
| 1 live ref | DONE (re-read) | manifest `deployed_commit` = `240ac2fe5a`; host md5 97 of 97 identical, 0 host-only files under `app/` and `deploy/` (`r26_live_md5_host.out`, SSM `08b445e9`) |
| 2 release tree | DONE | above; hunk equality 10 of 10; name-only diff vs `e3beea0b5c` = the runbook |
| 3 tests | DONE | below |
| 4 rollback | DONE (re-read) | `/c/tmp/og-rb20` clean at `240ac2fe5a`; live S3 artifact `opal-gateway-240ac2fe5a.tar.gz` = 100 files = 97 gateway + 3 dashboard: 97 of 97 equal the rb20 git tree, 97 of 97 equal the host-verified list, 0 only-in-artifact (`r26_cmp_rollback.out`) |
| 5 BEFORE / REHEARSAL | DONE | next section |
| 6 verify script | DONE | `r26_verify.sh before\|after` (+ `.py`) gains the route arms and the route BEFORE values; `r26_postdeploy.sh` folds the four route arms into `RL12_FLOOR.json` (dry-run composed on stand-ins). `before` on live: MainPID 758081, 51 key names and digests, 66 tools, /health 200, md5 92 of 97 (the 5 shipped files differ), route arm PASS. Negative control, `after` on the undeployed host: VERIFY FAIL 8 of 11 (the three failing checks are the shipped md5, chart_404 and chart_400; the route is not registered there); day_page_unchanged and audit_page_unchanged PASS; floor rl4.AC1 and ht.AC2 PASS 4 of 4 each (`r26_before.out`, `r26_negative_control.out`) |
| 7 check exercise | DONE | below |
| 7a route inventory | DONE | `tests/test_principal_cutover.py` 11 passed; `tests/test_data_entitlement_guard.py` 12 passed; each in its own process on the release tree, rc 0 (`r26_step7a.out`) |
| 8 ANNOUNCE | this file | |

### Step 3, tests (`r26_tests_release.out`, `r26_tests_baseline_full.out`, `r26_tests_baseline_failing_files.out`)
Release tree: 77 files, **626 passed, 7 failed**, in 6 files. Live baseline tree (`/c/tmp/og-rb20`): 74 files, 613 passed, 7 failed in the same 6 files. The 7 failing ids are identical on both trees, **0 new**, and the six failing files were re-run on the live tree this session: all 7 fail there too (`test_local_acceptance::test_ogv2_a12`, `test_blackdiamond::test_mx_t13_catalog_gated`, `test_portal_grant::test_asker_portal_scope_admits_granted_channel`, `test_portal_grant::test_asker_portal_scope_refuses_other_channel`, `test_portal_index::test_portal_tools_catalog_refs_resolve`, `test_schwab_export_stream::test_ogx4_ac03`, `test_schwab_host_inputs::test_grant_writer_stages_the_contract_only_from_the_standard`). The +13 passed = `app/tests/test_rivalfunds_view.py` 14 -> 17 (+3) and the three new files (status_row 4, dedupe_content 4, status_id_shape 2 = +10). `test_opal_portal_send_split.py` 5 passed. Both trees clean afterwards.

## BEFORE and REHEARSAL (step 5)
BEFORE = the installed live code; REHEARSAL = a host scratch copy carrying the 5 staged release files (md5 printed on the host and equal to the release list), installed tree untouched. The BEFORE reads for the allowlist, status tool, login and real holder come from the earlier session's runs (`r26_before_*.out`): the installed code did not move (md5 97 of 97 re-read at step 1), so they were not repeated; the route BEFORE is new.

| | BEFORE (installed code) | REHEARSAL (staged release bytes) |
|---|---|---|
| the scoped concierge, `opal_data_refresh_status` | DENIED (any client) | ADMITTED, on any client (unqualified row) |
| a tool nothing names (`send_email`, two synthetic names) | denied | still denied (0 of 3 admitted) |
| the upload row | no client: denied; registered client: admitted | unchanged |
| consent scopes, scoped concierge | 9 | 9 (`consent_scopes()` equal; unscoped probe 17) |
| tools registered | 66 | 66 |
| overlay rows | 1 | 2 |
| status tool, refused id (one containing `/`) | not called: live code has no check | refused, names `execution_id`, 0 HTTP requests |
| status tool, accepted id (the known ~01:26Z execution, never printed) | not called | OK, SUCCEEDED, terminal True (login POST + status GET + manifest GET) |
| portal login | OK | OK |
| real holder, query and download | 2150 returned = 2150 distinct = 2150 held, 0 unheld | the same, both paths |
| route registered: `GET /rivalfunds/{day}/chart/{fund}` | no | yes |
| `chart_404`: `/rivalfunds/2000-01-01/chart/ABC` | 404 (no route; not the handler's body) | **404, body names `no chart for this fund and day`** |
| `chart_400`: `/rivalfunds/2026-10-06/chart/abc` | 404 (no route) | **400** |
| chart route with no viewer | 401 | 401 |
| `day_page_unchanged`: `/rivalfunds/2026-10-06` | 200, 1279784 bytes, sha16 `ac999d182c92e212` | **200, 1279784 bytes, same digest: unchanged** |
| `audit_page_unchanged`: `/rivalfunds/2026-10-06/audit` | 200, 1381244 bytes, sha16 `270f6f5479ecdc32` | **200, 1381244 bytes, same digest: unchanged** |

Evidence: `r26_before_{allow,status,login,real,route}.out`, `r26_after_stage_{allow,status,login,real,route}.out` (route REHEARSAL 6 of 6, SSM `d446b641`; allow SSM `8b390153`; status `114b1888`; login `6103d3fc`). The route program is `r26_route_host.py.txt` (in-process, GuardMiddleware stack, synthetic viewer signed with a local test key, real read-only S3 GETs, scratch audit sink, `grants_written 0`). The overlay-before count for Phase B is counted from the live allowlist blob by `r26_postdeploy.sh` (1) and equals the BEFORE host count.

### Step 7, the check exercise (`r26_step7.sh`, scratch clone `x26`, a plumbing commit never merged, standing in for the POST-drain-back state: the worker head predates the RIV-rt-1 merge, so the clone's gateway files are overlaid with the release's before the check reads them)
| script | expected-PASS form | negative controls | `<expect>` (the order's text at `c38d69aa3d`) re.search |
|---|---|---|---|
| `rl12.AC1.sh` | `deployed=feddb37244 descends from 240ac2fe5a=yes; host shipped files equal the release bytes: 5 of 5 / entry files at HEAD=1; sentinel at HEAD=no; ... 0 / floor: rl4.AC1 yes; ht.AC2 yes / RESULT: PASS exit=0` | (1) the clone against the REAL undeployed host: `0 of 5`, FAIL; (2) the real pre-act tree: `descends ...=no`, `0 of 0`, FAIL | pass MATCH; both controls NO MATCH |
| `rl12.AC2.sh` | `fields=yes ssm=Success digest=yes / RESULT: PASS exit=0` | (1) record absent; (2) the rehearsal's true record (`installed_code` false); (3) status tool not admitted; (4) an unnamed tool admitted: each `fields=no`, FAIL | pass MATCH; all four NO MATCH |
Evidence: `r26_rl12.*.out`, `r26_expect_match.out`. The stand-in record is for the exercise only; Phase B writes its own `RL12_ALLOW.json` from the installed-code run. The criteria text did not change in A3; the scripts were not edited and match their `<expect>`.

## BLAST RADIUS -- written for three halves, covering all three cells
The release moves served output three ways: **one allowlist row WIDENS (Andrew's word), one id check NARROWS, one route is ADDED**; and the send path's dedupe key changes. Every other identity, tool and route is unchanged. No bucket, prefix, IAM, `.env`, Terraform, ALB, grant or state-store change; the host role, hosts and secrets are the installed ones. Rollback for all three: redeploy live `240ac2fe5a` (below).

### Half 1 -- OG-al-2: the scoped concierge's allowlist row (WIDENS; Andrew's word, record `@4403ac63df`, quoted in the file's comment: "rec approved")
- **What moves.** The one scoped identity ("the scoped concierge") gains ONE tool, `opal_data_refresh_status`, read-only (the tool's own code: portal service-account login POST, status GET, served-manifest GET; egress is the integration's existing host list, `www.opalinvest.dev` for these). The row is NOT client-qualified, so the tool is admitted on any client. The tool is already registered (66 before and after) and already callable by other identities at the integration's tier floor.
- **Named property: which tools the scoped concierge may call.** Decided by ONE function, `identity_scope.check`, reading **N = 2 sources**: the code seed `_SEED` (unchanged) and the overlay file `identity_tool_allowlist.txt` (+1 row). The overlay file has **N = 1 writer**: the deploy tarball (`deploy-to-ec2.sh:217`; no runtime writer; hot-reloaded per check). Rows are 2 after, 1 before.
- **Branches, both.** (a) Scoped concierge calls the status tool: ADMITTED (rehearsal True). (b) Scoped concierge calls a tool nothing names: DENIED (0 of 3 admitted). Also unchanged: the upload row (no client: denied; registered client: admitted) and an unscoped identity.
- **Consent does not change.** Readers of the consent set: `identity_scope.consent_scopes` and `graph_scope_map.TOOL_GRAPH_SCOPES` (**N = 2**); the status tool has no entry, so it contributes nothing. The scoped concierge's `/login` URL asks 9 scopes before and after (`consent_scopes()` equal); no `/login` was run.
- **Rollback per key.** Redeploying `240ac2fe5a` restores the overlay file (md5 `19f4fef5`, 1 row); the status tool is denied to the scoped concierge again. Nothing else moves.
- **Trigger:** the scoped concierge not admitted for the status tool; an unnamed tool admitted; the consent count off 9.

### Half 2 -- the send path's two changes: the id check (NARROWS) and the content-keyed dedupe (OG-up-2; fires MORE sends)
**(a) The execution-id shape check (row Z-S65, A1).** *Property: which execution ids reach the status URL path.* Sites that format an id into `STATUS_PATH`: **N = 3 in 2 functions** (`_read_status_once` line 195; `opal_data_refresh_status` lines 417 and 421). Writers of the check: **N = 1**, `_check_execution_id` (regex `[A-Za-z0-9_:-]{1,200}`, fullmatch), called by both functions before any request. Branches: *refused* (a slash, empty, non-string): the tool raises an error naming `execution_id` with 0 HTTP requests; the send path's `_read_status_once` returns `UNKNOWN` with 0 requests and never raises after `/trigger`. *Accepted* (`exec-<12 hex>`, `sscn-<12 hex>`, a UUID): unchanged behaviour; the rehearsal read the known ~01:26Z execution as SUCCEEDED. Rollback: redeploy removes the check (the pre-r26 gap of row Z-S65 returns).
**(b) The re-send dedupe (OG-up-2, CTO R36).** *Property: whether a `confirm=True` send fires a new `/trigger`.* The record `_RECENT_SENDS` has **N = 1 writer** (line 377, after a trigger) and **1 reader** (lines 320-322, purge and lookup); it is in-process, a 30-minute window, cleared on a gateway restart. The signature is now (name, size, **content hash**) instead of (name, size); the hash comes from the drive-item response already in hand (`file.hashes` sha256, quickXor, sha1, else `cTag`): no new request. Branches: (i) both hashes readable and the signature equals a record under 30 minutes old: `already_triggered=true`, that execution id, no upload, no second trigger (unchanged for an identical file); (ii) same name and size, different content: **fires** (before: wrongly skipped; this is the corrected same-date re-send the cell exists for); (iii) a hash unreadable on either file: **no dedupe**, the send fires like a first send and is still recorded. Residual named: a retry after a dropped transport fires again when the hash is unreadable. Rollback: redeploy restores the (name, size) key.
**Limit (stated, not hidden): the dedupe rests on offline tests** (`tests/test_opal_portal_dedupe_content.py` 4 passed, `test_opal_portal_send_split.py` 5 passed, `test_opal_portal_status_id_shape.py` 2 passed). No real send is ever run by this project, so **its first live exercise is the first corrected same-date re-send.** `_graph_find_pkl`'s real `file.hashes` shape was not probed.

### Half 3 -- RIV-rt-1: ONE ADDITIVE route, `GET /rivalfunds/{day}/chart/{fund}` (text from `RELEASE_NEEDS_RIV-rt-1_CHART_ROUTE_20261007.md` sections 2 and 3, `@ec89bbe212`)
- **What moves.** Before: not registered (a request answers the router's 404). After: behind the same identity wall as the other `/rivalfunds` paths. 200 with the stored JSON bytes when `<page prefix>date=<day>/charts/<FUND>.json` exists; 404 `no chart for this fund and day` when it does not; 400 on a bad day or fund with no S3 read; 401 with no viewer; 502 over the size cap or on any other S3 error. The key is confined: `valid_day` on the day and `fullmatch [A-Z0-9]{1,8}` on the fund, both before the key is built; no path separator reaches the key.
- **Reads ONE object** under the prefix the host role already reads for `index.html` and `audit.html`. 0 writes other than the audit-log line. The 60-second in-process page cache applies, so a re-published chart is served stale for up to 60 s.
- **Named property: what `/rivalfunds/{day}/chart/{fund}` returns.** Writers on the gateway: **N = 1**, `rivalfunds_view.rivalfunds_chart` (new); the one route line in `server.py` registers it. The object it reads has one writer, the ETFS_RIVALS publisher, outside this release. *Expected branch:* 200 with the object's bytes. *Other branch:* 404 `no chart for this fund and day`. On release day this is the ONLY branch live data can reach: **0 of 115 keys under `s3://opal-data-etfs/rivalfunds/etfs/platinum/page/` carry `/charts/`** (re-read this session, read-only list). *Failure branch:* a 5xx on a missing object, a 200 with no object, or `/rivalfunds/{day}` or `/audit` changing. Roll back.
- **Neighbours.** `/rivalfunds/{day}` and `/rivalfunds/{day}/audit` answered identically (status, bytes, digest) on the installed code and on the staged bytes. The Route line sits after `/audit` and before `/rivalfunds/{day}`.
- **Route inventory (form step 7a).** `ROUTE_CLASS` declares the route `access-layer`; `test_principal_cutover.py` 11 passed and `test_data_entitlement_guard.py` 12 passed on the release tree.
- **Rollback per key.** Redeploy the rollback tree at `240ac2fe5a`; the route is gone. Nothing else moves.
- **Trigger (each of the four, any one off its value):** `chart_404` not 404 with the named body; `chart_400` not 400; `day_page_unchanged` or `audit_page_unchanged` changed.
- **Limit (stated): the 200 arm rests on `app/tests/test_rivalfunds_view.py` (17 passed),** because 0 chart objects exist under the page prefix; no object is written to S3 to exercise it. The route arms run in-process on the host, not through the ALB (row Z-W28-S6, unchanged). The COO half on the handler carries to this sha because its hunks equal `git diff f7f2cb7c2e^1 f7f2cb7c2e` for the 4 files (10 of 10 equal above).

### Every other route and property
Writers unchanged. The floor (`rl4.AC1`, `ht.AC2`) holds or the release rolls back: both PASS 4 of 4 on the installed host today (`r26_negative_control.out`).

## Rollback (all three cells, one act)
Redeploy live `240ac2fe5abde944f15358ab563cb4b2ab63f09f` from `/c/tmp/og-rb20` (clean, detached at the live sha; equal 97 of 97 to the live S3 artifact `opal-gateway-240ac2fe5a.tar.gz`, `r26_cmp_rollback.out`). Rollback triggers: the scoped concierge not admitted for the status tool; an unnamed tool admitted; the consent count moved off 9; a floor read off its bar; any of the four route arms off its value; the tool count off 66.

## For Phase B (not started; the GO is the issuer's, with CTO + COO + CVO halves signed on the release sha)
- Scripts ready: `r26_verify.sh before <state>` then `after <state> <sha>`; `r26_postdeploy.sh <sha> <state>` writes `RL12_ALLOW.json` and `RL12_FLOOR.json` (incl. `status_id_refused`, `status_id_accepted`, `chart_404`, `chart_400`, `day_page_unchanged`, `audit_page_unchanged`). Re-run step 9 (live still `240ac2fe5a`) before any act.
- Preconditions from the issuer's needs record (section 4), not decided here: r26 touches the send path, so by the r25 timing rule it deploys only after today's Bloomberg send (~11:00Z) is confirmed served; the four ETFS_RIVALS commits reach origin on Andrew's push word before Phase B; the CVO who signs is named by the CTO.
- The release commit's trailer reads `Claude Sonnet 5.5` (the model that ran this phase), as in r25.

## Rows filed this phase
`NFRA_OPLGTW-Z-W28-S14` (the runner's staging filter missed the gateway-root allowlist; fixed in the r26 copies), `S15` (the bare `CLOUD` ref divergence; not reproduced), `S16` (the `FORCE_HEADMOVE` reset is not recorded), `S17` (the host body prints the Schwab master id; the saved r26 outputs are redacted and the runner now redacts it; older files not touched). All OBSERVATION / INERT, `disarm_owner` `2.0.0_SA_COO~O`.
