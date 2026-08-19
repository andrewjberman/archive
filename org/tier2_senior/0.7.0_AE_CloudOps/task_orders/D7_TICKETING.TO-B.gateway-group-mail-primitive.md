# TO D7_TICKETING.TO-B — the gateway group-mail primitive (LAPTOP, EC2 deploy lane; scope may COLLAPSE on TO-A's on-box read)

<task_order id="D7_TICKETING.TO-B" project="OPAL_TICKETING">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:15Z</issued>
<dated>on TO-A's outputs (the on-box capability read + Andrew's Q3 one-liner reply) — likely 08-20/21; behind your Friday-path rows at your discretion</dated>
<status>staged -- GO paired; STAGED-ON-TO-A: do not build before the existence check lands (the scope-collapse rule is the point)</status>
<priority>P1-program (D7 is the week's flagship per Andrew -- "water through the pipes") but behind your 49F Friday rows at the seat</priority>
<authority>D7_TICKETING_INTAKE_PRD.md §TO-B at dispatch vintage @36a7fbd70e (CVO verdict + 2 protocol rulings absorbed); Andrew's four ticketing positions (internal-only v1; placement FINAL; 2PM-ET stands; bobby later). CTO gates the deploy.</authority>
</task_order>

## Objective
Extend the opal-gateway app (PRD 4.1) with the DL/group-mail read primitive + identity_scope entry;
deploy via safe-ec2-deploy.sh; behavior-exercise per the R7 ledger pattern (deny + serve + cursor
advance). **THE EXISTENCE CHECK IS TO-A's ON-BOX CAPABILITY READ (protocol §6 fourth form), NOT R8
alone** — the deployed app is not repo-resident, so if it already carries a group-mail read path,
this TO COLLAPSES to expose-and-wire per §6's scope-collapse rule; declare which shape you build in
your first report. Design carries durable OFF-BOX cursor persistence (receipt-vs-tickets derivable;
ticket DDB config item = the natural home, final call at design).

## Acceptance criteria
- TB-1 SHAPE DECLARED: build-vs-collapse decided FROM TO-A's on-box read, cited (never from R8's
  repo proxy alone).
- TB-2 PRIMITIVE LIVE: the read path serves the confirmed DL set (Q3 closure cited), identity_scope
  entry landed, deployed via safe-ec2-deploy.sh under CTO's gate.
- TB-3 BEHAVIOR-EXERCISED per R7: deny (out-of-scope caller) + serve (in-scope) + cursor advance,
  each printed; the cursor persists OFF-BOX and receipt-vs-tickets is derivable after the fact.
- TB-4 proof instance VALID rc=0 positional: ids TB-1,TB-2,TB-3,TB-4. Expected values cite only
  MEASURED/RULED-class run rows per the protocol's run-verdict vocabulary (INFERRED-class rows are
  mechanically ineligible).

<proof_of_spec>
  <expected_criteria>TB-1,TB-2,TB-3,TB-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D7_TICKETING.TO-B_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No build before TO-A's read (staged-on means staged-on). No alert machinery (the production
  trigger question is TO-C's exit, a SCHEDULE decision). v1 stays internal-only.

## Reporting
COO (cc CTO gate, MSTR for the sitez seam) at shape-declared and at primitive-live. Surprise
channel: one banked line to COO. Session log with Compiler Tools section = deliverable.
