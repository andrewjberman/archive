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

---

## PHASE A RE-RUN (amendment A3 @`7b35ae056b`, ruling row `COMM_ASSIST-Z-S2` which disarms `Z-S1`)

A3 permits exactly ONE foreign `-var`, read live at the act. `PHASE_A_PLAN.txt` above stands as the pre-A3 reading.

17. A3 `-var` SOURCE, read at the act and never typed from the order: `aws iam get-role --role-name teams-global-transcripts-second-reader-role` -> trust policy saved at `r12_phase_a/A3_live_trust_read.json`. DENOMINATOR 1 statement of 1, 1 principal of 1; `Principal.AWS` is a STRING, normalised to a one-element JSON list. Derived argument: `second_reader_trust_principal_arns=["arn:aws:iam::313476888478:user/Opal_Terminal"]`. It equals the value the issuer quoted at 12:4xZ, but this seat read it rather than copying it. Role created 2026-10-09T09:55:13Z, so TO-APPLY-a18 has landed.
18. ARGV CORRUPTION ORACLE (the value carries an ARN with a `/` segment): native-python `repr(sys.argv[1])` echoed the argument back byte-identical to the file, both WITH and WITHOUT `MSYS_NO_PATHCONV=1`. `cmd //c echo` is NOT a usable oracle here -- it re-quotes and, with the guard set, swallowed the `//c` and opened a banner. The plan was run with the guard set, per the ARN-arg rule.
19. Fresh scratch `TF_DATA_DIR` (`tfdata-ca-d-2-phasea-a3`), confirmed outside every git tree; `init -input=false` rc=0, s3 backend configured, aws v5.100.0, NO migrate and NO reconfigure prompt.
20. `plan -input=false -no-color -lock=false -target=module.ldo_001 -var <the one above>` -> rc=0, a full plan body, saved as `PHASE_A_PLAN_2.txt` (219 lines). **`Plan: 1 to add, 3 to change, 0 to destroy`** -- NOT the expected `0 to add, 2 to change, 0 to destroy`. The A3 `-var` cleared the evaluation wall of `Z-S1`; what it exposed is a second, different wall.
21. THE FOUR ADDRESSES, exhaustively (plan line numbers): `aws_iam_role.silver_reader` **will be created** (:45); `aws_kms_key.transcripts` **updated in-place** (:86); `module.ldo_001.aws_lambda_function.handler` updated in-place (:175); `module.ldo_001.aws_lambda_function.ingress[0]` updated in-place (:192). PRECISE DECOMPOSITION: the 1 ADD is `silver_reader`; of the 3 CHANGES, ONE is outside the module (`aws_kms_key.transcripts`) and TWO are the module's own functions.
22. THE TWO IN-MODULE CHANGES ARE EXACTLY AS SPECIFIED: each function changes `source_code_hash` `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=` -> `+VT4f32xhMWitwdP9GFaNNXNTqym6uPRv0aif7vpblI=` (the step-5 build) and `last_modified` -> `(known after apply)`, with 27 unchanged attributes and 4 unchanged blocks hidden on each. No env, policy, role or other argument moves inside the module. At the committed default `""`, `MAIL_BEARER_SECRET` is correctly absent from the plan.
23. STOP CONDITION 1 -- AN ADD: `aws_iam_role.silver_reader` is NFRA_TRNSPT TR-r-21's silver-only reader (`readers.tf:92`), declared there "NOT APPLIED -- plan only". It is not COMM's resource and is not in any of the three signed halves.
24. STOP CONDITION 2 -- A DEPENDENCY A3 NAMES AS MUST-READ-NO-CHANGE: `aws_kms_key.transcripts`' `policy` reads `jsonencode({...}) -> (known after apply)`. The MINUS side carries 4 Sids -- `RootAdministersTheKeyAndCannotUseIt`, `NamedReadersUseTheKey` (Andrew_Berman + the second reader's role), `DellAgentUsersDecryptOnly`, `DellAgentUsersGenerateDataKey` (both dell1/dell2 agent users). There are ZERO `+` lines: the plan cannot show the replacement at all.
25. WHY IT IS UNPREDICTABLE, which is a different fact from why the key is in the plan: `main.tf:117` puts `Principal = { AWS = aws_iam_role.silver_reader.arn }` in the key policy, and that role does not exist yet, so the whole document is unknown until apply. (The key is DRAGGED IN because module.ldo_001 takes its id and ARN -- the issuer's A4 reading; the policy is UNKNOWABLE because of the `:117` reference.) An apply here would rewrite the transcripts key policy to a value no half could have signed, since no half can state an outcome the plan cannot print.
26. `aws_iam_role.second_reader` and its policy -- the other two dependencies A3 names -- read NO change: they appear nowhere in the plan's four addresses. That limb of A3 is satisfied.

## Verdict (A3 re-run)

**Branch A is correctly NOT met, and this seat STOPPED.** Applied nothing, opened no ledger, read no secret value, called no
route, sent no mail, invoked nothing; did not continue to step 1; `<status>` stays `pending`. No criterion was run and no proof
instance is written. No new surprise row: the issuer RULED this reading in amendment A4 @`57b66ed3cb` (order lines 156-161) and
carried the decoupling to round 13, so the finding is owned and dispositioned -- re-filing it as a row would duplicate an owned
finding. `PHASE B: NOT YET` at HEAD, now also waiting on NFRA_TRNSPT `TO-APPLY-s21` (pending, laptop `0.7.0_AE_CloudOps~TRL`);
OG-ap-3 is complete (`fab015fa54`).

---

## PHASE A2 -- cell `CA-d-3`, the KMS decoupling (A5 @`99b9155bda`; CTO fold UB-e9bc @`cfef5928ad`)

27. VALUE-PRESERVATION, measured BEFORE the edit: `kms describe-key --key-id alias/opal-data-transcripts` -> KeyId `44a2284f-1e14-4ea1-b6cb-f6121bfde35a`, State `Enabled`. That is the same key id `PHASE_A_PLAN_2.txt:88` printed for the key resource and the same key in both functions' live `LDO_KMS_KEY_ARN`. The alias and the resource name ONE key, so the edit moves the dependency edge and not the value.
28. `local.bucket` is `local.scope_row.bucket` (`main.tf:76`), and `aws_kms_alias.transcripts.name` is `"alias/${local.bucket}"` (`main.tf:145`) -- so the data source's STRING is the same alias Terraform already manages, written as the string and never as a reference to that alias resource.
29. EDIT, `chat_assist.tf` ONLY (commit `2c84d9521a`): added `data "aws_kms_key" "ldo_001_transcripts" { key_id = "alias/${local.bucket}" }` plus the why-comment, and repointed `kms_key_id` -> `data.aws_kms_key.ldo_001_transcripts.id` and `kms_key_arn` -> `.arn` (was the key resource's `.key_id` / `.arn`). No other file touched; nothing applied.
30. THE COMMENT'S WORDING IS CONSTRAINED BY THE CHECKER, which is worth recording because it reads as a trap: `d3_decouple.py:28` runs `re.findall(r"aws_kms_alias\.|aws_kms_key\.transcripts", head)` over the WHOLE file text of `git show HEAD:chat_assist.tf`, comments included. The order requires a comment saying why, so a comment naming either token would have failed the very check it exists to pass. The comment therefore says "the key resource declared in main.tf" and "the alias RESOURCE" without the literal tokens. Verified before committing: 0 forbidden tokens, and the check-1 data-source regex matches. The checker was read and not edited.
31. HEAD/TREE IDENTITY before the plan: `git diff --stat HEAD -- chat_assist.tf` empty, so the bytes the plan read are the bytes the checker reads at HEAD.
32. THE FALSIFIER, taken exactly as Phase A (committed default `""`, plus the one A3 foreign `-var` RE-READ live at this act: 1 statement of 1, 1 principal of 1 -> `["arn:aws:iam::313476888478:user/Opal_Terminal"]`), fresh scratch `TF_DATA_DIR` confirmed outside every git tree, clean `init` with no migrate or reconfigure prompt. Saved as `PLAN_D3.txt`.
33. **`Plan: 0 to add, 2 to change, 0 to destroy`** -- the expected reading. ADDRESS DENOMINATOR: 2 of 2, both the module's own (`module.ldo_001.aws_lambda_function.handler` :44, `...ingress[0]` :61). `aws_kms_key.transcripts` GONE from the plan, `silver_reader` GONE, `second_reader` absent, no `LDO_KMS_KEY_ARN` diff line. The two changes are `source_code_hash` `xWURpe/n...` -> `+VT4f32xh...` and `last_modified` -> `(known after apply)`, 27 unchanged attributes hidden on each.
34. `CAd2-AC3` -> **`RESULT: PASS`**, rc=0, all five checks True (`timeout 120 python .../d3_decouple.py`). It FAILed at the base, as the order states.

## Verdict (PHASE A2)

**The decoupling holds and the falsifier passes.** The reading that blocked Phase A -- a sibling's `silver_reader` create and an
unsignable `(known after apply)` key policy -- is GONE from a `-target=module.ldo_001` plan, which is what A5 set out to prove.
Applied nothing, opened no ledger, read no secret value, called no route, sent no mail, invoked nothing. No proof_of_spec
instance is written yet: `CAd2-AC1` and `CAd2-AC2` are PHASE B's and still FAIL at the base by design, so `<status>` stays
`pending` and is not flipped. `PHASE B: NOT YET` at HEAD. Under A5 the GO now needs OG-ap-3 (complete, `fab015fa54`) AND
either this cell merged with the halves RE-SIGNED for this edit, or NFRA_TRNSPT `TO-APPLY-s21` complete. The re-sign is the
issuer's and the signers'; this seat holds.
