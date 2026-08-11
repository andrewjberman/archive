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

- **BG practice fix (adopted, no machinery):** heartbeat at the top of each active turn,
  not once at launch. The defect was an unexercised existing API; the moratorium is untouched.
- **CTO question (queued):** should broker-side sweeps corroborate against agent_telemetry
  before acting on an absent/stale verdict? (An instrument-domain note, not a build order —
  nothing built without Andrew's word.)
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
