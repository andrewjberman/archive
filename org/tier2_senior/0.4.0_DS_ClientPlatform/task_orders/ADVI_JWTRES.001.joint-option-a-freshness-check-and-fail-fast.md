<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_JWTRES.001</id>
    <project>ADVI_JWTRES</project>
    <title>Option A — JWT freshness check + fail-fast in bronze orchestrator + standalone pull scripts</title>
    <issued_to>0.4.0_DS_ClientPlatform + 0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>1-2d (DS + AE in parallel)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_JWTRES.md §2 Option A + §4 Andrew rulings</ref>
    <ref type="source_brief">org/tier2_senior/0.6.1_AE_PartnerETL/deliverables/CTO_BRIEFING_INFLEC_HISTBACKFILL_AND_JWT_RESILIENCE_20260430.md §3</ref>
    <ref type="incident">2026-04-30 09:09Z silent-401 outage: all 5 Inflection bronze dim pulls failed `{ok:0,fail:5}` because JWT had expired 14 min before Lambda deploy. Bronze layer outage went undetected until gold downstream produced zero rows.</ref>
    <ref type="ssm_lift">inf-pipeline-v1.7.1 (b831e55c4) KMS+SSM Lambda fix; v1.7.4 (45af4950c) SSM agent race retry; v1.7.5 (9764c07e9) SM JWT store dual-path. JWTRES is defense-in-depth atop these.</ref>
    <ref type="canonical_pattern">docs/architecture/ADVI_ORIAPI.md §270/273/424/428/494 — Authorization: Session &lt;JWT&gt; (NOT Bearer)</ref>
    <ref type="jwt_paths">JWT stored in SM `orion/jwt/current` (raw token; consumer prepends `Session ` prefix) AND S3 `s3://opal-data-inf/orion/jwt/current.json` (JSON wrapper) — dual-path additive per v1.7.5</ref>
  </references>

  <context>
    Today (2026-04-30) silent-401 incident exposed a class of failure: JWT expired but bronze pulls continued executing, getting 401 responses, and silently returning zero records. Gold downstream produced zero output before the issue was detected.

    JWTRES Option A closes this class structurally: bronze orchestrator + standalone pull scripts must check JWT freshness BEFORE pulling. On near-expiry or post-expiry, fail-fast with a clear error and emit a CloudWatch metric so ops knows immediately.

    Andrew ruling: Option A first → production-validate → then Option B (async auto-recovery, separate TO). Option A is intentionally simple — no auto-recovery; just visibility + fail-fast.

    JWT freshness threshold: recommended 30 min (configurable via env var). Rationale: bronze pulls take 5-15 min depending on dim; 30-min headroom ensures completion within token lifetime.
  </context>

  <scope>

  ## DS sub-tasks (.001a — `0.4.0_DS_ClientPlatform`)

    1. **`check_jwt_freshness()` helper module** at `data/orion/manual_api/jwt_freshness.py` (new file).
       - Function signature: `def check_jwt_freshness(min_remaining_seconds: int = 1800) -> JwtFreshnessReport`
       - JWT load order: try SM `orion/jwt/current` first (raw token); fall back to S3 `s3://opal-data-inf/orion/jwt/current.json` (JSON wrapper) if SM access fails
       - Parse JWT exp claim (decode without verification — claim is unsigned; signature verification is Orion-side concern)
       - Returns `JwtFreshnessReport` dataclass with fields: `is_fresh: bool`, `seconds_remaining: int`, `expires_at: datetime`, `source: Literal["sm", "s3"]`, `raises_on_stale: Exception | None`
       - On near-expiry (< min_remaining_seconds): `is_fresh = False`, `raises_on_stale = JwtNearExpiryError(...)`
       - On post-expiry: `is_fresh = False`, `raises_on_stale = JwtExpiredError(...)`
       - Defensive: if both SM and S3 paths fail, raise `JwtUnreadableError` (treat as stale; fail-fast)

    2. **Pull script integration**. Modify all 5 standalone Inflection bronze pull scripts to call `check_jwt_freshness()` at startup:
       - `pull_inflection_assets.py` (or v2)
       - `pull_inflection_assets_v2.py`
       - `pull_inflection_representatives.py`
       - `pull_inflection_positions_daily.py`
       - `pull_inflection_<other>.py` (whatever's in `data/orion/manual_api/`)
       - On stale: print clear error message + sys.exit(2) (distinguishable exit code)
       - Configurable threshold via `--jwt-min-remaining-seconds` flag OR env var `JWT_MIN_REMAINING_SECONDS` (default 1800)

    3. **CW metric emission from DS side** (DS handles the ad-hoc emission since DS owns the standalone pull scripts; AE handles orchestrator-side per below):
       - On near-expiry detected: emit `Inflection/JwtResilience/JwtNearExpiry` metric (counter, dimensioned by script_name)
       - On post-expiry detected: emit `Inflection/JwtResilience/JwtExpired` metric (counter, dimensioned by script_name)
       - Use boto3 cloudwatch.put_metric_data; if put fails, log + continue (don't double-fail)

    4. **Unit tests** at `tests/test_jwt_freshness.py`:
       - Fresh JWT → `is_fresh=True`
       - Near-expiry JWT → `is_fresh=False, raises_on_stale=JwtNearExpiryError`
       - Expired JWT → `is_fresh=False, raises_on_stale=JwtExpiredError`
       - SM fallback to S3 (mock SM failure)
       - Both unreadable → JwtUnreadableError
       - Threshold configurability

  ## AE sub-tasks (.001b — `0.6.1_AE_PartnerETL`)

    5. **Bronze orchestrator integration**. inf-bronze-runner orchestrator (currently invokes pull scripts via SSM RunCommand or direct EC2 dispatch — AE confirms current pattern):
       - Pre-flight: orchestrator calls `check_jwt_freshness()` once before triggering ANY pull script
       - On stale: orchestrator emits `Inflection/JwtResilience/OrchestratorAbort` metric + exits non-zero + sends SNS alert to inf-otp-alert
       - On fresh: orchestrator continues; each pull script also re-checks (defense in depth — multi-process gap protection)

    6. **CW alarm `Inflection-JwtResilience-NearExpirySpike`**:
       - Triggers when `Inflection/JwtResilience/JwtNearExpiry` metric > 1 in 5min window
       - Routes to SNS topic `inf-otp-alert` (existing)
       - Andrew receives SMS/email immediately on JWT freshness failures

    7. **IAM grants for CW PutMetricData**. Both inf-bronze-runner role + standalone-pull-runner roles need:
       - `cloudwatch:PutMetricData` on `Inflection/JwtResilience/*` (or unrestricted PutMetricData if simpler)
       - SM `secretsmanager:GetSecretValue` on `orion/jwt/current` (already granted to inf-gold-layer per v1.7.5; verify or extend to bronze runners)

    8. **Terraform + 0-diff verify + tag**. Tag `inf-pipeline-v1.7.X` (next available).

  ## Joint integration testing

    9. **Production validation cycle**. After ship:
       - Wait for next Cycle (12:13Z UTC daily JWT refresh cron)
       - Verify: orchestrator logs show freshness check passing (positive case)
       - Manually expire JWT (or use a mock-expired JWT); verify orchestrator fails fast + alarm fires
       - Document validation results in session log

    10. **Production validation gate for Option B**. Per Andrew ruling: Option A must production-validate before Option B (async auto-recovery, separate TO ADVI_JWTRES.002 staged). Option A validation = 1 successful Cycle 2 + 1 successful manual-expiry test.

  </scope>

  <acceptance_criteria>
    1. `data/orion/manual_api/jwt_freshness.py` shipped with documented `check_jwt_freshness()` helper.
    2. JwtFreshnessReport dataclass + 3 exception classes (JwtNearExpiryError, JwtExpiredError, JwtUnreadableError) defined.
    3. SM-first → S3-fallback JWT load order implemented + tested.
    4. All 5 standalone bronze pull scripts integrate the freshness check at startup; near-expiry exits non-zero with clear error.
    5. inf-bronze-runner orchestrator integrates pre-flight freshness check + emits OrchestratorAbort metric on stale + sends SNS alert.
    6. CW metrics emitted to `Inflection/JwtResilience/*` namespace.
    7. CW alarm Inflection-JwtResilience-NearExpirySpike configured + SNS routing verified.
    8. IAM grants verified (PutMetricData + SM GetSecretValue on bronze runner roles).
    9. Terraform 0-diff; tag pushed; deploy recorded.
    10. Unit tests at tests/test_jwt_freshness.py PASS.
    11. Production validation: 1 clean Cycle (positive case) + 1 manual-expiry case (negative case validated).
    12. Compiler tools mandate satisfied.
    13. Pre-commit gate (CLAUDE.md Rule 14) PASS on all .py edits.
    14. RAVC4 to COO + CTO with: jwt_freshness.py path, CW namespace + alarm names, validation evidence (cycle + manual-expiry), validation cycle log link.

    DS side blocks AE side at: JwtFreshnessReport interface (AE wires orchestrator around it). AE side blocks DS at: SM IAM grant verification + CW namespace setup. DS+AE coordinate via direct MCP.
  </acceptance_criteria>

  <data_reprocess_scope>
    <no_reprocess_needed>jwt_freshness.py is a new startup-validation module; changes to pull scripts affect call gating only (startup check before any API calls); no change to bronze S3 write paths or data content; historical data semantically correct at prior version; no downstream consumer reads the changed code path for pre-patch partitions</no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-iam service [inf-bronze-runner role] before adding PutMetricData grant</check>
      <check>comp-iam service [standalone pull script runner roles] for SM access</check>
      <check>comp-blast on inf-bronze-runner Lambda or EC2 (whichever orchestrates) — verify no downstream surprises</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh on all .py edits</check>
      <check>from __future__ import annotations on jwt_freshness.py + modified pull scripts</check>
      <check>terraform plan + 0-diff verify (AE)</check>
    </before_commit>
    <after_commit>
      <check>comp-iam gaps (AE; verify no IAM regressions)</check>
      <check>S3 upload + comp-pipescript deployed MATCH (DS; if scripts integrated into chain)</check>
      <check>Tag + push + record-terraform-deploy.sh (AE)</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_artifacts>
      <artifact>data/orion/manual_api/jwt_freshness.py (NEW DS module; AE references for orchestrator integration)</artifact>
      <artifact>data/orion/manual_api/pull_inflection_*.py (modified by DS to integrate freshness check)</artifact>
      <artifact>CloudWatch namespace Inflection/JwtResilience (NEW; AE wires alarm; both emit metrics)</artifact>
      <artifact>SNS topic inf-otp-alert (existing; AE adds alarm subscription)</artifact>
      <artifact>SM secret orion/jwt/current (existing per v1.7.5; AE verifies bronze runner IAM grants)</artifact>
    </shared_artifacts>
    <coordination_protocol>
      DS authors jwt_freshness.py first (interface stable); AE wires orchestrator + CW alarm + IAM around it. Both ship in same wave. Direct MCP for handoff. ADVI_JWTRES.002 (Option B async auto-recovery) is staged separately and gates on .001 production validation.
    </coordination_protocol>
  </cross_domain_coordination>
</task_order>
