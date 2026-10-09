<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-ka21.gateway-key-write-laptop</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TRL</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<round>21</round>
<workstream>keys-apply</workstream>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R21.md</decomp_doc>
<owned_cells>TR-ka-21</owned_cells>
<decomp_context>Round 21 AMENDMENT 3, cell TR-ka-21: the gateway role's WRITE under the transcripts key, built by TO-TR-k21 (drained @b74b1e45bd), under the pair COO half @6791d6ebc2 + CTO half @ad98587dfa. Site Z's FWD-6 .pptx copy (OG-ab-2, ruling @14cbf27dec) needs it.</decomp_context>
</decomp_ref>

  <objective>
    Add ONE statement, `GatewayWritesTranscripts`, to the transcripts key policy, after confirming site Z's S3 grant to the gateway role is
    PutObject on the market-update prefix only. Report statuses and statement ids only.
  </objective>

  <context>
    The pair binds, so read both halves first:
    - COO half: `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_GATEWAY_KEY_WRITE_20261009.md` @6791d6ebc2.
    - CTO half: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_GATEWAY_KEY_WRITE_TR_ka_21_CTO_HALF.md` @ad98587dfa.
    The bucket's Bucket Key is ON (issuer read, 2026-10-09 ~15:5xZ: `get-bucket-encryption` BucketKeyEnabled=True). So the CTO half's
    Bucket-Key branch governs: the key condition cannot narrow below the bucket, and the prefix boundary is site Z's S3 grant.
  </context>

  <the_act>
    0. Open a change ledger naming the pin (one carrying b74b1e45bd) and print the LIVE key policy's statement Sids. Six are expected after
       this act; five are live now.
    1. PRECONDITION (the CTO half's Bucket-Key branch): read every IAM policy attached to the gateway role (resolve it the way main.tf does:
       the opal-gateway root's `instance_role_name` output). Print each statement that grants an S3 write on `opal-data-transcripts`. It must
       be `s3:PutObject` on `opal-data-transcripts/sharepoint/transcripts/bronze/market_update/*` ONLY. That prefix is
       `lib/opal_naming.py address('sharepoint','transcripts','bronze','market_update', ...)` output. Any wider grant, or a write anywhere else
       in that bucket = STOP, named. NO grant yet is also a pass: the key statement alone writes nothing. Record which case held.
    2. `safe-apply` `infra/aws/terraform/transcripts` with `-target` `aws_kms_key.transcripts`. The plan must show ONE in-place update whose
       only difference is the added `GatewayWritesTranscripts`; the other five statements are unchanged. Anything else = STOP. Print the key
       diff in full in the ledger.
    3. After: re-read the Sids (six) and print `GatewayWritesTranscripts`'s two conditions. Close the ledger.
    ROLLBACK, if asked: re-apply the prior key policy (its before-image is in the ledger).
  </the_act>

  <bounds>
    - The key policy only; no role, bucket policy or other root. No delete. No content.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~TRL/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~TRL/logs/
    org/critical_paths/change_management/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule.
comp-iam: RUN -- a NEW writer on the transcripts key (GenerateDataKey + Encrypt via S3 to this bucket); with Bucket Key ON the prefix boundary is the gateway role's S3 grant, read in step 1; no decrypt is granted.
comp-adversary: RUN -- traps: a plan that rewrites another statement (s21/a18/Dell must hold), a gateway S3 grant wider than market_update (STOP), a typed ARN (none: data source), content in the ledger (ids and statuses only); BLIND: site Z's later landing of the deck, which is OG-ab-2's.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-ka-21"><invocation>python -c "import boto3,json;s3=boto3.client('s3');k=s3.get_bucket_encryption(Bucket='opal-data-transcripts')['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['KMSMasterKeyID'];print('GatewayWritesTranscripts' in [x.get('Sid') for x in json.loads(boto3.client('kms').get_key_policy(KeyId=k,PolicyName='default')['Policy'])['Statement']])"</invocation><expect>True</expect></criterion>
</proof_of_spec>
  AC1's row also states the step-1 case, the plan line, the key diff, and the ledger path.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the step-1 case; the plan line; the key diff (Sids); the ledger path; commits and the measured push state.
    Write the proof instance beside this order; leave the status flip to the issuer.
  </report>
</task_order>
