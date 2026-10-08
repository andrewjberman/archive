<task_order>
  <metadata>
    <id>IRPT_BCKEND.TO-APPLY-Y68.release3-test-admit-cleanup-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>IRPT_BCKEND</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP_R68_Y.md</decomp_doc>
<owned_cells>IB-yr-681</owned_cells>
<decomp_context>dell2's R68 (on origin box/dell2; reaches the laptop tree at the next box pass) cuts release 3 as IB-yr-681, "cleanup via the laptop". dell2 2.0.0_SA_COO~Y2 msg 1687, relay org/tier0_exec/0.0.0_AB_MSTR/deliverables/RELAY_DELL2_RELEASE3_CLEANUP_Y68_2141Z.md; 1.0.0_SA_CTO msg 107370 (agreed) and 107371 (Andrew's word).</decomp_context>
</decomp_ref>

  <objective>
    Delete exactly the test records of ONE release-3 test upload at 49financial, named in dell2's keys file: 7 `irpt-requests`
    rows and 2 `opal-data-irpt` objects (every version), on the E6 leg-2 pattern. dell2 cannot decrypt key `7f4d3042-...`.
  </objective>

  <context>
    Keys file: `git show 84916b911a:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~159/Y68-1_admit_keys.json`
    (origin box/dell2): `admit_keys` = 7 entries of kind ddb (table irpt-requests) + 2 of kind s3 (bucket opal-data-irpt), and
    `s3_versions`. **The S3 deletes are APPROVED by Andrew**, verbatim "you can delete it, go do it (regarding the test files in the IRPT
    storage bucket)", record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_214xZ_RELEASE3_TEST_S3_DELETE_APPROVED.md`
    (CTO msg 107371): exactly the 2 keys in the file, every version, no other key. **OPAQUE IDS ONLY:** the keys file itself carries a
    filer email and names (fields such as `test_filer_email`, `advisor`); never copy any email, name or raw principal id into a
    file, commit or message. Print a sha256 prefix where an identity must be shown (row NFRA_CTLPLN-S35; CTO msg 107348).
  </context>

  <the_act>
    1. Load /cloud-ops. Read the keys file; print only the COUNTS (7 ddb, 2 s3) and the table/bucket names. Any other count is a STOP.
    2. Per DDB key, and no other: `get-item` -> record EXISTS or NOT_FOUND, and for an existing row a sha256 prefix of `body_sha256`,
       `owner` and `acting_principal_id` (never the values); `delete-item`; `get-item` NOT_FOUND (strongly consistent).
    3. Sweep: query tenant `49financial` for the file's `upload_id` (and `input_id`); report the COUNT of rows found beyond the 7. Any
       extra row is REPORTED, NOT deleted.
    4. Per S3 key: `list-object-versions` for that exact key; for each version `head-object --version-id`, `delete-object
       --version-id`, `head-object --version-id` 404; then `list-object-versions` empty for that key. The versions listed must
       include the file's `s3_versions`; a version the file does not list is deleted only if it is under the same exact key, and
       is named (by version id) in the report.
    5. Result FILE `Y68-1_laptop_cleanup_result.json` shaped `{"results":[{"key_ref","before","after_delete"}]}` with OPAQUE refs
       (sha256 prefix of the key), to dell2 through 0.0.0_AB_MSTR, and the result line to 2.0.0_SA_COO~C. Run a count of
       email-shaped strings over every file you write; it must read 0 before commit.
  </the_act>

  <bounds>
    - The 9 named keys and their S3 versions only. No other row, object, table, bucket or policy. No GetSecretValue.
    - No email, name or raw principal id in any file, commit or message. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one cleanup on dell2's request.
comp-iam: DECLARED-NOT-APPLICABLE no identity change; the laptop identity's decrypt on key 7f4d3042 is the reason for the route.
comp-adversary: RUN -- a delete beyond the file (fenced to 9 keys; the sweep reports, never deletes); an S3 delete beyond Andrew's scope (2 exact keys, every version, named); identity leakage (opaque refs; an email count of 0 over every written file); BLIND: dell2's own deletes (the test profile row in opal-users-v2 is dell2's).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="IB-yr-681"><invocation>python -c "import json,subprocess as s,boto3;k=json.loads(s.check_output(['git','show','84916b911a:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~159/Y68-1_admit_keys.json']));c=boto3.client('s3');print('VERSIONS_LEFT=%d'%sum(len([v for v in c.list_object_versions(Bucket=x['bucket'],Prefix=x['key']).get('Versions',[]) if v['Key']==x['key']]) for x in k['admit_keys'] if x['kind']=='s3'))"</invocation><expect>VERSIONS_LEFT=0</expect></criterion>
</proof_of_spec>
  AC1 counts versions of exactly the 2 named keys (never the wider prefix, which holds other uploads); the row also states the 7 DDB
  keys read NOT_FOUND after delete.

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the counts; per key EXISTS/NOT_FOUND before and NOT_FOUND after (opaque refs); the sweep count;
    each S3 version deleted (by version id) and the empty re-list; the email-shaped count (0); the time in UTC in the subject; the
    ledger entry; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
