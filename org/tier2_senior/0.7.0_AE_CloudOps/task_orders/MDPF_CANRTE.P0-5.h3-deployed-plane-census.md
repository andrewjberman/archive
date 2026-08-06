<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-h3-deployed-census</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Complete H3's DEPLOYED-PLANE half: sweep every deployed surface — Terraform, the Lambda source map, SSM
    documents, portal code, and DEPLOYED LAMBDA ENVIRONMENT VARIABLES — for readers of each
    candidate-retirement output prefix. Also close H8 by reconstructing the deployed publisher's provenance.
  </objective>

  <context>
    H3 RUNS FIRST IN THE PROGRAM (CTO~Z @70733b907) and its scope widened: it is the discharge instrument for
    Andrew's port-completeness condition on an IRREVERSIBLE act, not merely deletion safety.

    ### YOUR HALF vs DS~Z's HALF vs CVO~Z's HALF — three surfaces, one list, no overlap and no gap

      DS~Z (P0-4)  — SOURCE-visible: static import + S3 read/write graph over the CAPTURED closure.
      YOU (P0-5)   — DEPLOYED-plane: TF, source map, SSM docs, portal code, live Lambda env vars.
      CVO~Z (P0-6) — EXTERNAL: the bounded negative. NOT YOURS TO CLOSE and not yours to re-run.

    A deployed Lambda's ENVIRONMENT VARIABLE naming a prefix is a reader that NO SOURCE CENSUS CAN SEE —
    that is why this half exists as its own TO rather than as a section of DS~Z's.

    ### CANDIDATE-RETIREMENT PREFIXES

      `wsb-49f-model-aua-daily` outputs · `wsd-49f-partner-held-etf-daily` outputs ·
      anything under `s3://opal-data-mdpf/mdpf/feeds/*` · the four OWNTS outputs ·
      the bare `platinum/mdpf/aggregate_aua_timeseries.json`
    DS~Z's closure may add rows — coordinate rather than assume the list is closed.

    ### H8 — AND ITS FALLBACK BRANCH, WHICH NOBODY NAMED (CTO~Z Class C2)

    `01` §10 establishes the recorded provenance is KNOWN-WRONG: the source map describes the old
    build-alongside function and the old fenced role, while the live Lambda runs the egress role with
    canonical gold/platinum environment. The live publisher's logs also lack the later roster-completeness
    result, proving DEPLOYED BEHAVIOUR IS BEHIND REPOSITORY BEHAVIOUR.

    So H8 reads as clean Class A and IS NOT GUARANTEED TO BE. Reconstruction is an ATTEMPT. CTO~Z added the
    branch: IF THE DEPLOYED ARTIFACT HASH TIES TO NO COMMIT, PROVENANCE IS UNRECONSTRUCTIBLE, and the honest
    close is a limitation — "deployed provenance unreconstructible; rebuilt from repo tip at `<commit>`."
    Nobody named that branch, so it would otherwise be improvised under deploy pressure.

    ⚠ THE OPERATIONAL CONSEQUENCE, from `01` §10: A BLIND REBUILD FROM REPOSITORY SOURCE WOULD INTRODUCE A
    ROSTER READ AGAINST A MISSING OBJECT. `config/mdpf/partner_roster.json` and
    `config/mdpf/route_bindings.yaml` both returned 404 LIVE while repo code expects them. P2-1 lands those
    objects; until it does, repo-tip publisher behaviour is not deployable.

    ### YOUR OWN PARTIAL RESULT IS ALREADY BANKED

    You measured the orchestrator deployed-vs-repo as IDENTICAL — `s3://opal-data-mdpf/code/mdpf-daily-dispatch.sh`
    sha256 `cc3c6b56d40f12b4a87edada0a2263d2d19aff7e4fbd191ceeb10d1d93836ff7`, 688 lines, diff 0, with the
    VersionId and LastModified pinned. That is a genuine narrowing of H8 AND YOU SCOPED IT HONESTLY: it says
    the ORCHESTRATOR has not diverged and says nothing about the `.py` modules or site-packages. Keep that
    scoping discipline in this TO — a narrowing is not a closure.

    ### THE INSTRUMENT THAT UNDER-REPORTS

    MEASURED at c801ec9d5 on a fresh graph (age 0.0h, Nessie HEAD current): `comp-blast mdpf_aggregate_aua`
    returned "No downstream consumers found (no EXTRACTED edge — NOT provably zero)" against ledger evidence
    of FOUR consumers (@ad76ad830, 439 partitions content-verified). GRAPH SAID ZERO; GROUND TRUTH SAID FOUR.
    An under-reporting instrument does not produce a durable zero — it produces a FALSE NEGATIVE THAT LOOKS
    LIKE A FINDING. With teardown authorized, a zero-reader claim is now upstream of an irreversible act.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-which "what deployed resources reference this s3 prefix"</run>
      <expect>Routes to comp-estate / comp-aws / comp-pipescript, or runs comp-grep on-rails.</expect>
      <if_mismatch>Coverage gap -> COO~Z (Rule 21). Note: an EC2-inventory intent already returned no
      curated rule today — a SECOND distinct gap in one program is a routing signal, not noise.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-estate --resource &lt;each candidate prefix&gt;</run>
      <expect>Thread membership + declared consumers. READ THE PROVENANCE HEADER — keys are re-derived live,
      NAMES come from a snapshot the tool declares stale past 14d.</expect>
      <if_mismatch>Stale header -> `--refresh` before trusting a NAME. A NAME miss is not an absent resource.</if_mismatch>

      <run>comp-pipescript deployed</run>
      <expect>MATCH/STALE/MISSING across all trees, firm-separated.</expect>
      <if_mismatch>A STALE or MISSING row on any MDPF script is a finding for the deliverable.</if_mismatch>

    Phase 3 — after committing: every surface swept, with its denominator, in the session log Compiler Tools
    table. A denominator-free row is not accepted.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>The candidate-retirement prefix list</shared_resource>
    <also_in_to>P0-4 (DS~Z, source-visible half) · P0-6 (CVO~Z, external half) · P6-1 (retirement)</also_in_to>
    <last_write_owner>each seat owns its own surface; no seat owns the list</last_write_owner>
    <required_action>MCP DS~Z and CVO~Z to align the list so no row is assumed covered by another seat. Three
    surfaces, one list. Coordination artifact, NOT an approval step — nobody waits on a blessing.</required_action>

    <shared_resource>`infra/aws/lambda/ci/lambda-source-map.json`</shared_resource>
    <also_in_to>P3-1 (publisher correction) · P5-1 (source-map update in the cutover commit)</also_in_to>
    <required_action>THIS TO READS AND DIAGNOSES THE SOURCE MAP; IT DOES NOT CORRECT IT. The correction
    lands in the cutover commit (P5-1) so the map and the deployed bytes move together.</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. EVERY SURFACE SWEPT IS NAMED, WITH ITS DENOMINATOR: repo, `lambda-source-map.json`, Terraform, SSM
       documents, portal code, AND DEPLOYED LAMBDA ENVIRONMENT VARIABLES (function count queried).
       FORBIDDEN SHORTCUT, NAMED: a repo grep is NOT the deployed plane. The whole reason this TO is
       separate from DS~Z's is that a deployed env var referencing a prefix is invisible to source.

    2. PER PREFIX, A ROW WITH ITS OWN EVIDENCE — never a group verdict. Third state required:
       READER-FOUND / NO-READER-ON-THIS-SURFACE / NOT-DETERMINABLE (with reason).
       NOT-DETERMINABLE != NO READER, and a surface not queried is UNKNOWN, not zero.

    3. NO CONCLUSION RESTS ON A GRAPH EDGE COUNT. Corroborate every zero with a literal-key grep plus
       `comp-pipescript consumers`. If comp-blast is cited at all, cite it as a LOWER BOUND with its own
       disclaimer quoted.

    4. WHAT A ZERO MAY ASSERT: "no reader on the DEPLOYED surfaces named here." NEVER "no reader."
       RESERVED WORDS PROHIBITED on any absence claim: proof / provably / definitively / source-confirmed.
       DO NOT REPORT THIS CENSUS AS CLOSING H10 — that is CVO~Z's single declaration site.

    5. H8 RECONSTRUCTION ATTEMPTED AND ITS OUTCOME BRANCHED EXPLICITLY. Either the deployed publisher
       artifact hash TIES to a commit — state the commit and the hash — or it ties to NONE, in which case the
       close is the recorded limitation: "deployed provenance unreconstructible; rebuilt from repo tip at
       `<commit>`." Both are complete outcomes. Improvising a third under deploy pressure is not.

    6. THE SOURCE-MAP DRIFT IS ENUMERATED FIELD BY FIELD, not asserted as "stale." Which fields disagree
       with the live function (description, role, artifact key, hash, commit, deployed time, runtime, layer)
       and what the live value is. P5-1 corrects it; this TO produces the diff it corrects against.

    7. THE ROSTER/ROUTE-BINDINGS 404 IS RE-CONFIRMED LIVE OR REFUTED, with the head-object output cited.
       This is load-bearing: a blind rebuild from repo source would introduce a roster read against a
       missing object, so P3-1's deployability depends on P2-1 landing those two config objects first.

    8. DENOMINATORS USE EXPLICIT PAGINATION. ⛔ `--query 'length(...)'` ON A PAGINATED `list-*` RETURNS THE
       PAGE COUNT, NOT THE TOTAL — measured 2026-07-31: `aws events list-rules --query 'length(Rules)'`
       reported 100 when the truth was 142, no error, no warning. Count the materialised list.

    9. THE ORCHESTRATOR TIE IS CARRIED FORWARD WITH ITS SCOPE INTACT: it narrows H8 for
       `mdpf-daily-dispatch.sh` ONLY and says nothing about the `.py` modules or site-packages. Do not let
       it read as "deployed matches repo."
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/MDPF_H3_DEPLOYED_CENSUS_20260806.md</file>
      <file action="reference">infra/aws/lambda/ci/lambda-source-map.json</file>
      <file action="reference">infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Sweep the deployed plane incl. live Lambda env vars; name every surface + denominator.</requirement>
    <requirement id="2">One row per prefix with a third state available.</requirement>
    <requirement id="3">Attempt H8 reconstruction; branch explicitly on tie-vs-no-tie.</requirement>
    <requirement id="4">Enumerate source-map drift field by field. Do not correct it here.</requirement>
    <requirement id="5">Re-confirm or refute the roster/route-bindings 404 on the live primitive.</requirement>
    <requirement id="6">Do not close H10; do not re-run DS~Z's source census.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Deployed-plane census + H8 provenance reconstruction, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">The source-map field-by-field diff, for P5-1 to correct against</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT DELETE OR RETIRE ANYTHING. This TO dispositions. H13 is OPEN — S3 deletion is on CLAUDE.md's
    human-confirmation list and Andrew's teardown word did NOT authorize it.</rule>
    <rule>DO NOT CITE A ZERO-CONSUMER GRAPH RESULT AS RETIREMENT EVIDENCE — measured false zero on
    mdpf_aggregate_aua at c801ec9d5 (0 reported vs 4 real).</rule>
    <rule>DO NOT REPORT THIS CENSUS AS CLOSING H10. External/manual readers are CVO~Z's single declaration
    site and terminate in a recorded limitation, never a proof.</rule>
    <rule>DO NOT CORRECT THE SOURCE MAP IN THIS TO. It lands in the cutover commit so map and bytes move
    together.</rule>
    <rule>DO NOT REBUILD THE PUBLISHER FROM REPO SOURCE. A blind rebuild introduces a roster read against a
    404 object. P3-1 owns the rebuild and P2-1 must land the config objects first.</rule>
    <rule>DO NOT let a narrowing read as a closure. The orchestrator tie covers one file.</rule>
    <rule>NO NEW GATES. NO SHADOWS. NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS.</rule>
    <rule>DO NOT use `--query 'length(...)'` on a paginated `list-*` call — it returns the PAGE count.</rule>
    <rule>DO NOT use the shared dirty checkout as evidence of live state. Never rebase on SITEZ. Commit to
    your lane; push is MSTR~Z's. Working files in the scratchpad.</rule>
    <rule>DISCARD any comp-freshness verdict produced on this box before 2c4510421.</rule>
  </do_not>
</task_order>
