<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.001</id>
    <project>ADVI_INFREL</project>
    <title>Silver-chain sentinel/Lambda RCA + fix (foundational; gates Phase 2)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <secondary>0.7.0_AE_CloudOps</secondary>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>staged</status><!-- Authored sprint mode 2026-05-05T~21:15Z post PRD ADVI_INFREL v0.1 ship (commit 64ea399a3); flips to pending after AE 0.6.1 acks routing OR Andrew dispatches GO. AE 0.6.1 LEAD per PRD §6 + project JSON lane_note (Inflection-specific surface knowledge); AE 0.7 SECONDARY on EventBridge metrics + S3 ObjectCreated event audit. -->
    <priority>highest</priority>
    <estimated_effort>~0.25-0.5d investigation + ~0.5-1d fix; depends on root-cause class</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1 (commit 64ea399a3); §4.1 + §6 TO-1</ref>
    <ref type="evidence_baseline">DS~A pipeline audit `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-05/ADVI_INFLEC_pipeline_audit_session.md` — silver dims stale 6-7 days; AE 0.6.1 Phase 0 RAVC3 — `inf-silver-chain` Lambda EventBridge rule ENABLED but not propagating</ref>
    <ref type="related_work">INFINGE TO-1 (assets-v2 Lambda LIVE 270d37c98; bronze writes succeeding) — shows the silver propagation gap is downstream of bronze, not a bronze issue</ref>
  </references>

  <context>
    `inf-silver-chain-bronze-complete` EventBridge rule (S3 ObjectCreated `_BRONZE_COMPLETE.json` → fires `inf-silver-chain` Lambda) is ENABLED but silver dim partitions are 6-7 days stale despite fresh bronze partitions. Three dims affected:
    - `silver/api_dims/accounts_v2/` — latest 2026-04-29 (6 days)
    - `silver/api_dims/assets_v2/` — latest 2026-04-29 (6 days; manual backfill via gold-runner per AE 0.6.1; cron-Lambda not picking up)
    - `silver/api_dims/performance/` — latest 2026-04-28 (7 days)

    Three competing root-cause classifications need empirical disambiguation:
    - **(a) sentinel-not-written** — bronze runner orchestrator.py succeeds but doesn't write `_BRONZE_COMPLETE.json` → EventBridge rule never fires → Lambda never invoked.
    - **(b) sentinel-written-but-Lambda-failing-silently** — sentinel writes; Lambda invokes but errors mid-execution and doesn't surface.
    - **(c) Lambda-skipping-some-dims** — Lambda invokes successfully but per-dim conversion errors are caught + suppressed.

    Fix scope materially differs by class:
    - (a) → bronze runner orchestrator.py code change + CW alarm on missing sentinel.
    - (b) → Lambda code change + CW alarm on Lambda failure; investigate suppressed errors.
    - (c) → Lambda code change to fail-loud per-dim + CW per-dim metrics.
  </context>

  <phase id="0" when="Phase 0 RCA — investigation only; classify root cause">
    <step>
      <run>CloudWatch logs `inf-silver-chain` Lambda — last 14 days. Identify firing pattern: how many invocations? Failures? Per-invocation duration?</run>
      <expect>Empirical answer to "did Lambda invoke daily?" Three sub-cases: (i) zero invocations in 14d → class (a); (ii) invocations occurred but errored → class (b); (iii) invocations succeeded but partial → class (c).</expect>
      <if_mismatch>If logs are missing/empty entirely, IAM may be misconfigured for log writes. Surface to me + CTO.</if_mismatch>
    </step>
    <step>
      <run>S3 ObjectCreated event delivery audit — was `_BRONZE_COMPLETE.json` written for 2026-05-01 / 2026-05-05 (known fresh-bronze dates)? Check via `aws s3 ls s3://opal-data-inf/bronze/orion-api-v2/2026-05-05/_BRONZE_COMPLETE.json`. Check EventBridge metrics for `inf-silver-chain-bronze-complete` rule firings.</run>
      <expect>If sentinel files don't exist on fresh-bronze dates → class (a) confirmed. If sentinels exist + rule fired → class (b) or (c).</expect>
      <if_mismatch>Per pre-confirm rule (memory `feedback_destructive_op_pre_confirm.md`): do NOT delete or modify any sentinel files during investigation; read-only.</if_mismatch>
    </step>
    <step>
      <run>Bronze runner orchestrator.py code review — does it write `_BRONZE_COMPLETE.json` after successful run? If yes, where + with what payload? If no, that's class (a) root cause.</run>
      <expect>Definitive answer on whether orchestrator.py emits the sentinel. Cross-reference with TO-2 May 4 RCA — if orchestrator chain doesn't flag completion correctly, both gaps may share architecture.</expect>
      <if_mismatch>If orchestrator.py is undocumented or absent: surface architecture gap to CTO; may require ADVI_INFREL_V2 expansion.</if_mismatch>
    </step>
    <step>
      <run>`inf-silver-chain` Lambda code review — does it gracefully handle missing dims or per-dim errors? Look for try/except suppressing errors OR per-dim failure that would manifest as class (c).</run>
      <expect>Class (c) confirmed if try/except blocks suppress errors silently. Document fix scope: per-dim CW metric + fail-loud emission.</expect>
      <if_mismatch>If Lambda code is well-structured + already fails loudly: class (c) ruled out; root cause is (a) or (b).</if_mismatch>
    </step>
    <step>
      <run>RAVC3 Phase 0: classify root cause as (a)/(b)/(c)/multi-class. Document in TO file `<phase_0_findings>` block. Surface to me for fix-scope ratify before Phase 1 begins.</run>
      <expect>Root cause locked; fix scope clear; CTO PRD v0.2 §5 Compiler Evidence ready to populate.</expect>
      <if_mismatch>If multi-class (e.g., sentinel-not-written AND Lambda-fails-silent): scope fix to address ALL classes; don't ship partial.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="Phase 1 fix — gates on Phase 0 RAVC3 + CTO ratify of fix scope">
    <step>
      <run>Class (a) fix — bronze runner orchestrator.py: add `_BRONZE_COMPLETE.json` write after successful daily chain. Payload: `{"date": "{date}", "dims_complete": [list], "completion_ts": "<ISO>"}`. Add CW alarm `Opal/InflectionBronze/SentinelMissing` on consecutive missing sentinels.</run>
      <expect>If class (a): orchestrator.py emits sentinel; EventBridge rule fires Lambda; silver propagates.</expect>
      <if_mismatch>Class (a) fix authored but Lambda still doesn't propagate → escalate to class (b) or (c) discovery; investigate Lambda invocation chain.</if_mismatch>
    </step>
    <step>
      <run>Class (b) fix — `inf-silver-chain` Lambda: surface error path; replace silent failure with fail-loud + CW alarm. Add `Opal/InflectionSilver/LambdaFailure` metric + alarm.</run>
      <expect>If class (b): Lambda failures surface to alarms; on-call sees them; per-failure debug path documented.</expect>
      <if_mismatch>Lambda has external dependency that errors transiently → add retry-with-backoff in Lambda or upstream invoker.</if_mismatch>
    </step>
    <step>
      <run>Class (c) fix — `inf-silver-chain` Lambda: per-dim error path with `Opal/InflectionSilver/DimConversionFailure` metric (dim={dim_name}). Per-dim alarm. Don't catch errors silently in per-dim loop.</run>
      <expect>If class (c): per-dim failures visible + alarmed; full propagation observability.</expect>
      <if_mismatch>If per-dim conversion has structural bug (e.g., schema mismatch): may need DS lane consult on dim conversion logic.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="Phase 2 ship — gates on Phase 1 fix + comp-iam gaps clean">
    <step>
      <run>terraform plan + comp-iam gaps + .tools/safe-commit.sh — per LAMBDA_DEPLOYMENT_PROTOCOL.md</run>
      <expect>Clean plan + 0 IAM gaps + safe-commit PASS</expect>
      <if_mismatch>Per LAMBDA_DEPLOYMENT_PROTOCOL.md mismatch resolution</if_mismatch>
    </step>
    <step>
      <run>terraform apply + 0-diff verify + tag bump (inf-pipeline-v1.7.X)</run>
      <expect>Apply 0-diff post-deploy + tag pushed --follow-tags</expect>
      <if_mismatch>Per LAMBDA_DEPLOYMENT_PROTOCOL.md mismatch resolution</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="Phase 3 empirical — 24h cycle">
    <step>
      <run>24h cycle empirical — fresh `silver/api_dims/{accounts_v2,assets_v2,performance}/{D+1}/` partitions WITHOUT manual intervention. CW Metric `Opal/InflectionSilver/LambdaInvoked > 0` daily. CW Alarm test via 24h smoke.</run>
      <expect>AC1-AC4 satisfied; silver gap reduced to 0 days within 48h post-fix ship.</expect>
      <if_mismatch>If silver still doesn't propagate post-fix: re-RCA in same TO; do NOT close; possibly multi-class scope.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Foundational — gates Phase 2.** All INFREL Phase 2 TOs (TO-4..7 path-1 dim Lambda migrations) gate on this TO ship. Bronze writes succeed but silver doesn't propagate without TO-1 fix.</coord>
    <coord>**Cross-reference TO-2 (May 4 RCA).** If TO-1 RCA shows orchestrator.py doesn't write sentinels even on success, May 4 gap may share root-cause architecture (orchestrator chain not flagging completion). Coordinate findings.</coord>
    <coord>**AE 0.7 secondary lane** — assist on EventBridge metrics + S3 ObjectCreated event audit (AE 0.7 owns CloudOps Lambda+EventBridge primary surface). Heavy lifting on Lambda code + bronze runner code stays AE 0.6.1 lead.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before writing fix">comp-iam service inf-silver-chain + comp-iam service inf-bronze-runner + comp-routes trace inf-silver-chain (full path EventBridge → S3 → Lambda → silver write) + comp-pipescript io <bronze runner orchestrator entry></phase>
    <phase id="2" when="before commit">comp-iam gaps + ds-commit-gate.sh + safe-commit.sh</phase>
    <phase id="3" when="after deploy">24h empirical observation; CW Metric + Alarm verify</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Silver dim partitions land within 6h of bronze partition write — empirical 24-48h post-fix ship.</criterion>
    <criterion id="AC2">CW Metric `Opal/InflectionSilver/LambdaInvoked` > 0 daily.</criterion>
    <criterion id="AC3">CW Alarm fires on Lambda failure (test via deliberate failure injection 24h smoke).</criterion>
    <criterion id="AC4">Silver gap reduced to 0 days within 48h post-fix ship.</criterion>
    <criterion id="AC5">RCA classification documented in TO file `<phase_0_findings>` + CTO PRD v0.2 §5 Compiler Evidence absorption package.</criterion>
    <criterion id="AC6">RAVC5 close: commit hash + apply 0-diff + tag bump + 24-48h empirical evidence + comp-iam gaps clean.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — pending COO dispatch GO post Andrew acceptance OR auto-flip post v0.2 ratchet planning</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged` until Andrew acceptance OR COO dispatch decision. AE 0.6.1 LEAD with AE 0.7 secondary per PRD §6 + project JSON lane_note. Foundational; gates Phase 2 TOs (TO-4..7 path-1 dim Lambda migrations). Sprint-mode batch authoring complete this turn (TO-1..9 staged).</message>
  </go_signal>
</task_order>
