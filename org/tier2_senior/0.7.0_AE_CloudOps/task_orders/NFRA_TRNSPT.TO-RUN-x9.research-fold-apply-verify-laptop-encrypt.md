<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-RUN-x9.research-fold-apply-verify-laptop-encrypt</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R9.md</decomp_doc> round 9, cell TR-x-9 (dell2 decomposition R9 ruling 5; dell2 CTO analysis @08ff07562f and ruling 1542), the one act dell2 cannot do: dell2 `2.0.0_SA_COO~T2` msg 1554, relay `org/tier0_exec/0.0.0_AB_MSTR/deliverables/RELAY_DELL2_TRNSPT_KMS_ENCRYPT_ASK_20261008_2028Z.md`.
<owned_cells>TR-x-9</owned_cells>
</decomp_ref>

  <closure>
    COMPLETE (issuer, ~21:0xZ). Run 2026-10-08T20:42:22Z: 29 objects written and verified; issuer live count 29. Proof VALID
    after the decomp_doc repair (@0074e521aa). Temp extract retained pending Andrew's word on its deletion.
  </closure>

  <objective>
    Run dell2's research fold once, from dell2's commit, under the laptop identity (which can encrypt with the transcripts KMS
    key; dell2's grant is decrypt-only): it writes 29 new KMS-encrypted parquets under
    `s3://opal-data-transcripts/teams/transcripts/silver/research_meeting/` and reads them back. Return the printed counts and
    keys to dell2.
  </objective>

  <context>
    Commit `01e971915c` is on origin `box/dell2`. The script `data/transcripts/scripts/teams/research_fold.py` writes with
    `put_object` (`ServerSideEncryption=aws:kms`, the key resolved from `parse_silver.KMS_ALIAS`) and `--verify` reads back
    (counts and keys only; it prints no transcript text). The prefix holds 0 objects today and nothing reads it. Never-widen does
    not apply: the write set is a literal set of new keys (CLAUDE.md NEVER-1 non-application). Disk on the laptop is ~11 GB: do
    NOT add a full worktree.
  </context>

  <the_act>
    1. Load /cloud-ops. `aws s3api list-objects-v2 --bucket opal-data-transcripts --prefix teams/transcripts/silver/research_meeting/`
       (auto-paginated; count client-side): expect 0 objects. Any object there is a STOP (report the keys).
    2. Extract ONLY what the module needs from the commit into a fresh temp directory (no worktree):
       `git archive 01e971915c data/ lib/ | tar -x -C <tmpdir>` (add a path only if the import fails, and name it). Run from
       `<tmpdir>`: `python -m data.transcripts.scripts.teams.research_fold --apply --verify`.
    3. Re-list the prefix: expect exactly the keys the run printed (29). Record count and keys.
    4. Return the printed counts and keys as a FILE to dell2 through 0.0.0_AB_MSTR, and the result line to 2.0.0_SA_COO~C.
    5. Delete `<tmpdir>`.
    ROLLBACK, if dell2 asks: deleting those 29 keys. An S3 delete needs Andrew's recorded word (CLAUDE.md Agent Autonomy):
    do not delete without it.
  </the_act>

  <bounds>
    - One run, this prefix only. No other bucket, prefix or key policy. No read of transcript text into any file or message.
    - No full worktree. No push of a shared branch.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one ad-hoc run on dell2's request; no schedule is created.
comp-iam: DECLARED-NOT-APPLICABLE no identity change; the laptop identity's encrypt on the transcripts key is the reason for the route.
comp-adversary: RUN -- writing over existing objects (prefix must read 0 before; STOP otherwise); a wider write (the run's printed keys must equal the re-list); transcript text leaking into a report (counts and keys only); BLIND: dell2's later readers of the prefix.
lane: the <paths> block names the seat's own deliverables and logs; the run writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-x-9"><invocation>aws s3api list-objects-v2 --bucket opal-data-transcripts --prefix teams/transcripts/silver/research_meeting/ --query "length(Contents)"</invocation><expect>29</expect></criterion>
</proof_of_spec>
  The list is auto-paginated by the CLI; state the client-side count beside it in the proof row.

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the before count; the run's last lines (counts and keys); the after count and keys; the time
    in UTC in the subject line; the result file's path; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
