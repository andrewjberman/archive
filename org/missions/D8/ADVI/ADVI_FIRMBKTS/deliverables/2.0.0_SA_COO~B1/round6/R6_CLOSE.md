# ADVI_FIRMBKTS -- round 6 close: one blind read of all 150, and the emit path's cause (2.0.0_SA_COO~B1, dell1, 2026-10-13 ~08:0xZ)

**Instrument:** `round6/checks/r6_fwd1.py`, `r6_checks.py`; each instance validated with `proof-of-spec-check.py --governing-order`.
`round-close-check.py --project ADVI_FIRMBKTS --round 6`: 2 orders, 2 complete, proofs 2 of 2, judgment 0, verdict **MAY-CLOSE**. Class: LOCAL read
and one WORLD read-only seat order; nothing served moved; no AWS write; no probe event was sent.

## The result

| order | cell | executor | result |
|---|---|---|---|
| `FB-i-1` | FWD-1: ONE blind read of all 150 canonical locations under the stated face | `~67` (worker-light; authored neither earlier read) | `r6_fwd1.py agree`: system, firm, tier and table each equal the key 150 of 150, all four 150 of 150, unknown 0. The reader's worktree: `LOCATIONS.json` alone, one commit, `OPENED: none`. Ingested `1f6b56fd09`; instance VALID. |
| `FB-i-2` | the exec-summary emit path read runner-side | `0.7.0_AE_CloudOps~FB1` | verdict **REGION_UNSET, `inferred`**; no probe sent. FB1's commit `dbb6841b6e`; instance VALID. |

### FWD-1, stated for the CVO

One reader that neither earlier read's author wrote answered all 150 under the stated face, and equals the key on every field. The
composite the CTO named (two reads under two faces) is now one read of all 150. **Residual, unchanged:** the reader is a subagent of the
issuing session on one model; independence is by construction of the tree (one parentless commit, `LOCATIONS.json` alone), not a seat
outside this session. The face states the table rule, so equality shows the rule is learnable and unambiguous on these 150; it does not
re-ratify the mapping's grain.

### The emit path (FB-i-2), stated

FB1's reads (17 read-verb calls): (1) the dispatcher's own cumulative log `logs/gold-layer/gold_incremental_*.log` carries 325 WARN lines since
2026-04-22 and 0 `EventBridge chain-complete emitted` lines on any date; no log holds the exception (the script runs
`aws events put-events ... 2>&1 | grep -q`, discarding the CLI text). (2) No region is set anywhere on the runner's boot path (CLI v1 from apt;
no `--region`, `AWS_DEFAULT_REGION`, `AWS_REGION` or `aws configure` in the script, the deployed object, `run-gold-layer.sh`, `setup-instance.sh`,
`user-data.sh` or the systemd unit; `bd-gold-trigger` sets only `GOLD_INSTANCE_ID`); the runner's own Python callers pass `region_name`
explicitly. (3) The role holds `events:PutEvents` and, for `BD/GoldRunner`, `cloudwatch:PutMetricData`. (4) **The control:** the same shell,
seconds after the WARN, runs `aws cloudfront create-invalidation` (a global service) and prints OK 4 of 4 chains, with 14 CloudTrail
CreateInvalidation events by the runner's session in 7 days; `SHUTDOWN_ARMED` prints 4 of 4 chains; `BD/GoldRunner` holds 0 metrics in 6
regions while `AWS/Lambda` holds metrics in each. So the CLI, the role credentials and the output handling work, and the failing calls are the
REGIONAL ones. (5) A request-parameter error is excluded for representative values by an offline botocore validation of the entries file.
**Inferred, not proved:** no line on the runner names the exception.

**What the fix touches, stated now so it is not discovered later.** The fix (FB1's proposal, not applied) is one line in the DS lane's
`gold_dispatch.sh`: a region for the dispatcher's CLI. Once the emit works, every chain close fires `exec-summary-generator`, which writes up to
158 client-facing summary keys twice a day (round-3 ADDENDUM 12), AND the `BD/GoldRunner` metrics start (the same fix). It is therefore a
served change under a never-widen pair, not a rider.

## Defects of the issuer in this round (named)

1. `FB-i-2`'s step 2 (the probe via SSM on the runner) collided with the runner's EC2_MANIFEST, which bars SSM commands on it (row `D1-S44`); I
   did not read that manifest before cutting the step. The probe was conditional and was not needed.
2. The order and round 5's diagnosis took "no CloudTrail PutEvents" as discriminating; FB1's row `D1-S44` records that it is not (the call
   never reached the API on this reading, and PutEvents's CloudTrail class was never controlled).
3. The `BD/GoldRunner` empty-namespace evidence was first read by me as a hypothesis (round 6 L5 fact 5); FB1 measured the control (the
   global call succeeds, the regional ones do not) that makes it inference rather than hypothesis.

## What the run does not show (stated, not graded)

- The exception text is in no record; REGION_UNSET is inferred from the absence of a region on every path and the global-versus-regional control.
- No live emit with a region set has been tried; the fix is untested on the runner.
- FWD-1's reader independence residual (above); the legacy arm is unchanged.

## What changed at the close

1. `FB-i-1` flipped complete (issuer); `FB-i-2` flipped complete by FB1 at `dbb6841b6e`. 2. `dep_stage` EXECUTING -> ROUND_CLOSE.

## What is open (owners)

| item | owner | condition |
|---|---|---|
| the emit fix (a region for the dispatcher's CLI) and the first regeneration of up to 158 summaries | round 7, under a never-widen pair (CTO + COO halves) | the CTO's round-6 analysis; a sample read first, prior VersionIds as rollback; `D1-W65-S1`'s disarm IS this cell |
| FB-h-5 / D1-S41: the validator's live non-admin read | `1.0.0_SA_CTO~DELL1` | the first organic non-admin validator line, or a non-admin session a seat holds |
| D1-S43 (the fence instrument's re-baseline) | NFRA_CTLPLN via MSTR | the owner |
| the BD pricing rules | `4.0.0_SA_CRO~DELL1` (a brief; Andrew confirms its DONE WHEN) | not FIRMBKTS's |
| c290 SEV1 publish; portal `ROUTER_FIRM_SUFFIX` PROD; the exec-summary regeneration sample | Andrew | his word |
| armed or blocking rows | the CVO | `D1-W65-S1`, `D1-W66-S2` (ARMED, disarm owner this seat), `D1-S41`, `D1-S42`, `D1-S44` |
