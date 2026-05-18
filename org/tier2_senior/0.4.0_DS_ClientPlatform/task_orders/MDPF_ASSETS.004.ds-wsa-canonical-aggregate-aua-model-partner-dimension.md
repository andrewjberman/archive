<task_order>
  <metadata>
    <id>MDPF_ASSETS.004</id>
    <slug>ds-wsa-canonical-aggregate-aua-model-partner-dimension</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-18 (COO) to DS~A -- the lane that ran the MDPF Phase-0 custody audit (.001/.002), idle + available post-Phase-0. WS-A is fully unblocked: the three Phase-0 briefs have landed, the Schwab-only custody ruling is in, PRD v0.2 (section 3.4 corrected) is shipped, and CTO is standing ready for the Phase-0 contract review. Phase 1 of MDPF_ASSETS -- the foundation TO; gates all of Phase 2 (WS-B/C/D/E emit shape) + Phase 3 (WS-F consumption).</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF_ASSETS Phase 1, the single foundation. The convergent per-partner schema + the platinum aggregate-AUA contract must exist before any Phase-2 feeder (WS-B/C/D/E) can be authored to a stable emit shape. Author first.</priority>
    <sla>2-3d wall -- a data-contract design + CTO contract review + a thin aggregation gold script + fixture verification. Not a partner-pipeline build (those are Phase 2).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.1) -- section 3.1 (the decomposition), section 3.2 (convergent per-partner model-AUA schema), section 3.3 (ETF ownership decomposition -- the no-double-count rule WS-A's schema must support), section 3.4 (49F non-model term), section 3.5 (reconciliation invariant -- the three load-bearing identities), section 4 WS-A spec, section 7-Q5 (Cottonwood-ready dimension recommendation).</prd>
    <custody_ruling>Andrew direct 2026-05-18: Opal advised AUA = SCHWAB-CUSTODIED ONLY (~$1,655.4M). Anything not at Schwab is excluded. This fixes the section-3.4 non_model_aua(49F) term -- the WS-A contract reserves the schema slot; WS-E (Phase 2) computes it as a single Schwab-include filter. Recorded in MDPF_ASSETS.json (commit a2f4e399f).</custody_ruling>
    <phase0_briefs>
      - docs/briefs/mdpf-49f-nonmodel-custody-cutout-audit-20260518.md (MDPF_ASSETS.001, DS~A) -- the account-&gt;custodian crosswalk + the certified_aua decomposition; named gap (2): model_aua is a SmartX scalar, not account-keyed to BD -- WS-A should make the per-partner model-AUA grain explicit.
      - MDPF_ASSETS.002 brief (PFDE/PFOE ETF net-assets feasibility, DS~A).
      - MDPF_ASSETS.003 brief (Eclipse-&gt;Inflection model-AUA feasibility, DS~B) -- the holdings[] gap (Orion Trading/Models/{id}.items[]).
    </phase0_briefs>
    <reuse_anchor>ADVI / ADVI_FIRMSEP firmId partner-scoping -- live in production. WS-A's `partner` dimension canonical key IS `firmId`, the same identifier ADVI scopes on. Reuse the identifier + the rollup semantics (Aggregate = un-filtered sum of partner rows, exactly as ADVI firm rollups are sums of advisor rows). Do not fork.</reuse_anchor>
  </references>

  <context>
    MDPF_ASSETS evolves the Model Portfolios page's "Opal AUA" from a single-tenant 49F view into a partner-decomposed aggregate. WS-A is the foundation everything else lands on: it defines the data contract every Phase-2 feeder (WS-B 49F/SmartX, WS-C Inflection/Eclipse, WS-D ETF, WS-E 49F non-model) must emit to, and the platinum artifact WS-F (the portal selector) consumes.

    WS-A is NOT a partner pipeline. It builds no feeder. It builds two things: (1) the contract -- the convergent per-partner model-AUA schema (section 3.2) and the platinum aggregate-AUA artifact schema (sections 3.1 + 3.5); (2) a thin aggregation gold script that sums whatever convergent-schema partner rows exist into the platinum artifact, with the reconciliation block. At Phase 1 no Phase-2 feeder has shipped yet, so the aggregation is verified against synthetic fixtures -- the script must produce a valid (possibly empty) artifact with zero feeders and a correct aggregate with fixture feeders.

    The decomposition (section 3.1): `Opal Aggregate AUA = Sigma_partner [ model_aua(partner) + non_model_aua(partner) ]`. The `partner` dimension (`firmId`) is first-class on every row. There is no separate aggregate pipeline -- Aggregate is the un-filtered sum; a per-partner view is a `firmId` filter.

    The convergent-contract invariant (section 3.2): feeders are partner-pipeline-specific at ingestion but converge to ONE schema before the aggregate layer -- `(firmId, model_id, as_of_date, model_value, holdings[])`. The aggregate layer never branches on partner. WS-A owns that schema; getting it right is what lets WS-B/C/D/E be authored and built in parallel.
  </context>

  <scope>
    <step>Phase 0 -- contract design + CTO review. Draft, as a contract document (docs/architecture/ or docs/briefs/ -- AE/CTO's call on home):
      - The convergent per-partner model-AUA schema (section 3.2): the exact field set, types, and grain of `(firmId, model_id, as_of_date, model_value, holdings[])`. Address Phase-0 named gap (2): model_aua must be account-grain-attributable, not a bare SmartX scalar -- decide the grain (account-level vs model-level rows) and the holdings[] shape (the WS-C Orion items[] pull and the WS-B SmartX weights must both conform). The holdings[] shape must support the section-3.3 ETF no-double-count rule -- a partner-held ETF position is identifiable so it is counted once in model_aua, never also as standalone ETF AUA.
      - The platinum aggregate-AUA artifact schema (sections 3.1 + 3.5): the row grain, the `partner`/`firmId` dimension, the model/non_model split, and the section-3.5 reconciliation block (the three identities below).
      - The non_model_aua(partner) slot: a schema field WS-E (Phase 2) fills. Per the Schwab-only ruling, WS-E computes it as certified_aua restricted to Schwab-custodied accounts minus model_aua; WS-A does NOT compute it, only reserves the typed slot + documents the ruling in the contract.
      - The gold-script placement question: the aggregation reads convergent-schema feeders sourced across smartx + inf-pipeline + etfs. Decide (with CTO) which pipeline's gold/ directory hosts the MDPF aggregation script, or whether MDPF needs its own gold home + S3 prefix. Record the decision.
      - Cottonwood-readiness (PRD section 7-Q5): the `partner` dimension is built fully generic now -- a new partner is a new `firmId` + a new feeder, zero aggregate-layer change. Confirm the contract has no hard-coded 49financial/inflection branch.
      CTO reviews + ratifies the contract before the Phase-1 build. Surface the contract to COO + CTO; do not start Phase 1 until CTO ratifies (the contract gates four downstream workstreams -- a contract change after WS-B/C/D/E start is expensive).</step>
    <step>Phase 1 -- the aggregation gold script. Build the thin gold script that: reads the convergent-schema per-partner model-AUA artifacts + the per-partner non-model artifacts from their S3 prefix(es); sums per section 3.1 into the platinum aggregate-AUA artifact; carries the `firmId` partner dimension first-class on every row (Aggregate = un-filtered sum, per-partner = filter); emits the section-3.5 reconciliation block. The script must produce a valid artifact with zero feeders present (empty aggregate, reconciliation trivially holds) and a correct aggregate when feeders are present. Rule 15 (`from __future__ import annotations` first import); ds-commit-gate before commit.</step>
    <step>Phase 2 -- fixture verification of the reconciliation invariant (section 3.5). With synthetic partner fixtures (>=2 partners, each with model + non-model rows, >=1 shared ETF position), verify the three load-bearing identities:
      1. `Opal Aggregate AUA == Sigma_partner ( model_aua + non_model_aua )` -- exact.
      2. Per ETF: `ETF_total_net_assets == Sigma_partner held_{partner} + public_residual`; `public_residual` is the measured plug -- a NEGATIVE residual is an ERROR-class signal (partner attribution over-counts), not a silent absorb.
      3. No double-count: an ETF position held by a partner client appears in exactly one place -- that partner's model_aua -- never also as standalone ETF AUA.
      Negative test: a fixture engineered to produce a negative public_residual must raise ERROR, not pass. Per the ADVI_INFGRO epsilon-discipline + ADHC_VALGATE Class-C framing, a reconciliation residual is measured + surfaced + gated, never silently absorbed.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-transform schema-check ModelPortfolios (the WS-F consumer of the WS-A artifact)</run>
        <expect>The ModelPortfolios.tsx field surface today (stacked AUM chart + getNonModelAumForDate roll-forward) -- so the platinum artifact schema is designed toward what WS-F will consume, not a shape WS-F must adapt around.</expect>
        <if_mismatch>Note the gap; the artifact schema leads, WS-F (Phase 3) conforms -- but a deliberate, recorded design choice, not an accident.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript io [the new aggregation gold script]</run>
        <expect>No COLUMN GAPS (every column the script reads from a convergent-schema feeder is loaded); PORTAL CONSUMERS shows the platinum aggregate-AUA artifact reaching the Model Portfolios downstream.</expect>
        <if_mismatch>Reconcile the load set before closing.</if_mismatch>
      </step>
      <step>
        <run>comp-blast [the aggregation gold function]</run>
        <expect>Blast radius is the new MDPF platinum artifact + the ModelPortfolios consumer only -- no unintended overlap with the live INF gold chain or the SmartX/ETFS pipelines.</expect>
        <if_mismatch>If the script lands in a shared gold/ directory, confirm with COO it does not enter an existing chain's run set unintentionally.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>WS-A defines a contract + builds a NEW aggregation gold script over NEW convergent-schema artifacts; no existing data pipeline producer is modified, no existing artifact is rewritten. The aggregation script runs ad-hoc / fixture-driven at Phase 1-2 (no feeders shipped yet); it enters a scheduled chain only after Phase-2 feeders land -- a later TO.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    WS-A builds a NEW gold script + a NEW platinum artifact -- no file overlap with the live INF gold chain (INFGRO.007/.009, BIWNDW.002, INF_C_02/03) or with the SmartX / ETFS / Eclipse feeder pipelines. The gold-script placement decision (Phase 0) MUST be confirmed with CTO + COO before the Phase-1 build -- if the script lands in an existing pipeline's gold/ directory, it must not silently join that pipeline's chain run set (run comp-blast to confirm). The contract gates WS-B/C/D/E -- COO authors those Phase-2 build TOs against the CTO-ratified WS-A contract; do not pre-author them here. The `firmId` dimension reuses ADVI/ADVI_FIRMSEP semantics -- reuse the identifier, do not modify ADVI.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The convergent per-partner model-AUA schema (section 3.2) is defined as a contract document: field set, types, grain, the holdings[] shape. Phase-0 named gap (2) is addressed -- model_aua is account-grain-attributable, not a bare scalar. The holdings[] shape supports the section-3.3 no-double-count rule. CTO-ratified.</ac>
    <ac id="AC2">The platinum aggregate-AUA artifact schema (sections 3.1 + 3.5) is defined: row grain, first-class `firmId` partner dimension, model/non_model split, the non_model_aua slot documented with the Schwab-only ruling, the section-3.5 reconciliation block. CTO-ratified. No hard-coded partner branch (Cottonwood-ready, section 7-Q5).</ac>
    <ac id="AC3">The aggregation gold script ships: reads convergent-schema feeders, sums per section 3.1 with the `firmId` dimension first-class, emits the platinum artifact + reconciliation block. Produces a valid artifact with zero feeders and a correct aggregate with feeders. Rule 15 compliant; ds-commit-gate exit 0.</ac>
    <ac id="AC4">The three section-3.5 identities are verified against synthetic fixtures (>=2 partners, model + non-model, >=1 shared ETF position); the negative-public_residual fixture raises ERROR, not PASS.</ac>
    <ac id="AC5">The gold-script placement decision (which pipeline's gold/ home + S3 prefix, or a new MDPF home) is recorded and CTO/COO-confirmed. comp-blast confirms no unintended chain-set entry.</ac>
    <ac id="AC6">No emoji; ds-commit-gate exit 0 on every .py edit; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The convergent per-partner model-AUA schema + the platinum aggregate-AUA artifact schema -- a CTO-ratified contract document.
    - The aggregation gold script (section 3.1 decomposition + section 3.5 reconciliation block).
    - The fixture verification of the three reconciliation identities incl. the negative-residual ERROR test.
    - The gold-script placement decision record.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
