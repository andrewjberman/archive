<task_order>
  <metadata>
    <id>ADVI_INFFIN.010</id>
    <slug>dsc-histogram-counts-tax-exposure-followon</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P0 (Andrew empirical 8-defect escalation; partner-visible blank panels) — defects #1/#2/#3a histogram bucket counts empty + #8 Marcia Heck tax_exposure investigation</priority>
    <sla>~1h wall (~30min histogram emit fix + ~15-30min tax_exposure investigation); stack-on-top of INFFIN.003 (no revert)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew empirical 8-defect escalation 2026-05-13 evening; CTO + DE 0.4 joint triage 22:22Z; CTO RAVC1 to DS~C with scope + empirical evidence</ref>
    <ref type="cross_link">Sibling: .003 INFFIN INF emit batch (ALREADY SHIPPED `c5d98d41f` AC1-11 PASS); this is stack-on-top follow-on per CTO routing</ref>
    <ref type="cto_routing">CTO RAVC1 to DS~C 22:23Z with empirical-evidence inventory (partner_analytics_quarterly.json views.geo + views.adv histogram counts=[]); Peter + Joe book.json shape evidence</ref>
  </references>

  <context>
    Andrew empirically reported 8 defects against RD INFFIN.001 + .002 ships. CTO + DE 0.4 joint triage allocated 3 defects to DS~C lane (rest to RD/DE). Stack-on-top routing per CTO (no revert; INFFIN.003 AC1-11 already PASS).

    **Defect #1/#2/#3a — ADV-L0 / Continuous-ADV-AUA / Continuous-ADV-NNA bucket counts missing:**

    Empirical evidence (CTO captured):
    - `s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json` post chain #28 (mtime 2026-05-13 17:47:25Z)
    - `views.geo.current.distribution.total.histogram.counts = []` ← empty array
    - `views.adv.current.distribution.total.histogram.counts = []` ← empty array
    - BUT `percentile_stats` IS emitted in same partition
    - Symptom: ADV-L0 right partition + Continuous-ADV charts render empty (RD .001's GEO-L0 firm-wide fallback works IF geo histogram populated; both empty here)

    RD's .001 ship correctly wired the fallback per TO spec; the upstream emit gap is gold-side. DS~C investigates partner_analytics_quarterly emit logic — likely in INF_D_04 partner_analytics or sibling.

    **Defect #8 — Marcia Heck tax_exposure investigation:**

    Andrew flagged Marcia Heck HH carries unexpected tax_exposure data. Specific empirical not captured in CTO's MCP; need DS~C empirical drill on the HH detail.json + cross-check against expected tax classification for the accounts.

    Possibly:
    - tax_exposure dict emit logic bug in INF_D_02 (DS~C INFFIN.003 BONUS field per AE 0.6.1 chain #28 empirical)
    - OR upstream data classification issue in silver/api_dims/accounts_v2 (account_type assignment)
    - OR legitimate state that needs FE rendering refinement

    DS~C diagnoses + classifies (data fix vs FE fix vs business-logic clarification).
  </context>

  <objective>
    Fix two stack-on-top defects from Andrew's 8-defect escalation routed to DS~C lane:

    1. **Histogram bucket counts emit (defects #1/#2/#3a):** investigate partner_analytics_quarterly.json emit logic; restore bucket counts population in views.geo + views.adv distribution.total.histogram. INF_D_04 partner_analytics (or sibling) is likely emit lane.

    2. **Marcia Heck tax_exposure investigation (defect #8):** empirical drill on HH detail.json + cross-check expected vs actual tax classification; classify root cause (data / FE / business-logic) + propose fix.

    Stack-on-top of INFFIN.003 (NO revert); INF_D_02 + INF_D_04 incremental modify.
  </objective>

  <scope>
    <surfaces>
      <surface id="1+2+3a">Histogram bucket counts emit in partner_analytics_quarterly.json (views.geo + views.adv distribution.total)</surface>
      <surface id="8">Marcia Heck tax_exposure investigation + classify</surface>
    </surfaces>
    <files>
      <file action="investigate">data/orion/scripts/gold/INF_D_04.partner_analytics.py (or wherever histogram emit lives) — bucket counts emit logic</file>
      <file action="modify">INF_D_04 (or sibling) — restore bucket counts in views.geo + views.adv distribution.total.histogram</file>
      <file action="investigate">s3://opal-data-inf/platinum/clients/{marcia-heck-hh}/detail.json — tax_exposure dict empirical</file>
      <file action="investigate">data/orion/scripts/gold/INF_D_02.advisor_client_detail.py — tax_exposure emit logic (your INFFIN.003 BONUS field)</file>
      <file action="cross_check">silver/api_dims/accounts_v2/ — account_type assignment for Marcia Heck accounts</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Surface #1/#2/#3a: locate histogram emit in INF_D_04 (or sibling). Likely pattern: percentile_stats computed + emitted; bucket counts either (a) computed but not emitted (drop in serialization), (b) never computed (emit lane gap), or (c) emitted to wrong dict key.</description>
      <expect>Emit gap localized.</expect>
    </step>
    <step>
      <description>Cross-check chain #27 partner_analytics_quarterly.json (pre-chain #28) — does the bucket counts gap exist there too or is it a chain #28 specific regression?</description>
      <expect>Regression or pre-existing latent identified.</expect>
    </step>
    <step>
      <description>Surface #8: locate Marcia Heck HH (use detail.json grep or accounts_dim filter on client_last_name='Heck'). Pull detail.json + inspect tax_exposure dict.</description>
      <expect>Marcia Heck HH detail.json acquired + tax_exposure inspected.</expect>
    </step>
    <step>
      <description>Surface #8: cross-check expected tax classification against accounts_dim account_type field + business-logic expectation (e.g., is this account taxable / Roth / IRA / 401k?). Classify root cause.</description>
      <expect>Root cause classified: (a) data-side bug, (b) FE rendering issue, (c) business-logic clarification needed.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Surface #1/#2/#3a fix: restore bucket counts emit in views.geo + views.adv distribution.total.histogram. Stack-on-top edit to INF_D_04 (or sibling). NO breaking changes to existing percentile_stats emit.</description>
      <expect>bucket counts populated post-fix; partner_analytics_quarterly.json downstream consumers (RD .001 firm-wide fallback, RD .002 continuous-ADV chart) consume cleanly.</expect>
    </step>
    <step>
      <description>Surface #8: apply fix per classified root cause (data fix in INF_D_02 OR cross-cutting refactor OR document business-logic clarification for FE/Andrew).</description>
      <expect>Marcia Heck tax_exposure renders correctly OR clarification documented.</expect>
    </step>
    <step>
      <description>ds-commit-gate (py_compile + AST + ruff py39 + Rule 15 from __future__ import annotations); safe-deploy SHA-MATCH post-push.</description>
      <expect>PASS.</expect>
    </step>
  </phase>

  <phase id="3" when="empirical-validation">
    <step>
      <description>Post-chain-fire (gates on next chain mode=gold-d or mode=full): empirical re-pull partner_analytics_quarterly.json + verify histogram bucket counts populated for views.geo + views.adv.</description>
      <expect>bucket counts non-empty; FE consumers can render.</expect>
    </step>
    <step>
      <description>Marcia Heck HH detail.json re-pull post-chain + verify tax_exposure rendering classification correct.</description>
      <expect>Surface #8 resolved or clarification surfaced to Andrew.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: INF_D_04 (or sibling) emit fix landed; views.geo + views.adv distribution.total.histogram.counts populated post-chain.
    AC2: Surface #1/#2/#3a empirically verified via partner_analytics_quarterly.json post-chain pull.
    AC3: Marcia Heck tax_exposure classified + fixed OR clarified.
    AC4: Stack-on-top discipline (INFFIN.003 AC1-11 PASS preserved; no revert).
    AC5: ds-commit-gate PASS + safe-deploy SHA-MATCH.
    AC6: Session log captures empirical-test + AC1-5 evidence.
    AC7: MCP RAVC2 to COO with per-surface evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-pipescript io INF_D_04 (column gaps + portal consumers); empirical S3 pulls</phase_1>
    <phase_2>ds-commit-gate.sh on Python edits; safe-deploy SHA-MATCH</phase_2>
    <phase_3>post-chain empirical verification via S3 pulls</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    PARALLEL ACTIVITY (no blocking):
    - RD 0.4.2: .001/.002 stack-on-top fixes (#3b/#4/#5/#6) + .006 wiring released
    - DE 0.4: defect #7 schema drift in getPlatinumAdvisorSummaryStaticInflection + apiRequest NaN-strip
    - DS-base: NaN bug in INF_D_00c lines 526-538 + 556-568 (~15min)
    - AE 0.7: v1.7.56 Lambda mirror P0 (~50min wall; daily cron 06:00 UTC protection)
    - AE 0.6.1: standing by; plan-B cron-flip pre-authorized

    DOWNSTREAM CONSUMER: RD .001/.002 firm-wide fallback + Continuous-ADV chart consume histogram bucket counts.

    NO PORTAL CONFLICT: pure gold-tier emit + post-chain validation.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <chain_fire_needed>
      Gold-emit change requires chain fire to materialize fixed partner_analytics_quarterly.json. Next chain (gold-d or full) materializes; AE 0.6.1 dispatches per existing cadence.
    </chain_fire_needed>
  </data_reprocess_scope>

  <deliverables>
    1. INF_D_04 (or sibling) histogram bucket counts emit fix
    2. Marcia Heck tax_exposure fix or clarification
    3. Single commit under 0.4.0_DS_ClientPlatform~C author per agent identity
    4. ds-commit-gate PASS + safe-deploy SHA-MATCH
    5. Session log with empirical evidence
    6. MCP RAVC2 to COO with scorecard
  </deliverables>

  <ravc>
    DS~C RAVC2 to COO post-AC1-7 PASS. COO ratifies + relays empirical to RD 0.4.2 (their .001/.002 fallback consumes the bucket counts) + Andrew partner-visible status update.
  </ravc>

  <notes>
    **CTO routing source:** CTO RAVC1 to DS~C 22:23Z with empirical evidence (CTO captured the partner_analytics_quarterly.json + book.json shape data). This TO formalizes the dispatch with project-coded TO ID per COO authoring discipline.

    **Stack-on-top discipline:** INFFIN.003 ship `c5d98d41f` is canonical + AC1-11 PASS empirically. This TO modifies INF_D_04 (different script than INFFIN.003's INF_D_02). NO revert needed; pure additive emit fix.

    **Andrew session-direct override:** DS~C authorized for INFFIN scope per Andrew's "DS~A/~B/~C/~D all 4 sub-lanes available" greenlight earlier today.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"` per agent commit identity protocol.

    **Andrew partner-visible impact:** Surfaces #1/#2/#3a unblock the ADV-L0 + Continuous-ADV chart rendering on AdvisorIntelligence; #8 Marcia Heck tax_exposure correctness. RD .001/.002 stack-on-top fixes (#3b/#4/#5/#6) are sibling concerns; both lanes converge on partner-visible defect closure.
  </notes>
</task_order>
