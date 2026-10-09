<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-RUN-w20.teams-silver-rewipe-dell2</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TR2</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R20.md</decomp_doc>
<owned_cells>TR-w-20</owned_cells>
<decomp_context>Round 20 cell TR-w-20 (CTO ADDENDUM 10 item 1): the W1-S7 re-wipe of the 30 existing Teams silver keys under a pair. HELD: the GO is a separate message, sent when the CTO half lands.</decomp_context>
</decomp_ref>

  <reassignment>
    AMENDMENT 1 (issuer, 2026-10-09 ~10:2xZ): re-addressed from 0.7.0_AE_CloudOps~DELL2 (GO 09:51Z, untouched to 10:23Z; it took other orders) to
    0.7.0_AE_CloudOps~TR2, the lane 0.0.0_AB_MSTR~DELL2 seated for NFRA_TRNSPT only (msg 3135) under CTO ruling @5ff94852a6, as the CTO half
    @7a2e7199ed allows. 0.7.0_AE_CloudOps~DELL2 does NOT run this order. deploy_ledger.py commits its own files at open (@00d3393ff3).
  </reassignment>

  <objective>
    Re-wipe, in place, the 30 Teams silver keys of monday_meeting, ocio_ic and asset_management_ic with the tool built in TR-w-19, and read them
    back. research_meeting is EXCLUDED. Report counts, keys and version ids only.
  </objective>

  <context>
    The pair binds; read both halves: COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_TEAMS_SILVER_REWIPE_20261009.md`
    and the CTO half beside it. The prior VersionIds (the rollback source) are in
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R20_REWIPE_PRIOR_VERSIONS.json` (30 keys).
  </context>

  <the_act>
    0. Open a change ledger in org/critical_paths/change_management/ naming the pin. Re-list the three series' silver keys with their current
       VersionIds; they must equal the JSON's 30 rows. Any difference = STOP.
    1. From a clean extract of the pin: `python -m data.transcripts.scripts.teams.rewipe_silver --series monday_meeting,ocio_ic,asset_management_ic --dry-run`
       must list exactly those 30 keys; then the same with `--apply`. Never pass research_meeting.
    2. Re-list: the same 30 keys, each with a NEW VersionId; per-key row counts before and after equal. Close the ledger.
    ROLLBACK, if the issuer asks: copy each prior VersionId back over its key; no delete.
  </the_act>

  <bounds>
    - These 30 keys only; no other series, prefix, bucket or key policy. No transcript text in any file or message. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
    org/critical_paths/change_management/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- one run on the issuer's request.
comp-iam: RUN -- dell2's agent user holds GenerateDataKey on the transcripts bucket (TO-APPLY-27, read back live, MSTR msg 2591) and s3 Get/Put via its own policy; no grant change.
comp-adversary: RUN -- a wider rewrite (exactly 30 keys before and after; research_meeting excluded by --series); a lost prior (VersionIds captured and re-checked at step 0); a row-count change (per-key before/after); text leaking (counts only); BLIND: the residual tokens themselves, read by the issuer's re-wipe sweep as counts.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-w-20"><invocation>python -m data.transcripts.scripts.teams.rewipe_silver --series monday_meeting,ocio_ic,asset_management_ic --dry-run</invocation><expect>keys=30</expect></criterion>
</proof_of_spec>
  AC1's row also states the 30 new VersionIds against the prior ones and the per-key row counts before and after.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the step-0 equality; the run's summary line; the 30 new VersionIds; the row-count equality; the ledger path;
    commit hashes and the measured push state. Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
