# DSGN_AMGTV1 round 57 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~04:3xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round56.md` -> `AV-zzi-1` (R1b) + `AV-zzi-2` (R3 + R5, repairs batched). R1(a) -> the RESAPP route resolves names (CTO ruling @a9fc745d69; addendum @9e03417c14, RESAPP round 81). R6 withdrawn (AV-zi-1 kept). R2, R4 = walker false positives (decomposition v57) |
| orders | `TO-AV-zzi-1` -> `~121` (worker), merged @236a33509f; `TO-AV-zzi-2` -> `~122` (worker-light), merged @2bd3fe1068. Both instances VALID; rows minted: 0; no harness re-anchored |
| portal candidate | `2d42e9b7` = DEV `fd345aef` + 2 (`19a172da` AV-zzi-1, `2d42e9b7` AV-zzi-2), branch `cand/dsgn-amgtv1-r57` (dell1 portal repo, LOCAL). DEV moved from `0008ddd3` to `fd345aef` mid-round (other projects; no `SecurityAnalysis/` file), so the two worker commits were replayed onto it without conflict |
| drain on `2d42e9b7` | r57a 4 of 4; r57b 4 of 4; battery29 ALL PASS (14 of 14 harnesses, tsc rc=0, eslint rc=0); `notFound.test.tsx` 2 pass, 0 fail |
| round-close-check | `verdict=MAY-CLOSE` (2 of 2 complete) |

## The one real run -- 2026-10-09 04:18Z (on `a6b75e25`, the same two commits on `0008ddd3`)

- Signed-in `/ui-walk --route /security-analysis --security "Boeing" --security "Advanced Micro Devices Inc"`, local `dev:live` build. Walk
  `tmp/ui-walk/20261009T041800Z` (gitignored; screenshots stay local). 36 screenshots; the walker armed and disarmed itself cleanly.
- **Typed "Boeing" + Enter:** the page draws one panel, `No security found for "Boeing".`, with a "Back to all names" button. It has no
  overlay, no tabs and no "the feed is down". The 404s fell from 48 to 6: overlay and thesis, three each with the hooks' two retries.
  The walker's 6 `walker:control-missing` are the five tabs and the timeline, which are absent by design on a not-found.
- **"Advanced Micro Devices Inc" (the printed name):** every tab loads, with 0 API issues for AMD. The same walker classes as round 56
  stand (money in quoted headlines, the HeroDialog header contrast, an empty chart `tspan`), already ruled false positives.
- The walk ran on `a6b75e25`. The candidate sent for review, `2d42e9b7`, carries the same two commits replayed onto the newer DEV, with
  no `SecurityAnalysis/` difference between the bases.

## Carried to round 58

- RESAPP round-80 analysis R4 (msg 1684): the "no segment breakdown is shown" sentence must not appear beside a drawn segment table.
- After RESAPP round 81 lands (msg 1676): the not-found panel reads the route's own answer, including its "several companies match" list,
  and adds no lookup of its own.
