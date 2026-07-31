<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E3.debt-retirement-engine</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>UNASSIGNED -- do not seat while GATED (MSTR provisions on unblock)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>gated</status>

<priority>P3. **GATED -- DO NOT START.** This TO exists so the gate is legible and the unblock condition is written down, not so someone begins. Filed per LD-0365: Kimi-DEPENDENT work is TO'd but MARKED GATED so the fabric does not stall on it.</priority>

<gate>
**BLOCKED ON: WS-E1 lifecycle VALUES, which are Andrew-GATED on the Kimi user-input pipeline.**

The dependency is NOT bureaucratic and NOT re-routable. PRD lines 114-121, binding:

> "No retirement executes against a key whose contract lacks a lifecycle value; a `TRANSIENT`-contracted
> key is exempt from existence-based signals entirely."

E3 retires things. It decides what to retire from contracts. A contract with `lifecycle_class:
UNDECLARED` -- which is EVERY contract today, by Andrew's gate -- cannot authorize a single retirement.
**The engine is not slowed by the missing values; it is structurally inert without them.**

UNBLOCK CONDITIONS (all three, verified not assumed):
1. The Kimi user-input pipeline is live and producing lifecycle values (`0.7.0_AE_CloudOps~B` owns it).
2. Lifecycle values are populated in `org/modules/graph/estate-contracts/` for the target population,
   with `lifecycle_class` no longer UNDECLARED on the keys in scope.
3. Andrew's gate on lifecycle VALUES is lifted (the MECHANISM was never gated -- only the values).

**WHAT IS NOT BLOCKED AND IS ALREADY DONE: E3.0, the P1 safe slice.** Executed @2da40ba711 --
6 of 6 eligible candidates -> KEEP-DORMANT, 0 retirements, gates exercised, denominator printed at
every step. That is the PRD's acceptance bar for E3.0 MET, not a partial result. Do not re-run it and
do not treat E3 as unstarted: its zero-blast-radius half is closed.
</gate>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_ESTATE_PRD.md -- WS-E3 (lines 95-148).</ref>
  <ref type="done">@2da40ba711 -- E3.0 Wave-1 safe slice, CLOSED. org/tier2_senior/0.7.0_AE_CloudOps/deliverables/E30_WAVE1_SAFE_SLICE_20260730.md</ref>
  <ref type="population">The 353 dead surfaces from `comp-legacywriter --census` -- the first adjudicated population, joined against contracts as they land.</ref>
</references>

<objective>
Kill lists become DERIVED, never censused: `expired_obligation UNION superseded_with_live_successor`,
walked from WS-E1 contracts. When unblocked, the first artifact is ONE contract-derived retirement
executed under the full gate stack -- not the derived kill list, not the wave plan. One retirement,
exercised, with both numbers printed.
</objective>

<constraints>
1. **DEBT-DECOMMISSION REQUIRES >=2 CONFIRMED SIGNALS + no contradicting live-use + guard ruled out.**
   A single confirmed signal stays advisory. Default FAIL-SAFE is KEEP-DORMANT: a missed corpse is
   recoverable; a decommissioned belt is the named failure mode.
2. **TIER-C MECHANICAL SIGNALS ARE NEVER SUFFICIENT** (bare DISABLED, 0 invocations, no consumer,
   git-cold). They ARE the debt signals -- and a deliberate belt and a corpse are identical on every
   one of them.
3. **THE TRANSIENT TRAP IS THE REASON FOR THE GATE, AND IT DEFEATS THE >=2-SIGNAL BAR.** A live
   written->consumed->deleted trigger marker (`gold/trigger-pending.json` class) is absent from S3 at
   every moment you look, and it independently reads absent AND dormant AND reader-less. **Two
   confirmed signals, both wrong, on a live pipeline trigger.** Confirmation across correlated
   instruments is not independence. This is precisely why no retirement may execute against a key
   whose contract lacks a lifecycle value.
4. **EVERY WAVE STATES BOTH NUMBERS** -- derived-from-contracts AND census-only (the surfaces the
   derivation structurally cannot see), with the gap named as COVERAGE DEBT. PRD 133-140: the derived
   engine and the census cover COMPLEMENTARY populations. **Retiring the census while coverage is
   partial makes actual recall FALL at the moment the program reports it rising** -- the
   denominator-shrinks-and-looks-like-progress shape, inside the workstream built to prevent it.
   The census retires when the coverage gap is ZERO, not when the engine works.
5. **THE UNIT OF RETIREMENT IS THE WRITE, NOT THE PRODUCER** (LD-0330). Never-widen sign-off where a
   served surface is touched. Every retirement exercised, never inferred.
6. Recursive deletion / S3 object deletion requires human confirmation -- CLAUDE.md Agent Autonomy.
   This workstream's core act is on that list. **No retirement executes without it.**
7. No emojis / non-ASCII anywhere.
</constraints>

<acceptance_criteria>
1. E3.0 safe-slice retirements executed clean at P1 -- **ALREADY MET @2da40ba711.**
2. The derived kill list exists with its DERIVATION printed (not its output alone).
3. Every wave states BOTH numbers with the coverage-debt gap named.
4. >=N contract-derived retirements executed under gates at P3 (N set at decomposition, once the
   contracted population is known -- it cannot honestly be set before the gate lifts).
5. Zero new C-SILENT residents going forward: a resource created without a contract is a commit-gate
   warning ramping to a deny (announce-then-enforce). **This is also WS-E5's enforcement carrier** --
   E5's acceptance item 3 rides this exact ramp, so sequencing E3 late imposes a stated ceiling on E5.
6. ZERO retirements against uncontracted-lifecycle or TRANSIENT keys.
</acceptance_criteria>

<cross_domain_coordination>
- `~B` owns the Kimi pipeline that gates this. E3's unblock is downstream of ~B's delivery.
- **WS-E5 has a STATED DEPENDENCY ON THIS WORKSTREAM'S COMMIT-GATE RAMP** (PRD 195-197). E5 is running
  NOW under ~D and will hit that ceiling; it has been told to build to it and name it. When E3
  unblocks, close that seam deliberately -- do not let E5's enforcement half go quietly unbuilt.
- Never-widen sign-off (CTO+COO) required where a served surface is touched.
</cross_domain_coordination>

<notes>
WHY THIS TO IS FILED GATED RATHER THAN LEFT UNWRITTEN: an unwritten gated workstream is
indistinguishable from a forgotten one, and the difference matters at the moment the gate lifts --
which will be someone else's session. The unblock conditions above are the deliverable of this file
today. Everything else in it waits.

THE HONEST STATEMENT OF WHAT THIS COSTS: E3 gated means the estate's debt keeps accruing at its
current rate for the duration, and the 353 dead surfaces stay dead-but-present. That is the right
trade -- a decommissioned belt is unrecoverable and a corpse is not -- but it should be stated as a
cost being paid deliberately, not as a neutral pause.
</notes>
</task_order>
