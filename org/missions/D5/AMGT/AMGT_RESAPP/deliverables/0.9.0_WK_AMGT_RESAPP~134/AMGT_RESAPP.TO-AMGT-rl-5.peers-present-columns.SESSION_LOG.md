# Session log -- AMGT_RESAPP.TO-AMGT-rl-5.peers-present-columns -- 0.9.0_WK_AMGT_RESAPP~134

Worktree: C:/tmp/wk-amgt-37-134 (branch wk-AMGT_RESAPP-134); portal nested repo at
C:/tmp/wk-amgt-37-134/portal (branch wk-AMGT_RESAPP-134-portal, portal_ref bc07b6a1).

1. Bar check: `git rev-parse --abbrev-ref HEAD` -> wk-AMGT_RESAPP-134; `test -d org && test -d
   .tools` -> TREE-OK; `test -f portal/scripts/ui-class-census.mjs` -> INSTRUMENT-OK;
   `git -C portal log -1 --format=%h` -> c657eb91; `merge-base --is-ancestor c657eb91 HEAD` ->
   PEERS-BASE-OK. No BLOCKING row.

2. Read the cell's current files: PeersTab.tsx (dark idiom, table over ALL 17 columns),
   cscTable.ts (unchanged shape needed), peersCarry.harness.cjs and peersReadFailed.harness.cjs
   (both must keep passing), portal/DESIGN.md C3/C5/C11/C12, Panel.tsx (nested variant ->
   bg-[hsl(var(--bg-surface))]), PanelHeader.tsx (ALWAYS dark band regardless of variant, not in
   this cell's <paths> -- decided NOT to use it, built the header/subtitle/chip locally inside
   PanelContent instead, consistent with the pattern in
   src/pages/InvestorReporting/header/ScopeSummary.tsx), HelperTip.tsx/Tooltip.tsx (hover-gated,
   client-only, renders no content into react-dom/server output when closed -- this is why the
   new harness stubs HelperTip rather than loading the real Tooltip, which uses real hooks and
   would crash if invoked outside an actual React render pass), states/PanelStates.tsx (the four
   C12 states, hook-free, safe to load for real -- used inert box stubs anyway since none of the
   13 AC1 checks probe them).

3. Rewrote PeersTab.tsx: one Panel variant="nested"; PanelEmpty/PanelLoading/PanelError wired for
   the four designed states (NO-PERMISSION left unwired, matching the rest of the product); a
   BasisChip (navy outline, rounded-[2px], label-size bold text) wrapped in a HelperTip carrying
   peers.test; subtitle line (comparable count / universe vintage / as-of) as plain flex spans (no
   literal separator glyph -- Rule 4, no non-ASCII in production code); table filtered to
   PRESENT_CARRIED + PRESENT_NOT_CARRIED columns only; a PRESENT_NOT_CARRIED column head wraps its
   label in its own HelperTip carrying cscTable's reason; summary rows carry the C3 sunken fill
   class; subject row bold; an <details> disclosure (collapsed by default -- no `open` attribute)
   listing every ABSENT/UNMAPPED column with its reason at footnote size; the counts paragraph and
   the absent-basis three-state paragraph kept verbatim in substance, restyled to navy-on-white.
   "--" (two ASCII hyphens, the existing codebase convention) stands in for the em-dash the TO
   names, never a literal U+2014 (Rule 4).

4. AC2 (census) passed immediately: FILES 2 TOTAL 0.

5. Extended peersCarry.harness.cjs and peersReadFailed.harness.cjs loaders with two new cases
   (@/ui/components/states -> inert boxes; @/components/HelperTip -> passthrough-plus-marker
   stub) so they keep resolving PeersTab.tsx's larger import set. Re-ran both: both still PASS,
   assertions untouched (AC3 verified).

6. Wrote the new peersPattern.harness.cjs: loads the REAL Panel/PanelContent (so panel_is_light
   reads the real variant class, not a stub's) plus the stub HelperTip; a fixture with 4
   present-carried + 1 present-not-carried (`div_yield`, no MEMBER_FIELD_FOR_CODE entry) + 12
   absent = 17 declared, 12 members, one subject. 13 named checks. First run: 14 lines printed
   (split absent_disclosure_count into two checks) and not_carried_em_dash FAILED -- debugged via
   a temporary debug copy of the harness that dumped the rendered HTML to a file
   (portal_peers_debug.html, deleted after use) and found (a) cscTable.ts's PRESENT_NOT_CARRIED
   reason is a FIXED template string that ignores `relation`, so the fixture's expected reason
   text was wrong, and (b) the AC1 spec names exactly 13 checks with `absent_disclosure_count 12`
   and `absent_reasons_listed 12` as NUMBERS, not booleans -- consolidated to 13 checks matching
   the task order's list verbatim. Second run: CHECKS-OK 13 of 13.

7. Controls: mutant (removed the '--' branch for PRESENT_NOT_CARRIED, confirmed ONLY
   not_carried_em_dash flips, all 12 other checks and AC2/AC3 unaffected, reverted, diff 0 bytes,
   re-ran AC1 to confirm the revert -- CHECKS-OK 13 of 13 again); determinism (AC1 run twice,
   diff of the two captured outputs: 0 bytes).

8. Committed the portal change: `cd portal && bash ../.tools/safe-commit.sh --author
   "0.9.0_WK_AMGT_RESAPP~134 <...>" -F <msgfile> -- tabs/PeersTab.tsx
   __harness__/peersCarry.harness.cjs __harness__/peersReadFailed.harness.cjs
   __harness__/peersPattern.harness.cjs` -> 9c8459ca8a08e230ee220375cfd4b2e0e7817361 on
   wk-AMGT_RESAPP-134-portal, parent bc07b6a1 (descendant of c657eb91, PEERS-BASE-OK preserved).

9. Re-ran AC1/AC2/AC3 verbatim against the committed bytes -- all three PASS. Non-ASCII byte-delta
   check on all four touched files: 0 (pure ASCII).

10. No BLOCKING row, no surprise row filed: everything the TO named was reachable and every
    invocation produced the named result on the first (post-debug) real attempt.
