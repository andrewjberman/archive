# IRPT_BCKEND: remediations, round 117 (workstream ~P) -- HELD outside the channel

Compiled by `3.0.0_SA_CVO` (seated on dell2), 2026-10-11T03:53:39Z. L8 input: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_117_P_DRAIN_END_20261011.md @57a120767a (msg 4020)`.

**HELD.** The surprise-corpus gate refuses a new remediation row while a task order in the workstream is not terminal
(`TO-IB-pr-420`, round 118, is issued). These 5 rows land in `surprise-channel/remediations/`, with the L10 slug, when it is.
OWNER: `3.0.0_SA_CVO`. UN-PARKS ON: TO-IB-pr-420 terminal.

```text
[
 {
  "id": "IRPT_BCKEND-D2-S60",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "BLOCKING",
  "hazard_standing": "ARMED",
  "mechanism": "The live irpt-status, irpt-performance-adapter and irpt-narrative zips carry keyword splits between served.py and the packaged modules. The calls fail closed with a TypeError; IB-pr-419 read irpt-performance-adapter as failing on performance-report. Round 117 rebuilt all three and applied none.",
  "evidence": [
   "investigation rows IRPT_BCKEND-D2-S60, D2-S61, D2-W281-S1",
   "this seat's live reads 2026-10-11T03:53:39Z: irpt-performance-adapter CodeSha256 o/643qVE... LastModified 2026-10-09T07:41:59Z; irpt-narrative iEwSFL34... 2026-10-09T14:48:05Z; irpt-status t6OJTCcm... 2026-10-09T18:02:51Z -- none applied since round 117",
   "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_117_P_DRAIN_END_20261011.md @57a120767a (msg 4020)"
  ],
  "remedy": "IB-pr-420 applies the adapter and the narrative under the IB-pr-416 pair, and 2.0.0_SA_COO~Y2 applies irpt-status. The close is the live-call arm at each apply, read by this seat on the served function.",
  "owner": "2.0.0_SA_COO~P2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~P2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-W278-S3",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The live irpt-status zip reads 1 name-limb mismatch; rev 5's RetentionPolicy.reference split is a method call that only the new method-call limb reads.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-W278-S3",
   "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_117_P_DRAIN_END_20261011.md @57a120767a (msg 4020)"
  ],
  "remedy": "Closes with D2-S60 at the irpt-status apply. The method-call limb joins the standing closure check so the next split is read before a release.",
  "owner": "2.0.0_SA_COO~Y2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~Y2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-W278-S4",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "narrative/entry.py declares no prospect or owner-read modes, so two served handlers are unreachable today; their lazy import of interactive_access would raise ModuleNotFoundError if either mode were configured.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-W278-S4"
  ],
  "remedy": "The cell that first configures either mode on irpt-narrative ships interactive_access in the bundle, or the handlers are removed from this host.",
  "owner": "2.0.0_SA_COO~P2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~P2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-W278-S5",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "The attribute limb reports an unknown keyword (path_ids) on the live irpt-narrative, cleared in the built zip; pytest _contracts at the pin reads 2 failed against the 9 of IB-pr-409's packet.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-W278-S5"
  ],
  "remedy": "The live mismatch closes with D2-S60 at the narrative apply. The issuer states which 2 contract tests fail at the pin and whether the release pair accepts them.",
  "owner": "2.0.0_SA_COO~P2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "2.0.0_SA_COO~P2",
   "round": "v118"
  },
  "closed": false
 },
 {
  "id": "IRPT_BCKEND-D2-S62",
  "project": "IRPT_BCKEND",
  "fabric": "dell2",
  "class": "OBSERVATION",
  "hazard_standing": "INERT",
  "mechanism": "IB-pr-418's AC1 grades against the 49F-only set, so it passes while the all-firm served-id hash list still hits tracked files: 5 in the project tree (3 of them named in the order's paths) and 7 in the investor-reporting Lambda tree, one of which is the shipped seam data file with 10,713 ids.",
  "evidence": [
   "investigation row IRPT_BCKEND-D2-S62",
   "this seat's run of the served account-id hash list (29,587 hashes, client-data-check's token rule) at HEAD: IRPT_BCKEND project tree 5 of 2,070 text files hit (1 each: 3 under checks/r19, 1 under checks/r19e, 1 battery file); infra/aws/lambda/investor-reporting 7 of 633 files hit (10,725 hits: _ids/data/custodian_key_seam.json 10,713, _ids/raw_keys.json 2, and 5 test files 10)"
  ],
  "remedy": "A containment cell graded against the all-firm hash list for the 5 project files and the 5 test files. A CTO ruling on the two data files (_ids/data/custodian_key_seam.json, _ids/raw_keys.json): excepted as shipped Lambda data, or moved out of the repo.",
  "owner": "1.0.0_SA_CTO~DELL2",
  "round": "v118",
  "remediation": {
   "state": "OPEN",
   "owner": "1.0.0_SA_CTO~DELL2",
   "round": "v118"
  },
  "closed": false
 }
]
```

## Update at the round 118 compile (2026-10-11T04:42:13Z)

Input: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUND_118_P_DRAIN_END_20261011.md @6eaa44414b (msg 4085)`. TO-IB-pr-420 is terminal; the gate still refuses while 2 IRPT_BCKEND orders read pending. UN-PARKS ON: every
IRPT_BCKEND order terminal. Changes to the rows above when they land:

- **D2-S60** narrows to irpt-status. The adapter and the narrative are repaired on the refusal path (this seat's live reads: digests
  equal the map; TypeError before each apply, typed NOT_AUTHORIZED after). Still open on those two: no ADMITTED request has run on
  the new bytes, and the three widenings on the adapter are applied and unexercised. The close is `2.0.0_SA_COO~Y2`'s irpt-status
  apply plus the first admitted request on each function.
- **D2-W278-S5**: the live attribute mismatch on irpt-narrative is closed by the apply. The 2 failing contract tests at the pin stay.
- **D2-W278-S3, D2-W278-S4, D2-S62**: unchanged.
- **New, to ride the same slug:** the source map's `last_deployed_commit` and `last_deployed_at` for the two applied functions still
  read 2026-10-04 (row D2-S70). Owner `2.0.0_SA_COO~P2`: the apply's ledger or the map records the 2026-10-11 deploy.

## Update 2026-10-11 ~06:5xZ: irpt-status is applied

This seat's live read: irpt-status carries `6idtFvAm` (revision 6), modified 2026-10-11T04:44:47Z; 30 invocations to 06:22Z with
0 TypeError, 0 Traceback, 0 RetentionRefused. All three functions of row **D2-S60** are now repaired, and irpt-status has served an
admitted read (IRPT_YCDGEN round 7's run). When this file lands, D2-S60 graduates as INERT with one residual: no admitted request has
run on the adapter or the narrative. D2-W278-S3 closes with it. New for the same slug: the source map's `artifact_sha256` for
irpt-status reads `E7VKvhg3`, not the live digest (IRPT_ANLREQ row D2-S32 carries it).

## Update 2026-10-11 ~07:0xZ: row D2-S62 does not graduate

`1.0.0_SA_CTO~DELL2` msg 4327 relays Andrew's word of 2026-10-09 (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_192xZ_CLIENT_DATA_IN_PRIVATE_GIT_NOT_WORTH_TIME.md`): no further moving,
redacting or renaming of tracked files for account ids. **D2-S62** (the containment cell passed on the 49F set while the all-firm list
still hits 12 tracked files) is dismissed on that word when this file lands, not graduated. No ruling on the two Lambda data files is
asked. The same word closes the containment follow-ons this seat named for ADVI_COTBKF.
