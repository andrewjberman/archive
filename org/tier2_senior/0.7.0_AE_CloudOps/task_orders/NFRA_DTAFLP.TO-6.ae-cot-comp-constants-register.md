<to_id>NFRA_DTAFLP.TO-6</to_id>
<project>NFRA_DTAFLP</project>
<title>Apply DS's ready comp-constants patch: register cot search_surface + FIRM_ID/FIRM_NAME constants (resolves TO-4 drift)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (from DS TO-4 RAVC2 cross-lane follow-up, 20260611T134335Z)</issued_by>
<issued_date>2026-06-11</issued_date>
<status>active -- LOW-PRI, sequenced post-P1/TO-2. Runtime UNAFFECTED (cot FIRM_ID='cottonwood' correct+deployed). Must land before P3/CVO AC10 0-residual close.</status>

DS's TO-4 (cot firm-native FIRM_ID drop, 6ce1ff5fc) surfaced a comp-constants drift: cot's FIRM_ID='cottonwood' diverges from bd/inf canonicals because cot is not registered in comp-constants.config.yaml. That file is ANY_EXEC_OR_AE-owned (owned-paths guard blocks DS commit). DS prepared a ready-to-apply patch:
  docs/briefs/dtaflp-to4-cot-comp-constants-registration.patch
registering a 'cot' search_surface + cot-lane FIRM_ID/FIRM_NAME constants (same pattern as the inf-lane entry DS added 2026-05-13).

EXECUTE: review the search_surface registration, `git apply` the patch, comp-build regen (0-error), commit under AE author line. Until landed, the comp-constants drift check fails on any future cot gold commit touching FIRM_ID + flags at CVO AC10. RAVC2 -> COO. NOT blocking the DTAFLP P1/TO-2 critical path.
