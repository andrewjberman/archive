# Task Order: ADVI_INFLV2.010 — RD: Option C Smoke Validation — Inflection v2 Layout

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-20260427-advi-inflv2-010</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-27</date>
    <status>open</status>
    <priority>HIGH — final gate before Andrew sign-off on Inflection v2</priority>
  </metadata>

  <objective>
    Full Option C smoke of the Inflection portal against the final INFLV2 state:
      - INFLV2.007 COMPLETE: BooksTab Inflection mode live (firm path, 3-entry advisor list,
        InflectionInsightsPanel)
      - INFLV2.008 COMPLETE: AdvisorsTab + AdvisorPublicProfile suppressed
      - INFLV2.009 COMPLETE: insights artifact live on S3 + CF invalidated
      - INFGRD.003 chain data: $~200M / 3 leaderboard entries on platinum

    This smoke is the definitive pre-production validation. RAVC from this task is the
    final gate before COO dispatches Andrew sign-off request.
  </objective>

  <scope>
    <task id="1" label="Gate check">
      Confirm all three gate RACVs received before starting smoke:
        1. DE RAVC from INFLV2.007 (BooksTab Inflection mode)
        2. DE RAVC from INFLV2.008 (AdvisorsTab suppressed)
        3. AE RAVC from INFLV2.009 (insights artifact + CF invalidated)
      Do NOT start smoke until all three received.
    </task>

    <task id="2" label="Option C smoke — full panel pass">
      Login as Andrew at opalinvest.dev, select Inflection in partner dropdown
      (AdvisorIntelligence/index.tsx firmId=inflection path).

      PARTNER ANALYTICS TAB (firm landing):
        - Header tiles: total AUA ~$200M, NMNC/NMEC/Existing radial renders non-zero
        - Period bars + GRO: renders quarterly bars at ~$200M scale
        - Mix: area chart renders with non-empty segments
        - NNA chart: renders correctly

      DISTRIBUTION TAB:
        - Present in nav
        - Geo cohort: shows stub / empty-state with placeholder copy (NOT an error)
        - Adv cohort: renders if data present
        - OFC option: NOT present (config-suppressed)

      BOOKS TAB:
        - Firm Overview panels render
        - Advisor list: exactly 3 entries (Inflection Wealth Management, Peter Lee,
          Patrick Scanlan). No other entries. No Keil entries.
        - ClientsList renders directly (no advisor-drill nav step visible)
        - InflectionInsightsPanel renders in Revenue Ops slot (NOT FeeEfficiencyPanel)
        - FeeEfficiencyPanel: NOT visible for firmId=inflection

      ADVISORS TAB:
        - NOT present in tab navigation for firmId=inflection

      ADVISOR PUBLIC PROFILE (non-admin):
        - NOT accessible / suppressed for firmId=inflection

      CONSOLE + NETWORK:
        - Zero JavaScript errors in console
        - No 404s or 5xx on platinum S3 key fetches
        - No HTML responses where JSON expected
    </task>
  </scope>

  <acceptance_criteria>
    <criterion id="1">
      PartnerAnalytics: AUA ~$200M (within $140M–$250M range). NMNC/NMEC/Existing
      radial non-zero. Period bars render.
    </criterion>
    <criterion id="2">
      Distribution: present in nav. Geo stub renders. OFC absent.
    </criterion>
    <criterion id="3">
      Books: exactly 3 advisor entries (IWM, Peter, Patrick). ClientsList renders
      directly. InflectionInsightsPanel renders. FeeEfficiencyPanel absent.
    </criterion>
    <criterion id="4">
      Advisors tab: NOT present in nav.
    </criterion>
    <criterion id="5">
      Zero JavaScript console errors. No unexpected 4xx/5xx.
    </criterion>
    <criterion id="6">
      RAVC sent to 2.0.0_SA_COO with:
        - PASS/FAIL verdict per tab (table format)
        - Actual AUA value observed
        - Actual advisor list entries observed
        - InflectionInsightsPanel: renders / blank / error
        - Console error count
        - Any FAIL items: panel name + observed vs expected
      Subject: RAVC — ADVI_INFLV2.010 [PASS|FAIL] | $[X]M AUA | Inflection v2 smoke
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT start until all three gate RACVs confirmed (.007 + .008 + .009).</constraint>
    <constraint>If AUA reads $429M instead of ~$200M, it is a CF cache miss — trigger
    CF invalidation and re-check before declaring FAIL.</constraint>
    <constraint>UNREACHABLE paths (AdvisorsTab, advisor drill, AdvisorPublicProfile) are
    pre-suppressed by INFLV2.008 — do NOT open defects against them; mark as SUPPRESSED PASS.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_INFLV2.007" status="open"
                note="BooksTab Inflection mode live."/>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_INFLV2.008" status="open"
                note="AdvisorsTab suppressed."/>
    <dependency agent="0.6.1_AE_PartnerETL" task="ADVI_INFLV2.009" status="open"
                note="Insights artifact live on S3 + CF invalidated."/>
  </dependencies>

  <deliverables>
    <deliverable type="mcp">RAVC to 2.0.0_SA_COO with full panel-by-panel verdict table.
    This is the Inflection v2 production sign-off gate.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md §10 (acceptance criteria)</ref>
    <ref type="portal">opalinvest.dev — Option C: login as Andrew + Select Partner → inflection</ref>
  </references>
</task_order>
```
