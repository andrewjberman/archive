<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFINGE.005b</id>
    <project>ADVI_INFINGE</project>
    <title>TXN migration to Lambda-native bronze pull via pull_inflection_transactions_v2.py (Phase 1b TO-5b; date-windowed Custom Reports; gates on TO-5a Class A empirical)</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>pending</status><!-- Flipped to pending 2026-05-06 (COO session 60): DS~A silver builder shipped (commit 33180d972, 20260506T151210Z). TO body updated per CTO Q-A/Q-B/Q-C rulings (paths + silver dim name + decom step). AE 0.6.1 GOed for Phase 0 Custom Reports rate-empirical + parity + orchestrator decom plan. CTO instruction: after all body edits + DS~A ship → GO. -->
    <priority>medium</priority>
    <estimated_effort>~30-60min AE post Phase 0 rate-empirical; pure clone+prefix substitute (no Phase 0 layer — pandas-pyarrow-requests-layer:1 already published); +Phase 0 Custom Reports rate-empirical ~30min</estimated_effort>
  </metadata>

  <references>
    <ref type="prd_canonical">docs/architecture/ADVI_INFINGE.md v0.2 (commit 050bd3695); §6.2 TO-5a → TO-5b conditional</ref>
    <ref type="cto_ruling">1.0.0_SA_CTO RULING 20260506T~1350Z — _v2.py canonical for Lambda-native TXN daily incremental. _rest.py deferred (inline local_dir + no date filter). Decision basis: pattern alignment TO-1..TO-3 + Lambda-fit economics + OOM risk on _rest.py.</ref>
    <ref type="txn_rate_empirical">ADVI_INFINGE.005 TO-5a COMPLETE — REST class: 5.2 RPS, Class A, 0 429s/503s. Custom Reports class NOT yet empirically tested — Phase 0 of this TO required before cron arms.</ref>
    <ref type="template_reference">TO-3 (ADVI_INFINGE.003) — Phase 1b Lambda module + Terraform pattern. TO-5b reuses with prefix substitution `positions` → `txn`. Layer pandas-pyarrow-requests-layer:1 already published (TO-2 Phase 0).</ref>
    <ref type="script_evidence">_v2.py:78 — LOCAL_PULLS_DIR = SCRIPT_DIR / "pulls" module-level constant (trivial /tmp patch, matches TO-1..TO-3 pattern). _v2.py:276,281 — --start-date / --end-date argparse args. _v2.py:182 — post_generate(jwt, start_date, end_date) with explicit @StartDate/@EndDate POST body params. Date-windowed daily incremental confirmed.</ref>
  </references>

  <context>
    `pull_inflection_transactions_v2.py` (Custom Reports endpoint) produces daily-incremental TXN data.
    Unlike `pull_inflection_transactions.py` (REST, full-history per run), _v2.py accepts --start-date/--end-date
    argparse arguments, enabling a bounded single-day window per Lambda invocation.

    Key advantages over _rest.py path (per CTO ruling):
    - Module-level LOCAL_PULLS_DIR (_v2.py:78) = trivial /tmp patch, no DS refactor needed.
    - Date-windowed payload = stable memory footprint regardless of account history growth.
    - Pattern consistency with TO-1..TO-3 = no structural deviation.

    Bronze output paths (verify against actual script output during Phase 0):
    - `bronze/orion-api/{date}/transactions.csv` (REPLACE pattern per CTO Q-A ruling — same key as orchestrator wrote; CSV per Custom Reports endpoint; orchestrator transactions DimSpec decommissioned at Lambda cutover)

    Silver convert outputs:
    - `silver/api_dims/transactions/{date}/data.parquet` (no _v2 suffix per CTO Q-B ruling)

    EventBridge cron: `cron(0 13 * * ? *)` = 13:00 UTC.
    Cron stagger position: REPS@12:30 → ASSETS_V2@12:45 → POSITIONS@12:50 → PERFORMANCE@12:55 → TXN@13:00.

    Lambda config: 1024MB / 900s (date-windowed payload bounded; profile at 80% headroom; scale up only on empirical demand).

    Naming (consistent with Phase 1b family):
    - Lambda function: `inf-api-txn`
    - EventBridge rule: `inf-api-txn-rule`
    - IAM execution role: `inf-api-txn-role`

    **CRITICAL — Phase 0 empirical required before cron arms:**
    TO-5a empirical was measured on the REST class endpoint. Custom Reports is a different endpoint
    family. Cron MUST NOT be armed until Phase 0 Custom Reports rate-empirical confirms 2+ RPS sustainable
    + zero failures OR CTO grants exception.
  </context>

  <phase id="0" when="before Phase 1 implementation — Custom Reports rate-empirical (required by CTO ruling)">
    <step>
      <run>Verify orchestrator transactions DimSpec decommission plan (REPLACE pattern per CTO Q-A ruling).
      The REPLACE pattern means: Lambda and orchestrator write the SAME bronze key
      (bronze/orion-api/{date}/transactions.csv). When Lambda goes live, orchestrator DimSpec
      for transactions must be decommissioned (disabled/removed) to avoid both writing the same key
      (last-write-wins race). Document: (a) current orchestrator DimSpec for transactions
      (pull_inflection_transactions.py or pull_inflection_transactions_v2.py?), (b) proposed cutover
      sequencing (Lambda armed before DimSpec decom? Or decom first?). Propose to COO in RAVC3.
      Follow same cutover pattern as TO-1/2/3 (ASSETS_V2, REPS, POSITIONS).
      </run>
      <expect>Clear decom plan documented before Lambda is armed. No racing writes to same bronze key.</expect>
      <if_mismatch>If orchestrator DimSpec unclear: ask AE 0.7 or DS~B for context on current transactions dim behavior in orchestrator.</if_mismatch>
    </step>
    <step>
      <run>Run pull_inflection_transactions_v2.py locally or on inf-bronze-runner EC2 with single-day window (--start-date YYYY-MM-DD --end-date YYYY-MM-DD; pick a recent date with known transaction activity). Measure: wall time, peak memory, API call count, observed RPS, 429/503 count.</run>
      <expect>Empirical numbers for Custom Reports endpoint. Target: 2+ RPS sustainable, 0 429s/503s. Wall target &lt;600s (within 900s Lambda timeout with headroom for /tmp patch overhead).</expect>
      <if_mismatch>If 429s exceed 5% of calls OR wall &gt;700s: surface to CTO before arming cron. May require smaller window, reduced concurrency, or defer to orchestrator path.</if_mismatch>
    </step>
    <step>
      <run>Row-set parity check: identify which gold script reads silver/api_dims/transactions_v2/ (or silver/api_dims/transactions/). Verify that Custom Reports endpoint returns equivalent row-set to current gold consumer's expectation (i.e., raw transaction rows not aggregated). Document the gold-script anchor and row count vs known daily transaction volume.</run>
      <expect>Parity confirmed: Custom Reports returns per-transaction rows equivalent to what gold consumers expect. Row count in expected range.</expect>
      <if_mismatch>If Custom Reports returns aggregated/transformed row-set vs raw transactions: HARD BLOCKER — surface to CTO + DS lane. _rest.py path-2 fallback activates per CTO ruling (LOW-priority deferred standalone TO). Do NOT proceed to Phase 1 until parity confirmed.</if_mismatch>
    </step>
    <step>
      <run>RAVC3 Phase 0: report empirical rate + parity outcome to COO. If 2+ RPS + zero failures + parity confirmed: COO sends Phase 1 GO. If marginal: COO routes to CTO. Include: wall time, memory peak, RPS, 429 count, parity status, gold-script anchor citation.</run>
      <expect>Phase 0 RAVC3 closes with clear GO/HOLD decision from COO.</expect>
      <if_mismatch>If results ambiguous (variable RPS across days): rerun 3x across different date windows; report distribution before RAVC3.</if_mismatch>
    </step>
  </phase>

  <phase id="1" when="after Phase 0 RAVC3 + COO GO — implementation; clone TO-3 module + prefix substitute">
    <step>
      <run>Verify inf-pipeline latest tag before beginning. `git tag -l "inf-pipeline-v*" | sort -V | tail -5`. Pick next semver patch.</run>
      <expect>Current latest tag visible; next patch identified.</expect>
      <if_mismatch>Per CLAUDE.md tag versioning rule — do NOT assume next version.</if_mismatch>
    </step>
    <step>
      <run>Clone `infra/aws/lambda/inf-pipeline/inf-api-positions/` → `infra/aws/lambda/inf-pipeline/inf-api-txn/`. Edit lambda_function.py to invoke pull_inflection_transactions_v2.py with daily single-day window args (--start-date {date} --end-date {date} derived from invocation context) + convert_orion_api_to_silver.py (--dim transactions). Apply /tmp patch on LOCAL_PULLS_DIR (_v2.py:78: SCRIPT_DIR / "pulls" → /tmp/pulls). Reference `pandas-pyarrow-requests-layer:1`.</run>
      <expect>Lambda handler invokes _v2.py with bounded single-day window; /tmp patch applied; sys.path co-location for rate_limiter + jwt_freshness; JWT fail-fast; NO lambda:InvokeFunction. Zip ~50-100KB.</expect>
      <if_mismatch>Pattern divergence from TO-3: document in commit message; CTO consult if material.</if_mismatch>
    </step>
    <step>
      <run>Clone `infra/aws/terraform/inf-pipeline/inf-api-positions.tf` → `infra/aws/terraform/inf-pipeline/inf-api-txn.tf`. Substitute prefix. IAM scope: bronze/orion-api/* PutObject + silver/api_dims/transactions/* PutObject + secretsmanager + s3:GetObject JWT. EventBridge cron `cron(0 13 * * ? *)` (13:00 UTC). Lambda memory_size 1024 (NOT 3072 default — date-windowed payload bounded). timeout 900.</run>
      <expect>9 resources to add; 0 destroys; clean plan. memory_size=1024 explicit in TF resource.</expect>
      <if_mismatch>If TO-3 pattern needs deviation for _v2.py Custom Reports invocation style: surface before terraform apply.</if_mismatch>
    </step>
    <step>
      <run>Update lambda-source-map.json with inf-api-txn entry.</run>
      <expect>New entry; CI drift detection picks it up.</expect>
      <if_mismatch>Per CLAUDE.md rule 4.</if_mismatch>
    </step>
    <step>
      <run>SILVER_BUILDERS extension on inf-silver-chain — add `transactions` if absent (verify; DS~A authoring build_transactions_dim() in convert_orion_api_to_silver.py per INFINGE.005b-silver TO). Gate Phase 0 empirical on DS~A RAVC3 confirming `transactions` registered. Document finding.</run>
      <expect>If present after DS~A ships: no edit, document. If absent: flag to DS~A before Phase 0 empirical. Crossref: `# AC6: ADVI_INFINGE.005b TO-5b — transactions silver-chain extension`.</expect>
      <if_mismatch>Per TO-3 Phase 2 pattern.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before terraform apply">
    <step>
      <run>terraform plan + comp-iam gaps + .tools/safe-commit.sh</run>
      <expect>Clean plan + 0 IAM gaps + safe-commit PASS</expect>
      <if_mismatch>Per TO-3 Phase 3 if_mismatch pattern.</if_mismatch>
    </step>
  </phase>

  <phase id="3" when="terraform apply + tag">
    <step>
      <run>terraform apply + 0-diff verify + tag bump + Lambda invoke empirical test (single-day window; manual fire with --start-date / --end-date OR wait for natural cron at 13:00 UTC tomorrow).</run>
      <expect>bronze/orion-api-v2/{date}/transactions_v2.json + silver/api_dims/transactions_v2/{date}/data.parquet written. Row count in range from Phase 0 parity baseline.</expect>
      <if_mismatch>If row count diverges from Phase 0 parity baseline: DO NOT close; loop back to DS lane for schema investigation.</if_mismatch>
    </step>
  </phase>

  <cross_domain_coordination>
    <coord>**Phase 0 gates everything.** No Phase 1 authoring until Phase 0 Custom Reports rate-empirical + parity RAVC3 + COO GO. CTO ruling is conditional: _v2.py default, _rest.py fallback only if Phase 0 surfaces hard blocker.</coord>
    <coord>**Cron stagger ordering:** REPS@12:30 → ASSETS_V2@12:45 → POSITIONS@12:50 → PERFORMANCE@12:55 → TXN@13:00 UTC. TXN fires last.</coord>
    <coord>**TO-4 PERFORMANCE deferred independently.** TO-5b does NOT unblock TO-4. They share the same _rest.py DS-lane issue for PERFORMANCE but TO-5b specifically targets _v2.py for TXN — different scripts.</coord>
    <coord>**INFREL TO-5 (transactions_v2).** Per PRD §7 OQ4: INFREL TO-5 scopes the silver-chain dim Lambda migration for transactions_v2. INFINGE TO-5b supplies the bronze Lambda; INFREL TO-5 handles silver-chain wiring. Coordinate TO completion sequence.</coord>
    <coord>**_rest.py fallback path:** If Phase 0 parity or rate surfaces hard blocker, COO routes to LOW-priority deferred TO covering _rest.py DS local_dir refactor + 4096MB Lambda. Do NOT author that TO unless Phase 0 fails.</coord>
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="0" when="before empirical">comp-pipescript io pull_inflection_transactions_v2.py — verify bronze/silver output contract; identify gold script reading silver/transactions_v2 for parity anchor.</phase>
    <phase id="1" when="before writing implementation">comp-iam service inf-api-txn + comp-pipescript io pull_inflection_transactions_v2.py — confirm IAM scope vs S3 write paths.</phase>
    <phase id="2" when="before commit">comp-iam gaps + ds-commit-gate.sh (lambda_function.py) + safe-commit.sh</phase>
    <phase id="3" when="after deploy">comp-iam gaps clean post terraform apply; 24h empirical at 13:00 UTC tomorrow.</phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Phase 0 Custom Reports rate-empirical: 2+ RPS sustainable + 0 429s/503s on single-day window run. Empirical numbers documented (wall, memory, RPS, 429 count).</criterion>
    <criterion id="AC2">Phase 0 parity check: gold-script anchor cited + row-set equivalence confirmed vs current consumer expectation.</criterion>
    <criterion id="AC3">Fresh `bronze/orion-api-v2/{D+1}/transactions_v2.json` + `silver/api_dims/transactions_v2/{D+1}/data.parquet` by 13:05 UTC daily.</criterion>
    <criterion id="AC4">CW Metric `Opal/InflectionIngestion/TxnPulled` increments daily.</criterion>
    <criterion id="AC5">CW Alarm fires on 2 consecutive failures.</criterion>
    <criterion id="AC6">comp-iam gaps clean post terraform apply.</criterion>
    <criterion id="AC7">Tag bumped + pushed (inf-pipeline-v1.7.X). Lambda memory_size=1024 confirmed in 0-diff terraform verify.</criterion>
    <criterion id="AC8">RAVC5 close package: Phase 0 empirical evidence + commit hash + apply 0-diff + tag bump + Lambda invoke empirical evidence + comp-iam gaps clean + parity row count.</criterion>
  </acceptance_criteria>

  <go_signal>
    <issued_at>20260506T~1515Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. DS~A silver builder shipped (33180d972). TO body updated per CTO Q-A/Q-B/Q-C. Execute Phase 0: (1) orchestrator DimSpec decom plan, (2) Custom Reports rate-empirical single-day window, (3) row-set parity check, (4) RAVC3 Phase 0 to COO. If Phase 0 Class A + parity confirmed: COO issues Phase 1 GO. If Phase 0 fails: COO routes to CTO for fallback ruling.</message>
  </go_signal>
</task_order>
