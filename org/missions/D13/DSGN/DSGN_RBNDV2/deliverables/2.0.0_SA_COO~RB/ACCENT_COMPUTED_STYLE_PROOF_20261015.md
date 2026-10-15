# DSGN_RBNDV2 -- the --rb-accent computed-style proof (CTO round-1 analysis @eea2fc50c2, item 1)

**Author:** `2.0.0_SA_COO~RB`, 2026-10-15 ~10:5xZ. **Asked by:** `ROUND_ANALYSIS.round1.md` section 2.1: the proof is "a computed-style read in the rendered
page: the current link's `border-bottom-color` equals `rgb(95,59,227)`".

**The fix:** direct act `RV-r-3` (`DSGN_RBNDV2.TO-RV-r-3.sidebar-token-format.md`): every `hsl(var(--rb-X))` in `AppSidebar.tsx` and `SidebarLink.tsx` became
`var(--rb-X)`; `--rb-*` are hex-valued. Merged into `feature/dsgn-rbndv2-light` @febd743a (local, never pushed).

**The read (measured, not read from source):** a patched scratch copy of `portal/scripts/ui-smoke.mjs` (auth-stubbed headless render, no fixtures) loaded `/market` against
the dev server of the feature-branch worktree at port 5175, then ran `getComputedStyle` in the page. The scratch copy and the server were deleted afterwards; nothing was
committed except this record.

| element | property | computed value |
|---|---|---|
| `aside a[aria-current="page"]` label span (text "Market Overview") | `border-bottom-color` | `rgb(95, 59, 227)` |
| the same span | `border-bottom-width` | `2px` |
| the sidebar section eyebrow span | `border-bottom-color` | `rgb(95, 59, 227)` |
| `body` | `background-color` | `rgb(234, 234, 247)` |

The underline sits on the label span inside the link (the board's `.nav-on span{border-bottom:2px solid #5F3BE3}`), so the link element itself reads `0px` and the
span carries the colour; that is the fixture's own structure.

**Limits, stated:** the render was the auth-stub, no-fixtures state (panels show their error state; the sidebar is the same component in a live signed-in render). A
click meant to expand the sidebar did not visibly take in that run, so the screenshot shows the collapsed rail; the read targets elements that exist in the markup in
both states and their computed colour does not depend on the rail's width. The first live walk (`tmp/ui-walk/20261015T063315Z`, before `RV-r-3`) and the CVO's grade
`RB1S-AC3` NOT MET are the "before"; the round-2 live walk is the "after" with the expanded sidebar.
