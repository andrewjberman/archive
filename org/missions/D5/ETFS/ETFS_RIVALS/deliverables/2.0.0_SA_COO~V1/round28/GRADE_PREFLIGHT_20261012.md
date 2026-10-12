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

Not done here: the order's `complete` flip. The report and the executor's proof-of-spec instance sit on box/sitez and are not
yet in this tree (the order file is edited at both ends, so I do not touch it until the merge arrives).

Close: crossbox `XB-20261011T112408Z-a6cc` from-side closed 2026-10-12T10:40:21Z on dell1 (json edit left for MSTR~DELL1's lane).
