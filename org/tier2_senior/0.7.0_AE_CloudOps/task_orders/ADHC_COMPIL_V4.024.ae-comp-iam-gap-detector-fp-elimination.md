<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.024</id>
    <project>ADHC_COMPIL_V4</project>
    <title>comp-iam gap detector false-positive elimination — EC2-shipped-shell distinction + AWS-managed-policy attachment parsing</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status>
    <completed_date>2026-05-08</completed_date>
    <completed_commit>4fd343b45</completed_commit>
    <priority>high</priority>
    <estimated_effort>~1d catalog (likely ~30-45min wall-clock per under-budget pattern)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md (V4 family)</ref>
    <ref type="prior_to_023">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADHC_COMPIL_V4.023.*.md (1-real-of-9 permission-gap classification + 7 FPs documented)</ref>
    <ref type="trigger">Andrew direct 2026-05-08 PM: "Lets get a TO to 0.7.0_AE to fix that iam gap detector"</ref>
    <ref type="anchor_data">V4.023 RAVC2 finding: comp-iam gaps had 78% false-positive rate (7 of 9 surfaced gaps were FPs across 2 distinct classes). Real gap rate: 1/9 = 11%; FP filter target: 0/9 (eliminate FPs while preserving real-gap detection).</ref>
  </references>

  <context>
    V4.022 backfilled BD Lambda IAM mappings (1 → 129/151 = 85% coverage), enabling `comp-iam gaps` to actually run gap-detection for the first time across BD Lambdas. Initial result: 9 surfaced gaps. V4.023 investigation classified them: **1 real bug** (bd-time-machine s3:CopyObject — fixed in `bd-v2.24.7`) + **7 false positives** across 2 distinct mechanism classes:

    **FP Class A (5 of 7 FPs) — EC2-shipped-shell**: Lambdas that ship shell scripts to EC2 instances via USER_DATA_SCRIPT variables or SSM `send_command` bodies. The `aws s3 cp` calls inside those strings run on the EC2's IAM profile (e.g., `bd-exporter-profile`, `inf-gold-layer-runner` profile), NOT the Lambda's role. Current comp-iam scans for boto3-style call patterns in Lambda source + flags against Lambda role indiscriminately. Specific Lambdas hit: `historical-prices-scheduler` (s3:GetObject + s3:PutObject ×2), `inf-assets-trigger` (s3:GetObject + s3:PutObject).

    **FP Class B (2 of 7 FPs) — AWS-managed-policy attachment**: Lambdas with role-policy-attachment using `policy_arn = arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess` (or similar AWS-managed). comp-iam currently scans `aws_iam_role_policy` inline statements only; doesn't infer actions from `aws_iam_role_policy_attachment` resources pointing at AWS-managed policies. Specific Lambda hit: `opal-news-layer3-curation` (s3:GetObject covered by `AmazonS3ReadOnlyAccess` attachment, but invisible to detector).

    **Cumulative impact target:** false-positive rate 78% → near-0%. Detector becomes meaningful production audit tool instead of agent-noise generator.
  </context>

  <scope>
    <step>
      <run>**Phase 0 — read existing comp-iam source.** Locate (a) Lambda source-scan logic for boto3-style call detection, (b) Terraform IAM-policy parser (currently `aws_iam_role_policy` inline only), (c) gap-comparison logic (Lambda calls vs role grants).</run>
      <expect>Three logical surfaces identified: source-scan / TF-parse / gap-compare. Refactor scope clear.</expect>
    </step>
    <step>
      <run>**Phase 1 — FP Class A detection (EC2-shipped-shell):** detect when an `aws s3 cp` / `aws s3 sync` / `aws cloudwatch put-metric-data` / similar AWS-CLI pattern is inside a string literal that gets shipped to EC2.

        Detection patterns (in priority order):
        1. **USER_DATA_SCRIPT context:** look for the pattern inside string assignments to variables matching `USER_DATA_SCRIPT`, `USER_DATA`, or used as `user_data` in subsequent ec2.run_instances / boto3 calls
        2. **SSM send_command body:** detect strings passed as `Parameters.commands` or `commands` arg to `ssm.send_command` / `ssm_client.send_command`
        3. **Heredoc / multi-line string:** Python triple-quoted strings + bash heredocs containing AWS-CLI invocations

        Behavior on detection: exclude that operation from Lambda-role gap analysis. Optionally: emit advisory "potential EC2-shipped-shell call detected; verify destination EC2 role has equivalent permission" without blocking. **Recommend: silent exclusion for v1; advisory output a v1.1 nice-to-have.**</run>
      <expect>5 known FPs (historical-prices-scheduler ×4 + inf-assets-trigger ×1) all classified as "EC2-shipped" + excluded from Lambda gap output.</expect>
      <if_mismatch>If detection logic over-includes (excludes Lambda calls that genuinely run inside Lambda + use aws-cli pattern not as EC2-shipped): tighten by requiring the pattern to be inside a known EC2-ship variable name OR adjacent to a confirmed `ec2.run_instances` / `ssm.send_command` call.</if_mismatch>
    </step>
    <step>
      <run>**Phase 2 — FP Class B detection (AWS-managed-policy attachment):** parse `aws_iam_role_policy_attachment` Terraform resources in iam.tf. For each:
        - Resolve `policy_arn` value (literal string or HCL variable reference)
        - If `policy_arn` matches `arn:aws:iam::aws:policy/<name>`, look up actions covered

        **AWS-managed policy action lookup:**
        - **Static lookup table** (start with common managed policies): `AmazonS3ReadOnlyAccess` → `s3:Get*`, `s3:List*`; `AmazonS3FullAccess` → `s3:*`; `AWSLambdaBasicExecutionRole` → `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`; `AmazonSSMReadOnlyAccess` → `ssm:Describe*`, `ssm:Get*`, `ssm:List*`; etc.
        - **Cache-with-API-fallback for unknown:** if policy_arn not in static table, attempt `aws iam get-policy-version` + cache result locally. If cache miss + no AWS API access (offline runs), emit "MANAGED_POLICY_UNKNOWN: <arn>" advisory but do NOT claim coverage.

        Wire managed-policy actions into the Lambda role's "granted actions" set used by gap-compare.</run>
      <expect>2 known FPs (opal-news-layer3-curation s3:GetObject ×1, plus 1 other surfaced) cleared from gap output via inferred AWS-managed-policy coverage.</expect>
      <if_mismatch>If managed-policy lookup is unreliable for niche ARNs: prefer "MANAGED_POLICY_UNKNOWN advisory + don't claim coverage" over "claim coverage based on guess." Real-gap detection is more important than FP elimination on edge cases.</if_mismatch>
    </step>
    <step>
      <run>**Phase 3 — empirical regression.** Re-run `comp-iam gaps` post-fix on full Lambda surface:
        - All 7 known V4.023 FPs cleared (Class A + Class B both)
        - Real gaps (none currently — bd-time-machine `s3:CopyObject` already fixed in V4.023; future real gaps must still surface)
        - Plant a synthetic real-gap fixture (e.g., remove `s3:GetObject` from a test Lambda's role) + verify detector still surfaces it

        **Empirical target:** false-positive rate drops 78% → 0% (or near-0%) on the same lambda-source-map post-V4.022 backfill. Real-gap detection preserved.</run>
      <expect>0 of 7 known FPs surface; ≥1 synthetic real-gap fixture surfaces correctly.</expect>
    </step>
    <step>
      <run>**Phase 4 — update comp-tools.yaml + segment-scope reference card.** comp-iam entry: document EC2-shipped-shell detection + AWS-managed-policy attachment coverage. Mark V4.024 ship date in the entry's `note` field.</run>
      <expect>Catalog reflects post-fix detector capabilities.</expect>
    </step>
    <step>
      <run>**Phase 5 — ship via safe-commit.sh; RAVC2 to CTO + COO** with full empirical evidence: pre/post FP count + synthetic real-gap detection proof + comp-tools.yaml update.</run>
      <expect>Clean ship.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">FP Class A detection landed: comp-iam excludes EC2-shipped-shell `aws s3 cp` patterns from Lambda-role gap analysis. 5 known FPs (historical-prices-scheduler ×4 + inf-assets-trigger ×1) cleared.</ac>
    <ac id="2">FP Class B detection landed: comp-iam parses `aws_iam_role_policy_attachment` resources + infers actions from AWS-managed policy ARNs via static lookup + API-fallback. 2 known FPs cleared.</ac>
    <ac id="3">Static lookup table includes minimum: `AmazonS3ReadOnlyAccess`, `AmazonS3FullAccess`, `AWSLambdaBasicExecutionRole`, `AmazonSSMReadOnlyAccess`, `AmazonSSMFullAccess`. Add others as encountered in repo.</ac>
    <ac id="4">Cache-with-API-fallback for unknown managed-policy ARNs: if AWS API call succeeds, cache locally; if offline / no access, emit `MANAGED_POLICY_UNKNOWN: <arn>` advisory and do NOT claim coverage (defaults to surfacing potential FP rather than silent miss).</ac>
    <ac id="5">Empirical: false-positive rate drops 78% → near-0% on V4.023 anchor cases (0 of 7 FPs surface post-fix).</ac>
    <ac id="6">Regression: synthetic real-gap fixture (e.g., remove `s3:GetObject` from test Lambda's role) still surfaces in `comp-iam gaps` output. Real-gap detection preserved.</ac>
    <ac id="7">comp-tools.yaml comp-iam entry + comp-tools-segment-scope.md gotchas section updated to reflect post-fix detector capabilities.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">Read comp-iam source — locate Lambda source-scan + TF-parse + gap-compare surfaces.</phase>
    <phase id="2">Pre-commit: 9-cell test matrix (7 known FPs cleared + 1 synthetic real-gap surfaces + 1 known-good Lambda regression-clean).</phase>
    <phase id="3">Post-commit empirical: rerun anchor cases; append rows to org/compiler-tools-log.md.</phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Pre/post FP count + 7 anchor FP clearances + synthetic real-gap detection proof + comp-tools.yaml diff</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Tracking EC2-shipped-shell calls AGAINST destination EC2 role (advisory output deferred; v1.1 enhancement). v1 just excludes from Lambda-role analysis.</item>
    <item>Generic Bash-AST parsing for arbitrary shell scripts. v1 uses targeted regex for `aws s3 cp` / `aws s3 sync` / common AWS-CLI patterns; full Bash AST is V5+ scope.</item>
    <item>Custom (non-AWS-managed) policy attachments — already covered by existing inline-statement parser; v1 doesn't change inline path.</item>
    <item>Permission-gap REMEDIATION on any newly-surfaced real gaps post-fix — separate scope; report-only.</item>
    <item>Cross-account IAM (single-account scope; consistent with V4.013 + .022 precedent).</item>
  </out_of_scope>

  <sequencing_recommendation>
    Dispatchable immediately per Andrew direct. AE 0.7 has shown sustained bandwidth this session; this fits the under-budget pattern. Standalone TO; no cross-deps with .015/.005 deferred items.
  </sequencing_recommendation>
</task_order>
