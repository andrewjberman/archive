# NFRA_OPALAI -- item-0 close run card for Andrew (2.0.0_SA_COO~AI, 2026-10-02 ~18:3xZ)

Every state below was measured at writing, except the two grant rows, which are as recorded (claim: held).

| item | value |
|---|---|
| opal_ai origin PROD | `bd7cd5d1ce` (G-PUSH on Andrew-direct ~18:1xZ "authorize the push", MSTR~Z msg 28618; ls-remote read) |
| runtime checkout `C:\opal_runtime\opal_ai` | `9c0a80b8d0`, clean, a fast-forward of PROD. The launcher pulls `bd7cd5d` at launch, and the push changed neither `launcher.ps1` nor `launch-gate.ps1` (row Z-S56) |
| OA-f-12 resolver on `bd7cd5d`, non-elevated | PASS (seam `CLAUDE_EXE: C:\Users\Opal_Agent\.local\bin\claude.exe`) |
| DAPI 8194 wall | live (OA-f-11 AC3 PASS) |
| Alyssa Keith's portal-only asker grant | ACTIVE (OA-g-3 @da3a2cafbe) |
| Menachem's grant | NOT active. It waits on his verified tid/oid (NFRA_OPLGTW G-E) |

## The call (one decision)

**Run the item-0 close run now, with Alyssa Keith as the colleague: yes / no?**
- REC: yes. Runbook Part C step 6 names Alyssa (your call-2 answer), and her grant is active. Your later G-ASKER word
  names Menachem, and his run follows as soon as his grant is active. That one open point was put to you by
  `1.0.0_SA_CTO~O` msg 26208; this card answers it with the issuer's REC.

## The run, on yes (about 10 minutes)

1. From a **NON-elevated** PowerShell (the launcher refuses an elevated one):
   `powershell -File C:\opal_runtime\opal_ai\opal\runtime\launcher.ps1 -Config C:\opal_runtime\runtime.config.json`
   - Expect `OK: checkout fast-forwarded to PROD`, then `GATE: PASS`, and a window titled `Opal_Agent Analyst` opens.
   - On any `LAUNCHER: REFUSE ...` line, stop and send that line to the COO.
2. If the Analyst window asks for a sign-in, it is the same as runbook steps 4-5: the DEDICATED Analyst account for
   Claude, then Opal Bloomberg for the gateway (with your phone MFA).
3. **Alyssa** sends the Opal Bloomberg account one Teams chat message about a figure the portal shows. For example:
   "How many accounts hold each Opal model portfolio, by firm?" A correct reply gives the figure, the as-of date, the
   source and the scope.
4. **You** (you have no asker profile) send the same account one question. The correct result is a refusal
   (`asker_no_profile`, with the how-to-get-access line). That is the un-admitted arm.
5. Tell the COO "done". `2.0.0_SA_COO~AI` captures both exchanges into `deliverables/2.0.0_SA_COO~AI/round2/`.
   `3.0.0_SA_CVO~O` then grades OA-t-1 J2: the figure, date, source and coverage must match the portal for that date.

## After a pass (the COO's acts, per CUTOVER_PLAN_20261001.md steps 6-7, accepted by `1.0.0_SA_CTO~O` msg 27958)

The held OA-t-1 / OA-t-3 parent halves merge. The `.tools/ajb.ps1` BG launch retires in the same sitting (PRD C11:
the cutover drops nothing silently). Then OA-e-8 measures the speed stages. The CLOUD push of that merge is
`0.0.0_AB_MSTR~Z`'s, as for any trunk push.
