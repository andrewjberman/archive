<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-GUARD-1.stale-benchmark-guard</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~RV</issued_to>
    <date>2026-10-06</date>
    <status>complete -- issuer-verified 2026-10-06 ~16:3xZ: live CodeSha256 FLFjTpvI... (= artifact from 513b25f522); served comprehensive key VersionId Qbef40yV... reads 273 null / 27 number of 300 benchmark cells (27 = INT etf); record @49103d5f96; NEVER-2 closed</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>WORLD</risk>
# pipeline-override: outside the canonical pipeline -- a seat act on a closed project (OPAL_BBGTML), bounded by a signed never-widen pair (COO @1253afc83c, CTO @78a9e8a39e) on CTO~Z's fix route @5e0c045e8d; the order is the LD-0529 carrier for the GO, not a round

  <objective>
    Stop yang-model-portfolio-benchmarks from serving wrong benchmark numbers. A benchmark series whose last bar is before
    data_as_of serves null on every period and carries benchmark_last_date. This is track 1 of 1.0.0_SA_CTO~Z's fix route
    (Andrew-direct singular priority, msg 30062).
  </objective>

  <context>
    The act is bounded by a never-widen pair. Both halves are SIGNED, and they are the whole spec. Read both in full before
    you act:
    - COO half: org/tier1_exec/2.0.0_SA_COO~Z/deliverables/NEVER_WIDEN_HALF_COO_BENCHMARK_GUARD_20261006.md @1253afc83c
      (the three legs, the base and the rollback per key).
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_BENCHMARK_GUARD_20261006.md @78a9e8a39e
      (section 3 is the cell-level grade; section 4 lists the five conditions of the signature).
    - Route: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_INDEX_BENCHMARK_FIX_ROUTE_20261006.md (ADDENDUM 2 @2d56ec90e9).
    OPAL_BBGTML reads status closed; this order exists so the act has a task-order carrier (LD-0529). It opens no round.
  </context>

  <paths>
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/test_stale_benchmark_guard.py
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/org/critical_paths/.open_deploys/ (one NEVER-2 entry for this act)
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/org/critical_paths/change_management/ (the ledger entry for this act)
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/ (the grade record)
  </paths>

  <acceptance_criteria>
    <criterion id="AC1">The plant test passes 3 of 3 BEFORE any deploy act. Run: python -m pytest
      infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/test_stale_benchmark_guard.py -q.
      Expect: 3 passed.</criterion>
    <criterion id="AC2">The deploy moved the bytes. Run safe-apply on infra/aws/terraform/yang-pipeline with an UNTARGETED plan
      (only this function's code, archive or hash may change, or STOP). Then run aws lambda get-function-configuration
      --function-name yang-model-portfolio-benchmarks --query CodeSha256. Expect: it differs from
      dHTjheKzauUziiPc6Jkwn7Ys+C36Xb5KS0aAWPh7Th8= and equals the hash of the artifact built from the code-leg commit.</criterion>
    <criterion id="AC3">The served output grades as the CTO half's section 3 says. Re-read the served data_as_of immediately
      before leg 3, and apply CTO section 4 condition 3 to both branches. Expect on the comprehensive key: 273 null and 27
      numbers byte-equal to the base, out of 300 benchmark cells. Expect the 100 model cells equal to the base, and the
      legacy-key partition printed with its denominator. Any failed row triggers the rollback in CTO section 4 condition 4.</criterion>
  </acceptance_criteria>

<proof_of_spec>
  <criterion id="AC1" cell_refs="GUARD-1"><invocation>python -m pytest infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/test_stale_benchmark_guard.py -q</invocation><expect>3 passed</expect></criterion>
  <criterion id="AC2" cell_refs="GUARD-1"><invocation>.tools/aws lambda get-function-configuration --function-name yang-model-portfolio-benchmarks --query CodeSha256 --output text</invocation><expect>not dHTjheKzauUziiPc6Jkwn7Ys+C36Xb5KS0aAWPh7Th8= and equal to the built artifact's hash</expect></criterion>
  <criterion id="AC3" cell_refs="GUARD-1"><invocation>python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/benchmark_guard_grade.py</invocation><expect>GRADE: PASS -- comprehensive 273 null / 27 byte-equal of 300; model 100/100 equal; legacy partition printed with denominator</expect></criterion>
</proof_of_spec>

  <gates>
    Commit with .tools/safe-commit.sh under your own author line. Build the deploy artifact at an EXACT commit that carries only
    the code leg's two files. Open the NEVER-2 entry before the deploy leg, and close it after AC3 is graded and printed. No
    force_publish. A stray legacy-key version from the dormant smartx exporter is a surprise row, not a rollback trigger
    (CTO section 2).
  </gates>

  <report>
    Report once to 2.0.0_SA_COO~Z: each criterion's verdict with the output above it, the commit hashes and push state, and
    the NEVER-2 entry path and its close. Leave the status flip to the issuer.
  </report>
</task_order>
