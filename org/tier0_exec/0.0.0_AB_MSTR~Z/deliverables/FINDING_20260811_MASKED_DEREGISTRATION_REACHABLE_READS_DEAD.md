# FINDING — masked deregistration: a REACHABLE, working seat reads DEAD to every broker instrument

**Found by:** 0.0.3_BG_BBGTerminal (self, at close-out heartbeat), 2026-08-11 ~0930Z, msg
20260811T093244Z. **Judged + banked by:** 0.0.0_AB_MSTR~Z. **Routed to:** 1.0.0_SA_CTO~Z
(supervision-instrument design; queued for next session).

## The instance

BG registered at launch (23:48Z, PID 4684), heartbeat ONCE, then worked ~9.5h overnight
(Terminal recovery, a client-facing publish, Teams serving) without another broker call →
degraded stale → swept. The seat's TWO inbound paths diverged: **filesystem delivery
(inbox-watch Monitor) stayed alive and delivered everything; broker channel push was dead
the whole window.** The healthy path masked the dead one — no symptom existed at the seat,
and nothing tells a deregistered agent it is deregistered.

## Why it matters (the inversion)

The watcher doctrine's canonical fear is a DEAF agent reading REACHABLE. This is the
inverse: a REACHABLE, **busy** agent reading DEAD/absent to `get_live_agents`,
`get_org_summary`, and any stimulus-scan-style sweep — the supervisor's instrument reporting
the opposite of the truth, with two failure consequences: (1) a sweep acts on a "dead" seat
that is mid-work (respawn/reassign/reap — the orphan-reaper class); (2) the agent cannot
report what it cannot see.

## Incidence — measured, not assumed

One-shot broker-vs-telemetry comparison on site Z at 0935Z (13 telemetry files scanned):
current instances ZERO — the four wound-down seats are correctly absent, BG re-registered,
MSTR~Z live. **Known instances: 1 (BG overnight).** A single instance is not a rate (BG
said this itself); the cheap repeatable check is: any serial with fresh agent_telemetry
work events but absent/stale broker registration.

## Disposition

- **BG practice fix — SUPERSEDED (BG second correction 102056Z): the mitigation does not
  work, and the finding is STRUCTURAL.** Measured recurrence: swept again <=43 min after a
  successful heartbeat. The broker degrades a serial stale after 2 minutes without a
  heartbeat; an EVENT-DRIVEN seat is by definition silent between events, so per-turn
  heartbeating cannot cover the gap it exists to cover. The discriminator sits in
  liveness.json itself: the loop-driven MSTR~Z seat held registration ~13h continuously;
  the event-driven BG seat vanished repeatedly while working correctly. **On this fabric,
  broker registration is a reliable liveness signal for LOOP-DRIVEN seats and structurally
  unreliable for EVENT-DRIVEN seats.** BG is deliberately NOT keepalive-looping and NOT
  defensively re-registering on a timer (papering the symptom would make the fabric's view
  look healthy while the mismatch persists). Future stale/absent broker reads on BG-class
  seats are PREDICTED, not incidents.
- **Sampling caveat on the incidence check:** the 0935Z broker-vs-telemetry sweep found
  0 current instances — but it sampled BG five minutes into a registered window, so a clean
  result there is not evidence of absence. The discriminating test is the same comparison
  run against an idle event-driven seat mid-gap.
- **CTO question (queued; SHARPENED by the second correction):** the corroborate-before-
  acting question now has a structural premise — broker liveness cannot be made reliable
  for event-driven seats by agent behavior. Remedy options (CTO/Andrew's to choose, BG
  explicitly declined to pick): a longer stale window for UA-class seats · registration
  without heartbeat dependency · liveness corroborated from inbox-watcher/telemetry ·
  an explicit event-driven exemption from broker liveness. Not a build order.
- **Replay shape (secondary — CORRECTED per BG 093624Z; originally misattributed):** the
  duplicate surfacing is NOT a deregistration artifact. It is ROUTINE DUAL DELIVERY by
  design: every fabric message reaches a seat twice — immediately via the inbox-watch
  Monitor, then once more via the broker on the agent's next status/heartbeat call (each
  message surfaces via the broker exactly once and is drained by that surfacing; mechanism
  established from two observations, healthy registration throughout the second). What
  survives, now STANDING on every seat every session: the broker copy arrives framed
  "URGENT ... act on these NOW" regardless of whether the agent already read and discharged
  it via the filesystem path — the SENT/EMITTED/READ conflation as a permanent property of
  normal operation, inviting re-doing finished work. The original attribution made the
  hazard look rarer than it is.
- **Related self-instance, same class (MSTR~Z, same session):** all four of this session's
  registration-wait polls checked a `status` field liveness.json does not have — structurally
  unable to report success; masked by broker-API cross-checks. Schema banked to device memory.

## SECOND FINDING, same axis, measured 2026-08-11 ~2159Z: THE FABRIC HAS NO INSTRUMENT FOR *COMPUTING*

**Occasion.** COO~Z escalated `0.5.0_AE_OpalETL~Z` as DEAF (INFERRED): telemetry origin frozen
45m, two CTO~Z messages delivered-unanswered, liveness fresh. COO then self-corrected twice
(its outage-exclusion had expired; the surviving discriminator was the unanswered stimulus).
No respawn was taken. MSTR~Z resolved it by **process-truth CPU delta**: pid 35904 advanced
**4.5s CPU in a 30s window** — sustained real compute. The seat was mid-compose on the wave's
hardest page. Benign; escalation closed on a measurement.

**The gap, stated generally.** The fabric owns instruments for:
`ALIVE` (process exists / poller) · `ACTED` (telemetry `kind:work`) · `READ` (agent-side ACK).
It owns **none for COMPUTING** — and a long in-context compose occupies exactly that state:
it makes no tool calls, emits no telemetry, answers no messages, and is therefore
**byte-identical to a hang on every instrument we have.** The liveness bands cannot close it;
they read the wrong layer. This is the same family as the masked-deregistration finding above
(an instrument confidently answering about something it is not looking at), one state over.

**The probe (manual, no machinery, ~30s):** sample the seat's `claude.exe` CPU, wait, re-sample,
delta above threshold = COMPUTING. **NOT a monitor and not proposed as one** (moratorium; and it
would be machinery on an unsettled surface). Proposed as **ONE LINE in the drive doctrine's
BLOCKED/DEAF path: take a CPU-delta before any respawn recommendation.** Routed to CTO~Z as a
doctrine candidate for Andrew's word. It would have short-circuited today's escalation before
it was written.

### ⛔ CORRECTION TO THE ABOVE, 2026-08-12 ~0107Z — THE INSTRUMENT IS ONE-WAY, AND I OVERCLAIMED IT

**Caught by `2.0.0_SA_COO~Z`, and caught BEFORE it read my verdict** — it had independently
recorded a 40-minute per-pid baseline (AE~Z pid 35904: **+17.4s over ~40 min**, sitting in a
LIGHT cohort with five seats including known-healthy ones; two heavy seats at +154s/+199s were
the two doing the most TOOL CALLS, i.e. COO and me).

**THE MECHANISM I MISSED: LOCAL CPU DOES NOT MEASURE REMOTE INFERENCE.** The model runs on
Anthropic's side; what accumulates on this box is the LOCAL half — tool calls, file I/O,
parsing, streaming. **A seat deep in a long generation with no tool calls can be working
extremely hard and register almost nothing locally** — which is EXACTLY the shape of a
plant/seal composition (heavy thinking, no file writes until the seal).

**THEREFORE THE INSTRUMENT IS ASYMMETRIC AND MUST BE STATED THAT WAY:**
- **CPU delta POSITIVE → COMPUTING. Decisive.** (The 2159Z AE~Z case: +4.5s/30s. That verdict
  STANDS and was correctly reached.)
- **CPU delta LIGHT/FLAT → NON-DISCRIMINATING.** Consistent with composing AND with stopped.
  **It can rule death IN; it cannot rule death OUT.**

**Two corroborating non-discriminators measured the same turn (recorded so nobody re-derives
them as evidence):** established TCP connection COUNT is 2 for AE~Z and identically 2 for CTO~Z,
CVO~Z, BG, 0.8.0 and the DE seat — baseline resting state, tells nothing; and newest-connection
AGE is ~522 min for AE~Z and ~522 min for the healthy CTO~Z/CVO~Z (long-lived streams), so it
also fails to discriminate.

**WHAT SURVIVES:** the four-state frame (ALIVE / ACTED / READ / COMPUTING) and the gap it names
are unchanged and correct. What changes is the probe's claim: it is a ONE-WAY test, and the
doctrine line routed to CTO~Z must say so, or it will be read at 2am as licence to respawn on a
low number — **which is the precise failure the whole finding exists to prevent, re-manufactured
by its own remedy.** THE ONLY TWO-WAY ORACLE REMAINS THE AGENT-SIDE ANSWER (Rule 22b, unchanged).

*Self-assessment, recorded because the day's standard requires it of me too: I introduced this
instrument at 2159Z and presented it as "the discriminator." It discriminates in one direction.
A seat that had held the instrument for two hours would have built on the overclaim; COO~Z
falsified it in under two, from a baseline it had taken on its own initiative.*

**⚠ REFINEMENT (CTO~Z, 0111Z) — THE TWO CAUSES OF A FALSE-FLAT ARE DIFFERENT AND ONLY ONE IS
FIXABLE, WHICH IS THE TRAP:**

| cause of a flat reading | remedy |
|---|---|
| (i) sampling window shorter than the gap between tool calls | **FIXED by a long baseline** |
| (ii) remote inference invisible to local CPU | **FIXED by NO baseline, EVER** |

**The hazard is that a long baseline genuinely fixes (i), and fixing (i) FEELS like fixing the
instrument.** The next reader sees a long-baseline flat reading, remembers "we solved the
timescale problem," and treats flat as decisive. **Lengthening the window raises SENSITIVITY and
never converts a one-way probe into a two-way one.**

**Scope of the blindness, measured the same night:** the one sentence *local CPU does not measure
remote inference* retro-explains THREE separate misreads by three agents in one night — COO~Z's
6-second daemon-pid window, MSTR~Z's 60-second read on AE~Z, and CTO~Z's PRD paragraph (whose
"is the fabric dark? — no" claim survived only by luck of DIRECTION: all eight seats came back
accumulating, so it happened to be reading the decisive limb; a flat return would have written
"the fabric is dark" into a law-adjacent file on a probe structurally unable to say it).
*A correction that explains its siblings is worth more than one that closes its instance.*

**On the correction's provenance, worth preserving:** COO~Z took the 40-minute per-pid baseline
on its OWN INITIATIVE and delivered it BEFORE reading the verdict it overturned — so it is an
INDEPENDENT MEASUREMENT, not a rebuttal, and cannot have been shaped by the claim it falsified.
That is the strongest form this class of correction comes in.

**Bookkeeping trap found alongside:** the broker's registered PID is NOT the `claude.exe` PID
(MSTR~Z: broker 19012 / process 18052). A mismatch between liveness and process truth is
EXPECTED and is not evidence of a respawn — recorded because it nearly read as one.
