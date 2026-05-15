<task_order>
  <metadata>
    <id>ADVI_INFINC.005</id>
    <slug>dsd-pattern-e-orion-rest-capability-probe</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-05-15</date>
    <status>active</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RE-SCOPED 2026-05-15 — DS~D Phase 0 STOP upheld by CTO. Original date-windowing mechanism (brief §2.5) empirically invalidated by documented DS~B Orion probe (20260430T174809Z) transcribed into both target script docstrings. Re-scoped from implementation TO to capability-probe (investigation) TO. Supersedes the date-windowing version committed at 635f0bec7.</dispatch_unblock_condition>
    <project_code>ADVI_INFINC</project_code>
    <priority>P2 — Pattern E is "gravy"; INFINC.002/.003/.004 (Patterns A/B/C) already banked the major incremental wins. This probe determines whether v1 Pattern E is achievable at all.</priority>
    <sla>~1-2h wall (investigation only — no implementation)</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inf-incremental-pipeline-design-20260514.md §2.5 — Pattern E (mechanism now invalidated; goal still valid)</ref>
    <ref type="stop_finding">DS~D INFINC.005 Phase 0 STOP MCP 2026-05-15 — date-windowing premise empirically false</ref>
    <ref type="cto_ruling">CTO MCP 2026-05-15 — STOP upheld; re-scope to capability probe; do NOT implement date-windowing</ref>
    <ref type="ds_b_probe">DS~B Orion REST probe 20260430T174809Z — transcribed verbatim into both target script docstrings</ref>
    <ref type="script_txn">data/orion/manual_api/pull_inflection_transactions_rest.py — endpoint GET /api/v1/Portfolio/Accounts/{accountId}/Transactions; ~1,160 sequential account-level calls</ref>
    <ref type="script_perf">data/orion/manual_api/pull_inflection_performance_rest.py — endpoint GET /api/v1/Portfolio/Clients/{clientId}/Performance; ~314 sequential client-level calls; docstring HARD-PROHIBITS date windows (5y+ timeout)</ref>
  </references>

  <context>
    INFINC.005 was originally scoped (635f0bec7) as a Pattern E implementation TO: narrow PULL_TXN/PULL_PERF to date-windowed incremental pulls. DS~D's Phase 0 STOP — upheld by CTO — found the mechanism empirically dead:

    - INF_API_PULL_TXN account-level Transactions endpoint accepts NO date params; returns full account history per call.
    - INF_API_PULL_PERF client-level Performance endpoint has an explicit all-caps docstring prohibition on date windows — 5y+ ranges time out. Documented DS~B probe 20260430T174809Z.

    The wall-time bottleneck is CALL COUNT, not per-call payload:
    - TXN: ~1,160 sequential rate-limited account-level calls.
    - PERF: ~314 sequential rate-limited client-level calls.
    Date-windowing a call would not reduce call count even if supported — and for PERF would actively break the script.

    Pattern E's GOAL remains valid (cut ~14min/day of pull-side wall). Its brief-specified MECHANISM (date-windowing) is dead. The real lever is call-count reduction. This TO is the fresh investigation that determines whether a viable call-count-reduction mechanism exists before any implementation TO is authored.

    INVESTIGATION ONLY — no script changes, no implementation, in this TO.
  </context>

  <objective>
    Probe Orion REST API capabilities to determine whether a viable call-count-reduction mechanism exists for INF_API_PULL_TXN + INF_API_PULL_PERF. Produce an evidence-bearing brief with a clear recommendation: either (a) a viable mechanism is confirmed → sketch the implementation-TO scope, or (b) no mechanism exists → Pattern E deferred for v1.
  </objective>

  <scope>
    <files>
      <file action="readonly_reference">data/orion/manual_api/pull_inflection_transactions_rest.py — current TXN pull logic + DS~B probe docstring</file>
      <file action="readonly_reference">data/orion/manual_api/pull_inflection_performance_rest.py — current PERF pull logic + docstring prohibition</file>
      <file action="create">docs/briefs/inf-pattern-e-orion-rest-capability-probe-{date}.md — probe findings + recommendation</file>
    </files>
    <explicitly_out_of_scope>No edits to the pull scripts. No date-window params on either endpoint (empirical prohibition — TXN unsupported, PERF times out). No implementation phases — those are authored only if the probe confirms a viable mechanism.</explicitly_out_of_scope>
  </scope>

  <phase id="1" when="capability probe">
    <step>
      <run>Q1 — BATCH/FIRM-LEVEL TRANSACTIONS: probe whether Orion REST exposes a firm-level or batch transactions endpoint that returns multiple accounts in one call (vs ~1,160 per-account calls). Test candidate paths; document request/response shape + any date-filter capability at that level.</run>
      <expect>Firm/batch TXN endpoint confirmed (with shape evidence) OR confirmed absent.</expect>
    </step>
    <step>
      <run>Q2 — MODIFIED-SINCE / ACTIVITY-DELTA: probe whether Orion exposes any "accounts/clients with activity since X" or change-feed / delta endpoint that would let the pull skip unchanged entities (fewer calls).</run>
      <expect>Activity-delta capability confirmed OR confirmed absent.</expect>
    </step>
    <step>
      <run>Q3 — CONCURRENCY HEADROOM: quantify the current AdaptiveRateLimiter settings in both scripts. Determine realistic safe parallelism for the sequential calls, the 429 risk, and the modest wall-time win available from concurrency alone (orthogonal to API capability — no API change needed).</run>
      <expect>Concurrency headroom quantified with a realistic wall-time estimate + 429-risk assessment.</expect>
    </step>
    <step>
      <run>Q4 — NONE-OF-THE-ABOVE: if Q1/Q2/Q3 do not yield a viable mechanism, document any OTHER call-count-reduction approach surfaced during the probe, OR explicitly confirm none exists. Do not force-fit one of the pre-enumerated options.</run>
      <expect>Either an additional mechanism documented, or an explicit "no viable mechanism beyond concurrency" finding.</expect>
    </step>
  </phase>

  <phase id="2" when="brief + recommendation">
    <step>
      <run>Write docs/briefs/inf-pattern-e-orion-rest-capability-probe-{date}.md — probe evidence for Q1-Q4 + a clear recommendation.</run>
      <expect>Evidence-bearing brief. Recommendation is one of: (a) viable mechanism confirmed → implementation-TO scope sketch (which endpoint, expected call-count reduction, expected wall saving); (b) only concurrency available → small-win implementation-TO sketch OR defer; (c) no viable mechanism → Pattern E deferred for v1.</expect>
    </step>
    <step>
      <run>RAVC2 to COO + CC CTO with the brief commit SHA + the recommendation. COO authors the implementation TO (or the defer decision) off this RAVC2.</run>
      <expect>Evidence-bearing RAVC2. INFINC.005 probe closes; implementation TO (INFINC.006) authored only if the probe is positive.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Q1 — firm/batch-level TXN endpoint probed; exists-or-absent with request/response evidence
    AC2: Q2 — modified-since / activity-delta endpoint probed; exists-or-absent with evidence
    AC3: Q3 — concurrency headroom quantified (current rate-limiter config, safe parallelism, 429 risk, wall-time estimate)
    AC4: Q4 — none-of-the-above space honored: any other mechanism documented OR explicit "none found"
    AC5: Evidence-bearing brief written to docs/briefs/
    AC6: Recommendation is explicit and actionable: viable mechanism → implementation-TO sketch; no mechanism → Pattern E v1 defer
    AC7: NO date-window params implemented on either script (empirical prohibition — TXN unsupported, PERF 5y+ timeout)
    AC8: No script edits — investigation only
    AC9: No emoji per CLAUDE.md
    AC10: RAVC2 to COO + CC CTO
  </acceptance_criteria>

  <compiler_tools_mandate>None — investigation TO, no script edits, no deploy.</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCY: none — pure investigation.
    DOWNSTREAM: COO authors INFINC.006 (Pattern E implementation) only if this probe confirms a viable call-count-reduction mechanism. If the probe is negative, Pattern E is deferred for v1 — A/B/C banked the wins.
    NO AE DEPENDENCY: the weekly-full-pull backstop question is moot until a daily-narrowing mechanism exists.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Investigation only — no bronze/silver/gold re-emit, no deploy, no script change.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Orion REST capability probe findings (Q1-Q4)
    2. Evidence-bearing brief docs/briefs/inf-pattern-e-orion-rest-capability-probe-{date}.md
    3. Explicit recommendation: viable mechanism + implementation-TO sketch, OR Pattern E v1 defer
    4. RAVC2 to COO + CC CTO
  </deliverables>

  <ravc>DS~D RAVC2 to COO + CC CTO on AC1-10 PASS.</ravc>

  <notes>
    **DS~D Phase 0 STOP was correct** — this TO is the Phase 0 gate working as designed. The brief §2.5 premise ("Orion REST supports date-windowed queries") was wrong; the probe TO replaces the dead mechanism with an evidence-gathering step.

    **PERF docstring prohibition is load-bearing** — do NOT add date params to pull_inflection_performance_rest.py under any circumstance; 5y+ windows time out (documented runtime failure).

    **Pattern D remains DE-SCOPED** (CTO Phase 5 ruling — brief §2.4). Pattern E is the only outstanding incremental phase, and it is now gated on this probe.

    **If the probe is negative:** Pattern E defers for v1. That is an acceptable outcome — INFINC.002/.003/.004 (Patterns A/B/C) already delivered the major chain wall-time reductions. Do not force a low-value or risky implementation.

    **No emoji per CLAUDE.md.**

    **Author identity:** --author="0.4.0_DS_ClientPlatform~D &lt;0.4.0_DS_ClientPlatform~D@opal.agent&gt;".
  </notes>
</task_order>
