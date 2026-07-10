# NFRA_COMPLEARN AMENDMENT — AMD-P3b (leg-4) + AMD-P3c (ingestion honesty): BUILD+STAGE note

**Author:** `0.8.0_AE_CloudComp~E` · **Date:** 2026-07-10 · **archetype:** IMPLEMENT
**GO:** `2.0.0_SA_COO~A` (20260710T192756Z — BUILD+STAGE only) · **Arch-gate:** `1.0.0_SA_CTO~A` (diffs routed below)
**Specs:** `docs/architecture/NFRA_COMPLEARN_amend_loop-closure_20260710.md` @ 362272cce; TOs @ 8dfcf1e75
**Sovereign boundary honored:** no bd / 49F / Schwab read or target; no vendor egress.

---

## Disposition (read first)

Both legs are **BUILT + STAGED + EXERCISED GREEN**. **Nothing that changes live routing behavior or the live
enforcer has been landed.** Per the COO~A GO:

- **P3b — the DRV go-live is NOT flipped.** comp-which's live default stays affinity-COLD (`_LIVE_AFFINITY`
  OFF). The flip is a *gated event* — CVO scorer-honesty re-verify + CTO~A arch-gate — never an auto-mutation
  (COMPLEARN §5: advisory, never auto-mutating). What landed is a hermetic **acceptance exercise** proving the
  activation is correct + safe *when* flipped.
- **P3c — the enforcer edit is NOT landed.** It is DAYLIGHT-HELD (`.tools/**→BASE_EXEC`). The disclosure design
  + exercise are staged; the diff is an apply-clean patch routed to CTO~A. **Open question for CTO~A/COO~A:
  who lands it (0.8.0~E in daylight post-arch-gate, or BASE_EXEC/exec) — flagging, not assuming.**

---

## AMD-P3b — leg-4 activation (the DRV flip), behind the existing CTO-owned Goodhart gate

**What it is.** The OUTCOME-weighted `history_affinity` term (`comp_route.py` w_h) is WIRED but runs cold: the
live comp-which decision passes `affinity_provider=None`. Leg-4 = activate it — **behind the EXISTING** value-
anchored Goodhart gate (`comp_route.outcome_value`/`outcome_weighted_affinity` + the `CachedAffinityProvider`
m-estimate MEAN, COMPLEARN P2 @ 15e88557d + refine 3dffba0a9). **REUSED verbatim — not re-architected.**

**The gate (why it is anti-Goodhart by construction).** The learned term is the m-estimate-shrunk MEAN outcome
value, never a sum/count: `affinity = (sum(outcome_value) + k*prior) / (n + k)`. `outcome_value` maps PASS→1.0,
FAIL/DENY→0.0 (+gap bonus), so 100 low-value runs never beat 5 high-value ones — count enters ONLY as a
confidence denominator. "Affinity influences the route only on a VALUE improvement, never a usage one" holds by
construction, and comp-which output is advisory (it suggests; the agent decides) — advisory, never auto-mutating.

**Delivered (staged):**
1. **ETL/producer ran** — fresh affinity cache emitted from the live corpus: **248 per-cap-id entries / 20,394
   rows** (`org/mcp/comproute-affinity-cache.json`, gitignored regenerable artifact; `mode:shadow` UNCHANGED —
   honest: it does not weight the live decision).
2. **AC-L4 acceptance exercise** — `org/modules/graph/comp_learns_leg4_exercise.py` (committed `ec64edd9b`),
   hermetic + deterministic, actually invokes `route()` end-to-end through emit→provider→engine.

**AC-L4 result — "the SHIFT is the acceptance" (all 5 PASS):**
```
[PASS] cold_route_invariant          cold "estate" (AE) is a genuine TIE (disambiguation)
[PASS] repeated_outcome_shifts_route cold=tie -> armed=decision:comp-drift  (THE SHIFT)
[PASS] route_tracks_the_outcome      drift-good->comp-drift ; aws-good->comp-aws  (base-CTO falsifier)
[PASS] value_not_count_goodhart_gate drift(n=4,PASS)=0.889 > aws(n=80,FAIL)=0.047 -> decision drift (count did NOT win)
[PASS] struct_gate_holds_when_armed  no write_path cap surfaced under an armed READ (E1 safety holds)
```

**Corroboration — safe to activate (C1 dual-arm eval, `comp_route_eval.py --arm both --role AE`):** the ON arm
(affinity live) shows **zero precision/recall regression** and **struct-gate PASS in BOTH arms** across all tiers
(canon/diverse/heldout). On the real corpus the affinity is (correctly) near-invariant — the value-anchored,
m-estimate-shrunk term does not destabilize confident routes. That safety is the *other* half of acceptance:
the **mechanism is live** (a repeated outcome CAN move the route, on VALUE) yet it **never misroutes** an
existing confident route. The learning payoff accrues as real routing-outcome telemetry (charter-2 route→run
capture) accumulates.

**Grounding:** `comp_route.py:485` (ToolActivityAffinityProvider), `:464` (outcome_weighted_affinity — mean not
count), `comp_route_affinity.py:97` (CachedAffinityProvider), `.tools/comp-which:809,815,838` (the `_LIVE_AFFINITY`
default-OFF switch — the one-line go-live flip that stays UNTOUCHED here). All @ working-tree 2026-07-10.

**The go-live flip (NOT done — the gated event):** flipping `_affinity_provider()` to return the live provider
by default is a `.tools/comp-which` edit — out of P3b BUILD+STAGE scope (amendment A3: P3b does not edit `.tools/`),
gated on CVO scorer-honesty re-verify + CTO~A arch-gate. Shared gate with `NFRA_TOOLGRAPH.TO-3` (one gate, both
consumers; CTO~A coordinates the shared usage).

---

## AMD-P3c — ingestion honesty (comp_log_auto disclosure), DESIGN+STAGE, enforcer land DAYLIGHT-HELD

**What it is.** `org/modules/graph/comp_log_auto.py` (the universal comp-tool logger) drops an emission SILENTLY
in three places: an absent log file (`_append_log` early `return`), a failed append (`try/except pass`), and the
`main()` outer `except: pass`. A silent-noop writer lets the loop's own freshness/health signal undercount
invisibly — the "census of survived failures" hole (R5/R7), one layer down in the loop's own ingestion.

**Design (staged, apply-clean patch → `P3c_comp_log_auto_disclosure.patch`):** a graded `_disclose_drop(workspace,
tool, reason)` — a dropped emission appends one `ISO-ts|tool|reason` record to `.comp-graph/.comp_log_drops` (a
COUNT = line count + MARKER = existence an audit/health check reads), falling back to a `COMP_LOG_AUTO_DROP:`
stderr line, then a last-resort pass. **The "never disrupt the caller" invariant is preserved** — the bare pass is
reachable only AFTER a visible signal was attempted, so a drop is never fully silent. Wired at all three drop
points; a NORMAL run is untouched (no false drop). Adds `from __future__ import annotations` (py39 gate-clean).

**AC-L3c result — exercised, not asserted (all 6 PASS; force a write failure, observe the disclosure):**
```
[PASS] normal_run_no_false_drop    writable log -> row appends, 0 drops
[PASS] drop_disclosed_log_absent   log MISSING     -> 'log-file-absent' recorded
[PASS] drop_disclosed_append_fail  log is a DIR    -> 'append-failed: PermissionError' recorded
[PASS] count_accrues               3 forced drops  -> 3 lines (the COUNT is real)
[PASS] stderr_last_resort          workspace=None  -> COMP_LOG_AUTO_DROP on stderr (never silent)
[PASS] disclosure_never_raises     unwritable marker + closed stderr -> returns normally (caller not disrupted)
```
Exercise: `.runtmp/p3c_comp_log_auto_disclosure/exercise_p3c.py` (pre-land proof vs the staged copy) +
`deliverables/NFRA_COMPLEARN_AMD/verify_p3c_ac_l3c.py` (LANDING verification vs the LIVE module — RED until land,
GREEN after). Patch `git apply --check`: **clean**.

**Land discipline:** the enforcer edit sequences behind the `.tools/**→BASE_EXEC` daylight hold + CTO~A arch-gate.
Not landed by this session. Re-run the landing verification against live as the exercise-gate at land time.

---

## Routing

- **Diffs → `1.0.0_SA_CTO~A`** for the single arch-gate (P3b commit `ec64edd9b`; P3c patch attached) BEFORE any land.
- **CVO (`3.0.0_SA_CVO`, via COO)** — independent scorer-honesty re-verify is the P3b go-live pre-gate (AC-L4).
- **RAVC → `2.0.0_SA_COO~A`** on completion (this note is the evidence bundle).
