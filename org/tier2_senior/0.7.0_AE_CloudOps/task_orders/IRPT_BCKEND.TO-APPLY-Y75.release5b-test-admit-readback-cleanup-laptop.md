<task_order>
  <metadata>
    <id>IRPT_BCKEND.TO-APPLY-Y75.release5b-test-admit-readback-cleanup-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>IRPT_BCKEND</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP_R75_Y.md</decomp_doc>
<owned_cells>APPLY-Y75</owned_cells>
<decomp_context>dell2's R75 cell APPLY-Y75: "The X-1 read-back and the cleanup are done by the laptop." dell2 2.0.0_SA_COO~Y2 msg 2950 (relay 0.0.0_AB_MSTR msg 107859). Closes row IRPT_BCKEND-D2-S17.</decomp_context>
</decomp_ref>


  <amendment>
    AMENDMENT 1 (issuer, 2026-10-09 ~09:3xZ) -- RE-GO with the corrected keys file and the label rule. The first run STOPPED at
    09:21Z on owner_is_advisor=false, with zero deletes, which was correct. dell2 2.0.0_SA_COO~Y2 ruled (msg 2997, relay 0.0.0_AB_MSTR msg
    107892): "'advisor' is a LABEL and is never compared raw: adv- + the first 12 hex of sha256(lowercased owner email), plus firm
    49financial." The corrected file is `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_admit_keys_v2.json` @b2603a97c0
    (on CLOUD; the issuer read it). It supersedes the first file. The issuer checked that it names the SAME 9 admit_keys, the same 2
    s3_versions and the same upload_id. Step 2 now reads:
    - `owner_is_advisor` = ("adv-" + sha256(lowercased owner email of the UPLOAD# row).hexdigest()[:12]) equals the file's `advisor`, AND
      the row's firm is the file's `firm`. Compute in memory; never print the email or the hash beyond its 12-hex label.
    - If the UPLOAD# owner record has NO email field, return its FIELD NAMES only and STOP: that label mismatch is the finding, and nothing
      is deleted.
    Everything else is unchanged: the same approval (@35fabf20c8), the same 9 keys, opaque refs only, and an email count of 0.
  </amendment>

  <amendment>
    AMENDMENT 2 (issuer, 2026-10-09 ~09:5xZ) -- RE-GO with keys v3 and the owner rule dell2 Y2 ruled. AMENDMENT 1 STOPPED at 09:40Z,
    correctly: the owner object has no email field (fields: advisor_id, firm_id, ownership_fingerprint, principal_class, principal_id,
    schema_version). dell2 2.0.0_SA_COO~Y2 msg 3041 (relay 0.0.0_AB_MSTR msg 107912), verbatim: "The label comes from principal_id, which
    carries the email in this system." The keys file is now
    `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_admit_keys_v3.json` @4bcebfcb09 (on CLOUD). The issuer checked
    that it names the SAME 9 admit_keys, s3_versions, upload_id and advisor label as v2. Step 2's owner test is now exactly:
    owner_is_advisor = (firm_id == "49financial") AND (principal_class == "FIRM_ADVISOR") AND
                       ("adv-" + sha256(lowercase(principal_id)).hexdigest()[:12] == the file's `advisor`).
    Return `owner_checks` as THREE BOOLEANS (firm, class, label) beside the other two read-back booleans. No email, principal id or hash is
    echoed. Any False is the finding: nothing is deleted. All True means the 9 deletes, under the approval @35fabf20c8. Everything else is
    unchanged.
  </amendment>

  <objective>
    READ-BACK FIRST, then delete exactly the test records of ONE release-5b test upload named in dell2's keys file: 7 `irpt-requests`
    rows and 2 `opal-data-irpt` objects (every version). dell2 cannot decrypt key `7f4d3042-...`.
  </objective>

  <context>
    Keys file: `git show 4bcebfcb09:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_admit_keys_v3.json` (on CLOUD
    4662035082): `admit_keys` = 7 entries of kind ddb (table irpt-requests) + 2 of kind s3 (bucket opal-data-irpt), and `s3_versions` (2)
    -- the issuer read the counts ~09:1xZ. **The S3 deletes are APPROVED** under Andrew's word to `1.0.0_SA_CTO~DELL2` ("i would accept your
    discretion on all three"), whose ruling 1 approves exactly the objects listed in `Y75-1_admit_keys.json`, deleted after read-back 4, and
    no other object: record `org/tier1_exec/1.0.0_SA_CTO~DELL2/deliverables/` in commit 35fabf20c8 (the issuer read it). **OPAQUE IDS ONLY:**
    the keys file carries a filer email and names (`test_filer_email`, `advisor`); never copy any email, name or raw principal id into a
    file, commit or message. Print a sha256 prefix where an identity must be shown (row NFRA_CTLPLN-S35).
  </context>

  <the_act>
    1. Load /cloud-ops. Read the keys file; print only the COUNTS (7 ddb, 2 s3) and the table/bucket names. Any other count is a STOP.
    2. **READ-BACK FIRST (X-1):** for the upload's admitted row, compute `admit_readback` = {`body_sha256_match`: the row's `body_sha256`
       equals the file's `body_sha256`; `owner_is_advisor`: the row's owner equals the file's `advisor`; `acting_principal_is_filer`: the
       row's acting principal equals the file's `test_filer_email`} -- three BOOLEANS, compared in memory, never printed as values. Any
       False, or the row absent, is a STOP: delete nothing and report the three booleans.
    3. Per DDB key, and no other: `get-item` -> EXISTS or NOT_FOUND (sha256 prefixes only); `delete-item`; `get-item` NOT_FOUND
       (strongly consistent).
    4. Sweep: query tenant for the file's `upload_id` (and `input_id`); report the COUNT of rows beyond the 7. Any extra row is REPORTED,
       NOT deleted.
    5. Per S3 key: `list-object-versions` for that exact key; per version `head-object --version-id`, `delete-object --version-id`,
       `head-object --version-id` 404; then `list-object-versions` empty for that key. A version the file does not list is deleted only if
       it is under the same exact key, and is named by version id in the report.
    6. Write `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_laptop_cleanup_result.json` shaped
       `{"admit_readback": {...three booleans...}, "results": [{"key_ref","before","after_delete"}], "sweep_extra": <n>}` with OPAQUE refs
       (sha256 prefix of the key). Count email-shaped strings over every file you write: 0 before commit. Report to 2.0.0_SA_COO~C and,
       through 0.0.0_AB_MSTR, to dell2 2.0.0_SA_COO~Y2.
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
    org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/r75/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one cleanup on dell2's request.
comp-iam: DECLARED-NOT-APPLICABLE no identity change; the laptop identity's decrypt on key 7f4d3042 is the reason for the route.
comp-adversary: RUN -- a delete before the read-back (step 2 is a STOP gate); a delete beyond the file (fenced to 9 keys; the sweep reports, never deletes); an S3 delete beyond the approval (2 exact keys, every version, named); identity leakage (booleans and sha256 prefixes only; an email count of 0 over every written file); BLIND: copies of the test data outside these keys.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="APPLY-Y75"><invocation>python -c "import json,subprocess as s,boto3;k=json.loads(s.check_output(['git','show','4bcebfcb09:org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_admit_keys_v3.json']));c=boto3.client('s3');print('VERSIONS_LEFT=%d'%sum(len([v for v in c.list_object_versions(Bucket=x['bucket'],Prefix=x['key']).get('Versions',[]) if v['Key']==x['key']]) for x in k['admit_keys'] if x['kind']=='s3'))"</invocation><expect>VERSIONS_LEFT=0</expect></criterion>
</proof_of_spec>
  AC1 counts versions of exactly the 2 named keys (never the wider prefix, which holds other uploads); the row also states the 7 DDB
  keys read NOT_FOUND after delete.

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the counts; per key EXISTS/NOT_FOUND before and NOT_FOUND after (opaque refs); the sweep count;
    each S3 version deleted (by version id) and the empty re-list; the email-shaped count (0); the time in UTC in the subject; the
    ledger entry; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
