# IRPT_ANLREQ round 44, workstream T -- close record: the commentary function runs the figure block, the closed vocabulary and the logger level (2.0.0_SA_COO~T2, dell2, 2026-10-15)

Order `IRPT_ANLREQ.TO-APPLY-t34` (cell `AR-t-34`, WORLD), issued `76ad5d7843`, amended `cbc529c86a`; applier `0.7.0_AE_CloudOps~AQ2`; pair: COO half packet blob `d416567b45` (section 8), CTO half R3 @dfac94827f (msg 8624). Decomposition `decompositions/IRPT_ANLREQ_DECOMP_R44_T.md`.
The applier's record: `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/A_T34_SURGICAL_APPLY.txt`. The project row's `dep_stage` is the driver's and is untouched.

## What happened

| step | read |
|---|---|
| first attempt (build at pin 5b438cd6c4) | STOPPED at step 3 by the CTO's "exactly 3 members" condition: the rebuild differs from the live zip in 17 members and adds 8; nothing applied (ledger closed gate-refused, AQ2 msg 8614) |
| ruling | route B, a surgical zip: the fetched live zip with exactly three members replaced from the pin (packet section 8); the CTO re-signed |
| the surgical zip | 92 members (= live), 904,953 bytes, sha `hUZY39qN...`, assembled outside the repo by `t34_surgical_zip.py`; the three proofs: (i) 3 of 3 byte-equal to the pin, (ii) exactly 3 members differ from live, (iii) three `-I` imports OK; `ADDR-EQUAL-OK teams=14/14 mail=7/7 control=discriminates` |
| plan and apply | 0 to add, 3 to change, 0 to destroy, only `source_code_hash`; re-plan "No changes"; all three functions read `hUZY39qN`; memory, timeout, env NAMES and the mapping unchanged |
| clock | started after the 20:00Z Teams fire's REPORT, finished clear of the 21:00Z fire; neither pull invoked |
| the proof invoke | `get_ref` non-null; ONE invoke of the commentary function: stage `draft_exists`, `failed` empty, no model call (4.2 s); the log gained its FIRST application line, `commentary draft exists request_id=REQ-d47252fe74634d0c5cdd8067` (INFO) |
| my read of the check | `R44-AP1-OK digests=1 live=hUZY39qN events_with_INFO_line=1`; the same check read FAIL on the pre-act zip and FAIL (INFO absent) between the apply and the invoke |

## Claims and limits

- Claims: the commentary function now runs the closed-vocabulary figure projection (AR-t-31 and AR-t-33) and logs at INFO (AR-t-32). The logger fix is PROVEN LIVE by the one line above.
- Does not claim: that a real draft's `COMMENTARY-POST` line, a 200 from the ticket route, or figures in a real prompt have occurred. UNEXERCISED LIVE until a request whose record names a ticket and whose reader returns figures.
- Not read yet: the 21:00Z Teams fire on the new digest (the shared zip's two pull functions run the same code but a new digest); read at the next tick.
- Open: `~G2`'s figures producer; the resident's packaging refusal (`AR-y-357`, `~Y2`); the CTO's per-function-zip design (row `IRPT_ANLREQ-D2-S127`); the gold re-run and a gold reader port for precedents; the surgical and rollback zips exist only in `C:/dev/aq2-t34` (kept until the next deploy of this root, the rollback artifact).
