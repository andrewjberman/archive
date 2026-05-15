<task_order>
  <metadata>
    <id>ADVI_INFINC.005</id>
    <slug>dsd-pattern-e-incremental-api-pulls</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>active</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — INFINC.004 RAVC2 received (8e17ef54e). CTO Phase 5 ruling 2026-05-15: Pattern E APPROVED as INFINC.005; Pattern D DE-SCOPED (brief §2.4 — firm-level artifacts already incremental, no win).</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P1 — Pattern E eliminates ~14min/day of unconditional full-history API re-pull (~25% of daily pull-side wall)</priority>
    <sla>~3-4h wall actual per Pod 4 velocity (correctness-sensitive — backdated-correction handling)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.5 (Pattern E mechanics) + §3 migration map rows INF_API_PULL_TXN / INF_API_PULL_PERF</ref>
    <ref type="cto_ruling">CTO MCP 2026-05-15 — Phase 5 = Pattern E approved; 4 TO conditions (data_reprocess_scope block, cron-first sequencing, cross_domain_coordination, in-window backdated-correction AC)</ref>
    <ref type="phase4">ADVI_INFINC.004 RAVC2 (8e17ef54e) — Pattern C complete; aggregate 53.6s→24.6s</ref>
    <ref type="script_txn">data/orion/manual_api/pull_inflection_transactions_rest.py — INF_API_PULL_TXN (~7min full re-pull today)</ref>
    <ref type="script_perf">data/orion/manual_api/pull_inflection_performance_rest.py — INF_API_PULL_PERF (~9min full re-pull today)</ref>
  </references>

  <context>
    Pattern E = incremental API pulls. Two Orion REST pull scripts currently do an unconditional full-history re-pull on every chain run:

    INF_API_PULL_TXN (pull_inflection_transactions_rest.py):
      Current: re-pulls the entire transaction history each run → bronze/transactions/{date}.parquet. ~7min wall.

    INF_API_PULL_PERF (pull_inflection_performance_rest.py):
      Current: re-pulls the entire performance history each run → bronze/performance/{date}.parquet. ~9min wall.

    Combined ~16min daily of redundant re-pull.

    v1 optimization per brief §2.5:
      Orion REST supports date-windowed queries. Target behavior:
        1. Read max(transDate) from the most recent existing bronze partition.
        2. Pull only [max_date - 90d, today] — a 90-day trailing window plus everything since last pull.
        3. Append to / merge with prior bronze; dedupe by transaction_id (TXN) / equivalent PK (PERF).
      Drops combined daily wall ~16min → ~2min Mon-Sat.

    CORRECTNESS RISK — backdated corrections:
      Orion can backdate a correction transaction (e.g., a Sell dated 60 days ago, booked today). A pure incremental-from-max pull would miss any correction older than the trailing window.
      Mitigations (brief §2.5 — BOTH required):
        1. 90-day trailing window — N=90 covers observed backdating patterns. Catches in-window corrections on every daily run.
        2. Weekly full-pull backstop — one full-history re-pull per week (Sunday) catches anything beyond the 90-day window.

    NON-NEGOTIABLE SEQUENCING (CTO condition b):
      The weekly full-pull backstop MUST be in place BEFORE or IN THE SAME COMMIT AS the daily-window narrowing. Never narrow the daily pull before the backstop exists — out-of-window corrections would be silently lost with no recovery path.

    INF_API_PULL_POSITIONS_DAILY is NOT in scope — it only pulls today's snapshot already (brief migration map: unchanged).
  </context>

  <objective>
    Migrate INF_API_PULL_TXN + INF_API_PULL_PERF to incremental date-windowed pulls: 90-day trailing window + since-last-max on daily runs, with a weekly full-pull backstop. Eliminate ~14min/day of redundant re-pull while guaranteeing backdated-correction correctness.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/manual_api/pull_inflection_transactions_rest.py — date-windowed pull + dedupe</file>
      <file action="modify">data/orion/manual_api/pull_inflection_performance_rest.py — date-windowed pull + dedupe</file>
      <file action="readonly_reference">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.5 — Pattern E specification</file>
      <file action="conditional">chain scheduling / EventBridge config — only if Phase 1 selects the AE-cron mechanism (see Phase 1)</file>
    </files>
  </scope>

  <phase id="0" when="before write — I/O surface + deploy path + overlap">
    <step>
      <run>Read both pull scripts. Confirm: (a) current pull-loop structure, (b) Orion REST endpoint + whether it accepts date-window query params (start-date/end-date or since), (c) bronze output path + partition pattern, (d) the PK for dedupe (transaction_id for TXN; confirm the equivalent for PERF).</run>
      <expect>Pull structure understood. Date-window query capability confirmed against Orion REST. Dedupe PK identified for both scripts.</expect>
    </step>
    <step>
      <run>Confirm the deploy path for data/orion/manual_api/ scripts. These are NOT under data/*/scripts/{gold,silver,bronze}/ — verify how they reach the runner (S3 code sync? bundled in chain dispatch?) and confirm the commit→deploy cycle that applies.</run>
      <expect>Deploy path confirmed. If S3-synced like gold scripts, safe-deploy.sh applies; if bundled differently, document the correct cycle.</expect>
    </step>
    <step>
      <run>comp-pipescript overlap INF_API_PULL_TXN INF_API_PULL_PERF — confirm shared S3 artifacts / downstream consumers that need coordination (CTO condition c).</run>
      <expect>Shared-artifact surface mapped. Downstream bronze consumers (silver converters) identified — they must be unaffected by incremental vs full-pull (same bronze shape).</expect>
    </step>
  </phase>

  <phase id="1" when="weekly full-pull backstop — MUST land first or same-commit as Phase 2">
    <step>
      <run>Select the weekly full-pull mechanism. Two options:
        OPTION A (script-internal, recommended): the pull script self-detects Sunday (or reads a FULL_PULL env var) and does a full-history re-pull on that day, incremental Mon-Sat. Backstop ships ATOMICALLY in the same commit as the daily-window narrowing — sequencing requirement structurally guaranteed.
        OPTION B (AE EventBridge cron): a separate weekly EventBridge rule fires a full-pull. Mixed-lane — AE 0.6.1 lands the rule FIRST as a hard gate before Phase 2.
      Recommend Option A: atomic ship means the daily pull literally cannot be narrowed without the backstop branch present. If Option B is required for an external scheduling reason, coordinate with AE 0.6.1 and flag COO.</run>
      <expect>Mechanism selected. If Option A: backstop logic written into both scripts (full-pull branch on Sunday/env-var). If Option B: AE 0.6.1 EventBridge rule landed + confirmed live BEFORE Phase 2.</expect>
      <if_mismatch>If Orion REST cannot serve a full-history pull on demand for the Sunday backstop, STOP and escalate to COO — the backstop is non-negotiable.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — daily-window narrowing (gated on Phase 1 backstop)">
    <step>
      <run>INF_API_PULL_TXN: add date-windowed pull. Read max(transDate) from the most recent bronze/transactions partition; pull [max_date - 90d, today]; append to prior bronze; dedupe by transaction_id keeping last. Sunday/env-var → full-history pull (Phase 1 backstop branch).</run>
      <expect>Daily run pulls only the 90-day trailing window. Dedupe by transaction_id. Bronze output shape byte-identical to full-pull shape (no schema change).</expect>
    </step>
    <step>
      <run>INF_API_PULL_PERF: same Pattern E migration. Date-windowed pull + dedupe by the PERF PK confirmed in Phase 0. Sunday/env-var → full-history backstop.</run>
      <expect>Daily run windowed. Dedupe correct. Bronze shape unchanged.</expect>
    </step>
    <step>
      <run>Intraday re-fire handling (brief §2.5 edge case): if the chain re-fires later the same day after the morning pull already wrote today's bronze, the pull should re-pull to catch intraday activity. Make this explicit — `--since {last_pull_ts}` for an intraday refresh vs `--start-date {today-90d}` for the normal daily window.</run>
      <expect>Intraday re-fire behavior explicit and correct, not accidental.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh on both scripts (py_compile + AST + ruff py39) if the gate applies to manual_api/ scripts per Phase 0 deploy-path finding.</run>
      <expect>3-gate PASS, or documented N/A if manual_api/ is outside the gate scope.</expect>
    </step>
  </phase>

  <phase id="3" when="validation">
    <step>
      <run>First-run (cold / full-pull): run INF_API_PULL_TXN in full-pull mode. Verify complete bronze partition written, baseline row count + wall time recorded.</run>
      <expect>Full-pull baseline captured.</expect>
    </step>
    <step>
      <run>Second-run (incremental): run again in daily-window mode. Verify (a) only [max_date-90d, today] pulled, (b) wall time materially reduced (~7min → &lt;1min target for TXN), (c) bronze row count + content reconcile with the full-pull baseline (no rows lost, no dupes).</run>
      <expect>Incremental run materially faster; bronze reconciles with full-pull baseline.</expect>
    </step>
    <step>
      <run>BACKDATED-CORRECTION-IN-WINDOW test (CTO condition d): inject or identify a transaction dated within the last 90 days but newly booked. Run the incremental daily pull. Verify the in-window backdated correction IS captured in the resulting bronze.</run>
      <expect>In-window (&lt;90-day) backdated correction empirically captured by the daily incremental run. AC9.</expect>
    </step>
    <step>
      <run>Weekly full-pull backstop test: trigger the Sunday/env-var full-pull path. Verify a full-history re-pull occurs and catches a correction OUTSIDE the 90-day window.</run>
      <expect>Backstop catches out-of-window corrections.</expect>
    </step>
    <step>
      <run>Repeat second-run + in-window-correction validation for INF_API_PULL_PERF.</run>
      <expect>Same pass criteria for PERF.</expect>
    </step>
  </phase>

  <phase id="4" when="commit + deploy + RAVC2">
    <step>
      <run>safe-commit.sh --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;" -m "feat(INFINC.005): Pattern E incremental API pulls — PULL_TXN/PULL_PERF date-windowed + weekly backstop" -- data/orion/manual_api/pull_inflection_transactions_rest.py data/orion/manual_api/pull_inflection_performance_rest.py</run>
      <expect>Commit clean. No contamination.</expect>
    </step>
    <step>
      <run>Deploy per the cycle confirmed in Phase 0 (safe-deploy.sh + S3 upload if S3-synced). If Option B cron was used, confirm the EventBridge rule is live.</run>
      <expect>Scripts deployed. Backstop confirmed live.</expect>
    </step>
    <step>
      <run>SSM-direct or chain validation: incremental daily run wall-time logged vs full-pull baseline. Report delta.</run>
      <expect>Wall time materially reduced on incremental runs.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 with: commit SHA, deploy confirmation, first-run vs incremental-run wall comparison, backdated-correction-in-window capture evidence, weekly-backstop evidence.</run>
      <expect>Evidence-bearing RAVC2. ADVI_INFINC Pattern A-E complete — incremental pipeline v1 done.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: INF_API_PULL_TXN does date-windowed incremental pull on daily runs ([max_date-90d, today])
    AC2: INF_API_PULL_PERF same Pattern E incremental pull
    AC3: Dedupe by transaction_id (TXN) / confirmed PK (PERF) — no duplicate rows, no lost rows vs full-pull baseline
    AC4: Weekly full-pull backstop in place (Option A script-internal Sunday branch, OR Option B AE EventBridge rule) — landed BEFORE or SAME-COMMIT as the daily narrowing
    AC5: Bronze output shape byte-identical between incremental and full-pull modes — downstream silver consumers unaffected
    AC6: Incremental daily run wall materially less than full-pull (~7min→&lt;1min TXN target; ~9min→&lt;1min PERF target)
    AC7: Intraday re-fire handled explicitly (--since vs --start-date)
    AC8: Weekly full-pull backstop empirically catches an out-of-window backdated correction
    AC9: In-window (&lt;90-day) backdated correction empirically captured by the daily incremental run (CTO condition d)
    AC10: ds-commit-gate.sh PASS on both scripts, or documented N/A if manual_api/ is outside gate scope
    AC11: from __future__ import annotations preserved as first import (if applicable to manual_api/ scripts)
    AC12: No emoji per CLAUDE.md
    AC13: RAVC2 to COO + CC CTO + AE 0.6.1 with wall-time + backdated-correction evidence
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 0 comp-pipescript overlap INF_API_PULL_TXN INF_API_PULL_PERF; Phase 2 ds-commit-gate.sh x2 (if in scope); Phase 4 safe-deploy per Phase 0 finding.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCY: INFINC.004 RAVC2 (8e17ef54e) — COMPLETE.
    MIXED-LANE (CTO condition c): DS bronze pull-script changes (DS~D) + weekly full-pull backstop. If Phase 1 selects Option B (AE EventBridge cron), AE 0.6.1 owns the EventBridge rule and MUST land it first as a hard gate. If Option A (script-internal), the backstop ships atomically — no AE dependency.
    SEQUENCING (CTO condition b): the weekly full-pull backstop lands FIRST or SAME-COMMIT as the daily-window narrowing. Never narrow the daily pull before the backstop exists.
    DOWNSTREAM: silver converters consuming bronze/transactions + bronze/performance — bronze shape unchanged, consumers unaffected.
    AE 0.6.1: CC on RAVC2; coordinate the Option-B cron if selected.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_scope>No historical bronze re-emit required for the migration itself. The first post-deploy run should be a full-pull (cold) to establish the baseline partition the incremental window reads from; subsequent daily runs are incremental. The weekly Sunday backstop re-pulls full history. No silver/gold re-emit — bronze shape is unchanged. No Lambda redeploy.</reprocess_scope>
  </data_reprocess_scope>

  <deliverables>
    1. INF_API_PULL_TXN Pattern E migration (date-windowed + dedupe + backstop)
    2. INF_API_PULL_PERF Pattern E migration
    3. Weekly full-pull backstop (Option A or B per Phase 1)
    4. Validation evidence: incremental vs full wall comparison + in-window + out-of-window backdated-correction capture
    5. RAVC2
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO + AE 0.6.1 on AC1-13 PASS.</ravc>

  <notes>
    **Pattern D DE-SCOPED:** Per CTO Phase 5 ruling 2026-05-15 + brief §2.4 — firm-level latest-state artifacts (INF_D_00/00b/00c/00d/07/05a/06a/08/09) run &lt;30s each and are already structurally incremental. No Pattern D TO. Pattern E is the final v1 incremental phase.

    **Backstop-first is the correctness invariant.** Option A (script-internal Sunday branch) is recommended specifically because it makes the sequencing requirement structurally impossible to violate — the narrowing and the backstop are the same commit. Prefer it unless an external scheduling constraint forces Option B.

    **manual_api/ deploy path:** these scripts are under data/orion/manual_api/, not data/*/scripts/bronze/. Phase 0 confirms the applicable commit→deploy cycle. Rule 13/14/15 strict applicability is Phase-0-determined.

    **No emoji per CLAUDE.md.**

    **Author identity:** --author="0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;".
  </notes>
</task_order>
