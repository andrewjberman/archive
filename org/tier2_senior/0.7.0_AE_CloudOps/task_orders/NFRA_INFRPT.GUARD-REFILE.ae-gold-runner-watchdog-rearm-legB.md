# TASK ORDER — NFRA_INFRPT.GUARD-REFILE

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_INFRPT is complete; this TO was last touched 2026-06-29, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: staged</status>
<priority>LOW — belt-and-suspenders hardening, NOT an open exposure (Leg A nets the risk)</priority>
<date>2026-06-29</date>

## Why this exists (re-file, not new)

Re-filed from the closed orphan `ADVI_INFETL.BRONZE-FIX.gold-runner-idle-safety-net` (BRONZE-FIX #10).
When COO closed the 8 INFETL orphans (MSTR-delegated, 81e74cdac), `0.7.0~A` spot-checked the 3
safety guards against the LIVE inf gold runner (i-0ed5afded2ebd4ed4 / orion-gold-dispatch.sh) and
found this ONE leg genuinely ABSENT — so per MSTR's rule it's re-filed under a live NFRA banner so the
real hardening isn't buried (RAVC 20260629T133319Z).

## Grounded state (0.7.0~A, live)

The idle-safety-net was a CTO BOTH-NETS ruling (trace-first). Current live state:
- **Leg A — CW overrun alarm = LIVE + sufficient for the core risk.** Alarm `inf-gold-runner-overrun`,
  AWS/EC2 CPUUtilization > 1% for 6x1h (running >=6h vs ~2h envelope) -> opal-critical-surface-alerts
  SNS, dim InstanceId=i-0ed5afded2ebd4ed4. Catches hard-crash-before-arm, watchdog-death, any
  indefinite run. **This is why this TO is LOW priority — the exposure is netted (detect+alert).**
- **Leg B — watchdog re-arm sequenced post-dispatch = ABSENT.** run-gold-layer.sh still deletes the
  watchdog timer at boot (lines 104-113); the dispatch's own comment flags the
  crashed-dispatch-never-arms exposure as #9-F1 "unchanged by this guard."

## Objective

Restore Leg B: re-arm the watchdog timer AFTER the dispatch completes (the CTO-mandated 2nd net), so a
crashed dispatch that never armed shutdown is still auto-reaped — not left to the ~6h detect+alert
window (Leg A) + manual operator stop (~$35.96/mo node cost per stranded run).

<acceptance_criteria>
1. run-gold-layer.sh (or the dispatch wrapper) re-arms the watchdog timer post-dispatch so a
   crashed/never-armed dispatch is auto-reaped, not only Leg-A-detected.
2. Verified on the live runner (the re-arm actually fires on a crash-path test, not just present in source).
3. Deploy via the standard EC2 code path (S3 -> instance, per EC2_CODE_DEPLOYMENT_STANDARD); no inline edits on the VM.
4. RAVC to 2.0.0_SA_COO with the crash-path test evidence.
</acceptance_criteria>

## Note

LOW priority / STAGED — pick it up after the hot cot-auth (DATEMODE-B / probe) + DC-crawl work. It is
tracked here precisely so it is not buried; it is not a fire (Leg A holds the line).
