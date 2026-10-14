# CN-i-2 repair: the issuer's real run (2.0.0_SA_COO~D1, 2026-10-14 ~19:3xZ)

**Build read:** `bun run dev:live --port 5174` from a portal worktree on `cand/dell1/mdpf-canon-aua-trend-groups-repair`, head **fd5433a3a76cb8b2f05b986220b70925a9f12ed3** (PROD `fa10e758` plus the three feature commits, each an identical patch to
`4f100451`, `34cd12d2` and `71ed7393`). Before the walk the server's own source was read: `trendGrouping.ts` and `CategoryViewTree.tsx` carry the repair (`presentTrendEntries`, `trendDetailNote`, `lime500`). An earlier walk of 19:27Z read ANOTHER seat's dev server on the same port
(an older tree) and is not evidence; it was not read. Walker: `/ui-walk` as the dormant UI walker, Global (All), Trend pressed; disarmed afterwards (a login with the walk password refused). Screenshots are local only (`tmp/ui-walk/20261014T193640Z`, gitignored; never committed).

## Seen (LOOKED at the screenshots)

- **The note is on the face**, under the Trend subtitle: "Per-model detail begins May 15, 2026; earlier model assets are in the Total and are not broken out." (the boundary is read from the served object's `meta.by_model_fold.per_model_detail_begins`).
- **No band for the earlier dates:** before about 2026-05-19 the period-end bars and the daily area show only the grey Other AUA, as in the candidate the CVO graded; nothing is drawn for the withheld model dollars (the CTO's ruling, PRD v2.18).
- **Client Unsupervised is lime**, no longer the Ultra-Short Term orange: legend and the Client breakdown both show it green; the five model colours are untouched (Ultra Short-Term orange, Short-Term amber, Intermediate-Term green, Long-Term blue, Ultra Long-Term red).
- **The Total Assets breakdown repaints with it.** The Client drill-down (opened by the walk) shows `Client - Opal Unsupervised` as a lime dot and a lime bar. This is the shared colour table; there is no Trend-only override. The fresh approval row names it.

## NOT exercised

- **The tooltip fix was not rendered.** The walker's hover step ran on the Snapshot view before Trend was pressed, so no Trend tooltip was drawn; the fix is graded only by its pure helper and the build arm (`r8_cn_i_2.py build`, 13 of 13 at the worker's commit). The CVO's tooltip clause (dates C and D) still wants a hover on the Trend daily chart.
- Per-firm scopes (the per-firm objects carry no fold meta, so no note is drawn there by design); the Client chips' dated history on dates A to E.

## Observed, not caused by this repair, not examined

The Client drill-down's header reads $341.10M while the Client card on the page reads $292.26M, and the two lines in the drill-down sum to $341.09M. The repair touches only a colour on that surface. Recorded as an observation for the CVO; no row filed.
