<task_order>
  <metadata>
    <id>YALP_MDSRC.L1</id>
    <slug>ae-yang-pipeline-lineage-map</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_owner>0.3.0_DE_TradingOperations -- the React frontend component side + the "Data Refresh" portal page. 0.7.0_AE leads the write-side (yang-pipeline Lambdas / S3 buckets / portal-publisher read Lambdas / routes) + the comp-graph extension.</co_owner>
    <date>2026-05-22</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <!-- GO ON PICKUP 2026-05-22 (COO /loop drive). Andrew directive 2026-05-22: produce a complete MIRROR-IMAGE lineage map of the yang-pipeline -- every yang-pipeline Lambda (write-data side AND portal-publisher read-data side) mapped to the granular React frontend components, so we know EXACTLY where every import and write happens in concert. Runs PARALLEL to D2 (Andrew: "idle agent, now"). -->
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 -- Andrew-direct. The complete lineage map is necessary groundwork for the future production cutover + ongoing portal-data correctness.</priority>
    <sla>~3-5 days.</sla>
  </metadata>

  <references>
    <comp_graph>.comp-graph/graph.json (1.28MB) + the extractors in org/modules/graph/ (extract_lambda_routes.py, extract_s3.py, extract_routes.py, extract_transforms.py, extract_pipeline.py, extract_iam.py, extract_eventbridge.py). comp-trace / comp-blast / comp-routes / comp-pipescript / comp-transform query it. EXTEND this graph -- do NOT build a new compiler. The node model (Lambda, S3, route, transform, React component) already exists; L1's work is verifying + completing the edges for this specific lineage and emitting the comprehensive map.</comp_graph>
    <yang_scripts>docs/reference/yang-original-scripts/ -- Yang's original notebooks (dc_index / dc_macro / dc_fields_all ticker+field maps; the model-portfolio regression methodology). Deliverable A processes these into a structured rubric.</yang_scripts>
    <data_refresh>The portal "Data Refresh" page -- a pipeline-operations surface. Use it as an additional visibility source for what the pipeline writes/refreshes and when.</data_refresh>
  </references>

  <context>
    Andrew directive 2026-05-22: we need to know EXACTLY where every single import and write happens in concert across the yang-pipeline -- the writer Lambdas, the S3 buckets/keys they write, the portal-publisher Lambdas that read those artifacts, and the granular React frontend components that display the data. Today comp-trace answers this one node at a time; no comprehensive mirror-image map exists. L1 produces it. The deliverable underpins the future production cutover (knowing the full lineage is what makes a clean cutover possible) and ongoing portal-data correctness.
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- Yang-scripts structured rubric: process docs/reference/yang-original-scripts/ into a structured working rubric -- the dc_index / dc_macro asset+ticker taxonomy, the dc_fields_all field-code map, and the model-portfolio regression/factor-spread methodology -- organized so an agent can look up any datum's Bloomberg origin + Yang's intended transform.

      DELIVERABLE B -- the MIRROR-IMAGE yang-pipeline lineage map. For EVERY data point the yang-pipeline produces and the portal displays, map BOTH directions:
      - WRITE side: which yang-pipeline Lambda writes it; what it is procured from (Bloomberg field / SmartX / FRED / computed); which S3 bucket + key it lands in.
      - READ side: which portal-publisher Lambda reads that S3 artifact; which granular React frontend component renders it.
      Deliver at TWO granularities: (1) ATOMIC -- data-point-by-data-point (every field of every artifact); (2) GROUPED -- three roll-ups: by React component, by Lambda-read (publisher), by Lambda-write (producer).

      METHOD: extend + query the comp-graph. Verify edge-completeness for the yang-pipeline write Lambdas + the portal-publisher read paths + the React components; fill gaps in the org/modules/graph/extract_*.py extractors where coverage is thin. Cross-check against: the yang-pipeline Lambda source, the portal publisher, the React frontend, the Yang rubric (Deliverable A), and the "Data Refresh" portal page.

      Output: a committed lineage-map artifact (structured doc/brief, or a comp-graph-emitted report) + any comp-graph extractor extensions.
    </in_scope>
    <out_of_scope>
      - ANY production / AWS / portal change -- L1 is read + map + document only. No cutover, no Lambda edit, no Terraform.
      - The D2 YCharts-vs-Bloomberg comparison (separate TO, in flight).
      - The production cutover (a future project).
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>L1 IS a comp-graph task -- the comp-graph is the deliverable's vehicle. Use comp-trace (full chain, both directions), comp-routes (CF->S3 paths), comp-pipescript (portal consumers / column gaps), comp-transform schema-check (React component fields) as the building blocks; extend the extractors (org/modules/graph/extract_*.py) where the yang-pipeline-writer + portal-publisher + React-component edges are incomplete. Reproduce the comp-* runs in the session log.</note>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - Lead 0.7.0_AE_CloudOps: the write-side (yang-pipeline Lambdas, S3 buckets/keys), the portal-publisher read Lambdas, the comp-graph extractors, routes/IAM.
    - Co-owner 0.3.0_DE_TradingOperations: the React frontend component side -- which granular component renders which datum -- and the "Data Refresh" portal page as a visibility source.
    - Coordinate with 0.1.0_DS / 0.2.0_DS (on D2) for YCharts-side context if needed -- L1 does not block on D2.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Deliverable A: Yang's scripts processed into a structured rubric (dc_index/dc_macro taxonomy + dc_fields_all field map + regression methodology), committed.</ac>
    <ac id="AC2">Deliverable B atomic layer: every yang-pipeline data point mapped write-side (producer Lambda / source / S3 bucket+key) AND read-side (publisher Lambda / React component) -- data-point-by-data-point.</ac>
    <ac id="AC3">Deliverable B grouped layer: the three roll-ups -- by React component, by Lambda-read, by Lambda-write.</ac>
    <ac id="AC4">comp-graph extended where edge-coverage was incomplete; comp-* runs reproduced in the session log; the "Data Refresh" page cross-checked. Committed lineage-map artifact. RAVC2 to 2.0.0_SA_COO.</ac>
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT build a new compiler -- extend the existing comp-graph. A net-new tool only if the comp-graph genuinely cannot model a needed edge class -- flag that to COO first with the specific gap.</rule>
    <rule>Do NOT make any production / AWS / portal / Lambda / Terraform change -- L1 reads + maps only.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
