# COMM_ASSIST.TO-CA-d-2 PHASE A -- READINGS

**Seat:** `0.7.0_AE_CloudOps~CA`, site Z, 2026-10-09. **Basis:** `box/sitez` @`9ba3e56d87`, which contains the go commit
`5697f9b764` and the halves' read-at `b1b8f5b4fe` (`merge-base --is-ancestor`, with a not-an-ancestor negative control).
**Authority:** `<status>pending</status>` at HEAD; UB-20261009T111212Z-f17d SIGNED by `3.0.0_SA_CVO~Z` @2026-10-09T11:36:29Z
(`org/critical_paths/unblock/20261009T1136Z_UB-20261009T111212Z-f17d.md:3,112`).
**PHASE B line at HEAD:** `PHASE B: NOT YET` -- nothing of steps 1-9 was run.
**PHASE A applied nothing, opened no ledger, read no secret value and called no route.**

## Step 4 -- BEFORE reads (all saved under `r12_phase_a/`)

1. `teams-global-chat-assist-handler-lambda` CodeSha256 `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=`, LastModified `2026-10-08T22:32:01.000+0000`, CodeSize 219476, runtime python3.12 -- EXPECTED (round 7's package).
2. `teams-global-chat-assist-ingress-lambda` CodeSha256 `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=`, LastModified `2026-10-08T22:31:55.000+0000`, CodeSize 219476, runtime python3.12 -- EXPECTED.
3. Neither function's `Environment.Variables` carries `MAIL_BEARER_SECRET` (12 keys each, both lists saved verbatim) -- EXPECTED.
4. Live zip via `get-function` -> `Code.Location`: 219476 bytes, sha256 `c56511a5efe746489901cf14ba2f9aaec26949e567504acd107056aadbeb3394`, base64 `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=` -- the downloaded bytes hash to the live `CodeSha256`, so the saved rollback artifact IS the running package. Saved UNTRACKED at `r12_phase_a/BEFORE_live_teams-chat-assist.zip` (a binary is not committed; PHASE B re-reads step 4 at the act, which is the rollback copy that binds).
5. `teams-global-chat-assist-policy` (`arn:aws:iam::313476888478:policy/teams-global-chat-assist-policy`) DefaultVersionId `v3`, UpdateDate `2026-10-08T08:15:28+00:00` -- EXPECTED (the COO half read v3).
6. `chat_assist.tf` at HEAD: `variable "chat_assist_mail_bearer_secret_arn"` `default = ""` (line 28), file clean in the worktree -- EXPECTED.

## Step 5 -- builds and the import test

7. `bash infra/aws/lambda/transcripts-pull/build.sh` rc=0 -- `dist/transcripts-pull.zip`, 88 files, 876616 bytes, sha256-b64 `cyPpVSMTVyUIOqJ5goGFIR4bBBkMTrkrgq2HgGHbcrY=`.
8. `bash infra/aws/lambda/teams-chat-assist/build.sh` rc=0 -- `dist/teams-chat-assist.zip`, 32 files, 261471 bytes, sha256-b64 `+VT4f32xhMWitwdP9GFaNNXNTqym6uPRv0aif7vpblI=`. This differs from the live `xWURpe/n...`, which is the expected `source_code_hash` delta the plan was to show.
9. Import test, the COO half's Branch B verbatim against `infra/aws/lambda/teams-chat-assist/dist/pkg`: `python -c "import sys; sys.path[:0]=['<pkg>']; import handlers, data.transcripts.scripts.teams_chat.tenant"` -> rc=0, no output. PASS, so the registry's 1,464 additive leaves resolve at import.

## The scratch preview plan -- BLOCKED, and this is the one reading that is not as expected

10. `TF_DATA_DIR` = `<scratchpad>/tfdata-ca-d-2-phasea`, created fresh; `git -C <dir> rev-parse --show-toplevel` -> `fatal: not a git repository`, i.e. outside every git tree -- EXPECTED.
11. `init -input=false` rc=0 against the declared s3 backend: "Successfully configured the backend", modules `ldo_001` + `ldo_001.name`, aws v5.100.0 from the lock file. NO migrate and NO reconfigure prompt -- EXPECTED, so no STOP on that limb.
12. `terraform -chdir=infra/aws/terraform/transcripts plan -input=false -no-color -lock=false -target=module.ldo_001`, variable at its committed `""` and no `-var` -> **rc=1, NO PLAN BODY**: `Error: No value for required variable ... on readers.tf line 15: variable "second_reader_trust_principal_arns"`. Saved as `PHASE_A_PLAN.txt`. **NOT the expected `0 to add, 2 to change, 0 to destroy`** -- the plan never evaluated, so neither the expected reading nor any other was produced.
13. DENOMINATOR for that finding: 6 of 6 root `.tf` files parsed, 6 root variables total, EXACTLY 1 without a default (`second_reader_trust_principal_arns`); 0 `.tfvars`/`.auto.tfvars` in the root and 0 tracked by git. So nothing in the tree supplies it.
14. POSITIVE CONTROL, same scratch dir and same init: `terraform validate` -> rc=0 "Success! The configuration is valid." The blocker is the missing variable VALUE alone -- not the scratch dir, the backend, the init or the config.
15. OWNER and INTENT: `readers.tf:12-13` says the absent default is deliberate ("a plan without it is refused by terraform"). Added by `0.9.0_WK_NFRA_TRNSPT~2` in `0693227a69` (TO-TR-p18) and `3c68dab9c9` (TO-TR-r21). `NFRA_TRNSPT.TO-APPLY-a18:34` supplies it as a `-var` at its own apply and commits no default.
16. THE COLLISION: CA-d-2 forbids `-var` on this shared root (RULES FOR THIS CELL; COO half lines 11-13: a `-var` silently unwires the mail key on the next apply). NFRA_TRNSPT requires a `-var` for the same root. **PHASE B's step 6 hits the same wall**, so this is not a PHASE A artifact.

## Verdict

**STOPPED at reading 12, per PHASE A's own instruction.** Steps 4 and 5 are complete and every reading in them is as
expected. `COMM_ASSIST-Z-S1` is filed BLOCKING/ARMED with `disarm_owner` `2.0.0_SA_COO~ZZ` (the order prescribes `COMM_ASSIST-Z-AE-S<k>`, which the row gate refuses -- grammar `<CODE>-(Z-)?(W<n>-|C-)?S<k>`; no override taken, and the order's line is the issuer's to correct). This seat applied nothing,
opened no ledger, read no secret, sent no mail, invoked nothing, and did not continue to step 1. `<status>` stays
`pending`; no criterion was run (both FAIL at the base by the issuer's own pre-cut read) and no proof instance is written.
