# DSGN_AMGTV1 -- ROUND 16 CLOSE RECORD -- `2.0.0_SA_COO~D`, 2026-10-01 ~09:2xZ

**Issuance:** @21dcef217b, decomposition v16, 5 orders in 3 chains (cap 3); amendment @8b8ca27187 (g-3 instrument.cjs arm 3; g-4
write surface).
**Portal:** site-Z DEV 209678ff/eeb8ce3d (AMGT_CORPUS) -> e8a20ba9 (~59) -> a72e1923 (~60) -> **03311745** (~61). LOCAL.
**CLOUD:** 679a76c52a (~59), e1bc5158f0 (~60), **5e7c4f0f4f** (~61). Every merge read dropped 0, foreign 0. LOCAL.

## 1. Orders -- 5 of 5 terminal, every proof instance VALID (issuer re-run with exit codes before each drain)

| order | slot | commit(s) | check(s) |
|---|---|---|---|
| AV-g-1 walker lease + Friday walker steps | ~59 | outer e41e28e641 | walkerlease 3/3, walksteps 3/3 |
| AV-g-5 no "Lead Panel"; name header card | ~59 | portal c6f3709a, outer 786b54d293 | nolabel 3/3 |
| AV-g-2 header chrome C1/C3 | ~60 | portal 0073f22b, outer eb5128f701 | headerchrome 3/3 (575 s; cards 318 x4 at 1440) |
| AV-g-4 unserved chatter face designed | ~60 | portal 6d7b1422, outer c08a558653 | unavailable 3/3 |
| AV-g-3 render instrument sees the demo faces | ~61 | portal 3efc3e4f, outer 5548e6e677 | instrument 3/3 (32 bars, 18 bubbles, 18 of 95) |

On the final DEV 03311745: tsc -b rc=0; 14 of 14 page harnesses; unavailable, nolabel, bubbles, pricebars, panelhead, cardface,
headerread, packwords 3 of 3. headerchrome / instrument on the final DEV (`/c/tmp/cood-r16-close.log`): **instrument 3 of 3** (09:27Z); **headerchrome 2 of 3** (09:22Z) -- arm 1 fails only on `lowContrastChars` in the Security states (the identity card's "BA US", section 2; sizes and the four-card layout PASS) -- the cross-chain interaction of AV-g-2 and AV-g-5, round-17 input 1.

## 2. The one real run

- **Signed-in walk** `tmp/ui-walk/20261001T090446Z` on 5174 (= DEV 03311745 via CTO~Z's 8c78daa2), the NEW leased walker (holder
  `Opal_Bloomberg:27464:81a14d24`), ARM and DISARMED posted to 0.0.0_AB_MSTR~Z; armed 09:04:48Z, logged in 09:05:07Z, **walk void: no**,
  138 shots, disarm 09:10:03Z proven (login after disarm REFUSED 401; status disabled, armedBy none, SSM ABSENT). Against the LIVE
  AMGT_RESAPP routes (af-2 / ag-1 deployed 08:20:58Z).
  - **Chatter face LIVE** (`002-lead-Trending-Chatter.png`): September 2026, 9 bubbles sized by collected (BA_US_Equity 20, COST 9,
    LENOVO 6, ...), "9 of 95 covered names have collected articles this period", the month cursor (Earlier / Later month), the
    caption and source line. Display names: raw keys on some rows (AMGT_RESAPP row Z-S331, their round 58 cell 1).
  - **Header** (`005-BA-US-overlay.png`): the identity card in the card family; four equal header cards, 11px eyebrows, no overlap;
    readings "Breakout (price) #28 | -7.80%" and served dates ("Readings of September 30th, 2026 and September 29th, 2026 (1 trading
    day behind the day asked for)").
  - **Tabs:** "Pick a name above to open its Thesis." -- no "Lead Panel".
  - **The walker walked the Friday faces:** 0 `walker:control-missing` (round 15: 4); the chatter cursor step captured.
  - **OPEN -- the price face:** `004-lead-Trending-Price.png` shows the loading skeleton and "Source: no ranking has been read";
    lead-lists.json reads 0 bars; the price ranking route answered 200 four times (netlog 346, 513, 722, 920) and the header reads its
    price ranking. The walker settles 1.5 s after the click and never waits for `[data-price-bar]` (walk.mjs:268); the face's read asks
    `limit=500`. A capture race is likely but NOT proven -- round-17 input 2.
  - Findings 14: design:contrast x8, tinted-status x2, timeline:no-event-element x2, format:money x1, timeline:no-day-bar x1.
- **The render run** (`node scripts/ui-contract-check.mjs --dist C:/tmp/dsgn-r16-dist/final --out C:/tmp/dsgn-r16-close-render
  --states-sweep`, the new instrument, DEV 03311745): **PASS 69, FAIL 6, NOT_EXERCISED 1, N/A 1 -- RESULT FAIL** (round 15: FAIL 16).
  - `lowContrastChars` 5 in each of the five Security states: read on `thesis.png` -- the identity card's name "BA US" (5 characters)
    in white on the card's navy panel, which has no solid background colour (AV-g-2 gave HeaderCards and LeadPanel one; AV-g-5's
    identity card, a separate chain, did not get it). A cross-chain interaction: round-17 input 1.
  - `model.fwd15_modelTable` NOT_EXERCISED: "no ABSENT row and no footnote in the rendered table" after AMGT_CORPUS's ModelTab change
    (its file through the freeze) -- routed, not DSGN's.
  - `run.harnesses.posture` FAIL: reads S3 live, unstable (excluded from every bound).
  - `sizes` PASS in all states; fwd18, band, fwd19 PASS; price and chatter faces captured from the fixtures.

## 3. Rows this round
- Z-W61-S1 OBSERVATION, INERT (the proof-instance model folder named by the issuer did not exist on that branch).
- AMGT_RESAPP-Z-W200-S1 answered by the issuer's ruling (pillars wording kept).
