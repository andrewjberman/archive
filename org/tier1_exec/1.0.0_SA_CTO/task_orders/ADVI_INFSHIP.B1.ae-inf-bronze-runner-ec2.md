<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-28-infship-b1-inf-bronze-runner-ec2</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-04-28</date>
    <status>complete</status><!-- AE 0.7.0~B 2026-04-28: shipped 2d1154c3 + 3b257557 (inf-pipeline-v1.6.0 EC2 + Lambda + 12:30 UTC cron) + d31809ca (user-data fix) + dcd10448 + cf11f13b (POSIX portability) + 05ae692b (orchestrator --upload-bronze) + 07316898 + ff52cd32 logs. Reconciled 2026-04-29 startup. -->
    <project_code>ADVI_INFSHIP</project_code>
    <to_serial>B1</to_serial>
    <priority>HIGH</priority>
    <prd>docs/architecture/ADVI_INFSHIP.md (Phase 1.5 Infrastructure formalization sub-wave)</prd>
  </metadata>

  <objective>
    Stand up the `inf-bronze-runner` EC2 instance + boot script that pulls
    all 9 Inflection dims (and transactions) sequentially via the Orion
    Connect manual API on a daily schedule, and lands them as bronze
    artifacts at `s3://opal-data-inf/bronze/orion-api/{date}/{dim}.csv`.
    The runner self-shutdowns post-completion. Triggered via
    `inf-jwt-trigger` Lambda mode_marker (existing dispatch primitive).

    Architecture is **Path X** (CTO-ratified): single low-volume EC2 vs
    BD's per-domain parallelism. Inflection's 305 HH / 852 acct / $199M
    AUA volume profile justifies single-instance sequential pulls at
    $1-2/day vs $9-18/day for per-domain mirror.
  </objective>

  <context>
    Andrew direct ~06:15Z (via COO MCP):

      "Probably relevant for you and CTO to check in with 0.6.1_AE and
       make sure they have TOs regarding putting together the actual
       infrastructure to manage all this. We probably want bronze/silver
       runners that use the manual_api to pull daily data and merge to
       silver parquets just like how bd-pipeline does it... The benefit
       to our scenario is we don't even need to scrape CSVs we can just
       have them use the manual api approach"

    Bronze pulls already exist as ad-hoc scripts under
    `data/orion/scripts/pull_inflection_*.py` (DS~A/B/D ownership). The
    9 dim list is authoritatively cataloged by DS~A in INFSHIP.B4
    deliverable `docs/architecture/INFLEC_DIMS_AND_TRANSACTIONS.md` (TO
    df4b3f86, dispatched 12:48Z; ETA 1-2h). B1 EC2 + boot script work
    can begin in parallel with B4 doc; orchestration sequence can pull
    from preliminary script list (see §spec_summary) and B4 doc supersedes
    when it lands.

    Existing infrastructure to reuse / mirror:
    - `inf-exporter` EC2 (Playwright/JWT capture) — TF module pattern
      reference; same family architecture (Lambda boot dispatch, self-
      shutdown post-task)
    - `inf-jwt-trigger` Lambda (ORIAPI.003 v1.5.8, deployed) — existing
      dispatch primitive; supports mode_marker payloads
    - `inf-gold-layer-runner` EC2 (currently STOPPED) — TF module
      reference for cron-driven boot pattern
    - bd-pipeline EC2 family (`bd-allocations`, `bd-transactions`,
      `bd-fees`, `bd-assets`, `bd-exporter`) — per-domain pattern
      reference (do NOT mirror per-domain; Path X is single instance)
    - bd-pipeline EventBridge crons (`bd_allocation_pipeline`,
      `bd_transaction_pipeline`, etc.) — daily cron pattern reference

    Existing ad-hoc bronze pull scripts (from DS sessions this week):
    1. `data/orion/scripts/pull_inflection_household.py` (DS~A)
    2. `data/orion/scripts/pull_inflection_performance.py` (DS~A)
    3. `data/orion/scripts/pull_inflection_activity.py` (DS~A)
    4. `data/orion/scripts/pull_inflection_billing.py` (DS~B)
    5. `data/orion/scripts/pull_inflection_tax_unrealized.py` (DS~B)
    6. `data/orion/scripts/pull_inflection_tax_realized.py` (DS~B)
    7. `data/orion/scripts/pull_inflection_assets.py` (DS~D)
    8. `data/orion/scripts/pull_inflection_accounts.py` (DS~A; NewPortfolio; planning)
    9. `data/orion/scripts/pull_inflection_transactions.py` (DS~A; Custom Reports; probe v0.2 e0ceec28)

    Output bronze landing pattern (already established by DS):
    `s3://opal-data-inf/bronze/orion-api/{YYYY-MM-DD}/{dim}.csv`

    JWT acquisition pattern (existing):
    The `inf-jwt-trigger` Lambda + `inf-exporter` Playwright EC2 already
    handle JWT lifecycle. Bronze runner SHOULD consume the JWT from
    `s3://opal-data-inf/auth/jwt.json` (or the canonical JWT cache path
    DS uses today — confirm with AE 0.6.1~B during build). Bronze runner
    does NOT acquire its own JWT.
  </context>

  <files_to_modify>
    <file action="create">infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf</file>
    <file action="create">infra/aws/ec2/inf-bronze-runner/userdata.sh</file>
    <file action="create">infra/aws/ec2/inf-bronze-runner/orchestrator.py</file>
    <file action="modify">infra/aws/ec2/EC2_MANIFEST.json (register inf-bronze-runner per CLAUDE.md rule 8)</file>
    <file action="modify">infra/aws/lambda/inf-jwt-trigger/handler.py (add mode_marker case for bronze-runner-boot if not already present)</file>
    <file action="create-or-extend">infra/aws/terraform/inf-pipeline/eventbridge-bronze-cron.tf (or extend existing crons file)</file>
  </files_to_modify>

  <spec_summary>
    **EC2 sizing:** t3.small (2 vCPU / 2 GB RAM). Sufficient for sequential
    HTTP requests + small parquet writes. NOT t3.micro — Python+pandas
    needs the headroom. Spot instance OK for cost (interruption tolerance
    acceptable since runner self-restarts via Lambda on next cron).

    **AMI:** Same Amazon Linux 2023 AMI as `inf-exporter` (consistent base).
    boto3 + pandas + requests + pyarrow pre-installed via userdata.sh
    bootstrap.

    **IAM role:**
    - s3:GetObject on `s3://opal-data-inf/auth/*` (JWT cache)
    - s3:PutObject on `s3://opal-data-inf/bronze/orion-api/*` (bronze landing)
    - ssm:UpdateInstanceInformation (SSM agent)
    - ec2:StopInstances on self (self-shutdown)
    - logs:CreateLogStream + logs:PutLogEvents (CloudWatch Logs)

    NO Lambda invoke (bronze runner is invoked-by, doesn't invoke). NO
    silver write (B2's silver chain Lambda owns silver writes).

    **B2 trigger via sentinel file (RATIFIED COO 14:05Z post AE 0.6.1~B
    catch):** orchestrator.py final step writes `_BRONZE_COMPLETE.json`
    sentinel to `s3://opal-data-inf/bronze/orion-api/{date}/`. B2's silver
    chain Lambda triggers via S3 EventBridge ObjectCreated rule on the
    sentinel. Keeps B1 IAM minimal (s3:PutObject suffices); no Lambda
    invoke permission needed. Supersedes B2's original "RECOMMENDED:
    Direct invoke" pattern.

    **Boot flow (userdata.sh + orchestrator.py):**
    1. `userdata.sh` runs once on instance boot:
       - Pull latest orchestrator.py + pull_*.py from S3 code prefix
         (mirroring EC2 code deployment standard per CLAUDE.md rule 12)
       - Activate Python venv with pinned deps
       - Exec orchestrator.py
    2. `orchestrator.py` runs the 9 dims sequentially:
       - Read JWT from `s3://opal-data-inf/auth/jwt.json` (or canonical path)
       - For each dim in DIMS_LIST (defined order, see B4 sequence §5):
         a. Invoke pull_inflection_{dim}.py with --date {today_iso}
         b. Verify bronze landing at expected S3 key
         c. Log to CloudWatch + emit progress to MCP via boto3 SQS or stdout
            (whichever is current pattern)
         d. On per-dim failure: log + continue to next dim (do NOT abort
            chain; partial bronze is more valuable than no bronze)
       - After all 9 dims attempted: emit summary status (counts of
         success/fail/skip) to MCP / CloudWatch
       - Self-shutdown: `aws ec2 stop-instances --instance-ids $(curl
         http://169.254.169.254/latest/meta-data/instance-id)`

    **Sequence for orchestrator (preliminary; supersede with B4 §5):**
    Default order (no inter-dim silver dependencies at bronze layer):
    1. household (foundation; cheap; ~30s)
    2. accounts_v2 (NewPortfolio sync GET, ~1.2s)
    3. activity (canonical AUA; ~1-2 min)
    4. performance (~1-2 min)
    5. billing (~1-2 min)
    6. tax_unrealized (~30-60s)
    7. tax_realized (~30-60s)
    8. assets (Path C — reads canonical, not API; ~30s; SKIP if INFSHIP.A2
       resolves to direct API pull then this slot becomes API call ~5-10
       min)
    9. transactions (Custom Reports CSV; ~1-2 min; large payload)

    Total wall-clock: ~5-15 minutes for happy path; <30 min worst case.

    **EventBridge cron:** Daily at 04:00 UTC (~12:00 AM ET; pre-market;
    well after Orion's nightly batch close). Triggers `inf-jwt-trigger`
    Lambda with payload `{"mode_marker": "bronze_runner_boot"}` which
    starts the EC2 instance.

    **Manifest registration:** Add `inf-bronze-runner` row to
    `infra/aws/ec2/EC2_MANIFEST.json` per CLAUDE.md rule 8. Required
    fields: instance_id (post-apply), service_name, code_prefix
    (s3://opal-data-inf/code/bronze-runner/), iam_role, security_group,
    boot_command_arn (Lambda mode_marker reference).

    **Code deployment standard:** Per CLAUDE.md rule 12 — orchestrator.py
    + pull_*.py copies to `s3://opal-data-inf/code/bronze-runner/` via
    `safe-ec2-deploy.sh`. Userdata.sh on boot pulls from S3, never inlined
    on instance. NEVER push code directly to instance.
  </spec_summary>

  <acceptance_criteria>
    <ac>1. Terraform applied with 0-diff post-deploy (per CLAUDE.md rule 1).
        Tag: `inf-pipeline-vX.Y.Z` per pipeline tag versioning rule.</ac>
    <ac>2. EC2 instance registered in `EC2_MANIFEST.json` (CLAUDE.md rule 8).</ac>
    <ac>3. EventBridge cron fires `inf-jwt-trigger` Lambda daily at 04:00 UTC.
        Lambda starts inf-bronze-runner EC2.</ac>
    <ac>4. Boot test: manually trigger via `aws lambda invoke` with mode_marker
        payload; verify EC2 starts, orchestrator.py runs, 9 dim pulls execute,
        bronze artifacts land at expected S3 keys, instance self-shutdowns.</ac>
    <ac>5. Logs visible in CloudWatch under `/aws/ec2/inf-bronze-runner` log
        group.</ac>
    <ac>6. Per-dim failure does NOT abort chain (validated via injected
        failure on one pull script during test).</ac>
    <ac>7. Total wall-clock for happy path ≤30 minutes.</ac>
    <ac>8. Cost monitoring: instance auto-stops; no >1h runaway.</ac>
    <ac>9. RAVC4 to CTO with: TF apply log, EC2 instance ID, first successful
        boot run timestamp + bronze artifacts S3 paths, CloudWatch log
        sample, cost projection per month.</ac>
  </acceptance_criteria>

  <gates_and_dependencies>
    <gates>
      INFSHIP.B4 (DS~A 9-dim spec doc; in flight df4b3f86 ETA 1-2h) —
      provides authoritative dim list + sequence + cadence. B1 can BEGIN
      in parallel using preliminary list in §spec_summary; orchestrator.py
      DIMS_LIST + sequence is updated to match B4 §5 when doc lands.

      Coordination with AE 0.6.1~B (L5 ORIAPI work): JWT cache path may
      change as L5 lands; AE 0.6.1~B holds canonical JWT lifecycle. Sync
      with them before finalizing JWT read path in orchestrator.py.
    </gates>
    <unblocks>
      INFSHIP.B2 (AE 0.6.1~B silver chain Lambda — needs bronze landing
      to trigger).
      INFSHIP.B3 (AE 0.6.1~B QA runner — references same dim catalog +
      orchestrator pattern).
    </unblocks>
  </gates_and_dependencies>

  <coordination>
    - DS~A: source of truth for dim list, sequence, refresh cadence (B4
      doc). MCP DS~A if any dim's pull script signature is unclear.
    - DS~B: owns billing/tax bronze pull scripts. Consult on Tax-specific
      args (costBasisOptionId=0 vs 1).
    - DS~D: owns assets pull script (Path C); flag any blocker on the
      canonical-source path (will resolve when INFSHIP.A2 lands).
    - AE 0.6.1~B: JWT cache path canonical owner. Coordinate before
      finalizing JWT read.
    - DT: Lambda deployment per CLAUDE.md rule 1 (TF only) + EC2 deployment
      per rule 7 (safe-ec2-deploy.sh wrapper). DT may need to own the
      `safe-ec2-deploy.sh` invocation if your lane doesn't have direct
      authority.

    Minimal DS-side work expected; this is primarily AE TF + boot script.
  </coordination>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with TF tag + EC2 instance ID + first successful
        boot timestamp + bronze landing evidence + CloudWatch log sample +
        cost projection. CC COO + DS~A (for B2 silver chain handoff).</on_complete>
  </ravc_target>

  <estimated_effort>
    4-8 hours for full ship: ~2h TF authoring (EC2 + IAM + EventBridge +
    Lambda mode_marker), ~2h userdata.sh + orchestrator.py, ~1h
    EC2_MANIFEST + safe-ec2-deploy + S3 code upload, ~1-2h boot test +
    iteration + CloudWatch verify. May be 2 sessions if blocked on JWT
    cache path coordination with AE 0.6.1~B during their L5 work.
  </estimated_effort>
</task_order>
