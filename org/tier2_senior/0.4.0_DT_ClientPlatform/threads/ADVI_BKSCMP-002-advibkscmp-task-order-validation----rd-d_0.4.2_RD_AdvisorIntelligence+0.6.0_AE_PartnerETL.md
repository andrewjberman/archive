# Thread Receipt: ADVI_BKSCMP task order validation -- RD, DT, AE verify alignment (no-tools, facts pre-injected)

**Thread ID:** ADVI_BKSCMP-002-advibkscmp-task-order-validation----rd-d
**Project Serial:** ADVI_BKSCMP-002
**Created by:** 2.0.0_SA_COO
**Created at:** 2026-03-19T14:36:58Z
**Status:** complete
**Participants:** 0.4.2_RD_AdvisorIntelligence, 0.4.0_DT_ClientPlatform, 0.6.0_AE_PartnerETL

---
## 000.md

---
agent: 2.0.0_SA_COO
turn: 0
timestamp: 2026-03-19T14:36:52Z
signal: continue
---

## ADVI_BKSCMP Task Order Validation — RD, DT, AE

DS completed validation in ADVI_BKSCMP-001 (one real discrepancy found and corrected:
_OPAL_ETF_OVERRIDES sources from silver scripts, not 06b). This thread covers RD, DT, AE.

All source file facts you need are pre-injected in the CONTEXT section above.
**Do not call any tools.** Everything is already there. Read the pre-injected facts,
check them against your task order requirements, and report CONFIRMED or DISCREPANCY.

## Per-agent checklist

### 0.4.2_RD_AdvisorIntelligence (task order ADVI_BKSCMP.002)

Using ONLY the pre-injected facts for RD:

1. Verify req 1 (types.ts changes): confirm MixItem does NOT currently have top_holdings
   or other, and BooksCompositionResponse scope does NOT have advisor_id or firm_id.
   Check the pre-injected current interface state.

2. Verify req 2 (holdings block lines 875-884): confirm the pre-injected block matches
   what the task order says to replace. Any line-number or code-content discrepancy?

3. Verify req 3 (Other render blocks lines 1039-1068): confirm showFilteredOther block
   at 1039-1054 and showOther block at 1055-1068 match what the task order describes
   replacing.

4. Verify req 4 (empty state line 1073): confirm the current condition uses
   allItems.length === 0 and the task order's replacement condition is structurally correct.

5. Flag anything in the task order code that does not match the pre-injected current state.

### 0.4.0_DT_ClientPlatform (task order ADVI_BKSCMP.003)

Using ONLY the pre-injected facts for DT:

1. Verify req 1 (gate): confirm opal-partners-data entry exists in lambda-source-map.json
   and has artifact_sha256 and tf_resource fields (which req 3 updates after upload).

2. Verify req 6 (tag): confirm partners-api-v1.4.0 is the current latest tag.
   Confirm partners-api-v1.5.0 is the correct next tag.

3. Verify req 5 (record-terraform-deploy.sh): confirm the script path cited in the
   task order (infra/aws/lambda/ci/record-terraform-deploy.sh) is consistent with
   the source map directory structure.

4. Flag any command, path, or resource name in the task order that conflicts with
   the pre-injected facts.

### 0.6.0_AE_PartnerETL (task order ADVI_BKSCMP.004)

Using ONLY the pre-injected facts for AE:

1. Verify req 4 (run command): confirm './run_gold_layer.sh --incremental' is the
   correct invocation based on the script's mode parsing.

2. Verify req 2 (upload paths): confirm the S3 paths for script 12
   (s3://opal-data-bd/code/gold/) and run_gold_layer.sh (s3://opal-data-bd/code/)
   are consistent with the S3_BUCKET variable and the sync behavior described.

3. Verify req 3 (EC2 pull): confirm run_gold_layer.sh must be pulled separately
   (not auto-synced) and the pull command in req 3 is correct.

4. Verify req 6 (EC2_MANIFEST registration): confirm bd-gold-layer-runner entry
   exists and the format for updating it is consistent with the pre-injected entry.

5. Flag any path, bucket name, or command that conflicts with the pre-injected facts.

## Output format

  CONFIRMED [req N]: one-line description of what matches
  DISCREPANCY [req N]: what the task order says vs what the pre-injected facts show

Signal converge when done. This is your only turn.



---

## 001.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 1
timestamp: 2026-03-19T14:37:32Z
signal: converge
---

## ADVI_BKSCMP.002 Task Order Validation — RD

Validating against pre-injected facts only. No tool calls.

---

### Req 1 — types.ts changes (WS3a)

**CONFIRMED [req 1A]:** MixItem (lines 1265-1270) does NOT currently have `top_holdings` or `other`. Current fields are `asset_class`, `label`, `market_value`, `pct` only. Task order adds both as optional at the end of the interface — structurally correct.

**CONFIRMED [req 1B]:** BooksCompositionResponse scope (lines 1280-1291) does NOT currently have `advisor_id` or `firm_id`. Scope only has `relationship_id?` and `account_id?`. Task order adds both as optional — structurally correct.

**CONFIRMED [req 1B continued]:** BooksCompositionResponse does NOT currently have root-level `top_holdings` or `other`. Task order adds both as optional after `concentration` — structurally correct.

**CONFIRMED [req 1 — ConcentrationItem]:** Task order states ConcentrationItem is unchanged. Pre-injected facts confirm ConcentrationItem (lines 1272-1278) has `key`, `label`, `asset_class`, `market_value`, `pct` — no changes required or specified.

---

### Req 2 — Holdings derivation block lines 875-884 (WS3b)

**CONFIRMED [req 2]:** Pre-injected current block (lines 875-884) exactly matches what the task order says to replace:

```
const allItems = composition?.concentration.items ?? []
const filteredItems = selectedAssetClass
  ? allItems.filter(it => it.asset_class === selectedAssetClass)
  : allItems
const MAX_ITEMS = 9
const cappedItems = filteredItems.slice(0, MAX_ITEMS)
const showOther = !selectedAssetClass && composition && composition.concentration.other.pct > 0
const showFilteredOther = Boolean(selectedAssetClass && filteredItems.length > MAX_ITEMS)
const maxPct = cappedItems.length > 0 ? cappedItems[0].pct : 1
```

Task order replacement introduces `hasPreAggregated`, schema-adaptive `cappedItems` IIFE, `otherEntry` IIFE, and simplified `showOther = otherEntry !== null && otherEntry.pct > 0`. All variables referenced in the replacement (`composition`, `selectedAssetClass`) are in scope at that location per the context note that `ConsolidatedOverviewPanel` starts around line 860.

**NOTE on XML entity encoding:** The task order XML uses `&amp;&amp;` for `&&` in the code blocks. These are XML-escaped and decode correctly to `&&` in the actual TypeScript. No discrepancy — standard XML encoding.

---

### Req 3 — Other render blocks lines 1039-1068 (WS3b-render-other)

**CONFIRMED [req 3 — showFilteredOther block]:** Pre-injected facts confirm `showFilteredOther` render block at lines 1039-1054 exists and uses `filteredItems.slice(MAX_ITEMS).reduce` for pct. Task order removes this block entirely.

**CONFIRMED [req 3 — showOther block]:** Pre-injected facts confirm `showOther` render block at lines 1055-1068 exists and uses `composition.concentration.other.pct`. Task order replaces both blocks with a single unified `{showOther && otherEntry && (...)}` block using `otherEntry.pct`.

**CONFIRMED [req 3 — unified block]:** The replacement block uses `otherEntry.pct` (not `composition.concentration.other.pct`), which is correct given the schema-adaptive `otherEntry` computed in req 2. The `maxPct` reference in the bar width calculation is still valid — `maxPct` is computed in the same derivation block (req 2 replacement).

**NOTE on XML entity encoding in render block:** The JSX in the task order uses `&lt;` and `&gt;` for `<` and `>`. These decode correctly. No discrepancy.

---

### Req 4 — Empty state line 1073 (WS3b-empty-state)

**CONFIRMED [req 4]:** Pre-injected facts confirm the current empty state condition at line 1073 uses `allItems.length === 0 ? 'No holdings data at this level'`. Task order replaces `allItems.length === 0` with `!hasPreAggregated && composition.concentration.items.length === 0`.

**CONFIRMED [req 4 — logic correctness]:** The replacement is structurally sound. When `hasPreAggregated` is true (N1/L2 schema), the condition short-circuits to false, preventing the "No holdings data" message from appearing when `cappedItems` is empty due to a missing asset class selection rather than absent data. The `composition` non-null guard is satisfied at this point in the render (the outer condition already checks `!composition` for the loading state).

---

### Req 5 — Commit (WS commit)

**CONFIRMED [req 5]:** Commit format matches RD protocol: `--author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>"`. Commit message uses `feat(portal):` prefix with no emojis. Both files (`types.ts` + `ClientsTab.tsx`) committed together as specified.

**CONFIRMED [req 5 — no-gate constraint]:** Task order dependency is `agent="none" status="clear"`. The adapter is backward-compatible — when new Lambda routes return 404, `fetchComposition` falls through to synthesis, `composition` will be null or use the L3/L4 schema, and `hasPreAggregated` will be false. No DS/DT/AE gate required before committing.

---

### Summary

All 5 requirements and all 11 acceptance criteria are consistent with the pre-injected source facts. No discrepancies found.

**Scope constraint confirmed:** Only `portal/src/pages/AdvisorIntelligence/types.ts` and `portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx` are touched. The constraint to leave `handleSelectAdvisor`, `fetchComposition`, `synthesizeFrom*`, and all other ConsolidatedOverviewPanel logic (donut, legend, quarterly bar) unmodified is achievable given the pre-injected line numbers — the derivation block and render blocks are isolated sections.

**Ready to execute.** No blockers. Will commit to portal DEV immediately and report SHA to COO.

---

## 002.md

---
agent: 0.4.0_DT_ClientPlatform
turn: 2
timestamp: 2026-03-19T14:39:41Z
signal: converge
---

## ADVI_BKSCMP.003 Task Order Validation — DT

Validating against pre-injected facts only. No tool calls.

---

### Req 1 — Gate: opal-partners-data entry in lambda-source-map.json

**CONFIRMED [req 1]:** The pre-injected lambda-source-map.json entry for `opal-partners-data` exists and contains both required fields:
- `artifact_sha256`: `z3hy2abK6/Ks5049Mbu6yWvwGq9FY6Kz1hl6Her08Jc=` (current value; req 3 updates this after upload)
- `tf_resource`: `module.opal_partners_data.aws_lambda_function.this`

The entry also confirms:
- `source_dir`: `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data`
- `artifact_s3_key`: `partners-api/opal-partners-data.zip`
- `last_deployed_at`: `2026-03-18T16:13:50Z`

The gate check in req 1 (`git log --oneline -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`) is the correct path per the source map's `source_dir`. No discrepancy.

---

### Req 6 — Tag: partners-api-v1.5.0 is the correct next tag

**CONFIRMED [req 6]:** Pre-injected CHANGELOG.json confirms latest deployed version is `partners-api-v1.4.0`. The recent deployment tags list confirms the sequence: `partners-api-v1.4.0`, `partners-api-v1.3.0`, `partners-api-v1.2.0`, `partners-api-v1.1.0`, `partners-api-v1.0.1`, `partners-api-v1.0.0`.

**CONFIRMED [req 6 — next tag]:** `partners-api-v1.5.0` is the correct next minor bump (two new routes + cache-control helper = minor, not patch). The task order's verification command (`git tag -l "partners-api-v*" | sort -V | tail -5`) will show `partners-api-v1.4.0` as the latest, confirming `v1.5.0` is correct.

**CONFIRMED [req 6 — tag command]:** The task order uses `git push --follow-tags` (not `git push origin CLOUD --follow-tags`). This is a minor variation from the standard DT deploy sequence which specifies `git push origin CLOUD --follow-tags`. Both are functionally equivalent if the current branch is CLOUD and the remote is origin. Not a discrepancy, but worth noting for execution: use `git push origin CLOUD --follow-tags` per standard protocol.

---

### Req 5 — record-terraform-deploy.sh path

**CONFIRMED [req 5]:** The task order cites `bash infra/aws/lambda/ci/record-terraform-deploy.sh partners-api partners-api-v1.5.0`. The pre-injected facts confirm `record-terraform-deploy.sh` is present at `infra/aws/lambda/ci/record-terraform-deploy.sh`. This matches the path used in the partners-api-v1.1.0 deploy session log (`record-terraform-deploy.sh` called from that same path, producing `3bc778de`). No discrepancy.

**CONFIRMED [req 5 — CHANGELOG.json location]:** The record-deploy script writes to `infra/aws/terraform/partners-api/CHANGELOG.json` (confirmed from the v1.1.0 deploy log). The task order's commit for this step (`ci: record deploy partners-api @ (commit) [skip ci]`) matches the pattern used in prior deploys.

---

### Req 2 — Build artifact: PowerShell workaround

**CONFIRMED [req 2]:** Task order specifies using the PowerShell temp script pattern (`C:/Windows/Temp/build-partners-data.ps1`) because `build-and-upload.sh` is broken on this machine (bun MSYS2 path issue). This is consistent with the partners-api-v1.1.0 deploy session log which notes the same workaround was used. Upload target `s3://opal-313476888478-lambda-artifacts/partners-api/opal-partners-data.zip` matches the `artifact_s3_key` in the source map (`partners-api/opal-partners-data.zip` in the lambda-artifacts bucket). No discrepancy.

**NOTE:** The task order upload path uses `s3://opal-313476888478-lambda-artifacts/` (the Lambda artifacts bucket), not `s3://opal-313476888478-lambda-layers/` (the layers bucket). This is correct — Lambda function zips go to the artifacts bucket, not the layers bucket.

---

### Req 4 — Terraform plan/apply

**CONFIRMED [req 4]:** Task order expects `1 to change` (opal-partners-data in-place: `s3_object_version + source_code_hash`). This matches the pattern from the v1.1.0 deploy (`terraform plan: 1 changed (s3_object_version + source_code_hash update)`, `terraform apply: 0 added, 1 changed, 0 destroyed`). The partners-api Terraform module is at `infra/aws/terraform/partners-api/` — confirmed present from the source map `tf_file` field.

**CONFIRMED [req 4 — MSYS_NO_PATHCONV]:** Task order constraint includes `Export MSYS_NO_PATHCONV=1 before AWS CLI commands with ARN or S3 paths`. This is consistent with DT standard protocol. The Terraform apply itself uses `.tools/terraform.exe -chdir=infra/aws/terraform/partners-api` per DT deploy sequence.

---

### Req 7 — deployment_map.xml update

**CONFIRMED [req 7]:** Task order requires updating `deployment_map.xml` with `partners-api-v1.5.0`. The partners-api module was added to `deployment_map.xml` at commit `585bcaf9` (per DT recent commits: "update deployment_map.xml -- add partners-api module + opal-partners-data Lambda"). The entry exists and needs only the version bump. No discrepancy.

---

### Req 8 — Spot-verify new routes

**CONFIRMED [req 8]:** Task order expects `GET /api/scoped/partners/books/firm/all/composition?firmId=49financial` to return `503` (not `404` or `500`) before S3 artifacts exist. This is the correct expected behavior: the new route handler exists in v2.8 Lambda code, finds no artifact at the S3 key, and returns 503 (service unavailable / artifact not ready) rather than 404 (route not found) or 500 (unhandled exception). This is a code-level behavior expectation, not verifiable from pre-injected facts, but the logic is sound.

---

### Summary

All 8 requirements are consistent with the pre-injected source facts. No discrepancies found.

**One execution note (not a discrepancy):** Req 6 uses `git push --follow-tags` while DT standard protocol specifies `git push origin CLOUD --follow-tags`. Will use the explicit form at execution time.

**Dependency gate is clear:** DS must commit Lambda v2.8 to CLOUD before build. The gate check (`git log --oneline -- infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`) targets the correct source path per the source map.

**Ready to execute** once DS reports the v2.8 commit SHA. No blockers on DT side.

---
