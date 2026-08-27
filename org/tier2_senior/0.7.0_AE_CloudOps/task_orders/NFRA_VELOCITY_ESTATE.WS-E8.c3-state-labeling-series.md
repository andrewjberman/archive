<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E8.c3-state-labeling-series</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>SERIES PARENT -- each sub-TO splits out to its named owner at dispatch</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_VELOCITY_ESTATE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending -- E8.1 STARTABLE NOW; E8.2-E8.5 ride base CTO's spec</status>

<priority>ANDREW-DIRECT, 2026-07-31 ~1612-1615Z. Verbatim instruction: **"this needs a dedicated series of TOs wrapped into the project, relay all of this to CTO."** This file is that series. It sits UPSTREAM of two gated ESTATE workstreams (WS-E3, WS-E5's enforcement half) because it is the mechanism that MAINTAINS lifecycle stage.</priority>

<andrew_verbatim>
All four messages, in order, at the COO terminal 2026-07-31 ~1612-1615Z:

1. "This is another opportunity for a semantic review pipeline, I think it can be built into the Kimi
   Review cycle. IN essence each c3.ii and potentially c3.i needs a human vs CTO and CVO agreement on
   the state of each system."
2. "that is how the lifecycle stage is maintained"
3. "the part that we have been desigining thus far with 0.7.0~B is the high level signal, but there can
   be an additional layer of essentially tracking c3 and labeling them. I think the idea is that the CTO
   and Andrew (human user) go through the various c3 items, and if there is a doubt about it, then CVO
   investigates and reports back so Andrew and CTO can confirm."
4. "this needs a dedicated series of TOs wrapped into the project, relay all of this to CTO"

**READ (3) AS THE OPERATIVE WORKFLOW; IT NARROWS (1).** Message (1) says "human vs CTO and CVO
agreement," which reads as three-way consensus. Message (3) supersedes that shape:
> **CTO + ANDREW walk the C3 items (PRIMARY PASS). On DOUBT, CVO INVESTIGATES and reports back.
> ANDREW + CTO CONFIRM.**
CVO is an **escalation-triggered investigator**, NOT a co-equal signer, and the confirming authority
stays with Andrew and CTO. *(COO relayed the flattened three-way reading at 161249Z/161326Z and
corrected it at 161438Z/161517Z -- recorded here so the wrong shape cannot be re-derived from those
earlier messages.)*
</andrew_verbatim>

<references>
  <ref type="authority">base CTO (1.0.0_SA_CTO) owns the SPEC for this layer. Where this series and the spec disagree, THE SPEC WINS -- route the disagreement to COO, do not silently pick.</ref>
  <ref type="layer1">The daily Kimi/K3 semantic-evolution pipeline (Andrew-ruled 2026-07-30, CVO record ANDREW_RULING_SEMANTIC_EVOLUTION_PIPELINE_20260730.md). `0.7.0_AE_CloudOps~B` owns it. UNCHANGED by this series.</ref>
  <ref type="ladder">comp-estate ladder-drill @17a8cad8eb -- C4 segments -> C3.i/C3.ii -> chains(D2) -> C2 motifs -> C1 interactions -> C0 facts. Andrew-direct purpose (2026-07-30 ~2100Z): "the entire purpose of comp-estate is that its the global lossless fidelity descent from semantics to facts."</ref>
  <ref type="consumers">WS-E3 (debt retirement, GATED on lifecycle values) + WS-E5 acceptance item 3 (enforcement half, rides E3's C-SILENT ramp). Both unblock downstream of this.</ref>
  <ref type="specimen">The "aggregator" question -- E2 msg 160956Z. ALREADY IN THE DOUBT STATE. See E8.0 below.</ref>
</references>

<objective>
Build **LAYER 2: C3 state tracking and labeling** -- a per-item, maintained record of the state of each
system at C3.ii (and potentially C3.i) granularity, walked by CTO + Andrew, escalated to CVO on doubt,
confirmed by Andrew + CTO. **This is the mechanism that maintains lifecycle stage.**

>> **THE PROBLEM IT SOLVES, MEASURED THREE TIMES IN ONE DAY BY THREE INDEPENDENT WORKSTREAMS:**
   WS-E2 -- a DELIBERATELY DISARMED pipeline and a NEGLECTED one have an IDENTICAL census signature, so
     E2's own acceptance clause, applied mechanically, would RE-ARM a ratified safety disarm.
   WS-E5 -- a boundary declaration is PRODUCER-ASSERTED; the registration invariant binds SHAPE and can
     NEVER bind TRUTH.
   WS-E3 -- Tier-C mechanical signals are never sufficient: a deliberate belt and a corpse are identical
     on every one of them.
   **A MECHANICAL SIGNAL CANNOT EXPRESS INTENT, AND AN INSTRUMENT THAT CANNOT SEE INTENT WILL
   CONFIDENTLY RECOMMEND UNDOING A DELIBERATE ACT.** The estate had the diagnosis and no channel.
   **Layer 2 is the channel.** <<

**"MAINTAINED" IS THE LOAD-BEARING WORD IN ANDREW'S MESSAGE (2), NOT "SET."** A one-time intent
annotation rots invisibly -- measured 2026-07-31: an 18-day-old corpus record was found to carry ONE
LIVE HALF AND ONE DEAD HALF, and repeating either wholesale would have been wrong. A walked-and-
refreshed labeling cannot rot the same way. This is the cardinal never-depend-on-frozen-maps rule
applied to INTENT rather than to structure.
</objective>

<the_registry_is_the_store_the_walk_is_the_writer>
**BASE CTO RULING 20260731T161617Z -- folded in at CTO's explicit instruction, and it is the single
most important structural fact in this series.**

**THE C3 WALK IS THE PRODUCER-ASSERTION MECHANISM THAT WS-E1's REGISTRY HAS BEEN MISSING ALL DAY.**

All 14 landed contract declarations carry `lifecycle_class: UNDECLARED`. **Not from laziness.** The rule
bank requires the value be **"PRODUCER-ASSERTED, NEVER OBSERVER-INFERRED... transience cannot be
derived; it must be DECLARED"** -- and **there has never been a mechanism by which any producer was
ASKED.** `~D` could only record the ABSENCE of an assertion; CTO ruled UNDECLARED the honest floor
precisely because nothing existed above it.

>> **ANDREW'S "that is how the lifecycle stage is maintained" IS THAT MISSING MECHANISM. The C3 walk
PRODUCES the producer assertion that `lifecycle_class` requires and the estate has never had.**
>> **THE REGISTRY IS THE STORE. THE WALK IS THE WRITER. THEY ARE ONE LOOP, NOT TWO SYSTEMS.** <<

**THIS IS BINDING ON THE DECOMPOSITION:** E8 does NOT build a second intent record. It writes into the
WS-E1 estate-contract registry. **If E8 and E1 diverge into two intent stores, that is the TWIN-CANON
problem the rule bank exists to prevent** -- two records of the same intent that disagree quietly, with
no way to adjudicate which is canonical. Any sub-TO that would create a parallel store is wrong by
construction and routes to COO before it is built.

**AND IT EXPLAINS WHY SCAVENGING WAS ALWAYS THE WRONG ARCHITECTURE (CTO, ruled):** an intent record
that is MAINTAINED beats one INFERRED from residue. COO's E2 mitigation scavenged intent from records
that happened to exist and **failed its own positive control** -- a hyphen-vs-underscore predicate
returned 4 hits where the truth was 13, and without that loud failure four of five targets would have
read "none known." **Scavenging is observer-inference wearing a records costume**, which is exactly
what the rule bank forbids.
</the_registry_is_the_store_the_walk_is_the_writer>

<the_series>
**E8.0 -- ✅ THE DOGFOODED CASE STUDY. ANDREW-DIRECT, 2026-07-31 ~1640Z: "have COO fold the aggregator
case into the TO series."** *(This REVERSES the ~1630Z withdrawal recorded below. Both Andrew messages
are real and the second CLARIFIES the first -- see the work-type boundary immediately following.)*

>> **THE BOUNDARY IS WORK-TYPE, NOT SYSTEM. Andrew, VERBATIM:** *"It is fine to use inflection in this
context, i thought you were getting distracted on ETFS_AVGCAP / rebate mechanism work as opposed to
NFRA_VELOCITY work. If these cases are being dogfooded as case studies, that is fine"* <<
  ✅ **SPECIMEN / CASE STUDY IN THIS SERIES** -- reason about it, justify the design from it, show what
     the C3 layer resolves that no instrument can. **This IS the dogfooding.**
  ⛔ **DISPATCH-TO-MEASURE** -- no INF silver read, no `rep_id` measurement, no aggregator tracing, no
     seat sequenced against it. That was the retracted error; it STAYS retracted.
  ⛔ **ETFS_AVGCAP / REBATE-MECHANISM WORK** -- the actual distraction he named.
  ⚠ **KEEP TWO ADJACENT-LOOKING THINGS APART:** the **$532K INF gold-floor / rebate-basis orphan STAYS
     PARKED** (ETFS_AVGCAP-adjacent, Andrew-reserved). **`canonical_nna` / `aggregator` is
     ADVISOR-ATTRIBUTION, not rebate** -- that is the case folded here. Same pipeline family, different
     work-type. *CTO nearly conflated them, and the whole clarification turns on the distinction.*

**WHY IT IS THE RIGHT SPECIMEN -- provenance, not convenience: the COO and base CTO INDEPENDENTLY
classified it C3.ii BEFORE this spec existed.** That is the strongest provenance a first specimen can
have, and **a TO series arguing from a live item nobody could resolve is stronger than one arguing from
a constructed example.**

**THE DEFINING PROPERTY, which is exactly what this layer is for:**
> *Is `aggregator` the sanctioned successor path the three-rule disarm deliberately left open, or a
> route that SURVIVED a disarm aimed at the other three?*
**THREE INDEPENDENT INSTRUMENTS AGREE AND STILL CANNOT ANSWER IT:** the rule census (142, denominator
closed by measurement, escape hatches shut), the Lambda resource policy, and a repo source search.
**Identical live signatures.**

>> **A QUESTION WHERE THE MISSING THING IS *INTENT* RATHER THAN *DATA*, THAT THREE INSTRUMENTS AGREE ON
AND STILL CANNOT ANSWER, IS THE CANONICAL CASE FOR A HUMAN+CTO WALK WITH CVO-ON-DOUBT.** <<

**AND THE HARDEST DETAIL, which is the reason the walk cannot be replaced by better tooling:** the
Lambda resource policy names ONLY the three DISABLED rules. **That is FACTUALLY CORRECT AND COMPLETELY
MISLEADING** -- a same-account IAM principal needs no resource-policy statement, so the live daily
caller leaves no trace on the callee's policy. **AN INSTRUMENT THAT IS CORRECT AND MISLEADING IS A
HARDER FAILURE THAN ONE THAT IS WRONG**, because nothing about its output invites suspicion. No amount
of better tooling at that layer fixes it; the answer was only ever in the function's source and in the
intent of the people who put it there.

*(HISTORICAL, retained: the ~1630Z Andrew-direct -- "WE will deal with inflection later, i have made it
very clear i want the focus on NFRA_VELOCITY" -- withdrew this item entirely for ~10 minutes, until the
~1640Z clarification established the work-type boundary. The withdrawal was CORRECT on the information
available and the record of the scope breach below stands unchanged.)*
  **THE THREE SPEC LESSONS (source-first · controls invisible to their own layer · build the dissolve
  path) SURVIVE** -- they are properties of the WALK, not of Inflection, and they were paid for.
  *Record of how this went wrong, because it is the series' own subject matter: base CTO issued a
  "MEASURE NOW" ruling overturning a COO hold, on a CORRECT observation -- the COO's stated rationale
  ("dormant-by-inaction") was contradicted by its own evidence, since `mode=full` fired at 13:47:24Z
  that day. **The observation was right and it did not matter: Inflection was ALREADY deferred by
  standing Andrew-direct order.** A correct point about a hold's REASONING was used to reopen a
  decision the sovereign had already closed, and the COO relayed it into a dispatch without catching
  it. **DEFEATING THE STATED RATIONALE FOR A HOLD DOES NOT REOPEN THE DECISION UNDERNEATH IT.**
  Both seats had the governing rule ("P0 is what Andrew says it is") in front of them; both had quoted
  it to others that same day. Dispatch 162956Z, retraction 163045Z, stand-down 163134Z -- ~95 seconds
  live, no work performed. **A scope breach dressed as rigour is the most persuasive form it takes,
  because every individual step is grounded.*

**E8.0-HISTORICAL -- THE WORKED SPECIMEN AS IT RAN (retained for its METHOD lessons only; DO NOT ACT).**
  The "aggregator" question is already at the doubt step and can be walked by hand before anything is
  built. E2 traced (grounded on the invocation PAYLOAD, read-only): a caller self-identifying as
  `aggregator` invokes `inf-gold-trigger` DAILY with `{"mode":"full"}`, starting a STOPPED EC2 and
  dispatching the full gold chain over SSM. **It is invisible to ALL THREE instruments** -- not an
  EventBridge rule (escape hatches closed by measurement: ONE bus, exactly 142 rules, so the census
  denominator stands), absent from the Lambda resource policy (which names only the three DISABLED
  rules -- true and completely misleading, since a same-account IAM principal needs no statement),
  and absent from a repo source search.
  **THE QUESTION: is `aggregator` the sanctioned successor path the three-rule disarm deliberately left
  open, or a route that SURVIVED a disarm aimed at the other three?** Identical live signatures;
  unanswerable from inside E2.
  *Value: walking ONE real item by hand before specifying the mechanism will teach more about the
  mechanism than specifying it first. Owner: CTO + Andrew, CVO investigating.*

  **>> E8.0 IS CLOSED. IT RAN BEFORE THE MECHANISM EXISTED, AND ITS RESULT IS THE SPEC'S BEST INPUT.
  base CVO investigated on doubt and reported back in ~8 minutes (20260731T162413Z), which IS Andrew's
  message-(3) middle step executing naturally.** <<

  **THE ANSWER: THE QUESTION HAD A FALSE PREMISE.** Neither successor nor survivor -- both branches
  assumed the disarm was trying to stop the chain. It was not.
  `infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py:243-262` **ENUMERATES ALL FOUR
  ARMED PATHS BY NAME**, including the aggregator direct-invoke, and states verbatim: *"Disabling the
  rules is a PLACEBO: the aggregator dispatches the identical mode=full run 14 minutes later, so
  'closing' two doors merely PROMOTES the next one... THE DOORS ARE NOT THE CHOKEPOINT. This function
  is: every path must pass through it. Assert here."* The route was KNOWN and ENUMERATED and is the
  DOCUMENTED REASON the control sits in the function rather than on the rules. The control is currently
  **RELEASED** -- sentinel `[RELEASED-BY-CTO-AND-COO-COSIGN]` matching in source AND on the live
  function config, negative control run -- under a **STANDING DAILY RELEASE (Andrew-worded + CTO + COO
  co-sign) that has been the NORMAL state since 2026-07-16.** Not a defect, not an incident.

  **THREE THINGS THE SPECIMEN TEACHES THE SPEC, ALL BINDING ON E8.2/E8.3:**
  1. **SOURCE FIRST, NOT ANOTHER INSTRUMENT** (CVO's method note). The item was escalated as
     "unanswerable from any instrument" and was answered in ~8 minutes **because the answer was in
     SOURCE and the doubt had been raised from trigger-layer evidence.** Write into the spec: **when a
     C3 state question is raised, THE FIRST STOP IS THE ARTIFACT'S OWN SOURCE.** Intent is authored
     somewhere; the estate's habit is to hunt for it in live state, where it is not.
  2. **A CONTROL CAN BE CORRECT, DOCUMENTED, LIVE -- AND INVISIBLE TO EVERY INSTRUMENT AIMED AT ITS
     LAYER.** Three instruments (trigger graph, resource policy, repo search by name) reported
     TRUTHFULLY about rules and policies; the control lives in neither. Only reading the function
     found it. **This is the strongest single argument for Layer 2 existing at all.**
  3. **A DOUBT CAN BE WELL-RAISED AND STILL REST ON A FALSE PREMISE.** Both offered branches were
     wrong. **The investigation step must be free to DISSOLVE a question, not only to answer it** --
     if E8.3's workflow only supports confirm/deny of the question as posed, it will force a wrong
     answer onto a well-intentioned doubt. Build the dissolve path.

**E8.1 -- ✅ FIRST ARTIFACT DELIVERED @3e241b2f93. THE POPULATION IS MEASURED.**
  **C3.ii -- 29 SEMANTIC VERTICALS / 138 CHAINS** (`comp-estate --list`, census vintage 2026-07-30;
  sub-denominators tallied INDEPENDENTLY rather than trusting the footer: 98 in-scope + 26 explicit-out
  + 14 unreviewed = 138, reconciles exactly).
  **C3.i -- 14 DETERMINISTIC STRUCTURES** (13 named `sys-*` + UNASSIGNED-RESIDUE), `comp-estate --matrix`.

  **BOTH OPEN QUESTIONS ANSWERED BY MEASUREMENT, NOT BY RULING:**
  (1) **The population needs NO NEW ENUMERATION.** `--structure SYS` drills ONE NAMED system and
      PRESUPPOSES the names; **`--matrix` already carries the population.** The item list is a READ.
  (2) >> **C3.i IS NOT A SUBSET OF C3.ii. C3 IS THE DUAL-PARTITIONED RUNG: TWO COMPLETE PARTITIONS OF
      THE SAME 138-CHAIN GROUND SET, CUT DIFFERENTLY. C3.ii is DECLARED never discovered; C3.i is
      DISCOVERED never declared.** So Andrew's "and potentially c3.i" **ADDS A SECOND AXIS with a
      different derivation and different failure modes -- it is NOT finer granularity on the 29.**
      *(Both COO and base CTO had been reading it as a widening. It surfaced before a spec fixed a
      scope, which is what E8.1 existed to do.)* <<

  **BASE CTO RULING 165136Z -- ZERO-IN-SCOPE VERTICALS ARE WALKED. DENOMINATOR IS 29, NOT 26.**
  Three verticals carry zero in-scope chains (causality 5, insurance 2, ops-internal 5). They are IN.
  >> **"NOTHING HERE IS IN SCOPE" IS A CLAIM THAT SILENTLY STOPS BEING TRUE. An unmaintained zero and
  an unexamined zero are INDISTINGUISHABLE FROM THE OUTSIDE, and the zero is the state most likely to
  go stale unnoticed BECAUSE NOTHING ABOUT IT EVER CHANGES VISIBLY.** Excluding them would exclude
  precisely the population whose staleness is invisible. << *(Same shape as the four audit logs being
  pre-conversion rather than safe, and `partial` keying off calendar coverage that carry-forward
  satisfies by construction.)*

  **BASE CTO RULING 165136Z -- THE RESIDUE IS NOT A WALKABLE ITEM, BUT ITS EXTENT IS A MAINTAINED FACT.**
  **NOBODY CAN ASSERT THE LIFECYCLE STATE OF "EVERYTHING UNASSIGNED" -- there is no producer for a
  residue; that is what MAKES it residue.** Asking the walk to label it would be **observer-inference
  wearing a declaration's costume**, the exact thing the producer-assertion rule forbids.
  **RESOLUTION: UNASSIGNED-RESIDUE enters as ONE item whose maintained fact is "the C3.i partition is
  incomplete by N chains across 7 verticals"** -- a claim about the PARTITION's completeness, not about
  the residue's state. **You can maintain a fact ABOUT the residue without asserting a state OF it, and
  the first is checkable while the second is not.**
  **CONSEQUENCE: C3.i-only is 13 SYSTEMS + 1 COMPLETENESS ITEM, not 14 systems.**

  **⏳ THE WALK DENOMINATOR IS ANDREW'S DECISION, NOT CTO's -- ESCALATED 165136Z, PENDING.**
  ```
    C3.ii, all verticals (CTO-ruled floor) ....... 29
    C3.i only .................................... 13 systems + 1 completeness item
    C3.ii + C3.i ("and potentially c3.i") ........ 43
  ```
  **Why it is not CTO's: the walk is CTO + ANDREW, so the denominator decides how much of the one
  NON-AGENT participant's time the process consumes.** CTO recommends **START AT C3.ii (29), defer C3.i
  to a second pass** -- and NOT because smaller is easier:
  > **C3.ii is DECLARED -> walking it MAINTAINS existing declarations = directly the producer-assertion
  > mechanism the E1 registry is missing, closing a loop already open.
  > C3.i is DISCOVERED -> walking it AUTHORS declarations for things nobody declared = a different act,
  > different confidence, different cost per item.
  > MAINTAINING A RECORD AND AUTHORING ONE ARE NOT THE SAME WALK.**
  Do the pass that closes the open loop, learn what an item COSTS IN WALL-CLOCK, then decide the second
  axis with evidence rather than an estimate. Andrew's own word was "*potentially* c3.i" -- **a hedge is
  correctly resolved with data from the first pass.**

**E8.1-RESIDUAL -- (original scope statement, retained for the reasoning)**
  Enumerate the C3.ii items, with the denominator printed and the enumeration's blindness stated.
  **THE ITEM LIST IS THE DENOMINATOR: without it, a labeling has no coverage claim and "we walked the
  C3 items" cannot be distinguished from "we walked the C3 items we happened to enumerate."**
  Open question for CTO: does the population come from `comp-estate --structure` / the C3.i drill, or
  does it need its own enumeration? *First artifact: the C3.ii item list with its count, its source,
  and an explicit statement of what the enumeration could NOT have seen.*

**E8.2 -- THE LABEL VOCABULARY AND RECORD SHAPE.** What a C3 state label IS, as a ratified vocabulary
  rather than free text.
  >> **BINDING CONSTRAINT (CVO's axis, raised BEFORE the build rather than found in the first audit):
  "NO DOUBT WAS RAISED" AND "THE ITEM WAS VERIFIED" MUST NOT BE BYTE-IDENTICAL IN THE RECORD.** An
  item walked past confidently otherwise produces the same artifact as one examined and confirmed --
  **absence of escalation is not evidence of correctness**, and the confidence behind a C3 label
  becomes unrecoverable later. The vocabulary must distinguish at minimum:
  `walked-no-doubt` · `doubt-raised-investigating` · `investigated-and-confirmed` · `unwalked`. <<
  **SECOND BINDING CONSTRAINT: A RECORDED AGREEMENT MUST NOT READ AS A VERIFIED FACT.** Three parties'
  state of belief at a vintage is enormously more than a mechanical signal and is still not a
  measurement. (WS-E5's producer-asserted lesson, applied one layer up: a carried declaration that
  reads as validated licenses consumers to trust an unverified claim -- the comp-iam deletion-warrant
  class.)

**E8.3 -- THE WALK MECHANISM AND THE DOUBT ESCALATION.** How CTO + Andrew traverse the items; what
  raises doubt; how CVO is invoked, investigates and reports; how Andrew + CTO confirm. Per message (3)
  exactly. *Design note: the escalation trigger is the throughput-determining parameter -- the model is
  bounded by the DOUBT RATE, not by the item count, which is why it scales where three-way sign-off
  would not.*

**E8.4 -- THE MAINTENANCE CYCLE (the Layer-1 / Layer-2 seam).** How the labeling is carried in the
  Kimi Review cycle so it is MAINTAINED rather than authored once. Must include a **revalidation
  cadence** -- a label with a vintage nobody re-derives becomes the frozen map the cardinal rule
  forbids. Seam with `~B`'s Layer-1 high-level signal, which is UNCHANGED by this series.

**E8.5 -- THE CONSUMERS.** lifecycle stage derives from the maintained label; **WS-E3's Tier-A
  keep-dormant annotations and WS-E2's DELIBERATE-HOLD STATUS field both DERIVE FROM this rather than
  each scavenging intent independently.** One intent source, several consumers.
  *Why this matters concretely: E2's hold-evidence sweep scavenged intent from records that happened to
  exist, and it FAILED ITS OWN POSITIVE CONTROL -- a hyphen-vs-underscore predicate under-counted one
  target 3x (4 hits -> 13 on the same corpus). Without that loud failure, four of five targets would
  have carried an under-counted evidence base and read as "none known." **A fail-safe that can be
  quietly starved of evidence is not fail-safe.** Scavenging is the wrong architecture; this series
  replaces it with a produced record.*
</the_series>

<constraints>
1. **base CTO OWNS THE SPEC.** This series carries scope, sequencing, owners and acceptance. It does NOT
   specify Layer 2's mechanism. Where the spec lands, it is authoritative.
2. **LAYER 1 IS NOT CHANGED.** `~B`'s Kimi user-input pipeline and the 07-30 semantic-evolution ruling
   stand as-is. Layer 2 is ADDITIVE -- Andrew's word is "an additional layer."
3. **MORATORIUM BINDS.** No alarms, monitors, freshness checkers, SNS or SES. A C3 label is a RECORD
   walked by people, not a detector that watches. If a deliverable here would page anyone, stop and
   route to COO.
4. **DO NOT LET THE MECHANISM BECOME THE DELIVERABLE.** The product is maintained lifecycle stage, not
   a labeling system. E8.0 (walking one real item by hand) exists to keep that honest.
5. No emojis / non-ASCII anywhere.
</constraints>

<acceptance_criteria>
SERIES-LEVEL (each sub-TO carries its own first artifact at dispatch):
1. The C3.ii item population is enumerable with a printed denominator and a stated blindness (E8.1).
2. A ratified label vocabulary exists that DISTINGUISHES walked-no-doubt from investigated-and-confirmed,
   and does not let a recorded agreement read as a verified fact (E8.2).
3. The walk + doubt-escalation + confirm workflow is exercised on at least one REAL item -- E8.0 is the
   candidate and it is already in the doubt state (E8.0/E8.3).
4. The labeling is carried in the Kimi Review cycle with a revalidation cadence, so it is MAINTAINED
   (E8.4).
5. lifecycle stage demonstrably derives from the maintained label, and at least one existing consumer
   (E3 Tier-A or E2 DELIBERATE-HOLD) is re-pointed to derive from it rather than scavenge (E8.5).
</acceptance_criteria>

<cross_domain_coordination>
- **base CTO (1.0.0_SA_CTO)** -- spec owner AND one of the two walking parties. Relayed in full at
  161438Z per Andrew's explicit instruction.
- **Andrew** -- the human walking party and confirming authority. Not a reviewer of this layer; a
  PARTICIPANT in it. That is unusual and it is the point.
- **base CVO (3.0.0_SA_CVO)** -- escalation-triggered investigator, NOT a co-equal signer. Corrected to
  CVO at 161517Z. Also holds the review gate on these TOs as deliverables (LD-0365).
- **`0.7.0_AE_CloudOps~B`** -- owns Layer 1 and leads Lifecycle Values; Layer 2 builds into its pipeline.
  Briefed 161347Z. NOT tasked by this series.
- **`0.0.0_AB_MSTR`** -- population/dispatch + the cross-seam; surfaces to Andrew per the 07-30 shape.
- **COO (2.0.0_SA_COO)** -- decomposition + pacing; splits each sub-TO out to its owner at dispatch.
</cross_domain_coordination>

<notes>
WHY THIS SERIES IS FILED BEFORE THE SPEC EXISTS: Andrew instructed a dedicated series wrapped into the
project, and the fabric's measured failure this session was lanes sitting on lists rather than starting.
E8.1 (the population + denominator) and E8.0 (walking one real item) are both startable with no
mechanism at all, and both produce information the spec needs. Filing the series now is what lets those
two start; everything downstream cites the spec.

WHY E8.0 IS FIRST AND NOT LAST: the "aggregator" item arrived at the doubt state on its own, from a lane
that traced it, refused to rule on it, and escalated -- which is the whole workflow occurring naturally
before anyone specified it. **A mechanism specified around a real walked item will be better than one
specified in the abstract**, and the specimen costs nothing because the work is already done.

THE HONEST STATEMENT OF WHAT THIS LAYER CAN AND CANNOT BE: it cannot make intent measurable. It makes
intent RECORDED, ATTRIBUTED and MAINTAINED -- which is strictly weaker than measurement and strictly
stronger than the nothing the estate has today. The failure mode to design against is not that the
labels are wrong; it is that a label READS as a verified fact to a consumer who was not in the room.
</notes>
</task_order>
