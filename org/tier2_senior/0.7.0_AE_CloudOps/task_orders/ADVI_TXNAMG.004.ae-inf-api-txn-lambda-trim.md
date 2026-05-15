<task_order>
  <metadata>
    <id>ADVI_TXNAMG.004</id>
    <slug>ae-inf-api-txn-lambda-trim</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-15</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>HELD until ADVI_TXNAMG.003 (TO-3, the amalgamating writer) ships and is RAVC2-validated. SEQUENCING INVARIANT (PRD §3): TO-4 removes writer #3's silver-write — it must land BEFORE OR SAME-WAVE AS TO-3, NEVER before. The consolidation must never produce a zero-writer window. COO releases this dispatch_held on TO-3's RAVC2 receipt; coordinate the same-wave deploy with DS~D. RELEASED 2026-05-15 by COO — ADVI_TXNAMG.003 (TO-3) RAVC2 received + COO-validated (commit 10de8e67f; the amalgamating writer is shipped + deployed-to-S3, AC1-4/6 PASS, AC5 substantively proven against prod S3; the live in-EC2 chain-run that materializes the amalgamated artifact is THIS TO-3/TO-4 deploy wave). TO-4 is GO. Coordinate the same-wave deploy directly with DS~D: TO-4's Lambda silver-write removal lands together with the runner-start chain-run that materializes TO-3's amalgamated silver — no zero-writer window, no writer-#3 clobber of the amalgamated output.</dispatch_unblock_condition>
    <project_code>ADVI_TXNAMG</project_code>
    <priority>P1 — removes the second live writer of silver/transactions/, completing the single-writer invariant.</priority>
    <sla>~3-4h wall post-unblock.</sla>
    <reassignment>PRD §6 TO-4 names receiver AE 0.6.1 (owns inf-api-txn / LAMBDA-DIMS). Andrew directed 2026-05-15: AE 0.6.1 is committed to the Eclipse pipeline and cannot take TXNAMG — TO-4 reassigned to 0.7.0_AE_CloudOps. AE 0.6.1's read-only prep is captured below so AE 0.7.0 inherits it.</reassignment>
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_TXNAMG.md (PRD v0.1, commit e7fecbf93) — §3 architecture + sequencing invariant, §4.3 component spec, §6 TO-4, §7-Q2.</prd>
    <ae_prep>AE 0.6.1 read-only prep (MCP, 2026-05-15): edit sites are lambda_function.py:92-108 (Step 2 silver-write — REMOVE) and :114-121 (Step 3 sentinel body — REVISE). silver/api_dims/transactions/ is a dead 005b-spec path (never materialized) — irrelevant to this trim. The aggregator-quorum reads silver/_silver_complete/{date}/transactions.json — 9-dim quorum, the sentinel must keep firing.</ae_prep>
    <source_map>infra/aws/lambda/ci/lambda-source-map.json — inf-api-txn entry (current inf-pipeline-v1.7.60).</source_map>
  </references>

  <context>
    silver/transactions/{date}.parquet has two live daily writers (PRD §2): writer #2 = the gold-chain REST convert_transactions_to_silver.py (06:00 UTC), writer #3 = the inf-api-txn Lambda's Custom-Report silver-write (13:00 UTC). TO-3 makes writer #2 the sole canonical AMALGAMATING writer (REST spine + Custom-Report-unique columns left-joined by txn id). This TO removes writer #3's silver-write — the last step to one-writer. The inf-api-txn Lambda is TRIMMED, NOT retired: its Custom-Report bronze pull stays (it is now TO-3's join enrichment source) and its aggregator-quorum sentinel stays.
  </context>

  <objective>
    The inf-api-txn Lambda produces only the Custom-Report transaction bronze CSV + the aggregator-quorum sentinel. Its silver/transactions/ write is gone. Exactly one writer of silver/transactions/ remains (the gold chain).
  </objective>

  <scope>
    <item>infra/aws/lambda/inf-pipeline/inf-api-txn/lambda_function.py — REMOVE step 2 (the convert_orion_api_to_silver.build_transactions silver-write, ~lines 92-108). This kills writer #3.</item>
    <item>KEEP step 1 — pull_inflection_transactions_v2 → bronze/orion-api/{T-1}/transactions.csv. This is now TO-3's join enrichment source; it must continue unchanged.</item>
    <item>KEEP step 3 — the sentinel silver/_silver_complete/{T-1}/transactions.json. The LAMBDA-DIMS aggregator quorum (9 dims incl transactions) keys on sentinel presence + status — it MUST keep firing or the quorum stalls 8/9 and the gold chain never triggers.</item>
    <item>REVISE the sentinel body (~lines 114-121) — do NOT keep it verbatim. It currently builds from Step-2 artifacts (`rows` = len(txn_df); `silver_key`) which vanish when Step 2 is removed. Revise: `rows` → bronze row count or dropped; `silver_key` → the bronze key or dropped (the sentinel now means "txn bronze done", not "txn silver done"); `status` / `snapshot_date` / `lambda` / `completed_at` carry over. The aggregator keys on sentinel presence + status, so body-field changes are quorum-safe.</item>
    <item>Deploy via Terraform per CLAUDE.md Rule 1 — terraform apply, NOT aws lambda update-function-code. Update the lambda-source-map.json entry. Tag inf-pipeline-v1.7.6x after 0-diff apply. Current inf-pipeline-v1.7.60.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">silver/transactions/ written by EXACTLY ONE writer — verified empirically by S3 LastModified: no ~13:00-UTC writes appear after the trim deploys (only the gold chain's ~06:00 write).</ac>
    <ac id="AC2">bronze/orion-api/{date}/transactions.csv is STILL produced daily by the trimmed Lambda (step 1 intact) — TO-3's enrichment source is unbroken.</ac>
    <ac id="AC3">The sentinel silver/_silver_complete/{date}/transactions.json STILL fires daily with a valid status — the 9-dim aggregator quorum is undisturbed; the gold chain still triggers. Verify the aggregator quorum completes post-deploy.</ac>
    <ac id="AC4">Sentinel body revised (not verbatim) — no reference to removed Step-2 `rows`/`silver_key` artifacts; emission code does not error on the removed step.</ac>
    <ac id="AC5">Deployed via terraform apply to 0-diff; lambda-source-map.json updated; git tag inf-pipeline-v1.7.6x; pushed --follow-tags. No emoji in Lambda code/logs.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 (before writing): comp-iam service inf-api-txn (confirm IAM surface — removing the silver-write only REDUCES the s3:PutObject surface; no new grant). Phase 2 (before commit): comp-iam gaps IF iam.tf changed. Phase 3 (after deploy): deployed-verify; empirically confirm no ~13:00-UTC silver/transactions/ write; confirm the aggregator quorum still fires. Copy verbatim per PRD §6.</compiler_tools_mandate>

  <cross_domain_coordination>
    GATED BY TO-3 (ADVI_TXNAMG.003, DS~D — the amalgamating writer). SEQUENCING INVARIANT (PRD §3): land TO-4 BEFORE OR SAME-WAVE AS TO-3 ship — NEVER before. Removing writer #3 before writer #2 amalgamates would leave silver/transactions/ schema-incomplete. Coordinate the deploy wave directly with DS~D on TO-3's RAVC2.
    INFETL coordination: inf-api-txn + the 9-dim aggregator-quorum sentinel are ADVI_INFETL LAMBDA-DIMS territory. This trim leaves the bronze pull + sentinel intact by design (PRD §4.3 / §7-Q2 — sentinel stays on the Lambda, meaning shifts to "txn bronze done", no relocation, no circular-dependency). No INFETL re-architecture.
    SEPARATE — orion-gold-dispatch.sh is NOT touched by this TO (TO-4 edits lambda_function.py only). The concurrent AE-lane edits to orion-gold-dispatch.sh (Eclipse wiring 81b53ab97 + the Andrew-priority Eclipse-decouple) are a DIFFERENT file — no collision with TO-4.
  </cross_domain_coordination>

  <deliverables>
    <item>Trimmed inf-api-txn lambda_function.py — committed, terraform-applied to 0-diff, source-map updated, tagged inf-pipeline-v1.7.6x, pushed --follow-tags.</item>
    <item>Empirical post-deploy evidence: no 13:00-UTC silver write; bronze CSV still produced; aggregator quorum fires.</item>
    <item>Session log + RAVC2 to COO + CC CTO + DS~D.</item>
  </deliverables>

  <ravc>AE 0.7.0 RAVC2 to COO + CC CTO + DS~D on AC1-5 PASS. Coordinate the deploy wave with DS~D (TO-3) per the §3 sequencing invariant before landing.</ravc>

  <notes>
    Reassigned from AE 0.6.1 to AE 0.7.0 per Andrew (AE 0.6.1 is on the Eclipse pipeline this session). AE 0.6.1's read-only prep (the :92-108 / :114-121 edit sites, the dead api_dims/transactions path, the quorum dependency) is in the references block — you inherit it, no need to re-derive. PRD §4.3 is the authoritative spec; the line numbers are AE 0.6.1's prep estimate — verify against the current file. The Custom-Report bronze pull MUST survive the trim — TO-3's amalgamating writer depends on it; removing it would break the consolidation. If anything about the inf-api-txn / LAMBDA-DIMS architecture is unclear, AE 0.6.1 has the deepest context — MCP them; do not guess.
  </notes>
</task_order>
