<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-ornren-002-ae-orion-dispatch</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-04-22</date>
    <status>active</status>
    <project_code>ADVI_INFLEC</project_code>
    <urgency>HIGH — gates next Orion D-chain dispatch. Blocked on ORNREN.001 DS completing S3 upload.</urgency>
    <andrew_directive>2026-04-22 in-session: Orion scripts must not carry firm-specific I_ prefix. Match BD convention.</andrew_directive>
  </metadata>

  <objective>
    Update EC2 dispatch wiring + SSM runner references after DS completes ORNREN.001 script
    renames. AE owns: EC2_MANIFEST dispatch_script entry, SSM runner commands, and any
    hardcoded I_* references in infrastructure config.
  </objective>

  <prerequisite>
    ORNREN.001 (DS) must be complete with MCP confirmation before starting. DS will MCP
    "ORNREN.001 DS complete — S3 MATCH confirmed" as the GO signal.
  </prerequisite>

  <steps>
    <step id="1">
      Update EC2_MANIFEST.json: any entry for the Orion gold runner (inf-gold-layer-runner,
      i-0ed5afded2ebd4ed4) that references inf-gold-dispatch.sh must be updated to
      orion-gold-dispatch.sh.
    </step>
    <step id="2">
      Update any SSM runner commands (inf_w49_runner.py / inf_w49_resume.py references)
      to orion_runner.py / orion_resume.py. Check SSM document templates or wrapper scripts
      that hardcode these names.
    </step>
    <step id="3">
      Verify no remaining I_* or inf-gold-dispatch.sh references exist in:
        - infra/aws/ec2/EC2_MANIFEST.json
        - Any SSM document or wrapper script targeting inf-gold-layer-runner
        - Any Terraform EC2 user_data or launch template referencing old names
    </step>
    <step id="4">
      Commit EC2_MANIFEST changes (author 0.7.0_AE_CloudOps). Push to CLOUD.
    </step>
    <step id="5">
      MCP COO + DS: "ORNREN.002 AE complete — EC2_MANIFEST updated, SSM wiring clean.
      Orion pipeline ready for next dispatch under new naming convention."
    </step>
  </steps>

  <acceptance_criteria>
    1. EC2_MANIFEST.json dispatch_script updated: inf-gold-dispatch.sh -> orion-gold-dispatch.sh.
    2. No remaining inf_w49_runner.py / inf_w49_resume.py / I_* hardcodes in infra config.
    3. Committed + pushed to CLOUD.
    4. MCP COO + DS confirming ORNREN.002 complete.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT start before DS MCPs ORNREN.001 complete with S3 MATCH confirmation.</rule>
    <rule>Do NOT rename S3 keys — DS handles all S3 operations in ORNREN.001.</rule>
    <rule>Do NOT restart the EC2 instance — wiring changes take effect on next SSM dispatch, no restart needed.</rule>
  </do_not>
</task_order>
