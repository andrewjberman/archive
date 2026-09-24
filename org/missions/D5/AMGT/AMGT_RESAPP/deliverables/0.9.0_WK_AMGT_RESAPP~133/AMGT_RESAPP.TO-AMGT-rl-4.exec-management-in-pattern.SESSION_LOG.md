# Session log -- AMGT_RESAPP.TO-AMGT-rl-4.exec-management-in-pattern -- 0.9.0_WK_AMGT_RESAPP~133

1. Bar check: `git rev-parse --abbrev-ref HEAD` -> `wk-AMGT_RESAPP-133`; `org` and `.tools`
   present; `portal/scripts/ui-class-census.mjs` present. TREE-OK.
2. Read `ExecManagementTab.tsx`, `execText.harness.cjs`, `execFallback.harness.cjs`,
   `tabs.harness.cjs`, `DESIGN.md`, `Panel.tsx`, `states/index.ts` + `PanelStates.tsx`,
   `Controls.tsx`, `types.ts` (Officer/ManagementBlock/CeoProfileReading), and the four
   `execFixture.*.json` + `tabsFixture.BA_US_Equity.json` fixtures.
3. Ran `tabs.harness.cjs` at the pre-edit bytes: confirmed `CHECK exec_officers_rendered
   false`, `CHECKS-WRONG-WAY exec_officers_rendered`, and isolated the cause -- the tabs
   fixtures' `ceo_profile_reading.reading` is the literal string
   `"NOT_CONFIRMED_INSTRUMENT_CANNOT_SAY"` on 4 of 5 QA names, a value outside the
   component's six known CEO-reading states; the `CeoProfile` fallback branch hard-coded
   `data-ceo-profile="UNREADABLE_OBJECT"` regardless, so the harness's
   `data-ceo-profile="${reading}"` check never matched.
4. Ran `ui-class-census.mjs` on the pre-edit file: `idiom=25 size=1 weight=0 radius=0
   shadow=0 total=26`, matching the brief's stated 26.
5. Rewrote `ExecManagementTab.tsx`: `Panel variant="nested"`, navy/darkGray ink throughout,
   the catalyst table (officer/role/role start/tenure/profile/confirmed), a tabular-nums
   right-aligned tenure cell, a profile cell that is a secondary button (`buttonClass`) when
   MATCHED and an icon-plus-text "ABSENT" cell otherwise, a confirmed cell with a status dot
   WITH its own label, the averages line as the panel's footer, `management.generated`
   rendered as a navy outline "Machine" chip, and every non-SERVED read routed through
   `PanelEmpty`/`PanelLoading`/`PanelError`. Fixed the CEO fallback to tag
   `data-ceo-profile={state}` (the object's own raw reading) instead of a fixed label.
6. `states/index` and `Controls` imported by RELATIVE path, not `@/...` alias: tabs.harness's
   STUBS map does not carry either alias and is out of this cell's <paths> to edit; a
   relative import resolves through the harness's own real-source loader instead.
7. Fixed a `PanelError` prop bug caught before running any harness (`detail` is not a prop of
   `PanelError`; it is `hint`).
8. Added `execPattern.harness.cjs` (new, AC1): 9 checks against CAT_US_Equity (FILING),
   ASML_NA_Equity (ABSENT/ZERO_OFFICERS) and tabsFixture.BA_US_Equity (12 officers, MATCHED +
   ABSENT-enrichment mix, `generated: true`). Debugged one regex defect (`<th[^>]*>` also
   matches the literal string `<thead>`; fixed with a negative lookahead) before all 9 read
   green.
9. Added loader stubs for the two new relative imports plus `@/lib/utils` to
   `execText.harness.cjs` and `execFallback.harness.cjs` (both in this cell's write grant).
   `execText`'s 5 checks needed no logic change. `execFallback`'s `resolved_unchanged` and
   `absent_unchanged` compared full-HTML byte-identity against the pre-inversion PIN, which no
   longer applies once the whole markup is redesigned on purpose (this cell's own charter) --
   rewrote both to check the SAME facts the pinned copy carried, plus a positive marker only
   the new code can produce, so they still discriminate old from new; the file's own comment
   already names this precedent (the Z-S193 class, rk-80's CEO-period carve-out).
10. Ran all three kept/new harnesses plus the census against the working tree: AC1 9/9, AC2
    idiom=0, AC3 tabs 20/20 (`exec_officers_rendered` now true, no other check newly
    WRONG-WAY), execText 5/5, execFallback 5/5. `tsc --noEmit` clean.
11. Committed the four files in the portal nested repo:
    `62ee58b3e43dbe2f201799a0dd5a4a27ee28328e`. Re-ran all four invocations at that commit --
    identical output.
12. Wrote this proof-of-spec instance; validating with
    `.tools/proof-of-spec-check.py`, then committing the instance + deliverables + the outer
    gitlink move together (status flip is the issuer's, per the task order).
