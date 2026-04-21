<task_order>
  <metadata>
    <id>ADVI_STAUDT.COHORT-A</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <lane_preference>~D (or whichever DS lane is idle post-chain-full recovery per CTO 2026-04-21T15:50Z ACK)</lane_preference>
    <co_owner>0.4.0_DE_ClientPlatform (portal footnote display, sub-deliverable inline)</co_owner>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P2 — small transparency surface. Headline summary only. NO gold-runner filter changes. Scoped to Cohort A (599 accts / $44.7M dropped silver→canonical).</priority>
    <sla>Combined ~4h (DS emit ~2-3h + DE footnote display ~1h)</sla>
    <decision_authority>Andrew 5-item walkthrough 2026-04-21 PM per CTO session log `org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md` §1. Commit `0a37d545`.</decision_authority>
  </metadata>

  <references>
    <ref type="decision_record">org/tier1_exec/1.0.0_SA_CTO/logs/2026-04-21/session36_five_item_decisions.md §1</ref>
    <ref type="killed_brief">docs/briefs/aua_active_account_filter_redesign.md — DELETED in `0a37d545`. Multi-signal active-account detector proposal KILLED; replaced with THIS TO (headline summary only).</ref>
    <ref type="prior_investigation">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/aua_active_filter_investigation_and_brief.md (preserved as research record)</ref>
    <ref type="project_json">org/projects/ADVI_STAUDT.json (phase updated `0a37d545`)</ref>
    <ref type="cohort_definition">Cohort A = 599 accounts / $44.7M dropped between `silver/allocations[d]` and `gold/canonical/holdings[d]`. These accounts BD sees but we drop during canonical normalization. DISTINCT from Cohort B (166 accts / $41M BD-excluded-by-account-type: SLATs/DAFs/HSAs/PCRAs — UNTRACKED per 2026-04-20 "we don't track that" decision, NOT in scope here).</ref>
  </references>

  <objective>
    Emit a headline summary artifact describing Cohort A (599 accounts dropped silver→canonical) as a D_04 output for portal footnote display. Users see a small transparency footnote on the firm overview / leaderboard surfaces explaining "$44.7M across 599 accounts dropped during canonical normalization" with headline breakdowns (AUA, client count, state distribution, top-N named).

    **EXPLICIT SCOPE LOCK:** NO changes to A_03 / B_00 / C_01 filter logic. NO new `gold/canonical/account_activity/` artifact. NO multi-signal detector. NO re-inclusion of Cohort A into canonical AUA. This is pure transparency reporting on accounts we CHOSE to drop — their exclusion remains correct.
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py — add Cohort A summary computation + emit `gold/platinum/firm/cohort_a_summary.json` (or equivalent key; DS picks final path in Phase 0)</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add validator block for the new artifact (field presence + non-zero count + $44.7M ±5% AUA sanity)</file>
      <file action="read-only">data/black_diamond/scripts/silver/*.py (for cohort A identification logic — silver side of the silver→canonical drop)</file>
      <sub_deliverable owner="0.4.0_DE_ClientPlatform">portal/src/* — wire the `cohort_a_summary.json` artifact into the firm overview / leaderboard footer as a small transparency footnote. Scope: single small text-with-tooltip component. No new tab, no new chart.</sub_deliverable>
    </files>
  </scope>

  <deliverables>
    <deliverable id="cohort-a-identification">
      DS derives Cohort A = accounts present in `silver/allocations[latest_date]` (active BD accounts with non-zero `cash_market_value + amv`) but absent from `gold/canonical/holdings[latest_date]`. Expected baseline: ~599 accounts / ~$44.7M AUA (CTO session log §1 figures; exact count may drift ±10% with silver refresh).
    </deliverable>
    <deliverable id="summary-artifact-emission">
      D_04 emits `gold/platinum/firm/cohort_a_summary.json` (DS may propose alternate key — flag at Phase 0) with headline fields:
      - `account_count` (int) — total accts in Cohort A
      - `total_aua` (float) — sum of `cash_market_value + amv` from silver
      - `client_count` (int) — derived via `household` / `rep_id` grouping in `silver/accounts` or dimensional table
      - `state_distribution` (array of `{state, count, aua}`) — joined via `silver/accounts` or dim table; `client_state` lives on client, not account
      - `top_n_named` (array of `{account_label, aua}`) — top 20 by AUA for portal footnote display; respect PII/pseudonymization pattern per `memory/feedback_aua_term_definitions.md`
      - `snapshot_date` (date) — the silver date cohort was computed against
      - `methodology_note` (short string) — e.g., "Accounts active in BD silver that are excluded during canonical normalization due to [reason]. See session log for full methodology."
    </deliverable>
    <deliverable id="validator-config">
      Add validator block to `gold_validate_config.yaml` for the new artifact:
      - Required-fields presence check (all 7 headline fields exist)
      - `account_count > 400 AND < 900` (WARN if outside; hard-fail at ERROR only if 0 or >2000)
      - `total_aua > 30_000_000 AND < 60_000_000` (WARN if outside; hard-fail if 0 or negative)
      - `state_distribution` non-empty; sum of state counts ≈ `account_count` (tolerance ±3 for unknown-state)
      - `top_n_named.length == 20` (or documented alternate N)
    </deliverable>
    <deliverable id="de-portal-footnote" owner="0.4.0_DE_ClientPlatform">
      Wire `cohort_a_summary.json` into portal as a small transparency footnote on firm overview page footer (or leaderboard footer — DE picks most natural placement). Display:
      - 1-line headline: e.g., "Note: $44.7M across 599 accounts excluded during normalization."
      - Hover/tooltip OR small expander reveals: client count, state top-3, top-5 named, methodology note.
      - Do NOT surface top_n_named inline unless gated by appropriate permission (follow existing RBAC patterns for PII-adjacent displays).
      - Minimal component, no new tab, no new chart, no new API endpoint (artifact consumed via existing platinum/firm/ route if available — check `comp-platinum reverse cohort_a_summary`).
    </deliverable>
  </deliverables>

  <wire_contract>
    - Zero impact on canonical AUA. Firm total_aua remains $1,646.4M (post B_01 cap) — Cohort A is NOT re-included.
    - Zero impact on leaderboards, charts, or existing per-advisor attributions. The summary artifact is a separate, read-only transparency feed.
    - One new S3 key under `gold/platinum/firm/` (or equivalent). Existing artifacts untouched.
    - Portal footnote is a cosmetic addition — no state change, no filter change, no new query key (reuses existing firm-overview data fetch if co-located).
  </wire_contract>

  <acceptance_criteria>
    1. `D_04.client_portal_summary.py` emits `cohort_a_summary.json` with all 7 headline fields populated.
    2. `account_count` between 400-900 (expected ~599 ±silver drift).
    3. `total_aua` between $30M-60M (expected ~$44.7M).
    4. `comp-validate D_04 --artifact /tmp/cohort_a_summary.json` exits 0 (new validator block added to `gold_validate_config.yaml` in same commit).
    5. `state_distribution` sums to `account_count ±3` (accommodating unknown-state).
    6. `top_n_named` respects pseudonymization pattern per `memory/feedback_aua_term_definitions.md` — real names only where PII rules allow.
    7. Sub-deliverable: DE portal footnote displays on firm overview (or leaderboard) footer; click/hover surfaces breakdown. Screenshot + `/frontend-dev` acceptance captured in DE session log.
    8. Session log reproducing every `<run>` from `<compiler_tools_mandate>` with observed output + pass/fail vs `<expect>`.
    9. NO changes to A_03 / B_00 / C_01 / filter logic / `gold/canonical/` shape. Verified via `git diff --stat` scope check pre-commit.
    10. MCP COMPLETE to COO citing commit hash + artifact key + screenshot.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_04</run>
        <expect>READS include silver/allocations + silver/accounts (for Cohort A derivation). WRITES lists existing platinum/firm/* keys. No COLUMN GAPS on current state.</expect>
        <if_mismatch>If silver/allocations not in READS, add it to D_04's load list (this is a new consumer pattern). Document the new READ in session log.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_04</run>
        <expect>Downstream = existing platinum consumers (firm overview, leaderboard, role_breakdown). No new portal components expected yet (footnote is display-only, consumes existing data fetch).</expect>
        <if_mismatch>If new downstream appears, flag to COO before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse cohort_a_summary (or chosen final key)</run>
        <expect>No current consumers (it's a new artifact). Confirms the key is new, not colliding with existing.</expect>
        <if_mismatch>If collision, pick a different key name.</if_mismatch>
      </step>
      <step>
        <run>Cohort A definition sanity: `python -c "from data.black_diamond.scripts.... ; count_cohort_a()"` (or equivalent scripted check) against latest silver</run>
        <expect>~599 accts ±10% / ~$44.7M AUA ±10%. Matches CTO session log §1 baseline figures.</expect>
        <if_mismatch>If count diverges materially (e.g., 50 or 5000), silver has shifted or methodology is wrong. Debug before emitting artifact.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>`python -c "import ast; ast.parse(open('data/black_diamond/scripts/gold/D_04.client_portal_summary.py').read())"` AND `python -c "import importlib.util; ..."` (HLOT2 standardization pattern)</run>
        <expect>Both exit 0. Catches latent NameError / missing import / top-level ImportError — same-class defense as 081223b5 / 048a6fa3.</expect>
        <if_mismatch>STOP. Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/cohort_a_summary.json</run>
        <expect>Exit 0. All ERROR checks pass (new validator block included).</expect>
        <if_mismatch>STOP. Do not commit until ERROR clean.</if_mismatch>
      </step>
      <step>
        <run>git diff --stat</run>
        <expect>Only D_04.client_portal_summary.py + gold_validate_config.yaml + session log touched. NO A_03/B_00/C_01/canonical/filter-logic diffs.</expect>
        <if_mismatch>Scope leak — revert extra file edits before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast D_04 (post-commit)</run>
        <expect>Same consumer set as Phase 1. If new consumer appeared, it's either the new artifact reader (expected, if comp-platinum picked it up) or an unintended new downstream (investigate).</expect>
        <if_mismatch>Unexpected downstream = flag to COO.</if_mismatch>
      </step>
      <step>
        <run>DE sub-deliverable: `/frontend-dev` on the footnote component</run>
        <expect>Component renders at expected footer position; footnote text + tooltip/expander work; top-N list respects RBAC; screenshot PASS.</expect>
        <if_mismatch>Fix per `/frontend-dev` actionable fixes block; iterate up to 5 times.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>Zero coordination with other active TOs. D_04 is touched; no other active TO touches D_04 simultaneously.</item>
    <item>DE sub-deliverable waits for DS artifact emission + commit. DE starts once DS MCPs artifact-ready.</item>
    <item>NO coordination with STAUDT.CHART-ALIGN (different surface — CHART-ALIGN touches D_00c leaderboard cutover; COHORT-A touches D_04 summary emission). Parallel-safe.</item>
    <item>Cohort A re-derivation methodology must preserve the silver→canonical drop rationale. If DS discovers the drop reason is inadvertent (e.g., a bug), FLAG to CTO/COO before emitting — this TO assumes the drop is correct and reports on it transparently, not a bug-fix disguise.</item>
  </cross_domain_coordination>

  <next>
    On staged→pending GO from COO (or Andrew direct): DS Phase 0 (run compiler mandate Phase 1) → propose artifact key name + MCP COO → DS Phase 1 build → DS commit + qa-runner `--group D` + S3 upload → MCP DE with artifact-ready + expected fields. DE picks up footnote wiring → /frontend-dev acceptance → MCP COO COMPLETE.
  </next>
</task_order>
