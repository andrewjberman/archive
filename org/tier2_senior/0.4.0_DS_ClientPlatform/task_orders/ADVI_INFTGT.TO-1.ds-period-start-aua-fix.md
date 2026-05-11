<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-1</id>
    <project>ADVI_INFTGT</project>
    <title>[P0] Fix period_start_aua denominator — cap inflated aua_growth_pct; emit null when below sanity floor</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <priority>P0 — partner-blocking</priority>
    <authorized_by>Andrew direct GO 2026-05-11; PRD ADVI_INFTGT v0.1 (1.0.0_SA_CTO)</authorized_by>
  </metadata>

  <context>
    Leaderboard shows Peter Lee QTD aua_growth_pct = +4331.6%, Patrick = +7741.2%.
    Root cause: period_start_aua denominator ($3.7M vs $165M current AUA) is from a
    mismatched account set between window-start snapshot and current snapshot.
    PRD §4.1 + §5.3: fix lives upstream of INF_D_00c (likely INF_D_00b.portal_timeseries
    or INF_C_02.client_performance). INF_D_00c is a re-emitter; trace the producer first.
  </context>

  <scope>
    <step>Phase 1 — Trace: `comp-trace period_start_aua --direction both`;
      `comp-pipescript io INF_D_00b`; `comp-pipescript io INF_D_00c`;
      `comp-blast build_firm_dashboard`. Locate the script that produces
      period_start_aua and understand the account-set selection logic.</step>

    <step>Phase 2 — Fix producer: ensure period_start_aua uses the SAME account set
      as current_aua (not a different snapshot). If account-set consistency is not
      achievable in one TO, emit aua_growth_pct: null when
      period_start_aua &lt; current_aua * 0.20 (sanity floor — DS design call per PRD §7.4).
    </step>

    <step>Phase 3 — RD defense layer: add null-guard at AdvisorPublicProfile.tsx:541
      and AdvisorsTab.tsx:342 — render "—" cleanly when aua_growth_pct is null.
      (Flag to RD via inbox; they will execute; this step is DS signaling only.)</step>

    <step>Pre-commit gate: `.tools/ds-commit-gate.sh` on all edited .py files.</step>

    <step>Local standalone verify: run the fixed script; check Peter Lee QTD
      aua_growth_pct is plausible (&lt;±50%) or null.</step>

    <step>Commit + push + S3 deploy + comp-pipescript deployed MATCH.</step>

    <step>RAVC2 to COO with before/after values for Peter Lee + Patrick Scanlan.</step>
  </scope>

  <acceptance_criteria>
    1. Peter Lee QTD aua_growth_pct is either a plausible number (&lt;±50%) or null.
    2. Patrick Scanlan QTD aua_growth_pct is either plausible or null.
    3. No advisor shows a growth% above 500% in any window.
    4. Portal renders "—" cleanly for null aua_growth_pct (RD side — flag to RD).
    5. Pre-commit gate exits 0.
    6. S3 deploy MATCH.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-trace period_start_aua --direction both`
      `comp-pipescript io INF_D_00b`; `comp-pipescript io INF_D_00c`
      `comp-blast build_firm_dashboard`
      `comp-platinum reverse leaderboard`
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on all .py edits
      local standalone verify with Peter Lee result
    </phase>
    <phase id="3" when="after commit">
      `comp-pipescript deployed` MATCH on affected scripts
      `comp-validate INF_D_00c --artifact /tmp/leaderboard.json`
    </phase>
  </compiler_tools_mandate>

  <notes>
    Sanity floor design decision (per PRD §7.4): options are (a) 20% of current_aua,
    (b) static $1M floor, (c) snapshot-pair existence check. DS~B picks the most
    defensible — document choice in RAVC2.

    DS~A is EOD — this TO routed to DS~B as primary. When DS~A is back, they
    cross-check the leaderboard fix.

    Frontend null-guard (AdvisorPublicProfile.tsx + AdvisorsTab.tsx) is a separate
    dispatch to RD — COO will relay once this RAVC2 lands.
  </notes>
</task_order>
