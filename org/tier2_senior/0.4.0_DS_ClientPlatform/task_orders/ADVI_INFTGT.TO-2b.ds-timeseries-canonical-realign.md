<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-2b</id>
    <project>ADVI_INFTGT</project>
    <title>[P1] Group-D coordinated parity rerun — all group-D artifacts agree on partner-facing total_aua values (≤$1k delta)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <revised>2026-05-11 — scope flipped post-Andrew correction: dashboard.json is STALE, not canonical</revised>
    <status>active</status>
    <priority>P1 — parity gap (RD HOLDING on hero patch; coordinated rerun is the resolution)</priority>
    <authorized_by>CTO ruling 2026-05-11 (REVISION post-Andrew direct correction); Andrew direct: "dashboard.json must be stale then, dashboard.json should be updated with group D run and stay in parity with the rest"</authorized_by>
  </metadata>

  <context>
    Andrew flagged hero tile shows $201M but expected $203M. Initial COO/CTO hypothesis was that timeseries_overview.json was lagging dashboard.json (treating dashboard.json as canonical). **Andrew correction:** dashboard.json is ITSELF stale — it's just another group-D artifact and current group-D runs haven't kept it in parity with sibling outputs.

    **Architectural pattern ratified (revised):**
    All group-D artifacts (`dashboard.json`, `header_metrics.json`, `timeseries_overview.json`, `leaderboard.json`, `partner_analytics_*.json`, `nmec_nmnc_nna.json`, `cash_drag.json`, `activity_scan.json`, `concentration_risk.json`) MUST be in parity. They are coordinated outputs of a single group-D run reading from the same silver snapshot. Partner-facing AUA values (total_aua at firm level) must AGREE across all artifacts within rounding/cut tolerance.

    Discrepancies between group-D outputs are STALENESS or COVERAGE-GAP evidence, not architectural cut-distinctions.

    PRD §2 ratification was wrong ("0.10% drift, immaterial — log-only"). Andrew + CTO correction: it's NOT immaterial, it's staleness. PRD §2 amendment is queued in CTO §7 batched commit.
  </context>

  <scope>
    <step>Phase 1 — Pre-rerun audit:
      `comp-pipescript io INF_D_00` — verify scripts use same silver snapshot
      `comp-pipescript io INF_D_04` — confirm dashboard.json producer reads same source as leaderboard.json producer
      `comp-pipescript postdeps INF_D_04` — verify downstream chain
      Document: current state of all group-D artifacts (LastModified + total_aua values from each)
    </step>

    <step>Phase 2 — Coordinated rerun:
      Execute fresh group-D run on inf-gold-layer-runner (or qa-runner with OUTPUT_PREFIX=qa/).
      All group-D scripts must read from the SAME silver snapshot (latest available).
      Sequence: INF_D_00 → INF_D_00b → INF_D_00c → INF_D_04 → ... → INF_D_08 (or whatever the dispatch.sh manifest dictates)
    </step>

    <step>Phase 3 — Parity verification:
      Pull all group-D artifacts. Verify partner-facing total_aua agrees across:
      - `dashboard.json` total_aua
      - `header_metrics.json` total.aua
      - `timeseries_overview.json` last_period.total_aua
      - `leaderboard.json` (sum across all advisor entries' AUA for firm total)
      - `partner_analytics_monthly.json` / `_quarterly.json` / `_annual.json` most-recent-period headlines
      Acceptance: ≤$1k delta across ALL hero AUA values.
    </step>

    <step>Phase 4 — Parity-check gate (structural prevent-recurrence):
      Add post-run parity check in `comp-validate` (or new post-run script in `data/orion/scripts/gold/lib/`) that asserts these values agree within $1k.
      Hook into INFETL daily-chain so this becomes steady-state behavior (not just one-off).
      Coordinate with AE 0.7 on integration into the silver-aggregator → gold trigger flow.
    </step>

    <step>Phase 5 — Portal verification:
      After coordinated rerun, partner-build should display correct values:
      - Hero tile "TOTAL AUA" matches partner expectation (~$203M canonical post-rerun)
      - Distribution Snapshot donut center matches hero
      - Continuous Segment Analytics cumulative may STILL be wrong (separate TO-4b bug)
      RD does NOT need code changes — fresh artifacts via cache invalidation suffice.
    </step>

    <step>Pre-commit gate per CLAUDE.md rule 14 on any edited .py files.</step>

    <step>Commit + push + S3 deploy + CF invalidation for affected platinum/firm/* paths.</step>

    <step>RAVC2 to COO with:
      - Before/after total_aua values from all 5+ artifacts
      - Confirmation of ≤$1k delta
      - Parity-check gate location + sample output
      - CF invalidation ID for platinum/firm/*
    </step>
  </scope>

  <acceptance_criteria>
    1. Coordinated group-D rerun executed; all artifacts regenerated from same silver snapshot.
    2. Partner-facing total_aua agrees across `dashboard.json`, `header_metrics.json`, `timeseries_overview.json` last_period, `leaderboard.json` firm-sum, `partner_analytics_*.json` headlines — ≤$1k delta.
    3. Parity-check gate added (post-run script OR `comp-validate` extension).
    4. Parity-check gate integrated into INFETL daily-chain (steady-state behavior).
    5. CF invalidation fired for platinum/firm/* paths.
    6. Portal-side verify: hero tile + Snapshot donut center display correct values.
    7. Pre-commit gate exits 0 on any .py edits.
    8. RAVC2 includes 5+ artifact before/after table + parity gate evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-pipescript io INF_D_04`
      `comp-pipescript io INF_D_00`
      `comp-pipescript postdeps INF_D_04`
      `comp-platinum reverse dashboard`
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on edited .py files
      Local artifact comparison (5+ files)
    </phase>
    <phase id="3" when="after commit">
      `comp-validate INF_D_04 --artifact /tmp/dashboard.json`
      Manual SHA verify on S3 deploy
      `comp-pipescript deployed` MATCH on any modified gold scripts
    </phase>
  </compiler_tools_mandate>

  <notes>
    **Coordination:** May need AE 0.6.1 if dispatching via SSM to a runner. DS~A can also run locally via the cascade harness if appropriate.

    **NOT partner-blocking right now** — RD is HOLDING per CTO ruling; no portal patch needed. Demo today reads what's there. Tomorrow's coordinated rerun produces correct partner-facing values.

    **Architectural lasting value:** the parity-check gate is the structural prevent-recurrence. After this lands, no future group-D run can ship with artifacts that disagree on total_aua.

    **DS~A may also self-pick TO-4b (continuous-geo-aua bug investigation) — same DS lane, sibling investigation.**
  </notes>
</task_order>
