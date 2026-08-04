<task_order>
<to_id>MDPF_CANRTE.W2.modelb-spine-shadow</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>pending</status>
<priority>P1 (Phase-C wave 2; joint acceptance on record; Andrew "Proceed" 1706Z. SEQUENCE BEHIND W-1 -- this consumes its bindings)</priority>

<title>MDPF_CANRTE W-2: the Model-B firm-parameterized spine builder, build-alongside -- SHADOW staging writes only, 3-green-scheduled-cycles parity before any swap</title>

<context>
GOVERNING DOCUMENT: your Phase-B plan @c68f238e5 SS3 (W-2); the plan wins conflicts, surface
them. F-3 MODEL-B ruled; SS2.1 spine contract canonized; the swap idiom is the plan's own:
build-alongside -> DELTA=0 on 3 consecutive green SCHEDULED cycles -> single dispatch re-point.
</context>

<scope>
Exactly the plan's W-2: ONE firm-parameterized spine builder consuming W-1 bindings, emitting
the canonized contract per firm + the existing global fold mechanism, writing to the SHADOW
prefix -- AMENDED 1748Z by joint word (COO 174803Z + CTO co-word 174841Z, on your Rule-22a
implicitDeny finding): gold/mdpf_revamp/_canrte_shadow/{firm}/aggregate_aua_timeseries.json
(RE-SITED under the granted prefix; ZERO IAM change; consumer-exclusion mechanically grounded:
accrual reads roster-declared scopes and _canrte_shadow is not a roster firm, publisher derives
from portal/gold/mdpf listing only) -- on the same schedule, alongside the incumbents.
CTO CLEANUP RIDER (binding): the shadow tree gets an explicit REGISTERED DELETE STEP (at W-2
close or W-5, whichever the plan sequences) -- it dies by declared step, not by memory. The cottonwood L1 dim + its vocabulary/composition gates are
UNTOUCHED (declared vendor-necessity; today's Moderate-Income arc is live proof they are
load-bearing). NO dispatch re-point in this TO -- the swap is its own step gated on the 3-green
parity record; this TO delivers the builder + the shadow emission + the parity harness reads.
THE DELTA=0 CLASS (plan SS7) governs: stamp-normalized byte equality, mutant control exercised
BEFORE first gating use, parity read on SCHEDULED cycles only (never ad-hoc, NEVER#4).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>RULE-22a RIDER (JOINT-ACCEPTANCE BINDING, CTO 170636Z folds it into TO text): for the NEW prefix gold/mdpf_canrte_shadow/* -- aws iam simulate-principal-policy --policy-source-arn &lt;the runner role&gt; --action-names s3:PutObject --resource-arns &lt;one exact shadow key&gt; (ONE resource-arn per call); then the POSITIVE CONTROL as a SEPARATE invocation against a known-granted key</run>
      <expect>Shadow-prefix write allowed (or the grant gap NAMED before any code); positive control allowed in isolation. comp-iam is necessary-not-sufficient here -- it models (action), never (action,resource), and FAILS GREEN on new prefixes.</expect>
      <if_mismatch>STOP. A denied shadow write surfaces as an IAM change request (AE lane, TF only) BEFORE the builder lands -- never a silent retry loop at runtime.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io &lt;the incumbent spine builders&gt; --pipeline mdpf (baseline manifests) + confirm W-1 landed (bindings file present, validator green)</run>
      <expect>Baselines captured; W-1 tie-out green cited.</expect>
      <if_mismatch>STOP -- W-2 on unlanded bindings is building on air.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>the DELTA=0 comparator MUTANT control (perturb one series value in a copy; pipe-free rc)</run>
      <expect>Comparator FAILS on the mutant -- exercised before first gating use, captured verbatim. A comparator that cannot fail is not a control.</expect>
      <if_mismatch>STOP. Fix the comparator before any parity claim exists.</if_mismatch>
    </step>
    <step>
      <run>first shadow emission (may be direct-invoked for MECHANISM proof only -- it is NOT a parity cycle) + comparator vs incumbent, denominator printed</run>
      <expect>Mechanism works end-to-end; the run is labeled MECHANISM-PROOF, explicitly NOT counted toward the 3-green record.</expect>
      <if_mismatch>Fix before commit; a builder that cannot produce its shadow artifact has nothing to parity.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit + deploy">
    <step>
      <run>deploy per Rule-13; arm the parity record: 3 consecutive green SCHEDULED cycles, each comparator output logged with denominator + cycle id</run>
      <expect>TO closes at BUILD-COMPLETE with the parity record OPEN (0/3) -- the record accrues on the schedule; the dispatch re-point is a SEPARATE future step gated on 3/3 + COO/CTO read.</expect>
      <if_mismatch>Do not self-advance to the swap on any count less than 3/3 scheduled -- the count is the gate, not a formality.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Consumes W-1's file (same seat, self-sequence). Shadow prefix is NEW -- no consumer may read it
(it is not a serve key, not a staging key the accrual sees; confirm the accrual/publisher
listing scopes exclude it, cite the listing prefix at source). Incumbent builders untouched and
runnable throughout (they retire in W-4/W-5, not here). Today's supersede/composition-revert
stream: your chain-green tie reads ride their own thread -- keep artifacts separate.
</cross_domain_coordination>

<acceptance_criteria>
1. Rule-22a shadow-prefix verification captured (both invocations, isolated positive control).
2. Comparator mutant control captured BEFORE first gating use.
3. Builder deployed; shadow emission proven (mechanism-proof labeled as such); accrual/publisher
   listing-scope exclusion cited at source.
4. Parity record armed and honestly OPEN (0/3 scheduled) at TO close -- no swap, no re-point.
5. AMENDED 1748Z: the shadow-tree DELETE STEP registered (named owner + trigger: W-2 close or
   W-5 per plan sequencing) -- the CTO cleanup rider on the re-site co-word.
Plus: session log Compiler Tools section reproducing every run. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="plan">@c68f238e5 SS3 + SS7 (governing)</ref>
  <ref type="rulings">F-3 MODEL-B + SS2.1 contract (MDPF_CANRTE_FORK_RULINGS_20260804.md)</ref>
  <ref type="rider">Rule-22a shadow-prefix IAM (COO 165942Z rider, CTO 170636Z concur -- folded into Phase-1 text per the joint record)</ref>
  <ref type="sibling">MDPF_CANRTE.W1.route-bindings-config (consumes its output)</ref>
</references>

<dependencies>
  <dependency agent="0.4.0_DS_ClientPlatform" task="MDPF_CANRTE.W1.route-bindings-config" status="sequence-first at your seat"/>
</dependencies>
</task_order>
