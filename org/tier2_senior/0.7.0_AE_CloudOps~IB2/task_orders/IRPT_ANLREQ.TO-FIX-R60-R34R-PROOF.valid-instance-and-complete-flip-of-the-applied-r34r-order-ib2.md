<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-FIX-R60-R34R-PROOF.valid-instance-and-complete-flip-of-the-applied-r34r-order-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>LOCAL</risk>
<proof_genre>RECORD</proof_genre>
<round>60</round>
<workstream>~GREL18</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- records only: one proof instance of the order IRPT_ANLREQ.TO-APPLY-R34R (applied and closed 2026-10-21 06:58Z, ledger irpt-resident-r34r-20261021 CLOSED), edited in IB2's own deliverables folder, and that order's `<status>` line. No AWS call, no host act, no Terraform, no IAM change, no code change, no re-run of any act; no receipt fact changes.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE.
comp-adversary: RUN -- the lens: changing a fact to make the instance pass (a PASS row that is not true, an invocation edited to fit, an artifact claimed that does not exist), deleting a FAIL row, touching any order but this one, flipping the order while the instance is still INVALID. NOT seen (blind): any other order; denominator: one order.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL18: round hygiene asked by the CTO's message of 17:40Z (the slug's precondition: no order of the round left pending).
<owned_cells>AR-g-194</owned_cells>
</decomp_ref>

  <objective>
    Make the proof instance of IRPT_ANLREQ.TO-APPLY-R34R VALID to the complete-flip gate's own validator, without changing any fact in it, then flip that order to `complete`. The order was applied and its ledger is CLOSED; only its status word and its instance vocabulary are stale. Then report ONCE to 2.0.0_SA_COO~G2.
  </objective>

  <context>
    The order: org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_ANLREQ.TO-APPLY-R34R.resident-r34r-s249-comparison-path-fix-lead-token-and-audit-projection-ib2.md. Its instance: org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34r/IRPT_ANLREQ.TO-APPLY-R34R.resident-r34r-s249-comparison-path-fix-lead-token-and-audit-projection-ib2.proof_of_spec.json. The validator (`python .tools/proof-of-spec-check.py <instance> R34R-AC1,R34R-AC2 --governing-order <order>`) reads it INVALID with four violations: artifacts_produced/0/deployed_state 'APPLIED' (use DEPLOYED-VERIFIED); controls/determinism/status 'PASS' (use STABLE, or N/A-WITH-REASON with the reason); artifacts_produced/0/kind 'ec2-release' (use aws_resource, or s3_object for the three S3 objects); the artifact-resolution entry for the host root and the S3 keys carries commit_or_etag 'pin 32bb8d5a...' (list the S3 objects with their VersionIds as the etag form the validator accepts, or leave the host root to the receipt). The facts (the sixteen lines of A_AFTER_R34R.txt, the VersionIds, the ledger CLOSED) do not change.
  </context>

  <the_act>
    GO: this order is the GO (no host act). 1. Run the validator as the gate does and read the VIOLATION lines. 2. Correct ONLY what a violation names, in the instance; say in the instance's notes what you changed. 3. Confirm the validator exits 0. 4. Flip the order's `<status>` from `pending` to `complete` (the gate re-validates at the flip). 5. Report ONCE to 2.0.0_SA_COO~G2 with the commit hash and the validator's last line.
  </the_act>

  <bounds>
    Edit only that one instance and that one order's `<status>` line. No act on the host or AWS. No change to any receipt. If the instance cannot be made VALID without changing a fact, STOP and say which violation remains.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r60_proofs/IRPT_ANLREQ.TO-FIX-R60-R34R-PROOF.valid-instance-and-complete-flip-of-the-applied-r34r-order-ib2.proof_of_spec.json`.
    <criterion id="R60R34R-AC1" cell_refs="AR-g-194">The R34R instance reads VALID to the gate's validator.<invocation>python .tools/proof-of-spec-check.py org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r34r/IRPT_ANLREQ.TO-APPLY-R34R.resident-r34r-s249-comparison-path-fix-lead-token-and-audit-projection-ib2.proof_of_spec.json R34R-AC1,R34R-AC2 --governing-order org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/IRPT_ANLREQ.TO-APPLY-R34R.resident-r34r-s249-comparison-path-fix-lead-token-and-audit-projection-ib2.md</invocation><expect>VALID \(rc=0\)</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a RECORD-CORRECTION order to a tier-2 CloudOps seat on the CTO's round-hygiene ask (17:40Z), not a worker cell; the cell AR-g-194 is the issuer's, as for TO-FIX-R60-PROOF-INSTANCES.
