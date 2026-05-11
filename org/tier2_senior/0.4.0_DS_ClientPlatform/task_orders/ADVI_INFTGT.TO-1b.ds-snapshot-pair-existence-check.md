<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-1b</id>
    <project>ADVI_INFTGT</project>
    <title>[P1] period_start_aua snapshot-pair existence check — architect against account-set drift root cause; layer with 20% floor + $1M absolute secondary</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>active</status>
    <priority>P1 — parity gap (not partner-blocking; current TO-1 ship covers demo)</priority>
    <authorized_by>CTO Q4 ruling 2026-05-11 (20260511T191055Z) — ACCEPT P0 ship a1594ae69 + AUTHORIZE P1 follow-up. Andrew GO on ADVI_INFTGT 2026-05-11.</authorized_by>
  </metadata>

  <context>
    TO-1 (`a1594ae69`) shipped a 20% relative floor that catches Peter Lee ($3.7M < $33M floor → null) and Patrick Scanlan. P0 partner-blocking surface CLOSED. Good ship.

    The 20% floor is a heuristic — it catches the symptom (small denominator) but doesn't address the root cause (account-set drift between window-start snapshot and current snapshot). Peter has $1.2M YTD-start AUA vs $165M current — the start figure is not from the same accounts as the current figure. That's the bug.

    CTO Q4 ruling layered the guards:
    - **Primary (architectural — this TO):** snapshot-pair existence check
    - **Secondary (defense-in-depth — this TO):** absolute $1M floor
    - **Tertiary (already shipped TO-1):** 20% relative floor

    These compose naturally. TO-1b refines + adds the architectural layer; doesn't replace what's already shipped.
  </context>

  <scope>
    <step>Phase 1 — Trace producer:
      `comp-trace period_start_aua --direction both`
      Likely producer: `_aua_at_start()` in `INF_C_02.client_performance` OR `INF_D_00b.portal_timeseries`.
      `comp-pipescript io INF_C_02` + `comp-pipescript io INF_D_00b`
      Confirm: which function reads window-start snapshot? How does it select the account set?
    </step>

    <step>Phase 2 — Account set identification:
      For each advisor + window (QTD/YTD/MAX):
      - account_set_start = set of account_ids with positions in the snapshot at window_start_date
      - account_set_current = set of account_ids with positions in the current snapshot
      Compute symmetric difference. Define divergence threshold.
    </step>

    <step>Phase 3 — Snapshot-pair existence check (PRIMARY guard):
      When `len(account_set_start ^ account_set_current) / len(account_set_current) > 0.10`
      (proposed threshold: 10% of accounts present in one but not the other — DS~B finalizes),
      emit `aua_growth_pct: null` AND log a structured WARN with the divergence ratio for observability.

      Alternative compositions for the threshold (DS~B picks):
      - Symmetric difference ratio (proposed: > 10%)
      - Jaccard distance > 0.10
      - Asymmetric: missing accounts ratio > X AND added accounts ratio > Y
    </step>

    <step>Phase 4 — $1M absolute floor (SECONDARY guard):
      When `period_start_aua < 1_000_000` AND `current_aua > 1_000_000`,
      emit `aua_growth_pct: null` (catches genuinely-new-advisor edge cases with consistent account sets).
    </step>

    <step>Phase 5 — Composition:
      Primary + Secondary + 20% relative floor (TO-1 tertiary) layer cleanly. ALL three checks evaluate; ANY of them emits null → null wins. Document the layered logic in a docstring.
    </step>

    <step>Pre-commit gate per CLAUDE.md rule 14: `.tools/ds-commit-gate.sh` on all edited .py files.</step>

    <step>Local standalone verify: 4 advisor canonical cases:
      - Peter Lee: account-set drift (YTD $1.2M start vs $165M current) → null via PRIMARY guard
      - Patrick Scanlan: account-set drift → null via PRIMARY guard
      - Joe Brandenburg: 21 clients, account-set consistent → plausible aua_growth_pct (positive growth)
      - Judith Ozinga (if data): same-account-set new client → plausible value
      Document the canonical 4-case verification in RAVC2.
    </step>

    <step>Commit + push + S3 deploy + comp-pipescript deployed MATCH (or manual SHA verify per INF bucket gap).</step>

    <step>RAVC2 to COO with:
      - Producer function located (file + line range)
      - Threshold chosen + rationale
      - 4-advisor canonical verification table
      - Before/after for each
      - Confirmation that 20% floor (TO-1) + $1M absolute + snapshot-pair all compose
    </step>
  </scope>

  <acceptance_criteria>
    1. Producer function for period_start_aua located and traced.
    2. Snapshot-pair existence check implemented as PRIMARY guard.
    3. $1M absolute floor implemented as SECONDARY guard.
    4. 20% floor (TO-1) preserved as TERTIARY guard — three-layer composition documented.
    5. Peter Lee + Patrick Scanlan still emit null (consistent with TO-1).
    6. Joe Brandenburg + same-account-set advisors emit plausible aua_growth_pct (not null).
    7. Structured WARN log on snapshot-pair-divergence-emit-null with divergence ratio.
    8. Pre-commit gate exits 0.
    9. S3 deploy MATCH (manual or comp-pipescript when INF bucket support lands).
    10. RAVC2 includes 4-advisor verification table + threshold rationale.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-trace period_start_aua --direction both`
      `comp-pipescript io INF_C_02`
      `comp-pipescript io INF_D_00b`
      `comp-blast _aua_at_start` (or the producer name once traced)
    </phase>
    <phase id="2" when="before commit">
      `.tools/ds-commit-gate.sh` on all edited .py files
      Local standalone verify with 4-advisor canonical cases
    </phase>
    <phase id="3" when="after commit">
      `comp-validate INF_D_00c --artifact /tmp/leaderboard.json`
      Manual SHA verify or `comp-pipescript deployed` MATCH
    </phase>
  </compiler_tools_mandate>

  <notes>
    Threshold tuning (Phase 3, 10% symmetric difference): heuristic. DS~B may discover the actual data warrants higher/lower based on real advisor account churn patterns. Document the chosen threshold in RAVC2.

    NOT BLOCKING for partner demo prep tonight — current TO-1 ship covers the demo cleanly. This TO can ship tomorrow or later this week.

    DS~A may also take this when back if DS~B prefers to defer.
  </notes>
</task_order>
