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

## State re-read 2026-10-09 ~02:2xZ (2.0.0_SA_COO~AI, after the 2026-10-08 site Z reboot)

The card above is unchanged; these rows supersede its measured table where they differ. Measured at writing unless marked.

| item | value |
|---|---|
| opal_ai origin PROD and DEV | both `de5ce25fa3` (`git ls-remote`, 2026-10-09 ~01:4xZ). The card's PROD `bd7cd5d1ce` is superseded |
| runtime checkout `C:\opal_runtime\opal_ai` | `9c0a80b8d0`, clean (0 porcelain lines). `9c0a80b8d0` is an ancestor of `de5ce25fa3`, so the launcher's fast-forward to PROD holds |
| what that fast-forward brings | 5 files: the two shebang removals (opal_ai CI fix), the WFP installer `wall-dapi-8194-wfp.ps1` and the R1 script, and `resolve-claude.ps1` (OA-f-12). `launcher.ps1` and `launch-gate.ps1` are unchanged across `9c0a80b8d0..de5ce25fa3` |
| DAPI 8194 wall | holds across the reboot: OA-f-11 AC4 PASS (`F11_PERSISTENCE.json`, measured 2026-10-09T01:41Z, boot 2026-10-08T20:56:05Z): Opal_Agent and Opal_MSP 8194 REFUSED, 8790 OPEN; operator 8194 OPEN. Drained @438c776cd8 |
| Terminal | bbcomm listening on 127.0.0.1:8194 at ~01:4xZ (pid 18020) |
| 8790 view server | not listening at ~01:4xZ (the AC4 probe started and stopped it). Whether the close run needs it up beforehand was not read this pass |
| Alyssa Keith's portal-only asker grant | as recorded, ACTIVE (OA-g-3 @da3a2cafbe). Claim: held, not re-read this pass |
| the sitting | not set: Andrew-direct 2026-10-06 ~21:1xZ, "nothing we can do on the call 1 at this time". Not re-asked |

Nothing in the run steps changes. On Andrew's word for a time, the card runs as written.
