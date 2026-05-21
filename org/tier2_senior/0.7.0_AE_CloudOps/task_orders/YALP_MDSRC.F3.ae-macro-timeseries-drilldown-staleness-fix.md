<task_order>
  <metadata>
    <id>YALP_MDSRC.F3</id>
    <slug>ae-macro-timeseries-drilldown-staleness-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — COO-issued, sibling of YALP_MDSRC.F2. Surfaced by the F1 audit's Finding F7 (added to the F1 brief in response to an Andrew follow-up). 0.7.0_AE_CloudOps already holds F2 (the sibling yield_curve staleness fix) — F3 may be batched with F2 as one macro-pipeline-staleness pass (the execution batching is your call; the TOs stay distinct for clean RAVC tracking). No gate — standalone defect fix, independent of the YALP migration.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — a live user-visible data inconsistency on the Macroeconomics page (a drill-down chart ending January next to a heatmap row showing May). Not the migration; worth fixing now.</priority>
    <sla>~0.5 effort-day — the core fix is a config-list extension + an orphan-file delete + a yang-generator redeploy. The unemployment_rate depth check is a small added investigation.</sla>
  </metadata>

  <references>
    <f1_brief>docs/briefs/mdsrc-fred-macro-sourcing-audit-20260520.md — the F1 FRED macro-sourcing audit (0.2.0_DS~A). Finding F7 is in brief §2.4 + recommendation §5.4 (committed 2736610b5). §2.4 carries the exact enumeration of the 15 missing indicators — that section IS the spec for this TO.</f1_brief>
    <f2_sibling>YALP_MDSRC.F2 (0.7.0_AE_CloudOps) — the sibling fix: yield_curve_fred.json ~4-month staleness. F2 + F3 + F1's own findings are the user-visible-stale-data cluster on the Macroeconomics page; F1-brief §5.4 groups them.</f2_sibling>
    <generator>The yang-generate-macro-timeseries generator — its hardcoded INDICATORS list is the defect locus. Phase 0 locates it (comp-pipescript io yang-generate-macro-timeseries).</generator>
  </references>

  <context>
    Andrew asked a follow-up on the F1 audit: do we have the Macroeconomics drill-down modal data for all indicators, with a 40-year lookback. DS~A probed S3 (json/macro/timeseries/) and surfaced Finding F7, now in the F1 brief:
    - COVERAGE is fine — all 79 served indicators have a timeseries file (the modal resolves every click). There are 80 files: 79 + 1 ORPHAN from an old slug scheme.
    - STALENESS — the defect: 16 of 80 files are ~4 months stale, frozen 2026-01-12, while the other 64 refresh weekly. The yang-generate-macro-timeseries INDICATORS list has only 64 entries; the 15 indicators NOT in the list never regenerate. Result: clicking DXY shows a chart ending 2026-01-09 while the heatmap row beside it shows May — a visible internal inconsistency. Same failure class as F1 (config list shorter than the rendered set) and the F2 yield-curve staleness.
    - LOOKBACK — history is 1990->2026, ~36 years (~437 monthly points), NOT 40. This is a SOURCE limit: the Bloomberg data_pkl price_monthly starts ~1990. It is not a fixable defect — it is documented here as the answer to Andrew's 40-year question; do not chase it.
    - DEPTH — uneven: unemployment_rate carries only 145 points vs the ~432 expected for a monthly series back to 1990 (gdp_qoq's 145 IS correct — GDP is quarterly). This one warrants a quick check (generator bug vs source limit).
    The 15 missing indicators (per DS~A / brief §2.4): the 5 Currency series + Factory Orders + Trade Balance + TIC Flows + Unit Labor Cost + Retail ex-Auto (x2) + Vehicle Sales + S&P PMI (x2) + Fed NLP. Confirm the exact set against brief §2.4.
  </context>

  <scope>
    <scope_amendment note="COO-authorized 2026-05-20 — F3 P2 finding supersedes the F1-F7 orphan diagnosis">
      AE's F3 P1 deployed the INDICATORS 64->79 extend (yang-v2.4.5) — fixed 13/15. P2 found the root cause is bigger AND the F1-brief F7 mis-diagnosed the "orphan": fed_balance_sheet_as_pct_of_gdp.json is NOT an orphan — it is the file the frontend ACTIVELY REQUESTS (MacroTimeSeriesModal.tsx computes the slug client-side). The real defect is a GENERATOR-vs-FRONTEND slugify divergence: the generator's slugify maps & / % to '_' (writes s_p_pmi_*, fed_balance_sheet_as_of_gdp) while the frontend slugify (MacroTimeSeriesModal.tsx:187) maps & -> "and", % -> "pct" (requests sandp_pmi_*, fed_balance_sheet_as_pct_of_gdp). Mismatch on every name with & or %.
      F3 SCOPE AMENDED: (1) align the generator's slugify() to the frontend's (& -> "and", % -> "pct", / and - -> "_") — a small generator code change + one redeploy + re-invoke. (2) The "delete the orphan" step is RE-SCOPED: do NOT delete fed_balance_sheet_as_pct_of_gdp.json (it is live) — the genuine orphans are the generator's OWN wrong-slug outputs (s_p_pmi_manufacturing.json, s_p_pmi_services.json, fed_balance_sheet_as_of_gdp.json); zero-consumer-check EACH (the consumer is a runtime-computed slug, not a literal — verify the frontend requests the sandp_pmi_/as_pct_of_ form, not these) before deleting. The original do_not "confirm zero live consumers first" is what correctly caught this — it stands.
    </scope_amendment>
    <in_scope>
      PHASE 0 (locate + confirm): locate the yang-generate-macro-timeseries generator + its INDICATORS list (comp-pipescript io yang-generate-macro-timeseries). Confirm the 64-entry list + the exact 15 missing indicators against F1-brief §2.4. Identify the orphan timeseries file (the 80th, from the old slug scheme). Confirm the deploy mechanism for this yang generator.
      PHASE 1 (fix):
      - Extend the INDICATORS list 64 -> 79 so every served indicator regenerates on the weekly refresh. Add exactly the 15 missing indicators per brief §2.4 — no more, no fewer.
      - Delete the orphan timeseries file (the stale 80th, no live consumer).
      - Redeploy the yang-generate-macro-timeseries generator Lambda via terraform (CLAUDE.md Rule 1 / safe-apply).
      PHASE 2 (verify):
      - Trigger or await one generation run; confirm all 79 timeseries files refresh to a current date (the previously-frozen 16 included).
      - Confirm the DXY-vs-heatmap inconsistency is resolved.
      DEPTH CHECK (small, secondary): investigate the unemployment_rate shallow depth (145 vs ~432 points). If it is a generator bug (e.g. a wrong source column or a truncated window), fix it within this TO; if it is a genuine source limit, document it and move on. Do not let this expand the TO — timebox it.
    </in_scope>
    <out_of_scope>
      - The 40-year lookback — it is a Bloomberg-source limit (data_pkl starts ~1990); not fixable, already answered. Do not chase it.
      - The F2 yield_curve fix — separate sibling TO (though you may batch the execution).
      - The FRED migration + the other F1 findings — they ride into v0.4 / the FRED implementation TO.
      - Any portal-frontend change — the modal renders fine; this is a data-staleness fix only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the fix">
      <step>
        <run>comp-pipescript io yang-generate-macro-timeseries</run>
        <expect>The load list + COLUMN GAPS + portal consumers for the generator — locate the INDICATORS list accurately and confirm the consumer set (the MacroTimeSeriesModal drill-down).</expect>
        <if_mismatch>If not a comp-graph node, fall back to a direct source read of infra/aws/lambda/v2_portal/yang_pipeline/ + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh on the generator file</run>
        <expect>All three checks exit 0 (py_compile + ds-precommit-check + ruff py39).</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after deploy">
      <step>
        <run>comp-pipescript deployed yang-generate-macro-timeseries + verify the terraform plan is 0-diff + check the refreshed artifact dates</run>
        <expect>Runner has the committed code (MATCH); 0-diff; all 79 timeseries files carry a current date.</expect>
        <if_mismatch>STALE/MISSING -> redeploy; if files still frozen -> re-investigate before signalling done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Sibling of F2 (same agent, same Macroeconomics-page-staleness theme) — batch the execution if efficient. The orphan-file delete is an S3 object deletion — confirm zero live consumers before deleting (a deletion is a confirm-first operation). No other active TO touches the yang macro generators. RAVC2 feeds v0.4 context.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase 0: the yang-generate-macro-timeseries INDICATORS list located; the 64-entry list + the exact 15 missing indicators confirmed against F1-brief §2.4; the orphan file identified; the deploy mechanism confirmed.</ac>
    <ac id="AC2">Phase 1: the INDICATORS list extended 64 -> 79 (exactly the 15 per §2.4); the orphan timeseries file deleted (zero live consumers confirmed first); the generator Lambda redeployed via terraform (full cycle: commit -> plan -> safe-apply -> 0-diff -> tag -> push --follow-tags).</ac>
    <ac id="AC3">Phase 2: all 79 drill-down timeseries files confirmed refreshed to a current date; the DXY-vs-heatmap internal inconsistency resolved.</ac>
    <ac id="AC4">The unemployment_rate depth investigated: a generator bug fixed within this TO, or a source limit documented. Timeboxed — does not expand the TO.</ac>
    <ac id="AC5">Phase-1 comp-pipescript io + Phase-2 ds-commit-gate + Phase-3 comp-pipescript deployed + 0-diff reproduced in the session log Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The extended INDICATORS list + the orphan-file delete + the redeployed yang-generate-macro-timeseries generator; git tag.
    - The unemployment_rate depth finding (fix or documented source limit).
    - Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT chase the 40-year lookback — it is a Bloomberg-source limit, already answered; F3 does not extend history.</rule>
    <rule>Do NOT deploy via console or aws lambda update-function-code — terraform via safe-apply (CLAUDE.md Rules 1 + 18).</rule>
    <rule>Do NOT delete the orphan file without first confirming zero live consumers (a deletion is confirm-first).</rule>
    <rule>Do NOT let the unemployment_rate depth check expand the TO — timebox it; if it is a deep issue, document + surface to COO rather than chasing it here.</rule>
    <rule>No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
