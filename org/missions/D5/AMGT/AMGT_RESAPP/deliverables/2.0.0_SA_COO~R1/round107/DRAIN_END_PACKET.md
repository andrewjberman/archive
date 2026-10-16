# AMGT_RESAPP round 107 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FILLED, 2026-10-16 ~00:5xZ; all six orders terminal. AC6 of `AMGT-bn-4` (the walk's screenshot read, which carries round 106's `bm-5` AC5 changes 2 and 3) awaits the CVO's grade.** Round 107 is the CTO's round-106 analysis (`ledger/ROUND_ANALYSIS.round106.md`), issued at `9234de7c19` under this seat's keys (`bn-1`, `bn-2`, `bn-3`, `bn-4`, `bn-5`; `bn-6` was cut later on the CTO's ruling `CTO_RULING_G4_CUT_BN6_20261015.md` @842cf564f3).
`~R2`'s AIFILL workstream is NOT in this packet. All commits named here are LOCAL on `box/dell1` until box-sync carries them, except `077b203366` (on origin/CLOUD).

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-bn-1` | one Opal-internal portal feature: a team-filled Key Figures P/E cell in a withheld column prints a visible research team estimate mark | complete @e1232e9919, merged @5c8e9cd79a | worker ~471 (two passes, two amendments: a live PBR fixture, and a short-named instance because the canonical path was past MAX_PATH); candidate `cand/dell1/amgt-sa-team-estimate-mark` @bb56c53d; harness 12 of 12; approval row a333 ruled by the CTO (`CTO_APPROVAL_A333_TEAM_ESTIMATE_MARK_20261015.md`); a duplicate approval row 5663 was withdrawn (`WITHDRAWN_DUPLICATE_APPROVAL_ROW_5663_20261015.md`); rows W471-S1..S5 |
| `AMGT-bn-2` | the UI walker opens a named disclosure first so the All-figures grid is reached | complete, merged @21a23e0a80 | worker ~472; `--open-first "All figures"`; row W472-S1 |
| `AMGT-bn-3` | the promote of that one feature to PROD (SERVED) | complete @66ae679a7d | `0.4.0_DT_ClientPlatform~H1`; release/20261015T223053Z, PROD `e0e69da7766d` (portal-v2.1.227), CI success, ledger CLOSED; AC1 5 of 5 blobs EQUAL, AC3 receipt count 6 |
| `AMGT-bn-4` | the fresh-draw walk (ten drawn plus SHOP CN and PBR US) with the All-figures grid open on a local build of PROD | complete @5cbfaa2e06, merged @d91c1619a7 | worker ~474, instance VALID rc=0; four walks A to D, each 3 of 3 `OPEN-FIRST "All figures": opened` (122 to 193 rows), `OK: DISARMED`, post-disarm login HTTP 401 REFUSED, `walk void: no`; build = PROD `e0e69da7`, port 5174 (now free); shots outside the repository at `C:/dev/ui-walk-evidence/bn-4/{A,B,C,D}/`; **AC6 is JUDGMENT** (yours); worker row W474-S1 |
| `AMGT-bn-5` | A4's price-pull window is held as data (steps 30, 90, 365; step 0 now) | complete, merged @077b203366 (on origin/CLOUD) | worker ~473; `price_axis_window.json` + `price_axis_pull.py`; 18 tests; the apply (step 0 to 1) is a separate pair, COO half signed @ae5b80ec40, CTO half signed |
| `AMGT-bn-6` | G4's code half: `lib/research/llm_batch`, three batch tasks registrable DISABLED behind an event trigger | complete @283eea91d5, merged @ed81a198e3 | worker ~475; 19 tests; `register --plan` prints three TASK lines each `ENABLED=false`, `OWNER=2.0.0_SA_COO~R1`, `PLAN: 3 task(s), 0 created`; NOTHING registered or enabled; rows W475-S1..S4 |

## 2. The issuer's real runs

- **Walk draw for 2026-10-16** (`round107/walk_draw_20261016.json`, fresh against round 106's draw): ZURN SW, ML FP, 939 HK, ICT PM, 1299 HK, IDXX US, OMAB MM, COST US, NOVN SW, CLX US, plus SHOP CN and PBR US named by the order. Five of the ten are withheld names (ZURN SW, 939 HK, ICT PM, 1299 HK, NOVN SW).
- **Served body, read live by the issuer (read-only):** four of the five withheld drawn names (ZURN SW, 939 HK, ICT PM, 1299 HK) carry `forecast_withheld` for 2026 to 2028, no vendor P/E rows and no team P/E row. NOVN SW has a team P/E.
- **Mechanics re-read from the walk files by the issuer:** walker account `armed=no`, port 5174 free, build task stopped.

## 3. WHAT THE READINGS SAY

**The issuer's own reads (Read tool):**
- **ZURN SW** (`A/20261016T000245Z/shots/012-ZURN-SW-Model.png`): Key Figures has NO P/E row, so the withhold reason prints nowhere on Key Figures. The What Changed table prints vendor P/E ratios (14.9x to 15.1x) under the label "a line this page has no name for yet". Two grid crops (`ZURN_model_05.png`, `_06.png`): the grid is open with many rows; team-template rows carry the footer "The research team keeps no workbook for this company; this row is from the team's template".
- **SHOP CN** (`D/20261016T001622Z/shots/039-SHOP-CN-Model.png`): the Key Figures P/E row prints 74x-193.1x, 67.8x and 53.0x, each under "research team estimate": the mark shows on the team-filled cells (round 106 change 3 as the CTO read it).
- **The four withheld names with no team P/E** (ZURN SW, 939 HK, ICT PM, 1299 HK): no P/E row on Key Figures, so no cell to carry the mark or a reason. Filed as `D1-S35` (mine) and `W474-S1` (the worker's, same finding).
- **Change 3 shows** on SHOP CN, NOVN SW and PBR US (2026E and 2027E marked; the 2025 range is unmarked by the CTO's ruling). Change 2 (a grid dash states its reason) reads as built on the two grid crops the issuer read; the worker read grid rows in detail on ZURN SW and 939 HK only.

**Not verified by the issuer:** the worker's Model, Exec and overlay reads of the other names (`session_log.txt`, `nonzero_steps.txt`, 139 lines); a pointer from the worker that the overlay EV prints in dollars (`$31.68B`, `$110B`, `$335B`) on PHP, HKD and CHF listings while the Model block says Figures in USD. The walker's `STEP` findings are pointers, not verdicts.

I propose no verdict on AC6.

## 4. Open and carried

- **A4 step 1** (30 to 90 days): both pair halves are signed and the code is at step 0. H1 measured A2's first day at site Z as Fri 2026-10-16 (07:00 ET pull on line 62, msg 6370); under the two-trading-day rule the step lands Tue 2026-10-20 at the earliest, once H1 reads Friday's manifest and site Z's day-0 read is relayed. Step 2 (365 days) waits on the CTO's read of a measured 90-day window.
- **G4 enable** is a separate never-widen pair (not this round's cell): a measured one-key Anthropic cost, the population count, the first fire's figure and a stop at 1.5 times it. The first fire is due by rule (b) over the whole population. Drafting and posture have no whole-population entry (W475-S3): a round-108 cell after the three tasks run once.
- **Candidates for the CTO's round-107 analysis:** a Key Figures reason line for a withheld name with no P/E row (`D1-S35`); a name for the What Changed line that prints withheld vendor ratios; the overlay EV currency pointer.
- Evidence outside the repository: `C:/dev/ui-walk-evidence/bn-4/`. Left on disk: `C:/dev/wk-resapp-418` and its leftovers, the two stale build worktrees `C:/tmp/aa5-build` and `C:/tmp/bd2-build` (a recursive delete is Andrew-class, not done).
