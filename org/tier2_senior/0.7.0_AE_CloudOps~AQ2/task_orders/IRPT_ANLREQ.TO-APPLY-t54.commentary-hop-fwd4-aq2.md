<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-t54.commentary-hop-fwd4-aq2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>55</round>
<workstream>~T</workstream>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R55_T.md</decomp_doc>
<owned_cells>AR-tf-76</owned_cells>
<decomp_context>Round 55, cell AR-tf-76: the release of the commentary hop's part of FWD-4 (C-HOP-FAILURE): a narrow IAM grant, the draft-store Lambda's new zip, the commentary function's surgical zip, then a driven proof. The pair is COMPLETE; the issuer holds it.</decomp_context>
</decomp_ref>

  <objective>
    Apply, ONE ARTIFACT AT A TIME and in this order, (1) the two new inline-policy statements S6 and S7 of `irpt-commentary-draft-store-role`, (2) the new zip of `irpt-commentary-draft-store-lambda`, (3) a SURGICAL zip of the commentary function `outlook-global-commentary-draft-lambda` (the pull functions keep their zip). Then the driven proof of the packet's section 3 on an EXISTING job row of a synthetic test request. No model call. Statuses, hashes and counts only.
  </objective>

  <context>
    The pair binds; read both halves first.
    COO half and packet: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~T2/R54_FWD4_COMMENTARY_HOP_DEPLOY_PACKET_20261016.md`, AS AMENDED (section 9, AMENDMENT 1), commit `5722f5c90f`, git blob `27db48afd438dc926025f6f07cbf1df7cc1843e3` (it replaces blob `8dcbccc512` of the first cut). READ ITS SECTIONS 1 TO 9; they are the act, this order only adds the conditions and the proof arms.
    CTO half, RE-SIGNED on the amended blob (msg 9195): `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R54_FWD4_COMMENTARY_HOP_CTO_HALF.md` @fc8422ba1c (first signed @e22f40258c, msg 9181).
    The pin: the artifacts' blobs are named in the packet header and section 9 (HEAD `4061e6a0d8` or a descendant that changes NONE of them); the `.tf` blob is now `0ab8d2e9ebed9f7d041ac19df9783151bc78f8d6` (repaired by AR-tf-77, `0a0214b507`). The source-map row for `durable_job.py` is landed (`110d6583be`).
    Terraform roots: the draft-store role, policy and Lambda are in `infra/aws/terraform/investor-reporting/export/commentary_draft_store.tf`; the commentary function is in `infra/aws/terraform/transcripts`.
    KNOWN (issuer's reads 2026-10-16 ~07:4xZ): draft-store Lambda digest `cwf6bUEbPvKkpOtbldaTmzaqst08D/L7DFB32RtJP1A=` (139,803 bytes); its inline policy carries S1 to S5; the commentary function and both pull functions read `hUZY39qN`.
  </context>

  <cto_conditions_verbatim>
    (CTO half SIGNED @e22f40258c, msg 9181) 1. The proof's positive arm uses an EXISTING job row of a synthetic test request (r41b's, or one minted); a nonexistent id answers false on both invokes because of attribute_exists(#job), so it is the negative control. 2. The draft-store zip is built BUILD_ONLY twice, identical, and its digest goes into the ledger before the deploy. 3. The full simulate battery. 4. One artifact at a time.
  </cto_conditions_verbatim>

  <the_act>
    0. NEVER-2 ledger read (every live worktree, `ls-tree`). Open ONE change ledger naming this order, the HEAD you build from and the three artifacts. Check the clock: the Teams pull fires on the hour 13:00Z to 22:00Z on weekdays and the mail pull at 23:30Z; the commentary function's step (3) finishes clear of a fire or starts after that fire's REPORT line; say which.
    1. PRECONDITION reads, no write (STOP on any mismatch, name it): the two Lambdas' CodeSha256 (draft store `cwf6bUEb...`, commentary `hUZY39qN...`, both pull functions `hUZY39qN...`), LastModified, MemorySize, Timeout and environment NAMES; the role's inline policy Sids (S1 to S5); the commentary function's event source mapping (1, Enabled). Fetch both deployed zips OUTSIDE the repo, print their base64 sha256 (these are the rollback artifacts).
    2. SIMULATE battery on the new policy (CTO condition 3), before any apply: `aws iam simulate-custom-policy` with the policy document S1 to S7 as the TF plan renders it. ALLOWED: `dynamodb:UpdateItem` on the jobs table with `dynamodb:Attributes` hop_failure, tenant, job and `dynamodb:ReturnValues` NONE and a served firm's leading key. DENIED: PutItem, DeleteItem, GetItem, Query, Scan on the jobs table, and an UpdateItem naming any other attribute. State that S7's encryption context cannot be simulated; the proof's write is its evidence. Any mismatch = STOP, nothing applied.
    3. ARTIFACT 1, the grant: `terraform plan` in the draft-store root, plan-only first: exactly ONE resource changes in place (the inline policy of `irpt-commentary-draft-store-role` gaining S6 and S7), 0 add, 0 destroy; any other resource or attribute = STOP. Then `safe-apply` of that target, then a re-plan: `No changes`. After read: the inline policy Sids S1 to S7.
    4. ARTIFACT 2, the draft-store zip: build it from the source map entry `irpt-commentary-draft-store-lambda` at its pins BUILD_ONLY TWICE; the two zips must be byte-identical; print the base64 sha256 and the member count and RECORD THE DIGEST IN THE LEDGER BEFORE THE DEPLOY (CTO condition 2). DIFF its members against the fetched live zip: exactly `commentary_draft_store.py` (changed) and `durable_job.py` (added) may differ; any other = STOP and name it. The zip must contain `submission.py` and `durable_job.py`; the zip imports `commentary_draft_store` in a clean interpreter (`python -I`, extract root on `sys.path`, working directory NOT the repo). Deploy through the Terraform path only (never `aws lambda update-function-code`); after read: the live CodeSha256 equals the recorded digest.
    5. ARTIFACT 3, the commentary function, SURGICAL as in R42 section 8 and t34 amendment 1: copy the fetched live commentary zip (digest `hUZY39qN`), replace EXACTLY the member(s) the pin changed (`data/transcripts/scripts/commentary/lambda_handler.py`, from `git show <HEAD>:<path>`), add nothing, remove nothing. Print the surgical zip's sha256 and member count, the three proofs of t34 step 4' (replaced member byte-equal to the pin; every other member byte-equal to the live zip; clean-interpreter import of `commentary.lambda_handler`, `commentary.drafter`, `commentary.entry`), record the digest in the ledger. Targeted apply of `aws_lambda_function.commentary` ONLY (`-target`); the plan reads 0 add, 1 change (only `source_code_hash` and what follows), 0 destroy. After read: the commentary function runs the surgical digest; BOTH pull functions still read `hUZY39qN`; Memory, Timeout, environment names and the event source mapping unchanged.
    6. PROOF (one driven sequence; NO model call, NO ticket post). PRECONDITION: read the synthetic job row by `get-item` on `irpt-jobs` with key tenant `49financial`, job `REQ-d47252fe74634d0c5cdd8067` (the FWD-1 run's request, filed by the synthetic staff user `fwd1-staff-r41b` with the synthetic holdings file; CTO condition 1): it must EXIST, its state must be recorded (expected READY) and `hop_failure` must be ABSENT; otherwise STOP the proof (artifacts stay applied; report). Invoke `irpt-commentary-draft-store-lambda` with `{"op":"fail","tenant":"49financial","request_id":"REQ-d47252fe74634d0c5cdd8067","hop":"COMMENTARY","code":"COMMENTARY_DRAFT_REFUSED"}` TWICE: the first answer `{"status":"OK","hop_failure_written":true}`, the second `false`. Read the row: `hop_failure` = {hop COMMENTARY, code COMMENTARY_DRAFT_REFUSED, at a UTC stamp}, and the job state UNCHANGED from the precondition. NEGATIVE ARMS (each one invoke): the same op with a request id that has NO job row (a syntactically valid `REQ-` plus 24 zeros) answers `hop_failure_written` false and `get-item` reads that key ABSENT afterwards (no row created); the same op naming tenant `inflection` with the 49financial request id answers `{"status":"REFUSED","reason":"UNAVAILABLE"}` and the 49financial row is unchanged. Then RESTORE the synthetic row: record the written `hop_failure` value, then remove ONLY that attribute from that ONE row with a conditional update (condition: its code equals the recorded one), and read it ABSENT. Side effects stated: one attribute written and removed on one synthetic row; no other row.
    7. Close the ledger. If step 3, 4 or 5 fails after its apply, or step 6 shows a result other than expected: ROLL BACK in session in reverse order (the fetched zips back by the Terraform path, the previous inline policy restored, each artifact read back to its recorded pre-act state) and say so; nothing is left half-landed.
  </the_act>

  <amendment_1>
    AMENDMENT 1 (issuer, 2026-10-16 ~08:2xZ), on your STOP at the plan (msg 9184; record `deliverables/irpt_anlreq_t54/A_PRE_T54.txt`): the defect was the issuer's (a missing comma in the grant source); it is REPAIRED on trunk (`0a0214b507`, blob `0ab8d2e9eb`) and the pair is re-signed (above). THIS AMENDMENT IS YOUR GO TO RESUME. Your ledger `irpt-t54-commentary-hop-20261016` may stay open (its window runs to ~13:53Z); steps 0, 1 and 2 stand if your reads are still equal to the packet (re-read the digests and the policy Sids: any change = STOP); redo step 2's simulate battery if you rebuilt anything.
    NEW STEP 3a, before step 3's plan: in the draft-store root `terraform init -backend=false` and `terraform validate` on the repaired file; ANY error = STOP, nothing applied, and paste the first error's text (it may be a separator the scanner did not read). Then step 3 as written, and steps 4 to 7 unchanged.
  </amendment_1>

  <amendment_2>
    AMENDMENT 2 (issuer, 2026-10-16 ~08:5xZ), on your report (msg 9235). (a) NEGATIVE ARM A is ACCEPTED AS CORRECTED, no rollback: the order's text was mis-specified. `store()` resolves the REQUESTS record first (the same binding as `put`), so a request id with no record answers `REFUSED`/`UNAVAILABLE` and never reaches the jobs write; the substantive check (no row created, key ABSENT after) held. The writer's own `false` on a missing job row (the `attribute_exists(#job)` condition) is covered offline by the AR-tf-74 tests; a live arm for it would need a request record with no job row, and no synthetic one exists. Your proof stands: 4 arms plus the corrected arm A. (b) NEW STEP 8: record the deploy of the draft-store Lambda in the source map by the standing procedure you use after a Terraform deploy (`record-terraform-deploy.sh` or its successor), so that `artifact_sha256` of `irpt-commentary-draft-store-lambda` reads `RizVjaXi...` and no longer `cwf6bUEb...`; say in your report which command and which commit. This is your standing lane for that line (your `ci: record deploy` commits). If the procedure refuses, STOP and report; do not edit the map by hand. (c) Then close the ledger and write the proof instance; the status flip is mine.
  </amendment_2>

  <amendment_3>
    AMENDMENT 3 (issuer, 2026-10-16 ~09:1xZ), on your close (msg 9238). Everything is graded: your instance is VALID and my live read agrees. The flip gate looks for the proof instance BESIDE the order, in `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/` itself (t34 kept its instance there), not in `deliverables/irpt_anlreq_t54/`, and the issuer's lane cannot write your deliverables folder. PLACE the same instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/IRPT_ANLREQ.TO-APPLY-t54.commentary-hop-fwd4-aq2.proof_of_spec.json` (a copy of the one at `9dc717f16d`, unchanged bytes; keep the original), commit it, and tell me the hash. The status flip is then mine.
  </amendment_3>

  <bounds>
    - Exactly the three artifacts of the packet, one at a time. No other function, role, table, queue, schedule, mapping, key or secret. Never `aws lambda update-function-code`; never a bare `terraform apply`.
    - The proof touches ONE row (the synthetic request's) and removes what it wrote. No client job, no other firm's row, no `put-item`/`delete-item` on `irpt-jobs`.
    - No transcript text, mail content, prompt text, draft text, bearer or address in any file or message.
    - No outside-model call. No second proof sequence without the issuer's word.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~AQ2/logs/
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
  </paths>

<preflight>
comp-schedule: RUN -- artifact 3 changes the code behind the commentary function only (its queue mapping unchanged); the pull functions' schedules (`teams-global-transcripts-pull-hourly` cron(0 13-22 ? * MON-FRI *), the mail pull cron(30 23 * * ? *)) are not touched, and the surgical zip does not reach those functions. Step 0 keeps the commentary apply clear of a fire.
comp-iam: RUN -- `comp-iam service irpt-commentary-draft-store-lambda` printed `No service matching` against 197 Lambda services and 222 roles (the function and role are not in its census; the cloud graph, vintage 2026-10-16 06:23Z, lists the function, role and inline policy as DECLARED). The lens is BLIND on this subject, declared and not read as clean. The grant is checked by the static test (11 tests, 12 of 12 mutants caught), by step 2's simulate battery and by step 6's write.
comp-adversary: RUN -- a rollback artifact mistaken for a dist zip (step 1 fetches the deployed bytes); the draft-store zip built once and trusted (step 4 builds twice); `durable_job.py` missing from the zip (step 4's member rule); the surgical zip reaching a pull function (step 5's after read); a proof on a nonexistent row read as success (step 6's negative arms); the proof leaving a `hop_failure` on a row (step 6's restore).
lane: the applier's deliverables, logs, the change ledger and its sentinel.
</preflight>

<proof_of_spec>
  <criterion id="AR76-tf-AC1" cell_refs="AR-tf-76"><invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/R55_CHECKS/r55_checks.py ap1</invocation><expect>R55-AP1-OK</expect></criterion>
</proof_of_spec>
  AC1's row also states the precondition reads, the two rollback artifacts' hashes, the grant's plan line, the simulate battery's allowed and denied lines, the draft-store zip's twice-built digest and member diff, the surgical zip's three proofs and sha, the after reads (including both pull functions), each proof answer (the two positive invokes, the two negative arms, the row before and after), the restore read, and the ledger path.
  Dry-run before the act (issuer, 2026-10-16 ~08:0xZ): `R55-AP1-FAIL inline policy lacks S6,S7` -- FAIL as expected. The checker's `--self-test` reads `R55-SELFTEST-OK`.

<expected_criteria>AR76-tf-AC1</expected_criteria>

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: every item AC1's row lists; the check line; the ledger path and its closed state; commit hashes (read with an author filter) and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
