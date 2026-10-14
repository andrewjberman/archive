# The 2026-10-14 07:00Z non-fire read of `astn-wsjft-3am-run` (carried from round 84; owner `2.0.0_SA_COO~W1`)

**Read (after 07:20Z on 2026-10-14), read only:**

```
.tools/aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations --dimensions Name=FunctionName,Value=astn-wsjft-orchestrator --start-time 2026-10-14T06:50:00Z --end-time 2026-10-14T07:20:00Z --period 1800 --statistics Sum --region us-east-1 --query 'Datapoints[].[Timestamp,Sum]' --output text
```

**Expected:** no datapoint (CloudWatch emits none for a Lambda that was not invoked). A datapoint with Sum 1.0 means the schedule fired and the disable did not hold.

**Positive control, read 2026-10-13 ~23:3xZ with the same command on the two previous mornings (schedule ENABLED then):**
- window 2026-10-13T06:50:00Z..07:20:00Z -> one datapoint, Sum 1.0 (timestamp 2026-10-13T02:50:00-04:00);
- window 2026-10-12T06:50:00Z..07:20:00Z -> one datapoint, Sum 1.0.
So the instrument sees a fire when there is one; an empty result for 2026-10-14 is a real non-fire and not a blind read.

**Also read with it:** `aws scheduler get-schedule --name astn-wsjft-3am-run --query State --output text` still reads `DISABLED`, and `aws ec2 describe-instances --instance-ids i-059405dfefcb4b44a --query "Reservations[].Instances[].State.Name" --output text` reads `stopped` (the 07:00Z fire used to launch it).

## RESULT (read 2026-10-14T11:42Z by 2.0.0_SA_COO~W1, the command above verbatim, rc 0)

- window 2026-10-14T06:50:00Z..07:20:00Z: NO datapoint (empty output). The schedule did not fire.
- positive control, same command, window 2026-10-13T06:50:00Z..07:20:00Z: `2026-10-13T02:50:00-04:00 1.0`. The instrument sees a fire when there is one.
- `scheduler get-schedule --name astn-wsjft-3am-run --query State`: `DISABLED`.
- `ec2 describe-instances --instance-ids i-059405dfefcb4b44a --query "Reservations[].Instances[].State.Name"`: `stopped`.
- Earlier read, same function, 06:30Z..08:00Z with 300 s periods: `Datapoints []`, control 10-10 to 10-13 one per day.

Owed read CLOSED. The round-84 packet's "What I did NOT verify" first line is answered: the 07:00Z fire did not run.
