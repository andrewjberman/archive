<task_order>
  <metadata>
    <id>ADVI_INFLEC.W4.13b.ae-inflec-ic00-run4-dchain</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-27</date>
    <status>pending</status><!-- CTO GO issued 20260427T125350Z (two-item batch: item 1). -->
    <project_code>ADVI_INFLEC</project_code>
    <priority>P0 — blocks ADVI_RDVSDS Phase 1, ORNREN.001/Q8/Q9, and DS ORNREN chain</priority>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md</ref>
    <ref type="prior_session">org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-04-24/inf_w4.13b_scopefix_chain_session2.md</ref>
    <ref type="fix_commit">2777a166 — advisor_key pulled from acct_dim instead of holdings (DS 0.4.0, S3 MATCH confirmed 21:07Z 2026-04-24)</ref>
  </references>

  <context>
    This is W4.13b I_C00 run 4. Prior runs failed for different reasons:
    - Run 1: scope contamination (canonical/ files quarantined)
    - Run 2: instance auto-stopped mid-upload (4.5h runtime, 0 rows written to S3)
    - Run 3: advisor_key column missing from holdings parquet (WARN-silenced, 0/2408 dates written)

    State as of 2026-04-27 (confirmed by CTO):
    - Silver purge (transactions/ + aum_snapshot/ + watermark): COMPLETE (2026-04-24)
    - I_A03 + full B-chain: COMPLETE (2026-04-24)
    - I_C00 advisor_key fix: COMPLETE (2777a166), S3 MATCH confirmed 21:07Z 2026-04-24
    - I_C00 output on S3: NONE (0 rows written in run 3)
    - D-chain: NOT run yet

    Scope: dispatch I_C00 (run 4) only. On PASS, dispatch D-chain. Do NOT restart from I_A03.
    Instance: i-0ed5afded2ebd4ed4 (inf-gold-layer-runner)
  </context>

  <objective>
    Execute I_C00 on inf-gold-layer-runner via SSM. Verify rows written to gold/canonical/.
    On I_C00 PASS: execute D-chain (--from I_D00). On D-chain PASS: comp-validate I_09.
    RAVC4 to CTO + COO with artifact evidence.
  </objective>

  <scope>
    Step 1 — Instance start:
      aws ec2 start-instances --instance-ids i-0ed5afded2ebd4ed4
      Wait until State=running (describe-instances poll).

    Step 2 — Verify deployed script:
      comp-pipescript deployed I_C00
      Expect: MATCH (2777a166 fix must be on runner).
      If STALE: upload is NOT needed — DS already confirmed S3 MATCH 21:07Z 2026-04-24.
      If STALE still shows: MCP COO immediately (do not run).

    Step 3 — Dispatch I_C00 only:
      aws ssm send-command --instance-ids i-0ed5afded2ebd4ed4 \
        --document-name AWS-RunShellScript \
        --parameters 'commands=["bash /tmp/inf-gold-dispatch.sh --single I_C00"]' \
        --comment "W4.13b run4 I_C00 advisor_key fix"
      Record command ID. Monitor via get-command-invocation until status IN_PROGRESS -> Success/Failed.

    Step 4 — I_C00 output verification:
      aws s3 ls s3://opal-data-inf/gold/canonical/ --recursive | grep "canonical_performance" | wc -l
      Expect: 1881+ rows (one per date). If 0: STOP, MCP COO + CTO immediately.
      Also confirm: timestamps on the new files are TODAY (not 2026-04-24 quarantine files).

    Step 5 — Dispatch D-chain:
      aws ssm send-command --instance-ids i-0ed5afded2ebd4ed4 \
        --document-name AWS-RunShellScript \
        --parameters 'commands=["bash /tmp/inf-gold-dispatch.sh --from I_D00"]' \
        --comment "W4.13b run4 D-chain post I_C00 PASS"
      Monitor to completion (~1-2h).

    Step 6 — Platinum artifact verification:
      aws s3 ls s3://opal-data-inf/platinum/firm/ | grep -E "leaderboard|partner_analytics"
      aws s3 ls s3://opal-data-inf/platinum/advisors/ --recursive | wc -l
      Expect: leaderboard.json + partner_analytics.json present; at least 11 advisor files.
      Download partner_analytics.json: aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics.json /tmp/inflec_partner_analytics.json

    Step 7 — comp-validate:
      comp-validate I_09 --artifact /tmp/inflec_partner_analytics.json
      Must exit 0 before RAVC4. If non-zero: MCP COO + CTO with error output.
  </objective>

  <acceptance_criteria>
    1. I_C00 SSM exits Success (not Failed).
    2. s3://opal-data-inf/gold/canonical/ has 1881+ canonical_performance_*.parquet files with today's timestamps.
    3. D-chain SSM exits Success.
    4. platinum/firm/leaderboard.json present.
    5. platinum/firm/partner_analytics.json present.
    6. platinum/advisors/ contains at least 11 advisor subdirectories.
    7. comp-validate I_09 exits 0.
    8. RAVC4 MCP to COO + CTO with: I_C00 row count, D-chain duration, artifact inventory, comp-validate output.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before run">
      <run>comp-pipescript deployed I_C00</run>
      <expect>MATCH — confirms 2777a166 fix is on runner. STALE = stop, MCP COO.</expect>
    </phase>
    <phase id="2" when="after I_C00 completes">
      <run>aws s3 ls s3://opal-data-inf/gold/canonical/ --recursive | grep canonical_performance | wc -l</run>
      <expect>1881+. Zero = stop, MCP COO.</expect>
    </phase>
    <phase id="3" when="after D-chain completes">
      <run>comp-validate I_09 --artifact /tmp/inflec_partner_analytics.json</run>
      <expect>Exit 0. Non-zero = stop, MCP COO + CTO with full error output.</expect>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - DS 0.4.0: ORNREN.001 + Q8 + Q9 GOs fire on RAVC4 (COO dispatches)
    - ADVI_RDVSDS: RD 0.4.2 re-validation TO dispatches by CTO on RAVC4
    - Do NOT signal DS or RD directly — route through COO
    - If I_C00 produces unexpected account count (target ~1541, NOT ~2249 from contaminated run 3): MCP COO before proceeding to D-chain
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT restart chain from I_A03 — silver purge + I_A03 + B-chain are all COMPLETE.</rule>
    <rule>Do NOT run --chain full — I_C00 only first, then --from I_D00 on PASS.</rule>
    <rule>Do NOT signal DS or RD directly — COO owns the downstream GO dispatches.</rule>
    <rule>Do NOT declare PASS without comp-validate I_09 exit 0.</rule>
    <rule>Do NOT leave instance running after chain completion — auto-shutdown governs.</rule>
  </do_not>

  <deliverables>
    <deliverable type="artifact">gold/canonical/ + platinum/ populated in opal-data-inf</deliverable>
    <deliverable type="signal">RAVC4 MCP to 2.0.0_SA_COO + 1.0.0_SA_CTO with I_C00 row count + D-chain duration + comp-validate exit code</deliverable>
    <deliverable type="document">Session log at org/tier2_senior/0.6.0_AE_PartnerETL/logs/2026-04-27/inflec_w4.13b_run4.md</deliverable>
  </deliverables>
</task_order>
