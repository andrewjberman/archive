# ADVI_FIRMBKTS round 6 -- L5 ground truth (2.0.0_SA_COO~B1, dell1, 2026-10-13 ~08:0xZ)

Claims: M = measured by this seat now, H = held (a cited record).

| # | fact | claim | source |
|---|---|---|---|
| 1 | The round-5 analysis (msg 4693) names 2 items and 1 carried item; the CVO's slug msg 4691 and `REMEDIATION_v6.md` @02e2a330df graded FWD-1 PARTIAL (a composite of two reads under two faces), FWD-4 PARTIAL. | H | `ledger/ROUND_ANALYSIS.round5.md` |
| 2 | The canonical arm of round 4's list is 150 locations; the readers' round-4 face carried no table-component sentence, round 5's does. Reader authors so far: `~27`, `~28` (round 4), `~61`, `~62` (round 5); `~67` authors neither. | M | `round4/READING_KEY.json`, orders `FB-g-4`, `FB-g-5`, `FB-h-1`, `FB-h-2` |
| 3 | `gold_dispatch.sh` has NO `--region`, NO `AWS_DEFAULT_REGION`, NO `AWS_REGION` and NO `aws configure` (native grep of the file, 0 matches). The emit is `aws events put-events --entries file://... 2>&1 \| grep -q '"FailedEntryCount": 0'` at line 850; its stderr is merged into the test and discarded. | M | `data/black_diamond/scripts/gold/gold_dispatch.sh` |
| 4 | The dispatcher's other regional calls swallow their errors (`>/dev/null 2>&1 \|\| true`): `cloudwatch put-metric-data --namespace BD/GoldRunner` (lines 1346, 1598, 1604), `ec2 describe-tags` (1584). | M | same file |
| 5 | `cloudwatch list-metrics --namespace BD/GoldRunner` returns 0 metrics in us-east-1, us-east-2, us-west-1, us-west-2, eu-west-1 and eu-central-1 (list-metrics holds the last two weeks); the control `AWS/Lambda` `Invocations` returns metrics. | M | `.tools/aws cloudwatch list-metrics`, 06:5xZ-07:5xZ |
| 6 | The estate's own runner code says: a runner's CLI/boto3 has no region unless one is set; it does NOT fall back to IMDS. | M | `infra/aws/ec2/estate-report-runner/estate_report_runner.py:188` |
| 7 | The SSM document the 49F trigger sends (`advi-49f-chain-dispatch`) belongs to the 49F chain (`chain_49f_entrypoint.py`); it sets no region and does not run `gold_dispatch.sh`. The gold dispatcher's launcher (`bd-gold-trigger`) is not read yet. | M | `lambda get-function-configuration advi-49f-gold-dispatch`, `ssm get-document` |
| 8 | CloudTrail holds no PutEvents in 17 regions over 90 days; the rule, bus, Lambda policy and role grant read correct (`FB-h-6`); the runners `bd-gold-layer-runner` and `bd-gold-qa-runner` are stopped between chains (launched 04:00:47Z, stopped). | H | `round5/R5_CLOSE.md`; `0.9.0_WK_ADVI_FIRMBKTS~65/EXEC_SUMMARY_DIAGNOSIS.json` |
| 9 | The CTO's word authorizes exactly ONE non-matching `PutEvents` from the dispatcher's own identity, and only if the read is still indeterminate. | H | `ROUND_ANALYSIS.round5.md` section 2 |
| 10 | The reader worktree `C:/dev/wk-firmbkts-r6-reader`: one parentless commit `80ff50f2f576`, `LOCATIONS.json` alone, sha256 `84afab43...6e8`, 150 locations. | M | `r6_fwd1.py build` output |

## Base dry-runs

| order | criterion | base |
|---|---|---|
| FB-i-1 | AC1 reader | FAIL as expected (0 of 4; 4 of 4 on a full fixture answers file; 3 of 4 with one extra file) |
| FB-i-2 | AC1 runner record | FAIL as expected (absent; a probe call not recorded in `test_event` FAIL; a planted `s3 rm` FAIL; good fixtures with and without the one probe PASS) |
