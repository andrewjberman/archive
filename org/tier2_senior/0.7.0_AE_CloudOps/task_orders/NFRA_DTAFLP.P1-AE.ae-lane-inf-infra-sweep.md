<to_id>NFRA_DTAFLP.P1-AE</to_id>
<project>NFRA_DTAFLP</project>
<title>P1 AE-lane §8 infra sweep: data/orion->data/inf in 31 owned-paths-blocked files (inf-pipeline Lambdas 24 + ec2 inf-runners + split-form orchestrator:327) + redeploy</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (DS P1-DS RAVC2 cross-lane routing 924bc6c22, 162016Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>complete -- LANDED (46d0b98ae: §8 AE-lane infra provenance sweep data/orion->data/inf, bundled-Lambda 24 + ec2 inf-* 7, git-side VERIFIED 0-residual per /drive log a1abe90f0). Ground-truth verified by COO 2026-06-11 ~1946Z (data/orion GONE). The cross-lane infra remainder DS routed to AE (owned-paths CLOUD_OPS_OR_ETL/SHARED_OPAL_ETL) is swept. Board <status> was lagged (read active); trued up by COO under full-send true-up. KNOWN residuals (sweep-completeness fix-legs, dispatched 2026-06-11 ~1949Z, do NOT reopen the mv): (1) 5 data/inf/manual_api/* files still hardcode data/orion/ -> dangling post-mv; routed to AE to fold into the pre-existing manual_api comp-constants debt (low-pri, not in gold chain, not deployed). (2) DAG-builder catalog residual surfaced by AE~B during D5 verify: build_inf_gold_dag's orion-gold-dispatch.sh catalog-discovery + test_multi_pipeline.py expectation missed the rename -> D_04 dropped from inf-gold DAG index, 9 RED tests (org/modules/graph/tests). Fix dispatched to base-AE (execute) + CTO (rule builder-side); split-path blind-spot class. NOT a runtime break (gold scripts run fine); comp-graph index + test-suite only. RAVC2 -> COO+CTO.</status>

SWEEP data/orion->data/inf in 31 files DS couldn't commit (owned-paths blocked): infra/aws/lambda/inf-pipeline/** (24) + inf-portal-advisor-publisher + smartx_rest_pull + infra/aws/ec2/inf-bronze-runner/** + ec2/inf-gold-layer-runner/RUNBOOK. DS sent the detailed file list.

OPERATION: `sed -i 's|data/orion|data/inf|g'` on the literal path-prefix (SAFE — preserves vendor orion_* names: _orion_api_silver_lib.py, orion_billing_dim, convert_orion_api_to_silver, etc., which don't contain 'data/orion'). PLUS the SPLIT-FORM Edit at infra/aws/ec2/inf-bronze-runner/orchestrator.py:327 (`/ "orion" /` -> `/ "inf" /`). Multi-form per CTO (contiguous + backslash + split-form).

REDEPLOY after sweep: inf-pipeline Lambdas via terraform; inf-bronze-runner + inf-gold-layer-runner via safe-ec2-deploy.

5 manual_api debt files (pull_inflection_{assets,reps,transactions} + pull_tax_realize_full + probe_tax_txn): pre-existing inf-content Rule-14 debt (ruff/AST-FP) + comp-constants INFLECTION_REP_IDS {3,6,11,12}-vs-[3,11,12] DATA decision (AE/inf's, separate from P1, low-pri). Clear-debt-then-sweep OR defer to CVO AC10 accept as comment/dev-path residuals.

This is the AE operational half of CVO AC10 0-residual (spans AE-leg d0e2226b8-certified + DS-lane 924bc6c22-verified + THIS + P3 + floored/debt disposition). RAVC2 -> COO+CTO+CVO (AC10).
