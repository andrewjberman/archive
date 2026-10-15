# IRPT_BCKEND round 3, workstream ~PO (the Orion Inflection raw feed), the unlocated flat-key writer -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~06:4xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @14f2b2da5b on the CTO half of the Orion pairs packet (condition 1) and the four managers' answers: IB-pr-559 `complete` (merged @e7837beeca). `python .tools/round-close-check.py --project IRPT_BCKEND --round 3 --workstream "~PO"` reads `MAY-CLOSE`. I re-ran IB202-1 AC1 to AC3 on the landed tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **Nothing was stopped, started, changed or written to AWS; every call was a describe, list, get, head or lookup.**

## What the CVO needs to know

- **The writer of the daily Orion Inflection flat keys is located (measured): the Orion pull steps of the gold chain on the `inf-gold-layer-runner` EC2 instance.** `inf-gold-trigger` starts the instance and sends the chain by SSM at about 11:32Z each day; the chain (`orion-gold-dispatch.sh`, `chain:full`, steps `INF_API_PULL_TXN`, `INF_API_PULL_PERF`, `INF_API_PULL_POSITIONS_DAILY`) runs the pull scripts, which write the flat keys 11:40-11:52Z; the instance stops itself after the chain. CloudTrail S3 data events (org trail, recorded for `opal-data-inf` only since 2026-10-13 20:30Z) show the PutObject events by the runner's instance-profile role session on 2026-10-14. The `code/manual_api` and `code/gold` copies of the three pull scripts are identical.
- **What it means for the signed Orion pairs packet (sha256 `c3dcc22f02e8...`, both halves signed):** pair (b) as signed PORTS the manual CLI writes into a new scheduled handler and RETIRES them; but those pulls are live steps of a chain that also feeds the silver transactions and performance steps (row D2-W403-S3, ARMED, owner me). Porting beside the chain would be a second producer; retiring them would cut the silver steps. I recommend to the CTO that pair (b) be re-cut as a RE-TIMING of the existing chain trigger into the 06:00 New York fold (no new producer), and that pair (a) re-run the 36 absent days through the same chain steps. That is the CTO's call and is asked in the same tick.
- **Other findings:** no `StopInstances` event (the instance stops itself); the SSM command text is hidden by CloudTrail; S3 server access logs are not enabled.
- **Rows:** D2-S186 dispositions D2-W403-S1 to S4. STILL ARMED, carried: D2-W403-S3 (the handover couples to the gold chain), D2-S184 (superseded by the located writer; closes when the pair is re-cut), D2-W394-S2, D2-W392-S2, W349-S1, W361-S1, W348-S2, W368-S2 (owner me), D2-S158 (with the CTO).
- **Not cut and why:** the Orion build slices (the port and the schedule declaration wait on the re-cut; the Scope-account addendum waits on B-IN's feed, CTO msgs 8110 and 8112: NO_START_DATE_AT_SOURCE measured per observed account, inferred otherwise, GROUP_NO_SERIES / NOT_DETERMINED for a group with no series).
- **Scratch awaiting Andrew's word (recursive deletes):** `C:/dev/_scratch403` holds downloaded org-trail logs, besides the earlier directories (open call dell2-20261015T014138Z-53cb).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
