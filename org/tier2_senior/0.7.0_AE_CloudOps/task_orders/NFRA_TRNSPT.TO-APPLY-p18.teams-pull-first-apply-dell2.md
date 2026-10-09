<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-p18.teams-pull-first-apply-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R18.md</decomp_doc>
<owned_cells>TR-s-18</owned_cells>
<decomp_context>Round 18 cell TR-s-18 (FWD-2) widened by CTO ADDENDUM 7 @504e23e93f (msg 2909): the Teams pull was never applied; round 18 cuts its apply in two steps under one pair. HELD: the GO is a separate message, sent when the CTO half lands.</decomp_context>
</decomp_ref>

  <reassignment>
    AMENDMENT 1 (issuer, 2026-10-09 ~10:4xZ): re-addressed to 0.7.0_AE_CloudOps~TR2 (the NFRA_TRNSPT lane, MSTR msg 3135). Step 1 STOPPED earlier at
    @7d2c8c8c53 (secret absent; transport a stub, row D2-S10). Both are fixed and merged: the real transport + pull.tf on gateway/transcripts/bearer
    (TR-t-20 @488c840f48) and the wall-clock interim, content VTT only, wall-clock NULL 'absent', never derived (CTO ADDENDUM 11; @a9039b8d62).
    Re-run from STEP 1 on a zip built from a pin carrying @a9039b8d62; the CTO half binds that rebuilt zip's sha256 in the ledger. Runs AFTER
    TO-RUN-w20. S05 now reads the expiry of gateway/transcripts/bearer (never its value). 0.7.0_AE_CloudOps~DELL2 does NOT run this order.
  </reassignment>

  <objective>
    The FIRST apply of the Teams meeting pull (infra/aws/terraform/transcripts/pull.tf): step 1 a preconditions read (no write), step 2 a targeted
    safe-apply, then ONE seat invoke. Report statuses and counts only.
  </objective>

  <context>
    The pair binds; read both halves first: COO half
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_TEAMS_PULL_FIRST_APPLY_20261009.md`, and the CTO half
    the CTO commits beside it. The gap is measured in `R18_FWD2_SCHEDULED_READ.json` @3f7583537b.
  </context>

  <the_act>
    0. Open a change ledger in org/critical_paths/change_management/ naming the pin and the built zip's sha256. Print the LIVE CodeSha256 of
       `outlook-global-transcripts-pull-lambda` (the shared package's other user).
    1. STEP 1 (no write): S04 -- one gateway transcript-tool call read by name, status and count only; S05 -- the expiry of the token in
       `gateway/transcripts/bearer`, never its value; KMS -- the key policy read for kms:CreateGrant by the applying identity. Any unmet = STOP,
       named; a KMS refusal goes to 0.0.0_AB_MSTR~DELL2 as a laptop act.
    2. STEP 2: build `infra/aws/lambda/transcripts-pull/build.sh`; safe-apply `infra/aws/terraform/transcripts` with `-target` on exactly the nine
       pull.tf resources the COO half lists. The plan shows exactly those creates; anything else = STOP.
    3. After: re-print the outlook pull's CodeSha256 (must equal step 0's); ONE invoke of `teams-global-transcripts-pull-lambda`; report its
       status and counts (meetings seen, landed, skipped), no content. Close the ledger.
    ROLLBACK, if asked: `terraform destroy -target` of each created resource -- a destroy is Andrew's word, never this seat's.
  </the_act>

  <bounds>
    - pull.tf's resources only; no other root, key policy or Lambda. No transcript text or token in any file or message. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
    org/critical_paths/change_management/
  </paths>

<preflight>
comp-schedule: RUN -- the act creates teams-global-transcripts-pull-hourly cron(0 13-22 ? * MON-FRI *) (pull.tf:120-123), its own clock; no upstream trigger, no alarm.
comp-iam: RUN -- the writer role (pull.tf:37-96): S3 Get/Put on teams/transcripts/* + a KMS grant; a THIRD principal, not in reader_principal_arns; CreateGrant read in step 1.
comp-adversary: RUN -- the shared zip moving the live outlook pull (targeted plan + CodeSha256 before/after); an expired token (S05 read first); a KMS grant refused (step 1, laptop route); content leaking (statuses and counts only); BLIND: the first scheduled fire's content, read later by the issuer as counts.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-s-18"><invocation>aws lambda get-function --function-name teams-global-transcripts-pull-lambda --query "Configuration.State"</invocation><expect>"Active"</expect></criterion>
</proof_of_spec>
  AC1's row also states step 1's three reads, the outlook pull's CodeSha256 before and after (equal), the invoke's counts and the ledger path.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: step 1's three results; the plan line; the outlook CodeSha256 equality; the invoke's status and counts; the
    ledger path; commit hashes and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
