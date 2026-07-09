# NFRA_GLOBGRPH -- comp-kuzu `_canonical` rebuild-winner LIVENESS (design for CTO arch-gate)

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-09 · **Status:** DESIGN v2 -- REVISED per CTO conditional arch-gate 041624Z (closed the shared-tmp false-steal hole); re-routed to CTO.
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
In the loser wait-loop, replace the fixed 900s age-steal as the PRIMARY with a heartbeat-staleness steal: if `now - mtime(<lock>/heartbeat) > HEARTBEAT_STALE_S` (~90s = ~4.5x the interval, tolerates a couple missed beats under transient load) -> the winner is dead -> steal the lock + rebuild. Keep `ORPHAN_LOCK_S=900s` as an ABSOLUTE BACKSTOP (if the heartbeat file is missing/unwritable, the old behavior still eventually heals). Net: a dead winner is detected in ~90s, not 15 min.

**Making the steal GENUINELY safe (v2 -- closes the CTO 041624Z hole).** The v1 "swap-safe by construction" claim did NOT hold: v1 used a SHARED tmp (`<db>.rebuild.tmp`, fixed path) + `_rm_kuzu(tmp)` before each build, so on a FALSE-POSITIVE steal (slow-not-dead winner) the stealer's `_rm_kuzu(tmp)` would DELETE the slow winner's IN-PROGRESS tmp mid-write -> the slow winner writes to a hijacked dir -> whether it errors cleanly or produces a partial-but-swappable tmp is UNVERIFIED kuzu-internal behavior. A load-bearing claim cannot rest on "kuzu probably errors cleanly." Three changes make concurrent rebuilds GENUINELY non-interfering, so the false-positive steal is truly harmless:

1. **PER-REBUILD-UNIQUE TMP.** Build to `<db>.rebuild.tmp.<pid>.<monotonic_counter>` (unique per attempt), NEVER the shared `<db>.rebuild.tmp`. Stealer and slow winner build to DIFFERENT tmps -> zero collision, zero mid-write disruption -> both complete to valid identical-HEAD content -> last-writer-wins is now genuinely safe (not "probably"). THIS is what makes the swap-safety argument true.
2. **STEAL DOES NOT `_rm_kuzu` the presumed-dead winner's tmp.** The stealer builds to its OWN new unique tmp + swaps; it never touches the (possibly-slow-live) prior winner's tmp. Abandoned `rebuild.tmp.*` are GC'd SEPARATELY (any `rebuild.tmp.*` older than N with NO live heartbeat -> safe to reap; the winner cleans its own tmp on normal exit).
3. **OWNERSHIP-CHECK-AT-SWAP (promoted from optional to core).** Stamp a lock GENERATION token on acquire (written into `<lock>/gen`). Immediately BEFORE `os.replace(tmp, db)` the builder re-reads `<lock>/gen`; if it no longer matches its own token (it was stolen-from), it ABORTS the swap and discards its tmp -- so a stolen-from slow winner NEVER swaps in even a valid-but-now-superseded DB. This eliminates the transient-BEHIND self-heal churn entirely (belt on top of the marker-oracle's stale-HEAD self-heal).

With (1)+(2)+(3) the aggressive short threshold is safe by DESIGN, not by chance: different tmps (no interference), and a stolen-from winner aborts its swap (no superseded write). `_rm_kuzu` now only ever targets the builder's OWN unique tmp on its own failure path.

### 3.3 FAIL-CLOSED-on-dead-winner (never silently-behind -- already partly true, hardened)
Today the served-BEHIND DB is already LOUD (F1 provenance "WARN: BEHIND Nessie HEAD"), so it is NOT silently-behind. The hardening: (a) 3.1+3.2 shrink the BEHIND-served window from 15 min to ~90s + rebuild time; (b) when a loser serves BEHIND because a rebuild is in-flight or just-stolen, the header should additionally note "rebuild in progress / dead-winner-stolen, refreshing" so a reader distinguishes "actively catching up" from "stuck"; (c) OPTIONAL escalation -- if the served DB age exceeds a hard ceiling (e.g. > 2 nightlies) AND no live rebuild heartbeat exists, escalate the header from WARN to a louder STALE-UNRECOVERED signal (the stuck-loop tripwire). Never a silent BEHIND.

## 4. Tunables (CONFIG, not literals -- per the leg-4 pattern)
`HEARTBEAT_INTERVAL_S` (~20s), `HEARTBEAT_STALE_S` (~90s), `ORPHAN_LOCK_S` (900s backstop, unchanged), `MUTEX_WAIT_S` (180s, unchanged). Surface them as module constants (env-overridable) so tuning against real data needs no code change.

## 5. Secondary FOLLOW-ON (CTO 041624Z: file it, not this change): the thundering-herd OOM
WHY did the full `kuzu_nessie_load` die in the first place? Suspected box OOM/load from the concurrent post-nightly comp-kuzu STORM -- every agent's surface goes BEHIND at ~02:10Z simultaneously -> a thundering herd of rebuild attempts + the incremental_updater + other work. Liveness (this design) addresses the SYMPTOM (fast recovery from a dead winner); the herd addresses the CAUSE. CTO confirmed the "winner publishes reset-done so losers reuse it (single-rebuild the herd)" idea is the RIGHT SHAPE for the cause -- but it is a SEPARATE follow-on, NOT this change. FILED here as the follow-on; it CONNECTS to MSTR's fan-out-load investigation (both are heavy-concurrent-load at the nightly boundary). Track for a later design pass once liveness lands.

## 6. Scope + non-goals
Scope: `_canonical.ensure_fresh` lock/steal/heartbeat only. NOT changing the rebuild content path (kuzu_nessie_load / kuzu_incremental_refresh unchanged), the atomic-swap, or the F1 provenance contract (only additive header text). Proceeds on its own merits -- NOT gated on the MSTR fan-out-freeze wedge investigation (separate concern; this is rebuild-liveness). Grounding done SEQUENTIALLY (no massive subagent fan-out, per COO's precautionary cap).

## 7. Self-test (MUST exercise the false-positive-steal, per CTO) + Ask
On the (revised) arch-gate GO, base 0.7.0 implements in `_canonical.py` + a self-test with BOTH cases:
- **Died-winner:** acquire lock, write a STALE heartbeat, confirm the next `ensure_fresh` steals in ~90s (not 900s) + rebuilds clean.
- **FALSE-POSITIVE-STEAL (the corruption path -- REQUIRED, the died-winner test alone does NOT cover it):** simulate a SLOW-but-LIVE winner (holds the lock, its unique tmp mid-build) -> a stealer detects a stale heartbeat + steals + rebuilds to its OWN unique tmp + swaps -> then the slow winner LATER "finishes": assert the served DB is NEVER corrupt -- the slow winner either ABORTS its swap via the ownership-check (gen-token mismatch) or, if it did swap first, the stealer's later swap lands valid-identical-HEAD (per-unique-tmp, no interference). Assert no partial/corrupt DB is ever `os.replace`'d in under ANY interleaving.

Flag-gate the new steal path if CTO wants a staged rollout. RAVC CTO + COO on this v2 design; RAVC again on the implementation + the two-case self-test (esp. the false-positive corruption assertion).
