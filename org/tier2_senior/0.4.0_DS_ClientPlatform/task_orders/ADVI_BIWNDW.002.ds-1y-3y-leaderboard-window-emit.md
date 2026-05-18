<task_order>
  <metadata>
    <id>ADVI_BIWNDW.002</id>
    <slug>ds-1y-3y-leaderboard-window-emit</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-15. The 49F D_00c half has no gate -- proceed. The INF_D_00c half: author the window-emit code now, but the INF gold chain run co-sequences with the open INFGRO firm_return_pct_twr fix (same file) -- see cross_domain_coordination. Code authoring is not gated; only the INF chain run coordinates.</dispatch_unblock_condition>
    <project_code>ADVI_BIWNDW</project_code>
    <priority>P1 -- Andrew-directed. The data half of the Books-tab BI window-coverage fix: without 1Y/3Y in leaderboard.json those windows cannot work regardless of the FE.</priority>
    <sla>~4-6h wall (the code is a small symmetric change; the cost is the coverage check and the gold chain runs).</sla>
  </metadata>

  <references>
    <brief>docs/briefs/books-bi-window-coverage-20260515.md (DE 0.4, commit 4bb9e2012) -- section-3a the DATA defect, section-5 the BE implementation table (BE-1..BE-6), section-6 sequencing + the INFGRO coordination note.</brief>
    <directive>Andrew direct 2026-05-15 -- the /Books-tab windowed metrics must re-compute on the BI panel window; 1Y/3Y currently fall back to QTD because the data does not carry those windows.</directive>
    <sibling_to>ADVI_BIWNDW.001 (DE) -- the FE window-coverage fixes. The FE already expects windows['1Y'] and windows['3Y'] (brief FE-3 no-op); this TO produces exactly those keys.</sibling_to>
    <infgro_intersection>The open INFGRO firm_return_pct_twr window-aggregation defect (DE 0.4 finding 2026-05-15, session log b1fd04b30) is in the SAME file as the INF half of this TO -- INF_D_00c.portal_leaderboard.py. It is HELD + routed to CTO. See cross_domain_coordination.</infgro_intersection>
  </references>

  <context>
    platinum/firm/leaderboard.json -- the data source for the /Books-tab advisor-summary metric table -- emits only QTD/YTD/MAX windows for both firms (DE 0.4 verified from S3 2026-05-15). PRODUCER ARCHITECTURE -- DEFINITIVE 2026-05-15 (DS~C full empirical producer trace, COO-confirmed by grep). The two firms have DIFFERENT leaderboard architectures -- the change is NOT symmetric, and this per-firm scope SUPERSEDES the "_window_date_range() in both" framing in BE-1/BE-2 below:
  49F -- data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py builds gold/artifacts/employee_leaderboard.json and ALREADY emits 1Y+3Y (WINDOWS dict, line 59) -- D_00c needs ZERO change. data/black_diamond/scripts/gold/D_04.client_portal_summary.py reads employee_leaderboard.json and DOWN-SELECTS it to platinum/firm/leaderboard.json (the AC3 target; write at line 2417) via the limiter _LEADERBOARD_WINDOWS = ('QTD','YTD','MAX') at line 2192 (build loop line 2316, available_windows line 2392). 49F FIX = widen that tuple to ('QTD','YTD','MAX','1Y','3Y'); the 1Y/3Y data already exists upstream.
  Inflection -- data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py writes platinum/firm/leaderboard.json directly and genuinely hardcodes QTD/YTD/MAX in _window_date_range() (line ~314) + the build loop (line ~1206) + available_windows (line ~1227). Inflection FIX = add the 1Y/3Y branches there (the BE-1/BE-2 change applies AS WRITTEN for the Inflection half only).
  NOTE: data/orion/scripts/gold/D_00c.portal_leaderboard.py is a stale pre-ORNREN Inflection orphan (FIRM_ID='inflection') -- NOT a live producer; do NOT edit it (flagged for cleanup). The DE 0.4 brief mis-traced the 49F chain. This TO adds 1Y and 3Y. The per-metric aggregators (NNA / new-clients / GRO / GRO-decomposition) already take (window_start, window_end) and are window-agnostic -- only the date-range resolver + the build loop are hardcoded, so this is a low-risk symmetric change.
  </context>

  <objective>
    Both orion gold leaderboard producers emit 1Y and 3Y windows in addition to QTD/YTD/MAX, so platinum/firm/leaderboard.json carries windows['1Y'] and windows['3Y'] for both firms -- letting the /Books-tab BI panel's 1Y/3Y selections resolve to real data instead of the silent QTD fallback.
  </objective>

  <scope>
    <item>BE-4 (Phase 0 -- coverage check, GATING): before emitting, verify history depth at the 3Y horizon -- 1Y needs at least 1y silver history; 3Y needs about 3y (holdings partitions back 3y for GRO's _aua_at_start, transaction history for NNA / new-clients). The MAX window already aggregates inception-to-date successfully (brief: Inflection MAX = 293 new clients / $135M NNA) so deep history exists -- but confirm the 3Y horizon explicitly. Same class as the INFGRO.006 MAX-coverage proof. If 3Y coverage is short for a firm, surface to COO before emitting 3Y for that firm.</item>
    <item>BE-1 -- Add 1Y (data_as_of minus 365d) and 3Y (data_as_of minus 1095d) branches to _window_date_range() in BOTH D_00c.portal_leaderboard.py and INF_D_00c.portal_leaderboard.py. Symmetric change.</item>
    <item>BE-2 -- Extend the build loop to ('QTD','YTD','MAX','1Y','3Y') and the available_windows literal, in both scripts. The emitted window keys MUST be exactly '1Y' and '3Y' (uppercase) -- the FE PERIOD_TO_LB_WINDOW map (TO-1 sibling) keys on those exact strings; this is the interface contract.</item>
    <item>BE-3 (no work) -- no per-aggregation change: the NNA / new-clients / GRO / GRO-decomposition aggregators are already (window_start, window_end)-parameterized and window-agnostic. Confirm, do not modify.</item>
    <item>BE-6 -- payload size check: +2 windows is about +60-70% on leaderboard.json. Confirm the file stays under the D_04 / dashboard split-mode threshold; if not, surface to COO.</item>
    <item>BE-5 (document, not fix) -- GRO (aua_growth_pct) is structurally null for MAX (no reliable inception-to-date AUA start) and may be null for 1Y/3Y when no holdings partition sits near the window start; the FE renders an em-dash gracefully. Note this in the deliverable; do not attempt to fix it here.</item>
    <item>SCOPE BOUNDARY: this TO emits the windows in the gold producers. It does NOT touch the FE (TO-1) and does NOT decide the Inflection BI-panel window-option set (product Q1). Emit 1Y + 3Y in BOTH scripts regardless of Q1 -- keeping the two producers symmetric; whether Inflection's panel exposes a 3Y button is an FE/product question that does not change the data.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">BE-4 coverage check run + recorded: 1Y and 3Y history depth confirmed for both firms (or short coverage surfaced to COO before emit).</ac>
    <ac id="AC2">_window_date_range() + the build loop + available_windows extended to QTD/YTD/MAX/1Y/3Y in BOTH D_00c.portal_leaderboard.py and INF_D_00c.portal_leaderboard.py. Window keys emitted as exactly '1Y' / '3Y'.</ac>
    <ac id="AC3">49F: D_00c committed + the 49F gold chain re-run; s3://opal-data-bd/platinum/firm/leaderboard.json carries available_windows [QTD,YTD,MAX,1Y,3Y] with populated windows.</ac>
    <ac id="AC4">Inflection: INF_D_00c window-emit code committed; the INF gold chain run co-sequenced with the INFGRO firm_return_pct_twr fix per cross_domain_coordination (one chain cycle, not two) -- surfaced to COO before the INF chain run. A RAVC2 reporting "INF code committed, chain run held for the INFGRO co-land" is a valid AC4 state. s3://opal-data-inf/platinum/firm/leaderboard.json carries [QTD,YTD,MAX,1Y,3Y] after that run.</ac>
    <ac id="AC5">comp-pipescript io on both scripts (COLUMN GAPS check for the new window aggregations); ds-commit-gate.sh on both .py before commit; payload size confirmed under threshold (BE-6); from __future__ import annotations is the first import (Rule 15). No emoji.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before writing): comp-pipescript io on data/black_diamond/scripts/gold/D_04.client_portal_summary.py (49F) + data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py (Inflection) -- COLUMN GAPS. Phase 2 (before commit): ds-commit-gate.sh on both .py; comp-pipescript deployed before any chain run. Phase 3 (after each chain run): verify leaderboard.json available_windows + windows keys on S3.</compiler_tools_mandate>

  <cross_domain_coordination>
    INFGRO INTERSECTION -- the critical coordination. INF_D_00c.portal_leaderboard.py is also the file of the open INFGRO firm_return_pct_twr window-aggregation defect (DE 0.4 finding 2026-05-15, log b1fd04b30; HELD + routed to CTO; COO-tracked). The brief (section-6) directs: do NOT run two separate INF gold chain cycles. Sequencing:
      - 49F (D_00c): no INFGRO entanglement -- commit + run the 49F gold chain freely as soon as the code + coverage check are done.
      - INF (INF_D_00c): author + commit the 1Y/3Y window-emit code, but DO NOT independently trigger the INF gold chain run. The INF chain run must fold the 1Y/3Y window-emit together with the INFGRO firm_return_pct_twr fix into ONE cycle. Surface to COO when the INF window-emit code is ready; COO signals when the INFGRO disposition lands (CTO-held) so the two changes co-land in one INF chain run. If the same DS owner holds both the INFGRO fix and this TO, fold both edits and run once.
    DS LANE: this TO is for the orion-gold owner -- per the brief, DS~C / base 0.4.0_DS_ClientPlatform, who also owns the INFGRO defect. Pick up accordingly; if a different DS lane takes this, coordinate the INF chain run with the INFGRO owner.
    SIBLING TO-1 (DE): no interface to design -- the FE already keys on '1Y'/'3Y'; emit those exact keys and the FE resolves them (brief FE-3 no-op).
  </cross_domain_coordination>

  <deliverables>
    <item>D_00c + INF_D_00c emitting QTD/YTD/MAX/1Y/3Y; 49F leaderboard.json refreshed; INF window-emit code committed + the INF chain run co-sequenced with the INFGRO fix.</item>
    <item>BE-4 coverage-check result + BE-6 payload-size result recorded in the session log / RAVC2.</item>
    <item>Session log + RAVC2 to COO on AC1-5 (CC the INFGRO owner if a different lane).</item>
  </deliverables>

  <ravc>0.4.0_DS_ClientPlatform RAVC2 to COO on AC1-5.</ravc>

  <notes>
    The brief (4bb9e2012) is authoritative -- DE 0.4 verified the leaderboard.json window sets from S3 and traced the producers; do not re-derive. The change is small + symmetric (the date-range resolver + the build loop); the real cost is the coverage check and the chain runs. The window keys are an interface contract with TO-1 -- emit exactly '1Y' and '3Y'. The single most important thing in this TO: do NOT run the INF gold chain twice -- fold the 1Y/3Y emit with the INFGRO firm_return_pct_twr fix, and surface to COO before the INF chain run. No emoji in code or logs; from __future__ import annotations is the first import (Rule 15).
  </notes>
</task_order>
