# IRPT_DASHBD: remediations, rounds 55 and 56 (workstream B) -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T03:04:16Z. L8 inputs: `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUNDS_55_56_B_DRAIN_END_20261009.md @90310834e8 (msg 3869)` and `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUND_55_B_DRAIN_END_DB_B_110_20261011.md @be5f9a4b74 (msg 3936)`.

**HELD.** The surprise-corpus gate refuses a new remediation row while a task order in the workstream is not terminal
(`IRPT_DASHBD.TO-DB-b-86` is ACTIVE). These 4 rows land in `surprise-channel/remediations/`, with the L10 slug, when it is.
OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: TO-DB-b-86 terminal.

**For the CTO's round analysis, from the second packet:** the R45 pair was signed on a packet that predates the DB-b-110 cut and the
docstring redaction, so the R45 release packet needs a refresh at the new source bytes before the apply.

```text
[
 {
  "id": "IRPT_DASHBD-D2-W86-S1",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "ADDENDUM 21 states the NOT_COMPARABLE set two ways that do not coincide: the date test selects 549 of the 990 outside segments, the 319 that DB-b-106 flagged share 197 of them. The worker applied the date test, so the restated tie-out's split rests on one of two readings.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W86-S1",
   "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUNDS_55_56_B_DRAIN_END_20261009.md @90310834e8 (msg 3869)"
  ],
  "remedy": "One ruling naming which set ADDENDUM 21 means. If it is not the date test, the 990-segment split is re-cut.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v57",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v57"
  },
  "closed": false
 },
 {
  "id": "IRPT_DASHBD-D2-W86-S2",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "A per-segment convention shift exists for 74 of the 990 outside segments, so CONVENTION (9) is a floor. 916 segments have no two-sided convention measure without re-reading custodian rows, and 244 remain UNEXPLAINED.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W86-S2",
   "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUNDS_55_56_B_DRAIN_END_20261009.md @90310834e8 (msg 3869)"
  ],
  "remedy": "The round analysis states whether the tie-out is accepted with CONVENTION as a floor, or a cell re-reads the custodian rows for the 916.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v57",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v57"
  },
  "closed": false
 },
 {
  "id": "IRPT_DASHBD-D2-W87-S1",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "A worker's safe-apply passed only because APPLY-WHO and CROSSBOX-DEPLOY ran in WARN mode and the HALT gate took HALT_ACK=1. Under ENFORCE the same order is refused, so an order that names a worker as the applier is valid only while those gates warn.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W87-S1",
   "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUNDS_55_56_B_DRAIN_END_20261009.md @90310834e8 (msg 3869)"
  ],
  "remedy": "The issuer names an applier the gates admit (an AE seat) for the next apply order, or the CTO rules that a worker may apply under a signed pair. No gate change is asked here.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v57",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v57"
  },
  "closed": false
 },
 {
  "id": "IRPT_DASHBD-D2-W85-S1",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "MEASURED_THRESHOLDS_R1.json is tracked at neither path handler.thresholds_path() reads, so a kit run refuses without an untracked copy. DB-b-110 measured before and after with the same untracked file; whether that file equals the one the served gold is graded against is not established.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W85-S1",
   "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/IRPT_DASHBD_ROUND_55_B_DRAIN_END_DB_B_110_20261011.md @be5f9a4b74 (msg 3936)"
  ],
  "remedy": "Place the thresholds file where the handler reads it (tracked, or shipped beside the handler) and record its sha256 against the served copy.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v57",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v57"
  },
  "closed": false
 }
]
```
