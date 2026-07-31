<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E8.c3-state-labeling-series</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>SERIES PARENT -- each sub-TO splits out to its named owner at dispatch</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending -- E8.1 STARTABLE NOW; E8.2-E8.5 ride base CTO's spec</status>

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

<the_series>
**E8.0 -- THE WORKED SPECIMEN (available NOW, needs no mechanism).**
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

**E8.1 -- THE ITEM POPULATION AND ITS DENOMINATOR. STARTABLE NOW; PRECONDITION FOR EVERYTHING ELSE.**
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
