# FB-i-2 -- the runner-side read of the exec-summary emit path (0.7.0_AE_CloudOps~FB1, 2026-10-13T07:47:33Z)

**Verdict: `REGION_UNSET`, claim `inferred`. The probe was NOT sent.**

## What the logs hold
- The dispatcher's `gold/logs/` holds 578 objects (575 `.log`); the newest 10 `chain_full_*.log` carry no emit line (0 WARN, 0 emitted). The
  emit's WARN is in the runner's cumulative log `logs/gold-layer/gold_incremental_*.log`: 325 WARN lines from 2026-04-22, 0 "emitted" lines on any
  date. Four chain closes read in full context (2026-10-12 02:27Z and 06:10Z, 2026-10-13 01:12Z and 06:14Z): the WARN is preceded by the
  `perf_report` merge lines and followed by the `CDNCOHT post-chain invalidation` header. No exception text is anywhere near it: the call is
  `aws events put-events ... 2>&1 | grep -q '"FailedEntryCount": 0'`, so the CLI's own output is discarded.

## The emit path
- Client: AWS CLI v1 from the Ubuntu apt package (`setup-instance.sh` line 19). Credentials: the instance profile `bd-exporter-profile`
  (role `bd-exporter-ec2-role`, which holds `events:PutEvents` on the default bus). Launcher: `bd-gold-trigger` starts the instance; the
  systemd unit runs `run-gold-layer.sh` (S3 copy equals the repo's), which runs `run_gold_layer.sh` and the dispatcher. No SSM document.
- Region: none set anywhere on that path (no `--region`, `AWS_DEFAULT_REGION`, `AWS_REGION` or `aws configure`). The runner's python callers
  pass `region_name='us-east-1'` themselves (`A_00.accounts_dimension.py:596`).

## The controls
- The same shell, seconds after the WARN, runs `aws cloudfront create-invalidation` (global service) and prints `CDNCOHT invalidation OK` 4 of
  4 chains; CloudTrail shows 14 `CreateInvalidation` events by the runner's session in 7 days. CLI, credentials and output handling work.
- `BD/GoldRunner` holds 0 metrics in 6 regions, and IAM does allow that namespace (`GldRunnerMetrics`): a regional CLI call failing silently,
  not a permission. The `Opal/DataQuality` AccessDenied in the same log is a different namespace the policy does not list.
- CloudTrail has 0 `PutEvents` events from any principal in 7 days, so its silence is not by itself a discriminator.

## What is not proved
No line names the exception. A parameter error is excluded only offline (botocore validation of a representative entries file). One
non-matching `PutEvents` from the runner would prove or refute the region cause. It was not sent: the runner is stopped (next chain 23:00Z),
and `infra/aws/ec2/EC2_MANIFEST.json` carries `_access_policy` "EVENTBRIDGE ONLY. No agent, no human, no SSM command may start, stop, or
run commands on this instance" for `bd-gold-layer-runner`, which the order's step 2 (an SSM command) contradicts; the CTO's word and that
standing policy need reconciling before any probe.

## The fix (NOT applied)
`export AWS_DEFAULT_REGION=us-east-1` (or `--region`) at the top of `data/black_diamond/scripts/gold/gold_dispatch.sh`, the DS lane's file,
under its own never-widen pair: once the emit works, every chain close fires `exec-summary-generator` (up to 158 summary keys, twice a day).
