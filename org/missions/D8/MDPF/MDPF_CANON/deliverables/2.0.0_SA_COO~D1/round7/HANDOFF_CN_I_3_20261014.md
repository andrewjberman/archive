# CN-i-3 hand-off (2.0.0_SA_COO~D1, 2026-10-14 ~20:4xZ, for the re-seat at the 21:00Z dell1 restart)

## State, measured

CN-i-3 (the Global AUA Trend at PROD's text, every other scope the feature's) is **NOT built**. The CTO's message 5862 reads it as "built and held"; that premise is wrong, and this note is the correction.

- Worker `0.9.0_WK_MDPF_CANON~25` fitted **5 of the 10 sites** and stopped with AC1 FAIL (its report; I checked the branch): portal `wk-MDPF_CANON-25-portal` @`19494a76` (one file, +72/-35 against `f8c7d310`), outer `wk-MDPF_CANON-25` @`43f7919403` (instance schema clean, proof-of-spec rc=1, order NOT flipped). Fitted: sites 1, 5, 6, 7, 9. Not fitted: 2, 3, 4, 8, 10 and the two area `const color` statements. **Global is therefore a mix at that head: do not render it as the candidate and do not register it.**
- Its rows `MDPF_CANON-D1-W25-S1` to `S9` are in `INVESTIGATION_v1.md` on its branch (not merged).

## What went wrong, and whose it is

1. **The recipe is mine and it was wrong for statement-level sites.** "`isGlobalTrend` then `? PROD` then `: feature`, each text on its own lines" only fits expressions. Sites 2 (a trailing-comma array element), 3 (a `return` statement), 4 (a `const` statement), 8 (assignment statements) and 10 (a JSX attribute) cannot take it. The worker was right to stop and not improvise.
2. **My check P1 is too strict.** It requires every line the feature removed to be present, including two that the keep-list tells the worker to leave removed: the `[scopeAumMetrics]` dependency line (the "as of" change replaced it, row W25-S7) and the `import { CategoryViewTree }` line (replaced by the import that adds `l1ColorOf`). AC1 cannot pass while the keep-list holds. **P2 is also too strict** for any site rewritten as a value constant (a trimmed-line match fails when a `const x =` wraps the same expression).
3. **The worker's branch lacks the re-cut order** (row W25-S8): `dafba4dbf3` is not an ancestor of `wk-MDPF_CANON-25`, so its checker read the old CN-i-2 order. Bring trunk into that branch before any further work there.

## What a re-seat needs (in order)

1. Do NOT build further until Andrew chooses ship-now or wait (CTO msg 5862). If he chooses to wait for the full-history Trend, CN-i-3 is moot except for its non-Trend edits, which already sit on the candidate. If he chooses ship-now:
2. Re-spec the recipe: for the five statement-level sites, define two named constants with the two texts and select by `isGlobalTrend`; relax P1 and P2 to compare normalised expression text (strip a trailing comma and a wrapping `const x =`), and exempt the two lines above with their reasons; make AC1 able to fail.
3. Merge trunk into `wk-MDPF_CANON-25`, continue worker `~25` (portal base `scratch/canon-i3-base`, which is current PROD `5ab67a65` plus the three feature commits with patch-ids equal to `fd5433a3`).
4. Real run: PROD's Global Trend baseline is already taken (local, gitignored: `tmp/ui-walk/20261014T202731Z`, PROD `5ab67a651a`, shots `002--portfolios-press-Trend.png`, `hover-after-press-1-viewport.png`, `hover-after-press-2-viewport.png`); render the head on 5174 and compare pixel for pixel with `pixdiff.py` (a PIL script in my session scratchpad: difference bbox and count; recreate it, it is 20 lines). Then a fresh client-facing row on a branch cut FROM PROD (the approval tool refuses a branch that overlaps DEV), held.

## Already true and not to repeat

- Andrew declined the Trend as built (row 19ae closed declined); approved the other popup edits, the lime repaint and the 49F view; the CTO ruled Inflection and Cottonwood keep the feature text (msg 5854). DEV `9e637fe51e` carries the declined Trend (landed before the CTO's hold; the CTO owns that).
- PRD v2.19 (@02852d9d16): Andrew picked Variant 1, the Global Trend with full history; the CRO's spec is `org/tier1_exec/4.0.0_SA_CRO/deliverables/MDPF_CANON_GLOBAL_AUA_TREND_FULL_HISTORY_SPEC_20261014.md` @8025c4d7f1. It is the next round's enrichment, withheld until the CVO re-signs the ratified-text half; a producer cell under a never-widen pair, then a portal cell.
- Port 5174 is free; I stopped every server I started; worktrees `wk-cand-render` and `wk-prod-render` and their node_modules junctions are removed. Slot `wk-canon-r7-25` (outer and portal) still exists.
