<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-s21.silver-reader-role-laptop</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<round>21</round>
<workstream>readers-apply</workstream>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R21.md</decomp_doc>
<owned_cells>TR-a-21</owned_cells>
<decomp_context>Round 21 AMENDMENT 1, cell TR-a-21: FWD-5's silver-only reader role, built by TO-TR-r21 (drained @365a08577e), applied under the pair COO half @23251db022 + CTO half @91e314b74e. The laptop applies because dell2's identity does not administer the transcripts key; routed via 0.0.0_AB_MSTR~DELL2. a18's APPLY leg landed 09:55Z, so this is the CTO half's sequential branch.</decomp_context>
</decomp_ref>

  <objective>
    Apply FWD-5's silver-only reader role (`teams-global-transcripts-silver-reader-role`, name() output): a role, its policy and attachment, and
    ONE added key-policy statement `SilverReaderDecryptOnly`. Then prove it with three reads, reporting statuses only.
  </objective>

  <context>
    The pair binds, so read both halves first:
    - COO half: `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_SILVER_READER_20261009.md` @23251db022.
    - CTO half: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_FWD5_SILVER_READER_CTO_HALF.md` @91e314b74e.
    - Ruling row on research_meeting: D2-S13 @728d223ddc.
  </context>

  <the_act>
    0. Open a change ledger in org/critical_paths/change_management/ naming the pin (one carrying 365a08577e) and print the LIVE key policy's
       statement Sids (names only).
    1. `safe-apply` `infra/aws/terraform/transcripts` with `-target` on `aws_iam_role.silver_reader`, `aws_iam_policy.silver_reader`,
       `aws_iam_role_policy_attachment.silver_reader` and `aws_kms_key.transcripts`. The plan must show those 3 CREATES and ONE in-place key-policy
       update whose ONLY difference is the added `SilverReaderDecryptOnly` statement. Anything else = STOP, named. Print the key diff in full in
       the ledger.
    2. Proof, read by the Dell2 agent user assuming the new role (a raw-tier reader per the ruling); statuses only, no content:
       one Teams silver object (monday_meeting) -> 200; one Teams bronze object -> AccessDenied; one research_meeting silver object -> AccessDenied.
       Pick each key by listing as the agent user itself, never through the role.
    3. Close the ledger.
    ROLLBACK, if asked: re-apply the prior key policy (the before-image is in the ledger); destroying the three creates is Andrew's word.
  </the_act>

  <bounds>
    - Only those four targets; no other root, Lambda or principal. No transcript text in any file or message. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
    org/critical_paths/change_management/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule.
comp-iam: RUN -- a new role trusted by the three raw-tier readers (Andrew + the two Dell agent users; CTO ruling 3248), GetObject on two silver prefixes with research_meeting denied, plus ONE decrypt-only key statement via S3; the plan's key diff is checked in step 1.
comp-adversary: RUN -- traps: a key diff carrying a second change (a18 already live, so its principal must read unchanged), a typed ARN (none: derived in readers.tf), content in the proof (statuses only), a proof read made through the wrong identity; BLIND: Andrew's own read, which grades FWD-5 later.
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-a-21"><invocation>aws iam get-role --role-name teams-global-transcripts-silver-reader-role --query "Role.RoleName"</invocation><expect>"teams-global-transcripts-silver-reader-role"</expect></criterion>
</proof_of_spec>
  AC1's row also states the plan line, the full key diff, the three proof statuses and the ledger path.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2: the plan line; the key diff; the three statuses; the ledger path; commit hashes and the measured push state.
    Write the proof instance; leave the status flip to the issuer.
  </report>
</task_order>
