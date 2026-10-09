# DSGN_AMGTV1 -- signed-in /security-analysis walk on portal DEV 0008ddd3 (2.0.0_SA_COO~D1, 2026-10-09 03:20Z)

The FREE work of an empty drive tick (`/next-calls DSGN_AMGTV1 --drive`, keep-driving ON) is input for the round-56 analysis. Walk
`tmp/ui-walk/20261009T032032Z` (gitignored; screenshots stay local): `--route /security-analysis --security "Advanced Micro Devices"
--security "Boeing"` on the local `dev:live` build. 17 steps, 0 guard aborts. The walker armed and disarmed itself cleanly (its
no-delete fix has reached dell1).

## Findings, in words

1. **A typed name pressed with Enter loads nothing, and the error blames the feed.** For each `--security`, the walker found no price-bar row
   printing the exact name, so it typed the name into "Search any ticker" and pressed Enter. The page then requested
   `/api/scoped/amgt/security/<typed text>/{thesis,overlay,peers}` with the raw text ("Advanced%20Micro%20Devices", "Boeing"). All
   48 requests answered 404. The page drew "The identity header could not be loaded" and "Thesis could not be loaded. Try again; if it
   keeps failing, the feed is down." The feed is not down; the typed text is not a security key. A person typing a company name meets
   the same thing. NOT measured: whether the search box offers a pick list that a person would choose from before pressing Enter.
2. **Timeline:** `timeline:no-day-bar` and `timeline:no-event-element` on both names. These are likely downstream of finding 1, since
   nothing loaded. This is not evidence against the timeline itself.
3. **Lead panel, Trending x Chatter:** `walker:control-missing` -- no "Earlier month" control was found to press.
4. **Lead panel, Trending x Price:** `layout:truncated` -- 2 truncated labels.
5. Console: 48 x 404 (finding 1), 4 duplicate `createRoot` warnings and 2 x 401 at the sign-in probe (noted at round 55 as not page defects).

## Re-walk on loaded data -- 03:24Z, `tmp/ui-walk/20261009T032433Z`

`--security "Advanced Micro Devices Inc"`, the name as the price bar prints it: the row was clicked, and every tab loaded. 29 steps,
0 API issues; 6 console errors (sign-in probe and `createRoot`); the walker disarmed cleanly. 8 findings:

| check | where | observed |
|---|---|---|
| `format:money` | 23 steps, from Thesis-expanded on | money written both as "USD 1,234" and "$1,234" on one page |
| `layout:clipped` | 26 steps, from the overlay on | 1 text element cut off sideways by its container |
| `format:dates` | 8 Model steps (version picks Oct 6 -> Oct 3) | "2026-09-22" beside "September 22nd, 2026" |
| `design:contrast` | the timeline day | 3 text elements under 3:1 |
| `timeline:no-event-element` | AMD timeline | no `[data-timeline-event]` element (no event layer built, or none served) |
| `walker:control-missing` | lead Trending x Chatter | no "Earlier month" control |
| `layout:truncated` | lead Trending x Price | 2 truncated labels |
| `thread:name-not-found` | the walker | a WALKER artifact: the row's text carries the move ("Advanced Micro Devices Inc +27.7%"), so `--thread`'s exact-name match fails; the `--security` click succeeds |

Finding 1 above (typed text + Enter -> 404 -> "the feed is down") stands beside these. These are evidence for the CTO's round-56 analysis.
They are not cells: the enrichment list is the CTO's.
