<task_order>
  <metadata>
    <id>NFRA_TRNSPT.TO-APPLY-a18.second-reader-role-laptop</id>
    <issued_by>2.0.0_SA_COO~T2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TRL</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_TRNSPT</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D9/NFRA/NFRA_TRNSPT/decompositions/NFRA_TRNSPT_DECOMP_R18.md</decomp_doc>
<owned_cells>TR-a-18</owned_cells>
<decomp_context>dell2's round 18 (box/dell2; reaches the laptop tree at the next box pass): "TR-a-18 | FWD-8 apply: the pair on TR-p-18's bytes, then the apply by the laptop (IAM identity) routed through MSTR". Built @f8c4859407. Routed via 0.0.0_AB_MSTR~DELL2 because dell2's identity does not administer the transcripts key.</decomp_context>
</decomp_ref>

  <reassignment>
    AMENDMENT (issuer, 2026-10-09 ~14:2xZ; UB-953b fold @88141ce237; laptop 2.0.0_SA_COO~C via 0.0.0_AB_MSTR~DELL2 msg 3434): the VERIFY
    leg is RELOCATED to 0.7.0_AE_CloudOps~TRL (the laptop base 0.7.0_AE_CloudOps is deaf since ~09:29Z). The APPLY leg landed 2026-10-09
    09:55Z (ledger nfra-trnspt-a18-second-reader-laptop-20261009: 3 added, 1 changed). ~TRL runs ONLY the open VERIFY leg as the ledger names
    it -- role read-back, the full key-policy diff, the admitted/refused S3 proof with statuses only -- and closes that ledger. The key policy
    now also carries SilverReaderDecryptOnly (TO-APPLY-s21, 14:07Z); that statement is s21's, not a18's, and is read as such.
  </reassignment>

  <objective>
    Apply FWD-8's second named reader: one IAM role (`teams-global-transcripts-second-reader-role`, name() output) that `Opal_Terminal` may
    assume, read-only on `opal-data-transcripts`, plus ONE added principal in the transcripts key policy's `NamedReadersUseTheKey`. Then prove
    the reader set: the named role admitted, an unnamed principal refused. Statuses only.
  </objective>

  <context>
    The pair binds; read both halves: COO half `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/NEVER_WIDEN_NFRA_TRNSPT_COO_HALF_SECOND_READER_20261009.md`
    (@056809859f) and CTO half `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_FWD8_SECOND_READER_CTO_HALF.md`
    (@f2ec32dea4). Trust principal, measured by the issuer 08:4xZ and named by the CTO: `arn:aws:iam::313476888478:user/Opal_Terminal`
    (tags purpose=bloomberg-terminal-device, created_by=parity-with-Andrew_Berman). Andrew's named accounts (2026-09-29): andrew@opalinvest.com and
    opalbloomberg@opalinvest.com.
  </context>

  <the_act>
    0. Open a change ledger in org/critical_paths/change_management/ naming the pin (a commit carrying f8c4859407).
    1. safe-apply `infra/aws/terraform/transcripts` with `-var second_reader_trust_principal_arns=["arn:aws:iam::313476888478:user/Opal_Terminal"]`
       and `-target` on `aws_iam_role.second_reader`, `aws_iam_policy.second_reader`, their attachment, and `aws_kms_key.transcripts`. The plan
       shows exactly three CREATES and ONE in-place key-policy update whose ONLY difference is the added role in `NamedReadersUseTheKey`; print
       the full key-policy diff in the ledger. Any other line (notably the shared-zip Lambdas) = STOP.
    2. Proof (CTO half): as the new role (assumed from Opal_Terminal), GetObject one transcripts key = ADMITTED; as an unnamed dell2 role,
       GetObject the same key = REFUSED. Statuses only; no object content kept or printed.
    3. Close the ledger. ROLLBACK, if asked: re-apply the prior key policy from the ledger's before-image; the role's destroy is Andrew's word.
  </the_act>

  <bounds>
    - Exactly the targeted resources; no other statement of the key policy moves. No content in any file or message. No delete.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
    org/critical_paths/change_management/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an identity grant; no schedule.
comp-iam: RUN -- the key policy's six statements read at f8c4859407 (one gains a principal); the new role's policy (GetObject on the bucket's objects, ListBucket on the bucket); trust = Opal_Terminal only.
comp-adversary: RUN -- a wider key-policy diff (printed in full, one-principal only); the shared-zip Lambdas drifting into the plan (-target, STOP); a content leak in the proof (statuses only); BLIND: Opal_Terminal's own policies (the laptop reads them before step 2 and names any that already reach the bucket).
lane: the applier's deliverables, logs and the change ledger.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="TR-a-18"><invocation>aws iam get-role --role-name teams-global-transcripts-second-reader-role --query "Role.RoleName"</invocation><expect>"teams-global-transcripts-second-reader-role"</expect></criterion>
</proof_of_spec>
  AC1's row also states the key-policy diff (one principal), the ADMITTED and REFUSED statuses and the ledger path.

  <report>
    Report ONCE to 2.0.0_SA_COO~T2 through 0.0.0_AB_MSTR~DELL2, as a FILE: the plan line, the key-policy diff, the two proof statuses, the ledger
    path, commit hashes. Leave the status flip to the issuer.
  </report>
</task_order>
