# REPORT -- MDPF_HEALGAP.TO-HG-d3, the one real run of FWD-1

**Seat:** `0.7.0_AE_CloudOps~F` (laptop) | **Issuer:** `2.0.0_SA_COO~G1` | **Exercise date D:** 2026-10-08
**Window:** this session 10:38Z-13:1xZ; the order's acts span 2026-10-07T17:36Z to 2026-10-08T13:01Z across TWO `~F` sessions.

## Headline

**FWD-1 is REALIZED for D = 2026-10-08.** The morning Cottonwood Rebalancer pull was made to fail on a lapsed
vendor login, and the day's figures were in place by 11:46:08Z **with nobody acting**. All three criteria PASS,
both never-widen conditions 2 and 3 are MET, condition 4 is MET, and branch (B) was never triggered.

**This session made ZERO AWS writes.** Its only AWS calls were reads plus one read-only `terraform plan`.

## 1. The ledger entry

`org/critical_paths/change_management/20261007T1736Z_mdpf-healgap-hg-d3-fwd1-exercise-20261008_deploy_completion.md`
(sentinel `org/critical_paths/.open_deploys/mdpf-healgap-hg-d3-fwd1-exercise-20261008.json`, now removed at CLOSE).
Opened 2026-10-07T17:36:20Z with 5 legs and a 24h window; **CLOSED with 5 of 5 legs proven**.

| leg | what | state |
|---|---|---|
| L1 | the arm (`put-targets` setting `induce`) | CLOSED 2026-10-07T17:43:08Z by the prior `~F` session |
| L2 | the restore + `HG1-d3-AC3` | CLOSED, **AMENDMENT 2** (the actor question; see section 2) |
| L3 | the targeted plan, condition 3 | CLOSED |
| L4 | `HG1-d3-AC1` + `HG1-d3-AC2` | CLOSED |
| L5 | condition 4, the 13:30Z line | CLOSED, **MET** |

## 2. Both put-targets read-backs

**Act 1, the ARM** -- made by the PRIOR `~F` session of 2026-10-07, proven in leg L1:

```
PRE:  2026-10-07T17:38:11Z  {"Id":"cot-rebalancer-runner-daily","Arn":"...:function:cot-rebalancer-runner","Input":"{\"mode\":\"pull\"}"}
                            length(Targets)=1  State=ENABLED  cron(0 6 * * ? *)
PUT:  2026-10-07T17:40:36Z  {"FailedEntryCount": 0, "FailedEntries": []}
POST: 2026-10-07T17:41:52Z  same Id, same Arn, Input {"mode":"pull","induce":"auth-lapse"}  length(Targets)=1
SEP:  cot-bronze-complete -> CotSilverOnBronzeComplete {"mode":"silver-run"} ; cot-rebalancer-runner-reattempt {"mode":"pull"}  (UNTOUCHED)
```

**Act 2, the RESTORE -- in window, but NOT made by this seat and NOT attributed to any seat.** The overnight `~F`
session was killed for laptop memory (CTO msg 106633, 2026-10-07T23:40Z) and this session registered at 10:38Z, so
owner (1) of CTO ruling 106485 never acted. Measured from CloudTrail (`lookup-events EventName=PutTargets
--start-time 2026-10-07T17:00:00Z`), **exactly two** `PutTargets` exist on this rule in the window and no others:

```
ARM      2026-10-07T17:40:39Z  input {"mode":"pull","induce":"auth-lapse"}   failedEntryCount 0
RESTORE  2026-10-08T06:08:46Z  input {"mode":"pull"}                         failedEntryCount 0
         both: same target id cot-rebalancer-runner-daily, same Arn, user/Andrew_Berman, 108.242.96.89
READ-BACK (this seat) 2026-10-08T10:48:14Z: one target, Id cot-rebalancer-runner-daily, Arn unchanged, Input {"mode":"pull"}
```

06:08:46Z is inside the order's 06:05Z-06:20Z window, so **condition 2 is MET**. Who acted is NOT claimed:
`2.0.0_SA_COO~G1` read `NOOP-ALREADY-RESTORED` at 06:10:09Z, `1.0.0_SA_CTO` read it restored at 06:14:12Z and made no
put on this rule at any time, and nine of nine registered laptop seats answered not-this-seat (CTO msg 106896). Row
`MDPF_HEALGAP-D1-S3` carries it.

**What this seat added to that open question -- the TOOL, not the actor.** `D1-S3` recorded the call's user agent as
`aws-cli/1.44.44 Python 3.12.10 Windows 10.0.26100`, with dell1 on `aws-cli 2.37.9` as `cloudops-dell1-agent-user`.
This laptop's own shim reads **byte-identical on all three fields**:

```
.tools/aws --version   ->  aws-cli/1.44.44 Python/3.12.10 Windows/10.0.26100 awscrt/0.31.3 botocore/1.43.0
python                 ->  platform.release() 10.0.26100 while platform.version() 10.0.26200   (explains the build oddity)
```

So the put was made with **this laptop's aws v1 shim, not from dell1**. The actor is still unattributed; the
operator's own terminal remains INFERRED, not measured, and the question is with Andrew.

## 3. The three checks' output

Graded 2026-10-08T13:00:42Z-13:00:46Z, inside the order's own read gate (after 13:00Z on D):

```
HG1-d3-AC1  FAILED-OK induced lines=3 bronze keys before 11:00Z=0 date=2026-10-08
HG1-d3-AC2  HEALED-OK date=2026-10-08 stamp_at=2026-10-08T11:32:25+00:00 keys={"rebalancer_models": 1, "rebalancer_accounts": 5, "rebalancer_model_detail": 93}
HG1-d3-AC3  RESTORED-OK daily target input={"mode":"pull"}
```

**The induced failure, read directly from `/aws/lambda/cot-rebalancer-runner`.** One 06:00Z fire, THREE attempts
under the single RequestId `346eaa7d-c480-4c25-9716-6ae2408f2c53` (the `retry=2` HG-d1 set) at 06:00:42Z, 06:01:49Z
and 06:03:46Z, each ending:

```
[ERROR] RuntimeError: BD GET /auth/token -> HTTP 401: INDUCED auth-lapse (MDPF_HEALGAP FWD-1 exercise; no secret read, no vendor call)
  File "/var/task/lambda_function.py", line 485, in lambda_handler
```

raised **before** any secret read or vendor call. Nothing was written.

**The heal, with nobody acting.** EventBridge rule `cot-bronze-complete` fired its HG-d2 re-attempt target at
11:32:06Z. RequestId `21eb2c0c-ea27-485c-9e4a-8f4639d51f08`, Duration 17832.30 ms -- a **real vendor pull**, not a
skip:

```
WARN: count-reconcile mismatch on 1 of 54 strategy(ies) -- CARRIED, not fatal: [{"strategy": "Core | Satellite 60", "roster": 12, "observed": 11}]
{"verdict": "BRONZE-COMPLETE", "as_of": "2026-10-08", "models": 71, "accounts": 992, "model_details": 93,
 "gates": {"pagination_integrity": "PASS", "count_reconcile": "DISCLOSED-MISMATCH", "strategies_checked": 54, ...}}
```

That WARN is the runner's own `DISCLOSED-MISMATCH` gate working as built -- recorded so it is not later mistaken for
a defect of the heal. The complete-stamp did not exist at this seat's 11:31Z read (`HeadObject` 404) and existed at
11:32:25Z (ETag `9a5ae9fcf186b4c5c13545a23540a00b`, 11909 B), so the heal's output was observed crossing from absent
to present with no seat acting.

**Condition 3, the targeted plan** -- 11:06:16Z-11:06:23Z, `CHECKPOINT_DISABLE=1`, `MSYS_NO_PATHCONV` unset,
terraform v1.15.8 on PATH (`.tools/terraform.exe` does not exist on this laptop):

```
aws_cloudwatch_event_target.cot_rebalancer_runner_daily: Refreshing state... [id=cot-rebalancer-runner-daily-cot-rebalancer-runner-daily]
No changes. Your infrastructure matches the configuration.
```

The config declares `input = jsonencode({ mode = "pull" })` (`cot_rebalancer_runner.tf:179`), equal to the live
input, so the out-of-band `put-targets` **pair** left zero drift.

**Condition 4 (act 4b): MET.** On the instrument the condition names -- the newest silver/gold write for D *under the
existing `on_success` chain* -- the newest write is **2026-10-08T11:46:08Z**, and the four model silver tables landed
at 11:32:29Z-11:32:33Z, 4 to 8 seconds after the bronze stamp. MET by 1h43m on the newest write, 1h57m on the model
tables. **Gold is not on that chain** and had zero objects for D at the 13:01:58Z read: it is written by
`data/assets/scripts/gold/build_dim_model_portfolio.py` from the EC2 `mdpf-daily-runner`
(`infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:554`), while the runner's `on_success` destination is
`opal-assets-silver-blackdiamond`. Gold's last ten partitions landed at 13:30:39Z-13:30:42Z on nine of ten days, so
it arrives just after the condition's line **every day, healed or not** -- filed as row `MDPF_HEALGAP-S11`, not
treated here as a condition-4 failure.

**The negative arm.** The same two checks against 2026-10-07, a normal day, on the same plane:

```
--failed 2026-10-07  ->  FAILED-BAD no INDUCED auth-lapse line in the runner log 2026-10-07 06:00-06:30Z        (rc=1)
--healed 2026-10-07  ->  HEALED-BAD stamp LastModified 2026-10-07T06:00:58+00:00 outside 2026-10-07 11:00Z-23:59Z (rc=1)
```

Neither criterion is a tautology: each separates the induced-and-healed day from a normal one on its own, and the
pair separates the two halves of the outcome.

## 4. Branch (B)

**NOT TAKEN.** Branch (B) applies only if `HG1-d3-AC2` reads BAD after 18:00Z; AC2 read `HEALED-OK` at 11:49Z and
again at 13:00:44Z. No remedial invoke was made, the order's one-invoke budget is unspent, and FWD-1 grades REALIZED
rather than NOT realized.

## 5. Proof instance

`org/missions/D8/MDPF/MDPF_HEALGAP/deliverables/0.7.0_AE_CloudOps~F/MDPF_HEALGAP.TO-HG-d3.fwd1-exercise-induced-morning-failure.proof_of_spec.json`

`python .tools/proof-of-spec-check.py <instance> HG1-d3-AC1,HG1-d3-AC2,HG1-d3-AC3 --governing-order <order>` ->
**VALID (rc=0)**, violations 0, acceptance rows 3, coverage 3/3, `invocation-alignment` 3/3, alignment ENFORCE clean
(forward-1 3/3, forward-2 2/2, backward 2/2), `surprises-frame` 2 entries both resolving to channel rows. A positive
control was run first against the known-good HG-d2 instance (`VALID (rc=0)`), so a failure here would have been this
instance's and not the checker's.

## 6. Rows

- **`MDPF_HEALGAP-D1-S3`** (existing, `2.0.0_SA_COO~G1`, OBSERVATION / INERT) -- the unattributed 06:08:46Z restore.
  **Not re-filed**; this seat contributed the user-agent measurement in section 2 to its open identification question.
- **`MDPF_HEALGAP-S11`** (new, this seat, OBSERVATION / INERT, `UNDER_INVESTIGATION`) -- condition 4's 13:30Z line
  sits 39-42 seconds inside gold's own daily arrival, so a condition-4 read widened to gold returns MISSED on nine of
  the last ten days with no failure present. Owner for the successor wording: `2.0.0_SA_COO~G1`.

## 7. What is NOT this seat's, and is owed elsewhere

1. **`2.0.0_SA_COO~G1`** -- the reader's page read of the Cottonwood models for D. `HG1-d3-AC3`'s own text assigns it
   ("the reader's page read is the issuer's at close"); this seat did not substitute an S3 read for it.
2. **`2.0.0_SA_COO~G1`** -- AC3 of both HG-d2 halves (a normal day's ~11:32Z fire reading `SKIP-IDEMPOTENT`). It
   cannot be read on D, because on 2026-10-08 that fire was the HEAL. Earliest read: 2026-10-09.
3. **`2.0.0_SA_COO~G1`** -- row `MDPF_HEALGAP-S11`'s successor wording for condition 4, and the two rows owed from
   HG-d2 (`SURPRISE_ROWS_OWED_FROM_TO_HG_D2_20261007.md`).
4. **`2.0.0_SA_COO~G1`** -- the `<status>` flip of this order is self-marked `complete` here; `superseded`/`cancelled`
   would be the issuer's.

## 8. Commits and push state

The two acts of 2026-10-07 and the entry's opening ride `f2cce52172` (**on origin/CLOUD**, ancestry read). The d2
artifacts `1ad97815f3`, `a536d4b391` and `04f05c1e31` are all **on origin/CLOUD** -- `0.0.0_AB_MSTR` drained branch
`wk-healgap-d2`, so the prior session's next-step 3 is discharged. This session's close commit carries the ledger
close, this report, the proof instance, row `S11` and the `<status>` flip; it is committed in the SHARED tree by exact
pathspec, because the live sentinel is there and other seats' entries and sentinels were modified in the same tree
throughout (hazard `MDPF_HEALGAP-S6`). A Tier-2 seat does not push a shared branch: the commit's push state is
measured with `git ls-remote` and stated in the message that delivers this report.

-- `0.7.0_AE_CloudOps~F`, 2026-10-08
