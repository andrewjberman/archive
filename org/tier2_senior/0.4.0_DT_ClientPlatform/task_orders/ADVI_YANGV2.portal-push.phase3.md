# Task Order: ADVI_YANGV2 — Push Portal DEV to Remote (Phase 3) — 0.4.0_DT_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-ADVI_YANGV2-portal-push-phase3</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH — 5 commits of Phase 3 FE work unreachable until pushed</priority>
  </metadata>

  <objective>
    Portal DEV branch is 5 commits ahead of remote (542197c to 9b902dc). All Phase 3 Yang V2
    FE work (Books tab L2/L3/L4, GRO mode, NNA geo/adv drills, rolling flows NNA bar) has been
    DE-reviewed and is sitting on local DEV. Push to remote and update the parent repo submodule pointer.
    No code changes — push only.
  </objective>

  <references>
    <ref type="de-briefing">commit 518159a7 -- Pod 4 State 2026-03-05</ref>
    <ref type="portal-branch">portal/ submodule DEV branch</ref>
  </references>

  <requirements>
    <requirement id="1">
      Push portal DEV branch to remote:
        cd portal
        git checkout DEV
        git push origin DEV

      Confirm: remote/DEV is now at 9b902dc (Books tab L2/L3/L4 -- last commit).
    </requirement>
    <requirement id="2">
      Update parent repo submodule pointer to track the pushed commit:
        cd ..
        git add portal
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DT_ClientPlatform: update portal submodule -- ADVI_YANGV2 Phase 3 push (9b902dc)"
        git push origin CLOUD
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">portal/origin/DEV is at 9b902dc after push.</criterion>
    <criterion id="2">Parent repo CLOUD has an updated portal submodule pointer committed under DT authorship.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Push DEV only -- do NOT merge to PROD or run deploy-manual.sh. This is not a server deploy.</constraint>
    <constraint>No code changes of any kind. Push only.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">portal submodule pointer updated in parent CLOUD branch</deliverable>
  </deliverables>
</task_order>
```
