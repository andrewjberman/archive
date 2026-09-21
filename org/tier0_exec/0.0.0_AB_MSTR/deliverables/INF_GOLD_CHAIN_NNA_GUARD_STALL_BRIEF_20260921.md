# BRIEF -- Inflection (INF) gold chain stalled since 2026-09-06 on the NNA coverage guard

**Author:** 0.0.0_AB_MSTR, 2026-09-21 ~16:50Z, at Andrew's request ("write a brief on the Inflection Issue,
I will hand it off to a designated agent to remediate").
**Status:** diagnosis only. Nothing has been changed. The remediating agent is named by Andrew.
**Vintage:** every live read below was taken 2026-09-21 between 15:05Z and 16:45Z. Repo citations are at
HEAD `dd96141e4f`; the guard and excusal file were last changed at `8ba56144ec`.

---

## 1. The problem in one paragraph

The INF full gold chain on the EC2 `inf-gold-layer-runner` (`i-0ed5afded2ebd4ed4`) has hard-failed
**every day from 2026-09-06 through 2026-09-21 (16 of 16 runs)** at step 33 of 65,
`INF_C_01.canonical_nna`. Its data-integrity guard refuses to rewrite the 2026-09-04 NNA partition without
two accounts that were in it before. Because the chain stops there, the 32 later steps and both portal
publishers never run. **Every file the portal serves for the Inflection tenant is frozen at the 2026-09-05
run (data as of 2026-09-04).** Each failure fires the `inf-gold-chain-failed` alarm, and that is the email
and text noise Andrew is receiving.

## 2. The exact refusal (identical on 09-06, 09-13 and 09-21 -- three logs read)

```
ERROR: I_C01 failed: NNA PARTITION COVERAGE REGRESSION -- 2 account(s) carrying $0.00 of SERVED NNA
are about to be DROPPED from partitions that are being REWRITTEN.
    A VENDOR ROSTER IS A STATEMENT ABOUT TODAY. IT MUST NOT REWRITE THE PAST.
      account    351: $     120,000.00  dropped from 1 partition(s), e.g. ['2026-09-04']
      account   1206: $    -120,000.00  dropped from 1 partition(s), e.g. ['2026-09-04']
    If an account SHOULD lose its history, that is a DECISION: record it in
    lib/nna_coverage_excusals.json with a reason and who decided. Do not disable this guard.
nna_coverage_guard.NNACoverageRegression  (nna_coverage_guard.py:320, raised from INF_C_01.canonical_nna.py:918)
```

- Log: `s3://opal-data-inf/diagnostic/chain_logs/chain_full_20260921_113302.log`, lines 36700-36722.
  Same accounts and partition in `chain_full_20260906_113239.log` and `chain_full_20260913_113301.log`.
- Failure marker: `s3://opal-data-inf/gold/meta/pipeline-failed.json` ->
  `{"chain":"full","run_date":"2026-09-21","failed_at":"2026-09-21T12:35:37Z","exit_code":1,...}`
- Last success marker: `gold/meta/pipeline-complete.json`, LastModified **2026-09-05 12:52:20 GMT**.

**Reading of the numbers (inference, not measured):** +$120,000 into account 351 and -$120,000 out of
account 1206 on 2026-09-04 nets to $0, which looks like one internal transfer between two accounts. The
2026-09-05 run wrote it into the 09-04 partition. From 09-06 on, the vendor feed no longer produces those
rows for that date, so every rebuild would silently delete them. The guard exists to stop exactly that.
**Nobody has yet looked at the source data to confirm why the rows disappeared. That is the first job.**

## 3. Blast radius, measured

- **Chain:** 32 of 65 steps succeed daily (API pulls, silver, INF_A_*, INF_B_*, INF_C_00). Fails at
  INF_C_01. Never run since 09-05: INF_C_01b through INF_D_11 (32 steps).
  Source: `s3://opal-data-inf/telemetry/inf-gold-layer-runner/status.json`, run
  `chain_full_20260921_113344`.
- **Served portal data frozen.** All 29 top-level files under `s3://opal-data-inf/platinum/firm/` were
  last written 2026-09-05 12:46-12:50Z. That includes header_metrics, leaderboard, timeseries_*,
  partner_analytics_*, cumulative_chart, clients_tab, fee_efficiency, mix_summary, dashboard and
  advisor_nna_canonical. `header_metrics.json` says `"generated_at": "2026-09-05T12:49:01Z"` and
  `"data_as_of": "2026-09-04"`. Per-advisor `platinum/advisors/*/summary.json` were also last written
  2026-09-05.
- **Publishers idle.** `inf-portal-publisher` and `inf-portal-advisor-publisher` fire only on the
  `pipeline-complete.json` write. Their last log events were 2026-09-05 12:52Z and 12:53Z.
- **No alternate feed found.** The portal reads Inflection from `opal-data-inf` (router suffix `inf`,
  `portal/src/api/endpoints/advisor-intelligence.ts`). No Lambda in `infra/aws/lambda/` refers to
  `opal-data-inflection`, the LGIC full-name bucket. That bucket's own policy explicitly denies the
  Andrew IAM users, so its contents were not inspected (see also msg 99087 from `0.7.0_AE_CloudOps~V`).
  `opal-data-portal-v2/platinum/advi/` holds only 49financial.
  ⚠ Andrew believes Inflection ADVI still updates daily. That is **not reconciled**. Section 6 has the
  open question.

## 4. The alert noise, and why it is working correctly

- Alarm `inf-gold-chain-failed` (`infra/aws/terraform/inf-pipeline/alarms.tf:93`): metric
  `Inflection/GoldChain.ChainFailed`, period 3600, 1 evaluation period, missing data treated as not
  breaching. It is emitted by `fatal_alert()` in `data/inf/scripts/gold/orion-gold-dispatch.sh:168`.
- Daily metric counts: 1 per day from 09-06 through 09-21, and 0 from 08-12 through 09-05. Each day it
  goes to ALARM at ~12:36Z and back to OK at ~15:36Z.
- Actions (both ALARM and OK) go to two topics:
  `opal-infrastructure-alerts` -> SMS, and `opal-partner-etl-ops-alerts` -> SMS plus
  `partner-etl-ops-queue` -> `partner-etl-ops-sqs-consumer` -> **SES email**.
  So each day produces **2 emails and 4 texts**.
- ⛔ **Do not mute the alarm.** It is the only thing surfacing a 16-day freeze of partner-facing data.
  It goes quiet by itself on the first run that completes.

## 5. Remediation -- the decision is the work, and it is not the remediator's to make alone

The guard names two legitimate outcomes. The remediator investigates, recommends one, and **carries it to
a decider**. Precedent (excusals for 237, 609, 560/703/1225) was a CTO ruling, and on 2026-07-23 Andrew
directed that an excusal needs a **vendor raw-fact basis**, not inference.

**Step 1 -- establish the fact.** Why did the 09-04 rows for 351 and 1206 leave the source?
- Compare the 09-04 transactions for both accounts in the vendor pull and silver as the 09-05 run saw
  them against today's pull.
- Check the vendor (Orion) record for a reversal, reclassification or cancelled journal. Also check
  whether either account's roster, `isActive` or `cancelDate` changed.
- ⚠ Vendor API egress: follow the INF pipeline's existing pull path. Do not make a new ad-hoc vendor
  call without Andrew's word (CLAUDE.md, vendor-egress rule).

**Step 2 -- choose the branch on that fact.**

| Finding | Remedy |
|---|---|
| The vendor reversed or cancelled the transfer (history genuinely changed) | Excuse **both** accounts in `data/inf/scripts/gold/lib/nna_coverage_excusals.json` with `{reason, decided_by, date}` and the raw fact quoted. Deploy under Rule 13 (DS lane, `safe-deploy`). |
| The rows vanished from our feed, not from the vendor's books (pull/window/filter defect) | Fix the upstream pull or silver step so 09-04 is reproduced. Leave the excusal file untouched. |

⛔ **THE EXCUSAL IS ACCOUNT-WIDE, NOT PARTITION-SCOPED -- READ THIS BEFORE CHOOSING THE FIRST BRANCH.**
`nna_coverage_guard.py:303-304` matches on account id alone:
`excused = {a: v for a, v in lost.items() if a in excusals}`.
Excusing 351 or 1206 removes the guard's protection for those accounts in **every partition, on every
future run**. Every prior excusal was an account that had **exited or closed** (roster exit, estate
closure, vendor cancellation), where that is harmless. **If 351 and 1206 are live accounts, a permanent
account-wide excusal for one $120k transfer on one date is a much larger grant than the incident.** Say
this explicitly to the decider. If the decider wants a date-scoped excusal, that is a guard code change
and its own decision.

**Step 3 -- prove it.** Run the chain ad hoc as QA through `inf-gold-trigger`. Then confirm:
- `pipeline-complete.json` is newly written;
- `platinum/firm/header_metrics.json` shows a current `data_as_of`;
- the alarm stays OK.
Ad-hoc runs are QA only. The scheduled ~11:32Z fire is the acceptance.

**Lanes:**
- INF gold scripts and the excusal file are DS-owned (`0.4.0_DS_ClientPlatform`, Rule 13, deploy via
  `safe-deploy`).
- The excusal ruling has been the CTO's.
- MSTR does not remediate.

## 6. Open questions for the remediator

1. **The "ADVI updates daily" observation.** Andrew sees Inflection ADVI changing daily, but the S3
   evidence in section 3 says it cannot be. Find out which value he sees move before assuming anything.
   It could be a date label computed from the current date, a Lambda view reading silver/gold that is
   still refreshed by the 32 steps that do run, or a different tenant. If a real second serving path
   exists, it is its own finding (a possible duplicate path, which is under a standing Andrew veto).
2. **Did anything else change on 09-05/09-06?** The same two accounts have appeared from day one, so one
   vendor-side event is the likely single cause. Confirm it rather than assume it.

## 7. Separate, lower-priority finding: daily EC2 start churn (not the cause)

- **What happens each morning.** The runner gets ~5 `StartInstances` calls in 2 minutes (CloudTrail,
  09-18..09-21):
  - `inf-assets-trigger` at ~11:18Z;
  - `inf-gold-trigger` at ~11:32Z;
  - `inf-ec2-retry-launch` three times.
- **Why.** The first start after the gold trigger is bounced by AWS as `stopped`, reason
  `Server.InternalError`. Then:
  - `inf-ec2-launch-monitor` publishes "EC2 launch failure" to `inf-otp-alert`;
  - that topic texts +1-305-201-0419 (not email) and invokes the retry Lambda;
  - the instance comes up and the chain runs normally.
  The same pattern hit `inf-bronze-runner` at 11:15Z on 09-21.
- **Small defect.** `inf-ec2-retry-launch` does all 3 attempts even after the first one succeeds. It does
  not check state between attempts; the log reads "Final instance state after 3 retry attempts: running".
  This is harmless, because a start on a running instance is a no-op.
- **Not related** to the chain failure: the chain runs about an hour after these starts before failing on
  data. Worth its own small ticket for the owning AE seat, and only if Andrew wants the texts gone.

## 8. Do-nots

- Do not disable, bypass or weaken `nna_coverage_guard` (its own error text forbids it).
- Do not mute or delete `inf-gold-chain-failed`.
- Do not write an excusal without a recorded decider and the vendor raw fact.
- Do not stand up a parallel publish path to "get data flowing" (standing veto on shadow pipelines).
