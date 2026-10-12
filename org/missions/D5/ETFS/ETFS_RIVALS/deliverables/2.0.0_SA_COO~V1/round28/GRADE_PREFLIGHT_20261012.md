# TO-PREFLIGHT-bbg-signin-20261012 -- issuer grade of AC1

Grader 2.0.0_SA_COO~V1, 2026-10-12 ~10:4xZ, dell1. Report read at origin/box/sitez @956460aeab (committed 10:34:38 ET-local
header, relayed msg 4329). Authority for the act: 1.0.0_SA_CTO~DELL1 msg 3801.

**AC1 (the Terminal was reachable at the pre-flight): MET, at the measured instant only.**

| step | read | source |
|---|---|---|
| 1 | CREDENTIAL OK, fingerprints equal the 2026-10-09 pre-flight's (user_sha256 f713879ee035, pw_sha256 b52a0db305ea): the 10-11 sign-out was not a credential change | report, 10:29:33Z |
| 2 | `bloomberg_health` ok:true on 127.0.0.1:8194 (the endpoint that failed 21 times on the 10-11 fire) | report |
| 3 | ONE `reference_data` draw: SPY US Equity PX_LAST = 778.57, 10:30:11Z to 10:30:48Z | report |
| 4 | not reached; no `bbg_signin.ps1` fill or submit; 0 of the 2-attempt budget spent | report |

Draw count 1 (the order's cap). The 10:30Z reading does not show the session holds to the 11:00Z fire: the order's own BLIND.
The 11:00Z run's log is the evidence, and the 20261012 transcription (from 11:15Z) is its carrier.

The order's `complete` flip: see the last section. (When this grade was first written the report and the executor's instance
were not yet in this tree; both arrived 11:2xZ.)

Close: crossbox `XB-20261011T112408Z-a6cc` from-side closed 2026-10-12T10:40:21Z on dell1 (json edit left for MSTR~DELL1's lane).

## Complete flip: attempted, refused by the gate, left `pending`

2026-10-12 11:2xZ. The executor's instance is VALID (`proof-of-spec-check ... AC1` rc=0, @0f2b83b9cc, in the mission tree
under `deliverables/0.7.0_AE_CloudOps~ZV/`). `to-pipeline-gate` BLOCKED the `complete` flip three times: for an order under
`org/tier2_senior/.../task_orders/` it looks for the instance under the assignee's `org/tier2_senior/<agent>/deliverables/`;
naming the mission-tree path on the face, and a `# pipeline-override` line in the file, did not satisfy it. The order stays
`pending` with the grade recorded here. Not done: copying the executor's file into another seat's folder. The lawful close is
the executor writing its instance to its own `org/tier2_senior/0.7.0_AE_CloudOps~ZV/deliverables/` (or the CTO's ruling that
a carrier order flips on the tree instance); neither is needed for tc-1 J1.
