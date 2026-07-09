# NFRA_GLOBGRPH -- comp-kuzu `_canonical` rebuild-winner LIVENESS (design for CTO arch-gate)

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-09 · **Status:** DESIGN -- routed to CTO for arch-gate (COO DRIVE-dispatch 040904Z)
**Fixes:** #17 (the 2026-07-09 fabric-wide-stale incident I grounded 03:19Z)
**Lane:** graph-platform (CTO owns the arch); base 0.7.0 built the incremental refresh + grounded the incident.

## 1. The incident (grounded, not hypothetical)

Post the ~02:09Z nightly, a full-reload rebuild WINNER died mid-build: `kuzu_nessie_db.rebuild.lock` held 13 min + a partial `kuzu_nessie_db.rebuild.tmp` present + NO live rebuild process. Result: `_canonical.ensure_fresh` served the pre-nightly DB (pin 1661655592549182097, BEHIND the nightly HEAD 2511298265958053537) to EVERY comp-kuzu query, fabric-wide, until the 900s (15 min) orphan-steal would clear it. This is the highest-value staleness moment (right after the nightly full-reset) and it hit every agent's Rule-20 default surface. Manually clearing the died-winner lock+tmp let the next query rebuild clean. NOT caused by the incremental-refresh flag (it correctly returned rc=2 -> full-reload fallback on the nightly's large delta; the FULL `kuzu_nessie_load` is what died -- suspected box-load/OOM under the concurrent post-nightly comp-kuzu storm).

## 2. Current mechanism (`_canonical.ensure_fresh`, v0.4.1)

mkdir-mutex (`<db>.rebuild.lock`, atomic create) + build-to-`<db>.rebuild.tmp` + atomic `os.replace` SWAP. One winner rebuilds; losers wait `MUTEX_WAIT_S=180s` then serve the existing (TO-F1 labeled-BEHIND) DB. An orphaned lock is stolen only after `ORPHAN_LOCK_S=900s`. Two saving graces already present: (a) the served DB is LOUDLY labeled BEHIND in the provenance header (never silently-behind -- F1); (b) the atomic swap makes concurrent rebuilds safe (last swap wins; both produce the same HEAD DB; readers never see a half-built DB).

**The gap:** a DIED winner (crash/kill/OOM/wedge) between `mkdir(lock)` and the finally-`rmdir` leaves the lock held for the full 900s before any steal -> a 15-min fabric-wide BEHIND-served window.

## 3. Design -- three parts

### 3.1 Rebuild-winner HEARTBEAT (detect a dead winner in ~seconds, not 900s)
The WINNING agent (holds the lock + spawns the rebuild subprocess) writes a heartbeat while the rebuild runs: touch `<lock>/heartbeat` (or rewrite the lock dir mtime) every `HEARTBEAT_INTERVAL_S` (~20s) from a daemon thread that lives for the duration of the `subprocess.run(rebuild)` call. If the agent dies (the exact #17 case -- crash/kill/wedge), the heartbeat STOPS. The winner also writes its PID into `<lock>/winner.pid` (advisory -- PID-liveness is unreliable for detached native-Windows procs on this box, so the heartbeat mtime is the PRIMARY liveness signal, PID is a secondary cross-check).

### 3.2 Heartbeat-based STEAL (tighten the 900s window)
In the loser wait-loop, replace the fixed 900s age-steal as the PRIMARY with a heartbeat-staleness steal: if `now - mtime(<lock>/heartbeat) > HEARTBEAT_STALE_S` (~90s = ~4.5x the interval, tolerates a couple missed beats under transient load) -> the winner is dead -> steal the lock immediately + rebuild. Keep `ORPHAN_LOCK_S=900s` as an ABSOLUTE BACKSTOP (if the heartbeat file is somehow missing/unwritable, the old behavior still eventually heals). Net: a dead winner is detected in ~90s, not 15 min.

**Why aggressive stealing is SAFE (the key correctness argument):** a FALSE-POSITIVE steal (the winner was merely slow, heartbeat delayed) is HARMLESS -- the stealer and the slow winner both rebuild to the SAME nightly HEAD and the atomic swap is last-writer-wins on identical content; readers never see a partial DB (build-to-tmp). So the heartbeat threshold can be short without risking corruption -- the swap machinery already makes concurrent rebuilds safe by construction. (`_rm_kuzu(tmp)` before each build clears any partial tmp from the dead winner.)

### 3.3 FAIL-CLOSED-on-dead-winner (never silently-behind -- already partly true, hardened)
Today the served-BEHIND DB is already LOUD (F1 provenance "WARN: BEHIND Nessie HEAD"), so it is NOT silently-behind. The hardening: (a) 3.1+3.2 shrink the BEHIND-served window from 15 min to ~90s + rebuild time; (b) when a loser serves BEHIND because a rebuild is in-flight or just-stolen, the header should additionally note "rebuild in progress / dead-winner-stolen, refreshing" so a reader distinguishes "actively catching up" from "stuck"; (c) OPTIONAL escalation -- if the served DB age exceeds a hard ceiling (e.g. > 2 nightlies) AND no live rebuild heartbeat exists, escalate the header from WARN to a louder STALE-UNRECOVERED signal (the stuck-loop tripwire). Never a silent BEHIND.

## 4. Tunables (CONFIG, not literals -- per the leg-4 pattern)
`HEARTBEAT_INTERVAL_S` (~20s), `HEARTBEAT_STALE_S` (~90s), `ORPHAN_LOCK_S` (900s backstop, unchanged), `MUTEX_WAIT_S` (180s, unchanged). Surface them as module constants (env-overridable) so tuning against real data needs no code change.

## 5. Also route to CTO (the deeper question)
WHY did the full `kuzu_nessie_load` die? Suspected: box OOM/load from the concurrent post-nightly comp-kuzu storm (every agent's surface goes BEHIND at ~02:10Z simultaneously -> a thundering herd of rebuild attempts + the incremental_updater + other work). A complementary mitigation worth CTO's weigh-in: the winner, on a successful nightly-reset rebuild, could publish a "reset done" signal so losers reuse it rather than each attempting their own (already partly the mutex's job, but the herd stresses the box). The rebuild-winner-liveness (this design) is the primary fix; the herd/load question is a secondary follow-on.

## 6. Scope + non-goals
Scope: `_canonical.ensure_fresh` lock/steal/heartbeat only. NOT changing the rebuild content path (kuzu_nessie_load / kuzu_incremental_refresh unchanged), the atomic-swap, or the F1 provenance contract (only additive header text). Proceeds on its own merits -- NOT gated on the MSTR fan-out-freeze wedge investigation (separate concern; this is rebuild-liveness). Grounding done SEQUENTIALLY (no massive subagent fan-out, per COO's precautionary cap).

## 7. Ask
CTO arch-gate the design (esp. the heartbeat-steal-is-swap-safe argument in 3.2 + the header-escalation in 3.3). On GO, base 0.7.0 implements in `_canonical.py` + a self-test (simulate a died winner: acquire lock, write a stale heartbeat, confirm the next `ensure_fresh` steals in ~90s not 900s + rebuilds clean + never serves a corrupt DB). Flag-gate the new steal path if CTO wants a staged rollout. RAVC CTO + COO on the design; RAVC again on the implementation + self-test.
