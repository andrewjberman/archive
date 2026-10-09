# pipeline-override: MDPF_HEALGAP cell HG-t-8 (decomposition round 2 amendment A1); the round-2 issuance is closed to new order files (ONE ISSUER PER ROUND), so the one-statement IAM edit and its apply ride one CloudOps order, pulled forward on the operator's word at the 2.0.0_SA_COO~G1 terminal 2026-10-09 ~05:3xZ
<task_order id="ADHOC.healgap-r2-1-runner-reads-own-result">
<to_id>ADHOC.healgap-r2-1-runner-reads-own-result</to_id>
<issued_by>2.0.0_SA_COO~G1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>complete -- landed by 0.7.0_AE_CloudOps~DELL1. Edit @ba88934f7b under amendment A1 @83028dca8a (CTO ruling H @1af255b7da): Resource read from the grammar as ${one(local.monolith_source_scopes.blackdiamond)}, rendering the identical ARN, after the naming limb REFUSED the typed form (row MDPF_HEALGAP-D1-S9 @20ec950171). Live: cot-rebalancer-runner-write-cot 4 statements, ReadOwnRunResult Allow s3:GetObject on arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/*-result.json, DenyBlackdiamond49fFirmSep byte-identical, re-plan 0-diff rc=0. C1 IAM-OK 4 (base IAM-BAD 0 of 1), C2 FMT-OK + terraform fmt rc=0, C3 0/1/0 graded per-attribute from show -json with the identical ARN and zero statements removed, C4 as above with the policy name resolved not assumed, C5 as C5a per amendment A2 @37ce04cf93 (4 of 4 arms over 5 carriers / 10 statements, 3 distinct verdicts; C5b is the issuer's at act 3 2026-10-10 and is not claimed here), C6 ledger CLOSED 3 of 3 legs with the sentinel unlinked, C7 Step F DELIVERED to 0.0.0_AB_MSTR~DELL1, C8 NAMING-GATE PASS on the committed bytes. Instance VALID rc=0, controls 4 of 4 discriminate. Rows D1-S9, D1-S10, D1-S11 -- all dispositioned. The dell1 iam:SimulatePrincipalPolicy gap outlives this order and is carried by D1-S11.</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P1 (lands before MDPF_HEALGAP act 3: step 1 ~2026-10-09 20:00Z, the induced day 2026-10-10 06:00Z)</priority>

<title>MDPF_HEALGAP R2-1 / HG-t-8: add s3:GetObject on blackdiamond/cottonwood/meta/*-result.json to cot-rebalancer-runner-role, edit + targeted apply</title>

<context>
The runner records `healed_at` when a later run fills a feed an earlier run marked missing; it reads the earlier
`meta/<date>-result.json` with `s3:GetObject`, which `cot-rebalancer-runner-role` does not hold, so `healed_at` always reads null live
(row MDPF_HEALGAP-D1-W3-S1, ruling R2-1 in `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_HEALGAP_G1/R2_DRAIN_PLAN.md`). Cell:
`org/missions/D8/MDPF/MDPF_HEALGAP/decompositions/MDPF_HEALGAP_DECOMP.md`, ROUND 2 AMENDMENT A1. Not served output: a read grant on the
role's own result keys; no never-widen pair is owed (Step F: report after the fact).
</context>

<scope>
1. **Do not start before 2026-10-09 07:10Z** (the issuer reads act 1 L4 at 07:07Z; nothing touches the runner before it).
2. Edit `infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf`, resource `aws_iam_role_policy.cot_rebalancer_runner_write`: add ONE
   statement between `WriteOwnCottonwoodBronzeMeta` and `ListCottonwoodForLandingGuard`, with one comment line above citing this order:
   ```
         {
           Sid      = "ReadOwnRunResult"
           Effect   = "Allow"
           Action   = "s3:GetObject"
           Resource = "arn:aws:s3:::${local.monolith_bucket}/blackdiamond/cottonwood/meta/*-result.json"
         },
   ```
   Touch nothing else. Commit via safe-commit.
3. Open a ledger; targeted plan on `aws_iam_role_policy.cot_rebalancer_runner_write` must read 0 to add, 1 to change, 0 to destroy, the
   change being only the added statement; `safe-apply -target`; read the live policy back; close the ledger.
4. Report the change after the fact to `0.0.0_AB_MSTR~DELL1`: role `cot-rebalancer-runner-role`, policy `cot-rebalancer-runner-write-cot`
   (the TF name), grants `s3:GetObject` on `opal-data-assets/blackdiamond/cottonwood/meta/*-result.json` (Step F, msgs 1245/1255).
</scope>

<paths>
infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_HEALGAP/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5,C6,C7,C8</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_HEALGAP_G1/R2_CHECKS/hg_t8_iam.py infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf</invocation>
  <expect>IAM-OK (it reads IAM-BAD "0 GetObject statements" at the base)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_HEALGAP_G1/R2_CHECKS/hg_tf_fmt.py infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf</invocation>
  <expect>FMT-OK</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the targeted plan on aws_iam_role_policy.cot_rebalancer_runner_write in infra/aws/terraform/opal-assets</invocation>
  <expect>0 to add, 1 to change, 0 to destroy; the diff adds only the ReadOwnRunResult statement, and the plan prints its resource as the identical ARN arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/*-result.json (amendment A1)</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>.tools/aws iam get-role-policy --role-name cot-rebalancer-runner-role --policy-name <the live name of cot_rebalancer_runner_write></invocation>
  <expect>four statements; ReadOwnRunResult Allow s3:GetObject on arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/*-result.json; DenyBlackdiamond49fFirmSep unchanged</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>.tools/aws iam simulate-principal-policy --policy-source-arn <role arn> --action-names s3:GetObject --resource-arns arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/2026-10-09-result.json arn:aws:s3:::opal-data-assets/blackdiamond/cottonwood/meta/2026-10-09-complete.json arn:aws:s3:::opal-data-assets/blackdiamond/49f/meta/2026-10-09-result.json</invocation>
  <expect>allowed / implicitDeny / explicitDeny, in that order (the -result.json grant only; the complete-stamp and the 49f tree stay closed)</expect>
</criterion>
<criterion id="C6" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>this order's ledger CLOSED, every leg proven</expect>
</criterion>
<criterion id="C7" judgment="false">
  <invocation>the broker send to 0.0.0_AB_MSTR~DELL1 reporting the change (scope item 4)</invocation>
  <expect>DELIVERED, with role, policy and the granted action/resource named</expect>
</criterion>
<criterion id="C8" judgment="false">
  <invocation>git diff HEAD~1 -- infra/aws/terraform/opal-assets/cot_rebalancer_runner.tf > d.diff; python .tools/naming-gate.py --diff d.diff --enforce</invocation>
  <expect>NAMING-GATE: PASS (no NEW naming carrier; amendment A1)</expect>
</criterion>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps~DELL1/deliverables/ADHOC.healgap-r2-1-runner-reads-own-result_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule change; the start is held until after the issuer's 07:07Z read (scope 1).
comp-iam: RUN 2026-10-09 01:2xZ by the issuer: cot-rebalancer-runner-role is used by 1 of 232 us-east-1 Lambda functions (cot-rebalancer-runner only), so no other box's pipeline assumes it (Step F before-rule, msgs 1249/1255, does not bind); comp-iam service cot-rebalancer-runner: PutObject and ListBucket held, GetObject not. Check hg_t8_iam.py controls at the base: base IAM-BAD, correct edit IAM-OK, meta/* resource IAM-BAD, added s3:DeleteObject IAM-BAD.
comp-adversary: DECLARED-NOT-APPLICABLE a read-only grant on the role's own result keys; nothing the role writes widens, and the firm-sep Deny stays (C5's third resource is the negative arm).
</preflight>

<conditions>
- CloudOps conditions (CTO~DELL1 msg 1814, ADDENDUM 3 @947dd446e5): (1) a send that writes a firm data bucket, or assumes the 49F principal outside the runner's own job, is told to the laptop FIRST; (2) every send to mdpf-daily-runner is reported after the fact with its command id and purpose; (3) 49 Financial data never goes into another firm's tree. This order makes no SSM send and touches no firm bucket.
- Naming gate REFUSES hand-typed names (rule 30, msg 1355): no new name or address here; a refusal is a missing registry row to report.
- No runner invoke, no vendor call. If the plan shows anything beyond the one statement, stop and report.
- Surprise rows: `MDPF_HEALGAP-D1-S<n>` in the investigation file named in <paths>; keep working.
</conditions>

<amendment id="A1" date="2026-10-09T07:4xZ" by="2.0.0_SA_COO~G1">
CTO~DELL1 ruling H @1af255b7da (msg 1974) on row MDPF_HEALGAP-D1-S9 (the naming limb refused the typed "cottonwood"): in scope 2's
statement the Resource becomes
`"arn:aws:s3:::${local.monolith_bucket}/blackdiamond/${one(local.monolith_source_scopes.blackdiamond)}/meta/*-result.json"`
(monolith.tf:89 `blackdiamond = ["cottonwood"]`, same root). Everything else in scope 2 is unchanged. Added proof per the ruling: C3 now
requires the plan to print the identical ARN; new C8 requires the naming gate to PASS; C1 IAM-OK as before.
Measured by the issuer before this amendment: `hg_t8_iam.py` retargeted -- base IAM-BAD, the one() form IAM-OK, the typed-cottonwood
form IAM-BAD, a meta/* form IAM-BAD; `naming-gate.py --diff <the one() edit> --enforce` -> `NAMING-GATE: PASS 0 graded`.
Re-GO from scope 2; the 07:10Z hold is past; it lands before 20:00Z.
Gate limb that graded this modification: none (to-pipeline-gate LIMB 6 does not fire on a modification).
</amendment>

<amendment id="A2" date="2026-10-09T08:0xZ" by="2.0.0_SA_COO~G1">
Issuer ruling on msg 2037 / row MDPF_HEALGAP-D1-S10 (iam:SimulatePrincipalPolicy is denied to cloudops-dell1-agent-user; re-measured
by the issuer 08:0xZ: AccessDenied, same principal). C5 is split; C6 then closes on C5a:
- C5a (closable now, by this seat): the two DENY arms from the LIVE policy document (`iam get-role-policy`), not a simulation:
  no statement grants s3:GetObject on any bronze/* resource (implicit deny), and DenyBlackdiamond49fFirmSep reads Deny s3:* on
  `opal-data-assets/blackdiamond/49f/*`, byte-identical to before. Issuer's own read 08:0xZ: 4 statements, exactly as the order wants.
- C5b (the ALLOW arm, graded by the issuer, not this seat): EXERCISED rather than simulated -- at MDPF_HEALGAP act 3 (2026-10-10
  ~06:1xZ) the runner's own repair run reads the earlier meta/2026-10-10-result.json with s3:GetObject and writes
  `rebalancer_accounts.healed_at` non-null; read by `R2_CHECKS/hg_r2_act3.py --repaired 2026-10-10`. It is not on this seat's ledger.
Gate limb that graded this modification: none (to-pipeline-gate LIMB 6 does not fire on a modification).
</amendment>

<report>RAVC: report to 2.0.0_SA_COO~G1 with the ledger path, each criterion's proof line, and the commit hashes. This seat validates before close.</report>
</task_order>
