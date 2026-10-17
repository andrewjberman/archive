# bu-2 session log -- 0.9.0_WK_AMGT_RESAPP~505 (verbatim run outputs)

## 1. Harness at the unedited head (d1bed0fb, before any product edit; base file recorded in a prior recording pass)
```
CHECK E1_visible_cells_read_long_form FAIL (before "2026-11-06" (want "November 6th, 2026"), after "2026-11-11" (want "November 11th, 2026"))
CHECK E2_detail_reads_long_form_both_versions FAIL (detail "Full figures Earlier version: 2026-11-06 Later version: 2026-11-11 Date of the issuer's next expected earnings report (a DATE, not a number).")
CHECK E3_no_iso_day_in_whole_visible_render FAIL (ISO "2026-11-06" in "suer's next expected earnings report (a DATE, not a number) 2026-11-06 2026-11-11 -- -- Fu")
CHECK E4_control_rio_render_byte_identical_visible PASS (rows 47 (base 47); visible sha256 a4db551488920171477b4315ece4de0ad4890287714d3758a69eddaa9d85976a)
CHECK E5_census_denominator_and_dispositions PASS (102 sites, denominator 102, files read 37, bypass 30, undispositioned 0)
CHECK E6_not_a_day_prints_as_it_came PASS (before "n/a" after "n/a" change "--" pct "--")
CHECK E7_sibling_harnesses_still_pass PASS (exit 0; CHANGED LIST VALUE HARNESS: YES (16 of 16 checks); exit 0; CHANGED OBJECT CELLS HARNESS: YES (6 of 6 checks); exit 0; EARNINGS LONG DATES HARNESS: YES (7 of 7 checks))
DATE RULE HARNESS: NO (4 of 7 checks)
```

## 2. Harness after the What Changed edit (WhatChangedPanel only)
```
CHECK E1_visible_cells_read_long_form PASS (before "November 6th, 2026" (want "November 6th, 2026"), after "November 11th, 2026" (want "November 11th, 2026"))
CHECK E2_detail_reads_long_form_both_versions PASS (detail "Full figures Earlier version: November 6th, 2026 Later version: November 11th, 2026 Date of the issuer's next expected earnings report (a DATE, not a number).")
CHECK E3_no_iso_day_in_whole_visible_render PASS (visible text 10554 chars, no ISO day)
CHECK E4_control_rio_render_byte_identical_visible PASS (rows 47 (base 47); visible sha256 a4db551488920171477b4315ece4de0ad4890287714d3758a69eddaa9d85976a)
CHECK E5_census_denominator_and_dispositions PASS (102 sites, denominator 102, files read 37, bypass 30, undispositioned 0)
CHECK E6_not_a_day_prints_as_it_came PASS (before "n/a" after "n/a" change "--" pct "--")
CHECK E7_sibling_harnesses_still_pass PASS (exit 0; CHANGED LIST VALUE HARNESS: YES (16 of 16 checks); exit 0; CHANGED OBJECT CELLS HARNESS: YES (6 of 6 checks); exit 0; EARNINGS LONG DATES HARNESS: YES (7 of 7 checks))
DATE RULE HARNESS: YES (7 of 7 checks)
```

## 3. AC1 harness after the reason-site edits, and two same-input runs (identical)
```
CHECK E1_visible_cells_read_long_form PASS (before "November 6th, 2026" (want "November 6th, 2026"), after "November 11th, 2026" (want "November 11th, 2026"))
CHECK E2_detail_reads_long_form_both_versions PASS (detail "Full figures Earlier version: November 6th, 2026 Later version: November 11th, 2026 Date of the issuer's next expected earnings report (a DATE, not a number).")
CHECK E3_no_iso_day_in_whole_visible_render PASS (visible text 10554 chars, no ISO day)
CHECK E4_control_rio_render_byte_identical_visible PASS (rows 47 (base 47); visible sha256 a4db551488920171477b4315ece4de0ad4890287714d3758a69eddaa9d85976a)
CHECK E5_census_denominator_and_dispositions PASS (102 sites, denominator 102, files read 37, bypass 30, undispositioned 0)
CHECK E6_not_a_day_prints_as_it_came PASS (before "n/a" after "n/a" change "--" pct "--")
CHECK E7_sibling_harnesses_still_pass PASS (exit 0; CHANGED LIST VALUE HARNESS: YES (16 of 16 checks); exit 0; CHANGED OBJECT CELLS HARNESS: YES (6 of 6 checks); exit 0; EARNINGS LONG DATES HARNESS: YES (7 of 7 checks))
DATE RULE HARNESS: YES (7 of 7 checks)
--- run 2 identical
```

## 4. AC2 (r107_feature_green_v3.sh, tail and rc)
```
repo-wide lint rc 0 (information only: PROD itself reads non-zero in a file this feature does not touch) | typecheck rc 0 | lint rc 0 (src/pages/SecurityAnalysis) | harness 33 of 36 pass | base 29 of 35 | regressions 0: none | pre-existing: assembled.harness.cjs exportCompare.harness.cjs timelineFourStates.harness.cjs
R103 FEATURE GREEN: YES (typecheck rc 0, lint rc 0, harness 33 of 36 pass, base 29 of 35, regressions 0, pre-existing: assembled.harness.cjs exportCompare.harness.cjs timelineFourStates.harness.cjs)
exit=0
```

## 5. AC3 (r103_feature_surface_check.py)
```
  page      src/pages/SecurityAnalysis/__harness__/dateRule.harness.cjs
  page      src/pages/SecurityAnalysis/__harness__/dateRuleFixture.ICT_PM_compare_scalar_date.json
  page      src/pages/SecurityAnalysis/__harness__/dateRuleFixture.base_rio_visible.json
  page      src/pages/SecurityAnalysis/__harness__/dateSites.fixture.json
  page      src/pages/SecurityAnalysis/components/AiFillBlock.tsx
  page      src/pages/SecurityAnalysis/components/ChatterBubbles.tsx
  page      src/pages/SecurityAnalysis/components/CheckFaceBadge.tsx
  page      src/pages/SecurityAnalysis/components/DossierSections.tsx
  page      src/pages/SecurityAnalysis/components/HeaderBrief.tsx
  page      src/pages/SecurityAnalysis/components/HeaderCards.tsx
  page      src/pages/SecurityAnalysis/components/InputProvenance.tsx
  page      src/pages/SecurityAnalysis/components/PriceBars.tsx
  page      src/pages/SecurityAnalysis/components/RankedChart.tsx
  page      src/pages/SecurityAnalysis/components/RankedList.tsx
  page      src/pages/SecurityAnalysis/components/SegmentBreakdown.tsx
  page      src/pages/SecurityAnalysis/components/SegmentTable.tsx
  page      src/pages/SecurityAnalysis/components/TimelinePanel.tsx
  page      src/pages/SecurityAnalysis/components/TimelineWordCloud.tsx
  page      src/pages/SecurityAnalysis/components/model/WhatChangedPanel.tsx
  page      src/pages/SecurityAnalysis/tabs/ExecManagementTab.tsx
  page      src/pages/SecurityAnalysis/tabs/PostureTab.tsx
R103 FEATURE SURFACE: YES (21 files: 21 page, 0 shared named, 0 forbidden, 0 unnamed)
```

## 6. Approval row check-only (not registered)
```
APPROVAL-REGISTER result=OK row=- head_sha=9a8ef5e451e118735e819682c32de816c84a16a8 commits=1 check-only=yes waived=0
rc=0
```
