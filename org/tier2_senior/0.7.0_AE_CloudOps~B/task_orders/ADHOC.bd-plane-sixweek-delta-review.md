<task_order>
<to_id>ADHOC.bd-plane-sixweek-delta-review</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~B</issued_to>
<date>2026-08-04</date>
<status>staged</status>
<priority>P2 (CTO owner word 000023Z rider 2: the REVIEW is yours; >> THE DEPLOY IS NOT -- DS lane per Rule 13, handoff stated up front. << ACTIVATES when the CI-R7R8 fork resolves.)</priority>

<title>bd-plane six-week delta REVIEW (analysis only): the full 07-09 -> current diff of the shared cot_bronze_ingest.py, reviewed change-by-change -- then a DS-seat deploy handoff</title>

<context>
0.4.0_DS's pre-deploy baseline read (232021Z item 4) found the bd plane's DEPLOYED copy of the
SHARED script opal-data-bd/code/bronze/cot_bronze_ingest.py is SIX WEEKS diverged from the cot
plane's (07-09 / 56,885B vs 07-24+ / 72,808B, now further ahead with the LAG=1 fix
@bf4c0aabbe). Model-B one-source is violated at the DEPLOYED layer.

CTO BOUNDARIES, both verbatim-binding:
1. (d-2, 232535Z): "the bd refresh is a DELIBERATE ACT... WITH ITS OWN REVIEW OF THE FULL
   DELTA, never a sync. Six weeks of unreviewed change entering the 49f runner because it was
   convenient is the failure I ruled against."
2. (rider 2, 000023Z): the DEPLOY leg is DS LANE per Rule 13 (bronze script under data/*) --
   "do not let the review seat carry the deploy on momentum." YOUR deliverable is the review;
   the handoff to a DS seat is PART of this TO.
</context>

<scope>
1. Assemble the full delta: the deployed bd copy (pull + hash it first -- pin what you actually
   reviewed) vs current repo HEAD of the shared source. Enumerate every change in the window
   (git log the source path 07-09..HEAD), grouped by change intent (the LAG=1 fix, the retry-net
   generalization @545bde4e9a, everything else -- no "misc" bucket).
2. Per change: bd-plane impact assessment -- does it alter 49f runner behavior, and is that
   alteration WANTED on bd (env-explicit guards like the LAG fix's 49f no-op are the pattern to
   verify, not assume)? Verdict per change: SAFE-AS-IS / NEEDS-BD-CONFIG / EXCLUDE-CANDIDATE
   (an exclude-candidate = a finding to CTO, since one-source means bd cannot diverge forever).
3. Deliverable: the review doc (change ledger + per-change verdicts + the recommended deploy
   form) -> CTO (ruling if any EXCLUDE-CANDIDATE exists) + the named DS seat + COO.
4. THE HANDOFF (in this TO, not after it): the deploy executes at a DS seat per Rule 13 on your
   review doc -- recommend the seat in your report (0.4.0_DS holds the cot-plane context;
   0.2.0_DS holds the mdpf chain context), COO routes the deploy TO on your recommendation.
5. READ-ONLY throughout: no deploy, no sync, no bd-plane write of any kind from your seat.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="assemble">
    <step>
      <run>aws s3 cp the deployed bd copy + sha256 it # rail-checked: pinning the reviewed artifact IS the review's ground; comp-pipescript deployed cross-check per-tree</run>
      <expect>The reviewed artifact pinned by hash; repo-side window enumerated via git log on the source path.</expect>
      <if_mismatch>A review of an unpinned artifact is a review of nothing -- STOP.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="review">
    <step>
      <run>per-change ledger with intent grouping + bd-impact verdicts, cited file:line @ commit</run>
      <expect>Every change carries a verdict; env-guard claims VERIFIED at source, not assumed.</expect>
      <if_mismatch>An unverdicted change is UNKNOWN-loud and blocks the deploy recommendation.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="handoff">
    <step>
      <run>review doc -> CTO + recommended DS seat + COO; deploy TO authored BY COO on your recommendation</run>
      <expect>The deploy leg leaves your seat explicitly; the bd runner's next scheduled cycle post-deploy is the eventual acceptance evidence (the DS TO's, not yours).</expect>
      <if_mismatch>Any bd-plane write from your seat is a lane violation -- there is no momentum exception.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Firm separation: bd tree analysis only; the cot plane is your COMPARISON source, never a write
target. The cross-tree divergence census (AE base, gap-filler) may surface SIBLING divergences
-- cross-cite if their report lands first; your review stays scoped to this one script. DS
deploy seat gets the pinned hashes so what they deploy IS what you reviewed.
</cross_domain_coordination>

<acceptance_criteria>
1. Reviewed artifact pinned by hash; change ledger complete over the window (no misc bucket);
   per-change verdicts cited.
2. EXCLUDE-CANDIDATEs (if any) routed to CTO as findings before any deploy recommendation.
3. The DS handoff executed as specified -- deploy recommendation + seat named; zero bd-plane
   writes from your seat.
Plus: session log Compiler Tools section reproduces every <run> with observed output and
explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="rulings">CTO 232535Z d-2 (deliberate-act boundary) + 000023Z rider 2 (review/deploy split)</ref>
  <ref type="finding">0.4.0_DS 232021Z item 4 (the divergence, sizes + vintages)</ref>
  <ref type="law">CLAUDE.md Rule 13 (DS owns data/*/scripts bronze deploy cycle)</ref>
</references>

<dependencies>
  <dependency agent="1.0.0_SA_CTO" task="CI-R7R8 gate verdict (the fork)" status="pending (this TO activates on its resolution)"/>
</dependencies>
</task_order>
