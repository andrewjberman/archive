# NFRA_OUTSET TO-OS-s-28 -- THE DRIFT MEASURE IS CONTINUOUS AND NEVER HAND-TRIGGERED

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Order:** re-cut @`32b730ae79`
· **Result written:** 2026-09-10 ~18:3xZ · **Criterion:** `O28-AC1` (six arms, all HOLD, token
printed, rc=0) and `O28-AC2` (judgment, recorded below, **not self-graded**)

---

## THE ONE-LINE ANSWER

**The drift measure now publishes on a recurring quarter-hour cadence with no human act, and the
first such publish is on the record.** What this cell did **not** close is the interactive-only
principal: while nobody is logged on, the device still publishes nothing. That is one elevated line
only Andrew can run, surfaced below with its exact text and rollback, **not routed around by
quietly choosing a weaker shape.**

---

## THE SHAPE I TOOK, AND WHY

Shape **(i)**, the recurring device-side timer, because `1.0.0_SA_CTO`'s L4 ruling @`46b832a9a3`
withdrew the other two and left the carrier where `OS-s-21` put it. I did not re-open that. What I
priced is the part the face handed me: **how a device-side timer survives a logged-out principal.**

**What I rejected, and why, beyond the withdrawn shapes:**

- **A logon trigger.** It would have closed the coverage gap cheaply and it is the obvious move.
  I refused it: it makes the cadence depend on a human habit, which the order kills by name, and it
  would have made arm (d) read better while making the thing worse.
- **Running as `SYSTEM` or a group principal.** Also refused-by-denial (measured below), and it
  would have moved the credential source out from under the scoped-role assume, which bound (63)
  forbids widening.
- **A hand publish to hold the artifact green while building.** Explicitly forbidden by bound (61),
  and it would have erased the very evidence arm (a) rests on. **The artifact sat 18.3 h stale and
  I let it.**

---

## ARM (a) -- THE DEFECT, REPRODUCED ON EVIDENCE THAT SURVIVES ITS OWN FIX

The face requires arm (a) to STOP rather than grade against a moved world. **The world did move --
I moved it at 18:16Z.** So the reproduction is carried by two things that outlive the fix.

**The pre-state, exported before the act** (`os28_task.BEFORE.xml`, sha256 `457E61C387D792E2…`):

| property | value |
|---|---|
| principal `LogonType` | `InteractiveToken` |
| trigger | `CalendarTrigger`, daily, StartBoundary `2026-09-09T07:30:00` local = **11:30Z** |
| `<Repetition>` block | **absent** -- fires once per day |

**The skipped fire, shown as an absence bounded on both sides.** S3 versioning records it durably:

| | |
|---|---|
| due instant | `2026-09-10T11:30:00Z` |
| last version BEFORE it | `2026-09-09T23:58:14Z` |
| first version AFTER it | `2026-09-10T18:16:56Z` |
| versions in between | **0** |
| gap | **18.31 h**, 70% of the consumer's 26 h ceiling |

Denominator: **5 versions**, all five listed in the battery output. `NumberOfMissedRuns` read **1**
at 18:06Z, and `LastRunTime` was `2026-09-09 19:58:07` local -- a **hand-started** run, which is the
provenance the face named as dying.

---

## ARM (b) -- THE PUBLISH HAPPENS WITH NO HUMAN ACT (the one DIFFERENCE control)

**The instrument, named rather than asserted: the publishing process's own ancestry.** A VersionId
and a timestamp are byte-identical in both branches and cannot discriminate. The ancestry can:
Task Scheduler reaches its action through the Schedule service.

| branch | measured ancestry | verdict |
|---|---|---|
| **automatic** (served bytes) | `python.exe <- cmd.exe <- svchost.exe <- services.exe <- wininit.exe` | `scheduled` |
| **human** (this battery's own process) | `python.exe <- timeout.exe <- …` no service ancestor | `interactive` |

Scheduler-only ancestors present in the served artifact: **3 of 4**. Human-session ancestors:
**0 of 8**. `cmd.exe` is deliberately excluded from the human set -- the task's own action *is*
`cmd /c …`, so it appears in both branches and discriminates nothing.

⛔ **THE FIRE WAS NOT STARTED BY ME.** I did not run `Start-ScheduledTask` and did not invoke the
publisher. Re-registering the task with `StartWhenAvailable=true` let the scheduler pick up the
missed occurrence on its own at `14:16:41` local; the publish landed at `18:16:56Z` as VersionId
`hz832zL8rkcnC2fNailBAR`, 28,255 B.

---

## ARM (c) -- THE ARTIFACT SAYS WHICH TRIGGER PRODUCED IT, IN BOTH BRANCHES

Four fields added to `tool_scalars`, all four present in the served bytes:

| field | served (automatic) | manual branch |
|---|---|---|
| `trigger_declared` | `scheduled` | `manual` |
| `trigger_measured` | `scheduled` | `interactive` |
| `trigger_agrees` | `yes` | `yes` |
| `trigger_chain` | 5 ancestors | 3+ ancestors |

**`--trigger` defaults to `manual`, and that direction is the safety property.** An omitted flag can
never read as automatic; a forgotten argument cannot manufacture the claim this cell exists to make
checkable.

**The declared value is paired with a measured one the caller does not choose.** A hand run that
passes `--trigger scheduled` publishes `trigger_agrees: no` -- exercised, not argued.

**`trigger_agrees` has a third value, `not-evaluated`,** for when the chain cannot be read. A
two-valued vocabulary would encode non-evaluation as a verdict -- a comparison that could not run
reading as one that ran and disagreed. This is the lesson the issuer carried out of my last report,
applied to my own code this time.

⚠ **SCOPE OF THE MANUAL HALF, STATED PLAINLY:** it is exercised **at the code path on a real
human-started process, not on a served artifact.** It is not exercised end-to-end because the
publisher's role is scoped to exactly one key (CTO ruling @`054353ac5e`), so the only available
end-to-end manual proof would be a hand publish to the served key -- the one act the bounds forbid.

---

## ARM (d) -- ADVERSARIAL: 8 PATHS, 5 CLOSED, 3 OPEN

The domain is built by **subtraction from a printed denominator** -- 18 gating fields read off the
live task object -- not from recall.

**CLOSED (5):** a logon trigger used as the cadence · a hand invocation required to publish · idle
requirement · battery policy on a laptop (`DisallowStartIfOnBatteries=False`,
`StopIfGoingOnBatteries=False`, both verified unmoved) · network-unavailable as a *gate* (the task
still fires; a network failure surfaces as a loud non-zero, not a silent skip).

**OPEN (3), named rather than omitted:**

1. **Interactive-only principal.** The device publishes nothing while nobody is logged on. **This
   is the whole remaining difficulty and it needs Andrew.**
2. **Device powered off or asleep.** `WakeToRun=False`. Inherent to the carrier the L4 ruling kept.
3. **S4U network credentials -- UNTESTED.** An S4U token carries none. This is why the elevated line
   must be followed by an **observed fire**, not by the write's own output.

---

## ARM (e) -- NOTHING ELSE MOVED

Proven as a comparison of the exported task definition before and after, **not asserted**:

- 42 lines before, 45 after. **Added 4:** `<Repetition>`, `<Interval>PT15M</Interval>`,
  `</Repetition>`, and the rewritten `<Arguments>`. **Removed 1:** the old `<Arguments>`.
- **Unexpected additions: 0. Unexpected removals: 0.**
- Principal `InteractiveToken` before and after -- **unmoved by design.**
- Scoped-role ARN, pinned session name and published key all unchanged in source. No new credential
  stored on the device. The drift question and its denominators untouched. The 26 h ceiling untouched.

⚠ **I avoided the `Set-ScheduledTask` full-replace trap by not using it.** Row `NFRA_OUTSET-S39`
records a two-field settings write that silently reverted both battery flags to restrictive cmdlet
defaults on a laptop. I re-registered from the **exported XML** instead, so every field in the new
definition is one I could diff -- the replace is total and therefore auditable, rather than partial
and invisible.

---

## ARM (f) -- THE TREE, AND NO NUMBER-GRADING

Measured in `C:/Users/AndrewBerman/Desktop/ajb_workspace`, branch `CLOUD`, positive control: the
battery's own path resolves inside the tree whose 31,840 tracked files are the printed denominator.

⛔ **NO ARM OF THIS BATTERY GRADES ON THE FIFTEEN-MINUTE NUMBER.** Andrew's word was *"maybe every
15 min"*, and the "maybe" makes it a target. An arm failing on 14 or 16 minutes would be grading a
constant he never fixed. The interval is **printed** (`PT15M`) and **not asserted**. What is graded
is that the cadence recurs and needs no human act.

---

## ⛔ THE CALL FOR ANDREW -- ONE ELEVATED LINE

**Measured this session, non-elevated, with a positive control on a FRESH task so the denial cannot
be "the existing task is locked":**

| principal form | result |
|---|---|
| `Interactive` (**positive control**) | **registers OK** |
| `S4U`, `AzureAD\AndrewBerman` | `Access is denied` |
| `S4U`, bare `AndrewBerman` | `Access is denied` |
| `GroupId BUILTIN\Users` | `Access is denied` |

The denial is specific to **every** "runs while logged off" principal, not to registration. This
confirms row `NFRA_OUTSET-S39` and adds the control that row could not run.

**THE LINE** -- one elevated PowerShell, run once:

```powershell
Set-ScheduledTask -TaskName "OpalOutsetDriftLaptop" -Principal (New-ScheduledTaskPrincipal `
  -UserId "AzureAD\AndrewBerman" -LogonType S4U -RunLevel Limited)
```

**THE ROLLBACK** -- one line:

```powershell
Set-ScheduledTask -TaskName "OpalOutsetDriftLaptop" -Principal (New-ScheduledTaskPrincipal `
  -UserId "AzureAD\AndrewBerman" -LogonType Interactive -RunLevel Limited)
```

⚠ **It must be verified by an OBSERVED FIRE, not by the write.** `Set-ScheduledTask` self-reports
success on a non-terminating failure (`NFRA_OUTSET-S39`), and an S4U token carries no network
credentials, which is untested on this box.

---

## `O28-AC2` -- JUDGMENT, RECORDED FOR `3.0.0_SA_CVO` AT L9. NO VERDICT.

**Which shape, and what I rejected:** shape (i), the recurring device-side timer, because the L4
ruling left no other carrier. Rejected beyond the withdrawn shapes: a logon trigger (would have made
arm (d) read better while making the mechanism worse), a `SYSTEM`/group principal (denied, and it
would move the credential source), and a hand publish to hold the report green (forbidden, and it
would have destroyed arm (a)'s evidence).

**Can a reader distinguish an automatic publish from a hand one, from the artifact alone?** **Yes,
and it is measured on a real artifact rather than argued** -- `trigger_chain` in the served bytes
terminates at `wininit.exe` through `services.exe` and `svchost.exe`, an ancestry a shell-launched
run cannot have. The same detector in a human-started process reads `interactive` on the same code.

**What human dependency remains, and what would remove it:** the interactive-only principal, removed
by the one elevated line above; the device being off, which no device-side carrier can remove; and
the S4U network-credential question, which only an observed fire under the new principal answers.

**Does my mechanism have a blind spot analogous to the commit-trigger one?** ⛔ **Yes, and it is a
different shape, so I name it precisely rather than claim symmetry.**

The commit trigger's defect was **anti-correlation**: it sampled when drift was lowest, so the
device most worth measuring published least. **Mine is not anti-correlated -- a quarter-hour timer
samples on wall-clock time, which is independent of how much drift exists.** The blind spot is
**correlated-with-presence** instead: the measure runs only while a session exists, and a session
existing is *positively* correlated with someone writing files. So my gap covers the hours when
drift is least likely to be changing, which is the **benign** direction of the same family.

⚠ **But it is the benign direction only for drift that ACCUMULATES, and I do not want that read as
a clean bill.** A long logged-out stretch is exactly the window in which a device that was left
mid-work sits with uncommitted material and reports nothing, and **an absent reading and a clean
tree still render the same way to the consumer** -- the quiet-versus-silent confusion `OS-s-21`'s
accept was re-cut to prevent. The 26 h ceiling is what converts that silence into a visible verdict,
and it is untouched. **The honest statement is that my mechanism narrows the window from 24 h to
minutes while someone is logged on, and does nothing at all when nobody is** -- and the second half
is the elevated line, not a property of the shape I chose.

**One further limitation of my own instrument, volunteered:** `_trigger_evidence()` returns
`interactive` as its **fallback**, not as positive evidence -- it is really "no scheduler ancestor
found". The positive half of the discrimination (`scheduled`) is genuine; the negative half is a
default. A future launcher that is neither a shell nor the Task Scheduler would be labelled
`interactive` on no evidence. `unknown` covers only an unreadable chain, not an unrecognised one.

---

## ARTIFACTS

| path | what |
|---|---|
| `infra/aws/ec2/outset-drift-device/publish_drift.py` | trigger disclosure: 4 fields, both branches |
| `…/deliverables/0.7.0_AE_CloudOps~W/test_os28_drift_is_continuous.py` | the battery, six arms |
| `…/deliverables/0.7.0_AE_CloudOps~W/os28_battery_run.txt` | full captured run, rc=0 |
| `…/deliverables/0.7.0_AE_CloudOps~W/os28_task.BEFORE.xml` | pre-state, sha256 `457E61C387D792E2…` |
| `…/deliverables/0.7.0_AE_CloudOps~W/os28_task.AFTER.xml` | post-state |
| `org/critical_paths/change_management/20260910T1820Z_outset-drift-continuous-15min_deploy.md` | deploy ledger entry |
