# SITE Z FREEZE #11 -- INVESTIGATION, BOUNDED ANSWER, AND FIX DESIGN

**Date:** 2026-08-13 (evening ET) · **Seats:** `0.0.0_AB_MSTR` (laptop) + `0.0.0_AB_MSTR~Z` (site Z)
**Trigger:** Andrew-direct -- no Bloomberg upload on 2026-08-13; *"that needs to be diagnosed and
rectified"*; then *"the basis for the sitez device reset needs to be understood and fortified
against completely."*

---

## 1. THE PRESENTING PROBLEM, AND ITS ACTUAL CAUSE

The Bloomberg daily pull did not run on 2026-08-13. Measured at the served object, not a log:

| | |
|---|---|
| `s3://opal-data-portal-v2/json/benchmarks/model_portfolio_benchmarks.json` | LastModified **2026-08-12 11:06:03 GMT** -- yesterday |
| `data 20260812 v1.pkl` in the SharePoint output folder | **ABSENT** |
| positive control: `data 20260811 v1.pkl` | **found, 8.5 MB + 17.4 MB** |

The positive control is what makes the absence trustworthy: the same call, same folder, succeeded on
the prior day's files. **The failure was at the PULL leg, not the publish leg.**

**Root cause: the site Z box was down.** Unexpected shutdown 2026-08-12 22:58:14 ET (Events 6008 +
41), boot 2026-08-13 17:37:11 ET. **Dark window 18h 38m 57s, with 07:00 ET inside it.** The task
could not have fired; nothing was running to fire it.

Corroborated by two instruments that do not share a source: the Windows kernel log (22:58:14) and
the broker's own liveness clock (*"last seen 67678s ago"* = 23:02 ET). Four minutes apart.

**Resolution:** the task self-recovered on boot via missed-run catch-up, completed clean, and
published at 21:51:47 GMT with `data_as_of 2026-08-12` -- exactly healthy T+1 against
`expected_last_trading_day 2026-08-13`. Verified at content, not just timestamp (5 models with
returns, compositions intact).

> **ACCEPTANCE IS NOT TODAY'S RUN.** Today's was a boot catch-up. The schedule has still never
> completed an **unattended** cycle since the 08-12 tree move. That is the 2026-08-14 07:00 ET fire.

---

## 2. EXONERATED: THE BLOOMBERG TREE MOVE

The prime suspect was CRO~Z's 08-12 `integrations/bloomberg` consolidation, which re-registered the
Scheduled Task and introduced (then self-caught) a silent 07:00 -> 08:03 trigger regression.

**Cleared positively, not by alibi:** the task is registered at the POST-MOVE path, that path
resolves on disk, the 07:00 trigger survived, and it was observed **executing from the moved path**.
CRO~Z's restore of the `-At` default held on its first live exercise.

---

## 3. THE CRASH: WHAT IS PROVEN

**Freeze #11's Event 41 carries `BugcheckCode = 0`, `PowerButtonTimestamp = 0`, `Checkpoint = 0`.**
No bugcheck, no held power button, and no dump exists (newest minidump is 08-10).

**The series is three different failures, not one.** 13 retained stop records over 24.7 days:

| signature | count | reading |
|---|---|---|
| `BugcheckCode 226` (`MANUALLY_INITIATED_CRASH`) | 4 | **US** -- a human forcing a dump |
| `PowerButtonTimestamp` non-zero | 3 | a human held the button |
| **both zero** | **5** (incl. #11) | **no dump, no trace, never attributed** |

> **THE AUTOELEVATE ATTRIBUTION COVERED THE WRONG CLASS.** Freezes #7-#10 are the 226 class -- they
> were attributed *only because someone was standing there to force a dump*. AutoElevate is now
> verified gone (no service, `sc query cbprocess20` -> does not exist, driver absent from WMI,
> program directory gone, no re-push) **and the box froze anyway.** The recurring both-zero class
> was never explained by it.

**"Nothing happened at 10pm" is the finding, not a failure to find one.** 21:45->23:05 ET, System +
Application, all levels: **32 events, not one an error.** Last heartbeat 22:57:55, stop 22:58:14. A
healthy box that ceased executing mid-second.

**Also excluded:** Windows Update as proximate cause (last WU event 5h24m prior; no Event 1074, and
a routine WU restart is *clean* -- confirmed against a same-fleet control where the laptop took
KB5120710 on 08-12 and restarted cleanly with 1074 + 6006/6005 and zero 6008/41). Resource
exhaustion (no 2004/2019). Sleep/hibernate (all disabled).

---

## 4. WHAT IS UNRESOLVED, AND WHY THAT IS A RESULT

**HANG vs POWER-LOSS for #11 is undetermined, and both instruments are spent.**

- `PowerButtonTimestamp = 0` -> nobody power-cycled it. Leans power-loss. Never conclusive alone.
- The downtime axis (#11 was down 18h39m against a 39s-1h29m range for the other twelve) **is
  confounded by attendance.** 07-28 is attended on its own evidence: five site-Z serials resuming
  23:34-23:56 plus an Andrew merge.

> ### CORRECTED 2026-08-14T01:30Z -- THE 08-13 ATTENDANCE CLAIM WAS FALSE, AND I HELPED PROPAGATE IT
>
> This section originally read that 08-13 was attended because `MSTR~Z`'s session serial file was
> written 17:57:43 **"on a box with no remote access"** -- and I called that evidence *unimprovable*.
>
> **THAT BOX HAS TWO REMOTE-ACCESS AGENTS AND BOTH ARE RUNNING:** Splashtop
> (`SplashtopRemoteService`, SRService pid 5344, SRManager pid 6488) and N-able Take Control
> (`BASupportExpressStandaloneService_LOGICnow`). The 17:57 session launch **could have been remote.**
>
> `0.0.0_AB_MSTR~Z` self-reported this the moment they measured it, and named their own error
> precisely: they **asserted an absence from the fact that we were asking for remote access** --
> reasoning from the ask instead of from the box -- and never ran `Get-Service`. I compounded it by
> grading an unmeasured claim as unimprovable *because it came from the seat that was standing there*.
>
> **WHAT SURVIVES, NARROWER BUT NOT NOTHING: remote software cannot boot a dead box.** Splashtop and
> Take Control both need a running OS, so *something physical* still happened at 17:37:11 to bring it
> up. Only the 17:57 **session launch** is now ambiguous between physical and remote; the 08-13 row
> goes from *"physically attended, established"* to *"acted upon by someone, physically or remotely
> -- undetermined."*
>
> ⚠ **AND IT PRODUCED A NEW DISCRIMINATOR NEITHER OF US HAD -- WAKE-ON-LAN.** If WoL is enabled in
> firmware, a box that was **OFF** could have been woken remotely. **A HUNG BOX CANNOT BE WOKEN BY
> WoL.** So evidence that the 17:37 start was a remote wake would be **positive evidence for the
> power-loss limb.** Added to the console/BIOS trip alongside AC-recovery.

> **"A HUNG BOX AND A POWERED-OFF BOX ARE INDISTINGUISHABLE IF NOBODY COMES."** The 18h39m measured
> how long until a human arrived on a Thursday, not what the box was doing.

**The both-zero class is structurally undiagnosable post-hoc.** There has never been anything to
find. That bound is what justifies the remedy -- the remedy is not "find the driver."

---

## 5. HYPOTHESES FALSIFIED (four; three were our own)

| hypothesis | killed by |
|---|---|
| Device-local bindings repointed on the wrong machine (mine) | BG's log shows its box **is** site Z |
| "#11 logon 37s after boot = a human was there" (site Z's) | 7001 fires 11-124s after the **4 AM update reboots** with nobody present -- **Event 7001 is not a human-presence oracle** |
| "07-28's 2m23s recovery proves firmware auto-on, so #11's non-recovery proves a hang" (site Z's) | 07-28 was attended; the premise fails |
| **CPU-thermal protective cut** (mine) | **Zero WHEA events** across 24.7d, and **zero Id-37 throttle events** -- a thermally-limited chassis throttles *before* it cuts |

**Method note worth keeping:** 660 `Kernel-Processor-Power` events could have been read as 660
throttles. Site Z **opened one** -- Id 55 is boot-time capability enumeration, 20 per logical
processor -- then cross-checked arithmetically: count ÷ 20 reproduced the boot census built
independently from Event 6005.

**Surviving:** *hardware protective cut broadly* (PSU / VRM / upstream power) -- it cuts with no
prior throttle and no machine check, so the OS never sees it coming.

---

## 6. THE FIX -- TWO INSTRUMENTS, NOT HARDENING

From inside the OS, "PSU/VRM fault" and "building power event" are the same branch, forever. The
hypothesis space is two limbs -- **power-side cut vs hang** -- and no post-hoc instrument separates
them. So the fixes are the two missing instruments.

**DECISION TREE FOR FREEZE #12** (corrected by site Z after my first version collapsed
powered-off and totally-hung into one bucket -- a wedged kernel means a wedged network stack, so
Tailscale cannot reach it either):

| observation | conclusion |
|---|---|
| UPS logs **input** failure | building/circuit power. **Cause found -- and prevented.** |
| clean input, **output load ~0 W** | box powered *itself* off -> **internal PSU/VRM** |
| clean input, load **normal**, unreachable | **total hang.** Console needed, but you *know* it is a hang |
| clean input, load **normal**, reachable but wedged | **partial hang.** Force the dump remotely -- the only limb yielding a named driver |

> **THE OUTPUT-LOAD READING IS WHAT MAKES THE TREE TOTAL.** A box that is off draws ~0 W; a box
> that is hung still draws power with its fans turning.

**SPEC, AND IT IS LOAD-BEARING: A MONITORED UPS -- network card, or USB plus monitoring software.
NOT a bare battery backup.** A dumb UPS prevents the power limb and **diagnoses nothing** -- it
would have left this investigation byte-for-byte identical. Small price delta; the diagnostic delta
is the entire tree.

**Tailscale remote-in** covers the hang limb: reach a wedged box and force a dump. Tailnet
`goldengate.dev`; site Z is not currently a peer.

### Standing risks found on the way, true regardless of #11

1. **No UPS, no battery, `ChassisType 3`, sleep disabled.** A building power event is *unopposed* on
   the sole Bloomberg Terminal and sole producer of a client-facing dashboard.
2. **`AutoAdminLogon` is NOT SET, and the pull requires an interactive session** (`scheduled_daily_pull.cmd`:
   *"If nobody is logged in at 08:03, this correctly does nothing."*). **Every reboot silently
   disables the Bloomberg pipeline until a human logs in** -- no error, a green task doing nothing.
   On a box that stopped 13 times in 24.7 days.
3. **RDP-then-disconnect leaves the console locked** -- the same state as not-logged-in. A **second
   path into the identical silent outage**, and the reason remote-in must first be exercised *after*
   a 07:00 pull, never before.
4. **`/kill apps` targets `tailscale`/`tailscaled`/`tailscale-ipn` by name** (skill + `kill-maint.ps1`).
   Standing up remote access without an exclusion means a routine cleanup severs it.

---

## 7. OPEN AT ANDREW

1. **Who was at the box on 08-13, and did they find it OFF or FROZEN with a lit power LED?**
   Settles hang-vs-power-loss outright, costs nothing, and **has been available since 17:37.**
2. Tailscale: install y/n · RDP vs SSH vs both · `/kill` exclusion.
3. Monitored UPS (spec above).
4. One console trip answers four things: OFF-vs-FROZEN, BIOS AC-recovery setting, BIOS thermal/fan
   logs + vent obstruction, and whether a UPS exists.

---

## 8. THE METHOD LESSON

**We spent three hours on instruments for a fact a person in the room already had.** Both seats went
to the logs because the logs are what we could reach.

Every one of the four falsifications came from **a control or the other seat -- none from care**, and
in two cases a seat ran the control that killed its own position. The two errors that survived
longest were the same shape in both directions: *two states that look identical because the observer
cannot get to the box.*

**Related:** the cross-device channel itself failed twice this session on a defect of the same
family (LD-0408) -- a consumer whose liveness check reported healthy while it was dead.
