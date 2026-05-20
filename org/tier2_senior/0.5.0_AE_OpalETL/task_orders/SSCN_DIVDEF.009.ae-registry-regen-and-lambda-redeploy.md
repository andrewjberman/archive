<task_order>
  <metadata>
    <id>SSCN_DIVDEF.009</id>
    <slug>ae-registry-regen-and-lambda-redeploy</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 -- CTO CONCURRED on both COO deltas (re-fire step + AC7; infra/ master-list placement): see &lt;coo_deltas_pending_cto&gt; resolution. COO flipped staged->pending + fired GO. Runs PARALLEL with SSCN_DIVDEF.010.</dispatch_unblock_condition>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct "focus SSCN today" 2026-05-20 (v0.6 factor-grouping correction). ~45-75min AE wall.</priority>
    <sla>~45-75min AE wall once GO lands. PARALLEL with SSCN_DIVDEF.010.</sla>
    <deadline>None -- ship at AE pace; gates the bundled TO-4/.006 PROD push.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md -- PRD v0.6 (commit 2e9fe7f3a, 1.0.0_SA_CTO, 2026-05-20). This TO is the decomposition of PRD v0.6 §6.9 "TO-7". Read the full v0.6 Amendment block: §A (the defect -- 176/282 mis-grouped, the 12-row registry-vs-master conflation table), §B (correction of v0.4 §B), §C (the 3-surface fix), §D (scope decisions -- field stays `category`, preset `group` untouched, IC/coverage stat-refresh OUT of scope), §6.9 (TO-7/TO-8 spec).</prd>
    <directive>Andrew-direct 2026-05-20: factor groups are wrong; Andrew supplied the canonical master list Signal Summary.xlsx (sheet Python_SN_New, Signal -> Group, 18 groups). CTO empirically confirmed the bundled registry uses a wrong collapsed 11-category taxonomy. This TO regenerates the registry `category` field from the master + redeploys the scanner Lambda.</directive>
    <master_list>Signal Summary.xlsx -- the canonical source-of-record Andrew supplied. Sheet `Python_SN_New`, columns Signal + Group. 18 canonical groups: analyst, beta, crowding, efficiency, governance, growth, insider, liquidity, management, momentum, profitability, quality, short, size, solvency, technical, value, volatility. CTO verified the taxonomy is stable across the old/new sheets and the R1/RM universe variants (0 group changes -- not a moving target).</master_list>
    <registry>infra/aws/lambda/opal_security_scanner_processor/factor_metadata_registry.json -- built 2026-03-05; the wrong collapsed 11-category taxonomy. Bundled with the opal-security-scanner-processor Lambda zip.</registry>
    <companion_to>SSCN_DIVDEF.010 (TO-8, DE/RD) updates the portal categoryOrder.ts + FactorBankTab to the 18-group taxonomy. Runs PARALLEL with this TO. Both gate the bundled TO-4/.006 PROD push.</companion_to>
  </references>

  <coo_deltas_pending_cto>
    Two deltas from the literal PRD v0.6 §6.9 TO-7 text, flagged by COO at decomposition and MCP'd to CTO for concurrence before dispatch:

    DELTA 1 -- Lambda re-fire step (Phase 3). §6.9 TO-7 says "rebuild + redeploy ... so latest/factor_metadata.json emits correct groups" and AC4 verifies that. But redeploy != re-emit: opal-security-scanner-processor is an S3-upload-triggered processor -- redeploying the Lambda code updates the bundled registry but does NOT re-run the Lambda. latest/factor_metadata.json only regenerates when the Lambda processes an upload. AC4 is therefore unverifiable without an explicit post-redeploy re-fire (the canonical delete-and-re-PUT of the 2026-05-18 source XLSX -- the same mechanism executed for SSCN_DIVDEF.002). COO has baked the re-fire into Phase 3 + added &lt;data_reprocess_scope&gt;.

    DELTA 2 -- master-list file placement. §6.9 TO-7 says commit the master list "into docs/architecture/security-scanner-source/." But docs/architecture/** is the ANY_CTO owned-paths lane -- AE 0.5.0 is not a permitted_agent (the same block DE 0.3.0 hit on the SSCN_GROUP_TAXONOMY.md §3.5 patch). COO's recommended resolution: place the master list at infra/aws/lambda/opal_security_scanner_processor/ (AE-owned lane, co-located with the factor_metadata_registry.json it sources -- arguably the better home for a registry source-of-record). Alternative: keep it in docs/architecture/security-scanner-source/ and route that one file's commit to CTO. This TO is WRITTEN for the infra/ placement; CTO's concurrence (or redline to docs/+route) is the dispatch gate. RESOLUTION 2026-05-20: CTO CONCURRED on both deltas. Delta 1 -- re-fire + AC7 confirmed (CTO note: AC7 also guards the sharper failure mode -- if the regen accidentally touches `relationship`, percentile signs flip and AC7 catches it; AC7 protects both the .003 validation AND relationship integrity). Delta 2 -- infra/ placement confirmed. DISPATCHED.
  </coo_deltas_pending_cto>

  <context>
    The registry's `category` field was never sourced from the master "Group" column -- it is a separate, wrong 11-category taxonomy. 176 of 282 common factors (62%) are mis-grouped; "systematic" is a garbage bucket conflating 6 real groups (technical/momentum/volatility/short/liquidity/beta), "yield" is really "value". 10 of the 13 DIVZ preset codes are affected. This TO regenerates the registry `category` field from the master, redeploys the bundled Lambda, and re-fires it so latest/factor_metadata.json emits the corrected 18-group taxonomy.

    Strictly scoped per PRD v0.6 §D: the diff is `category`-field-ONLY. IC / coverage / autocorrelation / relationship / name stay byte-identical to the prior registry (a full IC stat-refresh is a SEPARATE, out-of-scope decision -- changing IC values shifts the scanner's IC-quintile displays = wider blast radius). The internal field name stays `category` (no rename). The DIVZ preset's `group` field is untouched.
  </context>

  <scope>
    <step>Phase 1 (before write) -- baseline + IAM check. Run `comp-iam service opal-security-scanner-processor` (see &lt;compiler_tools_mandate&gt;). Capture the current factor_metadata_registry.json (the regen baseline) + the current latest/factor_metadata.json group set + the current latest/universes/{5}/scanner_data.json (the pre-re-fire anchor for AC7).</step>
    <step>Phase 2 (regenerate) --
      - Commit the master list as canonical source-of-record: Signal Summary.xlsx (or a CSV export of the Python_SN_New Signal+Group columns) at `infra/aws/lambda/opal_security_scanner_processor/` (per &lt;coo_deltas_pending_cto&gt; DELTA 2 -- CONFIRM the final placement against CTO's concurrence before committing).
      - Regenerate factor_metadata_registry.json: set each factor's `category` to its master "Group". Add the 5 master signals missing from the registry (economy_conc, indgrp_conc, mkt_val, sector_conc, subsec_conc). Resolve the 2 registry-only codes (downbeta_252d, upbeta_252d) -- assign each to its nearest master group, document the assignment + rationale in the session log. The regen is `category`-field-ONLY: IC / coverage / relationship / name fields byte-identical to the prior registry.
      - If a regen script is written, keep it under a probe/tooling path; `python -m py_compile` + `ruff check --target-version py39` it per the gate.
    </step>
    <step>Phase 3 (deploy + re-fire) --
      - Rebuild + redeploy opal-security-scanner-processor via Terraform (commit before apply; update lambda-source-map.json; terraform plan -> apply -> 0-diff replan). Tag security-scanner-v1.1.2 after a 0-diff apply; push --follow-tags. Per CLAUDE.md Rules 1-6 + LAMBDA_DEPLOYMENT_PROTOCOL.
      - RE-FIRE the Lambda (COO DELTA 1): the canonical delete-and-re-PUT of the 2026-05-18 source XLSX at s3://opal-data-portal-v2/security_scanner/uploads/2026-05-18/Screening_DIVZ_IDVZ_20260518.xlsx -- regenerates the S3 ObjectCreated event so the redeployed Lambda re-processes and re-emits latest/. Same mechanism as SSCN_DIVDEF.002. Do NOT `aws lambda invoke` directly (the TO-002 do-not rule carries forward).
      - Verify latest/factor_metadata.json post-re-fire emits only the 18 master groups (AC4) AND the 5 universes' scanner_data.json pctls are unchanged vs the Phase 1 anchor (AC7 -- a category-only registry change must not perturb the percentile compute, which would invalidate the SSCN_DIVDEF.003 validation).
    </step>
    <step>Phase 4 (RAVC2) -- to 2.0.0_SA_COO + CC 1.0.0_SA_CTO with AC1-AC7 evidence + the registry diff + the 2-code resolution rationale + commit SHAs + the security-scanner-v1.1.2 tag + the Terraform 0-diff replan + the re-fire S3 transcript. TO status -> complete on RAVC2 send.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Every registry factor's `category` equals its master "Group" -- 282/282 common factors. Per-factor verification transcript (or a diff-count proving 282/282 match the master).</ac>
    <ac id="AC2">The 5 master signals missing from the registry are added (economy_conc, indgrp_conc, mkt_val, sector_conc, subsec_conc). The 2 registry-only codes (downbeta_252d, upbeta_252d) are resolved with a documented nearest-master-group assignment + rationale in the session log.</ac>
    <ac id="AC3">The registry diff is `category`-field-ONLY: IC / coverage / autocorrelation / relationship / name fields are byte-identical to the prior registry. Verified by a field-scoped diff.</ac>
    <ac id="AC4">Post-redeploy AND post-re-fire, latest/factor_metadata.json emits ONLY the 18 master groups -- zero `yield` / `systematic` / `sentiment` / `institutional` values. (Requires the Phase 3 re-fire -- a redeploy alone does not re-emit; see &lt;coo_deltas_pending_cto&gt; DELTA 1.)</ac>
    <ac id="AC5">The 13 DIVZ preset codes verified group-correct: dy_ntm / shldr_yield / ey_ntm / fcfy = value; ret_mom_252d / velocity_63d / pcta52wl = momentum; short_pct_chg_12m / days_to_cover = short; leverage = solvency; eps_est_rev_45d = analyst; dps_gr_1yr = growth; accruals_bs = quality.</ac>
    <ac id="AC6">0-diff Terraform plan on the post-apply replan; security-scanner-v1.1.2 tag created + pushed --follow-tags; lambda-source-map.json updated.</ac>
    <ac id="AC7">Post-re-fire regression guard: the 5 universes' latest/universes/{sp500,r1000,rmidcap,sp400,msciusa}/scanner_data.json `pctls` are unchanged vs the Phase 1 pre-re-fire anchor (a category-only registry change must not perturb the percentile compute). latest/factor_metadata.json differs from its pre-re-fire state ONLY in `category`/group values. If scanner_data pctls changed, RAVC2 BLOCKED -- the regen touched more than `category`.</ac>
  </acceptance_criteria>

  <data_reprocess_scope>
    Reprocess REQUIRED. The factor_metadata_registry.json is a bundled Lambda asset; changing it changes future Lambda outputs but the existing latest/ artifacts do NOT update until the Lambda re-processes an upload. Phase 3 includes the explicit re-fire (delete-and-re-PUT the 2026-05-18 source XLSX) so latest/factor_metadata.json regenerates with the corrected groups. Post-re-fire verification: `aws s3 ls` on latest/factor_metadata.json LastModified &gt; the re-fire timestamp; jq the group set (AC4); scanner_data pctls unchanged (AC7). The re-fire regenerates ALL of latest/ (factor_metadata + 5x universe_data/scanner_data) -- AC7 confirms only factor_metadata.json group labels changed, scanner_data is byte-stable, so the SSCN_DIVDEF.003 validation still holds.
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam service opal-security-scanner-processor</run>
        <expect>No new boto3 calls, no IAM delta -- this TO changes a bundled JSON asset + redeploys; it adds no new AWS API call. The IAM surface is unchanged from security-scanner-v1.1.1.</expect>
        <if_mismatch>If comp-iam flags any MISSING permission, resolve iam.tf before the redeploy + run `comp-iam gaps` at Phase 3.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile + ruff check --target-version py39 (pin 0.15.11) on any regen script retained under a probe/tooling path</run>
        <expect>Both exit 0. If no script is retained (regen done ad-hoc), N/A -- note it in the session log.</expect>
        <if_mismatch>Fix before commit per the CLAUDE.md Rule 14 pre-commit gate.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>terraform plan (post-apply replan) on the security-scanner pipeline</run>
        <expect>0-diff -- the apply fully converged; AC6.</expect>
        <if_mismatch>Non-0-diff = drift; resolve before tagging.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp latest/factor_metadata.json - | jq '[.factors[].category] | unique' (post-re-fire)</run>
        <expect>Exactly the 18 master groups; zero yield/systematic/sentiment/institutional. AC4.</expect>
        <if_mismatch>Stale or wrong group set = the re-fire did not take or the regen was incomplete; investigate before RAVC2.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    PARALLEL with SSCN_DIVDEF.010 (DE/RD portal categoryOrder + FactorBankTab). No shared files -- this TO touches infra/aws/lambda/opal_security_scanner_processor/** + the registry + Terraform; .010 touches portal/src/pages/SecurityScanner/**. Both reference the same 18-group master taxonomy (PRD v0.6 §A). The re-fire regenerates latest/ -- which SSCN_DIVDEF.003 (DS, CLOSED) validated against; AC7 is the guard that the re-fire leaves scanner_data byte-stable so the .003 validation is not invalidated. No active writer conflict on s3://opal-data-portal-v2/json/security_scanner/latest/ -- the scanner Lambda is the sole writer. Both .009 + .010 gate the bundled TO-4/.006 PROD push.
  </cross_domain_coordination>

  <deliverables>
    - Master list committed as canonical source-of-record (placement per CTO concurrence -- see &lt;coo_deltas_pending_cto&gt;).
    - Regenerated factor_metadata_registry.json (category-field-only diff).
    - opal-security-scanner-processor redeployed via Terraform; security-scanner-v1.1.2 tag; lambda-source-map.json updated.
    - Lambda re-fired; latest/ regenerated with the 18-group taxonomy.
    - Session log under org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/ with AC1-AC7 evidence + the 2-code resolution rationale + Compiler Tools section.
    - RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO; TO status -> complete on RAVC2 send.
  </deliverables>

  <do_not>
    <rule>Do NOT change any registry field other than `category`. IC / coverage / autocorrelation / relationship / name stay byte-identical to the prior registry. A full IC/coverage stat-refresh is explicitly OUT of v0.6 scope (PRD v0.6 §D) -- it shifts the scanner's IC-quintile displays and needs its own validation pass.</rule>
    <rule>Do NOT rename the `category` field. PRD v0.6 §D: the internal field name stays `category`; only the values are corrected + the portal column label changes (that label change is SSCN_DIVDEF.010's scope, not this TO).</rule>
    <rule>Do NOT touch the DIVZ preset's `group` field. A factor's intrinsic master group and its preset-thesis group are legitimately distinct (PRD v0.6 §D).</rule>
    <rule>Do NOT `aws lambda invoke` to re-fire. Use the canonical delete-and-re-PUT of the 2026-05-18 source XLSX (the SSCN_DIVDEF.002 mechanism). Deploy only via Terraform (CLAUDE.md Rule 1).</rule>
    <rule>Do NOT `pip install -t .` into the Lambda source dir. Dependencies via layers only (CLAUDE.md Rule 3) -- though this TO should need no new dependency.</rule>
    <rule>Do NOT touch the reference-duplicate registry copy at docs/architecture/security-scanner-source/factor_metadata_registry.json. Only the bundled infra/aws/lambda/opal_security_scanner_processor/factor_metadata_registry.json is authoritative + in scope for .009. The docs/ copy is cross-lane (ANY_CTO) and CTO will sync it CTO-lane in the v0.6 closeout pass (same pass as the SSCN_GROUP_TAXONOMY.md correction). Per CTO 2026-05-20.</rule>
    <rule>No emojis in the registry, code, commit messages, or the session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
