<to_id>NFRA_DTAFLP.P1</to_id>
<project>NFRA_DTAFLP</project>
<title>P1 rename: git mv data/orion -> data/inf (~190 files) + orion-side Class-A wiring; black_diamond STAYS</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0179 Andrew sovereign GO, PROCEED-REDUCED-SCOPE 205454Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- LANDED 2026-06-11 15:23Z (d0e2226b8: git mv data/orion -> data/inf, 190 R100 renames + AE Class-A wiring, reduced-scope orion->inf). Ground-truth verified by COO 2026-06-11 ~1946Z: data/orion tree GONE, data/inf EXISTS. The post-02:00Z gate was for the rename's TIMING relative to the nightly; the mv landed cleanly at 15:23Z (well before the cron) so the gate is moot. P1-DS sweep (924bc6c22) + P1-AE infra remainder (46d0b98ae, 0-residual verified) complete the lanes. Board <status> was lagged (read active); trued up by COO under full-send true-up. RAVC2-accepted prior session (/drive log 6b01ded54).</status>

Execute the reduced-scope P1: git mv data/orion/ -> data/inf/ ONLY (data/black_diamond stays; data/cot already abbreviated). Class-A wiring orion-side only: safe-deploy.sh + safe_deploy_core.py path key, pipeline_cli/extract_*/validate_cli orion path strings, EC2_MANIFEST, lambda-source-map, CI, .gitignore. FLAG the 18 path-COMPONENT-form refs (segment "orion"->"inf") to CTO during the mv -- CTO owns them in his cert pass. PRESERVE vendor/API names (orion_api, _orion_api_silver_lib.py, "Orion API"); KEEP orion-gold-dispatch.sh name (firm-abbrev, COO ruling). comp-build regen + all gates (test_safe_deploy, parity-gates, comp-pipescript deployed MATCH) post-mv. CTO cert + 0-residual (data/orion only) follows your RAVC2. RAVC2 to COO + CTO.
