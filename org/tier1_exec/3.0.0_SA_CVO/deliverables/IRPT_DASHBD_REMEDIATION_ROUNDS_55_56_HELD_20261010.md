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

## Added at the rounds 57-58 compile (2026-10-11T04:22:33Z)

Inputs: `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~88/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH.md` and `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~89/COTTONWOOD_VALUE_RULE24.json` (msg 4035 (rounds 57 and 58 drained @2a6ac2e4e0, @b01e44444e)).
UN-PARKS ON: TO-DB-b-86 and TO-DB-b-116 terminal. D2-W88-S1 and D2-W88-S3 are ARMED and sit in the project's INVESTIGATION_v1.md
with their disarm owners; they do not wait on this file.

```text
[
 {
  "id": "IRPT_DASHBD-D2-W88-S1",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "ARMED",
  "mechanism": "On the 2026-10-08 kit day the returns table is not hash-equal between the live-pinned members and HEAD's: method_version goes from 2 to null on all 6,901 rows, because HEAD's producer carries DB-b-96 and DB-b-102 while the staged sources.json stays at its pin. An R45 release at HEAD's producer with the pinned sources.json serves a null method_version.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W88-S1",
   "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~88/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH.md"
  ],
  "remedy": "The R45 pair names which sources.json rides the release (one that declares method_version for the 49F source), and the kit comparison reads method_version equal on all rows before the apply.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v59",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v59"
  },
  "closed": false
 },
 {
  "id": "IRPT_DASHBD-D2-W88-S3",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "ARMED",
  "mechanism": "The returns manifest the four-member candidate writes states method_version, valuation_source, fee_treatment and price_basis as the literal absent, where the live code writes method_version 2.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W88-S3",
   "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~88/NEVER_WIDEN_PACKET_R45_RELEASE_REFRESH.md"
  ],
  "remedy": "DB-b-115 (in flight) lands the manifest fields; the close is the kit manifest read with method_version 2 stated.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v59",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v59"
  },
  "closed": false
 },
 {
  "id": "IRPT_DASHBD-D2-W89-S1",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The Cottonwood adapter's docstring and COLUMNS_NULL entry say method_version is NULL on purpose while the code stamps 3; METHOD_ROWS row 3 does not state as-traded close or net of fees and inherits an income basis and flow convention measured for the custodian channel.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W89-S1",
   "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_DASHBD_ROUND_58_L9_GRADE_20261011.md"
  ],
  "remedy": "Before the first Cottonwood partition is minted: correct the adapter's two stale statements, and read the emitted dim row 3 and manifest for a sentence false for Cottonwood, editing row 3 under its own rule-24 record if one is found.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v59",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v59"
  },
  "closed": false
 }
]
```

## Added at the rounds 59-62 compile (2026-10-11T05:21:36Z)

Inputs: msg 4142 (rounds 59-62 drained @bbc9e11292, @2f0664fab0, @6d0b3ce3a8, @4d4e3ee317).
Follow-on with no row yet, for the same slug: the live 49F thresholds file carries no claims, so its next dim row reads `held`
on two thresholds that are measured (grade file `org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_DASHBD_ROUND_62_L9_GRADE_20261011.md`).

```text
[
 {
  "id": "IRPT_DASHBD-D2-W93-S3",
  "project": "IRPT_DASHBD",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The dim_return_method contract's method_versions lists rows 1 and 2, while the producer's METHOD_ROWS holds rows 2 and 3. Row 3 is the row the Cottonwood mint stamps, and the contract does not declare it.",
  "evidence": [
   "investigation row IRPT_DASHBD-D2-W93-S3",
   "org/standards/IRPT_DASHBD_DIM_RETURN_METHOD_CONTRACT.json at HEAD, contract_version 0.4.0"
  ],
  "remedy": "The contract lists row 3 before the first row-3 partition is written (the CB-al-2 mint), under the rule-24 record DB-b-102 left beside its deliverable.",
  "owner": "2.0.0_SA_COO~D2",
  "round": "v63",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~D2",
   "round": "v63"
  },
  "closed": false
 }
]
```
