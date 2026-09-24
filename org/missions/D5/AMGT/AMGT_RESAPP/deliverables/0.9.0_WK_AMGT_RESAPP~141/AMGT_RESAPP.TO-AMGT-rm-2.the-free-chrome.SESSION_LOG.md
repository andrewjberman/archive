AMGT_RESAPP.TO-AMGT-rm-2 -- the free chrome -- session log, 0.9.0_WK_AMGT_RESAPP~141

1. First act (task order bar): `git rev-parse --abbrev-ref HEAD` -> wk-AMGT_RESAPP-141;
   `git rev-parse --show-toplevel` -> C:/tmp/wk-amgt-38-141; `test -d org && test -d .tools` ->
   TREE-OK; `grep -c 'scope' portal/scripts/ui-contract-check.mjs` -> 20 (non-zero, not
   BLOCKING); starting census `node scripts/ui-class-census.mjs
   src/components/PageHeaderVariants.tsx src/ui/components/panels/PanelHeader.tsx
   src/ui/components/panels/PanelFooter.tsx` -> FILES 3 TOTAL 11, matching the cell text's stated
   starting point exactly.

2. Read the three files. Confirmed PageHeaderVariants.tsx:46 `font-light`, PanelHeader.tsx:62
   `rounded-t-lg` + :75 `font-semibold`, PanelFooter.tsx:93 `rounded-b-lg`, and (issuer note 2)
   PanelFooter.tsx:106 `leftContent && 'text-right flex-shrink-0'` with its sibling wrapper (:104)
   carrying no min-w-0.

3. Confirmed by direct regex replay (node one-liner against `git show HEAD:<path>`) that
   ui-class-census.mjs's RADIUS_NAMED pattern (`/rounded-(md|lg|xl|2xl|3xl)\b/g`) reads 0 hits on
   both `rounded-t-lg` and `rounded-b-lg` -- the pattern requires the ladder token immediately
   after "rounded-", and the -t-/-b- side token defeats it. This is the census blind spot AC1
   names.

4. Edits (all three WHAT-YOU-BUILD files):
   - PageHeaderVariants.tsx:46 `font-light` -> `font-normal` (300 -> 400).
   - PanelHeader.tsx:62 `rounded-t-lg` -> `rounded-t-[4px]`; :75 `font-semibold` -> `font-bold`
     (600 -> 700), uppercase tracking unchanged.
   - PanelFooter.tsx:93 `rounded-b-lg` -> `rounded-b-[4px]`.
   - PanelFooter.tsx row AMGT_RESAPP-W144-S1 (rm-5, routed here): :104 leftContent wrapper gains
     `min-w-0`; :106 content wrapper's `flex-shrink-0` replaced with `min-w-0` (both flex children
     can now shrink and wrap instead of one refusing to shrink and forcing an overflow the panel's
     rounded corners then clip). Presentation only, no prop/behaviour change.

5. Re-ran the census: weight/radius/shadow -> 0 on all three files; idiom stays at 4+4 (8 total),
   all `text-white`/`text-white/NN` on the strip's `bg-[hsl(var(--bg-header))]` background --
   documented per-line in AC1-idiom-exclusions.md under the issuer-specified clause "C5 inversion
   on a dark strip." PanelHeader's pre-existing size=1 (DataTimestamp `text-[10px]`, :99) is a C2
   concern outside this cell's C1/C11 mandate; unchanged before/after.

6. Determined the C11 shadow limb: wrote a small Playwright one-liner (run from inside portal/ so
   playwright-core resolves; copied to portal/scripts/_tmp_shadow_check.mjs for the run, deleted
   immediately after -- never committed) that opens /security-analysis against the live dev
   server (port 5183) and reads `getComputedStyle(el).boxShadow` on the first element whose
   className contains `rounded-t-[4px]` (the PanelHeader strip) and `rounded-b-[4px]` (the
   PanelFooter strip), plus the `<aside>` sidebar for contrast. Both strips read boxShadow "none";
   the sidebar reads the real shadow-lg box-shadow values, matching its own class list
   (`...bg-[hsl(var(--bg-header))] border-r shadow-lg...`, App.tsx:271, untouched -- not this
   cell's file). Output saved to shadow-check-output.json.

7. AC2: ran the literal invocation against the port-5183 dev server. scope=main: weights column
   PASS on all six states (was FAIL [300,600] at the round baseline per issuer note 1; now the
   sidebar's 500/600 never appear in main, and this cell's own 300/600 sources are fixed), radii
   PASS on all six (was FAIL ["8px"]), shadows PASS on all six (unchanged, already PASS at
   baseline -- confirms C11's shadow limb was never main-scope's problem). scope=body table
   (informational) still shows FAIL [500,600] / FAIL 1 (shadow) / FAIL ["8px"] on every state --
   the sidebar's, untouched, reported not fixed. sizes FAILs [10] on thesis/model persist in BOTH
   scopes -- the DataTimestamp size, out of this cell. Six PNGs, all > 20 KB (74132..363363
   bytes). RESULT line reads FAIL because of the sizes column (not this cell's target); the
   criterion's own <expect> is scoped to weight/radii/shadow + the six-PNG/idiom-exclusion
   requirements, all of which hold.

8. AC3 needed `--route`/`--out` on ui-smoke.mjs (named in the cell text) AND on ui-measure.mjs
   (not named, but AC3's own invocation passes --route to it too) -- filed AMGT_RESAPP-W141-S1,
   disarmed same-turn (fix applied, both files are in <paths>, additive over the old positional
   form). Ran ui-smoke.mjs --route /market --out .../market-after.png (127198 bytes) against port
   5183, then ui-measure.mjs --route /market --scope main (stripContainers 12), then `npx tsc -b
   --noEmit` (tsc=0).

   To get the BEFORE stripContainers count without touching the live worktree (git stash is
   blocked on this shared-worktree-blast hazard, correctly, even scoped to specific paths): added
   a throwaway git worktree of the nested portal repo's own HEAD (c7b022a1, pre-edit, since no
   commit had landed yet) at C:/tmp/portal-rm2-baseline, symlinked node_modules to the shared
   install (same mechanism the real worktrees use), ran a second vite dev server on port 5184,
   and measured /market there: stripContainers=12, weights {300:8,400:599,500:40,600:161,700:365},
   radii {4px:17, 8px:10, 3px:1, pill:1}. AFTER (port 5183, my edits): stripContainers=12
   (unchanged -- classify()'s stripContainers test is background-colour-only, independent of
   radius/weight by construction, so this is the expected and necessary result, not a
   coincidence), weights {400:607, 500:40, 600:79, 700:447} (300's 8 folded into 400; 600 dropped
   by 82 and 700 rose by 82, matching PanelHeader title semibold->bold across /market's six
   strip-carrying panels), radii {4px:23 (was 17, +6), 8px:4 (was 10, -6), 3px:1, pill:1} (six
   panel strips' worth of 8px->4px, the residual 8px:4 belonging to elements outside my three
   files -- another cell's). Tore the baseline worktree down afterward (`git worktree remove
   --force`; node_modules needed a robocopy-mirror-to-empty-dir pass first -- `ln -s` on this
   device did not create a reparse point for the target directory, `fsutil reparsepoint query`
   confirmed "not a reparse point", so it had fully copied ~287 MB and a plain `rd`/`rmtree` hit
   Windows long-path limits; robocopy `/MIR` against an empty source directory handles arbitrary
   path depth and finished in ~2 minutes). This is bookkeeping for AC3's evidence, not a change to
   any tracked file.

9. Controls: mutant -- reverted PanelHeader.tsx:75 to font-semibold, re-ran the file's own census
   (weight 0 -> 1, FIRED-AS-EXPECTED), restored the fix and confirmed the restore was byte-
   identical (`diff` clean) and the census read weight 0 again. Determinism -- ran the three-file
   census twice in a row post-fix; byte-identical output both times.

10. Filed AMGT_RESAPP-W141-S1 in the project's surprise channel (INVESTIGATION_v1.md, JSON array,
    per org/surprise_channel/schemas/investigation_item.schema.json); validated with
    `.tools/surprise-row-gate.py` (rc=0).

11. Portal commit 4aa49151af5ec8602b9562835b9fece4bd56a35f (5 files: ui-measure.mjs, ui-smoke.mjs,
    PageHeaderVariants.tsx, PanelFooter.tsx, PanelHeader.tsx). Outer commit carries the portal
    gitlink move, this deliverables folder, and the surprise-channel row.

12. Stopped the dev server (PID 47868, port 5183) before finishing.
