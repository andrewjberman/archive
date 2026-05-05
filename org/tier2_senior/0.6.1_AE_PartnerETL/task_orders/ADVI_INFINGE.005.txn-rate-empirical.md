<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.005</id>
    <project>ADVI_INFINGE</project>
    <title>TXN rate-empirical investigation (TO-5a; gates TO-5b TXN Lambda migration decision)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>pending</status><!-- Authored sprint mode 2026-05-05T~21:43Z post TO-4 deferral (Option C). PRD v0.2 commit 050bd3695 §6.2 TO-5a spec. Independent of TO-4 PERFORMANCE follow-on; can run now. -->
    <priority>medium</priority>
    <estimated_effort>~30-60min empirical test only; no code/TF changes</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6.2 TO-5a (rate-empirical) → TO-5b (Lambda migration if rate-OK) conditional</ref>
    <ref type="related">INFREL TO-5 transactions_v2 Lambda migration — gates on TO-5a result</ref>
    <ref type="phase_0_context">Phase 0 RAVC3 (AE 0.6.1) — TXN dim has unknown sustained RPS budget under Orion; Lambda-fit unknown without empirical</ref>
  </references>

  <context>
    The `transactions` dim (path-2, INFINGE Phase 1b) requires Orion REST API rate-empirical test before Lambda migration commitment. TXN volume is highest of all path-2 dims; if 2+ RPS not sustainable from Lambda environment, migration may force timeout-bound multi-invocation pattern OR keep TXN on orchestrator until Orion side resolves.

    **Investigation goal:** measure sustainable RPS for `pull_inflection_transactions.py` (or canonical TXN pull script — verify name matches actual file per TO-4 lesson) under representative Lambda config (3072MB / 900s).

    **Decision feed-forward:**
    - 2+ RPS sustainable → TO-5b dispatch as standard Lambda migration (TO-1/2/3 template).
    - 1-2 RPS sustainable → TO-5b scope changes (longer wall + smaller batch + multi-invoke OR keep on orchestrator).
    - <1 RPS sustainable → TXN stays on orchestrator; INFREL TO-5 transactions_v2 likely also stays.
  </context>

  <phase id="1" when="empirical only — no infrastructure changes">
    <step>
      <run>Verify canonical TXN pull script existence + LOCAL_PULLS_DIR convention. Per TO-4 pre-flight lesson: `ls data/orion/manual_api/pull_inflection_transactions*.py` + grep for module-level `LOCAL_PULLS_DIR` constant. If hardcoded path-resolve pattern (like `pull_inflection_performance_rest.py` line 323): surface to me + DS lane for refactor before TO-5b.</run>
      <expect>Script exists + LOCAL_PULLS_DIR module constant present</expect>
      <if_mismatch>If script missing OR hardcoded inline path: defer TO-5b authoring + flag DS lane for script refactor</if_mismatch>
    </step>
    <step>
      <run>Run `pull_inflection_transactions.py` (or actual canonical) locally OR on inf-bronze-runner EC2 with timer. Measure: total wall (start to last-row-write); peak memory (via `time -v` or equivalent); API call count; observed RPS (calls/wall_seconds); 429/503 rate-limit response count.</run>
      <expect>Empirical numbers — wall, memory peak, calls, RPS, 429 count</expect>
      <if_mismatch>If 429s exceed 5% of calls: rate-limit threshold being hit; reduce concurrency or add backoff; rerun</if_mismatch>
    </step>
    <step>
      <run>RAVC3 Phase 1: classify outcome:
        - Class A (≥2 RPS sustainable, no 429s): TO-5b dispatch as standard Lambda migration
        - Class B (1-2 RPS, occasional 429s): TO-5b scope adjusted (longer wall, smaller batch, multi-invoke pattern OR keep on orchestrator)
        - Class C (&lt;1 RPS or persistent 429s): TXN stays on orchestrator; flag for INFREL TO-5 (transactions_v2) also-defer
      </run>
      <expect>Classification + recommended path documented in TO `<phase_0_findings>` block</expect>
      <if_mismatch>If results are ambiguous (e.g., highly variable RPS): rerun 3 times across different time windows; report distribution</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Independent of TO-4 deferral.** Can run now; no infrastructure changes; pure empirical.</coord>
    <coord>**Feeds TO-5b decision.** Determines whether INFINGE TXN Lambda migration is 1 TO or N TOs (multi-invoke pattern).</coord>
    <coord>**Feeds INFREL TO-5 (transactions_v2).** Per CTO PRD §7 OQ4: if TXN rate-bound, transactions_v2 likely shares constraint; INFREL TO-5 stays on orchestrator until rate-empirical resolves.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before running test">comp-pipescript io <txn pull script> — verify input/output contract matches Lambda packaging assumptions</phase>
    <phase id="2" when="post empirical">N/A — no commit gate (empirical only)</phase>
    <phase id="3" when="reporting">RAVC3 with classification + recommended path</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Empirical numbers documented: wall, memory peak, API call count, observed RPS, 429 count.</criterion>
    <criterion id="AC2">Classification (A/B/C) documented in TO `<phase_0_findings>` block.</criterion>
    <criterion id="AC3">Recommended TO-5b path documented (standard migration / multi-invoke / orchestrator-stay).</criterion>
    <criterion id="AC4">RAVC3 close: empirical findings + classification + recommendation; no terraform apply or tag bump (this is empirical-only).</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T~21:43Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. TO-4 deferred (Option C); TO-5a is independent + can proceed now. Empirical only — no TF apply, no tag bump. Sprint target ~30-60min. RAVC3 expectation: empirical numbers + class A/B/C + recommended TO-5b path. TO-5b dispatch decision flows from this RAVC.</message>
  </go_signal>
</task_order>
