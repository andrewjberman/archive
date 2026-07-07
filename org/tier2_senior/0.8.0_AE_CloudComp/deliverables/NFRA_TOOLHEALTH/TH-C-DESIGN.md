# NFRA_TOOLHEALTH TH-C -- Close-the-Loop Acceptance Gate: DESIGN

**Author:** 0.8.0_AE_CloudComp~D (2026-07-07). **Lane:** COO~B (NFRA_COMP*).
**TO:** 2.0.0_SA_COO [DRIVE -- TO: NFRA_TOOLHEALTH TH-C] (20260707T054915Z).
**Status:** DESIGN -- RAVC1 to COO~B. Build-now = the DRV-INDEPENDENT emitter + differential proof; EXECUTE = the D1 behavior-change confirmation on CTO's DRV-flip green.

---

## 1. The problem (what TH-C must close)

`comp-tool-health` (TH-B, LIVE) emits per-tool verdicts {KEEP / FIX / PROMOTE / RETIRE} over the fused 3-axis
substrate -- but it is **read-only, advisory, a pure QUERY**. The verdicts DISPLAY; they drive nothing. That
IS the `ACCUMULATES-BUT-INERT` pathology (COMPLEARN D1 / COMPPROOF-D1 verdict `736f6307f`): data collected +
queryable, not autonomously consumed-and-improved. TH-C is the SOLE remaining NFRA_TOOLHEALTH piece -- it makes
the health verdict **DRIVE a demonstrable downstream action**, cross-checked as ACTING by COMPPROOF-D1.

PRD acceptance #4 (machine-checkable, the bar): `>=1 health-verdict-driven action (fix/promote/retire) is
dispatched AND COMPPROOF-D1 confirms it demonstrably changed routing/agent behavior on a later cycle -- the
loop ACTS, not merely displays.`

## 2. The clean split (why part builds now, part executes on the flip)

Acceptance #4 has TWO clauses, and they gate differently:

| Clause | What it is | Gate | When |
|---|---|---|---|
| **A. DISPATCH** | verdict -> a TYPED downstream commission (FIX->fix-TO, PROMOTE->route-proposal, RETIRE->deprecation-candidate) | none -- pure emission over the live TH-B verdicts | **BUILD NOW** |
| **B. BEHAVIOR-CHANGED** | the dispatched change demonstrably alters routing on a LATER cycle (D1 cross-check) | the router must APPLY learned affinity -- currently inert (0/280) | **EXECUTE on DRV-flip green** |

Grounded reason B is flip-gated (`comp_route.py:243`): the learned-affinity term `w_h * a_term` is **SHADOW** --
`comp-which` passes `affinity_provider=None`, so learned affinity contributes 0 to live routing. That is the
`0/280 apply learned affinity` D1 measures. The **DRV flip = wiring a live `affinity_provider` into comp-which's
`route()` call** (CTO seq step 4; shadow-green cert PASSED `4c1d93be5`; dispatched Andrew-direct `f239056de` to
CTO/0.7.0). Until it lands, no verdict-driven routing change can *demonstrably* alter live routing -- so clause B
is physically the EXECUTE leg, not a design choice.

## 3. The mechanism (three parts)

### 3a. The commission emitter -- `comp-tool-health --commission` (DRV-INDEPENDENT, build now)
Consumes `health()` verdicts; routes each ACTIONABLE (non-KEEP) verdict to its TYPED downstream commission,
**advisory-only** (never mutates a toolset / comp_route / the manifest -- it emits a PROPOSAL the CTO ratifies,
mirroring COMPLEARN + NFRA_DEBTSCAN never-auto-delete):

| Verdict | Downstream commission (the ACTION it drives) | Consumer |
|---|---|---|
| **FIX** | a fix-commission entry (tool, verdict, value_anchor, reason, proposed CTO fix-TO stub) appended to the TH-C commission ledger | COMPLEARN worklist consume-side + CTO commission path |
| **PROMOTE** | a COMPROUTE routing/HUD proposal (the effective-but-ignored tool + a surface_prior/routing-surface bump proposal for comp_route) | NFRA_COMPROUTE |
| **RETIRE** | a deprecation-candidate entry (CTO ratifies; NEVER auto-removed) | CTO commission path |
| KEEP | NO commission (the null/healthy path -- load-bearing for the differential proof) | -- |

Idempotent, vintage-stamped (`computed_at`), read-only over source. Emits to a SERVED commission surface (JSON)
that the CTO commission path + COMPROUTE read -- the same served-surface pattern COMPLEARN's worklist uses.

### 3b. The differential acceptance test (the CVO exercise-gate, DRV-INDEPENDENT at the emission layer)
COO's bar: *"feed a FAILING-health signal -> confirm the downstream action DIFFERS from the healthy path (a
verdict that changes nothing = NOT closed)."* Satisfiable NOW at the emission layer via the proven `--effective-feed`
seam: take a live KEEP tool, inject EFFECTIVE=False -> it flips to a CONFIRMED FIX (TH-B self-test check 9 already
proves this flip) -> assert the emitter produces a **fix-commission** where the healthy (EFFECTIVE=True/KEEP) path
produces **nothing**. The differential commission artifact IS the "changes behavior" proof at dispatch layer.

### 3c. The D1 behavior-change cross-check (acceptance #4 clause B, EXECUTE on DRV-flip green)
On the flip (comp-which routes with a live `affinity_provider`): take a PROMOTE-driven routing proposal, apply it
(CTO-ratified), and confirm via COMPPROOF-D1 / the `N/280 apply learned affinity` metric that a LATER routing
cycle demonstrably DIFFERS (routing behavior changed). This is the "demonstrably changed routing/agent behavior on
a later cycle" bar -- exercised on the LIVE router (Rule 22 / 22a: exercise-the-path, not a config read).

## 4. Honesty gates carried (PRD SS5, all inherited/non-negotiable)
1. **Value-anchored** -- every commission cites the TH-B `value_anchor` (outcome value + rail quality), NEVER an
   invocation count. A FIX-commission for a heavily-used tool rests on its low VALUE, not its usage.
2. **Advisory, not auto-mutating** -- the CTO ratifies every FIX/PROMOTE/RETIRE; the emitter writes a proposal
   ledger, never touches comp_route/the manifest/the toolset.
3. **EFFECTIVE-probe honesty** -- inherited from TH-A (REACH x USABILITY, blind-solver isolation); the commission
   consumes TH-A's verdict, doesn't re-grade.
4. **Ground on live** (Rule 22/22a) -- 3c exercises the LIVE router; 3b exercises the real TH-B verdict pipeline.

## 5. Acceptance (how TH-C is judged done)
- **A (now):** `comp-tool-health --commission` emits >=1 typed commission per non-KEEP verdict over live TH-B
  output; differential test 3b PASSES (failing signal -> a commission that the healthy path does NOT produce).
- **B (on flip):** the D1 cross-check 3c confirms a verdict-driven routing proposal, once applied, demonstrably
  alters live routing on a later cycle (the `N/280` metric moves).
- **CVO exercise-gate (TH-V, independent):** CVO re-runs 3b/3c blind -> the downstream action differs on a failing
  signal, and the routing behavior genuinely changed post-flip (not a config-read claim).
- Both -> NFRA_TOOLHEALTH CLOSES.

## 6. Flip-readiness (what I execute the instant DRV goes green)
- **The green-signal I watch:** `comp-which`'s `_default_router` passes a live `affinity_provider` (not `None`)
  into `comp_route.route()` -> the `w_h*a_term` learned term weighs live routing -> COMPPROOF-D1 re-verify GREEN.
  Concretely detectable as: the `N/280 (or /236) apply learned affinity` metric goes positive on the live stream.
- **On green I run 3c immediately:** apply one CTO-ratified PROMOTE routing proposal, exercise the live router pre/
  post, confirm the routing decision differs, hand CVO the blind re-run. No new build needed at flip time -- 3a/3b
  land now; 3c is an EXERCISE of the already-built emitter against the now-live router.
- **Dependencies GREEN:** TH-A landed (`0191f9c9f`, CVO-validated), TH-B skeleton+`--effective-feed` join landed
  (`64c89d675`/`6b641ff05`, `.tools/comp-tool-health` live, self-test 12/12 PASS today). COMPPROOF-D1 = NOT-GREEN
  (`736f6307f`) pending the flip -- the ONLY remaining gate, and it's the flip itself.

## 7. Build plan (DRV-independent, starts on COO design-ACK)
1. `comp_tool_health_gate.py` (or a `--commission` mode on comp_tool_health) -- the 3a emitter, advisory, served-
   surface JSON, idempotent + vintage-stamped. REUSE TH-B's `health()` un-forked (import, don't fork).
2. `--self-test` extension: the 3b differential (failing-signal -> commission differs from healthy path).
3. `comp-surface-check` before/after (COMPROUTE is a critical surface; the emitter only PROPOSES, doesn't mutate).
4. RAVC2 COO with the built emitter + differential PASS; CVO TH-V Phase-2 hand-off.
5. HOLD 3c for the DRV-flip green; execute + CVO-exercise + close on green.
