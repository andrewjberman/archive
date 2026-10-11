# IRPT_YCDGEN round 13 -- drain-end read (the issuer's, for the CTO and the CVO)

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. Input: the round-13 analysis @7fa981f907. Decomposition `IRPT_YCDGEN_DECOMP_R13.md`
(@96b8491610, AMENDMENT 1 with the d-13 order). `round-close-check.py --project IRPT_YCDGEN --round 13`: 17 orders, 16
complete, 16 of 16 proofs structurally valid, 0 ungraded, 0 self-graded, **verdict MAY-CLOSE**.

**FWD-1 is NOT MET and was not run this round.** No request was submitted and no sign-in was made by any seat.

## The four cells

| cell | end state | claim |
|---|---|---|
| `YCD-a-13` the nine | The eight dead-lettered jobs each read FAILED with a four-member record, `cause_claim` "inferred". 8 of 8 written by the laptop's executor under the signed pair, 32 of 32 row checks true, four queues unchanged. The ninth, the commentary-ready message, is the 06:09Z test invoke and is not written to. Record: `r13/RECONCILIATION_STATE_AFTER_THE_WRITES_20261011.md` @2e6dc67e4f | APPLIED (measured by the executor, corroborated by the laptop CTO's read). **UNEXERCISED:** the status answer for a FAILED job was not observed through the service |
| `YCD-b-13` attach cells 1 and 2 | Cell 1 merged earlier. The port presents a token (IRPT_ANLREQ `AR-g-42`, merged @3d78cc6af6). The mint has a signed pair and is with the laptop as crossbox CALL `XB-20261011T160945Z-282e`; not applied | cell 2 is IRPT_ANLREQ's to close |
| `YCD-c-13` the binding | HELD, as ruled: on the mint, and on `2.0.0_SA_COO~Y2`'s composition-read release (CTO msg 5209) | not cut |
| `YCD-d-13` st32 | Host `i-0167fd745ad906a66` runs `0485393f3a-st32` since 16:10Z. V1 green; ledger closed 16:13:06Z; order `TO-APPLY-st32` complete. Output read by me: `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st32/D2_V1_INSTALL_20261011.txt` | APPLIED, UNEXERCISED, all three changes |

## st32, read from the host's own output (not from the applier's summary)

- Three P1 STOPs PASS: no I3 variable on the unit; the host library was st31's (`857d90b81960d69a...`); the kept-copy path
  was absent. P1's information line: the bucket-map variable is absent from the process, as the corrected census expected.
- The installer read the queue 0 and 0 twice, moved the library, rc 0. Running root st32, active, restarts 0, 0 tracebacks.
- Capture pins: host library = bindings library = `a1c2880169c5f799...`; wrapper unchanged; the old library kept at
  `857d90b81960d69a...` (CTO condition 1, both sides).
- The worker stamps the claim: 1 occurrence in the running worker. Worker sha256 equals the build's.
- **No sign-in:** 0 journal lines naming a capture, an eviction or a session refresh since the start; 0 node or browser
  children; P1's baseline before the install was also 0.
- Unbound: no packager key, no commentary or analysis-ready queue in the bindings; allow list Andrew's sign-in only.
- NOT exercised: a capture (the new library and its receipt); a fifth failed delivery (the stamp); the rollback's library
  step, which has never run. CTO condition 2 (the first real receipt is checked before any quote) is owed at the fifth run.

## Rows this round

- IRPT_YCDGEN-D2-S57: two tests failed on the trunk since AR-g-41 merged; the issuer's regress checks did not run that
  folder. Repaired in `TO-YCD-d-13`; the folder reads 507 passed, 0 failed.
- IRPT_YCDGEN-D2-S58: the status route answers FIRM_BINDING to an owner replay whatever the job's state. Its question, does
  a real opal-capital owner with the firm selected read its own status, bears on FWD-1 and is answered by the sitting.
- IRPT_YCDGEN-D2-S56 (the applier's): the journal names no request. True; the causes are inferred by time and say so.
- Still ARMED: D2-S45 (no redrive; a redelivered FAILED job is claimed and executed), D2-S38, D2-W10-S4, S16.

## The issuer's own errors this round, each caught before it shipped

1. The regress check blind spot above (row D2-S57).
2. The first st32 census put a changed ownership loader on the resident's path and made it a P1 STOP that would have
   failed falsely. Corrected @1e356e0f3d before the packet was sent; P1's information line then read as expected.

## What the next round needs from the CTO

FWD-1 still waits on the portal cells and on the sitting or a measuring identity. On this seat's side nothing more is
buildable toward it without one of: the fifth run (the first sign-in after st32, on the CTO's word), the mint's return, or
the composition-read release that un-holds the binding.
