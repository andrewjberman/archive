<task_order>
<to_id>MDPF_GLOBAL.T5A.legacy-inventory-reader-census</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~F</issued_to>
<date>2026-08-03</date>
<status>staged</status>
<priority>P1 (spine: unblocked by T1.A @389c528ddb; the delta census here also ANSWERS whether T1.B happens at all -- ruling item 5. CENSUS ONLY: T5.B kills stay gated on CANON PROVEN.)</priority>

<title>T5.A: Legacy inventory + reader census -- every legacy publisher/scheduler/bucket/route enumerated with per-artifact READER evidence, dispositioned into a kill-list</title>

<context>
MDPF_GLOBAL PRD Addendum C s.C.4 T5.A row, unblocked by T1.A's census @389c528ddb. You are the
right seat: your T3.A census + phantom-route deep capture @297db6f6bf produced half of this WS's
seed evidence, and the method (live-grounded, denominator-printed, plane-labeled) is the same.

THE DECISION THIS CENSUS FEEDS (T2.B ruling @440d16e018, items 4-5): the underscore plane + runner
chain retire at T5 CONDITIONAL on YOUR delta census -- and "if the runner chain retires whole,
T1.B's mdpf migration is satisfied by elimination." T1.B authoring is HELD at COO pending your
verdict. Your census answers: what does the runner chain uniquely provide that the canonical
revamp/hyphen chain does not, and who actually READS each legacy artifact.

SEED EVIDENCE, ALL BANKED (fold in, re-verify only where stated):
1. CTO reader items (ruling item 4): portal_data_proxy /aum/aggregate-mdpf reads the top-level
   UNDERSCORE file; the top-level HYPHEN key /api/general/mdpf/aggregate-aua-timeseries.json
   resolves to DOES NOT EXIST (your 403 capture, S3-origin-answered, plane-labeled).
2. Your @297db6f6bf contrast -- ADJUDICATE IT HERE: underscore root artifact (as_of_last=07-31,
   n_dates=436) vs live consumer route global/ hyphen key (as_of_last=07-30, n_dates=453), two
   200s on one behavior disagreeing on frontier AND coverage, mechanism INFERRED. T5.A retires
   that INFERRED label: which chain writes each, why the axes differ, which is canon-conformant.
3. Dead root fetcher portal-proxy.ts:505-509 (403, zero page consumers) -- CTO 210706Z: goes on
   the kill-list as a PORTAL-SIDE item, not just the route.
4. T1.A inputs @389c528ddb: LEGACY-KILL-CANDIDATE canonical-schwab-si2-download-schedule
   (nominated only -- NB the 49F converter ops are Andrew-deprecated off main chain, MEMORY
   standing; disposition with that context); UNKNOWN-LOUD smartx-daily-export-trigger +
   smartx-model-monthly-pull-daily (disable rationale unrecoverable from live state); F5 legacy
   json/mdpf plane has NO scheduled producer, writers dispositioned CANONICAL-retained per the
   HOLD doc read in full.
5. The banked json/mdpf retire BLOCKER: dim_mdpf_aggregate_aua_timeseries.py:567 bare
   except -> {} fails silent -- T5.B's enumerated pre-kill fix; your census carries it as the
   blocking annotation on every json/mdpf entry.
6. Publish-vs-vintage law from your own capture: an S3 Last-Modified on this path is a publish
   event, not a data-vintage claim -- apply when reading access/write evidence.

NAME-COLLISION TRAP (s.C.4 acceptance names it): json/mdpf 4-way collision -- hyphenated
account-distribution.json is THE LIVE SERVED PORTAL BELL (MEMORY standing). EVERY entry resolves
by FULL bucket + key, never basename.
</context>

<scope>
1. Enumerate EVERY legacy publisher / scheduler / bucket / route on the MDPF estate: the
   underscore platinum plane, the runner chain (mdpf-daily-trigger -> SSM -> runner EC2 ->
   opal-data-mdpf/code/), the legacy json/mdpf plane, opal-data-mdpf's EventBridge attachments
   (memo-named example -- enumerate explicitly), legacy routes. Denominator printed per class;
   T1.A's census + T3.A's route map are your seeds, live state is your ground.
2. Per-artifact READER evidence: code refs (comp-grep/comp-blast + hand-verified dynamic reads --
   remember comp-pipescript is blind to the assets tree AND to dispatch-staged writes; the
   coverage build is only STAGED, so hand-derive where the tool is blind and say so) + CF/S3
   access logs over a STATED window (existing logs only -- no new logging, moratorium). State the
   window and its limits honestly: a quiet log over a short window is weak absence evidence,
   label it as such.
3. Disposition every entry into the kill-list: {RETIRE-WHOLE-CANDIDATE / RETIRE-AFTER-REPOINT /
   RETAIN-CANONICAL / UNKNOWN-loud}, each with reader-count evidence + the blocking annotations
   (item 5 above; T1.B-elimination implications flagged per entry).
4. THE DELTA CENSUS VERDICT (the T2.B item-5 answer, called out as its own deliverable section):
   what the runner chain uniquely provides vs the canonical chain -- feature-by-feature, with the
   underscore/hyphen axis disagreement (seed item 2) adjudicated. End with an explicit
   RETIRES-WHOLE: yes/no/conditional recommendation for CTO.
5. READ-ONLY: nothing is killed, disabled, or re-pointed in this WS. No alarms/monitors.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before census">
    <step>
      <run>Read T1.A census.yaml @389c528ddb + your own T3.A cache-map + comp-estate mdpf</run>
      <expect>Seed inventory assembled; known instrument gaps carried (comp-estate: accrual-as-C0 + cot-legs-unrendered; comp-pipescript: assets tree + dispatch-staged writes).</expect>
      <if_mismatch>STOP. A seed contradiction (census vs estate map) is a finding to resolve before enumerating.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on each legacy producer fn before dispositioning it</run>
      <expect>EXTRACTED consumers enumerated -- treat as LOWER BOUND (the tool's own note); dynamic/FUNC-key reads hand-greped per its guidance.</expect>
      <if_mismatch>An entry dispositioned RETIRE-* on tool output alone without the dynamic-read grep is REWORK.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="during census, before commit">
    <step>
      <run>live enumeration: opal-data-mdpf EventBridge attachments + bucket notification config + S3 access-log reads over the stated window # rail-checked: T5.A reader census; live reads ARE the census act</run>
      <expect>Denominators printed per class; every claim plane-labeled (desired/applied/exercised per Rule 22a).</expect>
      <if_mismatch>STOP. An unpaginated or unlabeled enumeration is not a census.</if_mismatch>
    </step>
    <step>
      <run>adjudicate seed item 2: source-confirm which chain writes the underscore root vs the global/ hyphen key and why n_dates/frontier differ (file:line @ commit)</run>
      <expect>INFERRED label retired -- mechanism cited and coherent with T2.A's chain map.</expect>
      <if_mismatch>Deliver best-evidence + keep INFERRED, loud -- do not ship an unexercised adjudication.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>report to COO + CTO: kill-list path + commit + per-class denominators + the RETIRES-WHOLE verdict + T1.B implication</run>
      <expect>CTO gets the delta-census verdict for the item-5 call; COO unblocks-or-cancels T1.B on it.</expect>
      <if_mismatch>A report without the verdict section is REWORK -- the verdict IS the deliverable.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only census; no shared writes. T2.C (AE base) is implementing the schedule floor concurrently
-- their new schedule is NOT a legacy entry; coordinate so your census snapshot states its vintage
relative to their apply (before/after). T1.C (0.2.0_DS) is restructuring the cot leg -- its 6d
circular re-stage is in your enumeration path; their checklist @5b42aff274 is context, their rows
are NOT kill-list entries. The coverage build (0.8.0~B, staged) retires your hand-derive burden
only when it lands -- do not wait on it.
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. Denominator printed; every entry carries reader-count evidence and disposition.
2. opal-data-mdpf's EventBridge attachments enumerated (memo-named example).
3. The json/mdpf 4-way name-collision trap explicitly resolved by FULL bucket+key per entry.
Plus (this TO's additions, CTO-sourced): the delta-census RETIRES-WHOLE verdict section with the
T1.B-elimination implication; seed item 2's INFERRED label retired or loudly kept; the :567
bare-except blocker annotated on every json/mdpf entry.
Plus standing norms: every causal claim cites file:line @ commit or is labeled INFERRED; no new
alarms/monitors; access-log windows stated with honest limits.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (s.C.2 T5 + s.C.3 ruling items 4-5 + s.C.4 T5.A row)</ref>
  <ref type="seed">T1.A census @389c528ddb; your T3.A @0f71d7d2f9 + deep capture @297db6f6bf; T2.A diagnosis @0b5acf3148</ref>
  <ref type="blocker">dim_mdpf_aggregate_aua_timeseries.py:567 (MEMORY standing json/mdpf retire blocker)</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3; CTO T2.B ruling 205937Z + 210706Z item 1</ref>
</references>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="MDPF_GLOBAL.T1A.trigger-route-census" status="complete"/>
</dependencies>
</task_order>
