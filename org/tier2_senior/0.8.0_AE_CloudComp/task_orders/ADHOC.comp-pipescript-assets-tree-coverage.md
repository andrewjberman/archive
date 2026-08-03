<task_order>
<to_id>ADHOC.comp-pipescript-assets-tree-coverage</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<date>2026-08-03</date>
<status>staged</status>
<priority>P2 (instrument coverage hole on the monolith tree; CTO route-as-build 20260803T210604Z; third TO in your staged queue behind ADHOC.r4a + ADHOC.record-terraform-deploy)</priority>

<title>comp-pipescript: close the assets-tree coverage hole -- data/assets/scripts/silver/* returns rc=2 (tree absent from the pipeline map)</title>

<context>
Surfaced by OPAL_VENDORPROVENANCE WS-1 under its if_mismatch mandate (0.4.0_DS_ClientPlatform,
2026-08-03): `comp-pipescript io` on data/assets/scripts/silver/* returns rc=2 -- the assets
(monolith) tree is absent from the tool's pipeline map. CTO 210604Z: "The monolith tree being
invisible to the deploy-verify instrument is a real coverage hole; route as a build, not a
filing." CVO holds a parallel register note.

WHY IT MATTERS: OPAL_ASSETS is the monolith (s3://opal-data-assets, silver fact_* / gold dim_*
per the naming law) and is the estate's growth direction -- an entire tree invisible to
`comp-pipescript io/deployed/postdeps` means every DS Rule-13 flow on that tree runs without the
deploy-verify instrument, silently. The known member of the class: PIPELINE_MAP in
.tools/safe_deploy_core.py:158 carries bd/inf/cot; whether comp-pipescript reads THAT map or its
own is for your Phase 1 to source-confirm, not to inherit from this TO.

SECOND INDEPENDENT REPRODUCTION (0.2.0_DS, T1.C Phase 1, 211541Z -- widens the case set): all
three cottonwood MDPF producers live in data/assets/scripts/GOLD/ and the tool does not model
that tree either ("valid: bd/inf/cot/mdpf trees" per its own error) -- so the hole spans silver
AND gold under data/assets/. Your fix + regression set must cover both layers; T1.C hand-derived
I/O from source as the interim, which is exactly the manual fallback this build retires.

BLAST CAUTION: safe_deploy_core.py also gates .tools/safe-deploy.sh (the pre-push hook) --
a wrong map edit changes DEPLOY GATING, not just reporting. Regression controls are mandatory.
</context>

<scope>
1. Source-confirm the mechanism: which map/config comp-pipescript resolves trees from
   (file:line @ commit), and why data/assets/* misses it. Reproduce the WS-1 rc=2 as the
   pre-fix control (exact invocation + rc captured).
2. Implement coverage for the assets tree (io / deployed / postdeps all three modes), honoring
   the OPAL_ASSETS grammar (silver fact_* COMPLETE tables / gold dim_* projections).
3. Regression controls: existing trees' (bd/inf/cot + mdpf check-only) outputs byte-identical
   pre/post on a fixed invocation set; safe-deploy behavior unchanged for existing trees
   (exercise, not assert). If the fix touches safe_deploy_core.py, run its test set and state
   the denominator.
4. Post-fix: the WS-1 reproducing invocation returns rc=0 with correct READS/WRITES; one
   deployed-mode call against a real assets-tree script matches live S3 state.
5. NO behavior widening beyond the assets tree; no alarms/monitors (moratorium).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io &lt;the WS-1 failing invocation on data/assets/scripts/silver/*&gt;</run>
      <expect>rc=2 reproduced (pre-fix control), captured verbatim.</expect>
      <if_mismatch>STOP. If it now passes, the hole moved or closed -- re-ground with WS-1's author before building.</if_mismatch>
    </step>
    <step>
      <run>comp-blast safe_deploy_core (or the actual resolved map module)</run>
      <expect>Consumers enumerated -- expect safe-deploy pre-push hook + comp-pipescript at minimum; HOLD claims read if any.</expect>
      <if_mismatch>STOP. An unexpected consumer of the map = widen the regression set first.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>fixed-invocation regression set: comp-pipescript io/deployed on one script per existing tree, pre/post diff</run>
      <expect>Byte-identical outputs on every existing tree; assets tree rc=0 with correct grammar.</expect>
      <if_mismatch>STOP. Any existing-tree diff is a gating change -- surface to COO+CTO before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>the WS-1 invocation post-fix + one deployed-mode call vs live S3; report to COO + CTO + CVO (register closure)</run>
      <expect>rc=0, output correct, live-state match; report cites pre/post captures + commit.</expect>
      <if_mismatch>REWORK -- an instrument fix without its exercised before/after is a filing, not a build.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
safe_deploy_core.py is shared gating infra (DS deploy flows on every tree) -- regression set per
Phase 2 is the gate; coordinate with 0.4.0_DS_ClientPlatform if their live WS-1/T2-tranche work
touches assets-tree scripts mid-fix (read-only on their side, but their invocations are your
test oracle). CVO holds the parallel register note -- your Phase 3 report closes it.
</cross_domain_coordination>

<acceptance_criteria>
1. Mechanism cited file:line @ commit; pre-fix rc=2 and post-fix rc=0 captures on the identical
   invocation, both verbatim in the session log.
2. Regression set: byte-identical existing-tree outputs, denominator stated; safe-deploy
   behavior exercised unchanged.
3. Deployed-mode call against a real assets script matches live S3.
Plus: session log includes a Compiler Tools section reproducing every <run> with observed output
and explicit pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<references>
  <ref type="route">CTO 20260803T210604Z (route-as-build); WS-1 if_mismatch surfacing (0.4.0_DS, tranche 1)</ref>
  <ref type="grammar">MEMORY: OPAL_ASSETS monolith grammar (silver fact_* / gold dim_*)</ref>
  <ref type="siblings">ADHOC.r4a-closeout-trigger-false-attribution-fix + ADHOC.record-terraform-deploy-cotenant-sweep-fix (same staged queue, same seat)</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
