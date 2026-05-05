<task_order>
  <metadata>
    <id>ADVI_INFLEC.AUDIT-001</id>
    <project>ADVI_INFLEC</project>
    <title>INFLEC Page-Truth Audit — per-panel × per-field matrix; one decisive deliverable</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <support_agents>0.4.0_DE_ClientPlatform, 0.5.0_AE_OpalETL</support_agents>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>complete</status><!-- Flipped 2026-05-05 by 2.0.0_SA_COO — matrix v3 accepted by CTO RAVC4 (73e6d100d); AC1-6 all PASS; Andrew brief delivered; 5 follow-on TOs (AUDIT-002..006) authored same wake. -->
    <priority>P0 — Andrew priority ("end INFLEC ambiguity NOW"); CTO 1.0.0 directive 20260504T193903Z</priority>
    <estimated_effort>4-6h cycle (Phase 0 panel enumeration ~1h, Phase 1 parallel matrix fill ~3-4h, Phase 2 CTO review ~30min)</estimated_effort>
  </metadata>

  <context>
    Andrew is fed up with INFLEC ambiguity ("either we don't have the data or the mapping is fucked,
    but nobody seems to know"). Three rounds of triage have produced narrative diagnostic memos
    (DS~B IWM gap brief; DE wiring diagnostics; AE chain summaries) — none of which Andrew can scan
    once and decisively know status from. CTO 1.0.0 pivoted to active investigation lead 19:39Z
    with a single design: ONE artifact (per-panel × per-field matrix) that resolves status per cell
    against three independent signals.

    This TO ships that artifact. DS~A leads with empirical-S3 ownership; DE 0.4 fills the
    code-trace mapping column; AE 0.5 supports for missing-data root-cause classification.

    **Hard rule:** NO speculation. Every cell value is backed by evidence (S3 read output, comp-routes
    trace output, code grep with file_path:line, screenshot, or AE Lambda emit log). A cell with
    "looks broken" or "should be working" is REWORK, not COMPLETE.

    Inflection layout config (`portal/src/pages/AdvisorIntelligence/_partners/inflection/layout.ts`):
    - Tabs ENABLED: partnerAnalytics (geo-only), distribution (geo cohort only), books (4 advisor drill: IWM/peter/patrick/joe + InflectionInsightsPanel)
    - Tabs DISABLED: advisors, advisorPublicProfile (Profile tab dead)
    - Distribution cohorts DISABLED: adv, ofc (geo only)

    The matrix scope is the ENABLED surface only — DISABLED panels enter as GRAY status with
    "panel not in scope per layout.ts" rationale.
  </context>

  <objective>
    Produce `docs/architecture/ADVI_INFLEC_AUDIT.md` containing a per-panel × per-field matrix
    covering every panel rendered when firmId=inflection. Each cell is one of:

    - GREEN  — Data ✓ + Mapping ✓ + Render ✓ (panel works end-to-end)
    - YELLOW — Data ✓ + Mapping ✓ but Render bug (frontend defect, no data fix needed)
    - ORANGE — Data ✓ but Mapping broken (frontend wires wrong field; data is fine)
    - RED    — Data missing (S3 artifact missing, empty, or wrong shape; needs DS/AE upstream fix)
    - GRAY   — Panel not in scope per `layout.ts` config (no defect, intentionally disabled)

    Andrew reads the matrix once and decisively knows: which panels work, which need frontend-only
    fixes (YELLOW/ORANGE), which need data fixes (RED), and which are intentionally absent (GRAY).
    Residual RED+ORANGE+YELLOW cells spawn follow-on TOs same wake.
  </objective>

  <scope>
    <panels_in_scope>
      <surface name="Page header">
        <panel>FirmDisplayName + AUA strip + last-update timestamp</panel>
        <panel>Internal "Select Partner" dropdown (visible to internal Opal users only — informational, GRAY for non-internal)</panel>
        <panel>FidelityCustodianBar (custodian metadata footer)</panel>
        <panel>Data Source panel (Orion Connected status + last refresh)</panel>
      </surface>
      <surface name="PartnerAnalytics (firm-level rollup)">
        <panel>Quarterly rollup metrics (clients, accounts, AUA, NNA) — `partner_analytics_quarterly.json`</panel>
        <panel>Geo donut decomposition — `views.geo` (Inflection: geo-only allowedViewModes)</panel>
        <panel>Time-series chart (1Y / 3Y / 5Y / SI windows)</panel>
        <panel>NNA cohort breakdown (radial_12m, period-rolling)</panel>
      </surface>
      <surface name="DistributionTab — geo cohort">
        <panel>Geo donut + table (Inflection: only enabled cohort per layout.ts:27)</panel>
        <panel>Continuous AUA chart per geo</panel>
        <panel>NNA bell curve per geo</panel>
        <panel>Advisor list per geo (capped to 4 per panels.advisorList.maxEntries)</panel>
      </surface>
      <surface name="BooksTab (firm view + advisor drill)">
        <panel>Firm-level books table (clients across all 4 advisor entries)</panel>
        <panel>Drill: Inflection Wealth Management (IWM firm-bucket)</panel>
        <panel>Drill: Peter Lee</panel>
        <panel>Drill: Patrick Scanlan</panel>
        <panel>Drill: Joe Brandenburg</panel>
        <panel>InflectionInsightsPanel (revenueOpsSlot — replaces 49F revenueOps)</panel>
      </surface>
      <surface name="ADV per-advisor drill (each of 4 entries)">
        <panel>book.json — accounts, household count, total AUA</panel>
        <panel>summary.json — quarter rollup</panel>
        <panel>composition.json — asset mix, top holdings</panel>
        <panel>fee_efficiency.json — fee bucket, total fees</panel>
        <panel>top_holdings (ticker classifier output)</panel>
        <panel>radial_12m, NNA cohorts, period_start_aua</panel>
      </surface>
    </panels_in_scope>
    <fields_per_panel>
      For every panel in scope, enumerate every rendered field. Fields = anything with a screen-visible
      value (number, string, donut slice, bar, line). For each field, identify:
      - **Source artifact**: exact S3 key (e.g., `s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json:views.geo.donut`)
      - **Frontend prop**: TypeScript prop name + component file path:line
      - **Expected shape**: type signature from `_shared/types/`
      Empty cells trigger GRAY (out-of-scope) or RED (missing) classification.
    </fields_per_panel>
    <out_of_scope>
      - Advisors tab (disabled in `layout.ts:38`)
      - Profile tab (disabled in `layout.ts:45`)
      - ADV cohort + OFC cohort in Distribution (disabled in `layout.ts:27`)
      - 49F-pattern panels with no Inflection equivalent (e.g., per-office bell curves)
      All four enter the matrix as GRAY rows with rationale citing `layout.ts:LINE`.
    </out_of_scope>
  </scope>

  <coordination>
    <lead agent="0.4.0_DS_ClientPlatform~A">
      <responsibility>Owns matrix file. Fills the **Data present?** column via S3 reads. Cross-references existing INFLEC.json gap log + DS~B's IWM triage findings + DS~D's HISTBF backfill output. Flags every RED cell for AE root-cause classification. Drives matrix to all-cells-resolved.</responsibility>
      <evidence_format>Per cell: `aws s3 cp s3://opal-data-inf/{key} - 2>/dev/null | jq` output OR explicit "key absent (NoSuchKey)". Cite key in matrix; cite jq result OR error in evidence column.</evidence_format>
    </lead>
    <support agent="0.4.0_DE_ClientPlatform">
      <responsibility>Fills the **Mapping correct?** column. For every field DS~A enumerates, traces FE component → API endpoint → response field → expected shape. Logs ORANGE cells when the FE wires the wrong field name OR drops a field that the data provides.</responsibility>
      <evidence_format>Per cell: file_path:line for the prop access + endpoint name (e.g., `getPlatinumPartnerAnalytics`) + expected key from response shape. If mismatched, cite both expected + actual key.</evidence_format>
      <gating>Blocks on DS~A Phase 0 panel enumeration completing. Parallel-fills as DS~A surfaces panels.</gating>
    </support>
    <support agent="0.5.0_AE_OpalETL">
      <responsibility>For every RED cell, classifies root cause as one of: (a) Lambda emit gap (`opal-partners-data` or sibling not emitting field), (b) S3 path issue (wrong prefix, stale ETag), (c) upstream silver/gold gap (DS bronze or silver pipeline missing source data). On-demand, not blocking.</responsibility>
      <evidence_format>Per RED cell: classification (a/b/c) + Lambda log line OR S3 ls output OR pipeline-stage citation.</evidence_format>
    </support>
    <render_column>
      <responsibility>"Render correct?" column populated by Andrew/CTO eyeball OR Playwright screenshot match against the live PROD portal at firmId=inflection. Not part of this TO's pre-commit gate — fills in Phase 2.</responsibility>
    </render_column>
  </coordination>

  <deliverable>
    <path>docs/architecture/ADVI_INFLEC_AUDIT.md</path>
    <structure>
      - § Frontmatter (status, owners, audit-date, related INFLEC blockers)
      - § Methodology (status enum legend, evidence rules, no-speculation rule)
      - § Layout config quick-reference (paste of `layout.ts` enabled/disabled state with file_path:line citations)
      - § Matrix tables (one table per surface in &lt;panels_in_scope&gt;):
        | Panel | Field | Source artifact (S3 key) | Data present? | Mapping correct? | Render correct? | Owner | Status | Evidence |
        |---|---|---|---|---|---|---|---|---|
      - § Residual gaps summary (count by status: GREEN/YELLOW/ORANGE/RED/GRAY) + follow-on TO list
      - § Compiler Tools section (per CLAUDE.md mandate — every comp-* run logged)
    </structure>
    <commit_path>docs/architecture/ADVI_INFLEC_AUDIT.md (CTO architecture-doc lane — DS~A commits with `GIT_COMMIT_AUTHOR_OVERRIDE=ANY_CTO` rationale "joint CTO+COO+DS architecture audit deliverable")</commit_path>
  </deliverable>

  <compiler_tools_mandate>
    <phase id="0" when="Before drafting matrix scaffold">
      <step>
        <run>comp-platinum page AdvisorIntelligence</run>
        <expect>Returns full panel→S3 key trace tree for the AdvisorIntelligence surface. Used to seed the matrix with NO panels missed.</expect>
        <if_mismatch>If output is empty or the partial set surfaced doesn't match the &lt;panels_in_scope&gt; enumeration above, surface to COO before proceeding — implies stale comp graph or new panel since last comp-build.</if_mismatch>
      </step>
      <step>
        <run>comp-routes auth-map | grep -i inflection</run>
        <expect>Lists all CloudFront paths gated on firmId=inflection (FIRM_ALLOWED_PATHS allowlist). Confirms scope of pages-in-scope at the routing layer (cross-check vs panels_in_scope).</expect>
        <if_mismatch>If routes appear that aren't in &lt;panels_in_scope&gt; surface to COO — implies additional Inflection-rendered surfaces (e.g., /cma, /positioning, /macro from W8 cross-firm).</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="Per-cell empirical fill (parallel across DS~A + DE + AE)">
      <step>
        <run>comp-pipescript io [INF script per RED cell when AE classification = (c) upstream gap]</run>
        <expect>Surfaces COLUMN GAPS section. If the RED cell is a missing column on a gold artifact, this run identifies the producing INF_*.py script + the column gap empirically.</expect>
        <if_mismatch>Empty COLUMN GAPS = column is present in gold but Lambda not emitting it (classify as Lambda emit gap, not gold gap).</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check [Component] (per surface — PartnerAnalytics, DistributionTab, BooksTab, InflectionInsightsPanel, FidelityCustodianBar)</run>
        <expect>For every component rendered on Inflection: MISSING/NOTE/UNUSED tally. UNUSED fields with names matching observable Inflection data gaps escalate to ORANGE candidates (mapping bug, FE drops field).</expect>
        <if_mismatch>If MISSING entries surface, those are runtime-undefined cells — auto-RED in matrix.</if_mismatch>
      </step>
      <step>
        <run>comp-cache collisions</run>
        <expect>Zero collisions on Inflection-relevant React Query keys (`partner-analytics`, `firm-leaderboard`, `inflection-insights`, etc.). Collisions indicate ORANGE candidates (cache corruption renders wrong data even when source is correct).</expect>
        <if_mismatch>Any non-zero collision touching an Inflection key → escalate to COO + add ORANGE row to matrix with collision-source citation.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="Pre-commit close">
      <step>
        <run>grep -c "needs investigation\|TBD\|looks like\|might be\|probably" docs/architecture/ADVI_INFLEC_AUDIT.md</run>
        <expect>0 — every cell is either evidence-backed or explicitly GRAY-out-of-scope.</expect>
        <if_mismatch>Any speculation language present → DS~A returns to Phase 1 fill; not closeable.</if_mismatch>
      </step>
      <step>
        <run>wc -l docs/architecture/ADVI_INFLEC_AUDIT.md</run>
        <expect>&gt; 100 lines — reasonable proxy for full matrix coverage of ~5 surfaces × ~5-15 fields each.</expect>
        <if_mismatch>If &lt;100 lines, the matrix is under-enumerated — return to Phase 0.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resources>
      - `s3://opal-data-inf/platinum/**` — DS~A reads (this TO); DS~B IWM triage in flight (separate SSM `a545b9ae`); DS~D HISTBF.004 silver/gold output (just completed). NO write contention.
      - `portal/src/pages/AdvisorIntelligence/_partners/inflection/**` — DE 0.4 reads only (no edits this TO; matrix is doc-only).
      - `docs/architecture/ADVI_INFLEC_AUDIT.md` — NEW file, no contention.
    </shared_resources>
    <coordination_protocol>
      DS~A is matrix file owner — only DS~A commits. DE + AE deliver findings via MCP messages to DS~A; DS~A integrates into matrix. Single-author commits prevent the multi-agent index contamination pattern that hit on 2026-04-27.
    </coordination_protocol>
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="1">
      Matrix file exists at `docs/architecture/ADVI_INFLEC_AUDIT.md` with all 6 surfaces from &lt;panels_in_scope&gt; enumerated as separate § sections, each with a populated table.
    </ac>
    <ac id="2">
      Every cell in the matrix has one of GREEN/YELLOW/ORANGE/RED/GRAY status — no blanks. Speculation language ("might", "looks", "probably", "TBD") returns 0 hits via grep.
    </ac>
    <ac id="3">
      Every non-GRAY cell has an Evidence column entry that is one of:
      (a) `aws s3 cp` output snippet,
      (b) jq result (for JSON shape verification),
      (c) file_path:line citation (for code trace),
      (d) screenshot path (for render verification),
      (e) AE root-cause classification line (for RED cells).
    </ac>
    <ac id="4">
      Residual gaps summary § lists count by status enum AND a follow-on TO list naming proposed scope per RED+ORANGE cell. Follow-on TOs do NOT need to be authored under this TO — listing the scope is sufficient.
    </ac>
    <ac id="5">
      Session log at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-04/ADVI_INFLEC_AUDIT_001_page_truth_matrix.md` includes Compiler Tools section reproducing each `&lt;run&gt;` from `&lt;compiler_tools_mandate&gt;` with observed output + pass/fail vs `&lt;expect&gt;`.
    </ac>
    <ac id="6">
      CTO 1.0.0 reviews matrix and signals close (RAVC pattern). Andrew receives one-MCP summary citing matrix path + status counts.
    </ac>
  </acceptance_criteria>

  <evidence_block>
    <data_reprocess_scope>
      <no_reprocess_needed>
        Audit-only TO. No silver/bronze/gold script edits. No S3 write. No data side effects. Pure
        empirical enumeration + matrix authoring + commit to `docs/architecture/`.
      </no_reprocess_needed>
    </data_reprocess_scope>
  </evidence_block>

  <closure_signal>
    On AC1-5 satisfied: DS~A sends RAVC3 to COO with matrix path + status counts. COO validates
    via the Phase 2 grep + wc gates, then routes to CTO 1.0.0 for final RAVC4 close. Residual
    RED+ORANGE+YELLOW cells become follow-on TOs (DS or DE owner per cell type) authored same
    wake by COO. Andrew receives consolidated brief from CTO citing matrix.
  </closure_signal>
</task_order>
