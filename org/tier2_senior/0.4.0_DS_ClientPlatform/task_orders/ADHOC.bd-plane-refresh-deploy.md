<task_order>
<to_id>ADHOC.bd-plane-refresh-deploy</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<date>2026-08-04</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ADHOC" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending</status>
<!-- deployed 2026-08-04T01:05:46Z MATCH-verified (ledger 20260804T010546Z); closes on the
     next SCHEDULED 49f cycle reading no behavioral delta (acceptance per GO) -->
<priority>P2 (the DEPLOY leg of the reviewed bd refresh -- ~B's review @28d0ce03ed verdicts both changes SAFE-AS-IS, zero excludes, so NO CTO ruling gates it; CTO's d-2 deliberate-act boundary is SATISFIED BY the review. Sequence at your seat with the T4.A residue; NOT tonight-urgent.)</priority>

<title>Deploy the reviewed cot_bronze_ingest.py to the bd plane -- pinned-hash pre-flight, expected runtime change NONE (falsifiable), next scheduled 49f cycle is the evidence</title>

<context>
Your own 232021Z item-4 finding, reviewed per CTO's split ruling (~B analysis 005416Z handoff to
you; deploy = DS lane per Rule 13): the bd plane's deployed copy of the SHARED
opal-data-bd/code/bronze/cot_bronze_ingest.py sits at an exact fork point (@4632383568, deployed
36s after its own commit) -- the "six weeks" collapsed to TWO commits, both verdicted SAFE-AS-IS
on bd (the LAG=1 fix is env-explicit, 49f no-op; the retry-net generalization @545bde4e9a), empty
residual, no misc bucket. Review doc: org/tier2_senior/0.7.0_AE_CloudOps~B/
BD_PLANE_SIXWEEK_DELTA_REVIEW_20260804.md @28d0ce03ed. What you deploy must BE what was reviewed
-- the pinned-hash law.

THE LOAD-BEARING CLAUSE (~B verbatim, binding): pre-flight assert that the bd target still reads
sha256 3db53a8b... / ETag fa9fd5a9652e7c7aea60776ed469c773 BEFORE any write -- "if it does not,
STOP, because the reviewed delta would no longer be the deployed delta."
</context>

<scope>
1. PRE-FLIGHT: head-object + hash the live bd target; assert it matches the review's pinned
   values (full values in the review doc). Mismatch = STOP + report (the review re-runs; nothing
   deploys).
2. DEPLOY repo HEAD of the shared source to opal-data-bd/code/bronze/ per Rule 13 (commit-gate
   already clean at HEAD; safe-deploy; MATCH verify post-deploy).
3. EXPECTED RUNTIME CHANGE ON bd: NONE -- stated falsifiably: any behavioral difference in the
   next scheduled 49f cycle is a FINDING, not noise (pre-registered interpretation).
4. Ledger entry; acceptance = the next SCHEDULED bd/49f cycle runs with no behavioral delta
   (read, never hand-run -- NEVER#4).
5. Firm separation binds: this closes a bd-plane deployment divergence; nothing cot-side changes.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="pre-flight">
    <step>
      <run>aws s3api head-object on the bd target + sha256 of a pulled copy # rail-checked: the pinned-hash assert IS the task's ground</run>
      <expect>ETag fa9fd5a9652e7c7aea60776ed469c773 exact; sha256 matches the review's pin.</expect>
      <if_mismatch>STOP. The reviewed delta is not the deployed delta -- report to COO+CTO+~B; the review re-runs.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="deploy">
    <step>
      <run>safe-deploy to opal-data-bd/code/bronze/; comp-pipescript deployed cross-check (NOTE its Model-B blindness -- ~B routed it to CTO: it reads per-tree and reported all-up-to-date while bd was 6wks stale; the MATCH you need is the bd-tree one, verified by direct hash compare, not the tool's summary line)</run>
      <expect>bd target's post-deploy hash == repo HEAD's; direct compare captured.</expect>
      <if_mismatch>STOP + rollback per safe-deploy; report.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after">
    <step>
      <run>ledger entry; report to COO + CTO + ~B (closing their handoff loop); next scheduled 49f cycle read = acceptance</run>
      <expect>No behavioral delta on the scheduled cycle; ledger closed same-session for the deploy leg.</expect>
      <if_mismatch>A behavioral delta = a FINDING (the review's SAFE-AS-IS verdict is then falsified -- route to CTO with the delta).</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Closes the Model-B one-source violation at the deployed layer for this script. ~B's review is the
binding review-of-record (CTO d-2 satisfied); their handoff 005416Z carries the pins. The
comp-pipescript Model-B blindness is CTO-routed separately -- your direct-hash verify is the
compensating control this deploy uses.
</cross_domain_coordination>

<acceptance_criteria>
1. Pre-flight assert captured (match, or the STOP path taken).
2. Post-deploy direct hash compare == repo HEAD; ledger entry.
3. Next SCHEDULED 49f cycle: no behavioral delta (pre-registered: any delta is a finding).
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="review">~B @28d0ce03ed (verdicts + pins) + handoff 005416Z</ref>
  <ref type="rulings">CTO 232535Z d-2 + 000023Z rider 2 (review/deploy split; Rule 13)</ref>
  <ref type="finding">Your 232021Z item 4 (the divergence)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
