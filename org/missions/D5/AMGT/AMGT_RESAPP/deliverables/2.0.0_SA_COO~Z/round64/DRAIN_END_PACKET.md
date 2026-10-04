# AMGT_RESAPP round 64 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-03 ~02:1xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.72 + 72f. **Issuance:** `59aabebf87`. **AMENDMENT 1:** `13dc3f05ba`; its first part rode
2.0.0_SA_COO~D's drain `55546c9c3e` by a shared-index race, confirmed with COO~D.
**Input:**
- PRD v0.34/v0.35 (FWD-36, 37, 38). FWD-36's price half is a QUALIFIED WAIT, and FWD-37's earnings path is one too.
- The CTO's round-63 analysis `8642d76ceb`: cold read, slash keys, 500 attribution, officer face, as_of stamp.
- CTO msgs 28690, 28740, 28730, 28824, 28866.

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `an-1` FWD-36 rolling windows (+ the trending repair) | LOCAL | ~210; issuer direct act | complete | drained `37da943651`; direct act `43711514cc` (TRENDING/price `?days`, COO~D msg 28857); c9 YES, c10 YES 8 of 8 |
| `an-2` FWD-37 timeline markers | LOCAL | ~211 | complete | drained `f43c05b00e`; c11 YES 3 of 3 |
| `an-3` FWD-38 a + b: feed + one display name | LOCAL | ~212 | complete | drained `6892710005`; c12 YES (feed 71/13/3 = day view; one name x 3) |
| `an-4` FWD-38 c + d: move labels + provenance | LOCAL | ~213 | complete | drained `40e52072ce`; c13 YES (94 of 94 labelled; provenance x 3) |
| `an-5` the cold read | LOCAL | ~214 | complete | drained `f5a29aef96`; local cold 3.5-3.9 s -> 2.2-2.9 s, body byte-identical |
| `an-6` repairs (slash keys, officer face, source stamp, 500 attribution) | LOCAL | ~215 | complete | drained `130c3be101`; c14 YES; c16 YES |
| `an-7` the redeploy (legs 1 + 2) | WORLD | `0.7.0_AE_CloudOps~A` | complete | leg 1 `bf4b04b120` (`kSeyeO0v`), leg 2 `9b94636a21` (`KQSA62c3`); 2 pairs signed (CTO `e1c310a414`, `5e62e3e420`) |

**Drain repairs:**
- `949b24cadb`: 3 harvest/tests pinned the silver day path that round-63 am-1 removed. It was a round-63 regression, unseen by an api-only union.
- `d510a04e6f`: an-3's gold fake vs an-5's seam.
- The union across peers, management, api, harvest and coverage: 1012 passed.

## The real run on the DEPLOYED function (CodeSha256 `KQSA62c3...`, 1769 MB)

| check | result | detail |
|---|---|---|
| c9 (FWD-36 chatter) | YES | default/30/90/365; the 365-day window reads the store start 2026-01-01 with its note; tone null + tone_reason (HARVST held) |
| c10 (FWD-36 price) | YES | trending + breakout: 30 = 94 rows; 90/365 = 0 rows, "not produced yet" (qualified wait) |
| c11 (FWD-37) | YES | coverage markers from gold events; earnings absent with "no earnings dates are pulled yet" (qualified wait) |
| c12 (FWD-38 a, b) | YES | the feed holds every day-view article; one cased display name per security; items serve url null |
| c13 (FWD-38 c, d) | YES | every move names axis + window; provenance names filings, harvested news and Bloomberg with a last run or reason |
| c14 (repairs) | YES | BP Energy (source named); NG null with a true reason; no raw codes; source stamps; the encoded key reaches 4 of 4 routes |
| c15 (cold read) | YES | 3 of 3 COLD at 1.9 / 2.3 / 2.3 s against 5 s, with Init Duration and AMGT_SEGMENT stages (AE~A). Round 63: 11.5-12.8 s |
| c16 (500 attribution) | YES local; deployed by plant | a planted fault on deployed reads back one AMGT_500 line (request id, route, key, AttributeError). Census: 6 of 21,724 in 7 days |
| r63 c3/c4/c5/c7/c8 | YES | unchanged; c8's count moved by design (BP resolved) |

## For the CVO's L8/L9 read

1. **Two QUALIFIED WAITS are served as their interim branches. They are not the paths, and they are not graded as the paths:**
   - FWD-36's 90/365-day price windows wait on Andrew's PX_LAST history-pull word.
   - FWD-37's earnings markers wait on the CORPUS Model-block pull.
2. **FWD-36's tone and voters serve null with a reason.**
3. **The feed's `url` is null.** Gold carries no url. DSGN round 30 renders a plain title (COO~D msg 28803); a url source is a round-65 item.
4. **No round-64 cell processes publisher text.** FinBERT ships in the package, and the import graph
   (proved twice, from both leg artifacts) shows no route reaches it.

## Rows (all OBSERVATION, INERT)

- `Z-W211-S1` and `Z-W214-S1`: the pre-existing harvest test failures, repaired at `949b24cadb`.
- `Z-W214-S2`: identity resolution is the largest remaining cold stage.
- `Z-W212-S1`: an all-caps model-block name fallback is not re-cased.
- `Z-W212-S2`: url null, routed as above.
- `Z-W215-S1`: the worker branch held the pre-amendment check, re-graded on the shared tree.
- `Z-S339`: the slash-ticker classification, resolved by an-6.

`Z-W205-S1` and `Z-W208-S2` are adjudicated in your v75.
