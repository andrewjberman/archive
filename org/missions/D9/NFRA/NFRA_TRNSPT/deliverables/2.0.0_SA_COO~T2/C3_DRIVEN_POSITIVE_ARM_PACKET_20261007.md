# Packet -- C3: the driven positive arm of FWD-7 (one scheduled fire reaching 2026-08-11), NFRA_TRNSPT round 4

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author and operator:** `2.0.0_SA_COO~T2` (dell2), 2026-10-07 ~15:5xZ.
**Authority:** CTO round-3 analysis `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_NFRA_TRNSPT_ROUND_3_20261007.md`
@c2b5eb89a4 section 4 item C3; decomposition `decompositions/NFRA_TRNSPT_DECOMP_R4.md` cell TR-p-4. **COO half: SIGNED below.**
No vendor call, no alarm, no SNS, no SES, no grant, no `aws_lambda_permission`, no new resource.

## 1. What ships (two applies, one function)

| | value |
|---|---|
| code | CLOUD `8f82af6281` (contains chain A, merged at `6598c4cf6b`: `mail_handler.py` WINDOW_DAYS 1..120 listed as spans of <=31 days; one counts-only `MAIL-PULL-FIRE` line per fire). LOCAL |
| package | `build.sh` in a CLEAN detached worktree at `8f82af6281` (`C:/dev/wk-trnspt-c3`): 48 members, 478,258 bytes, CodeSha256 `VGIq85Xxm5KVLCnv16BASS63RsPMHScMEwZJP5SuMNY=` (deployed today: `teStghgdPZn8urHt8+IzpRM1HqZLiae6QN0LHvNwT3c=`, 41 members, 2026-10-02T04:01Z) |
| deployed layout (rule 103374) | the zip extracted alone: `mail_handler` imports from it; it carries `1..120` and `MAIL-PULL-FIRE`; `address()` resolves `s3://opal-data-transcripts/outlook/transcripts/state/pull_runs/run=X/run.json` (the key the five scheduled fires already wrote); `criterion.load_tables()` reads `assets+registry`, 2 authors. `r2_bundle_import_check.py` BUNDLE-IMPORT-OK files=48 |
| suite | branch 244 passed / 0 failed / 5 collection errors that exist on the shared tree before round 4 (row NFRA_TRNSPT-S15, owner 4.0.0_SA_CRO); the 5 new round-4 tests pass |
| APPLY 1 (plan read 2026-10-07 ~15:4xZ from dell2, `-target=aws_lambda_function.mail_pull`) | **0 to add, 1 to change, 0 to destroy**: `source_code_hash` teSt... -> VGIq...; `environment.variables.WINDOW_DAYS` "7" -> "60"; 2 other env values and 27 attributes unchanged. The apply re-plans; no saved plan is applied |
| APPLY 2 (after the graded fire) | `WINDOW_DAYS` "60" -> "7" in `mail_pull.tf`, same target; code unchanged |
| why 60 | the next scheduled fire is 2026-10-07T23:30Z; 2026-08-11 is 57 days before it; 60 covers the whole of that day with 3 days' margin. Under the 120 cap |

## 2. Blast radius, by branch

**Writers of the named property.** `WINDOW_DAYS` on `outlook-global-transcripts-pull-lambda`: 1 writer, Terraform from
`infra/aws/terraform/transcripts/mail_pull.tf` (N=1, read). The function's writes are unchanged in kind from round 3's packet
(`deliverables/2.0.0_SA_COO~D/MAIL_PULL_SCHEDULE_PACKET_20261002.md` section 2): bronze under `outlook/transcripts/bronze/analysis_commentary/`
has 2 writers, both `pull.run`; silver `.../silver/analysis_commentary/date=<d>/` has 2 writers, both `silver.build`; run records 1
writer per run id. The function's IAM policy is unchanged (prefix `outlook/transcripts/*` only).

**What the fire may touch.** Every message a table sender sent in the 60 days before the fire that the criterion ADMITS and whose
sidecar is not in bronze. The rule is `pull.run(..., admitted_only=True)`: a near miss writes nothing; an admitted message writes its
bronze objects (4 for a message with one PDF, measured round 3) under a NEW key named by its `internetMessageId`, never overwriting
a different sidecar (refused). Measured today: 0 `outlook` bronze objects written since 2026-10-02 (24 `outlook` objects in total,
key census from dell2), so no admitted message in the window is in bronze except the 2026-07-06 one, which is outside 60 days.
Named candidates in the window from the round-2 record: 2026-08-11 (Manav, the target) and 2026-09-02 (Yang). The fire may land
both; that is the rule's output, not a widening.

| branch | what the fire writes | rollback per key |
|---|---|---|
| lands the 2026-08-11 message (and any other admitted message in the window) | per message its bronze objects under new keys; per landed date ONE new silver parquet `date=<d>`; `run.json`, `silver.json` | delete the new bronze keys and the new `date=<d>` silver keys, each listed by key from dell2 (`list-objects-v2`, keys and LastModified only; no read). Nothing existing is overwritten, so nothing is restored |
| lands nothing (listing returns no admitted row, or every row a near miss) | `run.json`, `silver.json` only. The fire line reads `landed=0`; then the criterion is listed as the cause to read (laptop fenced read of `run.json` counts) | none needed |
| listing refused for every sender | `GatewayToolsAbsent` raises; nothing written; the error is in the log | none needed |
| the 2026-08-11 message is already in bronze | NOT A BRANCH: 0 `outlook` bronze objects since 10-02, and the analysis measured it outside bronze |

**Rollback of the apply.** APPLY 2 is the rollback of the env value. The code rolls back by re-applying at `e3707e911f`'s
build (`teSt...`); C1 and C2 are additive (a wider accepted range, one stdout line), so a 7-day fire on the new code behaves as
today plus one log line.

## 3. Sequence and grading

1. Ledger entry opened in `org/critical_paths/change_management/` (legs: L1 apply-1, L2 verify config, L3 the scheduled fire,
   L4 apply-2, L5 verify config + next fire's line) before APPLY 1.
2. APPLY 1 via `.tools/safe-apply.sh` from the clean worktree, `-target=aws_lambda_function.mail_pull`, re-planned at apply; then
   `get-function-configuration` reads CodeSha256 `VGIq...` and `WINDOW_DAYS` 60.
3. The 2026-10-07T23:30Z SCHEDULED fire. Grade: (1) its `MAIL-PULL-FIRE` line reads `landed>=1`, and its invocation is EventBridge's
   (no manual invoke in the window; CloudWatch `Invocations` = 1 for the hour); (2) a laptop FILE via the fenced-read path
   (analysis section 3): bronze hashes equal the sidecar's, silver `held_out` state, counts only; (3) APPLY 2, then the 2026-10-08
   23:30Z fire's line reads `window_days=7`.
4. Ledger closed when every leg carries its proof.

**Which machine applies:** dell2. The change is the function's code and one environment value; it writes no Lambda permission, no
policy, no grant. `terraform plan` from dell2 read state and every resource in the target's graph without refusal.

## COO half -- SIGNED

`2.0.0_SA_COO~T2`, 2026-10-07: SIGNED for the blast radius above, both branches, one key (the function's `WINDOW_DAYS`, plus its
code at `8f82af6281`), rollback `WINDOW_DAYS=7` and the code at `teSt...`.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
