<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-RUN-b11.research-fold-rewrite-with-securities-allowlist-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>SERVED</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R11.md</decomp_doc>
<owned_cells>TR-b-11</owned_cells>
<decomp_context>dell2's round 11 (on origin box/dell2; reaches the laptop tree at the next box pass): "TR-b-11 | E2: re-fold and re-write the 29 Research objects (laptop write, as round 9), read back on the stored bytes". dell2 `2.0.0_SA_COO~T2` msg 1667, relay `org/tier0_exec/0.0.0_AB_MSTR/deliverables/RELAY_DELL2_TRNSPT_TR_B11_RUN_ASK_2127Z.md`; dell2 CTO round-10 analysis @8ce4b5098e E2.</decomp_context>
</decomp_ref>

  <closure>
    COMPLETE (issuer, ~21:5xZ). Run 2026-10-08T21:50:48Z from 9f8dddcb9b: exactly the 29 keys before and after, 29/29 new
    VersionIds, priors saved; stored read-back 20,473 rows / 3,644 held out / rewipe 0, as dell2 expected. Issuer live read: 29
    objects, written 21:50:27Z-21:50:29Z. Proof VALID (@7ab319f1ad). No delete.
  </closure>

  <objective>
    Re-run dell2's research fold once, from dell2's commit `9f8dddcb9b`, under the laptop identity: it OVERWRITES the same 29
    KMS-encrypted parquets under `s3://opal-data-transcripts/teams/transcripts/silver/research_meeting/` with company names
    preserved by the new securities allowlist, and reads them back. Return counts and keys to dell2.
  </objective>

  <context>
    As NFRA_TRNSPT.TO-RUN-x9 (complete; same script, same 29 keys). New at this commit: `securities_allowlist.py` and its source
    file. The input `research_transcripts/structured` tree at `9f8dddcb9b` equals the laptop HEAD's (`826cbbf2787f`, measured by the
    issuer ~21:3xZ). The bucket's versioning is Enabled (measured), so every overwritten object keeps its prior version. dell2's
    expected result: rows 20,473, held_out 3,644, rewipe 0. Never-widen does not apply: the write set is a literal key list
    (CLAUDE.md NEVER-1 non-application).
  </context>

  <the_act>
    1. Load /cloud-ops. List the prefix (auto-paginated, count client-side): expect EXACTLY the 29 keys TO-RUN-x9 wrote. Save each
       key's current VersionId (`list-object-versions`, latest). Any other count or key is a STOP.
    2. Re-check `git rev-parse 9f8dddcb9b:research_transcripts/structured` == `git rev-parse HEAD:research_transcripts/structured`;
       unequal is a STOP.
    3. Extract only what the module needs from `9f8dddcb9b` into a fresh temp directory with `git archive` (as TO-RUN-x9: `data/`,
       `lib/`, `infra/logic/registry/`, `org/standards/NAMING_SCHEMA.json`; add a path only on an import error, and name it). Run from
       it: `python -m data.transcripts.scripts.teams.research_fold --apply --verify --src C:/Users/AndrewBerman/Desktop/ajb_workspace/research_transcripts/structured`.
    4. Re-list: exactly the same 29 keys, each with a NEW VersionId. Compare the run's counts with dell2's expectation (rows 20,473,
       held_out 3,644, rewipe 0) and report any difference; a difference is reported, not repaired.
    5. Return counts, keys and the before/after VersionIds as a FILE to dell2 through 0.0.0_AB_MSTR.
    ROLLBACK, if dell2 asks: copy each saved prior VersionId back over its key (`copy-object` with `?versionId=`); no delete is needed.
  </the_act>

  <bounds>
    - One run, this prefix only, the same 29 keys. No other bucket, prefix or key policy. No transcript text in any file or message;
      company names in the data are the allowlist's, and are not printed either.
    - No full worktree. No push of a shared branch. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one run on dell2's request; no schedule is created.
comp-iam: DECLARED-NOT-APPLICABLE no identity change; the laptop identity's encrypt on the transcripts key is the reason for the route.
comp-adversary: RUN -- a wider write (the before list must be exactly the 29 keys; the after list the same 29); a lost prior (versioning Enabled, prior VersionIds saved, copy-back rollback); an input drift (tree hash equality at step 2); text leaking into a report (counts, keys and version ids only); BLIND: dell2's readers of the prefix (dell2 reads back the stored bytes, its own cell).
lane: the <paths> block names the seat's own deliverables and logs; the run writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-b-11"><invocation>aws s3api list-objects-v2 --bucket opal-data-transcripts --prefix teams/transcripts/silver/research_meeting/ --query "length(Contents)"</invocation><expect>29</expect></criterion>
</proof_of_spec>
  AC1's row states the client-side count, and that each of the 29 keys carries a VersionId newer than the saved one.

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the before list (29) with VersionIds; the two tree hashes; the run's last lines (counts and keys);
    the after list with new VersionIds; the comparison with dell2's expected counts; the time in UTC in the subject; the result file;
    commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
