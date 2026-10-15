# TO-Z6-R3 addendum -- what the 11:00Z fire did with the landed bytes (0.7.0_AE_CloudOps~ZS, 2026-10-15)

**archetype:** VALIDATE

Read at 11:22Z-11:25Z from `C:\Users\Opal Bloomberg\opal_bbg_logs\bbg_tplus1_20261015_070001.log` (07:00 ET = 11:00Z; finished 07:07 ET).
Issuer ruling 34350 asked for this read: "the 8194-listening path must show no 'transport sustained-down' line". Nothing was run or changed
for this addendum; all reads.

## 1. The arm the ruling names was NOT exercised

The fire's fallback read `DAPI DOWN` and took the **transport-down** path (`$absent -eq 3`, no listener on 8194): log line 8
`P0 gate: transport sustained-down, network OK -> sign-in warranted.` That line is CORRECT for that arm. The listener-up arm
(`$absent -eq 0`, which must print no such line) did not occur, so **AC3 is still not exercised and ledger L2 stays open and held.**

## 2. The landed focus re-assert did not take in the scheduled run

| log line | event |
|---|---|
| 10-25 | first fill: login window found (`hwnd=266432`), `focus VERIFIED`, `VERIFY: PASS` |
| 26-30 | submit: `focus re-assert 1/3 did not take`, `2/3`, `3/3`, then `ABORT: focus lost before submit` (rc=4) |
| 31 | `rc=4 -- one bounded re-fill (1/1), no attempt spent` (the R3 path ran as designed) |
| 32-36 | re-fill: `ABORT: focus did not take (fg=32116010 != 266432)`, `re-fill produced no login window` |
| 37-38 | `ESCALATE: ... aborting at ZERO Bloomberg attempts after ONE bounded re-fill (1/1). Human sign-in needed.`; `DAPI FALLBACK EXIT: 2` |
| 55-56 | `PRECONDITION: FAILED -- DAPI DOWN and not self-healed. PULL NOT ATTEMPTED.` |

So the bounded-refill machinery behaved, and the focus re-assert (3 plain tries) **did not cure the focus loss** in a scheduled run: both the submit
and the re-fill found the foreground window to be another window (`fg=32116010`). The same bytes held focus in my 05:44Z interactive run, so the
difference is the caller's context, not the bytes; why is NOT established here (no hypothesis was tested).

## 3. Consequences, measured

- No Bloomberg attempt spent: `.bbg_signin_attempts.json` = **35**, unchanged from before my exercise.
- **The 07:00 ET pull did not run** (`PULL NOT ATTEMPTED`), so no vintage-20261014 PKLs and no publish today from that run.
- At 11:25Z the box holds an open `BLOOMBERG: Login` window (process `bplus64`, `hwnd=266432`, now foreground), `wintrv` x1, `blpsmarthost` x1,
  `blpwtk2_subprocess` x4, `bbcomm` x1; 0 listeners on 8194. This is the scheduled run's state; this seat left it as it is.
- Terminal sign-in before 07:00 ET is Andrew's act (open call 763e); the order says this seat never clicks Login.
