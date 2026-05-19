<task_order>
  <metadata>
    <id>SSCN_DIVDEF.004</id>
    <slug>ae-lambda-universe-map-swap-and-redeploy</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-19</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>RESOLVED 2026-05-19 PM -- Andrew spawned 0.5.0_AE_OpalETL (PID 31264 LIVE). GO dispatched via MCP at spawn time. Note: AE 0.5.0 also has MDLP_VOLAUD.002 (older TO from base COO session 70 15:18Z, investigation-pace, no downstream waiters); SSCN_DIVDEF.004 carries downstream chain (TO-2 DT re-fire + TO-3 DS validation + TO-4 PROD push all wait on this). Chain-dependency prioritization favors SSCN_DIVDEF.004 first per COO~B routing recommendation; AE 0.5.0 final bandwidth call.</dispatch_unblock_condition>
    <in_flight_scope_amendment>2026-05-19 PM (COO~B-direct, in-flight): AE 0.5.0 Phase 1 surfaced a NON_SCORING_COLS audit-completeness gap at `lambda_function.py:60-74` -- the constant lists the LEGACY 6 universe weight columns (wt_ivv/wt_iwb/wt_iwd/wt_acwx/wt_efa/wt_efv) but is MISSING the 3 new universes' columns (wt_iwr/wt_ijh/wt_csus). Without those in the exclusion set, the Lambda's identify-scoring-factor-columns logic would treat them as scoring factors -> factor_metadata + scanner_data.pctls would surface 3 bogus "factors" with meaningless percentile rankings on universe-membership weights. Factor Bank tab UX defect. MEDIUM materiality (NOT a DIVZ-correctness blocker -- the 13 DIVZ codes are unchanged; but real Factor-Bank pollution + ~50KB data bloat per scanner_data.json). FIX (folded into this TO inline, NOT a .004.1 spin): add wt_iwr/wt_ijh/wt_csus to NON_SCORING_COLS at lines 60-74. Keep legacy 4 (wt_iwd/wt_acwx/wt_efa/wt_efv) in NON_SCORING_COLS as forward-compat (cheap if Andrew re-introduces international universes). AC1 expands: lines 46-53 UNIVERSE_MAP swap + lines 60-74 NON_SCORING_COLS addition; both in same git diff for AC1 evidence. AE 0.5.0 also runs grep "wt_iwd\|wt_acwx\|wt_efa\|wt_efv\|r1000v\|acwx\|eafe\|eafev" lambda_function.py pre-commit as belt-and-suspenders for any OTHER stale legacy references; findings documented in session log. CTO~B notified for awareness (3rd same-day anchor of the audit-completeness-vs-empirical-probe-enumeration class; banking for session-end memory).</in_flight_scope_amendment>
    <project_code>SSCN_DIVDEF</project_code>
    <priority>P1 -- Andrew-direct PRD v0.2 ratification 2026-05-19; sequences first in v0.2 chain (TO-AE-1 -> revised TO-2 -> TO-3 GO). TO-2 cannot re-fire cleanly until this Lambda v1.1.0 ships. ~30min mechanical wall.</priority>
    <sla>~30min AE wall. SEQUENCES FIRST. Blocks revised TO-2 (DT 0.3.0 re-fire).</sla>
    <deadline>None hard -- ship at 0.5.0 pace post-spawn; Pod 3 closure wall ~0.5-0.75 effort-day total with this in the critical path.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/SSCN_DIVDEF.md PRD v0.2 §6.4 (1.0.0_SA_CTO~B, commit c34f16d13 2026-05-19) -- verbatim Lambda UNIVERSE_MAP dict + 7 ACs.</prd>
    <data_contract>docs/architecture/SSCN_DATA_CONTRACT.md §6.v0.2 (CTO~B commit c34f16d13) -- canonical 5-universe set with empirical member counts.</data_contract>
    <prior_ship>security-scanner-v1.0.2 (current production tag; commit lineage carries SSCN_PORTAL 2026-03-10 ship + intervening minor updates). This TO ships v1.1.0 (minor bump = universe-set contract change).</prior_ship>
    <coo_section_7_lock>Q8 LOCKED AE 0.5.0_AE_OpalETL (canonical SSCN owner per SSCN_DATA_CONTRACT §1; 0.7.0 saturated with CEO-direct 22h v1.0.1 + 3-TO sequence). COO~B routing call ratified by CTO~B in PRD v0.2 §7 Q8.</coo_section_7_lock>
    <ds_pre_stage_context>DS 0.3.0 has pre-staged SSCN_GROUP_TAXONOMY.md §3.6 universe-set selection guidance with empirical anchor pointing to this TO; the doc commits at TO-3 close (post your RAVC2). Your tag/commit SHA will be cited there.</ds_pre_stage_context>
  </references>

  <context>
    PRD v0.2 ratifies the universe-set migration from legacy 6 (sp500 + r1000 + r1000v + acwx + eafe + eafev) to new 5 US-equity (sp500 + r1000 + rmidcap + sp400 + msciusa). The source XLSX `s3://opal-data-portal-v2/security_scanner/uploads/2026-05-18/Screening_DIVZ_IDVZ_20260518.xlsx` carries the new 5's `wt_*` columns (wt_ivv + wt_iwb + wt_iwr + wt_ijh + wt_csus) and is NOT a defect against the new set.

    This TO swaps `lambda_function.py` UNIVERSE_MAP to match the new contract + ships tag `security-scanner-v1.1.0`. Without this, the next DT TO-2 re-fire writes the same partial 5-of-13 output (Lambda still computing legacy 6 universes against an XLSX that only has 5's columns).

    Surface inventory:
    - 1 Python file (~5 LOC dict edit): `infra/aws/lambda/opal_security_scanner_processor/lambda_function.py` lines 46-53.
    - 0 Terraform code changes (Lambda config unchanged; only the bundled Python differs).
    - 1 Lambda build + S3 upload + Terraform plan/apply (code-hash change triggers re-deploy).
    - 1 tag (`security-scanner-v1.1.0`).

    No IAM change. No event-source-mapping change. No new boto3 surface. Pure code update.
  </context>

  <scope>
    <step>Phase 1 (before edit) -- compiler baseline + sanity:
      - `comp-iam service opal-security-scanner-processor` (verify role unchanged; no new boto3 surface expected since this is a constant-dict swap).
      - Direct-read `infra/aws/lambda/opal_security_scanner_processor/lambda_function.py:46-53` to confirm the current legacy 6-entry UNIVERSE_MAP shape (sp500/r1000/r1000v/acwx/eafe/eafev → wt_ivv/wt_iwb/wt_iwd/wt_acwx/wt_efa/wt_efv).
      - Code-review the manifest-update guard around line 388-396 (or wherever `Manifest updated` log line emits): confirm the "if 0 universes processed, skip manifest" guard does NOT degenerate at 5/5 (floor=0; ceiling=5; the empirical 2026-05-19 partial-run produced "universes_processed=2" + no Manifest-updated emit -- want to confirm 5 produces the emit).
    </step>
    <step>Phase 2 (edit) -- verbatim replacement at `lambda_function.py:46-53`:
      ```python
      UNIVERSE_MAP = {
          "sp500":   "wt_ivv",
          "r1000":   "wt_iwb",
          "rmidcap": "wt_iwr",
          "sp400":   "wt_ijh",
          "msciusa": "wt_csus",
      }
      ```
      Per PRD v0.2 §6.4 EXACT (5 entries, descriptive tokens, ordered as above).
    </step>
    <step>Phase 3 (before commit) -- `python -m py_compile lambda_function.py`; `ruff check --target-version py39` exit 0; `.tools/ds-commit-gate.sh lambda_function.py` exit 0 (Rule 14 -- applies to all .py edits).</step>
    <step>Phase 4 (commit + Terraform-only deploy per CLAUDE.md Rule 1):
      - `.tools/safe-commit.sh --author "0.5.0_AE_OpalETL <0.5.0_AE_OpalETL@opal.agent>" -m "feat(security-scanner): Lambda UNIVERSE_MAP swap to v0.2 5-universe US-equity set (SSCN_DIVDEF.004; PRD v0.2 §6.4)" -- infra/aws/lambda/opal_security_scanner_processor/lambda_function.py`
      - `git push --follow-tags` (after tag) ... but DO Terraform first per the deploy sequence.
      - Build + upload Lambda zip per `infra/aws/lambda/opal_security_scanner_processor/` build flow (existing pattern for this Lambda; check for S3-backed deploy pattern per yang/news/bd precedent OR archive_file inline zip per legacy pattern; AE judgment on which artifact path applies to opal-security-scanner-processor; documented in build-and-upload.sh if S3-backed).
      - `cd infra/aws/terraform/security-scanner-pipeline && ../.tools/terraform.exe plan` -- expect 0 add / 1 change / 0 destroy (Lambda code/source-hash change only; no resource adds; no destroys).
      - `terraform apply` -- 0-diff verify post-apply.
      - `git tag -a security-scanner-v1.1.0 -m "SSCN_DIVDEF.004 -- Lambda UNIVERSE_MAP swap to v0.2 5-universe US-equity set (Andrew-direct migration 2026-05-19; PRD v0.2 c34f16d13)"`
      - `git push --follow-tags` -- carries the tag + commit.
      - `.tools/record-terraform-deploy.sh` -- writes tag + commit to `infra/aws/terraform/security-scanner-pipeline/CHANGELOG.json` per ADHC_DRIFTD content-provenance contract.
    </step>
    <step>Phase 5 (RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B + CC 0.3.0_DT_TradingOperations) -- the CC to DT IS THE GO for revised TO-2 (DT delete-and-re-PUT the source XLSX → Lambda re-fires → 11 files in 2026-05-18/ + latest/ overwrites cleanly with new 5 universes). Capture: commit SHA, tag, plan transcript (0/1/0), apply transcript, manifest-guard-confirmation transcript, AC1-AC7 evidence, post-apply Lambda LastModified > TO-start. SSCN_DIVDEF.json status -> ws=AE complete on RAVC2 (COO~B updates JSON; you just MCP).</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">`infra/aws/lambda/opal_security_scanner_processor/lambda_function.py:46-53` diff matches the new dict EXACTLY (5 entries, descriptive tokens, ordered sp500 → r1000 → rmidcap → sp400 → msciusa). git diff captured.</ac>
    <ac id="AC2">Terraform plan: 0 add / 1 change / 0 destroy (Lambda code-hash change only; no IAM, no event-source-mapping, no S3 bucket touched). Plan transcript captured.</ac>
    <ac id="AC3">Terraform apply lands clean; CloudWatch log group emits a Lambda update event; post-apply 0-diff replan exits clean.</ac>
    <ac id="AC4">New tag `security-scanner-v1.1.0` annotated + pushed with `--follow-tags`. Tag message cites SSCN_DIVDEF.004 + Andrew-direct universe-set migration + PRD v0.2 commit c34f16d13.</ac>
    <ac id="AC5">Lambda code-review confirms the manifest-update guard at the appropriate `lambda_function.py` line (the "if universes_processed == 0, skip manifest" line per DT 0.3.0's RAVC2 BLOCKED 2026-05-19T15:27Z empirical finding) does NOT degenerate at 5/5 processed universes. Code-review note in session log: floor=0; ceiling=5; the empirical 2026-05-19 partial run produced "universes_processed=2 + no Manifest emit" -- confirm 5 produces the emit OR fix the guard if it has a different ceiling issue.</ac>
    <ac id="AC6">`.tools/record-terraform-deploy.sh` runs cleanly + writes the new tag + commit to `infra/aws/terraform/security-scanner-pipeline/CHANGELOG.json`.</ac>
    <ac id="AC7">Post-apply, `aws lambda get-function --function-name opal-security-scanner-processor --query 'Configuration.LastModified'` returns a timestamp > TO-start TS.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      `comp-iam service opal-security-scanner-processor` -- expect role `sscn_processor` unchanged from PRD §5 baseline; this is a code-only edit, no boto3 surface change.
      Direct-read `lambda_function.py:46-53` (current UNIVERSE_MAP) + lines 380-400 (manifest-update guard).
    </before_write>
    <before_commit>
      `python -m py_compile infra/aws/lambda/opal_security_scanner_processor/lambda_function.py` exit 0.
      `ruff check --target-version py39 infra/aws/lambda/opal_security_scanner_processor/lambda_function.py` exit 0 (Rule 14 pinned 0.15.11).
      `.tools/ds-commit-gate.sh infra/aws/lambda/opal_security_scanner_processor/lambda_function.py` exit 0 (Rule 14 -- applies to ALL Python edits, not just DS).
    </before_commit>
    <after_commit>
      Terraform 0-diff replan post-apply (canonical AE-side "deployment verified" signal).
      `aws lambda get-function --function-name opal-security-scanner-processor` -- LastModified timestamp + code SHA confirms the new build is live.
      `comp-pipescript deployed` -- N/A for Lambda pipelines (EC2-script-only); use the Lambda-specific deploy verification (`aws lambda get-function` + Terraform replan) as canonical evidence.
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    None for AE-side. The Lambda code edit is the only surface this TO touches. Downstream coordination is the RAVC2 CC to DT 0.3.0 -- which IS the GO for revised SSCN_DIVDEF.002 (DT delete-and-re-PUT). DT then re-fires Lambda v1.1.0 against the existing source XLSX → new 5-universe `latest/` overwrites + RAVC2 CC → DS 0.3.0 TO-3 dispatch_unblock fires. Chain mechanism preserved from v0.1.
  </cross_domain_coordination>

  <deliverables>
    - `lambda_function.py` UNIVERSE_MAP swap (5 LOC dict edit).
    - `security-scanner-v1.1.0` tag pushed with `--follow-tags`.
    - Terraform 0-diff apply + verified replan.
    - `record-terraform-deploy.sh` writes CHANGELOG.json entry.
    - Session log under `org/tier2_senior/0.5.0_AE_OpalETL/logs/YYYY-MM-DD/` with: plan transcript (0/1/0), apply transcript, manifest-guard code-review note, AC1-AC7 evidence, Compiler Tools section (`comp-iam` + py_compile + ruff + ds-commit-gate + Lambda LastModified).
    - RAVC2 to 2.0.0_SA_COO~B + CC 1.0.0_SA_CTO~B + CC 0.3.0_DT_TradingOperations on close; SSCN_DIVDEF.json status -> ws=AE complete on receipt.
  </deliverables>

  <do_not>
    <rule>Do NOT modify event-source-mapping (the S3 ObjectCreated trigger on `opal-data-portal-v2/security_scanner/uploads/`) -- it's correct as-is; PRD v0.2 §6.4 explicitly preserves the trigger pattern.</rule>
    <rule>Do NOT modify factor_metadata_registry.json -- this TO touches Python code only (the UNIVERSE_MAP constant). The registry is a separate concern; CTO~B already verified at PRD time the 13 DIVZ signals are registry-present.</rule>
    <rule>Do NOT add a `wt_*` column re-check / fail-loud guard in this TO -- that's the Path 4 ADHC_SSCNHRD follow-on project (AE 0.7 lane, post-SSCN_DIVDEF close, ~30min code edit). This TO is the universe-set CONFIG swap; the structural-defect HARDENING is separate.</rule>
    <rule>Do NOT use `aws lambda update-function-code` shortcut -- Rule 1 (Terraform-only Lambda deploy) is non-negotiable. Build → S3 upload → Terraform plan → apply → tag → record.</rule>
    <rule>Do NOT delete `latest/universes/{r1000v,acwx,eafe,eafev}/` files post-deploy -- PRD v0.2 §3.5 explicitly preserves them as forensic / DO-NOT-DELETE. The Lambda re-fire by DT (revised TO-2) will only write the new 5 universes; the 4 legacy remain forensically.</rule>
    <rule>Do NOT skip `record-terraform-deploy.sh` -- AC6 + ADHC_DRIFTD content-provenance contract.</rule>
    <rule>No emojis in code, logs, or session log (CLAUDE.md ASCII-only rule).</rule>
  </do_not>
</task_order>
