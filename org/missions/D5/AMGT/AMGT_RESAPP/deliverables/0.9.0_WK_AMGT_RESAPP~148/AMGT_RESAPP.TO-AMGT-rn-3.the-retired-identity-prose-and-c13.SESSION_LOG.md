# SESSION LOG -- `0.9.0_WK_AMGT_RESAPP~148` on `AMGT-rn-3`

1. Bar check: `git rev-parse --abbrev-ref HEAD` -> `wk-AMGT_RESAPP-148`; `test -d org && test -d .tools` -> TREE-OK.
2. Read the task order's WORKER FACE and the check scripts at
   `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round39/checks/rn-3.AC{1,2,3}.sh`.
3. Read `org/tier1_exec/1.0.0_SA_CTO/deliverables/AMGT_COMPLETION_20260923/L4R_C13_RATIFIED.md` section 5
   for the verbatim C13 clause. Landed it in `portal/DESIGN.md` after C12, before "## Do and don't".
4. Read `portal/src/index.css` to confirm the live token mapping: `--bg-band` is overridden on `body`
   to `--layer-body` (`221 45% 18%` = rgb(25,38,67)); `--bg-header` is `--layer-strip`
   (`221 67% 12%` = #0A1733, the OLD literal). Confirmed the rgb conversion with a small python check
   (colorsys.hls_to_rgb).
5. Corrected the 13 named sites, and discovered AC1 grades FILE-granular (any hit of `0A1733`/`10,23,51`
   anywhere in the file, not just the named lines) -- index.css carried four further live hits
   (:153, :366, :421, :593) not named in the task order, and ui-smoke.mjs's cited line (:630) was
   actually :635. Corrected all of them; filed `AMGT_RESAPP-W148-S1` (OBSERVATION/INERT,
   DISMISSED_WITH_REASON -- fixed same-turn, no separate remedy needed).
6. Recomputed contrast ratios that had been measured against the retired #0A1733 literal, against the
   current --bg-band rung (rgb(25,38,67)), using the WCAG relative-luminance formula in a short python
   script; stated both the body-rung and header-rung values where the surrounding sentence named a ratio.
7. `PrintExportAction.tsx:136`'s scrim literal `bg-[rgba(10,23,51,0.6)]` -> `bg-[hsl(var(--bg-header))]/60`,
   matching the project's own existing arbitrary-opacity token form (`RollbackConfirmDialog.tsx`'s
   `text-[hsl(var(--bg-header))]/70`), not a `color-mix()` inline (that form is not used anywhere else in
   the portal).
8. Ran all three ACs: AC1 exit=0 (outside allow-list: 0), AC2 exit=0 (6 of 6), AC3 exit=0 (class census
   identical to baseline, 9 lines).
9. `git status --porcelain` in both the parent worktree and the nested portal confirmed exactly the 12
   files named in `<paths>` (11 src/scripts files + DESIGN.md) were touched -- no server started, no
   install, no push.
10. Committed the portal submodule (`02e04083`, `wk-AMGT_RESAPP-148-portal`), then the parent worktree's
    gitlink move (`2906e31cc4`, `wk-AMGT_RESAPP-148`).
11. Appended surprise row `AMGT_RESAPP-W148-S1` to the investigation file; validated the fenced JSON block
    parses (600 rows) and ran `.tools/surprise-row-gate.py` on the file (OK).
