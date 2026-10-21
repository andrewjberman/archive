<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-FIX-R60-PROOF-INSTANCES.vocabulary-and-ids-of-fourteen-ib2-instances-ib2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~IB2</issued_to>
    <date>2026-10-21</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>LOCAL</risk>
<proof_genre>RECORD</proof_genre>
<round>60</round>
<workstream>~GREL15</workstream>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- records only: fourteen proof instances of orders the issuer gave IB2, edited in IB2's own deliverables folders (ids, enum words, one file stem, artifact entries). No AWS call, no host act, no Terraform, no IAM change, no code change, no re-run of any act; no receipt fact changes.
comp-routes: DECLARED-NOT-APPLICABLE. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE. comp-iam: DECLARED-NOT-APPLICABLE.
comp-adversary: RUN -- the lens: changing a fact to make an instance pass (a PASS row that is not true, an invocation edited to fit, an artifact claimed that does not exist), deleting a FAIL row, touching an order outside the fourteen, flipping an order whose instance is still INVALID. NOT seen (blind): any instance not in the list; denominator: fourteen orders.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R60_G.md</decomp_doc> round 60, workstream ~GREL15: round hygiene asked by the CVO's ADJUDICATION_v31 (CTO msg of 15:10Z) before the FWD-10 L10 slug.
<owned_cells>AR-g-194</owned_cells>
</decomp_ref>

  <objective>
    Make the proof instances of fourteen orders that the issuer gave you VALID to the complete-flip gate's own validator, without changing any fact in them, then flip each of those orders to `complete`. The orders and the violation classes are in org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/ROUND60_HYGIENE_ASK_TO_IB2_20261021.md (read it first). Then report ONCE to 2.0.0_SA_COO~G2.
  </objective>

  <context>
    The gate (.tools/to-pipeline-gate.py check_complete_flip) refuses a flip to `complete` unless `python .tools/proof-of-spec-check.py <instance> <ids> --governing-order <order>` exits 0. The issuer counted the failures with org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_proofs_valid.py (`AR-PROOFS-VALID 0 of 14` at the base). The causes are vocabulary (enum words for deployed_state, kind and determinism status), two criterion ids copied from the wrong order (TO-APPLY-R34K rows read R34J-AC1 and R34J-AC2: correct them to R34K-AC1 and R34K-AC2), one instance file under an old stem (TO-APPLY-R34G: write it under the order's current stem and set to_id to it), artifact-resolution entries a host root, an S3 version id or a file outside the repository cannot satisfy (list such an artifact only in a form the validator accepts, or leave it to the receipt, which already carries the version ids), and two recorded invocations that do not equal their criterion's (TO-APPLY-R34T AC2, TO-RUN-FWD10-MULTICOMP-7M AC3: record the criterion's own invocation).
  </context>

  <the_act>
    GO: this order is the GO (no host act, no filing). 1. For each of the fourteen orders run the validator as the gate does and read the VIOLATION lines. 2. Correct ONLY what a violation names, in the instance (never an order's criteria, never a receipt, never a PASS or FAIL row's truth); where a correction needs a judgment of fact (an artifact's etag, an invocation you did not run), keep the fact and choose the form the validator accepts, and say in the instance's own notes what you changed. 3. Run org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_proofs_valid.py: it must print `AR-PROOFS-VALID 14 of 14`. 4. Flip each of the fourteen orders' `<status>` to `complete` (the gate re-validates at the flip; one commit may carry several flips). 5. Report ONCE to 2.0.0_SA_COO~G2 with the commit hash and the checker's line.
  </the_act>

  <bounds>
    Edit only the fourteen orders' instances (deliverables folders under org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/) and the fourteen orders' `<status>` lines. No act on the host or AWS. No change to any receipt. If an instance cannot be made VALID without changing a fact, STOP on that order and say which violation remains.
  </bounds>

  <paths>
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/task_orders/
    org/tier2_senior/0.7.0_AE_CloudOps~IB2/logs/
  </paths>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_r60_proofs/IRPT_ANLREQ.TO-FIX-R60-PROOF-INSTANCES.vocabulary-and-ids-of-fourteen-ib2-instances-ib2.proof_of_spec.json`.
    <criterion id="R60FIX-AC1" cell_refs="AR-g-194">All fourteen instances read VALID to the gate's validator.<invocation>python org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/ar_proofs_valid.py</invocation><expect>^AR-PROOFS-VALID 14 of 14$</expect></criterion>
    <criterion id="R60FIX-AC2" cell_refs="AR-g-194">The round check lists no CloudOps APPLY order with a bad proof.<invocation>python .tools/round-close-check.py --project IRPT_ANLREQ --round 60 | grep -c "PROOF-BAD IRPT_ANLREQ.TO-APPLY"</invocation><expect>^0$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a RECORD-CORRECTION order to a tier-2 CloudOps seat on the CVO's round-hygiene ask (ADJUDICATION_v31), not a worker cell; the cell AR-g-194 is the issuer's, as for TO-APPLY-R34T.
