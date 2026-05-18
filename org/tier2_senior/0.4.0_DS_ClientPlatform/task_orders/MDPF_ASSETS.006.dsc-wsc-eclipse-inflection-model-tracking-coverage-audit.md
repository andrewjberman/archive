<task_order>
  <metadata>
    <id>MDPF_ASSETS.006</id>
    <slug>dsc-wsc-eclipse-inflection-model-tracking-coverage-audit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-18 (COO) to DS~C -- Andrew spun up the lane for this. A read-only coverage-verification investigation; not gated on anything. NOTE: if this lane also holds the INF chain-#2 RAVC2 cascade (INFGRO.007 / BIWNDW.002 / INFGRO.009 verification), that cascade is chain-gated (~17:30Z) and takes precedence WHEN chain #2 lands -- run this investigation now, pause for the 3 RAVC2s when the chain completes, then resume.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- Andrew-direct, "asap." MDPF WS-C (Inflection model AUA = Cohort 2a/2b). Andrew wants the Eclipse/Inflection model-asset tracking coverage definitively mapped before the WS-C build TO is scoped.</priority>
    <sla>1-1.5d wall -- a coverage-verification investigation ending in a brief. Read-only; consolidate existing work + one deep-dive (transactions). NOT a build.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.3+) -- section 3.0 cohort taxonomy (Inflection = Cohort 2; 2a model AUA, 2b non-model AUA), section 3.2 convergent model-AUA schema, section 4 WS-C, section 7-Q2/Q3.</prd>
    <prior_work_DO_NOT_REDO>
      - docs/briefs/mdpf-eclipse-inflection-model-aua-feasibility-20260518.md (MDPF_ASSETS.003, DS~B, 2026-05-18) -- the WS-C feasibility. ALREADY ESTABLISHED: WS-C is GO; the shipped Eclipse pipeline carries account/household/model grain; the one convergent-schema gap is holdings[] (ticker-level composition via Orion Trading/Models/{id}.items[]); Opal ETFs PFDE/PFOE are line-item positions in 7 of 9 Opal models; Inflection non-model (Cohort 2b) ~$106M exists in the same feed (IWM $87.9M + unassigned $18.2M). DS~C CONSOLIDATES + VERIFIES this against live artifacts -- does not re-run the feasibility.
      - docs/briefs/data-scientist-eclipse-ingestion-feasibility-20260514.md -- the 2026-05-14 Eclipse feasibility probe (the Eclipse<->Orion model-ID map; the .runtmp/orion_model_probe/ snapshots).
      - ADVI_ECLDAT.json -- the Eclipse ingestion project, Phases 1-4 SHIPPED 2026-05-14/15. ECLDAT.004 shipped INF_E_00.eclipse_model_portfolios.py (the gold 'E' family). Session log of record: org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-15/DS_A_session8_advi_ecldat_freshness_and_gold.md.
    </prior_work_DO_NOT_REDO>
    <shipped_pipeline>data/orion/scripts/{bronze/pull_eclipse_portfolios.py, silver/convert_eclipse_portfolios_to_silver.py, gold/INF_E_00.eclipse_model_portfolios.py} -- writes s3://opal-data-inf/{bronze,silver,gold}/eclipse/{date}/. Chain-wired into CATALOG + CHAIN_FULL (the E-family trio).</shipped_pipeline>
  </references>

  <context>
    Andrew (direct, 2026-05-18, "asap"): "tracking of model assets via eclipse for inflection ... I think we have already done this on 5/15, but I want you to verify what level of coverage is there." The 5/15 work is ADVI_ECLDAT Phases 1-4 -- the shipped Eclipse ingestion that emits gold/eclipse/{date}/ at account(399) / household(214) / model(10) grains. MDPF_ASSETS.003 (today) confirmed WS-C feasibility off that pipeline.

    What .003 did NOT cover is the TRANSACTION dimension -- it was a model-AUA (point-in-time value) feasibility, not a flow/transaction audit. Andrew's questions go further than .003: how are transactions tracked/marked with regard to model distribution, how are they classified, and is any of that in the inf pipeline or separate. That is the genuine open area and the substance of this TO.

    Deliverable: a single definitive COVERAGE MAP brief that answers all six of Andrew's questions with evidence, marks each data element covered / partial / gap, and names where each lives. It feeds (does not replace) the WS-C Phase-2 build TO. Read-only -- inspect shipped scripts + live S3 artifacts + prior probe snapshots; a live read-only API probe is permitted only where a question cannot be answered from existing artifacts (the .003 / 2026-05-14 method).
  </context>

  <scope>
    <step>Phase 0 -- absorb, do not redo. Read the .003 brief, the 2026-05-14 feasibility brief, ADVI_ECLDAT.json + the ECLDAT.004 session log, and the three shipped Eclipse scripts. Inventory what is already established so this investigation adds, not repeats.</step>
    <step>Phase 1 -- answer Andrew's six questions with evidence. Verify each against the live S3 artifacts (latest silver/eclipse + gold/eclipse partition), not just the briefs:
      Q1 -- COVERAGE OF THE 5/15 WORK: what ADVI_ECLDAT Phases 1-4 actually delivered; the state, grains, and freshness of gold/eclipse/. Confirm the partition cadence (.003 flagged partitions are sparse -- 2026-05-15, -17 -- not strictly daily; verify whether the E-family chain-trio now runs daily).
      Q2 -- HOUSEHOLD-LEVEL MODEL MEMBERSHIP: do we know, per Inflection household, which Opal model(s) its assets are in? Verify model_portfolio_households.parquet + the account-grain household_id/eclipse_model_id linkage. Does coverage reach the individual client/person within a household, or stop at household_id? State precisely.
      Q3 -- ACCOUNT-LEVEL GRANULARITY: confirm the per-account grain (model_portfolio_accounts.parquet, 399 rows) -- what each account row carries (model assignment, value, household, custodian). Confirm one account = one model, or whether an account can span models.
      Q4 -- TRANSACTIONS vs MODEL DISTRIBUTION (the deep-dive, .003 did not cover this): Are Inflection transactions ingested at all -- does the INF transaction pipeline (INF_API_PULL_TXN / silver transactions) cover the Eclipse/Inflection accounts? Are transactions marked or taggable with model membership? Is there any notion of model-distribution / rebalance / model-assignment-change events -- a flow record of assets moving into/out of/between models? How would a transaction be attributed to a model today (e.g. txn.account_id -> portfolio.model_id point-in-time join), and what breaks that (model reassignment over time -- is there a model-assignment history, or only the current model_id)? This is the question to hammer down.
      Q5 -- CLASSIFICATION: how are accounts/assets classified into models today (the OPAL_ECLIPSE_MODEL_IDS hardcoded set; portfolios_simple.model_id assignment) -- and how, if at all, are transactions/flows classified by model. Distinguish the two clearly.
      Q6 -- STORAGE / PIPELINE LOCATION: map exactly where every piece lives. Is the Eclipse model data in the inf pipeline (s3://opal-data-inf/.../eclipse/) or a separate store? Is transaction data in the same pipeline or separate? Produce the storage map (artifact -> S3 path -> grain -> producing script -> chain membership).</step>
    <step>Phase 2 -- the coverage map. Produce one brief (docs/briefs/) with: (a) a coverage table -- every data element x grain x covered/partial/gap x storage location; (b) the explicit answer to each of Q1-Q6; (c) a GAP LIST -- what the WS-C Phase-2 build (and any transaction-model-attribution work) must add, separating the already-known holdings[] gap from anything new this audit surfaces, especially on the transaction side; (d) whether the transaction-model dimension is in WS-C scope or warrants its own workstream. RAVC2 to COO.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io on the INF transaction scripts (INF_API_PULL_TXN and the silver/gold transaction scripts) + comp-trace on the transaction artifacts -- to ground Q4 (whether the transaction pipeline carries or could carry a model dimension).</run>
        <expect>The transaction pipeline's column surface + where it reads/writes -- evidence for whether a model field exists, is joinable, or is absent.</expect>
        <if_mismatch>If the graph tools do not resolve the Eclipse/transaction nodes, fall back to direct inspection of the scripts + the live silver transaction artifacts; note which.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>N/A -- MDPF_ASSETS.006 is a read-only coverage-verification investigation; no code shipped, no AWS surface added. State so in one line.</run>
        <expect>N/A.</expect>
        <if_mismatch>n/a</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A read-only investigation. No pipeline producer modified, no artifact rewritten, no reprocessing. A live read-only Eclipse/Orion API probe is permitted only where a question cannot be answered from existing S3 artifacts or prior probe snapshots.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    Read-only -- no file overlap. The investigation inspects ADVI_ECLDAT's shipped pipeline + the INF transaction pipeline; it modifies neither. If a live API probe is needed, reuse the existing JWT machinery (the Orion JWT in Secrets Manager orion/jwt/current, the Eclipse JWT helpers in pull_eclipse_portfolios.py) -- do not provision new auth. If this lane also holds the INF chain-#2 RAVC2 cascade, those 3 RAVC2s take precedence when chain #2 lands (~17:30Z); this investigation yields to them and resumes after.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A coverage-map brief ships at docs/briefs/ with a coverage table: every Eclipse/Inflection model-tracking data element x grain x covered/partial/gap x storage location (S3 path + producing script + chain membership).</ac>
    <ac id="AC2">Each of Andrew's six questions (Q1 5/15-coverage, Q2 household-level model membership, Q3 account-level granularity, Q4 transactions vs model distribution, Q5 classification, Q6 storage location) is answered explicitly with evidence from live artifacts -- not just restated from the .003 brief.</ac>
    <ac id="AC3">Q4 is the deep-dive: a definitive finding on whether Inflection transactions are ingested, whether they carry or can be joined to a model dimension, whether model-distribution / rebalance / model-reassignment events are tracked, and how transaction-to-model attribution would work (and what breaks it). If model-assignment history is absent, say so and state the consequence.</ac>
    <ac id="AC4">A GAP LIST that separates the already-known holdings[] gap (from .003) from anything new this audit surfaces; a recommendation on whether transaction-model tracking belongs in the WS-C build or its own workstream. Surfaced to COO for build-TO scoping.</ac>
    <ac id="AC5">No emoji; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Eclipse/Inflection model-tracking coverage-map brief (docs/briefs/).
    - The answer to each of Andrew's six questions, evidenced.
    - The gap list + the WS-C-scope-vs-own-workstream recommendation, surfaced to COO.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
