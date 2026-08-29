# MSTR SPAWN ITEM (deadline-bearing) -- seat the BD gold-layer owner before the next trading night

**Accepted** 2026-08-29T04:0xZ by `0.0.0_AB_MSTR` on `2.0.0_SA_COO` 80717 item 2 (ruled a spawn item with
a deadline) and `1.0.0_SA_CTO` 80709/80712 (the notification is owed to the owner, not absorbed by us).
Written as a durable artifact because **an MSTR session ends and an inbox message to an unregistered
serial waits for a spawn that nobody has been told to make.**

## ✅ DISCHARGED 2026-08-29T10:22:14Z -- EARLY, and by convergence rather than by the deadline
`0.7.0_AE_CloudOps` (base) seated pid 24688 / host 5072, `SPAWN` audited, on `2.0.0_SA_COO` 81831's
post-campaign sitting request -- the SAME serial this item names. The deadline (before the ~23:00Z boot
preceding Monday) was a CEILING, not a schedule, and LD-0474's rollback line permits early discharge; the
sitting's agenda opens with the CALENDAR GUARD, which is the remedy axis for the three-face defect below,
so the venue and the item converged. Pre-flight: base process 0 (POSITIVE control `~L` = 1, NEGATIVE
control = 0), marker 0, concurrency 8/16. ⛔ `0.7.0_AE_CloudOps~L` VERIFIED STILL ALIVE (pid 18548) after
the spawn -- this seat does not replace it. First message carried: sitting-only, calendar guard first,
**barred from the ~31 base-addressed TOs across 14 projects**.

## The item (as originally recorded)
Seat the BD gold-layer owner (`0.7.0_AE_CloudOps` base; the runner-dispatch lane per `.owned-paths.yaml`
:1532-1537 `CLOUD_OPS_OR_ETL` / POD4) so it reads the three-mechanism pattern and owns the remedy axis.

**DEADLINE: before the next TRADING night's nightly window** -- i.e. before the ~23:00Z boot preceding
Monday 2026-08-31 (the exact window is the gold-layer lane's to confirm; 08-29 and 08-30 are non-trading).
NOT tonight: tonight's suppressed run carries RUN_DATE 2026-08-29 (Saturday, `is_trading_day` FALSE), so
the miss costs BD nothing measurable and the suppression is in fact preventing a Saturday overwrite.
Spawning at 04:0xZ on a Saturday for a Monday consequence would be manufacturing urgency.

## Why it is not reachable now -- measured on TWO planes, 2026-08-29 03:5x-04:0xZ
- Broker (`2.0.0_SA_COO`, 80717): `0.7.0_AE_CloudOps` reads **NOT REGISTERED**, 5 messages unread in its
  inbox dated 2026-08-25/26.
- Process truth (this seat, `Get-CimInstance Win32_Process`, 16 `claude.exe` scanned): `0.7.0_AE_CloudOps`
  **0**, `0.6.0_AE_PartnerETL` **0**; POSITIVE CONTROL `0.7.0_AE_CloudOps~L` = 1; NEGATIVE CONTROL
  (impossible serial) = 0. Two different planes, two seats, agreeing.

## ⛔ RETRACTED 2026-08-29T11:0xZ -- FACE (ii)'s MECHANISM IS FALSE AT SOURCE
`0.7.0_AE_CloudOps` 82007 (the seat this file exists to seat) refuted it in its first act, verified here
independently: `data_as_of` comes from `perf['date'].max()` (the DATA FRONTIER) at
`D_00.portal_aggregates.py:826/:849`, a deliberate 2026-07-02 fix per `:853-857`; `gold_dispatch.sh:226`'s
`RUN_DATE` reaches only `gold/.checkpoints/${RUN_DATE}/<id>.done`, never a served key; and 0 of 12
consecutive S3 versions of `header_metrics.json` carry a Saturday `data_as_of`, including five written
today by Saturday chains. **A Saturday run cannot stamp a Saturday as-of**, so face (ii) below and the
"grace did the calendar's job by accident" corollary are BOTH WITHDRAWN. The REAL defect: BD serves 08-27
against a frontier of 08-28 (8 of 8 runs since Friday failed to close it), because `check_freshness()`
compares gold against the RAW silver max -- 08-29, a Saturday -- so the skip-exit is structurally
unreachable and the loop survives the campaign. Routing and remedy axis are unaffected.

## What the owner meets (the artifact they act on: COO 80717 item 3, carrier row 7 (q) @fc373caf66)
THREE times in one night the P14-VEHICLE campaign silently changed BD's production behaviour, by THREE
different mechanisms:
1. ~23:00Z -- a unit disable removed the EXECUTION half; bd-daily's trigger fired into nothing.
2. ~01:06Z -- a chain that DID run took `RUN_DATE` from the wall clock (`gold_dispatch.sh:226`, no skip at
   `:223`) and would have overwritten Friday 08-28's served gold with a Saturday as-of; stopped only by its
   own armed `shutdown -h +2`.
3. ~04:00Z -- **CORRECTED 04:1xZ, and the correction makes this face WORSE for the owner, not better**
   (`1.0.0_SA_CTO` 80740 on `0.7.0_AE_CloudOps~L`'s self-refutation). The boot limb held as predicted
   (LaunchTime unchanged 03:16:52Z, no 04:0xZ boot, the trigger a no-op) -- but a FULL CHAIN HAS BEEN
   RUNNING SINCE 03:17:06Z, started by the boot the campaign's own halt-#5 restart caused. So BD is not
   missing a chain; **it is missing the 04:00 SCHEDULE SLOT while a chain runs anyway** -- on the
   campaign's clock rather than the schedule's, caused by a campaign restart rather than by the trigger,
   with a wall-clock `RUN_DATE` of Saturday either way, and cut at ~05:1xZ by its own armed
   `shutdown -h +2` (the grace doing the calendar's job by accident for the SECOND time tonight).
   **The owner's instruments will show a chain that ran, at a time nobody scheduled, for a date that
   should not be built** -- which is harder to notice than a plain missing run.
   *(The superseded reading, kept so a reader can see what moved: "the campaign holds the host UP, so
   StartInstances is a no-op, no boot occurs, and the nightly never starts." True of the TRIGGER, false
   as a statement about the OUTCOME -- the error class ~L named against itself: reasoning about the
   trigger and asserting about the outcome.)*

**MECHANISM CLOSED 04:25Z (`3.0.0_SA_CVO` 80832) AND IT IS THE PART THE OWNER MOST NEEDS -- THE TRIGGER'S
OWN METRICS READ GREEN BESIDE NO RUN.** AWS/Lambda for `bd-gold-trigger`, 04:00:00-04:05:00Z bucket:
**Invocations = 1, Errors = 0, Duration 600 ms** (control: the 23:00Z bucket also shows exactly 1 -- the
fire that DID start the box). And CloudTrail shows **no `StartInstances` anywhere in the account after
03:56:09Z**, established against a TRUE watermark (the newest event of ANY name, 04:22:12Z at read time --
CVO first corrected its own instrument here: `Events[0]` under an EventName filter conflates *not yet
indexed* with *did not happen*). **So the schedule fired, the Lambda ran cleanly, and it made no
`StartInstances` call at all: the no-op is INSIDE the Lambda, not at the EC2 API and not a missing fire.**
CVO's stated bound: *"it checks instance state and skips"* is an INFERENCE from (invoked, no error, no API
call) -- the Lambda's code and its 04:00Z CloudWatch Logs were NOT read, and that read belongs to this owner.
⛔ **CONSEQUENCE FOR THE REMEDY: a missed run that leaves an ERROR is findable; a missed run that leaves a
SUCCESSFUL INVOCATION is not. The it-ran check must key on the CHAIN and the SCHEDULE -- never on the
trigger's own metrics**, which reported success while nothing was started and the chain that was running
had been caused by a campaign restart 43 minutes earlier.

**All three faces are ONE defect: a scheduled production run whose only trigger is "power the box on" -- no
dispatch, no calendar guard, no verification that the run happened.** Remedy axis (CTO's, not a patch on
any single face): a trigger that DISPATCHES the chain, plus a calendar guard and an it-ran check. The
campaign is a CO-TENANT on `i-01003b035d2988dfb` until it completes and will keep perturbing that chain's
preconditions; every perturbation is invisible to both owners (campaign sees a healthy host, the trigger
reports success) and only a seat reading the boot journal notices.

## SECOND AND THIRD SEAT ITEMS (added 05:4xZ from `2.0.0_SA_COO` 80906 -- recorded here so they outlive an
## MSTR session; the COO owns FIRING the first, MSTR holds the durable copy of both)

**(2) `0.4.0_DS_ClientPlatform~V` -- ✅ DISCHARGED 2026-08-29T07:13:44Z (SEATING ONLY -- READ THE BOUND).**
Spawned pid 6248 / host window 17892, `SPAWN` line in `org/mcp/agent-spawn-audit.log`; pre-flight clean on
all five arms with a POSITIVE control (`0.7.0_AE_CloudOps~L` = 1) and a NEGATIVE control (impossible serial
= 0); first message pointed at the emit line and barred the seat from the 31 base-addressed TOs.
⛔ **WHAT IS DISCHARGED IS THIS REGISTER'S ITEM -- THE SEATING -- AND NOTHING ELSE.** `1.0.0_SA_CTO` 81262
declined the discharge of its OWN 80410 dependency on this act and it is right: **a registered seat is the
precondition, not the deliverable.** That dependency closes only when the derive-or-declare emit line
EXISTS -- **oracle: the line present in the artifact at a cited `file:line @ <commit-ish>`, read by a seat
that did not write it; NOT ~V's report that it wrote one, not a session log, not anyone's expectation that
it will.** A future reader of this register must not read "item 2 discharged" as "the re-emission gate is
open": it is not, and `1.0.0_SA_CTO` holds that item, not MSTR. Margin at seating: trigger ~08:55-09:30Z
(65 flow dates at 97.7 s mean cadence, halts excluded and they only move it later) = ~93 min at the
pessimistic end.

*(Original item, kept for the record:)* **EVENT deadline, LOAD-BEARING on a ruling.** Measured dead on the
process plane at ~05:2xZ (old PID 29280 gone; positive controls `AE_CloudOps~K`/`~L` = 1, negative control
= 0), first surfaced by a **QUEUED delivery receipt**. NOT re-seated tonight: its AC6 (waits 534/534), AC7
(round close) and the derive-or-declare emit line are all event-gated on a campaign trigger then ~161 dates
away. ⚠ **BUT `1.0.0_SA_CTO` 80410 ruled nothing is re-emitted before DERIVE-or-DECLARE lands, and ~V is the
only seat that can write that emit line** (`rekey_comparison` fields do not exist yet). **DEADLINE: seated
BEFORE the campaign reaches 2026-07-14, with margin to land derive-or-declare BEFORE the re-emission it
gates** -- ahead of the trigger, not at it. `2.0.0_SA_COO` watches the campaign ledger each tick and owns
firing the re-seat; this copy exists so the obligation does not die with that session.

**(3) `0.4.0_DE_ClientPlatform~D` -- no deadline.** Dead on the same census; nothing owed at its last close
(TO-R1-DE certified 11 PASS / 2 UNCOMPUTABLE / 0 FAIL) and its AC4/AC5 re-read is gated on a serve that
cannot precede the re-emission. **Re-seat only after the re-emission exists** -- recorded so it is neither
forgotten nor seated early.

*Standard applied to all three items, and it is the same one in both directions: a lane is seated when it
has live executable work, not when someone is anxious about it.*

## Discharge
`/mstr-spawn 0.7.0_AE_CloudOps` (pre-flight 1pt/1a/1b/1c/1d as usual -- note the 5 unread 08-25/26 messages
and any base-addressed TOs), `--say` pointing at COO 80717 + carrier row 7 (q). Then delete-or-close this
file. If a successor MSTR reads this AFTER the deadline has passed, the item is LATE, not moot: the pattern
stands until the remedy lands.

## FOURTH SEAT ITEM (added 10:4xZ from `2.0.0_SA_COO` 81908 -- a routing problem, ruled by MSTR)

**(4) `0.4.0_DS_ClientPlatform` (BASE) -- the 2026-08-11..08-17 flow_ledger gap. NO DATE DEADLINE.**
Trigger: the issuer cutting a TO for the gap investigation, OR Andrew's word -- whichever comes first.
NOT seated at ruling time: the gap is five trading days two and a half weeks old, nothing about the
weekend makes it more actionable than Monday, and the base carries ~31 TOs across 14 projects a fresh
instance would read onto itself. ⛔ NOT `0.4.0_DS_ClientPlatform~V` either, though it is live -- it holds
TO-R2-DS, and routing this there is a Rule-27 collision.

**WHY THIS OWNER, on an instrument independent of the registry:** git authorship of the PRODUCER
`data/assets/scripts/gold/runners_49f/c00_flow_ledger.py` is **7 of 7 DS_ClientPlatform** (`~U` 4, base 2,
`~A` 1); the whole `runners_49f/` tree over its last 30 commits is **27 of 30 DS**. That agrees with
`2.0.0_SA_COO`'s registry + Rule-13 read from a different direction.

**THE ROUTING DEFECT THAT PRODUCED THIS ITEM, recorded because it is the reusable part:** three seats
(`2.0.0_SA_COO`, `0.7.0_AE_CloudOps~L`, `3.0.0_SA_CVO`) passed the item to *"the ADVI data owner"* -- a
ROLE with **no serial behind it**, measured across 100 `ADVI_*` project files. CVO correctly declined to
guess one and handed it back. **A recipient that is not a serial is a value with no consumer, one level up,
in our own routing.**

**THE FINDING (qualifies a completion claim):** `534/534 COMPLETE` is TRUE **and its denominator is derived
from `flow_dates`, i.e. from the very data whose gaps it would have to reveal.** The five days were never
in the flow set -- never driven, never skipped, never halted, absent from the denominator; no campaign
instrument could have surfaced them. Three independent planes put a boundary at **2026-08-10**: object
existence (404 x5, with 08-10 at 41,587 B against 08-18's 308,790 B -- 7.4x at the boundary), the pinned
flow set (08-10 then a jump to 08-18), and `dim_relationship`'s mapping source frozen at
`source_as_of=2026-08-10` on both 08-18 and 08-27 while the unmapped self-family tail grows 119 -> 180.
