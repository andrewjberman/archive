<task_order>
  <metadata>
    <id>ADVI_INFINC.006</id>
    <slug>dsd-pattern-e-txn-firm-windowed-pull</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — INFINC.005 capability probe RAVC2 received (734a2aec6). TXN firm-level windowed endpoint empirically confirmed; PERF no mechanism on probed surface. This TO implements the confirmed TXN mechanism + folds in a short-window PERF probe.</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P2 — Pattern E gravy; Patterns A/B/C banked the major wins. TXN ~7min/day is a confirmed clean win.</priority>
    <sla>~3-4h wall (TXN implementation correctness-sensitive — backdated-correction handling)</sla>
  </metadata>

  <references>
    <ref type="probe">ADVI_INFINC.005 RAVC2 (734a2aec6) — Orion REST capability probe; brief docs/briefs/inf-pattern-e-orion-rest-capability-probe-20260515.md</ref>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.5 — Pattern E goal (mechanism now corrected by INFINC.005 probe)</ref>
    <ref type="script_txn">data/orion/manual_api/pull_inflection_transactions_rest.py — INF_API_PULL_TXN target</ref>
    <ref type="script_perf">data/orion/manual_api/pull_inflection_performance_rest.py — INF_API_PULL_PERF — Phase 0 short-window probe target only (NOT implemented in this TO)</ref>
    <ref type="endpoint_firm">GET /api/v1/Portfolio/Transactions?startDate=&endDate= — firm-wide, one call; window cap ≤30d without entity id; practical ~7-14d/call</ref>
    <ref type="endpoint_client">GET /api/v1/Portfolio/Clients/{id}/Transactions?startDate=&endDate= — per-client, no 31-day cap (entity-scoped)</ref>
  </references>

  <context>
    INFINC.005 probe (734a2aec6) confirmed the real Pattern E mechanism for TXN — call-count reduction via the firm-level Transactions endpoint:

    - GET /api/v1/Portfolio/Transactions?startDate=&endDate= returns the ENTIRE FIRM in one call. 7-day window probed at 47,401 rows / 767 accounts / ~10s.
    - Window cap: ≤30 days without an entity id (31d → 400). 30-day firm window timed out at 120s. Practical safe window ~7-14 days per call.
    - One firm-level windowed call replaces ~1,160 per-account calls (~7min today).
    - Client-level endpoint (GET /Clients/{id}/Transactions) accepts windows with NO 31-day cap — viable for the weekly full-history backstop (~314 calls, no timeout risk).
    - Bronze schema is STABLE across account/client/firm Transactions endpoints — verified identical key sets in the probe. No downstream silver impact.

    PERF: the probe found NO firm-level endpoint (404) and no activity-delta. ~314 per-client calls. ONE untested lever remains: short date windows on the client Performance endpoint. The PERF docstring prohibits 5y+ windows (timeout) — but Pattern E uses SHORT windows, and the probe already proved the TXN docstring's "no date params" claim was flat wrong. Phase 0 of this TO runs that short-window PERF probe. PERF implementation is NOT in this TO — it gets its own TO only if the Phase 0 probe is positive.

    CORRECTNESS — backdated corrections (carried from the original Pattern E design): Orion can backdate a correction (a transaction dated 60 days ago, booked today). The daily trailing window + weekly full-history backstop together guarantee capture. Backstop-first sequencing is non-negotiable.
  </context>

  <objective>
    Migrate INF_API_PULL_TXN to an incremental firm-level windowed pull (daily trailing window, ~1 call/window vs ~1,160 account calls) with a weekly full-history backstop via the client-level endpoint. Eliminate ~7min/day of redundant TXN re-pull while guaranteeing backdated-correction correctness. Phase 0 additionally probes short-window viability on the PERF client endpoint.
  </objective>

  <scope>
    <files>
      <file action="modify">data/orion/manual_api/pull_inflection_transactions_rest.py — firm-level windowed incremental pull + weekly client-level backstop + dedupe</file>
      <file action="readonly_reference">data/orion/manual_api/pull_inflection_performance_rest.py — Phase 0 short-window probe target ONLY; no edits</file>
      <file action="create">docs/briefs/inf-pattern-e-perf-short-window-probe-{date}.md — Phase 0 PERF probe findings (brief or RAVC2-inline)</file>
    </files>
  </scope>

  <phase id="0" when="before write — TXN endpoint confirm + PERF short-window probe">
    <step>
      <run>Re-confirm against live Orion REST: firm-level /Portfolio/Transactions windowed behavior + the exact column schema vs the current account-level pull output. Confirm the dedupe PK (transaction id field name) and that firm/client/account endpoints return identical schema.</run>
      <expect>Firm endpoint behavior + schema parity confirmed. Dedupe PK identified.</expect>
    </step>
    <step>
      <run>PERF SHORT-WINDOW PROBE: test 7-day and 14-day windows on GET /api/v1/Portfolio/Clients/{id}/Performance for a sample client. The docstring prohibits 5y+ windows — determine empirically whether SHORT windows return data without timeout.</run>
      <expect>Clear finding: short-window PERF pulls viable (with row counts + latency) OR they also fail/time out. Documented for the PERF defer/implement decision.</expect>
      <if_mismatch>If short-window PERF works, note it in the RAVC2 — COO authors a PERF implementation TO. If it fails, PERF defers for v1.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="TXN weekly full-history backstop — lands first or same-commit as Phase 2">
    <step>
      <run>Implement the weekly full-history backstop in pull_inflection_transactions_rest.py: on Sunday (or a FULL_PULL env var), pull complete history via the client-level endpoint (~314 calls, no 31-day cap, no timeout risk). This is the correctness backstop for any backdated correction older than the daily trailing window.</run>
      <expect>Backstop branch implemented. Ships in the same commit as Phase 2 — the daily window cannot go live without it.</expect>
    </step>
  </phase>

  <phase id="2" when="TXN daily incremental — firm-level windowed pull">
    <step>
      <run>Implement the daily incremental path: firm-level /Portfolio/Transactions windowed pull. Daily trailing window = EXACTLY 7 days (CTO spec — gives 6 days of overlap-safety against missed/failed runs; well under the 30-day API cap). Do NOT size the window to the ~14-day ceiling. Append to prior bronze; dedupe by transaction id keeping last. Mon-Sat = incremental; Sunday = Phase 1 backstop.</run>
      <expect>Daily run pulls the 7-day trailing window in 1 firm-level call (~10s) vs ~1,160 account calls (~7min). Bronze output shape byte-identical to the full-pull shape.</expect>
    </step>
    <step>
      <run>Intraday re-fire handling: if the chain re-fires same-day after the morning pull, re-pull the trailing window to catch intraday activity. Make explicit (--since vs --start-date), not accidental.</run>
      <expect>Intraday re-fire behavior explicit and correct.</expect>
    </step>
    <step>
      <run>ds-commit-gate.sh on pull_inflection_transactions_rest.py (py_compile + AST + ruff py39). manual_api/ scripts are S3-synced per INFINC.005 Phase 0 finding — gate + Rule 15 apply.</run>
      <expect>3-gate PASS. from __future__ import annotations preserved as first import.</expect>
    </step>
  </phase>

  <phase id="3" when="validation">
    <step>
      <run>First-run (full-history backstop path): run the Sunday/env-var full pull. Capture baseline row count + wall time.</run>
      <expect>Full-history baseline captured via client-level endpoint.</expect>
    </step>
    <step>
      <run>Second-run (daily incremental): run the firm-level windowed path. Verify (a) trailing window only, (b) wall ~7min→&lt;1min, (c) bronze reconciles with the full-pull baseline — no rows lost, no dupes.</run>
      <expect>Incremental run materially faster; bronze reconciles.</expect>
    </step>
    <step>
      <run>BACKDATED-CORRECTION-IN-WINDOW test: identify/inject a transaction dated within the trailing window but newly booked. Run the daily incremental. Verify the in-window backdated correction IS captured.</run>
      <expect>In-window backdated correction empirically captured by the daily run. AC8.</expect>
    </step>
    <step>
      <run>Weekly backstop test: run the Sunday full-history path. Verify it catches a correction OUTSIDE the daily trailing window.</run>
      <expect>Backstop catches out-of-window corrections. AC9.</expect>
    </step>
  </phase>

  <phase id="4" when="commit + deploy + RAVC2">
    <step>
      <run>safe-commit.sh --author "0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;" -m "feat(INFINC.006): Pattern E TXN — firm-level windowed incremental pull + weekly client-level backstop" -- data/orion/manual_api/pull_inflection_transactions_rest.py</run>
      <expect>Commit clean.</expect>
    </step>
    <step>
      <run>safe-deploy.sh — push CLOUD + S3 upload to code/manual_api/. comp verify deployed.</run>
      <expect>Deployed clean.</expect>
    </step>
    <step>
      <run>SSM-direct or chain validation: daily incremental wall vs full-pull baseline. Report delta.</run>
      <expect>Wall materially reduced.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO + AE 0.6.1 with: commit SHA, deploy confirmation, wall comparison, in-window + out-of-window backdated-correction evidence, AND the Phase 0 PERF short-window probe finding (viable → COO authors PERF TO; not viable → PERF defers v1).</run>
      <expect>Evidence-bearing RAVC2. TXN Pattern E closes; PERF decision routed off the Phase 0 probe finding.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: INF_API_PULL_TXN daily run uses the firm-level /Portfolio/Transactions windowed endpoint (trailing window, ~7-14d/call)
    AC2: Weekly full-history backstop via the client-level endpoint — lands BEFORE or SAME-COMMIT as the daily narrowing
    AC3: Dedupe by transaction id — no duplicate rows, no lost rows vs full-pull baseline
    AC4: Bronze output shape byte-identical between incremental and full-pull modes — downstream silver consumers unaffected
    AC5: Daily incremental wall materially less than full-pull (~7min → &lt;1min target)
    AC6: Intraday re-fire handled explicitly (--since vs --start-date)
    AC7: Daily trailing window = EXACTLY 7 days (CTO spec — 6-day overlap-safety; not sized to the ~14d/30d ceiling)
    AC8: In-window backdated correction empirically captured by the daily incremental run
    AC9: Weekly backstop empirically catches an out-of-window backdated correction
    AC10: Phase 0 PERF short-window probe executed — 7d/14d client Performance windows tested; viable-or-not documented with evidence
    AC11: ds-commit-gate.sh PASS on pull_inflection_transactions_rest.py; from __future__ import annotations preserved
    AC12: No emoji per CLAUDE.md
    AC13: RAVC2 to COO + CC CTO + AE 0.6.1 with wall-time + backdated-correction + PERF-probe evidence
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 2 ds-commit-gate.sh; Phase 4 safe-deploy.sh + deployed verify.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCY: INFINC.005 RAVC2 (734a2aec6) — COMPLETE.
    SEQUENCING (carried from CTO Phase 5 conditions): the weekly full-history backstop (Phase 1) lands FIRST or SAME-COMMIT as the daily narrowing (Phase 2). Never narrow the daily pull before the backstop exists.
    BACKSTOP MECHANISM: script-internal Sunday/env-var branch — ships atomically with the narrowing, no AE cron dependency. (If an external scheduling reason forces a separate EventBridge rule, coordinate AE 0.6.1 — but script-internal is strongly preferred for atomic-ship sequencing safety.)
    FIRM-LEVEL FALLBACK (CTO ruling): if the firm-level windowed endpoint regresses or its behavior proves unstable in production, the client-level endpoint (GET /Clients/{id}/Transactions, ~314 calls, no 31-day cap) is the documented fallback for the daily path — slower than firm-level but still well under the ~1,160-account baseline. Note this fallback in the script.
    DOWNSTREAM: silver converters consuming bronze/transactions — bronze shape unchanged, unaffected.
    AE 0.6.1: CC on RAVC2.
    PERF: out of implementation scope here — Phase 0 probe only. COO authors a PERF TO off the RAVC2 if the short-window probe is positive.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_scope>No historical bronze re-emit required for the migration. The first post-deploy run should be a full-history pull (Phase 1 backstop path) to establish the baseline partition the incremental window reads from; subsequent daily runs are incremental. The weekly Sunday backstop re-pulls full history. No silver/gold re-emit — bronze shape unchanged. No Lambda redeploy.</reprocess_scope>
  </data_reprocess_scope>

  <deliverables>
    1. INF_API_PULL_TXN Pattern E migration — firm-level windowed daily pull + weekly client-level backstop + dedupe
    2. Phase 0 PERF short-window probe finding
    3. Validation evidence — incremental vs full wall comparison + in-window + out-of-window backdated-correction capture
    4. RAVC2 with PERF decision routing
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO + AE 0.6.1 on AC1-13 PASS.</ravc>

  <notes>
    **The DS~B docstring was wrong, the STOP was right.** INFINC.005's Phase 0 STOP corrected a stale docstring AND surfaced the firm-level endpoint — a better mechanism than the brief specified. The same skepticism applies to the PERF "5y+ timeout" docstring: Phase 0 here tests short windows empirically rather than trusting the docstring.

    **Backstop-first is the correctness invariant.** The Sunday/env-var full-history branch (Phase 1) and the daily narrowing (Phase 2) ship in one commit — the narrowing literally cannot go live without the backstop.

    **PERF is NOT implemented here.** Phase 0 probes it; the RAVC2 routes the decision. Do not edit pull_inflection_performance_rest.py in this TO.

    **Pattern D remains DE-SCOPED** (CTO Phase 5 ruling — brief §2.4).

    **No emoji per CLAUDE.md.**

    **Author identity:** --author="0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;".
  </notes>
</task_order>
