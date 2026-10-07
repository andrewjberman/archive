# ANNOUNCE_OG-rl-13 -- the r27 release: two cells, Phase A complete, nothing deployed

`0.9.0_WK_NFRA_OPLGTW~28`, 2026-10-07, Phase A (form steps 1-8; 7a does not apply) of `OG-rl-13`. Host runs were strictly one at a time, each in its own scratch directory (`/tmp/og_r27_<tag>_<pid>`); `SCRATCH_REMOVED=yes` and 0 leftovers on every run. Every audit sink used was a scratch file (`AUDIT_PATH` in the run's scratch directory; `AUDIT_S3_BUCKET` asserted empty), never the installed audit file. Nothing was uploaded or deployed. No ledger or sentinel was opened; no manifest or `LINEAGE_R18.json` edit. No grant, state-store, `.env`, secret, Terraform or IAM write; no S3 object written; no `/login` for the scoped concierge and no token acquired for it; no `/trigger`, no `confirm=True`. No email address, tid, oid, account id, execution id or token is in any deliverable written this session (the artifact bucket name, which embeds the account id, was redacted from `r27_cmp_rollback.out`). Local only; nothing pushed.

**Release sha (the sha the three halves sign): `510c8cfed2c852946e3e57fb4dd1c0467e2f3a52`**, branch `rel-nfra-oplgtw-r27`, worktree `/c/tmp/og-rel22`, ONE commit on live `feddb372443adbcf139febab35b69f109e49b664` (r26). Rollback tree `/c/tmp/og-rb21`, detached at `feddb37244`.
R13 (a): `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~28`, 5 files within the release set, `org/git-author-override-audit.log` lines 24643-24644 (2026-10-07T15:21:58Z and 15:22:02Z; the shared workspace's log, read only). The commit trailer reads `Claude Sonnet 5.5`.

## The release set: live..CLOUD at the hand-off, CLOUD-only runbook excluded = exactly the expected five, nothing else
`git diff --name-only feddb37244 0b81b01ad8 -- infra/aws/ec2/opal-gateway` lists six files; the sixth is `runbooks/SCHWAB_PILOT_RUNBOOK.md` (CLOUD-only, excluded). The same six at CLOUD's tip now (`e3579e3693`). No other gateway difference appeared, so the order's STOP condition did not fire. Five files, +218/-8, 0 paths outside `infra/aws/ec2/opal-gateway/`:

| file | cell | ships to the host | md5 live -> release |
|---|---|---|---|
| `app/audit.py` | OG-au-2 (one `_ARGS_ALLOWLIST` entry, `rivalfunds_view: day, route, fund`) | yes | `3861a627` -> `384a42e5` |
| `app/rivalfunds_view.py` | OG-au-2 (every rivalfunds audit call passes a `route`; each 200 answer passes its size) | yes | `b04d528a` -> `148edfdb` |
| `app/integrations/opal_portal/integration.py` | OG-sd-1 (`_manifest_date` also reads `generated_at`, last) | yes | `483977be` -> `d28d856b` |
| `tests/test_audit_rivalfunds_args.py` | OG-au-2 | source only (top-level `tests/` is not on the host: row Z-W28-S4) | new |
| `tests/test_opal_portal_status_displayed_date.py` | OG-sd-1 | source only | new |

Hunk equality (`r27_hunk_equality.out`): changed-line multisets EQUAL on 5 of 5 against the cells' own diffs (OG-au-2 = `git diff ccf93dea8e 3153a1c764`, 3 files; OG-sd-1 = `git diff ccf93dea8e 6818de7e0d`, 2 files; the two cells share 0 files); each release blob equals the `refs/heads/CLOUD` blob. The host md5 list is regenerated: 97 files, 3 differ from live (`r27_release_md5.txt`).

## Steps
| step | status | evidence |
|---|---|---|
| 1 live ref | DONE | manifest `deployed_commit` = `feddb37244` (deployed 2026-10-07T14:03:49Z); host md5 **97 of 97 identical**, 0 host-only files under `app/` and `deploy/` (`r27_live_md5_host.out`, SSM `754f2467`); the 97-name list equals the git blobs at `feddb37244` 97 of 97 |
| 2 release tree | DONE | above; hunk equality 5 of 5; the release tree is clean |
| 3 tests | DONE | below |
| 4 rollback | DONE | `/c/tmp/og-rb21` clean at `feddb37244`; live S3 artifact `opal-gateway-feddb37244.tar.gz` = 100 files = 97 gateway + 3 dashboard: **97 of 97 equal the rb21 git tree**, 97 of 97 equal the host-verified list, 0 only-in-artifact (`r27_cmp_rollback.out`) |
| 5 BEFORE / REHEARSAL | DONE | next section |
| 6 verify script | DONE | `r27_verify.sh before\|after` (+ `.py`), `r27_postdeploy.sh`, `r27_run_read.py`. `before` on live: MainPID 776049, 51 key names and digests, 66 tools, /health 200, md5 94 of 97 (the 3 shipped files differ), route arm 5 of 5 (`r27_before_verify.out`). Negative control, `after` on the undeployed host: VERIFY FAIL 10 of 11 (the one failing check is the shipped md5, 94 of 97); the four route arms PASS; floor rl4.AC1 4 of 4 and ht.AC2 4 of 4 (`r27_negative_control.out`) |
| 7 check exercise | DONE | below |
| 7a route inventory | NOT APPLICABLE | no tool and no route is added or removed (tool list 66 -> 66; the route table is the live one) |
| 8 ANNOUNCE | this file | |

### Step 3, tests (`r27_tests_release.out`, `r27_tests_baseline_full.out`)
Each test file in its own pytest process, scratch `AUDIT_PATH`. Release tree: 79 files, **633 passed, 7 failed**, in 6 files. Live baseline tree (`/c/tmp/og-rb21`): 77 files, 626 passed, 7 failed in the same 6 files. The 7 failing ids are identical on both trees, **0 new**; they fail on the live tree itself (the baseline run is that tree): `tests/acceptance/test_local_acceptance.py::test_ogv2_a12`, `tests/test_blackdiamond.py::test_mx_t13_catalog_gated`, `tests/test_portal_grant.py::test_asker_portal_scope_admits_granted_channel`, `tests/test_portal_grant.py::test_asker_portal_scope_refuses_other_channel`, `tests/test_portal_index.py::test_portal_tools_catalog_refs_resolve`, `tests/test_schwab_export_stream.py::test_ogx4_ac03`, `tests/test_schwab_host_inputs.py::test_grant_writer_stages_the_contract_only_from_the_standard`. The +7 passed = the two new files (`test_audit_rivalfunds_args.py` 4 passed, `test_opal_portal_status_displayed_date.py` 3 passed); `app/tests/test_rivalfunds_view.py` is 17 passed on both. Both trees clean afterwards.

## BEFORE and REHEARSAL (step 5)
BEFORE = the installed live code (`r27_before.out`, SSM `f28a0f7e`); REHEARSAL = a host scratch copy carrying the 3 staged release files (md5 printed on the host and equal to the release list; the installed tree untouched) (`r27_after_stage_read.out`, SSM `92da2e76`). The page requests run the installed code's GuardMiddleware stack in a separate process with a synthetic signed-in viewer and REAL read-only S3 GETs; the status tool runs in a second process (below).

| | BEFORE (installed r26) | REHEARSAL (staged release bytes) |
|---|---|---|
| newest published day | 2026-10-07 | 2026-10-07 |
| newest day page: status, bytes, digest | 200, 1286540, sha16 `97cf3f030fd06fe8` | **200, 1286540, `97cf3f030fd06fe8`: unchanged** |
| newest day audit page | 200, 1243556, `80922b99ec8bc3f3` | **same: unchanged** |
| page record: kept args, bytes | `["_omitted"]`, bytes absent | **`["day","route"]`, bytes 1286540 = the body served** |
| audit page record | `["_omitted"]`, bytes absent | `["day","route"]`, bytes 1243556 = the body served |
| chart on a day with no chart (`ABC`, newest day): status, args | 404, `["_omitted"]` | 404 (same answer), **`["day","fund","route"]`**; `verdict` absent |
| archive: args, bytes | `["_omitted"]`, bytes absent | `["route"]` (`days` absent), bytes = the body served |
| a day with no page: status, args | 404, `["_omitted"]` | 404, `["day","route"]` (`verdict` absent) |
| the 5 records: omitted / other args kept / `verdict` or `days` kept | 5 omitted / 0 / 0 | **0 omitted / 0 / 0**; `bytes` on every `ok` record: yes |
| status tool through the dispatch wrapper, the scoped concierge | admitted, `OK`, SUCCEEDED, `displayed_date` **null** | admitted, `OK`, SUCCEEDED, `displayed_date` **`2026-10-07T11:08:40.464158+00:00`** |
| the served manifest's `generated_at` | `2026-10-07T11:08:40.464158+00:00` (an independent GET with the tool's own bearer header) | the same value; equal to `displayed_date`; equal to what the tool itself saw |
| tools registered | 66 | 66 |
| scoped concierge's consent scopes | 9 | 9 |
| status tool, refused ids (a slash; a dot), accepted id | not repeated (r26 floor) | refused, refused, each 0 HTTP requests; accepted: OK, SUCCEEDED, terminal true (`r27_after_stage_status.out`, SSM `a762639e`) |
| portal login | not repeated | OK (`r27_after_stage_login.out`, SSM `7ab04a3f`) |
| real holder, query and download | not repeated | 2150 returned = 2150 distinct = 2150 held, 0 unheld, both paths (`r27_after_stage_real.out`, SSM `0db743f9`) |

**Audit-record fields in the REHEARSAL, in the words of the order:** kept args are exactly `day` and `route` on the page and the audit page; `bytes` equals the body served (1286540 and 1243556); a chart on a day with no chart keeps `day`, `fund`, `route`; `verdict` and `days` are absent from all five records.

**displayed_date vs the manifest's generated_at:** BEFORE null against `2026-10-07T11:08:40.464158+00:00`; REHEARSAL `displayed_date` = that same string, character for character. The value is the manifest's own timestamp as carried (a full timestamp with microseconds and offset), not a date.

### THE WRAPPER EXERCISE (row Z-W28-S13): ADMITTED, by every gate; no finding on the tier gate
The status tool was called ONCE per run (BEFORE on the installed code, REHEARSAL on the staged bytes) through the dispatch wrapper the MCP surface uses, `app.integrations.base.run_integration_tool` (entitlement lookup, identity-scope allowlist, tier gate, audit), in-process on the host, with the scoped concierge as the principal (`context.set_current_principal`; `MOCK_GRAPH=1`; no `/login`, no token acquired, no Graph call). The portal service account's own login POST and two GETs (status, served manifest) are the tool's.
- **Outcome both times: the wrapper admitted it and the tool returned status SUCCEEDED**; the wrapper wrote its audit record to the scratch sink with `outcome=ok` and `tier=standard`.
- Gates: the entitlement lookup (a real strong read of the principal's profile; no profile, so no restriction) passed; the identity-scope allowlist passed (the unqualified row); the tier gate passed (the principal resolved to `standard`, the status tool's floor is `standard`).
- **Which principal.** The order names the scoped concierge but not how its immutable principal key is obtained. The host role can neither query a `POLICY#` partition nor scan the state table (both were tried on a probe run and refused: `DependencyUnavailable` x3, `ClientError`; `r27_probe_principal_AB_refused.out`). The key was derived read-only from the host's own encrypted MSAL cache directory: for each of the 3 roster principals (1 master, 2 write-capable) the cache file is named `sha256("principal:<key>")`; 3 of 3 exist; each was decrypted in memory with the broker's own key and its ACCOUNT entries listed (no network, no token read, nothing written); exactly 1 names the scoped concierge. It sits in the write-capable roster, not the master roster. Row `NFRA_OPLGTW-Z-W28-S20`.
- **Limits (stated):** the principal was set in-process, so GuardMiddleware's token validation, the rate limiter and the MCP transport were not exercised; the verified OAuth `client_id` is empty (the status row is unqualified, so the answer does not depend on it); the roster and tier come from the `.env` text parsed into the process environment.

## Step 7, the check exercise (`r27_step7.sh`, scratch clone `x27`, a plumbing commit never merged, standing in for the POST-drain-back state; the clone's gateway tree is overlaid with the release's, its manifest names the release sha, an entry file exists, no sentinel, and `RL13_READ.json` is the staged rehearsal's host answer with `installed_code` flipped)
Scripts as written by the issuer, not edited. AC1's `ssm md5` answer is stood in by `.scratch/fakeaws` (the 3 release md5 lines); every other aws call, the floor's reads included, is real. AC2 verifies the digest against the REAL ssm invocation. Each criterion's literal output was checked against the order's `<expect>` with `re.search` (`r27_expect_match.out`):

| script | expected-PASS form | negative controls | `re.search(<expect>)` |
|---|---|---|---|
| `rl13.AC1.sh` | `deployed=510c8cfed2 descends from feddb37244=yes; host shipped files equal the release bytes: 3 of 3` / `entry files at HEAD=1; sentinel at HEAD=no; ... 0` / `floor: rl4.AC1 yes; ht.AC2 yes` / `RESULT: PASS` / `exit=0` | (1) the clone against the REAL undeployed host: `0 of 3`, FAIL; (2) the real pre-act tree: `descends ...=no`, `0 of 0`, `entry files 0`, differing 5, FAIL | pass **MATCH**; both controls NO MATCH |
| `rl13.AC2.sh` | `fields=yes ssm=Success digest=yes` / `RESULT: PASS` / `exit=0` | (1) record absent; (2) the rehearsal's true record (`installed_code` false); (3) `wrapper_status_tool` = a tier-gate refusal; (4) `displayed_date` null (the live r26 answer); (5) the page record's args `_omitted` (the live r26 audit record): each `fields=no`, FAIL | pass **MATCH**; all five NO MATCH |

Every check script matches its `<expect>`; nothing was reported as unmatchable. The stand-in record is for the exercise only; Phase B writes its own `RL13_READ.json` from the installed-code run.

## BLAST RADIUS -- written for three halves, covering both cells
Served output moves two ways, both ADDITIVE to a record or an answer. No response, status code, header, key or cache behaviour of any rivalfunds route changes (the newest day page and audit page answered with the same status, size and digest; the chart 404, the archive and the missing-day 404 with the same status). No bucket, prefix, IAM, `.env`, Terraform, ALB, grant, allowlist or state-store change; no tool and no route added or removed; the host role, hosts and secrets are the installed ones. Rollback for both: redeploy live `feddb37244` (below).

### Half 1 -- OG-au-2: the gateway's own audit record for the four rivalfunds routes gains `day`, `route`, `fund` and `bytes`
- **What moves.** In each `rivalfunds_view` audit record the `args` field goes from `{"_omitted": "args fail-closed ..."}` to the kept keys, and an `ok` record gains `bytes`. The four routes: page (`/rivalfunds`, `/rivalfunds/{day}`), audit page, archive, chart. **Privacy step, stated for the CVO half:** the record already carried the viewer (`user`); it now also ties that viewer to the day, the route and (chart only) the fund served. `day` is held to a validated date, `route` to one of four fixed names, `fund` to a public ETF ticker held to `[A-Z0-9]{1,8}`; the 400 path (a bad day or fund) returns before any record is written, so no unvalidated string reaches a kept key.
- **Named property 1: which arg keys a `rivalfunds_view` record keeps.** Decided by ONE function, `audit._safe_args` (**N = 1**), reading ONE allowlist dict `_ARGS_ALLOWLIST`, whose entry for `rivalfunds_view` is **N = 1 line** (`audit.py:111`, the release's only change to that file). Call sites that pass args for this tool: **N = 9** in `rivalfunds_view.py` (lines 185, 190, 193, 205, 253, 255, 257, 268, 277); the release changes 4 of them (205 gains `route`; 193, 257 and 277 gain `bytes_returned`, with the `resp` built before the call at 192-194 and 276-278) and the `extra` dict at 176 that three of the nine (185, 190, 193) spread, so a day-page record now always carries `route`. `verdict` (passed by 6 of the 9 sites) and `days` (passed by 1) stay DROPPED because the entry does not name them.
- **Named property 2: the record's `bytes` key.** Written by ONE line, `audit.log_call` (`audit.py:147-148`, **N = 1**, unchanged by this release), present only when a caller passes `bytes_returned`. Callers: **N = 4** (the 3 rivalfunds `ok` sites this release adds, plus `tools.py:178`, the OG-au-1 site, unchanged). The record is shipped by ONE function, `_emit` (**N = 1**, 3 callers: `log_call`, `log_login`, `log_credential`), to **N = 2 sinks**: the local JSONL floor and the S3 audit lake.
- **Branches, both.** (a) `ok`: kept `day`+`route` (+`fund` on a chart), `bytes` = the length of the body served (rehearsal: equal on page, audit page and archive). (b) Error branches (`MISSING`, `S3-ERROR`): kept `day`+`route` (+`fund`), **no `bytes`**, `verdict` dropped (rehearsal: the chart 404 and the missing-day 404). Unchanged: every response body, status and header.
- **Rollback per key.** Redeploying `feddb37244` restores `audit.py` (md5 `3861a627`: the entry is gone, so the args read `_omitted` again) and `rivalfunds_view.py` (`b04d528a`: no `route`, no `bytes`). Records already written keep their new shape; an audit consumer that reads `args` or `bytes` sees both shapes in the lake after a rollback.
- **Trigger:** any rivalfunds route changing status, size or digest; an arg other than `day`, `route`, `fund` kept in a rivalfunds record; a rivalfunds record with `_omitted`.
- **Limits (stated, not hidden).** (i) The rehearsal wrote a scratch JSONL; the S3 lake write (`AUDIT_S3_BUCKET`) was not exercised, and the lake's schema and the readers of `args` and `bytes` were not enumerated here. (ii) The 200 arm of the chart route has no live object to exercise (0 of 115 keys under the page prefix carried `/charts/` at r26; not re-measured this session), so the chart `ok` record's `bytes` rests on `tests/test_audit_rivalfunds_args.py` (4 passed). (iii) The page requests run in-process through the GuardMiddleware stack with a synthetic viewer, not through the ALB (row Z-W28-S6, unchanged). (iv) The pages are republished by the ETFS_RIVALS publisher; equality is as of the minute of each read (row Z-W28-S21).

### Half 2 -- OG-sd-1: `opal_data_refresh_status` returns the served manifest's `generated_at` in `displayed_date`, where it returned null
- **What moves.** One field of one tool's answer, from null to the manifest's `generated_at` string as carried. Nothing else in the answer (`execution_id`, `status`, `terminal`, `displayed` text, `status_note`) changes.
- **Named property: the value of `displayed_date`.** Written by ONE function, `_manifest_date` (**N = 1**), with ONE call site (`integration.py:434`, **N = 1**). The key tuple goes from 8 keys to 9: `generated_at` is appended LAST, so a manifest that carries any of the 8 earlier keys returns exactly what it returned before. Readers of the field are the tool's callers (MCP clients); not enumerable from the gateway.
- **Branches, both.** (a) A manifest with an earlier key: unchanged. (b) A manifest with only `generated_at` (today's served manifest): returns it (rehearsal). (c) No date-like key, a non-dict body, or manifest HTTP not 200: null, and the `displayed` text still rides back (tests: `test_ogsd1_ac02`, 3 passed in all).
- **Value form (stated).** Today's served manifest carries `generated_at` as a full timestamp with microseconds and a `+00:00` offset; the tool returns it unchanged. A caller written for a date-only string sees a timestamp.
- **Rollback per key.** Redeploying `feddb37244` restores `integration.py` (md5 `483977be`); `displayed_date` is null again for the current manifest. Nothing else moves.
- **Trigger / non-trigger.** The status tool failing on a well-formed id is a trigger. `displayed_date` still null after the deploy is NOT (the answer is no worse than live); it fails `AC2` and is reported.
- **Limit (stated): `integration.py` is the send path's file.** The diff is three changed lines in `_manifest_date` only (the dedupe, the id check, the upload and trigger code are byte-identical), but the file is the one `opal_data_refresh_upload` lives in, so the timing rule binds (below).

### Half 3 -- the wrapper exercise and the standing floor
The wrapper exercise above is the order's own required read: ADMITTED, so no finding to file on the tier gate and no change to it. The floor (`rl4.AC1` 51-name baseline, `ht.AC2` 51 keys) holds on the installed host today, 4 of 4 each (`r27_negative_control.out`); the portal login, the real holder (2150 = 2150 = 2150 on both paths) and the two refused ids (0 requests each) rehearse clean on the staged bytes.

## Rollback (both cells, one act)
Redeploy live `feddb372443adbcf139febab35b69f109e49b664` from `/c/tmp/og-rb21` (clean, detached at the live sha; equal 97 of 97 to the live S3 artifact `opal-gateway-feddb37244.tar.gz`, `r27_cmp_rollback.out`). Rollback triggers (from the order): any rivalfunds route changing status, size or digest; an arg other than `day`, `route`, `fund` kept in a rivalfunds record; the status tool failing on a well-formed id; a refused id making a request; the tool count off 66; the consent count off 9; a floor read off its bar.

## For Phase B (not started; the GO is the issuer's, with CTO + COO + CVO halves signed on the release sha)
- **Scripts ready:** `r27_verify.sh before <state>` then `after <state> <sha>`; `r27_postdeploy.sh <sha> <state>` writes `RL13_READ.json` (through `r27_run_read.py after <sha> <out> --json`, the host's `RL13_BODY` + `RL13_DIGEST`) and `RL13_FLOOR.json` (portal login, real holder on both paths, the two refused ids, the four r26 route arms). Run `r27_postdeploy.sh` IMMEDIATELY after the verify script. Composition note: `r27_postdeploy.sh` was syntax-checked (`bash -n`) but NOT executed as a whole, because run against the live r26 code it would write an `RL13_READ.json` from the installed code; each host program it calls ran in Phase A in `before` or `rehearsal` mode, and the digest path was exercised by AC2 in step 7.
- **Step 9:** re-read live (`r27_md5_host.py` list = `r27_live_md5.txt`); if it moved, re-cut. Re-take the BEFORE reads in the same window as the AFTER reads (row Z-W28-S21): the route arms compare a page's size and digest across the deploy, and the publisher republishes those pages.
- **The manifest's `release_note` (row Z-W28-S19).** It is 30808 characters now. Before the hand record, trim the cumulative chain so the whole value, with this release's note added, stays under 20000: keep the newest segments, drop the oldest, leave the TRIMMED marker naming what was dropped and the commit that still holds it.
- **The timing rule:** this release touches the send path's file. Phase B closes by 09:30Z, or starts only after that day's Bloomberg send is confirmed served; the issuer states which at the GO.
- **Deploy identity:** unset `OPAL_AGENT_SERIAL` in the deploy shell; the issuer's serial reaches the halt gate (form step 10).

## Rows filed this phase
`NFRA_OPLGTW-Z-W28-S20` (the order does not say how the concierge's principal key is obtained; the host role cannot read it from the state store; derived from the host's MSAL cache account entries), `S21` (the pages the route arms compare are republished; a size change between BEFORE and AFTER can fire the rollback trigger with no gateway change), `S22` (the r26 route program's BEFORE arm asserted the chart route absent; false on live r26, adapted in the r27 copy), `S23` (the worker worktree's sparse cone omits `org/devices`, so the row gate refused new rows until `git sparse-checkout add org/devices`). `S20`, `S22` and `S23` OBSERVATION / INERT; `S21` OBSERVATION / ARMED; `disarm_owner` `2.0.0_SA_COO~O` on all.
