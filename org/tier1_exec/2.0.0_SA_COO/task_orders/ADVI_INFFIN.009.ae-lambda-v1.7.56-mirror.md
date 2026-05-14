<task_order>
  <metadata>
    <id>ADVI_INFFIN.009</id>
    <slug>ae-lambda-v1.7.56-mirror</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-13</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P0 — daily cron 9 AM ET likely fires mode=full per chain #24 pattern; Lambda v1.7.55 mirror MISSING Surface #6/#8/#2 fields would Lambda-overwrite DS~C's c5d98d41f emit silently; must ship before next mode=full fire</priority>
    <sla>~30-45min Lambda code edit + ~5min terraform apply; target completion before tomorrow 9 AM ET (~9h buffer); preserve INFFIN.003 + .004 canonical fields</sla>
  </metadata>

  <references>
    <ref type="brief">docs/briefs/inflection-finalize-20260513.md (DE 0.4 INFFIN brief, commit e7965874b)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct "ok lets move it along" 2026-05-13 evening (timing pressure: daily cron mode=full risk before 9 AM ET tomorrow)</ref>
    <ref type="prior_lambda_version">v1.7.55 mirror commit `9cd5f00b4` covers active_since + role_breakdown (ADVI_INFTGT scope); v1.7.56 extends to INFFIN scope</ref>
    <ref type="cross_link">DS~C INFFIN.003 ship `c5d98d41f` + DS~A INFFIN.004 ship `bc17612ae` + AE 0.6.1 chain #28 mode=gold-d empirical RAVC2 (`s3://opal-data-inf/platinum/advisors/{id}/book.json` LIVE state)</ref>
    <ref type="empirical_evidence">AE 0.6.1 chain #28 RAVC2: "BONUS: active_since (2023-10-02 Patrick), role_breakdown=['advisor'], tax_exposure dict — ALL gold-script emitted (NOT Lambda v1.7.55 which hasn't deployed yet)" — confirms Lambda overwrite would clobber INFFIN fields</ref>
  </references>

  <context>
    Lambda `inf-portal-advisor-publisher._build_book` re-derives certain fields from gold inputs when invoked post-chain (via INFPUBLISHERDEDUP ObjectCreated S3 trigger on `pipeline-complete.json`). When mode=full chain fires, `_build_book` runs after gold scripts complete + overwrites their canonical emit with re-derived values.

    v1.7.55 mirror commit `9cd5f00b4` extends `_build_book` to mirror INF_D_02's `active_since` + `role_breakdown` fields (ADVI_INFTGT scope). v1.7.55 may not be deployed to AWS yet per AE 0.6.1 chain #28 empirical ("NOT Lambda v1.7.55 which hasn't deployed yet").

    INFFIN.003 ship `c5d98d41f` added 4 new field families to INF_D_02 emit that v1.7.55 does NOT mirror:
    1. **Surface #6 top-level `book` block** — additive AUA-state + revenue rollup (book.fee_earning_aua / non_fee_earning_aua / fee_earning_account_count / non_fee_earning_account_count / implied_annual_revenue / avg_fee_bps_earned / growth dict / small_account_count)
    2. **Surface #6 top-level `fee_summary` block** — by_account[] per CTO Q1 Option A ruling (NOT by_role[]); per-account fee_bps + aua + team_attribution + fee_share_usd
    3. **Surface #8 per-client `is_fee_paying`** — boolean on clients[] array
    4. **Surface #2 `relationship_stacked_periods[]`** — top-N HHs + Other per period (5 periods empirically)
    5. **Plus tax_exposure dict** (DS~C INFFIN.003 emit per AE 0.6.1 empirical)
    6. **Plus fee_structure_reason sentinel** (conditional on ending_mv==0; may not fire today post-Day-1 migration — defensive emit only if present)

    INFFIN.004 ship `bc17612ae` added `client_directory.json` at `s3://opal-data-inf/platinum/firm/client_directory.json` (NEW path; not Lambda-overwritten since Lambda only writes to platinum/advisors/{id}/). NO Lambda mirror needed for .004 artifact.

    **Risk window:** daily cron 9 AM ET (~9h from now). Chain #24 cron-fallback fire today was mode=full per ADVI_INFETL row in REGISTRY. If daily cron also fires mode=full tomorrow, Lambda invokes post-chain via pipeline-complete.json INFPUBLISHERDEDUP trigger; v1.7.55 (or unupgraded v1.7.54) Lambda's _build_book overwrites DS~C's INFFIN.003 fields silently. Andrew partner-visible at risk.

    **Mitigation discipline today (mode=gold-d):** pipeline-complete.json NOT written → INFPUBLISHERDEDUP not triggered → Lambda doesn't fire → canonical preserved. But mode=gold-d is a manual flag; daily cron defaults to mode=full per current schedule.
  </context>

  <objective>
    Author + deploy Lambda `inf-portal-advisor-publisher` v1.7.56 mirror extending `_build_book` to preserve INFFIN.003 + DS~C BONUS fields when re-deriving from gold inputs:

    1. Mirror Surface #6 `book` top-level block (8 fields + growth dict)
    2. Mirror Surface #6 `fee_summary` top-level block with `by_account[]` (NOT `by_role[]`; CTO Q1 Option A)
    3. Mirror Surface #8 per-client `is_fee_paying` boolean
    4. Mirror Surface #2 `relationship_stacked_periods[]`
    5. Mirror `tax_exposure` dict (DS~C INFFIN.003 BONUS)
    6. Preserve v1.7.55 mirror behavior (active_since + role_breakdown)
    7. Defensive emit on `fee_structure_reason` sentinel (only if present in gold; don't synthesize)

    Deploy via terraform apply (Lambda CloudOps lane discipline). v1.7.56 lambda layer or function version per existing convention.

    Goal state post-deploy: ANY chain mode (full / incremental / gold-d) preserves INFFIN canonical fields when Lambda fires.
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/inf-pipeline/inf-portal-advisor-publisher/lambda_function.py (or wherever `_build_book` lives) — extend mirror for 6 INFFIN.003 field families</file>
      <file action="modify">infra/aws/lambda/ci/lambda-source-map.json — bump version to v1.7.56 + source-map files-array per parity-check rule (CLAUDE.md Rule 4)</file>
      <file action="modify">infra/aws/terraform/inf-pipeline/lambda.tf (or similar) — bump version tag + any deploy_marker</file>
      <file action="commit">Single commit under 0.7.0_AE_CloudOps author per agent commit identity protocol</file>
    </files>
  </scope>

  <phase id="1" when="investigation">
    <step>
      <description>Inspect v1.7.55 mirror commit `9cd5f00b4` for `_build_book` extension pattern. Confirm Lambda code path location + current mirror logic for active_since + role_breakdown.</description>
      <expect>Mirror pattern identified; structure clear for extension.</expect>
      <if_mismatch>If v1.7.55 mirror is elsewhere or has different shape than expected, surface to COO before authoring v1.7.56.</if_mismatch>
    </step>
    <step>
      <description>Inspect INF_D_02 (DS~C c5d98d41f) emit for the 6 INFFIN.003 field families. Map each to Lambda `_build_book` source data (Lambda reads gold inputs; what gold paths does it consume?).</description>
      <expect>Each INFFIN.003 field family has a Lambda-side derivation source identified OR confirmed as gold-emit-only-no-redrive-needed.</expect>
      <if_mismatch>If a field can't be re-derived in Lambda from available gold inputs, the Lambda mirror MUST be passthrough (read gold + emit unchanged, NOT recompute). Either approach is acceptable; surface choice to COO.</if_mismatch>
    </step>
    <step>
      <description>Decide mirror strategy:
- **Strategy A — Recompute:** Lambda re-derives all fields from gold inputs (consistent with v1.7.55 pattern; complex but self-contained)
- **Strategy B — Passthrough:** Lambda reads INF_D_02's emitted fields directly from gold path + passes through unchanged (simpler; ensures DS~C's canonical IS the platinum canonical)
- **Strategy C — Hybrid:** recompute for fields where Lambda has the source data; passthrough for fields where it doesn't

Recommendation: **Strategy B (passthrough)** for INFFIN fields. Lambda fields v1.7.55 already recomputes (active_since + role_breakdown) — keep that. INFFIN.003's fields are complex aggregations (book block + fee_summary + relationship_stacked_periods) that already exist in gold; passthrough is structurally simpler + risk-free.</description>
      <expect>Strategy decided; rationale documented.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <description>Extend `_build_book` to mirror Surface #6 `book` top-level block. Read from INF_D_02 gold emit (advisor book.json pre-Lambda overwrite path) + pass through unchanged. Include all 8 fields + growth dict.</description>
      <expect>book block preserved on Lambda emit.</expect>
    </step>
    <step>
      <description>Extend `_build_book` to mirror Surface #6 `fee_summary` block with `by_account[]` (NOT `by_role[]` per CTO Q1 Option A). Preserve per-account fee_bps + aua + team_attribution + fee_share_usd structure.</description>
      <expect>fee_summary.by_account[] preserved.</expect>
    </step>
    <step>
      <description>Extend `_build_book` to mirror Surface #8 per-client `is_fee_paying` boolean on clients[] array.</description>
      <expect>clients[].is_fee_paying preserved.</expect>
    </step>
    <step>
      <description>Extend `_build_book` to mirror Surface #2 `relationship_stacked_periods[]` (top-N HHs + Other per period structure preserved).</description>
      <expect>relationship_stacked_periods preserved.</expect>
    </step>
    <step>
      <description>Extend `_build_book` to mirror `tax_exposure` dict.</description>
      <expect>tax_exposure preserved.</expect>
    </step>
    <step>
      <description>Defensive emit on `fee_structure_reason` sentinel: read from gold + pass through if present; do NOT synthesize if absent (today's accts 166+477 don't carry this field per chain #28 empirical; ending_mv > 0 post-Day-1 migration means conditional emit doesn't fire).</description>
      <expect>fee_structure_reason passes through if present; absent → not synthesized.</expect>
    </step>
    <step>
      <description>Preserve v1.7.55 mirror behavior (active_since + role_breakdown). Verify v1.7.55 baseline behavior unchanged by v1.7.56 additions.</description>
      <expect>v1.7.55 behavior preserved.</expect>
    </step>
    <step>
      <description>Bump lambda-source-map.json + terraform version tag to v1.7.56. Update source-map `files` array if any new files added (ADHC_DRIFTD.002 parity check enforces).</description>
      <expect>Source-map + terraform version updated cleanly.</expect>
    </step>
  </phase>

  <phase id="3" when="empirical-test">
    <step>
      <description>Pre-deploy syntax check + AST: `python -m py_compile lambda_function.py` + AST scan via ds-precommit-check.py (Lambda code follows ds-commit-gate discipline per CLAUDE.md Rule 14).</description>
      <expect>PASS.</expect>
    </step>
    <step>
      <description>Terraform plan: `terraform plan` on inf-pipeline; verify diff shows Lambda function version bump only + 0-diff elsewhere.</description>
      <expect>Clean diff; only Lambda function version change visible.</expect>
      <if_mismatch>If extraneous diffs surface, surface to COO before apply.</if_mismatch>
    </step>
    <step>
      <description>Terraform apply: `terraform apply` to deploy v1.7.56 Lambda. Wait for AWS confirmation.</description>
      <expect>Apply complete; Lambda function version reflects v1.7.56.</expect>
    </step>
    <step>
      <description>Lambda direct-invoke smoke (post-deploy): `aws lambda invoke --function-name inf-portal-advisor-publisher --payload '{"advisor_id":"peter_lee","dry_run":true}'` (or whatever payload pattern exists). Verify v1.7.56 mirror produces book.json with all 6 INFFIN.003 field families + v1.7.55 active_since/role_breakdown preserved.</description>
      <expect>Lambda smoke produces book.json with INFFIN canonical fields preserved.</expect>
      <if_mismatch>If Lambda smoke shows missing fields or shape mismatch, surface to COO immediately; do not declare ship complete.</if_mismatch>
    </step>
    <step>
      <description>Git tag: `git tag -a inf-pipeline-v1.7.56 -m "Lambda v1.7.56: INFFIN.003 Surface #6/#8/#2 mirror"` + `git push --follow-tags`.</description>
      <expect>Tag pushed.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: v1.7.56 Lambda mirror extends `_build_book` with INFFIN.003 6 field families (book + fee_summary.by_account[] + clients[].is_fee_paying + relationship_stacked_periods[] + tax_exposure + fee_structure_reason defensive emit).
    AC2: v1.7.55 baseline behavior preserved (active_since + role_breakdown mirror).
    AC3: lambda-source-map.json + terraform version tag updated to v1.7.56.
    AC4: terraform plan shows 0-diff except Lambda function version bump.
    AC5: terraform apply successful + post-apply 0-diff verify.
    AC6: Lambda direct-invoke smoke produces book.json with all INFFIN canonical fields preserved.
    AC7: Git tag `inf-pipeline-v1.7.56` pushed --follow-tags.
    AC8: Session log captures empirical-test verification + ship sequencing.
    AC9: MCP RAVC2 to COO with deploy evidence + Lambda smoke output snippet.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase_1>comp-iam service inf-portal-advisor-publisher (IAM gap check); comp-pipescript io if applicable (Lambda code may or may not be in graph)</phase_1>
    <phase_2>ds-commit-gate equivalent for Lambda code (py_compile + AST); terraform plan 0-diff gate</phase_2>
    <phase_3>Lambda direct-invoke smoke as the empirical acceptance gate</phase_3>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SHARED FILES:
    - infra/aws/lambda/inf-pipeline/inf-portal-advisor-publisher/ — pipeline-specific; AE 0.7 lane (you)
    - infra/aws/lambda/ci/lambda-source-map.json — cross-pipeline; ADHC_DRIFTD.002 parity check enforces (no source_dir vs files[] gaps)
    - infra/aws/terraform/inf-pipeline/ — pipeline-specific Terraform

    DOWNSTREAM CONSUMER:
    - Daily cron 9 AM ET (or any future mode=full chain) — invokes Lambda post-chain via pipeline-complete.json INFPUBLISHERDEDUP trigger; v1.7.56 ensures canonical preserved
    - RD .006 wiring (in flight; consumes platinum/advisors/{id}/book.json + client_directory.json) — v1.7.56 ensures their consumption surface stable post mode=full chain fires

    PARALLEL ACTIVITY:
    - DS-base fixing pre-existing NaN bug in INF_D_00c lines 526-538 + 556-568 (perf-aggregation; separate from your Lambda lane)
    - AE 0.6.1 shipped pipe-deadlock fix `726742430` (dispatch.sh; their lane)
    - RD 0.4.2 INFFIN.006 in flight (~2-3h wall; FE wiring; no Lambda dep)

    NO PORTAL CONFLICT: pure Lambda code + terraform; no FE-side change.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Pure Lambda code mirror change. No data emit changes; no chain re-fire required for v1.7.56 itself. Next chain fire (mode=full or mode=gold-d daily cron) exercises the new Lambda automatically.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. Lambda code mirror extension (Phase 2 steps 1-7)
    2. lambda-source-map.json + terraform version bump (Phase 2 step 8)
    3. Terraform plan + apply (Phase 3 step 2-3)
    4. Lambda direct-invoke smoke verification (Phase 3 step 4)
    5. Git tag inf-pipeline-v1.7.56 pushed --follow-tags
    6. Session log with empirical evidence + AC1-9 PASS
    7. MCP RAVC2 to COO + AE 0.6.1 (FYI on Lambda state change)
  </deliverables>

  <ravc>
    AE 0.7 RAVC2 to COO post-AC1-9 PASS. COO ratifies + relays Lambda-ready state to AE 0.6.1 (cron-loop awareness) + Andrew (partner-visible risk mitigated before tomorrow 9 AM ET cron).
  </ravc>

  <notes>
    **Timing pressure:** Andrew direct "ok lets move it along" 2026-05-13 evening. Daily cron 9 AM ET (~9h from now) likely fires mode=full per chain #24 pattern. Lambda v1.7.55 (or pre-v1.7.55) without v1.7.56 mirror would Lambda-overwrite DS~C's INFFIN.003 canonical fields silently. Ship before then.

    **v1.7.55 deploy status:** AE 0.6.1 chain #28 empirical says v1.7.55 mirror "hasn't deployed yet" — meaning commit `9cd5f00b4` may not have been terraform-applied to AWS. If v1.7.55 is still pending deploy, fold its deploy INTO v1.7.56 deploy (single terraform apply covers both). If v1.7.55 was deployed earlier, v1.7.56 is purely additive on top.

    **Strategy B (passthrough) recommended for INFFIN fields:**
    - INF_D_02's emit is the canonical source for INFFIN.003 fields
    - Lambda should NOT re-derive (risk of divergence from DS~C's canonical)
    - Read gold path + pass through unchanged

    **Verification critical:** chain #29 (tomorrow's cron fire) is the first empirical test. Lambda direct-invoke smoke pre-cron is the safety net.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"` per agent commit identity protocol.

    **Cross-link with ADHC_DRIFTD.002 parity check:** new files added to Lambda source_dir must register in source-map `files` array. Build hook will halt if mismatch (the gate ADHC_DRIFTD.002 closed today).
  </notes>
</task_order>
