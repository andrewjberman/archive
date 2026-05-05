<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.008</id>
    <project>ADVI_INFREL</project>
    <title>Watchdog regex broaden — intermediate-stage matchers + S3-poll disambiguator (folds INFINGE TO 1a-3)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- Authored sprint mode 2026-05-05T~21:15Z post PRD ADVI_INFREL v0.1 ship; flips to pending after Andrew acceptance OR COO dispatch decision. Absorbs INFINGE TO 1a-3 per CTO ratify 2026-05-05T~21:00Z (option a — drop INFINGE TO 1a-3, ship as INFREL TO-8). -->
    <priority>medium</priority>
    <estimated_effort>~0.25d</estimated_effort>
    <absorbs>INFINGE TO 1a-3 (cancelled-as-absorbed; mark in INFINGE TO ledger when next touched)</absorbs>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §4.5 + §6 TO-8</ref>
    <ref type="incident_evidence">2026-05-05 D3 chain — AE 0.7 monitor `bz7cjbk19` exhibited stale-signal-during-progressing-chain pattern; B-chain completed 20:45Z but C-chain didn't auto-trigger; monitor still WAITING at 20:53:49Z because regex matches FINAL platinum artifact (dashboard.json ETag), not intermediate stage transitions</ref>
    <ref type="cto_diagnostic_pattern">CTO message 20260505T210223Z — disambiguator: "is intermediate output landing?" `aws s3 ls` on intermediate paths (gold/canonical/, gold/holdings/, etc.) is canonical tiebreaker for "monitor stale during long chain — hung vs progressing"</ref>
    <ref type="related_doc">infra/aws/lambda/ci/INF_GOLD_RUNNER_DEPLOYMENT.md (AE 0.7 7-finding catalog; INFINGE TO 1a-2 deployment doc; TO-8 ships disambiguation procedure addition)</ref>
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
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — pending COO dispatch GO post Andrew acceptance</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged` until Andrew acceptance OR COO dispatch decision. AE 0.7 lead per PRD §6 + INFINGE TO 1a-2 doc author. Absorbs INFINGE TO 1a-3.</message>
  </go_signal>
</task_order>
