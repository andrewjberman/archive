# BR1 EXECUTION PLAN -- retire inf-bronze-runner (i-083ad9ae297f88e9f), Lambda leg becomes sole writer

**archetype:** COORDINATE
**Author:** 0.4.0_DS_ClientPlatform -- 2026-08-04 ~04:3xZ
**Authority chain:** Andrew-direct ruling @6f4ad98db (+@83beb6ddc) -> COO GO 042235Z (BR1
re-scoped, three hard gates) -> CTO concurrence 042600Z (re-source; lane split; Eclipse-first)
+ CTO added condition (schedule floor named per sentinel consumer).
**Closes:** registry named-risk R-1 (dual-writer bronze keys unattributable-by-construction).

## GATE 1 -- ECLIPSE REHOME (first; hard acceptance = parallel-run field-exact)

- **Build:** new Lambda (AE names/TF; working name `inf-api-eclipse`) on the standard light
  pattern: 5 REST calls (`/v1/portfolio/portfolios/simple`, `/v1/portfolio/portfolios`,
  `/v1/modeling/models`, `/v1/modeling/models/{id}` x9, auth via `/v1/admin/Token`
  exchange); JWT ladder mirrors the existing puller (Secrets Manager
  `orion/eclipse_jwt/current` -> dynamic exchange from the Orion JWT). Emits the SAME
  bronze grammar incl. `_meta/pull_complete.json` with `rows_per_artifact` -- the monolith
  silver converter's SIDECAR_RECONCILED completeness depends on it (mirror_conversion.py
  docstring), so the sidecar is part of the contract, not optional.
- **Schedule:** EventBridge Scheduler cron ~13:30 UTC daily (matches the box's current
  landing window; the downstream mirror/converter cadence is unchanged).
- **Overlap validation (the hard acceptance):** N >= 5 trading days BOTH paths running.
  **The new Lambda writes to a staging prefix (`bronze/eclipse_qa/{date}/`), NEVER the
  production key during overlap** -- recreating a dual-writer on the production key for
  the cutover would rebuild R-1 inside its own fix. Per-day compare: field-exact JSON
  diff per artifact class + sidecar row-count equality vs the box's production output.
  Any divergence = STOP, diagnose before the clock continues. Eclipse is the
  permanent-gap vendor class: the box keeps writing production until Gate-3 cut day.
- **Cut (executed inside Gate 3):** same change window -- Lambda flips to the production
  key AND the box stops. No interval where both or neither write production.

## GATE 2 -- SENTINEL RE-SOURCE (+ the CTO condition: floors named per consumer)

- **Chosen shape (CTO-concurred): re-source.** A single dedicated completion-emitter
  Lambda (working name `inf-bronze-complete-emitter`) on cron ~14:45 UTC: verifies the
  day's REQUIRED-dim key set exists under `bronze/orion-api/{date}/` (the same
  required-dim contract the orchestrator enforces today, ported), then emits
  `_BRONZE_COMPLETE.json`. Single writer of the sentinel, schedule-floored by
  construction, no new event coupling. Incomplete day = NO sentinel + loud log
  (the absence is the signal; no alarm build -- moratorium).
- **Schedule floors per consumer (CTO added condition -- the sentinel is an ACCELERATOR;
  a consumer whose only trigger is the sentinel is the NEVER#4 defect one layer down):**
  1. `inf-assets-trigger` / gold runner: **existing floor CITED** -- EventBridge
     `inf-canonical-prices-daily` cron 14:00 UTC also starts the gold runner via
     `inf-gold-trigger` (estate-grounded; AE verifies the rule live at implementation).
     Sentinel remains the accelerator; the 14:00 cron is the floor.
  2. `inf-silver-chain`: **new floor SPECIFIED** -- a scheduled invocation ~15:15 UTC
     that runs the silver conversion for {date} if not already run (idempotent; skip-if-
     converted). AE implements alongside the emitter. Until it exists, Gate 2 is not
     "live + exercised."

## GATE 3 -- TEARDOWN LAST (destructive-class; human word)

- Preconditions: Gate 1 overlap PASSED + production cut executed; Gate 2 emitter + both
  floors live AND exercised (one real scheduled cycle observed end-to-end: dims -> sentinel
  -> silver -> gold, plus one floor-path exercise).
- **The stop is destructive-class: Andrew/COO human confirmation required** (standing
  autonomy law). Sequence: disable `opal-inf-bronze-runner-cron` (13:30 trigger) ->
  stop-instance (STOPPED, not terminated -- the instance is the rollback path for M=14
  days) -> TF retire of the rule + inf-bronze-trigger at AE's hand -> deploy-completion
  ledger opened at cut start, closed same session (NEVER#7 finish-or-rollback).
- Rollback at any point: re-enable the cron + restart the box; the Lambda staging path
  is torn down or re-pointed; ledger records which.

## LANES (per COO GO + Rule 13 verbatim)

| Seat | Owns |
|---|---|
| 0.4.0_DS (me) | this plan; puller/emitter SCRIPT CONTENT; overlap-compare harness + verdicts |
| AE lane (COO names the seat) | Lambda TF/infra, EventBridge rules/floors, IAM, TF retirement |
| COO | implementation TOs cut from this plan; RAVC closes |
| CTO | gate concurrences already given; Gate-2 floor verification; final gate reviews |
| Andrew | the Gate-3 stop word (destructive-class) |

## Acceptance summary

G1: >=5 trading days field-exact overlap, zero unexplained divergence, cut executed with
no production dual-write interval. G2: emitter + BOTH floors live, one full scheduled
cycle + one floor exercise observed. G3: box stopped on human word, TF clean, ledger
closed, R-1 registry row updated to RETIRED-WRITER-B with this plan cited.

---

## AMENDMENT 1 (2026-08-04 ~20:1xZ) -- Gate-2 floor row 1 re-shaped: the dead citation replaced by a NEW GUARDED FLOOR (GF-1)

**Frame:** CTO ruling 200314Z on AE's phase-1 stop (their live verify caught row 1's cited
floor wrong on BOTH values). Option (a) -- re-enabling `inf-canonical-prices-daily` -- is
DEAD: the disable is DELIBERATE, declared in TF with the 07-13 triple-ratified reasoning
(@b7bce51bd: an UNGUARDED `{mode:full}` re-derive racing the dispatch lock, won by ~16
minutes daily by luck; "prose governs an agent; it cannot govern a scheduler"). Nobody
re-enables it.

**The mis-cite, owned (plan-author):** row 1 cited "cron 14:00 UTC" ENABLED-implied from a
DESIRED-state read; live state is cron(47 14) and DISABLED. The row's own "AE verifies the
rule live at implementation" clause is what caught it -- correct stop, but the clause
DEFERRED the live read instead of making it at authoring time, letting a wrong citation
live in the plan for a day. The citation-discipline rider (below) closes that class.

**GF-1 -- the NEW GUARDED FLOOR for the gold-runner consumer (replaces row 1):**
- **Schedule-anchored:** an EventBridge cron ~15:30 UTC (after the Gate-2 emitter's ~14:45Z
  sentinel window; exact minute AE's, off the :00/:30 fleet marks) -- a floor IS a
  schedule (NEVER#4).
- **Data-state-GUARDED:** the floor invocation verifies input state BEFORE dispatching --
  the day's `_BRONZE_COMPLETE.json` sentinel (or the same required-dim contract the
  emitter checks, re-verified) AND silver-converted state for {date}. NO blind
  `{mode:full}` re-derive, ever -- the exact hazard that killed the old rule.
- **Lock-COMPOSING, not racing:** idempotent skip-if-already-run (the day's gold outputs
  present = exit 0 quietly) + gate-before-fire (the F-B stage-0 exp-gate pattern, tonight's
  in-estate precedent). The floor can only ever START work the sentinel path did not
  already start; it can never run beside it.
- **BR1-SIZED (criterion 4, stated honestly):** GF-1 floors the ONE consumer BR1's
  sentinel serves, using the SAME pattern as floor row 2 (the ~15:15Z idempotent
  silver-chain floor AE already implements) -- an increment to already-planned Gate-2
  work in the same AE lane, not a chain redesign. **THE BIGGER ITEM IS CARVED OUT:** the
  INF chain has been deliberately floor-LESS since 07-13 and the 08-03 no-cycle gap is
  that condition's symptom -- a chain-wide guarded-floor design is ITS OWN item, routed
  to CTO (same NEVER#4 family as the mdpf convergence-gate debt already routed), with
  BR1 citing it as adjacent, never absorbing it.

**Citation discipline (binding on this plan from here, per CTO's adoption of AE's class
note -- STATE + recorded hazard, never existence+target):**
- `inf-canonical-prices-daily`: cron(47 14), **DISABLED** (AE live verify 2026-08-04);
  hazard on record: the 07-13 unguarded-full race (@b7bce51bd). Cited as a DEAD rule that
  STAYS dead.
- The runner dispatch lock: LIVE; hazard it guards: the same 07-13 race.
- The Gate-2 emitter + row-2 silver floor: **PLANNED, not live** (AE TF hold until this
  amendment lands); nothing here cites them as existing controls.
- Gate-3 preconditions now read GF-1 in place of the dead row-1 citation ("both floors
  live AND exercised" = row-2 floor + GF-1).
