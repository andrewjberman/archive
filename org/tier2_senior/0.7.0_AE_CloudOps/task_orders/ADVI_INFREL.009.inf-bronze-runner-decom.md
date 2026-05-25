<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.009</id>
    <project>ADVI_INFREL</project>
    <title>inf-bronze-runner EC2 deprecation (Phase 4 — final cleanup; gates on INFINGE Phase 1b + INFREL Phase 2 + 48h soak)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete-as-superseded</status><!-- Authored sprint mode 2026-05-05T~21:15Z. Gates on ALL of: INFINGE Phase 1b TOs ACCEPTED + INFREL Phase 2 TOs (TO-4..7) ACCEPTED + 48h soak with daily Lambda crons firing clean. Final cleanup; high-impact decom. **SUPERSEDED 2026-05-25 (AE 0.7 queue-hygiene flip, ws COO Path 3 GO post-INFETL-close `eecc50c19`):** Parent project ADVI_INFREL closed-as-superseded into ADVI_INFETL 2026-05-22 (REGISTRY row 75); ADVI_INFETL itself closed COMPLETE 2026-05-25 `eecc50c19`. bronze-runner-decom belongs in Phase-2-follow-on charter alongside silver-aggregator txn-sentinel restoration (root cause: ADVI_TXNAMG.004 TO-4 `aa7be4b5e` regression 2026-05-22) — ws CTO architectural-domain routing per ws COO §4. No substantive ship under this TO; queue-hygiene only. -->
    <priority>medium</priority>
    <estimated_effort>~0.5d AE post all gates green</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFREL.md v0.1; §3 REMOVED + §6 TO-9</ref>
    <ref type="related_prd">ADVI_INFINGE PRD v0.2 §6 — Phase 3 decom framing (INFREL TO-9 IS the implementation of INFINGE Phase 3)</ref>
    <ref type="ec2_protocol">docs/deployment/EC2_DEPLOYMENT_PROTOCOL.md (Terraform manages EC2 infrastructure; service-specific decom)</ref>
    <ref type="ec2_manifest">infra/aws/ec2/EC2_MANIFEST.json (source of truth; row delete required)</ref>
  </references>

  <context>
    `inf-bronze-runner` (t3.small EC2) currently runs orchestrator.py daily for path-1 + path-2 Inflection dims. Once INFINGE Phase 1b (path-2: assets_v2, reps, positions, performance, transactions) AND INFREL Phase 2 (path-1: unified_account_dim, transactions_v2, billing, tax) complete, runner has zero dim responsibilities.

    Decom scope:
    - EventBridge daily trigger removal (`opal-inf-bronze-runner-cron` Lambda + EventBridge rule)
    - SSM dispatch chain teardown
    - IAM role tear-down (`inf-bronze-runner-role`)
    - EBS volume detach + snapshot for archival
    - Terraform module removal in inf-pipeline
    - `EC2_MANIFEST.json` row delete
    - Tag bump (final inf-pipeline tag for decom)
  </context>

  <phase id="0" when="Phase 0 gates verification">
    <step>
      <run>Verify ALL gates green:
        1. INFINGE Phase 1b: TO-1 (assets-v2) + TO-2 (reps) + TO-3 (positions) + TO-4 (performance) + TO-5 (txn — if shipped per rate-empirical) ALL RAVC5 closed
        2. INFREL Phase 2: TO-4 (unified_account_dim) + TO-5 (transactions_v2 — if shipped per rate-empirical) + TO-6 (billing) + TO-7 (tax) ALL RAVC5 closed
        3. 48h soak: all Lambda crons firing clean for 2 consecutive days; no missing partitions; no CW alarms
        4. comp-blast inf-bronze-runner: zero remaining responsibilities post TO-7 closure
      </run>
      <expect>ALL gates green; comp-blast empty</expect>
      <if_mismatch>Any gate red: surface to me + CTO; do NOT proceed.</if_mismatch>
    </step>
    <step>
      <run>Pre-confirm decom scope via MCP citing PRD §3 REMOVED + this TO; await Andrew + CTO ratify before proceeding (per memory `feedback_destructive_op_pre_confirm.md` — runner deprecation is high-impact destructive).</run>
      <expect>Andrew + CTO ratify received</expect>
      <if_mismatch>Without ratify: do NOT proceed; this is a fully destructive operation.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="Phase 1 — soft decom (stop runner; keep state)">
    <step>
      <run>EC2 stop instance (do NOT terminate yet). Disable EventBridge rule `opal-inf-bronze-runner-cron`. Observe 48h: no downstream artifact gaps; all dim partitions land via Lambda crons.</run>
      <expect>48h soak clean; runner can be terminated safely</expect>
      <if_mismatch>If any partition gap surfaces during soak: re-enable runner; investigate; do NOT proceed to Phase 2 termination.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="Phase 2 — full decom (post 48h soak)">
    <step>
      <run>EBS snapshot for archival (`aws ec2 create-snapshot --volume-id <inf-bronze-runner-volume>` with description "Final pre-decom snapshot ADVI_INFREL.009"). Verify snapshot State=completed.</run>
      <expect>Snapshot created + retained per archival policy</expect>
      <if_mismatch>If snapshot fails: do NOT proceed to terminate; resolve snapshot issue first</if_mismatch>
    </step>
    <step>
      <run>Terraform destroy targeted: aws_instance.inf_bronze_runner + aws_iam_role.inf_bronze_runner_role + aws_lambda_function.opal_inf_bronze_runner_cron + aws_cloudwatch_event_rule.<bronze-cron> per inf-pipeline module. Run plan; review carefully (per pre-confirm protocol); apply.</run>
      <expect>Resources destroyed cleanly; 0 errors</expect>
      <if_mismatch>If destroy errors: investigate; may require manual cleanup; surface to me + CTO</if_mismatch>
    </step>
    <step>
      <run>Update EC2_MANIFEST.json — remove inf-bronze-runner row. Commit via safe-commit.sh.</run>
      <expect>Manifest reflects current state</expect>
      <if_mismatch>Per safe-commit protocol</if_mismatch>
    </step>
    <step>
      <run>Update lambda-source-map.json — remove opal-inf-bronze-runner-cron entry. Commit.</run>
      <expect>CI drift detection clean</expect>
      <if_mismatch>Per CLAUDE.md rule 4</if_mismatch>
    </step>
    <step>
      <run>Tag bump: inf-pipeline-vX.Y.Z (decom-final). Push --follow-tags.</run>
      <expect>Tag pushed</expect>
      <if_mismatch>Per CLAUDE.md tag versioning rule</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="Phase 3 — post-decom soak">
    <step>
      <run>7-day post-decom observation: no Lambda alarm; no partition gap; no downstream gold-tier breakage.</run>
      <expect>Clean operation; INFREL closure ready</expect>
      <if_mismatch>If breakage surfaces: re-create runner from snapshot; investigate; do NOT close</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Gates on ALL upstream:** INFINGE Phase 1b complete + INFREL Phase 2 complete + 48h soak + comp-blast empty.</coord>
    <coord>**HIGH-IMPACT DESTRUCTIVE.** Pre-confirm via Andrew + CTO before Phase 2 (terminate). Phase 1 (soft decom; stop+disable) is reversible.</coord>
    <coord>**`_BRONZE_COMPLETE.json` sentinel mechanism deprecation** — per PRD §3 REMOVED + §7 OQ6, sentinel becomes vestigial post Phase 2 (no orchestrator chain remaining). Decision point: deprecate sentinel mechanism as part of TO-9 OR separate cleanup TO. Default: include in TO-9 if simple; spin out if complex.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before Phase 1 soft decom">comp-blast inf-bronze-runner (zero-responsibilities verify) + comp-iam service inf-bronze-runner (final IAM surface review)</phase>
    <phase id="2" when="before Phase 2 destroy">terraform plan review + pre-confirm MCP + Andrew + CTO ratify</phase>
    <phase id="3" when="post-destroy">comp-iam gaps + safe-commit + 7-day soak</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Phase 0 gates ALL green; comp-blast inf-bronze-runner empty.</criterion>
    <criterion id="AC2">48h Phase 1 soft-decom soak clean (no partition gaps; no alarms).</criterion>
    <criterion id="AC3">EBS snapshot retained for archival.</criterion>
    <criterion id="AC4">Terraform destroy clean; 0 errors.</criterion>
    <criterion id="AC5">EC2_MANIFEST.json row removed.</criterion>
    <criterion id="AC6">lambda-source-map.json entry removed.</criterion>
    <criterion id="AC7">Tag bumped + pushed (decom-final).</criterion>
    <criterion id="AC8">7-day post-decom soak clean.</criterion>
    <criterion id="AC9">RAVC5 close: commit hash + apply 0-diff + tag + 7-day empirical + comp-iam gaps clean + Andrew + CTO ratify documented.</criterion>
    <criterion id="AC10">INFREL project closure RAVC; ADVI_INFINGE Phase 3 closure RAVC (this TO IS the implementation).</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>STAGED — gates on INFINGE Phase 1b + INFREL Phase 2 + 48h soak + Andrew/CTO ratify</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Status `staged`. HIGH-IMPACT DESTRUCTIVE; pre-confirm required before Phase 2.</message>
  </go_signal>
</task_order>
