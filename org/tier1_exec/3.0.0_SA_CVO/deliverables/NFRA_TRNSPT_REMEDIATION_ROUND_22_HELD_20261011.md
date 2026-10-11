# NFRA_TRNSPT: remediations, round 22 -- HELD outside the channel

<sweep_watermark>2026-10-11T04:12Z</sweep_watermark>

Round 22 slug by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T04:12:03Z. L8 input: `org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_CLOSE.md @733aec56af (msg 4030)`. No judgment criterion. Graduated, round label v23:
4 rows, OPEN. ARMED: 1 (D2-S19), disarm owner `2.0.0_SA_COO~T2`, due before the Monday 2026-10-12 13:00Z fire.
Also carried by the close record, not rows: the handler's totals line omits read_refused; `test_eod_voice.py` does not collect.

**HELD.** The surprise-corpus gate refuses a new remediation row while a task order is not terminal
(`NFRA_TRNSPT.TO-APPLY-a18.second-reader-role-laptop` reads pending). These 4 rows land in `surprise-channel/remediations/`, with the
L10 slug, when it is. OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: TO-APPLY-a18 terminal.
The ARMED row D2-S19 does not wait on this file: it is in the project's INVESTIGATION_v1.md with its disarm owner.

```text
[
 {
  "id": "NFRA_TRNSPT-D2-S19",
  "project": "NFRA_TRNSPT",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "ARMED",
  "mechanism": "The Teams pull reports Max Memory Used equal to its 128 MB Memory Size on every invocation that read transcript content (4 of 25). A fire that lands more than one transcript can be killed at the limit; a killed run writes no run record.",
  "evidence": [
   "investigation row NFRA_TRNSPT-D2-S19",
   "the same log's 25 REPORT lines: Max Memory Used equals Memory Size (128 of 128 MB) on 4 invocations -- 2026-10-09 16:01, 16:02, 16:04 and the driven run of 2026-10-11 03:40; the other 21 read 98 to 100 MB",
   "this seat's live reads 2026-10-11T04:12:03Z: teams-global-transcripts-pull-lambda CodeSha256 AI4UQD0M..., LastModified 2026-10-11T03:36:14Z, Active/Successful, equal to the sha256 of the local dist zip (AI4UQD0M...); MemorySize 128, Timeout 300; target of rule teams-global-transcripts-pull-hourly"
  ],
  "remedy": "Before Monday 2026-10-12 13:00Z: raise memory_size under a never-widen pair (the setting only), or record why 128 MB holds. Monday's read takes the REPORT line beside run.json.",
  "owner": "2.0.0_SA_COO~T2",
  "round": "v23",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~T2",
   "round": "v23"
  },
  "closed": false,
  "disarm_owner": "2.0.0_SA_COO~T2"
 },
 {
  "id": "NFRA_TRNSPT-D2-S16",
  "project": "NFRA_TRNSPT",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "INERT",
  "mechanism": "The scheduled Teams pull failed on every fire from 2026-10-09T16:00Z (21 invocations) because one refused content read raised. The fix is deployed and ran clean once on a seat-driven invoke. The scheduled trigger has not fired on the new code.",
  "evidence": [
   "investigation row NFRA_TRNSPT-D2-S16",
   "this seat's filter-log-events on /aws/lambda/teams-global-transcripts-pull-lambda since 2026-10-09T12:00Z: 107 events, 25 invocations; 21 [ERROR] GatewayGraphError, first 2026-10-09T16:01:13Z, last 22:03:28Z; the one invocation since (2026-10-11T03:38:50Z to 03:40:09Z, 79.3 s) logs no error",
   "this seat's live reads 2026-10-11T04:12:03Z: teams-global-transcripts-pull-lambda CodeSha256 AI4UQD0M..., LastModified 2026-10-11T03:36:14Z, Active/Successful, equal to the sha256 of the local dist zip (AI4UQD0M...); MemorySize 128, Timeout 300; target of rule teams-global-transcripts-pull-hourly",
   "org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_CLOSE_READBACK_20261011.md"
  ],
  "remedy": "Read the Monday 2026-10-12 13:00Z fire from run.json per-series counts, with the function log beside it. That read closes this row.",
  "owner": "2.0.0_SA_COO~T2",
  "round": "v23",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~T2",
   "round": "v23"
  },
  "closed": false
 },
 {
  "id": "NFRA_TRNSPT-D2-S15",
  "project": "NFRA_TRNSPT",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "INERT",
  "mechanism": "Four monday_meeting transcripts (2026-04-10, 04-13, 05-04, 06-01) are listed by the gateway and their content is refused; they never landed and are ABSENT by this route. Any meeting not landed within about 120 days is lost the same way, and research_meeting's listing is refused today.",
  "evidence": [
   "investigation row NFRA_TRNSPT-D2-S15",
   "org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~T2/R22_CLOSE_READBACK_20261011.md section 3"
  ],
  "remedy": "The CTO rules FWD-3 on the 4 (accepted as lost, or another source named) and FWD-2's wording for research_meeting. Andrew's SharePoint folder link is the open call.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v23",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v23"
  },
  "closed": false
 },
 {
  "id": "NFRA_TRNSPT-D2-S17",
  "project": "NFRA_TRNSPT",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The transcripts Terraform root has no default and no tfvars for second_reader_trust_principal_arns, so every plan needs a -var. A guessed value on an untargeted apply would rewrite who may read the tier.",
  "evidence": [
   "investigation row NFRA_TRNSPT-D2-S17"
  ],
  "remedy": "A committed tfvars or a default for the variable, taken from applied state. It names who reads the tier, so it is the CTO's call.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v23",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v23"
  },
  "closed": false
 }
]
```
