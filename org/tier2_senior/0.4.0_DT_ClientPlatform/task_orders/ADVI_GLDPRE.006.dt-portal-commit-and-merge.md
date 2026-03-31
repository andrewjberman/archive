<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-20-gldpre-006-dt</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-20</date>
    <status>complete</status>
    <project_code>ADVI_GLDPRE</project_code>
  </metadata>

  <objective>
    Commit the CTO's ClientsTab.tsx fix to portal DEV. After the full gold rerun
    completes (AE GLDPRE.005), merge portal DEV to PROD and deploy. This single
    merge clears the shared gate for GLDPRE + MIXV2 + MVP318 + MVPLVL.
  </objective>

  <context>
    Reference:
    - docs/architecture/ADVI_GLDPRE_PRD.md — WS5
    - Portal submodule: src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx

    Current portal DEV HEAD: a4f71d7 ([GLDPRE] WS4+WS5 4-class taxonomy)

    The CTO's session found a bug in ClientsTab.tsx deriveQuarterlyFromTimeseries:
    lines referencing structured_notes and other fields that no longer exist on the
    4-class FirmMixPeriodPoint type. These produce NaN values at runtime.

    The fix is already applied in the portal working tree (unstaged). It removes
    2 lines from deriveQuarterlyFromTimeseries:
      - structured_notes: { value: total * mix.structured_notes, pct: mix.structured_notes },
      - other:            { value: total * mix.other,            pct: mix.other },

    This is a 2-line deletion.
  </context>

  <scope>
    <files>
      <file action="commit">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Verify the ClientsTab.tsx fix is in the working tree:
        cd portal
        git diff src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx

      Expected: removal of structured_notes and other lines from
      deriveQuarterlyFromTimeseries (around line 767-769). The function
      should have exactly 4 class lines: equity, fixed_income, alternatives, cash.

      If the diff is empty (fix was lost), apply it:
      In deriveQuarterlyFromTimeseries, remove these two lines:
        structured_notes: { value: total * mix.structured_notes, pct: mix.structured_notes },
        other:            { value: total * mix.other,            pct: mix.other },
    </requirement>

    <requirement id="2">
      Commit to portal DEV:
        cd portal
        git add src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "fix(portal): remove structured_notes/other from deriveQuarterlyFromTimeseries (GLDPRE 4-class)"
    </requirement>

    <requirement id="3">
      GATE: Wait for AE to confirm GLDPRE.005 Phase 4 (full gold rerun) is complete
      and all verification checks pass. Do NOT merge to PROD before this.
    </requirement>

    <requirement id="4">
      After gold rerun is verified, merge portal DEV to PROD:
        cd portal
        git checkout PROD
        git merge DEV --no-ff -m "merge DEV->PROD: GLDPRE 4-class + MVP318 WS6 + MVPLVL + MIXV2 portal gate"
        git checkout DEV

      Then deploy to server via deploy-manual.sh.
    </requirement>

    <requirement id="5">
      Update the parent repo portal submodule pointer:
        cd ..  (back to ajb_workspace root)
        git add portal
        git commit --author="0.4.0_DT_ClientPlatform &lt;0.4.0_DT_ClientPlatform@opal.agent&gt;" \
          -m "ci: update portal submodule to PROD merge (GLDPRE + MVP318 + MVPLVL + MIXV2)"
        git push --follow-tags
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">ClientsTab.tsx deriveQuarterlyFromTimeseries has exactly 4 class lines (equity, fixed_income, alternatives, cash)</criterion>
    <criterion id="2">Portal DEV commit pushed</criterion>
    <criterion id="3">Gold rerun verified before PROD merge (AE confirmation)</criterion>
    <criterion id="4">Portal PROD merge-forward from DEV completed</criterion>
    <criterion id="5">Portal deployed to server via deploy-manual.sh</criterion>
    <criterion id="6">Parent repo submodule pointer updated and pushed</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>PROD is merge-only — never commit directly to PROD</constraint>
    <constraint>Do NOT merge to PROD before AE confirms gold rerun success</constraint>
    <constraint>Do NOT push portal PROD without reviewing all pending DEV commits since last PROD merge</constraint>
    <constraint>The types.ts +1389/-11 diff is correct — CLSUNI runtime destroyed the file, this restores it</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="GLDPRE.005 Phase 4" status="pending">
      Full gold rerun must complete and pass verification before PROD merge.
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="GLDPRE.002 WS2" status="complete">
      DS committed WS2 to 06b at 61f76c8b on CLOUD. Gate cleared.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">ClientsTab.tsx fix on portal DEV</deliverable>
    <deliverable type="deploy">Portal DEV -> PROD merge + server deploy</deliverable>
    <deliverable type="commit">Parent repo submodule pointer update</deliverable>
  </deliverables>
</task_order>
