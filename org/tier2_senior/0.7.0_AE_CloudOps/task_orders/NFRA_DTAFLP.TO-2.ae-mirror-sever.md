<to_id>NFRA_DTAFLP.TO-2</to_id>
<project>NFRA_DTAFLP</project>
<title>TO-2 SEVER: remove ssm.tf bd->cot re-mirror sync + repoint opal-data-cot/code/gold deploys to data/cot/scripts/gold</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0179 Andrew sovereign GO, PROCEED-REDUCED-SCOPE 205454Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>active -- GO (LD-0179). GATE: TO-1 done (6b0be4337) so structurally open; execute in the morning window. CAUTION: do NOT run a cot deploy from the git tree until DS TO-1b retarget lands (7 live opal-data-bd refs hard-fail under the cot IAM Deny until retargeted).</status>

Sever the opal-data-bd -> opal-data-cot gold mirror: remove the ssm.tf re-mirror sync; repoint cot gold deploys to source from data/cot/scripts/gold (git). This resolves the STANDING HOLD (any bd->cot re-mirror is UNSAFE -- clobbers the cot mirror patches). Terraform via safe-apply. RAVC2 to COO + CTO; CVO AC10 0-residual close-gate follows P3 completion.
