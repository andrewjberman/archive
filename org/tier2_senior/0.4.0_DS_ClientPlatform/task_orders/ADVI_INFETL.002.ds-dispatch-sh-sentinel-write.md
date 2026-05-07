<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.002</id>
    <project>ADVI_INFETL</project>
    <title>orion-gold-dispatch.sh writes gold/meta/pipeline-complete.json sentinel at chain success</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>normal</priority>
    <estimated_effort>~0.25d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md §3 (5-tier model, Tier 4 sentinel write at chain end), §4 (component specs), §6 Phase 1 TO-2</ref>
    <ref type="bd_pattern">data/black_diamond/scripts/gold/bd-canonical-prices-incremental.sh — sentinel write at chain success (canonical reference for the pattern)</ref>
    <ref type="target_file">data/orion/scripts/gold/orion-gold-dispatch.sh</ref>
    <ref type="ownership">CLAUDE.md rule 13 — DS owns gold-script commit→QA-deploy cycle including S3 upload, even when DT is online</ref>
  </references>

  <context>
    INFETL §3 architecture mandates that Tier 4 (gold) writes a completion sentinel
    `gold/meta/pipeline-complete.json` at successful chain end. This sentinel is the
    structural prerequisite for the S3-event-driven publisher chain (Tier 5a) being
    wired in TO-5: `aws_s3_bucket_notification.opal_data_inf` will fire `inf-portal-publisher`
    on ObjectCreated for that key. Without the sentinel write in dispatch.sh, the
    publisher cannot be invoked even after TO-1 (cron) and TO-3 (publisher Lambda) ship.

    The sentinel JSON metadata must include enough information for downstream
    consumers to identify the run (chain mode, run date, completion timestamp).

    Negative path is critical: dry-run / --single / --from modes that do NOT execute
    the full chain must NOT emit the sentinel — emitting on a partial run would fire
    the publisher against incomplete state.
  </context>

  <scope>
    <step>
      Read data/orion/scripts/gold/orion-gold-dispatch.sh fully. Identify the chain-success
      branch (after all 40 scripts in CHAIN_FULL exit 0) and the modes that run it
      (--chain full vs --single vs --from vs --dry-run).
    </step>
    <step>
      Add a sentinel-write step at chain success ONLY (i.e., gated on CHAIN_FULL
      successful completion; not in --single or --from or --dry-run paths).
      The write must include this minimum metadata in the JSON body:
        {
          "chain": "full",
          "run_date": "{YYYY-MM-DD}",       // chain run target date
          "completed_at": "{ISO-8601 UTC}", // wall-clock completion timestamp
          "git_sha": "{git rev-parse HEAD}", // optional but recommended for traceability
          "instance_id": "{IMDS instance-id}" // optional
        }
      Write target: s3://opal-data-inf/gold/meta/pipeline-complete.json
      Use `aws s3 cp` (NOT `aws s3api put-object`) for parity with existing dispatch.sh patterns.
    </step>
    <step>
      Pre-commit gate: NONE (this is a .sh file, not .py — ds-commit-gate.sh covers Python).
      Manual verification: bash -n orion-gold-dispatch.sh (syntax check), and a dry-run
      to confirm sentinel does NOT emit on dry-run.
    </step>
    <step>
      Commit via .tools/safe-commit.sh with --author "0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;"
      -m "feat(ADVI_INFETL.002): orion-gold-dispatch sentinel write gold/meta/pipeline-complete.json at chain success"
      -- data/orion/scripts/gold/orion-gold-dispatch.sh
    </step>
    <step>git push origin CLOUD</step>
    <step>S3 upload: aws s3 cp data/orion/scripts/gold/orion-gold-dispatch.sh s3://opal-data-inf/code/gold/orion-gold-dispatch.sh</step>
    <step>Verify: comp-pipescript deployed orion-gold-dispatch.sh — must show MATCH (no drift between local and S3-deployed copy).</step>
    <step>
      QA empirical: dispatch a manual chain via inf-gold-qa-runner SSM (NOT the PROD runner)
      using OUTPUT_PREFIX=qa/ to avoid platinum collisions. After QA chain success, verify:
        aws s3 ls s3://opal-data-inf/gold/meta/pipeline-complete.json
      Then test dry-run: confirm pipeline-complete.json key timestamp does NOT update
      after a --dry-run dispatch. (May need to set OUTPUT_PREFIX=qa/ for the dry-run probe.)
    </step>
    <step>RAVC to COO: commit hash + S3 ETag + comp-pipescript MATCH evidence + QA SSM CmdId + sentinel JSON sample.</step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript deployed orion-gold-dispatch.sh — required MATCH</tool>
    <tool>comp-blast orion-gold-dispatch.sh — should show new edge to inf-portal-publisher AFTER TO-3 + TO-5 ship (forward-looking; not gated on this TO)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Single-line edit (or small bash block) ships clean — bash -n PASS, comp-pipescript deployed MATCH.</criterion>
    <criterion id="AC2">QA dispatch on inf-gold-qa-runner emits sentinel at chain end (S3 head-object confirms object presence + LastModified within seconds of chain completion).</criterion>
    <criterion id="AC3">Sentinel JSON metadata includes chain label + run_date + completed_at timestamp at minimum (additional fields acceptable).</criterion>
    <criterion id="AC4">Dry-run + --single + --from modes do NOT emit sentinel (negative path verified empirically — sentinel object timestamp unchanged after partial-mode dispatches).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — TO-2 ships in parallel with TO-1, TO-3, TO-4.</upstream>
    <downstream>TO-5 (S3 ObjectCreated rule wiring) cannot be empirically validated until TO-2 sentinel writes are landing.</downstream>
  </gates_dependencies>

  <risks_failure_modes>
    <risk>
      Sentinel emits on partial-run modes due to missed gating → triggers publisher against
      incomplete gold state → produces inconsistent platinum. AC4 negative-path test is the gate.
    </risk>
    <risk>
      QA empirical run takes ~60-90 min for full chain. Plan for the QA dispatch to land
      overnight or during a working block; do NOT block the TO RAVC on multi-hour wait.
      Acceptable to send RAVC after AC1+AC2 with AC3+AC4 verified post-QA-completion in a
      follow-on RAVC2.
    </risk>
  </risks_failure_modes>

  <go_signal>
    <issued_at>pending Andrew confirmation of OQ1+OQ8+INFNNA-scope</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD. TO authored pre-Andrew GO per CTO RAVC2 authorization. COO will dispatch via inbox message + status flip to "active" when Andrew confirms scope.</message>
  </go_signal>
</task_order>
