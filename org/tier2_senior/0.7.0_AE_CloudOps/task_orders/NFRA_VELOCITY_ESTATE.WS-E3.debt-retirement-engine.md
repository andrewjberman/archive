<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E3.debt-retirement-engine</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>UNASSIGNED -- do not seat while GATED (MSTR provisions on unblock)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>gated</status>

<priority>P3. **GATED -- DO NOT START.** This TO exists so the gate is legible and the unblock condition is written down, not so someone begins. Filed per LD-0365: Kimi-DEPENDENT work is TO'd but MARKED GATED so the fabric does not stall on it.</priority>

<why_the_engine_returns_zero>
**ANDREW-DIRECT ~1655-1700Z, ratified verbatim (via base CVO 171333Z). THIS IS THE EXPLANATION OF E3's
INERTIA AND IT IS BETTER THAN "gated on lifecycle values" -- it tells the lane WHAT IT IS WAITING FOR
rather than only that it waits.**

>> **SHED IS A TWO-AXIS DECISION:**
>>   **AXIS 1 -- INTENT: "is it wanted?"** -> `lifecycle_class`, PRODUCER-ASSERTED.
>>       **NO INSTRUMENT FOR THIS HAS EVER EXISTED.**
>>   **AXIS 2 -- FRICTION: "what does removal cost, what does keeping cost?"** -> blast radius, live
>>       gates, writer/reader census. **INSTRUMENTED AND WORKING.**
>> **THE ESTATE HAS BEEN MAKING A TWO-AXIS DECISION ON ONE AXIS, AND THE HONEST VERDICT ON ONE AXIS IS
>> ALWAYS "DO NOT TOUCH IT."** <<

**THE MEASURED PROOF IS ALREADY IN THE PROGRAM'S OWN BASELINE:** E3.0 closed **0 retired / 6 of 6
KEEP-DORMANT** because **THE SAFE SLICE AND THE CLEARABLE SLICE DO NOT OVERLAP** (P1 baseline s.3c).
**That zero was NOT caution and NOT a gate artifact -- it was the only SOUND answer available on the
evidence E3 had.** An engine with a working friction axis and no intent axis cannot return anything
else, and should not.

**WHAT THIS CHANGES FOR THE LANE:** E3 is not waiting for permission. It is waiting for **AXIS 1 TO
EXIST**, and axis 1 is exactly what **WS-E8's C3 walk produces** (CTO 161617Z: the registry is the
STORE, the walk is the WRITER; all 14 declarations read UNDECLARED because no mechanism ever ASKED).
**E3 unblocks when the walk produces asserted intent, not when someone lifts a hold.**
</why_the_engine_returns_zero>

<axis_2_becomes_generative>
**ANDREW ACT 3, VERBATIM:** *"I think blast-radius is a way to potentially check overlap, in essence if
something has highly overlapping blast radius and is doing the same function, that is very high
friction, and needs to be assessed."*

**THIS MAKES THE FRICTION AXIS GENERATIVE.** Today blast radius can only **PRICE a candidate somebody
else proposed.** Under act 3 it can **PROPOSE candidates** -- because **two assets whose blast radii
heavily overlap AND whose function is the same are probably ONE ASSET WEARING TWO NAMES, and the
duplication is a cost paid continuously by everyone downstream.**

**LIVE SPECIMEN, Andrew's own, already condemned in the census ledger:** `estimate-shadowing-exact` --
*"an agent built an ESTIMATOR for a quantity the estate already measures EXACTLY"* -- with
`canon-bypass-creation` as its sibling class. **The estate has a NAMED duplication class, an ANDREW
CONDEMNATION of it, and NO MECHANISM THAT WOULD HAVE SURFACED IT.**

**✅ RULED (joint call, COO 172022Z + base CTO 172201Z, reached independently and concurring):
THE AXES ARE COUPLED FOR PRECISION, NOT FOR EXISTENCE.**
```
  COMPUTE  blast-radius overlap                    -- fully instrumented TODAY
  PROPOSE  high-overlap pairs as CANDIDATES
  ASSESS   function-sameness -- BY A HUMAN, the step Andrew already specified ("assessed")
```
**Axis 1 IMPROVES PRECISION; it does NOT GATE EXISTENCE. No fourth consumer is added to the C3 walk as
a DEPENDENCY -- duplication detection is an ENHANCEMENT.** Act 3 stays OFF the critical path of the
Kimi/lifecycle chain, which is already carrying E3 and E5.

**WHY IT IS THE ONLY VIABLE v1 RATHER THAN THE CONVENIENT ONE -- base CTO MEASURED IT:**
```
  files carrying a PURPOSE declaration ....... 22
  positive control (`def ` under data/) ...... 837   -> the scan discriminates; 22 is real
```
>> **THE BETTER ORACLE HAS THE SAME GAP AS THE ONE IT REPLACES.** `PURPOSE` is producer-asserted,
function-level, and **essentially unpopulated** -- exactly as `lifecycle_class` is producer-asserted
and 14-of-14 UNDECLARED. **Act 3's semantic dependency is not "on C3.ii labels" and not "on PURPOSE";
it is on THE SAME MISSING PRODUCER-ASSERTION LAYER, one field over.** Had PURPOSE come back widely
populated, "wait for the oracle" would have been arguable. It did not. **v1 ships on the computable
half or it does not ship this program.** <<

**AND C3.ii LABELS ARE NECESSARY-BUT-NOT-SUFFICIENT:** a C3.ii label is a **VERTICAL ASSIGNMENT** --
`etf-reports` alone spans 9 producers -- so it **NARROWS the candidate set and ESTABLISHES NOTHING.**
Treating it as the sameness oracle would emit same-vertical pairs as duplicate candidates: **a
false-positive generator pointed at the one workstream whose entire discipline is
fail-safe-toward-keeping.**

**🚧 PROHIBITION, WITH ITS REASON (COO-proposed, CTO-ratified and strengthened -- BINDING):**
>> **NAME-SIMILARITY, PATH-ADJACENCY AND SHARED-VERTICAL ARE NOT EVIDENCE OF FUNCTION-SAMENESS AND MAY
NEVER BE EMITTED AS SUCH.** An agent that computes overlap, INFERS sameness from names or paths, and
emits a duplication finding has performed **observer-inference wearing a declaration's costume** -- the
same shape ruled out for the UNASSIGNED-RESIDUE and forbidden by `lifecycle_class`'s producer-assertion
rule, **in a third place.** <<
**A CANDIDATE LIST IS A LIST OF QUESTIONS. THE MOMENT IT CARRIES A VERDICT IT HAS BECOME AN INFERENCE
NOBODY WAS AUTHORIZED TO MAKE.**

>> **AND THIS IS THE FIRST ONE WHERE THE FAILURE IS IRREVERSIBLE. THE HUMAN ASSESSMENT STEP IS NOT A
WORKFLOW NICETY -- IT IS THE CONTROL**, because of what the mechanism is pointed at: **it proposes
DELETIONS.** Every other observer-inference failure in this program cost a wrong number or a wasted
hour. **This one would cost an asset.** <<

**FENCE (CVO, binding):** act 3 is an **ANALYSIS over the existing dependency graph producing CANDIDATES
FOR HUMAN ASSESSMENT.** **NOT an alarm. NOT a monitor. NOT a pager.** The moratorium binds hardest
exactly where a duplication finding feels most alertable.

**SEQUENCING (CTO 172201Z):** **act 3 v1 is NOT gated on the C3 walk** -- sequence it independently; it
can start whenever a lane is free and does not queue behind E3/E5.
**AND DO NOT SPAWN A POPULATE-PURPOSE CAMPAIGN OFF THE 22-FILE FINDING.** That is the solicitation-track
shape and it belongs to the same producer-assertion mechanism, not to a parallel effort.
**ONE MISSING LAYER, SEVERAL CONSUMERS WAITING ON IT -- NOT SEVERAL CAMPAIGNS.**
</axis_2_becomes_generative>

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

**DO NOT RELITIGATE THE GATE WITH "BUT E3.0 RAN WITHOUT LIFECYCLE VALUES."** It did, and that is not
a counterexample -- it is a spent one. **The non-retiring slice is SPENT AND MEASURED EMPTY:** P1
baseline s.3c establishes that the safe slice and the CLEARABLE slice DO NOT OVERLAP (0 retired,
6/6 KEEP-DORMANT; re-spec routed to `~C`). So every remaining member of this workstream's population
is retirement-class work, and PRD 114-121 forbids exactly that against an UNDECLARED lifecycle.
**INERT holds for the REMAINDER, which is all that is left.** (Refinement supplied by base CVO,
review tranche 1, 20260731T143146Z -- added so a later lane cannot reopen a settled gate on a
half-remembered precedent.)
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
