# TO D9_TAXSMA.TO-c1 — daily tracking (LAPTOP) — **WAIVED AHEAD OF THE MEETING, GATED ON THE GUARDRAIL TEST SET**

<task_order id="D9_TAXSMA.TO-c1" project="OPAL_TAXSMA">
<issued_to>0.7.0_AE_CloudOps (build + staging); 1.0.0_SA_CTO applies</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:15Z</issued>
<dated>available NOW -- the only (c)-leg released ahead of the Yang/Alyssa meeting</dated>
<status>staged -- GO paired. **HARD-GATED ON THE GUARDRAIL TEST SET CLOSING FIRST** (see below). Not gated on the meeting.</status>
<priority>P2 -- but the gate below is P0-class in consequence</priority>
<authority>D9_TAX_SMA_OPS_PRD.md §4.3 (c1) + the DONE definition as amended per CVO P1-1 @3ae19879fb, at dispatch vintage @fac13ccc3a. **WAIVER: Andrew-direct 2026-08-19 ~20:12Z ("All approved" on the COO /open-calls card 8) — build TOs otherwise hold for the meeting; (c1) is released ahead.** Records @1e0ec3b079 + @3c8c3f1035. Placement: LAPTOP-ONLY per D9's own split table (TF/safe-apply/deploy lanes) — D9's item-level sitez placement moves build labor, and apply-bearing legs route laptop by envelope law (CTO-confirmed).</authority>
</task_order>

## Objective
Finish PT2 multi-account (code + IAM staged per the record → **CTO applies**) + the WS-5 scheduled
trigger. This satisfies "track the assets daily."

## ⛔ THE GATE — READ THIS BEFORE ANYTHING ELSE. IT IS NOT A CHECKLIST ITEM.
**(c1) IS EXACTLY THE LEG THAT MAKES THIS CHAIN RUN DAILY AND UNATTENDED.** That is why the DONE
bar was amended: **this is the one bar in the entire D-set whose failure mode is UNAUTHORIZED TRADE
EXECUTION AGAINST CLIENT ACCOUNTS AT A CUSTODIAN.**

CVO's P1-1 found the original bar ("the guardrail is verifiably intact") was **satisfiable by a
design read**. It is now **TESTS THAT CAN FAIL**, run on **DEPLOYED BYTES** (Rule 22a CODE layer),
and **THE SET MUST CLOSE BEFORE (c1) SHIPS**:

1. **CREDENTIAL-ABSENCE SCAN OF THE DEPLOYED ARTIFACTS THEMSELVES.** **NEVER a repo grep** — a repo
   grep structurally cannot see what shipped. Download/inspect the deployed package.
2. **DEMONSTRATED NON-REACHABILITY** of any Schwab upload/execute call site **from the pipeline
   entry point.** Demonstrated, not asserted — show the reachability analysis and what would have
   made it fail.
3. **THE WORKFLOW MAP NAMES** the LAST automated step, the FIRST human step, and the HANDOFF
   ARTIFACT between them. A guardrail whose boundary nobody can name is not a guardrail.

**If any of the three cannot be closed, (c1) DOES NOT SHIP and that is the correct outcome** —
report it and stop. Shipping an unattended daily runner over an unproven guardrail is the one
failure here that is not recoverable by a rollback.

## Acceptance criteria
- **c1-1 GUARDRAIL TEST SET CLOSED, ALL THREE**, on deployed bytes, each shown as a test that could
  have failed.
- **c1-2 PT2 MULTI-ACCOUNT COMPLETE**; code + IAM staged per the record; **CTO applies** (Terraform
  only — never `aws lambda update-function-code`, never a bare `terraform apply`).
- **c1-3 WS-5 SCHEDULED TRIGGER LIVE** — a real **SCHEDULE**, visible in Terraform. A trigger whose
  only firing condition is another pipeline's success is not a schedule and does not satisfy this.
- **c1-4 EXERCISED GREEN ON 2 CONSECUTIVE DAYS** tracking all registry accounts (the DONE bar's own
  wording) — exercised, not a config read.
- **c1-5 IAM VERIFIED ON THE LIVE PRIMITIVE** for any new resource: one `--resource-arns` per call,
  positive control as a SEPARATE invocation, `--context-entries` for conditioned statements;
  `accessanalyzer validate-policy` (never `simulate-principal-policy`) for action-name validity.
- **c1-6 proof instance VALID rc=0 positional: ids c1-1..c1-6.** MEASURED/RULED-class run rows only;
  INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>c1-1,c1-2,c1-3,c1-4,c1-5,c1-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D9_TAXSMA.TO-c1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Do not ship ahead of the guardrail set. The waiver released (c1) from the MEETING gate — **it did
  not release it from the guardrail gate**, and conflating the two would be the most expensive
  misreading available here.
- Do not start (c2)-(c5). They still wait for the Yang/Alyssa meeting.
- No alert/monitor/notification machinery (standing moratorium). A SCHEDULE is not a monitor.

## Reporting
COO at guardrail-set-closed (report this BEFORE building further — it is the gate, and a late
report on it is worth nothing), and at exercised-green. cc CTO (applies + gate). Coordinate with
the site-Z D9 assessment seat: they are told to treat daily-tracking as IN-FLIGHT, not as a hole.
Session log w/ Compiler Tools section = deliverable.
