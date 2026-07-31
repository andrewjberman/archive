<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E6.harness-r4-trigger-binding</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>0.7.0_AE_CloudOps~E (lane to be spawned by 0.0.0_AB_MSTR on receipt of the sequence)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>

<priority>P4 by the PRD phase order, PULLED FORWARD TO NOW on two grounds: (1) it is KIMI-INDEPENDENT -- it needs no lifecycle value, no user-input pipeline, and is unaffected by the Andrew gate that parked E1's values and E3; (2) its stated precondition IS ALREADY DONE. Andrew's standing rule is to defer the unsolvable and proceed past it. This is what "past it" looks like.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_ESTATE_PRD.md -- WS-E6 (lines 205-223). Three items: R8 conversion, R4 trigger binding, path tuning.</ref>
  <ref type="landed">@d82aa5b8f1 -- R8, the conversion instrument, ALREADY LANDED: .tools/comp-which (+126), org/modules/graph/comp-output-contracts.yaml, comp_log_auto.py, and a 242-line test (test_e6r8_route_run_conversion.py). THE PRD NAMES R8 AS E6's PRECONDITION -- "until conversion is measurable, every behavioral claim is unfalsifiable." That precondition is DISCHARGED. You are not starting E6 cold.</ref>
  <ref type="law">CLAUDE.md TRIGGER_LAYER doctrine + Rule 21 (comp-rail). The unrun tools move from *available* to *fires-at-a-moment-of-work*.</ref>
</references>

<objective>
WS-E6 item 2: R4 TRIGGER BINDING. Bind two comp-tools to the moments of work where they are
load-bearing, so they fire at a moment rather than merely existing in a catalog:
  closeout -> `comp-state`
  deploy   -> `comp-pipescript deployed`

>> YOUR FIRST ARTIFACT: ONE of the two bindings, FIRING, MUTANT-PROVEN. Not both. Not the map. <<

Pick whichever is cheaper to exercise and land it end-to-end: the trigger bound, observed firing at
its real moment of work, and PROVEN falsifiable by a mutant (deliberately break the precondition and
watch it FAIL -- a passing assertion that has never been mutated has never been tested). Report that
one, then take the second.

Do not begin with the path-tuning map (item 3). That is the workstream's third item and it depends on
conversion being measured across real routes; starting there is starting at the end.
</objective>

<constraints>
1. **THE OUTPUT LANDS AS AN OWNED ITEM, NOT A LOG LINE.** The PRD is explicit. A trigger that fires
   and writes to a log nobody owns has moved the tool from "unrun" to "unread," which is not progress.
2. **PROTECT THE MEMORIZED HEAD** (PRD item 3, binding on item 2 as well): NEVER insert a router hop
   where memory already routes correctly. A forced hop is a latency tax that trains skimming -- and an
   agent trained to skim the rail is a worse outcome than an unbound tool.
3. **NO ALARMS, NO MONITORS, NO NOTIFICATION MACHINERY.** Standing moratorium (Andrew-direct
   2026-07-28). A trigger binding is NOT a monitor -- it fires a tool at a moment of work and lands an
   owned item. If your design starts to look like a watcher, a checker, or a notifier, you have
   drifted off the TO; stop and route to me.
4. **MUTANT-PROVEN IS THE BAR, AND IT IS NOT NEGOTIABLE.** The PRD says "firing mutant-proven."
   Demonstrate the binding can go RED before you claim it is green. An unpersisted mutant proved a
   guard could fail ONCE, in a session, and then stopped existing -- persist the mutant.
5. Do not modify `comp-which`'s routing table to make a binding look like it fires. That is
   instrumenting the instrument.
6. No emojis / non-ASCII anywhere.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before build">
    <step>
      <run>comp-which "what fires comp-state and when does a closeout happen"</run>
      <expect>The current selection path for comp-state, and whether any trigger already exists. Establishes the pre-state you are moving from -- you cannot claim a conversion improvement without it.</expect>
      <if_mismatch>A dead-end is a rail coverage gap: record and report it.</if_mismatch>
    </step>
    <step>
      <run>Read the R8 conversion instrument @d82aa5b8f1 -- comp_log_auto.py + comp-output-contracts.yaml + test_e6r8_route_run_conversion.py</run>
      <expect>You understand how route->run conversion is joined BEFORE you add a trigger, because your binding must be visible to that instrument or it is unmeasurable. R8 found there was no key on EITHER side; know what key it established.</expect>
      <if_mismatch>If your binding cannot be seen by the conversion instrument, that is a design finding to raise BEFORE building, not after.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="the mutant">
    <step>
      <run>Break the binding's precondition deliberately; observe the trigger FAIL; restore; observe it PASS. Persist the mutant as a test.</run>
      <expect>A RED then a GREEN, both observed, the mutant COMMITTED. Scored on OUTPUT, never on rc (harness rc is corrupted on this box unless the /c mount is live).</expect>
      <if_mismatch>If you cannot make it go red, it is not a test -- it is a decoration with an assertion-shaped syntax.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
FIRST ARTIFACT (report on this alone):
1. ONE of the two bindings (closeout->comp-state OR deploy->comp-pipescript deployed) demonstrably
   FIRES at its real moment of work -- exercised, observed from the run's own output, never inferred
   from configuration.
2. Its mutant is PERSISTED and committed: the binding proven able to go RED.
3. Its output lands as an OWNED item with a named owner, not a log line.

SUBSEQUENT (do not block artifact 1 on these):
4. The second binding, same three bars.
5. Router conversion rate reportable WITH A DENOMINATOR (the PRD's headline acceptance for E6) --
   this rides R8's instrument and is the measurement item 3 depends on.
6. >=1 friction reduction validated against the measured map, with the memorized head protected.
7. Session log with a Compiler Tools section reproducing each run vs expect.
</acceptance_criteria>

<cross_domain_coordination>
- **SEAT RESOLVED 20260731T142036Z.** This TO was briefly drafted against `~B`; that was WRONG and is
  corrected here. `~B` owns the Kimi user-input pipeline (Andrew-authorized directly ~1320Z, confirmed
  in writing by MSTR 132601Z) -- its broker summary reading "holding v4" is STALE, not evidence it is
  free. **Do not pull `~B` onto this work.** `~D` is free and is taking WS-E5 in parallel; this lane is
  spawned fresh for E6.
- **YOU ARE THE SECOND OF TWO PARALLEL KIMI-INDEPENDENT LANES.** `~D` runs WS-E5 (estate sensors)
  concurrently. E5 and E6 are independent by construction -- E5 works detector boundary declarations
  against the E1 registry; you work the harness selection paths. If you find yourself needing an E5
  artifact, that is a seam finding to route to me, not a dependency to wait on.
- base CTO (1.0.0_SA_CTO) is the arch-gate on anything touching comp-tool STANDARD surfaces. Note
  `comp-which` IS such a surface -- a routing-table change routes to CTO before it lands.
- base CVO (3.0.0_SA_CVO) verifies TO deliverables.
- `~A` owns the Aug-1 14:00Z ETFS month-end fire, hard deadline TOMORROW. Nothing in E6 should reach
  it; if a trigger binding you design would fire on the deploy path ~A depends on, STOP and route to me.
</cross_domain_coordination>

<notes>
WHY THIS WORKSTREAM IS WORTH DOING WHILE THE GLAMOROUS ONES ARE GATED: E6 is the only workstream whose
subject is whether the estate's OTHER instruments are actually reached at the moment they would have
helped. A tool that exists, is correct, is documented, and is never invoked at the moment of work has
the same estate value as one that was never built -- and it is worse, because it appears on the
catalog as coverage. The 295x under-report R8 closed is the measurement of exactly that gap.

WHY MUTANT-PROVEN AND NOT "IT FIRED WHEN I RAN IT": a binding observed firing once, in a session
where the author was watching for it, is a demonstration and not a control. The question that decides
whether this is real: if the precondition silently stopped holding tomorrow, would anything print? If
the honest answer is no, you have built a thing that fires when observed -- which is the shape of
every instrument in the estate that has ever lied.
</notes>
</task_order>
