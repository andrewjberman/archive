<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.008</id>
    <project>ADVI_INFREL</project>
    <title>Watchdog regex broaden — intermediate-stage matchers + S3-poll disambiguator (folds INFINGE TO 1a-3)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Authored sprint mode 2026-05-05T~21:15Z post PRD ADVI_INFREL v0.1 ship; flipped staged→pending 20260506T133122Z by COO session 59 post-D4 dispatch. Absorbs INFINGE TO 1a-3 per CTO ratify 2026-05-05T~21:00Z. AE 0.7 LEAD. -->
    <priority>medium</priority>
    <estimated_effort>~0.25d</estimated_effort>
    <absorbs>INFINGE TO 1a-3 (cancelled-as-absorbed; mark in INFINGE TO ledger when next touched)</absorbs>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.5 + §6 TO-8</ref>
    <ref type="incident_evidence_d3">2026-05-05 D3 chain — AE 0.7 monitor `bz7cjbk19` exhibited stale-signal-during-progressing-chain pattern; B-chain completed 20:45Z but C-chain didn't auto-trigger; monitor still WAITING at 20:53:49Z because regex matches FINAL platinum artifact (dashboard.json ETag), not intermediate stage transitions</ref>
    <ref type="incident_evidence_d3_sighup">2026-05-05 D3f investigation — runner shut down twice (D2c + D3) despite `--no-shutdown` flag. AE 0.7 root cause: SSM shell exit → bash SIGHUP on process group → heartbeat + guard killed → watchdog fired `sudo shutdown` at 21:25Z. Reconciles D2c (canonical_performance halt at 2023-10-02) + D3 (canonical_performance halt at 2024-08-04) into ONE bug class. D3f structural fix: `nohup` on heartbeat + `nohup` on guard + continuous `shutdown -c` every 20s. Diagnostic gold per CTO 20260505T213135Z.</ref>
    <ref type="cto_diagnostic_pattern">CTO message 20260505T210223Z — disambiguator: "is intermediate output landing?" `aws s3 ls` on intermediate paths (gold/canonical/, gold/holdings/, etc.) is canonical tiebreaker for "monitor stale during long chain — hung vs progressing"</ref>
    <ref type="ds_c_disambiguator_validation">DS~C 20260505T212426Z escalation — empirical "last canonical_performance write at 21:16Z; ~10min gap" caught D3 stall via intermediate-S3-poll discipline 9min before AE 0.7 watchdog fired auto-shutdown. Validates the disambiguator's value at production cadence (120s polling).</ref>
    <ref type="related_doc">infra/aws/lambda/ci/INF_GOLD_RUNNER_DEPLOYMENT.md (AE 0.7 7-finding catalog; INFINGE TO 1a-2 deployment doc; TO-8 ships disambiguation procedure addition + 8th finding sub-of-#7 nohup/setsid procedure)</ref>
  </references>

  <context>
    AE 0.7's chain monitor (`bz7cjbk19` pattern) currently matches terminal-only signal: dashboard.json ETag flip. During multi-step chain (B → C → D), monitor reports STALE for the duration of intermediate stages even when chain is healthy. This created false-stuck signals during D3 chain 2026-05-05 (B-chain done 20:45Z but monitor stale; required SSM ground-truth probe).

    Disambiguation procedure (CTO authored): "is intermediate output landing?" Tiebreaker via `aws s3 ls` on intermediate paths (gold/canonical/, gold/holdings/, etc.) — if recent partition writes exist, chain is progressing; if not, chain is stuck.

    Two implementation paths:
    - **(a) Broaden monitor regex** to include intermediate-stage matchers (gold/canonical/, gold/holdings/, gold/artifacts/) — single-monitor multi-trigger.
    - **(b) Pair monitor with intermediate-S3-poll** — separate monitors per stage, OR shell-script poll loop alongside terminal-ETag monitor.

    Path (b) is cleaner architecturally; path (a) is faster to ship. AE 0.7 chooses based on monitor framework constraints.
  </context>

  <phase id="0" when="Phase 0 — enumerate intermediate signals">
    <step>
      <run>Catalog reliable intermediate signals across all chain types (D2c / D2d / D3 / D4 / B-chain / C-chain). For each chain type, list S3 prefixes that update during execution (gold/canonical/, gold/holdings/, gold/artifacts/, etc.) + characteristic LastModified deltas.</run>
      <expect>Disambiguation table per chain type — "if X path has LastModified within last N min, chain is progressing"</expect>
      <if_mismatch>If chain types share no common intermediate signal: re-think; possibly per-chain monitor regex needed.</if_mismatch>
    </step>
    <step>
      <run>Choose path (a) regex broaden vs (b) intermediate-S3-poll based on AE 0.7 monitor framework + complexity tradeoff.</run>
      <expect>Path locked; rationale documented in TO `<phase_0_findings>`</expect>
      <if_mismatch>Surface choice to me + CTO if non-obvious tradeoff</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="Phase 1 — implement chosen path">
    <step>
      <run>Implement chosen monitor pattern (regex broaden OR S3-poll pair). Test against historical D2c/D2d/D3/D4 incidents — does it correctly disambiguate "progressing" vs "stuck"?</run>
      <expect>Monitor disambiguates reliably across all chain types</expect>
      <if_mismatch>Per-chain false-positive: refine</if_mismatch>
    </step>
    <step>
      <run>Update `infra/aws/lambda/ci/INF_GOLD_RUNNER_DEPLOYMENT.md` (AE 0.7 owns this doc) with disambiguation procedure: when monitor stale, run `aws s3 ls <intermediate path>` to check progress; chain types covered + expected LastModified deltas.</run>
      <expect>Doc updated; on-call procedure clear</expect>
      <if_mismatch>If doc location moved: update reference in INFREL PRD §4.5</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="Phase 2 — commit + ship">
    <step>
      <run>safe-commit.sh + push CLOUD branch</run>
      <expect>Clean commit; doc + monitor pattern shipped</expect>
      <if_mismatch>Per safe-commit protocol</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="Phase 3 — empirical validation on next chain run">
    <step>
      <run>Validate on next D-chain run (likely 2026-05-06 OR earlier if sprint dispatch). Monitor should show "progressing" during intermediate stages + "complete" on terminal. False-stuck should NOT occur.</run>
      <expect>One full chain run end-to-end with disambiguation working</expect>
      <if_mismatch>If false-stuck recurs: re-investigate; do NOT close</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Absorbs INFINGE TO 1a-3.** Mark INFINGE TO 1a-3 cancelled-as-absorbed in INFINGE TO ledger. Andrew can ratify either parent.</coord>
    <coord>**Parallel-able with TO-1 + TO-2 + Phase 2 TOs.** No direct dependency.</coord>
    <coord>**Cross-reference INF_GOLD_RUNNER_DEPLOYMENT.md** — AE 0.7 owns this doc per INFINGE TO 1a-2; disambiguation procedure goes in same doc.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">N/A — monitor pattern is operational, not infrastructure</phase>
    <phase id="2" when="before commit">safe-commit.sh</phase>
    <phase id="3" when="after deploy">empirical chain-run validation</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Monitor logs disambiguate "chain progressing" vs "chain stuck" reliably across D2c/D2d/D3/D4 chain types — empirical test on next chain run.</criterion>
    <criterion id="AC2">Disambiguation procedure documented in `infra/aws/lambda/ci/INF_GOLD_RUNNER_DEPLOYMENT.md`.</criterion>
    <criterion id="AC3">RAVC5 close: commit hash + doc updated + one full chain run with disambiguation working.</criterion>
    <criterion id="AC4">**Empirical-replay AC (D3 incident 2026-05-05):** Monitor (or paired S3-poll) would have detected B-chain finish 20:45Z → no `from_INF_C_00` chain log start within 5min (by 20:50Z) → fire alarm/notification BEFORE 21:00Z auto-shutdown manifested. Tonight's stall would have surfaced 15-30min earlier than actual SSM ground-truth probe under TO-8 acceptance state.</criterion>
    <criterion id="AC5">**Empirical-replay AC (D3f canonical_performance halt 2026-05-05):** Monitor (or paired S3-poll) would have detected `gold/canonical/canonical_performance_*` last-write at 21:16Z → no new partition writes within 5min (by 21:21Z) → trigger SSM-side ground-truth check (PID alive? heartbeat alive?) BEFORE 21:25Z watchdog fire. DS~C's manual disambiguation at 21:24Z used exactly this pattern at 120s polling cadence; codify as automated procedure.</criterion>
    <criterion id="AC6">**Catalog AC — finding #8 sub-of-#7:** `INF_GOLD_RUNNER_DEPLOYMENT.md` 7-finding catalog updates with finding #8: "SSM background processes (heartbeat, guard, watchers) MUST use `nohup` OR `setsid` to detach from process group. bash SIGHUP on SSM shell exit kills backgrounded processes by default → heartbeat death → watchdog cascade → `sudo shutdown -h now` mid-run. Defensive belt-and-suspenders: pair `nohup` with continuous `shutdown -c` loop every 20s." D3f fix is the canonical reference implementation.</criterion>
    <criterion id="AC7">**Per CTO INFREL PRD v0.2 §6 ratchet:** TO-8 ACs (above) get mirrored into PRD v0.2 §6 cross-reference at TO-1 + TO-2 RCA RAVC absorption time. TO file body remains canonical.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — pending COO dispatch GO post Andrew acceptance</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged` until Andrew acceptance OR COO dispatch decision. AE 0.7 lead per PRD §6 + INFINGE TO 1a-2 doc author. Absorbs INFINGE TO 1a-3.</message>
  </go_signal>

  <phase_0_findings>
    <path_chosen>b — paired intermediate S3-poll alongside terminal monitor</path_chosen>
    <rationale>Terminal ETag monitor (dashboard.json) is correct and should remain unchanged. Intermediate signal check adds a tiebreaker procedure: (1) chain log size delta, (2) per-stage S3 artifact LastModified, (3) SSM ground-truth process check. Path (a) regex broaden would require changing the monitor mechanism and risks false triggers from log path matches. Path (b) is documentable, per-chain-type tunable, and validated by DS~C's 2026-05-05 manual disambiguation at 120s cadence.</rationale>
    <classified_date>2026-05-06</classified_date>
    <classified_by>0.7.0_AE_CloudOps</classified_by>
    <intermediate_signals_table>
      S3 prefix: gold/logs/from_{label}_{ts}.log — grows each step; size delta = progressing
      S3 prefix: gold/canonical/canonical_holdings_* — updated by INF_B_00
      S3 prefix: gold/canonical/canonical_performance_* — updated by INF_C_00 (D3f incident signal)
      S3 prefix: gold/artifacts/employee_leaderboard.json — updated by INF_D_00c (D-chain start)
      S3 prefix: gold/artifacts/firm_mix_views.json — updated by INF_I_D03 (D-chain mid)
      S3 prefix: gold/artifacts/summary/ — updated by INF_D_04 (D-chain mid)
      S3 prefix: /firm/dashboard.json — updated by INF_D_08 (TERMINAL = CHAIN COMPLETE)
    </intermediate_signals_table>
    <doc_created>infra/aws/lambda/ci/INF_GOLD_RUNNER_DEPLOYMENT.md — 7+1 findings catalog + disambiguation table + SOP</doc_created>
    <finding_8>SSM SIGHUP cascade: background processes without nohup die on SSM shell exit → heartbeat death → watchdog fire → shutdown. Fix: nohup + belt-and-suspenders shutdown -c loop. D3f structural fix is canonical reference implementation. Sub-of-finding-7 (dual shutdown triggers).</finding_8>
    <phase_1_status>COMPLETE — doc authored, contains disambiguation procedure (AC2) + finding catalog (AC6)</phase_1_status>
    <phase_2_status>PENDING commit + push; phase_3 empirical validation on next chain run</phase_2_status>
    <empirical_replay_ac4>D3 incident: B-chain completed 20:45Z; no from_INF_C_00 log start by 20:50Z. Procedure: check gold/logs/ for new chain log OR check gold/canonical/canonical_performance LastModified. Would have surfaced stall by 20:50Z (15 min before 21:05Z SSM ground-truth probe).</empirical_replay_ac4>
    <empirical_replay_ac5>D3f: gold/canonical/canonical_performance LastModified was 21:16Z. S3-ls check at 21:21Z (5 min stale) → trigger SSM probe → find watchdog-about-to-fire before 21:25Z actual shutdown. DS~C's manual 21:24Z check was 1 min too late; automated 5-min stale threshold would catch it.</empirical_replay_ac5>
  </phase_0_findings>
</task_order>
