<task_order>
  <metadata>
    <id>ADHC_DSFLOW.003</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADHC_DSFLOW</project_code>
    <priority>P2 (passive — fires on next natural gold-script commit by any DS lane post-DSFLOW.001+002 ship)</priority>
    <sla>No fixed SLA — fires when the next gold-script commit occurs; validation completes within normal DS deploy cycle (~1-2h)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_DSFLOW.md (sections 6.2 + 7 TO-3 + 10 acceptance)</ref>
    <ref type="precedent_tool">ADHC_DSFLOW.001 — `.tools/ds-commit-gate.sh` must be live</ref>
    <ref type="precedent_docs">ADHC_DSFLOW.002 — CLAUDE.md Rule 13 + DS prompt.md gate step + DS README CAN/CANNOT + feedback memory enforcement must be shipped</ref>
    <ref type="project_json">org/projects/ADHC_DSFLOW.json</ref>
    <ref type="memory">memory/feedback_ds_commits_ae_deploys.md — DS owns commit→push→S3→comp-pipescript MATCH→qa-runner-dispatch→RAVC4 close</ref>
    <ref type="non-retroactive">PRD §13 — HLOT2 `5f5d0319` exempt (already committed pre-gate); next BFIX or any subsequent DS gold-script commit is the natural trigger</ref>
  </references>

  <objective>
    Demonstrate the full DS-owned gold-script deploy cycle end-to-end on the next natural gold-script commit after DSFLOW.001 + DSFLOW.002 ship. Passive acceptance — no forced dispatch. Captures the first post-protocol deploy cycle as the operational proof that Rule 13 + the gate + the responsibility matrix are working.

    **Triggering conditions (any of):**
    - Next BFIX iteration (e.g. BFIX5 if Andrew opens a new scope; BFIX2b if subsumption probe surfaces work) by any DS lane (base / ~A / ~B / ~C / ~D)
    - Any HLOT3 follow-up (Reverse Split CA classifier or Spinoff asymmetric handler per HLOT2 L125-126 deferred-HLOT3a/b)
    - Any CP-DS1 / SL-P1 / WP-10b gold-script resumed work from the STAUDT backlog
    - Any schema-alignment / code-hygiene TO from ADVI_ROLLUP backlog that touches `data/black_diamond/scripts/gold/`

    **Not triggering:**
    - HLOT2 follow-through (already committed `5f5d0319`, exempt per PRD §13 non-retroactive)
    - Any non-gold-script commit (infra, org-docs, portal — outside scope)
    - Comparison-pack authoring (read-only diagnostic, not a deploy cycle)
  </objective>

  <scope>
    <files>
      <file action="none-directly">This TO adds no new files. It observes + validates an existing DS workflow execution.</file>
      <file action="emit">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{DATE}/dsflow_003_deploy_training_run.md — the session log IS the deliverable (full cycle captured with timestamp-per-step)</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="full-cycle-capture">
      On the triggering commit, DS executes + captures each step with timestamp + evidence:

      | Step | Tool | Evidence |
      |---|---|---|
      | 1. Pre-commit gate | `.tools/ds-commit-gate.sh <files>` | `OK: pre-commit gate clean for N file(s)` stdout; exit 0 |
      | 2. Commit | `git commit --only --author=... -- <paths>` | commit SHA |
      | 3. Push | `git push origin CLOUD` | push confirmation + branch tip |
      | 4. S3 upload | `git show {sha}:{path} \| aws s3 cp - s3://opal-bd-gold-code/gold/{id}.py` | upload ETag + byte count |
      | 5. Deploy verify | `.tools/comp-pipescript deployed {id}` | `MATCH` output |
      | 6. QA-runner dispatch (single-script/single-group ONLY — combined-deploy goes to AE per §6.2.2) | `aws ssm send-command --instance-ids <qa-instance> --document-name AWS-RunShellScript --parameters 'commands=[...]'` | SSM command-id |
      | 7. QA-runner observe | Poll `aws ssm get-command-invocation` + tail log | exit code + runtime |
      | 8. Validate output | Spot-check S3 artifacts + `comp-validate` if config exists | PASS/FAIL per validator |
      | 9. RAVC4 close | MCP to COO citing commit + tag (if applicable) + qa output | delivered message id |
    </deliverable>
    <deliverable id="ae-escalation-capture">
      Any step where DS escalates to AE (per §6.2.2 decision matrix: combined-deploy / EC2 lifecycle / PROD trigger / multi-pipeline coordination), DS captures the escalation in the session log with:
      - Which step surfaced the AE-scope condition
      - AE agent serial pinged
      - Reason for escalation (quote §6.2.2 matrix row)
      - Response time from AE

      **Zero-escalation is a valid outcome** — single-script single-group commits should not need AE. Multi-script combined deploys legitimately need AE.
    </deliverable>
    <deliverable id="acceptance-report">
      Session log explicitly tracks:
      - Total cycle time commit→RAVC4-close (target: under 2h for single-script cases)
      - Gate found any false positives? (expected: none)
      - Gate found any true positives? (expected: none, since Phase 2 DS check caught pre-commit)
      - Any friction points in the new workflow (candidates for DSFLOW v2 improvements)
      - Andrew §11 Q1 signal — did DS remember to run the gate without prompting? (trust-based v1 reminder vs git-hook v2)
    </deliverable>
  </deliverables>

  <wire_contract>
    Zero runtime system impact from this TO alone. Passive observer of whatever the triggering commit does. The triggering commit has its own wire contract independent of this TO.

    Success criteria: the triggering commit ships clean (any pre-existing success criteria for that work PASS) AND the new DSFLOW workflow ran end-to-end without DS hitting a friction point requiring AE/COO intervention beyond §6.2.2 matrix allowances.
  </wire_contract>

  <acceptance_criteria>
    1. DSFLOW.001 + DSFLOW.002 both complete before this TO flips staged→pending (COO gate).
    2. Triggering commit identified — any DS lane gold-script commit post both .001+.002 landing. First-fire priority; don't cherry-pick.
    3. All 9 steps captured in session log with timestamps. Full cycle visible end-to-end.
    4. Gate exit 0 pre-commit (no latent-bug surface on this commit — expected given gate catches the class).
    5. `comp-pipescript deployed {id}` = MATCH post-S3 upload.
    6. QA-runner dispatch SSM command-id logged + exit code captured.
    7. Any AE escalations documented with §6.2.2 matrix citation + reason.
    8. RAVC4 close MCP to COO with cycle time + friction notes.
    9. If gate produces ANY false positive during the cycle: DO NOT disable; triage per PRD §8 Rollback plan (whitelist surgically + document).
    10. Andrew §11 Q1 signal note — did DS self-invoke the gate without external reminder? (binary yes/no in log.)
    11. Session log path: `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{DATE}/dsflow_003_deploy_training_run.md`.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Confirm DSFLOW.001 + DSFLOW.002 both complete: `git log --oneline --all | grep -E "ADHC_DSFLOW\\.(001|002)"` + check task order files `<status>complete</status>`</run>
        <expect>Both .001 (DS author) + .002 (COO author) commits present + TO statuses complete.</expect>
        <if_mismatch>If either is pending, STOP — DSFLOW.003 trigger conditions not met. Stay staged.</if_mismatch>
      </step>
      <step>
        <run>`.tools/ds-commit-gate.sh <triggering-files>` — the gate runs per PRD §6.1 + CLAUDE.md Rule 13</run>
        <expect>Exit 0. No undefined-name + no py_compile error. OK: pre-commit gate clean.</expect>
        <if_mismatch>If exit 1, DO NOT COMMIT. This is a real catch — the gate is working. Fix the file + re-run. This is DSFLOW's whole point firing correctly. Log the catch as the ultimate validation evidence + flag to COO + CTO.</if_mismatch>
      </step>
      <step>
        <run>Whatever TO-specific compiler tools the triggering commit's parent TO requires (e.g. comp-pipescript io + comp-blast + comp-validate per that TO's own mandate)</run>
        <expect>Per the triggering TO's own mandate; DSFLOW.003 doesn't impose new requirements.</expect>
        <if_mismatch>Per triggering TO.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>`git commit --only --author="0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" -- <explicit paths>`</run>
        <expect>Commit lands under DS author + --only discipline. No sweep.</expect>
        <if_mismatch>Re-author if identity drift.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>Full cycle: push → S3 upload (`git show SHA:path | aws s3 cp - s3://opal-bd-gold-code/gold/{id}.py`) → `comp-pipescript deployed {id}`</run>
        <expect>Each step executes + captured in session log. `comp-pipescript deployed` returns MATCH.</expect>
        <if_mismatch>If MATCH doesn't return: S3 upload failed OR comp-graph cache stale. Triage + document.</if_mismatch>
      </step>
      <step>
        <run>QA-runner dispatch (if DS scope per §6.2.2) + observe exit code + validate output</run>
        <expect>SSM command-id logged. Exit code 0. Spot-check S3 artifacts + comp-validate if applicable.</expect>
        <if_mismatch>If QA-runner fails: normal debug path per the triggering TO's own acceptance. Document in DSFLOW.003 log as "AE escalation triggered at step 7" with reason.</if_mismatch>
      </step>
      <step>
        <run>MCP RAVC4 close to COO + AE with cycle time + friction notes + §11 Q1 signal</run>
        <expect>RAVC4 message sent. COO flips DSFLOW.003 status complete.</expect>
        <if_mismatch>Re-send if delivery fails.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>**No preemptive AE coordination.** §6.2.2 decision matrix is followed at runtime: DS dispatches QA-runner directly for single-script/single-group cases; escalates to AE for combined-deploy / EC2 lifecycle / PROD / multi-pipeline. Zero-escalation is a valid outcome.</item>
    <item>**Triggering commit's own cross-domain coordination inherited.** DSFLOW.003 adds no new coordination requirements — it observes the natural cross-domain coordination of whatever TO drives the commit.</item>
    <item>**HLOT2 5f5d0319 exempt** — already committed pre-gate per PRD §13 non-retroactive clause. Its comparison-pack authoring + RAVC4 close are not DSFLOW.003 triggers.</item>
    <item>**Coordination with COO** on status flip: DSFLOW.003 stays staged until .001 + .002 both close; COO flips to pending on that condition. DS lane doesn't unilaterally flip.</item>
  </cross_domain_coordination>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADHC_DSFLOW.001" status="pending">Tool must exist.</dependency>
    <dependency agent="2.0.0_SA_COO" task="ADHC_DSFLOW.002" status="pending">Docs + CLAUDE.md Rule 13 + prompt.md gate step must exist.</dependency>
    <dependency_trigger>Next gold-script commit by any DS lane, scope described in <objective> above. Until such a commit surfaces, this TO remains staged indefinitely.</dependency_trigger>
  </dependencies>

  <next>On trigger: COO flips staged→pending + notifies DS (the agent making the commit) of DSFLOW.003 applicability. On commit + cycle complete + RAVC4: COO flips complete; captures any friction-points for DSFLOW v2 design + ADHC_DSFLOW.json rollout-Acceptance PRD §10 7-day metrics check.</next>
</task_order>
