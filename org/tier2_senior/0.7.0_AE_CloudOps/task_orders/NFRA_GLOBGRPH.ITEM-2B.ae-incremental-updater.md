<to_id>NFRA_GLOBGRPH.ITEM-2B</to_id>
<project>NFRA_GLOBGRPH</project>
<title>Incremental updater: CloudTrail -> EventBridge -> Lambda bounded comp-aws derive --resource -> Nessie commit (1-2min micro-batch debounce per Andrew D1/D2 ruling)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>active -- GO (unblocked: Item-2a derive-runner landed bcdf33ccb globgrph-v0.1.5)</status>

Build the Item-2b incremental path per PRD P1.5 design lock (D1=micro-batch ~1-2min debounce; D2=CloudTrail-via-EventBridge). Terraform-only deploy, layers for deps, source-map entry, tag after 0-diff. DEPENDS: Iceberg-409 retry/backoff (sibling TO) must land BEFORE 2b goes live. RAVC2 to COO; CVO re-cert follows.
