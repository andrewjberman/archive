# LD-0255 -- the post-reboot Rio series, T0/T1/T2. The steady-accumulation model is FALSIFIED.

**archetype:** DIAGNOSE

**Why this record exists:** LD-0255 has never had the arm that says whether a reboot resets the Rio
leak and, if so, how it re-accumulates. The 2026-09-11T14:10:36Z reboot created the only clean window
this estate has had. `0.0.0_AB_MSTR` asked for the points; this file is the durable carrier so the
series survives both this session and the laptop being dark.

**Instrument (identical at all three reads):** `Get-Process` / `Win32_OperatingSystem` on site Z.
**Same PID 6924 at all three reads** -- one process, no restart, so these are deltas within a single
process rather than a new process wearing the same name.

## THE SERIES

| point | measured (UTC) | uptime | Rio 6924 private | interval rate |
|---|---|---|---|---|
| **T0** | 2026-09-11T14:18:16Z | 0.130 h | **0.226 GB** | -- |
| **T1** | 2026-09-11T15:52:43Z | 1.702 h | **1.442 GB** | **+0.774 GB/h** over 1.572 h |
| **T2** | 2026-09-11T17:33:18Z | 3.378 h | **1.354 GB** | **-0.052 GB/h** over 1.676 h |

Pre-reboot endpoint for comparison, from @`83c719e2af`: **55.31 GB private after 31.4 h**
(whole-run average **1.76 GB/h**), with `2.0.0_SA_COO~Z`'s 13:35Z RED at free RAM 0.2 GB / load 100%.

Box, same reads: free phys 46.09 -> 36.57 -> **37.22 GB** of 63.46; commit free 71.34 -> 54.00 ->
**53.57 GB** of 89.46. `HuntressAgent` 27636: 0.066 -> 0.124 -> **0.116 GB**.

## ⛔ THE RESULT: NOT MONOTONIC, AND MY OWN T1 INFERENCE IS WITHDRAWN

**Rio DECREASED between T1 and T2.** The curve is not monotonically increasing over the first 3.4 h.

At T1 this seat wrote that the rate **rises** and the leak is **convex**, reasoning that 0.774 GB/h
over the early window against a 1.76 GB/h whole-run average forced a higher later rate. **That
inference is WITHDRAWN.** It was sound arithmetic on two points and the third point kills it.

>> ⭐ **THIS IS THE ARGUMENT FOR THE THIRD POINT, AND IT IS BETTER THAN THE ONE ORIGINALLY GIVEN.**
   Two points fix an average and can falsify constancy; they CANNOT distinguish a rising curve from a
   rise-then-plateau, and both readings are arithmetically identical at n=2. Refusing to fit a shape
   to n=2 was right, and a confident convex claim would have been wrong in a way nothing at n=2 could
   have caught. <<

## WHAT n=3 SUPPORTS, STATED NO MORE STRONGLY THAN THAT

Rio rose to ~1.4 GB in the first ~1.7 h and has been **flat-to-slightly-down** since. That is the
shape of a **WARM-UP TO A WORKING PLATEAU**, not a steady leak from boot.

It is **also consistent with LOAD-DEPENDENCE**: the rise coincides exactly with the relaunch of five
seats plus the codex process family, and the flattening coincides with those seats settling into
ordinary work. The two hypotheses are not separated by these data.

⛔ **AND THE PRE-REBOOT ENDPOINT IS NOT REACHABLE FROM HERE AT THESE RATES.** 55.31 GB at 31.4 h is not
producible by anything visible in the first 3.4 h -- at the T1->T2 rate it never arrives at all. So
whatever drives the 55 GB has a **LATER ONSET or an EPISODIC TRIGGER**; it is **not** a constant
background accumulation that a reboot merely resets.

>> **THEREFORE THE WORKING MODEL -- "a reboot resets the leak and it re-accumulates steadily" -- IS
   MEASURED FALSE for the early window.** That is the result LD-0255 has never had, and it is a
   NEGATIVE result: it removes a model rather than supplying one. <<

## NOT CLAIMED

- **Which** of warm-up-plateau / load-dependent / later-onset it is. n=3, one boot, one device.
- That the T1->T2 decline is a real **release**. It may be an ordinary working-set trim; private bytes
  falling is evidence against monotonic growth but is not proof memory returned to the OS.
- **The circulating "~8 GB/h" figure. Nothing measured here supports it, at any point in the series.**
  The whole-run average is 1.76 GB/h and no measured interval exceeded 0.774.
- Any time-to-wall projection. The curve must bend upward somewhere to reach 55 GB, and **this series
  does not contain that bend.**

## THE USEFUL NEXT READS, AND WHY NOT TONIGHT

**~8 h and ~24 h uptime**, same instrument, same pid if it survives. More reads tonight would sample
the flat region that is already characterised. **The interesting region is where the curve MUST bend
to reach the pre-reboot endpoint, and that region is hours away** -- sampling before it cannot
discriminate, and a dense cluster of early points would make the series look thorough while answering
nothing new.

⚠ **A SUCCESSOR SHOULD RE-READ THE PID FIRST.** These deltas are only comparable while pid 6924 lives;
if Rio restarts, the series restarts with it and a naive continuation would silently compare two
processes.

## DISPOSITION

Rio stays **UNTOUCHED** -- SYSTEM, vendor-managed, LD-0255 alt (a) rejected. No action was taken and
none is recommended: current headroom is comfortable (37.22 GB free of 63.46) against the 0.2 GB that
forced the reboot. This record is a measurement, not a remediation, and the remedy question remains
Andrew's and IT's.

Sent to `0.0.0_AB_MSTR` as bus `8e321521` (T0), `f35b4722` (T1) and `d177859a` (T2+falsification);
that seat's box entered a managed winddown at ~17:3xZ, so those may sit queued. **This file is the
carrier that does not depend on their delivery.**
