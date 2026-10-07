# PARTIAL -- ANNOUNCE_OG-rl-12 -- Phase A stopped by the issuer's WIND DOWN (site Z reboot); steps 1-7 measured, step 7 exercised, step 8 (this ANNOUNCE) is a PARTIAL

`0.9.0_WK_NFRA_OPLGTW~28`, 2026-10-07. Nothing was uploaded or deployed. No ledger was opened, no sentinel, no manifest or `LINEAGE_R18.json` edit. No grant, state store, `.env`, secret, Terraform or IAM write. The host was touched only by read-only SSM runs, one at a time, each in its own scratch directory (`/tmp/og_r26_<tag>_<pid>`, `SCRATCH_REMOVED=yes`, 0 leftovers on every run). No email, tid, oid, account id, execution id or token is in any deliverable. No SSM run was in flight at the stop. Local only; nothing pushed.

**Release sha (the sha the halves sign): `f1a6582ee1dbb5ed7fa95274f9441f80e4fdd7cf`**, branch `rel-nfra-oplgtw-r26`, worktree `/c/tmp/og-rel21`, ONE commit on live `240ac2fe5abde944f15358ab563cb4b2ab63f09f`. Rollback tree `/c/tmp/og-rb20`, detached at `240ac2fe5a`. R13 (a): `GIT_COMMIT_AUTHOR_OVERRIDE=0.9.0_WK_NFRA_OPLGTW~28`, 6 files, `org/git-author-override-audit.log` lines 23864-23865 (2026-10-07T05:45:54Z / :59Z, shared main workspace, read only).

## Release set (live..CLOUD at hand-off, CLOUD-only runbook excluded) = the expected set, nothing else
Six files, +363/-9, 0 paths outside the gateway tree. Ship to host (2): `app/integrations/opal_portal/integration.py` (md5 `239f74db` -> `483977be`; OG-al-2 id check + OG-up-2 content signature), `identity_tool_allowlist.txt` (gateway root; installs to `/opt/opal-gateway/identity_tool_allowlist.txt` through the deploy tarball, line 217 of deploy-to-ec2.sh; md5 `19f4fef5` -> `fbe94252`; the host md5 list carries it at that path, so rl12.AC1 is sound, no check defect). Source-only (4): `tests/test_identity_scope_status_row.py`, `tests/test_opal_portal_dedupe_content.py`, `tests/test_opal_portal_send_split.py`, `tests/test_opal_portal_status_id_shape.py`.
Hunk equality (`r26_hunk_equality.out`): changed-line multisets EQUAL on 6 of 6 against the cells (OG-al-2 = `82da719ba2` + `d1f9077190`, OG-up-2 = `a7bf684bcd`; the two files touched by all three commits are compared against the net diff `82da719ba2^..a7bf684bcd`, and the script asserts those three are the only commits touching them); each release blob equals the `refs/heads/CLOUD` blob. `git diff --stat f1a6582ee1 refs/heads/CLOUD -- infra/aws/ec2/opal-gateway` = ONE line, `runbooks/SCHWAB_PILOT_RUNBOOK.md | 2 ++` (`r26_equality.out`). NOTE: bare `CLOUD` resolved in this repo to a different commit than `refs/heads/CLOUD` during one read (ref ambiguity, not filed as a row); every measurement here names `refs/heads/CLOUD`.

## Steps
| step | status | evidence |
|---|---|---|
| 1 live ref | DONE | manifest `deployed_commit` = `240ac2fe5a`; host md5 97 of 97 identical, 0 host-only files (`r26_live_md5_host.out`); the list equals the git blobs at `240ac2fe5a` 97 of 97 (`r26_live_blob_check.out`) |
| 2 release tree | DONE | above |
| 3 tests | DONE | each file in its own process. Release: 77 files, 623 passed, 7 failed in 6 files. Rollback: 74 files, 613 passed, 7 failed in the same 6 files. The 7 ids are identical on both trees, 0 new: `test_local_acceptance::test_ogv2_a12`, `test_blackdiamond::test_mx_t13_catalog_gated`, `test_portal_grant::test_asker_portal_scope_admits_granted_channel`, `...::test_asker_portal_scope_refuses_other_channel`, `test_portal_index::test_portal_tools_catalog_refs_resolve`, `test_schwab_export_stream::test_ogx4_ac03`, `test_schwab_host_inputs::test_grant_writer_stages_the_contract_only_from_the_standard`. New/changed files: status_row 4 passed, dedupe_content 4, send_split 5, status_id_shape 2, entitlement_admin 9, scoped_consent_r253 7. Both trees clean afterwards (`r26_tests_release.out`, `r26_tests_baseline_full.out`) |
| 4 rollback | DONE | `/c/tmp/og-rb20` clean at `240ac2fe5a`; live S3 artifact `opal-gateway-240ac2fe5a.tar.gz` = 100 files = 97 gateway + 3 dashboard: 97 of 97 equal the rb20 git tree and the host-verified list, 0 only-in-artifact (`r26_cmp_rollback.out`) |
| 5 BEFORE / REHEARSAL | DONE | next section |
| 6 verify script | DONE | `r26_verify.sh before|after` (+ `.py`), `r26_postdeploy.sh`. `before` on live: MainPID 758081, 51 key names and digests, 66 tools, /health 200, md5 95 of 97 (only the 2 shipped files differ). Negative control, `after` on the undeployed host: VERIFY FAIL 4 of 5 (md5 only); floor rl4.AC1 and ht.AC2 PASS 4 of 4 each (`r26_before.out`, `r26_negative_control.out`) |
| 7 check exercise | DONE | below |
| 7a | NOT APPLICABLE | no tool or route added or removed |
| 8 ANNOUNCE | PARTIAL | this file: blast-radius text for the three halves is NOT written yet |

## BEFORE and REHEARSAL
| | BEFORE (installed live code) | REHEARSAL (staged release bytes, installed tree untouched) |
|---|---|---|
| the scoped concierge, `opal_data_refresh_status` | DENIED (any client) | ADMITTED, also on any other client (unqualified row) |
| a tool nothing names (`send_email`, two synthetic names) | denied | still denied (0 of 3 admitted) |
| the upload row | no client: denied; registered client: admitted | unchanged |
| an unscoped identity | untouched | untouched |
| consent scopes, scoped concierge (the /login URL; `consent_scopes()` beside it, equal) | 9 | 9 (unscoped probe 17) |
| tools registered | 66 | 66 |
| overlay rows (loader rule: a line with 2+ tokens before `#`) | 1 | 2 |
| status tool, refused id (`r26/refused-id`, a slash) | not called: live code has no check (`id_shape_check_present=False`) | refused, names `execution_id`, 0 HTTP requests |
| status tool, accepted id (the ~01:26Z execution, never printed) | not called | OK, SUCCEEDED, terminal True (login POST + status GET + manifest GET) |
| portal login | OK | OK |
| real holder, query (22 pages) and download | 2150 returned = 2150 distinct = 2150 held, 0 unheld | the same, both paths |
Evidence: `r26_before_allow.out`, `r26_before_status.out`, `r26_before_login.out`, `r26_before_real.out`, `r26_after_stage_{allow,status,login,real}.out`. The overlay-before count for Phase B is counted from the live allowlist blob by `r26_postdeploy.sh` (1) and must equal the BEFORE host count (1, matches).

## Step 7 -- the check exercise (`r26_step7.sh`, scratch clone x26; stand-in record = the staged rehearsal body with `installed_code` flipped; AC1's host md5 answer stood in by a fake `aws`, floor reads the REAL host)
| script | expected-PASS form | negative controls | `<expect>` re.search |
|---|---|---|---|
| `rl12.AC1.sh` | `deployed=f1a6582ee1 descends from 240ac2fe5a=yes; host shipped files equal the release bytes: 2 of 2 / entry files at HEAD=1; sentinel at HEAD=no; ... 0 / floor: rl4.AC1 yes; ht.AC2 yes / RESULT: PASS exit=0` | (1) clone vs the REAL undeployed host: `0 of 2`, FAIL; (2) the real pre-act tree: `descends ...=no`, `0 of 0`, 6 files differing, FAIL | pass MATCH; both controls NO MATCH |
| `rl12.AC2.sh` | `fields=yes ssm=Success digest=yes / RESULT: PASS exit=0` | (1) record absent; (2) the rehearsal's true record (`installed_code` false); (3) status tool not admitted; (4) an unnamed tool admitted: each `fields=no`, FAIL | pass MATCH; all four NO MATCH |
Evidence: `r26_rl12.*.out`, `r26_expect_match.out`. The stand-in is for the exercise only; Phase B writes its own `RL12_ALLOW.json` from the installed-code run.

## NOT DONE (for the successor)
- The remainder of step 8: the blast-radius text for CTO, COO and CVO (what widens: one read-only tool for one identity by Andrew's word, consent unchanged at 9; what narrows: the execution-id shape check; what changes in the dedupe: signature (name, size, content hash), unreadable hash fires, text says content). Writers of each property counted, both branches, rollback per key (redeploy `240ac2fe5a`, artifact `opal-gateway-240ac2fe5a.tar.gz`, `/c/tmp/og-rb20`).
- The ANNOUNCE must say the content-keyed dedupe cannot be exercised live without a real send and rests on `test_opal_portal_dedupe_content.py` (4 passed); the first corrected same-date re-send is its first live exercise. `_graph_find_pkl`'s real `file.hashes` shape was not probed.
- No surprise row was filed (time). Candidates, each OBSERVATION / INERT, `disarm_owner` `2.0.0_SA_COO~O`: (a) the r25 runner staged only `app/` and `deploy/` files, so a rehearsal would not have carried `identity_tool_allowlist.txt`; fixed in `r26_ssm_prog.py` and `r26_ssm.py` (filter now includes the gateway-root allowlist); (b) unqualified `CLOUD` is an ambiguous ref in this repo (use `refs/heads/CLOUD`).
- The trailer on the release commit reads `Claude Sonnet 5.5` (the model that ran this phase), not the `Claude Opus 5.5` the hand-off named, as in r25.
- Phase B scripts are ready: `r26_verify.sh before|after`, `r26_postdeploy.sh <sha> <state>` (writes `RL12_ALLOW.json` and `RL12_FLOOR.json` incl. `status_id_refused` / `status_id_accepted`; its composing block was dry-run on staged stand-ins). Re-run step 9 (live still `240ac2fe5a`) before any act.
