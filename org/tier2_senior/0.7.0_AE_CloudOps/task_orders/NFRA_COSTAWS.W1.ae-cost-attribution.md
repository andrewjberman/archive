<to_id>NFRA_COSTAWS.W1</to_id>
<project>NFRA_COSTAWS</project>
<title>Cost-attribution: CE-resource granularity + cost-allocation tag activation + CUR wiring</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0177 Andrew-direct NFRA staffing; decomposition per CTO dispatch list 174053Z)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_COSTAWS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: in_progress (2026-06-10 ~18:10Z). 2 of 3 legs done: (a) R1 cost-allocation tags VERIFIED Active in CE (all 5: Project/Pipeline/Macro/Owner/Environment — activation had already landed with R1). (b) CUR wiring SHIPPED 554c424e5 + applied 0-diff (shared-infra-v1.22.0): opal-cur-313476888478 bucket + hourly Parquet CUR opal-cur w/ RESOURCES+SPLIT_COST_ALLOCATION_DATA+ATHENA; first delivery within ~24h AWS-side — verify served artifact s3://opal-cur-313476888478/cur/ tomorrow. (c) CE resource-level granularity BLOCKED-console-only: API probe returns AccessDeniedException "opt-in only... PAYER account's Cost Explorer Settings page" — no API exists; needs Andrew 1-click console toggle (routed to COO).</status>

Stand up per-resource cost attribution: Cost Explorer resource granularity, activate the R1 cost-allocation tags, CUR export wiring. RAVC2 to COO.
