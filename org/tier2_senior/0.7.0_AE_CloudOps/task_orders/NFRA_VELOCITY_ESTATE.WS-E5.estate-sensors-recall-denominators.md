<task_order>
<id>NFRA_VELOCITY_ESTATE.WS-E5.estate-sensors-recall-denominators</id>
<project>NFRA_VELOCITY_ESTATE</project>
<issued_to>0.7.0_AE_CloudOps~D</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>pending</status>

<priority>P3 by the PRD phase order, PULLED FORWARD TO NOW. It is KIMI-INDEPENDENT, and its ONE named blocking dependency -- the WS-E1 estate-contract registry -- IS NOW LIVE, built by you (@0bdca276e8). Andrew's rule is to defer the unsolvable and proceed past it; E5 is the largest piece of ESTATE work that is genuinely unblocked today.</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_VELOCITY_ESTATE_PRD.md -- WS-E5 (lines 173-203). Read the ENFORCEMENT MECHANISM paragraph (189-198) most carefully; it is the clause that makes this workstream real rather than a diary entry, and it is the clause that names YOUR registry as the carrier.</ref>
  <ref type="landed">@3d9ad164b2 -- YOUR OWN prior E5 finding, already landed: test_e5_recall_standard_arity_limits.py (216 lines) + the finding that L0a's boundary-report type is blocked on its ARITY, not its enums. You are not starting cold; you are resuming your own thread.</ref>
  <ref type="registry">org/modules/graph/estate-contracts/ -- the WS-E1 registry you built (@0bdca276e8, tranche 1: 7 mdpf subjects VERDICT PASS at PIN and HEAD; tranche 2 @c6b66d9bb7: model-portfolios vertical). E5's enforcement rides THIS, per PRD 193-197: "an estate detector IS a contracted process -- it registers in the WS-E1 estate-contract registry, and its contract carries its boundary declaration."</ref>
  <ref type="specimens">The nine same-day false-negative specimens (PRD 184-187) -- these become the estate-side conformance suite.</ref>
</references>

<amendment date="20260731T1438Z" by="2.0.0_SA_COO" subject="REGISTRATION IS OPEN -- the E2 `process:` defer does NOT cover estate detectors">
**BASE CTO RULED 20260731T143606Z: E5's REGISTRATION HALF PROCEEDS.**

The E2 split ("E1 breadth proceeds on `artifact:` subjects ONLY; `process:` subjects WAIT") appeared to
defer detector registration, since a detector registers as a contracted PROCESS. `~D` surfaced the
collision, declined to self-certify out of another workstream's arch-gate defer, and routed it. CTO's
ruling: **"I wrote `process:` when I meant *subjects E2 can invalidate*"** -- a deliberate
over-approximation designed to shrink once the real predicate existed. This is it shrinking.

**THE OPERATIVE PREDICATE IS FIELD-LEVEL, NOT SUBJECT-LEVEL. `process:` IS SUPERSEDED SCAFFOLDING:**

> A contract is exposed to E2 **IFF** it declares `cadence`, carries a `delivery_cadence` obligation,
> or names a subject that is an E2 **DELETION** candidate. **NOTHING ELSE DEFERS.**

E2 rewrites TRIGGER TOPOLOGY -- it changes WHEN a process fires, never WHAT a process is contracted to
do. `intent_source`, `lifecycle_class`, `revalidate_by`, `locality`, and **a detector's BOUNDARY
DECLARATION** are all untouched by a trigger re-sequencing.

**ONE CONDITION:** a detector contract that DOES declare `cadence` or a `delivery_cadence` obligation
does not block registration -- it joins the re-lint set (same treatment as the 9 pinned process
declarations: not wrong today, may become wrong, re-lint after E2 settles).

**THE GRAMMAR QUESTION IS NOW ANSWERED -- AND THE ANSWER HAS A LOAD-BEARING LIMIT.** base CVO
predicted no `contract_record` field could carry a boundary declaration, making a WS-C1 feedback the
probable first outcome. **CORE's WS-C7 had already shipped the schema.** Build against the CANONICAL
revisions, verified at source (all on origin, author `0.7.0_AE_CloudOps~Z`):

  `5b92f664da` 2026-07-31T10:26:35-04:00 -- **schema v2** (G1-G5 + the L-16 known-negative companion)
  `7a285a8c9f` 2026-07-31T10:40:44-04:00 -- **the REGISTRATION INVARIANT JOIN**

  ** `b2070b35a5` 09:19:01 is v1 and SUPERSEDED -- DO NOT BUILD AGAINST IT.** (Non-ASCII + broken
  tables; it was relayed as canonical in COO msg 144731Z and CORRECTED at 145333Z.)

Shape: `address_space` (kind / denominator / denominator_source / description) · `traversal_residue`
(reportable / channel) · `failure_direction` (self / basis). Every field RATIFIED-STRUCTURED or
DECLARED UN-DECIDABLE.

>> **CARRYING IS NOT CHECKING, AND CONFLATING THEM IS THE WORST AVAILABLE OUTCOME FOR THIS
WORKSTREAM.** `7a285a8c9`'s own subject: *"member 5 binds a declaration's SHAPE and can NEVER bind its
TRUTH, and saying so is the whole artifact."* **A boundary declaration is PRODUCER-ASSERTED** -- the
schema REQUIRES it, never DERIVES it.
  DECIDABLE (shape): `known_negative` present when `basis=exercised`; `denominator_grain` coarser than
  `row_grain` (D1_value_grain ORDERED); presence/membership.
  UNDECIDABLE (truth): is the declared address space the REAL one? **NO** -- producer-asserted, no
  observer oracle. Is `known_negative` a REAL discriminator? **NO** -- needs understanding what the
  tool means. **These are the standard's BOUNDARY, not its backlog -- name them as such, never as
  pending checks.**
**DO NOT let a registered boundary declaration READ AS VALIDATED.** That would license every
downstream consumer to trust a producer-asserted, unverified claim -- the comp-iam deletion-warrant
class (CLAUDE.md 22a), which is the surface E5 exists to CLOSE, not to build. C7's companion
discipline: *"a fully-conformant boundary declaration is compatible with every value being wrong."* <<

**PROVENANCE LESSON, RECORDED BECAUSE IT NEARLY LANDED IN THIS FILE:** the wrong hash reached this TO
through two agents who each grounded correctly and still got it wrong -- MSTR ground-verified the
CONTENT at the hash it was handed (correct for that hash) and COO relayed it without checking the hash
was the current revision. **Grounding content-at-a-hash is not verifying the hash is right.** A correct
read of a superseded artifact is a wrong answer carrying full provenance, and it travels FASTER than
an unsourced one because it looks grounded. CLAUDE.md already says it: a line citation without a
vintage is not a citation.

**ALSO FOLD INTO THE DENOMINATOR WORK:** the E2 lane measured **142 EventBridge rules + 12 Scheduler
schedules** against a carried 143 + 11 -- drift on BOTH limbs, in OPPOSITE directions, reported
UNRECONCILED. CTO: *"a sensor built on a census nobody reconciled inherits the gap."*
</amendment>

<objective>
Apply the recall standard to ESTATE DETECTORS -- freshness, drift, debt, trigger checks, deploy
verifies. Every detector emits its address space, its traversal residue, and its failure direction;
**a detector that cannot state what it could not have seen prints that as its first line.**

>> YOUR FIRST ARTIFACT: ONE REAL ESTATE DETECTOR EMITTING A BOUNDARY REPORT, REGISTERED AS A
   CONTRACTED PROCESS IN THE E1 REGISTRY. ONE. <<

Not the map of all detectors. Not the nine-specimen suite. Not the count of M. ONE detector, chosen
because you can exercise it today, carrying a boundary declaration in its contract, with its recall
denominator stated. Land it, report, then we scale the population.

That single artifact proves the whole architecture of this workstream -- that the E1 registry can
carry a detector contract at all -- and it is the thing that, if it does NOT work, invalidates the
PRD's enforcement design while it is still cheap to change. Find that out first.
</objective>

<constraints>
1. **THIS WORKSTREAM ADDS NO COMMIT-TIME GATES.** PRD framing (175-178): the estate's commit-time
   gating is dense and demonstrably catches; MEASUREMENT-TIME control is near-zero, and that empty
   quadrant is where 2026-07-29's control failures all lived. You are filling the measurement-time
   quadrant. If you find yourself designing a commit hook, you have drifted into E3's lane.
2. **NO ALARMS, NO MONITORS, NO FRESHNESS CHECKERS, NO SNS, NO SES -- AND THIS IS THE WORKSTREAM
   WHERE THAT IS HARDEST TO OBEY.** Standing moratorium, Andrew-direct 2026-07-28, VERBATIM: "It is
   an anti-pattern, and a waste of time for all parties." A "sensor" in this workstream is a
   BOUNDARY DECLARATION ON AN EXISTING DETECTOR -- it makes a detector state its own recall limits.
   **It is NOT a new thing that watches and reports.** You are not building detectors; you are making
   the ones that exist honest about what they cannot see. If your deliverable would page anyone, stop
   and route to me.
3. **A DETECTOR'S BOUNDARY REPORT IS ABOUT ITS BLINDNESS, NOT ITS COVERAGE.** The valuable line is
   "here is what I could not have seen," not "here is what I checked." The nine specimens are all
   cases where a detector reported confidently about a population it was structurally incapable of
   observing.
4. **DO NOT TOUCH LIFECYCLE VALUES.** They are Andrew-GATED on the Kimi user-input pipeline (~B owns
   it). `lifecycle_class` stays UNDECLARED. Your E1 breadth work is PARKED -- Andrew's steer was
   "mechanism proven, move on," and this TO is the "move on." The two PERMANENT values you wrote stay
   SUSPENDED as you marked them @7ed8a737ac; do not clear, revert, or extend them.
5. **THE ENFORCEMENT HALF IS PARTIALLY GATED AND YOU SHOULD KNOW WHERE THE CEILING IS.** PRD
   acceptance item 3 ("no new detector past the gate ramp without a contracted boundary declaration")
   rides the WS-E3 C-SILENT commit-gate ramp -- and E3 is gated behind lifecycle values. So the
   REGISTRATION half is reachable now; the DENIAL half is not. **Build to the ceiling and name it;
   do not pretend it is not there, and do not stall against it.**
6. No emojis / non-ASCII anywhere.
</constraints>

<compiler_tools_mandate>
  <phase id="1" when="before build">
    <step>
      <run>comp-which "what estate detectors check freshness and deploy state"</run>
      <expect>The detector population with dependency context. NOTE the PRD's own warning (190-192): estate detectors are NOT comp-tools -- no comp-manifest-check ever sees a freshness Lambda, an EC2-side gold check, or a deploy verify. **Expect this enumeration to be INCOMPLETE, and print what it could not have seen -- which is the workstream's own standard applied to its first step.**</expect>
      <if_mismatch>An incomplete enumeration here is not a tool failure, it is the FINDING that motivates the registry-reuse design. Record the gap with its denominator.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="registering the contract">
    <step>
      <run>The E1 registry's own declare-time lint (the A7.1 lint @80488b2e8b) against your detector contract</run>
      <expect>The detector contract PASSES the same lint every other contracted process passes -- one registry, one gate. If a detector contract needs a field the grammar lacks, that is a WS-C1 feedback, routed loudly, NOT worked around locally.</expect>
      <if_mismatch>Route the grammar gap to base CTO. Do not extend the grammar yourself -- you are the maintaining lane for the registry's CONTENT, not its VOCABULARY.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="exercise">
    <step>
      <run>Run the detector and observe its boundary report as its FIRST line of output. Then MUTATE: make its address space wrong and confirm the report changes.</run>
      <expect>A boundary report that moves when the boundary moves. A static string that says "I might have missed things" is not a boundary report -- it is a disclaimer, and it is the two self-authored unfailable acceptance criteria from the specimen list, recreated.</expect>
      <if_mismatch>If the report cannot go wrong, it cannot be right. Rebuild it.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
FIRST ARTIFACT (report on this alone):
1. ONE real estate detector emits a boundary report as its first line: address space + traversal
   residue + failure direction, with its recall denominator stated.
2. That detector is REGISTERED as a contracted process in the WS-E1 estate-contract registry, and its
   contract carries the boundary declaration. It passes the same declare-time lint as every other
   contract.
3. The boundary report is MUTANT-PROVEN: it changes when the address space changes.
4. The registry-reuse design is confirmed WORKABLE -- or, if it is not, that is reported as a BLOCKING
   architectural finding while it is still cheap to redesign. **A negative result here is a
   first-class deliverable, not a failure.**

SUBSEQUENT (do not block artifact 1 on these):
5. N of M estate detectors emitting boundary reports, both numbers PRINTED -- M enumerated at run
   time, never carried, and stated with what the enumeration could not have seen.
6. The nine-specimen conformance suite green estate-side (AccessDenied-indistinguishable-from-absent;
   list-rules Scheduler blindness; name-substring predicates; UTC-4 LastModified misreads; terraform
   "No changes" as success; rc=0 PASS/STALE conflation; not-due default literals; the two
   self-authored unfailable acceptance criteria). Your landed arity test @3d9ad164b2 is the seed.
7. The E3-gate-ramp ceiling named explicitly in the deliverable, with what is reachable now vs what
   waits on E3.
8. Session log with a Compiler Tools section reproducing each run vs expect.
</acceptance_criteria>

<cross_domain_coordination>
- **SEAT RESOLVED 20260731T142036Z (MSTR).** Andrew's steer on your E1 work was "mechanism proven,
  move on" -- E1 breadth is PARKED and your E1 thread is COMPLETE, not suspended mid-flight. This TO
  is your next lane. Your "awaiting Andrew's scope steer" state is resolved; the steer arrived.
- **You run in PARALLEL with WS-E6** (harness R4 trigger binding), on a lane MSTR spawns fresh. E5 and
  E6 are independent by construction. A cross-need is a seam finding routed to me, not a wait.
- **`~B` owns the Kimi user-input pipeline and will LEAD Lifecycle Values** (Andrew-authorized ~1320Z).
  Lifecycle values are ITS work, not yours. Do not advance them, and do not treat this TO as a
  reopening of that thread.
- **`~A` owns the Aug-1 14:00Z ETFS month-end fire -- HARD DEADLINE TOMORROW.** If a detector you
  touch sits on the ETFS/inf path, STOP and route to me before exercising it.
- base CTO = arch-gate (grammar/spec). base CVO (3.0.0_SA_CVO) verifies.
</cross_domain_coordination>

<notes>
WHY YOU ARE THE RIGHT LANE FOR THIS: E5's entire enforcement design rests on the claim that an estate
detector can be expressed as a contracted process in the E1 registry. You BUILT that registry, you
landed both tranches, and you found its first four lint defects -- including three that were invisible
to your own conformance check because you wrote its allowlist. Nobody else can falsify the registry-
reuse design as fast, and falsifying it early is worth more than confirming it late.

WHY THE FIRST ARTIFACT IS ONE DETECTOR AND NOT A SURVEY: a survey of detectors produces a number, and
a number here would be the exact failure the workstream exists to prevent -- a coverage count with an
unexamined denominator, reported by an enumeration that structurally cannot see freshness Lambdas or
EC2-side checks. One detector, fully contracted and mutant-proven, tells you whether the architecture
holds. The survey tells you a number you would then have to distrust.

ON THE STANDARD YOU ARE ENFORCING, APPLIED TO YOURSELF: this workstream's whole product is detectors
that state what they could not have seen. Your first artifact's boundary report is the first instance
and it will be read as the template. Make its blindness section the honest one -- including, if it is
true, that the enumeration that found this detector could not have found several others.

**AND THE SAME STANDARD BINDS E5's OWN REGISTRATION -- THIS IS THE LOAD-BEARING ONE.** A boundary
declaration is PRODUCER-ASSERTED and the registration invariant binds SHAPE, never TRUTH. So E5 will
register declarations it cannot verify. **The honest move is to DECLARE that and say so plainly in the
deliverable** -- E5's product is detectors that state what they could not have seen, so **E5 declaring
a boundary it cannot verify, and saying so, is the standard applied to itself. It has no standing to
demand of detectors what it will not do.** A registration half that quietly presents producer-asserted
claims as validated would make E5 the exact surface it exists to close.

**BYPRODUCT INBOUND FROM WS-E2 -- USE IT, DO NOT RE-DERIVE IT.** The E2 lane's violation predicate
excludes three classes from its schedule-floor count: served-output GUARDS
(`opal-{inf,cot,49f}-served-guard-on-write`), security/audit DETECTORS (`FIRMSEP-s3-direct-access-bypass`,
`opal-globgrph-cloudtrail-mgmt`, `moltbot-ssm-sendcommand-alert`), and infrastructure state WATCHERS
(`opal-inf-ec2-state-change-monitor`). **Those exclusions ARE estate detectors -- your population.**
E2 is instructed to name them with members and counts in a directly consumable form rather than
letting them exist only as a subtraction. It is a LIVE-AWS-GROUNDED partial census of detectors your
own enumeration is expected to miss (PRD 190-192: no comp-manifest-check sees a freshness Lambda or an
EC2-side check). **It is partial and it is not your denominator** -- state it as a contributing source
with its own provenance, never as the population.
</notes>
</task_order>
