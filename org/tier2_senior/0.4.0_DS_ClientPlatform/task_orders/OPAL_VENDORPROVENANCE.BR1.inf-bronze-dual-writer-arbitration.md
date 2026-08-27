<task_order>
<to_id>OPAL_VENDORPROVENANCE.BR1.inf-bronze-dual-writer-arbitration</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_VENDORPROVENANCE, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
<priority>P2-staged (COO ownership disposition on CTO routing 222345Z. NOT blocking T4.A or the T2.C apply. ACTIVATES on T4.A completion or explicit COO GO -- whichever first. Staged-not-parked: this TO exists so the finding cannot close as "covered."</priority>

<title>BR1: the inf bronze DUAL WRITER (6 dim feeds, same key, last-writer-wins) -- decision brief for the CTO arbitration ruling, then implement</title>

<context>
CTO routing 222345Z on your own T4.A tranche-1 limitation note, ELEVATED from a verdict-doc
narrowing to a first-class provenance defect: for the inf dual-producer dims, BOTH producers
(the per-dim Lambda crons AND the EC2 orchestrator -- your WS-1 tranche-1 finding) write the
SAME bronze key, last-writer-wins. Attribution collapses BEFORE silver exists: "which producer
produced the served bytes" is UNANSWERABLE BY CONSTRUCTION -- the losing write is gone before
any downstream instrument can see it.

WHY THIS IS NOT COVERED BY T2.B (CTO explicit): unification settled the GOLD/serving plane;
this is BRONZE, one layer upstream. And the reassuring measurement must not close it: your dup
rate 0.0 across 40 partition-measurements says the writes AGREE TODAY -- a no-arbitration dual
writer's FIRST disagreement is silent AND unattributable. Same "two producers, no arbitration"
class MDPF_DEBTCLEAN names, one layer further upstream.

RULE 17a CONTEXT (CTO): a bronze key whose content depends on which producer ran last is raw in
FORMAT only -- the arbitration fix RESTORES bronze's one job, it does not bend the rule.

ALREADY DONE (do not redo): you are raising the affected feeds to NAMED-RISK registry rows
(unattributable-by-construction wording) per CTO's direct instruction -- that is the RISK record;
this TO is the WORK record.
</context>

<scope>
PHASE A -- THE DECISION BRIEF (this TO's first deliverable; CTO rules on it):
1. Enumerate the affected feeds precisely (the 6 dual-written dims + any others the census
   missed -- denominator printed): per feed, both producers' write paths file:line @ commit,
   trigger/cadence of each, and the measured overlap window.
2. Arbitration OPTIONS with costs, per the CTO fix shape: (i) SINGLE WRITER (which producer
   retires per feed; what breaks); (ii) DISTINCT KEYS per producer (key schema change; what
   downstream reads must learn). Recommend per feed; label INFERRED where costs are estimated.
3. Route the brief to CTO (cc COO) -- the arbitration choice is an architecture ruling.
PHASE B -- IMPLEMENT per the ruling (may be re-assigned by COO to the AE lane for Lambda/EC2
legs at ruling time; your Phase-A brief should say which legs are DS-lane vs AE-lane).
OUT OF SCOPE: any interim "monitoring" of the dual writes (moratorium); any change before the
CTO ruling.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="Phase A, before the brief">
    <step>
      <run>comp-estate &lt;inf vertical&gt; + comp-pipescript io on each producer script (both families); hand-derive where tool-blind, labeled</run>
      <expect>Both write paths per feed confirmed at source with file:line @ commit; trigger map per producer.</expect>
      <if_mismatch>A feed with only ONE confirmed writer leaves the affected set -- shrink the denominator honestly, do not pad the finding.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on each producer fn</run>
      <expect>Downstream consumers of each producer's OTHER outputs enumerated -- the single-writer option's cost baseline.</expect>
      <if_mismatch>Unexpected consumers widen the brief, not the fix.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="brief before routing">
    <step>
      <run>verify the NAMED-RISK registry rows landed (your own parallel instruction from CTO) and cross-cite them in the brief</run>
      <expect>Risk record and work record point at each other.</expect>
      <if_mismatch>Land the rows first -- the brief must not be the only carrier of the risk.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after CTO ruling">
    <step>
      <run>implementation per ruling (Phase B; possibly re-assigned) -- its own mandate authored at ruling time</run>
      <expect>Phase B TO/amendment carries the ruling verbatim.</expect>
      <if_mismatch>No implementation before the ruling, none outside it.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The producers span DS scripts and AE-owned Lambda/EC2 triggers -- Phase A is read-only census
(no gate); Phase B lane-splits per the brief. The inf tree carries the F2-era posture history --
any Phase-B infra change lands under full deploy law with the current posture checked at that
time. WS-5's completeness evaluator inherits the NAMED-RISK rows regardless of this TO's timing.
</cross_domain_coordination>

<acceptance_criteria>
1. Phase A brief: affected-feed denominator printed; both write paths per feed cited file:line @
   commit; both arbitration options costed per feed with a recommendation; DS-vs-AE lane split
   stated; routed to CTO cc COO.
2. NAMED-RISK registry rows cross-cited (risk record != work record, both exist).
3. Phase B proceeds only on the CTO ruling, carried verbatim.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="routing">CTO 20260803T222345Z (elevation + fix shape + not-covered-by-T2.B grounds)</ref>
  <ref type="finding">Your T4.A tranche 1 @a356870e40 (attribution structurally unobservable) + WS-1 tranche 1 (dual-producer overlap)</ref>
  <ref type="class">docs/architecture/MDPF_DEBTCLEAN_PRD.md (the two-producers-no-arbitration class)</ref>
</references>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_GLOBAL.T4A.exemplar-table-verdicts" status="pending (BR1 activates on T4.A completion or explicit COO GO)"/>
</dependencies>
</task_order>
