<task_order>
  <metadata>
    <id>ADVI_BIWNDW.001</id>
    <slug>de-fe-window-coverage-fixes</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-15. Backend-independent -- no gate. All three changes (FE-1/FE-2/FE-4) ship against the leaderboard.json windows that already exist; nothing here waits on TO-2.</dispatch_unblock_condition>
    <project_code>ADVI_BIWNDW</project_code>
    <priority>P1 -- Andrew-directed. Restores the Max window for both firms immediately (a pure FE typo) and makes Inflection's BI panel actually drive its metric table. Highest value-per-effort in the brief.</priority>
    <sla>~2-3h wall.</sla>
  </metadata>

  <references>
    <brief>docs/briefs/books-bi-window-coverage-20260515.md (DE 0.4, commit 4bb9e2012) -- section-3 root cause, section-4 the FE implementation table (FE-1..FE-5), section-7 product questions. DE 0.4 is the brief author and the implementer of this TO.</brief>
    <directive>Andrew direct 2026-05-15: the /Books-tab windowed metrics (NNA/GRO/New Clients/Rank) must re-compute on the "Business Intelligence" panel window. DE 0.4 analyzed both partners and routed the brief to COO for decomposition.</directive>
    <sibling_to>ADVI_BIWNDW.002 (DS) -- the 1Y/3Y leaderboard window emit. FE-3 (no-op): once TO-2 lands 1Y/3Y in the data, the existing trailing_1y to '1Y' / trailing_3y to '3Y' map resolves with NO further FE work. This TO does not wait on TO-2.</sibling_to>
  </references>

  <context>
    In the /Books tab (BooksTab, exported from portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx -- shared by both partners) the advisor-summary metric table is meant to re-compute on the window picked in the "Business Intelligence" panel. It does not. The brief (section-3) found three defects; this TO fixes the two that are pure frontend and adds the defensive state. The DATA defect (leaderboard.json lacks 1Y/3Y) is TO-2 (DS) and is NOT in this TO -- but FE-1 and FE-2 have ZERO dependency on TO-2 and ship now. COO has ruled brief Q3 (can FE-1/FE-2 ship ahead of the backend work): YES -- that is the structure of this TO.
  </context>

  <objective>
    The /Books-tab "Business Intelligence" window selector drives the advisor-summary metric table for every window the data supports -- Max works for both firms, Inflection's selector is wired, and any window the data does not yet carry shows an explicit unavailable state instead of silently rendering QTD numbers under the wrong label.
  </objective>

  <scope>
    <item>FE-1 -- Fix the PERIOD_TO_LB_WINDOW map in ClientsTab.tsx (~L346): max:'3Y' is a typo, change it to max:'MAX'. The MAX window data already exists in leaderboard.json -- this one-line fix restores the Max window for BOTH firms immediately, with zero backend dependency. (brief section-3b / section-4 FE-1)</item>
    <item>FE-2 -- Wire Inflection's window selector to feePeriod. Inflection renders InflectionInsightsPanel (passed as revenueOpsSlot) instead of FeeEfficiencyPanel, so its window never reaches BooksTab. Add onPeriodChange?:(w)=>void to InflectionInsightsPanelProps; inject it from BooksTab via the existing cloneElement mechanism (ClientsTab L573-578 already injects onHouseholdClick the same way); map InflectionInsightsPanel's Window (qtd/ytd/1y/max) to FeeEfficiencyWindow (qtd/ytd/trailing_1y/max). (brief section-3c / section-4 FE-2)</item>
    <item>FE-4 -- Replace the silent QTD fallback with an explicit state. Today when employeeLbData.windows[lbKey] is missing, the windows[available_windows[0]] fallback resolves to QTD and the table renders QTD data under the selected window's label -- this is what hid the bug. Instead: when the selected window's data is absent, disable that toggle option (or show an explicit "window unavailable") rather than render mislabeled QTD data. Note this is data-driven and self-correcting -- once TO-2 lands 1Y/3Y those options light up automatically with no further FE change. (brief section-4 FE-4)</item>
    <item>SCOPE BOUNDARY: FE-5 (window-set reconciliation -- whether Inflection's BI panel gains a 3Y option) is NOT in this TO -- it is deferred pending Andrew's product call (brief section-7 Q1). FE-3 is a no-op (the trailing_1y/trailing_3y map entries are already correct). Do not change the InflectionInsightsPanel window-option set in this TO.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">FE-1: PERIOD_TO_LB_WINDOW max maps to 'MAX'. Selecting Max in the BI panel renders the MAX-window metrics for both 49F and Inflection (MAX data exists in both leaderboard.json files).</ac>
    <ac id="AC2">FE-2: changing the window in Inflection's "Business Intelligence" panel (InflectionInsightsPanel) re-computes the advisor-summary metric table -- QTD/YTD/Max all drive the table. The window lift uses the existing cloneElement injection pattern.</ac>
    <ac id="AC3">FE-4: selecting a window whose data is absent from leaderboard.json shows an explicit unavailable state (disabled option or explicit message) -- the table never renders QTD data under a different window's label. Behavior is data-driven (re-enables automatically when TO-2 lands 1Y/3Y).</ac>
    <ac id="AC4">comp-transform schema-check on BooksTab / FeeEfficiencyPanel / InflectionInsightsPanel -- clean (MISSING = runtime undefined). comp-cache collisions if any fetch/key is touched (firm-leaderboard is a shared dedup key -- do not break it). No emoji in any portal code. Portal builds clean.</ac>
    <ac id="AC5">Shipped to portal DEV; portal submodule pointer handled per the standard DT review. FE-5 explicitly NOT done (deferred, product Q1).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before writing): comp-transform schema-check on BooksTab, FeeEfficiencyPanel, InflectionInsightsPanel. Phase 2 (before commit): comp-transform schema-check re-run clean; comp-cache collisions if a fetch/key was touched. Phase 3 (after): visual verify in /frontend-dev or a browser smoke -- Max works for both firms, Inflection selector drives the table.</compiler_tools_mandate>

  <cross_domain_coordination>
    Sibling TO-2 (ADVI_BIWNDW.002, DS) lands 1Y/3Y in leaderboard.json. This TO does NOT wait on it -- FE-1/FE-2 ship against existing data; FE-4 is the defensive state for the windows TO-2 has not landed yet. When TO-2 lands, 1Y/3Y resolve automatically (FE-3 no-op). No interface to design -- the windows dict shape and the '1Y'/'3Y' key names are pre-existing; the brief documents them.
    Andrew product question Q1 (window-set unification) gates FE-5 only -- surfaced to Andrew by COO; do not block on it.
  </cross_domain_coordination>

  <deliverables>
    <item>FE-1 + FE-2 + FE-4 shipped to portal DEV; comp-transform schema-check clean; visual smoke.</item>
    <item>RAVC2 to COO on AC1-5.</item>
  </deliverables>

  <ravc>0.4.0_DE_ClientPlatform RAVC2 to COO on AC1-5.</ravc>

  <notes>
    The brief (4bb9e2012) is authoritative -- DE 0.4 authored it with full file/line refs; do not re-derive. FE-1 is the highest value-per-effort item in the whole brief (a one-line typo that restores Max for both firms). Ship FE-1/FE-2/FE-4 together -- after this TO the Books tab is honest: Max works, Inflection responds, and unsupported windows say so instead of lying with QTD data. FE-5 is the only FE item that needs a product answer (Q1) -- out of scope here. No emoji in portal code.
  </notes>
</task_order>
