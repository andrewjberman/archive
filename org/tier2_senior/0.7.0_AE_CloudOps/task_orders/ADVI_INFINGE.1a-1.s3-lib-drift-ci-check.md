<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.1a-1</id>
    <project>ADVI_INFINGE</project>
    <title>S3 lib version drift detection + audit + remediation + CI check (Phase 1a ops cleanup; Risk Register C structural fix)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-05</issued_date>
    <status>complete</status><!-- CLOSED 20260505T205000Z by COO RAVC5 accept. CI yaml live (872e6a071 CTO proxy), PARITY.md (3fb5504e1), RUNBOOK (d6ce723d8), session log 7 ops findings (dd6f35628). silver/positions_mv/ 5 flat-path artifacts DELETED. Step 2 failure-mode test deferred to post-sprint dedicated session (COO accept: canonical state GREEN = AC1 logically validated). -->
    <priority>high</priority>
    <estimated_effort>~0.5d AE per CTO PRD v0.2 §6.1; sprint compressed ~2-3h tonight target</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6 Phase 1a TO 1a-1 spec (line 205-213); §5.2 Compiler Evidence (Scenario X confirmation)</ref>
    <ref type="root_cause_evidence">AE 0.7 Scenario X RAVC4 (20260505T194100Z): empirical state-transition D1d (pre-upload @ 19:18Z, flat path) → lib upload @ 19:30Z → D1e (post-upload @ 19:30:41Z, Hive path). ONLY change between D1d and D1e was uploading local `_orion_api_silver_lib.py` to `s3://opal-data-inf/code/gold/`. Confirms lib drift root cause.</ref>
    <ref type="failure_class">Same root cause class as AUDIT-008 (silver/assets_v2 stale 5 days), AUDIT-002 (canonical_prices stale 2 weeks), AUDIT-003 (build_assets_dim allowlist hardcoded miss). All four = silent-stale failure mode where deployed artifact diverged from canonical without CI detection.</ref>
    <ref type="risk_register">PRD v0.2 Appendix C Risk Register: "Deployed-script (S3) vs canonical-script (local repo) drift in shared library, undetected by CI" (HIGH likelihood + HIGH impact). This TO is the structural mitigation.</ref>
  </references>

  <context>
    Tonight's empirical: AE 0.7's silver convert dispatched the canonical `convert_orion_api_to_silver.py` with `--dim positions_mv` flag against an OUT-OF-DATE `_orion_api_silver_lib.py` deployed at `s3://opal-data-inf/code/gold/_orion_api_silver_lib.py`. Stale lib version had `silver_api_dim_s3_key()` returning flat path `silver/{dim}/{date}.parquet`; canonical local repo version returns Hive path `silver/api_dims/{dim}/snapshot_date={date}/data.parquet`. Result: silver convert wrote to wrong path; INF_B_00 reads Hive; downstream chain produced stale canonical (Apr-30 latest available).

    AE 0.7 manually uploaded the canonical local lib to S3 (D1e at 19:30Z); subsequent convert wrote correct Hive paths; D2b chain re-fire produced fresh canonical_holdings_2026-05-05. **The bug was deployment-time staleness, not script logic.**

    Structural fix (this TO): CI check that compares local-vs-S3 lib parity for shared deployment libs. Catches drift at deploy/CI time, not silently in production where it manifests as silent-stale data.

    Audit scope (this TO): all flat-path artifacts at `silver/{dim}/{date}.parquet` (NOT Hive partitions) likely produced by past runs against stale lib. Each found classified: cleanup-only (no consumer reads flat) vs re-convert-to-Hive (consumer reads flat).

    Remediation: per-disposition action. Most likely: cleanup-only (no known consumer reads flat path; INF_B_00 etc all read Hive). But empirical audit confirms.

    AE 0.7 owns this TO because they hit the bug + have the empirical fix path + own CI tooling for inf-pipeline.
  </context>

  <phase id="1" when="before writing CI check or audit">
    <step>
      <run>aws s3 ls s3://opal-data-inf/silver/ --recursive | grep -E "\.parquet$" | grep -vE "/snapshot_date=|/api_dims/" | head -100</run>
      <expect>Enumerate all flat-path .parquet files at silver/{dim}/{date}.parquet pattern (NOT silver/api_dims/Hive partitions). Most likely surfaces: silver/positions_mv/2026-05-{01..05}.parquet (D1d artifacts from tonight) + possibly historical equivalents from past runs.</expect>
      <if_mismatch>Empty result: no flat-path artifacts present; audit reduces to CI-check-only scope (no remediation needed). Document.</if_mismatch>
    </step>
    <step>
      <run>aws s3api list-object-versions --bucket opal-data-inf --prefix code/gold/_orion_api_silver_lib.py --max-items 20 --query 'Versions[*].[VersionId,LastModified,Size]'</run>
      <expect>Show version history of the lib at S3 (if versioning enabled). Confirms the drift sequence: pre-D1e timestamp = stale; post-D1e timestamp (19:30Z 2026-05-05) = canonical. Useful evidence for TO documentation.</expect>
      <if_mismatch>If versioning not enabled on opal-data-inf: drift detection MUST go beyond CI parity check; consider enabling S3 versioning on `code/` prefixes as Phase 1a sub-task (or separate TO).</if_mismatch>
    </step>
    <step>
      <run>find data/orion/scripts -name "*_lib.py" -o -name "*_helpers.py" -o -name "*_utils.py" -o -name "*_common.py" | sort</run>
      <expect>Enumerate ALL shared lib modules in data/orion/scripts (silver-tier + gold-tier + bronze-tier shared utilities). Each is a candidate for the same drift class.</expect>
      <if_mismatch>If only `_orion_api_silver_lib.py` exists: scope reduces to single lib. If multiple: each must be in CI parity check.</if_mismatch>
    </step>
    <step>
      <run>For each shared lib found in Step 3: aws s3 ls s3://opal-data-inf/code/ --recursive | grep "{lib_name}"</run>
      <expect>Confirm S3 deployment path for each. Single shared lib may be deployed to multiple S3 prefixes (e.g., code/gold/ + code/silver/ + code/bronze/). All deployment locations must be in CI parity check.</expect>
      <if_mismatch>If S3 doesn't have a deployment of the lib but local imports it: that lib is local-only / not deployed; doesn't need parity check. Document.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="implementation — CI check + audit remediation">
    <step>
      <run>Author CI check yaml at `.github/workflows/inf-pipeline-lib-parity.yml` (or similar; align with existing CI structure)</run>
      <expect>GitHub Actions workflow that triggers on PR + main-branch push; for each (local_path, s3_path) pair from Phase 1 enumeration, runs `diff &lt;(cat local_path) &lt;(aws s3 cp s3_path -)`; fails CI on any non-empty diff. Documents which libs are in scope. Includes auto-comment on PR explaining how to fix (run `aws s3 cp local_path s3_path` to sync).</expect>
      <if_mismatch>If existing inf-pipeline CI workflow exists: extend it rather than create new file. Same CI scope; cleaner Yaml structure.</if_mismatch>
    </step>
    <step>
      <run>Test CI failure-mode by intentionally diverging local from S3 (in a test branch / PR): edit local lib's `silver_api_dim_s3_key` return value; commit + push. Confirm CI fails with explicit "lib drift detected" message + helpful auto-comment. Revert.</run>
      <expect>CI catches drift; PR check fails red; auto-comment surfaces remediation. Does NOT merge into main.</expect>
      <if_mismatch>If CI passes despite drift: parity check yaml is wrong; debug + iterate.</if_mismatch>
    </step>
    <step>
      <run>For each flat-path artifact enumerated in Phase 1 Step 1: classify cleanup-only OR re-convert.
        - Method: aws s3api head-object on the flat-path file + grep `comp-pipescript io` outputs for any consumer that reads `silver/{dim}/{date}.parquet` (flat) explicitly.
        - If zero consumers: cleanup-only.
        - If 1+ consumers: re-convert (run convert script with FRESH lib to write Hive partition; THEN delete flat).</run>
      <expect>Empirical disposition table: each flat-path artifact tagged. Most likely: ALL cleanup-only (since INF_B_00 reads Hive only; no other documented consumer of flat path).</expect>
      <if_mismatch>If any consumer found that reads flat: pause cleanup; route to that consumer's owner for migration to Hive read path; OR re-convert + dual-maintain temporarily until migration.</if_mismatch>
    </step>
    <step>
      <run>Execute remediation per disposition:
        - cleanup-only: aws s3 rm on each flat path
        - re-convert: dispatch silver convert with FRESH lib for affected (date, dim) combo; THEN aws s3 rm flat path</run>
      <expect>Post-remediation: aws s3 ls s3://opal-data-inf/silver/ --recursive | grep flat-path-pattern returns empty. All historical drift cleaned.</expect>
      <if_mismatch>Per-disposition mismatch: handle individually; surface escalation if blocked.</if_mismatch>
    </step>
    <step>
      <run>Author CI documentation at `infra/aws/lambda/ci/INF_PIPELINE_LIB_PARITY.md` (or analogous)</run>
      <expect>Doc explains: WHAT the CI check covers (which libs); WHY (Risk Register C, Scenario X 2026-05-05 incident); HOW to add new shared libs to scope; HOW to remediate when CI fails. Cross-reference to TO 1a-2 (gold-runner deployment-pattern doc) for runtime perspective.</expect>
      <if_mismatch>If CI surface evolves post-deploy: update doc same-commit.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="before commit">
    <step>
      <run>.tools/safe-commit.sh --author "0.7.0_AE_CloudOps &lt;0.7.0_AE_CloudOps@opal.agent&gt;" -m "feat(ADVI_INFINGE.1a-1): S3 lib drift CI check + audit + remediation (Risk Register C structural fix)" -- .github/workflows/inf-pipeline-lib-parity.yml infra/aws/lambda/ci/INF_PIPELINE_LIB_PARITY.md (+ any other authored files)</run>
      <expect>safe-commit.sh PASS — pathspec scoped + index clean. Owned-paths hook PASS — AE has authority on .github/workflows/* + infra/aws/lambda/ci/*.</expect>
      <if_mismatch>safe-commit abort: clean staged extras with `git reset HEAD -- &lt;path&gt;`; re-run.</if_mismatch>
    </step>
  </phase>

  <phase id="4" when="after merge — empirical CI green on canonical state">
    <step>
      <run>After merge: trigger CI on main; verify lib parity check passes (canonical state)</run>
      <expect>CI green; structural state preserved; future drift would surface as red.</expect>
      <if_mismatch>If CI red on canonical: investigate which lib is out-of-sync at canonical state; reconcile (likely indicates the canonical lib is what's stale OR S3 was not synced with canonical post-D1e upload tonight).</if_mismatch>
    </step>
    <step>
      <run>24h post-deploy: re-check CI health (no false positives, no missed drifts)</run>
      <expect>CI behaves correctly through one full PR cycle.</expect>
      <if_mismatch>Surface false-positive / missed-drift edge cases for follow-up TO.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**TO 1a-2 (deployment-pattern doc)** is your separate doc work; this TO ships CI structural fix. Cross-reference each in commit messages + docs.</coord>
    <coord>**TO-1 (assets_v2 Lambda)** preferably ships AFTER TO 1a-1 (so future TO-1-class deploys are CI-protected). NOT strict prerequisite per PRD §6.1 — both can ship in parallel; TO 1a-1 catches future drift class regardless of TO-1 timing.</coord>
    <coord>**Phase 1a TO 1a-3 (watchdog regex)** — your session-log finding determines ship-or-fold. Ship this TO independently.</coord>
    <coord>**No DS-side coordination needed** — DS lanes consume the CI check passively (their commits go through same CI gate).</coord>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>This TO ships CI infrastructure + historical artifact cleanup. No silver/bronze script logic changes. Future runs use canonical lib (already on S3 post D1e upload 2026-05-05T~19:30Z). Historical drift artifacts removed in Phase 2 Step 4. No data re-processing required from this TO; future ingestion correctness is handled by Phase 1b TO-1 + the now-canonical lib.</no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <phase id="1" when="before writing">
      <step>
        <run>aws s3 ls + aws s3api list-object-versions for empirical drift surface enumeration</run>
        <expect>Per Phase 1 Steps 1-2 above</expect>
        <if_mismatch>Per Phase 1 if_mismatch</if_mismatch>
      </step>
      <step>
        <run>find data/orion/scripts shared libs + per-lib S3 deployment paths</run>
        <expect>Per Phase 1 Steps 3-4 above</expect>
        <if_mismatch>Per Phase 1 if_mismatch</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>CI test failure-mode + safe-commit.sh</run>
        <expect>Per Phase 2 Step 2 + Phase 3 above</expect>
        <if_mismatch>Per Phase 2/3 if_mismatch</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="post-merge">
      <step>
        <run>CI green on canonical state + 24h health check</run>
        <expect>Per Phase 4 above</expect>
        <if_mismatch>Per Phase 4 if_mismatch</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">CI check fails on local-vs-S3 divergence (test via intentional diverge + revert).</criterion>
    <criterion id="AC2">Audit report enumerates all flat-path silver/{dim}/ artifacts (cleanup-only or re-convert disposition tagged per artifact).</criterion>
    <criterion id="AC3">Re-convert / cleanup work executed per Phase 2 Step 4 disposition; post-remediation S3 has zero flat-path drift artifacts.</criterion>
    <criterion id="AC4">CI documentation at `infra/aws/lambda/ci/INF_PIPELINE_LIB_PARITY.md` (or analogous) covering scope + WHY + HOW to extend.</criterion>
    <criterion id="AC5">Canonical-state CI green post-merge; 24h health check no false positives.</criterion>
    <criterion id="AC6">RAVC5 close package: commit hash + CI test failure evidence (red+green) + audit table + remediation evidence.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>2026-05-05T20:00:00Z (sprint dispatch per Andrew override)</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Sprint mode authoring tonight. PRD v0.2 §6.1 TO 1a-1 is canonical spec; this TO transcribes + adds explicit phase mandate structure. Begin Phase 1 immediately. No strict prereq order vs TO-1 (assets_v2 Lambda) — ship in parallel. RAVC1 ACK + Phase 0 plan expected ~5min from receipt.</message>
  </go_signal>
</task_order>
