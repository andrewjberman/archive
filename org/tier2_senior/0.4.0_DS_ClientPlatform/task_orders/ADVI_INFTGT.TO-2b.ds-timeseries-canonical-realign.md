<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-2b</id>
    <project>ADVI_INFTGT</project>
    <title>[P1] timeseries_overview canonical realign — last_period.total_aua matches dashboard.json canonical ($202.96M)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>active</status>
    <priority>P1 — parity gap (not partner-blocking; RD path A interim covers demo)</priority>
    <authorized_by>CTO ruling 2026-05-11 on RD 5-regression report; pairs with RD Option A under TO-2 + TO-3 scope</authorized_by>
  </metadata>

  <context>
    Andrew flagged hero tile "TOTAL AUA" reads $201M instead of canonical $202.96M. Root cause: PartnerAnalytics + DistributionTab read `last_period.total_aua` from `timeseries_overview.json` (quarterly cut) — which sums to $201M for the most recent quarter. Canonical `total_aua` lives in `dashboard.json` ($202,958,135).

    **Architectural pattern ratified by CTO 2026-05-11:** Hero tiles ALWAYS show canonical `total_aua` from `dashboard.json`. Downstream cut-specific views show cut values + explicit labels + (optionally) deltas vs canonical.

    **RD interim ship (under TO-3 scope, Option A):** Hero tile + donut center fetch dashboard.json total_aua and override the last-period value at render time. Bars stay quarterly (cut chip honest). Closes the visual demo gap immediately.

    **This TO is the DS-side architectural fix:** re-align `timeseries_overview.json` so its `last_period.total_aua` matches `dashboard.json` canonical. After this lands, RD's override layer is no longer needed (but harmless to leave as defense-in-depth).
  </context>

  <scope>
    <step>Phase 1 — Trace producer:
      `comp-trace timeseries_overview --direction both`
      Likely producer: INF_D_00b.portal_timeseries OR INF_D_00.portal_aggregates.
      Confirm: which script emits the `last_period.total_aua` field? What cut does it use?
    </step>

    <step>Phase 2 — Reconcile:
      `dashboard.json` canonical total_aua = $202,958,135 (sourced from header_metrics path)
      `timeseries_overview.json` last_period.total_aua = $201M (quarterly cut)
      
      Identify the divergence:
      - Are they reading different account sets?
      - Different filter dates?
      - Different cut definitions?
      
      The producer must align last_period.total_aua to MATCH dashboard.json's source-of-truth cut.
    </step>

    <step>Phase 3 — Implementation:
      Option 1: Re-point timeseries producer to use canonical total_aua source-of-truth (same as dashboard.json)
      Option 2: Add a defensive override at script output: `if last_period.snapshot_date == current_snapshot_date: last_period.total_aua = canonical_total_aua`
      
      Option 1 is structurally cleaner. Option 2 is faster but adds a side-effect.
    </step>

    <step>Pre-commit gate per CLAUDE.md rule 14: `.tools/ds-commit-gate.sh` on all edited .py files.</step>

    <step>Local verify: re-run producer; confirm `last_period.total_aua` in output matches `dashboard.json` canonical.</step>

    <step>Commit + push + S3 deploy + manual SHA verify.</step>

    <step>RAVC2 to COO with before/after values + chosen option rationale.</step>
  </scope>

  <acceptance_criteria>
    1. `timeseries_overview.json` `last_period.total_aua` matches `dashboard.json` canonical ($202.96M) ±0.1%.
    2. No regression on other panels reading timeseries data.
    3. Architectural pattern documented (hero tile canonical-source convention) in script docstring.
    4. Pre-commit gate exits 0.
    5. S3 deploy MATCH.
    6. RAVC2 includes before/after for last_period.total_aua + chosen Option rationale.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-trace timeseries_overview --direction both`
      `comp-pipescript io INF_D_00b`
      `comp-pipescript io INF_D_00`
    </phase>
    <phase id="3" when="after commit">
      Manual SHA verify on S3 deploy
    </phase>
  </compiler_tools_mandate>

  <notes>
    Not partner-blocking. RD's interim Option A (hero canonical fetch override) covers the demo today. This TO is the architectural-correctness layer that lands tomorrow when DS~A is back.

    DS~B may take this if they want extra bandwidth, but DS~A is the natural owner per timeseries lineage.
  </notes>
</task_order>
