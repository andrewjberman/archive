<task_order>
  <metadata>
    <id>ADVI_JWTRES.002</id>
    <project>ADVI_JWTRES</project>
    <title>Option B — Async JWT Auto-Recovery (inf-jwt-trigger invoke + SM poll)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>implementation-complete-deploy-staged</status><!-- 0.7.0_AE_CloudOps 2026-05-01: code committed a63d76d51 (recover_or_exit + orchestrator) + e3325b6d4 (IAM tf). terraform plan 1-add 0-change 0-destroy. RAVC4 sent to COO+CTO. Deploy (tf apply + S3 upload) staged pending Wave B RAVC4 + COO Wave C GO. CW namespace: Inflection/JwtResilience (same as Phase 1; COO/CTO confirm if Inflection/HistBackfill/RateLimiter intended). -->
    <priority>P1 — bolsters HISTBF backfill resilience; Wave C dispatch authorization conditional on this shipping</priority>
    <estimated_effort>3-5d (per AE 0.7 estimate in source brief §3)</estimated_effort>
    <gates_on>Andrew GO (given 2026-05-01). Deploy gates on ADVI_HISTBF Wave B RAVC4 (do not modify running Wave B orchestrator mid-run).</gates_on>
  </metadata>

  <context>
    JWTRES Phase 1 (Option A — fail-fast) shipped 2026-04-30:
    - jwt_freshness.py assert_fresh_or_exit() in bronze orchestrator + standalone pull scripts
    - Behavior: if JWT TTL ≤ 30 min → emit CW metric JwtNearExpiry → exit non-zero
    - Ops response required: manual inf-jwt-trigger Lambda invoke, then re-run

    Andrew direction 2026-05-01: proceed to Phase 2 (Option B — auto-recovery).
    Motivation: the device cookie (~30-90d, enables skip-OTP re-login via Playwright) IS the
    long-duration credential. The 10h session JWT is a short-lived derivative. Option B closes
    the loop: when the JWT expires, automatically use the device cookie path (via inf-jwt-trigger
    Lambda) to get a fresh JWT without human intervention.

    JWT architecture facts (source brief §2):
    - SM:  orion/jwt/current (raw JWT string)
    - S3:  s3://opal-data-inf/orion/jwt/current.json (JWT + issued_at_iso + expires_at_iso + ttl_seconds)
    - inf-jwt-trigger Lambda: invokes inf-exporter EC2 via SSM → orion_export.ts --mode jwt-extract
      → Playwright captures Authorization: Session header → writes SM + S3
    - EC2 boot-to-JWT latency: ~13 min
    - Poll ceiling: 15 min (2-min buffer above boot latency)

    HISTBF Wave B v3 is currently in flight (CYCLE 56b947d9, ~125h run).
    Do NOT deploy to production orchestrator mid-run. Implement + test now; deploy
    before Wave C dispatch authorization.
  </context>

  <objective>
    Upgrade the bronze orchestrator so that JWT near-expiry triggers automatic recovery
    instead of a hard stop. The recovery path: invoke inf-jwt-trigger Lambda → poll SM
    orion/jwt/current for issued_at_iso advancement → resume with fresh JWT.
    If recovery fails (timeout), fall back to Phase 1 fail-fast behavior (emit CW +
    abort cleanly).

    Implement as changes to:
    1. jwt_freshness.py — add recover_or_exit(lambda_name, max_wait_s=900) function
    2. run_backfill_orchestrator.py — call recover_or_exit (not assert_fresh_or_exit)
       at orchestrator startup AND at the start of each dim iteration (not just startup)
    3. IAM — add lambda:InvokeFunction on inf-jwt-trigger ARN to
       inf-bronze-runner-ec2-role via Terraform (inf-pipeline iam.tf)
    4. CW metrics — JwtAutoRecoveryAttempted, JwtAutoRecoverySucceeded,
       JwtAutoRecoveryFailed (distinct from Phase 1 JwtNearExpiry/JwtRefreshFailed)

    Individual pull scripts (pull_inflection_*.py) KEEP their Phase 1
    assert_fresh_or_exit() as secondary defense. No changes to pull scripts.
  </objective>

  <acceptance_criteria>
    1. recover_or_exit() implemented in jwt_freshness.py:
       - Reads current issued_at_iso from S3 orion/jwt/current.json
       - Invokes inf-jwt-trigger Lambda (async — do not wait for Lambda return; it's
         fire-and-poll, not synchronous)
       - Polls SM orion/jwt/current every 30s, checks issued_at_iso advanced vs snapshot
       - On advancement: reload JWT, log recovery success, emit JwtAutoRecoverySucceeded
       - On 15-min timeout: emit JwtAutoRecoveryFailed, exit non-zero with clear error

    2. run_backfill_orchestrator.py calls recover_or_exit() (replacing
       assert_fresh_or_exit()) at:
       - Orchestrator startup (before any pulls begin)
       - Start of each dim iteration (e.g., before each chunk-dispatch loop)
       This ensures mid-run JWT expiry is caught at the next dim boundary, not just
       at next restart.

    3. IAM: lambda:InvokeFunction on inf-jwt-trigger ARN added to
       inf-bronze-runner-ec2-role via Terraform. terraform plan shows 0 unintended
       changes. Tag: inf-pipeline-v1.7.{next}.

    4. CW metrics: JwtAutoRecoveryAttempted, JwtAutoRecoverySucceeded,
       JwtAutoRecoveryFailed emitted to Inflection-HistBackfill-RateLimiter namespace
       (same namespace as Phase 1 metrics for dashboard parity).

    5. Local test: add a dry-run mode / mock test to jwt_freshness.py verifying
       the poll loop logic (mock issued_at_iso advancement after N polls). Gate
       the commit with ds-commit-gate (py_compile + AST scanner + ruff).

    6. DEPLOY GATE: Do NOT apply terraform or deploy to production S3 until
       ADVI_HISTBF Wave B RAVC4 is received. Upload to S3 code path and plan
       the terraform apply in advance; execute deployment when Wave B closes and
       COO issues Wave C dispatch authorization.

    7. RAVC4 to COO + CTO on completion, including:
       - terraform plan output (0 unintended changes)
       - jwt_freshness.py diff summary (recover_or_exit added, assert_fresh_or_exit
         preserved for pull script use)
       - CW metric namespace confirmed
       - Confirmation: production deploy is staged, awaiting COO Wave B RAVC4 → Wave C GO
  </acceptance_criteria>

  <notes>
    Source brief spec: AE 0.6.1 brief §3 Option B — "bronze orchestrator invokes
    inf-jwt-trigger Lambda directly and polls SM orion/jwt/current until issued_at_iso
    advances or timeout (15 min)."

    The inf-jwt-trigger Lambda ARN is available in the inf-pipeline Terraform state or
    AWS console. The Lambda is already deployed and in production use (ADVI_INFSHIP.B1,
    ADVI_ORIAPI.004 CW alert integration).

    Andrew direction 2026-05-01: device cookie (~30-90d) as the long-duration credential
    enabling automatic JWT refresh without human intervention. This TO implements that path.

    Option C (direct REST auth — bypassing Playwright) remains deferred per Andrew 2026-04-30
    ruling. Do not scope-expand into Option C here.

    JWTRES.001b (AE 0.6.1) wired Phase 1. Coordinate with AE 0.6.1 if the orchestrator
    has changed since 2026-04-30 (check git log for run_backfill_orchestrator.py).
  </notes>
</task_order>
