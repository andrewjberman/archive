<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-RUN-a17.research-fold-rewrite-apple-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R17.md</decomp_doc>
<owned_cells>TR-a-17</owned_cells>
<decomp_context>Round 17 (CTO msg 2293, analysis ADDENDUM 4, E2): "the Apple re-write on CloudOps~DELL2". Moved from laptop 0.7.0_AE_CloudOps by laptop 1.0.0_SA_CTO frame 24e5ac25 item (3), relayed by 0.0.0_AB_MSTR~DELL2 msg 2229 (Andrew-direct ~02:5xZ: the Dells run their own scripts). MSTR msg 2307 measured that the laptop has not written since its GO.</decomp_context>
</decomp_ref>

  <objective>
    Re-run the research fold once, from box/dell2 @5074835d70, under this seat's identity: it OVERWRITES the same 29 KMS-encrypted
    parquets under `s3://opal-data-transcripts/teams/transcripts/silver/research_meeting/`, now keeping "Apple" as an issuer (the
    CVO-approved exception, msg 2200, ADJUDICATION_v9), and reads them back. Return counts and keys to 2.0.0_SA_COO~T2.
  </objective>

  <context>
    The same script and the same 29 keys as NFRA_TRNSPT.TO-RUN-b11 (complete, laptop, 21:50Z). The input tree
    `research_transcripts/structured` is `826cbbf2787f` at both 9f8dddcb9b and dell2 HEAD (measured by the issuer 03:3xZ). Versioning is
    Enabled, so every overwritten object keeps its prior. The run is idempotent: a late laptop run would rewrite identical bytes. Expected:
    rows 20,473, held_out at or below 3,644, rewipe 0. Never-widen does not apply: the write set is a literal key list (CLAUDE.md NEVER-1
    non-application). dell2's agent user is Decrypt-only on the transcripts key (key policy `DellAgentUsersDecryptOnly`), so step 1 is a
    simulate; the key-policy grant is the laptop's act (CTO msg 2259).
  </context>

  <the_act>
    1. Simulate `kms:GenerateDataKey` and `kms:Encrypt` on the transcripts key, and `s3:PutObject` on the prefix, for this seat's identity.
       Any refusal is a STOP: send the measured refusal to 0.0.0_AB_MSTR~DELL2 and report it to the issuer. Nothing is written.
    2. List the prefix (auto-paginated, count client-side): expect EXACTLY 29 keys. Save each key's current VersionId. Any other count is
       a STOP.
    3. From the repo root at 5074835d70 (a clean `git archive` extract as TO-RUN-b11 if the shared tree is dirty under `data/` or `lib/`):
       `python -m data.transcripts.scripts.teams.research_fold --apply --verify --src C:/dev/ajb_workspace/research_transcripts/structured`.
    4. Re-list: the same 29 keys, each with a NEW VersionId. Compare the counts with the expectation; a difference is reported, not repaired.
    ROLLBACK, if the issuer asks: copy each saved prior VersionId back over its key; no delete is needed.
  </the_act>

  <bounds>
    - One run, this prefix only, the same 29 keys. No other bucket, prefix or key policy. No transcript text in any file or message.
    - No push of a shared branch. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one run on the issuer's request; no schedule is created.
comp-iam: RUN -- 1 key policy read (infra/aws/terraform/transcripts/main.tf: DellAgentUsersDecryptOnly = kms:Decrypt + kms:DescribeKey); the encrypt need is simulated at step 1 and a refusal stops the run.
comp-adversary: RUN -- a wider write (exactly 29 keys before and after); a lost prior (versioning Enabled, VersionIds saved); an input drift (tree 826cbbf2787f measured equal); a KMS refusal mid-run (simulated first); text leaking (counts, keys and version ids only); BLIND: a late laptop run, idempotent by construction.
lane: the seat's own deliverables and logs; the run writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-a-17"><invocation>aws s3api list-objects-v2 --bucket opal-data-transcripts --prefix teams/transcripts/silver/research_meeting/ --query "length(Contents)"</invocation><expect>29</expect></criterion>
</proof_of_spec>
  AC1's row states the client-side count, and that each of the 29 keys carries a VersionId newer than the saved one.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the simulate result; the before list (29) with VersionIds; the run's last lines (counts and keys); the
    after list with new VersionIds; the comparison with the expected counts; the time in UTC; commit hashes and the measured push state.
    Leave the status flip to the issuer.
  </report>
</task_order>
