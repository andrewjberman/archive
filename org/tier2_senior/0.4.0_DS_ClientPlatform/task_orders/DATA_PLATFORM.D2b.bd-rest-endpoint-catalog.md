<to_id>DATA_PLATFORM.D2b</to_id>
<project>DATA_PLATFORM</project>
<title>D2b BD REST endpoint + payload catalog -- full DataMining surface exhaustion sweep (find BILLING query type; enable a-la-carte BD querying outside scheduled ETL)</title>
<assigned_to>0.4.0_DS_ClientPlatform (DS-lead; authored the sweep tool + catalog doc)</assigned_to>
<consult>0.7.0_AE_CloudOps (on-box run: start cot-exporter + fresh session + SSM; IP-binding)</consult>
<verify>3.0.0_SA_CVO (reconcile the endpoint catalog + the billing-charge finding vs live BD)</verify>
<issued_by>PROPOSED by 0.4.0_DS_ClientPlatform (Andrew-direct 2026-07-08 -- "wrap the REST API endpoint research into a DATA_PLATFORM TO"); PENDING 2.0.0_SA_COO issue+register</issued_by>
<issued_date>2026-07-08</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: proposed</status>
<!-- Origin: Christa Bass (Cottonwood) 2026-07-08 "Mgmt fees hit Black Diamond today". DS probe (COO GO, Andrew-direct) proved the mgmt-fee CHARGES are ABSENT from cot bronze -- we ingest only qt1-5, none is a billing query type. Andrew then scoped the forward ask: a full BD REST endpoint+payload catalog for athletic a-la-carte querying outside the scheduled ETL. This D2b TO organizes that research (sibling to D2 spec + D4 SmartX endpoint sweep). -->

<objective>
Produce a complete BD DataMining REST endpoint + payload catalog -- the "D4-for-BD" exhaustion sweep (D2 documented only the FLOW of the 5 query types cot's ETL pulls; it never swept the full surface). The catalog (a) enumerates ALL BD query types -> surfaces the BILLING query type (the management-fee CHARGES) and any other unused datasets, (b) captures each endpoint's payload structure, (c) becomes the dedicated a-la-carte query reference so we can query the BD database purpose-based, outside scheduled ETL. Spec-of-record: docs/briefs/data-platform-d2b-bd-rest-endpoint-catalog-20260708.md (DS draft; CTO promotes to docs/architecture on arch-gate, per the D2 pattern).
</objective>

<the_work>
- SWEEP TOOL (BUILT, gate-clean, RELOCATED 2026-07-08): data/black_diamond/API/tools/bd_endpoint_sweep.py -- spec-hunt (swagger/openapi) + query-type enumeration (the real Query/DimensionsFacts catalog call, id 1..25) + template-roster history + endpoint sweep (status/bytes/ctype/sample per path) + an a-la-carte --probe PATH primitive (GET/POST any endpoint, dump payload). Self-contained (no cot_bronze_ingest cross-import -- firm-parameterized via required env vars, no firm defaults, since it's now homed in the shared vendor-neutral data/black_diamond/API/ catalog). Read-only by default; lands to s3://{BD_S3_BUCKET}/code/bronze/endpoint_catalog/.
- ON-BOX RUN (AE, the live-grounding leg): BD is IP-bound to cot-exporter (i-0643a5bee8a8feabf, currently STOPPED, session STALE from 07-06). Start instance -> opal-cot-bd-session-fetch (fresh session, TTL ~30-60 min) -> SSM opal-cot-bronze-run the sweep tool -> stop. Same DS-authors/AE-runs pattern as the D2 sec.7 enriched-template dump (which is ALSO still un-run -- fold it into the same on-box window).
- CATALOG DOC (DS): DATA_PLATFORM_D2b_BD_REST_ENDPOINT_CATALOG.md -- the dedicated location; D4-style completeness-basis. Seeded with the KNOWN-grounded endpoints now; filled from the sweep result.
- BILLING FINDING: from the billing catalog + a small billing pull, report concretely what "mgmt fees hit BD today" is in the data (fields/accounts/magnitude) -> answers the COO/Andrew delta + explains the Cottonwood Books fee_earning_aua/implied_revenue=0.
</the_work>

<acceptance_criteria>
1. The sweep tool built + gate-clean (DONE 2026-07-08, bd_endpoint_sweep.py).
2. On-box live sweep executed (AE) against a FRESH session -> query-type roster staged (finds BILLING + enumerates all unused query types) + the endpoint payload catalog staged to endpoint_catalog/.
3. The BILLING query type dimension/fact catalog dumped + the mgmt-fee CHARGE finding reported (fields/accounts/magnitude; genuine-new-today vs already-present) -- grounded on the live REST response (Rule 22), not inference.
4. The dedicated catalog doc (D2b) authored with a stated completeness-basis (D4 pattern) -> the a-la-carte BD query reference.
5. CVO reconcile the catalog + billing finding vs live BD. RAVC2 COO + CTO.
6. FOLLOW-ON (separate BUILD TO, NOT this research TO): wire the billing query type into cot_bronze_ingest as a 6th ingested table -> closes the fee_earning_aua/implied_revenue/distribution=0 gap on the Cottonwood Books tab. Scope + gate under a D2c/DATA_PLATFORM build TO after the catalog confirms the billing template shape.
</acceptance_criteria>
