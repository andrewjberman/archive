<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.006-data</id>
    <project>ADVI_INFLFE</project>
    <title>INFLFE.006 DS data fix — INF_D_04 rep-coverage gate + DG-1/DG-2/DG-3 schema parity</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <note>TO authored retroactively at close — work was executed from verbal/inbox GO (COO session60 INFLFE.006 DG dispatch). No prior file existed.</note>
  </metadata>

  <context>
    INFLFE.006-data covered three phases of INF_D_04.client_portal_summary.py fixes:

    Phase 1 (commit a9435bc90): Apply AUDIT-003 rep-coverage gate (INFLECTION_REP_IDS.issubset check)
    to _build_aua_view and _build_geo_view. Root cause: rep 6 (joe_brandenburg) absent from
    aum_snapshot → partner_analytics views showing $182.5M (partial-rep) instead of $199.6M (holdings).

    Phase 2 (commit 9de58963d): DG-1/DG-2/DG-3 fixes:
    - DG-1: _build_clients_tab_slim — apply same AUDIT-003 rep-coverage gate
    - DG-2: clients-tab-slim schema — rename aua→total_aua + add tax stub
    - DG-3: geo city fields — emit key (from state_key + city slug) + label (display) + color field;
      fixes formatSegLabel crash on missing seg.key in Distribution drilldown (portal B1 root cause data side)

    Phase 3 (commit eef80ee93): silver/transactions/ path correction + remove stale
    api_dims_transactions freshness entry (CTO ruling: legacy silver/transactions/ path canonical).
  </context>

  <acceptance_criteria>
    <criterion id="AC1">partner_analytics_quarterly.json total_aua = $199,649,186.31 (was $182.5M)</criterion>
    <criterion id="AC2">NMNC segment present and non-zero (was $0 due to household_id mismatch)</criterion>
    <criterion id="AC3">partner_analytics_monthly.json total_aua = $199,649,186.31</criterion>
    <criterion id="AC4">Pre-commit gate exit 0 (py_compile + AST scan + ruff)</criterion>
    <criterion id="AC5">clients-tab-slim.json emits total_aua field (not bare aua) + tax stub</criterion>
    <criterion id="AC6">RAVC to COO with commit hashes and PROD verification</criterion>
  </acceptance_criteria>

  <completion_evidence>
    <commit hash="a9435bc90" author="0.4.0_DS_ClientPlatform~A" date="2026-05-06">
      fix(ADVI_INFLFE.006-data): _build_aua_view + _build_geo_view rep-coverage gate parity with AUDIT-003
      PROD verified: partner_analytics_quarterly.json total_aua=$199,649,186.31 (delta=+$17.1M)
      NMNC=$19,682,951.16 (was $0), NMEC=$7,486,368.27 (was $0)
    </commit>
    <commit hash="9de58963d" author="0.4.0_DS_ClientPlatform~A" date="2026-05-06">
      fix(ADVI_INFLFE.006-data): DG-1/DG-2/DG-3 — clients-tab-slim AUDIT-003 gate + total_aua rename + tax stub; geo city key/label/color/distribution
    </commit>
    <commit hash="6a5231e46" author="0.4.0_DS_ClientPlatform~A" date="2026-05-06">
      log(ADVI_INFLFE.006-data): session close — rep-coverage gate applied, PROD verified $199.6M
    </commit>
    <commit hash="eef80ee93" author="0.4.0_DS_ClientPlatform~A" date="2026-05-06">
      fix(ADVI_INFINGE.005b): build_transactions output silver/transactions/ + rm stale api_dims freshness entry
    </commit>
    <session_log>org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-06/ADVI_INFLFE_006_data_aua_view_rep_coverage_gate.md</session_log>
  </completion_evidence>

  <compiler_tools_mandate>
    <before_write>comp-pipescript io INF_D_04 (implicit — AUDIT-003 gate pattern already validated)</before_write>
    <before_commit>ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py — exit 0</before_commit>
    <after_commit>Manual artifact spot-check (comp-validate NO_CONFIG for INF_D_04 — BD leaderboard checks inapplicable to INF partner_analytics)</after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
  </cross_domain_coordination>
</task_order>
