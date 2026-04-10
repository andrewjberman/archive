<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-v2-prestep-integration</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-10</date>
    <status>complete</status>
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Reinstate `build_canonical_prices_v2.py` as a scheduled daily job on the bd-gold-layer-runner EC2, executed as a pre-step before `gold_dispatch.sh` on every boot. This closes the weekend/holiday gap in canonical_prices that caused the Apr 3-5 chart dropout and will recur on every Saturday, Sunday, and US market holiday for the rest of 2026 until fixed. v2 runs FIRST, writes a fresh canonical_prices.parquet with T3 linear_interpolation filling gap dates, then the gold A/B/C/D chain consumes it. DS handles the code + gold_dispatch integration + S3 deploy; an AE handoff brief covers the EventBridge rule and eventual bd-price-update Job 1 deprecation.
  </objective>

  <context>
    Background: Today's session established (a) canonical_prices v2 is deprecated from the gold runner and the daily canonical_prices update was migrated to bd-price-update Lambda in the late-March ADVI_PRICES wave, (b) bd-price-update only fires on weekdays via the bd-allocation-processor → async-invoke chain, (c) the Lambda has no T3 linear_interpolation or gap-date fill logic, so weekend and holiday dates are never written to canonical_prices, (d) every gold script that reads canonical_prices with a naive date lookup (A_03.positions_cube, B_00.canonical_holdings, B_01.holdings_lots, E_05, E_06, E_07, E_10, E_11, E_13, E_14, E_16) has a latent version of the bug the other DS just fixed in B_00. Full trace is in `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/gold_trigger_chain_trace_and_d00c_role_split_fix.md` parts 5-6, with Andrew's decision on the remediation path in the subsequent conversation.

    Andrew's decision (2026-04-10): reinstate v2 as a scheduled nightly job on the gold runner, running as a pre-step before gold_dispatch. v2 is a full rebuild (not incremental) — it reads all transactions + historical_prices and writes a fresh canonical_prices.parquet each run. On the c6i.16xlarge gold runner with parallel ThreadPoolExecutor I/O, expected runtime is ~10-20 minutes, which is acceptable given the runner is already boot-warm for the gold chain.

    Architecture after this TO ships:

    ```
    22:00 UTC daily cron (every day, not just weekdays)
      ↓
    bd-gold-trigger Lambda (or a new dedicated trigger Lambda — AE choice)
      ↓
    bd-gold-layer-runner EC2 boots
      ↓
    run-gold-layer.sh
      ↓
    build_canonical_prices_v2.py      ← NEW PRE-STEP
      (full rebuild: T1 + T2 + T3 interpolation + T4 carry-forward)
      writes silver/prices/canonical_prices.parquet
      ↓
    gold_dispatch.sh --chain full --incremental
      (existing chain; A_03 and B_01 now see fresh canonical_prices with weekend fill)
      ↓
    auto-shutdown
    ```

    Prerequisites: ADVI_GLDRST.021 (source-tag + diff-before-ship) must be complete first. This TO does NOT modify v2's outlier cap or aggregation logic — that is frozen per .021.

    Coordination with bd-price-update Lambda: once v2 runs nightly, the Lambda's Job 1 (daily canonical_prices write) becomes redundant work. Two-phase handling: (a) leave both running for the first week, (b) diff weekday v2 output vs Lambda output on overlapping dates to confirm v2 matches or cleanly dominates, (c) AE disables Job 1 in the Lambda (keep Job 2 for interpolated_prices since v2 still reads it). Phase (c) is in the AE handoff brief, not this TO.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    - `comp-blast build_canonical_prices_v2.py` — confirm current consumers (should be none in the live pipeline since v2 isn't scheduled; any matches are historical references)
    - `comp-blast gold_dispatch.sh` — confirm downstream blast radius of the orchestrator before inserting a new pre-step
    - `comp-pipescript io build_canonical_prices_v2.py` — capture v2's I/O contract (reads: silver/transactions/, silver/historical_prices.parquet, silver/prices/canonical_prices.parquet; writes: silver/prices/canonical_prices.parquet)
    - Read `data/black_diamond/scripts/gold/run_gold_layer.sh` and `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh` in full — understand the current boot-to-dispatch wrapper chain and pick the right insertion point.

    Phase 2 (before committing):
    - `comp-pipescript io` on the modified `gold_dispatch.sh` and the new silver-prep chain — confirm v2 is registered in the catalog and runs before A_00
    - Dry run: `bash gold_dispatch.sh --chain silver-prep --dry-run` (or whatever the new chain name is) should execute v2 with `--dry-run` and exit cleanly without writing to S3
    - Run v2 once locally against dev transactions if available; verify the output row count and date range are sane

    Phase 3 (after committing, before the first production run):
    - `comp-blast run-gold-layer.sh` — verify the boot script changes haven't broken the normal chain path
    - Manually verify on a test EC2 boot (or via SSM dry-run) that the new pre-step executes, v2 writes canonical_prices, and gold_dispatch picks it up. If a full test boot is not feasible, document the verification deferral and the plan to watch the first scheduled production run closely.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `data/black_diamond/scripts/gold/gold_dispatch.sh` (dispatcher orchestrator — DS owns code, AE owns deployment cadence)
    shared_resource: `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh` (EC2 boot script — AE territory, DS may read-only reference)
    shared_resource: `infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh` (stale comment at line 11 to be cleaned up as part of this TO)
    shared_resource: `infra/aws/terraform/bd-pipeline/eventbridge.tf` (new daily cron rule — AE writes terraform, DS writes the AE brief)
    shared_resource: `infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py` (Job 1 eventually disabled — AE work, documented in the AE brief but NOT modified in this TO)
    also_in_to: ADVI_GLDRST.021 (must complete first; .022 depends on .021's source tag being live)
    last_write_owner: 0.4.0_DS_ClientPlatform for gold_dispatch.sh + v2 script, 0.6.0_AE_PartnerETL for run-gold-layer.sh + eventbridge.tf + terraform
    required_action: "Read the AE handoff brief section of this TO. DS cannot edit run-gold-layer.sh directly — it lives in infra/aws/ec2/ which is AE territory. DS delivers the brief as docs/briefs/ae-brief-v2-prestep-integration.md and references it in the session log Next Steps. AE picks up the brief separately."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. **v2 script location decision.** EITHER (a) `build_canonical_prices_v2.py` is moved from `data/black_diamond/scripts/silver/` to `data/black_diamond/scripts/gold/` so the existing `aws s3 sync "s3://${S3_BUCKET}/code/gold/"` in `run-gold-layer.sh:79` picks it up, OR (b) the script stays in silver/ and a targeted `aws s3 cp` is added to the boot script to pull it alongside the gold sync. Pick option (a) if v2's `from lib.ticker_overrides import ...` at v2:46 can resolve against `code/gold/lib/` (it should — gold/lib has the same layout as silver/lib for these shared modules). Document the decision in the session log.

    2. **gold_dispatch.sh catalog entry.** v2 is registered in `gold_dispatch.sh` CATALOG with a new ID (suggested: `S_00` for "silver prep 00", or reuse a convention from the existing ID scheme). The entry uses `--dry-run` translation like the other catalog entries so `--dry-run` dispatch still works. Default flags are `--upload` (v2 writes canonical_prices to S3).

    3. **New chain `silver-prep` or equivalent.** A new chain definition in `gold_dispatch.sh` includes exactly `S_00` (v2), runs ahead of the full chain. The `full` chain definition is updated to `silver-prep + foundation + canonical + downstream` so a single `--chain full` invocation runs v2 first, then A, B, C, D in sequence. The `rebuild` alias follows suit.

    4. **Freshness gate integration.** v2 runs BEFORE the existing `check_freshness()` gate at `gold_dispatch.sh:152-181`, OR the freshness gate is updated to skip v2 and only gate A/B/C/D. Rationale: v2 must run even when silver allocations haven't advanced, because weekend/holiday dates still need gap-fill interpolation from the existing historical_prices.parquet. A v2 run on a no-new-data day is a no-op in terms of weekday dates but still fills weekends.

    5. **run_gold_layer.sh wrapper.** The wrapper at `data/black_diamond/scripts/gold/run_gold_layer.sh` delegates to `gold_dispatch.sh --chain full --incremental` in `incremental` mode and `gold_dispatch.sh --chain rebuild` in `full` mode (unchanged). The wrapper now transparently runs v2 first because v2 is part of the `full` chain definition.

    6. **deploy-to-ec2.sh stale comment cleanup.** The comment at `infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh:11` is updated to reflect the new reality. If v2 moves to `code/gold/` (option a), the comment drops the `code/silver/` line entirely since silver scripts are no longer synced to the runner. If v2 stays in silver/ (option b), the comment is updated to list only the files that are actually pulled.

    7. **AE handoff brief.** A new file `docs/briefs/ae-brief-v2-prestep-integration.md` is written, addressed to 0.6.0_AE_PartnerETL, covering:
       - New daily cron EventBridge rule: `cron(0 22 * * ? *)` — every day including weekends and holidays, targeting the existing `bd-gold-trigger` Lambda OR a new dedicated trigger Lambda (AE choice). Note: this is in addition to the existing `bd-gold-nightly-fallback` at 23:00 UTC weekdays, not a replacement.
       - Diff protocol for the first week: leave bd-price-update Job 1 running, diff v2's weekday canonical_prices against the Lambda's output on overlapping dates, confirm match or dominance, then disable Job 1 in the Lambda (keep Job 2 for interpolated_prices).
       - IAM check: confirm the gold runner's instance profile already has s3:GetObject + s3:PutObject on `silver/prices/*` and `silver/historical_prices.parquet`. It should (bd-price-update Lambda has these permissions and the gold runner has broader S3 access), but verify before shipping.
       - Rollback plan: if v2 on the gold runner fails or corrupts canonical_prices, the rollback is to (a) revert gold_dispatch.sh to drop the silver-prep chain step, (b) push + S3 deploy, (c) rely on bd-price-update Lambda's existing Job 1 path for weekday canonical_prices until the bug is fixed. Weekends will regress to the current dropout behavior during rollback.

    8. **Dry-run verification.** Before committing, run `bash data/black_diamond/scripts/gold/gold_dispatch.sh --chain full --dry-run` locally. Verify the output shows v2 being invoked first, then A_00 through D_04 in order. No S3 writes should occur.

    9. **Compile check.** `python -m py_compile` on any modified Python files. `bash -n` syntax check on `gold_dispatch.sh` before committing.

    10. **Commit + push + S3 deploy.** Standard DS cycle. Files: modified `gold_dispatch.sh`, relocated or unchanged `build_canonical_prices_v2.py`, modified `deploy-to-ec2.sh` comment, new `docs/briefs/ae-brief-v2-prestep-integration.md`. `--author` on commit, push to CLOUD, `aws s3 sync` or targeted `aws s3 cp` for each changed script file. Parity scan after upload: all changed files' local md5 must equal S3 etag.

    11. **Runner NOT triggered.** As with .021, this TO is code staging only. The first v2 run on the gold runner happens when Andrew or AE manually triggers the runner (or when the next scheduled EventBridge fire occurs after AE lands the new cron rule). DS does not trigger the runner in this TO.

    12. **Session log** documents: the script location decision (option a or b + rationale), the diff-before-ship output from the local dry run, the AE brief path, the commit SHA, the S3 etags, the Compiler Tools section with all three phases, and the Next Steps block naming AE 0.6.0 for the EventBridge + Job 1 follow-up.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/gold_dispatch.sh</file>
      <file action="modify or move">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
      <file action="modify">infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh</file>
      <file action="create">docs/briefs/ae-brief-v2-prestep-integration.md</file>
      <file action="reference">infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh</file>
      <file action="reference">data/black_diamond/scripts/gold/run_gold_layer.sh</file>
      <file action="reference">infra/aws/terraform/bd-pipeline/eventbridge.tf</file>
      <file action="reference">infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">ADVI_GLDRST.021 MUST be complete before this TO starts. Check the status field on .021 — if not `complete`, do not begin work. The source-tag change from .021 is a prerequisite because v2 will run nightly once this TO ships and the silent-rewrite audit problem must be fixed first.</requirement>
    <requirement id="2">Do NOT modify v2's T1 logic, outlier cap, or aggregation semantics. The behavior of v2 is frozen per .021. This TO is strictly about WHERE and WHEN v2 runs, not WHAT it computes.</requirement>
    <requirement id="3">Do NOT modify `run-gold-layer.sh` in `infra/aws/ec2/bd-gold-layer-runner/`. That file is AE territory. Any required changes to the EC2 boot script go in the AE brief, not direct edits.</requirement>
    <requirement id="4">Do NOT modify terraform or add EventBridge rules directly. DS cannot touch `infra/aws/terraform/`. Document the required EventBridge rule in the AE brief with full parameters (rule name, schedule expression, target Lambda, tags).</requirement>
    <requirement id="5">Do NOT disable bd-price-update Job 1 in the Lambda. That is explicitly AE follow-up work, documented in the brief, sequenced for after the first week of parallel v2 + Lambda runs.</requirement>
    <requirement id="6">Do NOT trigger the gold runner, invoke any Lambda, or run v2 in production as part of this TO. Dry-run locally for verification, and hand off the first production run to Andrew or AE.</requirement>
    <requirement id="7">The freshness gate decision (criterion #4) MUST be documented explicitly in the session log with the chosen path and rationale. This is the most subtle correctness question in the TO — v2 must run even when no new allocations have landed, otherwise weekends never get filled.</requirement>
    <requirement id="8">If the script location decision (criterion #1) picks option (b) — v2 stays in silver/ and the boot script is updated to sync it — document the AE follow-up needed (AE must update run-gold-layer.sh:79 to add a silver sync line). If option (a) is picked (move v2 to gold/), no AE change is needed on the boot script.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Commit on CLOUD with gold_dispatch.sh changes, v2 move (if option a), deploy-to-ec2.sh comment cleanup, and the new AE brief file. `--author=0.4.0_DS_ClientPlatform`.</deliverable>
    <deliverable type="s3_upload">Updated gold_dispatch.sh and (if option a) relocated build_canonical_prices_v2.py uploaded to `s3://opal-data-bd/code/gold/`. Etag parity verified.</deliverable>
    <deliverable type="document">`docs/briefs/ae-brief-v2-prestep-integration.md` with EventBridge rule spec, IAM verification checklist, diff protocol for the first week, bd-price-update Job 1 deprecation plan, and rollback procedure.</deliverable>
    <deliverable type="document">Session log with the script location decision + rationale, the freshness gate decision + rationale, the local dry-run output, the commit SHA, the S3 etags, and the Compiler Tools section.</deliverable>
    <deliverable type="document">Next Steps block in session log naming AE 0.6.0 for: (a) new EventBridge rule, (b) IAM verification, (c) first-week diff protocol, (d) eventual bd-price-update Job 1 disable.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT start this TO until ADVI_GLDRST.021 is marked complete.</rule>
    <rule>Do NOT modify v2's T1 outlier cap, aggregation, or any pricing logic. Frozen per .021.</rule>
    <rule>Do NOT edit `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh` (AE territory). Document required changes in the AE brief.</rule>
    <rule>Do NOT edit `infra/aws/terraform/**` or add EventBridge rules. Document in the AE brief.</rule>
    <rule>Do NOT disable bd-price-update Job 1. Document in the AE brief as phase-2 follow-up.</rule>
    <rule>Do NOT trigger the gold runner in this TO. First production run is deferred to Andrew or AE post-brief.</rule>
    <rule>Do NOT skip the freshness gate decision documentation. v2 must run on no-new-data days for weekends to get filled; this is load-bearing and must be explicit.</rule>
    <rule>Do NOT invoke bd-price-update Lambda directly or manually. Let the existing schedule handle it during the parallel-run week.</rule>
  </do_not>
</task_order>
