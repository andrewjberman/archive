# DSGN_RBNDV2 -- round 8 close run: the panel tone, the silver nesting steps, the darker positive and negative pair (direct acts RV-b-1, RV-g-1, RV-n-1, RV-g-2)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~21:2xZ. **Source:** Andrew's four messages, verbatim in `ANDREW_DIRECT_20261015_PANEL_TONE.md`. **Branch read:** `feature/dsgn-rbndv2-light` @e88ffb03 (LOCAL, never pushed), dev build at `localhost:5174` (served detached from the integration checkout, HTTP 200). Direct acts are round-less: they run no L8 to L10; this record is the COO's one real run, and Andrew's own smoke test is the grade (DEC-5).

## Drain (merge-time checks, in the portal-only checkout, real typecheck)

| order | worker | proof (re-run in its worktree before the merge) | portal merge | workspace merge | rulings needed |
|---|---|---|---|---|---|
| RV-b-1 panel tone `#F8F8FD` | ~23 | VALID | d67e4815 | cb47ea9e45 | two: a pinned rule-count arm and a pinned bare-triple arm of `rb-1-r` / `rb-1-r2`, and the `checkOldRule` count arm |
| RV-g-1 `--success` / `--danger` darker | ~24 | VALID | ca146d09 | 67832503ad | one: selector `[data-panel-surface="light"]:not(.dark-band *)` (a pinned scope-prefix arm of `rb-1-t`) |
| RV-n-1 silver steps for nested containers | ~25 | VALID | ded7ae13 | 839ba4571d | two: 16 explicit selectors instead of `:is()` (the same `rb-1-t` arm splits on commas); 30000 ms timeouts on the git-show tests |
| RV-g-2 return-delta tokens darker | ~26 | VALID | e88ffb03 | 4e75c0ad1e | none |

At the last portal merge: `tsc -p tsconfig.app.json --noEmit` rc=0; design, panels, modal and market-performance tests 48 pass 0 fail (35 files); eslint rc=0 on the design tests. Every diff reviewed: 0 non-ASCII bytes added. Worktrees and branches removed; nothing pushed.

## Live reads (the walker, computed styles on `/market`)

| Andrew's point | read | result |
|---|---|---|
| EAEAF7 for the sidebar and background | body, sidebar rail, page wrapper | `rgb(234, 234, 247)` on six pages (the question was answered by measurement; the white was the panels) |
| softer panel (his "Try your recommendation") | panel roots | `rgb(248, 248, 253)` (#F8F8FD), 42 and 34 percent of the viewport on Market Overview |
| silver for the item containers (his fourth message) | Trending Topics rows | `rgb(238, 241, 246)` (#EEF1F6), border colour transparent; 56 silver surfaces vs 330 panel-tone surfaces on `/market`; the second layer (#E6EBF4) is in the stylesheet as 16 explicit selectors and was not read on `/market` (no element on that page nests one item container inside another) |
| red and green darker for positive and negative | signed figures | 148 positive `rgb(20, 113, 59)` (#14713B, 5.74 to 1 on the panel tone; was `rgb(45, 205, 136)` at 1.94 to 1) and 128 negative `rgb(187, 27, 48)` (#BB1B30, 5.99 to 1; was `rgb(251, 112, 132)` at 2.56 to 1) |

## What went wrong on the way (and was owned)

- I first named the wrong shared pair (`--success` and `--danger`). `RV-g-1` merged and a live read showed the signed figures UNCHANGED; the figures read `--delta-positive` / `--delta-negative` through `performanceUtils.ts`. Corrected by `RV-g-2`. `RV-g-1` still darkens the titles and status chips that read `--success` and `--danger`.
- Four pinned design tests (`rb-1-r`, `rb-1-r2`, `rb-1-t`) pinned the exact form of the CSS blocks these cells change. Each worker stopped on a BLOCKING row and was re-seated on an issuer ruling (amendments committed on main and on the worker's branch); no test was weakened beyond the rulings.

## Carried, not cut

- 540 figures on `/market` read the ink `rgb(22, 51, 114)` (heat-table cells and other text that the legibility rule turned navy); they are not red or green. Whether heat-table figures should show gain and loss colours is the heat-map design call still owed (FWD-4, his answer at this terminal).
- The local push candidate `cand/laptop/dsgn-rbndv2-light` (@c8181090ca) is now stale against the feature branch; it is re-cut from the last PROD (a short local rehearsal) before any push word.
- Calls: `002b` (tooltip placement), the heat-map answer; his next page's comments.
