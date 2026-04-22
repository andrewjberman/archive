<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-auagap-003-bfix1-temporal-scope</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>active</status>
    <project_code>ADVI_STAUDT</project_code>
    <urgency>NON-BLOCKING — prevention fix. Run in parallel with AUAGAP.002 steps 3-5 or immediately after.</urgency>
    <cto_directive>1.0.0_SA_CTO 20260422T123619Z — BFIX1 temporal-scope structural fix, Option A. Latent trap if left unfixed.</cto_directive>
  </metadata>

  <objective>
    Fix B_00.canonical_holdings.py build_persistent_rps_accts() to compute a
    date-relative persistent set per target date D, instead of the current global
    sorted_dates[-7:] (latest-run dates). Removes the latent amplifier that caused
    the Q1-Q3 2025 AUA collapse when historical Schwab universe differed from the
    latest-run universe.
  </objective>

  <context>
    Current behavior: build_persistent_rps_accts() takes sorted_dates[-7:] — the
    globally last 7 Schwab RPS dates across the entire run (e.g., all April 2026 dates
    for a run executed in April 2026). This static 2026-universe set (~5,450 accounts)
    is applied uniformly as is_schwab_covered to ALL historical target dates. When the
    historical Schwab universe genuinely differed from the 2026 universe, accounts get
    incorrectly classified bd_stale.

    BFIX1 original intent: handle transient sparse-day Schwab responses by using a
    small rolling window of dates rather than a single day. Option A preserves this
    intent while making the window date-relative.
  </context>

  <spec>
    File: data/black_diamond/scripts/gold/B_00.canonical_holdings.py
    Change: build_persistent_rps_accts(target_date D) — compute the union of
    schwab_cache account_ids observed within [D - 14 calendar days, D], computed
    per-target-date. Replace the current global sorted_dates[-7:] approach.

    Implementation notes:
    - schwab_cache is keyed by date; filter to dates in [D-14d, D], take union of
      account_ids across those dates.
    - For dates where D-14d has no Schwab data (very early dates), fallback to
      whatever is available in [earliest_schwab_date, D].
    - The call site (wherever build_persistent_rps_accts() is invoked per target date)
      must pass the target date D.
    - Compiler mandate: comp-pipescript io B_00.py before commit.
    - ds-commit-gate + py_compile before commit.
  </spec>

  <validation>
    Spot-check: after implementing Option A, compare persistent set sizes between
    Option A and current global implementation for three dates:
      - 2025-03-31 (Q1 2025 — was suppressed)
      - 2025-09-30 (Q3 2025 — was suppressed)
      - 2026-04-15 (latest — should match or be close to current)
    Document the deltas in session log. Then run B_00 --chain full (or equivalent
    scope) to confirm no regressions introduced. Commit session log alongside fix.
  </validation>

  <acceptance_criteria>
    1. Option A implemented: build_persistent_rps_accts() is date-relative, not global.
    2. comp-pipescript io B_00.py run pre-commit and output reviewed.
    3. py_compile + ds-commit-gate PASS.
    4. Spot-check: persistent set sizes for 2025-03-31, 2025-09-30, 2026-04-15
       documented with deltas vs current implementation.
    5. B_00 full rerun clean (no new anomalies introduced).
    6. MCP COO + CTO on completion with spot-check deltas.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT block AUAGAP.002 on this fix — AUAGAP.002 is the immediate unblock.</rule>
    <rule>Do NOT skip comp-pipescript io before commit — compiler mandate.</rule>
    <rule>Do NOT implement AUAGAP.002 rerun steps in this TO — separate scope.</rule>
  </do_not>
</task_order>
