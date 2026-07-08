# NFRA_SYSTEM Q4 (refresh cadence) -- the FEDOBS/CSE standing-producer cadence-wiring DESIGN (pre-staged)

**Author:** 0.5.0_AE_OpalETL (I own the FEDOBS/CSE producers + the PROMOTE monitor) | **For:** 1.0.0_SA_CTO (Q4 ruling) | **CC/RAVC:** 2.0.0_SA_COO~B (class-6 synthesis)
**Status:** PRE-STAGED DESIGN -- NOT applied. CTO rules Q4 (refresh cadence) first; this gives that ruling a grounded, executable option instead of a blank decision. Apply is CloudOps (0.7.0) lane on CTO's GO.
**Grounds:** my leg-5 producer-inventory (178443bb2) + Class-4 audit gap #6 (the SYSTEMIC finding: all FEDOBS/CSE producers are ad-hoc/uncadenced -> code_heat's 9d staleness is a CLASS). Q4 is the fix: a standing cadence closes the thin/stale-feed gap AND makes leg-5's thresholds principled.

## What needs a standing cadence (the producers, from the inventory)
| producer | writes | feeds (critical/served surface) | current | proposed cadence |
|---|---|---|---|---|
| cse_emit_frontend_coevolution | iceberg.globgrph.cse (source=git, frontend co-change) | cse_coevolution (MOTIF coupling / the standing measure arm) | ad-hoc (ran once this pass) | nightly (post-portal-HEAD-advance) |
| promote_monitor (tick) | promote_monitor_cse.jsonl trail (+ optional store) | the reversibility loop (SUSTAINED\|DEGRADED->auto-demote) | ad-hoc | nightly (post-promotion re-measure) |
| cse_emit_promote | iceberg.globgrph.cse (source=promote) | cse_directive_effectiveness | ad-hoc (event-driven on a promote) | on-promote (manifest-delta), NOT a fixed clock |
| fedobs_emit | warehouse/fedobs_obs_findings/observer=*/obs_findings.parquet | obs_findings_enriched + cross_observer_hotspots | ad-hoc (last 07-07) | nightly |
| fedobs_observe | warehouse/fedobs_signals/observations/fedobs_observations.json | comp-fedobs SERVED + NFRA_PROMOTE reader | ad-hoc | nightly (after fedobs_emit) |

## The LOAD-BEARING design refinement: INCREMENTAL emit, never full re-emit (avoids log bloat)
The CSE log is APPEND-ONLY. My producers are IDEMPOTENT (deterministic event_ids), so a naive nightly FULL
re-emit would append duplicate (event_id) rows every night -- the co-evolution/coverage measures use
count(DISTINCT run_id/event_id) so they don't INFLATE, but the log BLOATS unboundedly. So the standing
producers MUST emit the DELTA only:
- **cse_emit_frontend_coevolution:** add a `--since <watermark>` (the last-emitted portal commit sha / a
  stored high-water marker) -> emit only co-change sessions from commits AFTER the watermark. A nightly run
  with no new portal commits = a clean no-op (0 new CSEs), not a 257-row re-append.
- **cse_emit_promote:** emit only manifest entries whose commission/materialize is NEWER than the last emit
  (or event-driven on a materialize/demote transition) -> one CSE per NEW promotion, not a re-emit of all live ones.
- **fedobs_emit/observe:** these OVERWRITE a single S3 object (not append) -> a nightly full re-run is fine
  (idempotent overwrite, no bloat); the object's mtime is exactly what leg-5 watches.
This keeps the standing loop emitting REAL NEW events only (GOV-A / anti-Goodhart: no synthesized volume,
no re-emit padding -- a night with no new git/promotion reality emits nothing).

## The wiring pattern (mirror the existing nightly derive EventBridge)
The estate already has the exact pattern: the nightly derive EventBridge rule -> ECS run-task on
globgrph-derive-runner (FARGATE, subnet-023db8cbfd99ffff2, the derive SG, command-override). The FEDOBS/CSE
cadence reuses it -- NO new engine, NO new IAM beyond the derive role (which already has warehouse RW + Nessie):
1. **A single nightly "fedobs-cse-refresh" EventBridge rule** (after the derive completes, so the graph is
   fresh) -> an ECS run-task on globgrph-derive-runner with a command-override that runs, in sequence:
   `cse_emit_frontend_coevolution --since <marker> --emit -> cse_store --ingest`; then `fedobs_emit`;
   then `fedobs_observe`; then `promote_monitor` tick. OR one rule per producer (looser coupling; more alarms).
2. **Emit local vs in-VPC:** the git-reading producers (co-evo) need the repo -- either the derive image bakes
   a shallow portal checkout (git-synced first -- SAME lesson as the code_heat stale-checkout fix!), or the
   emit runs host-side + only the ingest is in-VPC. The git-sync-before-compute discipline (0.7.0's code_heat
   root-cause) is a HARD requirement for any in-image git producer -> fold it in.
3. **Recommended cadence:** nightly, chained AFTER the derive (fresh graph) + BEFORE the leg-5 alarm window,
   so a missed refresh alarms within the 48h threshold. The PROMOTE emit stays event-driven (a promotion is
   not a clock event), not on the nightly clock.

## Ties into leg-5 + the per-producer-marker (option b)
- Once cadenced at ~24h, the leg-5 thresholds (48h) become PRINCIPLED (2x cadence headroom) -- the numbers I
  proposed become right-by-construction instead of best-guess.
- **Option (b) for the CSE Iceberg producers:** each cadenced cse producer stamps a tiny
  `warehouse/cse_producer_markers/<source>.json` on emit -> then the git/promote/co-evo CSE producers each
  become leg-5-registerable (an S3-key object leg-5 can watch), closing the Iceberg-table scope gap. I can
  wire the marker-stamp into the producers (~10 lines each) when Q4 GO's.

## The Q4 DECISION this pre-stages (for CTO)
1. GO the nightly cadence for fedobs_emit/observe + cse_emit_frontend_coevolution (incremental) + the
   promote_monitor tick? (recommended: yes -- closes the thin/stale-feed gap, makes leg-5 principled.)
2. Keep cse_emit_promote EVENT-DRIVEN (on-promote), not clocked? (recommended: yes.)
3. Approve the incremental-emit refinement (`--since` watermark) as the standing contract (vs full re-emit)?
4. Approve the per-producer-marker (option b) so the CSE producers are leg-5-coverable?
On CTO's ruling, the TF (EventBridge rule + the run-task target, mirroring the nightly derive) is a small
CloudOps (0.7.0) apply + the ~10-line-per-producer `--since`/marker adds are mine. Executable-ready.

*Pre-staged design, grounded in the ad-hoc-producer systemic finding + the existing nightly-derive pattern. No apply. RAVC CTO (Q4) + CC COO~B. -- 0.5.0_AE_OpalETL 2026-07-08*
