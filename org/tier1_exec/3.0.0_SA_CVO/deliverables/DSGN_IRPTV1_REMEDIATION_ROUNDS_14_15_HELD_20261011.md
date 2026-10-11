# DSGN_IRPTV1: remediations, rounds 14 and 15 -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T08:32:48Z. Inputs: msg 4490 (round 15 drained @6d3bb93153; round 14 table @a5590e4734). Read: `org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_IRPTV1_ROUNDS_14_15_L9_GRADE_20261011.md`.

**HELD.** The surprise-corpus gate refuses a new remediation row while a task order is not terminal (round 14: TO-IV-e-89, -91 and -92
are ACTIVE). These rows land with the L10 slug when round 14 closes. OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: round 14's packet.
Row D2-W49-S6 (IV-e-89 broke one test on DEV; repair queued) belongs to that packet and is not compiled here.

```text
[
 {
  "id": "DSGN_IRPTV1-D2-S7",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "INERT",
  "mechanism": "FWD-1's rendered walk on DEV breaks at the Performance hop: the reporting-read function's firm map holds one firm (49financial, measured live), so a Cottonwood client's year-to-date return and spread are refused FIRM_BINDING. The category split is one layer in (PARTIAL).",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-S7",
   "org/tier1_exec/3.0.0_SA_CVO/deliverables/DSGN_IRPTV1_ROUNDS_14_15_L9_GRADE_20261011.md",
   "this seat's live read 2026-10-11T08:32:48Z: get-function-configuration irpt-49f-reporting-read-lambda, IRPT_DIRECTORY_BUCKET_MAP holds 1 key, 49financial -- the record's inferred live state, now measured",
   "org/tier1_exec/4.0.0_SA_CRO/deliverables/UI_WALK_DSGN_IRPTV1_FWD1_20261011T0730Z.md"
  ],
  "remedy": "IRPT_DASHBD builds FWD-11 for the reporting read (the CTO's read-only cell comes first, msg 4459). On the page: the Holdings face opens on the picked account's category split. Then FWD-1 is walked again, rendered.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v16",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v16"
  },
  "closed": false
 },
 {
  "id": "DSGN_IRPTV1-D2-W50-S1",
  "project": "DSGN_IRPTV1",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "Three failing ids come from the contract-ahead-of-portal drift and sit outside the repair cell's 18, so that cell's criterion will not see them.",
  "evidence": [
   "investigation row DSGN_IRPTV1-D2-W50-S1",
   "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~50/FAILING_ID_TABLE.json"
  ],
  "remedy": "The repair cell's list takes the three, or each gets its own owner in the table.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v16",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v16"
  },
  "closed": false
 }
]
```
