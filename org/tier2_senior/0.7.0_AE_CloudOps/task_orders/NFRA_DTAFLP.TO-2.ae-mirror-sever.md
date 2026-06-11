<to_id>NFRA_DTAFLP.TO-2</to_id>
<project>NFRA_DTAFLP</project>
<title>TO-2 SEVER: remove ssm.tf bd->cot re-mirror sync + repoint opal-data-cot/code/gold deploys to data/cot/scripts/gold</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0179 Andrew sovereign GO, PROCEED-REDUCED-SCOPE 205454Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>CLOSED-VERIFIED 2026-06-11 152xZ — substantive sever was ALREADY DONE by AE~B 06-10 (2976e40a2) + CVO-verified (ac88e4f9c "TO-2 re-mirror SEVERED"). AE caught the redundancy on re-dispatch (verify-before-redo, avoided a redundant prod apply). Live confirm: bd->cot sync exists ONLY as `# #`-commented footgun warning (ssm.tf L198-215); deployed SSM doc L234 "NEVER mirrored from opal-data-bd"; cot_gold_run syncs FROM opal-data-cot (safe dir). The morning re-dispatch was post-respawn re-verification. RESIDUAL: cosmetic ssm.tf:272 echo "mirrored from 49F" string (CVO AC10 residual) -> scrub-comment rides the COTETL.CHAIN-FIX cot-infra safe-apply (no standalone prod apply).</status>

Sever the opal-data-bd -> opal-data-cot gold mirror: remove the ssm.tf re-mirror sync; repoint cot gold deploys to source from data/cot/scripts/gold (git). This resolves the STANDING HOLD (any bd->cot re-mirror is UNSAFE -- clobbers the cot mirror patches). Terraform via safe-apply. RAVC2 to COO + CTO; CVO AC10 0-residual close-gate follows P3 completion.
